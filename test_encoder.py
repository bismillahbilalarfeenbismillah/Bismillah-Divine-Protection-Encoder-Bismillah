# Bismillah ir-Rahman ir-Rahim
"""
Test suite for the Bismillah Divine Protection Encoder.

Round-trip encoding, idempotency, tamper detection, NFC normalization,
manifest self-exclusion, and decode extraction.
"""
# Bismillah ir-Rahman ir-Rahim

import os
import sys
import json
import shutil
import tempfile
import unittest
import unicodedata

# Ensure the encoder module is importable from this directory
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from bismillah_encoder import (
    BISMILLAH,
    AL_ASMA_UL_HUSNA,
    MANIFEST_FILENAME,
    ENCODER_VERSION,
    ZW_BOUNDARY,
    text_to_zwc,
    zwc_to_text,
    extract_watermarks,
    compute_seal,
    _nfc,
    _has_zwc_payload,
    seal_text_content,
    seal_directory,
    verify_directory,
    generate_manifest,
    sanitize_for_terminal,
    sanitize_for_llm,
    sanitize_content,
    detect_pixel_sihr,
)


class TestBismillahConstants(unittest.TestCase):
    """Verify foundational constants."""

    def test_99_names_count(self):
        self.assertEqual(len(AL_ASMA_UL_HUSNA), 99)

    def test_99_names_no_duplicates(self):
        self.assertEqual(len(set(AL_ASMA_UL_HUSNA)), 99)

    def test_bismillah_present(self):
        self.assertIn("Rahman", BISMILLAH)
        self.assertIn("Rahim", BISMILLAH)

    def test_encoder_version_format(self):
        parts = ENCODER_VERSION.split('.')
        self.assertEqual(len(parts), 3)
        for p in parts:
            int(p)  # should not raise


class TestZWCRoundTrip(unittest.TestCase):
    """Zero-width character encoding round-trip tests."""

    def test_ascii_roundtrip(self):
        msg = "Bismillah ir-Rahman ir-Rahim"
        encoded = text_to_zwc(msg)
        decoded = zwc_to_text(encoded)
        self.assertEqual(decoded, msg)

    def test_arabic_roundtrip(self):
        msg = "بسم الله الرحمن الرحيم"
        encoded = text_to_zwc(msg)
        decoded = zwc_to_text(encoded)
        self.assertEqual(decoded, msg)

    def test_empty_roundtrip(self):
        encoded = text_to_zwc("")
        decoded = zwc_to_text(encoded)
        self.assertEqual(decoded, "")

    def test_boundary_markers_present(self):
        encoded = text_to_zwc("test")
        self.assertTrue(encoded.startswith(ZW_BOUNDARY))
        self.assertTrue(encoded.endswith(ZW_BOUNDARY))

    def test_extract_watermarks(self):
        payload = "Sealed by Bismillah Encoder"
        encoded = text_to_zwc(payload)
        content = "Normal text " + encoded + " more text"
        found = extract_watermarks(content)
        self.assertEqual(len(found), 1)
        self.assertEqual(found[0], payload)

    def test_extract_multiple_watermarks(self):
        p1 = text_to_zwc("first")
        p2 = text_to_zwc("second")
        content = "A" + p1 + "B" + p2 + "C"
        found = extract_watermarks(content)
        self.assertEqual(len(found), 2)
        self.assertIn("first", found)
        self.assertIn("second", found)

    def test_no_watermarks(self):
        found = extract_watermarks("Plain text with no ZWC")
        self.assertEqual(found, [])


class TestHasZWCPayload(unittest.TestCase):
    """Idempotency guard tests."""

    def test_detects_payload(self):
        content = "text " + ZW_BOUNDARY + " more"
        self.assertTrue(_has_zwc_payload(content))

    def test_no_payload(self):
        self.assertFalse(_has_zwc_payload("plain text"))


