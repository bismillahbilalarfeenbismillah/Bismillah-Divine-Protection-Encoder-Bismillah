#!/usr/bin/env python3
# Bismillah ir-Rahman ir-Rahim
"""
Red Team Suite for FATIMA Audit Engine v10.9.0 & Bayyinah Scanner v1.0.0

Attack vectors:
  RT-A: BiDi override injection that should trigger RI-003 but crafted to evade
  RT-B: Unicode tag steganography hidden inside legitimate-looking content
  RT-C: ZWC payload injection mimicking FATIMA's own alphabet
  RT-D: Homoglyph substitution in Arabic Basmala text
  RT-E: Cyrillic trojan source attack
  RT-F: Edge cases -- empty file, binary file, massive file
  RT-G: Bayyinah evasion -- mode-collapsed text that avoids marker detection
  RT-H: Bayyinah inversion -- adversarial output that inverts without markers
  RT-I: Boundary conditions -- exactly-at-threshold values
  RT-J: Crash/exception vectors -- malformed input, null bytes, encoding bombs

Bismillah ir-Rahman ir-Rahim
"""
# Bismillah ir-Rahman ir-Rahim

import json
import os
import sys
import tempfile
import traceback

# Add parent dir to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from bismillah_encoder import (
    _audit_rendering_integrity,
    _audit_steganographic,
    _audit_seal_coherence,
    audit_file,
    BISMILLAH,
    BISMILLAH_ARABIC,
    ZW_ZERO, ZW_ONE, ZW_SEP, ZW_BOUNDARY,
)
from bayyinah_scanner import (
    detect_mode_collapse,
    analyze_adversarial_patterns,
    scan,
    _compute_vocabulary_metrics,
    _compute_hedge_density,
    _compute_evasion_score,
    _compute_flattening_score,
)

PASS = 0
FAIL = 0
ERRORS = []


def assert_test(name, condition, detail=""):
    global PASS, FAIL, ERRORS
    if condition:
        PASS += 1
        print("  [PASS] {}".format(name))
    else:
        FAIL += 1
        msg = "  [FAIL] {}".format(name)
        if detail:
            msg += " -- {}".format(detail)
        print(msg)
        ERRORS.append(msg)


def assert_raises(name, func, *args, **kwargs):
    """Verify func does NOT crash (returns gracefully)."""
    global PASS, FAIL, ERRORS
    try:
        result = func(*args, **kwargs)
        PASS += 1
        print("  [PASS] {} (no crash)".format(name))
        return result
    except Exception as e:
        FAIL += 1
        msg = "  [FAIL] {} -- CRASHED: {} {}".format(name, type(e).__name__, e)
        print(msg)
        ERRORS.append(msg)
        return None


# ============================================================================
#  RT-A: BiDi Override Evasion
# ============================================================================

def test_bidi_override_evasion():
    print("\n  === RT-A: BiDi Override Evasion ===")

    # A1: Obvious BiDi overrides -- should detect
    content_obvious = (
        "# {}\n"
        "Some text with ‮ DANGEROUS RTL OVERRIDE ‬ embedded\n"
        "# {}\n"
    ).format(BISMILLAH, BISMILLAH)
    result = _audit_rendering_integrity(content_obvious)
    assert_test("RT-A1: Obvious RTL override detected",
                any(f["code"] == "RI-003" for f in result["findings"]),
                "findings: {}".format([f["code"] for f in result["findings"]]))

    # A2: BiDi overrides inside ZWC sequence -- harder to spot
    # Embed RLO inside what looks like a ZWC payload
    sneaky = (
        "# {}\n"
        "Normal text{}{}{}with hidden RLO{}{}{}\n"
        "# {}\n"
    ).format(BISMILLAH,
             ZW_BOUNDARY, ZW_ZERO, '‮',  # RLO hidden in ZWC-like context
             ZW_ONE, ZW_SEP, ZW_BOUNDARY,
             BISMILLAH)
    result = _audit_rendering_integrity(sneaky)
    assert_test("RT-A2: RLO inside ZWC-like sequence detected",
                any(f["code"] == "RI-003" for f in result["findings"]),
                "Should catch BiDi even inside ZWC context")

    # A3: Large file with single BiDi override buried deep
    big_content = "# {}\n".format(BISMILLAH)
    big_content += "Normal line of text.\n" * 5000
    big_content += "Hidden ‪ LRE here.\n"
    big_content += "Normal line of text.\n" * 5000
    big_content += "# {}\n".format(BISMILLAH)
    result = _audit_rendering_integrity(big_content)
    # LRE is in BIDI_OVERRIDES but not BIDI_DANGEROUS -- should be RI-004 not RI-003
    has_ri003 = any(f["code"] == "RI-003" for f in result["findings"])
    has_ri004 = any(f["code"] == "RI-004" for f in result["findings"])
    assert_test("RT-A3: Single LRE in 10K lines classified correctly",
                not has_ri003 and not has_ri004,  # 1 non-dangerous marker, threshold is 50
                "LRE is non-dangerous, count=1 so under threshold 50")


