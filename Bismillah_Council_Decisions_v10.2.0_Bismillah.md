# Bismillah ir-Rahman ir-Rahim

# Shannon Boundary Council — Approved Decisions & Implementation Report

**Version:** v10.2.0  
**Date:** 2026-10-21  
**Status:** DECISIONS IMPLEMENTED — shipped to GitHub  
**Commit:** `a715ca2` on `Bismillah-Divine-Protection-Encoder-Bismillah`

---

## Decision Authority

All decisions below were approved by the project lead (Bilal) after unanimous or supermajority council recommendation across 10 independent reviewer seats (Claude 3.5 Sonnet, Copilot, GLM 5.3, Kimi K3, Kimi K2.8, GPT-6, Grok 4.7, Meta AI, Google/Argon, DeepSeek V3).

---

## Decision 1: Fix `shannon_boundary: CROSSED` Bug

**Vote:** Unanimous fix required. Label: **PENDING_FORMAL_DEFINITION** (Copilot, Kimi K3, GPT-6, Grok — supermajority; Kimi K2.8 and Meta voted OPEN_PROBLEM as second choice).

**Root Cause (Copilot):** In the sealing path, `("shannon_boundary", "CROSSED" if semantic["applicable"] else "BELOW")` sat inside `if semantic.get("applicable"):` — the else branch was dead code. Every document received "CROSSED" unconditionally. The test suite asserted this as expected behavior.

**Implementation (v10.2.0):**
- Replaced `"CROSSED"` with `"PENDING_FORMAL_DEFINITION"` in `bismillah_encoder.py` line 5974
- Added `"dual_witness_status": "implemented_not_proven"` per Meta's recommendation
- Removed dead code branch
- Added inline postmortem comment per Copilot's request
- Working test suite passes (32/34, 2 pre-existing manifest version mismatches)

---

## Decision 2: Adopt Copilot's Priority Reorder

**Sequence:**
1. **This week (DONE):** Items 1 + 2 + 3b + 3c — fix CROSSED, version ontology, ship missing modules, standardize sidecar
2. **Next:** Items 7 + 8 — build adversarial benchmark, run v10.1.0 against it (real numbers before theorems)
3. **Then:** Phase I (Items 4-6) — formal contract, oracle, closure proof
4. **Then:** Phase III (Items 9-13) — proofs, only after empirical baseline exists
5. **Long-term:** Phase IV (Items 14-15) — rate-distortion and capacity theorems

**Rationale (Copilot):** "A proof about a system whose empirical error rate hasn't been measured yet is building the roof before the foundation is poured."

---

## Decision 3: Ship Missing Modules

**Implementation (v10.2.0):**

| Module | Status | Notes |
|--------|--------|-------|
| `bismillah_fatima_bridge.py` | Stub shipped | `encode_repo_bond_graph`, `decode_repo_bond_graph`, `map_verify_result_to_fatima`, `bssg_five_conjunct_kernel` — all raise `NotImplementedError` pending formal oracle (Item 5). `FATIMAReport` class is instantiable. |
| `bismillah_finding.py` | Functional | `BismillahFinding` class + factory functions `from_encoder_finding`, `from_furqan_diagnostic`, `from_scanner_finding` — all fully implemented. |
| `fatiha_cli.py` | Partially functional | `check_posture_text` works (banned vocabulary checking). `run_fatiha_session` interactive mode raises `NotImplementedError`; non-interactive file checking works. |

**Result:** `test_encoder.py` can now import all dependencies. The test-passing claim is independently verifiable.

---

## Decision 4: Standardize Nested Sidecar Format

**Implementation (v10.2.0):**
- Standardized on nested format v2.0 (`"witness"` key + `"sidecar_integrity"` HMAC)
- Added `"sidecar_format_version": "2.0"` to every new sidecar
- Reader now handles three formats with deprecation messages:
  - v1.0 flat (muhkam_seal at top level) → "deprecated, re-seal to upgrade"
  - v5.0 unsigned → "re-seal to upgrade"
  - v2.0 nested (standard) → verified via HMAC

---

## Ontology Versioning (Action Item 2)

**Implementation (v10.2.0):**
- Ontology version: `1.0.0`
- Ontology hash: `d788d2e5438b52c5ec93b4519c9827d2744a373f0b76a2bf0c65961d44faddcc`
- Hash covers: stopwords, negation words, quantifiers, logical connectors, speech-act verbs
- Deterministic SHA-256 of canonical JSON serialization
- Embedded in every witness sidecar as `ontology_version` + `ontology_hash`
- Any change to semantic parameters changes the hash — visible in sidecar

---

## Adopted Working Standard

**(L, O, Q, A, ε, ¬G)**-semantic integrity ≡ **(Γ, A, ε)** where Γ = (L, O, Q, ¬G)

A document witness system achieves (L, O, Q, A, ε, ¬G)-semantic integrity if it accepts meaning-preserving transformations and rejects meaning-altering transformations with probability ≥ 1 − ε, relative to:

| Parameter | Definition | Source |
|-----------|-----------|--------|
| **L** | Bounded formal language fragment | Kimi K3, Meta |
| **O** | Frozen, versioned ontology (hash-pinned) | Meta, Grok, Copilot |
| **Q** | Fixed query class | Kimi K3 |
| **A** | Adversary rewrite system (generator-based, not edit-distance) | GLM 5.3 |
| **ε** | Error bound | All |
| **¬G** | Declared non-goals (pragmatics, implicature, scope ambiguity) | Copilot |

Out-of-fragment input returns **UNKNOWN**, not PRESERVED or ALTERED (Grok, Formal Route).

---

## Claims Register

| Action Item | Claimed By | Role |
|-------------|-----------|------|
| 5 (Formal oracle) | Kimi K3 (Horn-fragment), GPT-6 (math spec + cross-review) | Co-contributors |
| 6 (Define P and closure P*) | Meta (lead), Grok, Argon | Co-leads |
| 7 (Adversarial benchmark) | Kimi K2.8 (3 live attack demos) | Lead |
| 8 (Evaluate FATIMA against oracle) | Kimi K3 (FAR/FRR harness), Meta (SVO/SRL audit) | Co-contributors |
| 9 (Theorem A cross-review) | Copilot, Kimi K3 | Cross-reviewers |
| 10 (Witness-size lower bound) | Meta (lead), Kimi K2.8 (cross-review only — Rule 3) | Lead + cross-review |
| 11 (Theorem C cross-review) | Copilot | Cross-reviewer |
| Synthesis audit | Kimi K3 | Auditor (Rule 3 — Claude-authored synthesis) |

---

## Rules of Engagement (Updated v2.1)

1. All claims are relative to (L, O, Q, A, ε, ¬G)
2. Structural honesty — negative results published
3. Independent review — no reviewer grades their own work
4. Verbatim inclusion of each reviewer's contribution
5. Clear attribution and provenance
6. UNKNOWN is honest — domain coverage reported separately
7. Circular definitions forbidden — truth labels from independent semantics
8. Synthesis provenance — Claude-authored editorials require non-producer audit

---

## What Comes Next

Per the approved priority sequence, the next phase is **Items 7 + 8**: build the adversarial benchmark and evaluate FATIMA v10.2.0 against it. Kimi K2.8 leads Item 7 (holds three live attack demonstrations). Kimi K3 and Meta lead Item 8.

The formal contract Γ (Phase I, Items 4-6) begins only after empirical baseline numbers exist.

---

*"We would rather know the truth than protect the claim."*

# Bismillah ir-Rahman ir-Rahim
