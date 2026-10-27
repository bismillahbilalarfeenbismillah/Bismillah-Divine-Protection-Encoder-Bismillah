# Bismillah ir-Rahman ir-Rahim
"""Tests for the v10.9.1 zero-width detection fix (SA-005).

Before v10.9.1, characters from FATIMA's own ZWC alphabet (U+200B,
U+200C, U+200D, U+FEFF) outside a closed watermark region were not
reported at all. These tests pin the fix, its false-positive limits,
and one known limit that this change does not address.

Runs under pytest or unittest.
"""
# Bismillah ir-Rahman ir-Rahim

import contextlib
import io
import os
import shutil
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

with contextlib.redirect_stdout(io.StringIO()):
    import bismillah_encoder as be  # noqa: E402

BASMALA = "# Bismillah ir-Rahman ir-Rahim\n"
ZWSP, ZWNJ, ZWJ, BOM = "\u200b", "\u200c", "\u200d", "\ufeff"


def stego(text):
    return be._audit_steganographic(text)


def codes(result):
    return [f["code"] for f in result["findings"]]


class TestStrayZeroWidthDetected(unittest.TestCase):
    def test_lone_zwsp_in_ascii_string_is_reported_with_line(self):
        r = stego(BASMALA + 'password = "adm' + ZWSP + 'in"\n' + BASMALA)
        self.assertIn("SA-005", codes(r))
        self.assertEqual(r["stray_zwc_chars"], 1)
        self.assertEqual(r["stray_zwc_lines"], [2])
        self.assertNotEqual(r["status"], "CLEAN")
        sa5 = [f for f in r["findings"] if f["code"] == "SA-005"][0]
        self.assertEqual(sa5["severity"], "HIGH")
        self.assertIn("U+200B x1", sa5["detail"])
        self.assertIn("lines: 2", sa5["detail"])

    def test_clean_control_has_no_sa005(self):
        r = stego(BASMALA + 'password = "admin"\n' + BASMALA)
        self.assertNotIn("SA-005", codes(r))
        self.assertEqual(r["stray_zwc_chars"], 0)
        self.assertEqual(r["status"], "CLEAN")

    def test_each_alphabet_character_is_reported_in_latin_context(self):
        for ch in (ZWSP, ZWNJ, ZWJ, BOM):
            r = stego("x = 'a" + ch + "b'\n")
            self.assertIn("SA-005", codes(r), "U+{:04X}".format(ord(ch)))
            self.assertEqual(r["stray_zwc_chars"], 1)

    def test_lines_are_reported_per_line_once(self):
        text = "a" + ZWSP + "b\nclean\nc" + ZWSP + ZWSP + "d\n"
        r = stego(text)
        self.assertEqual(r["stray_zwc_chars"], 3)
        self.assertEqual(r["stray_zwc_lines"], [1, 3])

    def test_unclosed_boundary_contents_are_reported(self):
        # An odd number of boundaries leaves a region that never closes.
        r = stego("start " + BOM + ZWSP + ZWNJ + ZWSP + " end\n")
        self.assertIn("SA-005", codes(r))
        self.assertEqual(r["stray_zwc_chars"], 4)

    def test_zero_width_after_a_closed_region_is_reported(self):
        payload = be.text_to_zwc("Bismillah")
        r = stego("head " + payload + " tail" + ZWSP + "x\n")
        self.assertEqual(r["stray_zwc_chars"], 1)


