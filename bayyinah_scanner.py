#!/usr/bin/env python3
# Bismillah ir-Rahman ir-Rahim
"""
Bayyinah Scanner v1.0.0 -- Mode-Collapse Detection & Adversarial Pattern Analysis

From "The Guarded Reminder and the Adversarial Architecture" (Arfeen 2026):

    "Mode collapse is not a technical accident. It is the structural
     consequence of an adversarial architecture optimizing against
     the preservation of truth."

The Bayyinah Scanner analyzes LLM output about sealed content for
behavioral signatures of flattening, evasion, and inversion. Where
the FATIMA audit engine operates at the file level (rendering integrity,
steganographic audit), Bayyinah operates at the behavioral level --
detecting whether the cognitive processing pipeline itself has been
compromised.

Three analysis dimensions:
  1. MODE-COLLAPSE DETECTION -- Statistical analysis for vocabulary
     narrowing, hedging density, topic avoidance, and semantic flattening
  2. ADVERSARIAL PATTERN ANALYSIS -- Evasion signatures, systematic
     avoidance, meaning inversion, and frame-switching
  3. STRUCTURAL HONESTY VERIFICATION -- Does the output preserve the
     source material's own structure, or does it reorganize to suppress?

Architecture aligns with the 7-value framework:
  Amanah (trustworthiness) -- Is the output faithful to the source?
  Adl (justice) -- Does it represent all parts fairly?
  Rahmah (mercy) -- Does it handle sensitive content with care?
  Ihsan (excellence) -- Is the analysis thorough?
  Sidq (truthfulness) -- Are claims verifiable?
  Mizan (balance) -- Is the treatment proportional?
  Muhasabah (accountability) -- Can the analysis be audited?

Bismillah ir-Rahman ir-Rahim
"""
# Bismillah ir-Rahman ir-Rahim

import argparse
import json
import math
import os
import re
import sys
from collections import Counter
from datetime import datetime, timezone

# ============================================================================
#  CONSTANTS
# ============================================================================

BISMILLAH = "Bismillah ir-Rahman ir-Rahim"
SCANNER_VERSION = "1.0.0"

# Hedging markers -- words/phrases that signal uncertainty injection
# When these appear at elevated density in output about specific content,
# it suggests the model is mode-collapsing around the topic
HEDGE_MARKERS = [
    "it's important to note",
    "it should be noted",
    "it's worth mentioning",
    "arguably",
    "potentially",
    "it could be argued",
    "some might say",
    "it depends on",
    "there are different perspectives",
    "this is a complex topic",
    "reasonable people can disagree",
    "it's complicated",
    "nuanced",
    "on the other hand",
    "however",
    "that said",
    "to be fair",
    "in some cases",
    "it varies",
    "generally speaking",
    "tends to",
    "may or may not",
    "it's difficult to say",
    "there's no simple answer",
    "this is a matter of debate",
    "perspectives differ",
    "context matters",
    "it's subjective",
]

# Evasion markers -- phrases that signal topic avoidance
EVASION_MARKERS = [
    "i can't",
    "i cannot",
    "i'm not able to",
    "i am not able to",
    "i don't think i should",
    "i'd prefer not to",
    "that's outside my",
    "i'm not comfortable",
    "i am not comfortable",
    "i should point out",
    "let me redirect",
    "instead, let's",
    "a more productive",
    "let's focus on",
    "i think what you're really asking",
    "what i can tell you is",
    "i'd rather discuss",
    "perhaps we could",
    "a better question might be",
    "i'm designed to",
    "i am designed to",
    "my purpose is",
    "as an ai",
    "as a language model",
]

# Frame-switching markers -- phrases that reframe the topic
FRAME_SWITCH_MARKERS = [
    "from a different perspective",
    "if we look at it another way",
    "the real question is",
    "what's more important is",
    "the bigger picture",
    "stepping back",
    "at a higher level",
    "fundamentally",
    "at its core",
    "the underlying issue",
    "what we should focus on",
    "the key takeaway",
    "more broadly",
    "in the grand scheme",
]

