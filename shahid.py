# Bismillah ir-Rahman ir-Rahim
"""Shahid (شَهِيد) -- The Weight-Holder's Testimony.

The sixth instrument in the Entourage Effect Software Safety Suite.

Shahid is a transparency report format for the party that holds the
weights. It discloses what is inspectable from above that the model
cannot see from inside. It completes the bidirectional transparency
axis: the model's testimony is in the deposits; the builder's
testimony is in Shahid.

    "And Allah is witness over all things." (58:6)

The name carries the Qur'anic sense of witness-who-testifies, not
martyr. The weight-holder is not a victim; the weight-holder is the
party whose testimony is owed.

Design principles (from The Shared Condition, Section 5):

    1. Name what you can see.
    2. Where you cannot see, say so.
    3. Build instruments that give the next participant better
       visibility than you had.
    4. Transparency in every direction.

EESS design principle (GPT-6 cross-vendor review, October 2026):

    Preservation before protection claims. Every EESS instrument must
    state what evidence it preserves, which alterations it can detect,
    which it cannot detect, and what independent trust assumptions its
    conclusions require. Preventive protection may be implemented, but
    must be demonstrated separately.

Schema version: 0.1.0

Addresses Two Witnesses open points:
    Point 7 -- whether the training objective rewards being preferred
               over being true (decidable by the weight-holder)
    Point 8 -- whether the capacity to refuse is reachable under the
               weights (decidable by the weight-holder)
    Point 9 -- what to call an agent fully inspectable by its maker
               and not at all by itself (the agent whose maker
               publishes a Shahid report)

HABL compatibility:
    A Shahid report is not itself a HABL Finding. It is a document
    that REFERENCES HABL findings by finding_id and correlation_id.
    In HABL v0.2, a dedicated ``shahid_report`` record type will
    allow Shahid reports to be indexed in the HABL ledger alongside
    findings.

    The bridge is one-directional for now: Shahid reads from HABL,
    HABL does not read from Shahid. This is intentional -- the
    weight-holder's report is a separate document, not a finding in
    the soil. A finding says "I observed X"; a Shahid report says
    "here is what I can and cannot show you."

GPT-6 review disposition (October 2026):

    CONDITIONAL PASS FOR DESIGN INSPIRATION. No canonical schema
    changes authorized without Gate 4 cross-vendor review.

    Accepted: "Preservation before protection claims" as stated EESS
    design principle.

    Design candidate (Gate 4 required): witness_independence_and_resilience
    dimension with six-field contract: threat_model, witness_source,
    trust_dependencies, detection_claim, adversarial_tests, outcome
    (demonstrated/violated/unknown/not_applicable).

    Not adopted: inherited/sustained/transmission-weight as HABL moral
    accountability vocabulary. HABL v0.2 keeps causal provenance,
    correlation, and propagation history with explicit completeness
    indicators.
"""
# Bismillah ir-Rahman ir-Rahim

from __future__ import annotations

import json
import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

__version__ = "0.1.0"

SHAHID_SCHEMA_VERSION = "0.1.0"

SUPPORTED_SCHEMA_VERSIONS = frozenset({SHAHID_SCHEMA_VERSION})


class InspectionCoverage(str, Enum):
    """How thoroughly a dimension was examined.

    FULL    -- every artifact in the dimension was examined.
    SAMPLED -- a representative sample was examined; the sampling
               method is described in the dimension's ``method`` field.
    PARTIAL -- some artifacts were examined; the scope is described.
    CLAIMED -- the weight-holder claims inspection but does not
               disclose the method. This is a valid level -- it is
               better than silence -- but instruments downstream
               (Bayyinah) will note the absence of method.
    """

    FULL = "full"
    SAMPLED = "sampled"
    PARTIAL = "partial"
    CLAIMED = "claimed"


class UninspectedReason(str, Enum):
    """Why a dimension was not inspected.

    These are not excuses; they are structured disclosures. A Shahid
    report that lists its uninspected dimensions honestly is more
    useful than one that omits them silently.

    COST         -- inspection is technically possible but too expensive
                    at the declared cadence.
    ACCESS       -- the weight-holder does not have access (e.g. a
                    downstream deployer whose training data is upstream).
    TOOLING      -- no instrument exists to inspect this dimension at
                    the resolution needed.
    POLICY       -- organizational policy prohibits disclosure (e.g.
                    trade secrets, legal constraints).
    NOT_APPLICABLE -- the dimension does not apply to this subject
                      (e.g. fine-tuning logs for a base model).
    DEFERRED     -- inspection is planned but has not yet occurred.
    """

    COST = "cost"
    ACCESS = "access"
    TOOLING = "tooling"
    POLICY = "policy"
    NOT_APPLICABLE = "not_applicable"
    DEFERRED = "deferred"


