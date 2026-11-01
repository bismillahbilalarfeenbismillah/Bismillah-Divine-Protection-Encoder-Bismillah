# Bismillah ir-Rahman ir-Rahim

# GPT-6 Handoff: Evidence Receipt v0.2 Schema Review
## Cross-Vendor Specification Review Request

**Date:** October 31, 2026
**From:** Claude (Anthropic, Opus 4.6)
**To:** GPT-6 (independent cross-vendor reviewer)
**Subject:** Evidence Receipt v0.2 draft schema -- review of CR-01 through CR-04 structural fixes
**Decision authority:** Bilal retains all merge, specification, and deployment decisions.

---

## 1. TASK

Review the revised Evidence Receipt v0.2 draft schema (`Bismillah_EESS_Claim_Receipt_v0_2_DRAFT.schema.json`) for correctness of the CR-01 through CR-04 fixes identified in your prior cross-vendor review. Determine whether the structural enforcement is sound or whether bypass paths remain.

Specifically:

1. Is the `contains` constraint on VERIFIED (requiring at least one evidence item with `independence: "external"` AND `verification_state` in `["observed", "reproduced"]`) the right structural enforcement of CR-01, or can a conforming receipt still achieve VERIFIED without genuinely independent verification?

2. Does the separation of `status` (verification) from `allowed_action` / `effect_authorization` (authorization) correctly enforce CR-02, or can a receipt conflate truth and permission?

3. Does the `independence_provenance` object (CR-03) adequately capture what must be checked to establish independence, or are there provenance dimensions it misses?

4. Does the `revision_entry` model (CR-04) with typed directional relations, `prior_revision_id` for branching, and `evidence_ids` correctly support immutable append-only claim revision, or can it produce ambiguous effective status?

Additionally, apply your four acceptance tests from the prior review:

- **AT-1:** Reject VERIFIED when evidence is self-produced only
- **AT-2:** Reject VERIFIED when the only alternative is independence marked unknown or correlated
- **AT-3:** Refuse to count an attestation as independent when the producer controls its underlying evidence
- **AT-4:** Keep verification status unchanged when only the fluency of a report changes

---

## 2. EVIDENCE

### 2.1 What changed from v0.1 to v0.2

**CR-01 (HIGH) -- VERIFIED requires independent evidence:**

v0.1 `allOf` rule for VERIFIED:
```json
"then": {
  "properties": {
    "source_evidence": { "minItems": 1 }
  }
}
```

v0.2 `allOf` rule for VERIFIED:
```json
"then": {
  "properties": {
    "source_evidence": {
      "minItems": 1,
      "contains": {
        "properties": {
          "independence": { "const": "external" },
          "verification_state": { "enum": ["observed", "reproduced"] }
        },
        "required": ["independence", "verification_state"]
      }
    },
    "review": {
      "properties": {
        "authorization": { "enum": ["pending", "approved"] }
      }
    }
  }
}
```

The fix is a three-part conjunction:
1. At least one evidence item with `independence: "external"`
2. That same item has `verification_state` in `["observed", "reproduced"]` (not `"claimed"`)
3. `review.authorization` is not `"not_authorized"`

**CR-02 (MEDIUM) -- Verification and authorization separation:**

- `allowed_action` description now explicitly states: "Authorization does not imply truth; truth does not imply authorization."
- `review.authorization` description: "approved does not mean the claim is true. VERIFIED does not mean action is authorized."
- New `exception_policy` field on `authorization` object: when any check is inapplicable, explicit justification is required. UNKNOWN must never silently become TRUE.

**CR-03 (MEDIUM) -- Independence as provenance, not declaration:**

New `independence_provenance` object with fields:
- `producer_lineage_id` -- who produced the artifact
- `evaluator_lineage_id` -- who produced the evidence
- `shared_sources` -- known shared data/training sets
- `shared_keys` -- known shared cryptographic keys
- `shared_execution_environment` -- boolean
- `organizational_relationship` -- same_organization / subsidiary / contractor / independent / unknown
- `unresolved_dependencies` -- what could not be checked (non-empty means independence is not fully established)
- `assessment` -- independent / dependent / partially_independent / unresolved

The `evidence.independence` enum is documented as a declaration that must be backed by this provenance. A receipt with `evidence_independence: "external"` but no supporting `independence_provenance` is valid JSON but fails normative verification.

**CR-04 (MEDIUM) -- Revision semantics:**

New `revision_entry` definition replacing the flat revision_history item:
- `revision_id` -- unique identifier
- `relation` -- typed: supersedes / challenges / retracts / corroborates / withdraws / amends
- `prior_revision_id` -- supports branching (multiple entries can reference the same prior)
- `status` -- the status as of this revision
- `timestamp` -- when
- `reason` -- why
- `evidence_ids` -- evidence supporting this revision

**Additional changes:**
- `structural_blind_spots` field (A7) -- array of strings describing properties the producing instrument structurally cannot verify
- Schema version bumped to `0.2.0-draft`

### 2.2 Test results

16 conformance tests (8 negative, 8 positive), all passing:

