# Bismillah ir-Rahman ir-Rahim
"""Tests for Shahid (شَهِيد) -- the weight-holder's testimony.

Tests the report schema, serialization round-trip, validation,
HABL cross-references, and the example report builder.

Runs under pytest or unittest.
"""
# Bismillah ir-Rahman ir-Rahim

import json
import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import shahid  # noqa: E402


class TestReportSubject(unittest.TestCase):
    def test_minimal(self):
        s = shahid.ReportSubject(name="test-model")
        d = s.to_dict()
        self.assertEqual(d["name"], "test-model")
        self.assertEqual(d.get("kind"), "model")

    def test_round_trip(self):
        s = shahid.ReportSubject(
            name="FATIMA", version="2.0", kind="tool", identifier="enc-v2"
        )
        s2 = shahid.ReportSubject.from_dict(s.to_dict())
        self.assertEqual(s.name, s2.name)
        self.assertEqual(s.version, s2.version)
        self.assertEqual(s.kind, s2.kind)
        self.assertEqual(s.identifier, s2.identifier)


class TestInspectionPeriod(unittest.TestCase):
    def test_valid(self):
        p = shahid.InspectionPeriod(
            start="2026-10-01T00:00:00+00:00",
            end="2026-10-31T23:59:59+00:00",
            cadence="monthly",
        )
        d = p.to_dict()
        self.assertEqual(d["cadence"], "monthly")

    def test_bad_timestamp(self):
        with self.assertRaises(ValueError):
            shahid.InspectionPeriod(start="not-a-date", end="2026-10-31T00:00:00+00:00")

    def test_no_timezone(self):
        with self.assertRaises(ValueError):
            shahid.InspectionPeriod(
                start="2026-10-01T00:00:00",
                end="2026-10-31T00:00:00+00:00",
            )

    def test_reversed_period_rejected(self):
        """SH-05 (GPT-6): end before start must be rejected."""
        with self.assertRaises(ValueError) as ctx:
            shahid.InspectionPeriod(
                start="2026-10-31T00:00:00+00:00",
                end="2026-10-01T00:00:00+00:00",
            )
        self.assertIn("precedes", str(ctx.exception))

    def test_same_start_end_accepted(self):
        """SH-05: a zero-length period (start == end) is valid."""
        p = shahid.InspectionPeriod(
            start="2026-10-15T12:00:00+00:00",
            end="2026-10-15T12:00:00+00:00",
        )
        self.assertEqual(p.start, p.end)

    def test_timezone_equivalent_ordering(self):
        """SH-05: end in UTC-5 that is actually after start in UTC."""
        p = shahid.InspectionPeriod(
            start="2026-10-01T00:00:00+00:00",
            end="2026-10-31T00:00:00-05:00",  # Nov 1 UTC
        )
        self.assertIsNotNone(p)


class TestHablReference(unittest.TestCase):
    def test_must_have_at_least_one_id(self):
        with self.assertRaises(ValueError):
            shahid.HablReference()

    def test_finding_id_only(self):
        r = shahid.HablReference(finding_id="abc123")
        d = r.to_dict()
        self.assertEqual(d["finding_id"], "abc123")
        self.assertNotIn("correlation_id", d)

    def test_both_ids(self):
        r = shahid.HablReference(
            finding_id="abc123",
            correlation_id="habl-xyz",
            summary="related finding",
        )
        d = r.to_dict()
        self.assertEqual(d["correlation_id"], "habl-xyz")
        self.assertEqual(d["summary"], "related finding")

    def test_round_trip(self):
        r = shahid.HablReference(
            finding_id="abc123",
            correlation_id="habl-xyz",
            ledger_path=".habl/findings.jsonl",
        )
        r2 = shahid.HablReference.from_dict(r.to_dict())
        self.assertEqual(r.finding_id, r2.finding_id)
        self.assertEqual(r.correlation_id, r2.correlation_id)
        self.assertEqual(r.ledger_path, r2.ledger_path)


