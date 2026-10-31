# Bismillah ir-Rahman ir-Rahim
"""
Negative and positive conformance tests for Evidence Receipt v0.2.
Tests CR-01 through CR-04 from GPT-6 cross-vendor review.

Run: python -I docs/corpus2/Bismillah_test_evidence_receipt_v0_2_Bismillah.py
"""

import json
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Attempt to import jsonschema; install if missing
# ---------------------------------------------------------------------------
try:
    import jsonschema
    from jsonschema import validate, ValidationError
except ImportError:
    import subprocess
    subprocess.check_call(
        [sys.executable, "-m", "pip", "install", "--break-system-packages",
         "jsonschema"],
        stdout=subprocess.DEVNULL
    )
    import jsonschema
    from jsonschema import validate, ValidationError


SCHEMA_PATH = Path(__file__).parent / "Bismillah_EESS_Claim_Receipt_v0_2_DRAFT.schema.json"


def load_schema():
    with open(SCHEMA_PATH) as f:
        return json.load(f)


def make_base_receipt(**overrides):
    """Return a minimal valid PROVISIONAL receipt, then apply overrides."""
    receipt = {
        "schema_version": "0.2.0-draft",
        "claim_id": "TEST-001",
        "claim": "Test claim for validation",
        "claim_type": "observation",
        "tier": "Tier 3",
        "status": "PROVISIONAL",
        "source_evidence": [],
        "evidence_independence": "unknown",
        "method": {
            "name": "test-method",
            "version": "0.1",
            "scope": "unit test"
        },
        "allowed_action": "no_action",
        "review": {
            "reviewer": "test-reviewer",
            "date": "2026-10-31",
            "authorization": "not_authorized"
        },
        "limitations": ["test only"]
    }
    receipt.update(overrides)
    return receipt


def self_produced_evidence():
    """Evidence item that is self-produced, claimed, publisher_claim."""
    return {
        "evidence_id": "SELF-01",
        "source_id": "PRODUCER-01",
        "locator": "self-produced test",
        "kind": "publisher_claim",
        "independence": "self_produced",
        "verification_state": "claimed"
    }


def external_reproduced_evidence():
    """Evidence item that is external, reproduced -- genuinely independent."""
    return {
        "evidence_id": "EXT-01",
        "source_id": "INDEPENDENT-LAB-01",
        "locator": "independent reproduction",
        "kind": "reproduction",
        "independence": "external",
        "verification_state": "reproduced"
    }


def correlated_claimed_evidence():
    """Evidence that is correlated and only claimed -- not independent."""
    return {
        "evidence_id": "CORR-01",
        "source_id": "CORRELATED-SRC-01",
        "locator": "correlated source",
        "kind": "witness_attestation",
        "independence": "correlated",
        "verification_state": "claimed"
    }


def unknown_claimed_evidence():
    """Evidence with unknown independence -- not proven independent."""
    return {
        "evidence_id": "UNK-01",
        "source_id": "UNKNOWN-SRC-01",
        "locator": "unknown independence",
        "kind": "witness_attestation",
        "independence": "unknown",
        "verification_state": "claimed"
    }


# ---- Test infrastructure ----

passed = 0
failed = 0
errors = []


def expect_valid(name, receipt, schema):
    global passed, failed
    try:
        validate(instance=receipt, schema=schema)
        passed += 1
        print(f"  PASS: {name}")
    except ValidationError as e:
        failed += 1
        msg = f"  FAIL: {name} -- expected valid but got: {e.message}"
        print(msg)
        errors.append(msg)


def expect_invalid(name, receipt, schema):
    global passed, failed
    try:
        validate(instance=receipt, schema=schema)
        failed += 1
        msg = f"  FAIL: {name} -- expected invalid but schema accepted it"
        print(msg)
        errors.append(msg)
    except ValidationError:
        passed += 1
        print(f"  PASS: {name}")


# ---- Tests ----

def test_cr01_verified_self_produced_rejected(schema):
    """CR-01: VERIFIED with only self-produced publisher_claim must be rejected."""
    receipt = make_base_receipt(
        status="VERIFIED",
        source_evidence=[self_produced_evidence()],
        evidence_independence="self_produced",
        review={
            "reviewer": "producer",
            "date": "2026-10-31",
            "authorization": "not_authorized"
        }
    )
    expect_invalid("CR-01: VERIFIED + self_produced + claimed + not_authorized", receipt, schema)


def test_cr01_verified_self_produced_authorized_rejected(schema):
    """CR-01: VERIFIED with self-produced evidence is rejected even if authorized."""
    receipt = make_base_receipt(
        status="VERIFIED",
        source_evidence=[self_produced_evidence()],
        evidence_independence="self_produced",
        review={
            "reviewer": "producer",
            "date": "2026-10-31",
            "authorization": "approved"
        }
    )
    expect_invalid("CR-01: VERIFIED + self_produced even with approved review", receipt, schema)


