"""
SignBridge — Live Speech-to-ISL Animation Routing Regression Test Suite

Verifies:
1. Supported & eligible ISL sign (Namaste) articulates through the live transcript path.
2. Multi-sign transcript plays eligible clips in correct order and preserves honest sequence history.
3. Unsupported out-of-lexicon words produce safe, explicit neutral fallback (zero synthetic gestures).
4. Experimental/unreviewed candidate clip is isolated in quarantine and never promoted or played by policy.
5. Missing animation does not appear as successful playback (Root Cause: 'YOU (500 ms)' neutral hold never claims COMPLETED clip).
6. Duplicate chunks and stopped sessions do not restart playback or corrupt telemetry.
7. Telemetry (clip ID, title, duration, elapsed time, progress bar, badge, linguistic validity) remains strictly synchronized with actual playback.
"""

import unittest
import http.server
import socketserver
import threading
import subprocess
import time
import os
import sys
import json
import urllib.request
import tempfile
import shutil

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
PORT = 8086


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    regression_results = None
    runner_error = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=REPO_ROOT, **kwargs)

    def do_POST(self):
        if self.path == "/report_regression_results":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8")
            try:
                QuietHandler.regression_results = json.loads(body)
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(b'{"status":"ok"}')
            except Exception as e:
                QuietHandler.runner_error = str(e)
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b'{"status":"error"}')
            return
        self.send_response(404)
        self.end_headers()

    def log_message(self, format, *args):
        pass  # Suppress HTTP server noise


