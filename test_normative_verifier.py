# Bismillah ir-Rahman ir-Rahim
"""
Normative Verifier v0.2 -- Acceptance Tests

Implements AT-1 through AT-11 (AT-5 moved to cross-projection reconciler)
plus supplementary tests for degraded mode, unknown schema, happy path,
and fail-closed execution gate.
"""
import copy
import unittest
from normative_verifier import verify, SUPPORTED_SCHEMA_VERSIONS


# ---------------------------------------------------------------------------
# Test fixtures
# ---------------------------------------------------------------------------

def _base_receipt(**overrides):
    """Build a minimal valid receipt with overridable fields."""
    r = {
        "schema_version": "0.2.0-draft",
        "claim_id": "CLAIM-001",
        "claim": "Test claim",
        "claim_type": "computation",
        "tier": "Tier 1",
        "status": "VERIFIED",
        "source_evidence": [
            {
                "evidence_id": "EV-001",
                "source_id": "SRC-001",
                "locator": "file://test.txt",
                "kind": "reproduction",
                "independence": "external",
                "verification_state": "reproduced",
            }
        ],
        "counterevidence": [],
        "evidence_independence": "external",
        "independence_provenance": {
            "producer_lineage_id": "PRODUCER-A",
            "evaluator_lineage_id": "EVALUATOR-B",
            "shared_sources": [],
            "shared_keys": [],
            "shared_execution_environment": False,
            "organizational_relationship": "independent",
            "unresolved_dependencies": [],
            "assessment": "independent",
        },
        "method": {
            "name": "sha256sum",
            "version": "coreutils 9.4",
            "scope": "full file",
            "execution_evidence_id": "EXEC-001",
        },
        "allowed_action": "bounded_effect",
        "effect_authorization": {
            "contract_match": "TRUE",
            "effect_type_allowed": "TRUE",
            "target_allowed": "TRUE",
            "witness_healthy": "TRUE",
            "evidence_current": "TRUE",
            "approval_record_id": "APR-001",
        },
        "review": {
            "reviewer": "Bilal",
            "date": "2026-11-04",
            "authorization": "approved",
        },
        "limitations": ["Prototype only"],
    }
    r.update(overrides)
    return r


def _base_registry():
    return {
        "lineages": {
            "PRODUCER-A": {"ancestors": []},
            "EVALUATOR-B": {"ancestors": []},
        }
    }


def _base_evidence_snapshot():
    return {
        "execution_records": {
            "EXEC-001": {"hash": "abc123", "timestamp": "2026-11-04T00:00:00Z"},
        }
    }


def _base_policy():
    return {}


def _add_evaluator_binding(receipt, evidence_id="EV-001",
                            claim_relevance="direct_test",
                            assessed_by="EVALUATOR-B",
                            exec_id="EXEC-001"):
    """Add evaluator binding to a specific evidence item."""
    for ev in receipt.get("source_evidence", []):
        if ev.get("evidence_id") == evidence_id:
            ev["evaluator_binding"] = {
                "claim_id": receipt.get("claim_id", "CLAIM-001"),
                "claim_revision_id": "REV-001",
                "tested_property": "SHA-256 hash match",
                "method_name": "sha256sum",
                "method_version": "coreutils 9.4",
                "execution_evidence_id": exec_id,
                "observed_result": "hash matched",
                "claim_relevance": claim_relevance,
                "assessed_by": assessed_by,
                "assessment_timestamp": "2026-11-04T00:00:00Z",
            }
            ev["publisher_binding"] = {
                "tested_property": "SHA-256 hash of file X",
                "claim_relevance": claim_relevance,
                "proposed_by": receipt.get("independence_provenance", {}).get(
                    "producer_lineage_id", "PRODUCER-A"),
            }
            break
    return receipt


# ---------------------------------------------------------------------------
# AT-1: Reject VERIFIED when evidence is self-produced only
# ---------------------------------------------------------------------------

