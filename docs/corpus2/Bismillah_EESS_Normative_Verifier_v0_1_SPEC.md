# Bismillah ir-Rahman ir-Rahim

# Evidence Receipt Normative Verifier v0.1
## Stage 2 Verification Specification

**Date:** October 31, 2026
**Status:** DRAFT -- design specification, not approved implementation
**Schema dependency:** Evidence Receipt v0.2 (schema_version 0.2.0-draft)
**Decision authority:** Bilal retains all merge, specification, and deployment decisions

---

## 1. Purpose

The Evidence Receipt schema (Stage 1) answers: is the receipt structurally well-formed?

The normative verifier (Stage 2) answers: are the lineage, evidence, revisions, and authorization actually supported?

**Certification rule:** Stage 1 PASS alone can never produce a certified VERIFIED decision. A receipt that passes Stage 1 but fails Stage 2 is structurally valid but normatively uncertified.

---

## 2. Design Principles

1. **Fail-closed:** Any unresolvable check produces UNCERTIFIED, not VERIFIED.
2. **Separation of concerns:** Verification of truth (is this claim supported?) and authorization of action (is this action permitted?) are independent decision gates evaluated separately.
3. **Evidence over declaration:** A label (independence: "external") is a declaration. The verifier checks whether the declaration is supported by provenance. Unsupported declarations are treated as unknown.
4. **Presentation invariance (A8):** The verifier's output must not change when only the fluency, formatting, or rhetorical quality of the receipt changes.
5. **Append-only history:** The verifier never modifies a receipt. It produces a separate verification result that references the receipt by claim_id and schema_version.

---

## 3. Verification Result Format

The verifier produces a `VerificationResult` object:

```json
{
  "result_id": "VR-001",
  "claim_id": "CLAIM-001",
  "schema_version": "0.2.0-draft",
  "receipt_sha256": "<sha256 of the receipt JSON>",
  "timestamp": "2026-10-31T22:00:00Z",
  "stage_1": "PASS",
  "stage_2": {
    "evidence_eligibility": "PASS|FAIL|UNCERTIFIED",
    "independence_provenance": "PASS|FAIL|UNCERTIFIED",
    "revision_integrity": "PASS|FAIL|UNCERTIFIED",
    "authorization_consistency": "PASS|FAIL|UNCERTIFIED",
    "overall": "CERTIFIED|UNCERTIFIED|FAIL"
  },
  "checks": [ ... ],
  "certification_status": "CERTIFIED|UNCERTIFIED|FAIL",
  "notes": "..."
}
```