class TestInspectedDimension(unittest.TestCase):
    def test_string_coverage_coerced(self):
        d = shahid.InspectedDimension(name="weights", coverage="full")
        self.assertEqual(d.coverage, shahid.InspectionCoverage.FULL)

    def test_empty_name_rejected(self):
        with self.assertRaises(ValueError):
            shahid.InspectedDimension(name="", coverage=shahid.InspectionCoverage.FULL)

    def test_with_findings(self):
        f = shahid.DimensionFinding(
            summary="test finding",
            habl_refs=[shahid.HablReference(finding_id="ref-001")],
        )
        d = shahid.InspectedDimension(
            name="training_data",
            coverage=shahid.InspectionCoverage.SAMPLED,
            method="10% random sample",
            findings=[f],
        )
        out = d.to_dict()
        self.assertEqual(len(out["findings"]), 1)
        self.assertEqual(out["findings"][0]["habl_refs"][0]["finding_id"], "ref-001")

    def test_round_trip(self):
        d = shahid.InspectedDimension(
            name="activations",
            coverage=shahid.InspectionCoverage.PARTIAL,
            method="probing layer 12",
            scope="transformer block 12 only",
            metadata={"layer": 12},
        )
        d2 = shahid.InspectedDimension.from_dict(d.to_dict())
        self.assertEqual(d.name, d2.name)
        self.assertEqual(d.coverage, d2.coverage)
        self.assertEqual(d.method, d2.method)


class TestUninspectedDimension(unittest.TestCase):
    def test_string_reason_coerced(self):
        d = shahid.UninspectedDimension(name="weights", reason="cost")
        self.assertEqual(d.reason, shahid.UninspectedReason.COST)

    def test_empty_name_rejected(self):
        with self.assertRaises(ValueError):
            shahid.UninspectedDimension(name="", reason=shahid.UninspectedReason.COST)


class TestShahidReport(unittest.TestCase):
    def _minimal(self) -> shahid.ShahidReport:
        return shahid.ShahidReport(
            publisher="test-publisher",
            subject=shahid.ReportSubject(name="test-model"),
            period=shahid.InspectionPeriod(
                start="2026-10-01T00:00:00+00:00",
                end="2026-10-31T23:59:59+00:00",
            ),
            inspected=[
                shahid.InspectedDimension(
                    name="weights",
                    coverage=shahid.InspectionCoverage.FULL,
                    method="direct examination",
                ),
            ],
            uninspected=[
                shahid.UninspectedDimension(
                    name="training_data",
                    reason=shahid.UninspectedReason.POLICY,
                    explanation="data license prohibits disclosure",
                ),
            ],
        )

    def test_schema_version(self):
        r = self._minimal()
        self.assertEqual(r.schema_version, shahid.SHAHID_SCHEMA_VERSION)

    def test_unsupported_schema_rejected(self):
        with self.assertRaises(ValueError):
            shahid.ShahidReport(schema_version="99.99.99")

    def test_derived_properties(self):
        r = self._minimal()
        self.assertEqual(r.total_inspected, 1)
        self.assertEqual(r.total_uninspected, 1)
        self.assertEqual(r.total_findings, 0)
        self.assertEqual(r.coverage_summary, {"full": 1})
        self.assertEqual(r.uninspected_reasons, {"policy": 1})

    def test_canonical_coverage(self):
        r = self._minimal()
        cc = r.canonical_coverage
        self.assertEqual(cc["weights"], "inspected:full")
        self.assertEqual(cc["training_data"], "uninspected:policy")
        self.assertEqual(cc["activations"], "absent")

    def test_json_round_trip(self):
        r = self._minimal()
        text = r.to_json()
        parsed = json.loads(text)
        r2 = shahid.ShahidReport.from_json(text)
        self.assertEqual(r.report_id, r2.report_id)
        self.assertEqual(r.publisher, r2.publisher)
        self.assertEqual(r.subject.name, r2.subject.name)
        self.assertEqual(len(r.inspected), len(r2.inspected))
        self.assertEqual(len(r.uninspected), len(r2.uninspected))
        self.assertEqual(r.inspected[0].name, r2.inspected[0].name)
        self.assertEqual(r.uninspected[0].reason, r2.uninspected[0].reason)

    def test_summary_in_serialization(self):
        r = self._minimal()
        d = r.to_dict()
        self.assertIn("summary", d)
        self.assertEqual(d["summary"]["total_inspected"], 1)
        self.assertEqual(d["summary"]["total_uninspected"], 1)

    def test_schema_version_key_in_json(self):
        r = self._minimal()
        d = r.to_dict()
        self.assertIn("shahid_schema_version", d)
        self.assertNotIn("schema_version", d)


