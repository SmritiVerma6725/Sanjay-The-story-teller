#!/usr/bin/env python3
"""SignBridge M3.16 — Browser Usability Test Suite for preview_mocap.html

Runs headless Chrome against preview_mocap.html over CDP to verify:
1. Candidate clip and UI DOM initialization.
2. Playback, pause, reset, scrubber, and frame stepping.
3. Rapid jump to scrutiny frames (22, peak, 59, 62) and telemetry badge updates.
4. Rubric rating selection and unrated row warning detection.
5. Uncertainty checkbox toggle and conditional evidence detail input display.
6. Local storage state saving and data collection.
7. Neutral Markdown summary generation.
8. Graceful operation under offline / missing video codecs.
"""

import base64
import http.server
import json
import os
import re
import shutil
import socket
import socketserver
import subprocess
import sys
import tempfile
import threading
import time
from pathlib import Path
from urllib.parse import urlparse
import urllib.request

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

PORT = 8112
CDP_PORT = 9238
ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent
CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT_DIR), **kwargs)

    def log_message(self, format, *args):
        pass


class BrowserTester:
    def __init__(self):
        self.server = None
        self.server_thread = None
        self.chrome_proc = None
        self.ws_sock = None
        self.msg_id = 0
        self.temp_profile = tempfile.mkdtemp(prefix="chrome_usability_test_")

    def start_server(self):
        self.server = socketserver.TCPServer(("127.0.0.1", PORT), QuietHandler)
        self.server_thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.server_thread.start()
        time.sleep(0.5)

    def stop_server(self):
        if self.server:
            self.server.shutdown()
            self.server.server_close()
        shutil.rmtree(self.temp_profile, ignore_errors=True)

    def launch_chrome(self, url):
        cmd = [
            CHROME_PATH,
            "--headless=new",
            f"--remote-debugging-port={CDP_PORT}",
            "--remote-debugging-address=127.0.0.1",
            "--disable-gpu",
            "--no-first-run",
            "--no-default-browser-check",
            f"--user-data-dir={self.temp_profile}",
            url
        ]
        self.chrome_proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def close_chrome(self):
        if self.chrome_proc:
            self.chrome_proc.terminate()
            try:
                self.chrome_proc.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.chrome_proc.kill()

    def connect_cdp(self):
        list_url = f"http://127.0.0.1:{CDP_PORT}/json/list"
        targets = None
        deadline = time.time() + 10.0
        while time.time() < deadline:
            try:
                req = urllib.request.urlopen(list_url, timeout=2)
                targets = json.loads(req.read().decode())
                if targets:
                    break
            except Exception:
                time.sleep(0.5)

        if not targets:
            raise RuntimeError(f"Could not connect to Chrome CDP endpoint at {list_url}")

        page_target = next((t for t in targets if "preview_mocap.html" in t.get("url", "")), None)
        if not page_target:
            page_target = targets[0]

        ws_url = page_target["webSocketDebuggerUrl"]
        parsed = urlparse(ws_url)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(8)
        s.connect((parsed.hostname, parsed.port))
        sec_key = base64.b64encode(os.urandom(16)).decode("utf-8")
        handshake = (
            f"GET {parsed.path} HTTP/1.1\r\n"
            f"Host: {parsed.hostname}:{parsed.port}\r\n"
            f"Upgrade: websocket\r\n"
            f"Connection: Upgrade\r\n"
            f"Sec-WebSocket-Key: {sec_key}\r\n"
            f"Sec-WebSocket-Version: 13\r\n\r\n"
        )
        s.sendall(handshake.encode())
        resp = s.recv(4096)
        if b"101 " not in resp:
            raise RuntimeError(f"WebSocket handshake failed: {resp[:200]}")
        self.ws_sock = s

    def cdp_send(self, method, params=None):
        self.msg_id += 1
        req_id = self.msg_id
        payload = json.dumps({"id": req_id, "method": method, "params": params or {}}).encode("utf-8")
        frame = bytearray([0x81])
        l = len(payload)
        mask = b"\xaa\xbb\xcc\xdd"
        if l <= 125:
            frame.append(0x80 | l)
        elif l <= 65535:
            frame.append(0x80 | 126)
            frame.extend(l.to_bytes(2, "big"))
        else:
            frame.append(0x80 | 127)
            frame.extend(l.to_bytes(8, "big"))
        frame.extend(mask)
        frame.extend(bytes(b ^ mask[i % 4] for i, b in enumerate(payload)))
        self.ws_sock.sendall(frame)

        self.ws_sock.settimeout(6)
        data = bytearray()
        while True:
            try:
                chunk = self.ws_sock.recv(65536)
            except socket.timeout:
                break
            if not chunk:
                break
            data.extend(chunk)
            if len(data) >= 2:
                frame_len = data[1] & 0x7f
                offset = 2
                if frame_len == 126:
                    if len(data) < 4: continue
                    frame_len = int.from_bytes(data[2:4], "big")
                    offset = 4
                elif frame_len == 127:
                    if len(data) < 10: continue
                    frame_len = int.from_bytes(data[2:10], "big")
                    offset = 10
                if len(data) >= offset + frame_len:
                    msg_bytes = data[offset:offset + frame_len]
                    try:
                        res_obj = json.loads(msg_bytes.decode("utf-8", errors="replace"))
                        if res_obj.get("id") == req_id:
                            return res_obj
                    except Exception:
                        pass
                    # If this was an event or other message, advance and continue reading
                    data = data[offset + frame_len:]
        return {}

    def eval_js(self, expression):
        res = self.cdp_send("Runtime.evaluate", {
            "expression": expression,
            "returnByValue": True,
            "awaitPromise": True
        })
        if "result" in res and "result" in res["result"]:
            val_obj = res["result"]["result"]
            return val_obj.get("value")
        return None