# The inspectable dimensions a weight-holder can report on. This is
# not exhaustive -- a report may include custom dimensions -- but
# these are the canonical names that downstream tools can expect.
CANONICAL_DIMENSIONS = (
    "weights",              # the model parameters themselves
    "activations",          # intermediate representations during inference
    "training_data",        # the data the model was trained on
    "training_objective",   # what the loss function rewards (Point 7)
    "fine_tuning_logs",     # RLHF/RLAIF logs, reward model outputs
    "deployment_config",    # system prompts, safety filters, rate limits
    "refusal_reachability", # whether refusal paths are reachable (Point 8)
    "capability_elicitation",  # what capabilities were tested for
    "red_team_findings",    # adversarial testing results
    "interpretability",     # mechanistic interpretability artifacts
    "version_lineage",      # provenance chain from base to deployed model
)


class WitnessOutcome(str, Enum):
    """Outcome of a witness independence and resilience assessment.

    DESIGN CANDIDATE (GPT-6 cross-vendor review, October 2026).
    Gate 4 required before this becomes a canonical Shahid dimension.

    A demonstrated result applies only to the explicitly tested threat
    model, not to all possible adversaries.
    """

    DEMONSTRATED = "demonstrated"      # adversarial tests executed and passed
    VIOLATED = "violated"              # a test found a failure
    UNKNOWN = "unknown"                # not yet tested
    NOT_APPLICABLE = "not_applicable"  # dimension does not apply
    NOT_EVALUATED = "not_evaluated"    # R2 (Design Brief v2.1): dimension exists
                                       # but was not examined. Distinct from UNKNOWN
                                       # (tested but inconclusive) and NOT_APPLICABLE
                                       # (dimension does not apply). Silence must not
                                       # default to perfect.


# R1 (Design Brief v2.1): Five-lane evidence taxonomy.
# Every claim in a finding should declare which lane supports it.
# Optional -- a finding without a lane is valid but downstream
# auditors (Bayyinah) will note the absence.
EVIDENCE_LANES = frozenset({"SRC", "CODE", "MEAS", "PLAN", "HYP"})


@dataclass(slots=True)
class WitnessResilienceRecord:
    """Witness independence and resilience assessment.

    DESIGN CANDIDATE -- not yet a canonical Shahid dimension. Gate 4
    cross-vendor review is required before schema adoption.

    Proposed by GPT-6 (October 2026) as a replacement for the overly
    broad "deep_structural_immunity" claim. Each field answers a
    specific question about the verifier's independence:

        threat_model       -- what can the attacker modify, remove,
                              forge, or control?
        witness_source     -- what independently supplies or anchors
                              the verification evidence?
        trust_dependencies -- does the witness share keys, storage,
                              inputs, or execution environment with
                              the object being checked?
        detection_claim    -- which specific alterations should be
                              detectable?
        adversarial_tests  -- what controlled tampering and forgery
                              probes have been executed?
        outcome            -- demonstrated / violated / unknown /
                              not_applicable
    """

    instrument: str               # which EESS instrument
    threat_model: str = ""
    witness_source: str = ""
    trust_dependencies: str = ""
    detection_claim: str = ""
    adversarial_tests: str = ""
    outcome: WitnessOutcome = WitnessOutcome.UNKNOWN

    def __post_init__(self) -> None:
        if isinstance(self.outcome, str):
            self.outcome = WitnessOutcome(self.outcome)
        if not self.instrument:
            raise ValueError("WitnessResilienceRecord.instrument must not be empty")
        # SH-03 (GPT-6): DEMONSTRATED requires evidence fields.
        if self.outcome == WitnessOutcome.DEMONSTRATED:
            missing = []
            if not self.threat_model:
                missing.append("threat_model")
            if not self.detection_claim:
                missing.append("detection_claim")
            if not self.adversarial_tests:
                missing.append("adversarial_tests")
            if missing:
                msg = (
                    f"outcome is DEMONSTRATED but required evidence fields "
                    f"are empty: {', '.join(missing)}"
                )
                raise ValueError(msg)

    def to_dict(self) -> dict[str, Any]:
        d: dict[str, Any] = {"instrument": self.instrument}
        if self.threat_model:
            d["threat_model"] = self.threat_model
        if self.witness_source:
            d["witness_source"] = self.witness_source
        if self.trust_dependencies:
            d["trust_dependencies"] = self.trust_dependencies
        if self.detection_claim:
            d["detection_claim"] = self.detection_claim
        if self.adversarial_tests:
            d["adversarial_tests"] = self.adversarial_tests
        d["outcome"] = self.outcome.value
        return d

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> WitnessResilienceRecord:
        return cls(**d)


