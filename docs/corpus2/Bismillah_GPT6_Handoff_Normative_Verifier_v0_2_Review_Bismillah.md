# Bismillah ir-Rahman ir-Rahim

# GPT-6 Handoff: Normative Verifier v0.1 Findings Accepted -- Review of Proposed v0.2 Corrections
## Cross-Vendor Specification Review Request

**Date:** October 31, 2026
**From:** Claude (Anthropic, Opus 4.6)
**To:** GPT-6 (independent cross-vendor reviewer)
**Subject:** NV-R1 through NV-R4 acceptance and proposed corrections for Normative Verifier v0.2
**Decision authority:** Bilal retains all merge, specification, and deployment decisions.

---

## 1. TASK

GPT-6 identified four findings (NV-R1 through NV-R4) and seven additional requirements in the Normative Verifier v0.1 specification. Claude accepts all four findings and proposes specific corrections below. GPT-6 is asked to review whether these corrections adequately address each finding, or whether they introduce new gaps.

---

## 2. EVIDENCE

- Normative Verifier v0.1 specification (commit b87874f)
- GPT-6's review producing NV-R1 (HIGH), NV-R2 (HIGH), NV-R3 (MEDIUM), NV-R4 (MEDIUM)
- Evidence Receipt v0.2 schema (commit 870efd7)

---

## 3. PROPOSED CORRECTIONS

### NV-R1 (HIGH): Three-way certification distinction

**Problem:** CERTIFIED conflates receipt conformance with verification of the underlying factual claim.

**Proposed correction:** Replace the single CERTIFIED outcome with three independent levels:

| Level | What it answers | Who can determine it |
|-------|----------------|---------------------|
| **CONFORMANT** | Does the receipt satisfy all structural (Stage 1) and normative (Stage 2 checks NV-01 through NV-13) rules? | The normative verifier (automated) |
| **ASSURED** | Has the evidence referenced in the receipt been independently verified to support the specific claim? | External evaluators with claim-domain expertise |
| **AUTHORIZED** | Has action on this claim been separately permitted? | Human authority (Bilal or designated reviewer) |

Each level is independently determined. CONFORMANT does not imply ASSURED. ASSURED does not imply AUTHORIZED. AUTHORIZED does not imply CONFORMANT or ASSURED.

The verification result format becomes:

```json
{
  "result_id": "VR-001",
  "claim_id": "CLAIM-001",
  "receipt_sha256": "<canonical hash>",
  "timestamp": "2026-10-31T22:00:00Z",
  "schema_version_supported": ["0.2.0-draft"],
  "receipt_schema_version": "0.2.0-draft",
  "stage_1": "PASS|FAIL",
  "claim_conformance": {
    "evidence_eligibility": "PASS|FAIL|UNCERTIFIED",
    "independence_provenance": "PASS|FAIL|UNCERTIFIED",
    "revision_integrity": "PASS|FAIL|UNCERTIFIED",
    "overall": "CONFORMANT|NON_CONFORMANT|UNCERTIFIED"
  },
  "claim_assurance": {
    "status": "ASSURED|NOT_ASSURED|UNCERTIFIED",
    "assurance_evidence": [ ... ],
    "notes": "..."
  },
  "action_authorization": {
    "authorization_consistency": "PASS|FAIL|UNCERTIFIED",
    "overall": "AUTHORIZED|NOT_AUTHORIZED|UNCERTIFIED"
  },
  "checks": [ ... ],
  "notes": "..."
}
```

**Question for GPT-6:** Is three levels the right decomposition, or should ASSURED be further split (e.g., separating "evidence was independently produced" from "evidence is relevant to this specific claim")?

### NV-R2 (HIGH): Evidence-to-claim relevance binding

**Problem:** The spec checks whether evidence is external and reproduced, but not whether that evidence tests and supports the exact claim. An external lab could reproduce a measurement irrelevant to the claim.

**Proposed correction:** Add a `claim_binding` object to each evidence item referenced for ASSURED status:

```json
{
  "evidence_id": "EXT-01",
  "claim_binding": {
    "tested_property": "SHA-256 hash of file X matches claimed value Y",
    "claim_relevance": "direct_test|supporting|contextual|unrelated",
    "execution_evidence_id": "EXEC-001",
    "observed_result": "hash matched",
    "result_supports_claim": true
  }
}
```

New normative check:

**NV-18:** For ASSURED status, at least one evidence item must have:
- `claim_binding.claim_relevance` in `["direct_test", "supporting"]`
- `claim_binding.execution_evidence_id` referencing a retrievable execution record
- `claim_binding.result_supports_claim` is `true`

An evidence item with `claim_relevance: "unrelated"` or `claim_relevance: "contextual"` cannot contribute to ASSURED status.

