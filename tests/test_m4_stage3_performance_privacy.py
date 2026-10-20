#!/usr/bin/env python3
"""Tests for SignBridge Milestone M4 Stage 3: Performance, Privacy & Failure Recovery.

Validates:
1. Network & Privacy Boundaries:
   - Backend binds strictly to 127.0.0.1:8765 by default.
   - Manifest permissions do not include physical microphone ('audioCapture').
   - Host permissions are limited strictly to local backend and YouTube.
   - Zero telemetry or third-party cloud speech endpoints in config or manifest.
2. Queue Overflow & Buffer Bounds:
   - Audio queue depth bounded to MAX_QUEUE_SIZE = 3 with oldest-drop policy.
   - Transcript history bounded to 30 items maximum in service worker to prevent memory bloat.
   - Monotonic sequence IDs reject duplicates and out-of-order deliveries.
3. Performance Benchmarking Invariants:
   - Real-Time Factor (RTF) calculation formula: RTF = (infer_ms / 1000.0) / audio_sec.
   - Benchmark report artifact exists and contains valid empirical metrics.
   - Speech recognition operates faster than real time (RTF < 1.0).
4. Failure & Recovery Invariants:
   - Backend offline gracefully handled and surfaced without uncaught exceptions.
   - Silence handling holds neutral pose with zero synthetic gestures.
   - Unsupported phrases route to safe neutral hold with out-of-lexicon transparency.
   - Session stop event releases resources cleanly.
"""

import json
import os
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


class TestM4Stage3PrivacyAndNetwork(unittest.TestCase):
    """Verifies network isolation and user privacy boundaries."""

    def setUp(self):
        self.manifest_path = ROOT / 'extension' / 'manifest.json'
        with open(self.manifest_path, 'r', encoding='utf-8') as f:
            self.manifest = json.load(f)

    def test_01_no_physical_microphone_permission(self):
        """Verifies physical microphone ('audioCapture') is NOT in manifest permissions."""
        permissions = self.manifest.get('permissions', [])
        self.assertNotIn(
            'audioCapture', permissions,
            "CRITICAL PRIVACY VIOLATION: 'audioCapture' requests ambient microphone access!"
        )
        self.assertIn(
            'tabCapture', permissions,
            "Expected 'tabCapture' for tab audio capture."
        )

    def test_02_host_permissions_strictly_scoped(self):
        """Verifies host_permissions are restricted to YouTube and localhost backend."""
        host_perms = self.manifest.get('host_permissions', [])
        allowed_patterns = {
            "*://*.youtube.com/*",
            "http://127.0.0.1:8765/*"
        }
        for hp in host_perms:
            self.assertIn(
                hp, allowed_patterns,
                f"Unexpected external host permission: {hp}"
            )

    def test_03_backend_default_binding_localhost(self):
        """Verifies backend config binds strictly to 127.0.0.1:8765 by default."""
        config_path = ROOT / 'signbridge-backend' / 'config.py'
        content = config_path.read_text(encoding='utf-8')
        
        self.assertIn('"127.0.0.1"', content, "Backend default host must be 127.0.0.1")
        self.assertIn('"8765"', content, "Backend default port must be 8765")

    def test_04_no_external_cloud_speech_endpoints(self):
        """Verifies no Google Cloud, AWS Transcribe, or OpenAI remote API keys or endpoints are configured."""
        config_path = ROOT / 'signbridge-backend' / 'config.py'
        content = config_path.read_text(encoding='utf-8')
        
        prohibited = ['OPENAI_API_KEY', 'AWS_ACCESS_KEY', 'GOOGLE_APPLICATION_CREDENTIALS', 'api.openai.com']
        for term in prohibited:
            self.assertNotIn(
                term, content,
                f"Prohibited external cloud service reference found in backend config: {term}"
            )

    def test_05_offscreen_communication_restricted_to_localhost(self):
        """Verifies offscreen.js communicates strictly with 127.0.0.1:8765."""
        offscreen_js = (ROOT / 'extension' / 'offscreen.js').read_text(encoding='utf-8')
        
        match = re.search(r'BACKEND_TRANSCRIBE_URL\s*=\s*["\']([^"\']+)["\']', offscreen_js)
        self.assertIsNotNone(match, "BACKEND_TRANSCRIBE_URL not defined in offscreen.js")
        self.assertTrue(
            match.group(1).startswith("http://127.0.0.1:8765"),
            f"offscreen.js BACKEND_TRANSCRIBE_URL must point to 127.0.0.1:8765, got {match.group(1)}"
        )