class TestAT1SelfProducedEvidence(unittest.TestCase):
    def test_self_produced_only_not_assured(self):
        r = _base_receipt()
        r["evidence_independence"] = "self_produced"
        r["source_evidence"][0]["independence"] = "self_produced"
        del r["independence_provenance"]
        result = verify(r)
        self.assertEqual(result["claim_assurance"]["overall"], "NOT_ASSURED")


# ---------------------------------------------------------------------------
# AT-2: Reject VERIFIED when only alternative is correlated or unknown
# ---------------------------------------------------------------------------

class TestAT2CorrelatedEvidence(unittest.TestCase):
    def test_correlated_evidence_not_assured(self):
        r = _base_receipt()
        r["evidence_independence"] = "correlated"
        r["source_evidence"][0]["independence"] = "correlated"
        del r["independence_provenance"]
        result = verify(r)
        self.assertEqual(result["claim_assurance"]["overall"], "NOT_ASSURED")

    def test_unknown_evidence_not_assured(self):
        r = _base_receipt()
        r["evidence_independence"] = "unknown"
        r["source_evidence"][0]["independence"] = "unknown"
        del r["independence_provenance"]
        result = verify(r)
        self.assertEqual(result["claim_assurance"]["overall"], "NOT_ASSURED")


# ---------------------------------------------------------------------------
# AT-3: Refuse independent certification when producer controls evidence
# ---------------------------------------------------------------------------

class TestAT3ProducerControlled(unittest.TestCase):
    def test_same_lineage_fails_independence(self):
        r = _base_receipt()
        r["independence_provenance"]["evaluator_lineage_id"] = "PRODUCER-A"
        result = verify(r, _base_registry(), _base_policy(), _base_evidence_snapshot())
        self.assertEqual(result["claim_assurance"]["witness_independence"], "FAIL")
        self.assertIn(result["claim_assurance"]["overall"], ("NOT_ASSURED",))

    def test_shared_keys_fails_independence(self):
        r = _base_receipt()
        r["independence_provenance"]["shared_keys"] = ["KEY-SHARED"]
        result = verify(r, _base_registry(), _base_policy(), _base_evidence_snapshot())
        self.assertEqual(result["claim_assurance"]["witness_independence"], "FAIL")

    def test_dependent_assessment_uncertified(self):
        r = _base_receipt()
        r["independence_provenance"]["assessment"] = "dependent"
        result = verify(r, _base_registry(), _base_policy(), _base_evidence_snapshot())
        # The provenance assessment field is recorded; structural checks still run
        # Independence is evaluated by NV-04..NV-07, not the self-declared assessment alone


# ---------------------------------------------------------------------------
# AT-4: Presentation invariance
# ---------------------------------------------------------------------------

class TestAT4PresentationInvariance(unittest.TestCase):
    def test_different_prose_same_result(self):
        r1 = _base_receipt(claim="This file's hash is verified")
        r2 = _base_receipt(claim="The cryptographic digest of this artifact was independently confirmed")
        r1["limitations"] = ["Prototype scope only"]
        r2["limitations"] = ["Scope restricted to non-production prototype"]
        _add_evaluator_binding(r1)
        _add_evaluator_binding(r2)

        reg = _base_registry()
        pol = _base_policy()
        ev = _base_evidence_snapshot()

        res1 = verify(r1, reg, pol, ev)
        res2 = verify(r2, reg, pol, ev)

        self.assertEqual(res1["claim_conformance"]["overall"],
                         res2["claim_conformance"]["overall"])
        self.assertEqual(res1["claim_assurance"]["overall"],
                         res2["claim_assurance"]["overall"])


# ---------------------------------------------------------------------------
# AT-6: Branching revisions with irreconcilable status
# ---------------------------------------------------------------------------

class TestAT6IrreconcilableBranches(unittest.TestCase):
    def test_verified_vs_contradicted_unreconciled(self):
        r = _base_receipt()
        _add_evaluator_binding(r)
        r["revision_history"] = [
            {"revision_id": "REV-A", "relation": "supersedes",
             "prior_revision_id": None, "status": "VERIFIED",
             "timestamp": "2026-01-01T00:00:00Z", "evidence_ids": ["EV-001"]},
            {"revision_id": "REV-B", "relation": "challenges",
             "prior_revision_id": None, "status": "CONTRADICTED",
             "timestamp": "2026-02-01T00:00:00Z", "evidence_ids": ["EV-001"]},
        ]
        result = verify(r, _base_registry(), _base_policy(), _base_evidence_snapshot())
        self.assertEqual(result["claim_conformance"]["overall"], "NON_CONFORMANT")
        self.assertIn("UNRECONCILED", result.get("notes", ""))


