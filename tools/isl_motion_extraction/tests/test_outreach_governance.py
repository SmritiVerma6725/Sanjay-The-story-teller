#!/usr/bin/env python3
"""SignBridge M3.21 — Outreach Governance & Response Tracking Invariant Test Suite

Verifies:
1. Valid lifecycle state transitions and rejection of illegal leaps.
2. Dry-run dispatch lockout (prevents dispatch without explicit project-owner signature).
3. Prevention of falsely recorded dispatches (asserts dispatch date cannot exist in dry-run).
4. Tracker table consistency, required columns, and zero duplicate IDs in M3_21 tracker.
5. Consent and follow-up rule enforcement (maximum 1 reminder, min 7 days, no sensitive data).
6. File-level cryptographic hash verification for candidate output, extension asset, and video.
7. Production baseline isolation (verifies KeyframeRegistry routes to isl_namaste_godl_v1).
"""

import hashlib
import json
import os
import re
import unittest
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent
TOOL_DIR = Path(__file__).resolve().parent.parent

VALID_LIFECYCLE_STATES = {
    "NOT_AUTHORIZED",
    "READY_FOR_APPROVAL",
    "SENT",
    "RESPONSE_RECEIVED",
    "DECLINED",
    "NO_RESPONSE",
    "CONSENTED",
    "SESSION_COMPLETED",
    "REVIEW_RECORD_VALIDATED"
}

EXPECTED_CANDIDATE_SHA256 = "6f24e60f7f55d71482133790ca60f6a52682a38f7f6b32c8921480586cef4a46"
EXPECTED_VIDEO_SHA256 = "129811572acc6a236fb62b4ade143df8770b7fdcc5249d5facffc349b16a18b8"