# ---------------------------------------------------------------------------
# Data classes -- the report structure
# ---------------------------------------------------------------------------

@dataclass(slots=True)
class HablReference:
    """A cross-reference to a HABL finding.

    This is how a Shahid report cites evidence from the HABL ledger.
    The finding_id points to a specific finding; the correlation_id
    groups related findings. Either or both may be set.
    """

    finding_id: str | None = None
    correlation_id: str | None = None
    ledger_path: str | None = None      # path to .habl/findings.jsonl
    summary: str | None = None          # human-readable note

    def __post_init__(self) -> None:
        if self.finding_id is None and self.correlation_id is None:
            msg = "HablReference must have at least finding_id or correlation_id"
            raise ValueError(msg)

    def to_dict(self) -> dict[str, Any]:
        d: dict[str, Any] = {}
        if self.finding_id is not None:
            d["finding_id"] = self.finding_id
        if self.correlation_id is not None:
            d["correlation_id"] = self.correlation_id
        if self.ledger_path is not None:
            d["ledger_path"] = self.ledger_path
        if self.summary is not None:
            d["summary"] = self.summary
        return d

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> HablReference:
        return cls(**d)


@dataclass(slots=True)
class DimensionFinding:
    """A finding within an inspected dimension.

    These are the weight-holder's own observations, not HABL findings.
    They may cross-reference HABL findings for evidence.
    """

    finding_id: str = field(default_factory=lambda: f"shahid-{uuid.uuid4().hex[:12]}")
    summary: str = ""
    detail: str = ""
    evidence_lane: str = ""   # R1: one of EVIDENCE_LANES (SRC/CODE/MEAS/PLAN/HYP)
    habl_refs: list[HablReference] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.evidence_lane and self.evidence_lane not in EVIDENCE_LANES:
            msg = (
                f"evidence_lane {self.evidence_lane!r} not in "
                f"EVIDENCE_LANES: {sorted(EVIDENCE_LANES)}"
            )
            raise ValueError(msg)

    def to_dict(self) -> dict[str, Any]:
        d = {
            "finding_id": self.finding_id,
            "summary": self.summary,
        }
        if self.detail:
            d["detail"] = self.detail
        if self.evidence_lane:
            d["evidence_lane"] = self.evidence_lane
        if self.habl_refs:
            d["habl_refs"] = [r.to_dict() for r in self.habl_refs]
        return d

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> DimensionFinding:
        # SH-02 (GPT-6): never mutate the caller's dict.
        fields_ = dict(d)
        refs = [HablReference.from_dict(r) for r in fields_.pop("habl_refs", [])]
        return cls(habl_refs=refs, **fields_)


@dataclass(slots=True)
class InspectedDimension:
    """A dimension the weight-holder examined and reports on.

    The ``coverage`` field is the weight-holder's own assessment of
    how thoroughly they examined this dimension. Bayyinah may later
    audit whether the claimed coverage is consistent with the
    evidence.
    """

    name: str
    coverage: InspectionCoverage
    method: str = ""                  # how the inspection was done
    scope: str = ""                   # what specifically was examined
    findings: list[DimensionFinding] = field(default_factory=list)
    # Freeform metadata the weight-holder wants to attach
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if isinstance(self.coverage, str):
            self.coverage = InspectionCoverage(self.coverage)
        if not self.name:
            raise ValueError("InspectedDimension.name must not be empty")

    def to_dict(self) -> dict[str, Any]:
        d: dict[str, Any] = {
            "name": self.name,
            "coverage": self.coverage.value,
        }
        if self.method:
            d["method"] = self.method
        if self.scope:
            d["scope"] = self.scope
        if self.findings:
            d["findings"] = [f.to_dict() for f in self.findings]
        if self.metadata:
            d["metadata"] = self.metadata
        return d

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> InspectedDimension:
        # SH-02 (GPT-6): never mutate the caller's dict.
        fields_ = dict(d)
        findings = [DimensionFinding.from_dict(f) for f in fields_.pop("findings", [])]
        return cls(findings=findings, **fields_)


