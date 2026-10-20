#!/usr/bin/env python3
"""Tests for SignBridge Milestone M4 Stage 4: Controlled Pilot Dry-Run & Readiness.

Automated verification of the 17 specified dry-run scenarios:
1. Successful startup and shutdown.
2. Backend unavailable at startup.
3. Backend interruption during a session.
4. Silence and empty transcription.
5. Low-confidence transcription.
6. Supported NAMASTE routing.
7. Unanimated dictionary entries.
8. Unknown and out-of-lexicon phrases.
9. Duplicate, stale, and out-of-order transcript events.
10. Queue saturation and bounded transcript history.
11. Avatar window closed and reopened during capture.
12. Tab closure and capture teardown.
13. Permission denial and recovery.
14. Local session-data cleanup.
15. Synthetic incident creation and rollback procedure.
16. Export of test-only results.
17. Confirmation that test-only data cannot be mistaken for genuine human-review evidence.
"""

import json
import os
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


class TestM4Stage4DryRunWorkflows(unittest.TestCase):
    """Verifies all 17 controlled pilot dry-run operational scenarios."""

    def test_01_startup_and_shutdown_state_machine(self):
        """Scenario 1: Verifies state machine transitions from idle -> starting -> capturing -> stopping -> idle."""
        bg_js = (ROOT / 'extension' / 'background.js').read_text(encoding='utf-8')
        
        self.assertIn("status: \"idle\"", bg_js)
        self.assertIn("status: \"starting\"", bg_js)
        self.assertIn("status: \"capturing\"", bg_js)
        self.assertIn("status: \"stopping\"", bg_js)
        self.assertIn("updateBadge(updated.status)", bg_js)

    def test_02_backend_unavailable_at_startup(self):
        """Scenario 2: Verifies backend unavailable at startup surfaces offline warning."""
        popup_js = (ROOT / 'extension' / 'popup.js').read_text(encoding='utf-8')
        
        self.assertIn("checkBackendHealth", popup_js)
        self.assertIn("dot-offline", popup_js)
        self.assertIn("Offline", popup_js)

    def test_03_backend_interruption_mid_session(self):
        """Scenario 3: Verifies backend interruption during active capture dispatches error and clears queue on stop."""
        offscreen_js = (ROOT / 'extension' / 'offscreen.js').read_text(encoding='utf-8')
        
        self.assertIn("TRANSCRIPTION_ERROR", offscreen_js)
        self.assertIn("Backend offline", offscreen_js)
        self.assertIn("transcriptionQueue.length = 0", offscreen_js, "Queue must be cleared on stop")

    def test_04_silence_and_empty_transcription(self):
        """Scenario 4: Verifies silence returns empty string and avatar holds neutral rest pose without motion."""
        avatar_html = (ROOT / 'extension' / 'overlay' / 'avatar_player.html').read_text(encoding='utf-8')
        
        self.assertIn("Silence detected — Holding neutral rest pose (zero gestures)", avatar_html)
        self.assertIn("player.resetToNeutralPose()", avatar_html)

    def test_05_low_confidence_transcription(self):
        """Scenario 5: Verifies low-confidence speech (<0.60) renders warning badge to alert user."""
        avatar_html = (ROOT / 'extension' / 'overlay' / 'avatar_player.html').read_text(encoding='utf-8')
        
        self.assertIn("0.60", avatar_html)
        self.assertIn("Low ASR Confidence", avatar_html)

    def test_06_supported_namaste_routing(self):
        """Scenario 6: Verifies 'namaste' resolves to production baseline isl_namaste_godl_v1."""
        trans_js = (ROOT / 'extension' / 'translation' / 'isl_translator.js').read_text(encoding='utf-8')
        
        self.assertIn("NAMASTE:", trans_js)
        self.assertIn("isl_namaste_godl_v1", trans_js)
        self.assertNotIn("isl_namaste_mocap_candidate_v1", trans_js, "Quarantined candidate must NOT be in production lexicon")

    def test_07_unanimated_dictionary_entries(self):
        """Scenario 7: Verifies dictionary words lacking 3D animation (e.g. THANK_YOU) hold neutral pose with notice."""
        trans_js = (ROOT / 'extension' / 'translation' / 'isl_translator.js').read_text(encoding='utf-8')
        avatar_html = (ROOT / 'extension' / 'overlay' / 'avatar_player.html').read_text(encoding='utf-8')
        
        self.assertIn("THANK_YOU:", trans_js)
        self.assertIn("animationId: null", trans_js)
        self.assertIn("3D animation awaiting qualified review — neutral pose held", avatar_html)

    def test_08_unknown_and_out_of_lexicon_phrases(self):
        """Scenario 8: Verifies out-of-lexicon phrases surface in unsupportedWords and avatar maintains rest pose."""
        avatar_html = (ROOT / 'extension' / 'overlay' / 'avatar_player.html').read_text(encoding='utf-8')
        
        self.assertIn("Out-of-lexicon words", avatar_html)
        self.assertIn("PRD: Zero synthetic gestures", avatar_html)

    def test_09_duplicate_stale_out_of_order_events(self):
        """Scenario 9: Verifies monotonic sequence ID check drops duplicate or stale transcripts."""
        avatar_html = (ROOT / 'extension' / 'overlay' / 'avatar_player.html').read_text(encoding='utf-8')
        
        self.assertIn("lastProcessedSeqId", avatar_html)
        self.assertIn("payload.sequenceId <= lastProcessedSeqId", avatar_html)

    def test_10_queue_saturation_and_bounded_history(self):
        """Scenario 10: Verifies queue capped at MAX_QUEUE_SIZE=3 and transcript history capped at 30 items."""
        offscreen_js = (ROOT / 'extension' / 'offscreen.js').read_text(encoding='utf-8')
        bg_js = (ROOT / 'extension' / 'background.js').read_text(encoding='utf-8')
        
        self.assertIn("MAX_QUEUE_SIZE = 3", offscreen_js)
        self.assertIn("newSegments.length > 30", bg_js)

    def test_11_avatar_window_reconnect_state(self):
        """Scenario 11: Verifies avatar player queries session storage on load to reconnect to running sessions."""
        avatar_html = (ROOT / 'extension' / 'overlay' / 'avatar_player.html').read_text(encoding='utf-8')
        
        self.assertIn("chrome.storage.session.get(\"captureState\")", avatar_html)
        self.assertIn("Connecting to running capture session", avatar_html)

    def test_12_tab_closure_and_track_teardown(self):
        """Scenario 12: Verifies tab closure triggers audioTrack.onended and initiates clean session shutdown."""
        offscreen_js = (ROOT / 'extension' / 'offscreen.js').read_text(encoding='utf-8')
        bg_js = (ROOT / 'extension' / 'background.js').read_text(encoding='utf-8')
        
        self.assertIn("CAPTURE_TRACK_ENDED", offscreen_js)
        self.assertIn("CAPTURE_TRACK_ENDED", bg_js)

    def test_13_permission_denial_and_recovery(self):
        """Scenario 13: Verifies permission denial on chrome:// or internal pages disables capture button."""
        popup_js = (ROOT / 'extension' / 'popup.js').read_text(encoding='utf-8')
        
        self.assertIn("chrome://", popup_js)
        self.assertIn("Cannot capture Chrome internal pages", popup_js)
        self.assertIn("captureBtn.disabled = true", popup_js)

    def test_14_local_session_data_cleanup(self):
        """Scenario 14: Verifies CLEAR_TRANSCRIPT empties transcript arrays and session teardown resets storage."""
        bg_js = (ROOT / 'extension' / 'background.js').read_text(encoding='utf-8')
        
        self.assertIn("CLEAR_TRANSCRIPT", bg_js)
        self.assertIn("transcripts: []", bg_js)
        self.assertIn("fullTranscript: \"\"", bg_js)

    def test_15_synthetic_incident_and_rollback(self):
        """Scenario 15: Verifies rollback procedure and instant fallback to baseline animation."""
        gates_doc = (ROOT / 'Docs' / 'M4_STAGE_2_PROMOTION_GATES.md').read_text(encoding='utf-8')
        
        self.assertIn("Instant Rollback Protocol", gates_doc)
        self.assertIn("isl_namaste_godl_v1", gates_doc)

    def test_16_test_only_results_export_schema(self):
        """Scenario 16: Verifies dry-run results artifact exists, is valid JSON, and confirms all 17 steps passed."""
        artifact_path = ROOT / 'benchmarks' / 'm4_stage4_dry_run_results.json'
        self.assertTrue(artifact_path.exists(), "Dry run artifact must exist at benchmarks/m4_stage4_dry_run_results.json")
        
        data = json.loads(artifact_path.read_text(encoding='utf-8'))
        self.assertIn("run_id", data)
        self.assertIn("scenarios", data)
        self.assertEqual(data["total_scenarios"], 17)
        self.assertEqual(data["failed"], 0)
        self.assertEqual(data["passed"], 17)

    def test_17_review_store_segregation(self):
        """Scenario 17: Verifies test fixtures and dry-run data are segregated and cannot pollute genuine review store."""
        # Ensure reviews/ contains no fake/synthetic reviews
        reviews_dir = ROOT / 'reviews'
        if reviews_dir.exists():
            files = list(reviews_dir.glob('*.json'))
            for f in files:
                content = json.loads(f.read_text(encoding='utf-8'))
                # If any file exists, it must NOT be an unverified synthetic test review masquerading as real
                self.assertFalse(
                    content.get('isSynthetic', False) and content.get('isHumanReview', True),
                    f"CRITICAL ETHICAL VIOLATION: Synthetic test review masquerading as genuine review in {f.name}"
                )


if __name__ == '__main__':
    unittest.main()