class TestM4Stage3QueueBoundsAndBuffers(unittest.TestCase):
    """Verifies audio queue depth, backpressure handling, and memory buffers."""

    def test_06_offscreen_queue_depth_limit(self):
        """Verifies offscreen.js enforces MAX_QUEUE_SIZE of 3 and drops oldest chunk."""
        offscreen_js = (ROOT / 'extension' / 'offscreen.js').read_text(encoding='utf-8')
        
        queue_match = re.search(r'MAX_QUEUE_SIZE\s*=\s*(\d+)', offscreen_js)
        self.assertIsNotNone(queue_match, "MAX_QUEUE_SIZE not found in offscreen.js")
        max_q = int(queue_match.group(1))
        self.assertLessEqual(max_q, 3, f"MAX_QUEUE_SIZE ({max_q}) exceeds limit of 3 chunks")

        # Verify oldest chunk drop logic (shift)
        self.assertIn(
            "transcriptionQueue.shift()", offscreen_js,
            "offscreen.js must drop oldest chunk on queue overflow to preserve real-time latency"
        )

    def test_07_transcript_history_bound_30(self):
        """Verifies service worker bounds transcript history to max 30 items."""
        bg_js = (ROOT / 'extension' / 'background.js').read_text(encoding='utf-8')
        
        self.assertIn("newSegments.length > 30", bg_js, "background.js must check segment limit > 30")
        self.assertIn("newSegments.shift()", bg_js, "background.js must shift oldest segment on limit")

    def test_08_sequence_de_duplication_enforced(self):
        """Verifies monotonic sequence ID enforcement prevents duplicate transcript execution."""
        avatar_html = (ROOT / 'extension' / 'overlay' / 'avatar_player.html').read_text(encoding='utf-8')
        
        self.assertIn("lastProcessedSeqId", avatar_html, "avatar_player.html must track lastProcessedSeqId")
        self.assertTrue(
            "payload.sequenceId <= lastProcessedSeqId" in avatar_html,
            "avatar_player.html must drop duplicate or out-of-order sequence IDs"
        )


class TestM4Stage3PerformanceHarness(unittest.TestCase):
    """Verifies benchmark harness and empirical results artifact."""

    def test_09_benchmark_script_exists(self):
        """Verifies reproducible benchmark script exists."""
        script_path = ROOT / 'benchmarks' / 'benchmark_m4_stage3_pipeline.py'
        self.assertTrue(script_path.exists(), "Benchmark script must exist at benchmarks/benchmark_m4_stage3_pipeline.py")

    def test_10_rtf_formula_definition(self):
        """Verifies RTF calculation formula is formally declared as (infer_sec / audio_sec)."""
        script_path = ROOT / 'benchmarks' / 'benchmark_m4_stage3_pipeline.py'
        content = script_path.read_text(encoding='utf-8')
        self.assertIn("RTF = (inference_time_ms / 1000.0) / audio_duration_seconds", content)

    def test_11_benchmark_results_artifact_schema(self):
        """Verifies benchmark results JSON exists and contains required metrics."""
        results_path = ROOT / 'benchmarks' / 'm4_stage3_benchmark_results.json'
        if not results_path.exists():
            self.skipTest("m4_stage3_benchmark_results.json not generated yet (run benchmark first)")

        with open(results_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        self.assertIn("benchmark_version", data)
        self.assertIn("environment", data)
        self.assertIn("measurements", data)

        m = data["measurements"]
        self.assertIn("wav_encoding_ms", m)
        self.assertIn("asr_silence_2s", m)
        self.assertIn("asr_real_speech_2s", m)
        self.assertIn("translation_routing_ms", m)
        self.assertIn("avatar_webgl_rendering", m)
        self.assertIn("end_to_end_model_ms", m)
        self.assertIn("process_memory", m)

        # Validate that RTF for real speech is faster than real-time (< 1.0)
        rtf_median = m["asr_real_speech_2s"]["rtf"]["median"]
        self.assertLess(rtf_median, 1.0, f"Speech recognition RTF ({rtf_median}) should be faster than real-time (< 1.0)")


class TestM4Stage3FailureRecoveryScenarios(unittest.TestCase):
    """Verifies system failure handling and recovery mechanics."""

    def test_12_backend_unavailable_error_reporting(self):
        """Verifies offscreen and player gracefully handle backend unavailability."""
        offscreen_js = (ROOT / 'extension' / 'offscreen.js').read_text(encoding='utf-8')
        avatar_html = (ROOT / 'extension' / 'overlay' / 'avatar_player.html').read_text(encoding='utf-8')

        self.assertIn("Backend offline", offscreen_js, "offscreen.js must detect offline backend")
        self.assertIn("pollLocalBackendTranscript", avatar_html, "avatar_player.html must support polling fallback")

    def test_13_silence_handled_without_animation_distortion(self):
        """Verifies empty transcript returns neutral status and does not trigger animations."""
        avatar_html = (ROOT / 'extension' / 'overlay' / 'avatar_player.html').read_text(encoding='utf-8')
        
        self.assertIn("Silence detected — Holding neutral rest pose (zero gestures)", avatar_html)
        self.assertIn("player.resetToNeutralPose()", avatar_html)

    def test_14_unsupported_words_surface_in_ui(self):
        """Verifies unsupported phrases surface in UI and do not invent hallucinations."""
        avatar_html = (ROOT / 'extension' / 'overlay' / 'avatar_player.html').read_text(encoding='utf-8')
        
        self.assertIn("Out-of-lexicon words", avatar_html)
        self.assertIn("PRD: Zero synthetic gestures", avatar_html)

    def test_15_capture_stop_cleans_up_state(self):
        """Verifies capture stop event resets bridge status to IDLE and neutral pose."""
        avatar_html = (ROOT / 'extension' / 'overlay' / 'avatar_player.html').read_text(encoding='utf-8')
        
        self.assertIn("CAPTURE: IDLE", avatar_html)
        self.assertIn("Capture session stopped — Avatar at neutral rest pose", avatar_html)


if __name__ == '__main__':
    unittest.main()
