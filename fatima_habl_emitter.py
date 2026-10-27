# Bismillah ir-Rahman ir-Rahim
"""FATIMA audit -> HABL emitter.

Runs the Encoder's own ``audit_file()`` and records its findings as
HABL v0.1.1 Finding envelopes in ``<root>/.habl/findings.jsonl``.

This module is additive. It does not change the Encoder, its ``audit``
command, its output, or its exit codes.

Contract (Phase 2 design brief rev 2, reviewed by GPT-6):

1. Every native finding becomes exactly one HABL finding. FATIMA's code,
   severity, description and detail travel unchanged in ``payload``.
2. Category, kind and every severity change come from the tables below,
   keyed on code and native severity. Nothing is inferred from prose.
3. Line numbers are left unset: the audit reports them only inside
   English text.
4. A code, native severity, dimension or audit version this module was
   not written for is refused before anything is written.
5. Each audited file also gets one ``audit_run`` record listing what was
   examined, what was skipped, and the known detection gaps, so "no
   findings" can be told apart from "not audited". It is not an
   attestation and never says a file is safe or authentic.
6. A dimension that did not run gets its own ADVISORY finding; an audit
   error gets a HIGH finding. Missing coverage is never silent.
7. Findings are categories of observed conditions. "adversarial" means
   an attack surface was detected, not that anyone attacked. Seal
   findings describe consistency with the local witness sidecar and
   file metadata, not origin or cryptographic authenticity.
8. Severity is never changed because of other tools' findings.
9. Export fails closed: HABL missing or incompatible, or a failed
   append, raises :class:`HablExportError` (CLI exit 3). Everything is
   built and validated before one locked batch append. HABL v0.1.1 is
   not crash-atomic, so a crash mid-write can still leave a partial
   final record.
"""
# Bismillah ir-Rahman ir-Rahim

from __future__ import annotations

import argparse
import contextlib
import os
import sys
import uuid
from pathlib import Path
from types import ModuleType
from typing import Any

SOURCE_TOOL = "fatima"
EMITTER_VERSION = "0.1.0"

HABL_MIN_VERSION = (0, 1, 1)
HABL_MAX_VERSION_EXCLUSIVE = (0, 2, 0)
_HABL_REQUIRED_NAMES = ("Category", "Finding", "Location", "Severity", "append_findings")

# The mapping tables below were written against this audit version and
# checked code by code against its source. Another version must be
# reviewed before it is accepted.
SUPPORTED_AUDIT_VERSIONS = frozenset({"10.9.0"})

EXIT_OK = 0
EXIT_USAGE = 2
EXIT_EXPORT_FAILED = 3

DIMENSIONS = ("rendering_integrity", "steganographic", "seal_coherence")
_DIMENSION_PREFIX = {"rendering_integrity": "RI-", "steganographic": "SA-", "seal_coherence": "SC-"}

KIND_POLICY = "policy"
KIND_OBSERVED = "observed_condition"
KIND_LOCAL_SEAL = "local_seal_consistency"
KIND_COVERAGE = "coverage"
KIND_AUDIT_RUN = "audit_run"

# code -> (HABL category, kind)
CODE_TABLE: dict[str, tuple[str, str]] = {
    # Basmala placement: a seal-convention (policy) classification, not a
    # cryptographic seal result. A dedicated policy category is proposed
    # for HABL v0.2.
    "RI-001": ("seal", KIND_POLICY),
    "RI-002": ("seal", KIND_POLICY),
    "RI-006": ("seal", KIND_POLICY),
    # Detected attack surfaces.
    "RI-003": ("adversarial", KIND_OBSERVED),
    "RI-004": ("adversarial", KIND_OBSERVED),
    "RI-005": ("adversarial", KIND_OBSERVED),
    "SA-001": ("adversarial", KIND_OBSERVED),
    "SA-002": ("adversarial", KIND_OBSERVED),
    "SA-003": ("adversarial", KIND_OBSERVED),
    "SA-004": ("adversarial", KIND_OBSERVED),
    # Consistency with the local witness sidecar.
    "SC-001": ("seal", KIND_LOCAL_SEAL),
    "SC-002": ("seal", KIND_LOCAL_SEAL),
    "SC-003": ("seal", KIND_LOCAL_SEAL),
    "SC-004": ("temporal", KIND_LOCAL_SEAL),
    "SC-005": ("seal", KIND_LOCAL_SEAL),
    "SC-006": ("seal", KIND_LOCAL_SEAL),
}

