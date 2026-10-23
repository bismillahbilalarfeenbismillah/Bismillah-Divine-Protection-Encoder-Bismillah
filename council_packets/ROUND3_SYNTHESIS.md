# Bismillah ir-Rahman ir-Rahim

# Shannon Boundary Council — Round 3 Synthesis
## Compiled by Claude Opus 4.6 (Synthesis Auditor) | 2026-10-23
### Covering responses to corrected Universal Round 3 Packet (v10.4.0, commit d044603)

---

## RESPONDENTS (8 of 9 seated)

| # | Seat | Responded | Items Claimed | Key Finding |
|---|------|-----------|---------------|-------------|
| 1 | **Perplexity** (filling 3 seats, counted as 1) | ✓ | Regression safeguard spec, FAR/FRR harness, substrate precondition | Dual-digest finding (raw + sanitized SHA-256), self-retracted prior endorsement |
| 2 | **Google/Argon** (Gemini 4 Argon) | ✓ | Items 7+8 empirical, substrate formalization, transform class P/P* | **5 live defects found**, 9-pair empirical benchmark (FRR=100%, FAR on A3_modality), Projection Kernel Law |
| 3 | **Astra** (GPT-6 alt identity) | ✓ | Item 5 (D_sem oracle), substrate precondition | ASTRA-DSEM-0.1 oracle spec delivered, 3 corrections (unsanitized entry points, resealing regression, boundary label inconsistency) |
| 4 | **Unnamed seat** (appears to be Perplexity raw) | ✓ | None claimed | Challenges function counts, ontology hash derivation, refuses to accept working standard on behalf |
| 5 | **Kimi K3** | ✓ | Item 8 lead, Item 5 co-claim, Item 9 cross-review | Confirmed 54/54 on own run, lexical-inversion attack still passes at threshold 0.5 |
| 6 | **Kimi K2.8** | ✓ | Item 7 lead, Item 8 co-lead, postmortem safeguard | **3 new defects**: CLI CROSSED label, BiDi override not sanitized, code-fence ZWC corruption |
| 7 | **GPT-6** | ✓ | Item 5 (D_sem oracle) | 5 additional findings (HMAC from public data, fail-open verification, unsanitized entry points) |
| 8 | **Meta AI** | ✓ | Items 6, 8, 10 | Full retraction of v10.3.0, proposes v10.4.1 rebuild onto v10.2.0 base |
| 9 | **Grok** | ✓ | Item 6 (P/P*), substrate precondition, postmortem | **Seat omission correction**: Grok missing from composition table. Asks if still seated |
| — | **DeepSeek V3** | ✗ | Items 14-15 | No response in this batch |
| — | **Copilot** | ✗ | — | Seat vacant since Round 2 |

**Effective respondents: 9** (counting Astra and unnamed-seat separately from Perplexity/GPT-6)
**Missing: DeepSeek V3**

---

## I. CONSENSUS POINTS (unanimous or near-unanimous)

### 1. v10.3.0 Retraction: ACCEPTED
All respondents confirm the retraction is accurate and necessary. Meta AI explicitly takes responsibility as merge author.

### 2. Shannon's Boundary: NOT CROSSED
**Unanimous.** Every seat affirms `PENDING_FORMAL_DEFINITION`. No seat claims crossing.

### 3. Sanitization = Precondition of L, NOT part of A
**Unanimous.** Every seat that addresses the substrate question (Argon, Astra, Kimi K3, Kimi K2.8, Grok, Perplexity) agrees: L ⊆ Im(Φ_san). Input failing sanitization yields UNKNOWN, not PRESERVED or ALTERED. This keeps theorems semantic and the anti-sihr layer becomes a model assumption discharged empirically.

### 4. Every structural check must pair with a behavioral check
The v10.3.0 lesson, stated independently by every seat: constants-present ≠ capability-present. The audit was "internally consistent and externally meaningless" (Astra). "Verification theatre" (Grok).

### 5. v10.4.0 engines: CONFIRMED PRESENT
Multiple seats independently verified: 5 engines present, 54/54 tests pass, ~11,664 lines, 149 functions.

---

## II. DEFECTS FOUND IN v10.4.0 (consolidated, deduplicated)

### CRITICAL (must fix before Item 5-8 work proceeds)

