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
    "https://www.youtube.com/watch?v=jNQXAC9IVRw"
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
    # Open avatar player inside the extension context
    ext_url = "chrome-extension://fignfifoniblkonapihmkfakmlgkbkcf/overlay/avatar_player.html"
    req_obj = urllib.request.Request(f"http://127.0.0.1:9222/json/new?{ext_url}", method="PUT")
    avatar_target = json.loads(urllib.request.urlopen(req_obj).read().decode())
    print("Avatar target:", avatar_target)
    time.sleep(2)

    from urllib.parse import urlparse
    parsed = urlparse(avatar_target['webSocketDebuggerUrl'])
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

    # Check chrome.runtime in extension origin avatar player
    check_ext = send_recv(s, 1, "Runtime.evaluate", {
        "expression": "typeof chrome !== 'undefined' && typeof chrome.runtime !== 'undefined' && typeof chrome.runtime.sendMessage === 'function'",
        "returnByValue": True
    })
    print("\nHas chrome.runtime in extension avatar player page:", check_ext)

    # Query capture state via chrome.runtime.sendMessage
    get_state = send_recv(s, 2, "Runtime.evaluate", {
        "expression": """
        new Promise(resolve => {
            chrome.runtime.sendMessage({ type: 'GET_CAPTURE_STATE' }, resp => {
                resolve({ ok: true, state: resp });
            });
        })
        """,
        "awaitPromise": True,
        "returnByValue": True
    })
    print("\nCapture State query from extension avatar player:", get_state)

    # Now let's test REQUEST_START_CAPTURE from extension avatar player!
    start_test = send_recv(s, 3, "Runtime.evaluate", {
        "expression": """
        new Promise(resolve => {
            chrome.runtime.sendMessage({ type: 'REQUEST_START_CAPTURE' }, resp => {
                resolve({ resp, lastError: chrome.runtime.lastError ? chrome.runtime.lastError.message : null });
            });
        })
        """,
        "awaitPromise": True,
        "returnByValue": True
    })
    print("\nREQUEST_START_CAPTURE response from extension context:", start_test)

finally:
    proc.terminate()
    try: proc.wait(3)
    except: proc.kill()
