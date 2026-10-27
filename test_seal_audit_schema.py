# Bismillah ir-Rahman ir-Rahim
"""Tests for N1 (v10.9.2): seal-coherence checks read sidecar format 2.0.

Before v10.9.2, _audit_seal_coherence read ``timestamp``, ``dual_seal``
and ``layers``, which no sealing path writes. Every freshly sealed file
got SC-004/SC-005 (MEDIUM) and SC-006 (HIGH), and checks 5 and 6 never
compared anything. Check 3 (HMAC plus master-witness recompute) still
caught content changes.

What this fix does NOT prove: there is still no seal time in the
sidecar, so no temporal check runs; SC-004 says so as INFO.

Runs under pytest or unittest.
"""
# Bismillah ir-Rahman ir-Rahim

import contextlib
import io
import json
import os
import shutil
import sys
import tempfile
import time
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

with contextlib.redirect_stdout(io.StringIO()):
    import bismillah_encoder as be  # noqa: E402

FILES = {
    "notes.md": "Plain notes\nSecond line\n",
    "arabic.txt": "\u0633\u0644\u0627\u0645\n",
    "code.py": "def f(x):\n    return x\n",
}


def coherence(path):
    with contextlib.redirect_stdout(io.StringIO()):
        return be._audit_seal_coherence(path)


def codes(result, severity=None):
    return [f["code"] for f in result["findings"] if severity is None or f["severity"] == severity]


class SealedDir(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.mkdtemp()
        for name, text in FILES.items():
            with open(os.path.join(self.d, name), "w", encoding="utf-8") as fh:
                fh.write(text)
        with contextlib.redirect_stdout(io.StringIO()):
            be.seal_directory(self.d)

    def tearDown(self):
        shutil.rmtree(self.d)

    def path(self, name):
        return os.path.join(self.d, name)

    def edit_sidecar(self, name, change):
        side = self.path(name) + ".witness.bismillah"
        with open(side, encoding="utf-8") as fh:
            data = json.load(fh)
        change(data["witness"])
        with open(side, "w", encoding="utf-8") as fh:
            json.dump(data, fh)


class TestFreshSealIsCoherent(SealedDir):
    def test_no_false_warnings_on_fresh_seal(self):
        for name in FILES:
            r = coherence(self.path(name))
            self.assertTrue(r["coherent"], name)
            self.assertEqual(codes(r), ["SC-004"], name)
            self.assertEqual(codes(r, "INFO"), ["SC-004"], name)
            self.assertEqual((r["checks_passed"], r["checks_total"]), (5, 5), name)
            self.assertEqual(r["checks_not_available"], ["seal_time_vs_mtime"], name)

    def test_temporal_note_does_not_claim_a_check_ran(self):
        r = coherence(self.path("notes.md"))
        note = r["findings"][0]
        self.assertIn("not available", note["description"])
        self.assertIn("2.0", note["detail"])

    def test_full_audit_reports_version(self):
        with contextlib.redirect_stdout(io.StringIO()):
            r = be.audit_file(self.path("code.py"))
        self.assertEqual(r["audit_version"], "10.9.2")


class TestChangesAreStillCaught(SealedDir):
    def test_modified_content_fails_hmac_and_now_content_hash(self):
        time.sleep(0.01)
        p = self.path("notes.md")
        with open(p, encoding="utf-8") as fh:
            text = fh.read()
        with open(p, "w", encoding="utf-8") as fh:
            fh.write(text.replace("Second line", "Second LINE", 1))
        r = coherence(p)
        self.assertFalse(r["coherent"])
        self.assertIn("SC-003", codes(r, "CRITICAL"))
        # SC-005 compares against muhkam_seal; before v10.9.2 it never ran.
        self.assertIn("SC-005", codes(r, "CRITICAL"))

    def test_missing_layer_seal_is_reported(self):
        self.edit_sidecar("notes.md", lambda w: w["heavens"][3]["layer_seals"].pop())
        r = coherence(self.path("notes.md"))
        sc6 = [f for f in r["findings"] if f["code"] == "SC-006"]
        self.assertEqual(len(sc6), 1)
        self.assertEqual(sc6[0]["severity"], "HIGH")
        self.assertIn("153/154", sc6[0]["description"])
        self.assertIn("heaven 3", sc6[0]["detail"])

    def test_consistent_heaven_but_short_total_is_reported(self):
        # Each heaven agrees with itself, but the seals add up to 153.
        def short(w):
            w["heavens"][5]["layer_seals"].pop()
            w["heavens"][5]["layer_count"] = 13
        self.edit_sidecar("notes.md", short)
        r = coherence(self.path("notes.md"))
        sc6 = [f for f in r["findings"] if f["code"] == "SC-006"]
        self.assertEqual(len(sc6), 1)
        self.assertIn("153 layer seals in total", sc6[0]["detail"])

    def test_wrong_total_or_heaven_count_is_reported(self):
        self.edit_sidecar("code.py", lambda w: w.update(total_layers=150))
        self.assertIn("SC-006", codes(coherence(self.path("code.py")), "HIGH"))
        self.edit_sidecar("arabic.txt", lambda w: w["heavens"].pop())
        self.assertIn("SC-006", codes(coherence(self.path("arabic.txt")), "HIGH"))

    def test_missing_muhkam_seal_is_reported(self):
        self.edit_sidecar("code.py", lambda w: w.pop("muhkam_seal"))
        r = coherence(self.path("code.py"))
        sc5 = [f for f in r["findings"] if f["code"] == "SC-005"]
        self.assertEqual([f["severity"] for f in sc5], ["MEDIUM"])
        self.assertIn("No muhkam seal", sc5[0]["description"])


class TestLegacyShapesStillHonoured(SealedDir):
    def test_flat_layers_list_still_checked(self):
        self.edit_sidecar("notes.md", lambda w: w.update(layers=list(range(154))))
        self.assertNotIn("SC-006", codes(coherence(self.path("notes.md"))))
        self.edit_sidecar("notes.md", lambda w: w.update(layers=list(range(10))))
        self.assertIn("SC-006", codes(coherence(self.path("notes.md")), "HIGH"))

    def test_timestamp_when_present_is_compared(self):
        self.edit_sidecar("notes.md", lambda w: w.update(timestamp="2000-01-01T00:00:00+00:00"))
        r = coherence(self.path("notes.md"))
        sc4 = [f for f in r["findings"] if f["code"] == "SC-004"]
        self.assertEqual([f["severity"] for f in sc4], ["HIGH"])
        self.assertEqual(r["checks_not_available"], [])


class TestHeavenLayerProblems(unittest.TestCase):
    def good(self):
        return [{"layer_count": 14, "layer_seals": ["s"] * 14} for _ in range(11)]

    def test_valid_record(self):
        self.assertEqual(be._heaven_layer_problems(self.good(), 154), (154, []))

    def test_each_defect_named(self):
        h = self.good()
        h[0]["layer_count"] = 13
        counted, problems = be._heaven_layer_problems(h, 154)
        self.assertEqual(counted, 154)
        self.assertTrue(any("heaven 0 layer_count 13" in p for p in problems))
        self.assertEqual(be._heaven_layer_problems(None, 154)[1], ["heavens is NoneType, expected a list"])
        _, problems = be._heaven_layer_problems(self.good(), "154")
        self.assertTrue(any("total_layers" in p for p in problems))


if __name__ == "__main__":
    unittest.main()

# Bismillah ir-Rahman ir-Rahim
