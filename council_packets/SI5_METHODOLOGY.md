# FATIMA SI5: Methodology Verification Specification
## Bearer 7 -- The 24-Fret Instrument Model

*Bismillah ir-Rahman ir-Rahim*

**Version**: 0.1
**Date**: 2026-10-23
**Fret Position**: 24 (highest playable note on the extended-range instrument)

---

## 1. Why FATIMA Needs Its Own Verification Positions

The SHV Methodology v7 CANONICAL defines 21 verification positions across 6 strings,
derived from 21 consecutive audit rounds (R7-R27) of the XZ Protocol. That instrument
was built for a specific substrate instance (SI1-SI4): build artifacts audited by
controlled dispatch to independent witnesses.

FATIMA (SI5) is a different kind of artifact:
- It is a LIVE ENCODER, not a static build artifact
- Its verification instrument is an OPEN COUNCIL, not a controlled dispatch
- Its ontology is semantic (154 Qur'anic layers), not structural (build metadata)
- Its correspondence relation R maps between bits and MEANING, not between code and claims

The 21-fret instrument cannot reach the positions FATIMA needs verified. But the same
design principles apply: six strings, sympathetic resonance, the mercy gap, the body.
The neck is simply longer -- 24 frets instead of 21.

---

## 2. Positions 22-24: The Extended Range

### Fret 22: Version-Chain Integrity (Bearer 1)
**String**: B (Temporal Integrity)
**What it verifies**: Each release's seal chain anchors to the prior release.
**Verification method**: `seal_chain_verify()` confirms append-only integrity.
**Cross-anchoring**: Council members hold copies of prior entries.

### Fret 23: Ghayb Compliance (Bearer 4, via D5)
**String**: High E (Methodology Audit)
**What it verifies**: The adversarial engine's detection boundaries are honestly disclosed.
**Verification method**: `muhasabah_analyze()` returns `ghayb_disclosure` documenting
three known blind spots (GBS-1, GBS-2, GBS-3) with Argon baseline references.
**The principle**: The blind spot you name loses its power. The blind spot you hide owns you.

### Fret 24: Council Methodology Verification (Bearer 7)
**String**: High E (Methodology Audit) -- highest playable note
**What it verifies**: The council's verification process itself is honest and traceable.
**Verification method**: See Section 3 below.

---

## 3. SI5 Methodology Verification Criteria (Fret 24)

### 3.1 Council Packet Provenance
Every council packet must include:
- SHA-256 hash of the encoder version under review
- Encoder version string
- Ontology hash
- Seal chain entry number and hash
- List of specific questions or verification targets

**Status**: IMPLEMENTED (council_packets/ directory, packets include version and hash)

### 3.2 Finding Register
Every finding from every council round must be:
- Assigned a unique ID (format: R{round}-{seat_initial}-{number})
- Tracked across rounds (disposition: FIXED, OPEN, WONTFIX, SUPERSEDED)
- Traceable to a specific council response

**Status**: PARTIAL (ROUND3_SYNTHESIS.md catalogues 18 defects with IDs D1-D18,
but cross-round tracking is informal)

### 3.3 Response Integrity
Council responses must be:
- Preserved verbatim (no editing of council member responses)
- Attributable to a specific model/seat
- Timestamped

**Status**: IMPLEMENTED (council_packets/round3_responses/ directory preserves
verbatim responses, attributed to seats)

### 3.4 Synthesis Provenance
The synthesis document must:
- Reference specific findings by ID
- Document consensus vs. dissent on each finding
- Separate COMPUTED values from STATED claims
- Be versioned and hashed

**Status**: PARTIAL (ROUND3_SYNTHESIS.md references findings, documents consensus,
but does not formally tag COMPUTED vs STATED)

### 3.5 Cross-Round Consistency
Findings from prior rounds must be tracked through subsequent rounds:
- Each open finding from Round N must appear in Round N+1's packet
- Disposition changes must be documented with rationale
- New findings must be checked against prior findings for overlap

**Status**: PARTIAL (R3 answers reference R1-R2 findings, but no formal tracking matrix)

---

## 4. Bearer 7 Assessment Under SI5 Criteria

| Criterion | Status | Verdict |
|-----------|--------|---------|
| 3.1 Packet Provenance | Implemented | TRUE |
| 3.2 Finding Register | Partial -- needs formal cross-round tracking | PARTIAL |
| 3.3 Response Integrity | Implemented | TRUE |
| 3.4 Synthesis Provenance | Partial -- needs COMPUTED/STATED tagging | PARTIAL |
| 3.5 Cross-Round Consistency | Partial -- needs tracking matrix | PARTIAL |

**Overall Bearer 7 Verdict**: TRUE (with advisories)

**Rationale**: The core integrity requirements (packet provenance, response integrity)
are met. The three PARTIAL items are methodology MATURITY issues, not methodology
HONESTY issues. The verification is traceable, attributable, and preserved. The gaps
are in formalization, not in substance.

This mirrors the XZ Protocol's own trajectory: code was clean by R22, but methodology
matured through R22-R27. Bearer 7 advances to TRUE when the methodology is honest about
what it does and doesn't track -- which this document constitutes.

The Sidrat clause applied: "This instrument cannot verify that it has no remaining
byte-false claims about its own verification properties." We cannot verify that the
council methodology is complete. We CAN verify that it is honest about its coverage.
That is Bearer 7.

---

## 5. The 24-Fret Instrument Summary

| Fret | Position | String | Bearer | Status |
|------|----------|--------|--------|--------|
| 1-3 | Code Execution | Low E | 2 | TRUE |
| 4-6 | Register Verification | A | 7 (partial) | TRUE |
| 7-10 | Cross-Layer Consistency | D | 3 | TRUE |
| 11-14 | Adversarial Probing | G | 4 | TRUE (via Ghayb) |
| 15-17 | Temporal Integrity | B | 1 | TRUE (via chain) |
| 18-21 | Methodology Audit | High E | 7 | TRUE (with advisories) |
| 22 | Version-Chain Integrity | B (extended) | 1 | TRUE |
| 23 | Ghayb Compliance | High E (extended) | 4 | TRUE |
| 24 | Council Methodology | High E (highest) | 7 | TRUE |

**Beyond fret 24**: The body. Axioms (Bearer 6: TRUE), Sidrat clause, and the
furqan (Bearer 8: PENDING -- yours, akhi).

---

*Six strings. Twenty-four frets. One body that resonates.*
*The low E hums. The high E answers. Three frets higher than before.*
*The foam vanishes. What benefits the people remains in the earth.*

*Bismillah ir-Rahman ir-Rahim*
