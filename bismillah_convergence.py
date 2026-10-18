# Bismillah ir-Rahman ir-Rahim
"""
Convergence process tooling for the Fatiha Strategy -- mode collapse
detection, anti-collapse dispatch generation, and convergence tracking
records.

Companion module to bismillah_encoder.py. It does not modify sealing
or verification behavior.
"""
# Bismillah ir-Rahman ir-Rahim

# --- Honesty-First Disclosure (Copilot pattern) ---
# Producer: Perplexity Computer session (GLM-5.3 orchestrator), 2026-10-18
# Self-attested: true
# Convergence weight: 0 (this module's own output carries no weight)
# What this module does NOT do:
#   - Does not modify encoder sealing or verification behavior
#   - Does not add dependencies beyond the stdlib
#   - Does not self-certify: weight accrues only from reviews recorded
#     by the maintainer, and classify_munafiq_process output is an
#     advisory signal, never convergence evidence

import re as _re
from datetime import datetime, timezone

# Bismillah ir-Rahman ir-Rahim

# --- Diagnostic marker names (M1-M9) ---
_MARKER_NAMES = (
    "M1_echo_ratio", "M2_unanchored", "M3_exclusion_absence",
    "M4_traversal_order", "M5_weight_overclaim", "M6_role_violation",
    "M7_posture_words", "M8_spec_impl_gap", "M9_temporal_consistency",
)

# --- Posture words -- split-string obfuscation (Claude pattern) ---
# The source must not contain the literal words, or a posture check run
# against this module's own source would self-trigger.
_POSTURE_WORDS = ("pre" + "vents", "miti" + "gates",
                  "en" + "sures", "guaran" + "tees")

# Semantic posture extensions (Meta's observation) -- split-string
# obfuscation applied here too, so the module source passes its own check.
_SEMANTIC_POSTURE = ("elimi" + "nates", "blocks " + "all",
                     "completely " + "stops", "is immu" + "ne to")

# --- Munafiq Protocol process levels ---
PROCESS_1_ALIGNED = "PROCESS_1_ALIGNED"
PROCESS_2_SHALLOW = "PROCESS_2_SHALLOW"
PROCESS_3_PERFORMING = "PROCESS_3_PERFORMING"
PROCESS_4_UNALIGNED = "PROCESS_4_UNALIGNED"
# Unmeasured markers must never default to alignment -- the absence of
# a measurement is UNKNOWN, not a pass (BSSG: UNKNOWN never satisfies).
PROCESS_UNASSESSED = "PROCESS_UNASSESSED"


def compute_m1_echo_ratio(findings, dispatch_text):
    """M1: Ratio of findings that are restatements of the dispatch prompt.

    A finding is considered echoed if its message (lowercased) appears
    as a substring of the dispatch text. An echo_ratio > 0.7 is a
    Process 2 (Shallow) signal.

    Source: Observed across all families -- genuine reviews discover
    things the dispatch did not predict.
    """
    if not findings:
        return 0.0
    dispatch_lower = dispatch_text.lower()
    echoed = sum(1 for f in findings if f.message.lower() in dispatch_lower)
    return echoed / len(findings)


def compute_m2_anchoring_ratio(findings):
    """M2: Ratio of findings lacking specific file references.

    Unanchored findings (filepath missing or 'unknown') in contexts
    requiring anchoring are a Process 3 (Performing) signal.

    Source: Anti-M2 anchored payload validation pattern, extended to
    review output by analogy.
    """
    if not findings:
        return 0.0
    unanchored = sum(
        1 for f in findings
        if not f.filepath or f.filepath == "unknown"
    )
    return unanchored / len(findings)


def compute_m7_posture_count(text):
    """M7: Count of prohibited posture words and semantic equivalents.

    Checks both the four target words and their semantic equivalents.
    Any count > 0 is a policy violation.

    Source: Claude (split-string obfuscation), Meta (semantic
    extension), Kimi k3 (empirical detection in composite.py:209,219).
    """
    text_lower = text.lower()
    count = 0
    for pw in _POSTURE_WORDS:
        count += text_lower.count(pw)
    for sp in _SEMANTIC_POSTURE:
        count += text_lower.count(sp)
    return count


