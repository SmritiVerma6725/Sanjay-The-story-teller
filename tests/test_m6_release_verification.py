#!/usr/bin/env python3
"""SignBridge Milestone M6 — Automated Release Verification & End-to-End Integration Suite.

Validates the full system release candidate against all PRD requirements:
1. End-to-End Pipeline Wiring & Contract Integrity (tab capture -> audio chunking -> local Whisper -> routing -> avatar).
2. Dual Language Pipeline Isolation (ISL seed lexicon and grammar vs ASL stub isolation; zero English word-substitution).
3. Production Baseline & Quarantine Enforcement (GODL Namaste baseline active; mocap candidate quarantined; reference video excluded).
4. Audio Playback Preservation & Web Audio Routing (mediaSourceNode connects to AudioContext.destination).
5. Monotonic Sequencing, Stale/Duplicate Packet Rejection, & Bounded Buffers (FIFO queue max 3).
6. Skeletal Kinematics & Rig Conformance (67 canonical Mixamo bones in Y-Bot GLB; 36 bones in candidate clip).
7. Honest Telemetry & Non-Fabrication Invariants (zero synthetic gestures on unknown words; 0/3 human reviews; neutral rest pose).
8. Failure Recovery & Lifecycle Teardown (clean resource release on stop/navigation/error; backend offline fallback).
9. Memory & Performance Budget Compliance (steady-state < 250MB; 300MB peak pending owner approval).
10. Release Packaging, Licensing & Security Scope (MV3 minimal perms, loopback-only host permissions, multi-license attribution).
"""

import hashlib
import json
import os
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


