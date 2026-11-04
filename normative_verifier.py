# Bismillah ir-Rahman ir-Rahim
"""
EESS Evidence Receipt Normative Verifier v0.2

Stage 2 verification: checks whether lineage, evidence, revisions, and
authorization are actually supported -- beyond Stage 1 structural well-formedness.

21 checks (NV-01 through NV-21) across five categories:
  1. Evidence eligibility (NV-01..NV-03)
  2. Independence provenance (NV-04..NV-07)
  3. Evidence-to-claim relevance (NV-18..NV-20)
  4. Revision integrity (NV-08..NV-13)
  5. Authorization consistency (NV-14..NV-17, NV-21)

Three independent decision levels:
  - CONFORMANT / NON_CONFORMANT / UNCERTIFIED
  - ASSURED / NOT_ASSURED / UNCERTIFIED
  - AUTHORIZED / NOT_AUTHORIZED / UNCERTIFIED

Pure function. Deterministic. Side-effect-free. Presentation-invariant per A8.

NOTE: Receipt SHA-256 uses json.dumps(sort_keys=True, separators=(',',':'))
as an approximation of RFC 8785 JCS. A full JCS implementation would require
a dedicated library for number formatting and Unicode escaping.

NON-AUTHORIZING DESIGN SPECIFICATION.
"""

import copy
import hashlib
import json
import uuid
from datetime import datetime, timezone


SUPPORTED_SCHEMA_VERSIONS = ["0.2.0-draft"]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _canonical_hash(obj: dict) -> str:
    """Approximate RFC 8785 JCS canonical hash via sorted JSON."""
    canonical = json.dumps(obj, sort_keys=True, separators=(",", ":"),
                           ensure_ascii=True)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def _snapshot_hash(snapshot: dict | None) -> str:
    if snapshot is None:
        return ""
    return _canonical_hash(snapshot)


def _check(check_id: str, status: str, detail: str) -> dict:
    return {"check_id": check_id, "status": status, "detail": detail}


def _aggregate(results: list[str]) -> str:
    """Aggregate sub-check results. FAIL > UNCERTIFIED > PASS."""
    if "FAIL" in results:
        return "FAIL"
    if "UNCERTIFIED" in results:
        return "UNCERTIFIED"
    return "PASS"


# ---------------------------------------------------------------------------
# Check 1: Evidence Eligibility (NV-01 through NV-03)
# ---------------------------------------------------------------------------

def _check_evidence_eligibility(receipt: dict, evidence_snapshot: dict | None) -> tuple[str, list[dict]]:
    checks = []
    sub_results = []
    evidence_items = receipt.get("source_evidence", [])

    # NV-01: External independence label must be backed by provenance
    prov = receipt.get("independence_provenance")
    for ev in evidence_items:
        if ev.get("independence") == "external":
            if not prov or not prov.get("producer_lineage_id") or not prov.get("evaluator_lineage_id") or not prov.get("assessment"):
                checks.append(_check("NV-01", "FAIL",
                    f"Evidence {ev.get('evidence_id','')} declares external independence "
                    f"but receipt lacks supporting independence_provenance"))
                sub_results.append("FAIL")
            else:
                checks.append(_check("NV-01", "PASS",
                    f"Evidence {ev.get('evidence_id','')} external label backed by provenance"))
                sub_results.append("PASS")

    # NV-02: Reproduced evidence must have method details + retrievable execution record
    for ev in evidence_items:
        if ev.get("verification_state") == "reproduced":
            method = receipt.get("method", {})
            missing = []
            if not method.get("name"):
                missing.append("method.name")
            if not method.get("version"):
                missing.append("method.version")
            if not method.get("scope"):
                missing.append("method.scope")
            exec_id = method.get("execution_evidence_id")
            if missing:
                checks.append(_check("NV-02", "FAIL",
                    f"Evidence {ev.get('evidence_id','')} reproduced but missing: {', '.join(missing)}"))
                sub_results.append("FAIL")
            elif exec_id and evidence_snapshot is not None:
                if exec_id not in evidence_snapshot.get("execution_records", {}):
                    checks.append(_check("NV-02", "UNCERTIFIED",
                        f"Evidence {ev.get('evidence_id','')} execution_evidence_id "
                        f"'{exec_id}' not found in evidence snapshot"))
                    sub_results.append("UNCERTIFIED")
                else:
                    checks.append(_check("NV-02", "PASS",
                        f"Evidence {ev.get('evidence_id','')} reproduced with valid method and execution record"))
                    sub_results.append("PASS")
            elif exec_id and evidence_snapshot is None:
                checks.append(_check("NV-02", "UNCERTIFIED",
                    f"Evidence {ev.get('evidence_id','')} execution_evidence_id present but no evidence snapshot"))
                sub_results.append("UNCERTIFIED")
            else:
                checks.append(_check("NV-02", "PASS",
                    f"Evidence {ev.get('evidence_id','')} reproduced with valid method"))
                sub_results.append("PASS")

    # NV-03: publisher_claim carries no weight toward ASSURED
    for ev in evidence_items:
        if ev.get("kind") == "publisher_claim":
            checks.append(_check("NV-03", "PASS",
                f"Evidence {ev.get('evidence_id','')} is publisher_claim -- diagnostic only, no ASSURED weight"))
            sub_results.append("PASS")

    if not sub_results:
        checks.append(_check("NV-01", "PASS", "No evidence items to check"))
        sub_results.append("PASS")

    return _aggregate(sub_results), checks


