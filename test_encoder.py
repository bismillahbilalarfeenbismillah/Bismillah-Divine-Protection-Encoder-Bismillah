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
    seal_text_file,
    seal_binary_file,
    verify_directory,
    verify_zahir,
    _sorted_walk,
    generate_manifest,
    SealFinding,
    make_finding,
    SEVERITY_ERROR,
    SEVERITY_WARNING,
    SEVERITY_INFO,
    LAYER_L0,
    LAYER_L1,
    LAYER_L6,
    LAYER_L6B,
    LAYER_MANIFEST,
    LAYER_SYSTEM,
)
from unittest.mock import patch


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
        self.assertEqual(manifest["manifest_version"], "2.0")

    def test_manifest_has_self_exclusion_notice(self):
        generate_manifest(self.tmpdir)
        manifest_path = os.path.join(self.tmpdir, MANIFEST_FILENAME)
        with open(manifest_path, 'r') as f:
            manifest = json.load(f)
        self.assertIn("self_exclusion", manifest)

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


class TestSealFindings(unittest.TestCase):
    """Graft C04 -- structured SealFinding error capture (Evolved Language).

    Errors surface as structured findings in seal results, verify
    output, and manifests, preserving the original message text.
    """

    def test_finding_creation(self):
        finding = make_finding("a.txt", LAYER_L0, "SEAL-TEXT-SKIPPED-BINARY-CONTENT",
                               SEVERITY_WARNING, "not UTF-8 decodable")
        self.assertEqual(finding.filepath, "a.txt")
        self.assertEqual(finding.layer, LAYER_L0)
        self.assertEqual(finding.severity, SEVERITY_WARNING)
        self.assertEqual(finding.code, "SEAL-TEXT-SKIPPED-BINARY-CONTENT")
        self.assertEqual(finding.message, "not UTF-8 decodable")
        self.assertIsInstance(finding.filepath, str)

    def test_finding_preserves_cause_through_fallback(self):
        """Handler failure + successful sidecar fallback: WARNING finding
        carrying the primary cause, not the fallback's own message."""
        tmpdir = tempfile.mkdtemp(prefix="bismillah_finding_")
        try:
            target = os.path.join(tmpdir, "image.png")
            with open(target, "wb") as f:
                f.write(b"\x89PNG\r\n\x1a\n")

            def failing_handler(fp):
                return False, "invalid PDF"

            findings = []
            with patch.dict("bismillah_encoder.BINARY_HANDLERS",
                            {".png": failing_handler}):
                with patch("bismillah_encoder.create_sidecar",
                           return_value=(True, "Sidecar created")):
                    success, msg = seal_binary_file(target, findings)
            self.assertTrue(success)
            self.assertEqual(len(findings), 1)
            self.assertEqual(findings[0].severity, SEVERITY_WARNING)
            self.assertEqual(findings[0].code, "SEAL-BINARY-FALLBACK")
            self.assertEqual(findings[0].layer, LAYER_L6)
            self.assertIn("invalid PDF", findings[0].message)
        finally:
            shutil.rmtree(tmpdir, ignore_errors=True)

    def test_finding_carries_both_causes_on_total_failure(self):
        """Handler failure + failed sidecar fallback: WARNING with the
        primary cause plus ERROR with the sidecar failure."""
        tmpdir = tempfile.mkdtemp(prefix="bismillah_finding_")
        try:
            target = os.path.join(tmpdir, "image.png")
            with open(target, "wb") as f:
                f.write(b"\x89PNG\r\n\x1a\n")

            def failing_handler(fp):
                return False, "invalid PDF"

            findings = []
            with patch.dict("bismillah_encoder.BINARY_HANDLERS",
                            {".png": failing_handler}):
                with patch("bismillah_encoder.create_sidecar",
                           return_value=(False, "sidecar write failed")):
                    success, msg = seal_binary_file(target, findings)
            self.assertFalse(success)
            self.assertEqual(len(findings), 2)
            fallback = [f for f in findings if f.code == "SEAL-BINARY-FALLBACK"][0]
            error = [f for f in findings if f.code == "SEAL-BINARY-ERROR"][0]
            self.assertIn("invalid PDF", fallback.message)
            self.assertEqual(error.severity, SEVERITY_ERROR)
            self.assertEqual(error.layer, LAYER_L6B)
            self.assertIn("sidecar write failed", error.message)
        finally:
            shutil.rmtree(tmpdir, ignore_errors=True)

    def test_seal_binary_file_contract_unchanged(self):
        """Returns the v2.0.0 2-tuple contract; findings are a side effect."""
        tmpdir = tempfile.mkdtemp(prefix="bismillah_finding_")
        try:
            target = os.path.join(tmpdir, "image.png")
            with open(target, "wb") as f:
                f.write(b"\x89PNG\r\n\x1a\n")
            result = seal_binary_file(target)
            self.assertEqual(len(result), 2)
        finally:
            shutil.rmtree(tmpdir, ignore_errors=True)

    def test_text_seal_failure_propagates_through_seal_directory(self):
        """A non-UTF-8 text file produces a WARNING finding that reaches
        seal_directory's collected findings."""
        tmpdir = tempfile.mkdtemp(prefix="bismillah_finding_")
        try:
            with open(os.path.join(tmpdir, "binary.txt"), "wb") as f:
                f.write(b"\xff\xfe\x00bad")
            result = seal_directory(tmpdir)
            codes = [f.code for f in result["findings"]]
            self.assertIn("SEAL-TEXT-SKIPPED-BINARY-CONTENT", codes)
            finding = [f for f in result["findings"]
                      if f.code == "SEAL-TEXT-SKIPPED-BINARY-CONTENT"][0]
            self.assertEqual(finding.severity, SEVERITY_WARNING)
            self.assertEqual(finding.layer, LAYER_L0)
        finally:
            shutil.rmtree(tmpdir, ignore_errors=True)

    def test_unreadable_text_file_records_finding_not_abort(self):
        """Kimi k2.8: an OSError during text sealing is recorded as a
        finding rather than aborting the walk."""
        tmpdir = tempfile.mkdtemp(prefix="bismillah_finding_")
        try:
            target = os.path.join(tmpdir, "locked.txt")
            with open(target, "w") as f:
                f.write("content\n")
            with patch("builtins.open",
                       side_effect=PermissionError("denied")):
                result = seal_text_file(target)
            self.assertEqual(result.get("skipped"), "unreadable")
            codes = [f.code for f in result["findings"]]
            self.assertIn("SEAL-TEXT-UNREADABLE", codes)
        finally:
            shutil.rmtree(tmpdir, ignore_errors=True)

    def test_finding_in_verify_output(self):
        tmpdir = tempfile.mkdtemp(prefix="bismillah_finding_")
        try:
            link = os.path.join(tmpdir, "broken.txt")
            os.symlink("no_such_target", link)
            result = verify_directory(tmpdir)
            codes = [f.code for f in result["findings"]]
            self.assertIn("VERIFY-UNREADABLE", codes)
            unreadable = [f for f in result["findings"]
                          if f.code == "VERIFY-UNREADABLE"]
            self.assertTrue(all(f.severity == SEVERITY_ERROR for f in unreadable))
            self.assertTrue(all(f.layer == LAYER_SYSTEM for f in unreadable))
        finally:
            shutil.rmtree(tmpdir, ignore_errors=True)

    def test_finding_severity_levels(self):
        self.assertEqual((SEVERITY_INFO, SEVERITY_WARNING, SEVERITY_ERROR),
                         ("INFO", "WARNING", "ERROR"))
        with self.assertRaises(ValueError):
            make_finding("a.txt", LAYER_L0, "X", "CRITICAL",
                         "severity outside the declared set")
        for severity in (SEVERITY_INFO, SEVERITY_WARNING, SEVERITY_ERROR):
            finding = make_finding("a.txt", LAYER_L0, "X", severity, "m")
            self.assertIsInstance(finding, SealFinding)

    def test_finding_in_manifest(self):
        tmpdir = tempfile.mkdtemp(prefix="bismillah_finding_")
        try:
            link = os.path.join(tmpdir, "broken.txt")
            os.symlink("no_such_target", link)
            manifest = generate_manifest(tmpdir)
            entry = manifest["files"]["broken.txt"]
            self.assertEqual(entry["finding"]["code"], "MANIFEST-READ-FAILED")
            self.assertEqual(entry["finding"]["severity"], "ERROR")
            self.assertEqual(entry["finding"]["layer"], LAYER_MANIFEST)
        finally:
            shutil.rmtree(tmpdir, ignore_errors=True)