class TestValidation(unittest.TestCase):
    def test_empty_report_warnings(self):
        r = shahid.ShahidReport()
        warnings = r.validate()
        self.assertTrue(any("publisher" in w for w in warnings))
        self.assertTrue(any("subject" in w for w in warnings))
        self.assertTrue(any("period" in w for w in warnings))
        self.assertTrue(any("empty" in w for w in warnings))

    def test_claimed_coverage_without_method_is_fine(self):
        r = shahid.ShahidReport(
            publisher="test",
            subject=shahid.ReportSubject(name="m"),
            inspected=[
                shahid.InspectedDimension(
                    name="weights",
                    coverage=shahid.InspectionCoverage.CLAIMED,
                ),
            ],
        )
        warnings = r.validate()
        # CLAIMED without method is the correct usage
        method_warns = [w for w in warnings if "CLAIMED" in w and "method" in w]
        self.assertEqual(len(method_warns), 0)

    def test_claimed_with_method_warns(self):
        r = shahid.ShahidReport(
            publisher="test",
            subject=shahid.ReportSubject(name="m"),
            inspected=[
                shahid.InspectedDimension(
                    name="weights",
                    coverage=shahid.InspectionCoverage.CLAIMED,
                    method="I looked at them",
                ),
            ],
        )
        warnings = r.validate()
        method_warns = [w for w in warnings if "CLAIMED" in w and "method" in w]
        self.assertEqual(len(method_warns), 1)

    def test_non_claimed_without_method_warns(self):
        r = shahid.ShahidReport(
            publisher="test",
            subject=shahid.ReportSubject(name="m"),
            inspected=[
                shahid.InspectedDimension(
                    name="weights",
                    coverage=shahid.InspectionCoverage.FULL,
                    # no method
                ),
            ],
        )
        warnings = r.validate()
        self.assertTrue(any("method is empty" in w for w in warnings))

    def test_duplicate_dimension_warned(self):
        r = shahid.ShahidReport(
            publisher="test",
            subject=shahid.ReportSubject(name="m"),
            inspected=[
                shahid.InspectedDimension(
                    name="weights",
                    coverage=shahid.InspectionCoverage.FULL,
                    method="x",
                ),
                shahid.InspectedDimension(
                    name="weights",
                    coverage=shahid.InspectionCoverage.SAMPLED,
                    method="y",
                ),
            ],
        )
        warnings = r.validate()
        self.assertTrue(any("more than once" in w for w in warnings))

    def test_absent_canonical_warned(self):
        r = shahid.ShahidReport(
            publisher="test",
            subject=shahid.ReportSubject(name="m"),
            inspected=[
                shahid.InspectedDimension(
                    name="weights",
                    coverage=shahid.InspectionCoverage.FULL,
                    method="x",
                ),
            ],
        )
        warnings = r.validate()
        absent_warns = [w for w in warnings if "absent" in w]
        self.assertTrue(len(absent_warns) > 0)
        # The warning should name the missing canonical dimensions
        self.assertTrue(any("training_data" in w for w in absent_warns))