# Native severity -> HABL severity. HABL has no INFO level.
NATIVE_SEVERITY = {"CRITICAL": "critical", "HIGH": "high", "MEDIUM": "medium", "INFO": "advisory"}

# Overrides, keyed on (code, native severity). Approved in the design
# review: a missing or displaced Basmala is a policy gap and should not
# rank with BiDi overrides or tag steganography. The native severity
# stays in payload.native_severity.
SEVERITY_OVERRIDES: dict[tuple[str, str], str] = {
    ("RI-001", "CRITICAL"): "medium",
    ("RI-002", "HIGH"): "advisory",
}

# Known limits of the audit at the supported version, written into every
# audit_run record until fixed.
KNOWN_DETECTION_GAPS = (
    "Zero-width characters in the Encoder's own ZWC alphabet (U+200B, U+200C, "
    "U+200D, U+FEFF) are not reported when they appear outside a recognized "
    "watermark: steganographic.invisible_chars skips them and the payload check "
    "only looks for paired boundaries. Confirmed at Encoder d63689e.",
    "Line numbers appear only inside description or detail text, so findings "
    "carry no structured line.",
    "SC-002, SC-004, SC-005 and SC-006 each name more than one condition; "
    "(code, native severity) does not identify the condition. Read description.",
)


# ---------------------------------------------------------------------------
# Errors
# ---------------------------------------------------------------------------


class HablExportError(RuntimeError):
    """HABL export was requested and did not complete."""


class HablUnavailableError(HablExportError):
    """HABL is not installed, or its version or API is incompatible."""


class UnsupportedAuditError(HablExportError):
    """The audit report contains something this emitter was not written for."""


# ---------------------------------------------------------------------------
# HABL availability
# ---------------------------------------------------------------------------


def _parse_version(text: str) -> tuple[int, ...]:
    parts = []
    for piece in text.split(".")[:3]:
        digits = "".join(ch for ch in piece if ch.isdigit())
        if not digits:
            break
        parts.append(int(digits))
    return tuple(parts)


def require_habl() -> ModuleType:
    """Import HABL and confirm a compatible version and API."""
    try:
        import habl
    except ImportError as exc:
        raise HablUnavailableError("HABL export requested but habl is not installed") from exc
    raw = getattr(habl, "__version__", None)
    version = _parse_version(raw) if isinstance(raw, str) else ()
    if not version or not (HABL_MIN_VERSION <= version < HABL_MAX_VERSION_EXCLUSIVE):
        raise HablUnavailableError(
            "habl {!r} is not supported; this emitter needs habl >= 0.1.1, < 0.2".format(raw)
        )
    missing = [n for n in _HABL_REQUIRED_NAMES if not hasattr(habl, n)]
    if missing:
        raise HablUnavailableError("habl {} is missing required API: {}".format(raw, ", ".join(missing)))
    return habl


# ---------------------------------------------------------------------------
# Encoder access
# ---------------------------------------------------------------------------


def _load_encoder() -> ModuleType:
    """Import the Encoder with anything it prints sent to stderr, so a
    caller reading this module's stdout is not mixed with banners."""
    here = os.path.dirname(os.path.abspath(__file__))
    if here not in sys.path:
        sys.path.insert(0, here)
    with contextlib.redirect_stdout(sys.stderr):
        import bismillah_encoder
    return bismillah_encoder


def run_audit(filepath: str | Path) -> dict[str, Any]:
    """Call the Encoder's audit_file() directly (no CLI parsing)."""
    encoder = _load_encoder()
    with contextlib.redirect_stdout(sys.stderr):
        return encoder.audit_file(str(filepath))


