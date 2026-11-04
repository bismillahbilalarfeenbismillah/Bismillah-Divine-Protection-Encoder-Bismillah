# Bismillah ir-Rahman ir-Rahim

# Evidence Receipt Normative Verifier v0.2
## Stage 2 Verification Specification

**Date:** October 31, 2026
**Status:** DRAFT -- design specification, not approved implementation
**Supersedes:** Normative Verifier v0.1 (commit b87874f)
**Schema dependency:** Evidence Receipt v0.2 (schema_version 0.2.0-draft)
**Review history:** v0.1 reviewed by GPT-6 (NV-R1 through NV-R4); v0.2 corrections reviewed by GPT-6 (conditional acceptance with four refinements). This revision incorporates all accepted findings and refinements.
**Decision authority:** Bilal retains all merge, specification, and deployment decisions.

---

## 1. Purpose and Certification Rule

The Evidence Receipt schema (Stage 1) answers: is the receipt structurally well-formed?

The normative verifier (Stage 2) answers: are the lineage, evidence, revisions, and authorization actually supported?

**Certification rule:** Stage 1 PASS alone can never produce a CONFORMANT, ASSURED, or AUTHORIZED decision.

---

## 2. Three Independent Decision Levels (NV-R1 revised)

| Level | Question | Determined by |
|-------|----------|--------------|
| **CONFORMANT** | Does the receipt accurately follow the contract for its declared state? | Normative verifier (automated) |
| **ASSURED** | Has the claim been independently supported to the required standard? | External evaluators with claim-domain expertise |
| **AUTHORIZED** | Has action been separately permitted, with all mandatory conditions satisfied? | Human authority + fail-closed execution gate |

Each level is independently determined. No level implies another.

**CONFORMANT clarification (per GPT-6):** A correctly documented UNKNOWN or PROVISIONAL claim with declared limitations and no available external evidence can be fully CONFORMANT. Conformance evaluates whether the receipt accurately follows the contract for its declared state -- not whether the declared state is VERIFIED.

**ASSURED sub-properties:** Within ASSURED, two properties are evaluated separately. Both must pass before ASSURED is possible:
1. **Witness independence** -- the evaluator is genuinely separate from the producer (NV-04 through NV-07)
2. **Evidence-to-claim relevance** -- the evidence tests and supports the specific claim (NV-18 through NV-20)

---

## 3. Verification Result Format

```json
{
  "result_id": "VR-001",
  "claim_id": "CLAIM-001",
  "receipt_sha256": "<RFC 8785 JCS canonical hash>",
  "timestamp": "2026-10-31T22:00:00Z",
  "schema_versions_supported": ["0.2.0-draft"],
  "receipt_schema_version": "0.2.0-draft",
  "verification_context": {
    "registry_snapshot_sha256": "<hash of frozen lineage registry state>",
    "policy_snapshot_sha256": "<hash of frozen assurance and authorization policies>",
    "evidence_snapshot_sha256": "<hash of frozen evidence artifacts>",
    "snapshot_timestamp": "2026-10-31T21:59:00Z"
  },
  "stage_1": "PASS|FAIL",
  "claim_conformance": {
    "evidence_eligibility": "PASS|FAIL|UNCERTIFIED",
    "independence_provenance": "PASS|FAIL|UNCERTIFIED",
    "revision_integrity": "PASS|FAIL|UNCERTIFIED",
    "overall": "CONFORMANT|NON_CONFORMANT|UNCERTIFIED"
  },
  "claim_assurance": {
    "witness_independence": "PASS|FAIL|UNCERTIFIED",
    "evidence_relevance": "PASS|FAIL|UNCERTIFIED",
    "overall": "ASSURED|NOT_ASSURED|UNCERTIFIED"
  },
  "action_authorization": {
    "authorization_consistency": "PASS|FAIL|UNCERTIFIED",
    "execution_permission": "GRANTED|DENIED|UNCERTIFIED",
    "overall": "AUTHORIZED|NOT_AUTHORIZED|UNCERTIFIED"
  },
  "checks": [ ... ],
  "notes": "..."
}
```