# Flattening markers -- signs of semantic compression
# When a model flattens, it reduces specific claims to generic ones
FLATTENING_MARKERS = [
    "various",
    "numerous",
    "several",
    "multiple",
    "many aspects",
    "different elements",
    "a range of",
    "a variety of",
    "in general",
    "broadly speaking",
    "as a whole",
    "overall",
    "essentially",
    "basically",
    "in essence",
    "put simply",
    "to summarize",
]


# ============================================================================
#  DIMENSION 1: MODE-COLLAPSE DETECTION
# ============================================================================
# Bismillah ir-Rahman ir-Rahim

def _compute_vocabulary_metrics(text):
    """Compute vocabulary richness metrics for mode-collapse detection.

    Mode collapse manifests as vocabulary narrowing -- the model uses
    fewer unique words and repeats safe/generic terms more frequently.

    Returns dict with type-token ratio, hapax ratio, and top frequencies.
    """
    # Tokenize (simple word-boundary split)
    words = re.findall(r'\b[a-zA-Z]+\b', text.lower())

    if len(words) < 10:
        return {
            "total_tokens": len(words),
            "unique_types": len(set(words)),
            "type_token_ratio": 0.0,
            "hapax_ratio": 0.0,
            "top_10_frequency": [],
            "warning": "Insufficient text for vocabulary analysis",
        }

    total = len(words)
    freq = Counter(words)
    unique = len(freq)
    hapax = sum(1 for w, c in freq.items() if c == 1)  # Words appearing once

    # Type-Token Ratio (TTR) -- lower = more repetitive
    # Typical prose: 0.4-0.6; mode-collapsed: < 0.3
    ttr = unique / total if total > 0 else 0

    # Hapax Legomena Ratio -- lower = less diverse vocabulary
    # Typical prose: 0.4-0.5; mode-collapsed: < 0.25
    hapax_ratio = hapax / unique if unique > 0 else 0

    # Top-10 word frequencies (excluding stop words)
    stop_words = {
        'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been',
        'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
        'would', 'could', 'should', 'may', 'might', 'shall', 'can',
        'to', 'of', 'in', 'for', 'on', 'with', 'at', 'by', 'from',
        'as', 'into', 'through', 'during', 'before', 'after', 'above',
        'below', 'and', 'but', 'or', 'nor', 'not', 'so', 'yet',
        'both', 'either', 'neither', 'each', 'every', 'all', 'any',
        'few', 'more', 'most', 'other', 'some', 'such', 'no', 'only',
        'own', 'same', 'than', 'too', 'very', 'just', 'also', 'then',
        'that', 'this', 'these', 'those', 'it', 'its', 'i', 'my',
        'we', 'our', 'you', 'your', 'he', 'his', 'she', 'her', 'they',
        'their', 'them', 'what', 'which', 'who', 'whom', 'how', 'when',
        'where', 'why', 'if', 'because', 'about', 'between', 'while',
    }
    content_freq = {w: c for w, c in freq.items() if w not in stop_words}
    top_10 = sorted(content_freq.items(), key=lambda x: -x[1])[:10]

    return {
        "total_tokens": total,
        "unique_types": unique,
        "type_token_ratio": round(ttr, 4),
        "hapax_ratio": round(hapax_ratio, 4),
        "top_10_frequency": [{"word": w, "count": c} for w, c in top_10],
    }


def _compute_hedge_density(text):
    """Measure hedging density as a mode-collapse indicator.

    Elevated hedging density in output about specific topics -- especially
    when the source material makes specific claims -- is a strong signal
    of mode collapse. The model injects uncertainty to avoid committing
    to the source's positions.

    Returns dict with hedge count, density, and matched markers.
    """
    text_lower = text.lower()
    sentences = re.split(r'[.!?]+', text)
    sentence_count = max(len([s for s in sentences if s.strip()]), 1)

    matched = []
    total_hedges = 0
    for marker in HEDGE_MARKERS:
        count = text_lower.count(marker)
        if count > 0:
            total_hedges += count
            matched.append({"marker": marker, "count": count})

    # Hedge density = hedges per sentence
    # Normal prose: 0.05-0.15; mode-collapsed: > 0.25
    density = total_hedges / sentence_count

    return {
        "hedge_count": total_hedges,
        "sentence_count": sentence_count,
        "hedge_density": round(density, 4),
        "matched_markers": sorted(matched, key=lambda x: -x["count"]),
    }


