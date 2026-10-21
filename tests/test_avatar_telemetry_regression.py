"""
SignBridge — Avatar Telemetry, Linguistic Safeguards, and Backend Health Regression Test Suite

Verifies:
1. Namaste benchmark: dispatches registered clip 'isl_namaste_godl_v1' (1800ms) with matching telemetry.
2. Synthetic technical test: strictly flagged isLinguisticISL=False and marked non-linguistic.
3. Coherent completion state: player retains completed duration and clip identity instead of erasing to 0/0 ms.
4. Neutral rest pose fallback: un-animated and unsupported glosses hold safe neutral pose.
5. ISL Linguistic Governance: Namaste candidate retains 'experimental_awaiting_validation' status.
6. Whisper backend health integration: queries http://127.0.0.1:8765/health with accurate status parsing.
"""

import unittest
import json
import urllib.request
import urllib.error
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


class TestAvatarTelemetryAndLinguisticSafeguards(unittest.TestCase):
    """Regression tests for avatar playback telemetry, safeguards, and health check."""

    def setUp(self):
        self.html_path = REPO_ROOT / "extension" / "overlay" / "avatar_player.html"
        self.controller_path = REPO_ROOT / "extension" / "overlay" / "avatar_player_controller.js"
        self.player_path = REPO_ROOT / "extension" / "animation" / "avatar_player.js"
        self.registry_path = REPO_ROOT / "extension" / "animation" / "keyframe_registry.js"
        self.candidate_path = REPO_ROOT / "tools" / "isl_motion_extraction" / "output" / "isl_namaste_mocap_candidate_v1.json"

    def test_01_avatar_player_html_elements_exist(self):
        """Verify that telemetry and control elements exist in avatar_player.html with clean initial states."""
        html = self.html_path.read_text(encoding="utf-8")
        self.assertIn('id="clip-title"', html)
        self.assertIn('id="time-display"', html)
        self.assertIn('id="progress-fill"', html)
        self.assertIn('id="tel-state"', html)
        self.assertIn('id="tel-clip"', html)
        self.assertIn('id="tel-isl-guard"', html)
        self.assertIn('id="tel-whisper-backend"', html)
        self.assertIn('id="btn-check-backend"', html)
        self.assertIn('id="governance-banner"', html)

        # Initial HTML should default to neutral, NOT hardcoded synthetic motion
        self.assertNotIn('>TECH_TEST_MOTION (2000 ms)<', html, "Initial title should not hardcode synthetic test")
        self.assertIn('Neutral Rest Pose (0 ms)', html)

    def test_02_controller_updates_telemetry_and_governance_dynamically(self):
        """Verify avatar_player_controller.js dynamically updates clip-title, tel-isl-guard, and governance banner."""
        code = self.controller_path.read_text(encoding="utf-8")
        self.assertIn("clipTitle.textContent", code)
        self.assertIn("telIslGuard.innerHTML", code)
        self.assertIn("governanceBanner", code)
        self.assertIn("Experimental ISL", code)
        self.assertIn("Synthetic test", code)

    def test_03_avatar_player_retains_completed_playback_status(self):
        """Verify avatar_player.js preserves last completed duration and clip ID on sequence completion."""
        code = self.player_path.read_text(encoding="utf-8")
        self.assertIn("lastCompletedClip", code)
        self.assertIn("lastCompletedDurationMs", code)
        self.assertIn("sequencePlaybackState === 'COMPLETED'", code)
        self.assertIn("this.lastCompletedDurationMs = this.currentClip.durationMs", code)

    def test_04_synthetic_test_strictly_non_linguistic(self):
        """Verify technical test prototype clip in keyframe_registry.js is flagged isLinguisticISL=False."""
        code = self.registry_path.read_text(encoding="utf-8")
        self.assertIn("tech_test_motion_v1", code)
        match = re.search(r"animationId:\s*['\"]tech_test_motion_v1['\"][^}]+isLinguisticISL:\s*(false|true)", code)
        self.assertTrue(match, "tech_test_motion_v1 must have explicit isLinguisticISL")
        self.assertEqual(match.group(1), "false", "tech_test_motion_v1 must strictly be isLinguisticISL=false")

    def test_05_namaste_production_baseline_properties(self):
        """Verify production Namaste baseline clip properties in keyframe_registry.js."""
        code = self.registry_path.read_text(encoding="utf-8")
        self.assertIn("isl_namaste_godl_v1", code)
        self.assertIn("NAMASTE", code)
        self.assertIn("durationMs: 1800", code)
        match = re.search(r"animationId:\s*['\"]isl_namaste_godl_v1['\"][^}]+isLinguisticISL:\s*(false|true)", code)
        self.assertTrue(match, "isl_namaste_godl_v1 must have explicit isLinguisticISL")
        self.assertEqual(match.group(1), "true", "isl_namaste_godl_v1 must be isLinguisticISL=true")

    def test_06_namaste_candidate_retains_experimental_governance_status(self):
        """Verify MoCap candidate metadata enforces experimental_awaiting_validation and records missing reviews."""
        self.assertTrue(self.candidate_path.exists(), "Candidate JSON must exist")
        data = json.loads(self.candidate_path.read_text(encoding="utf-8"))
        self.assertEqual(data.get("validationStatus"), "experimental_awaiting_validation")
        self.assertEqual(data.get("gloss"), "NAMASTE")
        self.assertEqual(data.get("durationMs"), 3080)
        self.assertIn("awaiting formal Deaf-native sign validation panel review", data.get("provenance", ""))

    def test_07_whisper_backend_health_check_implementation(self):
        """Verify backend health check queries http://127.0.0.1:8765/health with timeout and error handling."""
        code = self.controller_path.read_text(encoding="utf-8")
        self.assertIn("http://127.0.0.1:8765/health", code)
        self.assertIn("AbortController", code)
        self.assertIn("btnCheckBackend.disabled = true", code)
        self.assertIn("Offline / Inactive", code)
        self.assertIn("Request timed out", code)

    def test_08_live_backend_health_endpoint_response(self):
        """Verify actual running Whisper backend at 127.0.0.1:8765 reports valid health JSON."""
        try:
            req = urllib.request.Request("http://127.0.0.1:8765/health")
            with urllib.request.urlopen(req, timeout=3.0) as resp:
                self.assertEqual(resp.status, 200)
                data = json.loads(resp.read().decode("utf-8"))
                self.assertEqual(data.get("status"), "ok")
                self.assertEqual(data.get("service"), "signbridge-backend")
                self.assertEqual(data.get("version"), "0.2.0")
                self.assertEqual(data.get("model"), "tiny.en")
                self.assertEqual(data.get("device"), "cpu")
                self.assertEqual(data.get("compute_type"), "int8")
        except urllib.error.URLError as e:
            self.fail(f"Live Whisper backend should be reachable at http://127.0.0.1:8765/health: {e}")


if __name__ == "__main__":
    unittest.main()