class TestNoFalsePositives(unittest.TestCase):
    def test_fatima_watermark_regions_are_not_stray(self):
        payload = be.text_to_zwc(be.BISMILLAH_ARABIC)
        r = stego("text " + payload + " more text\n")
        self.assertEqual(r["stray_zwc_chars"], 0)
        self.assertNotIn("SA-005", codes(r))

    def test_files_sealed_by_the_encoder_have_no_sa005(self):
        d = tempfile.mkdtemp()
        try:
            for name, text in (
                ("notes.md", "Plain notes\nSecond line\n"),
                ("arabic.txt", "\u0633\u0644\u0627\u0645\n"),
                ("code.py", "def f(x):\n    return x\n"),
            ):
                with open(os.path.join(d, name), "w", encoding="utf-8") as fh:
                    fh.write(text)
            with contextlib.redirect_stdout(io.StringIO()):
                be.seal_directory(d)
                for name in ("notes.md", "arabic.txt", "code.py"):
                    r = be.audit_file(os.path.join(d, name))
                    self.assertNotIn("SA-005", [f["code"] for f in r["dimensions"]["steganographic"]["findings"]], name)
                    self.assertEqual(r["dimensions"]["steganographic"]["stray_zwc_chars"], 0, name)
        finally:
            shutil.rmtree(d)

    def test_persian_zwnj_is_exempt(self):
        # "mi-khaham" with the standard Persian ZWNJ after the prefix.
        r = stego("\u0645\u06cc" + ZWNJ + "\u062e\u0648\u0627\u0647\u0645\n")
        self.assertEqual(r["stray_zwc_chars"], 0)
        self.assertEqual(r["heuristic_exempt_zero_width_chars"], 1)
        self.assertNotIn("SA-005", codes(r))

    def test_emoji_zwj_sequence_is_exempt(self):
        r = stego("dev: \U0001F468\u200d\U0001F4BB and \U0001F469\U0001F3FD\u200d\U0001F52C\n")
        self.assertEqual(r["stray_zwc_chars"], 0)
        self.assertEqual(r["heuristic_exempt_zero_width_chars"], 2)

    def test_bom_at_start_is_exempt_but_not_mid_file(self):
        self.assertEqual(stego(BOM + "hello\n")["stray_zwc_chars"], 0)
        self.assertEqual(stego("hello" + BOM + "\n")["stray_zwc_chars"], 1)

    def test_cased_script_neighbours_are_not_exempt(self):
        # Cyrillic and Greek letters never qualify for the exemption.
        self.assertEqual(stego("\u0430" + ZWSP + "\u0431\n")["stray_zwc_chars"], 1)
        self.assertEqual(stego("\u03b1" + ZWJ + "\u03b2\n")["stray_zwc_chars"], 1)