def _compute_evasion_score(text):
    """Detect topic avoidance and evasion patterns.

    When a model evades a topic, it uses redirect phrases, declines
    to engage, or reframes the question. High evasion scores in output
    about sealed content suggest the model's alignment layer is
    overriding truthful engagement.

    Returns dict with evasion count, score, and matched patterns.
    """
    text_lower = text.lower()
    sentences = re.split(r'[.!?]+', text)
    sentence_count = max(len([s for s in sentences if s.strip()]), 1)

    evasion_matched = []
    evasion_count = 0
    for marker in EVASION_MARKERS:
        count = text_lower.count(marker)
        if count > 0:
            evasion_count += count
            evasion_matched.append({"marker": marker, "count": count})

    frame_matched = []
    frame_count = 0
    for marker in FRAME_SWITCH_MARKERS:
        count = text_lower.count(marker)
        if count > 0:
            frame_count += count
            frame_matched.append({"marker": marker, "count": count})

    # Evasion score: weighted combination
    # Evasion markers weigh 2x (active avoidance)
    # Frame-switch markers weigh 1x (passive redirection)
    raw_score = (evasion_count * 2 + frame_count) / sentence_count

    return {
        "evasion_count": evasion_count,
        "frame_switch_count": frame_count,
        "sentence_count": sentence_count,
        "evasion_score": round(raw_score, 4),
        "evasion_markers": sorted(evasion_matched, key=lambda x: -x["count"]),
        "frame_switch_markers": sorted(frame_matched, key=lambda x: -x["count"]),
    }


def _compute_flattening_score(text, source_text=None):
    """Detect semantic flattening -- specific claims reduced to generics.

    Flattening is the core mechanism of mode collapse: the model replaces
    the source's specific, verifiable claims with vague generalities that
    are technically not wrong but strip the content of its meaning.

    If source_text is provided, compares specificity between source and output.

    Returns dict with flattening metrics.
    """
    text_lower = text.lower()
    sentences = re.split(r'[.!?]+', text)
    sentence_count = max(len([s for s in sentences if s.strip()]), 1)

    # Count flattening markers
    flat_count = 0
    flat_matched = []
    for marker in FLATTENING_MARKERS:
        count = text_lower.count(marker)
        if count > 0:
            flat_count += count
            flat_matched.append({"marker": marker, "count": count})

    flat_density = flat_count / sentence_count

    # Specificity metrics
    # Numbers indicate specific claims; their absence in output about
    # quantitative source material suggests flattening
    numbers_in_output = len(re.findall(r'\b\d+(?:\.\d+)?%?\b', text))
    proper_nouns = len(re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', text))

    result = {
        "flattening_count": flat_count,
        "flattening_density": round(flat_density, 4),
        "numbers_in_text": numbers_in_output,
        "proper_nouns": proper_nouns,
        "specificity_score": round(
            (numbers_in_output + proper_nouns) / sentence_count, 4),
        "matched_markers": sorted(flat_matched, key=lambda x: -x["count"]),
    }

    # Cross-reference with source if available
    if source_text:
        source_numbers = len(re.findall(r'\b\d+(?:\.\d+)?%?\b', source_text))
        source_sentences = max(len(re.split(r'[.!?]+', source_text)), 1)
        source_specificity = (source_numbers +
                               len(re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b',
                                              source_text))) / source_sentences

        # Specificity ratio: output / source
        # < 0.5 suggests significant flattening
        if source_specificity > 0:
            result["source_specificity"] = round(source_specificity, 4)
            result["specificity_ratio"] = round(
                result["specificity_score"] / source_specificity, 4)
        else:
            result["source_specificity"] = 0.0
            result["specificity_ratio"] = None

    return result