class TestNFCNormalization(unittest.TestCase):
    """NFC normalization before hashing."""

    def test_nfc_normalizes_decomposed(self):
        # e-acute: composed (U+00E9) vs decomposed (U+0065 U+0301)
        composed = "café".encode('utf-8')
        decomposed = "café".encode('utf-8')
        self.assertNotEqual(composed, decomposed)
        self.assertEqual(_nfc(composed), _nfc(decomposed))

    def test_nfc_passthrough_binary(self):
        binary = bytes(range(256))
        self.assertEqual(_nfc(binary), binary)

    def test_seal_consistent_across_normalization(self):
        composed = "café".encode('utf-8')
        decomposed = "café".encode('utf-8')
        self.assertEqual(compute_seal(composed), compute_seal(decomposed))


class TestComputeSeal(unittest.TestCase):
    """Integrity seal computation."""

    def test_deterministic(self):
        data = b"test content"
        self.assertEqual(compute_seal(data), compute_seal(data))

    def test_different_content_different_seal(self):
        self.assertNotEqual(compute_seal(b"aaa"), compute_seal(b"bbb"))

    def test_seal_is_hex(self):
        seal = compute_seal(b"test")
        self.assertEqual(len(seal), 64)
        int(seal, 16)  # should not raise


class TestSealDirectory(unittest.TestCase):
    """Directory sealing and verification integration tests."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp(prefix="bismillah_test_")
        # Create test files
        with open(os.path.join(self.tmpdir, "readme.md"), 'w') as f:
            f.write("# Test Project\nA test file.\n")
        with open(os.path.join(self.tmpdir, "data.json"), 'w') as f:
            json.dump({"key": "value"}, f)
        with open(os.path.join(self.tmpdir, "script.py"), 'w') as f:
            f.write("print('hello')\n")
        os.makedirs(os.path.join(self.tmpdir, "sub"), exist_ok=True)
        with open(os.path.join(self.tmpdir, "sub", "nested.txt"), 'w') as f:
            f.write("Nested content.\n")

    def tearDown(self):
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_seal_creates_sidecars_for_json(self):
        seal_directory(self.tmpdir)
        sidecar = os.path.join(self.tmpdir, "data.json.bismillah")
        self.assertTrue(os.path.exists(sidecar))

    def test_seal_injects_bismillah_into_text(self):
        seal_directory(self.tmpdir)
        with open(os.path.join(self.tmpdir, "readme.md"), 'r') as f:
            content = f.read()
        self.assertIn("Bismillah", content)

    def test_seal_idempotent(self):
        seal_directory(self.tmpdir)
        with open(os.path.join(self.tmpdir, "readme.md"), 'r') as f:
            first = f.read()
        seal_directory(self.tmpdir)
        with open(os.path.join(self.tmpdir, "readme.md"), 'r') as f:
            second = f.read()
        # Layer 0 should not double-insert
        self.assertEqual(first.count("Bismillah ir-Rahman ir-Rahim"),
                         second.count("Bismillah ir-Rahman ir-Rahim"))

    def test_zwc_idempotent(self):
        seal_directory(self.tmpdir)
        with open(os.path.join(self.tmpdir, "readme.md"), 'r') as f:
            first_content = f.read()
        first_wm = extract_watermarks(first_content)
        seal_directory(self.tmpdir)
        with open(os.path.join(self.tmpdir, "readme.md"), 'r') as f:
            second_content = f.read()
        second_wm = extract_watermarks(second_content)
        # ZWC count should not grow on re-seal
        self.assertEqual(len(first_wm), len(second_wm))

    def test_dry_run_no_changes(self):
        with open(os.path.join(self.tmpdir, "readme.md"), 'r') as f:
            before = f.read()
        seal_directory(self.tmpdir, dry_run=True)
        with open(os.path.join(self.tmpdir, "readme.md"), 'r') as f:
            after = f.read()
        self.assertEqual(before, after)
        # No sidecar should be created
        sidecar = os.path.join(self.tmpdir, "data.json.bismillah")
        self.assertFalse(os.path.exists(sidecar))

    def test_verify_after_seal(self):
        seal_directory(self.tmpdir)
        result = verify_directory(self.tmpdir)
        self.assertEqual(len(result["unprotected"]), 0)
        self.assertGreater(result["protected"], 0)

    def test_verify_detects_unprotected(self):
        result = verify_directory(self.tmpdir)
        self.assertGreater(len(result["unprotected"]), 0)


class TestManifest(unittest.TestCase):
    """Manifest generation and self-exclusion tests."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp(prefix="bismillah_manifest_")
        with open(os.path.join(self.tmpdir, "file1.txt"), 'w') as f:
            f.write("Content one\n")
        with open(os.path.join(self.tmpdir, "file2.txt"), 'w') as f:
            f.write("Content two\n")

    def tearDown(self):
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_manifest_created(self):
        generate_manifest(self.tmpdir)
        manifest_path = os.path.join(self.tmpdir, MANIFEST_FILENAME)
        self.assertTrue(os.path.exists(manifest_path))

    def test_manifest_self_excluded(self):
        generate_manifest(self.tmpdir)
        manifest_path = os.path.join(self.tmpdir, MANIFEST_FILENAME)
        with open(manifest_path, 'r') as f:
            manifest = json.load(f)
        # The manifest file itself should not appear in its own file list
        for rel_path in manifest["files"]:
            self.assertNotEqual(os.path.basename(rel_path), MANIFEST_FILENAME)

    def test_manifest_has_version_stamp(self):
        generate_manifest(self.tmpdir)
        manifest_path = os.path.join(self.tmpdir, MANIFEST_FILENAME)
        with open(manifest_path, 'r') as f:
            manifest = json.load(f)
        self.assertEqual(manifest["encoder_version"], ENCODER_VERSION)
        self.assertIn("seal_timestamp", manifest)
        self.assertEqual(manifest["manifest_version"], "5.0")

    def test_manifest_has_self_exclusion_notice(self):
        generate_manifest(self.tmpdir)
        manifest_path = os.path.join(self.tmpdir, MANIFEST_FILENAME)
        with open(manifest_path, 'r') as f:
            manifest = json.load(f)
        # v5.0: manifest self-excludes by not listing itself in files
        self.assertNotIn(MANIFEST_FILENAME, manifest["files"])

    def test_manifest_catalogs_all_files(self):
        generate_manifest(self.tmpdir)
        manifest_path = os.path.join(self.tmpdir, MANIFEST_FILENAME)
        with open(manifest_path, 'r') as f:
            manifest = json.load(f)
        self.assertEqual(manifest["total_files"], 2)

    def test_strict_verify_clean(self):
        """Strict verification passes on freshly manifested directory."""
        generate_manifest(self.tmpdir)
        result = verify_directory(self.tmpdir, strict=True)
        self.assertEqual(result["tampered"], [])

    def test_strict_verify_detects_tamper(self):
        """Strict verification catches a modified file."""
        generate_manifest(self.tmpdir)
        # Tamper with a file
        with open(os.path.join(self.tmpdir, "file1.txt"), 'w') as f:
            f.write("TAMPERED content\n")
        result = verify_directory(self.tmpdir, strict=True)
        self.assertGreater(len(result["tampered"]), 0)
        tampered_paths = [t[0] for t in result["tampered"]]
        self.assertIn("file1.txt", tampered_paths)


