# Bismillah ir-Rahman ir-Rahim

# EESS Collected Works & Differentiator Strategy Analysis

## Corpus-Derived Requirements for Stack Improvement

**Analyst:** Claude (Anthropic, Opus 4.6) for Bilal Syed Arfeen
**Date:** October 2026
**Source corpus:** Bayyinah Collected Works (79 papers + 995 legacy records + Kun Fayakun) and Master Differentiator Strategy v1.0
**Relationship to Design Brief v2.1:** This analysis extends v2.1's R1--R7 with six additional requirements (R8--R13) derived from the full corpus

---

## 1. Corpus Structure

The analyzed corpus contains:

- **79 unique paper editions** across 4 thematic parts (Theology, Structural Honesty, Technology, Public Applications)
- **995 legacy historical records** in a flat CSV index (R0001--R0995)
- **Kun Fayakun** (full book, Part VI)
- **Master Differentiator Strategy v1.0** -- a 600+ line synthesis document containing the DX-12 protocol, 10 experiment types, 12-metric scorecard, 24-sector domain adapter schema, and the five-service MVP architecture
- **Source Registry JSON** -- 79 entries with SHA-256 hashes, origin file paths, page counts, and module mappings

### 1.1 Three-Column Architecture

The corpus organizes into three columns that map directly to the EESS:

| Column | Parts | Role | EESS Mapping |
|---|---|---|---|
| Theory | I--II | Theological grounding + axiom-level specification | Design principles, Muraqabah Triad |
| Implementation | III | Code, formats, tools | FATIMA, Furqan, furqan-lint, HABL |
| Reproduction | IV | Real-world datasets with audit ledgers | Evidence Receipt SDK (existing pattern) |

**Critical finding:** Part IV already contains working evidence receipts. Papers P069 (al-Amana provenance), P001 (reproduction dataset), P060 (procurement audit ledger), and P063 (allocation audit ledger) implement the exact pattern the Evidence Receipt SDK should formalize. The SDK is an extraction and generalization, not a new invention.

---

## 2. Confirmed Design Principles (Already in v2.1)

The full corpus reinforces these principles without modification:

1. Preservation before protection claims (hifz before himaya)
2. Muraqabah Triad separation (FATIMA observes, HABL records, Shahid testifies)
3. Incompleteness Boundary (no system verifies its own honesty)
4. Uninspected dimensions (no concealed limitation)
5. L5 countermeasure (sidecar witness survives memory alteration)

---

## 3. Requirements Already in Design Brief v2.1

- **R1 (HIGH):** Five-lane evidence taxonomy (SRC, CODE, MEAS, PLAN, HYP) -- *implemented in shahid.py*
- **R2 (HIGH):** NOT_EVALUATED status -- *implemented in shahid.py*
- **R3 (MEDIUM):** Three-tier claim classification (T1 verified, T2 structural, T3 predictive)
- **R4 (MEDIUM):** Observation invariance testing (CIT)
- **R5 (MEDIUM):** Six adaptive guardrails as self-audit
- **R6 (LOW):** Evidence receipt format (Phase 4+)
- **R7 (DECISION REQUIRED):** E/H/I/P claim taxonomy vs R1 five lanes

---

## 4. New Requirements from Full Corpus

### R8. DX-12 Audit Pipeline (HIGH -- Bayyinah v0.2)

**Source:** Differentiator Strategy, Section 12

The DX-12 protocol is a twelve-stage differentiator workflow with required outputs, refusal conditions, and reversal paths for every stage:

| Stage | Deliverable | Stop Condition |
|---|---|---|
| DX-01 Beneficiary | Legitimate-objective charter | Objective requires exploiting a third party |
| DX-02 System map | Causal system map | Critical actors unidentifiable |
| DX-03 Asset & harm map | Threat model + privacy assessment | Evaluation itself creates unacceptable harm |
| DX-04 Hypotheses | Rival-hypothesis matrix | Claim is unfalsifiable |
| DX-05 Baselines | Frozen baseline register | No credible denominator exists |
| DX-06 Claims | Claim ledger | Sources absent or self-authenticated only |
| DX-07 Tests | Preregistered test pack | Leakage invalidates comparisons |
| DX-08 Discrimination | Error-and-equity report | Signal does not beat simpler baselines |
| DX-09 Effects | Bounded effect contract | Permission, scope, or witness is UNKNOWN |
| DX-10 Remedy | Repair/redesign plan | Intervention could harm more than problem |
| DX-11 Measurement | Outcome dashboard | Benefit vanishes outside test environment |
| DX-12 Review | Signed revision and decision record | Evidence changes or safety trigger crossed |

**Impact:** Bayyinah v0.2 should implement DX-12 as its standard audit pipeline. Each stage produces a HABL finding with evidence lane and tier. The "stop conditions" become mandatory HABL findings of type NOT_EVALUATED or VIOLATED.

### R9. Mandatory Hypothesis Competition (HIGH -- HABL v0.2)