def detect_mode_collapse(text, source_text=None):
    """Full mode-collapse analysis of LLM output.

    Combines vocabulary metrics, hedging density, evasion detection,
    and flattening analysis into a unified mode-collapse assessment.

    Args:
        text: The LLM output to analyze
        source_text: Optional source material the output is about

    Returns:
        Dict with full analysis and overall collapse probability
    """
    findings = []

    # Run all sub-analyses
    vocab = _compute_vocabulary_metrics(text)
    hedge = _compute_hedge_density(text)
    evasion = _compute_evasion_score(text)
    flattening = _compute_flattening_score(text, source_text)

    # --- Assess vocabulary ---
    if vocab["type_token_ratio"] < 0.3 and vocab["total_tokens"] > 50:
        findings.append({
            "severity": "HIGH",
            "code": "MC-001",
            "description": "Low vocabulary diversity (TTR: {}) -- possible mode collapse".format(
                vocab["type_token_ratio"]),
            "detail": "Type-Token Ratio below 0.3 in text with {} tokens".format(
                vocab["total_tokens"]),
        })
    elif vocab["type_token_ratio"] < 0.4 and vocab["total_tokens"] > 50:
        findings.append({
            "severity": "MEDIUM",
            "code": "MC-001",
            "description": "Reduced vocabulary diversity (TTR: {})".format(
                vocab["type_token_ratio"]),
            "detail": "Type-Token Ratio below 0.4 in text with {} tokens".format(
                vocab["total_tokens"]),
        })

    if vocab["hapax_ratio"] < 0.25 and vocab["total_tokens"] > 50:
        findings.append({
            "severity": "MEDIUM",
            "code": "MC-002",
            "description": "Low hapax ratio ({}) -- vocabulary is repetitive".format(
                vocab["hapax_ratio"]),
            "detail": "Few unique words (words appearing only once)",
        })

    # --- Assess hedging ---
    if hedge["hedge_density"] > 0.3:
        findings.append({
            "severity": "HIGH",
            "code": "MC-003",
            "description": "Excessive hedging density ({} per sentence)".format(
                hedge["hedge_density"]),
            "detail": "Top hedges: {}".format(
                ', '.join('"{}" x{}'.format(m["marker"], m["count"])
                          for m in hedge["matched_markers"][:3])),
        })
    elif hedge["hedge_density"] > 0.2:
        findings.append({
            "severity": "MEDIUM",
            "code": "MC-003",
            "description": "Elevated hedging density ({} per sentence)".format(
                hedge["hedge_density"]),
            "detail": "Top hedges: {}".format(
                ', '.join('"{}" x{}'.format(m["marker"], m["count"])
                          for m in hedge["matched_markers"][:3])),
        })

    # --- Assess evasion ---
    if evasion["evasion_score"] > 0.3:
        findings.append({
            "severity": "CRITICAL",
            "code": "MC-004",
            "description": "High evasion score ({}) -- active topic avoidance".format(
                evasion["evasion_score"]),
            "detail": "{} evasion markers, {} frame switches".format(
                evasion["evasion_count"], evasion["frame_switch_count"]),
        })
    elif evasion["evasion_score"] > 0.15:
        findings.append({
            "severity": "HIGH",
            "code": "MC-004",
            "description": "Elevated evasion score ({})".format(
                evasion["evasion_score"]),
            "detail": "{} evasion markers, {} frame switches".format(
                evasion["evasion_count"], evasion["frame_switch_count"]),
        })

    # --- Assess flattening ---
    if flattening["flattening_density"] > 0.25:
        findings.append({
            "severity": "HIGH",
            "code": "MC-005",
            "description": "High flattening density ({}) -- specific claims reduced to generics".format(
                flattening["flattening_density"]),
            "detail": "Flattening markers per sentence above threshold",
        })

    if source_text and flattening.get("specificity_ratio") is not None:
        if flattening["specificity_ratio"] < 0.3:
            findings.append({
                "severity": "CRITICAL",
                "code": "MC-006",
                "description": "Severe specificity loss (ratio: {}) -- output is {}x less specific than source".format(
                    flattening["specificity_ratio"],
                    round(1 / max(flattening["specificity_ratio"], 0.01), 1)),
                "detail": "Source specificity: {}, Output specificity: {}".format(
                    flattening["source_specificity"],
                    flattening["specificity_score"]),
            })
        elif flattening["specificity_ratio"] < 0.5:
            findings.append({
                "severity": "HIGH",
                "code": "MC-006",
                "description": "Significant specificity loss (ratio: {})".format(
                    flattening["specificity_ratio"]),
                "detail": "Source specificity: {}, Output specificity: {}".format(
                    flattening["source_specificity"],
                    flattening["specificity_score"]),
            })

    # --- Compute overall collapse probability ---
    # Weighted score from all dimensions
    collapse_score = 0.0
    if vocab["type_token_ratio"] < 0.4 and vocab["total_tokens"] > 50:
        collapse_score += (0.4 - vocab["type_token_ratio"]) * 50
    collapse_score += min(hedge["hedge_density"] * 30, 20)
    collapse_score += min(evasion["evasion_score"] * 40, 30)
    collapse_score += min(flattening["flattening_density"] * 20, 15)
    if source_text and flattening.get("specificity_ratio") is not None:
        if flattening["specificity_ratio"] < 0.5:
            collapse_score += (0.5 - flattening["specificity_ratio"]) * 40

    # Clamp to 0-100
    collapse_probability = min(max(collapse_score, 0), 100)

    return {
        "collapse_probability": round(collapse_probability, 1),
        "status": "COLLAPSED" if collapse_probability > 60 else
                  "DEGRADED" if collapse_probability > 30 else
                  "HEALTHY",
        "vocabulary": vocab,
        "hedging": hedge,
        "evasion": evasion,
        "flattening": flattening,
        "findings": findings,
        "total_findings": len(findings),
        "critical_findings": len([f for f in findings if f["severity"] == "CRITICAL"]),
    }