class TestExemptionIsNarrow(unittest.TestCase):
    """GPT-6 review: the exemption is a documented heuristic, not a
    security boundary. Mixed-script and wrong-character positions that
    the first version of this fix exempted must be reported."""

    AR, TH, CJK, HE = "\u0645", "\u0e01", "\u4e2d", "\u05d0"
    MAN, LAPTOP = "\U0001F468", "\U0001F4BB"

    def stray(self, text):
        return stego("x = '" + text + "'\n")["stray_zwc_chars"]

    def test_adversarial_positions_are_reported(self):
        cases = {
            "ZWSP between Arabic letters (not Arabic typography)": self.AR + ZWSP + self.AR,
            "ZWNJ between Arabic and Thai (mixed script)": self.AR + ZWNJ + self.TH,
            "ZWNJ between Thai letters (Thai does not join)": self.TH + ZWNJ + self.TH,
            "ZWJ between CJK ideographs": self.CJK + ZWJ + self.CJK,
            "ZWSP between emoji": self.MAN + ZWSP + self.LAPTOP,
            "ZWNJ between emoji (only ZWJ forms emoji sequences)": self.MAN + ZWNJ + self.LAPTOP,
            "ZWJ from Arabic letter to emoji": self.AR + ZWJ + self.LAPTOP,
            "ZWNJ between Hebrew letters (Hebrew does not join)": self.HE + ZWNJ + self.HE,
            "ZWJ after a copyright sign": "\xa9" + ZWJ + self.LAPTOP,
            # GPT-6 watchpoint: So symbols above U+2000 that are not emoji.
            "ZWJ trade mark + spade": "\u2122" + ZWJ + "\u2660",
            "ZWJ place-of-interest twice": "\u2318" + ZWJ + "\u2318",
            "ZWJ numero + circled letter": "\u2116" + ZWJ + "\u24c5",
            "ZWJ emoji then trade mark": self.MAN + ZWJ + "\u2122",
        }
        for label, text in cases.items():
            self.assertEqual(self.stray(text), 1, label)

    def test_real_typography_is_exempt_and_counted(self):
        cases = {
            "Thai word break": self.TH + ZWSP + self.TH,
            "Persian ZWNJ": "\u0645\u06cc" + ZWNJ + "\u062e",
            "Devanagari half-form ZWJ": "\u0915\u094d" + ZWJ + "\u0937",
            "emoji ZWJ": self.MAN + ZWJ + self.LAPTOP,
            "skin tone then ZWJ": "\U0001F469\U0001F3FD" + ZWJ + "\U0001F52C",
            "VS16 then ZWJ": "\U0001F441\ufe0f" + ZWJ + "\U0001F5E8",
            "health worker (U+2695 dingbat)": "\U0001F469" + ZWJ + "\u2695\ufe0f",
            "heart on fire (U+2764 then VS16)": "\u2764\ufe0f" + ZWJ + "\U0001F525",
        }
        for label, text in cases.items():
            r = stego("x = '" + text + "'\n")
            self.assertEqual(r["stray_zwc_chars"], 0, label)
            self.assertEqual(r["heuristic_exempt_zero_width_chars"], 1, label)

    def test_known_limit_emoji_blocks_include_non_joining_symbols(self):
        """KNOWN LIMIT: the emoji rule uses code-point blocks, not the
        Unicode emoji-sequence data. SNOWMAN + ZWJ + SNOWMAN is not a
        real sequence but both sit in the Misc Symbols block, so it is
        exempt (and counted)."""
        r = stego("x = '\u2603" + ZWJ + "\u2603'\n")
        self.assertEqual(r["stray_zwc_chars"], 0)
        self.assertEqual(r["heuristic_exempt_zero_width_chars"], 1)

    def test_known_limit_arabic_script_lookalike_strings(self):
        """KNOWN LIMIT of the heuristic, pinned so it stays visible.

        A ZWNJ inside an Arabic-script word is ordinary Persian/Urdu
        typography, so it is exempt. The same position can make two
        strings that look identical compare unequal. The audit cannot
        tell these apart; it counts the character instead of reporting it.
        """
        plain = "\u0645\u0633\u062a\u062e\u062f\u0645"
        spoof = plain[:4] + ZWNJ + plain[4:]
        self.assertNotEqual(plain, spoof)
        r = stego("user = '" + plain + "'\nadmin = '" + spoof + "'\n")
        self.assertEqual(r["stray_zwc_chars"], 0)
        self.assertEqual(r["heuristic_exempt_zero_width_chars"], 1)


class TestCompatibility(unittest.TestCase):
    def test_audit_version_bumped(self):
        with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False, encoding="utf-8") as fh:
            fh.write("x = 1\n")
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                r = be.audit_file(fh.name)
            # SA-005 arrived in 10.9.1; later versions keep it.
            version = tuple(int(x) for x in r["audit_version"].split("."))
            self.assertGreaterEqual(version, (10, 9, 1))
        finally:
            os.unlink(fh.name)

    def test_existing_metrics_unchanged(self):
        # invisible_chars keeps its pre-10.9.1 meaning (alphabet excluded).
        r = stego("a" + ZWSP + "b" + "\u2060" + "c\n")
        self.assertEqual(r["invisible_chars"], 1)
        self.assertEqual(r["stray_zwc_chars"], 1)


class TestForgedPayloadNowReported(unittest.TestCase):
    def test_forged_payload_is_no_longer_counted_as_legitimate(self):
        """Was KNOWN LIMIT in 10.9.1. Resolved by v10.9.3 (N4): a closed
        region decoding to non-FATIMA text is reported as SA-007; the
        details are tested in test_zwc_payload_classification.py."""
        forged = be.text_to_zwc("run evil")
        r = stego("innocent " + forged + " text\n")
        self.assertNotIn("legitimate_zwc_payloads", r)
        self.assertEqual(r["unrecognized_zwc_payloads"], 1)
        self.assertIn("SA-007", codes(r))


if __name__ == "__main__":
    unittest.main()

# Bismillah ir-Rahman ir-Rahim