def audit_targets(path: str | Path) -> list[Path]:
    """Files the Encoder's own audit_directory() would audit, same rules."""
    encoder = _load_encoder()
    p = Path(path)
    if p.is_file():
        return [p]
    exts = set(encoder.TEXT_EXTENSIONS) | set(encoder.CODE_EXTENSIONS) | set(encoder.BINARY_EXTENSIONS)
    out: list[Path] = []
    for dirpath, dirnames, filenames in os.walk(p):
        dirnames[:] = sorted(d for d in dirnames if d not in (".git", "__pycache__", "node_modules"))
        for fname in sorted(filenames):
            if fname.endswith(".bismillah") or fname.endswith(".pyc") or fname == encoder.SELF_NAME:
                continue
            if os.path.splitext(fname)[1].lower() in exts:
                out.append(Path(dirpath) / fname)
    return out


# ---------------------------------------------------------------------------
# Conversion
# ---------------------------------------------------------------------------


def ledger_file_path(file_path: str | Path, project_root: str | Path) -> str:
    """Project-root-relative POSIX path when inside the root, else as given.

    Same convention as the furqan-lint emitter, so findings from both
    tools on one file can correlate.
    """
    try:
        return Path(file_path).resolve().relative_to(Path(project_root).resolve()).as_posix()
    except ValueError:
        return str(file_path)


def _habl_severity(code: str, native: str) -> str:
    override = SEVERITY_OVERRIDES.get((code, native))
    if override is not None:
        return override
    if native not in NATIVE_SEVERITY:
        raise UnsupportedAuditError("unknown native severity {!r} on {}".format(native, code))
    return NATIVE_SEVERITY[native]


def _metrics(dimension_report: dict[str, Any]) -> dict[str, Any]:
    return {k: v for k, v in sorted(dimension_report.items()) if k != "findings"}


def report_to_findings(
    report: dict[str, Any],
    recorded_path: str,
    habl: ModuleType,
    run_id: str | None = None,
) -> list[Any]:
    """Convert one audit_file() report into HABL Findings.

    Order: native findings (dimension order, then report order), then
    coverage findings, then the audit_run record. All share one
    correlation_id for this run.
    """
    version = report.get("audit_version")
    if version not in SUPPORTED_AUDIT_VERSIONS:
        raise UnsupportedAuditError(
            "audit_version {!r} is not one this emitter was reviewed against ({})".format(
                version, ", ".join(sorted(SUPPORTED_AUDIT_VERSIONS))
            )
        )
    dimensions = report.get("dimensions")
    if not isinstance(dimensions, dict):
        raise UnsupportedAuditError("audit report has no dimensions mapping")
    unknown_dims = sorted(set(dimensions) - set(DIMENSIONS))
    if unknown_dims:
        raise UnsupportedAuditError("unknown audit dimension(s): {}".format(", ".join(unknown_dims)))

    run_id = run_id or "fatima-audit-" + uuid.uuid4().hex
    timestamp = report.get("timestamp")
    location = habl.Location(file=recorded_path)

    extra: dict[str, Any] = {}
    if timestamp is not None:  # otherwise HABL stamps the time of conversion
        extra["timestamp"] = timestamp

    def make(severity: str, category: str, summary: str, payload: dict[str, Any]) -> Any:
        return habl.Finding(
            source_tool=SOURCE_TOOL,
            severity=severity,
            category=category,
            summary=summary,
            location=location,
            correlation_id=run_id,
            payload=payload,
            **extra,
        )

    findings: list[Any] = []
    native_count = 0
    for dim in DIMENSIONS:
        if dim not in dimensions:
            continue
        dim_report = dimensions[dim]
        for raw in dim_report.get("findings", []):
            code = raw.get("code")
            native = raw.get("severity")
            if code not in CODE_TABLE:
                raise UnsupportedAuditError("unknown finding code {!r} in {}".format(code, dim))
            if not code.startswith(_DIMENSION_PREFIX[dim]):
                raise UnsupportedAuditError("code {} reported under dimension {}".format(code, dim))
            category, kind = CODE_TABLE[code]
            findings.append(
                make(
                    _habl_severity(code, native),
                    category,
                    raw.get("description", ""),
                    {
                        "record_kind": "finding",
                        "kind": kind,
                        "code": code,
                        "native_severity": native,
                        "description": raw.get("description"),
                        "detail": raw.get("detail"),
                        "dimension": dim,
                        "dimension_ran": True,
                        "dimension_metrics": _metrics(dim_report),
                        "audit_version": version,
                        "emitter_version": EMITTER_VERSION,
                    },
                )
            )
            native_count += 1

    examined = [d for d in DIMENSIONS if d in dimensions]
    skipped = [d for d in DIMENSIONS if d not in dimensions]
    error = report.get("error")
    if error is not None:
        skip_reason = "audit error: {}".format(error)
    else:
        skip_reason = "file not read as text (binary or unlisted extension); only seal coherence runs"
    for dim in skipped:
        findings.append(
            make(
                "advisory",
                "seal",
                "FATIMA did not examine {} for this file".format(dim),
                {
                    "record_kind": "finding",
                    "kind": KIND_COVERAGE,
                    "code": "FATIMA-NOT-EXAMINED",
                    "native_severity": None,
                    "dimension": dim,
                    "dimension_ran": False,
                    "reason": skip_reason,
                    "audit_version": version,
                    "emitter_version": EMITTER_VERSION,
                },
            )
        )
    if error is not None:
        findings.append(
            make(
                "high",
                "seal",
                "FATIMA audit could not complete for this file",
                {
                    "record_kind": "finding",
                    "kind": KIND_COVERAGE,
                    "code": "FATIMA-AUDIT-ERROR",
                    "native_severity": None,
                    "error": str(error),
                    "native_overall_status": report.get("overall_status"),
                    "audit_version": version,
                    "emitter_version": EMITTER_VERSION,
                },
            )
        )

    findings.append(
        make(
            "advisory",
            "seal",
            "FATIMA audit run: {} of {} dimensions examined, {} native finding(s). "
            "Not an attestation; see known_detection_gaps.".format(len(examined), len(DIMENSIONS), native_count),
            {
                "record_kind": KIND_AUDIT_RUN,
                "kind": KIND_AUDIT_RUN,
                "native_overall_status": report.get("overall_status"),
                "native_finding_count": native_count,
                "native_critical_count": report.get("critical_findings"),
                "dimensions_examined": examined,
                "dimensions_not_examined": skipped,
                "error": None if error is None else str(error),
                "known_detection_gaps": list(KNOWN_DETECTION_GAPS),
                "audit_version": version,
                "emitter_version": EMITTER_VERSION,
            },
        )
    )
    return findings