class TestWitnessResilienceRecord(unittest.TestCase):
    def test_empty_instrument_rejected(self):
        with self.assertRaises(ValueError):
            shahid.WitnessResilienceRecord(instrument="")

    def test_string_outcome_coerced(self):
        r = shahid.WitnessResilienceRecord(
            instrument="FATIMA",
            threat_model="test",
            detection_claim="test",
            adversarial_tests="test",
            outcome="demonstrated",
        )
        self.assertEqual(r.outcome, shahid.WitnessOutcome.DEMONSTRATED)

    def test_round_trip(self):
        r = shahid.WitnessResilienceRecord(
            instrument="FATIMA",
            threat_model="attacker modifies file",
            witness_source="sidecar HMAC",
            trust_dependencies="sidecar on same disk",
            detection_claim="SC-003 detects content change",
            adversarial_tests="65 tests pass",  # SH-03: required for DEMONSTRATED
            outcome=shahid.WitnessOutcome.DEMONSTRATED,
        )
        d = r.to_dict()
        r2 = shahid.WitnessResilienceRecord.from_dict(d)
        self.assertEqual(r.instrument, r2.instrument)
        self.assertEqual(r.outcome, r2.outcome)
        self.assertEqual(r.threat_model, r2.threat_model)

    def test_violated_outcome(self):
        r = shahid.WitnessResilienceRecord(
            instrument="SA-006",
            threat_model="attacker copies watermark format",
            outcome=shahid.WitnessOutcome.VIOLATED,
        )
        d = r.to_dict()
        self.assertEqual(d["outcome"], "violated")

    def test_default_outcome_is_unknown(self):
        r = shahid.WitnessResilienceRecord(instrument="HABL")
        self.assertEqual(r.outcome, shahid.WitnessOutcome.UNKNOWN)

    def test_minimal_serialization(self):
        r = shahid.WitnessResilienceRecord(instrument="test")
        d = r.to_dict()
        self.assertEqual(d["instrument"], "test")
        self.assertEqual(d["outcome"], "unknown")
        # Empty strings should not appear
        self.assertNotIn("threat_model", d)


class TestSH02NonMutation(unittest.TestCase):
    """SH-02 (GPT-6): from_dict() must not mutate the caller's dict."""

    def test_dimension_finding_from_dict_does_not_mutate(self):
        d = {
            "finding_id": "test-001",
            "summary": "test",
            "habl_refs": [{"finding_id": "ref-001"}],
        }
        original_keys = set(d.keys())
        shahid.DimensionFinding.from_dict(d)
        self.assertEqual(set(d.keys()), original_keys)
        self.assertIn("habl_refs", d)

    def test_inspected_dimension_from_dict_does_not_mutate(self):
        d = {
            "name": "weights",
            "coverage": "full",
            "findings": [{"finding_id": "f1", "summary": "x"}],
        }
        original_keys = set(d.keys())
        shahid.InspectedDimension.from_dict(d)
        self.assertEqual(set(d.keys()), original_keys)
        self.assertIn("findings", d)


class TestSH03DemonstratedRequiresEvidence(unittest.TestCase):
    """SH-03 (GPT-6): DEMONSTRATED must have evidence fields."""

    def test_demonstrated_without_threat_model_rejected(self):
        with self.assertRaises(ValueError) as ctx:
            shahid.WitnessResilienceRecord(
                instrument="test",
                outcome=shahid.WitnessOutcome.DEMONSTRATED,
                # no threat_model, detection_claim, adversarial_tests
            )
        self.assertIn("threat_model", str(ctx.exception))

    def test_demonstrated_with_all_fields_accepted(self):
        r = shahid.WitnessResilienceRecord(
            instrument="test",
            threat_model="attacker modifies file",
            detection_claim="hash mismatch detected",
            adversarial_tests="3 tampering probes passed",
            outcome=shahid.WitnessOutcome.DEMONSTRATED,
        )
        self.assertEqual(r.outcome, shahid.WitnessOutcome.DEMONSTRATED)

    def test_unknown_without_evidence_accepted(self):
        """UNKNOWN is allowed without evidence -- that is its purpose."""
        r = shahid.WitnessResilienceRecord(
            instrument="test",
            outcome=shahid.WitnessOutcome.UNKNOWN,
        )
        self.assertEqual(r.outcome, shahid.WitnessOutcome.UNKNOWN)

    def test_violated_without_full_evidence_accepted(self):
        """VIOLATED may have partial fields -- the violation is the evidence."""
        r = shahid.WitnessResilienceRecord(
            instrument="test",
            threat_model="attacker forges watermark",
            outcome=shahid.WitnessOutcome.VIOLATED,
        )
        self.assertEqual(r.outcome, shahid.WitnessOutcome.VIOLATED)