class TestSortedWalk(unittest.TestCase):
    """Upgrade 4 -- deterministic traversal (Kimi k2.8 determinism fix)."""

    def test_sorted_walk_deterministic_order(self):
        tmpdir = tempfile.mkdtemp(prefix="bismillah_walk_")
        try:
            for sub in ("zeta", "alpha", "mid"):
                os.makedirs(os.path.join(tmpdir, sub))
                for name in ("b.txt", "a.txt"):
                    with open(os.path.join(tmpdir, sub, name), "w") as f:
                        f.write("x\n")
            roots = [root for root, _, _ in _sorted_walk(tmpdir)]
            self.assertEqual(roots[0], tmpdir)
            subdirs = [os.path.relpath(r, tmpdir)
                       for r in roots[1:]]
            self.assertEqual(subdirs, sorted(subdirs))
            for root, dirnames, filenames in _sorted_walk(tmpdir):
                self.assertEqual(filenames, sorted(filenames))
                self.assertEqual(dirnames, sorted(dirnames))
        finally:
            shutil.rmtree(tmpdir, ignore_errors=True)

    def test_sorted_walk_exclusions(self):
        tmpdir = tempfile.mkdtemp(prefix="bismillah_walk_")
        try:
            os.makedirs(os.path.join(tmpdir, ".git", "objects"))
            os.makedirs(os.path.join(tmpdir, "keep"))
            roots = [os.path.relpath(root, tmpdir)
                     for root, _, _ in _sorted_walk(tmpdir, exclusions={".git"})]
            self.assertNotIn(".git", roots)
            self.assertIn("keep", roots)
            for root, dirnames, _ in _sorted_walk(tmpdir, exclusions={".git"}):
                self.assertNotIn(".git", dirnames)
        finally:
            shutil.rmtree(tmpdir, ignore_errors=True)