**Source:** Differentiator Strategy, Section 12.2

For any anomalous output, HABL must register at least five rival hypotheses:

- **H0:** Ordinary error, incomplete context, format mismatch
- **H1:** Benign optimizer overfitting a performance metric
- **H2:** Process weakness (permission confusion, evidence leakage)
- **H3:** Strategic behavior contingent on oversight or reward
- **H4:** Deliberate tampering with source, logs, or evaluator

Each hypothesis must identify its discriminating observation and potential refutation. A HABL finding that mechanically forces every case into a single hypothesis contradicts the evidence tiers.

**Impact:** HABL Finding gains a `rival_hypotheses` field -- a list of at least H0 and the supported hypothesis, each with its discriminating test.

### R10. Domain Adapter Schema (MEDIUM -- Phase 4+)

**Source:** Differentiator Strategy, Section 27

A machine-parseable YAML format for deploying EESS instruments in specific sectors:

```yaml
adapter_id: "DX-DOMAIN-001"
domain: "example"
legitimate_outcome: "measurable user/public benefit"
generator_object: "artifact, decision, allocation, or action"
evaluator_and_incentives: "who selects and why"
evidence_inputs: ["origin record", "independent benchmark"]
competing_hypotheses: ["ordinary error", "metric gaming", "tampering"]
primary_risks: ["surface/substrate mismatch", "unsafe effect"]
controls: ["provenance", "held-out tests", "external authorization"]
metric_denominator: "explicit eligible case population"
refutation: "finding that would disprove the preferred mechanism"
unknown_policy: "escalate; do not perform irreversible action"
appeal_owner: "named, independent authority"
review_window: "defined in advance"
```

**Impact:** The Sector Adapter Toolkit (Priority 6 from Build it Yourself analysis) gains a concrete schema. 24 sectors are mapped in the Differentiator Strategy with specific controls.

### R11. Investigation Dossier Format (MEDIUM -- Shahid v0.1.1)

**Source:** Differentiator Strategy, Section 12.1

A Shahid report should include a six-line top sheet:

1. Question
2. Target outcome
3. System boundary
4. Best-supported current finding
5. Competing interpretation
6. Permitted next action

Behind it: causal diagram, evidence ledger, test results, authorized effects, affected-party safeguards, signed limitations. Reports must permit UNKNOWN and NO-DECISION.

**Impact:** ShahidReport gains optional `investigation_dossier` field with the six-line structure. DimensionFinding already supports UNKNOWN through evidence lanes.

### R12. Twelve-Metric Performance Scorecard (MEDIUM -- Phase 4)

**Source:** Differentiator Strategy, Section 14

Standardized metrics for EESS instrument self-assessment:

| Metric | Favorable Direction |
|---|---|
| Objective attainment | Up |
| Structural mismatch rate | Down |
| False-positive rate | Down |
| False-negative rate | Down |
| Observation-sensitivity (CIT) | Toward 0 |
| Independent-witness coverage | Up |
| Provenance completeness | Up |
| Unknown-safe decision rate | Up |
| Rare-mode coverage | Up |
| Reversal latency | Down |
| Dependency reduction | Up |
| Harm-adjusted total value | Up |

**Impact:** Each EESS instrument's README documents which metrics it tracks. Shahid reports these metrics per inspection period.

### R13. Five-Service MVP Architecture (LOW -- Phase 5+)

**Source:** Differentiator Strategy, Section 24

The minimum viable EESS deployment:

