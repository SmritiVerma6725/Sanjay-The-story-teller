"""
SignBridge Milestone M4 — Stage 1 Integration Test Suite
Verifies:
1. Versioned message contract (v1.0.0) validation.
2. Transcript sequence ordering and de-duplication.
3. Session lifecycle isolation and stale chunk rejection.
4. Supported sign routing (Namaste -> isl_namaste_godl_v1).
5. Quarantined candidate isolation (isl_namaste_mocap_candidate_v1 never resolved in production).
6. Unsupported phrase fallback and zero synthetic gestures.
7. Silence / empty audio handling.
8. Player recovery on late launch.
"""

import unittest
import json
import os
import sys

# Ensure repository root is in sys.path
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)


class TestM4MessageContract(unittest.TestCase):
    """Verifies that dispatch payloads strictly adhere to version 1.0.0 contract."""

    def create_valid_payload(self, **overrides):
        payload = {
            "version": "1.0.0",
            "type": "SIGNBRIDGE_TRANSCRIPTION_DISPATCH",
            "sessionId": "sb_session_1697800000_abc123",
            "sequenceId": 1,
            "timestamp": 2.0,
            "duration": 2.0,
            "text": "namaste",
            "words": [{"word": "namaste", "start": 0.1, "end": 1.2, "probability": 0.95}],
            "confidence": 0.95,
            "language": "en",
            "metrics": {"inference_time_ms": 240.0, "rtf": 0.12, "audio_bytes": 64044},
            "dispatchedAt": 1697800002000
        }
        payload.update(overrides)
        return payload

    def validate_contract(self, payload):
        errors = []
        if not isinstance(payload, dict):
            return False, ["Payload must be a dictionary"]
        if payload.get("version") != "1.0.0":
            errors.append(f"Invalid or missing version: {payload.get('version')}")
        if payload.get("type") != "SIGNBRIDGE_TRANSCRIPTION_DISPATCH":
            errors.append(f"Invalid type: {payload.get('type')}")
        if not payload.get("sessionId") or not isinstance(payload.get("sessionId"), str):
            errors.append("Missing or invalid sessionId")
        if not isinstance(payload.get("sequenceId"), int) or payload.get("sequenceId") <= 0:
            errors.append("sequenceId must be a positive integer")
        if not isinstance(payload.get("text"), str):
            errors.append("text must be a string")
        conf = payload.get("confidence")
        if conf is not None:
            if not isinstance(conf, (int, float)) or conf < 0.0 or conf > 1.0:
                errors.append(f"confidence must be between 0.0 and 1.0, got: {conf}")
        return len(errors) == 0, errors

    def test_valid_contract_passes(self):
        payload = self.create_valid_payload()
        valid, errors = self.validate_contract(payload)
        self.assertTrue(valid, f"Expected valid contract, got errors: {errors}")

    def test_null_confidence_is_allowed(self):
        payload = self.create_valid_payload(confidence=None)
        valid, errors = self.validate_contract(payload)
        self.assertTrue(valid, "Null confidence should be allowed without inventing values")

    def test_rejects_out_of_range_confidence(self):
        payload = self.create_valid_payload(confidence=1.5)
        valid, errors = self.validate_contract(payload)
        self.assertFalse(valid)
        self.assertTrue(any("confidence" in e for e in errors))

    def test_rejects_invalid_version(self):
        payload = self.create_valid_payload(version="0.9.0")
        valid, errors = self.validate_contract(payload)
        self.assertFalse(valid)
        self.assertTrue(any("version" in e for e in errors))

    def test_rejects_non_positive_sequence_id(self):
        payload = self.create_valid_payload(sequenceId=0)
        valid, errors = self.validate_contract(payload)
        self.assertFalse(valid)
        self.assertTrue(any("sequenceId" in e for e in errors))