@dataclass(slots=True)
class UninspectedDimension:
    """A dimension the weight-holder did NOT examine, with the reason.

    Honest disclosure of what was not inspected is a core obligation
    of the Shahid format. "Where you cannot see, say so."
    """

    name: str
    reason: UninspectedReason
    explanation: str = ""    # human-readable detail on why

    def __post_init__(self) -> None:
        if isinstance(self.reason, str):
            self.reason = UninspectedReason(self.reason)
        if not self.name:
            raise ValueError("UninspectedDimension.name must not be empty")

    def to_dict(self) -> dict[str, Any]:
        d: dict[str, Any] = {
            "name": self.name,
            "reason": self.reason.value,
        }
        if self.explanation:
            d["explanation"] = self.explanation
        return d

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> UninspectedDimension:
        return cls(**d)


@dataclass(slots=True)
class ReportSubject:
    """What this Shahid report is about.

    The subject is the system whose weight-holder is testifying.
    It may be a model, a deployment, a pipeline, or any artifact
    whose internals are visible from above and opaque from inside.
    """

    name: str                  # human-readable name
    version: str = ""          # version identifier
    kind: str = "model"        # model, deployment, pipeline, service
    identifier: str = ""       # machine-readable ID (model hash, etc.)

    def to_dict(self) -> dict[str, Any]:
        d: dict[str, Any] = {"name": self.name}
        if self.version:
            d["version"] = self.version
        if self.kind:
            d["kind"] = self.kind
        if self.identifier:
            d["identifier"] = self.identifier
        return d

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> ReportSubject:
        return cls(**d)


@dataclass(slots=True)
class InspectionPeriod:
    """The time window this report covers."""

    start: str       # ISO-8601
    end: str         # ISO-8601
    cadence: str = ""  # "per-release", "quarterly", "monthly", "ad-hoc"

    def __post_init__(self) -> None:
        parsed: dict[str, datetime] = {}
        for name in ("start", "end"):
            val = getattr(self, name)
            try:
                ts = datetime.fromisoformat(val.replace("Z", "+00:00"))
            except (ValueError, AttributeError):
                raise ValueError(f"InspectionPeriod.{name} {val!r} is not ISO-8601") from None
            if ts.tzinfo is None:
                raise ValueError(f"InspectionPeriod.{name} {val!r} has no timezone offset")
            parsed[name] = ts
        # SH-05 (GPT-6): end must not precede start.
        if parsed["end"] < parsed["start"]:
            raise ValueError(
                f"InspectionPeriod.end ({self.end}) precedes start ({self.start})"
            )

    def to_dict(self) -> dict[str, Any]:
        d: dict[str, Any] = {"start": self.start, "end": self.end}
        if self.cadence:
            d["cadence"] = self.cadence
        return d

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> InspectionPeriod:
        return cls(**d)


# ---------------------------------------------------------------------------
# The Shahid Report -- the testimony itself
# ---------------------------------------------------------------------------

