import subprocess
import time
import os
import sys
import json
import urllib.request
import socket
import hashlib
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
    "https://www.youtube.com/watch?v=jNQXAC9IVRw"
], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

try:
    time.sleep(3)
    req = urllib.request.urlopen("http://127.0.0.1:9222/json/list")
    targets = json.loads(req.read().decode())
    sw_target = next((t for t in targets if t.get('type') == 'service_worker' and 'fignfifoniblkonapihmkfakmlgkbkcf' in t.get('url', '')), None)
    
    if sw_target:
        from urllib.parse import urlparse
        parsed = urlparse(sw_target['webSocketDebuggerUrl'])
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
        print("Handshake response headers:\n", resp.decode(errors='replace'))
        
        # Now send Runtime.evaluate
        payload = json.dumps({"id": 1, "method": "Runtime.evaluate", "params": {"expression": "chrome.runtime.getManifest()", "returnByValue": True}}).encode('utf-8')
        frame = bytearray([0x81, 0x80 | len(payload)])
        mask = b'\x12\x34\x56\x78'
        frame.extend(mask)
        frame.extend(bytes(b ^ mask[i % 4] for i, b in enumerate(payload)))
        s.sendall(frame)
        
        s.settimeout(5)
        raw_resp = s.recv(4096)
        print("Raw frame response:\n", raw_resp)
        # Parse unmasked server frame
        if len(raw_resp) >= 2:
            length = raw_resp[1] & 0x7f
            offset = 2
            if length == 126:
                offset = 4
                length = int.from_bytes(raw_resp[2:4], 'big')
            body = raw_resp[offset:offset+length]
            print("Decoded body:", body.decode(errors='replace'))

finally:
    proc.terminate()
    try: proc.wait(3)
    except: proc.kill()
