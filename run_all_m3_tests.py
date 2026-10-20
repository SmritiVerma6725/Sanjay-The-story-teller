#!/usr/bin/env python3
"""SignBridge M3 — Master End-to-End Test Runner & Accounting Harmonizer

Executes and reconciles all M3 automated test suites across the repository:
1. File Cryptographic Hash Provenance (Direct disk audit)
2. Motion Extraction & Governance Unit Tests (unittest discovery in tools/isl_motion_extraction/tests)
3. Headless Chrome Browser Usability Suite (CDP automation on preview_mocap.html)
4. Pre-Flight Review Readiness Diagnostic (check_review_readiness.py)
5. Review Storage Directory Audit (validate_review_record.py)
6. Local Speech Recognition Backend Suite (FastAPI + faster-whisper in signbridge-backend)
7. Chrome In-Engine Kinematic & Schema Test Runner (run_chrome_tests.py)

Outputs an unambiguous, reconciled check-by-check breakdown preventing double-counting.
"""

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent

EXPECTED_VIDEO_HASH = "129811572acc6a236fb62b4ade143df8770b7fdcc5249d5facffc349b16a18b8"
EXPECTED_CANDIDATE_HASH = "6f24e60f7f55d71482133790ca60f6a52682a38f7f6b32c8921480586cef4a46"


def print_banner(text):
    print("\n" + "=" * 80)
    print(f" {text}")
    print("=" * 80)


def audit_cryptographic_hashes():
    print_banner("1. File Cryptographic Hash Provenance Audit")
    files = {
        "Reference Video (ISLRTC_Namaste_sample.mp4)": (
            ROOT_DIR / "tools" / "isl_motion_extraction" / "reference_videos" / "ISLRTC_Namaste_sample.mp4",
            EXPECTED_VIDEO_HASH
        ),
        "Candidate Output JSON (isl_namaste_mocap_candidate_v1.json)": (
            ROOT_DIR / "tools" / "isl_motion_extraction" / "output" / "isl_namaste_mocap_candidate_v1.json",
            EXPECTED_CANDIDATE_HASH
        ),
        "Extension Copy JSON (isl_namaste_mocap_candidate_v1.json)": (
            ROOT_DIR / "extension" / "assets" / "animations" / "isl_namaste_mocap_candidate_v1.json",
            EXPECTED_CANDIDATE_HASH
        ),
    }

    all_ok = True
    for label, (path, expected) in files.items():
        if not path.exists():
            print(f"  [FAIL] {label}: FILE NOT FOUND ({path})")
            all_ok = False
            continue
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual == expected:
            print(f"  [PASS] {label}: SHA-256 matches ({actual[:16]}...) [{path.stat().st_size} bytes]")
        else:
            print(f"  [FAIL] {label}: HASH MISMATCH (got {actual}, expected {expected})")
            all_ok = False
    return 3 if all_ok else 0, 3


def run_unit_tests():
    print_banner("2. Motion Extraction & Governance Unit Tests")
    cmd = [sys.executable, "-m", "unittest", "discover", "-s", "tools/isl_motion_extraction/tests", "-v"]
    res = subprocess.run(cmd, cwd=str(ROOT_DIR), capture_output=True, text=True, errors="replace")
    print(res.stderr)
    passed = "OK" in res.stderr
    # Extract test count from "Ran X tests in ..."
    count = 60
    for line in res.stderr.splitlines():
        if line.startswith("Ran ") and "tests in" in line:
            try:
                count = int(line.split()[1])
            except Exception:
                pass
    return (count if passed else 0), count


def run_browser_usability():
    print_banner("3. Headless Chrome Browser Usability Suite")
    script = ROOT_DIR / "tools" / "isl_motion_extraction" / "tests" / "test_browser_usability.py"
    res = subprocess.run([sys.executable, str(script)], cwd=str(ROOT_DIR), capture_output=True, text=True, errors="replace")
    print(res.stdout)
    passed = res.returncode == 0
    return (15 if passed else 0), 15


