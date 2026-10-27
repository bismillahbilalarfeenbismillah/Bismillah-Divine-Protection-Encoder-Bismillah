# Bismillah ir-Rahman ir-Rahim
"""Tests for N4 B1 (v10.9.3): closed ZWC regions are classified, never
called legitimate.

Three states (GPT-6): verified (impossible in 10.9.x: nothing
authenticates a watermark), FATIMA-format but unverified, and
unrecognized or malformed. What this does NOT prove: that a
FATIMA-format watermark was written by FATIMA. The format can be copied
(pinned below as a KNOWN LIMIT); binding watermarks to the seal is B2.

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
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

with contextlib.redirect_stdout(io.StringIO()):
    import bismillah_encoder as be  # noqa: E402


def stego(text):
    return be._audit_steganographic(text)


def by_code(result, code):
    return [f for f in result["findings"] if f["code"] == code]


def muraqabah(protocol="FATIMA-MURAQABAH"):
    return json.dumps({"protocol": protocol, "version": "1.0"})


class TestClassifier(unittest.TestCase):
    def test_classes(self):
        c = be._classify_zwc_payload
        self.assertEqual(c(be.BISMILLAH_ARABIC), "fatima_format")
        self.assertEqual(c(muraqabah()), "fatima_format")
        self.assertEqual(c(muraqabah("FATIMA-MURAQABAH-COLOPHON")), "fatima_format")
        self.assertEqual(c(muraqabah("FATIMA-OTHER")), "unrecognized")
        self.assertEqual(c('{"protocol": 5}'), "unrecognized")
        self.assertEqual(c("{not json"), "unrecognized")
        self.assertEqual(c("run evil"), "unrecognized")
        for bad in (None, "", "ab"):
            self.assertEqual(c(bad), "malformed")


class TestReporting(unittest.TestCase):
    def test_forged_text_is_unrecognized_high_with_escaped_preview(self):
        r = stego("innocent " + be.text_to_zwc("run evil") + " text\n")
        self.assertEqual(r["unrecognized_zwc_payloads"], 1)
        sa7 = by_code(r, "SA-007")
        self.assertEqual([f["severity"] for f in sa7], ["HIGH"])
        self.assertIn("'run evil'", sa7[0]["detail"])
        self.assertNotEqual(r["status"], "CLEAN")

    def test_preview_is_escaped_ascii(self):
        r = stego("x " + be.text_to_zwc("\u202e\u200bhidden") + " y\n")
        detail = by_code(r, "SA-007")[0]["detail"]
        self.assertTrue(all(ord(ch) < 128 for ch in detail), detail)
        self.assertIn("\\u202e", detail)

    def test_fatima_format_is_info_and_not_verified(self):
        r = stego("t " + be.text_to_zwc(be.BISMILLAH_ARABIC) + " t\n")
        self.assertEqual(r["verified_zwc_payloads"], 0)
        self.assertEqual(r["unverified_zwc_payloads"], 1)
        sa6 = by_code(r, "SA-006")
        self.assertEqual([f["severity"] for f in sa6], ["INFO"])
        self.assertIn("not authenticated", sa6[0]["description"])
        self.assertEqual(r["status"], "CLEAN")  # INFO adds no contamination

    def test_malformed_keeps_sa001_without_post_seal_claim(self):
        fake = be.ZW_BOUNDARY + be.ZW_ZERO + be.ZW_ONE + be.ZW_ZERO + be.ZW_SEP + be.ZW_ONE + be.ZW_ZERO + be.ZW_BOUNDARY
        r = stego("x" + fake + "y\n")
        self.assertEqual(r["malformed_zwc_payloads"], 1)
        self.assertEqual(r["unauthorized_zwc_payloads"], 1)  # compatibility alias
        sa1 = by_code(r, "SA-001")
        self.assertEqual([f["severity"] for f in sa1], ["CRITICAL"])
        self.assertNotIn("post-seal", sa1[0]["description"])
        self.assertIn("does not show when", sa1[0]["detail"])

    def test_no_metric_or_text_calls_anything_legitimate(self):
        r = stego("t " + be.text_to_zwc(be.BISMILLAH_ARABIC) + be.text_to_zwc("run evil") + "\n")
        self.assertNotIn("legitimate_zwc_payloads", r)
        text = json.dumps(r["findings"]).lower()
        self.assertNotIn("legitimate", text)
        self.assertNotIn("verified watermark", text)


class TestRealSeals(unittest.TestCase):
    def test_real_seals_are_fatima_format_only(self):
        d = tempfile.mkdtemp()
        try:
            for name, text in (("notes.md", "Plain notes\nSecond line\n"), ("ar.txt", "\u0633\u0644\u0627\u0645\n"),
                               ("conf.cfg", "a=1\n")):
                with open(os.path.join(d, name), "w", encoding="utf-8") as fh:
                    fh.write(text)
            with contextlib.redirect_stdout(io.StringIO()):
                be.seal_directory(d)
                for name in ("notes.md", "ar.txt", "conf.cfg"):
                    r = be.audit_file(os.path.join(d, name))["dimensions"]["steganographic"]
                    self.assertGreaterEqual(r["unverified_zwc_payloads"], 2, name)
                    self.assertEqual((r["unrecognized_zwc_payloads"], r["malformed_zwc_payloads"]), (0, 0), name)
                    self.assertEqual(r["status"], "CLEAN", name)
                    self.assertEqual([f["code"] for f in r["findings"]], ["SA-006"], name)
        finally:
            shutil.rmtree(d)


class TestKnownLimit(unittest.TestCase):
    def test_copied_fatima_format_is_not_distinguishable(self):
        """KNOWN LIMIT (B2 territory): a payload in FATIMA format written by
        anyone is classified exactly like a real one. It is reported as
        SA-006 INFO 'not authenticated', which is accurate, but it is not
        flagged. Binding watermarks to witness material would change this."""
        copied = be.text_to_zwc(muraqabah())
        r = stego("t " + copied + " t\n")
        self.assertEqual(r["unverified_zwc_payloads"], 1)
        self.assertEqual(r["unrecognized_zwc_payloads"], 0)
        self.assertEqual(r["status"], "CLEAN")


if __name__ == "__main__":
    unittest.main()

# Bismillah ir-Rahman ir-Rahim