def test_cr01_verified_correlated_rejected(schema):
    """CR-01: VERIFIED with only correlated claimed evidence must be rejected."""
    receipt = make_base_receipt(
        status="VERIFIED",
        source_evidence=[correlated_claimed_evidence()],
        evidence_independence="correlated",
        review={
            "reviewer": "correlated-reviewer",
            "date": "2026-10-31",
            "authorization": "approved"
        }
    )
    expect_invalid("CR-01: VERIFIED + correlated + claimed", receipt, schema)


def test_cr01_verified_unknown_rejected(schema):
    """CR-01: VERIFIED with only unknown-independence claimed evidence rejected."""
    receipt = make_base_receipt(
        status="VERIFIED",
        source_evidence=[unknown_claimed_evidence()],
        evidence_independence="unknown",
        review={
            "reviewer": "unknown-reviewer",
            "date": "2026-10-31",
            "authorization": "approved"
        }
    )
    expect_invalid("CR-01: VERIFIED + unknown + claimed", receipt, schema)


def test_cr01_verified_external_reproduced_accepted(schema):
    """CR-01 positive: VERIFIED with external reproduced evidence + authorized review."""
    receipt = make_base_receipt(
        status="VERIFIED",
        source_evidence=[external_reproduced_evidence()],
        evidence_independence="external",
        review={
            "reviewer": "independent-lab",
            "date": "2026-10-31",
            "authorization": "approved"
        }
    )
    expect_valid("CR-01 positive: VERIFIED + external + reproduced + approved", receipt, schema)


def test_cr01_verified_external_observed_accepted(schema):
    """CR-01 positive: VERIFIED with external observed evidence is accepted."""
    evidence = external_reproduced_evidence()
    evidence["verification_state"] = "observed"
    receipt = make_base_receipt(
        status="VERIFIED",
        source_evidence=[evidence],
        evidence_independence="external",
        review={
            "reviewer": "independent-observer",
            "date": "2026-10-31",
            "authorization": "approved"
        }
    )
    expect_valid("CR-01 positive: VERIFIED + external + observed + approved", receipt, schema)


def test_cr01_verified_mixed_with_one_external(schema):
    """CR-01 positive: VERIFIED with mixed evidence including one external reproduced."""
    receipt = make_base_receipt(
        status="VERIFIED",
        source_evidence=[
            self_produced_evidence(),
            external_reproduced_evidence()
        ],
        evidence_independence="mixed",
        review={
            "reviewer": "mixed-review",
            "date": "2026-10-31",
            "authorization": "approved"
        }
    )
    expect_valid("CR-01 positive: VERIFIED + mixed with one external reproduced", receipt, schema)


def test_cr01_verified_not_authorized_rejected(schema):
    """CR-01: VERIFIED with external evidence but not_authorized review rejected."""
    receipt = make_base_receipt(
        status="VERIFIED",
        source_evidence=[external_reproduced_evidence()],
        evidence_independence="external",
        review={
            "reviewer": "unauthorized",
            "date": "2026-10-31",
            "authorization": "not_authorized"
        }
    )
    expect_invalid("CR-01: VERIFIED + external + reproduced but not_authorized", receipt, schema)


def test_cr02_verified_no_action(schema):
    """CR-02: A VERIFIED claim can have no_action -- truth does not imply authorization."""
    receipt = make_base_receipt(
        status="VERIFIED",
        source_evidence=[external_reproduced_evidence()],
        evidence_independence="external",
        allowed_action="no_action",
        review={
            "reviewer": "independent-lab",
            "date": "2026-10-31",
            "authorization": "approved"
        }
    )
    expect_valid("CR-02: VERIFIED + no_action (truth != authorization)", receipt, schema)


def test_cr02_provisional_read_only(schema):
    """CR-02: A PROVISIONAL claim can have read_only_review -- separate gates."""
    receipt = make_base_receipt(
        status="PROVISIONAL",
        source_evidence=[self_produced_evidence()],
        evidence_independence="self_produced",
        allowed_action="read_only_review"
    )
    expect_valid("CR-02: PROVISIONAL + read_only_review (separate gates)", receipt, schema)


