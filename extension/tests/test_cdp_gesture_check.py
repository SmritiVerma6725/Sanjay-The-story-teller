import subprocess
import time
import os
import sys
import json
import urllib.request
import urllib.error
import asyncio

# Let's test standard library websocket using raw socket or asyncio
import socket
import hashlib
import base64

def simple_websocket_client(ws_url):
    # Parse ws://localhost:9222/devtools/page/...
    from urllib.parse import urlparse
    parsed = urlparse(ws_url)
    host = parsed.hostname
    port = parsed.port or 80
    path = parsed.path
    if parsed.query:
        path += "?" + parsed.query

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))

    sec_key = base64.b64encode(os.urandom(16)).decode('utf-8')
    handshake = (
        f"GET {path} HTTP/1.1\r\n"
        f"Host: {host}:{port}\r\n"
        f"Upgrade: websocket\r\n"
        f"Connection: Upgrade\r\n"
        f"Sec-WebSocket-Key: {sec_key}\r\n"
        f"Sec-WebSocket-Version: 13\r\n\r\n"
    )
    s.sendall(handshake.encode())
    resp = s.recv(4096).decode()
    if "101" not in resp:
        raise Exception(f"WebSocket handshake failed: {resp}")

    return s

def send_cdp_cmd(s, cmd_id, method, params=None):
    payload = json.dumps({"id": cmd_id, "method": method, "params": params or {}}).encode('utf-8')
    # Build standard unmasked/masked frame (client must mask)
    frame = bytearray()
    frame.append(0x81) # FIN + text opcode
    length = len(payload)
    mask = os.urandom(4)
    if length <= 125:
        frame.append(0x80 | length)
    elif length <= 65535:
        frame.append(0x80 | 126)
        frame.extend(length.to_bytes(2, 'big'))
    else:
        frame.append(0x80 | 127)
        frame.extend(length.to_bytes(8, 'big'))
    frame.extend(mask)
    masked_payload = bytearray(b ^ mask[i % 4] for i, b in enumerate(payload))
    frame.extend(masked_payload)
    s.sendall(frame)

def recv_cdp_resp(s, timeout=5):
    s.settimeout(timeout)
    data = bytearray()
    while True:
        chunk = s.recv(4096)
        if not chunk:
            break
        data.extend(chunk)
        # Parse frame
        if len(data) >= 2:
            payload_len = data[1] & 0x7F
            offset = 2
            if payload_len == 126:
                if len(data) < 4: continue
                payload_len = int.from_bytes(data[2:4], 'big')
                offset = 4
            elif payload_len == 127:
                if len(data) < 10: continue
                payload_len = int.from_bytes(data[2:10], 'big')
                offset = 10
            
            if len(data) >= offset + payload_len:
                payload = data[offset:offset+payload_len]
                return json.loads(payload.decode('utf-8', errors='replace'))

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
PROFILE_DIR = os.path.abspath("scratch_cdp_profile")
EXT_DIR = os.path.abspath("extension")

print("Launching Chrome...")
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
    # Query targets
    req = urllib.request.urlopen("http://127.0.0.1:9222/json/list")
    targets = json.loads(req.read().decode())
    
    sw_target = None
    yt_target = None
    for t in targets:
        if t.get('type') == 'service_worker' and 'fignfifoniblkonapihmkfakmlgkbkcf' in t.get('url', ''):
            sw_target = t
        if 'youtube' in t.get('url', ''):
            yt_target = t

    print("Found SW target:", sw_target is not None)
    print("Found YouTube target:", yt_target is not None)

    if sw_target:
        ws_url = sw_target['webSocketDebuggerUrl']
        print(f"Connecting to SW WebSocket: {ws_url}")
        s = simple_websocket_client(ws_url)
        
        # Test evaluating chrome.tabCapture.getMediaStreamId directly in SW
        expr = """
        (async () => {
            try {
                const tabs = await chrome.tabs.query({});
                const ytTab = tabs.find(t => t.url && t.url.includes('youtube'));
                if (!ytTab) return { error: 'No YouTube tab found in chrome.tabs' };
                try {
                    const streamId = await chrome.tabCapture.getMediaStreamId({ targetTabId: ytTab.id });
                    return { ok: true, streamId, tabId: ytTab.id };
                } catch (e) {
                    return { error: e.name + ': ' + e.message, tabId: ytTab.id };
                }
            } catch (err) {
                return { error: err.toString() };
            }
        })()
        """
        send_cdp_cmd(s, 1, "Runtime.evaluate", {"expression": expr, "awaitPromise": True, "returnByValue": True})
        resp = recv_cdp_resp(s)
        print("\n--- Direct SW tabCapture Evaluation Result ---")
        print(json.dumps(resp, indent=2))
        s.close()

finally:
    print("\nCleaning up...")
    proc.terminate()
    try:
        proc.wait(timeout=3)
    except:
        proc.kill()