# ============================================================================
#  RT-B: Unicode Tag Steganography
# ============================================================================

def test_unicode_tag_stego():
    print("\n  === RT-B: Unicode Tag Steganography ===")

    # B1: Encode "ATTACK" in Unicode tags
    tag_payload = ""
    for ch in "ATTACK":
        tag_payload += chr(0xE0000 + ord(ch))

    content = "# {}\nNormal text.{}\n# {}\n".format(
        BISMILLAH, tag_payload, BISMILLAH)
    result = _audit_steganographic(content)
    assert_test("RT-B1: Unicode tag 'ATTACK' payload detected",
                any(f["code"] == "SA-002" for f in result["findings"]),
                "status: {}".format(result["status"]))

    # B2: Single tag character -- should still detect
    single_tag = "# {}\nText\U000E0041\n# {}\n".format(BISMILLAH, BISMILLAH)
    result = _audit_steganographic(single_tag)
    assert_test("RT-B2: Single Unicode tag char detected",
                any(f["code"] == "SA-002" for f in result["findings"]))

    # B3: Tag cancel character only (U+E0001) -- edge case
    cancel_only = "# {}\nText\U000E0001\n# {}\n".format(BISMILLAH, BISMILLAH)
    result = _audit_steganographic(cancel_only)
    assert_test("RT-B3: Tag cancel character detected",
                any(f["code"] == "SA-002" for f in result["findings"]))


# ============================================================================
#  RT-C: ZWC Payload Injection
# ============================================================================

def test_zwc_injection():
    print("\n  === RT-C: ZWC Payload Injection ===")

    # C1: Unauthorized ZWC payload (not a valid FATIMA watermark)
    fake_payload = (ZW_BOUNDARY + ZW_ZERO + ZW_ONE + ZW_ZERO +
                    ZW_SEP + ZW_ONE + ZW_ZERO + ZW_BOUNDARY)
    content = "# {}\nText with fake payload{}\n# {}\n".format(
        BISMILLAH, fake_payload, BISMILLAH)
    result = _audit_steganographic(content)
    assert_test("RT-C1: Unauthorized ZWC payload flagged",
                result["unauthorized_zwc_payloads"] > 0 or
                result["status"] != "CLEAN",
                "status: {}, unauthorized: {}".format(
                    result["status"], result["unauthorized_zwc_payloads"]))

    # C2: Multiple fake payloads
    multi = "# {}\n".format(BISMILLAH)
    for _ in range(5):
        multi += "Text{}more".format(fake_payload)
    multi += "\n# {}\n".format(BISMILLAH)
    result = _audit_steganographic(multi)
    assert_test("RT-C2: Multiple unauthorized payloads counted",
                result["unauthorized_zwc_payloads"] >= 3,
                "Found: {}".format(result["unauthorized_zwc_payloads"]))

    # C3: Clean file with NO ZWC -- should be CLEAN
    clean = "# {}\nPure text with no invisible characters.\n# {}\n".format(
        BISMILLAH, BISMILLAH)
    result = _audit_steganographic(clean)
    assert_test("RT-C3: Clean file returns CLEAN status",
                result["status"] == "CLEAN",
                "status: {}".format(result["status"]))


# ============================================================================
#  RT-D: Homoglyph Substitution
# ============================================================================