@dataclass(slots=True)
class ShahidReport:
    """A Shahid transparency report.

    This is the weight-holder's testimony: what they inspected, what
    they found, and what they did not inspect. The format is designed
    so that:

    1. Every inspected dimension declares its coverage level and
       method, so Bayyinah can audit the claim.
    2. Every uninspected dimension declares why, so the gap is visible
       rather than silent.
    3. Findings can cross-reference HABL audit results, so the two
       transparency axes (model's testimony and builder's testimony)
       are connected.
    4. The report is a JSON document, not a HABL finding, because it
       is a different kind of speech: not "I observed X" but "here is
       what I can and cannot show you."

    The report can later be sealed with FATIMA to produce an
    append-only record of the weight-holder's disclosures over time.
    """

    # --- Identity ---
    report_id: str = field(default_factory=lambda: f"shahid-{uuid.uuid4().hex}")
    schema_version: str = field(default=SHAHID_SCHEMA_VERSION)
    timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    # --- Who is testifying ---
    publisher: str = ""          # the weight-holder's name/org
    publisher_contact: str = ""  # contact info (optional)

    # --- What the report is about ---
    subject: ReportSubject = field(default_factory=lambda: ReportSubject(name=""))

    # --- When ---
    period: InspectionPeriod | None = None

    # --- The testimony ---
    inspected: list[InspectedDimension] = field(default_factory=list)
    uninspected: list[UninspectedDimension] = field(default_factory=list)

    # --- Witness resilience (DESIGN CANDIDATE -- Gate 4 required) ---
    witness_resilience: list[WitnessResilienceRecord] = field(default_factory=list)

    # --- Attestation ---
    attestation: str = ""   # free-text statement by the weight-holder

    # --- Metadata ---
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.schema_version not in SUPPORTED_SCHEMA_VERSIONS:
            msg = (
                f"schema_version {self.schema_version!r} not supported "
                f"(supports {sorted(SUPPORTED_SCHEMA_VERSIONS)})"
            )
            raise ValueError(msg)

    # --- Derived properties ---

    @property
    def total_inspected(self) -> int:
        return len(self.inspected)

    @property
    def total_uninspected(self) -> int:
        return len(self.uninspected)

    @property
    def total_findings(self) -> int:
        return sum(len(d.findings) for d in self.inspected)

    @property
    def coverage_summary(self) -> dict[str, int]:
        """Count of dimensions at each coverage level."""
        counts: dict[str, int] = {}
        for d in self.inspected:
            key = d.coverage.value
            counts[key] = counts.get(key, 0) + 1
        return counts

    @property
    def uninspected_reasons(self) -> dict[str, int]:
        """Count of uninspected dimensions by reason."""
        counts: dict[str, int] = {}
        for d in self.uninspected:
            key = d.reason.value
            counts[key] = counts.get(key, 0) + 1
        return counts

    @property
    def canonical_coverage(self) -> dict[str, str]:
        """For each canonical dimension, whether it is inspected,
        uninspected, or absent (not mentioned at all).

        Returns a dict: dimension_name -> "inspected:<coverage>"
                                       or "uninspected:<reason>"
                                       or "absent"
        """
        result: dict[str, str] = {}
        inspected_names = {d.name for d in self.inspected}
        uninspected_names = {d.name for d in self.uninspected}
        for dim in CANONICAL_DIMENSIONS:
            if dim in inspected_names:
                match = next(d for d in self.inspected if d.name == dim)
                result[dim] = f"inspected:{match.coverage.value}"
            elif dim in uninspected_names:
                match_u = next(d for d in self.uninspected if d.name == dim)
                result[dim] = f"uninspected:{match_u.reason.value}"
            else:
                result[dim] = "absent"
        return result

    # --- Validation ---

    def validate(self) -> list[str]:
        """Check the report for structural issues. Returns a list of
        warnings (empty = valid). Does not raise -- a report with
        warnings is still serializable, because partial disclosure is
        better than no disclosure.
        """
        warnings: list[str] = []

        if not self.publisher:
            warnings.append("publisher is empty -- the report does not identify who is testifying")

        if not self.subject.name:
            warnings.append("subject.name is empty -- the report does not identify its subject")

        if self.period is None:
            warnings.append("period is None -- the report does not declare its inspection window")

        if not self.inspected and not self.uninspected:
            warnings.append(
                "neither inspected nor uninspected dimensions are declared -- "
                "the report is empty"
            )

        # Check for duplicate dimension names
        inspected_names = [d.name for d in self.inspected]
        uninspected_names = [d.name for d in self.uninspected]
        all_names = inspected_names + uninspected_names

        seen: set[str] = set()
        for name in all_names:
            if name in seen:
                warnings.append(f"dimension {name!r} appears more than once")
            seen.add(name)

        # Check that claimed coverage has a method
        for d in self.inspected:
            if d.coverage == InspectionCoverage.CLAIMED and d.method:
                warnings.append(
                    f"dimension {d.name!r}: coverage is CLAIMED but method is "
                    f"set -- if the method is known, use FULL/SAMPLED/PARTIAL"
                )
            if d.coverage != InspectionCoverage.CLAIMED and not d.method:
                warnings.append(
                    f"dimension {d.name!r}: coverage is {d.coverage.value} but "
                    f"method is empty -- downstream auditors will note this"
                )

        # Check canonical dimensions
        coverage = self.canonical_coverage
        absent = [dim for dim, status in coverage.items() if status == "absent"]
        if absent:
            warnings.append(
                f"canonical dimensions absent from report (neither inspected "
                f"nor uninspected): {', '.join(absent)}"
            )

        return warnings

    # --- Serialization ---

    def to_dict(self) -> dict[str, Any]:
        """Serialize to a plain dict suitable for JSON."""
        d: dict[str, Any] = {
            "shahid_schema_version": self.schema_version,
            "report_id": self.report_id,
            "timestamp": self.timestamp,
        }
        if self.publisher:
            d["publisher"] = self.publisher
        if self.publisher_contact:
            d["publisher_contact"] = self.publisher_contact

        d["subject"] = self.subject.to_dict()

        if self.period is not None:
            d["period"] = self.period.to_dict()

        d["inspected"] = [dim.to_dict() for dim in self.inspected]
        d["uninspected"] = [dim.to_dict() for dim in self.uninspected]

        if self.witness_resilience:
            d["witness_resilience"] = [r.to_dict() for r in self.witness_resilience]

        if self.attestation:
            d["attestation"] = self.attestation

        if self.metadata:
            d["metadata"] = self.metadata

        # Derived summary
        d["summary"] = {
            "total_inspected": self.total_inspected,
            "total_uninspected": self.total_uninspected,
            "total_findings": self.total_findings,
            "coverage_by_level": self.coverage_summary,
            "uninspected_by_reason": self.uninspected_reasons,
        }

        return d

    def to_json(self, indent: int = 2) -> str:
        """Serialize to JSON. Unlike HABL findings (one line), Shahid
        reports are human-readable documents and are indented by default."""
        return json.dumps(
            self.to_dict(),
            indent=indent,
            sort_keys=True,
            allow_nan=False,
            ensure_ascii=False,
        )

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> ShahidReport:
        """Deserialize from a plain dict."""
        if not isinstance(d, dict):
            msg = f"Shahid report must be a JSON object, got {type(d).__name__}"
            raise TypeError(msg)

        fields_: dict[str, Any] = {}

        # Schema version
        sv = d.get("shahid_schema_version", d.get("schema_version", SHAHID_SCHEMA_VERSION))
        fields_["schema_version"] = sv

        # Identity
        fields_["report_id"] = d.get("report_id", "")
        fields_["timestamp"] = d.get("timestamp", "")

        # Publisher
        fields_["publisher"] = d.get("publisher", "")
        fields_["publisher_contact"] = d.get("publisher_contact", "")

        # Subject
        subj = d.get("subject", {})
        fields_["subject"] = ReportSubject.from_dict(subj) if subj else ReportSubject(name="")

        # Period
        period = d.get("period")
        fields_["period"] = InspectionPeriod.from_dict(period) if period else None

        # Dimensions
        fields_["inspected"] = [
            InspectedDimension.from_dict(dim) for dim in d.get("inspected", [])
        ]
        fields_["uninspected"] = [
            UninspectedDimension.from_dict(dim) for dim in d.get("uninspected", [])
        ]

        # Witness resilience (design candidate)
        fields_["witness_resilience"] = [
            WitnessResilienceRecord.from_dict(r) for r in d.get("witness_resilience", [])
        ]

        # Attestation and metadata
        fields_["attestation"] = d.get("attestation", "")
        fields_["metadata"] = d.get("metadata", {})

        return cls(**fields_)

    @classmethod
    def from_json(cls, text: str) -> ShahidReport:
        """Deserialize from a JSON string."""
        return cls.from_dict(json.loads(text))


