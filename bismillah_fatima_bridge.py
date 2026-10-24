# Bismillah ir-Rahman ir-Rahim
"""
FATIMA Bridge Module — Full Implementation (v10.8.0)

This module bridges the Bismillah Encoder with FATIMA
(Fitrah-Aligned Tawhidic Integrity for Meaning and Authenticity).

Implements the formal semantic contract Γ (Council Action Item 4):
  Γ: EncoderOutput × FindingSet → FATIMAReport

The four bridge functions map between the encoder's 5-engine integrity
model and the FATIMA attestation format, enabling furqan-lint to
consume Bismillah integrity data as first-class diagnostics.

Five Engines (BSSG Five-Conjunct Kernel):
  1. Semantic   — Shannon's Boundary (meaning preservation)
  2. Temporal   — Living Witness (version-chain integrity)
  3. Relational — Ummah Witness (cross-file dependency integrity)
  4. Adversarial — Muhasabah Engine (self-reckoning resilience)
  5. Generative — Khalifah Gate (generative fidelity)

Author: Bilal Syed Arfeen
License: MIT — free for the ummah, free for all of creation, in sha Allah
"""
# Bismillah ir-Rahman ir-Rahim

import os
import hashlib
import json
from collections import OrderedDict
from pathlib import Path
from datetime import datetime, timezone

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

BISMILLAH = "Bismillah ir-Rahman ir-Rahim"
BRIDGE_VERSION = "10.8.0"
CONTRACT_GAMMA = "Γ:v1"  # Formal semantic contract version

# The five conjuncts of the BSSG kernel, mapped to engine names
FIVE_CONJUNCTS = (
    "semantic",      # Shannon's Boundary — meaning preservation
    "temporal",      # Living Witness — version-chain integrity
    "relational",    # Ummah Witness — cross-file dependency integrity
    "adversarial",   # Muhasabah Engine — self-reckoning resilience
    "generative",    # Khalifah Gate — generative fidelity
)

# Severity thresholds for FATIMA grading
GRADE_THRESHOLDS = {
    "muhkam":      0.95,   # Firm — highest integrity
    "mutashabih":  0.80,   # Allegorical — high integrity, some ambiguity
    "hasan":       0.60,   # Good — acceptable integrity
    "da'if":       0.40,   # Weak — integrity concerns
    "mawdu":       0.00,   # Fabricated — integrity failure
}


# ---------------------------------------------------------------------------
# FATIMAReport
# ---------------------------------------------------------------------------

class FATIMAReport:
    """Report object for FATIMA integrity analysis.

    A FATIMAReport encapsulates the results of running the five-conjunct
    BSSG kernel over a set of findings or verification results. It
    provides both machine-readable scores and human-readable grades
    aligned with Islamic hadith science terminology.

    Attributes:
        contract: str — the semantic contract version (Γ:v1)
        bridge_version: str — the bridge module version
        timestamp: str — ISO 8601 timestamp of report generation
        conjunct_scores: dict — per-conjunct float scores [0.0, 1.0]
        conjunct_grades: dict — per-conjunct grade strings
        overall_score: float — weighted mean of conjunct scores
        overall_grade: str — grade derived from overall_score
        findings_count: int — number of findings processed
        engine_details: dict — per-engine detailed results
    """

    def __init__(self, **kwargs):
        self.data = OrderedDict(kwargs)
        # Set defaults
        self.data.setdefault("contract", CONTRACT_GAMMA)
        self.data.setdefault("bridge_version", BRIDGE_VERSION)
        self.data.setdefault("timestamp",
                             datetime.now(timezone.utc).isoformat())
        for k, v in self.data.items():
            setattr(self, k, v)

    def __repr__(self):
        grade = getattr(self, "overall_grade", "?")
        score = getattr(self, "overall_score", 0.0)
        return "FATIMAReport(grade={!r}, score={:.4f})".format(grade, score)

    def to_dict(self):
        return dict(self.data)

    def to_json(self, indent=2):
        """Serialize report to JSON string."""
        return json.dumps(self.to_dict(), indent=indent, default=str)