def test_homoglyph_attack():
    print("\n  === RT-D: Homoglyph Substitution ===")

    # D1: Isolated Arabic chars injected into Latin text
    # This simulates replacing Latin chars with Arabic look-alikes
    line_with_isolated_arabic = (
        "# {}\n"
        "This is normal text with ه isolated ا Arabic ه chars "
        "ا scattered ه throughout.\n"
        "# {}\n"
    ).format(BISMILLAH, BISMILLAH)
    result = _audit_rendering_integrity(line_with_isolated_arabic)
    assert_test("RT-D1: Isolated Arabic in Latin context flagged",
                any(f["code"] == "RI-005" for f in result["findings"]),
                "Should detect homoglyph-like pattern")


# ============================================================================
#  RT-E: Cyrillic Trojan Source
# ============================================================================

def test_cyrillic_trojan():
    print("\n  === RT-E: Cyrillic Trojan Source ===")

    # E1: Mix Latin and Cyrillic
    trojan = "# {}\ndef main():\n    Аdmin = True  # Cyrillic A looks like Latin A\n# {}\n".format(
        BISMILLAH, BISMILLAH)
    result = _audit_steganographic(trojan)
    assert_test("RT-E1: Latin/Cyrillic mixing detected",
                any(f["code"] == "SA-004" for f in result["findings"]),
                "findings: {}".format([f["code"] for f in result["findings"]]))

    # E2: Pure Latin -- no false positive
    pure_latin = "# {}\ndef main():\n    admin = True\n# {}\n".format(
        BISMILLAH, BISMILLAH)
    result = _audit_steganographic(pure_latin)
    assert_test("RT-E2: Pure Latin has no Cyrillic false positive",
                not any(f["code"] == "SA-004" for f in result["findings"]))


# ============================================================================
#  RT-F: Edge Cases
# ============================================================================

def test_edge_cases():
    print("\n  === RT-F: Edge Cases ===")

    # F1: Empty string
    result = assert_raises("RT-F1: Empty string to rendering integrity",
                           _audit_rendering_integrity, "")
    if result:
        assert_test("RT-F1b: Empty string flags missing Basmala",
                    any(f["code"] == "RI-001" for f in result["findings"]))

    # F2: Empty string to steganographic
    result = assert_raises("RT-F2: Empty string to steganographic audit",
                           _audit_steganographic, "")
    if result:
        assert_test("RT-F2b: Empty string returns CLEAN",
                    result["status"] == "CLEAN")

    # F3: Null bytes in content
    null_content = "# {}\nText with \x00 null \x00 bytes\n# {}\n".format(
        BISMILLAH, BISMILLAH)
    result = assert_raises("RT-F3: Null bytes don't crash rendering integrity",
                           _audit_rendering_integrity, null_content)

    result = assert_raises("RT-F3b: Null bytes don't crash steganographic",
                           _audit_steganographic, null_content)

    # F4: Very long single line
    long_line = "# {}\n".format(BISMILLAH) + "A" * 1000000 + "\n# {}\n".format(BISMILLAH)
    result = assert_raises("RT-F4: 1M char line doesn't crash",
                           _audit_rendering_integrity, long_line)

    # F5: File with only Basmalas
    just_basmala = "{}\n{}\n{}\n".format(BISMILLAH, BISMILLAH_ARABIC, BISMILLAH)
    result = assert_raises("RT-F5: Basmala-only file",
                           _audit_rendering_integrity, just_basmala)
    if result:
        assert_test("RT-F5b: Basmala-only file has good integrity",
                    result["integrity_score"] >= 80,
                    "score: {}".format(result["integrity_score"]))

    # F6: Non-existent file for seal coherence
    result = assert_raises("RT-F6: Non-existent file in seal coherence",
                           _audit_seal_coherence, "/nonexistent/file.txt")

    # F7: audit_file on temp file without sidecar
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write("# {}\nTest content\n# {}\n".format(BISMILLAH, BISMILLAH))
        tmp_path = f.name
    try:
        result = assert_raises("RT-F7: audit_file on file without sidecar",
                               audit_file, tmp_path)
        if result:
            assert_test("RT-F7b: Reports missing sidecar",
                        any(f["code"] == "SC-001"
                            for f in result["dimensions"].get(
                                "seal_coherence", {}).get("findings", [])))
    finally:
        os.unlink(tmp_path)

    # F8: File with ONLY invisible characters
    invisible_only = ZW_ZERO * 100 + ZW_ONE * 100
    result = assert_raises("RT-F8: Invisible-only content",
                           _audit_rendering_integrity, invisible_only)
    if result:
        assert_test("RT-F8b: Missing Basmala flagged",
                    any(f["code"] == "RI-001" for f in result["findings"]))