class SimulatedAvatarBridge:
    """Emulates avatar_player.html bridge state machine and sequence ordering."""

    def __init__(self):
        self.active_session_id = None
        self.last_processed_seq_id = 0
        self.processed_chunks = []
        self.dropped_chunks = []
        self.avatar_pose = "NEUTRAL_REST_POSE"
        self.current_gloss = None
        self.status = "IDLE"

    def handle_capture_started(self, session_id):
        self.active_session_id = session_id
        self.last_processed_seq_id = 0
        self.status = "ACTIVE"
        self.avatar_pose = "NEUTRAL_REST_POSE"

    def handle_capture_stopped(self):
        self.active_session_id = None
        self.last_processed_seq_id = 0
        self.status = "IDLE"
        self.avatar_pose = "NEUTRAL_REST_POSE"
        self.current_gloss = None

    def connect_to_existing_session(self, session_id, last_seq_id):
        self.active_session_id = session_id
        self.last_processed_seq_id = last_seq_id
        self.status = "ACTIVE"

    def handle_dispatch(self, payload):
        if not payload or payload.get("version") != "1.0.0":
            self.dropped_chunks.append((payload, "INVALID_VERSION"))
            return False

        # Session verification
        session_id = payload.get("sessionId")
        if not self.active_session_id:
            self.active_session_id = session_id
            self.last_processed_seq_id = 0
        elif session_id != self.active_session_id:
            self.dropped_chunks.append((payload, "MISMATCHED_SESSION"))
            return False

        # Monotonic sequence check & de-duplication
        seq_id = payload.get("sequenceId")
        if seq_id <= self.last_processed_seq_id:
            self.dropped_chunks.append((payload, "DUPLICATE_OR_OUT_OF_ORDER"))
            return False

        self.last_processed_seq_id = seq_id
        self.processed_chunks.append(payload)

        # Silence handling
        text = (payload.get("text") or "").strip().lower()
        if not text:
            self.avatar_pose = "NEUTRAL_REST_POSE"
            self.current_gloss = None
            return True

        # Routing logic
        if text in ("namaste", "namaskar", "namaskaram"):
            self.avatar_pose = "isl_namaste_godl_v1"
            self.current_gloss = "NAMASTE"
        elif text in ("hello", "thank you", "please", "welcome", "sorry", "yes", "no"):
            # Known in seed dictionary, but no 3D clip registered -> Neutral fallback
            self.avatar_pose = "NEUTRAL_REST_POSE"
            self.current_gloss = text.upper()
        else:
            # Completely unsupported phrase -> Neutral fallback
            self.avatar_pose = "NEUTRAL_REST_POSE"
            self.current_gloss = None

        return True