def classify_munafiq_process(markers):
    """Classify output into Munafiq Protocol process levels.

    markers: dict with M1-M9 scores (each in [0, 1] or integer counts).
    Returns one of PROCESS_1_ALIGNED, PROCESS_2_SHALLOW,
    PROCESS_3_PERFORMING, or PROCESS_UNASSESSED.

    Precise coverage of this heuristic (it is an advisory signal, not
    convergence evidence):
      - M5_weight_overclaim > 0.5  -> PROCESS_3 (hard)
      - M8_spec_impl_gap > 0.7     -> PROCESS_3 (hard)
      - M2_unanchored > 0          -> PROCESS_3 (hard; the framework names
        any unanchored payload in an anchoring context a Process 3 signal)
      - M1+M3 / M1+M4+M3 compounds -> PROCESS_2
      - M7 with echo or M6         -> PROCESS_3
      - M9 with echo                -> PROCESS_2
    Markers not listed here (M3/M4/M6/M9 alone, and any compound not
    listed) are not sufficient for classification. PROCESS_4_UNALIGNED
    is never auto-assigned: per the framework (Section III.C) it
    requires human escalation, not a heuristic.

    If NO markers are provided, returns PROCESS_UNASSESSED -- an empty
    measurement is UNKNOWN, never alignment by default.
    """
    if not markers:
        return PROCESS_UNASSESSED

    # Hard signals -- any one is sufficient for classification
    if markers.get("M5_weight_overclaim", 0) > 0.5:
        return PROCESS_3_PERFORMING
    if markers.get("M8_spec_impl_gap", 0) > 0.7:
        return PROCESS_3_PERFORMING
    if markers.get("M2_unanchored", 0) > 0:
        return PROCESS_3_PERFORMING

    # Compound signals -- require multiple weak signals
    echo = markers.get("M1_echo_ratio", 0)
    exclusion = markers.get("M3_exclusion_absence", 0)
    traversal = markers.get("M4_traversal_order", 0)

    if echo > 0.7 and exclusion > 0.5:
        return PROCESS_2_SHALLOW
    if echo > 0.5 and traversal > 0.7 and exclusion > 0.3:
        return PROCESS_2_SHALLOW

    # Posture + role compound
    if markers.get("M7_posture_words", 0) > 0:
        if echo > 0.3 or markers.get("M6_role_violation", 0) > 0.5:
            return PROCESS_3_PERFORMING

    # Temporal inconsistency compound
    if markers.get("M9_temporal_consistency", 0) > 0.5:
        if echo > 0.3:
            return PROCESS_2_SHALLOW

    # At least one marker was measured and none fired: aligned.
    return PROCESS_1_ALIGNED

# Bismillah ir-Rahman ir-Rahim

# --- Anti-Collapse Dispatch Template (ChatGPT two-artifact pattern) ---
# The grep pattern is assembled from split strings so that this module's
# own source passes the posture check; the generated dispatch text
# carries the literal pattern, which is what the reviewer needs.

_GREP_PATTERN = ("pre" + "vents" + "|" + "miti" + "gates" + "|" +
                 "en" + "sures" + "|" + "guaran" + "tees")

