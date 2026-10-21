# Bismillah ir-Rahman ir-Rahim
"""
Fatiha CLI Module — Stub Implementation (v10.2.0)

Command-line interface for the Bismillah integrity system.
Named after Al-Fatiha (The Opening) — the gateway to verification.

Provides:
  - check_posture_text: Verify text content posture (banned vocabulary, etc.)
  - run_fatiha_session: Interactive verification session

STATUS: Stub — shipped per Council Action Item 3b so test_encoder.py
can import and the test suite is independently executable.
"""
# Bismillah ir-Rahman ir-Rahim

import sys
from collections import OrderedDict

# --- Banned vocabulary for posture checking ---
# Words that should not appear in integrity-critical documents
_BANNED_VOCABULARY = frozenset({
    # Overclaiming terms (the CROSSED bug taught us this lesson)
    'proven', 'proved', 'QED', 'trivially', 'obviously',
})

# --- Posture categories ---
POSTURE_CLEAN = 'CLEAN'
POSTURE_WARNING = 'WARNING'
POSTURE_VIOLATION = 'VIOLATION'


def check_posture_text(text, strict=False):
    """Check text for posture violations (banned vocabulary, overclaiming).

    Args:
        text: String to check.
        strict: If True, warnings become violations.

    Returns:
        dict with keys:
          - posture: CLEAN, WARNING, or VIOLATION
          - findings: list of finding dicts
          - word_count: total words checked
    """
    if not isinstance(text, str):
        text = str(text)

    words = text.lower().split()
    findings = []

    for i, word in enumerate(words):
        clean_word = word.strip('.,;:!?()[]{}"\'-')
        if clean_word in _BANNED_VOCABULARY:
            findings.append(OrderedDict([
                ("word", clean_word),
                ("position", i),
                ("context", " ".join(words[max(0, i-3):i+4])),
                ("severity", POSTURE_VIOLATION if strict else POSTURE_WARNING),
            ]))

    if not findings:
        posture = POSTURE_CLEAN
    elif strict or any(f["severity"] == POSTURE_VIOLATION for f in findings):
        posture = POSTURE_VIOLATION
    else:
        posture = POSTURE_WARNING

    return OrderedDict([
        ("posture", posture),
        ("findings", findings),
        ("word_count", len(words)),
    ])


def run_fatiha_session(target_path=None, interactive=True, **kwargs):
    """Run an interactive Fatiha verification session.

    Args:
        target_path: Path to file or directory to verify.
        interactive: If True, prompt for user input.

    Returns:
        dict: Session results.

    Raises:
        NotImplementedError: Full interactive session pending.
    """
    if interactive:
        raise NotImplementedError(
            "run_fatiha_session (interactive mode): pending implementation. "
            "Stub shipped per Council Action Item 3b. "
            "Use check_posture_text() for non-interactive posture checks."
        )

    # Non-interactive mode: basic posture check on file
    if target_path is None:
        return OrderedDict([
            ("status", "no_target"),
            ("message", "No target path provided."),
        ])

    try:
        with open(target_path, 'r', encoding='utf-8') as f:
            content = f.read()
        posture_result = check_posture_text(content)
        return OrderedDict([
            ("status", "completed"),
            ("target", target_path),
            ("posture", posture_result),
        ])
    except (IOError, OSError) as e:
        return OrderedDict([
            ("status", "error"),
            ("target", target_path),
            ("error", str(e)),
        ])


# Bismillah ir-Rahman ir-Rahim
