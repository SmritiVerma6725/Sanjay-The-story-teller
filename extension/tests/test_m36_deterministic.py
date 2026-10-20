import subprocess
import time
import os
import sys
import json
import urllib.request

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

CHROME_PATH = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
PORT = 8080
URL = f"http://localhost:{PORT}/overlay/avatar_player.html"

# Run chrome with a virtual time budget and dumped DOM evaluation
script_eval = """
window.addEventListener("load", async () => {
    const results = {};
    const wait = (ms) => new Promise(r => setTimeout(r, ms));
    await wait(800); // Allow player and model initialization

    // 1. Check Whisper Backend
    document.getElementById('btn-check-backend').click();
    await wait(1200);
    results.checkBackend = {
        backendText: document.getElementById('tel-whisper-backend').innerText
    };

    // 2. Click 'Hello'
    document.getElementById('btn-sample-hello').click();
    await wait(200);
    results.helloTest = {
        transcript: document.getElementById('tel-pipe-transcript').innerText,
        status: document.getElementById('tel-pipe-status').innerText,
        signs: document.getElementById('tel-pipe-signs').innerText,
        currentGloss: document.getElementById('tel-pipe-current-gloss').innerText,
        fallbackMode: document.getElementById('tel-pipe-fallback').innerText,
        playerState: document.getElementById('tel-state').innerText
    };

    // 3. Click 'Thank you'
    document.getElementById('btn-sample-thankyou').click();
    await wait(200);
    results.thankYouTest = {
        transcript: document.getElementById('tel-pipe-transcript').innerText,
        status: document.getElementById('tel-pipe-status').innerText,
        signs: document.getElementById('tel-pipe-signs').innerText,
        currentGloss: document.getElementById('tel-pipe-current-gloss').innerText,
        fallbackMode: document.getElementById('tel-pipe-fallback').innerText
    };

    // 4. Click 'Tech Motion + Hello (Combo)'
    document.getElementById('btn-sample-demo-combo').click();
    await wait(300); // During Tech Motion clip
    const phase1 = {
        signs: document.getElementById('tel-pipe-signs').innerText,
        activeGloss: document.getElementById('tel-pipe-current-gloss').innerText,
        fallbackMode: document.getElementById('tel-pipe-fallback').innerText,
        playerState: document.getElementById('tel-state').innerText
    };
    // Fast forward timeline by 2100ms
    if (window.player) {
        window.player.update(2100);
    }
    await wait(200); // Transitioned to HELLO neutral fallback
    const phase2 = {
        activeGloss: document.getElementById('tel-pipe-current-gloss').innerText,
        fallbackMode: document.getElementById('tel-pipe-fallback').innerText,
        playerState: document.getElementById('tel-state').innerText
    };
    results.comboTest = { phase1, phase2 };

    // 5. Select ASL and verify separation
    const sel = document.getElementById('select-target-lang');
    sel.value = 'ASL';
    sel.dispatchEvent(new Event('change'));
    document.getElementById('input-transcript').value = 'Hello welcome';
    document.getElementById('btn-translate-play').click();
    await wait(200);
    results.aslTest = {
        lang: document.getElementById('tel-pipe-lang').innerText,
        status: document.getElementById('tel-pipe-status').innerText,
        signs: document.getElementById('tel-pipe-signs').innerText,
        unsupported: document.getElementById('tel-pipe-unsupported').innerText,
        notice: document.getElementById('tel-pipe-notice').innerText
    };

    const outDiv = document.createElement('div');
    outDiv.id = 'm36-deterministic-results';
    outDiv.textContent = JSON.stringify(results);
    document.body.appendChild(outDiv);
})();
"""

html_page = urllib.request.urlopen(URL).read().decode('utf-8')
print("Successfully reached avatar player at:", URL)

# Create a temporary runner page that injects the deterministic test suite
runner_html_path = os.path.abspath("extension/overlay/avatar_player_m36_runner.html")
injected_html = html_page.replace("</body>", f"<script>{script_eval}</script></body>")
with open(runner_html_path, "w", encoding="utf-8") as f:
    f.write(injected_html)

try:
    cmd = [
        CHROME_PATH,
        '--headless=new',
        '--virtual-time-budget=10000',
        '--dump-dom',
        f"http://localhost:{PORT}/overlay/avatar_player_m36_runner.html"
    ]
    res = subprocess.run(cmd, capture_output=True, encoding='utf-8', errors='replace')
    dom = res.stdout

    import re
    match = re.search(r'<div id="m36-deterministic-results">(.*?)</div>', dom)
    if match:
        data = json.loads(match.group(1))
        print("\n=== M3.6 Deterministic Verification Results ===")
        print(json.dumps(data, indent=2))
        
        # Assertions
        # 1. Backend check
        assert "Online" in data["checkBackend"]["backendText"], "Whisper backend should report Online"
        print("✔ Check 1: Whisper Local Backend is ONLINE on port 8765")

        # 2. Hello fallback
        assert "HELLO" in data["helloTest"]["signs"], "HELLO sign should be identified"
        assert "Active (Held in Neutral" in data["helloTest"]["fallbackMode"], "HELLO must fall back to neutral rest pose"
        assert "FALLBACK NEUTRAL" in data["helloTest"]["playerState"], "Player state must be FALLBACK NEUTRAL"
        print("✔ Check 2: 'Hello' triggers seed dictionary match with safe NEUTRAL REST fallback")

        # 3. Thank you fallback
        assert "THANK_YOU" in data["thankYouTest"]["signs"], "THANK_YOU must match seed dictionary phrase"
        assert "Active (Held in Neutral" in data["thankYouTest"]["fallbackMode"], "THANK_YOU must fall back to neutral"
        print("✔ Check 3: 'Thank you' recognized by seed lexicon with safe NEUTRAL REST fallback")

        # 4. Combo test
        assert "Inactive (Playing Registered 3D Motion)" in data["comboTest"]["phase1"]["fallbackMode"], "Phase 1 must play registered clip"
        assert "Active (Held in Neutral" in data["comboTest"]["phase2"]["fallbackMode"], "Phase 2 must transition to neutral fallback for HELLO"
        print("✔ Check 4: 'Tech Motion + Hello' plays synthetic motion then transitions to neutral fallback")

        # 5. ASL separation
        assert data["aslTest"]["lang"] == "ASL", "Target language must be ASL"
        assert "0 sign(s)" in data["aslTest"]["signs"], "ASL must NOT produce signs or borrow ISL lexicon"
        assert "hello, welcome" in data["aslTest"]["unsupported"], "All words must be reported as unsupported"
        assert "unsupported" in data["aslTest"]["notice"].lower() or "asl" in data["aslTest"]["notice"].lower(), "ASL unsupported notice must be present"
        print("✔ Check 5: ASL separation strictly verified (no English word substitution)")

        print("\nALL 5 DETERMINISTIC CHECKS PASSED SUCCESSFULLY!")
    else:
        print("ERROR: Could not find m36-deterministic-results in DOM output")
        print(dom[-1000:])
        sys.exit(1)
finally:
    if os.path.exists(runner_html_path):
        os.remove(runner_html_path)