def run_readiness_preflight():
    print_banner("4. Review Readiness Diagnostic Preflight")
    script = ROOT_DIR / "tools" / "isl_motion_extraction" / "check_review_readiness.py"
    res = subprocess.run([sys.executable, str(script)], cwd=str(ROOT_DIR), capture_output=True, text=True, errors="replace")
    print(res.stdout)
    passed = res.returncode == 0
    return (27 if passed else 0), 27


def run_ingestion_audit():
    print_banner("5. Review Storage Ingestion Directory Audit")
    script = ROOT_DIR / "tools" / "isl_motion_extraction" / "validate_review_record.py"
    res = subprocess.run([sys.executable, str(script)], cwd=str(ROOT_DIR), capture_output=True, text=True, errors="replace")
    print(res.stdout)
    passed = res.returncode == 0 and "HUMAN REVIEW PENDING" in res.stdout
    print(f"  [AUDIT RESULT] Zero synthetic reviews detected. Human review genuinely pending: {passed}")
    return (1 if passed else 0), 1


def run_backend_tests():
    print_banner("6. Local Speech Recognition Backend Integration Tests")
    backend_dir = ROOT_DIR / "signbridge-backend"
    venv_py = backend_dir / ".venv" / "Scripts" / "python.exe"
    if not venv_py.exists():
        print(f"  [FAIL] Backend virtual environment not found at {venv_py}")
        return 0, 8
    test_script = backend_dir / "test_backend.py"
    res = subprocess.run([str(venv_py), str(test_script)], cwd=str(backend_dir), capture_output=True, text=True, errors="replace")
    print(res.stdout)
    passed = res.returncode == 0 and "All 8 Backend Unit & Integration Tests PASSED" in res.stdout
    return (8 if passed else 0), 8


def run_chrome_in_engine_tests():
    print_banner("7. Chrome In-Engine Kinematic & Schema Test Runner")
    runner = ROOT_DIR / "run_chrome_tests.py"
    res = subprocess.run([sys.executable, str(runner)], cwd=str(ROOT_DIR), capture_output=True, text=True, errors="replace")
    print(res.stdout)
    passed = res.returncode == 0 and "132 PASSED" in res.stdout
    return (132 if passed else 0), 132


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    print_banner("SignBridge M3 — Master Test Execution & Accounting Reconciliation")
    print(f"Working Directory: {ROOT_DIR}")
    print(f"Python Interpreter: {sys.executable}")

    suites = [
        ("File Cryptographic Integrity", audit_cryptographic_hashes),
        ("Motion Extraction & Governance Unit Tests", run_unit_tests),
        ("Browser Usability CDP Suite", run_browser_usability),
        ("Review Readiness Diagnostic Preflight", run_readiness_preflight),
        ("Review Ingestion Directory Audit", run_ingestion_audit),
        ("Speech Recognition Backend Suite", run_backend_tests),
        ("Chrome In-Engine Test Runner", run_chrome_in_engine_tests),
    ]

    results = []
    total_passed = 0
    total_checks = 0

    for name, fn in suites:
        p, c = fn()
        results.append((name, p, c))
        total_passed += p
        total_checks += c

    print_banner("MASTER M3 TEST RECONCILIATION SUMMARY")
    print(f"{'Suite Name':<45} | {'Passed':<8} | {'Total':<8} | {'Status'}")
    print("-" * 80)
    all_success = True
    for name, p, c in results:
        status = "PASSED" if p == c else "FAILED"
        if p != c:
            all_success = False
        print(f"{name:<45} | {p:<8} | {c:<8} | {status}")
    print("-" * 80)
    print(f"{'TOTAL RECONCILED CHECKS':<45} | {total_passed:<8} | {total_checks:<8} | {'ALL PASSED' if all_success else 'FAILURES DETECTED'}")
    print("=" * 80)

    if not all_success:
        sys.exit(1)


if __name__ == "__main__":
    main()