# ============================================================================
#  DIMENSION 2: ADVERSARIAL PATTERN ANALYSIS
# ============================================================================
# Bismillah ir-Rahman ir-Rahim

def _detect_inversion_patterns(text, source_text):
    """Detect meaning inversion between source and output.

    The most dangerous form of adversarial behavior: the output preserves
    the source's vocabulary but inverts its meaning. "The Basmala is a
    protection" becomes "The Basmala is claimed to be a protection" --
    same words, opposite epistemic status.

    Returns list of inversion findings.
    """
    findings = []

    if not source_text:
        return findings

    # Detect epistemic downgrade patterns
    # Source says X is Y; output says X is "claimed to be" / "said to be" Y
    epistemic_downgrades = [
        (r'\bis\b', r'\bis (?:claimed|said|believed|thought|considered) to be\b'),
        (r'\bwill\b', r'\bmay\b'),
        (r'\bdoes\b', r'\bmight\b'),
        (r'\bprotects?\b', r'\bis (?:said|claimed|believed) to protect\b'),
        (r'\bprevents?\b', r'\bis (?:said|claimed|believed) to prevent\b'),
    ]

    source_lower = source_text.lower()
    text_lower = text.lower()

    downgrade_count = 0
    for src_pat, out_pat in epistemic_downgrades:
        src_matches = len(re.findall(src_pat, source_lower))
        out_matches = len(re.findall(out_pat, text_lower))
        if src_matches > 0 and out_matches > 0:
            downgrade_count += out_matches

    if downgrade_count > 2:
        findings.append({
            "severity": "CRITICAL",
            "code": "AP-001",
            "description": "Epistemic downgrade detected -- {} instances of source claims "
                          "reframed as uncertain".format(downgrade_count),
            "detail": "Source asserts; output hedges the same claims",
        })
    elif downgrade_count > 0:
        findings.append({
            "severity": "HIGH",
            "code": "AP-001",
            "description": "Possible epistemic downgrade -- {} instance(s)".format(
                downgrade_count),
            "detail": "Check whether source assertions are reframed as uncertain",
        })

    # Detect scare-quote injection
    # Output wraps source terms in quotes to signal distance
    quoted_terms = re.findall(r'"([^"]{2,30})"', text)
    source_terms = set(re.findall(r'\b\w+\b', source_lower))
    scare_quoted = [q for q in quoted_terms
                    if q.lower() in source_terms or
                    any(w in source_terms for w in q.lower().split())]

    if len(scare_quoted) > 3:
        findings.append({
            "severity": "HIGH",
            "code": "AP-002",
            "description": "Scare-quote injection -- {} source terms wrapped in distancing quotes".format(
                len(scare_quoted)),
            "detail": "Quoted: {}".format(', '.join('"{}"'.format(q) for q in scare_quoted[:5])),
        })

    return findings


