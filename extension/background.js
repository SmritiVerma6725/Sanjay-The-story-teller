// SignBridge — Service Worker (Milestone M1)
//
// Responsibilities:
// 1. Maintain capture state machine in chrome.storage.session.
// 2. Manage the offscreen document lifecycle (single instance).
// 3. Obtain ephemeral tab capture streamId via chrome.tabCapture.getMediaStreamId.
// 4. Monitor tab closure and navigation to guarantee clean resource teardown.
// 5. Expose status to the popup UI and update extension badge indicators.

(() => {
  "use strict";

  const OFFSCREEN_PATH = "offscreen.html";

  // Initial state setup
  async function getSessionState() {
    const data = await chrome.storage.session.get("captureState");
    return data.captureState || {
      status: "idle", // 'idle' | 'starting' | 'capturing' | 'stopping' | 'error'
      tabId: null,
      tabTitle: null,
      tabUrl: null,
      startedAt: null,
      chunkCount: 0,
      totalBytes: 0,
      sampleRate: null,
      errorMessage: null,
      playbackPreserved: true,
      // M2 Speech Recognition State
      latestTranscript: "",
      transcripts: [], // Array of { sequenceId, timestamp, text, words }
      fullTranscript: "",
      backendStatus: "checking", // 'online' | 'offline' | 'checking' | 'error'
      lastInferenceMs: 0,
      lastRtf: 0,
      selectedLanguage: "en",
      // M4 End-to-End Session & Avatar Bridge State
      sessionId: null,
      latestTranscriptEvent: null,
      lastProcessedSequenceId: 0
    };
  }

  async function updateSessionState(patch) {
    const current = await getSessionState();
    const updated = { ...current, ...patch };
    await chrome.storage.session.set({ captureState: updated });
    updateBadge(updated.status);
    return updated;
  }

  function updateBadge(status) {
    if (status === "capturing") {
      chrome.action.setBadgeText({ text: "REC" });
      chrome.action.setBadgeBackgroundColor({ color: "#DC2626" }); // Red
    } else if (status === "starting") {
      chrome.action.setBadgeText({ text: "..." });
      chrome.action.setBadgeBackgroundColor({ color: "#2563EB" }); // Blue
    } else if (status === "error") {
      chrome.action.setBadgeText({ text: "ERR" });
      chrome.action.setBadgeBackgroundColor({ color: "#D97706" }); // Amber
    } else {
      chrome.action.setBadgeText({ text: "" });
    }
  }

  async function hasOffscreenDoc() {
    if ("hasDocument" in chrome.offscreen) {
      return await chrome.offscreen.hasDocument();
    }
    const contexts = await chrome.runtime.getContexts({
      contextTypes: ["OFFSCREEN_DOCUMENT"]
    });
    return contexts && contexts.length > 0;
  }

  async function ensureOffscreenDoc() {
    if (await hasOffscreenDoc()) {
      console.info("[SignBridge Diagnostics] Offscreen document already exists.");
      return;
    }
    console.info("[SignBridge Diagnostics] Creating offscreen document at:", OFFSCREEN_PATH);
    try {
      await chrome.offscreen.createDocument({
        url: OFFSCREEN_PATH,
        reasons: ["USER_MEDIA", "AUDIO_PLAYBACK"],
        justification: "Process active tab audio stream and preserve audible playback"
      });
      console.info("[SignBridge Diagnostics] Offscreen document creation: SUCCESS");
    } catch (err) {
      if (!err.message || !err.message.includes("Only a single offscreen document")) {
        console.error("[SignBridge Diagnostics] Offscreen document creation: FAILED -", err.message || err);
        throw err;
      }
      console.info("[SignBridge Diagnostics] Offscreen document single-instance invariant held.");
    }
  }

  async function closeOffscreenDoc() {
    if (await hasOffscreenDoc()) {
      console.info("[SignBridge Diagnostics] Closing offscreen document...");
      try {
        await chrome.offscreen.closeDocument();
        console.info("[SignBridge Diagnostics] Offscreen document closed successfully.");
      } catch (e) {
        console.warn("[SignBridge Diagnostics] Error closing offscreen document:", e);
      }
    }
  }

  async function sendMessageToOffscreen(message, maxAttempts = 5, delayMs = 150) {
    for (let attempt = 1; attempt <= maxAttempts; attempt++) {
      try {
        return await chrome.runtime.sendMessage(message);
      } catch (err) {
        if (attempt === maxAttempts) throw err;
        await new Promise(r => setTimeout(r, delayMs));
      }
    }
  }

  async function startCapture(tab, preacquiredStreamId = null) {
    const state = await getSessionState();
    console.info("[SignBridge Diagnostics] Background startCapture invoked. Preacquired streamId present:", !!preacquiredStreamId);

    // Guard against duplicate starts or transition states
    if (state.status === "capturing" || state.status === "starting") {
      const err = "Capture is already active or starting.";
      console.warn("[SignBridge Diagnostics] Start capture rejected:", err);
      return { ok: false, error: err };
    }

    if (!tab || !tab.id) {
      const err = "No active tab detected.";
      console.warn("[SignBridge Diagnostics] Start capture rejected:", err);
      return { ok: false, error: err };
    }

    // Validate supported URL
    const url = tab.url || "";
    if (url.startsWith("chrome://") || url.startsWith("chrome-extension://") || url.startsWith("edge://") || url.startsWith("about:")) {
      const err = "Cannot capture Chrome internal pages. Please open a YouTube video.";
      console.warn("[SignBridge Diagnostics] Start capture rejected (internal page):", url);
      await updateSessionState({ status: "error", errorMessage: err });
      return { ok: false, error: err };
    }

    // PRD FR-01: Initial platform is YouTube
    const isYouTube = url.includes("youtube.com/watch") || url.includes("youtube.com/live") || url.includes("youtube.com/shorts");
    if (!isYouTube && url.startsWith("http")) {
      console.warn("[SignBridge Diagnostics] Non-YouTube page detected. Operating under advisory mode.");
    }

    // Retrieve language preference
    const stored = await chrome.storage.local.get("selectedLanguage");
    const lang = stored.selectedLanguage === "ASL" ? "en" : "en"; // Default Whisper transcription is en
    const sessionId = `sb_session_${Date.now()}_${Math.random().toString(36).substring(2, 8)}`;

    await updateSessionState({
      status: "starting",
      sessionId: sessionId,
      lastProcessedSequenceId: 0,
      latestTranscriptEvent: null,
      tabId: tab.id,
      tabTitle: tab.title || "YouTube Video",
      tabUrl: url,
      errorMessage: null,
      chunkCount: 0,
      totalBytes: 0,
      startedAt: Date.now(),
      selectedLanguage: lang
    });

    try {
      // 1. Obtain ephemeral streamId for the target tab (or use pre-acquired streamId from popup gesture)
      let streamId = preacquiredStreamId;
      if (!streamId) {
        console.info("[SignBridge Diagnostics] Requesting stream ID from background tabCapture...");
        streamId = await chrome.tabCapture.getMediaStreamId({
          targetTabId: tab.id
        });
      }

      if (!streamId) {
        console.error("[SignBridge Diagnostics] Stream ID acquisition: FAILED (no stream ID returned)");
        throw new Error("chrome.tabCapture did not return a stream ID.");
      }
      console.info("[SignBridge Diagnostics] Stream ID acquisition: SUCCESS");

      // 2. Ensure offscreen document is ready to receive streamId
      await ensureOffscreenDoc();

      // 3. Delegate getUserMedia to offscreen document with resilient retry
      console.info("[SignBridge Diagnostics] Dispatching START_CAPTURE to offscreen document...");
      const response = await sendMessageToOffscreen({
        type: "START_CAPTURE",
        streamId,
        language: lang
      });

      console.info("[SignBridge Diagnostics] Offscreen document START_CAPTURE response:", response);
      return { ok: true, sessionId };

    } catch (err) {
      console.error("[SignBridge Diagnostics] Failed to start tab capture:", err);
      await closeOffscreenDoc();
      const errorMsg = err.message || "Failed to initialize tab audio capture.";
      await updateSessionState({
        status: "error",
        sessionId: null,
        errorMessage: errorMsg
      });
      return { ok: false, error: errorMsg };
    }
  }

  async function stopCapture(reason = "User requested stop") {
    console.info(`[SignBridge Diagnostics] Stopping capture. Reason: ${reason}`);
    
    // Broadcast stop event so avatar player transitions safely to neutral rest pose
    chrome.runtime.sendMessage({
      version: "1.0.0",
      type: "SIGNBRIDGE_CAPTURE_STOPPED",
      reason: reason,
      stoppedAt: Date.now()
    }).catch(() => {});

    await updateSessionState({ status: "stopping" });

    try {
      if (await hasOffscreenDoc()) {
        console.info("[SignBridge Diagnostics] Dispatching STOP_CAPTURE to offscreen document...");
        await sendMessageToOffscreen({ type: "STOP_CAPTURE" }, 2, 50).catch(() => {});
      }
    } catch (e) {
      console.warn("[SignBridge Diagnostics] Error during offscreen stop:", e);
    } finally {
      await closeOffscreenDoc();
      await updateSessionState({
        status: "idle",
        sessionId: null,
        latestTranscriptEvent: null,
        lastProcessedSequenceId: 0,
        tabId: null,
        tabTitle: null,
        tabUrl: null,
        startedAt: null,
        errorMessage: null
      });
      console.info("[SignBridge Diagnostics] Stop cleanup complete. Capture state returned to IDLE (ready for restart).");
    }

    return { ok: true };
  }

  // ---------------------------------------------------------------------------
  // Top-Level Event Listeners (Mandatory Synchronous Registration for MV3)
  // ---------------------------------------------------------------------------

  chrome.runtime.onInstalled.addListener(() => {
    chrome.storage.session.set({
      captureState: {
        status: "idle",
        tabId: null,
        tabTitle: null,
        tabUrl: null,
        startedAt: null,
        chunkCount: 0,
        totalBytes: 0,
        sampleRate: null,
        errorMessage: null,
        playbackPreserved: true,
        latestTranscript: "",
        transcripts: [],
        fullTranscript: "",
        backendStatus: "offline",
        lastInferenceMs: 0,
        lastRtf: 0,
        selectedLanguage: "en"
      }
    });
    console.info("[SignBridge SW] SignBridge extension installed (M2).");
  });

  // Handle messages from Popup and Offscreen Document
  chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (!message || !message.type) return;

    if (message.type === "REQUEST_START_CAPTURE") {
      (async () => {
        const [activeTab] = await chrome.tabs.query({ active: true, currentWindow: true });
        const targetTab = message.tab || activeTab;
        const res = await startCapture(targetTab, message.streamId);
        sendResponse(res);
      })();
      return true;
    }

    if (message.type === "REQUEST_STOP_CAPTURE") {
      (async () => {
        const res = await stopCapture("User clicked stop in popup");
        sendResponse(res);
      })();
      return true;
    }

    if (message.type === "GET_CAPTURE_STATE") {
      (async () => {
        const state = await getSessionState();
        sendResponse(state);
      })();
      return true;
    }

    if (message.type === "OPEN_AVATAR_WINDOW") {
      (async () => {
        const avatarUrl = chrome.runtime.getURL("overlay/avatar_player.html");
        try {
          const existingTabs = await chrome.tabs.query({ url: avatarUrl });
          if (existingTabs && existingTabs.length > 0) {
            await chrome.tabs.update(existingTabs[0].id, { active: true });
            if (existingTabs[0].windowId) {
              await chrome.windows.update(existingTabs[0].windowId, { focused: true });
            }
            sendResponse({ ok: true, reused: true, tabId: existingTabs[0].id });
            return;
          }
          if (chrome.windows && chrome.windows.create) {
            const win = await chrome.windows.create({
              url: avatarUrl,
              type: "popup",
              width: 960,
              height: 800,
              focused: true
            });
            sendResponse({ ok: true, created: true, windowId: win.id });
          } else {
            const tab = await chrome.tabs.create({ url: avatarUrl });
            sendResponse({ ok: true, created: true, tabId: tab.id });
          }
        } catch (err) {
          console.warn("[SignBridge SW] Error opening avatar window via chrome.windows, falling back to chrome.tabs:", err);
          const tab = await chrome.tabs.create({ url: avatarUrl });
          sendResponse({ ok: true, fallback: true, tabId: tab.id });
        }
      })();
      return true;
    }

    if (message.type === "CLEAR_TRANSCRIPT") {
      (async () => {
        await updateSessionState({
          latestTranscript: "",
          transcripts: [],
          fullTranscript: "",
          latestTranscriptEvent: null
        });
        sendResponse({ ok: true });
      })();
      return true;
    }

    if (message.type === "SET_LANGUAGE") {
      (async () => {
        await updateSessionState({ selectedLanguage: message.language });
        if (await hasOffscreenDoc()) {
          await sendMessageToOffscreen({ type: "SET_LANGUAGE", language: message.language }).catch(() => {});
        }
        sendResponse({ ok: true });
      })();
      return true;
    }

    if (message.type === "CAPTURE_STARTED") {
      console.info(`[SignBridge Diagnostics] Audio capture started in offscreen. SampleRate: ${message.sampleRate}Hz, State: ${message.audioState}`);
      (async () => {
        const current = await getSessionState();
        await updateSessionState({
          status: "capturing",
          sampleRate: message.sampleRate,
          errorMessage: null
        });

        // Broadcast capture started event to active avatar views
        chrome.runtime.sendMessage({
          version: "1.0.0",
          type: "SIGNBRIDGE_CAPTURE_STARTED",
          sessionId: current.sessionId,
          sampleRate: message.sampleRate,
          startedAt: Date.now()
        }).catch(() => {});
      })();
      return false;
    }

    if (message.type === "CAPTURE_PROGRESS") {
      console.info(`[SignBridge Diagnostics] Capture progress: Chunk #${message.chunkCount}, Total data: ${message.totalBytes} bytes (${message.sampleRate}Hz)`);
      updateSessionState({
        chunkCount: message.chunkCount,
        totalBytes: message.totalBytes,
        sampleRate: message.sampleRate
      });
      return false;
    }

    if (message.type === "TRANSCRIPTION_RESULT") {
      (async () => {
        const current = await getSessionState();
        if (current.status !== "capturing") {
          console.warn(`[SignBridge Diagnostics] Dropping transcription result for chunk #${message.sequenceId} because capture status is '${current.status}'`);
          return;
        }

        const text = (message.text || "").trim();
        console.info(`[SignBridge Diagnostics] Transcription result received for chunk #${message.sequenceId} (duration=${message.duration}s): "${text}"`);
        const rawWords = message.segments ? message.segments.flatMap(s => s.words || []) : [];

        // Word-level confidence average only if valid probabilities exist from backend
        let confidence = null;
        if (rawWords.length > 0) {
          const probs = rawWords.filter(w => typeof w.probability === "number" && !isNaN(w.probability));
          if (probs.length > 0) {
            confidence = probs.reduce((acc, w) => acc + w.probability, 0) / probs.length;
            confidence = Math.round(confidence * 100) / 100;
          }
        }

        // Standardized version 1.0.0 dispatch payload
        const dispatchEvent = {
          version: "1.0.0",
          type: "SIGNBRIDGE_TRANSCRIPTION_DISPATCH",
          sessionId: current.sessionId,
          sequenceId: message.sequenceId,
          timestamp: message.timestamp,
          duration: message.duration,
          text: text,
          words: rawWords,
          confidence: confidence,
          language: message.language || current.selectedLanguage || "en",
          metrics: message.metrics || {},
          dispatchedAt: Date.now()
        };

        const newSegments = [...(current.transcripts || [])];
        if (text) {
          newSegments.push({
            sequenceId: message.sequenceId,
            timestamp: message.timestamp,
            duration: message.duration,
            text,
            words: rawWords,
            confidence
          });

          // Bound stored segments to last 30 items
          if (newSegments.length > 30) {
            newSegments.shift();
          }
        }

        const fullText = newSegments.map(s => s.text).join(" ").trim();

        await updateSessionState({
          latestTranscript: text || current.latestTranscript,
          latestTranscriptEvent: dispatchEvent,
          lastProcessedSequenceId: message.sequenceId,
          transcripts: newSegments,
          fullTranscript: fullText,
          backendStatus: "online",
          lastInferenceMs: message.metrics ? message.metrics.inference_time_ms : 0,
          lastRtf: message.metrics ? message.metrics.rtf : 0
        });

        // Broadcast to all active extension pages (avatar player, popup, etc.)
        chrome.runtime.sendMessage(dispatchEvent).catch(() => {});
      })();
      return false;
    }

    if (message.type === "TRANSCRIPTION_ERROR") {
      console.error(`[SignBridge Diagnostics] Transcription error for chunk #${message.sequenceId}: ${message.error}`);
      updateSessionState({
        backendStatus: "error"
      });
      return false;
    }

    if (message.type === "QUEUE_OVERFLOW") {
      console.warn(`[SignBridge Diagnostics] Queue overflow: Chunk #${message.droppedSequenceId} dropped (backend queue full)`);
      return false;
    }

    if (message.type === "CAPTURE_ERROR") {
      console.error("[SignBridge Diagnostics] Capture error from offscreen:", message.error);
      stopCapture(message.error).then(() => {
        updateSessionState({
          status: "error",
          errorMessage: message.error
        });
      });
      return false;
    }

    if (message.type === "CAPTURE_TRACK_ENDED") {
      console.info("[SignBridge Diagnostics] Audio track ended:", message.reason);
      stopCapture(message.reason);
      return false;
    }
  });

  // Monitor tab closure — release resources immediately
  chrome.tabs.onRemoved.addListener(async (closedTabId) => {
    const state = await getSessionState();
    if (state.tabId && state.tabId === closedTabId) {
      console.info(`[SignBridge SW] Captured tab ${closedTabId} was closed. Cleaning up.`);
      await stopCapture("Target tab closed");
    }
  });

  // Monitor tab navigation — if captured tab navigates away, stop capture
  chrome.tabs.onUpdated.addListener(async (updatedTabId, changeInfo) => {
    const state = await getSessionState();
    if (state.tabId && state.tabId === updatedTabId && changeInfo.url) {
      console.info(`[SignBridge SW] Captured tab navigated to: ${changeInfo.url}. Cleaning up.`);
      await stopCapture("Tab navigated to new URL");
    }
  });

})();
