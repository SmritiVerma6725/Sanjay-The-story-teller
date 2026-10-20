import subprocess
import time
import os
import sys
import json
import urllib.request
import socket
import base64

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
PROFILE_DIR = os.path.abspath("scratch_cdp_profile")
EXT_DIR = os.path.abspath("extension")

proc = subprocess.Popen([
    CHROME_PATH,
    "--remote-debugging-port=9222",
    f"--user-data-dir={PROFILE_DIR}",
    f"--load-extension={EXT_DIR}",
    "--autoplay-policy=no-user-gesture-required",
    "--no-first-run",
    "--no-default-browser-check",
    "chrome://extensions/"
], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def send_recv(s, cmd_id, method, params=None):
    payload = json.dumps({"id": cmd_id, "method": method, "params": params or {}}).encode('utf-8')
    frame = bytearray([0x81])
    length = len(payload)
    mask = b'\xaa\xbb\xcc\xdd'
    if length <= 125:
        frame.append(0x80 | length)
    elif length <= 65535:
        frame.append(0x80 | 126)
        frame.extend(length.to_bytes(2, 'big'))
    else:
        frame.append(0x80 | 127)
        frame.extend(length.to_bytes(8, 'big'))
    frame.extend(mask)
    frame.extend(bytes(b ^ mask[i % 4] for i, b in enumerate(payload)))
    s.sendall(frame)

    s.settimeout(10)
    data = bytearray()
    while True:
        chunk = s.recv(65536)
        if not chunk:
            break
        data.extend(chunk)
        if len(data) >= 2:
            l = data[1] & 0x7f
            offset = 2
            if l == 126:
                if len(data) < 4: continue
                l = int.from_bytes(data[2:4], 'big')
                offset = 4
            elif l == 127:
                if len(data) < 10: continue
                l = int.from_bytes(data[2:10], 'big')
                offset = 10
            if len(data) >= offset + l:
                return json.loads(data[offset:offset+l].decode('utf-8', errors='replace'))

try:
    time.sleep(3)
    req = urllib.request.urlopen("http://127.0.0.1:9222/json/list")
    targets = json.loads(req.read().decode())
    ext_page = next((t for t in targets if 'extensions' in t.get('url', '')), None)
    print("Found extensions page:", ext_page)
    
    if ext_page:
        from urllib.parse import urlparse
        parsed = urlparse(ext_page['webSocketDebuggerUrl'])
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((parsed.hostname, parsed.port))
        sec_key = base64.b64encode(os.urandom(16)).decode('utf-8')
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
        time.sleep(1)

        # Capture screenshot of chrome://extensions/
        res = send_recv(s, 1, "Page.captureScreenshot", {"format": "png"})
        b64 = res.get('result', {}).get('data', '')
        if b64:
            img_data = base64.b64decode(b64)
            out_path = r"C:\Users\user\.gemini\antigravity-ide\brain\9466be36-35d0-42ba-86d7-83fc583b0849\chrome_extensions_page.png"
            with open(out_path, "wb") as f:
                f.write(img_data)
            print(f"Extensions page screenshot saved to: {out_path} ({len(img_data)} bytes)")

finally:
    proc.terminate()
    try: proc.wait(3)
    except: proc.kill()