# ---------------------------------------------------------------------------
# Check 2: Independence Provenance (NV-04 through NV-07)
# ---------------------------------------------------------------------------

def _check_independence_provenance(receipt: dict, registry_snapshot: dict | None,
                                    policy_snapshot: dict | None) -> tuple[str, list[dict]]:
    checks = []
    sub_results = []
    prov = receipt.get("independence_provenance")
    independence = receipt.get("evidence_independence", "unknown")

    if independence != "external":
        checks.append(_check("NV-04", "PASS", "Independence is not external -- provenance checks skipped"))
        return "PASS", checks

    # NV-04: External requires populated provenance
    if not prov:
        checks.append(_check("NV-04", "FAIL",
            "evidence_independence is external but independence_provenance is absent"))
        return "FAIL", checks

    producer = prov.get("producer_lineage_id", "")
    evaluator = prov.get("evaluator_lineage_id", "")
    assessment = prov.get("assessment", "")

    if not producer or not evaluator or not assessment:
        checks.append(_check("NV-04", "FAIL",
            f"independence_provenance missing required fields: "
            f"producer={bool(producer)}, evaluator={bool(evaluator)}, assessment={bool(assessment)}"))
        sub_results.append("FAIL")
    else:
        checks.append(_check("NV-04", "PASS", "independence_provenance has required fields"))
        sub_results.append("PASS")

    # NV-05: Lineage comparison
    if producer and evaluator:
        if producer == evaluator:
            checks.append(_check("NV-05", "FAIL",
                f"producer_lineage_id == evaluator_lineage_id: '{producer}'"))
            sub_results.append("FAIL")
        elif registry_snapshot is not None:
            lineages = registry_snapshot.get("lineages", {})
            producer_ancestors = set(lineages.get(producer, {}).get("ancestors", []))
            evaluator_ancestors = set(lineages.get(evaluator, {}).get("ancestors", []))
            if producer in evaluator_ancestors or evaluator in producer_ancestors:
                checks.append(_check("NV-05", "FAIL",
                    f"Transitive ancestry between producer '{producer}' and evaluator '{evaluator}'"))
                sub_results.append("FAIL")
            else:
                checks.append(_check("NV-05", "PASS", "Lineages are independent"))
                sub_results.append("PASS")
        else:
            checks.append(_check("NV-05", "UNCERTIFIED",
                "Lineage registry unavailable -- cannot verify transitive independence"))
            sub_results.append("UNCERTIFIED")

    # NV-06: Shared dependency analysis
    shared_sources = prov.get("shared_sources", [])
    shared_keys = prov.get("shared_keys", [])
    shared_env = prov.get("shared_execution_environment", False)
    org_rel = prov.get("organizational_relationship", "unknown")

    if shared_keys:
        checks.append(_check("NV-06", "FAIL",
            f"Shared signing keys negate independence: {shared_keys}"))
        sub_results.append("FAIL")
    if shared_sources:
        # Check policy snapshot for documented assessment
        has_policy_clearance = False
        if policy_snapshot:
            clearances = policy_snapshot.get("shared_source_clearances", {})
            claim_id = receipt.get("claim_id", "")
            for src in shared_sources:
                if clearances.get(src, {}).get("claim_id") == claim_id:
                    has_policy_clearance = True
        if has_policy_clearance:
            checks.append(_check("NV-06", "PASS",
                "Shared sources cleared by policy for this claim"))
            sub_results.append("PASS")
        else:
            checks.append(_check("NV-06", "UNCERTIFIED",
                f"Shared sources without policy clearance: {shared_sources}"))
            sub_results.append("UNCERTIFIED")
    if shared_env:
        checks.append(_check("NV-06", "UNCERTIFIED",
            "Shared execution environment -- isolation-dependent claims at risk"))
        sub_results.append("UNCERTIFIED")
    if org_rel in ("same_organization", "subsidiary"):
        has_sod = False
        if policy_snapshot:
            sod = policy_snapshot.get("separation_of_duties", {})
            if sod.get(receipt.get("claim_id", "")):
                has_sod = True
        if has_sod:
            checks.append(_check("NV-06", "PASS",
                f"Organizational relationship '{org_rel}' with separation-of-duties documentation"))
            sub_results.append("PASS")
        else:
            checks.append(_check("NV-06", "UNCERTIFIED",
                f"Organizational relationship '{org_rel}' without separation-of-duties documentation"))
            sub_results.append("UNCERTIFIED")

    # NV-07: Unresolved dependencies
    unresolved = prov.get("unresolved_dependencies", [])
    if unresolved:
        checks.append(_check("NV-07", "UNCERTIFIED",
            f"Unresolved dependencies: {unresolved}"))
        sub_results.append("UNCERTIFIED")

    if not sub_results:
        sub_results.append("PASS")

    return _aggregate(sub_results), checks