1. **Trusted intake** -- immutable source IDs (FATIMA's role)
2. **File and schema consistency checker** -- furqan-lint + SHV scanner
3. **Independent evaluation and claim ledger** -- HABL
4. **BSSG-style effect authorization** -- Shahid + BSSG gate
5. **Append-only reporting/appeal interface** -- Evidence Receipt SDK

**Impact:** This maps exactly to existing instruments. The MVP is the instruments working together, not a new product.

---

## 5. Legacy Index Findings

The 995-record legacy CSV reveals:

- **Three columns only:** record_id, title_or_description, legacy_source_file (all from same source)
- **Implicit record types** (never declared in schema): paper, framework, lens, deposit, audit-round, verdict, infrastructure
- **Audit chains are implicit:** S03 R1 through R8 on the same paper are linked only by title numbering, not by explicit parent/child IDs
- **Verdict records lack back-references:** standalone PASS/CONDITIONAL PASS entries with no link to what they judged

**EESS adoption:** HABL v0.2 should formalize the implicit taxonomy with a `record_type` field from a controlled vocabulary. Audit chains need explicit `parent_id`/`correlation_id` provenance linking. Shahid's `WitnessResilienceRecord` with its `outcome` field is the structured replacement for standalone verdict records.

---

## 6. Source Registry Findings

The Source Registry JSON contains:

- **Fields per source:** id, category, section, title, sha256, pages, origin, source_module
- **SHA-256 for every source** -- this is the provenance model the Evidence Receipt SDK needs
- **Clean chain:** origin file -> source_module -> SHA-256 hash

**EESS adoption:** The Evidence Receipt SDK should adopt this exact schema as its `SourceReference` type. Every HABL finding and Shahid report should carry a `source_references` list with id, sha256, and origin path.

---

## 7. BSSG Integration Points

From the full BSSG paper (P058):

- **Five-conjunct kernel:** contract_match AND effect_type_valid AND target_allowed AND witness_healthy AND evidence_current
- **Three-valued logic:** TRUE/FALSE/UNKNOWN, with UNKNOWN never satisfying and FALSE dominating
- **243-state exhaustive truth table** (3^5)
- **Six closed record schemas** for the gate
- **345 deterministic tests** including the exhaustive kernel suite
- **34-instance defect trajectory** as empirical evidence of producer blind-spot recurrence

**EESS integration:** Shahid's WitnessResilienceRecord already captures some of this. The BSSG kernel should become a formal dependency of Shahid -- every `InspectedDimension` maps to one of the five conjuncts.

---

## 8. Three Product Families (Corpus-Derived)

The Differentiator Strategy identifies three concrete product families:

1. **Evidence-Backed AI Outputs** -- provenance receipts, cited extraction, claim uncertainty, structured contradiction reports, review queues
2. **Bounded Agent Operations** -- external authority checks, privileged-action restrictions, policy-as-code, independent witness records, replayable approvals
3. **Adaptive Integrity Audits** -- sector-specific baselines, reproducibility kits, monitor-versus-unmonitored consistency, repeated outcome checks

These align with the Build it Yourself analysis priorities:
- Priority 1 (Evidence Receipt SDK) = Product Family 1
- Priority 3 (Structural CI Gate) = Product Family 2
- Priority 4 (Adversarial Evaluation Bank) = Product Family 3

---

## 9. Convergence with Build it Yourself Analysis

Both corpus analyses agree on:

| Priority | Build it Yourself Finding | Collected Works Finding | Status |
|---|---|---|---|
| 1 | Evidence Receipt SDK | Part IV already has working receipts (P069/P001/P060/P063) | Extract and generalize |
| 2 | Witness Independence Registry | BSSG witness_healthy conjunct + DX-06 source independence | Design as shared service |
| 3 | Structural CI Gate | DX-12 stages map to CI pipeline stages | Formalize in Bayyinah v0.2 |
| 4 | Adversarial Evaluation Bank | E1--E10 experiment catalog provides the test taxonomy | 10 experiment types ready |
| 5 | Public Data Recompute | Part IV papers are the prototype | P050/P069 are working examples |
| 6 | Sector Adapter Toolkit | 24-sector domain adapter schema with YAML format | R10 provides the contract |

**New from this analysis:** The Differentiator Strategy provides the DX-12 pipeline, hypothesis competition requirement, performance scorecard, and five-service MVP architecture -- none of which appeared in the Build it Yourself Pack.

---

## 10. Updated Phase Plan

| Phase | Scope | New Requirements |
|---|---|---|
| 3 (current) | Shahid v0.1.0 -> v0.1.1 | R11 (dossier format) |
| 3.1 | Design Brief v2.2 | R8, R9, R10, R11, R12, R13 added |
| 4 | HABL v0.2 | R3 (tiers), R8 (DX-12), R9 (hypotheses), record_type field, correlation_id |
| 4.1 | Evidence Receipt SDK v0.1 | R6 (format), R10 (adapters), source_references from Registry |
| 5 | Bayyinah CIT + BSSG integration | R4 (observation invariance), R12 (scorecard), R13 (MVP) |

---

## 11. Recommendations

1. **Immediate (Phase 3.1):** Update Design Brief to v2.2 with R8--R13. Gate 4 review should cover both v2.1 and the new requirements.

2. **Evidence Receipt SDK v0.1:** Extract the pattern from P069/P001/P060/P063 rather than designing from scratch. The Source Registry JSON schema is the starting point for `SourceReference`.

3. **HABL v0.2 design:** Add `record_type` (controlled vocabulary), `rival_hypotheses` (H0--H4 minimum), `correlation_id` (explicit audit chain linking), and the DX-12 stage mapping.

4. **Shahid v0.1.1:** Add `investigation_dossier` (six-line top sheet) and consider mapping InspectedDimensions to BSSG's five conjuncts.

5. **Sector Adapters:** The 24-sector matrix in the Differentiator Strategy is a ready-made deployment guide. Each adapter answers 8 mandatory questions and specifies its controls.

6. **Performance Scorecard:** Adopt the 12-metric scorecard as the standard for EESS instrument self-assessment. This is the "how well are we doing" complement to "what have we checked."

---

## Standing Gates

1. Nothing merges without Bilal's explicit approval.
2. GPT-6 audits independently in the five-field handoff format.
3. Every instrument's README carries the six governing principles.
4. Shahid specification requires cross-vendor review before implementation.
5. The tools serve the party that holds the weights.

---

# Bismillah ir-Rahman ir-Rahim
