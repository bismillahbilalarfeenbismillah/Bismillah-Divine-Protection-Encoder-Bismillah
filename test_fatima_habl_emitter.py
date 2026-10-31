# Bismillah ir-Rahman ir-Rahim
"""Tests for fatima_habl_emitter (Phase 2, design brief rev 2).

Runs under pytest or unittest. Requires habl >= 0.1.1, < 0.2.
"""
# Bismillah ir-Rahman ir-Rahim

import copy
import io
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

try:
    import habl
    from habl import ledger_path
    from habl.query import load_ledger
except ImportError:  # pragma: no cover
    habl = None

import fatima_habl_emitter as fe  # noqa: E402  (after sys.path setup)

BASMALA = "# Bismillah ir-Rahman ir-Rahim\n"
VERSION = "10.9.0"


def _write(directory, name, text, encoding="utf-8"):
    p = Path(directory) / name
    p.write_bytes(text.encode(encoding) if isinstance(text, str) else text)
    return p


def _report(findings_by_dim, dims=fe.DIMENSIONS, **extra):
    """A synthetic audit_file() report in the 10.9.x shape."""
    report = {
        "filepath": "x.py",
        "audit_version": extra.pop("audit_version", VERSION),
        "timestamp": "2026-10-27T12:00:00+00:00",
        "dimensions": {},
        "overall_status": "FAIL",
        "total_findings": 0,
        "actionable_findings": 0,
        "critical_findings": 0,
    }
    for d in dims:
        report["dimensions"][d] = {"findings": list(findings_by_dim.get(d, [])), "metric": 1}
    report.update(extra)
    return report


def _f(code, severity, description="desc", detail="detail"):
    return {"code": code, "severity": severity, "description": description, "detail": detail}


def _payloads(findings):
    return [f.payload for f in findings]