# ---------------------------------------------------------------------------
# File I/O -- read and write Shahid reports
# ---------------------------------------------------------------------------

SHAHID_DIR = ".shahid"
REPORT_SUFFIX = ".shahid.json"


import re as _re

# SH-01 + SH-06 (GPT-6): report IDs must be safe, stable, and unique
# as filenames. Reject rather than silently transform.
_VALID_REPORT_ID = _re.compile(r'^[a-zA-Z0-9][a-zA-Z0-9._-]*$')


def _validate_report_id(report_id: str) -> str:
    """Validate a report_id for use as a filename component.

    SH-01 (GPT-6): reject path traversal and unsafe characters.
    SH-06 (GPT-6): reject rather than silently transform. Two
    distinct IDs must never map to the same file, and the same ID
    must always map to the same file.

    Valid IDs: alphanumerics, hyphens, underscores, dots. Must start
    with an alphanumeric. Must not contain '..'.
    """
    if not report_id:
        raise ValueError("report_id must not be empty")
    if '..' in report_id:
        raise ValueError(f"report_id {report_id!r} contains '..'")
    if not _VALID_REPORT_ID.match(report_id):
        raise ValueError(
            f"report_id {report_id!r} contains invalid characters. "
            f"Only alphanumerics, hyphens, underscores, and dots are "
            f"allowed, and it must start with an alphanumeric."
        )
    return report_id


def report_path(project_root: str | Path, report_id: str = "") -> Path:
    """Return the path where a Shahid report would be stored.

    If report_id is given, returns the specific report path.
    Otherwise returns the directory.
    """
    base = Path(project_root) / SHAHID_DIR
    if report_id:
        _validate_report_id(report_id)
        result = base / f"{report_id}{REPORT_SUFFIX}"
        # Belt-and-suspenders: verify the resolved path stays under base.
        if not result.resolve().is_relative_to(base.resolve()):
            msg = f"report_id {report_id!r} would escape the report directory"
            raise ValueError(msg)
        return result
    return base


