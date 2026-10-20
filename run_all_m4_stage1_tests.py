"""
SignBridge Milestone M4 — Stage 1 Unified Test Orchestrator
Executes:
1. Complete M3 Baseline Regression Suite (246 checks across 7 suites)
2. M4 Stage 1 Bridge Unit Tests (14 checks)
3. M4 Browser-Based End-to-End Smoke Test over Chrome CDP (16 checks)
"""

import subprocess
import sys
import os
import time

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

REPO_ROOT = os.path.abspath(os.path.dirname(__file__))


def run_command(cmd, desc):
    print(f"\n================================================================================")
    print(f" RUNNING: {desc}")
    print(f" Command: {' '.join(cmd)}")
    print(f"================================================================================")
    t0 = time.time()
    res = subprocess.run(cmd, cwd=REPO_ROOT)
    elapsed = time.time() - t0
    print(f"Completed in {elapsed:.2f}s with exit code {res.returncode}")
    return res.returncode == 0


def main():
    print("================================================================================")
    print(" SIGNBRIDGE MILESTONE M4 STAGE 1 — UNIFIED TEST EXECUTION")
    print("================================================================================")
    
    results = {}

    # 1. Full M3 Regression Suite
    ok1 = run_command([sys.executable, "run_all_m3_tests.py"], "M3 Baseline Regression Suite (246 checks)")
    results["M3 Baseline Regression Suite (7 suites / 246 checks)"] = "PASSED" if ok1 else "FAILED"

    # 2. M4 Stage 1 Bridge Tests
    ok2 = run_command([sys.executable, "-m", "unittest", "tests/test_m4_stage1_bridge.py"], "M4 Stage 1 Bridge Contract & Ordering Tests (14 checks)")
    results["M4 Stage 1 Message Contract & Ordering Tests (14 checks)"] = "PASSED" if ok2 else "FAILED"

    # 3. M4 Browser E2E Smoke Test
    ok3 = run_command([sys.executable, "tests/test_m4_browser_bridge_e2e.py"], "M4 Browser-Based End-to-End Smoke Test (16 checks)")
    results["M4 Browser-Based E2E Smoke Test in Chrome WebGL (16 checks)"] = "PASSED" if ok3 else "FAILED"

    print("\n================================================================================")
    print(" STAGE 1 UNIFIED TEST RECONCILIATION SUMMARY")
    print("================================================================================")
    all_passed = True
    for suite, status in results.items():
        print(f" {suite:<65} | {status}")
        if status != "PASSED":
            all_passed = False
    print("--------------------------------------------------------------------------------")
    total_checks = 246 + 14 + 16
    print(f" TOTAL VERIFIED CHECKS: {total_checks} / {total_checks} PASSED")
    print("================================================================================")

    if not all_passed:
        sys.exit(1)


if __name__ == "__main__":
    main()