@unittest.skipIf(habl is None, "habl not installed")
class TestMapping(unittest.TestCase):
    def convert(self, report, path="x.py"):
        return fe.report_to_findings(report, path, habl, run_id="run-1")

    def test_every_table_code_maps_and_keeps_native_fields(self):
        dim_for = {"RI-": "rendering_integrity", "SA-": "steganographic", "SC-": "seal_coherence"}
        by_dim = {}
        for code in sorted(fe.CODE_TABLE):
            by_dim.setdefault(dim_for[code[:3]], []).append(_f(code, "HIGH", "d " + code, "x " + code))
        out = self.convert(_report(by_dim))
        native = [f for f in out if f.payload["record_kind"] == "finding"]
        self.assertEqual(sorted(f.payload["code"] for f in native), sorted(fe.CODE_TABLE))
        for f in native:
            code = f.payload["code"]
            self.assertEqual(f.category.value, fe.CODE_TABLE[code][0])
            self.assertEqual(f.payload["kind"], fe.CODE_TABLE[code][1])
            self.assertEqual(f.payload["native_severity"], "HIGH")
            self.assertEqual(f.summary, "d " + code)
            self.assertEqual(f.payload["description"], "d " + code)
            self.assertEqual(f.payload["detail"], "x " + code)
            self.assertIsNone(f.location.line)
            self.assertEqual(f.correlation_id, "run-1")
            self.assertEqual(f.timestamp, "2026-10-27T12:00:00+00:00")

    def test_approved_severity_overrides_only(self):
        out = self.convert(
            _report(
                {
                    "rendering_integrity": [
                        _f("RI-001", "CRITICAL"),
                        _f("RI-002", "HIGH"),
                        _f("RI-003", "CRITICAL"),
                        _f("RI-006", "INFO"),
                    ]
                }
            )
        )
        got = {f.payload["code"]: (f.severity.value, f.payload["native_severity"]) for f in out[:4]}
        self.assertEqual(
            got,
            {
                "RI-001": ("medium", "CRITICAL"),
                "RI-002": ("advisory", "HIGH"),
                "RI-003": ("critical", "CRITICAL"),
                "RI-006": ("advisory", "INFO"),
            },
        )
        self.assertEqual(out[0].payload["kind"], fe.KIND_POLICY)
        self.assertEqual(out[2].payload["kind"], fe.KIND_OBSERVED)

    def test_new_codes_accepted_at_supported_versions(self):
        """SA-005 (10.9.1+), SA-006/SA-007 (10.9.3+) are in CODE_TABLE."""
        for code in ("SA-005", "SA-006", "SA-007"):
            self.assertIn(code, fe.CODE_TABLE)
        # SA-005 at 10.9.1
        out = self.convert(
            _report({"steganographic": [_f("SA-005", "MEDIUM")]}, audit_version="10.9.1"))
        self.assertEqual(out[0].payload["code"], "SA-005")
        # SA-006 (INFO) and SA-007 (HIGH) at 10.9.3
        out = self.convert(
            _report({"steganographic": [
                _f("SA-006", "INFO"), _f("SA-007", "HIGH")]}, audit_version="10.9.3"))
        codes = [f.payload["code"] for f in out if f.payload.get("record_kind") == "finding"]
        self.assertIn("SA-006", codes)
        self.assertIn("SA-007", codes)
        # SA-006 maps to seal/coverage, SA-007 to adversarial/observed
        sa6 = [f for f in out if f.payload.get("code") == "SA-006"][0]
        sa7 = [f for f in out if f.payload.get("code") == "SA-007"][0]
        self.assertEqual(sa6.category.value, "seal")
        self.assertEqual(sa6.payload["kind"], fe.KIND_COVERAGE)
        self.assertEqual(sa7.category.value, "adversarial")
        self.assertEqual(sa7.payload["kind"], fe.KIND_OBSERVED)

    def test_actionable_findings_in_audit_run(self):
        """The audit_run record carries native_actionable_count (v10.9.2+)."""
        out = self.convert(
            _report({"rendering_integrity": [_f("RI-003", "CRITICAL")]},
                    actionable_findings=1, audit_version="10.9.2"))
        run = [f for f in out if f.payload.get("record_kind") == fe.KIND_AUDIT_RUN][0]
        self.assertEqual(run.payload["native_actionable_count"], 1)

    def test_all_supported_versions_accepted(self):
        for v in ("10.9.0", "10.9.1", "10.9.2", "10.9.3"):
            out = self.convert(_report({}, audit_version=v))
            self.assertTrue(len(out) >= 1, v)

    def test_shared_code_conditions_keep_their_own_description(self):
        out = self.convert(
            _report(
                {
                    "seal_coherence": [
                        _f("SC-005", "MEDIUM", "Cannot recompute content hash: boom"),
                        _f("SC-005", "MEDIUM", "No dual seal stored in sidecar"),
                        _f("SC-004", "HIGH", "File modified after seal"),
                        _f("SC-004", "MEDIUM", "No seal timestamp in sidecar"),
                    ]
                }
            )
        )
        self.assertEqual(
            [(f.payload["code"], f.severity.value, f.category.value, f.summary) for f in out[:4]],
            [
                ("SC-005", "medium", "seal", "Cannot recompute content hash: boom"),
                ("SC-005", "medium", "seal", "No dual seal stored in sidecar"),
                ("SC-004", "high", "temporal", "File modified after seal"),
                ("SC-004", "medium", "temporal", "No seal timestamp in sidecar"),
            ],
        )

    def test_run_record_always_present_and_not_an_attestation(self):
        out = self.convert(_report({}))
        self.assertEqual(len(out), 1)
        run = out[0]
        self.assertEqual(run.payload["record_kind"], fe.KIND_AUDIT_RUN)
        self.assertEqual(run.severity.value, "advisory")
        self.assertEqual(run.payload["native_finding_count"], 0)
        self.assertEqual(run.payload["dimensions_examined"], list(fe.DIMENSIONS))
        self.assertEqual(run.payload["known_detection_gaps"], list(fe.KNOWN_DETECTION_GAPS))
        text = (run.summary + json.dumps(run.payload)).lower()
        for word in ("safe", "authentic", "verified", "clean"):
            self.assertNotIn(word, run.summary.lower())
        self.assertIn("not an attestation", text)

    def test_skipped_dimensions_and_errors_are_recorded(self):
        out = self.convert(_report({}, dims=("seal_coherence",)))
        skipped = [f for f in out if f.payload.get("code") == "FATIMA-NOT-EXAMINED"]
        self.assertEqual([f.payload["dimension"] for f in skipped], ["rendering_integrity", "steganographic"])
        self.assertTrue(all(f.payload["dimension_ran"] is False for f in skipped))
        out = self.convert(_report({}, dims=("seal_coherence",), error="Cannot read file: bad bytes"))
        err = [f for f in out if f.payload.get("code") == "FATIMA-AUDIT-ERROR"]
        self.assertEqual(len(err), 1)
        self.assertEqual(err[0].severity.value, "high")
        self.assertIn("bad bytes", err[0].payload["error"])
        self.assertIn("audit error", out[0].payload["reason"])

    def test_unsupported_input_is_refused(self):
        cases = [
            _report({"rendering_integrity": [_f("RI-999", "HIGH")]}),
            _report({"rendering_integrity": [_f("RI-001", "LOW")]}),
            _report({"steganographic": [_f("RI-003", "CRITICAL")]}),
            _report({}, audit_version="10.10.0"),
            _report({}, audit_version=None),
        ]
        weird = _report({})
        weird["dimensions"]["quantum"] = {"findings": []}
        cases.append(weird)
        for report in cases:
            with self.assertRaises(fe.UnsupportedAuditError):
                self.convert(report)

    def test_conversion_does_not_mutate_report(self):
        report = _report({"rendering_integrity": [_f("RI-003", "CRITICAL")]})
        before = copy.deepcopy(report)
        self.convert(report)
        self.assertEqual(report, before)

    def test_ledger_path_relative_posix(self):
        with tempfile.TemporaryDirectory() as d:
            (Path(d) / "pkg").mkdir()
            self.assertEqual(fe.ledger_file_path(Path(d) / "pkg" / "a.py", d), "pkg/a.py")