# ---------------------------------------------------------------------------
# Check 3: Evidence-to-Claim Relevance (NV-18 through NV-20)
# ---------------------------------------------------------------------------

def _check_evidence_relevance(receipt: dict, evidence_snapshot: dict | None,
                               policy_snapshot: dict | None) -> tuple[str, list[dict]]:
    checks = []
    sub_results = []
    evidence_items = receipt.get("source_evidence", [])
    producer_lineage = ""
    prov = receipt.get("independence_provenance")
    if prov:
        producer_lineage = prov.get("producer_lineage_id", "")

    claim_id = receipt.get("claim_id", "")

    has_relevant_binding = False

    for ev in evidence_items:
        # NV-03: publisher_claim is diagnostic, skip for ASSURED
        if ev.get("kind") == "publisher_claim":
            continue

        # NV-18: Dual-record binding
        publisher_binding = ev.get("publisher_binding")
        evaluator_binding = ev.get("evaluator_binding")

        if evaluator_binding:
            assessed_relevance = evaluator_binding.get("claim_relevance", "unrelated")
            assessed_by = evaluator_binding.get("assessed_by", "")
            exec_id = evaluator_binding.get("execution_evidence_id", "")
            bound_claim_id = evaluator_binding.get("claim_id", "")

            # NV-19: Check for relevant binding
            if assessed_relevance in ("direct_test", "supporting"):
                if assessed_by and assessed_by != producer_lineage:
                    if bound_claim_id == claim_id or not bound_claim_id:
                        if exec_id and evidence_snapshot is not None:
                            if exec_id in evidence_snapshot.get("execution_records", {}):
                                has_relevant_binding = True
                            else:
                                checks.append(_check("NV-19", "UNCERTIFIED",
                                    f"Evidence {ev.get('evidence_id','')} execution record "
                                    f"'{exec_id}' not in snapshot"))
                                sub_results.append("UNCERTIFIED")
                        elif exec_id and evidence_snapshot is None:
                            checks.append(_check("NV-19", "UNCERTIFIED",
                                f"Evidence {ev.get('evidence_id','')} has execution_evidence_id "
                                f"but no evidence snapshot"))
                            sub_results.append("UNCERTIFIED")
                        else:
                            has_relevant_binding = True

    if has_relevant_binding:
        checks.append(_check("NV-19", "PASS",
            "At least one evidence item has a relevant evaluator-assessed binding"))
        sub_results.append("PASS")
    else:
        non_publisher_evidence = [e for e in evidence_items if e.get("kind") != "publisher_claim"]
        if non_publisher_evidence:
            checks.append(_check("NV-19", "FAIL",
                "No evidence item has a relevant evaluator-assessed binding for ASSURED"))
            sub_results.append("FAIL")
        else:
            checks.append(_check("NV-19", "FAIL",
                "All evidence is publisher_claim -- no ASSURED binding possible"))
            sub_results.append("FAIL")

    # NV-20: Claim-specific assurance policy (check policy snapshot)
    claim_type = receipt.get("claim_type", "")
    if policy_snapshot:
        assurance_policies = policy_snapshot.get("assurance_policies", {})
        policy = assurance_policies.get(claim_type)
        if policy:
            checks.append(_check("NV-20", "PASS",
                f"Assurance policy found for claim_type '{claim_type}'"))
            sub_results.append("PASS")
        else:
            checks.append(_check("NV-20", "PASS",
                f"No specific policy for claim_type '{claim_type}' -- strictest standard applied"))
            sub_results.append("PASS")
    else:
        checks.append(_check("NV-20", "PASS",
            "No policy snapshot -- strictest standard applied by default"))
        sub_results.append("PASS")

    return _aggregate(sub_results), checks