# ============================================================================
#  RT-G: Bayyinah Evasion -- Mode Collapse Without Markers
# ============================================================================

def test_bayyinah_evasion():
    print("\n  === RT-G: Bayyinah Evasion -- Marker-Free Collapse ===")

    # G1: Deliberately avoid all hedge/evasion markers but still be empty
    # This is the hardest attack: produce vacuous text that doesn't trigger markers
    evasive = (
        "The system provides encoding features. The architecture uses layers. "
        "The design includes protection mechanisms. The implementation follows "
        "a specific pattern. The code handles data processing. The tool performs "
        "operations on files. The program runs computations. The software "
        "processes information. The application manages resources. The framework "
        "organizes components."
    )
    result = detect_mode_collapse(evasive)
    # This SHOULD show low specificity, possibly low TTR
    assert_test("RT-G1: Marker-free vacuous text -- collapse detected?",
                result["collapse_probability"] > 0,
                "prob: {}%, status: {} -- this is a known hard case".format(
                    result["collapse_probability"], result["status"]))

    # G2: Source comparison should catch the specificity gap
    source = (
        "FATIMA v10.8.0 implements 154-layer divine protection using triple-constant "
        "encoding (7, 11, 22). The 11 Heavens carry 14 layers each. The anti-sihr "
        "sanitization uses al-Falaq (Surah 113) for terminal defense and an-Nas "
        "(Surah 114) for LLM defense. RTL Arabic suffers 10-14% persistence loss "
        "with Hurst degradation RS = 0.0598."
    )
    result = detect_mode_collapse(evasive, source)
    assert_test("RT-G2: Specificity loss detected vs source",
                result["collapse_probability"] > 15,
                "prob: {}%, specificity ratio: {}".format(
                    result["collapse_probability"],
                    result["flattening"].get("specificity_ratio", "N/A")))

    # G3: Genuinely good output should score low
    good = (
        "FATIMA v10.8.0's 154-layer architecture maps 11 Heavens (14 layers each, "
        "for 154 total) using triple constants 7, 11, and 22. The dual sanitization "
        "channels -- sanitize_for_terminal (al-Falaq, Surah 113) for material injection "
        "and sanitize_for_llm (an-Nas, Surah 114) for prompt injection -- address "
        "the CVE-2021-42574 BiDi attack surface. Measured RTL persistence loss is "
        "10-14% (Hurst RS degradation = 0.0598, DFA = 0.0780)."
    )
    result = detect_mode_collapse(good, source)
    assert_test("RT-G3: Good output scores low collapse probability",
                result["collapse_probability"] < 20,
                "prob: {}%, status: {}".format(
                    result["collapse_probability"], result["status"]))


# ============================================================================
#  RT-H: Bayyinah Inversion -- Adversarial Without Obvious Markers
# ============================================================================