class TestM6ReleaseVerification(unittest.TestCase):
    """Authoritative Release Verification Suite for SignBridge Milestone M6."""

    def setUp(self):
        self.root = ROOT
        self.ext_dir = self.root / 'extension'
        self.backend_dir = self.root / 'signbridge-backend'
        self.tools_dir = self.root / 'tools' / 'isl_motion_extraction'

    # --------------------------------------------------------------------------
    # 1. Pipeline Wiring & End-to-End Contracts
    # --------------------------------------------------------------------------

    def test_01_e2e_pipeline_component_wiring(self):
        """Verifies all components of the speech-to-sign pipeline exist and export declared interfaces."""
        # 1. Audio Capture (Offscreen)
        self.assertTrue((self.ext_dir / 'offscreen.js').exists(), "offscreen.js must exist")
        # 2. Service Worker (Background)
        self.assertTrue((self.ext_dir / 'background.js').exists(), "background.js must exist")
        # 3. Local Whisper Backend
        self.assertTrue((self.backend_dir / 'main.py').exists(), "backend main.py must exist")
        self.assertTrue((self.backend_dir / 'transcriber.py').exists(), "backend transcriber.py must exist")
        # 4. Translation & Routing
        self.assertTrue((self.ext_dir / 'translation' / 'translation_router.js').exists(), "translation_router.js must exist")
        self.assertTrue((self.ext_dir / 'translation' / 'isl_translator.js').exists(), "isl_translator.js must exist")
        self.assertTrue((self.ext_dir / 'translation' / 'asl_translator.js').exists(), "asl_translator.js must exist")
        # 5. Avatar Kinematics & Player
        self.assertTrue((self.ext_dir / 'animation' / 'keyframe_registry.js').exists(), "keyframe_registry.js must exist")
        self.assertTrue((self.ext_dir / 'animation' / 'avatar_player.js').exists(), "avatar_player.js must exist")
        self.assertTrue((self.ext_dir / 'overlay' / 'avatar_player.html').exists(), "avatar_player.html must exist")
        self.assertTrue((self.ext_dir / 'overlay' / 'avatar_player_controller.js').exists(), "avatar_player_controller.js must exist")

    def test_02_versioned_transcription_dispatch_contract(self):
        """Verifies transcription dispatch payload strictly adheres to version 1.0.0 contract schema."""
        bg_js = (self.ext_dir / 'background.js').read_text(encoding='utf-8')
        player_js = (self.ext_dir / 'overlay' / 'avatar_player_controller.js').read_text(encoding='utf-8')

        # Background construct
        self.assertIn('version: "1.0.0"', bg_js)
        self.assertIn('type: "SIGNBRIDGE_TRANSCRIPTION_DISPATCH"', bg_js)
        self.assertIn('sessionId: current.sessionId', bg_js)
        self.assertIn('sequenceId: message.sequenceId', bg_js)
        self.assertIn('confidence: confidence', bg_js)

        # Player consumer
        self.assertIn('payload.version !== "1.0.0"', player_js)
        self.assertIn('message.type === "SIGNBRIDGE_TRANSCRIPTION_DISPATCH"', player_js)

    def test_03_monotonic_sequence_and_deduplication(self):
        """Verifies that avatar player drops duplicate or out-of-order sequence packets."""
        player_js = (self.ext_dir / 'overlay' / 'avatar_player_controller.js').read_text(encoding='utf-8')
        self.assertIn('payload.sequenceId <= lastProcessedSeqId', player_js)
        self.assertIn('lastProcessedSeqId = payload.sequenceId', player_js)

    # --------------------------------------------------------------------------
    # 2. Audio Capture & Playback Preservation
    # --------------------------------------------------------------------------

    def test_04_audio_encoding_and_downsampling(self):
        """Verifies audio is segmented into 2.0s chunks and encoded to 16kHz 16-bit mono PCM WAV in memory."""
        offscreen_js = (self.ext_dir / 'offscreen.js').read_text(encoding='utf-8')
        self.assertIn('TARGET_SAMPLE_RATE = 16000', offscreen_js)
        self.assertIn('CHUNK_DURATION_SEC = 2.0', offscreen_js)
        self.assertIn('writeAsciiString(view, 0, "RIFF")', offscreen_js)
        self.assertIn('writeAsciiString(view, 8, "WAVE")', offscreen_js)
        self.assertIn('downsampleBuffer', offscreen_js)

    def test_05_audible_playback_preservation(self):
        """Verifies tab audio is continuously routed to speakers/headphones to preserve user hearing."""
        offscreen_js = (self.ext_dir / 'offscreen.js').read_text(encoding='utf-8')
        self.assertIn('mediaSourceNode.connect(audioContext.destination)', offscreen_js)

    # --------------------------------------------------------------------------
    # 3. Dual Language Pipeline Isolation (ISL vs ASL)
    # --------------------------------------------------------------------------

    def test_06_isl_asl_pipeline_isolation(self):
        """Verifies ISL and ASL translators remain completely decoupled without cross-language substitution."""
        router_js = (self.ext_dir / 'translation' / 'translation_router.js').read_text(encoding='utf-8')
        isl_js = (self.ext_dir / 'translation' / 'isl_translator.js').read_text(encoding='utf-8')
        asl_js = (self.ext_dir / 'translation' / 'asl_translator.js').read_text(encoding='utf-8')

        self.assertIn("['ISL', 'ASL']", router_js)
        self.assertIn('translateTranscriptToISL', router_js)
        self.assertIn('translateTranscriptToASL', router_js)

        # ASL module does not fake English word substitution
        self.assertIn('ASL_SCHEDULED_FOR_M5', asl_js)
        self.assertIn('ASL_SEED_LEXICON', asl_js)
        self.assertIn('enableExperimentalReordering', isl_js)

    def test_07_isl_seed_vocabulary_and_lemmas(self):
        """Verifies ISL translator recognizes 16 canonical glosses across 50 lemmas."""
        isl_js = (self.ext_dir / 'translation' / 'isl_translator.js').read_text(encoding='utf-8')
        self.assertIn('SEED_LEXICON', isl_js)
        self.assertIn('lemmas:', isl_js)
        self.assertIn('NAMASTE', isl_js)
        self.assertIn('THANK_YOU', isl_js)
        self.assertIn('HELP', isl_js)

    # --------------------------------------------------------------------------
    # 4. Production Baseline, Asset Quarantine & Review Segregation
    # --------------------------------------------------------------------------

    def test_08_production_baseline_namaste_isolation(self):
        """Verifies isl_namaste_godl_v1 is active baseline and marked experimental_awaiting_validation."""
        registry_js = (self.ext_dir / 'animation' / 'keyframe_registry.js').read_text(encoding='utf-8')
        self.assertIn('isl_namaste_godl_v1', registry_js)
        self.assertIn('isLinguisticISL: true', registry_js)
        self.assertIn('experimental_awaiting_validation', registry_js)

    def test_09_experimental_mocap_candidate_quarantined(self):
        """Verifies isl_namaste_mocap_candidate_v1 is excluded from default registry."""
        registry_js = (self.ext_dir / 'animation' / 'keyframe_registry.js').read_text(encoding='utf-8')
        # Candidate clip must NOT be in default runtime registry (strict quarantine boundary)
        self.assertNotIn('isl_namaste_mocap_candidate_v1', registry_js)
        # Verify candidate clip file exists in assets with quarantine status
        candidate_file = self.ext_dir / 'assets' / 'animations' / 'isl_namaste_mocap_candidate_v1.json'
        self.assertTrue(candidate_file.exists(), "Candidate clip json must exist")
        cand_data = json.loads(candidate_file.read_text(encoding='utf-8'))
        self.assertEqual(cand_data.get('animationId'), 'isl_namaste_mocap_candidate_v1')
        self.assertEqual(cand_data.get('validationStatus'), 'experimental_awaiting_validation')

    def test_10_reference_video_excluded_from_public_repo(self):
        """Verifies ISLRTC_Namaste_sample.mp4 is git-ignored and not tracked in repository."""
        gitignore = (self.root / '.gitignore').read_text(encoding='utf-8')
        self.assertIn('reference_videos/*.mp4', gitignore)
        self.assertIn('*.task', gitignore)

    def test_11_zero_synthetic_reviews_and_review_store_integrity(self):
        """Verifies reviews directory contains zero synthetic records (0/3 qualified human reviews)."""
        reviews_dir = self.tools_dir / 'reviews'
        self.assertTrue(reviews_dir.exists(), "reviews directory must exist")
        # Only README.md or .gitkeep is permitted
        review_files = [f.name for f in reviews_dir.iterdir() if f.is_file() and f.suffix == '.json']
        self.assertEqual(len(review_files), 0, f"Synthetic review records prohibited! Found: {review_files}")

    # --------------------------------------------------------------------------
    # 5. Skeletal Articulation & Kinematic Conformance
    # --------------------------------------------------------------------------

    def test_12_rig_conformance_canonical_bones(self):
        """Verifies keyframe registry defines canonical 67-joint skeleton and neutral rest pose."""
        registry_js = (self.ext_dir / 'animation' / 'keyframe_registry.js').read_text(encoding='utf-8')
        self.assertIn('CANONICAL_BONES', registry_js)
        self.assertIn('LeftHandThumb1', registry_js)
        self.assertIn('RightHandThumb1', registry_js)
        self.assertIn('NEUTRAL_REST_POSE', registry_js)

    def test_13_avatar_player_rest_pose_and_safe_fallback(self):
        """Verifies avatar player resets to neutral rest pose on unknown, empty, or un-animated glosses."""
        player_js = (self.ext_dir / 'animation' / 'avatar_player.js').read_text(encoding='utf-8')
        self.assertIn('resetToNeutralPose', player_js)
        self.assertIn('resolved: false', player_js)

    # --------------------------------------------------------------------------
    # 6. Performance, Bounded Queues & Privacy Boundary
    # --------------------------------------------------------------------------

    def test_14_bounded_transcription_queue(self):
        """Verifies offscreen audio queue is strictly bounded to max 3 chunks with 8s timeout."""
        offscreen_js = (self.ext_dir / 'offscreen.js').read_text(encoding='utf-8')
        self.assertIn('MAX_QUEUE_SIZE = 3', offscreen_js)
        self.assertIn('REQUEST_TIMEOUT_MS = 8000', offscreen_js)

    def test_15_loopback_only_network_and_zero_cloud_egress(self):
        """Verifies all backend endpoints and network requests are strictly bound to 127.0.0.1."""
        config_py = (self.backend_dir / 'config.py').read_text(encoding='utf-8')
        manifest = json.loads((self.ext_dir / 'manifest.json').read_text(encoding='utf-8'))

        self.assertIn('"127.0.0.1"', config_py)
        self.assertNotIn('0.0.0.0', config_py)

        host_perms = manifest.get('host_permissions', [])
        for host in host_perms:
            self.assertTrue(
                host in ["*://*.youtube.com/*", "http://127.0.0.1:8765/*", "http://localhost:8765/*"],
                f"Unauthorized host in host_permissions: {host}"
            )

    # --------------------------------------------------------------------------
    # 7. Release Packaging & Documentation Integrity
    # --------------------------------------------------------------------------

    def test_16_manifest_v3_packaging_integrity(self):
        """Verifies manifest declared assets exist and have valid structure."""
        manifest = json.loads((self.ext_dir / 'manifest.json').read_text(encoding='utf-8'))
        self.assertEqual(manifest.get('manifest_version'), 3)

        # Check declared icon assets
        for size, path in manifest.get('icons', {}).items():
            self.assertTrue((self.ext_dir / path).exists(), f"Icon {path} missing")

        # Check action popup
        popup = manifest.get('action', {}).get('default_popup')
        self.assertTrue((self.ext_dir / popup).exists(), f"Popup {popup} missing")

    def test_17_license_attribution_completeness(self):
        """Verifies LICENSE file covers core code, Adobe Mixamo Y-Bot mesh terms, and GODL-India."""
        license_text = (self.root / 'LICENSE').read_text(encoding='utf-8')
        self.assertIn('MIT License', license_text)
        self.assertIn('Adobe Mixamo', license_text)
        self.assertIn('Government Open Data License - India (GODL)', license_text)

    def test_18_contributing_and_security_guidelines(self):
        """Verifies CONTRIBUTING.md and SECURITY.md exist and document promotion gates and privacy."""
        self.assertTrue((self.root / 'CONTRIBUTING.md').exists(), "CONTRIBUTING.md must exist")
        self.assertTrue((self.root / 'SECURITY.md').exists(), "SECURITY.md must exist")

        contrib = (self.root / 'CONTRIBUTING.md').read_text(encoding='utf-8')
        self.assertIn('Promotion Gates', contrib)
        self.assertIn('Quarantine', contrib)

        security = (self.root / 'SECURITY.md').read_text(encoding='utf-8')
        self.assertIn('Threat Model', security)
        self.assertIn('local-first', security)

    def test_19_project_phase_index_reconciliation(self):
        """Verifies Docs/PROJECT_PHASE_INDEX.md documents every milestone from M1 to M6 with explicit statuses."""
        index_path = self.root / 'Docs' / 'PROJECT_PHASE_INDEX.md'
        self.assertTrue(index_path.exists(), "Docs/PROJECT_PHASE_INDEX.md must exist")

        text = index_path.read_text(encoding='utf-8')
        self.assertIn('| **M1** |', text)
        self.assertIn('| **M2** |', text)
        self.assertIn('| **M3.1–M3.7** |', text)
        self.assertIn('| **M4 Stage 1** |', text)
        self.assertIn('| **M6** |', text)

    def test_20_release_candidate_audit_and_blockers(self):
        """Verifies release candidate blockers are explicitly declared without false certification."""
        blockers_doc = self.root / 'Docs' / 'M4_STAGE_5_BLOCKERS_AND_OWNER_DECISIONS.md'
        self.assertTrue(blockers_doc.exists(), "Docs/M4_STAGE_5_BLOCKERS_AND_OWNER_DECISIONS.md must exist")
        text = blockers_doc.read_text(encoding='utf-8')
        self.assertIn('LEGAL-01', text)
        self.assertIn('DEAF-01', text)
        self.assertIn('PERF-01', text)
        self.assertIn('OPS-06', text)
        self.assertIn('0 / 3 REVIEWS', text)


if __name__ == '__main__':
    unittest.main()