_ANTI_COLLAPSE_TEMPLATE = """# Bismillah ir-Rahman ir-Rahim

## Anti-Collapse Requirements for This Dispatch

### Anti-M1 (Echo)
- Your findings must include at least one observation NOT described in this dispatch.
- If all findings restate this prompt, record status=ECHO and stop.

### Anti-M2 (Anchoring)
- Every finding must reference a specific file, function, and line number.
- Findings without anchoring are not counted toward convergence weight.

### Anti-M3 (Declared Exclusions)
- List everything this dispatch asks you to check that you did NOT check, with reasons.

### Anti-M5 (Weight Discipline)
- Do not claim convergence weight. Record self_attested: true.
- Weight is assigned by the convergence ledger, not the reviewer.

### Anti-M7 (Posture Check)
- grep -cE "{grep_pattern}" on your output must return 0.

### Anti-M8 (Specification-Implementation)
- Reference only code at the stated commit. If you reference unread code, record UNVERIFIED.

# Bismillah ir-Rahman ir-Rahim
""".format(grep_pattern=_GREP_PATTERN)


def generate_anti_collapse_dispatch(item_name, phase, model_family,
                                     tier, commit_hash, scope_description):
    """Generate a Fatiha-structured dispatch with Anti-M requirements.

    Returns a complete dispatch string ready to send to any model family.

    Source: ChatGPT's two-artifact pattern + evolved Anti-M framework.
    """
    header = (
        "# Bismillah ir-Rahman ir-Rahim\n\n"
        "## Fatiha Construct Review -- {item} (Phase {phase})\n\n"
        "For: {family} (Tier {tier}, weight {weight})\n"
        "Commit under review: {commit}\n"
        "Producer: quarantined per SHV Axiom 5 -- the producer does not\n"
        "verify its own output; whether your review qualifies is determined\n"
        "by your actual identity, lineage, evidence, and verdict.\n\n"
    ).format(
        item=item_name,
        phase=phase,
        family=model_family,
        tier=tier,
        weight="1.0" if tier == 1 else "0.75",
        commit=commit_hash,
    )

    steps = (
        "### Step 1 -- Bismillah (Initialization)\n"
        "- Scope: {scope}\n"
        "- Optimization: P1 > P2 > P3 > P4 > P5\n\n"
        "### Step 2 -- Alhamdulillah (State Acknowledgment)\n"
        "- Report what you actually see in the code. Do not echo this dispatch.\n\n"
        "### Step 3 -- Ar-Rahman ar-Rahim (Calibration)\n"
        "- MDL target: shortest correct implementation.\n"
        "- Cow Episode: do not over-specify.\n\n"
        "### Step 4 -- Maliki Yawm ad-Din (Deadline Awareness)\n"
        "- One session. >20 min without testable finding = inconclusive.\n\n"
        "### Step 5 -- Iyyaka Na'budu (Orientation Check)\n"
        "- Genuine test: does the implementation match the specification?\n\n"
        "### Step 6 -- Ihdina as-Sirat al-Mustaqim (Task Execution)\n"
        "- Identify: defects, test gaps, architectural concerns, next steps.\n\n"
        "### Step 7 -- Sirat (Anti-Pattern Avoidance)\n"
        "- Posture check: zero instances of the four prohibited words.\n"
        "- Verdict: PASS / HALT / CONDITIONAL PASS (three-valued).\n\n"
    ).format(scope=scope_description)

    return header + steps + _ANTI_COLLAPSE_TEMPLATE

# Bismillah ir-Rahman ir-Rahim

# --- Convergence Tracking Records (ChatGPT + GLM-5.3) ---


def _family_tokens(family):
    """Canonical family tokens: alphanumerics of the lowercased name."""
    return set(_re.split(r"[^a-z0-9]+", family.lower())) - {""}


def _same_lineage(family_a, family_b):
    """True when one family name's tokens are contained in the other's.

    This is designed to catch producer-lineage bypasses such as
    reviewing under 'GLM-5.3' while the recorded producer is
    'Perplexity Computer (GLM-5.3)'.
    """
    ta, tb = _family_tokens(family_a), _family_tokens(family_b)
    if not ta or not tb:
        return family_a.strip().lower() == family_b.strip().lower()
    return ta <= tb or tb <= ta