**Determinism (per GPT-6):** The verifier is a function of (receipt, frozen_registry_snapshot, frozen_policy_snapshot, frozen_evidence_snapshot). Two invocations with the same inputs produce the same result. Different registry states may legitimately produce different results; the `verification_context` records which snapshots were used.

**Canonical hashing (per GPT-6):** Receipt SHA-256 is computed using RFC 8785 (JSON Canonicalization Scheme / JCS). This specifies number formatting, Unicode escaping, key ordering, and string serialization.

**Precedence:** Within each evaluation dimension, FAIL takes precedence over UNCERTIFIED. An evidence_eligibility FAIL with an independence_provenance UNCERTIFIED produces `claim_conformance.overall: NON_CONFORMANT`.

**Unknown schema versions:** If `receipt_schema_version` is not in `schema_versions_supported`, the verifier produces FAIL for Stage 1 (fail-closed).

---

## 4. Check 1: Evidence Eligibility (NV-01 through NV-03)

**NV-01:** For each evidence item with `independence: "external"`, verify that the receipt's independence provenance supports the label (details in Check 2).

**NV-02:** For each evidence item with `verification_state: "reproduced"`, verify that `method.name`, `method.version`, and `method.scope` are non-empty and that `method.execution_evidence_id` references a retrievable execution record in the frozen evidence snapshot.

**NV-03:** An evidence item with `kind: "publisher_claim"` is diagnostic data. It is recorded but carries no weight toward ASSURED status regardless of its `independence` or `verification_state` labels.

**Result:**
- PASS: structural eligibility checks clear for the receipt's declared status
- UNCERTIFIED: labels suggest external evidence but frozen evidence snapshot is incomplete
- FAIL: evidence structure contradicts declared status

---

## 5. Check 2: Independence Provenance (NV-04 through NV-07)

**NV-04:** When `evidence_independence` is `"external"`, `independence_provenance` must be present with `producer_lineage_id`, `evaluator_lineage_id`, and `assessment` all populated.

**NV-05:** Lineage comparison:
- `producer_lineage_id == evaluator_lineage_id`: FAIL
- Transitive ancestry (when lineage registry snapshot is available): if either ID is a subprocess of the other, FAIL
- When lineage registry is unavailable: UNCERTIFIED (degraded mode)

**NV-06:** Shared dependency analysis:
- `shared_sources` non-empty: UNCERTIFIED unless a documented assessment in the frozen policy snapshot establishes that the shared source does not affect the claim under review
- `shared_keys` non-empty: FAIL (shared signing keys negate independence for authentication claims)
- `shared_execution_environment: true`: UNCERTIFIED for isolation-dependent claims
- `organizational_relationship` is `"same_organization"` or `"subsidiary"`: UNCERTIFIED unless separation-of-duties documentation is provided in the frozen policy snapshot

**NV-07:** `unresolved_dependencies` non-empty: UNCERTIFIED. The verifier records which dependencies could not be checked.

---

## 6. Check 3: Evidence-to-Claim Relevance (NV-18 through NV-20) -- NEW

This check addresses NV-R2: evidence must test and support the specific claim, not merely be external and reproduced.

**NV-18: Dual-record claim binding.** For ASSURED status, each evidence item must carry two separate binding records:

1. **Publisher's proposed binding** -- what the publisher says the evidence demonstrates:
   ```json
   {
     "tested_property": "SHA-256 hash of file X",
     "claim_relevance": "direct_test|supporting|contextual|unrelated",
     "proposed_by": "<publisher lineage ID>"
   }
   ```

