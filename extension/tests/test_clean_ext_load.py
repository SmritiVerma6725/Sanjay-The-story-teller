import subprocess
import time
import os
import sys
import json
import urllib.request

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
PROFILE_DIR = os.path.abspath("clean_test_profile")
EXT_DIR = os.path.abspath("extension")

if not os.path.exists(PROFILE_DIR):
    os.makedirs(PROFILE_DIR)

cmd = [
    CHROME_PATH,
    "--remote-debugging-port=9222",
    f"--user-data-dir={PROFILE_DIR}",
    f"--disable-extensions-except={EXT_DIR}",
    f"--load-extension={EXT_DIR}",
    "--no-first-run",
    "--no-default-browser-check",
    "about:blank"
]
print("Running command:", " ".join(cmd))
proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

try:
    time.sleep(3)
    req = urllib.request.urlopen("http://127.0.0.1:9222/json/list")
    targets = json.loads(req.read().decode())
    print(f"\nTargets in clean profile ({len(targets)}):")
    for t in targets:
        print(f" - [{t.get('type')}] title='{t.get('title')}' url='{t.get('url')}'")

finally:
    proc.terminate()
    try: proc.wait(3)
    except: proc.kill()