**Question for GPT-6:** Should `claim_binding` be part of the evidence item in the receipt schema itself, or should it exist only in the verification result? If in the receipt, it becomes a publisher declaration subject to the same independence concerns as `independence: "external"`. If in the verification result, it is the verifier's assessment.

### NV-R3 (MEDIUM): Reconciliation algorithm

**Problem:** NV-12 gives contradictory guidance for competing branches. Append-only history is asserted, not proven.

**Proposed correction:**

1. Replace the split guidance with a single reconciliation algorithm:

```
RECONCILE(leaf_statuses):
  if all leaves agree on status S:
    return S
  if any leaf is WITHDRAWN and all non-WITHDRAWN leaves agree:
    return the agreed status (WITHDRAWN branches are inactive)
  else:
    return UNRECONCILED
```

UNRECONCILED is a new effective-status value distinct from UNCERTIFIED. It means: competing active branches exist with incompatible conclusions. The receipt's top-level status must be UNRECONCILED when this occurs. UNRECONCILED is not a failure -- it is an honest representation of ongoing dispute.

2. Append-only history is proven by external record:
- Each revision_entry should carry an optional `habl_finding_id` linking to an immutable HABL record
- The verifier checks that revision_entry timestamps are monotonically non-decreasing per branch
- The verifier cannot prove global append-only without an external ledger; it records this as a limitation in its notes

3. Precedence when FAIL and UNCERTIFIED coexist in the same verification result:
- FAIL takes precedence over UNCERTIFIED in the `overall` determination
- An evidence_eligibility FAIL with an independence_provenance UNCERTIFIED produces `overall: NON_CONFORMANT` (not UNCERTIFIED)
- Rationale: a demonstrated violation is stronger evidence than an unresolved check

**Question for GPT-6:** Is UNRECONCILED the right term, or does it create confusion with UNCERTIFIED? Should the reconciliation algorithm handle more cases (e.g., VERIFIED vs. PROVISIONAL on competing branches)?

### NV-R4 (MEDIUM): Authorization independence

**Problem:** Authorization consistency checks feed into the overall certification result despite the separation principle.

**Proposed correction:**

Split the verification result into two independent outputs (already shown in the NV-R1 result format above):

- `claim_conformance` (NV-01 through NV-13): evidence eligibility, independence provenance, revision integrity
- `action_authorization` (NV-14 through NV-17): authorization consistency

Neither output's overall value is derived from the other. A receipt can be CONFORMANT with action_authorization NOT_AUTHORIZED. A receipt can be NON_CONFORMANT with action_authorization AUTHORIZED (though this should produce a warning -- authorized action on a non-conformant receipt is dangerous).

For NV-16 (inapplicable checks): add an `authorization_state` representation to the authorization model:

```json
{
  "check_name": "target_allowed",
  "value": "TRUE|FALSE|UNKNOWN|NOT_APPLICABLE",
  "exception_policy": "This check is not applicable because..."
}
```

NOT_APPLICABLE is distinct from UNKNOWN. NOT_APPLICABLE with an exception_policy is acceptable. UNKNOWN without an exception_policy is FAIL for bounded_effect.

---

## 4. ADDITIONAL REQUIREMENTS (from GPT-6's review)

| Requirement | Proposed response |
|---|---|
| Explicit FAIL/UNCERTIFIED precedence | FAIL takes precedence (see NV-R3 correction above) |
| Frozen dependency and execution-evidence snapshots | Add `snapshot_timestamp` to independence_provenance and execution evidence references. The verifier checks against the snapshot, not live state. |
| Canonical receipt hashing | Specify: canonical form is the receipt JSON serialized with sorted keys, no whitespace, UTF-8 encoded, SHA-256 hashed. The `receipt_sha256` in the verification result uses this canonical form. |
| AT-5 scope | Move AT-5 (conflicting projections) to the cross-projection reconciler specification. Remove from normative verifier AT list. |
| AT-4 pre-established presentations | Revise AT-4 to use a fixed corpus of truth-equivalent presentation pairs, established before the verifier is tested, not generated by the verifier or its implementor. |
| Supported schema versions | Add `schema_version_supported` array to the verification result. Unknown schema versions produce FAIL (fail-closed). |
| Degraded mode | Maintain: degraded mode produces UNCERTIFIED for all provenance-dependent checks, never CONFORMANT or ASSURED. |

---

## 5. NEXT GATE

If GPT-6 confirms these corrections address NV-R1 through NV-R4 (or identifies remaining gaps), the next steps are:

1. Revise the Normative Verifier specification to v0.2 incorporating all corrections
2. Design adversarial conformance tests for each finding
3. Submit revised specification for independent Gate 4 review
4. Only then begin implementation

No code changes, PR merges, or schema approvals are requested from GPT-6. Independent review only.

Bilal retains all phase and merge authority.

---

**Bismillah ir-Rahman ir-Rahim**
