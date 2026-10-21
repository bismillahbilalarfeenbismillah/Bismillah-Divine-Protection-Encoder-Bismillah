# Bismillah ir-Rahman ir-Rahim
"""
Bismillah Finding Module — Stub Implementation (v10.2.0)

Standardized finding objects for the Bismillah integrity system.
Findings can originate from the encoder, the Furqan diagnostic,
or the security scanner.

STATUS: Stub — shipped per Council Action Item 3b so test_encoder.py
can import and the test suite is independently executable.
"""
# Bismillah ir-Rahman ir-Rahim

from collections import OrderedDict


class BismillahFinding:
    """A standardized finding from any Bismillah integrity check.

    Attributes:
        source: Origin of the finding ('encoder', 'furqan', 'scanner').
        severity: 'critical', 'warning', 'info'.
        category: Finding category string.
        message: Human-readable description.
        evidence: dict of supporting evidence.
        file_path: Path to the affected file, if applicable.
    """

    SEVERITIES = ('critical', 'warning', 'info')
    SOURCES = ('encoder', 'furqan', 'scanner', 'fatima')

    def __init__(self, source, severity, category, message,
                 evidence=None, file_path=None):
        if severity not in self.SEVERITIES:
            raise ValueError(
                "severity must be one of {}".format(self.SEVERITIES))
        self.source = source
        self.severity = severity
        self.category = category
        self.message = message
        self.evidence = evidence or {}
        self.file_path = file_path

    def __repr__(self):
        return "BismillahFinding(source={!r}, severity={!r}, category={!r})".format(
            self.source, self.severity, self.category)

    def to_dict(self):
        return OrderedDict([
            ("source", self.source),
            ("severity", self.severity),
            ("category", self.category),
            ("message", self.message),
            ("evidence", self.evidence),
            ("file_path", self.file_path),
        ])


def from_encoder_finding(raw_finding):
    """Convert a raw encoder finding dict to a BismillahFinding.

    Args:
        raw_finding: dict with keys from the encoder's internal format.

    Returns:
        BismillahFinding: Standardized finding.
    """
    return BismillahFinding(
        source='encoder',
        severity=raw_finding.get('severity', 'info'),
        category=raw_finding.get('category', 'general'),
        message=raw_finding.get('message', ''),
        evidence=raw_finding.get('evidence', {}),
        file_path=raw_finding.get('file_path'),
    )


def from_furqan_diagnostic(diagnostic):
    """Convert a Furqan diagnostic to a BismillahFinding.

    Args:
        diagnostic: dict from the Furqan diagnostic system.

    Returns:
        BismillahFinding: Standardized finding.
    """
    return BismillahFinding(
        source='furqan',
        severity=diagnostic.get('level', 'info'),
        category=diagnostic.get('type', 'diagnostic'),
        message=diagnostic.get('description', ''),
        evidence=diagnostic.get('data', {}),
        file_path=diagnostic.get('path'),
    )


def from_scanner_finding(scan_result):
    """Convert a security scanner result to a BismillahFinding.

    Args:
        scan_result: dict from the security scanner.

    Returns:
        BismillahFinding: Standardized finding.
    """
    return BismillahFinding(
        source='scanner',
        severity=scan_result.get('severity', 'warning'),
        category=scan_result.get('rule', 'scan'),
        message=scan_result.get('message', ''),
        evidence=scan_result.get('context', {}),
        file_path=scan_result.get('file'),
    )


# Bismillah ir-Rahman ir-Rahim
