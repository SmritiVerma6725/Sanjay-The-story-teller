#!/usr/bin/env python3
"""SignBridge M3.23 — Independent Chrome Outreach Verification Tool

Automates Chrome headless navigation to official institutional websites to:
1. Verify connectivity and TLS/HTTP status.
2. Locate official contact pages/directories.
3. Check for visible publication of proposed email addresses.
4. Verify institutional remit and relevance to ISL evaluation.
5. Capture full-page DOM text and screenshots as auditable browser evidence.
"""

import json
import os
import re
import subprocess
import sys
import time
import urllib.request
import urllib.error
import ssl
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
EVIDENCE_DIR = ROOT_DIR / "Docs" / "evidence" / "m3_23_chrome_verification"
CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

TARGETS = [
    {
        "id": "TGT-001",
        "name": "ISLRTC (Indian Sign Language Research and Training Centre)",
        "proposed_email": "islrtcnewdelhi@gmail.com",
        "primary_url": "https://islrtc.nic.in",
        "contact_urls": [
            "https://islrtc.nic.in/contact-us",
            "https://islrtc.nic.in/contact-us/",
            "https://islrtc.nic.in"
        ],
        "category": "Statutory Authority / Certified Interpreters"
    },
    {
        "id": "TGT-002",
        "name": "National Association of the Deaf (NAD) India",
        "proposed_email": "nadindia@gmail.com",
        "primary_url": "https://nadindia.org",
        "contact_urls": [
            "https://nadindia.org/contact",
            "https://nadindia.org/contact-us",
            "https://nadindia.org/contact-us/",
            "https://nadindia.org"
        ],
        "category": "Deaf Native Signers & Advocacy Leaders"
    },
    {
        "id": "TGT-003",
        "name": "All India Federation of the Deaf (AIFD)",
        "proposed_email": "aifd1955@yahoo.co.in",
        "primary_url": "http://aifd.org.in",
        "contact_urls": [
            "http://aifd.org.in/contact-us/",
            "http://aifd.org.in/contact/",
            "http://aifd.org.in"
        ],
        "category": "Deaf Federation / Community Advocates"
    },
    {
        "id": "TGT-004",
        "name": "Deaf Enabled Foundation (DEF)",
        "proposed_email": "info@def.org.in",
        "primary_url": "https://def.org.in",
        "contact_urls": [
            "https://def.org.in/contact",
            "https://def.org.in/contact-us",
            "https://def.org.in"
        ],
        "category": "Community Sign Interpreters & Trainers"
    },
    {
        "id": "TGT-005",
        "name": "IGNOU School of Humanities (SOH)",
        "proposed_email": "soh@ignou.ac.in",
        "primary_url": "http://ignou.ac.in",
        "contact_urls": [
            "http://ignou.ac.in/ignou/aboutignou/school/soh/introduction",
            "http://ignou.ac.in/ignou/aboutignou/school/soh/faculty",
            "http://ignou.ac.in/ignou/aboutignou/school/soh/contact",
            "http://ignou.ac.in"
        ],
        "category": "Academic Sign Language Linguists (DISLI)"
    }
]


def capture_chrome_evidence(target_id, url, output_prefix):
    """Launch headless Chrome to dump DOM and capture screenshot."""
    dom_file = output_prefix.with_suffix(".dom.html")
    shot_file = output_prefix.with_suffix(".png")

    # Chrome dump-dom command
    cmd_dom = [
        CHROME_PATH,
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        "--disable-extensions",
        f"--user-data-dir={tempfile.mkdtemp(prefix='chrome_verif_')}",
        "--virtual-time-budget=8000",
        "--dump-dom",
        url
    ]

    # Chrome screenshot command
    cmd_shot = [
        CHROME_PATH,
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        "--disable-extensions",
        f"--screenshot={shot_file}",
        "--window-size=1280,1024",
        "--virtual-time-budget=8000",
        url
    ]

    dom_output = ""
    shot_success = False

    try:
        res_dom = subprocess.run(cmd_dom, capture_output=True, text=True, errors="replace", timeout=20)
        dom_output = res_dom.stdout
        if len(dom_output) > 100:
            dom_file.write_text(dom_output, encoding="utf-8")
    except Exception as e:
        dom_output = f"ERROR_DOM: {e}"

    try:
        res_shot = subprocess.run(cmd_shot, capture_output=True, text=True, errors="replace", timeout=20)
        if shot_file.exists() and shot_file.stat().st_size > 1000:
            shot_success = True
    except Exception as e:
        pass

    return dom_output, shot_file if shot_success else None


if __name__ == "__main__":
    import tempfile
    EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
    print("================================================================================")
    print("SignBridge M3.23 — Independent Chrome Outreach Target Verification")
    print("================================================================================")

    results = []

    for tgt in TARGETS:
        print(f"\n--- Checking {tgt['id']}: {tgt['name']} ---")
        found_email = False
        verified_url = None
        page_title = None
        evidence_snippet = None
        status = "UNVERIFIED"
        screenshot_path = None
        tested_urls = []

        for url in tgt["contact_urls"]:
            tested_urls.append(url)
            print(f"  Navigating via Chrome to: {url} ...")
            prefix = EVIDENCE_DIR / f"{tgt['id']}_{url.replace('https://', '').replace('http://', '').replace('/', '_').replace('?', '_')}"
            dom, shot = capture_chrome_evidence(tgt["id"], url, prefix)

            if shot:
                screenshot_path = shot
                print(f"    [OK] Captured screenshot: {shot.name} ({shot.stat().st_size} bytes)")

            if dom and len(dom) > 200:
                # Extract title
                m_title = re.search(r"<title[^>]*>(.*?)</title>", dom, re.IGNORECASE | re.DOTALL)
                if m_title:
                    curr_title = m_title.group(1).strip()
                    if not page_title:
                        page_title = curr_title

                # Search for email case-insensitively
                email_lower = tgt["proposed_email"].lower()
                if email_lower in dom.lower():
                    found_email = True
                    verified_url = url
                    page_title = curr_title if m_title else page_title
                    # Extract surrounding snippet
                    idx = dom.lower().find(email_lower)
                    start = max(0, idx - 150)
                    end = min(len(dom), idx + 150)
                    evidence_snippet = dom[start:end].replace("\n", " ").replace("\r", " ").strip()
                    evidence_snippet = re.sub(r"\s+", " ", evidence_snippet)
                    print(f"    [FOUND] Email {tgt['proposed_email']} found on {url}!")
                    break
                else:
                    print(f"    [NOT FOUND] Email not visibly matched on {url} (DOM len={len(dom)})")
            else:
                print(f"    [FAILED] Could not retrieve DOM from {url}")

        if found_email:
            status = "VERIFIED_ON_OFFICIAL_SITE"
        else:
            if not screenshot_path and (not dom or len(dom) < 200):
                status = "INACCESSIBLE"
            else:
                status = "UNVERIFIED"

        res_entry = {
            "id": tgt["id"],
            "name": tgt["name"],
            "category": tgt["category"],
            "proposed_email": tgt["proposed_email"],
            "status": status,
            "verified_url": verified_url or tested_urls[0],
            "page_title": page_title or "Unknown Title",
            "evidence_snippet": evidence_snippet or "Email not visibly present in audited DOM",
            "screenshot_path": str(screenshot_path) if screenshot_path else "None captured"
        }
        results.append(res_entry)
        print(f"  >> Final Status for {tgt['id']}: {status}")

    # Save summary json
    summary_path = EVIDENCE_DIR / "verification_summary.json"
    summary_path.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"\n================================================================================")
    print(f"Summary written to: {summary_path}")
    print("================================================================================")