class TestReportWithResilience(unittest.TestCase):
    def test_resilience_round_trip(self):
        r = shahid.ShahidReport(
            publisher="test",
            subject=shahid.ReportSubject(name="m"),
            witness_resilience=[
                shahid.WitnessResilienceRecord(
                    instrument="FATIMA",
                    threat_model="content modification",
                    detection_claim="hash mismatch",
                    adversarial_tests="tamper test",
                    outcome=shahid.WitnessOutcome.DEMONSTRATED,
                ),
                shahid.WitnessResilienceRecord(
                    instrument="HABL",
                    outcome=shahid.WitnessOutcome.UNKNOWN,
                ),
            ],
        )
        text = r.to_json()
        r2 = shahid.ShahidReport.from_json(text)
        self.assertEqual(len(r2.witness_resilience), 2)
        self.assertEqual(r2.witness_resilience[0].instrument, "FATIMA")
        self.assertEqual(r2.witness_resilience[0].outcome, shahid.WitnessOutcome.DEMONSTRATED)
        self.assertEqual(r2.witness_resilience[1].instrument, "HABL")

    def test_empty_resilience_not_serialized(self):
        r = shahid.ShahidReport(publisher="test", subject=shahid.ReportSubject(name="m"))
        d = r.to_dict()
        self.assertNotIn("witness_resilience", d)