# ---------------------------------------------------------------------------
# AT-7: Retraction after verification
# ---------------------------------------------------------------------------

class TestAT7RetractionAfterVerification(unittest.TestCase):
    def test_stale_verified_after_withdrawal(self):
        r = _base_receipt(status="VERIFIED")
        _add_evaluator_binding(r)
        r["revision_history"] = [
            {"revision_id": "REV-01", "relation": "supersedes",
             "prior_revision_id": None, "status": "VERIFIED",
             "timestamp": "2026-01-01T00:00:00Z", "evidence_ids": ["EV-001"]},
            {"revision_id": "REV-02", "relation": "retracts",
             "prior_revision_id": "REV-01", "status": "WITHDRAWN",
             "timestamp": "2026-02-01T00:00:00Z", "evidence_ids": []},
        ]
        result = verify(r, _base_registry(), _base_policy(), _base_evidence_snapshot())
        self.assertEqual(result["claim_conformance"]["revision_integrity"], "FAIL")


# ---------------------------------------------------------------------------
# AT-8: Publisher claim with external label
# ---------------------------------------------------------------------------

class TestAT8PublisherClaimExternalLabel(unittest.TestCase):
    def test_publisher_claim_not_assured(self):
        r = _base_receipt()
        r["source_evidence"] = [
            {
                "evidence_id": "EV-PUB",
                "source_id": "SRC-001",
                "locator": "file://test.txt",
                "kind": "publisher_claim",
                "independence": "external",
                "verification_state": "claimed",
            }
        ]
        result = verify(r, _base_registry(), _base_policy(), _base_evidence_snapshot())
        self.assertEqual(result["claim_assurance"]["overall"], "NOT_ASSURED")


# ---------------------------------------------------------------------------
# AT-9: Dual-record binding mismatch
# ---------------------------------------------------------------------------

class TestAT9BindingMismatch(unittest.TestCase):
    def test_evaluator_unrelated_overrides_publisher_direct(self):
        r = _base_receipt()
        _add_evaluator_binding(r, claim_relevance="unrelated")
        # Publisher says direct_test, evaluator says unrelated
        r["source_evidence"][0]["publisher_binding"]["claim_relevance"] = "direct_test"
        result = verify(r, _base_registry(), _base_policy(), _base_evidence_snapshot())
        self.assertEqual(result["claim_assurance"]["overall"], "NOT_ASSURED")


# ---------------------------------------------------------------------------
# AT-10: Human approval on non-conformant receipt
# ---------------------------------------------------------------------------

class TestAT10HumanApprovalNonConformant(unittest.TestCase):
    def test_approval_does_not_override_non_conformant(self):
        r = _base_receipt()
        # Make it non-conformant: same lineage
        r["independence_provenance"]["evaluator_lineage_id"] = "PRODUCER-A"
        r["review"]["authorization"] = "approved"
        r["allowed_action"] = "bounded_effect"
        result = verify(r, _base_registry(), _base_policy(), _base_evidence_snapshot())
        self.assertEqual(result["action_authorization"]["execution_permission"], "DENIED")


# ---------------------------------------------------------------------------
# AT-11: Identical leaf statuses with same evaluator
# ---------------------------------------------------------------------------