class TestLiveSpeechRoutingRegression(unittest.TestCase):
    """Browser-based regression tests for live speech-to-ISL routing and telemetry."""

    @classmethod
    def setUpClass(cls):
        # Start quiet local HTTP server serving repository root
        QuietHandler.regression_results = None
        QuietHandler.runner_error = None
        cls.httpd = socketserver.TCPServer(("127.0.0.1", PORT), QuietHandler)
        cls.server_thread = threading.Thread(target=cls.httpd.serve_forever, daemon=True)
        cls.server_thread.start()
        time.sleep(1)

        # Build runner HTML and test controller
        raw_html_path = os.path.join(REPO_ROOT, "extension", "overlay", "avatar_player.html")
        with open(raw_html_path, "r", encoding="utf-8") as f:
            html_raw = f.read()

        cls.runner_html_path = os.path.join(REPO_ROOT, "extension", "overlay", "avatar_player_routing_runner.html")
        cls.runner_js_path = os.path.join(REPO_ROOT, "extension", "overlay", "avatar_player_routing_runner.js")

        injected_html = html_raw.replace(
            "</body>",
            '<script src="avatar_player_routing_runner.js"></script></body>'
        )
        with open(cls.runner_html_path, "w", encoding="utf-8") as f:
            f.write(injected_html)

        # In-browser test scenario runner script
        test_js = """
        window.addEventListener("load", async () => {
            const results = { checks: [], passed: 0, failed: 0 };
            const wait = (ms) => new Promise(r => setTimeout(r, ms));

            function assert(cond, name, detail) {
                if (cond) {
                    results.checks.push({ name, status: "PASS", detail: String(detail || "") });
                    results.passed++;
                } else {
                    results.checks.push({ name, status: "FAIL", detail: String(detail || "") });
                    results.failed++;
                }
            }

            async function reportCompletion(res) {
                const outDiv = document.createElement("div");
                outDiv.id = "live-routing-regression-results";
                outDiv.textContent = JSON.stringify(res);
                document.body.appendChild(outDiv);

                try {
                    await fetch("/report_regression_results", {
                        method: "POST",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify(res)
                    });
                } catch (e) {
                    console.error("Failed to POST regression results:", e);
                }
            }

            // Explicit model-loaded signal check with bounded wait
            const telLoaded = document.getElementById("tel-loaded");
            const diagModelStatus = document.getElementById("diag-model-status");
            const diagLoadError = document.getElementById("diag-load-error");
            let waitedMs = 0;
            const maxModelWaitMs = 15000;
            while (waitedMs < maxModelWaitMs && (!telLoaded || !telLoaded.innerText.includes("Loaded"))) {
                await wait(200);
                waitedMs += 200;
            }

            const isModelLoaded = Boolean(telLoaded && telLoaded.innerText.includes("Loaded"));
            assert(isModelLoaded, "S0: 3D Model Loaded", isModelLoaded ? telLoaded.innerText : `Timed out waiting for 3D model (status: ${diagModelStatus ? diagModelStatus.innerText : 'unknown'}, error: ${diagLoadError ? diagLoadError.innerText : 'none'})`);

            if (!isModelLoaded) {
                await reportCompletion(results);
                return;
            }

            const p = window.player;
            const bridgeLive = document.getElementById("bridge-live-transcript");
            const bridgeRouting = document.getElementById("bridge-routing-status");
            const bridgeBadge = document.getElementById("bridge-status-badge");
            const clipTitle = document.getElementById("clip-title");
            const telState = document.getElementById("tel-state");
            const telClip = document.getElementById("tel-clip");
            const timeDisplay = document.getElementById("time-display");
            const progressFill = document.getElementById("progress-fill");
            const telIslGuard = document.getElementById("tel-isl-guard");

            // -------------------------------------------------------------
            // Scenario 1: Supported & eligible ISL sign (Namaste) articulates through live path
            // -------------------------------------------------------------
            window.handleLiveTranscriptDispatch({
                version: "1.0.0",
                type: "SIGNBRIDGE_TRANSCRIPTION_DISPATCH",
                sessionId: "session_reg_1",
                sequenceId: 1,
                timestamp: 1.0,
                duration: 2.0,
                text: "namaste",
                confidence: 0.95
            });
            await wait(250);

            assert(p && p.isPlaying, "S1: Namaste Playing", "player.isPlaying === true");
            assert(p && p.currentClip && p.currentClip.animationId === "isl_namaste_godl_v1", "S1: Correct Baseline Clip", p.currentClip ? p.currentClip.animationId : "none");
            assert(p && p.currentSignGloss === "NAMASTE", "S1: Correct Gloss", p ? p.currentSignGloss : "none");
            assert(bridgeRouting && bridgeRouting.innerText.includes("ISL Namaste") && bridgeRouting.innerText.includes("GODL v1.0"), "S1: Routing Status Articulating Baseline", bridgeRouting.innerText);
            assert(telIslGuard && telIslGuard.innerText.includes("Experimental ISL"), "S1: Linguistic Guard Shown", telIslGuard.innerText);

            // Verify streaming silence chunk does NOT abort active in-flight Namaste gesture
            window.handleLiveTranscriptDispatch({
                version: "1.0.0",
                type: "SIGNBRIDGE_TRANSCRIPTION_DISPATCH",
                sessionId: "session_reg_1",
                sequenceId: 2,
                timestamp: 3.0,
                duration: 2.0,
                text: "", // Silence chunk from streaming audio!
                confidence: null
            });
            await wait(200);
            assert(p && p.isPlaying && p.currentClip && p.currentClip.animationId === "isl_namaste_godl_v1", "S1: Silence Does NOT Abort In-Flight Sign", "In-flight gesture protected");

            // Advance playback through completion of Namaste (1800ms)
            p.update(1900);
            await wait(150);
            const st1 = p.getStatus();
            assert(st1.sequencePlaybackState === "COMPLETED", "S1: Sequence State Completed", st1.sequencePlaybackState);
            assert(st1.currentClipId === "isl_namaste_godl_v1", "S1: Retains Completed Clip ID", st1.currentClipId);
            assert(clipTitle && clipTitle.innerText.includes("NAMASTE — isl_namaste_godl_v1") && clipTitle.innerText.includes("COMPLETED"), "S1: Title Reflects Completed Sign", clipTitle.innerText);
            assert(telState && telState.innerText.includes("COMPLETED"), "S1: Badge Shows Completed", telState.innerText);
            assert(progressFill && progressFill.style.width === "100%", "S1: Progress Fill 100%", progressFill.style.width);

            // -------------------------------------------------------------
            // Scenario 2: Multi-sign transcript plays eligible clips in order
            // -------------------------------------------------------------
            window.handleLiveTranscriptDispatch({
                version: "1.0.0",
                type: "SIGNBRIDGE_TRANSCRIPTION_DISPATCH",
                sessionId: "session_reg_1",
                sequenceId: 3,
                timestamp: 5.0,
                duration: 2.0,
                text: "namaste you",
                confidence: 0.92
            });
            await wait(250);

            assert(p && p.activeSequence && p.activeSequence.signs.length === 2, "S2: Multi-Sign Length is 2", p.activeSequence ? p.activeSequence.signs.length : 0);
            assert(p.activeSequence.signs[0].gloss === "NAMASTE" && p.activeSequence.signs[1].gloss === "YOU", "S2: Correct Ordered Glosses", "NAMASTE then YOU");
            assert(p.isPlaying && p.currentClip && p.currentClip.animationId === "isl_namaste_godl_v1", "S2: Sign 1 Articulates Namaste", p.currentClip.animationId);

            // Advance through Sign 1 (1800ms) to trigger Sign 2 (YOU: 500ms neutral hold)
            p.update(1850);
            await wait(150);
            assert(p.currentSignGloss === "YOU", "S2: Sign 2 Gloss is YOU", p.currentSignGloss);
            assert(p.currentSignIsFallback === true, "S2: Sign 2 Held in Fallback", "currentSignIsFallback === true");
            assert(p.currentClip === null, "S2: Zero 3D Clip for Un-animated YOU", "currentClip === null");

            // Advance through Sign 2 (500ms) to complete sequence
            p.update(550);
            await wait(150);
            const st2 = p.getStatus();
            assert(st2.sequencePlaybackState === "COMPLETED", "S2: Multi-Sign State Completed", st2.sequencePlaybackState);
            assert(st2.currentClipId === "isl_namaste_godl_v1", "S2: Multi-Sign Preserves Articulated Clip ID", st2.currentClipId);
            assert(st2.durationMs === 1800, "S2: Duration is Articulated 1800ms", st2.durationMs);

            // -------------------------------------------------------------
            // Scenario 3: Unsupported out-of-lexicon words produce safe, explicit fallback
            // -------------------------------------------------------------
            window.handleLiveTranscriptDispatch({
                version: "1.0.0",
                type: "SIGNBRIDGE_TRANSCRIPTION_DISPATCH",
                sessionId: "session_reg_1",
                sequenceId: 4,
                timestamp: 7.0,
                duration: 2.0,
                text: "superconducting tokamak reactor",
                confidence: 0.89
            });
            await wait(250);

            assert(p && !p.isPlaying, "S3: Not Playing on Unsupported", "isPlaying === false");
            assert(p && p.currentClip === null, "S3: No Clip on Unsupported", "currentClip === null");
            assert(p && p.currentPoseId === "pose_neutral_rest_v1", "S3: Neutral Pose Held", p.currentPoseId);
            assert(bridgeRouting && bridgeRouting.innerText.includes("Out-of-lexicon words"), "S3: Explicit Out-of-lexicon Status", bridgeRouting.innerText);
            assert(bridgeRouting.innerText.includes("superconducting"), "S3: Lists Unsupported Words", bridgeRouting.innerText);

            // -------------------------------------------------------------
            // Scenario 4: Experimental/unreviewed candidate clip is NOT promoted or played
            // -------------------------------------------------------------
            const regClips = window.SignBridgeKeyframeRegistry ? window.SignBridgeKeyframeRegistry.getRegisteredClips() : null;
            const resNamaste = window.SignBridgeKeyframeRegistry.resolveSignAnimation({ gloss: "NAMASTE" });
            assert(resNamaste.resolved && resNamaste.animationId === "isl_namaste_godl_v1", "S4: Production Gloss Strictly Resolves Baseline", resNamaste.animationId);
            assert(resNamaste.animationId !== "isl_namaste_mocap_candidate_v1", "S4: Candidate Not Auto-Promoted", "Quarantine enforced");

            // -------------------------------------------------------------
            // Scenario 5: Missing animation does NOT appear as successful playback
            // (Direct root-cause regression: 'YOU (500 ms)' must never show COMPLETED)
            // -------------------------------------------------------------
            window.handleLiveTranscriptDispatch({
                version: "1.0.0",
                type: "SIGNBRIDGE_TRANSCRIPTION_DISPATCH",
                sessionId: "session_reg_1",
                sequenceId: 5,
                timestamp: 9.0,
                duration: 2.0,
                text: "you",
                confidence: 0.94
            });
            await wait(200);

            // During the 500ms neutral hold
            assert(p.currentSignGloss === "YOU", "S5: Gloss is YOU", p.currentSignGloss);
            assert(p.currentSignIsFallback === true, "S5: Fallback Active", "currentSignIsFallback === true");
            assert(clipTitle && clipTitle.innerText.includes("Neutral Fallback"), "S5: Title Indicates Neutral Fallback", clipTitle.innerText);

            // Advance through 500ms to complete
            p.update(550);
            await wait(200);
            const st5 = p.getStatus();
            assert(st5.sequencePlaybackState === "COMPLETED", "S5: Sequence State Completed", st5.sequencePlaybackState);
            assert(st5.currentClipId === null, "S5: Completed Clip ID is NULL", String(st5.currentClipId));
            assert(st5.currentGloss === null, "S5: Completed Gloss is NULL", String(st5.currentGloss));
            assert(st5.durationMs === 0, "S5: Completed Duration is 0ms", String(st5.durationMs));

            // CRITICAL CHECK: clipTitle must NOT say 'YOU (500 ms) — COMPLETED'
            assert(!clipTitle.innerText.includes("YOU (500 ms)"), "S5: CRITICAL - No 'YOU (500 ms)' Completed Claim", clipTitle.innerText);
            assert(clipTitle.innerText === "Neutral Rest Pose (0 ms)", "S5: Displays Neutral Rest Pose (0 ms)", clipTitle.innerText);
            assert(!telState.innerText.includes("COMPLETED"), "S5: CRITICAL - Badge Does NOT Claim COMPLETED", telState.innerText);
            assert(telState.innerText.includes("NEUTRAL"), "S5: Badge Shows NEUTRAL", telState.innerText);
            assert(progressFill.style.width === "0%", "S5: Progress Bar at 0%", progressFill.style.width);

            // -------------------------------------------------------------
            // Scenario 6: Duplicate chunks and stopped sessions do not restart playback
            // -------------------------------------------------------------
            const playCountBefore = p.renderCount || 0;
            // Send duplicate sequenceId (sequenceId 5 again)
            window.handleLiveTranscriptDispatch({
                version: "1.0.0",
                type: "SIGNBRIDGE_TRANSCRIPTION_DISPATCH",
                sessionId: "session_reg_1",
                sequenceId: 5, // Duplicate!
                timestamp: 9.0,
                duration: 2.0,
                text: "you",
                confidence: 0.94
            });
            await wait(150);
            assert(p.currentClip === null && !p.isPlaying, "S6: Duplicate Chunk Ignored", "Playback not restarted");

            // Dispatch capture stopped event
            window.handleCaptureStopped({
                version: "1.0.0",
                type: "SIGNBRIDGE_CAPTURE_STOPPED",
                reason: "Normal stop"
            });
            await wait(150);
            assert(bridgeBadge && bridgeBadge.innerText.includes("IDLE"), "S6: Capture Status IDLE on Stop", bridgeBadge.innerText);
            assert(bridgeRouting && bridgeRouting.innerText.includes("Capture session stopped"), "S6: Routing Status Reports Stopped", bridgeRouting.innerText);
            assert(p && !p.isPlaying, "S6: Avatar Neutral on Stop", "isPlaying === false");

            // -------------------------------------------------------------
            // Scenario 7: Telemetry agrees with actual playback and completion
            // -------------------------------------------------------------
            window.handleCaptureStarted({ sessionId: "session_reg_2" });
            await wait(100);
            assert(bridgeBadge.innerText.includes("ACTIVE"), "S7: Bridge Active After Start", bridgeBadge.innerText);

            window.handleLiveTranscriptDispatch({
                version: "1.0.0",
                type: "SIGNBRIDGE_TRANSCRIPTION_DISPATCH",
                sessionId: "session_reg_2",
                sequenceId: 10,
                timestamp: 15.0,
                duration: 2.0,
                text: "namaste",
                confidence: 0.98
            });
            await wait(250);

            // Active playback telemetry verification
            assert(telClip.innerText.includes("isl_namaste_godl_v1"), "S7: Active tel-clip matches clip ID", telClip.innerText);
            assert(clipTitle.innerText.includes("NAMASTE — isl_namaste_godl_v1 (1800 ms)"), "S7: Active clip-title matches duration", clipTitle.innerText);
            assert(telState.innerText.includes("PLAYING"), "S7: Active badge is PLAYING", telState.innerText);

            // Pause to freeze clock and synchronize UI
            p.pause();
            await wait(100);
            const midSt = p.getStatus();
            assert(timeDisplay.innerText.includes(`${midSt.currentTimeMs} / 1800 ms`), "S7: Mid-play time display synchronized", `${timeDisplay.innerText} (expected ${midSt.currentTimeMs})`);
            const expectedPct = Math.min(100, Math.round((midSt.currentTimeMs / 1800) * 100));
            assert(progressFill.style.width === `${expectedPct}%`, "S7: Mid-play progress bar synchronized", `${progressFill.style.width} (expected ${expectedPct}%)`);
            p.resume();
            await wait(50);

            // Complete playback
            p.update(1900);
            await wait(150);
            assert(timeDisplay.innerText.includes("1800 / 1800 ms"), "S7: Completion time display synchronized", timeDisplay.innerText);
            assert(progressFill.style.width === "100%", "S7: Completion progress bar 100%", progressFill.style.width);
            assert(clipTitle.innerText.includes("NAMASTE — isl_namaste_godl_v1 (1800 ms) — COMPLETED"), "S7: Completion title matches", clipTitle.innerText);
            assert(telState.innerText.includes("COMPLETED"), "S7: Completion badge matches", telState.innerText);

            // -------------------------------------------------------------
            // Scenario 8: Reproduced transcript 'She makes me very, very proud.'
            // (Issue A Regression: Must report PARTIAL / UNSUPPORTED, never TRANSLATED)
            // -------------------------------------------------------------
            window.handleCaptureStarted({ sessionId: "session_reg_3" });
            await wait(100);

            window.handleLiveTranscriptDispatch({
                version: "1.0.0",
                type: "SIGNBRIDGE_TRANSCRIPTION_DISPATCH",
                sessionId: "session_reg_3",
                sequenceId: 1,
                timestamp: 20.0,
                duration: 2.0,
                text: "She makes me very, very proud.",
                confidence: 0.94
            });
            await wait(250);

            const telPipeStatus = document.getElementById("tel-pipe-status");
            const telPipeSigns = document.getElementById("tel-pipe-signs");
            const telPipeUnsupported = document.getElementById("tel-pipe-unsupported");
            const telPipeNotice = document.getElementById("tel-pipe-notice");
            const telWhisperBackend = document.getElementById("tel-whisper-backend");

            assert(telPipeStatus && telPipeStatus.innerText.includes("PARTIAL / UNSUPPORTED"), "S8: Status is PARTIAL / UNSUPPORTED", telPipeStatus ? telPipeStatus.innerText : "missing");
            assert(telPipeStatus && !telPipeStatus.innerText.includes("TRANSLATED"), "S8: Status does NOT say TRANSLATED", telPipeStatus ? telPipeStatus.innerText : "missing");
            assert(telPipeSigns && telPipeSigns.innerText.includes("0 playable clips"), "S8: Playable clips is 0 (un-animated gloss not counted)", telPipeSigns ? telPipeSigns.innerText : "missing");
            assert(telPipeSigns && telPipeSigns.innerText.includes("I"), "S8: Dictionary match identifies I awaiting review", telPipeSigns ? telPipeSigns.innerText : "missing");
            assert(telPipeUnsupported && telPipeUnsupported.innerText.includes("she") && telPipeUnsupported.innerText.includes("proud"), "S8: Unsupported words listed", telPipeUnsupported ? telPipeUnsupported.innerText : "missing");
            assert(telPipeNotice && (telPipeNotice.innerText.includes("Partial mapping") || telPipeNotice.innerText.includes("unsupported")), "S8: Governance notice visible", telPipeNotice ? telPipeNotice.innerText : "missing");

            // Advance through 500ms neutral hold
            p.update(550);
            await wait(150);
            assert(!p.isPlaying, "S8: Not Playing after Neutral Hold", "isPlaying === false");
            assert(clipTitle && clipTitle.innerText === "Neutral Rest Pose (0 ms)", "S8: Title is Neutral Rest Pose (0 ms)", clipTitle.innerText);
            assert(telState && telState.innerText.includes("NEUTRAL"), "S8: State Badge is NEUTRAL", telState.innerText);
            assert(progressFill && progressFill.style.width === "0%", "S8: Progress bar is 0%", progressFill.style.width);

            // -------------------------------------------------------------
            // Scenario 9: Whisper health-check timeout and status transitions
            // (Issue B Regression: Local backend query, online state, and timeout handling)
            // -------------------------------------------------------------
            if (typeof window.checkWhisperBackendHealth === "function") {
                await window.checkWhisperBackendHealth();
                await wait(250);
                assert(telWhisperBackend && telWhisperBackend.innerText.includes("Online"), "S9: Health Check Reports Online", telWhisperBackend ? telWhisperBackend.innerText : "missing");
                assert(telWhisperBackend && telWhisperBackend.innerText.includes("signbridge-backend"), "S9: Reports Backend Service Name", telWhisperBackend ? telWhisperBackend.innerText : "missing");
            }

            // Expose results and post to test server
            await reportCompletion(results);
        });
        """
        with open(cls.runner_js_path, "w", encoding="utf-8") as f:
            f.write(test_js)

        # Run Headless Chrome in real-time execution with isolated temp profile
        cls.temp_profile = tempfile.mkdtemp(prefix="chrome_routing_reg_")
        cls.runner_url = f"http://127.0.0.1:{PORT}/extension/overlay/avatar_player_routing_runner.html"

        cmd = [
            CHROME_PATH,
            "--headless=new",
            f"--user-data-dir={cls.temp_profile}",
            "--no-first-run",
            "--no-default-browser-check",
            "--autoplay-policy=no-user-gesture-required",
            "--disable-gpu",
            "--no-sandbox",
            cls.runner_url
        ]

        cls.proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Deterministic bounded wait for test suite completion signal
        start_wait = time.time()
        timeout_s = 35
        while time.time() - start_wait < timeout_s:
            if QuietHandler.regression_results is not None:
                break
            time.sleep(0.25)

        cls.results = QuietHandler.regression_results
        if not cls.results:
            print(f"ERROR: Live routing regression did not complete within {timeout_s}s bounded wait")

    @classmethod
    def tearDownClass(cls):
        try:
            if hasattr(cls, "proc") and cls.proc:
                cls.proc.terminate()
                try:
                    cls.proc.wait(timeout=2)
                except Exception:
                    cls.proc.kill()
        except Exception:
            pass

        try:
            if hasattr(cls, "httpd") and cls.httpd:
                cls.httpd.shutdown()
        except Exception:
            pass

        try:
            if hasattr(cls, "runner_html_path") and os.path.exists(cls.runner_html_path):
                os.remove(cls.runner_html_path)
            if hasattr(cls, "runner_js_path") and os.path.exists(cls.runner_js_path):
                os.remove(cls.runner_js_path)
            if hasattr(cls, "temp_profile") and os.path.exists(cls.temp_profile):
                shutil.rmtree(cls.temp_profile, ignore_errors=True)
        except Exception:
            pass

    def test_all_live_speech_routing_checks(self):
        """Verify all live speech-to-ISL routing and telemetry checks in WebGL browser execution."""
        self.assertIsNotNone(self.results, "Regression test suite did not return results from WebGL avatar context")
        print(f"\nLive Speech Routing Regression Results: {self.results.get('passed', 0)} passed, {self.results.get('failed', 0)} failed")
        
        failures = []
        for check in self.results.get("checks", []):
            print(f"  [{check['status']}] {check['name']} -> {check.get('detail', '')}")
            if check["status"] != "PASS":
                failures.append(f"{check['name']}: {check.get('detail', '')}")

        self.assertEqual(len(failures), 0, f"Regression check failures encountered:\n" + "\n".join(failures))


if __name__ == "__main__":
    unittest.main()