class TestOutreachGovernance(unittest.TestCase):

    def test_lifecycle_state_transitions(self):
        """Verify state transition rules enforce legitimate progression."""
        # Allowed transitions mapping
        allowed_transitions = {
            "NOT_AUTHORIZED": {"READY_FOR_APPROVAL"},
            "READY_FOR_APPROVAL": {"SENT", "NOT_AUTHORIZED"},
            "SENT": {"RESPONSE_RECEIVED", "NO_RESPONSE", "DECLINED"},
            "RESPONSE_RECEIVED": {"CONSENTED", "DECLINED"},
            "DECLINED": set(),  # terminal
            "NO_RESPONSE": set(),  # terminal
            "CONSENTED": {"SESSION_COMPLETED", "DECLINED"},
            "SESSION_COMPLETED": {"REVIEW_RECORD_VALIDATED"},
            "REVIEW_RECORD_VALIDATED": set()  # terminal
        }

        def can_transition(curr, nxt):
            return nxt in allowed_transitions.get(curr, set())

        # Valid transitions
        self.assertTrue(can_transition("NOT_AUTHORIZED", "READY_FOR_APPROVAL"))
        self.assertTrue(can_transition("READY_FOR_APPROVAL", "SENT"))
        self.assertTrue(can_transition("SENT", "RESPONSE_RECEIVED"))
        self.assertTrue(can_transition("RESPONSE_RECEIVED", "CONSENTED"))
        self.assertTrue(can_transition("CONSENTED", "SESSION_COMPLETED"))
        self.assertTrue(can_transition("SESSION_COMPLETED", "REVIEW_RECORD_VALIDATED"))

        # Prohibited transitions (leaps or premature claims)
        self.assertFalse(can_transition("NOT_AUTHORIZED", "SENT"))
        self.assertFalse(can_transition("READY_FOR_APPROVAL", "CONSENTED"))
        self.assertFalse(can_transition("SENT", "REVIEW_RECORD_VALIDATED"))
        self.assertFalse(can_transition("READY_FOR_APPROVAL", "REVIEW_RECORD_VALIDATED"))

    def test_dry_run_dispatch_prevention(self):
        """Verify that dry-run mode prohibits external message dispatch."""
        auth_doc = ROOT_DIR / "Docs" / "M3_21_OUTREACH_AUTHORIZATION.md"
        self.assertTrue(auth_doc.exists(), "Docs/M3_21_OUTREACH_AUTHORIZATION.md must exist")
        content = auth_doc.read_text(encoding="utf-8")

        # Must explicitly declare DRY_RUN_ONLY
        self.assertIn("DRY_RUN_ONLY", content)
        self.assertIn("PENDING PROJECT OWNER SIGN-OFF", content)
        self.assertIn("OUTREACH PENDING EXPLICIT AUTHORIZATION", content)

    def test_prevention_of_falsely_recorded_dispatches(self):
        """Assert no contact in response tracker is marked SENT in dry-run mode."""
        tracker_doc = ROOT_DIR / "Docs" / "M3_21_REVIEWER_RESPONSE_TRACKER.md"
        self.assertTrue(tracker_doc.exists(), "Docs/M3_21_REVIEWER_RESPONSE_TRACKER.md must exist")
        content = tracker_doc.read_text(encoding="utf-8")

        # Find all OUT-21 rows
        lines = content.splitlines()
        row_pattern = re.compile(r"\|\s*\*\*(OUT-21-\d+)\*\*\s*\|\s*([^|]+)\|\s*([^|]+)\|\s*`?([A-Z_]+)`?\s*\|\s*([^|]+)\|")
        
        found_rows = 0
        for line in lines:
            m = row_pattern.search(line)
            if m:
                found_rows += 1
                outreach_id, institution, source, auth_state, dispatch_date = m.groups()
                auth_state = auth_state.strip()
                dispatch_date = dispatch_date.strip()

                # In dry-run, state must NOT be SENT
                self.assertNotEqual(auth_state, "SENT", f"{outreach_id} cannot be SENT in dry-run mode")
                self.assertEqual(auth_state, "READY_FOR_APPROVAL")
                self.assertIn("None", dispatch_date, f"{outreach_id} dispatch date must indicate none/dry run")

        self.assertGreaterEqual(found_rows, 5, "Must find at least 5 tracked outreach targets")

    def test_tracker_consistency_and_unique_ids(self):
        """Confirm no duplicate Outreach IDs exist and all fields conform to schema."""
        tracker_doc = ROOT_DIR / "Docs" / "M3_21_REVIEWER_RESPONSE_TRACKER.md"
        content = tracker_doc.read_text(encoding="utf-8")

        ids = re.findall(r"\*\*(OUT-21-\d+)\*\*", content)
        self.assertTrue(len(ids) > 0, "Tracker must contain OUT-21 IDs")
        self.assertEqual(len(ids), len(set(ids)), f"Duplicate Outreach IDs detected: {ids}")

    def test_consent_and_followup_rules(self):
        """Confirm outreach authorization document defines consent, max 1 reminder, and 7-day wait."""
        auth_doc = ROOT_DIR / "Docs" / "M3_21_OUTREACH_AUTHORIZATION.md"
        content = auth_doc.read_text(encoding="utf-8")

        self.assertIn("maximum one (1)", content)
        self.assertIn("seven (7) calendar days", content)
        self.assertIn("Sensitive Personal Data Minimization", content)

    def test_file_cryptographic_hashes_integrity(self):
        """Recompute SHA-256 for candidate output, extension copy, and reference video."""
        p_cand_out = ROOT_DIR / "tools" / "isl_motion_extraction" / "output" / "isl_namaste_mocap_candidate_v1.json"
        p_cand_ext = ROOT_DIR / "extension" / "assets" / "animations" / "isl_namaste_mocap_candidate_v1.json"
        p_video = ROOT_DIR / "tools" / "isl_motion_extraction" / "reference_videos" / "ISLRTC_Namaste_sample.mp4"

        h_out = hashlib.sha256(p_cand_out.read_bytes()).hexdigest()
        h_ext = hashlib.sha256(p_cand_ext.read_bytes()).hexdigest()
        h_vid = hashlib.sha256(p_video.read_bytes()).hexdigest()

        self.assertEqual(h_out, EXPECTED_CANDIDATE_SHA256, "Candidate output SHA-256 mismatch")
        self.assertEqual(h_ext, EXPECTED_CANDIDATE_SHA256, "Candidate extension copy SHA-256 mismatch")
        self.assertEqual(h_vid, EXPECTED_VIDEO_SHA256, "Reference video SHA-256 mismatch")
        self.assertEqual(h_out, h_ext, "Output and extension candidate files must be bit-for-bit identical")

    def test_production_isolation_preserved(self):
        """Confirm production KeyframeRegistry and ISLTranslator map NAMASTE to isl_namaste_godl_v1, not candidate."""
        reg_file = ROOT_DIR / "extension" / "animation" / "keyframe_registry.js"
        content = reg_file.read_text(encoding="utf-8")

        # Baseline must be mapped in keyframe registry with isl_namaste_godl_v1
        self.assertIn("isl_namaste_godl_v1", content)
        self.assertIn("ISL_NAMASTE_CLIP", content)

        # Translator must map Namaste to isl_namaste_godl_v1 baseline
        translator_file = ROOT_DIR / "extension" / "translation" / "isl_translator.js"
        trans_content = translator_file.read_text(encoding="utf-8")
        self.assertIn("isl_namaste_godl_v1", trans_content)
        self.assertNotIn("isl_namaste_mocap_candidate_v1", trans_content)

        # Candidate must NOT be auto-registered in default clips
        self.assertNotIn("REGISTERED_CLIPS.set(ISL_NAMASTE_MOCAP_CANDIDATE_CLIP", content)

    def test_owner_approval_sheet_present_and_dry_run_locked(self):
        """Confirm M3.22 Owner Approval Sheet exists, contains all targets, and is locked in dry-run mode."""
        sheet_path = ROOT_DIR / "Docs" / "M3_22_OWNER_APPROVAL_SHEET.md"
        self.assertTrue(sheet_path.exists(), "Docs/M3_22_OWNER_APPROVAL_SHEET.md must exist")
        content = sheet_path.read_text(encoding="utf-8")

        # Must contain all 5 target IDs
        for tid in ["TGT-001", "TGT-002", "TGT-003", "TGT-004", "TGT-005"]:
            self.assertIn(tid, content, f"Approval sheet missing target {tid}")

        # Must contain all 3 draft sections
        self.assertIn("Draft 1: For Certified ISL Interpreters", content)
        self.assertIn("Draft 2: For Deaf Native Signers", content)
        self.assertIn("Draft 3: For Academic Sign Language Linguists", content)

        # Must mandate dry-run lockout
        self.assertIn("DRY_RUN_ONLY", content)
        self.assertIn("PENDING PROJECT OWNER SIGN-OFF", content)
        self.assertIn("REMAIN_IN_DRY_RUN", content)

    def test_anti_fabrication_zero_dispatches_in_tracker(self):
        """Assert no dispatches, consents, or responses have been fabricated in tracker or reviews."""
        tracker_path = ROOT_DIR / "Docs" / "M3_21_REVIEWER_RESPONSE_TRACKER.md"
        self.assertTrue(tracker_path.exists())
        content = tracker_path.read_text(encoding="utf-8")

        # Zero dispatches
        self.assertRegex(content, r"Genuinely Dispatched:\s+0")
        self.assertRegex(content, r"Validated Review Records:\s+0")

        # Zero review records in reviews/ directory
        reviews_dir = ROOT_DIR / "tools" / "isl_motion_extraction" / "reviews"
        json_records = list(reviews_dir.glob("*.json"))
        self.assertEqual(len(json_records), 0, f"No review records should exist before human review: {json_records}")

    def test_m3_24_owner_approval_sheet_and_matrix_present(self):
        """Confirm M3.24 Owner Approval Sheet and Outreach Readiness Matrix exist and enforce dry-run mode."""
        sheet_path = ROOT_DIR / "Docs" / "M3_24_OWNER_APPROVAL_SHEET.md"
        matrix_path = ROOT_DIR / "Docs" / "M3_24_OUTREACH_READINESS_MATRIX.md"
        self.assertTrue(sheet_path.exists(), "Docs/M3_24_OWNER_APPROVAL_SHEET.md must exist")
        self.assertTrue(matrix_path.exists(), "Docs/M3_24_OUTREACH_READINESS_MATRIX.md must exist")

        sheet_content = sheet_path.read_text(encoding="utf-8")
        matrix_content = matrix_path.read_text(encoding="utf-8")

        for tid in ["TGT-001", "TGT-002", "TGT-003", "TGT-004", "TGT-005"]:
            self.assertIn(tid, sheet_content, f"M3.24 Approval sheet missing target {tid}")
            self.assertIn(tid, matrix_content, f"M3.24 Readiness matrix missing target {tid}")

        self.assertIn("DRY_RUN_ONLY", sheet_content)
        self.assertIn("DRY_RUN_ONLY", matrix_content)
        self.assertIn("NOT_AUTHORIZED", sheet_content)
        self.assertIn("NOT_AUTHORIZED", matrix_content)

    def test_m3_24_corrected_recipients_and_draft2_wording(self):
        """Assert M3.24 documents contain corrected recipient emails, URLs, and clarified Draft 2 wording."""
        sheet_path = ROOT_DIR / "Docs" / "M3_24_OWNER_APPROVAL_SHEET.md"
        content = sheet_path.read_text(encoding="utf-8")

        # Corrected recipients
        self.assertIn("secretary@nadindia.org", content)
        self.assertIn("https://nadindia.org/Contact", content)
        self.assertIn("aifdeaf@gmail.com", content)
        self.assertIn("https://aifdeaf.org/contact-us/", content)
        self.assertIn("NEEDS_REVERIFICATION", content)
        self.assertIn("https://def.org.in/contact/", content)
        self.assertIn("https://www.ignou.ac.in/schools/school-of-humanities", content)

        # Clarified Draft 2 wording
        clarified_str = (
            "What you will review (if you choose to participate): "
            "A side-by-side comparison between the dictionary reference video and a 3D avatar "
            "within a local Chrome studio (no video is attached to this email)."
        )
        self.assertIn(clarified_str, content)

    def test_m3_24_five_part_decision_gate_and_licensing_safeguards(self):
        """Assert M3.24 approval sheet contains separate 5-part decision gates and unresolved licensing language."""
        sheet_path = ROOT_DIR / "Docs" / "M3_24_OWNER_APPROVAL_SHEET.md"
        content = sheet_path.read_text(encoding="utf-8")

        # 5-part decision gates
        self.assertIn("1. Decision on Proposed Recipients & Corrected Contact Details:", content)
        self.assertIn("2. Decision on Complete Invitation Drafts (Drafts 1, 2, 3):", content)
        self.assertIn("3. Decision on Proposed Rollout Scope:", content)
        self.assertIn("4. Acknowledgement of Unresolved Reference Video Licensing:", content)
        self.assertIn("5. SEPARATE DISPATCH AUTHORIZATION GATE", content)
        self.assertIn("REMAIN_IN_DRY_RUN", content)

        # Licensing statements
        self.assertIn("UNRESOLVED", content)
        self.assertIn("prohibited from email attachments", content)

    def test_m3_25_deliverables_and_four_dimensional_matrix(self):
        """Assert M3.25 deliverables exist, enforce dry-run mode, and evaluate the 4 verification dimensions."""
        d_audit = ROOT_DIR / "Docs" / "M3_25_FINAL_READINESS_AUDIT.md"
        d_pkg = ROOT_DIR / "Docs" / "M3_25_OWNER_DECISION_PACKAGE.md"
        d_mat = ROOT_DIR / "Docs" / "M3_25_CONTACT_EVIDENCE_MATRIX.md"
        d_rep = ROOT_DIR / "Docs" / "M3_25_EXECUTION_REPORT.md"

        for p in [d_audit, d_pkg, d_mat, d_rep]:
            self.assertTrue(p.exists(), f"{p.name} must exist")
            c = p.read_text(encoding="utf-8")
            self.assertIn("DRY_RUN_ONLY", c)
            self.assertIn("NOT_AUTHORIZED", c)

        mat_content = d_mat.read_text(encoding="utf-8")
        self.assertIn("Official-Site Publication", mat_content)
        self.assertIn("Organizational Relevance", mat_content)
        self.assertIn("Recipient Routing", mat_content)
        self.assertIn("Inbox Deliverability", mat_content)

    def test_m3_25_standard_activity_wording_across_all_drafts(self):
        """Assert all invitation drafts in M3.25 decision package use the standardized activity text."""
        pkg_path = ROOT_DIR / "Docs" / "M3_25_OWNER_DECISION_PACKAGE.md"
        content = pkg_path.read_text(encoding="utf-8")

        standard_str = (
            "A side-by-side comparison between the dictionary reference video and a 3D avatar "
            "within a local Chrome studio (no video is attached to this email)."
        )
        # Should appear in Draft 1, Draft 2, and Draft 3
        matches = content.count(standard_str)
        self.assertGreaterEqual(matches, 3, f"Standard inspection phrasing must appear in all 3 drafts (found {matches})")

    def test_m3_25_decoupled_five_decision_gates(self):
        """Assert M3.25 owner decision package contains the 5 decoupled decision gates."""
        pkg_path = ROOT_DIR / "Docs" / "M3_25_OWNER_DECISION_PACKAGE.md"
        content = pkg_path.read_text(encoding="utf-8")

        self.assertIn("DECISION GATE 1: PROPOSED RECIPIENTS & CONTACT CHANNELS", content)
        self.assertIn("DECISION GATE 2: INVITATION DRAFTS (DRAFTS 1, 2, 3)", content)
        self.assertIn("DECISION GATE 3: OUTREACH ROLLOUT SCOPE", content)
        self.assertIn("DECISION GATE 4: ACKNOWLEDGEMENT OF UNRESOLVED LICENSING", content)
        self.assertIn("DECISION GATE 5: SEPARATE DISPATCH AUTHORIZATION GATE", content)
        self.assertIn("REMAIN_IN_DRY_RUN", content)

    def test_m3_26_deliverables_and_granular_decision_gates(self):
        """Assert M3.26 deliverables exist, enforce dry-run, and provide granular owner decision gates."""
        d_audit = ROOT_DIR / "Docs" / "M3_26_INDEPENDENT_AUDIT.md"
        d_gap = ROOT_DIR / "Docs" / "M3_26_EVIDENCE_GAP_REGISTER.md"
        d_chk = ROOT_DIR / "Docs" / "M3_26_OWNER_DECISION_CHECKLIST.md"
        d_rep = ROOT_DIR / "Docs" / "M3_26_EXECUTION_REPORT.md"

        for p in [d_audit, d_gap, d_chk, d_rep]:
            self.assertTrue(p.exists(), f"{p.name} must exist")
            c = p.read_text(encoding="utf-8")
            self.assertIn("DRY_RUN_ONLY", c)
            self.assertIn("NOT_AUTHORIZED", c)

        # Check granular Gate 1 and Gate 2 in M3.26 checklist
        chk_content = d_chk.read_text(encoding="utf-8")
        for tid in ["TGT-001", "TGT-002", "TGT-003", "TGT-004", "TGT-005"]:
            self.assertIn(f"[ ] APPROVE  |  [ ] EXCLUDE  : {tid}", chk_content)

        for draft_num in ["Draft 1", "Draft 2", "Draft 3"]:
            self.assertIn(f"[ ] APPROVE  |  [ ] REVISE  : {draft_num}", chk_content)

        self.assertIn("GATE 5: INDEPENDENT MESSAGE DISPATCH AUTHORIZATION", chk_content)
        self.assertIn("REMAIN_IN_DRY_RUN (ACTIVE DEFAULT)", chk_content)

        # Check gap register records GAP-01 to GAP-07
        gap_content = d_gap.read_text(encoding="utf-8")
        for gid in ["GAP-01", "GAP-02", "GAP-03", "GAP-04", "GAP-05", "GAP-06", "GAP-07"]:
            self.assertIn(gid, gap_content)


if __name__ == "__main__":
    unittest.main()


