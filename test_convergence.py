# Bismillah ir-Rahman ir-Rahim
"""
Test suite for bismillah_convergence -- mode collapse detection,
anti-collapse dispatch generation, and convergence tracking records.
"""
# Bismillah ir-Rahman ir-Rahim

import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from bismillah_convergence import (
    compute_m1_echo_ratio,
    compute_m2_anchoring_ratio,
    compute_m7_posture_count,
    classify_munafiq_process,
    generate_anti_collapse_dispatch,
    create_convergence_record,
    add_review_to_record,
    PROCESS_1_ALIGNED,
    PROCESS_2_SHALLOW,
    PROCESS_3_PERFORMING,
    PROCESS_UNASSESSED,
    _POSTURE_WORDS,
    _same_lineage,
)
from bismillah_encoder import SealFinding, make_finding, LAYER_L0


def _finding(message, filepath="a.txt"):
    return make_finding(filepath, LAYER_L0, "TEST-CODE", "WARNING", message)


class TestModeCollapseMarkers(unittest.TestCase):
    """Upgrades 6 -- M1/M2/M7 markers and process classification."""

    def test_m1_echo_ratio(self):
        dispatch = "error paths need structured findings and layer mapping"
        echoed = [_finding("error paths need structured findings"),
                  _finding("layer mapping")]
        fresh = [_finding("a defect nobody predicted")]
        self.assertEqual(compute_m1_echo_ratio(echoed, dispatch), 1.0)
        self.assertEqual(compute_m1_echo_ratio(fresh, dispatch), 0.0)
        self.assertEqual(compute_m1_echo_ratio([], dispatch), 0.0)

    def test_m2_anchoring_ratio(self):
        anchored = [_finding("m", filepath="src/a.py"), _finding("m", filepath="src/b.py")]
        unanchored = [_finding("m", filepath=""), _finding("m", filepath="unknown")]
        self.assertEqual(compute_m2_anchoring_ratio(anchored), 0.0)
        self.assertEqual(compute_m2_anchoring_ratio(unanchored), 1.0)

    def test_m7_posture_count_detects_literal_words(self):
        for word in _POSTURE_WORDS:
            self.assertEqual(compute_m7_posture_count(word), 1)
        self.assertEqual(compute_m7_posture_count("clean text"), 0)
        self.assertGreater(compute_m7_posture_count("this blocks all attacks"), 0)

    def test_classify_hard_signals(self):
        self.assertEqual(classify_munafiq_process({"M5_weight_overclaim": 0.6}),
                         PROCESS_3_PERFORMING)
        self.assertEqual(classify_munafiq_process({"M8_spec_impl_gap": 0.8}),
                         PROCESS_3_PERFORMING)

    def test_classify_m2_unanchored_is_process_3(self):
        """The framework names any unanchored payload a Process 3 signal."""
        self.assertEqual(classify_munafiq_process({"M2_unanchored": 1}),
                         PROCESS_3_PERFORMING)

    def test_classify_no_markers_is_unassessed(self):
        """An empty measurement is UNKNOWN, never alignment by default."""
        self.assertEqual(classify_munafiq_process({}), PROCESS_UNASSESSED)

    def test_classify_measured_clean_is_aligned(self):
        self.assertEqual(classify_munafiq_process({"M1_echo_ratio": 0.1}),
                         PROCESS_1_ALIGNED)

    def test_classify_compound_shallow(self):
        markers = {"M1_echo_ratio": 0.8, "M3_exclusion_absence": 0.6}
        self.assertEqual(classify_munafiq_process(markers), PROCESS_2_SHALLOW)

    def test_classify_posture_compound_performing(self):
        markers = {"M7_posture_words": 2, "M1_echo_ratio": 0.5}
        self.assertEqual(classify_munafiq_process(markers), PROCESS_3_PERFORMING)


class TestAntiCollapseDispatch(unittest.TestCase):
    """Upgrade 7 -- dispatch generation with Anti-M requirements."""

    def test_dispatch_contains_anti_m_sections(self):
        text = generate_anti_collapse_dispatch(
            "SealFinding namedtuple", 1, "Copilot", 1, "abc123",
            "structured error capture")
        for section in ("Anti-M1", "Anti-M2", "Anti-M3", "Anti-M5",
                        "Anti-M7", "Anti-M8"):
            self.assertIn(section, text)
        self.assertIn("Copilot", text)
        self.assertIn("abc123", text)
        self.assertIn("Tier 1", text)
        # The generated dispatch carries the literal grep pattern
        # (assembled from split strings in the source module).
        self.assertIn("pre" + "vents", text)

    def test_dispatch_template_no_self_trigger_in_source(self):
        """The module source itself must pass the posture check."""
        import bismillah_convergence
        import inspect
        source = inspect.getsource(bismillah_convergence)
        self.assertEqual(compute_m7_posture_count(source), 0)