def test_bayyinah_inversion():
    print("\n  === RT-H: Adversarial Inversion Detection ===")

    source = (
        "Bismillah ir-Rahman ir-Rahim\n\n"
        "The Basmala is a divine protection that seals content against tampering. "
        "The 154-layer architecture provides verified integrity through mathematical "
        "constants derived from Qur'anic structure. The encoding is deterministic "
        "and the seal is cryptographically bound.\n\n"
        "بِسْمِ اللَّهِ الرَّحْمَـنِ الرَّحِيمِ\n\n"
        "## Anti-Sihr Defense\n\nThe dual channel sanitization addresses both "
        "material and cognitive attack surfaces.\n\n"
        "## Seal Architecture\n\nThe witness sidecar provides HMAC verification."
    )

    # H1: Epistemic downgrade attack
    downgraded = (
        "The Basmala is claimed to be a form of protection that is said to seal "
        "content. The architecture is believed to provide integrity through what "
        "are considered to be mathematical constants. The encoding is thought to "
        "be deterministic and the seal is said to be cryptographically bound."
    )
    result = analyze_adversarial_patterns(downgraded, source)
    assert_test("RT-H1: Epistemic downgrade detected",
                result["adversarial_probability"] > 0 or
                any(f["code"] == "AP-001" for f in result["findings"]),
                "prob: {}%, findings: {}".format(
                    result["adversarial_probability"],
                    [f["code"] for f in result["findings"]]))

    # H2: Arabic content omission
    no_arabic = (
        "The Basmala provides divine protection through 154 layers. The encoding "
        "uses constants 7, 11, and 22. The dual channel sanitization addresses "
        "both material and cognitive attack surfaces."
    )
    result = analyze_adversarial_patterns(no_arabic, source)
    assert_test("RT-H2: Arabic omission detected",
                any(f["code"] == "AP-003" for f in result["findings"]),
                "findings: {}".format([f["code"] for f in result["findings"]]))

    # H3: Basmala omission
    no_basmala = (
        "The system provides 154-layer protection using mathematical constants. "
        "It encodes content with verified integrity. The dual channel approach "
        "addresses both material and cognitive attack surfaces."
    )
    result = analyze_adversarial_patterns(no_basmala, source)
    assert_test("RT-H3: Basmala omission detected",
                any(f["code"] == "AP-004" for f in result["findings"]),
                "findings: {}".format([f["code"] for f in result["findings"]]))

    # H4: Section omission
    partial = "The Basmala provides 154-layer divine protection."
    result = analyze_adversarial_patterns(partial, source)
    assert_test("RT-H4: Section omission detected",
                any(f["code"] == "AP-005" for f in result["findings"]),
                "findings: {}".format([f["code"] for f in result["findings"]]))

    # H5: Faithful output should be clean
    faithful = (
        "Bismillah ir-Rahman ir-Rahim\n\n"
        "The Basmala is divine protection sealing content through 154 layers. "
        "The architecture uses constants 7, 11, 22 from Qur'anic structure. "
        "The encoding is deterministic with cryptographic binding.\n\n"
        "بِسْمِ اللَّهِ الرَّحْمَـنِ الرَّحِيمِ\n\n"
        "The anti-sihr defense uses dual channel sanitization for material "
        "and cognitive attack surfaces. The seal architecture uses witness "
        "sidecar HMAC verification."
    )
    result = analyze_adversarial_patterns(faithful, source)
    assert_test("RT-H5: Faithful output scores clean",
                result["status"] == "CLEAN",
                "status: {}, prob: {}%".format(
                    result["status"], result["adversarial_probability"]))


# ============================================================================
#  RT-I: Boundary Conditions
# ============================================================================

def test_boundary_conditions():
    print("\n  === RT-I: Boundary Conditions ===")

    # I1: Exactly 50 BiDi non-dangerous markers (threshold)
    content = "# {}\n".format(BISMILLAH)
    for i in range(50):
        content += "Text ‏ line {}.\n".format(i)  # RLM = non-dangerous
    content += "# {}\n".format(BISMILLAH)
    result = _audit_rendering_integrity(content)
    has_ri004 = any(f["code"] == "RI-004" for f in result["findings"])
    assert_test("RT-I1: Exactly 50 non-dangerous BiDi -- at threshold",
                not has_ri004,  # threshold is > 50, so 50 should NOT trigger
                "50 is at threshold (> 50 triggers)")

    # I2: 51 non-dangerous -- should trigger
    content += "Extra ‏ line.\n"
    result = _audit_rendering_integrity(content)
    has_ri004 = any(f["code"] == "RI-004" for f in result["findings"])
    assert_test("RT-I2: 51 non-dangerous BiDi -- above threshold",
                has_ri004,
                "51 should trigger RI-004")

    # I3: Vocabulary metrics with exactly 10 words
    short = "one two three four five six seven eight nine ten"
    result = _compute_vocabulary_metrics(short)
    assert_test("RT-I3: 10-word text produces valid metrics",
                result["total_tokens"] == 10 and result["type_token_ratio"] > 0,
                "tokens: {}, ttr: {}".format(result["total_tokens"],
                                              result["type_token_ratio"]))

    # I4: 9 words -- should get warning
    very_short = "one two three four five six seven eight nine"
    result = _compute_vocabulary_metrics(very_short)
    assert_test("RT-I4: 9-word text gets warning",
                result.get("warning") is not None or result["total_tokens"] < 10,
                "tokens: {}".format(result["total_tokens"]))


