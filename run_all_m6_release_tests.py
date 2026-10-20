#!/usr/bin/env python3
"""SignBridge Milestone M6 — Master Unified Release & Integration Test Runner

Executes and reconciles:
1. M3 Baseline Regression Suite (246 checks across 7 sub-suites)
2. M4 Stage 1 Message Contract & Sequencing Unit Suite (14 unit test assertions)
3. M4 Stage 1 Browser-Based E2E Smoke Test in Chrome WebGL (16 checks via CDP)
4. M4 Stage 2 ISL Coverage, Inventory & Governance Unit Suite (14 unit test assertions)
5. M4 Stage 3 Performance, Privacy & Failure Recovery Unit Suite (15 unit test assertions)
6. M4 Stage 4 Controlled Pilot Dry-Run & Readiness Suite (17 unit test assertions)
7. M4 Stage 5 Complete Validation, Release Readiness & Governance Suite (18 unit test assertions)
8. M6 Automated Release Verification & End-to-End Pipeline Integration Suite (20 unit test assertions)

Total checks reconciled: 360 checks across 8 suites.
Generates: benchmarks/m6_release_test_results.json
"""

import datetime
import json
import os
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def run_suite(name, check_count, cmd):
    print("\n" + "=" * 80)
    print(f" RUNNING: {name} ({check_count} checks)")
    print(f" Command: {' '.join(cmd)}")
    print("=" * 80)
    t0 = time.time()
    res = subprocess.run(cmd, cwd=str(ROOT))
    elapsed = time.time() - t0
    status = "PASSED" if res.returncode == 0 else "FAILED"
    print(f"Completed in {elapsed:.2f}s with exit code {res.returncode}")
    return res.returncode, elapsed, status, check_count


def main():
    if hasattr(sys.stdout, 'reconfigure'):
        try:
            sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        except Exception:
            pass

    print("=" * 80)
    print(" SIGNBRIDGE MILESTONE M6 — MASTER UNIFIED RELEASE TEST EXECUTION")
    print("=" * 80)

    suites = [
        ("M3 Baseline Regression Suite (7 sub-suites)",
         246,
         [sys.executable, "run_all_m3_tests.py"]),
        ("M4 Stage 1 Bridge Contract & Ordering Unit Suite",
         14,
         [sys.executable, "-m", "unittest", "tests/test_m4_stage1_bridge.py"]),
        ("M4 Stage 1 Browser-Based E2E Smoke Test in Chrome WebGL",
         16,
         [sys.executable, "tests/test_m4_browser_bridge_e2e.py"]),
        ("M4 Stage 2 ISL Coverage & Governance Unit Suite",
         14,
         [sys.executable, "-m", "unittest", "tests/test_m4_stage2_isl_coverage.py"]),
        ("M4 Stage 3 Performance, Privacy & Failure Recovery Suite",
         15,
         [sys.executable, "-m", "unittest", "tests/test_m4_stage3_performance_privacy.py"]),
        ("M4 Stage 4 Controlled Pilot Dry-Run & Readiness Suite",
         17,
         [sys.executable, "-m", "unittest", "tests/test_m4_stage4_dry_run.py"]),
        ("M4 Stage 5 Complete Validation, Release Readiness & Governance Suite",
         18,
         [sys.executable, "-m", "unittest", "tests/test_m4_stage5_validation.py"]),
        ("M6 Automated Release Verification & End-to-End Pipeline Integration Suite",
         20,
         [sys.executable, "-m", "unittest", "tests/test_m6_release_verification.py"])
    ]

    results = []
    overall_exit = 0
    total_checks = 0
    passed_checks = 0

    for name, checks, cmd in suites:
        code, elapsed, status, count = run_suite(name, checks, cmd)
        total_checks += count
        if code == 0:
            passed_checks += count
        else:
            overall_exit = code
        results.append({
            "suite": name,
            "checks": count,
            "exit_code": code,
            "duration_seconds": round(elapsed, 2),
            "status": status
        })

    print("\n" + "=" * 80)
    print(" MILESTONE M6 UNIFIED RELEASE TEST RECONCILIATION SUMMARY")
    print("=" * 80)
    for r in results:
        status_str = f"{r['status']} ({r['duration_seconds']}s)"
        print(f" - {r['suite']:<65} : {r['checks']:>3} checks -> {status_str}")

    print("-" * 80)
    print(f" TOTAL RECONCILED CHECKS : {passed_checks} / {total_checks} PASSED")
    print(f" OVERALL SUITE STATUS    : {'SUCCESS' if overall_exit == 0 else 'FAILURE'}")
    print("=" * 80)

    # Save output report
    report = {
        "timestamp": datetime.datetime.now().isoformat(),
        "milestone": "M6",
        "stage": "Automated Release Verification & Integration Reconciliation",
        "governance_mode": "DRY_RUN_ONLY",
        "outreach_authorized": False,
        "total_checks": total_checks,
        "passed_checks": passed_checks,
        "overall_status": "SUCCESS" if overall_exit == 0 else "FAILURE",
        "exit_code": overall_exit,
        "suites": results
    }

    out_file = ROOT / "benchmarks" / "m6_release_test_results.json"
    out_file.parent.mkdir(parents=True, exist_ok=True)
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
    print(f"Saved machine-readable test evidence to: {out_file}")

    sys.exit(overall_exit)


if __name__ == "__main__":
    main()