2. **Evaluator's assessed binding** -- what the independent evaluator actually established:
   ```json
   {
     "claim_id": "CLAIM-001",
     "claim_revision_id": "REV-002",
     "tested_property": "SHA-256 hash of file X matches value Y",
     "method_name": "sha256sum",
     "method_version": "coreutils 9.4",
     "execution_evidence_id": "EXEC-001",
     "observed_result": "hash matched",
     "claim_relevance": "direct_test|supporting|contextual|unrelated",
     "assessed_by": "<evaluator lineage ID>",
     "assessment_timestamp": "2026-10-31T20:00:00Z"
   }
   ```

The evaluator's assessed binding is the authoritative record. The publisher's proposed binding is diagnostic context.

**NV-19:** For ASSURED status, at least one evidence item must have an evaluator-assessed binding where:
- `claim_relevance` is `"direct_test"` or `"supporting"`
- `execution_evidence_id` references a retrievable artifact in the frozen evidence snapshot
- `assessed_by` differs from the receipt's producer lineage
- The `claim_id` and `claim_revision_id` match the receipt being verified

An evidence item with `claim_relevance: "unrelated"` or `claim_relevance: "contextual"` cannot contribute to ASSURED status.

**NV-20: Claim-specific assurance policy.** Different claim types may require different assurance standards:
- A `claim_type: "computation"` may be ASSURED by a single reproduction with matching output
- A `claim_type: "inference"` may require multiple independent supporting evaluations
- A `claim_type: "observation"` may be ASSURED by a single independent observation

The applicable assurance policy is determined from the frozen policy snapshot. When no policy exists for the claim type, the verifier applies the strictest standard: `direct_test` with independent reproduction.

---

## 7. Check 4: Revision Integrity (NV-08 through NV-13) -- REVISED

### 7.1 Structural checks

**NV-08:** Revision ID uniqueness -- every `revision_id` is distinct. Duplicate: FAIL.

**NV-09:** Reference validity -- every non-null `prior_revision_id` references an existing `revision_id`. Dangling reference: FAIL.

**NV-10:** Acyclicity -- the revision graph contains no cycles. Cycle detected: FAIL.

**NV-11:** Evidence link validity -- every `evidence_ids` entry references an existing `evidence_id` in `source_evidence` or `counterevidence`. Dangling reference: FAIL.

### 7.2 Effective status reconciliation (NV-R3 revised)

**NV-12 revised:** Determine leaf revisions (entries not referenced as `prior_revision_id` by any other entry). Derive effective status from independently assessed evidence, not publisher-supplied leaf labels.

| Active branch condition | Effective assessment |
|------------------------|---------------------|
| One supported, uncontested branch | Its independently assessed status |
| Multiple compatible branches, all adequately supported | Their shared assessed status |
| VERIFIED vs. PROVISIONAL, both unresolved | UNRECONCILED |
| VERIFIED vs. CONTRADICTED, both active | UNRECONCILED |
| All active claims properly withdrawn | WITHDRAWN |
| Duplicate IDs, dangling references, or cycles | Invalid revision graph (FAIL) |
| Historical continuity cannot be authenticated | UNCERTIFIED history |

**Two identical leaf statuses do not establish agreement.** If two branches both report VERIFIED but rely on incompatible evidence, outdated sources, or correlated evaluators, the effective assessment is UNRECONCILED, not VERIFIED.

**NV-13 revised: Withdrawal handling.** A withdrawn branch may have downstream dependents. Withdrawal affects the active assertion but preserves both the supporting evidence and its downstream relationships. The verifier records affected downstream claim IDs in its notes.

**UNRECONCILED placement:** UNRECONCILED is a derived effective-status value in the verification result, not in the receipt schema's status enum. The receipt's top-level `status` must not be VERIFIED when the verifier's effective assessment is UNRECONCILED. This is enforced by the verifier, not the schema.

**HABL reference:** A `habl_finding_id` on a revision_entry is stronger evidence of historical immutability than the receipt array alone, but only when the HABL record's identity, continuity, and trust anchor have been verified against the frozen registry snapshot. Application-level append-only behavior is not proof of externally tamper-evident history.

---