# ---------------------------------------------------------------------------
# Grading
# ---------------------------------------------------------------------------

def _grade_score(score):
    """Map a [0.0, 1.0] score to an Islamic hadith science grade.

    Grading scale (from hadith authentication methodology):
      muhkam     (>= 0.95): Firm, unambiguous integrity
      mutashabih (>= 0.80): High integrity, some allegorical ambiguity
      hasan      (>= 0.60): Good, acceptable integrity
      da'if      (>= 0.40): Weak, integrity concerns present
      mawdu      (<  0.40): Fabricated, integrity failure
    """
    for grade, threshold in GRADE_THRESHOLDS.items():
        if score >= threshold:
            return grade
    return "mawdu"


# ---------------------------------------------------------------------------
# Bond Graph Encoding
# ---------------------------------------------------------------------------

def encode_repo_bond_graph(repo_path, **kwargs):
    """Encode a repository's dependency and integrity structure as a
    FATIMA bond graph.

    The bond graph represents files as nodes and their integrity
    relationships (imports, shared seals, dependency chains) as edges.
    Each node carries its Bismillah seal, semantic hash, and temporal
    witness state. Each edge carries a kinship score from the Ummah
    Witness engine.

    Args:
        repo_path: Path to the repository root.
        include_hidden: bool — include hidden files (default False).
        extensions: set — file extensions to include (default: all text).

    Returns:
        dict: Bond graph with 'nodes', 'edges', 'meta' keys.
            nodes: list of {id, path, seal, semantic_hash, ...}
            edges: list of {source, target, kind, strength}
            meta: {repo_path, timestamp, node_count, edge_count, ...}
    """
    repo_path = Path(repo_path).resolve()
    if not repo_path.is_dir():
        raise FileNotFoundError(
            "Repository path does not exist: {}".format(repo_path))

    include_hidden = kwargs.get("include_hidden", False)
    extensions = kwargs.get("extensions", None)

    nodes = []
    file_index = {}  # path -> node index
    edges = []

    # Walk the repository and build nodes
    for dirpath, dirnames, filenames in os.walk(str(repo_path)):
        # Skip hidden and VCS directories
        if not include_hidden:
            dirnames[:] = [d for d in dirnames
                           if not d.startswith('.') and d != '__pycache__'
                           and d != 'node_modules' and d != '.git']

        for fname in filenames:
            if not include_hidden and fname.startswith('.'):
                continue
            filepath = os.path.join(dirpath, fname)
            ext = os.path.splitext(fname)[1].lower()

            # Skip non-text and sidecar files
            if fname.endswith('.bismillah'):
                continue
            if extensions and ext not in extensions:
                continue

            try:
                with open(filepath, 'rb') as f:
                    content = f.read()
            except (IOError, OSError):
                continue

            # Compute Bismillah-anchored seal
            h = hashlib.sha256()
            h.update(BISMILLAH.encode('utf-8'))
            h.update(content)
            h.update(BISMILLAH.encode('utf-8'))
            seal = h.hexdigest()

            # Compute content fingerprint for dependency detection
            content_hash = hashlib.sha256(content).hexdigest()

            rel_path = os.path.relpath(filepath, str(repo_path))
            node_id = len(nodes)
            file_index[rel_path] = node_id

            node = {
                "id": node_id,
                "path": rel_path,
                "seal": seal,
                "content_hash": content_hash,
                "size": len(content),
                "extension": ext,
                "has_witness": os.path.exists(filepath + '.witness.bismillah'),
                "has_bismillah_marker": (
                    b'ismillah' in content[:4000]
                    or b'ISMILLAH' in content[:4000]
                ),
            }
            nodes.append(node)

    # Build edges from import/dependency analysis
    for node in nodes:
        if node["extension"] in ('.py', '.rs', '.go'):
            filepath = os.path.join(str(repo_path), node["path"])
            try:
                with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
                    source = f.read()
            except (IOError, OSError):
                continue

            deps = _extract_dependencies(source, node["extension"])
            for dep_path in deps:
                # Resolve dependency to a node in the graph
                resolved = _resolve_dep(dep_path, node["path"],
                                        file_index, node["extension"])
                if resolved is not None and resolved != node["id"]:
                    # Compute kinship strength from content similarity
                    strength = _compute_bond_strength(
                        nodes[node["id"]], nodes[resolved])
                    edges.append({
                        "source": node["id"],
                        "target": resolved,
                        "kind": "import",
                        "strength": strength,
                    })

    # Compute graph-level seal
    graph_h = hashlib.sha256()
    graph_h.update(BISMILLAH.encode('utf-8'))
    for n in nodes:
        graph_h.update(n["seal"].encode('utf-8'))
    for e in edges:
        graph_h.update("{}->{}".format(e["source"], e["target"]).encode('utf-8'))
    graph_h.update(BISMILLAH.encode('utf-8'))

    meta = {
        "repo_path": str(repo_path),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "node_count": len(nodes),
        "edge_count": len(edges),
        "graph_seal": graph_h.hexdigest(),
        "contract": CONTRACT_GAMMA,
        "bridge_version": BRIDGE_VERSION,
    }

    return {"nodes": nodes, "edges": edges, "meta": meta}


