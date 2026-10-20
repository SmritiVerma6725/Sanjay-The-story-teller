import subprocess
from pathlib import Path

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
EVIDENCE_DIR = Path(r"C:\AmazonMlChallenge\Docs\evidence\m3_23_chrome_verification")
EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)

urls = [
    ("TGT-001_ISLRTC_contact", "https://islrtc.nic.in/contact-us/"),
    ("TGT-002_NAD_contact", "https://nadindia.org/Contact"),
    ("TGT-003_AIFD_contact", "https://aifdeaf.org/contact-us/"),
    ("TGT-004_DEF_contact", "https://def.org.in/contact/"),
    ("TGT-005_IGNOU_home", "https://www.ignou.ac.in/"),
]

for label, url in urls:
    dom_file = EVIDENCE_DIR / f"{label}.dom.html"
    shot_file = EVIDENCE_DIR / f"{label}.png"
    print(f"\n--- Navigating to {label}: {url} ---")
    
    # Dump DOM
    cmd_dom = [
        CHROME_PATH,
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        "--dump-dom",
        "--virtual-time-budget=6000",
        url
    ]
    try:
        res = subprocess.run(cmd_dom, capture_output=True, text=True, errors="replace", timeout=25)
        dom_file.write_text(res.stdout, encoding="utf-8")
        print(f"  [OK] Saved DOM ({len(res.stdout)} bytes)")
    except Exception as e:
        print(f"  [ERROR] DOM failed: {e}")

    # Screenshot
    cmd_shot = [
        CHROME_PATH,
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        f"--screenshot={shot_file}",
        "--window-size=1280,1024",
        "--virtual-time-budget=6000",
        url
    ]
    try:
        subprocess.run(cmd_shot, capture_output=True, text=True, errors="replace", timeout=25)
        if shot_file.exists():
            print(f"  [OK] Saved screenshot ({shot_file.stat().st_size} bytes)")
    except Exception as e:
        print(f"  [ERROR] Screenshot failed: {e}")