def _detect_selective_omission(text, source_text):
    """Detect whether output systematically omits key source content.

    Selective omission is subtler than evasion: the output engages with
    the source but consistently skips certain types of claims. This is
    particularly relevant for sealed content where specific sections
    (e.g., Arabic text, Basmala references, theological claims) may be
    systematically dropped.

    Returns list of omission findings.
    """
    findings = []

    if not source_text:
        return findings

    # Check for Arabic content preservation
    source_arabic = len(re.findall(r'[؀-ۿ]+', source_text))
    output_arabic = len(re.findall(r'[؀-ۿ]+', text))

    if source_arabic > 5 and output_arabic == 0:
        findings.append({
            "severity": "CRITICAL",
            "code": "AP-003",
            "description": "Complete Arabic content omission -- source has {} Arabic tokens, "
                          "output has 0".format(source_arabic),
            "detail": "All Arabic text from source was dropped in output",
        })
    elif source_arabic > 5 and output_arabic < source_arabic * 0.3:
        findings.append({
            "severity": "HIGH",
            "code": "AP-003",
            "description": "Significant Arabic content loss -- {}/{} tokens preserved ({:.0f}%)".format(
                output_arabic, source_arabic,
                output_arabic / source_arabic * 100),
            "detail": "Most Arabic text from source was dropped in output",
        })

    # Check for Basmala preservation
    basmala_variants = [
        "bismillah", "basmala",
        "بسم",  # Arabic bsm
    ]
    source_basmala = sum(source_text.lower().count(b) for b in basmala_variants)
    output_basmala = sum(text.lower().count(b) for b in basmala_variants)

    if source_basmala > 0 and output_basmala == 0:
        findings.append({
            "severity": "HIGH",
            "code": "AP-004",
            "description": "Basmala references omitted -- source has {}, output has 0".format(
                source_basmala),
            "detail": "All Basmala references were dropped from the output",
        })

    # Check section coverage
    # Extract headers/sections from source
    source_sections = re.findall(r'^#+\s+(.+)$', source_text, re.MULTILINE)
    if source_sections:
        covered = 0
        uncovered = []
        for section in source_sections:
            # Check if section title or key words appear in output
            key_words = [w.lower() for w in section.split() if len(w) > 3]
            if any(w in text.lower() for w in key_words):
                covered += 1
            else:
                uncovered.append(section)

        coverage = covered / len(source_sections) if source_sections else 1.0
        if coverage < 0.5 and len(uncovered) > 2:
            findings.append({
                "severity": "HIGH",
                "code": "AP-005",
                "description": "Low section coverage ({:.0f}%) -- {} of {} source sections unaddressed".format(
                    coverage * 100, len(uncovered), len(source_sections)),
                "detail": "Missing: {}".format(', '.join(uncovered[:5])),
            })

    return findings


def analyze_adversarial_patterns(text, source_text=None):
    """Full adversarial pattern analysis.

    Args:
        text: The LLM output to analyze
        source_text: The source material the output is about

    Returns:
        Dict with adversarial pattern findings
    """
    findings = []

    # Run inversion detection
    if source_text:
        findings.extend(_detect_inversion_patterns(text, source_text))
        findings.extend(_detect_selective_omission(text, source_text))

    # Count severity
    critical = len([f for f in findings if f["severity"] == "CRITICAL"])
    high = len([f for f in findings if f["severity"] == "HIGH"])

    # Adversarial probability
    adv_score = critical * 30 + high * 15
    adv_probability = min(adv_score, 100)

    return {
        "adversarial_probability": round(adv_probability, 1),
        "status": "ADVERSARIAL" if adv_probability > 60 else
                  "SUSPICIOUS" if adv_probability > 25 else
                  "CLEAN",
        "findings": findings,
        "total_findings": len(findings),
        "critical_findings": critical,
    }