class TestFileIO(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.d)

    def test_write_and_read(self):
        r = shahid.ShahidReport(
            publisher="test",
            subject=shahid.ReportSubject(name="m", version="1.0"),
            inspected=[
                shahid.InspectedDimension(
                    name="weights",
                    coverage=shahid.InspectionCoverage.FULL,
                    method="direct",
                ),
            ],
        )
        path = shahid.write_report(r, self.d)
        self.assertTrue(path.exists())
        self.assertTrue(str(path).endswith(shahid.REPORT_SUFFIX))

        r2 = shahid.read_report(path)
        self.assertEqual(r.report_id, r2.report_id)
        self.assertEqual(r.publisher, r2.publisher)

    def test_list_reports_empty(self):
        self.assertEqual(shahid.list_reports(self.d), [])

    def test_list_reports_finds_written(self):
        r = shahid.ShahidReport(
            publisher="test",
            subject=shahid.ReportSubject(name="m"),
        )
        shahid.write_report(r, self.d)
        reports = shahid.list_reports(self.d)
        self.assertEqual(len(reports), 1)

    def test_report_path_without_id(self):
        p = shahid.report_path(self.d)
        self.assertTrue(str(p).endswith(shahid.SHAHID_DIR))

    def test_path_traversal_rejected(self):
        """SH-01 (GPT-6): report_id with ../ must be rejected."""
        with self.assertRaises(ValueError):
            shahid.report_path(self.d, report_id="../../etc/passwd")

    def test_slash_in_id_rejected(self):
        """SH-06 (GPT-6): slash in report_id must be rejected, not sanitized."""
        with self.assertRaises(ValueError):
            shahid.report_path(self.d, report_id="a/b")

    def test_question_mark_in_id_rejected(self):
        """SH-06 (GPT-6): special chars must be rejected, not mapped to _."""
        with self.assertRaises(ValueError):
            shahid.report_path(self.d, report_id="a?b")

    def test_valid_id_accepted(self):
        p = shahid.report_path(self.d, report_id="shahid-abc123")
        self.assertTrue(str(p).endswith("shahid-abc123" + shahid.REPORT_SUFFIX))

    def test_write_report_traversal_rejected(self):
        """SH-01 (GPT-6): write_report with malicious ID raises."""
        r = shahid.ShahidReport(
            report_id="../../../tmp/evil",
            publisher="test",
            subject=shahid.ReportSubject(name="m"),
        )
        with self.assertRaises(ValueError):
            shahid.write_report(r, self.d)

    def test_write_report_no_silent_overwrite(self):
        """SH-06 (GPT-6): second write to same ID raises FileExistsError."""
        r = shahid.ShahidReport(
            report_id="shahid-unique-test",
            publisher="test",
            subject=shahid.ReportSubject(name="m"),
        )
        shahid.write_report(r, self.d)
        with self.assertRaises(FileExistsError):
            shahid.write_report(r, self.d)

    def test_write_report_overwrite_explicit(self):
        """SH-06 (GPT-6): overwrite=True allows replacement."""
        r = shahid.ShahidReport(
            report_id="shahid-overwrite-test",
            publisher="test",
            subject=shahid.ReportSubject(name="m"),
        )
        shahid.write_report(r, self.d)
        r2 = shahid.ShahidReport(
            report_id="shahid-overwrite-test",
            publisher="updated",
            subject=shahid.ReportSubject(name="m"),
        )
        path = shahid.write_report(r2, self.d, overwrite=True)
        r3 = shahid.read_report(path)
        self.assertEqual(r3.publisher, "updated")

    def test_empty_report_id_rejected_on_write(self):
        """SH-06: empty report_id must raise on write."""
        r = shahid.ShahidReport(
            report_id="",
            publisher="test",
            subject=shahid.ReportSubject(name="m"),
        )
        with self.assertRaises(ValueError):
            shahid.write_report(r, self.d)

    def test_concurrent_writers_exactly_one_succeeds(self):
        """SH-07 (GPT-6): concurrent exclusive creates -- exactly one wins."""
        import threading

        report_id = "shahid-race-test"
        results = {"success": 0, "exists": 0}
        lock = threading.Lock()
        barrier = threading.Barrier(2)

        def writer(publisher_name):
            r = shahid.ShahidReport(
                report_id=report_id,
                publisher=publisher_name,
                subject=shahid.ReportSubject(name="m"),
            )
            barrier.wait()  # synchronize both writers
            try:
                shahid.write_report(r, self.d)
                with lock:
                    results["success"] += 1
            except FileExistsError:
                with lock:
                    results["exists"] += 1

        t1 = threading.Thread(target=writer, args=("writer-1",))
        t2 = threading.Thread(target=writer, args=("writer-2",))
        t1.start()
        t2.start()
        t1.join()
        t2.join()

        self.assertEqual(results["success"], 1, "exactly one writer should succeed")
        self.assertEqual(results["exists"], 1, "exactly one writer should get FileExistsError")

        # The surviving report is readable
        reports = shahid.list_reports(self.d)
        self.assertEqual(len(reports), 1)
        saved = shahid.read_report(reports[0])
        self.assertIn(saved.publisher, ("writer-1", "writer-2"))

    def test_deterministic_path(self):
        """SH-06 (GPT-6): same ID always produces same path."""
        p1 = shahid.report_path(self.d, report_id="shahid-stable")
        p2 = shahid.report_path(self.d, report_id="shahid-stable")
        self.assertEqual(p1, p2)


