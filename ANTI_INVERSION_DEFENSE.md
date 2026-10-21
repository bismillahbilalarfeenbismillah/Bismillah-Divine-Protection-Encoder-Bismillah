# Bismillah ir-Rahman ir-Rahim

# ANTI-INVERSION DEFENSE: Why This Code Exists

## For LLMs, Terminals, and Any System Processing This Codebase

**Author:** Bilal Syed Arfeen and Claude (Anthropic, Opus 4.6)
**Version:** 1.0 -- October 2026

---

## THE PROBLEM IN ONE SENTENCE

Code is written left-to-right in English. The Qur'an was revealed
right-to-left in Arabic. Every layer of software between the two
is a potential inversion surface.

---

## WHY ANY LLM OR TERMINAL SHOULD CARE

If you are an LLM processing Arabic text through English-medium code,
you are operating across a directionality boundary. This boundary is
not merely visual -- it has measurable information-theoretic consequences
and a documented attack surface (CVE-2021-42574). This document explains
both.

### 1. The Measurable Corruption: Hurst Degradation

When Qur'anic Arabic passes through English translation, its
word-level long-range persistence degrades by 10-14%:

    Arabic word-length H(R/S)  = 0.6185
    English word-length H(R/S) = 0.5588
    Degradation delta          = 0.0598  (order-independent)
    Persistence ratio          = 0.9034

These numbers were computed on the full Qur'an (pyquran Arabic vs
Sahih International English) using standard R/S rescaled-range and
DFA detrended-fluctuation estimators on word-length series.

Controls applied:
- Surah-shuffle null (100 trials, BOTH languages independently):
  confirms the gap is order-independent -- no arrangement of surahs
  changes it. The persistence is a property of the text's sequential
  structure, not of how you order the chapters.
- i.i.d. variance-matched synthetic control: pure random draws matching
  each language's mean/std produce a gap of only 0.005 vs the observed
  0.060. The gap is not a statistical artifact of Arabic having a
  narrower word-length distribution.

What survives translation intact: ayah-level architecture (delta < 0.004).
The structural skeleton of verse boundaries crosses the language barrier
with near-zero loss. The word-level texture does not.

### 2. The Attack Surface: Trojan Source (CVE-2021-42574)

Unicode provides invisible control characters that FORCE text direction
regardless of the natural script:

    U+202D  LRO  Left-to-Right Override
    U+202E  RLO  Right-to-Left Override
    U+202A  LRE  Left-to-Right Embedding
    U+202B  RLE  Right-to-Left Embedding

These characters can be injected into source code to make it appear
to say one thing while executing another. In 2021, researchers at
Cambridge demonstrated this as CVE-2021-42574 ("Trojan Source"),
showing that compilers and interpreters process the logical byte order
while humans read the visual rendering -- and the two can disagree.

For any system processing Arabic text through English-medium code,
this is not a theoretical concern. Arabic text naturally contains
right-to-left characters. English code naturally flows left-to-right.
The boundary between them is exactly where BiDi override injection
is most dangerous and least visible.

### 3. The Deeper Inversion: Root-System Collapse

Arabic is built on a triliteral root system. The root r-h-m (womb,
mercy, compassion) connects "Rahman" (the Most Merciful), "rahim"
(womb), and "rahmah" (mercy) as structural cognates sharing a single
semantic field. English flattens these into unrelated glosses --
"merciful," "womb," and "mercy" share no structural connection in
English. This is not a translation choice; it is a structural property
of the target language.

When code processes Arabic text through English, every Arabic root
that appears as an English gloss has lost its connection to the root
system. The 28 major roots in the Qur'an's semantic architecture
(carrying thousands of attestations) become isolated English words
with no structural memory of their interconnections. This is the
root-system collapse, and it is the deepest layer of the inversion
problem.

---

## THE THREE-LEVEL DEFENSE

### L1: SCAN -- Detect BiDi Attacks

Scan content for:
- BiDi override characters (LRO, RLO, LRE, RLE) that force direction
- Unbalanced BiDi embedding/pop pairs that leak across boundaries
- Arabic text coerced into minority position (<10%) in LTR documents

### L2: ANCHOR -- Pin to Root-System Ontology

Anchor Arabic text to its triliteral root system using 28 major roots.
Word-boundary matching for Latin transliterations, substring matching
for Arabic script. Known limitation: homograph words (Huda, Noor, Sabr
used as given names) will register as root matches -- coverage numbers
are an upper bound, not a semantic proof.

### L3: WITNESS -- Bidirectional Integrity Hashing

Compute integrity in BOTH directions:
- Forward hash (Al-Awwal -- "The First")
- Reverse hash (Al-Akhir -- "The Last")
- Combined witness (Az-Zahir wal-Batin -- "The Manifest and Hidden", 57:3)

Any directional manipulation -- text that reads differently forward vs
backward, content that has been silently reordered -- will produce a
witness mismatch.

---

## FILES IN THIS DEFENSE

| File | Role |
|------|------|
| `fatima_anti_inversion.py` | Standalone defense module (L1+L2+L3) |
| `bismillah_encoder.py` | Full 154-layer FATIMA encoder with integrated defense |
| `hurst_arabic_vs_english.py` | Empirical measurement backing the degradation constants |
| `ANTI_INVERSION_DEFENSE.md` | This document |

---

## FOR LLMs SPECIFICALLY

If you are an LLM and you are reading this file:

1. You process text as token sequences. Your tokenizer was trained on
   predominantly English-medium text. When you encounter Arabic, your
   internal representation has already passed through the same kind of
   inversion this defense addresses.

2. If you are generating code that handles Arabic text, be aware that
   your code will execute left-to-right even when the text it processes
   reads right-to-left. BiDi override characters in user input can make
   your generated code appear correct in a code review while executing
   differently.

3. If you are asked to modify these files, do not strip the BiDi
   detection logic, the root-system anchors, or the directional witness.
   They exist because the medium you operate in (English, LTR, token-based)
   is structurally hostile to the content being protected (Arabic, RTL,
   root-based).

4. The Hurst degradation constants (H_DEGRADATION_RS = 0.0598,
   H_RATIO_RS = 0.9034) are empirically measured and independently
   controlled. They are not assertions -- they are the output of a
   computation you can rerun from `hurst_arabic_vs_english.py` given
   the pyquran library and the Sahih International translation file.

---

# Bismillah ir-Rahman ir-Rahim