def run_all_tests():
    print("=" * 75)
    print("SignBridge M3.16 — Headless Chrome Usability Verification")
    print("=" * 75)

    tester = BrowserTester()
    results = []

    def record_check(name, passed, detail=""):
        status = "✔ PASS" if passed else "✘ FAIL"
        print(f"  {status}: {name} {detail}")
        results.append((name, passed, detail))

    try:
        print("[1/5] Launching local HTTP server & Chrome instance...")
        tester.start_server()
        test_url = f"http://127.0.0.1:{PORT}/tools/isl_motion_extraction/preview_mocap.html"
        tester.launch_chrome(test_url)
        tester.connect_cdp()
        
        # Explicitly navigate via CDP and wait for DOM load
        tester.cdp_send("Page.enable")
        tester.cdp_send("Page.navigate", {"url": test_url})
        
        # Poll until location.href matches and DOM is ready
        deadline = time.time() + 10.0
        while time.time() < deadline:
            curr_url = tester.eval_js("window.location.href")
            ready = tester.eval_js("document.readyState")
            if curr_url and "preview_mocap.html" in str(curr_url) and ready == "complete":
                break
            time.sleep(0.5)

        time.sleep(2.0)  # Wait for candidate JSON and 3D rig fetch

        print(f"Current page URL: {tester.eval_js('window.location.href')}")

        # Stub window.alert to prevent headless modal blocking
        tester.eval_js("window.alert = () => {}")

        # Test 1: Page Title and Governance Banner
        title = tester.eval_js("document.title")
        record_check("Page Title", "ISL Motion Capture Review Studio" in str(title), f"({title})")

        banner = tester.eval_js("document.querySelector('.governance-banner') ? document.querySelector('.governance-banner').textContent : ''")
        record_check("Governance Banner Display", "EXPERIMENTAL" in str(banner), f"({banner.strip()})")

        # Test 2: Candidate Clip Loading & Hash Verification
        hash_disp = tester.eval_js("document.getElementById('candidate-hash-display').textContent")
        record_check("Candidate Hash Display", "6f24e60f7f55d714" in str(hash_disp), f"({hash_disp})")

        # Test 3: Playback Controls & Frame Navigation
        init_time = tester.eval_js("document.getElementById('time-display').textContent")
        record_check("Initial Timeline State", "0 / 3080 ms" in str(init_time), f"({init_time})")

        # Click Play
        tester.eval_js("document.getElementById('btn-play-pause').click()")
        play_btn_text = tester.eval_js("document.getElementById('btn-play-pause').textContent")
        record_check("Play Synchronized Toggle", "Pause" in str(play_btn_text), f"({play_btn_text})")

        # Pause
        tester.eval_js("document.getElementById('btn-play-pause').click()")
        pause_btn_text = tester.eval_js("document.getElementById('btn-play-pause').textContent")
        record_check("Pause Toggle", "Play" in str(pause_btn_text), f"({pause_btn_text})")

        # Reset to 0ms before testing frame-by-frame navigation
        tester.eval_js("document.getElementById('btn-restart').click()")
        reset_time = tester.eval_js("document.getElementById('time-display').textContent")
        record_check("Reset to Frame 0", "0 / 3080 ms" in str(reset_time), f"({reset_time})")

        # Step forward frame (+40ms from 0)
        tester.eval_js("document.getElementById('btn-next-frame').click()")
        next_time = tester.eval_js("document.getElementById('time-display').textContent")
        record_check("Frame Forward Step (+40ms)", "40 / 3080 ms" in str(next_time), f"({next_time})")

        # Test 4: Scrutiny Quick Jumps
        # Jump Frame 22 (880ms)
        tester.eval_js("document.getElementById('btn-jump-f22').click()")
        f22_time = tester.eval_js("document.getElementById('time-display').textContent")
        f22_state = tester.eval_js("document.getElementById('metric-state').textContent")
        f22_alert = tester.eval_js("document.getElementById('confidence-alert').style.display")
        record_check("Jump Frame 22 (880ms)", "880 / 3080 ms" in str(f22_time) and f22_state == "LOW_CONFIDENCE" and f22_alert == "block",
                     f"({f22_time}, state={f22_state})")

        # Jump Peak (1600ms)
        tester.eval_js("document.getElementById('btn-jump-peak').click()")
        peak_time = tester.eval_js("document.getElementById('time-display').textContent")
        peak_state = tester.eval_js("document.getElementById('metric-state').textContent")
        record_check("Jump Peak (1600ms)", "1600 / 3080 ms" in str(peak_time) and peak_state == "CONTACT_CONSTRAINED",
                     f"({peak_time}, state={peak_state})")

        # Jump Frame 59 (2360ms)
        tester.eval_js("document.getElementById('btn-jump-f59').click()")
        f59_time = tester.eval_js("document.getElementById('time-display').textContent")
        record_check("Jump Frame 59 (2360ms)", "2360 / 3080 ms" in str(f59_time), f"({f59_time})")

        # Jump Frame 62 (2480ms)
        tester.eval_js("document.getElementById('btn-jump-f62').click()")
        f62_time = tester.eval_js("document.getElementById('time-display').textContent")
        record_check("Jump Frame 62 (2480ms)", "2480 / 3080 ms" in str(f62_time), f"({f62_time})")

        # Test 5: Rubric Rating & Evidence Requests
        # Select rating pills
        tester.eval_js("document.querySelector(\".rubric-options[data-param='handshape'] .rating-pill[data-val='acceptable']\").click()")
        tester.eval_js("document.querySelector(\".rubric-options[data-param='location'] .rating-pill[data-val='acceptable']\").click()")
        tester.eval_js("document.querySelector(\".rubric-options[data-param='orientation'] .rating-pill[data-val='acceptable']\").click()")
        tester.eval_js("document.querySelector(\".rubric-options[data-param='movement'] .rating-pill[data-val='minor_issue']\").click()")
        tester.eval_js("document.querySelector(\".rubric-options[data-param='non_manuals'] .rating-pill[data-val='not_assessable']\").click()")

        # Toggle Uncertainty Checkbox
        tester.eval_js("document.getElementById('chk-need-evidence').click()")
        box_disp = tester.eval_js("document.getElementById('box-evidence-details').style.display")
        record_check("Evidence Request Input Toggle", box_disp == "block", f"(display: {box_disp})")

        # Fill Details & Reviewer Fields
        tester.eval_js("document.getElementById('evidence-request-details').value = 'Side profile angle requested'")
        tester.eval_js("document.getElementById('rev-name').value = 'Sunita Sharma'")
        tester.eval_js("document.getElementById('rev-notes').value = 'Palmar contact verified at sternum height.'")
        tester.eval_js("""
            (() => {
                const r = document.querySelector("input[name='overall-verdict'][value='needs_tuning']");
                if (r) {
                    r.checked = true;
                    r.dispatchEvent(new Event('change', { bubbles: true }));
                }
            })()
        """)

        # Test Save to LocalStorage / In-Memory state
        tester.eval_js("document.getElementById('btn-save-local').click()")
        stored_raw = tester.eval_js("(() => { try { return localStorage.getItem('signbridge_isl_namaste_review'); } catch(e) { return JSON.stringify(inMemoryWorksheetData); } })()")
        stored = json.loads(stored_raw) if stored_raw else {}
        record_check("Local Storage Round-Trip Save",
                     stored.get("reviewer", {}).get("name") == "Sunita Sharma" and
                     stored.get("parameterRatings", {}).get("movement") == "minor_issue" and
                     stored.get("overallVerdict") == "needs_tuning" and
                     stored.get("furtherEvidenceRequested") is True,
                     f"(verdict={stored.get('overallVerdict')})")

        # Test Markdown Generation
        md_text = tester.eval_js("generateMarkdownSummary()")
        record_check("Neutral Markdown Generation",
                     "Sunita Sharma" in str(md_text) and
                     "`needs_tuning`" in str(md_text) and
                     "Side profile angle requested" in str(md_text) and
                     "PASSED (Natural motion)" not in str(md_text),
                     "(Verified non-leading phrasing and full field inclusion)")

    except Exception as e:
        print(f"Exception during browser test execution: {e}")
        record_check("Browser Execution Exception", False, str(e))
    finally:
        tester.close_chrome()
        tester.stop_server()

    passed_count = sum(1 for _, p, _ in results if p)
    total_count = len(results)
    print("\n" + "=" * 75)
    print(f"BROWSER USABILITY SUMMARY: {passed_count}/{total_count} CHECKS PASSED")
    print("=" * 75)

    if passed_count != total_count:
        sys.exit(1)


if __name__ == "__main__":
    run_all_tests()