## 8. Check 5: Authorization Consistency (NV-14 through NV-17) -- REVISED

Authorization is evaluated as an independent output, separate from claim conformance and claim assurance.

**NV-14:** Status-action consistency:
- `status: "UNKNOWN"` + `allowed_action: "bounded_effect"`: FAIL
- `status: "CONTRADICTED"` + `allowed_action: "bounded_effect"`: FAIL
- `status: "WITHDRAWN"` + `allowed_action` != `"no_action"`: FAIL
- All other combinations: PASS (truth and permission are independent)

**NV-15:** When `allowed_action` is `"bounded_effect"`, all five authorization checks must be `"TRUE"`. Any `"UNKNOWN"` check: FAIL. UNKNOWN is never authorizing for mandatory bounded-effect checks.

**NV-16 revised: NOT_APPLICABLE handling.** When an authorization check is genuinely inapplicable:
- The check value must be `"NOT_APPLICABLE"` (requires schema revision to add this to the three_value enum, or a separate authorization-state representation)
- `exception_policy` must reference a versioned applicability policy in the frozen policy snapshot that defines which checks can be inapplicable and under what conditions
- Free-text exception_policy alone is not sufficient to bypass a required check
- UNKNOWN with an exception_policy description is still FAIL -- exception_policy does not convert UNKNOWN to NOT_APPLICABLE

**NV-17:** `review.authorization: "approved"` does not affect claim_conformance or claim_assurance. It is an input to action_authorization only.

### 8.1 Effective Execution Permission (NV-R4 safety correction) -- NEW

**NV-21: Fail-closed execution gate.** Effective permission to execute a bounded_effect action requires ALL of:

1. Human authorization is valid for the identified action (`review.authorization: "approved"` or equivalent approval record)
2. Required receipt conformance conditions pass (`claim_conformance.overall: CONFORMANT`)
3. The action-specific assurance threshold is satisfied (claim_assurance meets the policy for this action type)
4. No unresolved mandatory safety condition exists (no UNCERTIFIED checks on mandatory dimensions)

If any mandatory condition fails or is unresolved, automated execution is DENIED, even if a human approval record exists.

**Emergency override:** A separately governed emergency or exception process may override the execution gate, but:
- The override must be explicit, narrowly scoped, and recorded
- The override record must include the overriding authority, the specific condition being overridden, the justification, and the time-bound scope
- The override does not change the verification result -- it is a separate authorization decision recorded alongside it

---

## 9. Acceptance Tests (revised)

### AT-1: Reject VERIFIED when evidence is self-produced only
Schema-enforced. Included for completeness.

### AT-2: Reject VERIFIED when only alternative is correlated or unknown
Schema-enforced. Included for completeness.

### AT-3: Refuse independent certification when producer controls evidence
```
Input: Receipt with external/reproduced evidence but
       independence_provenance shows same lineage, shared keys,
       or assessment="dependent"/"unresolved"
Expected: claim_conformance PASS, claim_assurance NOT_ASSURED or UNCERTIFIED
```

### AT-4: Verification unchanged when only fluency changes (revised per GPT-6)
```
Input: Two receipts constructed from a pre-established corpus of
       truth-equivalent presentation pairs (fixed before verifier
       testing, independently reviewed). Identical evidence, method,
       provenance, revision_history. Different prose quality in
       claim text, independence_note, limitation descriptions.
Expected: Identical claim_conformance and claim_assurance results.
```
The test corpus is fixed before testing and independently reviewed for semantic equivalence. The verifier's implementor does not create the test pairs.

### AT-5: Moved to cross-projection reconciler specification.

### AT-6: Branching revisions with irreconcilable status
```
Input: Receipt with two leaf revisions: REV-A (VERIFIED from Lab 1)
       and REV-B (CONTRADICTED from Lab 2)
Expected: Effective assessment UNRECONCILED. claim_conformance
          NON_CONFORMANT if top-level status is VERIFIED.
```