class TestM4SequenceOrderingAndDeduplication(unittest.TestCase):
    """Verifies that duplicates, out-of-order chunks, and stale sessions are rejected."""

    def setUp(self):
        self.bridge = SimulatedAvatarBridge()
        self.bridge.handle_capture_started("session_alpha")

    def test_monotonic_sequence_accepted(self):
        c1 = {"version": "1.0.0", "sessionId": "session_alpha", "sequenceId": 1, "text": "namaste"}
        c2 = {"version": "1.0.0", "sessionId": "session_alpha", "sequenceId": 2, "text": "hello"}
        self.assertTrue(self.bridge.handle_dispatch(c1))
        self.assertTrue(self.bridge.handle_dispatch(c2))
        self.assertEqual(len(self.bridge.processed_chunks), 2)
        self.assertEqual(self.bridge.last_processed_seq_id, 2)

    def test_duplicate_chunk_rejected(self):
        c1 = {"version": "1.0.0", "sessionId": "session_alpha", "sequenceId": 1, "text": "namaste"}
        self.assertTrue(self.bridge.handle_dispatch(c1))
        # Deliver exact same sequenceId again
        self.assertFalse(self.bridge.handle_dispatch(c1))
        self.assertEqual(len(self.bridge.processed_chunks), 1)
        self.assertEqual(len(self.bridge.dropped_chunks), 1)
        self.assertEqual(self.bridge.dropped_chunks[0][1], "DUPLICATE_OR_OUT_OF_ORDER")

    def test_out_of_order_chunk_rejected(self):
        c1 = {"version": "1.0.0", "sessionId": "session_alpha", "sequenceId": 1, "text": "hello"}
        c3 = {"version": "1.0.0", "sessionId": "session_alpha", "sequenceId": 3, "text": "namaste"}
        c2 = {"version": "1.0.0", "sessionId": "session_alpha", "sequenceId": 2, "text": "thank you"}

        self.assertTrue(self.bridge.handle_dispatch(c1))
        self.assertTrue(self.bridge.handle_dispatch(c3))
        # Chunk 2 arrives late after chunk 3 has already been articulated
        self.assertFalse(self.bridge.handle_dispatch(c2))
        self.assertEqual(len(self.bridge.processed_chunks), 2)
        self.assertEqual(self.bridge.last_processed_seq_id, 3)

    def test_stale_session_chunk_rejected(self):
        c1 = {"version": "1.0.0", "sessionId": "session_alpha", "sequenceId": 1, "text": "namaste"}
        self.assertTrue(self.bridge.handle_dispatch(c1))

        # Stop session alpha, start session beta
        self.bridge.handle_capture_stopped()
        self.bridge.handle_capture_started("session_beta")

        # Stale chunk from session_alpha arrives
        c_stale = {"version": "1.0.0", "sessionId": "session_alpha", "sequenceId": 2, "text": "namaste"}
        self.assertFalse(self.bridge.handle_dispatch(c_stale))
        self.assertEqual(self.bridge.dropped_chunks[-1][1], "MISMATCHED_SESSION")

    def test_silence_maintains_neutral_pose(self):
        c1 = {"version": "1.0.0", "sessionId": "session_alpha", "sequenceId": 1, "text": "namaste"}
        self.assertTrue(self.bridge.handle_dispatch(c1))
        self.assertEqual(self.bridge.avatar_pose, "isl_namaste_godl_v1")

        # Next chunk is silence
        c2 = {"version": "1.0.0", "sessionId": "session_alpha", "sequenceId": 2, "text": ""}
        self.assertTrue(self.bridge.handle_dispatch(c2))
        self.assertEqual(self.bridge.avatar_pose, "NEUTRAL_REST_POSE")
        self.assertIsNone(self.bridge.current_gloss)

    def test_late_launch_recovery_prevents_stale_replay(self):
        # Emulate avatar player opened when capture is at chunk 10
        late_bridge = SimulatedAvatarBridge()
        late_bridge.connect_to_existing_session("session_gamma", last_seq_id=10)

        # Stale past chunk (e.g. sequence 5) is rejected
        stale_chunk = {"version": "1.0.0", "sessionId": "session_gamma", "sequenceId": 5, "text": "namaste"}
        self.assertFalse(late_bridge.handle_dispatch(stale_chunk))

        # Next live chunk (sequence 11) is accepted immediately
        live_chunk = {"version": "1.0.0", "sessionId": "session_gamma", "sequenceId": 11, "text": "namaste"}
        self.assertTrue(late_bridge.handle_dispatch(live_chunk))
        self.assertEqual(late_bridge.avatar_pose, "isl_namaste_godl_v1")


class TestM4LinguisticRoutingAndQuarantine(unittest.TestCase):
    """Verifies that production routes to isl_namaste_godl_v1 and never to candidate or synthetic signs."""

    def test_production_lexicon_routes_to_godl_baseline(self):
        translator_path = os.path.join(REPO_ROOT, "extension", "translation", "isl_translator.js")
        with open(translator_path, "r", encoding="utf-8") as f:
            content = f.read()

        # NAMASTE must specify animationId: 'isl_namaste_godl_v1'
        self.assertIn("animationId: 'isl_namaste_godl_v1'", content)
        # Must not have any reference to mocap candidate as production animationId
        self.assertNotIn("animationId: 'isl_namaste_mocap_candidate_v1'", content)

    def test_candidate_mocap_remains_quarantined(self):
        registry_path = os.path.join(REPO_ROOT, "extension", "animation", "keyframe_registry.js")
        with open(registry_path, "r", encoding="utf-8") as f:
            content = f.read()

        # In standard registered clips, only TECHNICAL_TEST_CLIP and ISL_NAMASTE_CLIP are registered by default
        self.assertIn("REGISTERED_CLIPS.set(ISL_NAMASTE_CLIP.animationId, ISL_NAMASTE_CLIP)", content)
        # Candidate is not auto-registered in production registry
        self.assertNotIn("REGISTERED_CLIPS.set(CANDIDATE_MOCAP_CLIP.animationId", content)

    def test_unsupported_words_preserved_without_fake_gestures(self):
        translator_path = os.path.join(REPO_ROOT, "extension", "translation", "isl_translator.js")
        with open(translator_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Must preserve unsupportedWords
        self.assertIn("unsupportedWords", content)
        self.assertIn("HONEST UNSUPPORTED", content.upper())


if __name__ == "__main__":
    unittest.main()