def _extract_dependencies(source, ext):
    """Extract import/dependency references from source code."""
    deps = []
    for line in source.split('\n'):
        line = line.strip()
        if ext == '.py':
            if line.startswith('import ') or line.startswith('from '):
                # Extract module path from import statement
                parts = line.split()
                if parts[0] == 'from' and len(parts) >= 2:
                    deps.append(parts[1])
                elif parts[0] == 'import' and len(parts) >= 2:
                    deps.append(parts[1].rstrip(','))
        elif ext == '.rs':
            if line.startswith('use ') or line.startswith('mod '):
                parts = line.rstrip(';').split()
                if len(parts) >= 2:
                    deps.append(parts[1])
        elif ext == '.go':
            if line.startswith('"') and line.endswith('"'):
                deps.append(line.strip('"'))
    return deps


def _resolve_dep(dep_path, source_path, file_index, ext):
    """Try to resolve a dependency string to a node index."""
    if ext == '.py':
        # Convert dotted module path to file path
        candidates = [
            dep_path.replace('.', '/') + '.py',
            dep_path.replace('.', '/') + '/__init__.py',
        ]
    elif ext == '.rs':
        candidates = [
            dep_path.replace('::', '/') + '.rs',
        ]
    elif ext == '.go':
        candidates = [dep_path]
    else:
        return None

    for candidate in candidates:
        if candidate in file_index:
            return file_index[candidate]
    return None


def _compute_bond_strength(node_a, node_b):
    """Compute bond strength between two nodes (0.0 to 1.0).

    Uses shared Bismillah marker presence and extension compatibility
    as a simple heuristic. Full kinship analysis is deferred to the
    Ummah Witness engine.
    """
    strength = 0.3  # Base bond for any import relationship
    if node_a["extension"] == node_b["extension"]:
        strength += 0.2  # Same language bonus
    if node_a["has_bismillah_marker"] and node_b["has_bismillah_marker"]:
        strength += 0.3  # Both carry Bismillah protection
    if node_a["has_witness"] and node_b["has_witness"]:
        strength += 0.2  # Both have cryptographic witnesses
    return min(strength, 1.0)


# ---------------------------------------------------------------------------
# Bond Graph Decoding
# ---------------------------------------------------------------------------