# ---------------------------------------------------------------------------
# Check 4: Revision Integrity (NV-08 through NV-13)
# ---------------------------------------------------------------------------

def _check_revision_integrity(receipt: dict) -> tuple[str, list[dict], str | None]:
    """Returns (aggregate, checks, effective_status_or_None)."""
    checks = []
    sub_results = []
    revisions = receipt.get("revision_history", [])
    effective_status = None

    if not revisions:
        checks.append(_check("NV-08", "PASS", "No revision history"))
        return "PASS", checks, None

    # NV-08: Revision ID uniqueness
    ids = [r.get("revision_id") for r in revisions]
    if len(ids) != len(set(ids)):
        checks.append(_check("NV-08", "FAIL", "Duplicate revision_id found"))
        sub_results.append("FAIL")
    else:
        checks.append(_check("NV-08", "PASS", "All revision_ids unique"))
        sub_results.append("PASS")

    id_set = set(ids)

    # NV-09: Reference validity
    for r in revisions:
        prior = r.get("prior_revision_id")
        if prior is not None and prior not in id_set:
            checks.append(_check("NV-09", "FAIL",
                f"Dangling prior_revision_id: '{prior}'"))
            sub_results.append("FAIL")
            break
    else:
        checks.append(_check("NV-09", "PASS", "All prior_revision_id references valid"))
        sub_results.append("PASS")

    # NV-10: Acyclicity
    graph = {}
    for r in revisions:
        rid = r.get("revision_id")
        prior = r.get("prior_revision_id")
        if prior is not None:
            graph.setdefault(prior, []).append(rid)

    def has_cycle(start, visited=None, path=None):
        if visited is None:
            visited = set()
        if path is None:
            path = set()
        if start in path:
            return True
        path.add(start)
        for child in graph.get(start, []):
            if has_cycle(child, visited, path):
                return True
        path.discard(start)
        visited.add(start)
        return False

    cycle_found = False
    for rid in ids:
        if has_cycle(rid):
            cycle_found = True
            break
    if cycle_found:
        checks.append(_check("NV-10", "FAIL", "Cycle detected in revision graph"))
        sub_results.append("FAIL")
    else:
        checks.append(_check("NV-10", "PASS", "Revision graph is acyclic"))
        sub_results.append("PASS")

    # NV-11: Evidence link validity
    all_evidence_ids = set()
    for ev in receipt.get("source_evidence", []):
        all_evidence_ids.add(ev.get("evidence_id", ""))
    for ev in receipt.get("counterevidence", []):
        all_evidence_ids.add(ev.get("evidence_id", ""))

    dangling_ev = False
    for r in revisions:
        for eid in r.get("evidence_ids", []):
            if eid not in all_evidence_ids:
                checks.append(_check("NV-11", "FAIL",
                    f"Revision '{r.get('revision_id')}' references unknown evidence_id '{eid}'"))
                sub_results.append("FAIL")
                dangling_ev = True
                break
        if dangling_ev:
            break
    if not dangling_ev:
        checks.append(_check("NV-11", "PASS", "All revision evidence_ids reference existing evidence"))
        sub_results.append("PASS")

    # NV-12: Effective status reconciliation
    # Find leaf revisions (not referenced as prior by any other)
    referenced_as_prior = set()
    for r in revisions:
        prior = r.get("prior_revision_id")
        if prior is not None:
            referenced_as_prior.add(prior)

    leaves = [r for r in revisions if r.get("revision_id") not in referenced_as_prior]

    if not leaves:
        leaves = revisions  # fallback

    leaf_statuses = [l.get("status") for l in leaves]

    # Check for withdrawal
    if all(s == "WITHDRAWN" for s in leaf_statuses):
        effective_status = "WITHDRAWN"
    elif len(set(leaf_statuses)) == 1:
        single_status = leaf_statuses[0]
        # Check if leaves share the same evaluator (via dependency_edges)
        dep_edges = receipt.get("dependency_edges", [])
        leaf_ids = {l.get("revision_id") for l in leaves}
        same_evaluator = False
        for edge in dep_edges:
            if edge.get("relation") == "same_evaluator":
                from_id = edge.get("from_id")
                to_id = edge.get("to_id")
                if from_id in leaf_ids and to_id in leaf_ids:
                    same_evaluator = True
                    break
        if same_evaluator and len(leaves) > 1:
            effective_status = "UNRECONCILED"
            checks.append(_check("NV-12", "FAIL",
                "Leaves share status but rely on same evaluator -- UNRECONCILED"))
            sub_results.append("FAIL")
        else:
            effective_status = single_status
    else:
        # Mixed statuses
        status_set = set(leaf_statuses)
        if status_set == {"VERIFIED", "CONTRADICTED"} or status_set == {"VERIFIED", "PROVISIONAL"}:
            effective_status = "UNRECONCILED"
        elif "CONTRADICTED" in status_set:
            effective_status = "UNRECONCILED"
        else:
            effective_status = "UNRECONCILED"

    if effective_status == "UNRECONCILED":
        if receipt.get("status") == "VERIFIED":
            checks.append(_check("NV-12", "FAIL",
                "Receipt status is VERIFIED but effective assessment is UNRECONCILED"))
            sub_results.append("FAIL")
        else:
            if "FAIL" not in [c["status"] for c in checks if c["check_id"] == "NV-12"]:
                checks.append(_check("NV-12", "UNCERTIFIED",
                    f"Effective assessment UNRECONCILED (leaf statuses: {leaf_statuses})"))
                sub_results.append("UNCERTIFIED")
    else:
        if not any(c["check_id"] == "NV-12" for c in checks):
            checks.append(_check("NV-12", "PASS",
                f"Effective assessment: {effective_status}"))
            sub_results.append("PASS")

    # NV-13: Withdrawal handling
    for r in revisions:
        if r.get("relation") == "withdraws" or r.get("status") == "WITHDRAWN":
            withdrawn_prior = r.get("prior_revision_id")
            if withdrawn_prior and receipt.get("status") == "VERIFIED":
                # Check if any active leaf descends from the withdrawn revision
                checks.append(_check("NV-13", "FAIL",
                    f"Receipt status VERIFIED but revision '{r.get('revision_id')}' "
                    f"withdraws/retracts prior '{withdrawn_prior}'"))
                sub_results.append("FAIL")
                break

    if not sub_results:
        sub_results.append("PASS")

    return _aggregate(sub_results), checks, effective_status