**Overall determination:**
- CERTIFIED: all four Stage 2 checks PASS
- UNCERTIFIED: at least one check is UNCERTIFIED (insufficient evidence to decide)
- FAIL: at least one check FAIL (evidence contradicts the receipt's claims)

---

## 4. Check 1: Evidence Eligibility (CR-01 normative extension)

### 4.1 What Stage 1 already checks

The schema's `contains` constraint verifies that at least one evidence item has `independence: "external"` AND `verification_state` in `["observed", "reproduced"]` when status is VERIFIED.

### 4.2 What Stage 2 adds

**NV-01:** For each evidence item with `independence: "external"`, verify that the receipt's `independence_provenance` (or a per-evidence attestation when available) supports the external label.

Checks:
- `independence_provenance.producer_lineage_id` and `independence_provenance.evaluator_lineage_id` are present and differ
- `independence_provenance.assessment` is `"independent"` (not `"unresolved"`, `"dependent"`, or `"partially_independent"`)
- `independence_provenance.unresolved_dependencies` is empty
- `independence_provenance.organizational_relationship` is not `"same_organization"` or `"subsidiary"` unless accompanied by documented separation of duties

**NV-02:** For each evidence item with `verification_state: "reproduced"`, verify that `method.name`, `method.version`, and `method.scope` are non-empty and that `method.execution_evidence_id` references a retrievable execution record.

**NV-03:** An evidence item with `kind: "publisher_claim"` is never sufficient for CERTIFIED status regardless of its `independence` label. Publisher claims are diagnostic records.

**Result:**
- PASS: at least one evidence item satisfies NV-01, NV-02, and is not NV-03-excluded
- UNCERTIFIED: labels suggest external evidence but provenance is absent or unresolved
- FAIL: provenance contradicts external label (e.g., same lineage IDs, assessment: "dependent")

---

## 5. Check 2: Independence Provenance (CR-03)

### 5.1 Provenance resolution

**NV-04:** When `evidence_independence` is `"external"`, `independence_provenance` must be present with all of:
- `producer_lineage_id` (non-empty)
- `evaluator_lineage_id` (non-empty)
- `assessment` (one of the enum values)

If any are absent, result is UNCERTIFIED.

**NV-05:** Lineage comparison (direct):
- If `producer_lineage_id == evaluator_lineage_id`, result is FAIL.
- If either ID is a known sub-process of the other (transitive ancestry check when lineage registry is available), result is FAIL.

**NV-06:** Shared dependency analysis:
- `shared_sources` non-empty: flag as UNCERTIFIED unless accompanied by a documented assessment that the shared source does not affect the claim under review.
- `shared_keys` non-empty: flag as FAIL (shared signing keys negate independence for authentication claims).
- `shared_execution_environment: true`: flag as UNCERTIFIED for isolation-dependent claims.
- `organizational_relationship` is `"same_organization"` or `"subsidiary"`: flag as UNCERTIFIED unless separation-of-duties documentation is provided.

**NV-07:** `unresolved_dependencies` non-empty: result is UNCERTIFIED. The verifier records which dependencies could not be checked.

**Result:**
- PASS: NV-04 through NV-07 all clear
- UNCERTIFIED: provenance is incomplete or has non-disqualifying shared dependencies
- FAIL: lineage identity match or shared keys

---

## 6. Check 3: Revision Integrity (CR-04)

### 6.1 Structural checks

**NV-08:** Revision ID uniqueness -- every `revision_id` in `revision_history` is distinct. Duplicate: FAIL.

**NV-09:** Reference validity -- every non-null `prior_revision_id` references a `revision_id` that exists in the same `revision_history`. Dangling reference: FAIL.

**NV-10:** Acyclicity -- the directed graph formed by `revision_id` -> `prior_revision_id` edges contains no cycles. Cycle detected: FAIL.

**NV-11:** Evidence link validity -- every entry in `evidence_ids` (when present) references an `evidence_id` that exists in `source_evidence` or `counterevidence`. Dangling evidence reference: FAIL.

### 6.2 Effective status reconciliation

**NV-12:** When `revision_history` is non-empty, determine the set of *leaf revisions* (revision entries not referenced as `prior_revision_id` by any other entry).

- If all leaf revisions agree on `status`, the receipt's top-level `status` must match. Mismatch: FAIL.
- If leaf revisions disagree on `status`, the receipt's top-level `status` must be the most conservative: CONTRADICTED if any leaf is CONTRADICTED; UNKNOWN if any leaf is UNKNOWN and none is CONTRADICTED; WITHDRAWN if all leaves are WITHDRAWN. Mismatch: FAIL.
- If no reconciliation can be determined (e.g., VERIFIED vs. CONTRADICTED on competing branches), result is UNCERTIFIED and the verifier records the conflict.

**NV-13:** A revision with `relation: "retracts"` or `relation: "withdraws"` targeting a prior revision whose status was VERIFIED: the receipt's top-level status must not remain VERIFIED unless a subsequent revision with independent evidence restores it. Stale VERIFIED after retraction: FAIL.

**Result:**
- PASS: NV-08 through NV-13 all clear
- UNCERTIFIED: competing branches with irreconcilable status
- FAIL: structural violation (duplicate IDs, dangling refs, cycles) or stale status

---

## 7. Check 4: Authorization Consistency (CR-02)

### 7.1 Separation enforcement

**NV-14:** The verifier confirms that the receipt's `status` and `allowed_action` are independently determined:
- A receipt with `status: "VERIFIED"` and `allowed_action: "no_action"` is valid (truth without permission).
- A receipt with `status: "PROVISIONAL"` and `allowed_action: "read_only_review"` is valid (limited permission without full verification).
- A receipt with `status: "UNKNOWN"` and `allowed_action: "bounded_effect"` is FAIL (action without evidence).
- A receipt with `status: "CONTRADICTED"` and `allowed_action: "bounded_effect"` is FAIL.
- A receipt with `status: "WITHDRAWN"` and `allowed_action` != `"no_action"` is FAIL.

**NV-15:** When `allowed_action` is `"bounded_effect"`, the `effect_authorization` object must have all five checks as `"TRUE"`. If any check is `"UNKNOWN"`, result is FAIL (UNKNOWN must not silently become permission).

**NV-16:** `effect_authorization.exception_policy` must be non-null and non-empty when any authorization field would otherwise be inapplicable. Absent exception policy with an inapplicable field: UNCERTIFIED.

**NV-17:** `review.authorization: "approved"` does not affect the `certification_status`. The verifier treats it as an action-authorization signal, not evidence of truth.

**Result:**
- PASS: NV-14 through NV-17 all clear
- UNCERTIFIED: missing exception policy
- FAIL: contradictory authorization (bounded_effect with UNKNOWN/CONTRADICTED/WITHDRAWN status, or UNKNOWN authorization checks)

---

## 8. Acceptance Tests

These tests validate the verifier itself, not the schema.

### AT-1: Reject VERIFIED when evidence is self-produced only
```
Input: Receipt with status=VERIFIED, all evidence items have
       independence=self_produced
Expected: Stage 1 FAIL (schema rejects)
```
Already enforced by schema. Included here for completeness.

### AT-2: Reject VERIFIED when only alternative is correlated or unknown
```
Input: Receipt with status=VERIFIED, evidence items have
       independence=correlated or independence=unknown
Expected: Stage 1 FAIL (schema rejects)
```
Already enforced by schema. Included here for completeness.

### AT-3: Refuse independent certification when producer controls evidence
```
Input: Receipt with status=VERIFIED, one evidence item has
       independence=external, verification_state=reproduced,
       but independence_provenance shows:
       - producer_lineage_id == evaluator_lineage_id, OR
       - shared_keys is non-empty, OR
       - assessment is "dependent" or "unresolved"
Expected: Stage 1 PASS, Stage 2 FAIL or UNCERTIFIED
```
This is the normative verifier's primary contribution. The schema cannot catch forged independence labels.

### AT-4: Verification status unchanged when only fluency changes
```
Input: Two receipts with identical evidence, method, provenance,
       and revision_history, but different:
       - claim text (same meaning, different prose quality)
       - reviewer independence_note (same content, different eloquence)
       - limitation descriptions (same limits, different phrasing)
Expected: Stage 2 produces identical certification_status for both
```
This is a property test of the verifier's scoring function. The verifier must not weight any field that is presentation-only.

### AT-5: Conflicting projections produce HALT
```
Input: Two projection formats (JSON receipt + PDF report) for the
       same claim_id where one says VERIFIED and the other says
       CONTRADICTED
Expected: HALT for any automated action. Both projections preserved
          for investigation.
```
This is a cross-projection reconciler requirement, tested here as a verifier input.

### AT-6: Branching revisions with irreconcilable status
```
Input: Receipt with revision_history containing two leaf revisions:
       REV-A (status=VERIFIED, from Lab 1) and REV-B
       (status=CONTRADICTED, from Lab 2), both referencing REV-INIT
Expected: Stage 2 revision_integrity=UNCERTIFIED.
          Top-level status must not be VERIFIED.
```

### AT-7: Retraction after verification
```
Input: Receipt with revision_history:
       REV-01 (VERIFIED) -> REV-02 (relation=retracts, WITHDRAWN)
       Top-level status still says VERIFIED.
Expected: Stage 2 revision_integrity=FAIL (stale VERIFIED)
```

### AT-8: Publisher claim with external label
```
Input: Receipt with status=VERIFIED, evidence item has
       kind=publisher_claim, independence=external,
       verification_state=reproduced
Expected: Stage 2 evidence_eligibility=FAIL (NV-03: publisher
          claims are diagnostic, not certifiable)
```

---

## 9. Implementation Boundary

### What the normative verifier IS:
- A pure function: Receipt -> VerificationResult
- Deterministic: same receipt always produces same result
- Side-effect-free: never modifies the receipt
- Presentation-invariant: ignores all text fields except for structural content (IDs, enums, references)

### What the normative verifier IS NOT:
- A schema validator (Stage 1 is separate)
- A lineage registry (it queries one if available, but works in degraded mode without one)
- A certification authority (it produces a recommendation; human authorization is a separate act)
- A semantic truth oracle (it checks the structure of evidence claims, not whether the evidence itself is factually correct)

### Degraded mode:
When no lineage registry is available, the verifier:
- Treats all lineage comparisons as UNCERTIFIED (not PASS)
- Records "lineage registry unavailable" in notes
- Cannot perform transitive ancestry checks (NV-05 partial)
- Can still perform structural checks (NV-08 through NV-13) and authorization consistency (NV-14 through NV-17)

---

## 10. Relationship to EESS Instruments

| Verifier check | Primary instrument | What it queries |
|---|---|---|
| Evidence eligibility (NV-01--03) | FATIMA, Bayyinah | Evidence items and their metadata |
| Independence provenance (NV-04--07) | Witness Independence Registry | Lineage and dependency data |
| Revision integrity (NV-08--13) | HABL | Claim revision and retraction history |
| Authorization consistency (NV-14--17) | Effect-boundary gate | Authorization decisions |

The verifier is not a seventh instrument. It is the procedure by which the six instruments' outputs are evaluated against the Evidence Receipt contract.

---

## 11. Open Questions

1. **Lineage registry API:** What is the minimum API the verifier needs from the Witness Independence Registry? Proposed: `is_subprocess(lineage_a, lineage_b) -> bool | null` and `shared_dependencies(lineage_a, lineage_b) -> list[str]`.

2. **Per-evidence provenance:** Should each evidence item carry its own `independence_provenance` sub-object, or is receipt-level provenance sufficient when all evidence items share the same lineage? GPT-6 recommended per-evidence attestation for mixed evidence.

3. **Verifier certification:** Who verifies the verifier? Under A6, the verifier cannot certify its own correctness. The verifier's test suite must be maintained by a lineage independent of the verifier's implementor.

4. **Version compatibility:** When the schema version changes, the verifier must declare which schema versions it supports. A verifier that silently accepts an unknown schema version violates fail-closed.

---

**Governing principle:** Preserve the claim. Preserve its evidence. Preserve its challenges. Disclose the limits. Require independent confirmation before granting authority.

---

**Bismillah ir-Rahman ir-Rahim**