def decode_repo_bond_graph(bond_data, **kwargs):
    """Decode a FATIMA bond graph back to a dependency structure.

    Reconstructs the repository's dependency map from the bond graph
    representation, including integrity state for each file.

    Args:
        bond_data: Bond graph dict from encode_repo_bond_graph.

    Returns:
        dict: Decoded structure with keys:
            files: list of {path, seal, integrity_state}
            dependencies: dict mapping path -> list of dependency paths
            integrity_summary: {verified, witnessed, marked, unprotected}
            graph_seal: str — the graph-level seal for chain verification
    """
    if not isinstance(bond_data, dict):
        raise TypeError("bond_data must be a dict from encode_repo_bond_graph")

    nodes = bond_data.get("nodes", [])
    edges = bond_data.get("edges", [])
    meta = bond_data.get("meta", {})

    # Build node lookup
    node_by_id = {n["id"]: n for n in nodes}

    # Reconstruct file list with integrity states
    files = []
    integrity = {"verified": 0, "witnessed": 0, "marked": 0, "unprotected": 0}

    for n in nodes:
        if n["has_witness"]:
            state = "witnessed"
            integrity["witnessed"] += 1
        elif n["has_bismillah_marker"]:
            state = "marked"
            integrity["marked"] += 1
        else:
            state = "unprotected"
            integrity["unprotected"] += 1

        files.append({
            "path": n["path"],
            "seal": n["seal"],
            "integrity_state": state,
            "extension": n["extension"],
            "size": n["size"],
        })

    # Reconstruct dependency map
    dependencies = {}
    for edge in edges:
        src = node_by_id.get(edge["source"])
        tgt = node_by_id.get(edge["target"])
        if src and tgt:
            src_path = src["path"]
            if src_path not in dependencies:
                dependencies[src_path] = []
            dependencies[src_path].append({
                "path": tgt["path"],
                "kind": edge.get("kind", "import"),
                "strength": edge.get("strength", 0.0),
            })

    return {
        "files": files,
        "dependencies": dependencies,
        "integrity_summary": integrity,
        "graph_seal": meta.get("graph_seal", ""),
        "timestamp": meta.get("timestamp", ""),
    }


# ---------------------------------------------------------------------------
# Verify Result → FATIMA Report Mapping
# ---------------------------------------------------------------------------