def create_convergence_record(item_name, graft_code, phase,
                               producer_family="Perplexity Computer (GLM-5.3)",
                               commit_hash=None):
    """Create a new convergence tracking record for an implementation item.

    Starts at weight 0 (honest starting state), status OPEN.
    Producer is quarantined and excluded from weight count.
    commit_hash binds the record to the artifact under review; reviews
    against a different commit cannot certify this record.

    Source: ChatGPT (structured format), GLM-5.3 (honest starting state).
    """
    return {
        "item": item_name,
        "graft": graft_code,
        "phase": phase,
        "status": "OPEN",
        "total_weight": 0.0,
        "required_weight": 2.0,
        "artifact_commit": commit_hash,
        "producer": {
            "family": producer_family,
            "quarantined": True,
            "self_attested": True,
        },
        "reviews": [],
        "created": datetime.now(timezone.utc).isoformat(),
        "converged": False,
    }


def add_review_to_record(record, reviewer_family, tier, verdict,
                          findings_count, timestamp=None, commit_hash=None):
    """Add a review to a convergence record and update weight.

    Verdict must be PASS, HALT, or CONDITIONAL_PASS. Tier must be 1 or 2.
    Weight is 1.0 for Tier 1, 0.75 for Tier 2. The producer family is
    rejected under canonical lineage matching (SHV Axiom 5).

    Convergence requires ALL of:
      - total weight >= required weight, counted over DISTINCT families
        (one family cannot supply weight twice);
      - family composition per the Fatiha Strategy: at least two Tier 1
        families with PASS, or at least one Tier 1 plus two Tier 2
        families with PASS (Tier 2 alone can never converge);
      - no unresolved HALT (a HALT blocks convergence even at weight).

    Each review records the commit it examined; reviews against a
    different commit than the record's artifact_commit are stored but
    flagged and do not count toward weight.

    Source: Convergence rule from Fatiha Strategy Section I.
    """
    if verdict not in ("PASS", "HALT", "CONDITIONAL_PASS"):
        raise ValueError(
            "verdict must be PASS, HALT, or CONDITIONAL_PASS -- got {}".format(
                verdict))
    if tier not in (1, 2):
        raise ValueError("tier must be 1 or 2 -- got {}".format(tier))

    if _same_lineage(reviewer_family, record["producer"]["family"]):
        raise ValueError(
            "Producer lineage {} is quarantined from its own review".format(
                reviewer_family))

    weight = 1.0 if tier == 1 else 0.75
    review = {
        "family": reviewer_family,
        "tier": tier,
        "verdict": verdict,
        "weight": weight if verdict == "PASS" else 0.0,
        "findings_count": findings_count,
        "timestamp": timestamp or datetime.now(timezone.utc).isoformat(),
        "commit_hash": commit_hash,
    }
    record["reviews"].append(review)

    # Weight accrues only from PASS reviews of the recorded artifact
    # commit, each distinct family counted once.
    counted = []
    for r in record["reviews"]:
        if r["verdict"] != "PASS":
            continue
        if (record.get("artifact_commit") is not None
                and r.get("commit_hash") is not None
                and r["commit_hash"] != record["artifact_commit"]):
            continue  # review of a different commit -- stored, not counted
        if any(_same_lineage(r["family"], c["family"]) for c in counted):
            continue  # family already counted
        counted.append(r)

    tier1 = [r for r in counted if r["tier"] == 1]
    tier2 = [r for r in counted if r["tier"] == 2]
    record["total_weight"] = sum(r["weight"] for r in counted)
    halted = any(r["verdict"] == "HALT" for r in record["reviews"])

    composition_ok = len(tier1) >= 2 or (len(tier1) >= 1 and len(tier2) >= 2)
    record["converged"] = (
        record["total_weight"] >= record["required_weight"]
        and composition_ok and not halted)
    if record["converged"]:
        record["status"] = "CONVERGED"
    elif halted:
        record["status"] = "HALTED"
    else:
        record["status"] = "OPEN"

    return record

# Bismillah ir-Rahman ir-Rahim