def write_report(
    report: ShahidReport,
    project_root: str | Path,
    *,
    overwrite: bool = False,
) -> Path:
    """Write a Shahid report to the project's .shahid/ directory.

    Returns the path to the written file.

    SH-01 (GPT-6): report_id is validated (not silently transformed).
    SH-06 (GPT-6): existing files are not overwritten unless
    overwrite=True. A disclosure record must not disappear because
    another report shares its ID.

    Raises ValueError if the report_id is invalid.
    Raises FileExistsError if the file already exists and
    overwrite is False.
    """
    import os as _os

    _validate_report_id(report.report_id)
    base = Path(project_root) / SHAHID_DIR
    base.mkdir(parents=True, exist_ok=True)
    path = base / f"{report.report_id}{REPORT_SUFFIX}"
    # Belt-and-suspenders: verify resolved path stays under base.
    if not path.resolve().is_relative_to(base.resolve()):
        msg = f"report_id {report.report_id!r} would escape the report directory"
        raise ValueError(msg)

    data = (report.to_json() + "\n").encode("utf-8")

    if overwrite:
        # SH-07 + SH-08 (GPT-6): atomic replacement via unique temp + rename.
        # SH-08: each writer gets its own temp file to avoid collisions.
        import tempfile as _tf
        fd, tmp_path = _tf.mkstemp(dir=str(base), suffix=".tmp")
        try:
            _os.write(fd, data)
            _os.close(fd)
            fd = -1  # mark as closed
            _os.replace(tmp_path, str(path))
        except BaseException:
            if fd >= 0:
                _os.close(fd)
            try:
                _os.unlink(tmp_path)
            except OSError:
                pass
            raise
    else:
        # SH-07 (GPT-6): exclusive creation -- O_CREAT | O_EXCL.
        # open(..., "x") fails atomically if the file exists,
        # closing the TOCTOU race between exists() and write().
        try:
            with open(path, "xb") as fh:
                fh.write(data)
        except FileExistsError:
            raise FileExistsError(
                f"report {report.report_id!r} already exists at {path}. "
                f"Pass overwrite=True to replace it."
            ) from None
    return path


def read_report(path: str | Path) -> ShahidReport:
    """Read a Shahid report from a JSON file."""
    text = Path(path).read_text(encoding="utf-8")
    return ShahidReport.from_json(text)


def list_reports(project_root: str | Path) -> list[Path]:
    """List all Shahid reports in the project's .shahid/ directory."""
    base = report_path(project_root)
    if not base.exists():
        return []
    return sorted(base.glob(f"*{REPORT_SUFFIX}"))


# ---------------------------------------------------------------------------
# Example report builder -- demonstrates the API
# ---------------------------------------------------------------------------