def test_cr04_revision_with_typed_relations(schema):
    """CR-04: Revision history supports typed relations and branching."""
    receipt = make_base_receipt(
        status="CONTRADICTED",
        source_evidence=[external_reproduced_evidence()],
        evidence_independence="external",
        revision_history=[
            {
                "revision_id": "REV-001",
                "relation": "supersedes",
                "prior_revision_id": None,
                "status": "PROVISIONAL",
                "timestamp": "2026-10-01T00:00:00Z",
                "reason": "Initial submission"
            },
            {
                "revision_id": "REV-002",
                "relation": "challenges",
                "prior_revision_id": "REV-001",
                "status": "CONTRADICTED",
                "timestamp": "2026-10-15T00:00:00Z",
                "reason": "Independent reproduction failed",
                "evidence_ids": ["EXT-01"]
            },
            {
                "revision_id": "REV-003",
                "relation": "corroborates",
                "prior_revision_id": "REV-001",
                "status": "PROVISIONAL",
                "timestamp": "2026-10-16T00:00:00Z",
                "reason": "Second lab partially reproduces -- branching revision"
            }
        ],
        review={
            "reviewer": "revision-reviewer",
            "date": "2026-10-31",
            "authorization": "pending"
        }
    )
    expect_valid("CR-04: Branching revision history with typed relations", receipt, schema)


def test_provisional_empty_evidence_accepted(schema):
    """Baseline: PROVISIONAL with empty evidence is valid."""
    receipt = make_base_receipt(status="PROVISIONAL")
    expect_valid("Baseline: PROVISIONAL + empty evidence", receipt, schema)


def test_unknown_empty_evidence_accepted(schema):
    """Baseline: UNKNOWN with empty evidence is valid."""
    receipt = make_base_receipt(status="UNKNOWN")
    expect_valid("Baseline: UNKNOWN + empty evidence", receipt, schema)


def test_structural_blind_spots(schema):
    """A7: structural_blind_spots field is accepted."""
    receipt = make_base_receipt(
        structural_blind_spots=[
            "Cannot verify semantic correctness of Arabic root attestations",
            "Verification frame does not cover temporal relationships"
        ]
    )
    expect_valid("A7: structural_blind_spots accepted", receipt, schema)


def test_independence_provenance(schema):
    """CR-03: independence_provenance field is accepted."""
    receipt = make_base_receipt(
        independence_provenance={
            "producer_lineage_id": "claude-opus-4.6-session-abc",
            "evaluator_lineage_id": "gpt-6-session-xyz",
            "shared_sources": [],
            "shared_keys": [],
            "shared_execution_environment": False,
            "organizational_relationship": "independent",
            "unresolved_dependencies": [],
            "assessment": "independent"
        }
    )
    expect_valid("CR-03: independence_provenance accepted", receipt, schema)


def test_independence_provenance_unresolved(schema):
    """CR-03: Unresolved dependencies are recorded honestly."""
    receipt = make_base_receipt(
        independence_provenance={
            "producer_lineage_id": "system-a",
            "evaluator_lineage_id": "system-b",
            "shared_sources": ["common-training-corpus-v1"],
            "shared_keys": [],
            "shared_execution_environment": False,
            "organizational_relationship": "unknown",
            "unresolved_dependencies": [
                "Cannot determine if evaluator used same training data"
            ],
            "assessment": "unresolved"
        }
    )
    expect_valid("CR-03: Unresolved independence provenance accepted", receipt, schema)


# ---- Main ----

def main():
    global passed, failed

    schema = load_schema()
    print(f"Loaded schema: {SCHEMA_PATH.name}\n")

    print("--- CR-01: VERIFIED requires independent evidence ---")
    test_cr01_verified_self_produced_rejected(schema)
    test_cr01_verified_self_produced_authorized_rejected(schema)
    test_cr01_verified_correlated_rejected(schema)
    test_cr01_verified_unknown_rejected(schema)
    test_cr01_verified_external_reproduced_accepted(schema)
    test_cr01_verified_external_observed_accepted(schema)
    test_cr01_verified_mixed_with_one_external(schema)
    test_cr01_verified_not_authorized_rejected(schema)

    print("\n--- CR-02: Verification and authorization are separate ---")
    test_cr02_verified_no_action(schema)
    test_cr02_provisional_read_only(schema)

    print("\n--- CR-03: Independence provenance ---")
    test_independence_provenance(schema)
    test_independence_provenance_unresolved(schema)

    print("\n--- CR-04: Revision history with typed relations ---")
    test_cr04_revision_with_typed_relations(schema)

    print("\n--- Baselines and A7 ---")
    test_provisional_empty_evidence_accepted(schema)
    test_unknown_empty_evidence_accepted(schema)
    test_structural_blind_spots(schema)

    print(f"\n{'='*60}")
    print(f"Results: {passed} passed, {failed} failed, {passed + failed} total")

    if errors:
        print("\nFailures:")
        for e in errors:
            print(f"  {e}")

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())

# Bismillah ir-Rahman ir-Rahim