class TestVerifyZahir(unittest.TestCase):
    """Upgrade 3 -- zahir surface verification (L0, L1, L3b, L6b)."""

    def test_sealed_text_file_passes(self):
        tmpdir = tempfile.mkdtemp(prefix="bismillah_zahir_")
        try:
            path = os.path.join(tmpdir, "note.txt")
            with open(path, "w") as f:
                f.write("Bismillah ir-Rahman ir-Rahim\n" + "body line\n" * 5 +
                        "Bismillah ir-Rahman ir-Rahim\n")
            result = verify_zahir(path)
            self.assertTrue(result["passed"])
            self.assertIn(LAYER_L0, result["layers"])
            self.assertEqual(result["findings"], [])
        finally:
            shutil.rmtree(tmpdir, ignore_errors=True)

    def test_one_sided_bismillah_flags_warning(self):
        """Short-file regression: a two-line file with Bismillah only at
        the start must fail -- the head match is never reused as the
        tail match, even when head and tail windows would overlap."""
        tmpdir = tempfile.mkdtemp(prefix="bismillah_zahir_")
        try:
            path = os.path.join(tmpdir, "note.txt")
            with open(path, "w") as f:
                f.write("Bismillah ir-Rahman ir-Rahim\nbody\n")
            result = verify_zahir(path)
            self.assertFalse(result["passed"])
            self.assertTrue(result["has_start"])
            self.assertFalse(result["has_end"])
            codes = [f.code for f in result["findings"]]
            self.assertIn("SEAL-L0-ONE-SIDED", codes)
            warning = [f for f in result["findings"]
                      if f.code == "SEAL-L0-ONE-SIDED"][0]
            self.assertEqual(warning.severity, SEVERITY_WARNING)
            self.assertEqual(warning.layer, LAYER_L0)
        finally:
            shutil.rmtree(tmpdir, ignore_errors=True)

    def test_missing_bismillah_flags_error(self):
        tmpdir = tempfile.mkdtemp(prefix="bismillah_zahir_")
        try:
            path = os.path.join(tmpdir, "note.txt")
            with open(path, "w") as f:
                f.write("plain body\n")
            result = verify_zahir(path)
            self.assertFalse(result["passed"])
            codes = [f.code for f in result["findings"]]
            self.assertIn("SEAL-L0-MISSING", codes)
            error = [f for f in result["findings"]
                     if f.code == "SEAL-L0-MISSING"][0]
            self.assertEqual(error.severity, SEVERITY_ERROR)
        finally:
            shutil.rmtree(tmpdir, ignore_errors=True)

    def test_sidecar_only_file_uses_layer_6b(self):
        tmpdir = tempfile.mkdtemp(prefix="bismillah_zahir_")
        try:
            path = os.path.join(tmpdir, "data.json")
            with open(path, "w") as f:
                f.write("{}\n")
            with open(path + ".bismillah", "w") as f:
                f.write("Bismillah ir-Rahman ir-Rahim\n")
            result = verify_zahir(path)
            self.assertTrue(result["passed"])
            self.assertIn(LAYER_L6B, result["layers"])
        finally:
            shutil.rmtree(tmpdir, ignore_errors=True)

    def test_empty_sidecar_does_not_pass(self):
        """Sidecar existence alone is not verification: an empty sidecar
        produces a warning finding and does not pass."""
        tmpdir = tempfile.mkdtemp(prefix="bismillah_zahir_")
        try:
            path = os.path.join(tmpdir, "data.json")
            with open(path, "w") as f:
                f.write("{}\n")
            with open(path + ".bismillah", "w") as f:
                f.write("")
            result = verify_zahir(path)
            self.assertFalse(result["passed"])
            codes = [f.code for f in result["findings"]]
            self.assertIn("SEAL-ZAHIR-SIDECAR-EMPTY", codes)
        finally:
            shutil.rmtree(tmpdir, ignore_errors=True)

    def test_orphan_sidecar_flags_warning(self):
        """A sidecar beside a missing primary file is flagged, not
        treated as protection of the (nonexistent) primary."""
        tmpdir = tempfile.mkdtemp(prefix="bismillah_zahir_")
        try:
            path = os.path.join(tmpdir, "gone.json")
            with open(path + ".bismillah", "w") as f:
                f.write("Bismillah ir-Rahman ir-Rahim\n")
            result = verify_zahir(path)
            self.assertFalse(result["passed"])
            codes = [f.code for f in result["findings"]]
            self.assertIn("SEAL-ZAHIR-ORPHAN-SIDECAR", codes)
        finally:
            shutil.rmtree(tmpdir, ignore_errors=True)

    def test_filename_convention_detected(self):
        tmpdir = tempfile.mkdtemp(prefix="bismillah_zahir_")
        try:
            path = os.path.join(tmpdir, "Bismillah_note_Bismillah.txt")
            with open(path, "w") as f:
                f.write("Bismillah ir-Rahman ir-Rahim\n" + "body line\n" * 5 +
                        "Bismillah ir-Rahman ir-Rahim\n")
            result = verify_zahir(path)
            self.assertTrue(result["filename_sealed"])
            self.assertIn(LAYER_L1, result["layers"])
        finally:
            shutil.rmtree(tmpdir, ignore_errors=True)


# Bismillah ir-Rahman ir-Rahim

if __name__ == '__main__':
    print("\n  {} -- Running Test Suite\n".format(BISMILLAH))
    unittest.main(verbosity=2)

# Bismillah ir-Rahman ir-Rahim