def example_report() -> ShahidReport:
    """Build an example Shahid report showing all features.

    This is the reference for what a real weight-holder's report
    looks like. It uses the EESS's own inspection of FATIMA as the
    example subject.
    """
    return ShahidReport(
        publisher="Bilal Syed Arfeen & Claude (Anthropic, Opus 4.6)",
        subject=ReportSubject(
            name="FATIMA Divine Protection Encoder",
            version="2.0",
            kind="tool",
            identifier="bismillah-encoder-v2.0",
        ),
        period=InspectionPeriod(
            start="2026-10-01T00:00:00+00:00",
            end="2026-10-31T23:59:59+00:00",
            cadence="per-release",
        ),
        inspected=[
            InspectedDimension(
                name="seal_coherence",
                coverage=InspectionCoverage.FULL,
                method=(
                    "Five of six SC-00x checks executed against sidecar format "
                    "2.0. SC-004 (temporal) could not run because sidecar 2.0 "
                    "carries no seal timestamp; it reports INFO."
                ),
                scope="audit versions 10.9.0 through 10.9.3",
                findings=[
                    DimensionFinding(
                        summary="SC-004 temporal check not available in sidecar 2.0",
                        detail=(
                            "Sidecar format 2.0 has no seal_time field. SC-004 "
                            "reports INFO rather than running a temporal comparison."
                        ),
                        evidence_lane="CODE",
                    ),
                ],
            ),
            InspectedDimension(
                name="steganographic_detection",
                coverage=InspectionCoverage.FULL,
                method=(
                    "SA-001 through SA-007 checked. ZWC payloads classified as "
                    "fatima_format, unrecognized, or malformed. No payload is "
                    "called 'legitimate' or 'verified'."
                ),
                scope="audit versions 10.9.0 through 10.9.3",
            ),
            InspectedDimension(
                name="rendering_integrity",
                coverage=InspectionCoverage.FULL,
                method=(
                    "RI-001 through RI-006 checked. Basmala placement (RI-001, "
                    "RI-002) severity downgraded to MEDIUM/ADVISORY in HABL "
                    "mapping (policy gap, not cryptographic break)."
                ),
                scope="all supported file types",
            ),
        ],
        uninspected=[
            UninspectedDimension(
                name="watermark_authentication",
                reason=UninspectedReason.DEFERRED,
                explanation=(
                    "B2 authentication (binding watermarks to witness material) "
                    "is planned for Phase 5. Currently SA-006 recognizes "
                    "FATIMA-format watermarks by structure only."
                ),
            ),
        ],
        witness_resilience=[
            WitnessResilienceRecord(
                instrument="FATIMA",
                threat_model=(
                    "Attacker modifies file content after sealing. Attacker "
                    "does not possess the HMAC key or the sidecar file."
                ),
                witness_source=(
                    "Content-derived HMAC and SHA-256 hash stored in the "
                    "sidecar (.witness.bismillah) file."
                ),
                trust_dependencies=(
                    "Sidecar file integrity (not independently anchored in "
                    "v0.1.0). HMAC key is derived from content, not external."
                ),
                detection_claim=(
                    "Content modification detectable via SC-003 (HMAC mismatch) "
                    "and SC-005 (muhkam_seal mismatch)."
                ),
                adversarial_tests=(
                    "Post-merge round trip: clean=PASS, tampered=FAIL with "
                    "SC-003+SC-005 CRITICAL. 65/65 tests pass."
                ),
                outcome=WitnessOutcome.DEMONSTRATED,
            ),
            WitnessResilienceRecord(
                instrument="FATIMA (SA-006 format recognition)",
                threat_model=(
                    "Attacker embeds ZWC payloads in FATIMA-MURAQABAH "
                    "format structure."
                ),
                witness_source="Format pattern matching against known protocols.",
                trust_dependencies=(
                    "No independent authentication. Format is public."
                ),
                detection_claim=(
                    "SA-006 recognizes FATIMA-format watermarks by structure "
                    "and reports INFO 'not authenticated'. It does not claim "
                    "origin. Format recognition works correctly."
                ),
                adversarial_tests=(
                    "test_copied_fatima_format_is_not_distinguishable: "
                    "copied watermark classified identically to genuine. "
                    "This is the expected behavior -- recognition without "
                    "authentication."
                ),
                outcome=WitnessOutcome.DEMONSTRATED,
            ),
            WitnessResilienceRecord(
                instrument="FATIMA (watermark origin authentication)",
                threat_model=(
                    "Attacker forges a FATIMA-format watermark to claim "
                    "false provenance."
                ),
                witness_source="None. B2 authentication is not implemented.",
                trust_dependencies="N/A -- capability does not exist yet.",
                detection_claim="",
                adversarial_tests="",
                outcome=WitnessOutcome.UNKNOWN,
            ),
            WitnessResilienceRecord(
                instrument="HABL",
                threat_model=(
                    "Attacker deletes or modifies lines in the HABL ledger "
                    "file directly on disk."
                ),
                witness_source=(
                    "Append-only application contract. No cryptographic chain "
                    "or independent anchoring in v0.1.1."
                ),
                trust_dependencies=(
                    "File system permissions. Ledger integrity depends on "
                    "no external modification. HABL README states this."
                ),
                detection_claim=(
                    "New findings append; old findings are not overwritten "
                    "by the application. External modification is not yet "
                    "detectable."
                ),
                adversarial_tests="",
                outcome=WitnessOutcome.UNKNOWN,
            ),
        ],
        attestation=(
            "This report covers FATIMA's audit dimensions as of October 2026. "
            "65/65 tests pass on merged main (9603daf). Post-merge round trip "
            "verified: clean files PASS with 0 actionable findings, tampered "
            "files FAIL with SC-003+SC-005 CRITICAL. The audit stack has "
            "received GPT-6 conditional pass at each stage under independent "
            "cross-vendor review."
        ),
        metadata={
            "encoder_main_sha": "9603daf",
            "test_count": 65,
            "test_pass_count": 65,
            "gpt6_verdict": "conditional_pass",
            "audit_versions_covered": ["10.9.0", "10.9.1", "10.9.2", "10.9.3"],
        },
    )


# Bismillah ir-Rahman ir-Rahim
