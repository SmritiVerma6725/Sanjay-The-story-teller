// SignBridge — Popup Controller (Milestone M1)
//
// Responsibilities:
// 1. Detect active tab and enforce explicit user activation (PRD FR-01).
// 2. Dispatch REQUEST_START_CAPTURE and REQUEST_STOP_CAPTURE to service worker.
// 3. Render real-time audio telemetry (chunks, bytes, duration, sample rate).
// 4. Manage user language preference (ISL default vs ASL).
// 5. Check local backend health (127.0.0.1:8765) with graceful offline indicator.

(() => {
  "use strict";

  const BACKEND_URL = "http://127.0.0.1:8765/health";

  // DOM Elements
  const statusBadge = document.getElementById("statusBadge");
  const tabIndicator = document.getElementById("tabIndicator");
  const tabTitle = document.getElementById("tabTitle");
  const tabUrl = document.getElementById("tabUrl");
  const tabWarning = document.getElementById("tabWarning");
  const captureBtn = document.getElementById("captureBtn");
  const btnText = document.getElementById("btnText");
  const errorAlert = document.getElementById("errorAlert");
  const errorMessage = document.getElementById("errorMessage");
  const chunkCountEl = document.getElementById("chunkCount");
  const elapsedDurationEl = document.getElementById("elapsedDuration");
  const totalDataEl = document.getElementById("totalData");
  const sampleRateEl = document.getElementById("sampleRate");
  const backendDot = document.getElementById("backendDot");
  const backendText = document.getElementById("backendText");
  const refreshBackendBtn = document.getElementById("refreshBackendBtn");
  const langISL = document.getElementById("langISL");
  const langASL = document.getElementById("langASL");

  // M2 Transcript Elements
  const transcriptionBadge = document.getElementById("transcriptionBadge");
  const clearTranscriptBtn = document.getElementById("clearTranscriptBtn");
  const emptyTranscriptNotice = document.getElementById("emptyTranscriptNotice");
  const transcriptText = document.getElementById("transcriptText");
  const asrLatency = document.getElementById("asrLatency");
  const asrRtf = document.getElementById("asrRtf");
  const asrChunkSeq = document.getElementById("asrChunkSeq");
  const asrConfidence = document.getElementById("asrConfidence");
  const openAvatarBtn = document.getElementById("openAvatarBtn");

  let currentTab = null;
  let pollTimer = null;
  let currentState = null;

  // Format bytes into readable string
  function formatBytes(bytes) {
    if (!bytes || bytes === 0) return "0 KB";
    const k = 1024;
    if (bytes < k) return `${bytes} B`;
    if (bytes < k * k) return `${(bytes / k).toFixed(1)} KB`;
    return `${(bytes / (k * k)).toFixed(2)} MB`;
  }

  // Format seconds into mm:ss
  function formatDuration(seconds) {
    if (!seconds || isNaN(seconds)) return "00:00";
    const m = Math.floor(seconds / 60);
    const s = Math.floor(seconds % 60);
    return `${m.toString().padStart(2, "0")}:${s.toString().padStart(2, "0")}`;
  }

  // Check active tab
  async function inspectActiveTab() {
    try {
      const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
      currentTab = tab;

      if (!tab) {
        tabTitle.textContent = "No active tab detected";
        tabUrl.textContent = "--";
        captureBtn.disabled = true;
        return;
      }

      tabTitle.textContent = tab.title || "Untitled Tab";
      tabUrl.textContent = tab.url || "";

      const url = tab.url || "";
      const isInternal = url.startsWith("chrome://") ||
                         url.startsWith("chrome-extension://") ||
                         url.startsWith("edge://") ||
                         url.startsWith("about:");

      if (isInternal) {
        tabIndicator.className = "tab-indicator indicator-warning";
        tabWarning.classList.remove("hidden");
        captureBtn.disabled = true;
        captureBtn.title = "Cannot capture Chrome internal pages.";
      } else {
        tabWarning.classList.add("hidden");
        captureBtn.disabled = false;
        captureBtn.title = "";

        const isYouTube = url.includes("youtube.com/watch") ||
                          url.includes("youtube.com/live") ||
                          url.includes("youtube.com/shorts");

        if (isYouTube) {
          tabIndicator.className = "tab-indicator indicator-youtube";
        } else {
          tabIndicator.className = "tab-indicator indicator-neutral";
        }
      }
    } catch (err) {
      console.error("[SignBridge Popup] Error inspecting active tab:", err);
    }
  }

  let activePopupHealthCheckId = 0;
  let isPopupHealthCheckInFlight = false;

  // Check local Python backend health
  async function checkBackendHealth() {
    if (isPopupHealthCheckInFlight) return;
    const checkId = ++activePopupHealthCheckId;
    isPopupHealthCheckInFlight = true;

    backendText.textContent = "Checking...";
    const HEALTH_TIMEOUT_MS = 5000;
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), HEALTH_TIMEOUT_MS);

    try {
      const res = await fetch(BACKEND_URL, {
        method: "GET",
        signal: controller.signal
      });
      clearTimeout(timeoutId);

      if (checkId !== activePopupHealthCheckId) return;

      if (res.ok) {
        const data = await res.json();
        if (data && data.status === "ok") {
          backendDot.className = "status-dot dot-online";
          backendText.textContent = `Online (${data.model || "Whisper"}, ${data.compute_type || "CPU"})`;
        } else {
          backendDot.className = "status-dot dot-offline";
          backendText.textContent = "Offline (Malformed response)";
        }
      } else {
        backendDot.className = "status-dot dot-offline";
        backendText.textContent = `Offline (HTTP ${res.status})`;
      }
    } catch (e) {
      clearTimeout(timeoutId);
      if (checkId !== activePopupHealthCheckId) return;
      const isTimeout = e.name === "AbortError";
      backendDot.className = "status-dot dot-offline";
      backendText.textContent = isTimeout ? "Offline (Timeout >5s)" : "Offline (Run python run.py)";
    } finally {
      isPopupHealthCheckInFlight = false;
    }
  }

  // Update UI according to session state
  function renderState(state) {
    if (!state) return;
    currentState = state;

    // Badges & Buttons
    statusBadge.className = `badge badge-${state.status}`;
    statusBadge.textContent = state.status.toUpperCase();

    if (state.status === "capturing") {
      captureBtn.className = "btn btn-danger";
      btnText.textContent = "Stop Capture";
      captureBtn.disabled = false;
      captureBtn.querySelector(".btn-icon").innerHTML = "&#9632;"; // Square stop icon
    } else if (state.status === "starting") {
      captureBtn.className = "btn btn-primary";
      btnText.textContent = "Starting...";
      captureBtn.disabled = true;
      captureBtn.querySelector(".btn-icon").innerHTML = "&#8987;"; // Hourglass icon
    } else if (state.status === "stopping") {
      captureBtn.className = "btn btn-danger";
      btnText.textContent = "Stopping...";
      captureBtn.disabled = true;
    } else {
      // Idle or error
      captureBtn.className = "btn btn-primary";
      btnText.textContent = "Start Audio Capture";
      captureBtn.querySelector(".btn-icon").innerHTML = "&#9654;"; // Play icon
      if (tabWarning && !tabWarning.classList.contains("hidden")) {
        captureBtn.disabled = true;
      } else {
        captureBtn.disabled = false;
      }
    }

    // Telemetry
    chunkCountEl.textContent = state.chunkCount || 0;
    totalDataEl.textContent = formatBytes(state.totalBytes || 0);

    if (state.startedAt && state.status === "capturing") {
      const elapsed = Math.round((Date.now() - state.startedAt) / 1000);
      elapsedDurationEl.textContent = formatDuration(elapsed);
    } else {
      elapsedDurationEl.textContent = "00:00";
    }

    sampleRateEl.textContent = state.sampleRate ? `${state.sampleRate} Hz` : "--";

    // M2 Speech Transcription Rendering
    const hasTranscripts = state.transcripts && state.transcripts.length > 0;
    const displayText = state.fullTranscript || (state.transcripts ? state.transcripts.map(t => t.text).join(" ") : "");

    if (hasTranscripts && displayText.trim()) {
      emptyTranscriptNotice.classList.add("hidden");
      transcriptText.classList.remove("hidden");
      transcriptText.textContent = displayText.trim();
      if (clearTranscriptBtn) clearTranscriptBtn.disabled = false;
    } else {
      emptyTranscriptNotice.classList.remove("hidden");
      transcriptText.classList.add("hidden");
      transcriptText.textContent = "";
      if (clearTranscriptBtn) clearTranscriptBtn.disabled = true;
    }

    if (transcriptionBadge) {
      if (state.status === "capturing") {
        transcriptionBadge.className = "badge badge-capturing";
        transcriptionBadge.textContent = "LISTENING";
      } else if (hasTranscripts) {
        transcriptionBadge.className = "badge badge-idle";
        transcriptionBadge.textContent = "READY";
      } else {
        transcriptionBadge.className = "badge badge-idle";
        transcriptionBadge.textContent = "STANDBY";
      }
    }

    if (asrLatency) {
      asrLatency.textContent = state.lastInferenceMs ? `Latency: ${state.lastInferenceMs}ms` : "Latency: --";
    }
    if (asrRtf) {
      asrRtf.textContent = state.lastRtf ? `RTF: ${state.lastRtf}` : "RTF: --";
    }
    if (asrChunkSeq) {
      asrChunkSeq.textContent = `Chunk: #${state.chunkCount || 0}`;
    }
    if (asrConfidence) {
      const conf = state.latestTranscriptEvent && typeof state.latestTranscriptEvent.confidence === "number"
        ? `${Math.round(state.latestTranscriptEvent.confidence * 100)}%`
        : "--";
      asrConfidence.textContent = `Conf: ${conf}`;
    }

    // Error Alert
    if (state.errorMessage) {
      errorAlert.classList.remove("hidden");
      errorMessage.textContent = state.errorMessage;
    } else {
      errorAlert.classList.add("hidden");
    }
  }

  // Poll state from service worker
  async function refreshState() {
    try {
      const state = await chrome.runtime.sendMessage({ type: "GET_CAPTURE_STATE" });
      if (state) {
        renderState(state);
      }
    } catch (e) {
      // Service worker might be sleeping
    }
  }

  // Setup language selector persistence
  async function setupLanguageSelector() {
    try {
      const stored = await chrome.storage.local.get("selectedLanguage");
      const current = stored.selectedLanguage || "ISL";
      if (current === "ASL") {
        langASL.checked = true;
      } else {
        langISL.checked = true;
      }

      document.querySelectorAll("input[name='targetLanguage']").forEach((radio) => {
        radio.addEventListener("change", (e) => {
          const selected = e.target.value;
          chrome.storage.local.set({ selectedLanguage: selected });
          console.info(`[SignBridge Popup] Selected language set to: ${selected}`);
        });
      });
    } catch (err) {
      console.warn("[SignBridge Popup] Error initializing language preference:", err);
    }
  }

  function initializeEventListeners() {
    if (captureBtn) {
      captureBtn.addEventListener("click", async () => {
        console.info("[SignBridge Diagnostics] Capture button clicked. Current status:", currentState?.status || "unknown");
        if (!currentState) {
          await refreshState();
        }

        const isCapturing = currentState && currentState.status === "capturing";

        if (isCapturing) {
          console.info("[SignBridge Diagnostics] Action: User requesting stop capture.");
          captureBtn.disabled = true;
          btnText.textContent = "Stopping...";
          try {
            const res = await chrome.runtime.sendMessage({ type: "REQUEST_STOP_CAPTURE" });
            console.info("[SignBridge Diagnostics] Stop capture dispatched. Response:", res);
            await refreshState();
          } catch (err) {
            console.error("[SignBridge Diagnostics] Error stopping capture:", err);
            if (errorAlert && errorMessage) {
              errorAlert.classList.remove("hidden");
              errorMessage.textContent = `Stop error: ${err.message || err}`;
            }
          } finally {
            captureBtn.disabled = false;
          }
        } else {
          console.info("[SignBridge Diagnostics] Action: User requesting start capture for tab:", currentTab?.id || "unidentified");
          captureBtn.disabled = true;
          btnText.textContent = "Starting...";
          try {
            // Obtain ephemeral streamId directly within user gesture context
            let streamId = null;
            if (typeof chrome !== "undefined" && chrome.tabCapture && chrome.tabCapture.getMediaStreamId && currentTab && currentTab.id) {
              try {
                streamId = await chrome.tabCapture.getMediaStreamId({ targetTabId: currentTab.id });
                if (streamId) {
                  console.info("[SignBridge Diagnostics] Stream ID acquisition: SUCCESS (ephemeral ID obtained under user gesture)");
                } else {
                  console.warn("[SignBridge Diagnostics] Stream ID acquisition: FAILED (getMediaStreamId returned empty ID)");
                }
              } catch (captureErr) {
                console.warn("[SignBridge Diagnostics] Stream ID acquisition: FAILED in popup -", captureErr.message || captureErr);
              }
            } else {
              console.warn("[SignBridge Diagnostics] Stream ID acquisition: skipped in popup (tabCapture not available or tab unknown)");
            }

            const res = await chrome.runtime.sendMessage({
              type: "REQUEST_START_CAPTURE",
              streamId: streamId,
              tab: currentTab
            });

            if (res && !res.ok) {
              console.warn("[SignBridge Diagnostics] Start capture rejected by service worker:", res.error);
              if (errorAlert && errorMessage) {
                errorAlert.classList.remove("hidden");
                errorMessage.textContent = res.error || "Capture start was rejected.";
              }
            } else {
              console.info("[SignBridge Diagnostics] Start capture accepted by service worker.");
              if (errorAlert) {
                errorAlert.classList.add("hidden");
              }
            }
            await refreshState();
          } catch (err) {
            console.error("[SignBridge Diagnostics] Error requesting start capture:", err);
            if (errorAlert && errorMessage) {
              errorAlert.classList.remove("hidden");
              errorMessage.textContent = `Start error: ${err.message || err}`;
            }
          } finally {
            captureBtn.disabled = false;
          }
        }
      });
    }

    if (refreshBackendBtn) {
      refreshBackendBtn.addEventListener("click", () => {
        checkBackendHealth();
      });
    }

    if (openAvatarBtn) {
      openAvatarBtn.addEventListener("click", async () => {
        try {
          await chrome.runtime.sendMessage({ type: "OPEN_AVATAR_WINDOW" });
        } catch (err) {
          console.warn("[SignBridge Popup] Direct window message failed, opening tab:", err);
          chrome.tabs.create({ url: chrome.runtime.getURL("overlay/avatar_player.html") });
        }
      });
    }

    if (clearTranscriptBtn) {
      clearTranscriptBtn.addEventListener("click", async () => {
        try {
          await chrome.runtime.sendMessage({ type: "CLEAR_TRANSCRIPT" });
          await refreshState();
        } catch (err) {
          console.error("[SignBridge Popup] Error clearing transcript:", err);
        }
      });
    }
  }

  async function init() {
    initializeEventListeners();
    await inspectActiveTab();
    await setupLanguageSelector();
    await refreshState();
    await checkBackendHealth();

    // Poll capture state every 500ms while popup is open
    pollTimer = setInterval(refreshState, 500);
  }

  // Initialization
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }

  // Cleanup on popup close
  window.addEventListener("unload", () => {
    if (pollTimer) {
      clearInterval(pollTimer);
    }
  });

})();