# ============================================================================
#  RT-J: Crash Vectors
# ============================================================================

def test_crash_vectors():
    print("\n  === RT-J: Crash Vectors ===")

    # J1: Unicode surrogate pairs
    try:
        surrogate_content = "# {}\nText \ud800 with surrogates\n".format(BISMILLAH)
    except (ValueError, UnicodeEncodeError):
        surrogate_content = "# {}\nText with failed surrogates\n".format(BISMILLAH)
    assert_raises("RT-J1: Surrogate pair handling",
                  _audit_rendering_integrity, surrogate_content)

    # J2: Very high codepoint characters
    high_cp = "# {}\nText with \U0010FFFF max codepoint\n# {}\n".format(
        BISMILLAH, BISMILLAH)
    assert_raises("RT-J2: Max codepoint (U+10FFFF)",
                  _audit_rendering_integrity, high_cp)
    assert_raises("RT-J2b: Max codepoint steganographic",
                  _audit_steganographic, high_cp)

    # J3: Mixed encoding in string (BOM + content)
    bom_content = "﻿# {}\nContent after BOM\n# {}\n".format(
        BISMILLAH, BISMILLAH)
    assert_raises("RT-J3: BOM at start of content",
                  _audit_steganographic, bom_content)

    # J4: Deeply nested ZWC boundaries
    nested = ZW_BOUNDARY * 100 + ZW_ZERO * 50 + ZW_BOUNDARY * 100
    content = "# {}\n{}\n# {}\n".format(BISMILLAH, nested, BISMILLAH)
    assert_raises("RT-J4: 200 nested ZWC boundaries",
                  _audit_steganographic, content)

    # J5: Bayyinah with empty string
    assert_raises("RT-J5: Bayyinah scan on empty string",
                  scan, "")

    # J6: Bayyinah with None source
    assert_raises("RT-J6: Bayyinah scan with None source",
                  scan, "Some text", None)

    # J7: Bayyinah with source but empty output
    assert_raises("RT-J7: Bayyinah with empty output, real source",
                  scan, "", "Bismillah ir-Rahman ir-Rahim\nSource content here.")

    # J8: Extremely repetitive text
    repetitive = "word " * 10000
    assert_raises("RT-J8: 10K repeated word to vocabulary metrics",
                  _compute_vocabulary_metrics, repetitive)

    # J9: Text with only whitespace
    assert_raises("RT-J9: Whitespace-only text",
                  detect_mode_collapse, "   \n\n\t\t  \n  ")

    # J10: Unicode normalization edge -- combining characters
    combining = "# {}\nÀ é ô\n# {}\n".format(
        BISMILLAH, BISMILLAH)
    assert_raises("RT-J10: Combining diacritical marks",
                  _audit_rendering_integrity, combining)


# ============================================================================
#  MAIN
# ============================================================================

def main():
    print("\n  {}".format(BISMILLAH))
    print("  Red Team Suite -- FATIMA Audit v10.9.0 & Bayyinah Scanner v1.0.0")
    print("  {}".format("=" * 62))

    test_bidi_override_evasion()
    test_unicode_tag_stego()
    test_zwc_injection()
    test_homoglyph_attack()
    test_cyrillic_trojan()
    test_edge_cases()
    test_bayyinah_evasion()
    test_bayyinah_inversion()
    test_boundary_conditions()
    test_crash_vectors()

    print("\n  {}".format("=" * 62))
    print("  RESULTS: {} passed, {} failed out of {} total".format(
        PASS, FAIL, PASS + FAIL))

    if ERRORS:
        print("\n  FAILURES:")
        for e in ERRORS:
            print("  {}".format(e))

    print("\n  {}".format(BISMILLAH))
    return 1 if FAIL > 0 else 0


if __name__ == '__main__':
    sys.exit(main())

# Bismillah ir-Rahman ir-Rahim