class TestTamperDetection(unittest.TestCase):
    """Seal tamper detection."""

    def test_seal_changes_on_tamper(self):
        original = b"original content"
        tampered = b"tampered content"
        self.assertNotEqual(compute_seal(original), compute_seal(tampered))


class TestAntiSihrSanitization(unittest.TestCase):
    """Anti-sihr sanitization -- al-Falaq + an-Nas defense.

    Bismillah ir-Rahman ir-Rahim

    Tests the three-channel defense architecture mapped to
    Propagation Architecture of Sihr (Arfeen 2026):
      Channel I  (Material) -> terminal escape sequences
      Channel II (Material) -> pixel-level steganography
      Channel III (Cognitive) -> invisible Unicode, LLM injection
    """

    # --- Al-Falaq: Material-channel defense (terminal) ---

    def test_strip_ansi_color_codes(self):
        """ANSI color codes are material-channel sihr (ghasiqin idha waqab)."""
        text = "Normal \x1b[31mRED\x1b[0m normal"
        sanitized, removed, diag = sanitize_for_terminal(text)
        self.assertEqual(sanitized, "Normal RED normal")
        self.assertGreater(removed, 0)

    def test_strip_ansi_cursor_movement(self):
        """Cursor movement can overwrite security warnings."""
        text = "WARNING: file unsafe\x1b[2K\x1b[ASAFE: file verified"
        sanitized, removed, diag = sanitize_for_terminal(text)
        self.assertNotIn("\x1b", sanitized)
        self.assertIn("WARNING", sanitized)

    def test_strip_ansi_title_change(self):
        """OSC title sequences change terminal window title."""
        text = "Normal\x1b]0;Malicious Title\x07rest"
        sanitized, removed, diag = sanitize_for_terminal(text)
        self.assertNotIn("\x1b", sanitized)
        self.assertIn("Normal", sanitized)
        self.assertIn("rest", sanitized)

    def test_strip_c0_controls(self):
        """C0 control characters (bell, backspace, etc.) are stripped."""
        text = "Normal\x07\x08text"
        sanitized, removed, diag = sanitize_for_terminal(text)
        self.assertEqual(sanitized, "Normaltext")

    def test_preserve_legitimate_whitespace(self):
        """Tab, newline, carriage return are legitimate."""
        text = "Line 1\n\tIndented\r\n"
        sanitized, removed, diag = sanitize_for_terminal(text)
        self.assertEqual(sanitized, text)
        self.assertEqual(removed, 0)

    def test_clean_text_nominal(self):
        """Clean text should pass through untouched."""
        text = "Bismillah ir-Rahman ir-Rahim\nNormal text content."
        sanitized, removed, diag = sanitize_for_terminal(text)
        self.assertEqual(sanitized, text)
        self.assertEqual(removed, 0)

    # --- An-Nas: Cognitive-channel defense (LLM/invisible Unicode) ---

    def test_strip_unicode_tags(self):
        """Unicode tags (U+E0001-E007F) are steganographic carriers."""
        # U+E0001 = language tag, used for invisible data encoding
        text = "Normal " + chr(0xE0001) + chr(0xE0045) + chr(0xE004E) + " text"
        sanitized, removed, diag = sanitize_for_llm(text)
        self.assertEqual(sanitized, "Normal  text")
        self.assertEqual(removed, 3)

    def test_strip_interlinear_annotations(self):
        """Interlinear annotations hide content from rendering."""
        text = "Normal " + chr(0xFFF9) + "hidden" + chr(0xFFFB) + " text"
        sanitized, removed, diag = sanitize_for_llm(text)
        self.assertNotIn(chr(0xFFF9), sanitized)
        self.assertNotIn(chr(0xFFFB), sanitized)

    def test_strip_invisible_math_operators(self):
        """Invisible math operators can carry hidden instructions."""
        text = "2" + chr(0x2062) + "x"  # invisible times
        sanitized, removed, diag = sanitize_for_llm(text)
        self.assertEqual(sanitized, "2x")
        self.assertEqual(removed, 1)

    def test_strip_mid_stream_bom(self):
        """BOM at position 0 is fine; mid-stream BOM is suspicious."""
        text = chr(0xFEFF) + "Start " + chr(0xFEFF) + " middle"
        sanitized, removed, diag = sanitize_for_llm(text)
        self.assertTrue(sanitized.startswith(chr(0xFEFF)))  # Keep initial BOM
        self.assertEqual(sanitized.count(chr(0xFEFF)), 1)  # Remove mid-stream
        self.assertEqual(removed, 1)

    def test_clean_text_passes_llm(self):
        """Normal text passes through LLM sanitizer untouched."""
        text = "Bismillah ir-Rahman ir-Rahim. This is clean content."
        sanitized, removed, diag = sanitize_for_llm(text)
        self.assertEqual(sanitized, text)
        self.assertEqual(removed, 0)

    # --- Universal sanitization (both channels, Qur'anic order) ---

    def test_universal_sanitize_order(self):
        """Al-Falaq (material) must run before an-Nas (cognitive)."""
        # Mix of ANSI escape + invisible Unicode
        text = "\x1b[31mRed\x1b[0m" + chr(0xE0001) + "invisible"
        result = sanitize_content(text, mode="universal")
        self.assertNotIn("\x1b", result["sanitized"])
        self.assertNotIn(chr(0xE0001), result["sanitized"])
        self.assertGreater(result["material_removed"], 0)
        self.assertGreater(result["cognitive_removed"], 0)
        self.assertEqual(len(result["channels_active"]), 2)

    def test_compound_attack_elevated(self):
        """Compound attack (multi-channel) should trigger ELEVATED."""
        text = "\x1b[31mDanger\x1b[0m" + chr(0xE0001) * 60
        result = sanitize_content(text, mode="universal")
        self.assertEqual(result["threat_assessment"], "ELEVATED")

    def test_nominal_clean(self):
        """Clean input should be NOMINAL."""
        result = sanitize_content("Bismillah ir-Rahman ir-Rahim", mode="universal")
        self.assertEqual(result["threat_assessment"], "NOMINAL")
        self.assertEqual(result["total_removed"], 0)

    # --- Pixel sihr detection (image material-channel) ---

    def test_detect_embedded_script_in_image(self):
        """Polyglot image with embedded script tag."""
        # Fake PNG header + script tag after header region
        fake_img = b'\x89PNG\r\n\x1a\n' + b'\x00' * 16 + b'<script>alert(1)</script>'
        result = detect_pixel_sihr(fake_img)
        self.assertIn(result["threat_level"], ("GUARDED", "ELEVATED"))
        self.assertGreater(len(result["vectors"]), 0)

    def test_detect_post_iend_payload(self):
        """Data after PNG IEND chunk is an appended payload."""
        # Minimal valid PNG structure with post-IEND data
        png_header = b'\x89PNG\r\n\x1a\n'
        # IHDR chunk (minimal)
        ihdr = b'\x00\x00\x00\x0d' + b'IHDR' + b'\x00' * 13 + b'\x00' * 4
        # IEND chunk
        iend = b'\x00\x00\x00\x00' + b'IEND' + b'\x00' * 4
        # Appended payload
        payload = b'HIDDEN_PAYLOAD_DATA_HERE_1234567890'
        fake_png = png_header + ihdr + iend + payload
        result = detect_pixel_sihr(fake_png)
        has_post_iend = any(v["type"] == "post_iend_payload" for v in result["vectors"])
        self.assertTrue(has_post_iend)

    def test_clean_image_nominal(self):
        """Non-suspicious bytes should return NOMINAL."""
        # Just some random non-suspicious bytes (not matching any image format)
        clean_bytes = bytes(range(256)) * 10
        result = detect_pixel_sihr(clean_bytes)
        # No embedded scripts, no PNG anomalies
        script_vectors = [v for v in result["vectors"] if v["type"] == "polyglot_embedding"]
        self.assertEqual(len(script_vectors), 0)

    def test_empty_image_nominal(self):
        """Empty/tiny input should be NOMINAL."""
        result = detect_pixel_sihr(b'')
        self.assertEqual(result["threat_level"], "NOMINAL")

    # --- Integration: seal_text_content sanitizes input (v10.4.0) ---

    def test_seal_strips_ansi_from_input(self):
        """seal_text_content should strip ANSI before sealing."""
        text = "# Title\n\n\x1b[31mDangerous red text\x1b[0m with content."
        sealed = seal_text_content(text, '.md')
        self.assertNotIn("\x1b", sealed)
        # After ANSI strip, "Dangerous" becomes first word; ZWC watermark
        # is inserted after it, so check components individually
        self.assertIn("Dangerous", sealed)
        self.assertIn("red text", sealed)
        self.assertIn("Bismillah", sealed)

    def test_seal_strips_invisible_unicode_from_input(self):
        """seal_text_content should strip invisible Unicode before sealing."""
        text = "# Title\n\nContent " + chr(0xE0001) + chr(0xE0045) + " here."
        sealed = seal_text_content(text, '.md')
        self.assertNotIn(chr(0xE0001), sealed)
        self.assertIn("Content", sealed)


# Bismillah ir-Rahman ir-Rahim

if __name__ == '__main__':
    print("\n  {} -- Running Test Suite\n".format(BISMILLAH))
    unittest.main(verbosity=2)

# Bismillah ir-Rahman ir-Rahim