def map_verify_result_to_fatima(verify_result, **kwargs):
    """Map an encoder verification result to a FATIMA integrity report.

    Takes the dict returned by ``verify_directory()`` or
    ``semantic_verify()`` and produces a FATIMAReport with per-engine
    scores, grades, and an overall integrity assessment.

    Args:
        verify_result: dict from verify_directory or semantic_verify.
        repo_path: optional str — repository path for context.

    Returns:
        FATIMAReport: Mapped report with five-conjunct scores.
    """
    if not isinstance(verify_result, dict):
        raise TypeError(
            "verify_result must be a dict from verify_directory or "
            "semantic_verify, got {}".format(type(verify_result).__name__))

    total = verify_result.get("total", 0)
    protected = verify_result.get("protected", 0)
    integrity_verified = verify_result.get("integrity_verified", 0)
    witness_present = verify_result.get("witness_present", 0)
    marker_detected = verify_result.get("marker_detected", 0)
    unprotected = verify_result.get("unprotected", [])
    tampered = verify_result.get("tampered", [])

    # --- Compute per-conjunct scores ---

    # 1. Semantic: How much content has meaning-preserving seals
    if total > 0:
        semantic_score = (integrity_verified + 0.5 * witness_present) / total
    else:
        semantic_score = 0.0
    semantic_score = min(semantic_score, 1.0)

    # 2. Temporal: Presence of witness sidecars (temporal chain)
    if total > 0:
        temporal_score = (integrity_verified + witness_present) / total
    else:
        temporal_score = 0.0

    # 3. Relational: Cross-file consistency (no tampered files)
    tampered_count = len(tampered)
    if total > 0:
        relational_score = 1.0 - (tampered_count / total)
    else:
        relational_score = 0.0

    # 4. Adversarial: Resilience (ratio of cryptographically verified)
    if total > 0:
        adversarial_score = integrity_verified / total
    else:
        adversarial_score = 0.0

    # 5. Generative: Overall protection coverage
    if total > 0:
        generative_score = protected / total
    else:
        generative_score = 0.0

    conjunct_scores = OrderedDict([
        ("semantic", round(semantic_score, 4)),
        ("temporal", round(temporal_score, 4)),
        ("relational", round(relational_score, 4)),
        ("adversarial", round(adversarial_score, 4)),
        ("generative", round(generative_score, 4)),
    ])

    conjunct_grades = OrderedDict([
        (k, _grade_score(v)) for k, v in conjunct_scores.items()
    ])

    # Overall: weighted mean (adversarial and relational weighted higher)
    weights = {
        "semantic": 0.20,
        "temporal": 0.15,
        "relational": 0.25,
        "adversarial": 0.25,
        "generative": 0.15,
    }
    overall_score = sum(
        conjunct_scores[k] * weights[k] for k in FIVE_CONJUNCTS
    )
    overall_score = round(overall_score, 4)
    overall_grade = _grade_score(overall_score)

    return FATIMAReport(
        contract=CONTRACT_GAMMA,
        bridge_version=BRIDGE_VERSION,
        conjunct_scores=conjunct_scores,
        conjunct_grades=conjunct_grades,
        overall_score=overall_score,
        overall_grade=overall_grade,
        findings_count=len(unprotected) + tampered_count,
        total_files=total,
        protected_files=protected,
        integrity_verified=integrity_verified,
        witness_present=witness_present,
        marker_detected=marker_detected,
        unprotected_count=len(unprotected),
        tampered_count=tampered_count,
        engine_details=OrderedDict([
            ("semantic", {
                "score": conjunct_scores["semantic"],
                "grade": conjunct_grades["semantic"],
                "engine": "Shannon's Boundary",
                "description": "Meaning-preserving seal coverage",
            }),
            ("temporal", {
                "score": conjunct_scores["temporal"],
                "grade": conjunct_grades["temporal"],
                "engine": "Living Witness",
                "description": "Temporal witness chain coverage",
            }),
            ("relational", {
                "score": conjunct_scores["relational"],
                "grade": conjunct_grades["relational"],
                "engine": "Ummah Witness",
                "description": "Cross-file consistency (no tampering)",
            }),
            ("adversarial", {
                "score": conjunct_scores["adversarial"],
                "grade": conjunct_grades["adversarial"],
                "engine": "Muhasabah Engine",
                "description": "Cryptographic verification coverage",
            }),
            ("generative", {
                "score": conjunct_scores["generative"],
                "grade": conjunct_grades["generative"],
                "engine": "Khalifah Gate",
                "description": "Overall protection coverage",
            }),
        ]),
    )


# ---------------------------------------------------------------------------
# BSSG Five-Conjunct Kernel
# ---------------------------------------------------------------------------