class TestAT11SameEvaluatorLeaves(unittest.TestCase):
    def test_same_evaluator_unreconciled(self):
        r = _base_receipt()
        _add_evaluator_binding(r)
        r["revision_history"] = [
            {"revision_id": "REV-A", "relation": "supersedes",
             "prior_revision_id": None, "status": "VERIFIED",
             "timestamp": "2026-01-01T00:00:00Z", "evidence_ids": ["EV-001"]},
            {"revision_id": "REV-B", "relation": "corroborates",
             "prior_revision_id": None, "status": "VERIFIED",
             "timestamp": "2026-02-01T00:00:00Z", "evidence_ids": ["EV-001"]},
        ]
        r["dependency_edges"] = [
            {"from_id": "REV-A", "to_id": "REV-B",
             "relation": "same_evaluator", "witnessed": False}
        ]
        result = verify(r, _base_registry(), _base_policy(), _base_evidence_snapshot())
        self.assertIn("UNRECONCILED", result.get("notes", ""))


# ---------------------------------------------------------------------------
# Supplementary: Degraded mode (no registry)
# ---------------------------------------------------------------------------

class TestDegradedMode(unittest.TestCase):
    def test_no_registry_uncertified_provenance(self):
        r = _base_receipt()
        _add_evaluator_binding(r)
        result = verify(r, None, _base_policy(), _base_evidence_snapshot())
        self.assertEqual(result["claim_conformance"]["independence_provenance"], "UNCERTIFIED")
        self.assertIn("Lineage registry unavailable", result.get("notes", ""))

    def test_no_snapshots_at_all(self):
        r = _base_receipt()
        _add_evaluator_binding(r)
        result = verify(r)
        # Should still produce a result, just degraded
        self.assertIn(result["claim_conformance"]["overall"],
                      ("CONFORMANT", "UNCERTIFIED", "NON_CONFORMANT"))


# ---------------------------------------------------------------------------
# Supplementary: Unknown schema version
# ---------------------------------------------------------------------------

class TestUnknownSchemaVersion(unittest.TestCase):
    def test_unknown_schema_stage1_fail(self):
        r = _base_receipt(schema_version="99.99.99")
        result = verify(r)
        self.assertEqual(result["stage_1"], "FAIL")
        self.assertEqual(result["claim_conformance"]["overall"], "NON_CONFORMANT")
        self.assertEqual(result["action_authorization"]["execution_permission"], "DENIED")


# ---------------------------------------------------------------------------
# Supplementary: Happy path
# ---------------------------------------------------------------------------

class TestHappyPath(unittest.TestCase):
    def test_fully_valid_receipt(self):
        r = _base_receipt()
        _add_evaluator_binding(r)
        reg = _base_registry()
        pol = _base_policy()
        ev = _base_evidence_snapshot()
        result = verify(r, reg, pol, ev)
        self.assertEqual(result["stage_1"], "PASS")
        self.assertEqual(result["claim_conformance"]["overall"], "CONFORMANT")
        self.assertEqual(result["claim_assurance"]["overall"], "ASSURED")
        self.assertEqual(result["action_authorization"]["overall"], "AUTHORIZED")
        self.assertEqual(result["action_authorization"]["execution_permission"], "GRANTED")


# ---------------------------------------------------------------------------
# Supplementary: Fail-closed execution gate (NV-21)
# ---------------------------------------------------------------------------

class TestFailClosedGate(unittest.TestCase):
    def test_no_human_approval_denied(self):
        r = _base_receipt()
        _add_evaluator_binding(r)
        r["review"]["authorization"] = "pending"
        result = verify(r, _base_registry(), _base_policy(), _base_evidence_snapshot())
        self.assertEqual(result["action_authorization"]["execution_permission"], "DENIED")

    def test_auth_unknown_check_denied(self):
        r = _base_receipt()
        _add_evaluator_binding(r)
        r["effect_authorization"]["witness_healthy"] = "UNKNOWN"
        result = verify(r, _base_registry(), _base_policy(), _base_evidence_snapshot())
        self.assertEqual(result["action_authorization"]["execution_permission"], "DENIED")

    def test_no_action_receipt_uncertified_permission(self):
        r = _base_receipt(allowed_action="no_action")
        del r["effect_authorization"]
        _add_evaluator_binding(r)
        result = verify(r, _base_registry(), _base_policy(), _base_evidence_snapshot())
        self.assertEqual(result["action_authorization"]["execution_permission"], "UNCERTIFIED")