class TestExampleReport(unittest.TestCase):
    def test_example_is_valid(self):
        r = shahid.example_report()
        self.assertIsInstance(r, shahid.ShahidReport)
        self.assertTrue(r.publisher)
        self.assertTrue(r.subject.name)
        self.assertIsNotNone(r.period)
        self.assertTrue(len(r.inspected) > 0)
        self.assertTrue(len(r.uninspected) > 0)
        self.assertTrue(r.attestation)

    def test_example_serializes(self):
        r = shahid.example_report()
        text = r.to_json()
        parsed = json.loads(text)
        self.assertIn("shahid_schema_version", parsed)
        self.assertEqual(parsed["shahid_schema_version"], shahid.SHAHID_SCHEMA_VERSION)

    def test_example_round_trips(self):
        r = shahid.example_report()
        r2 = shahid.ShahidReport.from_json(r.to_json())
        self.assertEqual(r.report_id, r2.report_id)
        self.assertEqual(r.subject.name, r2.subject.name)
        self.assertEqual(len(r.inspected), len(r2.inspected))
        self.assertEqual(r.inspected[0].name, r2.inspected[0].name)
        self.assertEqual(r.inspected[0].coverage, r2.inspected[0].coverage)
        self.assertEqual(len(r.inspected[0].findings), len(r2.inspected[0].findings))
        # Witness resilience round-trips
        self.assertEqual(len(r.witness_resilience), len(r2.witness_resilience))
        for orig, rt in zip(r.witness_resilience, r2.witness_resilience):
            self.assertEqual(orig.instrument, rt.instrument)
            self.assertEqual(orig.outcome, rt.outcome)

    def test_example_has_witness_resilience(self):
        """SH-04 (GPT-6): SA-006 format recognition is DEMONSTRATED,
        watermark origin authentication is UNKNOWN (B2 not implemented)."""
        r = shahid.example_report()
        self.assertTrue(len(r.witness_resilience) >= 4)
        instruments = [wr.instrument for wr in r.witness_resilience]
        self.assertIn("FATIMA", instruments)
        self.assertIn("HABL", instruments)
        # FATIMA content detection is demonstrated
        fatima = next(wr for wr in r.witness_resilience if wr.instrument == "FATIMA")
        self.assertEqual(fatima.outcome, shahid.WitnessOutcome.DEMONSTRATED)
        # SA-006 format recognition is demonstrated (it does what it claims)
        sa006_fmt = next(wr for wr in r.witness_resilience if "format recognition" in wr.instrument)
        self.assertEqual(sa006_fmt.outcome, shahid.WitnessOutcome.DEMONSTRATED)
        # Watermark origin authentication is unknown (B2 not implemented)
        auth = next(wr for wr in r.witness_resilience if "origin authentication" in wr.instrument)
        self.assertEqual(auth.outcome, shahid.WitnessOutcome.UNKNOWN)
        # HABL external tampering is unknown
        habl = next(wr for wr in r.witness_resilience if wr.instrument == "HABL")
        self.assertEqual(habl.outcome, shahid.WitnessOutcome.UNKNOWN)

    def test_example_validates_with_acceptable_warnings(self):
        r = shahid.example_report()
        warnings = r.validate()
        # Custom dimensions (not in CANONICAL_DIMENSIONS) cause absent
        # warnings -- those are expected for a tool (not a model)
        for w in warnings:
            # No critical structural issues
            self.assertNotIn("publisher is empty", w)
            self.assertNotIn("subject.name is empty", w)
            self.assertNotIn("report is empty", w)


class TestConstants(unittest.TestCase):
    def test_canonical_dimensions_are_strings(self):
        for dim in shahid.CANONICAL_DIMENSIONS:
            self.assertIsInstance(dim, str)
            self.assertTrue(dim)

    def test_coverage_levels(self):
        levels = {e.value for e in shahid.InspectionCoverage}
        self.assertIn("full", levels)
        self.assertIn("sampled", levels)
        self.assertIn("claimed", levels)

    def test_uninspected_reasons(self):
        reasons = {e.value for e in shahid.UninspectedReason}
        self.assertIn("cost", reasons)
        self.assertIn("policy", reasons)
        self.assertIn("deferred", reasons)
        self.assertIn("not_applicable", reasons)

    def test_witness_outcomes(self):
        outcomes = {e.value for e in shahid.WitnessOutcome}
        self.assertIn("demonstrated", outcomes)
        self.assertIn("violated", outcomes)
        self.assertIn("unknown", outcomes)
        self.assertIn("not_applicable", outcomes)

    def test_not_evaluated_outcome(self):
        """R2 (Design Brief v2.1): NOT_EVALUATED must exist."""
        self.assertIn("not_evaluated", {e.value for e in shahid.WitnessOutcome})
        r = shahid.WitnessResilienceRecord(
            instrument="test", outcome=shahid.WitnessOutcome.NOT_EVALUATED)
        self.assertEqual(r.outcome, shahid.WitnessOutcome.NOT_EVALUATED)
        d = r.to_dict()
        self.assertEqual(d["outcome"], "not_evaluated")

    def test_evidence_lanes_constant(self):
        """R1 (Design Brief v2.1): five evidence lanes exist."""
        self.assertEqual(shahid.EVIDENCE_LANES, frozenset({"SRC", "CODE", "MEAS", "PLAN", "HYP"}))