def emit_paths(paths: list[Path], project_root: str | Path) -> int:
    """Audit each path and append every resulting finding in one batch.

    Returns the number of records appended. Raises HablExportError (or a
    subclass) if export did not complete; then nothing was written,
    unless the process or OS failed mid-write.
    """
    habl = require_habl()
    findings: list[Any] = []
    for path in paths:
        report = run_audit(path)
        recorded = ledger_file_path(path, project_root)
        try:
            findings.extend(report_to_findings(report, recorded, habl))
        except HablExportError:
            raise
        except (TypeError, ValueError, KeyError, AttributeError) as exc:
            raise HablExportError("could not build HABL findings for {}: {}".format(recorded, exc)) from exc
    if not findings:
        return 0
    try:
        habl.append_findings(findings, project_root)
    except (OSError, TypeError, ValueError) as exc:
        raise HablExportError("HABL append failed: {}".format(exc)) from exc
    return len(findings)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main(argv: list[str] | None = None, out: Any = None, err: Any = None) -> int:
    out = out or sys.stdout
    err = err or sys.stderr
    parser = argparse.ArgumentParser(
        prog="fatima_habl_emitter.py",
        description="Run the FATIMA audit and record its findings in a HABL ledger.",
    )
    parser.add_argument("path", help="File or directory to audit")
    parser.add_argument(
        "--habl-root",
        help="Directory holding .habl/ (default: the directory, or the file's parent)",
    )
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        return EXIT_USAGE if exc.code else EXIT_OK

    target = Path(args.path)
    if not target.exists():
        print("Not found: {}".format(target), file=err)
        return EXIT_USAGE
    root = Path(args.habl_root) if args.habl_root else (target if target.is_dir() else target.parent)

    try:
        count = emit_paths(audit_targets(target), root)
    except HablExportError as exc:
        print("HABL EXPORT FAILED: {}".format(exc), file=err)
        print("Nothing from this run was written.", file=err)
        return EXIT_EXPORT_FAILED
    print("HABL: {} record(s) appended to {}".format(count, Path(root) / ".habl" / "findings.jsonl"), file=out)
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())

# Bismillah ir-Rahman ir-Rahim