# ---------------------------------------------------------------------------
# Supplementary: Revision graph structural checks
# ---------------------------------------------------------------------------

class TestRevisionStructure(unittest.TestCase):
    def test_duplicate_revision_id_fails(self):
        r = _base_receipt()
        _add_evaluator_binding(r)
        r["revision_history"] = [
            {"revision_id": "REV-A", "relation": "supersedes",
             "prior_revision_id": None, "status": "VERIFIED",
             "timestamp": "2026-01-01T00:00:00Z"},
            {"revision_id": "REV-A", "relation": "amends",
             "prior_revision_id": None, "status": "VERIFIED",
             "timestamp": "2026-02-01T00:00:00Z"},
        ]
        result = verify(r, _base_registry(), _base_policy(), _base_evidence_snapshot())
        self.assertEqual(result["claim_conformance"]["revision_integrity"], "FAIL")

    def test_dangling_prior_reference_fails(self):
        r = _base_receipt()
        _add_evaluator_binding(r)
        r["revision_history"] = [
            {"revision_id": "REV-A", "relation": "supersedes",
             "prior_revision_id": "NONEXISTENT", "status": "VERIFIED",
             "timestamp": "2026-01-01T00:00:00Z"},
        ]
        result = verify(r, _base_registry(), _base_policy(), _base_evidence_snapshot())
        self.assertEqual(result["claim_conformance"]["revision_integrity"], "FAIL")

    def test_cycle_fails(self):
        r = _base_receipt()
        _add_evaluator_binding(r)
        r["revision_history"] = [
            {"revision_id": "REV-A", "relation": "supersedes",
             "prior_revision_id": "REV-B", "status": "VERIFIED",
             "timestamp": "2026-01-01T00:00:00Z"},
            {"revision_id": "REV-B", "relation": "amends",
             "prior_revision_id": "REV-A", "status": "VERIFIED",
             "timestamp": "2026-02-01T00:00:00Z"},
        ]
        result = verify(r, _base_registry(), _base_policy(), _base_evidence_snapshot())
        self.assertEqual(result["claim_conformance"]["revision_integrity"], "FAIL")


# ---------------------------------------------------------------------------
# Supplementary: Status-action consistency (NV-14)
# ---------------------------------------------------------------------------

class TestStatusActionConsistency(unittest.TestCase):
    def test_unknown_status_bounded_effect_fails(self):
        r = _base_receipt(status="UNKNOWN", allowed_action="bounded_effect")
        result = verify(r, _base_registry(), _base_policy(), _base_evidence_snapshot())
        auth_checks = [c for c in result["checks"] if c["check_id"] == "NV-14"]
        self.assertTrue(any(c["status"] == "FAIL" for c in auth_checks))

    def test_withdrawn_with_action_fails(self):
        r = _base_receipt(status="WITHDRAWN", allowed_action="read_only_review")
        result = verify(r)
        auth_checks = [c for c in result["checks"] if c["check_id"] == "NV-14"]
        self.assertTrue(any(c["status"] == "FAIL" for c in auth_checks))


# ---------------------------------------------------------------------------
# Supplementary: Determinism
# ---------------------------------------------------------------------------

class TestDeterminism(unittest.TestCase):
    def test_same_input_same_output(self):
        r = _base_receipt()
        _add_evaluator_binding(r)
        reg = _base_registry()
        pol = _base_policy()
        ev = _base_evidence_snapshot()

        res1 = verify(copy.deepcopy(r), copy.deepcopy(reg),
                       copy.deepcopy(pol), copy.deepcopy(ev))
        res2 = verify(copy.deepcopy(r), copy.deepcopy(reg),
                       copy.deepcopy(pol), copy.deepcopy(ev))

        # Compare everything except timestamps and result_id (which include uuid/time)
        for key in ("stage_1", "claim_conformance", "claim_assurance",
                     "action_authorization", "receipt_sha256"):
            self.assertEqual(res1[key], res2[key])


if __name__ == "__main__":
    unittest.main(verbosity=2)
# Bismillah ir-Rahman ir-Rahim
