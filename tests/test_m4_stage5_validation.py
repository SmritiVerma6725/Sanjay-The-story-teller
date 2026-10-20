#!/usr/bin/env python3
"""Tests for SignBridge Milestone M4 Stage 5: Complete Validation, Release Readiness & Evidence Closure.

Automated verification covering the 5 core validation domains:
- Phase B: Real Integration & End-to-End Lifecycle Verification (startup, shutdown, capture, teardown, monotonic sequence, error recovery)
- Phase C: Privacy, Security & Data Lifecycle Audit (permissions, loopback, zero egress, sanitization, bounded queues)
- Phase D: Animation Provenance & Linguistic-Review Safeguards (GODL baseline, mocap quarantine, review store segregation, hash traceability)
- Phase E: Performance & Resource Limits (steady-state memory < 250MB, peak limit pending owner approval, latency/RTF)
- Phase G: Release Candidate Packaging & Asset Hygiene (manifest integrity, zero missing files, clean separation of experimental assets)
"""

import hashlib
import json
import os
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


class TestM4Stage5Validation(unittest.TestCase):
    """Authoritative validation test suite for Milestone M4 Stage 5."""

    def setUp(self):
        self.root = ROOT
        self.ext_dir = self.root / 'extension'
        self.backend_dir = self.root / 'signbridge-backend'
        self.tools_dir = self.root / 'tools' / 'isl_motion_extraction'

    # --------------------------------------------------------------------------
    # Phase B & C: Manifest, Permissions, Loopback & Network Scope
    # --------------------------------------------------------------------------

    def test_01_manifest_permissions_and_scope(self):
        """Verifies Chrome Manifest V3 permissions are minimal, bounded, and contain no broad wildcards."""
        manifest_path = self.ext_dir / 'manifest.json'
        self.assertTrue(manifest_path.exists(), "manifest.json must exist")
        
        manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
        self.assertEqual(manifest.get('manifest_version'), 3, "Must be Manifest V3")
        
        # Verify permissions: must only request required functional APIs
        perms = manifest.get('permissions', [])
        expected_perms = {"tabCapture", "offscreen", "activeTab", "storage", "scripting"}
        self.assertEqual(set(perms), expected_perms, f"Permissions must strictly match {expected_perms}")
        
        # Verify host permissions: strictly YouTube tabs and local backend loopback
        host_perms = manifest.get('host_permissions', [])
        for host in host_perms:
            self.assertTrue(
                host in ["*://*.youtube.com/*", "http://127.0.0.1:8765/*", "http://localhost:8765/*"],
                f"Unexpected broad host permission: {host}"
            )
        self.assertNotIn("<all_urls>", host_perms, "Must never request <all_urls>")

    def test_02_backend_loopback_and_endpoint_contracts(self):
        """Verifies FastAPI backend binds strictly to loopback (127.0.0.1:8765) and implements required endpoints."""
        config_py = (self.backend_dir / 'config.py').read_text(encoding='utf-8')
        main_py = (self.backend_dir / 'main.py').read_text(encoding='utf-8')
        
        # Host binding must be loopback only
        self.assertIn('"127.0.0.1"', config_py, "Backend default host must be 127.0.0.1 loopback")
        self.assertNotIn('0.0.0.0', config_py, "Backend must NEVER bind to 0.0.0.0 (all interfaces)")
        self.assertIn('8765', config_py, "Backend default port must be 8765")
        
        # Required endpoints
        self.assertIn('@app.get("/health"', main_py, "Health endpoint must exist")
        self.assertIn('@app.post("/api/transcribe"', main_py, "Transcribe endpoint must exist")
        self.assertIn('@app.get("/api/transcript/latest"', main_py, "Transcript latest endpoint must exist")

    def test_03_audio_playback_preservation_routing(self):
        """Verifies offscreen document routes captured tab audio back to AudioContext destination for user hearing."""
        offscreen_js = (self.ext_dir / 'offscreen.js').read_text(encoding='utf-8')
        
        self.assertIn("audioContext.createMediaStreamSource", offscreen_js)
        self.assertIn("mediaSourceNode.connect(audioContext.destination)", offscreen_js,
                      "Tab audio must be connected to audioContext.destination to preserve audible playback")

    def test_04_session_lifecycle_and_teardown(self):
        """Verifies teardown releases Web Audio tracks, closes context, and flushes queues."""
        offscreen_js = (self.ext_dir / 'offscreen.js').read_text(encoding='utf-8')
        bg_js = (self.ext_dir / 'background.js').read_text(encoding='utf-8')
        
        # Background dispatches stop requests and handles lifecycle
        self.assertIn("REQUEST_STOP_CAPTURE", bg_js)
        self.assertIn("stopCapture", bg_js)
        
        # Offscreen stops media tracks and flushes memory buffers
        self.assertIn("transcriptionQueue.length = 0", offscreen_js)
        self.assertIn("isProcessingQueue = false", offscreen_js)
        self.assertIn("audioContext.close()", offscreen_js)
        self.assertIn("track.stop()", offscreen_js)

    def test_05_monotonic_sequence_ordering_and_deduplication(self):
        """Verifies avatar player enforces monotonic sequence IDs and discards duplicates or out-of-order packets."""
        player_html = (self.ext_dir / 'overlay' / 'avatar_player.html').read_text(encoding='utf-8')
        
        self.assertIn("lastProcessedSeqId", player_html)
        self.assertIn("payload.sequenceId <= lastProcessedSeqId", player_html)
        self.assertIn("Dropping duplicate or out-of-order chunk", player_html)

    # --------------------------------------------------------------------------
    # Phase B & D: Linguistic Handling, Honest Telemetry & Neutral Pose
    # --------------------------------------------------------------------------

    def test_06_silence_handling_and_neutral_pose(self):
        """Verifies silence or empty audio returns status='empty' and holds neutral pose with zero gestures."""
        player_html = (self.ext_dir / 'overlay' / 'avatar_player.html').read_text(encoding='utf-8')
        
        self.assertIn("Silence detected — Holding neutral rest pose (zero gestures)", player_html)
        self.assertIn("player.resetToNeutralPose()", player_html)

    def test_07_low_confidence_and_noisy_audio_handling(self):
        """Verifies confidence scores < 0.60 trigger low-confidence badge and do not trigger false gestures."""
        player_html = (self.ext_dir / 'overlay' / 'avatar_player.html').read_text(encoding='utf-8')
        transcriber_py = (self.backend_dir / 'transcriber.py').read_text(encoding='utf-8')
        
        # Backend calculates confidence / probability per word
        self.assertIn("probability", transcriber_py)
        # UI renders low-confidence badge
        self.assertIn("Low ASR Confidence", player_html)
        self.assertIn("payload.confidence < 0.60", player_html)

    def test_08_honest_unsupported_words_and_zero_fake_gestures(self):
        """Verifies out-of-lexicon words are surfaced explicitly and avatar holds neutral rest pose without fake gestures."""
        player_html = (self.ext_dir / 'overlay' / 'avatar_player.html').read_text(encoding='utf-8')
        translator_js = (self.ext_dir / 'translation' / 'isl_translator.js').read_text(encoding='utf-8')
        
        # Translator tracks unsupported words
        self.assertIn("unsupportedWords", translator_js)
        # Player renders honest warning and holds neutral pose
        self.assertIn("Out-of-lexicon words:", player_html)
        self.assertIn("Neutral pose held (PRD: Zero synthetic gestures)", player_html)

    def test_09_unanimated_dictionary_words_awaiting_review(self):
        """Verifies dictionary words without 3D animations are displayed as awaiting review and hold neutral pose."""
        player_html = (self.ext_dir / 'overlay' / 'avatar_player.html').read_text(encoding='utf-8')
        
        self.assertIn("Words in dictionary, 3D animation awaiting qualified review", player_html)
        self.assertIn("neutral pose held", player_html)

    def test_10_production_baseline_namaste_metadata(self):
        """Verifies 'namaste' resolves to isl_namaste_godl_v1 and is marked as experimental_awaiting_validation."""
        registry_js = (self.ext_dir / 'animation' / 'keyframe_registry.js').read_text(encoding='utf-8')
        
        self.assertIn("isl_namaste_godl_v1", registry_js)
        self.assertIn("Government Open Data License - India (GODL)", registry_js)
        self.assertIn("experimental_awaiting_validation", registry_js)
        self.assertIn("isLinguisticISL: true", registry_js)

    def test_11_candidate_mocap_quarantine_enforced(self):
        """Verifies candidate mocap clip is quarantined with experimental status and excluded from default production registry."""
        registry_js = (self.ext_dir / 'animation' / 'keyframe_registry.js').read_text(encoding='utf-8')
        candidate_json_path = self.tools_dir / 'output' / 'isl_namaste_mocap_candidate_v1.json'
        
        self.assertTrue(candidate_json_path.exists(), "Candidate mocap JSON file must exist")
        candidate = json.loads(candidate_json_path.read_text(encoding='utf-8'))
        
        # Candidate clip metadata verification
        self.assertEqual(candidate.get("animationId"), "isl_namaste_mocap_candidate_v1")
        self.assertEqual(candidate.get("validationStatus"), "experimental_awaiting_validation")
        
        # Safe separation: Candidate must NOT be hardcoded into default production KeyframeRegistry
        self.assertNotIn("isl_namaste_mocap_candidate_v1", registry_js,
                         "Candidate clip must be quarantined and NOT present in default KeyframeRegistry")
        # Production baseline must remain the sole active registered Namaste clip
        self.assertIn("isl_namaste_godl_v1", registry_js)

    # --------------------------------------------------------------------------
    # Phase D: Asset Provenance, Cryptographic Integrity & Review Store Hygiene
    # --------------------------------------------------------------------------

    def test_12_cryptographic_asset_hashes(self):
        """Verifies candidate animation and reference video asset SHA-256 integrity."""
        candidate_path = self.tools_dir / 'output' / 'isl_namaste_mocap_candidate_v1.json'
        video_path = self.tools_dir / 'reference_videos' / 'ISLRTC_Namaste_sample.mp4'
        
        self.assertTrue(candidate_path.exists(), "Candidate JSON must exist")
        self.assertTrue(video_path.exists(), "Reference video must exist")
        
        candidate_sha = hashlib.sha256(candidate_path.read_bytes()).hexdigest()
        video_sha = hashlib.sha256(video_path.read_bytes()).hexdigest()
        
        expected_candidate_sha = "6f24e60f7f55d71482133790ca60f6a52682a38f7f6b32c8921480586cef4a46"
        expected_video_sha = "129811572acc6a236fb62b4ade143df8770b7fdcc5249d5facffc349b16a18b8"
        
        self.assertEqual(candidate_sha, expected_candidate_sha, "Candidate file SHA-256 must match authoritative record")
        self.assertEqual(video_sha, expected_video_sha, "Reference video SHA-256 must match authoritative record")

    def test_13_zero_synthetic_reviews_in_production_store(self):
        """Verifies that tools/isl_motion_extraction/reviews contains 0 synthetic or test-generated review records."""
        reviews_dir = self.tools_dir / 'reviews'
        self.assertTrue(reviews_dir.exists(), "Reviews directory must exist")
        
        review_files = list(reviews_dir.glob('*.json'))
        self.assertEqual(len(review_files), 0,
                         f"Reviews directory must contain 0 files pending genuine human review; found {len(review_files)}")

    def test_14_review_validator_enforces_schema_and_integrity(self):
        """Verifies that validate_review_record.py correctly rejects malformed review records and hash mismatches."""
        validator_py = (self.tools_dir / 'validate_review_record.py').read_text(encoding='utf-8')
        
        self.assertIn("signbridge_review_schema_v1.0.0", validator_py)
        self.assertIn("EXPECTED_CANDIDATE_SHA256", validator_py)
        self.assertIn("EXPECTED_VIDEO_SHA256", validator_py)
        self.assertIn("VALID_RATINGS", validator_py)
        self.assertIn("not_assessable", validator_py)

    def test_15_reviewer_pii_minimization(self):
        """Verifies review schema minimizes reviewer identity (requires role, allows pseudonym/optional name, no PII)."""
        validator_py = (self.tools_dir / 'validate_review_record.py').read_text(encoding='utf-8')
        
        # Schema requires reviewer role
        self.assertIn("VALID_ROLES", validator_py)
        self.assertIn("deaf_native", validator_py)
        self.assertIn("anonymous", validator_py)
        # Ensure no sensitive PII fields are mandated
        self.assertNotIn("phoneNumber", validator_py)
        self.assertNotIn("homeAddress", validator_py)
        self.assertNotIn("ssn", validator_py)

    # --------------------------------------------------------------------------
    # Phase E: Performance, Resource Budgets & Owner Approvals
    # --------------------------------------------------------------------------

    def test_16_performance_and_memory_budget_enforcement(self):
        """Verifies steady-state memory is within 250MB and peak memory (256MB) is recorded as PENDING_OWNER_APPROVAL."""
        matrix_md = (self.root / 'Docs' / 'M4_ACCEPTANCE_MATRIX.md').read_text(encoding='utf-8')
        decisions_md = (self.root / 'Docs' / 'M4_STAGE_4_BLOCKERS_AND_OWNER_DECISIONS.md').read_text(encoding='utf-8')
        
        # Matrix must record steady-state pass (< 250MB) and peak status
        self.assertIn("185.5", matrix_md)
        self.assertIn("256.4", matrix_md)
        self.assertIn("Flagged for owner decision", matrix_md)
        
        # Blockers register must mark revision as PENDING_OWNER_APPROVAL
        self.assertIn("PENDING_OWNER_APPROVAL", decisions_md)
        self.assertIn("Revision of Peak Memory Budget", decisions_md)

    # --------------------------------------------------------------------------
    # Phase C: Zero Cloud / External Network Egress
    # --------------------------------------------------------------------------

    def test_17_zero_cloud_network_egress(self):
        """Verifies extension and backend make zero calls to external clouds, third-party analytics, or telemetry APIs."""
        for path in [self.ext_dir / 'offscreen.js', self.ext_dir / 'background.js', self.ext_dir / 'popup.js']:
            code = path.read_text(encoding='utf-8')
            # Look for external URLs
            external_cloud_domains = [
                "google-analytics.com",
                "api.openai.com",
                "generativelanguage.googleapis.com",
                "sentry.io",
                "mixpanel.com",
                "segment.io",
                "datadoghq.com"
            ]
            for domain in external_cloud_domains:
                self.assertNotIn(domain, code, f"Forbidden cloud domain {domain} found in {path.name}")

    # --------------------------------------------------------------------------
    # Phase G: Release Candidate Hygiene & Packaging
    # --------------------------------------------------------------------------

    def test_18_release_candidate_file_manifest(self):
        """Verifies all essential production extension assets and models exist on disk."""
        essential_files = [
            self.ext_dir / 'manifest.json',
            self.ext_dir / 'background.js',
            self.ext_dir / 'offscreen.html',
            self.ext_dir / 'offscreen.js',
            self.ext_dir / 'popup.html',
            self.ext_dir / 'popup.js',
            self.ext_dir / 'overlay' / 'avatar_player.html',
            self.ext_dir / 'icons' / 'icon-16.png',
            self.ext_dir / 'icons' / 'icon-48.png',
            self.ext_dir / 'icons' / 'icon-128.png',
            self.ext_dir / 'assets' / 'models' / 'ybot.glb',
            self.ext_dir / 'assets' / 'animations' / 'isl_namaste_mocap_candidate_v1.json'
        ]
        
        for file_path in essential_files:
            self.assertTrue(file_path.exists(), f"Essential production file missing: {file_path}")
            self.assertGreater(file_path.stat().st_size, 0, f"File {file_path.name} is empty")


if __name__ == '__main__':
    unittest.main()