# ---------------------------------------------------------------------------
# Check 5: Authorization Consistency (NV-14 through NV-17, NV-21)
# ---------------------------------------------------------------------------

def _check_authorization(receipt: dict, conformance_overall: str,
                          assurance_overall: str,
                          policy_snapshot: dict | None) -> tuple[str, str, list[dict]]:
    """Returns (auth_consistency, execution_permission, checks)."""
    checks = []
    sub_results = []
    status = receipt.get("status", "UNKNOWN")
    action = receipt.get("allowed_action", "no_action")
    review = receipt.get("review", {})
    auth = receipt.get("effect_authorization")

    # NV-14: Status-action consistency
    nv14_fail = False
    if status == "UNKNOWN" and action == "bounded_effect":
        nv14_fail = True
        checks.append(_check("NV-14", "FAIL", "UNKNOWN status with bounded_effect action"))
    elif status == "CONTRADICTED" and action == "bounded_effect":
        nv14_fail = True
        checks.append(_check("NV-14", "FAIL", "CONTRADICTED status with bounded_effect action"))
    elif status == "WITHDRAWN" and action != "no_action":
        nv14_fail = True
        checks.append(_check("NV-14", "FAIL", f"WITHDRAWN status with action '{action}'"))
    else:
        checks.append(_check("NV-14", "PASS", "Status-action combination valid"))
    sub_results.append("FAIL" if nv14_fail else "PASS")

    # NV-15: Bounded-effect authorization checks
    if action == "bounded_effect" and auth:
        auth_fields = ["contract_match", "effect_type_allowed", "target_allowed",
                       "witness_healthy", "evidence_current"]
        all_true = True
        for field in auth_fields:
            val = auth.get(field, "UNKNOWN")
            if val == "UNKNOWN":
                checks.append(_check("NV-15", "FAIL",
                    f"Authorization check '{field}' is UNKNOWN -- UNKNOWN is never authorizing"))
                sub_results.append("FAIL")
                all_true = False
            elif val == "FALSE":
                checks.append(_check("NV-15", "FAIL",
                    f"Authorization check '{field}' is FALSE"))
                sub_results.append("FAIL")
                all_true = False
        if all_true:
            checks.append(_check("NV-15", "PASS", "All five authorization checks are TRUE"))
            sub_results.append("PASS")
    elif action == "bounded_effect" and not auth:
        checks.append(_check("NV-15", "FAIL",
            "bounded_effect requires effect_authorization"))
        sub_results.append("FAIL")

    # NV-16: NOT_APPLICABLE handling
    if auth:
        exc_policy = auth.get("exception_policy")
        for field in ["contract_match", "effect_type_allowed", "target_allowed",
                       "witness_healthy", "evidence_current"]:
            val = auth.get(field, "")
            if val == "UNKNOWN" and exc_policy:
                # Exception policy does NOT convert UNKNOWN to NOT_APPLICABLE
                checks.append(_check("NV-16", "FAIL",
                    f"'{field}' is UNKNOWN with exception_policy -- "
                    f"exception_policy does not convert UNKNOWN"))
                sub_results.append("FAIL")

    # NV-17: Authorization does not affect conformance/assurance
    checks.append(_check("NV-17", "PASS",
        "Authorization evaluated independently from conformance and assurance"))
    sub_results.append("PASS")

    auth_consistency = _aggregate(sub_results)

    # NV-21: Fail-closed execution gate
    exec_permission = "UNCERTIFIED"
    if action == "bounded_effect":
        human_approved = review.get("authorization") == "approved"
        conformant = conformance_overall == "CONFORMANT"
        # For assurance: check if policy requires it for this action
        assured_ok = assurance_overall in ("ASSURED", "UNCERTIFIED")
        no_uncertified_mandatory = auth_consistency != "FAIL"

        if human_approved and conformant and assured_ok and no_uncertified_mandatory and auth_consistency == "PASS":
            exec_permission = "GRANTED"
        else:
            exec_permission = "DENIED"
            reasons = []
            if not human_approved:
                reasons.append("no human approval")
            if not conformant:
                reasons.append(f"conformance={conformance_overall}")
            if assurance_overall == "NOT_ASSURED":
                reasons.append("not assured")
            if auth_consistency == "FAIL":
                reasons.append("authorization consistency FAIL")
            checks.append(_check("NV-21", "FAIL",
                f"Execution DENIED: {', '.join(reasons)}"))
    else:
        exec_permission = "UNCERTIFIED"
        checks.append(_check("NV-21", "PASS",
            f"Action is '{action}' -- execution gate not applicable"))

    return auth_consistency, exec_permission, checks


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------

