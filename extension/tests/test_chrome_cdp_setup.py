import subprocess
import time
import os
import sys
import json
import urllib.request
import urllib.error

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
EXT_DIR = os.path.abspath("extension")
PROFILE_DIR = os.path.abspath("scratch_cdp_profile")

if not os.path.exists(PROFILE_DIR):
    os.makedirs(PROFILE_DIR)

print(f"Launching Chrome with profile: {PROFILE_DIR}")
print(f"Extension directory: {EXT_DIR}")

# Launch Chrome with debugging port
chrome_proc = subprocess.Popen([
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
    # 1. Poll /json/version
    version_data = None
    for attempt in range(15):
        time.sleep(1)
        try:
            req = urllib.request.urlopen("http://127.0.0.1:9222/json/version", timeout=2)
            version_data = json.loads(req.read().decode())
            print(f"Connected to Chrome remote debugging! Browser: {version_data.get('Browser')}")
            break
        except Exception as e:
            print(f"Waiting for Chrome debug port (attempt {attempt+1}/15)...")

    if not version_data:
        print("ERROR: Failed to connect to Chrome port 9222.")
        sys.exit(1)

    # 2. Query /json/list to inspect targets
    req = urllib.request.urlopen("http://127.0.0.1:9222/json/list", timeout=2)
    targets = json.loads(req.read().decode())
    print(f"\nDiscovered {len(targets)} debug targets:")
    
    extension_id = None
    service_worker_target = None
    for t in targets:
        print(f" - [{t.get('type')}] {t.get('title')} ({t.get('url')})")
        if t.get('type') == 'service_worker' and 'chrome-extension://' in t.get('url', ''):
            service_worker_target = t
            # url is chrome-extension://<id>/background.js
            extension_id = t.get('url').split('/')[2]

    print(f"\nActual Extension ID: {extension_id}")
    if not extension_id:
        print("WARNING: Extension service worker not found in target list.")

finally:
    print("Terminating Chrome test process...")
    chrome_proc.terminate()
    try:
        chrome_proc.wait(timeout=5)
    except Exception:
        chrome_proc.kill()