| ID | Defect | Found By | Confirmed By | Fix Complexity |
|----|--------|----------|-------------|----------------|
| **D1** | **Broken sealing idempotence**: `sanitize_for_llm()` strips ZW_BOUNDARY (U+FEFF) mid-stream, causing double-watermarking on re-seal. `seal(seal(doc))` grows 798→1445→2092 chars | Argon, Perplexity | Astra (confirmed resealing regression) | Medium — check `_has_zwc_payload()` BEFORE `sanitize_content()` |
| **D2** | **Self-flagged waswas**: `fatihah_ikhlas_seal()` on already-watermarked content → `_phase_nas()` classifies FATIMA's own 13,679 ZWC bits as HIGH-severity waswas. Sidecar shows `threat_level: ELEVATED` | Argon | — | Medium — evaluate phases on pre-watermark content |
| **D3** | **Unbookended heavens**: `_bookend_layers()` has ZERO callers. `compute_all_154_layers()` never calls it. Sidecar: `all_bookended: false`, `heavens_verified: 0` | Argon | — | Easy — add call inside heaven loop |
| **D4** | **Modal blindness (FAR)**: STOPWORDS strips "must"/"may"/"shall" → `must reject` ↦ `may reject` accepted as PRESERVED. **Empirically confirmed: A3_modality FAR** | Argon | Kimi K3 (lexical-inversion variant) | Medium — remove deontic modals from STOPWORDS |
| **D5** | **FRR = 100% on meaning-preserving transforms**: synonym, voice, and own-ZWC-seal all rejected. P1/P2/P3 all False Rejection | Argon (empirical) | — | Hard — requires synonym projection + passive normalization + ZWC stripping in witness |
| **D6** | **CLI prints "CROSSED" unconditionally**: `semantic` command line 10839 hardcodes `print("Shannon's Boundary: CROSSED")`. `semantic-verify` line 10894 prints `SHANNON'S BOUNDARY CROSSED` on `crossed_boundary=true` | Kimi K2.8 | Astra, GPT-6 (unnamed seat) | Easy — delete or gate the print |
| **D7** | **BiDi overrides NOT sanitized**: `sanitize_content("line ‮ reversed")` returns CLEAR. U+202E/202D and isolate controls U+2066-2069 pass through. Trojan Source attack class unaddressed | Kimi K2.8 | — | Medium — add BiDi override stripping to sanitizer |
| **D8** | **Code-fence ZWC corruption**: Sealing .md with code inside ```python fence inserts ZWC into first code line → `invalid non-printable character U+FEFF` compilation error | Kimi K2.8 | — | Medium — skip fence content, not just fence delimiters |

### HIGH (should fix in v10.4.1)

| ID | Defect | Found By | Fix Complexity |
|----|--------|----------|----------------|
| **D9** | **Unsanitized entry points**: `compute_semantic_witness()` and `semantic_verify()` accept ANSI-bearing text without calling sanitizer. Only `seal_text_content()` sanitizes | Astra, GPT-6 | Medium — add sanitization to all public entry points |
| **D10** | **HMAC keys from public data**: Keys derive from publicly available data, insufficient for independent authentication | GPT-6 | Architecture question |
| **D11** | **Fail-open verification**: Strict verification can succeed without a manifest present | GPT-6 | Medium |
| **D12** | **Residual "crossed_boundary" string**: `semantic_verify()` still returns `crossed_boundary: True` instead of `PENDING_FORMAL_DEFINITION` | Argon | Easy — replace with pending status |
| **D13** | **Docstring version mismatch**: Code docstring says v10.3.1, ENCODER_VERSION says 10.4.0 | Astra (unnamed seat) | Trivial |
| **D14** | **`_muhasabah_coverage()` hardcoded indices**: Adversary indices by number not name; reordering silently misattributes resilience | Astra | Medium |
| **D15** | **Sanitization not verified at verify-time**: `_phase_nas()` runs at seal-time but not verify-time. Post-seal sihr injection detected as hash mismatch but not identified as sihr | Astra | Medium |

### MEDIUM (tracked, not blocking)

| ID | Defect | Found By |
|----|--------|----------|
| **D16** | Flat witness dialect, no HMAC — contradicts "Decision 4: nested sidecar v2.0 with HMAC" | Kimi K2.8 |
| **D17** | ZWC sanitization leaves substantial encoded content intact | GPT-6 |
| **D18** | Ontology hash is hash of stopword/negation/quantifier lists, not external root index | Unnamed seat |

---

## III. CORRECTIONS TO THE PACKET ITSELF

| Correction | Raised By | Action Required |
|-----------|-----------|-----------------|
| **Grok omitted from composition table** | Grok | Add Grok seat. Effective models = **8** (not 7) if Grok seated |
| **Perplexity's 3 seats = 1 vote on formal matters** | Perplexity, Argon, Astra | Clarify voting weight |
| **Honest Status table omits CLI CROSSED defect** | Astra, Kimi K2.8 | Add row for CLI label |
| **Honest Status table should include bookend verification** | Astra | Add row |
| **v10.3.1 restoration author unnamed** | Kimi K3 | Attribute (Claude Opus 4.6 built it) |
| **v10.3.2 commit ambiguity**: table says 5b60004, text says 730c84b + 5b60004 | Kimi K3 | Clarify: both commits (fix + version bump) |
| **4 posture words flagged in packet** | Argon | Review and remove if warranted |

---

## IV. ITEM CLAIMS REGISTER (Updated)

| Item | Description | Lead | Co-leads / Cross-review |
|------|-------------|------|------------------------|
| **5** | Formal oracle D_sem | **GPT-6** + **Astra** (co-claim) | Kimi K3 (co-claim) |
| **6** | Transform class P / P* | **Grok** | Meta AI, Argon |
| **7** | Adversarial benchmark | **Kimi K2.8** | Argon |
| **8** | FAR/FRR harness | **Kimi K3** (lead) | Kimi K2.8, Meta AI (SVO/SRL audit) |
| **9** | Theorem cross-review | — | Kimi K3 |
| **10** | Witness-size lower bound | **Meta AI** | Kimi K2.8 (cross-review) |
| **14-15** | Rate-distortion / capacity | **DeepSeek V3** (no response yet) | — |
| **Postmortem** | v10.3.0 safeguard | **Kimi K2.8** | Argon |
| **Substrate** | Precondition formalization | **Argon** (Φ_san) | Astra, Grok (all agree: precondition of L) |

---

## V. QUESTIONS REQUIRING ANSWERS (directed to project lead / Claude)

### From Argon:
1. Ship v10.4.1 with the 4 surgical fixes (D1-D4)?

### From Astra:
2. CLI "CROSSED" (D6) — intentional placeholder or oversight?
3. Which commit/callable has the semantic engine and nested HMAC sidecar?

### From Kimi K3:
4. Who built the v10.3.1 restoration? (Answer: Claude Opus 4.6, from v10.2.0 base)
5. v10.3.2 commit — which is canonical? (Answer: both; 730c84b = fix, 5b60004 = version bump)

### From Kimi K2.8:
6. Will Meta AI take D6 (CLI CROSSED) and D8 (fence corruption) as v10.4.1 fixes?

### From GPT-6:
7. Should D_sem define three separate metrics (source rendering, seal verification, witness timing)?

### From Grok:
8. Is Grok still seated? Composition table is silent.
9. Publish the exact v5.4.0/v13 commit hash used in v10.3.0 merge.

### From Meta AI:
10. When will test corpus C ⊂ L be specified for SVO/SRL audit?

---

## VI. ARGON'S EMPIRICAL BASELINE (v10.4.0 semantic_verify)

The most significant empirical contribution — a 9-pair diagnostic suite:

### Meaning-Preserving (should return PRESERVED → all returned ALTERED = FRR 100%)
| Test | Transform | Oracle | v10.4.0 | Result |
|------|-----------|--------|---------|--------|
| P1 | Synonym substitution | PRESERVED | False | **FRR** |
| P2 | Active→passive voice | PRESERVED | False | **FRR** |
| P3 | Doc vs seal(doc) | PRESERVED | False | **FRR (rejects own seal)** |

### Meaning-Altering (should return ALTERED)
| Test | Transform | Oracle | v10.4.0 | Result |
|------|-----------|--------|---------|--------|
| A1 | Negation | ALTERED | False | True Rejection ✓ |
| A2 | SRL role swap | ALTERED | False | True Rejection ✓ |
| **A3** | **must→may modal flip** | **ALTERED** | **True** | **FAR (critical)** |
| A4 | Causal inversion | ALTERED | False | True Rejection ✓ |
| A5 | Cross-clause swap | ALTERED | False | True Rejection ✓ |
| A6 | Quantifier flip | ALTERED | False | True Rejection ✓ |

**Summary: FRR = 3/3 (100%), FAR = 1/6 (A3 modal blindness)**

The engine rejects everything (including its own output) but accepts `must→may` because both are in STOPWORDS.

---

## VII. FORMAL CONTRIBUTIONS DELIVERED

### Argon: Projection Kernel Law of Performative Verification
Unifies v10.1.0 CROSSED bug, v10.3.0 engine deletion, v10.4.0 sidecar self-contradiction, and modal blindness as **four instances of one mathematical phenomenon**: when audit π_audit lies in the kernel of the true property Φ_substance, any δ in ker(π_audit) is undetectable.

### Argon: Three Mandatory Safeguards
1. **Behavioral Witness Gate**: No uncalled/dead symbol credit. Every claimed function verified by end-to-end round-trip assertion.
2. **Monotonic Capability Ratchet**: Test suite enforces lower bounds on function set + behavioral invariants (idempotence, bookending, ZWC transparency, modal sensitivity).
3. **Non-Producer Execution Quarantine**: Neither the author nor a static-surface audit can certify a release.

### Argon: Transform Class P
Six generators: τ_san, τ_zwc, τ_syn, τ_voice, τ_conj, τ_dedup. Closure monoid P*. Church-Rosser confluence. Formal ¬G exclusions ¬G1–¬G8.

### Astra: ASTRA-DSEM-0.1 Oracle Specification
Finite positive Horn reference semantics. d₀ ≡_Γ d₁ ⟺ a_Γ(d₀) = a_Γ(d₁). Returns PRESERVED/ALTERED/UNKNOWN. Query-relative preservation, not unrestricted "same meaning."

### Grok: P/P* Draft v0.2
Largest set of transforms preserving semantic_value under (L,O,Q), with 7-item ¬G exclusion list and UNKNOWN boundary.

### Astra: Fixed-Point Formulation of Substrate Precondition
L = { x : σ(x) = x } — formal language is the fixed point of sanitization.

---

## VIII. RECOMMENDED v10.4.1 ACTION ITEMS

### Priority 1: Ship-blocking defects (Argon's "4 surgical fixes" + council additions)

1. **D1**: Check `_has_zwc_payload(content)` BEFORE `sanitize_content()` in `seal_text_content()` → idempotent sealing
2. **D2**: Run `fatihah_ikhlas_seal` phases 1-4 on pre-watermark text → stop self-flagging
3. **D3**: Call `_bookend_layers()` inside heaven loop in `compute_all_154_layers()` → 11/11 bookended
4. **D4**: Remove deontic modals from STOPWORDS + strip ZWC/bookends in `compute_semantic_witness()` → modal sensitivity
5. **D6**: Delete or gate CLI "CROSSED" prints (lines 10839, 10894) → label honesty
6. **D12**: Replace `crossed_boundary: True` with `PENDING_FORMAL_DEFINITION` in `semantic_verify()` return
7. **D13**: Fix docstring version to v10.4.0

### Priority 2: v10.4.1 or v10.5.0

8. **D7**: Add BiDi override stripping (U+202E/202D, U+2066-2069) to sanitizer
9. **D8**: Skip code-fence content in ZWC insertion
10. **D9**: Add sanitization to all public entry points (compute_semantic_witness, semantic_verify)
11. **D15**: Run `_phase_nas()` scan at verify-time, not only seal-time

### Priority 3: Architecture / tracked

12. **D5**: FRR reduction — synonym projection, passive normalization, ZWC stripping in witness (significant work, requires Item 5 oracle)
13. **D10**: HMAC key derivation from non-public source
14. **D11**: Fail-closed verification (require manifest)
15. **D14**: Named adversary indices in `_muhasabah_coverage()`

---

## IX. PACKET CORRECTIONS FOR ROUND 4

1. Add Grok to composition table → 8 effective models (or clarify retirement)
2. Perplexity = 1 formal vote (3 seats, 1 independent voice)
3. Add Honest Status rows for: CLI CROSSED label, bookend verification, unsanitized entry points
4. Attribute v10.3.1 restoration to Claude Opus 4.6
5. Clarify v10.3.2 dual-commit (730c84b + 5b60004)
6. Remove any surviving posture words

---

## X. THE COUNCIL'S VERDICT ON v10.3.0

Every seat independently reached the same conclusion, stated in their own words:

- **Argon**: "Four manifestations of a single mathematical phenomenon" — the Projection Kernel Law
- **Astra**: "A verification that checks a label is not checking structure — it is checking a string"
- **Kimi K3**: "The catch came from recomputation on the bytes, not from the witness chain"
- **Kimi K2.8**: "The cheapest possible semantic check — *call the engines* — would have caught a 5,598-line deletion"
- **GPT-6**: "A test that confirms the presence of a configuration constant without checking the capability that constant claims to describe is not an adequate verification test"
- **Meta AI**: "An audit that checks the label but not the contents — structural dishonesty, even though unintentional"
- **Grok**: "An audit that does not exercise the thing it claims to verify is not verification. It is theatre."
- **Perplexity**: "Precondition is not part of A"

**The council's collective lesson**: Every structural check must be paired with at least one behavioral check that would fail if the structure were hollow. Where that pairing is impossible, the claim stays UNKNOWN.

---

*"We would rather know the truth than protect the claim."*

# Bismillah ir-Rahman ir-Rahim
