import http.server
import socketserver
import threading
import subprocess
import time
import os
import sys
import re
import json
import struct

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

PORT = 8089
DIRECTORY = os.path.abspath("extension")

def test_manifest_and_assets():
    print("\n=== Manifest & Static Asset Verification ===")
    manifest_path = os.path.join(DIRECTORY, "manifest.json")
    assert os.path.exists(manifest_path), "manifest.json missing"
    
    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)
        
    assert manifest.get("manifest_version") == 3, "Must be Manifest V3"
    print("  âœ” PASS: manifest_version is 3")
    
    expected_permissions = {"tabCapture", "offscreen", "activeTab", "storage", "scripting"}
    actual_permissions = set(manifest.get("permissions", []))
    assert expected_permissions.issubset(actual_permissions), f"Missing permissions: {expected_permissions - actual_permissions}"
    print(f"  âœ” PASS: permissions verified ({', '.join(manifest.get('permissions'))})")
    
    expected_hosts = ["*://*.youtube.com/*", "http://127.0.0.1:8765/*"]
    for host in expected_hosts:
        assert host in manifest.get("host_permissions", []), f"Missing host permission: {host}"
    print(f"  âœ” PASS: host_permissions verified ({', '.join(manifest.get('host_permissions'))})")
    
    assert manifest.get("action", {}).get("default_popup") == "popup.html", "default_popup must be popup.html"
    assert os.path.exists(os.path.join(DIRECTORY, "popup.html")), "popup.html missing"
    assert os.path.exists(os.path.join(DIRECTORY, "popup.js")), "popup.js missing"
    assert os.path.exists(os.path.join(DIRECTORY, "popup.css")), "popup.css missing"
    assert os.path.exists(os.path.join(DIRECTORY, "offscreen.html")), "offscreen.html missing"
    assert os.path.exists(os.path.join(DIRECTORY, "offscreen.js")), "offscreen.js missing"
    assert os.path.exists(os.path.join(DIRECTORY, "background.js")), "background.js missing"
    print("  âœ” PASS: all declared files exist on disk")
    
    for size in [16, 48, 128]:
        icon_path = os.path.join(DIRECTORY, "icons", f"icon-{size}.png")
        assert os.path.exists(icon_path), f"icon-{size}.png missing"
        with open(icon_path, "rb") as f:
            header = f.read(24)
            assert header[:8] == b'\x89PNG\r\n\x1a\n', f"Invalid PNG header for icon-{size}.png"
            w, h = struct.unpack(">II", header[16:24])
            assert w == size and h == size, f"Icon dimension mismatch: expected {size}x{size}, got {w}x{h}"
        print(f"  âœ” PASS: icon-{size}.png verified ({size}x{size} PNG)")

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)
    def log_message(self, format, *args):
        pass

def start_server():
    with socketserver.TCPServer(("127.0.0.1", PORT), Handler) as httpd:
        httpd.serve_forever()

if __name__ == "__main__":
    test_manifest_and_assets()

    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()
    time.sleep(1)

    chrome_path = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
    test_suites = [
        ("M1 Audio Capture & Shell Suite", f"http://127.0.0.1:{PORT}/tests/test_m1_suite.html"),
        ("M2 Speech Recognition & Queue Suite", f"http://127.0.0.1:{PORT}/tests/test_m2_suite.html"),
        ("M3 Phase 3.1 Data Contracts Suite", f"http://127.0.0.1:{PORT}/tests/test_m3_suite.html")
    ]

    total_all = 0
    passed_all = 0
    failed_all = 0

    for suite_title, test_url in test_suites:
        print(f"\n==========================================")
        print(f"Executing Chrome In-Engine: {suite_title}")
        print(f"==========================================")

        budget = '60000' if 'm3' in test_url else '10000'
        cmd = [
            chrome_path,
            '--headless=new',
            f'--virtual-time-budget={budget}',
            '--dump-dom',
            test_url
        ]

        res = subprocess.run(cmd, capture_output=True, text=True)
        html = res.stdout
        results_match = re.search(r'<div id="results">(.*?)</div>\s*<div id="summary">(.*?)</div>', html, re.DOTALL)
        if results_match:
            results_html = results_match.group(1)
            summary_html = results_match.group(2)

            tests = re.findall(r'<div class="(suite|test)">(.*?)</div>', results_html)
            for cls, content in tests:
                clean = re.sub(r'<[^>]+>', '', content).strip()
                if cls == 'suite':
                    print(f"\n{clean}")
                else:
                    print(f"  {clean}")

            clean_summary = re.sub(r'<[^>]+>', '', summary_html).strip()
            print(f"\n{clean_summary}")

            numbers = re.findall(r'(\d+)\s+(total|PASSED|FAILED)', clean_summary)
            for num, kind in numbers:
                val = int(num)
                if kind == 'total': total_all += val
                elif kind == 'PASSED': passed_all += val
                elif kind == 'FAILED': failed_all += val
        else:
            print("Could not find results block in DOM output for:", test_url)

    print("\n========================================================")
    print(f"OVERALL IN-ENGINE TEST SUMMARY: {total_all} Total | {passed_all} PASSED | {failed_all} FAILED")
    print("========================================================")
    if failed_all > 0:
        sys.exit(1)