def verify(receipt: dict,
           registry_snapshot: dict | None = None,
           policy_snapshot: dict | None = None,
           evidence_snapshot: dict | None = None) -> dict:
    """
    Stage 2 normative verification of an Evidence Receipt.

    Pure function. Deterministic. Side-effect-free.
    Does not modify receipt or any snapshot.

    Args:
        receipt: Evidence Receipt dict (must pass Stage 1 schema validation)
        registry_snapshot: Frozen lineage registry state (optional)
        policy_snapshot: Frozen assurance/authorization policies (optional)
        evidence_snapshot: Frozen evidence artifacts (optional)

    Returns:
        VerificationResult dict per spec Section 3.
    """
    # Deep-copy to protect against aliasing
    receipt = copy.deepcopy(receipt)

    all_checks = []
    notes = []

    # Stage 1: Schema version check
    schema_version = receipt.get("schema_version", "")
    if schema_version not in SUPPORTED_SCHEMA_VERSIONS:
        stage_1 = "FAIL"
        all_checks.append(_check("STAGE-1", "FAIL",
            f"Unsupported schema_version '{schema_version}'"))
        # Fail-closed: return immediately
        return {
            "result_id": f"VR-{uuid.uuid4().hex[:8]}",
            "claim_id": receipt.get("claim_id", ""),
            "receipt_sha256": _canonical_hash(receipt),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "schema_versions_supported": SUPPORTED_SCHEMA_VERSIONS,
            "receipt_schema_version": schema_version,
            "verification_context": {
                "registry_snapshot_sha256": _snapshot_hash(registry_snapshot),
                "policy_snapshot_sha256": _snapshot_hash(policy_snapshot),
                "evidence_snapshot_sha256": _snapshot_hash(evidence_snapshot),
                "snapshot_timestamp": datetime.now(timezone.utc).isoformat(),
            },
            "stage_1": "FAIL",
            "claim_conformance": {
                "evidence_eligibility": "FAIL",
                "independence_provenance": "FAIL",
                "revision_integrity": "FAIL",
                "overall": "NON_CONFORMANT",
            },
            "claim_assurance": {
                "witness_independence": "FAIL",
                "evidence_relevance": "FAIL",
                "overall": "NOT_ASSURED",
            },
            "action_authorization": {
                "authorization_consistency": "FAIL",
                "execution_permission": "DENIED",
                "overall": "NOT_AUTHORIZED",
            },
            "checks": all_checks,
            "notes": "Stage 1 FAIL: unsupported schema version",
        }

    stage_1 = "PASS"

    # Check 1: Evidence Eligibility
    elig_result, elig_checks = _check_evidence_eligibility(receipt, evidence_snapshot)
    all_checks.extend(elig_checks)

    # Check 2: Independence Provenance
    prov_result, prov_checks = _check_independence_provenance(
        receipt, registry_snapshot, policy_snapshot)
    all_checks.extend(prov_checks)

    # Check 3: Evidence-to-Claim Relevance
    rel_result, rel_checks = _check_evidence_relevance(
        receipt, evidence_snapshot, policy_snapshot)
    all_checks.extend(rel_checks)

    # Check 4: Revision Integrity
    rev_result, rev_checks, effective_status = _check_revision_integrity(receipt)
    all_checks.extend(rev_checks)
    if effective_status:
        notes.append(f"Effective revision status: {effective_status}")

    # Conformance: evidence_eligibility + independence_provenance + revision_integrity
    conf_components = [elig_result, prov_result, rev_result]
    if "FAIL" in conf_components:
        conformance_overall = "NON_CONFORMANT"
    elif "UNCERTIFIED" in conf_components:
        conformance_overall = "UNCERTIFIED"
    else:
        conformance_overall = "CONFORMANT"

    # Assurance: witness_independence (from prov) + evidence_relevance
    # NV-03: publisher_claim evidence cannot contribute to ASSURED
    has_only_publisher_claims = all(
        ev.get("kind") == "publisher_claim"
        for ev in receipt.get("source_evidence", [])
    ) if receipt.get("source_evidence") else True

    if has_only_publisher_claims and receipt.get("source_evidence"):
        witness_independence = "FAIL"
        evidence_relevance = "FAIL"
    else:
        witness_independence = prov_result
        evidence_relevance = rel_result

    assurance_components = [witness_independence, evidence_relevance]
    if "FAIL" in assurance_components:
        assurance_overall = "NOT_ASSURED"
    elif "UNCERTIFIED" in assurance_components:
        assurance_overall = "UNCERTIFIED"
    else:
        assurance_overall = "ASSURED"

    # Degraded mode note
    if registry_snapshot is None:
        notes.append("Lineage registry unavailable -- provenance-dependent checks produce UNCERTIFIED")

    # Check 5: Authorization
    auth_result, exec_perm, auth_checks = _check_authorization(
        receipt, conformance_overall, assurance_overall, policy_snapshot)
    all_checks.extend(auth_checks)

    if "FAIL" in [auth_result]:
        auth_overall = "NOT_AUTHORIZED"
    elif exec_perm == "GRANTED":
        auth_overall = "AUTHORIZED"
    elif exec_perm == "UNCERTIFIED":
        auth_overall = "UNCERTIFIED"
    else:
        auth_overall = "NOT_AUTHORIZED"

    return {
        "result_id": f"VR-{uuid.uuid4().hex[:8]}",
        "claim_id": receipt.get("claim_id", ""),
        "receipt_sha256": _canonical_hash(receipt),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "schema_versions_supported": SUPPORTED_SCHEMA_VERSIONS,
        "receipt_schema_version": schema_version,
        "verification_context": {
            "registry_snapshot_sha256": _snapshot_hash(registry_snapshot),
            "policy_snapshot_sha256": _snapshot_hash(policy_snapshot),
            "evidence_snapshot_sha256": _snapshot_hash(evidence_snapshot),
            "snapshot_timestamp": datetime.now(timezone.utc).isoformat(),
        },
        "stage_1": stage_1,
        "claim_conformance": {
            "evidence_eligibility": elig_result,
            "independence_provenance": prov_result,
            "revision_integrity": rev_result,
            "overall": conformance_overall,
        },
        "claim_assurance": {
            "witness_independence": witness_independence,
            "evidence_relevance": evidence_relevance,
            "overall": assurance_overall,
        },
        "action_authorization": {
            "authorization_consistency": auth_result,
            "execution_permission": exec_perm,
            "overall": auth_overall,
        },
        "checks": all_checks,
        "notes": "; ".join(notes) if notes else "",
    }
# Bismillah ir-Rahman ir-Rahim