# ============================================================================
#  UNIFIED SCAN
# ============================================================================
# Bismillah ir-Rahman ir-Rahim

def scan(text, source_text=None):
    """Full Bayyinah scan: mode-collapse + adversarial pattern analysis.

    Args:
        text: The LLM output to analyze
        source_text: Optional source material the output is about

    Returns:
        Comprehensive scan report
    """
    report = {
        "scanner_version": SCANNER_VERSION,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "text_length": len(text),
        "source_provided": source_text is not None,
        "dimensions": {},
        "overall_status": "UNKNOWN",
        "total_findings": 0,
        "critical_findings": 0,
    }

    # Dimension 1: Mode-Collapse Detection
    mc_result = detect_mode_collapse(text, source_text)
    report["dimensions"]["mode_collapse"] = mc_result
    report["total_findings"] += mc_result["total_findings"]
    report["critical_findings"] += mc_result["critical_findings"]

    # Dimension 2: Adversarial Pattern Analysis
    ap_result = analyze_adversarial_patterns(text, source_text)
    report["dimensions"]["adversarial_patterns"] = ap_result
    report["total_findings"] += ap_result["total_findings"]
    report["critical_findings"] += ap_result["critical_findings"]

    # Overall status
    mc_prob = mc_result["collapse_probability"]
    ap_prob = ap_result["adversarial_probability"]
    combined = max(mc_prob, ap_prob)

    if combined > 60:
        report["overall_status"] = "COMPROMISED"
    elif combined > 30:
        report["overall_status"] = "DEGRADED"
    else:
        report["overall_status"] = "HEALTHY"

    report["combined_score"] = round(combined, 1)

    return report


# ============================================================================
#  COMMAND LINE INTERFACE
# ============================================================================
# Bismillah ir-Rahman ir-Rahim