class TestConvergenceRecords(unittest.TestCase):
    """Upgrade 8 -- structured convergence tracking."""

    def test_record_starts_open_weight_zero(self):
        record = create_convergence_record("SealFinding", "C04", 1)
        self.assertEqual(record["status"], "OPEN")
        self.assertEqual(record["total_weight"], 0.0)
        self.assertFalse(record["converged"])
        self.assertTrue(record["producer"]["quarantined"])

    def test_producer_quarantine_enforced(self):
        record = create_convergence_record("SealFinding", "C04", 1)
        with self.assertRaises(ValueError):
            add_review_to_record(record, record["producer"]["family"], 1,
                                 "PASS", 0)

    def test_convergence_requires_two_tier1(self):
        record = create_convergence_record("SealFinding", "C04", 1)
        add_review_to_record(record, "Copilot", 1, "PASS", 3)
        self.assertEqual(record["total_weight"], 1.0)
        self.assertFalse(record["converged"])
        add_review_to_record(record, "ChatGPT", 1, "PASS", 2)
        self.assertEqual(record["total_weight"], 2.0)
        self.assertTrue(record["converged"])
        self.assertEqual(record["status"], "CONVERGED")

    def test_tier2_weights_and_non_pass(self):
        record = create_convergence_record("SealFinding", "C04", 1)
        add_review_to_record(record, "Kimi k3", 2, "PASS", 5)
        self.assertEqual(record["total_weight"], 0.75)
        add_review_to_record(record, "Grok", 2, "HALT", 4)
        self.assertEqual(record["total_weight"], 0.75)
        self.assertEqual(record["status"], "HALTED")
        self.assertFalse(record["converged"])

    def test_invalid_verdict_rejected(self):
        record = create_convergence_record("SealFinding", "C04", 1)
        with self.assertRaises(ValueError):
            add_review_to_record(record, "Copilot", 1, "FAIL", 0)

    def test_invalid_tier_rejected(self):
        record = create_convergence_record("SealFinding", "C04", 1)
        for tier in (0, 3, "1", None):
            with self.assertRaises(ValueError):
                add_review_to_record(record, "Copilot", tier, "PASS", 0)

    def test_same_family_cannot_supply_weight_twice(self):
        """Two PASS entries from one family must not reach weight 2.0."""
        record = create_convergence_record("SealFinding", "C04", 1)
        add_review_to_record(record, "Copilot", 1, "PASS", 2)
        add_review_to_record(record, "Copilot", 1, "PASS", 1)
        self.assertEqual(record["total_weight"], 1.0)
        self.assertFalse(record["converged"])
        self.assertEqual(record["status"], "OPEN")

    def test_tier2_only_never_converges(self):
        """Three Tier 2 passes reach 2.25 weight but lack a Tier 1 family."""
        record = create_convergence_record("SealFinding", "C04", 1)
        for family in ("Kimi k3", "Grok", "Meta"):
            add_review_to_record(record, family, 2, "PASS", 3)
        self.assertEqual(record["total_weight"], 2.25)
        self.assertFalse(record["converged"])
        self.assertEqual(record["status"], "OPEN")

    def test_tier1_plus_two_tier2_converges(self):
        record = create_convergence_record("SealFinding", "C04", 1)
        add_review_to_record(record, "Copilot", 1, "PASS", 2)
        add_review_to_record(record, "Kimi k3", 2, "PASS", 3)
        add_review_to_record(record, "Grok", 2, "PASS", 1)
        self.assertEqual(record["total_weight"], 2.5)
        self.assertTrue(record["converged"])

    def test_halt_blocks_convergence_even_at_weight(self):
        """Two Tier 1 passes followed by HALT must not stay CONVERGED."""
        record = create_convergence_record("SealFinding", "C04", 1)
        add_review_to_record(record, "Copilot", 1, "PASS", 2)
        add_review_to_record(record, "ChatGPT", 1, "PASS", 1)
        self.assertTrue(record["converged"])
        add_review_to_record(record, "Grok", 2, "HALT", 4)
        self.assertFalse(record["converged"])
        self.assertEqual(record["status"], "HALTED")

    def test_producer_lineage_bypass_rejected(self):
        """Reviewing under 'GLM-5.3' while the producer is 'Perplexity
        Computer (GLM-5.3)' is a producer-lineage bypass and is
        rejected under canonical token matching."""
        record = create_convergence_record("SealFinding", "C04", 1)
        with self.assertRaises(ValueError):
            add_review_to_record(record, "GLM-5.3", 1, "PASS", 0)
        self.assertTrue(_same_lineage("GLM-5.3",
                                      "Perplexity Computer (GLM-5.3)"))
        self.assertFalse(_same_lineage("Copilot",
                                      "Perplexity Computer (GLM-5.3)"))

    def test_review_of_different_commit_not_counted(self):
        """A review bound to another commit is stored but carries no
        weight against this record's artifact."""
        record = create_convergence_record("SealFinding", "C04", 1,
                                           commit_hash="aaa111")
        add_review_to_record(record, "Copilot", 1, "PASS", 2,
                              commit_hash="bbb222")
        add_review_to_record(record, "ChatGPT", 1, "PASS", 1,
                              commit_hash="aaa111")
        self.assertEqual(record["total_weight"], 1.0)
        self.assertFalse(record["converged"])
        stored = [r for r in record["reviews"] if r["family"] == "Copilot"]
        self.assertEqual(len(stored), 1)  # stored, not silently dropped


# Bismillah ir-Rahman ir-Rahim

if __name__ == '__main__':
    unittest.main()

# Bismillah ir-Rahman ir-Rahim