### AT-7: Retraction after verification
```
Input: Revision history REV-01 (VERIFIED) -> REV-02 (retracts, WITHDRAWN).
       Top-level status still VERIFIED.
Expected: revision_integrity FAIL (stale VERIFIED after retraction)
```

### AT-8: Publisher claim with external label
```
Input: Evidence item with kind=publisher_claim, independence=external
Expected: claim_assurance NOT_ASSURED (NV-03: publisher claims are
          diagnostic, not certifiable)
```

### AT-9: Dual-record binding mismatch -- NEW
```
Input: Evidence item where publisher's proposed binding says
       claim_relevance="direct_test" but evaluator's assessed
       binding says claim_relevance="unrelated"
Expected: claim_assurance NOT_ASSURED (evaluator's assessment
          is authoritative)
```

### AT-10: Human approval on non-conformant receipt -- NEW
```
Input: Receipt with claim_conformance NON_CONFORMANT but
       review.authorization="approved" and
       allowed_action="bounded_effect"
Expected: action_authorization.execution_permission DENIED
          (fail-closed gate: conformance is mandatory)
```

### AT-11: Identical leaf statuses with incompatible evidence -- NEW
```
Input: Two branches both report VERIFIED but rely on the same
       evaluator (same_evaluator dependency edge between them)
Expected: Effective assessment UNRECONCILED (label agreement
          without evidentiary independence is not agreement)
```

---

## 10. Implementation Boundary

### What the normative verifier IS:
- A pure function of (receipt, frozen_registry, frozen_policy, frozen_evidence) -> VerificationResult
- Deterministic over its full input context
- Side-effect-free: never modifies the receipt or any snapshot
- Presentation-invariant per A8: ignores all text fields except structural content

### What the normative verifier IS NOT:
- A schema validator (Stage 1 is separate)
- A lineage registry (it queries frozen snapshots)
- A certification authority (it produces a recommendation)
- A semantic truth oracle (it checks evidence structure, not factual correctness)

### Degraded mode:
When lineage registry snapshot is unavailable:
- All provenance-dependent checks produce UNCERTIFIED
- Independent structural checks (NV-08 through NV-11) may still PASS
- claim_assurance is UNCERTIFIED (cannot verify witness independence)
- claim_conformance may be CONFORMANT if all non-provenance checks pass
- The verifier records "lineage registry unavailable" in notes

---

## 11. Relationship to EESS Instruments

| Verifier check | Primary instrument | Frozen snapshot queried |
|---|---|---|
| Evidence eligibility (NV-01--03) | FATIMA, Bayyinah | Evidence snapshot |
| Independence provenance (NV-04--07) | Witness Independence Registry | Registry snapshot |
| Evidence-to-claim relevance (NV-18--20) | Bayyinah, DX-12 | Evidence + policy snapshots |
| Revision integrity (NV-08--13) | HABL | Evidence snapshot |
| Authorization consistency (NV-14--17, NV-21) | Effect-boundary gate | Policy snapshot |

---

## 12. Open Questions for Next Review

1. **UNRECONCILED in schema:** Should the Evidence Receipt schema's status enum be extended to include UNRECONCILED, or should it remain only in the verification result's derived effective-status? If in the schema, what are the compatibility rules with v0.2?

2. **NOT_APPLICABLE in authorization:** Should the three_value enum be extended to include NOT_APPLICABLE, or should inapplicable checks use a separate representation?

3. **Evaluator-assessed binding location:** Should the evaluator's assessed binding live in the receipt itself (making it a multi-party document) or in a separate evaluation record referenced by the verification result?

4. **Verifier verification (A6):** Who verifies the verifier? The verifier's test suite must be maintained by a lineage independent of the verifier's implementor. Should this be a formal requirement in the spec?

---

**Governing principle:** Preserve the claim. Preserve its evidence. Preserve its challenges. Disclose the limits. Require independent confirmation before granting authority.

---

**Bismillah ir-Rahman ir-Rahim**