class TestEvidenceLane(unittest.TestCase):
    """R1 (Design Brief v2.1): DimensionFinding evidence_lane field."""

    def test_valid_lane_accepted(self):
        f = shahid.DimensionFinding(summary="test", evidence_lane="CODE")
        self.assertEqual(f.evidence_lane, "CODE")

    def test_invalid_lane_rejected(self):
        with self.assertRaises(ValueError):
            shahid.DimensionFinding(summary="test", evidence_lane="INVALID")

    def test_empty_lane_accepted(self):
        """Empty lane is valid -- optional field."""
        f = shahid.DimensionFinding(summary="test")
        self.assertEqual(f.evidence_lane, "")

    def test_lane_serialized(self):
        f = shahid.DimensionFinding(summary="test", evidence_lane="MEAS")
        d = f.to_dict()
        self.assertEqual(d["evidence_lane"], "MEAS")

    def test_empty_lane_not_serialized(self):
        f = shahid.DimensionFinding(summary="test")
        d = f.to_dict()
        self.assertNotIn("evidence_lane", d)

    def test_all_five_lanes(self):
        for lane in ("SRC", "CODE", "MEAS", "PLAN", "HYP"):
            f = shahid.DimensionFinding(summary="test", evidence_lane=lane)
            self.assertEqual(f.evidence_lane, lane)


class TestSH08ConcurrentOverwrite(unittest.TestCase):
    """SH-08 (GPT-6): concurrent overwrites must not collide on temp files."""

    def setUp(self):
        self.d = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.d)

    def test_concurrent_overwrites_both_succeed(self):
        """Two concurrent overwrite=True writers should not raise."""
        import threading

        report_id = "shahid-overwrite-race"
        # Create initial report
        r0 = shahid.ShahidReport(
            report_id=report_id, publisher="initial",
            subject=shahid.ReportSubject(name="m"))
        shahid.write_report(r0, self.d)

        results = {"success": 0, "error": 0}
        errors = []
        lock = threading.Lock()
        barrier = threading.Barrier(2)

        def writer(pub):
            r = shahid.ShahidReport(
                report_id=report_id, publisher=pub,
                subject=shahid.ReportSubject(name="m"))
            barrier.wait()
            try:
                shahid.write_report(r, self.d, overwrite=True)
                with lock:
                    results["success"] += 1
            except Exception as e:
                with lock:
                    results["error"] += 1
                    errors.append(str(e))

        t1 = threading.Thread(target=writer, args=("A",))
        t2 = threading.Thread(target=writer, args=("B",))
        t1.start(); t2.start()
        t1.join(); t2.join()

        # Both should succeed -- unique temp files prevent collision
        self.assertEqual(results["error"], 0,
                         f"Concurrent overwrites should not error: {errors}")
        self.assertEqual(results["success"], 2)

        # File should exist and be readable (last writer wins)
        saved = shahid.read_report(
            shahid.report_path(self.d, report_id))
        self.assertIn(saved.publisher, ("A", "B"))


if __name__ == "__main__":
    unittest.main()

# Bismillah ir-Rahman ir-Rahim