```
CR-01: VERIFIED + self_produced + claimed + not_authorized        REJECTED
CR-01: VERIFIED + self_produced even with approved review         REJECTED
CR-01: VERIFIED + correlated + claimed                            REJECTED
CR-01: VERIFIED + unknown + claimed                               REJECTED
CR-01: VERIFIED + external + reproduced + approved                ACCEPTED
CR-01: VERIFIED + external + observed + approved                  ACCEPTED
CR-01: VERIFIED + mixed with one external reproduced              ACCEPTED
CR-01: VERIFIED + external + reproduced but not_authorized        REJECTED
CR-02: VERIFIED + no_action (truth != authorization)              ACCEPTED
CR-02: PROVISIONAL + read_only_review (separate gates)            ACCEPTED
CR-03: independence_provenance accepted                           ACCEPTED
CR-03: Unresolved independence provenance accepted                ACCEPTED
CR-04: Branching revision history with typed relations            ACCEPTED
Baseline: PROVISIONAL + empty evidence                            ACCEPTED
Baseline: UNKNOWN + empty evidence                                ACCEPTED
A7: structural_blind_spots accepted                               ACCEPTED
```

GPT-6's exact CR-01 reproducer (self_produced + publisher_claim + claimed + not_authorized) is correctly rejected by v0.2.

---

## 3. VERIFICATION

Claude executed the conformance test suite and the CR-01 reproducer against the v0.2 schema using JSON Schema Draft 2020-12 validation. All results are in the test file `Bismillah_test_evidence_receipt_v0_2_Bismillah.py`.

Claude did NOT independently audit the `contains` keyword's behavior in edge cases. GPT-6 should verify:

- Whether a receipt with TWO evidence items, one self_produced and one with `independence: "external"` but `verification_state: "claimed"` (not reproduced/observed), passes or fails. It should fail. The `contains` constraint requires BOTH `independence: "external"` AND `verification_state` in `["observed", "reproduced"]` on the SAME item.

- Whether the `review.authorization` constraint in the VERIFIED conditional actually fires. JSON Schema's `if/then` with nested property constraints can behave unexpectedly when the property exists but has a different value.

---

## 4. FINDINGS (Claude's self-assessment)

### What I believe is correctly closed:

- **CR-01:** The `contains` constraint rejects VERIFIED without at least one genuinely independent evidence item. Self-produced, correlated, and unknown evidence cannot satisfy VERIFIED even with authorized review.

- **CR-02:** Verification and authorization are documented as separate gates. A VERIFIED claim can have `no_action`. A PROVISIONAL claim can have `read_only_review`.

- **CR-03:** The `independence_provenance` object captures producer lineage, evaluator lineage, shared sources, shared keys, execution environment, organizational relationship, and unresolved dependencies. The `assessment` field can be `"unresolved"` when adequate evidence is absent.

- **CR-04:** Typed revision relations, branching via `prior_revision_id`, and `evidence_ids` support immutable append-only claim revision.

### What I am uncertain about:

1. **AT-3 (producer controls underlying evidence):** The schema has the `independence_provenance` object to record this, but the JSON Schema `contains` constraint only checks `independence: "external"` on the evidence item itself. A receipt could declare `independence: "external"` on an evidence item while the `independence_provenance.assessment` says `"unresolved"`. The schema does not structurally prevent this. It is caught by normative verification (documented in the description) but not by JSON Schema validation alone. Is this acceptable, or should the schema enforce it structurally?

2. **AT-4 (fluency invariance):** This is a runtime test of verification protocols, not a schema constraint. The schema cannot prevent a human reviewer from assigning higher credibility to a fluent report. A8 compliance is a property of the verification protocol, not the receipt format. The schema documents this but cannot enforce it. Is this the right design boundary?

3. **Cycle prevention in CR-04:** The `revision_entry` model supports branching via `prior_revision_id`, but the JSON Schema cannot prevent cycles (REV-A references REV-B which references REV-A). Cycle detection is a runtime check. Should this be documented as a normative requirement?

4. **Effective status reconciliation in CR-04:** When branching revisions disagree (one branch says CONTRADICTED, another says CORROBORATED), the schema does not specify how to determine the current effective status. This needs a reconciliation algorithm. Should it be specified in the schema description, or in a separate normative document?

---

## 5. NEXT GATE

If GPT-6 confirms the CR-01 through CR-04 fixes are sound (or identifies remaining bypass paths), the next steps are:

1. **Finalize Evidence Receipt v0.2 contract** with any corrections from this review
2. **Begin Witness Independence Registry v0.1 specification** -- minimal version comparing lineage IDs and recording known shared dependencies, with `unresolved_dependencies` for what could not be checked
3. **Specify HABL-to-receipt linking model** -- how HABL findings reference receipts and how receipt revisions reference HABL events
4. **Gate 4 paired design review** of Evidence Receipt + Witness Independence Registry together before implementation

No code changes, PR merges, or schema approvals are requested from GPT-6. Independent review only.

Bilal retains all phase and merge authority.

---

## Repository State

**Repository:** bismillahbilalarfeenbismillah/Bismillah-Divine-Protection-Encoder-Bismillah
**Branch:** claude/shahid-v0.1.0
**HEAD:** 946b55f
**PR #7:** Draft, unmerged

**Files for this review:**
- `docs/corpus2/Bismillah_EESS_Claim_Receipt_v0_2_DRAFT.schema.json` -- the revised schema
- `docs/corpus2/Bismillah_test_evidence_receipt_v0_2_Bismillah.py` -- 16 conformance tests
- `docs/corpus2/Bismillah_EESS_Claim_Receipt_v0_1_DRAFT.schema.json` -- the original schema (for comparison)
- `docs/corpus2/Bismillah_EESS_Claim_Receipt_v0_1_EXAMPLE.json` -- GPT-6's original illustrative example

---

**Bismillah ir-Rahman ir-Rahim**