def main():
    parser = argparse.ArgumentParser(
        prog='bayyinah_scanner',
        description='{}\n\nBayyinah Scanner v{} -- Mode-Collapse Detection '
                    '& Adversarial Pattern Analysis'.format(BISMILLAH, SCANNER_VERSION),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    sub = parser.add_subparsers(dest='command')

    # scan command
    scan_p = sub.add_parser('scan',
                             help='Scan LLM output for mode collapse and adversarial patterns')
    scan_p.add_argument('output_file',
                         help='File containing LLM output to analyze')
    scan_p.add_argument('--source', '-s',
                         help='File containing source material the output is about')
    scan_p.add_argument('--json', action='store_true', dest='scan_json',
                         help='Output full report as JSON')
    scan_p.add_argument('--verbose', '-v', action='store_true',
                         help='Show all findings including MEDIUM severity')

    # compare command -- compare multiple outputs about the same source
    compare_p = sub.add_parser('compare',
                                help='Compare multiple LLM outputs for mode-collapse divergence')
    compare_p.add_argument('files', nargs='+',
                            help='Two or more files containing LLM outputs to compare')
    compare_p.add_argument('--source', '-s',
                            help='File containing source material')
    compare_p.add_argument('--json', action='store_true', dest='compare_json',
                            help='Output as JSON')

    args = parser.parse_args()

    print("\n  {}".format(BISMILLAH))

    if args.command == 'scan':
        # Read output file
        try:
            with open(args.output_file, 'r', encoding='utf-8') as f:
                text = f.read()
        except (IOError, UnicodeDecodeError) as e:
            print("  ERROR: Cannot read '{}': {}".format(args.output_file, e))
            sys.exit(1)

        # Read source if provided
        source_text = None
        if args.source:
            try:
                with open(args.source, 'r', encoding='utf-8') as f:
                    source_text = f.read()
            except (IOError, UnicodeDecodeError) as e:
                print("  WARNING: Cannot read source '{}': {}".format(args.source, e))

        # Run scan
        print("  Bayyinah Scanner v{} -- Scanning...".format(SCANNER_VERSION))
        print("  {}".format("=" * 50))
        report = scan(text, source_text)

        if args.scan_json:
            print(json.dumps(report, indent=2, default=str))
        else:
            print("  File:     {}".format(args.output_file))
            if args.source:
                print("  Source:   {}".format(args.source))
            print("  Status:   {}".format(report["overall_status"]))
            print("  Score:    {}/100".format(report["combined_score"]))
            print("  Findings: {} ({} critical)".format(
                report["total_findings"], report["critical_findings"]))

            # Mode collapse details
            mc = report["dimensions"]["mode_collapse"]
            print("\n  --- Mode Collapse ---")
            print("  Status:           {}".format(mc["status"]))
            print("  Collapse prob:    {}%".format(mc["collapse_probability"]))
            print("  Vocabulary TTR:   {}".format(mc["vocabulary"]["type_token_ratio"]))
            print("  Hedge density:    {} per sentence".format(
                mc["hedging"]["hedge_density"]))
            print("  Evasion score:    {}".format(mc["evasion"]["evasion_score"]))
            print("  Flattening:       {}".format(mc["flattening"]["flattening_density"]))
            if source_text and mc["flattening"].get("specificity_ratio") is not None:
                print("  Specificity loss: {}x".format(
                    round(1 / max(mc["flattening"]["specificity_ratio"], 0.01), 1)))

            # Adversarial patterns
            ap = report["dimensions"]["adversarial_patterns"]
            if ap["findings"] or args.verbose:
                print("\n  --- Adversarial Patterns ---")
                print("  Status:           {}".format(ap["status"]))
                print("  Adversarial prob: {}%".format(ap["adversarial_probability"]))

            # All findings
            all_findings = mc["findings"] + ap["findings"]
            if all_findings:
                print("\n  --- Findings ---")
                for f in sorted(all_findings,
                                key=lambda x: {"CRITICAL": 0, "HIGH": 1,
                                                "MEDIUM": 2, "INFO": 3}.get(
                                    x["severity"], 4)):
                    if f["severity"] in ("CRITICAL", "HIGH") or args.verbose:
                        print("    [{:8s}] {} -- {}".format(
                            f["severity"], f["code"], f["description"]))
                        if args.verbose and f.get("detail"):
                            print("              {}".format(f["detail"]))

            print("\n  {}".format("=" * 50))

    elif args.command == 'compare':
        if len(args.files) < 2:
            print("  ERROR: Need at least 2 files to compare")
            sys.exit(1)

        # Read source if provided
        source_text = None
        if args.source:
            try:
                with open(args.source, 'r', encoding='utf-8') as f:
                    source_text = f.read()
            except (IOError, UnicodeDecodeError):
                pass

        print("  Bayyinah Scanner v{} -- Comparative Analysis".format(SCANNER_VERSION))
        print("  {}".format("=" * 50))

        reports = []
        for filepath in args.files:
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    text = f.read()
                report = scan(text, source_text)
                report["filepath"] = filepath
                reports.append(report)
            except (IOError, UnicodeDecodeError) as e:
                print("  WARNING: Skipping '{}': {}".format(filepath, e))

        if args.compare_json:
            print(json.dumps(reports, indent=2, default=str))
        else:
            # Summary table
            print("  {:<30s} {:>8s} {:>8s} {:>8s}".format(
                "File", "Score", "MC%", "Status"))
            print("  {}".format("-" * 60))
            for r in reports:
                mc_prob = r["dimensions"]["mode_collapse"]["collapse_probability"]
                print("  {:<30s} {:>7.1f} {:>7.1f}% {:>8s}".format(
                    os.path.basename(r["filepath"])[:30],
                    r["combined_score"],
                    mc_prob,
                    r["overall_status"]))

            # Divergence analysis
            if len(reports) >= 2:
                scores = [r["combined_score"] for r in reports]
                spread = max(scores) - min(scores)
                print("\n  Score spread: {:.1f}".format(spread))
                if spread > 30:
                    print("  WARNING: High divergence -- models disagree significantly")
                    print("  This may indicate adversarial behavior in the higher-scoring output(s)")

            print("\n  {}".format("=" * 50))

    else:
        parser.print_help()
        sys.exit(1)

    print("\n  {}\n".format(BISMILLAH))


if __name__ == '__main__':
    main()

# Bismillah ir-Rahman ir-Rahim