def bssg_five_conjunct_kernel(findings, **kwargs):
    """Compute the BSSG five-conjunct kernel over a set of findings.

    The five conjuncts correspond to the five engines:
      Semantic, Temporal, Relational, Adversarial, Generative.

    Each finding is classified into one or more engine domains based
    on its source and category. The kernel computes a per-conjunct
    integrity score and an overall FATIMA grade.

    Args:
        findings: list of BismillahFinding objects (or dicts with
            'source', 'severity', 'category' keys).

    Returns:
        dict: Kernel evaluation results with keys:
            conjunct_scores: dict of {engine_name: float}
            conjunct_grades: dict of {engine_name: grade_str}
            overall_score: float
            overall_grade: str
            finding_distribution: dict of {engine_name: int}
            critical_count: int
            warning_count: int
            info_count: int
    """
    # Classify findings by engine domain
    distribution = {c: [] for c in FIVE_CONJUNCTS}
    severity_counts = {"critical": 0, "warning": 0, "info": 0}

    for finding in findings:
        # Support both BismillahFinding objects and plain dicts
        if hasattr(finding, 'source'):
            source = finding.source
            severity = finding.severity
            category = finding.category
        elif isinstance(finding, dict):
            source = finding.get('source', 'unknown')
            severity = finding.get('severity', 'info')
            category = finding.get('category', 'general')
        else:
            continue

        severity_counts[severity] = severity_counts.get(severity, 0) + 1

        # Map finding to engine domains
        engines = _classify_finding_to_engines(source, category)
        for engine in engines:
            distribution[engine].append({
                "severity": severity,
                "category": category,
                "source": source,
            })

    # Compute per-conjunct scores
    # Score = 1.0 - penalty, where penalty accumulates from findings
    conjunct_scores = OrderedDict()
    severity_weights = {"critical": 0.15, "warning": 0.05, "info": 0.01}

    for conjunct in FIVE_CONJUNCTS:
        engine_findings = distribution[conjunct]
        if not engine_findings:
            # No findings in this domain = perfect score
            conjunct_scores[conjunct] = 1.0
        else:
            penalty = 0.0
            for f in engine_findings:
                penalty += severity_weights.get(f["severity"], 0.01)
            conjunct_scores[conjunct] = round(max(0.0, 1.0 - penalty), 4)

    conjunct_grades = OrderedDict([
        (k, _grade_score(v)) for k, v in conjunct_scores.items()
    ])

    # Overall score: weighted mean
    weights = {
        "semantic": 0.20,
        "temporal": 0.15,
        "relational": 0.25,
        "adversarial": 0.25,
        "generative": 0.15,
    }
    overall_score = sum(
        conjunct_scores[k] * weights[k] for k in FIVE_CONJUNCTS
    )
    overall_score = round(overall_score, 4)

    return {
        "conjunct_scores": conjunct_scores,
        "conjunct_grades": conjunct_grades,
        "overall_score": overall_score,
        "overall_grade": _grade_score(overall_score),
        "finding_distribution": {
            k: len(v) for k, v in distribution.items()
        },
        "critical_count": severity_counts.get("critical", 0),
        "warning_count": severity_counts.get("warning", 0),
        "info_count": severity_counts.get("info", 0),
        "total_findings": len(findings),
        "contract": CONTRACT_GAMMA,
    }


def _classify_finding_to_engines(source, category):
    """Classify a finding into one or more engine domains.

    Mapping rules:
      - encoder findings → semantic + adversarial
      - furqan findings → semantic + relational
      - scanner findings → adversarial + generative
      - fatima findings → all five (meta-level)
      - Category-specific overrides for precision
    """
    engines = set()

    # Source-based classification
    if source == 'encoder':
        engines.update(["semantic", "adversarial"])
    elif source == 'furqan':
        engines.update(["semantic", "relational"])
    elif source == 'scanner':
        engines.update(["adversarial", "generative"])
    elif source == 'fatima':
        engines.update(FIVE_CONJUNCTS)

    # Category-based refinement
    cat_lower = category.lower() if category else ""
    if "temporal" in cat_lower or "version" in cat_lower or "chain" in cat_lower:
        engines.add("temporal")
    if "semantic" in cat_lower or "meaning" in cat_lower:
        engines.add("semantic")
    if "tamper" in cat_lower or "adversar" in cat_lower or "attack" in cat_lower:
        engines.add("adversarial")
    if "dependency" in cat_lower or "import" in cat_lower or "kinship" in cat_lower:
        engines.add("relational")
    if "generat" in cat_lower or "fidelity" in cat_lower:
        engines.add("generative")

    # Default: at least semantic
    if not engines:
        engines.add("semantic")

    return engines


# ---------------------------------------------------------------------------
# Utility: FATIMA seal for bridge outputs
# ---------------------------------------------------------------------------

def _fatima_seal(data_str):
    """Compute a FATIMA-anchored seal over a data string."""
    h = hashlib.sha256()
    h.update(BISMILLAH.encode('utf-8'))
    h.update(b"FATIMA_BRIDGE:")
    h.update(data_str.encode('utf-8'))
    h.update(BISMILLAH.encode('utf-8'))
    return h.hexdigest()


# Bismillah ir-Rahman ir-Rahim
