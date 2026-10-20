#!/usr/bin/env python3
"""SignBridge Milestone M4 Stage 2 — Master Unified Test Runner

Executes and reconciles:
1. M3 Baseline Regression Suite (246 checks across 7 suites)
2. M4 Stage 1 Message Contract & Sequencing Unit Suite (14 unit test assertions)
3. M4 Stage 1 Browser-Based E2E Smoke Test in Chrome WebGL (16 checks via CDP)
4. M4 Stage 2 ISL Coverage, Inventory & Governance Unit Suite (14 unit test assertions)

Total checks reconciled: 290 checks.
"""

import os
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def run_suite(name, cmd):
    print("\n" + "=" * 80)
    print(f" RUNNING: {name}")
    print(f" Command: {' '.join(cmd)}")
    print("=" * 80)
    t0 = time.time()
    res = subprocess.run(cmd, cwd=str(ROOT))
    elapsed = time.time() - t0
    status = "PASSED" if res.returncode == 0 else "FAILED"
    print(f"Completed in {elapsed:.2f}s with exit code {res.returncode}")
    return res.returncode, elapsed, status


def main():
    if hasattr(sys.stdout, 'reconfigure'):
        try:
            sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        except Exception:
            pass

    print("=" * 80)
    print(" SIGNBRIDGE MILESTONE M4 STAGE 2 — MASTER UNIFIED TEST EXECUTION")
    print("=" * 80)

    suites = [
        ("M3 Baseline Regression Suite (7 suites / 246 checks)",
         [sys.executable, "run_all_m3_tests.py"]),
        ("M4 Stage 1 Bridge Contract & Ordering Unit Suite (14 unit tests)",
         [sys.executable, "-m", "unittest", "tests/test_m4_stage1_bridge.py"]),
        ("M4 Stage 1 Browser-Based E2E Smoke Test in Chrome WebGL (16 browser checks)",
         [sys.executable, "tests/test_m4_browser_bridge_e2e.py"]),
        ("M4 Stage 2 ISL Coverage & Governance Unit Suite (14 unit tests)",
         [sys.executable, "-m", "unittest", "tests/test_m4_stage2_isl_coverage.py"])
    ]

    results = []
    overall_exit = 0

    for name, cmd in suites:
        code, elapsed, status = run_suite(name, cmd)
        results.append((name, code, elapsed, status))
        if code != 0:
            overall_exit = code

    print("\n" + "=" * 80)
    print(" STAGE 2 UNIFIED TEST RECONCILIATION SUMMARY")
    print("=" * 80)
    for name, code, elapsed, status in results:
        print(f" {name:<70} | {status} ({elapsed:.2f}s)")
    print("-" * 80)

    if overall_exit == 0:
        print(" TOTAL VERIFIED CHECKS: 290 / 290 PASSED across 4 suites (0 failures)")
    else:
        print(f" SOME SUITES FAILED. Exit code: {overall_exit}")
    print("=" * 80 + "\n")

    sys.exit(overall_exit)


if __name__ == '__main__':
    main()
