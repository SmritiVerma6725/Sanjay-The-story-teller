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

print("Checking extension manifest.json in:", EXT_DIR)
with open(os.path.join(EXT_DIR, "manifest.json")) as f:
    print(f.read())

proc = subprocess.Popen([
    CHROME_PATH,
    "--remote-debugging-port=9222",
    f"--user-data-dir={PROFILE_DIR}",
    f"--load-extension={EXT_DIR}",
    "--autoplay-policy=no-user-gesture-required",
    "--no-first-run",
    "--no-default-browser-check",
    "about:blank"
], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

try:
    time.sleep(3)
    req = urllib.request.urlopen("http://127.0.0.1:9222/json/list")
    targets = json.loads(req.read().decode())
    print("\nAll Targets in Chrome:")
    for t in targets:
        print(f" - [{t.get('type')}] title='{t.get('title')}' url='{t.get('url')}'")

finally:
    proc.terminate()
    try: proc.wait(3)
    except: proc.kill()