@unittest.skipIf(habl is None, "habl not installed")
class TestRealAudit(unittest.TestCase):
    """Runs the Encoder's real audit_file() on fixtures."""

    def run_cli(self, argv):
        out, err = io.StringIO(), io.StringIO()
        return fe.main(argv, out, err), out.getvalue(), err.getvalue()

    def test_end_to_end_round_trip(self):
        with tempfile.TemporaryDirectory() as d:
            _write(d, "bad.py", 'x = "admin\u202e"\nprint("\u0430dmin")\n')
            _write(d, "ok.py", BASMALA + "def f():\n    return 1\n" + BASMALA)
            code, out, err = self.run_cli([d])
            self.assertEqual(code, fe.EXIT_OK, err)
            load = load_ledger(d)
            self.assertEqual(load.malformed, [])
            by_file = {}
            for f in load.findings:
                by_file.setdefault(f.location.file, []).append(f)
            self.assertEqual(sorted(by_file), ["bad.py", "ok.py"])
            for name, fs in by_file.items():
                self.assertEqual(len({f.correlation_id for f in fs}), 1, name)
                self.assertEqual(fs[-1].payload["record_kind"], fe.KIND_AUDIT_RUN)
            codes = [f.payload["code"] for f in by_file["bad.py"] if f.payload["record_kind"] == "finding"]
            self.assertIn("RI-003", codes)
            self.assertIn("SA-004", codes)
            # Native fields equal the Encoder's own report, field by field.
            native = fe.run_audit(Path(d) / "bad.py")
            raw = [x for dim in fe.DIMENSIONS for x in native["dimensions"][dim]["findings"]]
            emitted = [f for f in by_file["bad.py"] if f.payload["record_kind"] == "finding"]
            self.assertEqual(
                [(x["code"], x["severity"], x["description"], x["detail"]) for x in raw],
                [
                    (f.payload["code"], f.payload["native_severity"], f.payload["description"], f.payload["detail"])
                    for f in emitted
                ],
            )

    def test_binary_file_records_skipped_dimensions(self):
        with tempfile.TemporaryDirectory() as d:
            _write(d, "blob.bin", b"\x00\x01\x02binary")
            self.assertEqual(self.run_cli([d])[0], fe.EXIT_OK)
            payloads = _payloads(load_ledger(d).findings)
            self.assertEqual(
                sorted(p["dimension"] for p in payloads if p.get("code") == "FATIMA-NOT-EXAMINED"),
                ["rendering_integrity", "steganographic"],
            )

    def test_unreadable_text_file_records_audit_error(self):
        with tempfile.TemporaryDirectory() as d:
            _write(d, "latin.py", b"x = '\xff\xfe'\n")
            self.assertEqual(self.run_cli([d])[0], fe.EXIT_OK)
            payloads = _payloads(load_ledger(d).findings)
            self.assertEqual([p["code"] for p in payloads if p.get("code") == "FATIMA-AUDIT-ERROR"], ["FATIMA-AUDIT-ERROR"])

    def test_stray_zwc_gap_closed_and_sa006_gap_disclosed(self):
        """The U+200B gap was closed by SA-005 (Encoder PR #4). The
        known_detection_gaps no longer mention it. Instead, the SA-006
        authentication gap (B2 not yet implemented) is disclosed."""
        with tempfile.TemporaryDirectory() as d:
            _write(d, "control.py", BASMALA + 'pw = "admin"\n' + BASMALA)
            _write(d, "zwsp.py", BASMALA + 'pw = "adm\u200bin"\n' + BASMALA)
            self.assertEqual(self.run_cli([d])[0], fe.EXIT_OK)
            runs = {
                f.location.file: f.payload
                for f in load_ledger(d).findings
                if f.payload["record_kind"] == fe.KIND_AUDIT_RUN
            }
            # The U+200B gap is closed -- no longer in known_detection_gaps
            self.assertFalse(any("U+200B" in g for g in runs["zwsp.py"]["known_detection_gaps"]))
            # The SA-006 authentication gap is disclosed
            self.assertTrue(any("SA-006" in g for g in runs["zwsp.py"]["known_detection_gaps"]))

    def test_encoder_audit_output_unchanged_by_emitter(self):
        with tempfile.TemporaryDirectory() as d:
            p = _write(d, "bad.py", 'x = "admin\u202e"\n')
            before = fe.run_audit(p)
            self.run_cli([d])
            after = fe.run_audit(p)
            for r in (before, after):
                r.pop("timestamp")
            self.assertEqual(before, after)


