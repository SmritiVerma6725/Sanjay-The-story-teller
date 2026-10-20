// SignBridge — Offscreen Audio Processor (Milestone M2)
//
// Responsibilities:
// 1. Consume tab capture streamId via navigator.mediaDevices.getUserMedia.
// 2. Preserve audible playback: route mediaStreamSource to AudioContext.destination.
// 3. Segment audio in memory into 2.0s 16kHz 16-bit mono PCM WAV slices.
// 4. Forward slices via bounded FIFO queue (max 3) to local Python backend (127.0.0.1:8765).
// 5. Enforce 8.0s timeout per request with zero cloud leakage and bounded memory.

(() => {
  "use strict";

  const BACKEND_TRANSCRIBE_URL = "http://127.0.0.1:8765/api/transcribe";
  const TARGET_SAMPLE_RATE = 16000;
  const CHUNK_DURATION_SEC = 2.0;
  const MAX_QUEUE_SIZE = 3;
  const REQUEST_TIMEOUT_MS = 8000;

  let mediaStream = null;
  let audioContext = null;
  let mediaSourceNode = null;
  let scriptProcessorNode = null;
  let muteGainNode = null;

  let chunkCount = 0;
  let totalBytes = 0;
  let sequenceIdCounter = 0;
  let captureStartTime = null;
  let selectedLanguage = "en";

  // Audio buffer state
  let sampleBuffer = [];
  let accumulatedSampleCount = 0;

  // Queue state
  const transcriptionQueue = [];
  let isProcessingQueue = false;

  // ---------------------------------------------------------------------------
  // WAV Encoder & Downsampler (100% Vanilla In-Memory PCM)
  // ---------------------------------------------------------------------------

  function downsampleBuffer(buffers, inputSampleRate, targetRate) {
    let totalLen = 0;
    for (let i = 0; i < buffers.length; i++) {
      totalLen += buffers[i].length;
    }
    const merged = new Float32Array(totalLen);
    let offset = 0;
    for (let i = 0; i < buffers.length; i++) {
      merged.set(buffers[i], offset);
      offset += buffers[i].length;
    }

    if (inputSampleRate === targetRate) {
      return merged;
    }

    const ratio = inputSampleRate / targetRate;
    const newLen = Math.round(totalLen / ratio);
    const result = new Float32Array(newLen);

    for (let i = 0; i < newLen; i++) {
      const origPos = i * ratio;
      const lower = Math.floor(origPos);
      const upper = Math.min(lower + 1, totalLen - 1);
      const frac = origPos - lower;
      result[i] = merged[lower] * (1 - frac) + merged[upper] * frac;
    }

    return result;
  }

  function writeAsciiString(view, offset, string) {
    for (let i = 0; i < string.length; i++) {
      view.setUint8(offset + i, string.charCodeAt(i));
    }
  }

  function encodeWavBlob(samples, sampleRate) {
    const buffer = new ArrayBuffer(44 + samples.length * 2);
    const view = new DataView(buffer);

    // RIFF chunk descriptor
    writeAsciiString(view, 0, "RIFF");
    view.setUint32(4, 36 + samples.length * 2, true);
    writeAsciiString(view, 8, "WAVE");

    // "fmt " sub-chunk
    writeAsciiString(view, 12, "fmt ");
    view.setUint32(16, 16, true);          // SubChunk1Size (16 for PCM)
    view.setUint16(20, 1, true);           // AudioFormat (1 for Linear PCM)
    view.setUint16(22, 1, true);           // NumChannels (1 for Mono)
    view.setUint32(24, sampleRate, true);  // SampleRate (16000)
    view.setUint32(28, sampleRate * 2, true); // ByteRate (SampleRate * Channels * BitsPerSample/8)
    view.setUint16(32, 2, true);           // BlockAlign (Channels * BitsPerSample/8)
    view.setUint16(34, 16, true);          // BitsPerSample (16-bit)

    // "data" sub-chunk
    writeAsciiString(view, 36, "data");
    view.setUint32(40, samples.length * 2, true);

    // Write 16-bit signed PCM samples with clamping
    let offset = 44;
    for (let i = 0; i < samples.length; i++, offset += 2) {
      const s = Math.max(-1, Math.min(1, samples[i]));
      view.setInt16(offset, s < 0 ? s * 0x8000 : s * 0x7FFF, true);
    }

    return new Blob([buffer], { type: "audio/wav" });
  }

  // ---------------------------------------------------------------------------
  // Bounded Transcription Queue
  // ---------------------------------------------------------------------------

  async function processTranscriptionQueue() {
    if (isProcessingQueue) return;
    isProcessingQueue = true;

    while (transcriptionQueue.length > 0) {
      const item = transcriptionQueue.shift();
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), REQUEST_TIMEOUT_MS);

      try {
        const formData = new FormData();
        formData.append("audio", item.blob, `chunk_${item.sequenceId}.wav`);
        formData.append("sequence_id", item.sequenceId.toString());
        formData.append("timestamp", item.timestamp.toFixed(2));
        if (selectedLanguage && selectedLanguage !== "auto") {
          formData.append("language", selectedLanguage);
        }

        console.info(`[SignBridge Diagnostics] Sending chunk #${item.sequenceId} (${item.blob.size} bytes) to backend: ${BACKEND_TRANSCRIBE_URL}`);
        const t0 = performance.now();
        const response = await fetch(BACKEND_TRANSCRIBE_URL, {
          method: "POST",
          body: formData,
          signal: controller.signal
        });
        const elapsedFetchMs = Math.round(performance.now() - t0);

        clearTimeout(timeoutId);

        if (!response.ok) {
          const errDetail = await response.text().catch(() => "Unknown error");
          console.error(`[SignBridge Diagnostics] Backend HTTP ${response.status} for chunk #${item.sequenceId} (${elapsedFetchMs}ms): ${errDetail}`);
          chrome.runtime.sendMessage({
            type: "TRANSCRIPTION_ERROR",
            sequenceId: item.sequenceId,
            error: `HTTP ${response.status}: ${errDetail}`
          }).catch(() => {});
          continue;
        }

        const data = await response.json();
        console.info(`[SignBridge Diagnostics] Backend HTTP ${response.status} for chunk #${item.sequenceId} (${elapsedFetchMs}ms, infer=${data.metrics?.inference_time_ms}ms, RTF=${data.metrics?.rtf}). Response text: "${data.text}"`);

        // Forward recognized speech to background service worker
        chrome.runtime.sendMessage({
          type: "TRANSCRIPTION_RESULT",
          sequenceId: data.sequence_id,
          timestamp: data.timestamp,
          duration: data.duration,
          text: data.text,
          language: data.language,
          languageProbability: data.language_probability,
          segments: data.segments || [],
          metrics: data.metrics || {}
        }).catch(() => {});

      } catch (err) {
        clearTimeout(timeoutId);
        const errMsg = err.name === "AbortError" ? "Request timed out (>8s)" : (err.message || "Backend offline");
        console.error(`[SignBridge Diagnostics] Failed to transcribe chunk #${item.sequenceId}:`, errMsg);
        chrome.runtime.sendMessage({
          type: "TRANSCRIPTION_ERROR",
          sequenceId: item.sequenceId,
          error: errMsg
        }).catch(() => {});
      }
    }

    isProcessingQueue = false;
  }

  function enqueueAudioSlice(blob, seqId, timestamp, duration) {
    if (transcriptionQueue.length >= MAX_QUEUE_SIZE) {
      const dropped = transcriptionQueue.shift();
      console.warn(`[SignBridge Diagnostics] Transcription queue full (limit=${MAX_QUEUE_SIZE}). Dropping oldest chunk #${dropped.sequenceId}`);
      chrome.runtime.sendMessage({
        type: "QUEUE_OVERFLOW",
        droppedSequenceId: dropped.sequenceId
      }).catch(() => {});
    }

    transcriptionQueue.push({
      blob,
      sequenceId: seqId,
      timestamp,
      duration
    });

    processTranscriptionQueue();
  }

  // ---------------------------------------------------------------------------
  // Capture Lifecycle Management
  // ---------------------------------------------------------------------------

  async function startCapture(streamId, language = "en") {
    console.info("[SignBridge Diagnostics] Offscreen startCapture called.");
    await stopCapture();
    selectedLanguage = language || "en";

    try {
      console.info("[SignBridge Diagnostics] Requesting getUserMedia for tab audio capture...");
      // 1. Acquire tab audio stream
      mediaStream = await navigator.mediaDevices.getUserMedia({
        audio: {
          mandatory: {
            chromeMediaSource: "tab",
            chromeMediaSourceId: streamId
          }
        },
        video: false
      });
      console.info("[SignBridge Diagnostics] getUserMedia: SUCCESS. Audio tracks found:", mediaStream.getAudioTracks().length);

      captureStartTime = Date.now();
      chunkCount = 0;
      totalBytes = 0;
      sequenceIdCounter = 0;
      sampleBuffer = [];
      accumulatedSampleCount = 0;
      transcriptionQueue.length = 0;

      // Handle stream track termination
      const audioTrack = mediaStream.getAudioTracks()[0];
      if (audioTrack) {
        audioTrack.onended = () => {
          console.info("[SignBridge Diagnostics] Audio track ended by browser/tab.");
          chrome.runtime.sendMessage({
            type: "CAPTURE_TRACK_ENDED",
            reason: "Tab closed or navigation occurred"
          }).catch(() => {});
          stopCapture();
        };
      }

      // 2. Playback Preservation via Web Audio API:
      // Connecting mediaSourceNode to audioContext.destination routes audio to speakers/headphones.
      audioContext = new AudioContext();
      if (audioContext.state === "suspended") {
        await audioContext.resume();
      }
      console.info(`[SignBridge Diagnostics] AudioContext initialized. State: ${audioContext.state}, Context SampleRate: ${audioContext.sampleRate}Hz`);

      mediaSourceNode = audioContext.createMediaStreamSource(mediaStream);
      mediaSourceNode.connect(audioContext.destination);
      console.info("[SignBridge Diagnostics] Audible playback preserved (mediaSource routed to audioContext.destination).");

      // 3. Audio Slicing & Downsampling (16kHz PCM WAV in memory):
      const bufferSize = 4096;
      scriptProcessorNode = audioContext.createScriptProcessor(bufferSize, 1, 1);
      muteGainNode = audioContext.createGain();
      muteGainNode.gain.value = 0; // Mute duplicate branch

      mediaSourceNode.connect(scriptProcessorNode);
      scriptProcessorNode.connect(muteGainNode);
      muteGainNode.connect(audioContext.destination);

      const samplesPerChunk = Math.floor(audioContext.sampleRate * CHUNK_DURATION_SEC);
      console.info(`[SignBridge Diagnostics] Audio recorder started. Slicing every ${CHUNK_DURATION_SEC}s (${samplesPerChunk} samples at context rate) -> Target rate: ${TARGET_SAMPLE_RATE}Hz mono PCM.`);

      scriptProcessorNode.onaudioprocess = (event) => {
        const inputData = event.inputBuffer.getChannelData(0);
        // Clone input data into sampleBuffer
        sampleBuffer.push(new Float32Array(inputData));
        accumulatedSampleCount += inputData.length;

        if (accumulatedSampleCount >= samplesPerChunk) {
          chunkCount++;
          sequenceIdCounter++;

          const timestamp = (sequenceIdCounter - 1) * CHUNK_DURATION_SEC;
          const downsampled = downsampleBuffer(sampleBuffer, audioContext.sampleRate, TARGET_SAMPLE_RATE);
          const wavBlob = encodeWavBlob(downsampled, TARGET_SAMPLE_RATE);

          sampleBuffer = [];
          accumulatedSampleCount = 0;
          totalBytes += wavBlob.size;

          console.info(`[SignBridge Diagnostics] PCM WAV chunk #${sequenceIdCounter} created: ${wavBlob.size} bytes (${CHUNK_DURATION_SEC}s slice at ${TARGET_SAMPLE_RATE}Hz). Total bytes: ${totalBytes}`);

          // Dispatch progress metadata to service worker
          chrome.runtime.sendMessage({
            type: "CAPTURE_PROGRESS",
            chunkCount,
            totalBytes,
            audioState: audioContext ? audioContext.state : "unknown",
            sampleRate: TARGET_SAMPLE_RATE,
            elapsedSeconds: captureStartTime ? Math.round((Date.now() - captureStartTime) / 1000) : 0
          }).catch(() => {});

          // Enqueue for local transcription
          enqueueAudioSlice(wavBlob, sequenceIdCounter, timestamp, CHUNK_DURATION_SEC);
        }
      };

      // 4. Notify service worker of successful start
      chrome.runtime.sendMessage({
        type: "CAPTURE_STARTED",
        sampleRate: TARGET_SAMPLE_RATE,
        audioState: audioContext.state,
        mimeType: "audio/wav"
      }).catch(() => {});
      console.info("[SignBridge Diagnostics] Audio capture fully running and streaming slices.");

    } catch (err) {
      console.error("[SignBridge Diagnostics] getUserMedia: FAILED -", err.name, err.message);
      await stopCapture();
      chrome.runtime.sendMessage({
        type: "CAPTURE_ERROR",
        error: `Audio capture initiation failed: ${err.name} - ${err.message || 'Permission denied'}`
      }).catch(() => {});
    }
  }

  async function stopCapture() {
    console.info("[SignBridge Diagnostics] Audio recorder stopping and cleaning up resources...");
    // Clear processing queue
    const queueCount = transcriptionQueue.length;
    transcriptionQueue.length = 0;
    isProcessingQueue = false;

    // Disconnect Web Audio processor nodes
    if (scriptProcessorNode) {
      try {
        scriptProcessorNode.onaudioprocess = null;
        scriptProcessorNode.disconnect();
      } catch (e) {}
      scriptProcessorNode = null;
    }

    if (muteGainNode) {
      try {
        muteGainNode.disconnect();
      } catch (e) {}
      muteGainNode = null;
    }

    if (mediaSourceNode) {
      try {
        mediaSourceNode.disconnect();
      } catch (e) {}
      mediaSourceNode = null;
    }

    if (audioContext) {
      try {
        if (audioContext.state !== "closed") {
          await audioContext.close();
        }
      } catch (e) {}
      audioContext = null;
    }

    if (mediaStream) {
      try {
        mediaStream.getTracks().forEach((track) => track.stop());
      } catch (e) {}
      mediaStream = null;
    }

    sampleBuffer = [];
    accumulatedSampleCount = 0;
    captureStartTime = null;
    console.info(`[SignBridge Diagnostics] Audio recorder stopped. Resources released (cleared ${queueCount} queued items).`);
  }

  // ---------------------------------------------------------------------------
  // Message Listener
  // ---------------------------------------------------------------------------

  if (typeof chrome !== "undefined" && chrome.runtime && chrome.runtime.onMessage) {
    chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
      if (!message || !message.type) return;

      if (message.type === "START_CAPTURE") {
        startCapture(message.streamId, message.language);
        sendResponse({ status: "initiating" });
        return true;
      }

      if (message.type === "STOP_CAPTURE") {
        stopCapture().then(() => {
          sendResponse({ status: "stopped", chunkCount, totalBytes });
        });
        return true;
      }

      if (message.type === "SET_LANGUAGE") {
        selectedLanguage = message.language || "en";
        sendResponse({ ok: true });
        return true;
      }

      if (message.type === "GET_OFFSCREEN_STATUS") {
        sendResponse({
          isActive: !!mediaStream,
          chunkCount,
          totalBytes,
          queueLength: transcriptionQueue.length,
          audioContextState: audioContext ? audioContext.state : "closed",
          sampleRate: TARGET_SAMPLE_RATE,
          elapsedSeconds: captureStartTime ? Math.round((Date.now() - captureStartTime) / 1000) : 0
        });
        return true;
      }
    });
  }

  console.info("[SignBridge Offscreen] Offscreen document audio processor (M2) initialized.");
})();