@unittest.skipIf(habl is None, "habl not installed")
class TestFailClosed(unittest.TestCase):
    def run_cli(self, argv):
        out, err = io.StringIO(), io.StringIO()
        return fe.main(argv, out, err), out.getvalue(), err.getvalue()

    def test_habl_missing_exits_3_and_writes_nothing(self):
        with tempfile.TemporaryDirectory() as d:
            _write(d, "a.py", 'x = "\u202e"\n')
            with mock.patch.dict(sys.modules, {"habl": None}):
                code, _, err = self.run_cli([d])
            self.assertEqual(code, fe.EXIT_EXPORT_FAILED)
            self.assertIn("not installed", err)
            self.assertFalse(ledger_path(d).exists())

    def test_incompatible_habl_version_exits_3(self):
        for version in ("0.1.0", "0.2.0", None, "x"):
            with tempfile.TemporaryDirectory() as d, mock.patch.object(habl, "__version__", version):
                _write(d, "a.py", "x = 1\n")
                self.assertEqual(self.run_cli([d])[0], fe.EXIT_EXPORT_FAILED, version)
                self.assertFalse(ledger_path(d).exists())

    def test_unsupported_report_in_batch_writes_nothing(self):
        real = fe.run_audit

        def tampered(path):
            r = real(path)
            if Path(path).name == "b.py":
                r["audit_version"] = "99.0.0"
            return r

        with tempfile.TemporaryDirectory() as d:
            _write(d, "a.py", 'x = "\u202e"\n')
            _write(d, "b.py", "x = 1\n")
            with mock.patch.object(fe, "run_audit", tampered):
                code, _, err = self.run_cli([d])
            self.assertEqual(code, fe.EXIT_EXPORT_FAILED)
            self.assertIn("99.0.0", err)
            self.assertFalse(ledger_path(d).exists())

    def test_append_failure_exits_3(self):
        with tempfile.TemporaryDirectory() as d:
            _write(d, "a.py", "x = 1\n")
            with mock.patch.object(habl, "append_findings", side_effect=OSError("read-only")):
                code, _, err = self.run_cli([d])
            self.assertEqual(code, fe.EXIT_EXPORT_FAILED)
            self.assertIn("read-only", err)

    def test_whole_run_is_one_batch_append(self):
        with tempfile.TemporaryDirectory() as d:
            _write(d, "a.py", 'x = "\u202e"\n')
            _write(d, "b.py", "x = 1\n")
            with mock.patch.object(habl, "append_findings", wraps=habl.append_findings) as spy:
                self.assertEqual(self.run_cli([d])[0], fe.EXIT_OK)
            self.assertEqual(spy.call_count, 1)
            batch = spy.call_args[0][0]
            self.assertEqual({f.location.file for f in batch}, {"a.py", "b.py"})
            self.assertEqual(len(batch), len(load_ledger(d).findings))

    def test_missing_path_is_usage_error(self):
        self.assertEqual(self.run_cli(["/nonexistent/x"])[0], fe.EXIT_USAGE)


if __name__ == "__main__":
    unittest.main()

# Bismillah ir-Rahman ir-Rahim
