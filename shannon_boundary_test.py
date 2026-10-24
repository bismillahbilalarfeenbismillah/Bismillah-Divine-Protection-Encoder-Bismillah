#!/usr/bin/env python3 -I
"""
Bismillah ir-Rahman ir-Rahim

Finite-Benchmark Detection Test Harness for the 154-Layer FATIMA Architecture
==============================================================================

Measures the 154-layer witness's mutation detection rate across a finite
set of systematic and adversarial mutations.

REMEDIATION v2.0 — addresses ChatGPT's valid critiques:
  [R1] Crash-detection vs seal-detection separated and reported independently
  [R2] SHA-256 baseline comparison + heaven-only / earth-only ablation
  [R3] Semantic mutation tests (negation, paraphrase, role-reversal)
  [R4] Full reproducibility: input digest, random seed, mutation log

Terminology correction: "Shannon proximity" renamed to "finite-benchmark
detection rate" — this harness measures detection over a finite mutation
sample, not a universal information-theoretic guarantee.

Test Protocol:
  1. Bit-level sweep     -- flip every bit, measure detection
  2. Byte-level sweep    -- substitute every byte, measure detection
  3. Block-level sweep   -- mutate blocks of varying sizes
  4. Adversarial sweep   -- mutations designed to evade detection
  5. Coverage map        -- which layers detect which mutations
  6. Size threshold      -- detection rate vs file size
  7. SHA-256 baseline    -- compare against single SHA-256 hash
  8. Ablation tests      -- heaven-only, earth-only, full comparison
  9. Semantic mutations   -- meaning-changing edits on text content

Bismillah ir-Rahman ir-Rahim
"""

import sys
import os
import time
import random
import json
import hashlib
from collections import defaultdict

# Import the encoder from the same directory
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bismillah_encoder as encoder

BISMILLAH = "Bismillah ir-Rahman ir-Rahim"


# ============================================================================
#  [R1] CORE DETECTION ENGINE — crash vs seal separated
# ============================================================================

class SealResult:
    """Result of computing layer seals. Distinguishes valid seals from crashes."""
    __slots__ = ('seals', 'crashed', 'error')

    def __init__(self, seals=None, crashed=False, error=None):
        self.seals = seals        # list of 154 seal strings, or None
        self.crashed = crashed    # True if encoder raised an exception
        self.error = error        # exception message if crashed


def compute_layer_seals(content_bytes):
    """Compute all 154 layer seals. Returns a SealResult.

    [R1] Never silently converts a crash to "detected". The caller
    decides how to classify computation failures.
    """
    try:
        result = encoder.compute_all_154_layers(content_bytes)
        return SealResult(seals=[layer["seal"] for layer in result["layers"]])
    except Exception as e:
        return SealResult(crashed=True, error=str(e))


class DetectionResult:
    """Result of comparing original vs mutated seals."""
    __slots__ = ('changed_layers', 'detection_type')

    def __init__(self, changed_layers, detection_type):
        self.changed_layers = changed_layers  # set of layer indices
        self.detection_type = detection_type  # "seal" | "crash" | "none"

    @property
    def detected(self):
        return self.detection_type != "none"

    @property
    def is_crash_detection(self):
        return self.detection_type == "crash"

    @property
    def is_seal_detection(self):
        return self.detection_type == "seal"


def detect_mutation(original_result, mutated_result):
    """Compare two SealResults. Returns DetectionResult.

    [R1] Three outcomes:
      - "seal":  valid seals computed, at least one layer differs
      - "crash": mutated content caused encoder to crash (reported separately)
      - "none":  valid seals computed, all 154 layers identical (blind spot)
    """
    if mutated_result.crashed:
        return DetectionResult(set(), "crash")

    if original_result.crashed:
        # Original also crashed — can't compare
        return DetectionResult(set(), "crash")

    changed = set()
    for i in range(len(original_result.seals)):
        if original_result.seals[i] != mutated_result.seals[i]:
            changed.add(i)

    if changed:
        return DetectionResult(changed, "seal")
    else:
        return DetectionResult(set(), "none")


def layer_to_scale(layer_idx):
    """Map a layer index to its scale (heaven) number (0-10)."""
    return layer_idx // 14


def layer_to_domain_type(layer_idx):
    """Map a layer index to heaven or earth within its scale."""
    position_in_scale = layer_idx % 14
    return "heaven" if position_in_scale < 7 else "earth"


def is_heaven_layer(layer_idx):
    """True if this layer is in the heaven (first 7) of its scale."""
    return (layer_idx % 14) < 7


def is_earth_layer(layer_idx):
    """True if this layer is in the earth (last 7) of its scale."""
    return (layer_idx % 14) >= 7


SCALE_NAMES = [
    "SUBATOMIC", "ATOMIC", "MOLECULAR", "CELLULAR", "ORGANIC",
    "ECOSYSTEM", "PLANETARY", "FRACTAL", "ADVERSARIAL", "COSMIC", "DIVINE",
]


# ============================================================================
#  [R4] REPRODUCIBILITY — seed, input digest, mutation log
# ============================================================================

class MutationLog:
    """Records every mutation for full reproducibility."""

    def __init__(self):
        self.entries = []
        self.seed = None
        self.input_sha256 = None
        self.input_size = None

    def set_input(self, content_bytes, seed):
        self.seed = seed
        self.input_size = len(content_bytes)
        self.input_sha256 = hashlib.sha256(content_bytes).hexdigest()

    def record(self, test_name, mutation_desc, detection_result):
        self.entries.append({
            "test": test_name,
            "mutation": mutation_desc,
            "detected": detection_result.detected,
            "detection_type": detection_result.detection_type,
            "layers_changed": len(detection_result.changed_layers),
        })

    def summary(self):
        total = len(self.entries)
        seal_det = sum(1 for e in self.entries if e["detection_type"] == "seal")
        crash_det = sum(1 for e in self.entries if e["detection_type"] == "crash")
        undetected = sum(1 for e in self.entries if e["detection_type"] == "none")
        return {
            "total_mutations": total,
            "seal_detections": seal_det,
            "crash_detections": crash_det,
            "undetected": undetected,
            "seal_detection_rate": seal_det / total if total > 0 else 0,
            "crash_rate": crash_det / total if total > 0 else 0,
            "total_detection_rate": (seal_det + crash_det) / total if total > 0 else 0,
        }

    def to_dict(self):
        return {
            "seed": self.seed,
            "input_sha256": self.input_sha256,
            "input_size": self.input_size,
            "summary": self.summary(),
            "log_sample": self.entries[:200],  # first 200 for JSON size
            "log_total": len(self.entries),
        }


# Global mutation log
mutation_log = MutationLog()


# ============================================================================
#  TEST 1: BIT-LEVEL SWEEP
# ============================================================================

def test_bit_level(content_bytes, max_bits=None):
    """Flip every single bit and measure detection rate."""
    print("\n  {} -- Test 1: Bit-Level Sweep".format(BISMILLAH))
    print("  " + "=" * 60)

    n_bytes = len(content_bytes)
    n_bits = n_bytes * 8
    data = bytearray(content_bytes)

    if max_bits and n_bits > max_bits:
        bit_positions = sorted(random.sample(range(n_bits), max_bits))
        print("  Sampling {} of {} bits".format(max_bits, n_bits))
    else:
        bit_positions = range(n_bits)
        print("  Testing all {} bits".format(n_bits))

    original = compute_layer_seals(bytes(data))
    seal_detected = 0
    crash_detected = 0
    undetected = 0
    undetected_positions = []
    layers_triggered = defaultdict(int)
    t0 = time.time()

    for count, bit_pos in enumerate(bit_positions):
        byte_idx = bit_pos // 8
        bit_idx = bit_pos % 8

        data[byte_idx] ^= (1 << bit_idx)
        mutated = compute_layer_seals(bytes(data))
        data[byte_idx] ^= (1 << bit_idx)

        result = detect_mutation(original, mutated)
        mutation_log.record("bit_level", "flip_bit_{}".format(bit_pos), result)

        if result.is_seal_detection:
            seal_detected += 1
            for layer in result.changed_layers:
                layers_triggered[layer] += 1
        elif result.is_crash_detection:
            crash_detected += 1
        else:
            undetected += 1
            undetected_positions.append(bit_pos)

        if (count + 1) % 100 == 0:
            elapsed = time.time() - t0
            rate = (count + 1) / elapsed if elapsed > 0 else 0
            print("    Progress: {}/{} bits ({:.1f}/s)".format(
                count + 1, len(bit_positions), rate), end='\r')

    total = seal_detected + crash_detected + undetected
    elapsed = time.time() - t0

    print("  " + " " * 70)
    print("  Results:")
    print("    Bits tested:         {}".format(total))
    print("    Seal detections:     {} ({:.4f}%)".format(
        seal_detected, seal_detected / total * 100 if total else 0))
    print("    Crash detections:    {} ({:.4f}%)".format(
        crash_detected, crash_detected / total * 100 if total else 0))
    print("    Undetected:          {}".format(undetected))
    print("    Seal detection rate: {:.6f}%".format(
        seal_detected / total * 100 if total else 0))
    print("    Total detect rate:   {:.6f}%".format(
        (seal_detected + crash_detected) / total * 100 if total else 0))
    print("    Time:                {:.1f}s".format(elapsed))

    if undetected_positions:
        print("    Blind spots (first 10): {}".format(undetected_positions[:10]))

    return {
        "test": "bit_level",
        "total": total,
        "seal_detected": seal_detected,
        "crash_detected": crash_detected,
        "undetected": undetected,
        "seal_detection_rate": seal_detected / total if total else 0,
        "total_detection_rate": (seal_detected + crash_detected) / total if total else 0,
        "undetected_positions": undetected_positions[:50],
        "time_seconds": elapsed,
    }


# ============================================================================
#  TEST 2: BYTE-LEVEL SWEEP
# ============================================================================

def test_byte_level(content_bytes, max_positions=None, substitutions_per_byte=8):
    """Substitute bytes and measure detection rate."""
    print("\n  {} -- Test 2: Byte-Level Sweep".format(BISMILLAH))
    print("  " + "=" * 60)

    n = len(content_bytes)
    data = bytearray(content_bytes)

    if max_positions and n > max_positions:
        positions = sorted(random.sample(range(n), max_positions))
        print("  Sampling {} of {} positions".format(max_positions, n))
    else:
        positions = range(n)
        print("  Testing all {} positions".format(n))

    original = compute_layer_seals(bytes(data))
    seal_detected = 0
    crash_detected = 0
    undetected = 0
    t0 = time.time()

    for count, pos in enumerate(positions):
        original_byte = data[pos]
        candidates = [v for v in range(256) if v != original_byte]
        subs = random.sample(candidates, min(substitutions_per_byte, len(candidates)))

        for sub_val in subs:
            data[pos] = sub_val
            mutated = compute_layer_seals(bytes(data))
            data[pos] = original_byte

            result = detect_mutation(original, mutated)
            mutation_log.record("byte_level",
                                "pos_{}_0x{:02x}_to_0x{:02x}".format(pos, original_byte, sub_val),
                                result)

            if result.is_seal_detection:
                seal_detected += 1
            elif result.is_crash_detection:
                crash_detected += 1
            else:
                undetected += 1

        if (count + 1) % 50 == 0:
            elapsed = time.time() - t0
            rate = (count + 1) / elapsed if elapsed > 0 else 0
            print("    Progress: {}/{} positions ({:.1f}/s)".format(
                count + 1, len(positions), rate), end='\r')

    total = seal_detected + crash_detected + undetected
    elapsed = time.time() - t0

    print("  " + " " * 70)
    print("  Results:")
    print("    Mutations tested:    {}".format(total))
    print("    Seal detections:     {}".format(seal_detected))
    print("    Crash detections:    {}".format(crash_detected))
    print("    Undetected:          {}".format(undetected))
    print("    Seal detection rate: {:.6f}%".format(
        seal_detected / total * 100 if total else 0))
    print("    Time:                {:.1f}s".format(elapsed))

    return {
        "test": "byte_level",
        "total": total,
        "seal_detected": seal_detected,
        "crash_detected": crash_detected,
        "undetected": undetected,
        "seal_detection_rate": seal_detected / total if total else 0,
        "total_detection_rate": (seal_detected + crash_detected) / total if total else 0,
        "time_seconds": elapsed,
    }


# ============================================================================
#  TEST 3: BLOCK-LEVEL MUTATIONS
# ============================================================================

def test_block_level(content_bytes, block_sizes=None, trials_per_size=50):
    """Mutate random blocks of varying sizes."""
    print("\n  {} -- Test 3: Block-Level Mutations".format(BISMILLAH))
    print("  " + "=" * 60)

    if block_sizes is None:
        block_sizes = [1, 2, 4, 8, 16, 32, 64, 128, 256]

    n = len(content_bytes)
    data = bytearray(content_bytes)
    original = compute_layer_seals(bytes(data))
    results_by_size = {}
    t0 = time.time()

    for bsize in block_sizes:
        if bsize > n:
            continue

        seal_det = 0
        crash_det = 0
        undet = 0

        for trial in range(trials_per_size):
            pos = random.randint(0, n - bsize)
            original_block = bytes(data[pos:pos + bsize])
            for i in range(bsize):
                data[pos + i] = random.randint(0, 255)
            if bytes(data[pos:pos + bsize]) == original_block:
                data[pos] = (data[pos] + 1) % 256

            mutated = compute_layer_seals(bytes(data))
            data[pos:pos + bsize] = original_block

            result = detect_mutation(original, mutated)
            mutation_log.record("block_level",
                                "block_{}_pos_{}_trial_{}".format(bsize, pos, trial),
                                result)

            if result.is_seal_detection:
                seal_det += 1
            elif result.is_crash_detection:
                crash_det += 1
            else:
                undet += 1

        total = seal_det + crash_det + undet
        results_by_size[bsize] = {
            "block_size": bsize,
            "trials": total,
            "seal_detected": seal_det,
            "crash_detected": crash_det,
            "undetected": undet,
            "seal_detection_rate": seal_det / total if total else 0,
        }
        print("    Block {:>4d}B: seal={} crash={} miss={} rate={:.2f}%".format(
            bsize, seal_det, crash_det, undet,
            seal_det / total * 100 if total else 0))

    elapsed = time.time() - t0
    print("    Time: {:.1f}s".format(elapsed))

    return {
        "test": "block_level",
        "results_by_size": results_by_size,
        "time_seconds": elapsed,
    }


# ============================================================================
#  TEST 4: ADVERSARIAL MUTATIONS
# ============================================================================

def test_adversarial(content_bytes):
    """Mutations specifically designed to evade detection."""
    print("\n  {} -- Test 4: Adversarial Mutations".format(BISMILLAH))
    print("  " + "=" * 60)

    n = len(content_bytes)
    data = bytearray(content_bytes)
    original = compute_layer_seals(bytes(data))
    results = []

    def run_adversarial(name, mutated_bytes):
        mutated = compute_layer_seals(mutated_bytes)
        result = detect_mutation(original, mutated)
        mutation_log.record("adversarial", name, result)

        entry = {
            "mutation": name,
            "detected": result.detected,
            "detection_type": result.detection_type,
            "layers_changed": len(result.changed_layers),
            "scales_changed": len(set(layer_to_scale(l) for l in result.changed_layers)) if result.changed_layers else 0,
        }
        results.append(entry)

        if result.is_seal_detection:
            status = "SEAL-DETECTED ({} layers, {} scales)".format(
                entry["layers_changed"], entry["scales_changed"])
        elif result.is_crash_detection:
            status = "CRASH-DETECTED (encoder exception)"
        else:
            status = "UNDETECTED"
        print("    {}: {}".format(name, status))

    run_adversarial("append_null_byte", bytes(data) + b'\x00')
    run_adversarial("append_space", bytes(data) + b' ')
    run_adversarial("prepend_null_byte", b'\x00' + bytes(data))

    mid = n // 2
    run_adversarial("insert_zwsp_middle",
                    bytes(data[:mid]) + '​'.encode('utf-8') + bytes(data[mid:]))
    run_adversarial("insert_zwnj_middle",
                    bytes(data[:mid]) + '‌'.encode('utf-8') + bytes(data[mid:]))
    run_adversarial("insert_bom_start",
                    '﻿'.encode('utf-8') + bytes(data))

    # Swap two bytes
    swapped = bytearray(data)
    if n >= 2:
        swapped[0], swapped[1] = swapped[1], swapped[0]
        run_adversarial("swap_first_two_bytes", bytes(swapped))

    run_adversarial("bitwise_not_entire_file", bytes(b ^ 0xFF for b in data))
    run_adversarial("duplicate_content", bytes(data) + bytes(data))
    if n > 1:
        run_adversarial("truncate_last_byte", bytes(data[:-1]))
    run_adversarial("right_shift_all_bits", bytes(b >> 1 for b in data))
    run_adversarial("bidi_override_inject",
                    bytes(data[:mid]) + '‮'.encode('utf-8') + bytes(data[mid:]))

    total = len(results)
    seal_count = sum(1 for r in results if r["detection_type"] == "seal")
    crash_count = sum(1 for r in results if r["detection_type"] == "crash")
    undet_count = sum(1 for r in results if r["detection_type"] == "none")

    print("  Summary:")
    print("    Total:         {}".format(total))
    print("    Seal-detected: {}".format(seal_count))
    print("    Crash-detected:{}".format(crash_count))
    print("    Undetected:    {}".format(undet_count))

    return {
        "test": "adversarial",
        "total": total,
        "seal_detected": seal_count,
        "crash_detected": crash_count,
        "undetected": undet_count,
        "seal_detection_rate": seal_count / total if total else 0,
        "total_detection_rate": (seal_count + crash_count) / total if total else 0,
        "details": results,
    }


# ============================================================================
#  TEST 5: SCALE COVERAGE MAP
# ============================================================================

def test_coverage_map(content_bytes, sample_mutations=200):
    """Build a coverage matrix: which scales detect which mutation types."""
    print("\n  {} -- Test 5: Scale Coverage Map".format(BISMILLAH))
    print("  " + "=" * 60)

    n = len(content_bytes)
    data = bytearray(content_bytes)
    original = compute_layer_seals(bytes(data))

    categories = {
        "single_bit": [], "single_byte": [], "small_block_4": [],
        "medium_block_32": [], "append": [], "truncate": [],
    }
    scale_hits = defaultdict(lambda: defaultdict(int))
    domain_hits = defaultdict(lambda: defaultdict(int))
    crash_counts = defaultdict(int)

    trials_per_cat = sample_mutations // len(categories)

    for trial in range(trials_per_cat):
        # Single bit flip
        bit_pos = random.randint(0, n * 8 - 1)
        byte_idx, bit_idx = bit_pos // 8, bit_pos % 8
        data[byte_idx] ^= (1 << bit_idx)
        result = detect_mutation(original, compute_layer_seals(bytes(data)))
        data[byte_idx] ^= (1 << bit_idx)
        if result.is_crash_detection:
            crash_counts["single_bit"] += 1
        for l in result.changed_layers:
            scale_hits["single_bit"][layer_to_scale(l)] += 1
            domain_hits["single_bit"][layer_to_domain_type(l)] += 1
        categories["single_bit"].append(result.detected)

        # Single byte substitution
        pos = random.randint(0, n - 1)
        orig = data[pos]
        data[pos] = (orig + random.randint(1, 255)) % 256
        result = detect_mutation(original, compute_layer_seals(bytes(data)))
        data[pos] = orig
        if result.is_crash_detection:
            crash_counts["single_byte"] += 1
        for l in result.changed_layers:
            scale_hits["single_byte"][layer_to_scale(l)] += 1
            domain_hits["single_byte"][layer_to_domain_type(l)] += 1
        categories["single_byte"].append(result.detected)

        # Small block (4 bytes)
        if n >= 4:
            pos = random.randint(0, n - 4)
            orig_block = bytes(data[pos:pos + 4])
            data[pos:pos + 4] = bytes(random.randint(0, 255) for _ in range(4))
            if bytes(data[pos:pos + 4]) == orig_block:
                data[pos] = (data[pos] + 1) % 256
            result = detect_mutation(original, compute_layer_seals(bytes(data)))
            data[pos:pos + 4] = orig_block
            if result.is_crash_detection:
                crash_counts["small_block_4"] += 1
            for l in result.changed_layers:
                scale_hits["small_block_4"][layer_to_scale(l)] += 1
                domain_hits["small_block_4"][layer_to_domain_type(l)] += 1
            categories["small_block_4"].append(result.detected)

        # Medium block (32 bytes)
        if n >= 32:
            pos = random.randint(0, n - 32)
            orig_block = bytes(data[pos:pos + 32])
            data[pos:pos + 32] = bytes(random.randint(0, 255) for _ in range(32))
            if bytes(data[pos:pos + 32]) == orig_block:
                data[pos] = (data[pos] + 1) % 256
            result = detect_mutation(original, compute_layer_seals(bytes(data)))
            data[pos:pos + 32] = orig_block
            if result.is_crash_detection:
                crash_counts["medium_block_32"] += 1
            for l in result.changed_layers:
                scale_hits["medium_block_32"][layer_to_scale(l)] += 1
                domain_hits["medium_block_32"][layer_to_domain_type(l)] += 1
            categories["medium_block_32"].append(result.detected)

        # Append
        appended = bytes(data) + bytes([random.randint(0, 255)])
        result = detect_mutation(original, compute_layer_seals(appended))
        if result.is_crash_detection:
            crash_counts["append"] += 1
        for l in result.changed_layers:
            scale_hits["append"][layer_to_scale(l)] += 1
            domain_hits["append"][layer_to_domain_type(l)] += 1
        categories["append"].append(result.detected)

        # Truncate
        if n > 1:
            result = detect_mutation(original, compute_layer_seals(bytes(data[:-1])))
            if result.is_crash_detection:
                crash_counts["truncate"] += 1
            for l in result.changed_layers:
                scale_hits["truncate"][layer_to_scale(l)] += 1
                domain_hits["truncate"][layer_to_domain_type(l)] += 1
            categories["truncate"].append(result.detected)

    # Print coverage matrix
    print("\n    Scale Coverage Matrix (hits per {} trials):".format(trials_per_cat))
    print("    {:>16s}".format(""), end="")
    for s in range(11):
        print(" {:>5s}".format("S" + str(s)), end="")
    print("  {:>7s} {:>6s}".format("DETECT", "CRASH"))

    for cat in categories:
        detections = categories[cat]
        det_rate = sum(detections) / len(detections) if detections else 0
        crashes = crash_counts.get(cat, 0)
        print("    {:>16s}".format(cat), end="")
        for s in range(11):
            hits = scale_hits[cat].get(s, 0)
            print(" {:>5s}".format(str(hits) if hits > 0 else "-"), end="")
        print("  {:>6.1f}% {:>5d}".format(det_rate * 100, crashes))

    # Heaven vs Earth complementarity
    print("\n    Heaven-Earth Complementarity:")
    print("    {:>16s}  {:>8s}  {:>8s}  {:>8s}".format(
        "Category", "Heaven", "Earth", "Ratio"))
    for cat in categories:
        h = domain_hits[cat].get("heaven", 0)
        e = domain_hits[cat].get("earth", 0)
        ratio = h / e if e > 0 else float('inf') if h > 0 else 0
        print("    {:>16s}  {:>8d}  {:>8d}  {:>8.2f}".format(cat, h, e, ratio))

    return {
        "test": "coverage_map",
        "categories": {cat: sum(v) / len(v) if v else 0 for cat, v in categories.items()},
        "scale_hits": {cat: dict(hits) for cat, hits in scale_hits.items()},
        "domain_hits": {cat: dict(hits) for cat, hits in domain_hits.items()},
        "crash_counts": dict(crash_counts),
    }


# ============================================================================
#  TEST 6: FILE SIZE THRESHOLD
# ============================================================================

def test_size_threshold(base_content, sizes=None, bit_trials_per_size=200):
    """Detection rate as a function of file size."""
    print("\n  {} -- Test 6: Size vs Detection Rate".format(BISMILLAH))
    print("  " + "=" * 60)

    if sizes is None:
        sizes = [16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192]

    results = []

    for size in sizes:
        if size <= len(base_content):
            content = base_content[:size]
        else:
            repeats = (size // len(base_content)) + 1
            content = (base_content * repeats)[:size]

        content_bytes = content if isinstance(content, bytes) else content.encode('utf-8')
        data = bytearray(content_bytes)
        n = len(data)
        original = compute_layer_seals(bytes(data))

        seal_det = 0
        crash_det = 0
        undet = 0

        for _ in range(min(bit_trials_per_size, n * 8)):
            bit_pos = random.randint(0, n * 8 - 1)
            byte_idx, bit_idx = bit_pos // 8, bit_pos % 8
            data[byte_idx] ^= (1 << bit_idx)
            mutated = compute_layer_seals(bytes(data))
            data[byte_idx] ^= (1 << bit_idx)

            result = detect_mutation(original, mutated)
            if result.is_seal_detection:
                seal_det += 1
            elif result.is_crash_detection:
                crash_det += 1
            else:
                undet += 1

        total = seal_det + crash_det + undet
        results.append({
            "size": size,
            "trials": total,
            "seal_detected": seal_det,
            "crash_detected": crash_det,
            "undetected": undet,
            "seal_detection_rate": seal_det / total if total else 0,
        })
        print("    Size {:>6d}B: seal={} crash={} miss={} rate={:.2f}%".format(
            size, seal_det, crash_det, undet,
            seal_det / total * 100 if total else 0))

    return {"test": "size_threshold", "results": results}


# ============================================================================
#  [R2] TEST 7: SHA-256 BASELINE COMPARISON
# ============================================================================

def test_sha256_baseline(content_bytes, trials=300):
    """Compare FATIMA 154-layer detection against a single SHA-256 hash.

    Both should detect every mutation — this validates that FATIMA
    achieves at least baseline SHA-256 performance, and measures
    whether the multi-layer architecture provides any advantage
    the baseline does not.
    """
    print("\n  {} -- Test 7: SHA-256 Baseline Comparison".format(BISMILLAH))
    print("  " + "=" * 60)

    n = len(content_bytes)
    data = bytearray(content_bytes)

    # Baselines
    original_sha = hashlib.sha256(bytes(data)).hexdigest()
    original_fatima = compute_layer_seals(bytes(data))

    sha_detected = 0
    fatima_seal_detected = 0
    fatima_crash_detected = 0
    both_detected = 0
    sha_only = 0
    fatima_only = 0
    neither = 0
    t0 = time.time()

    for trial in range(min(trials, n * 8)):
        bit_pos = random.randint(0, n * 8 - 1)
        byte_idx, bit_idx = bit_pos // 8, bit_pos % 8

        data[byte_idx] ^= (1 << bit_idx)
        mutated_bytes = bytes(data)
        data[byte_idx] ^= (1 << bit_idx)

        # SHA-256 check
        mutated_sha = hashlib.sha256(mutated_bytes).hexdigest()
        sha_det = mutated_sha != original_sha

        # FATIMA check
        mutated_fatima = compute_layer_seals(mutated_bytes)
        fatima_result = detect_mutation(original_fatima, mutated_fatima)

        if sha_det:
            sha_detected += 1
        if fatima_result.is_seal_detection:
            fatima_seal_detected += 1
        if fatima_result.is_crash_detection:
            fatima_crash_detected += 1

        fatima_det = fatima_result.detected
        if sha_det and fatima_det:
            both_detected += 1
        elif sha_det and not fatima_det:
            sha_only += 1
        elif fatima_det and not sha_det:
            fatima_only += 1
        else:
            neither += 1

    total = min(trials, n * 8)
    elapsed = time.time() - t0

    print("  Results ({} random bit-flip mutations):".format(total))
    print("    SHA-256 detected:        {} ({:.4f}%)".format(
        sha_detected, sha_detected / total * 100))
    print("    FATIMA seal-detected:    {} ({:.4f}%)".format(
        fatima_seal_detected, fatima_seal_detected / total * 100))
    print("    FATIMA crash-detected:   {} ({:.4f}%)".format(
        fatima_crash_detected, fatima_crash_detected / total * 100))
    print("    Both detected:           {}".format(both_detected))
    print("    SHA-256 only:            {}".format(sha_only))
    print("    FATIMA only:             {}".format(fatima_only))
    print("    Neither:                 {}".format(neither))
    print("    Time:                    {:.1f}s".format(elapsed))

    return {
        "test": "sha256_baseline",
        "total": total,
        "sha256_detected": sha_detected,
        "fatima_seal_detected": fatima_seal_detected,
        "fatima_crash_detected": fatima_crash_detected,
        "both_detected": both_detected,
        "sha256_only": sha_only,
        "fatima_only": fatima_only,
        "neither": neither,
        "sha256_rate": sha_detected / total if total else 0,
        "fatima_seal_rate": fatima_seal_detected / total if total else 0,
        "time_seconds": elapsed,
    }


# ============================================================================
#  [R2] TEST 8: ABLATION — heaven-only, earth-only, full
# ============================================================================

def test_ablation(content_bytes, trials=300):
    """Ablation test: do heaven layers and earth layers independently detect?

    Compares:
      - Full 154-layer witness (all seals)
      - Heaven-only (layers 0-6, 14-20, ... within each scale)
      - Earth-only (layers 7-13, 21-27, ... within each scale)

    If layers are truly independent detectors, each subset should
    still detect mutations — possibly at a lower rate than the full set.
    If heaven-only already catches everything, earth layers add no
    independent detection capacity.
    """
    print("\n  {} -- Test 8: Ablation (Heaven / Earth / Full)".format(BISMILLAH))
    print("  " + "=" * 60)

    n = len(content_bytes)
    data = bytearray(content_bytes)
    original = compute_layer_seals(bytes(data))

    if original.crashed:
        print("    ERROR: Cannot compute baseline seals. Skipping ablation.")
        return {"test": "ablation", "error": "baseline_crash"}

    full_det = 0
    heaven_det = 0
    earth_det = 0
    heaven_only_det = 0  # heaven catches it, earth doesn't
    earth_only_det = 0   # earth catches it, heaven doesn't
    both_det = 0
    neither_det = 0
    crashes = 0
    t0 = time.time()

    for trial in range(min(trials, n * 8)):
        bit_pos = random.randint(0, n * 8 - 1)
        byte_idx, bit_idx = bit_pos // 8, bit_pos % 8

        data[byte_idx] ^= (1 << bit_idx)
        mutated = compute_layer_seals(bytes(data))
        data[byte_idx] ^= (1 << bit_idx)

        if mutated.crashed:
            crashes += 1
            continue

        # Full detection
        full_changed = set()
        heaven_changed = set()
        earth_changed = set()

        for i in range(154):
            if original.seals[i] != mutated.seals[i]:
                full_changed.add(i)
                if is_heaven_layer(i):
                    heaven_changed.add(i)
                else:
                    earth_changed.add(i)

        if full_changed:
            full_det += 1
        h_det = len(heaven_changed) > 0
        e_det = len(earth_changed) > 0

        if h_det:
            heaven_det += 1
        if e_det:
            earth_det += 1
        if h_det and e_det:
            both_det += 1
        elif h_det and not e_det:
            heaven_only_det += 1
        elif e_det and not h_det:
            earth_only_det += 1
        else:
            neither_det += 1

    valid = min(trials, n * 8) - crashes
    if valid == 0:
        print("    All trials crashed. Cannot perform ablation.")
        return {"test": "ablation", "error": "all_crashed"}

    print("  Results ({} valid mutations, {} crashes excluded):".format(valid, crashes))
    print("    Full 154-layer:    {} / {} = {:.4f}%".format(
        full_det, valid, full_det / valid * 100))
    print("    Heaven-only (77):  {} / {} = {:.4f}%".format(
        heaven_det, valid, heaven_det / valid * 100))
    print("    Earth-only (77):   {} / {} = {:.4f}%".format(
        earth_det, valid, earth_det / valid * 100))
    print("    Both detect:       {}".format(both_det))
    print("    Heaven-only wins:  {}".format(heaven_only_det))
    print("    Earth-only wins:   {}".format(earth_only_det))
    print("    Neither detects:   {}".format(neither_det))
    elapsed = time.time() - t0
    print("    Time:              {:.1f}s".format(elapsed))

    # Independence assessment
    if heaven_only_det == 0 and earth_only_det == 0 and both_det == full_det:
        print("    Assessment: FULL REDUNDANCY — heaven and earth always co-fire")
    elif earth_only_det > 0 or heaven_only_det > 0:
        print("    Assessment: PARTIAL INDEPENDENCE — {}/{} unique earth, {}/{} unique heaven".format(
            earth_only_det, valid, heaven_only_det, valid))
    else:
        print("    Assessment: COUPLED — neither subset independently covers all mutations")

    return {
        "test": "ablation",
        "valid_trials": valid,
        "crashes_excluded": crashes,
        "full_detected": full_det,
        "heaven_detected": heaven_det,
        "earth_detected": earth_det,
        "both_detected": both_det,
        "heaven_only": heaven_only_det,
        "earth_only": earth_only_det,
        "neither": neither_det,
        "full_rate": full_det / valid,
        "heaven_rate": heaven_det / valid,
        "earth_rate": earth_det / valid,
        "time_seconds": elapsed,
    }


# ============================================================================
#  [R3] TEST 9: SEMANTIC MUTATIONS
# ============================================================================

def test_semantic(content_bytes):
    """Test meaning-changing edits on text content.

    Tests whether the architecture detects semantic changes:
      - Negation insertion ("improved" -> "did not improve")
      - Role reversal ("Alice sent Bob" -> "Bob sent Alice")
      - Paraphrase (same meaning, different words)
      - Numeric alteration (changing a number)
      - Homoglyph substitution (visually similar chars)

    Note: This tests whether structural seals change on semantic edits,
    NOT whether the encoder "understands" meaning. Any byte-level change
    should be detected; the question is whether the semantic witness
    adds anything beyond structural detection.
    """
    print("\n  {} -- Test 9: Semantic Mutations".format(BISMILLAH))
    print("  " + "=" * 60)

    # Use text content for semantic tests
    try:
        text = content_bytes.decode('utf-8')
    except UnicodeDecodeError:
        text = content_bytes.decode('latin-1')

    # Define semantic test pairs
    test_pairs = [
        # (name, original_text, mutated_text, category)
        ("negation_insert",
         "the patient improved significantly",
         "the patient did not improve significantly",
         "negation"),
        ("negation_remove",
         "this is not acceptable behavior",
         "this is acceptable behavior",
         "negation"),
        ("role_reversal",
         "Alice sent a message to Bob about the meeting",
         "Bob sent a message to Alice about the meeting",
         "role_reversal"),
        ("numeric_change",
         "the cost was 1500 dollars for the service",
         "the cost was 15000 dollars for the service",
         "numeric"),
        ("numeric_subtle",
         "version 10.8.0 of the encoder",
         "version 10.8.1 of the encoder",
         "numeric"),
        ("paraphrase_same_meaning",
         "the quick brown fox jumps over the lazy dog",
         "a fast dark fox leaps across the idle hound",
         "paraphrase"),
        ("synonym_substitution",
         "the algorithm is extremely efficient and fast",
         "the algorithm is highly effective and rapid",
         "paraphrase"),
        ("homoglyph_attack",
         "verification passed successfully",
         "veriﬁcation passed successfully",  # fi -> ﬁ ligature
         "homoglyph"),
        ("whitespace_semantic",
         "amount: 100",
         "amount:  100",  # double space
         "whitespace"),
        ("case_change_meaning",
         "the polish text needs review",
         "the Polish text needs review",
         "case_change"),
    ]

    results = []
    original_full = compute_layer_seals(content_bytes)

    for name, orig_text, mut_text, category in test_pairs:
        orig_bytes = orig_text.encode('utf-8')
        mut_bytes = mut_text.encode('utf-8')

        orig_seals = compute_layer_seals(orig_bytes)
        mut_seals = compute_layer_seals(mut_bytes)
        det_result = detect_mutation(orig_seals, mut_seals)

        # Also check SHA-256 for comparison
        orig_sha = hashlib.sha256(orig_bytes).hexdigest()
        mut_sha = hashlib.sha256(mut_bytes).hexdigest()
        sha_detected = orig_sha != mut_sha

        byte_diff = abs(len(orig_bytes) - len(mut_bytes))
        if len(orig_bytes) == len(mut_bytes):
            byte_diff = sum(1 for a, b in zip(orig_bytes, mut_bytes) if a != b)

        entry = {
            "name": name,
            "category": category,
            "fatima_detected": det_result.detected,
            "fatima_type": det_result.detection_type,
            "fatima_layers_changed": len(det_result.changed_layers),
            "sha256_detected": sha_detected,
            "byte_difference": byte_diff,
            "original_len": len(orig_bytes),
            "mutated_len": len(mut_bytes),
        }
        results.append(entry)

        fatima_status = "{} ({} layers)".format(
            det_result.detection_type.upper(), len(det_result.changed_layers))
        sha_status = "YES" if sha_detected else "NO"

        print("    {:<25s} FATIMA={:<20s} SHA256={:<4s} cat={}".format(
            name, fatima_status, sha_status, category))

    # Summary by category
    print("\n  Category Summary:")
    cats = defaultdict(list)
    for r in results:
        cats[r["category"]].append(r)
    for cat, entries in cats.items():
        fatima_det = sum(1 for e in entries if e["fatima_detected"])
        sha_det = sum(1 for e in entries if e["sha256_detected"])
        print("    {:<15s} FATIMA={}/{} SHA256={}/{}".format(
            cat, fatima_det, len(entries), sha_det, len(entries)))

    total = len(results)
    fatima_total = sum(1 for r in results if r["fatima_detected"])
    sha_total = sum(1 for r in results if r["sha256_detected"])

    print("\n  Note: Both FATIMA and SHA-256 detect ANY byte-level change.")
    print("  Semantic 'understanding' requires a different experiment —")
    print("  one that tests whether meaning-preserving byte changes")
    print("  (e.g., re-encoding, normalization) produce identical witnesses.")

    return {
        "test": "semantic",
        "total": total,
        "fatima_detected": fatima_total,
        "sha256_detected": sha_total,
        "fatima_rate": fatima_total / total if total else 0,
        "sha256_rate": sha_total / total if total else 0,
        "details": results,
    }


# ============================================================================
#  AGGREGATE REPORT — renamed per ChatGPT critique
# ============================================================================

def generate_report(all_results, content_size, reproducibility):
    """Generate the final detection benchmark report."""
    print("\n")
    print("  " + "=" * 68)
    print("  {} -- FINITE-BENCHMARK DETECTION REPORT".format(BISMILLAH))
    print("  " + "=" * 68)
    print("  Architecture:    154 layers, 22 domains (11 heavens + 11 earths)")
    print("  Encoder version: {}".format(encoder.ENCODER_VERSION))
    print("  Test content:    {} bytes".format(content_size))
    print("  Input SHA-256:   {}".format(reproducibility["input_sha256"]))
    print("  Random seed:     {}".format(reproducibility["seed"]))
    print("")

    # [R1] Separated detection table
    print("  {:>25s}  {:>10s}  {:>10s}  {:>10s}  {:>8s}".format(
        "Test", "Seal-Det", "Crash-Det", "Undetect", "Total"))
    print("  " + "-" * 68)

    for r in all_results:
        if "seal_detected" in r:
            print("  {:>25s}  {:>10d}  {:>10d}  {:>10d}  {:>8d}".format(
                r["test"],
                r.get("seal_detected", 0),
                r.get("crash_detected", 0),
                r.get("undetected", 0),
                r.get("total", 0)))

    # Mutation log summary
    log_summary = mutation_log.summary()
    print("")
    print("  AGGREGATE (from mutation log):")
    print("    Total mutations tested:   {}".format(log_summary["total_mutations"]))
    print("    Seal detections:          {} ({:.4f}%)".format(
        log_summary["seal_detections"],
        log_summary["seal_detection_rate"] * 100))
    print("    Crash detections:         {} ({:.4f}%)".format(
        log_summary["crash_detections"],
        log_summary["crash_rate"] * 100))
    print("    Undetected:               {} ({:.4f}%)".format(
        log_summary["undetected"],
        (1 - log_summary["total_detection_rate"]) * 100))
    print("    Seal detection rate:      {:.6f}%".format(
        log_summary["seal_detection_rate"] * 100))
    print("    Total detection rate:     {:.6f}%".format(
        log_summary["total_detection_rate"] * 100))

    seal_rate = log_summary["seal_detection_rate"]
    if seal_rate >= 1.0:
        print("\n    >> COMPLETE SEAL DETECTION ON FINITE BENCHMARK <<")
    elif seal_rate >= 0.999:
        print("\n    >> NEAR-COMPLETE SEAL DETECTION (>{:.1f}%) <<".format(seal_rate * 100))
    elif seal_rate >= 0.99:
        print("\n    >> HIGH SEAL DETECTION (>{:.1f}%) <<".format(seal_rate * 100))
    else:
        print("\n    >> SEAL DETECTION GAP: {:.4f}% <<".format((1 - seal_rate) * 100))

    # Pigeonhole warning
    print("\n  THEORETICAL NOTE:")
    print("    Witness space:     154 x 256 = 39,424 bits")
    print("    File at {} bytes: {} bits".format(content_size, content_size * 8))
    if content_size * 8 > 39424:
        print("    Pigeonhole:        file > witness space — collisions MUST exist")
        print("    (This is inherent to ALL hash-based systems, including SHA-256)")
    else:
        print("    Pigeonhole:        file < witness space — no mathematical collision guarantee")

    print("  " + "=" * 68)
    print("  {}".format(BISMILLAH))

    return {
        "seal_detection_rate": log_summary["seal_detection_rate"],
        "crash_rate": log_summary["crash_rate"],
        "total_detection_rate": log_summary["total_detection_rate"],
        "total_mutations": log_summary["total_mutations"],
        "seal_detections": log_summary["seal_detections"],
        "crash_detections": log_summary["crash_detections"],
        "undetected": log_summary["undetected"],
    }


# ============================================================================
#  MAIN
# ============================================================================

def main():
    # [R4] Deterministic seed for reproducibility
    seed = int.from_bytes(os.urandom(4), 'big')
    if len(sys.argv) > 2:
        seed = int(sys.argv[2])
    random.seed(seed)

    print("\n  {}".format(BISMILLAH))
    print("  Finite-Benchmark Detection Test Harness v2.0")
    print("  FATIMA v{} -- 154-Layer Architecture".format(encoder.ENCODER_VERSION))
    print("  Remediation: R1(crash/seal) R2(baseline+ablation) R3(semantic) R4(reproducibility)")
    print("  Random seed: {}".format(seed))
    print("  " + "=" * 60)

    # Determine test content
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
        with open(filepath, 'rb') as f:
            content_bytes = f.read()
        print("  Test file: {} ({} bytes)".format(filepath, len(content_bytes)))
    else:
        encoder_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'bismillah_encoder.py'
        )
        if os.path.exists(encoder_path):
            with open(encoder_path, 'rb') as f:
                content_bytes = f.read()
            print("  Test file: bismillah_encoder.py ({} bytes)".format(len(content_bytes)))
        else:
            content_bytes = (BISMILLAH * 20).encode('utf-8')
            print("  Test content: synthetic ({} bytes)".format(len(content_bytes)))

    # [R4] Record input for reproducibility
    input_sha256 = hashlib.sha256(content_bytes).hexdigest()
    print("  Input SHA-256: {}".format(input_sha256))
    mutation_log.set_input(content_bytes, seed)

    # Sampling parameters
    file_size = len(content_bytes)
    if file_size > 4096:
        max_bits = 500
        max_bytes = 200
        coverage_samples = 150
        baseline_trials = 300
        ablation_trials = 300
    elif file_size > 1024:
        max_bits = 1000
        max_bytes = 400
        coverage_samples = 200
        baseline_trials = 400
        ablation_trials = 400
    else:
        max_bits = None
        max_bytes = None
        coverage_samples = 300
        baseline_trials = 500
        ablation_trials = 500

    all_results = []

    # Tests 1-6: structural mutation detection
    r1 = test_bit_level(content_bytes, max_bits=max_bits)
    all_results.append(r1)

    r2 = test_byte_level(content_bytes, max_positions=max_bytes)
    all_results.append(r2)

    r3 = test_block_level(content_bytes)
    block_totals = {"seal_detected": 0, "crash_detected": 0, "undetected": 0, "total": 0}
    for v in r3["results_by_size"].values():
        block_totals["seal_detected"] += v["seal_detected"]
        block_totals["crash_detected"] += v["crash_detected"]
        block_totals["undetected"] += v["undetected"]
        block_totals["total"] += v["trials"]
    r3.update(block_totals)
    r3["seal_detection_rate"] = block_totals["seal_detected"] / block_totals["total"] if block_totals["total"] else 0
    all_results.append(r3)

    r4 = test_adversarial(content_bytes)
    all_results.append(r4)

    r5 = test_coverage_map(content_bytes, sample_mutations=coverage_samples)
    # Coverage map is diagnostic, not aggregated

    r6 = test_size_threshold(content_bytes)
    # Size threshold has per-size rates — diagnostic

    # [R2] Tests 7-8: baseline and ablation
    r7 = test_sha256_baseline(content_bytes, trials=baseline_trials)
    all_results.append(r7)

    r8 = test_ablation(content_bytes, trials=ablation_trials)
    # Ablation is diagnostic, reported separately

    # [R3] Test 9: semantic
    r9 = test_semantic(content_bytes)
    # Semantic is diagnostic, reported separately

    # Generate report
    reproducibility = {
        "seed": seed,
        "input_sha256": input_sha256,
        "input_size": file_size,
    }
    report = generate_report(all_results, file_size, reproducibility)

    # Save results to JSON
    output_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'shannon_boundary_results.json'
    )
    output_data = {
        BISMILLAH: True,
        "harness_version": "2.0",
        "remediations": ["R1_crash_seal_split", "R2_baseline_ablation",
                         "R3_semantic", "R4_reproducibility"],
        "encoder_version": encoder.ENCODER_VERSION,
        "reproducibility": reproducibility,
        "report": report,
        "tests": {r["test"]: {k: v for k, v in r.items() if k != "test"}
                  for r in all_results},
        "diagnostics": {
            "coverage_map": r5,
            "size_threshold": r6,
            "ablation": r8,
            "semantic": r9,
        },
        "mutation_log": mutation_log.to_dict(),
    }

    with open(output_path, 'w') as f:
        json.dump(output_data, f, indent=2, default=str)

    print("\n  Results saved to: {}".format(output_path))
    print("  To reproduce: python3 -I shannon_boundary_test.py <file> {}".format(seed))
    print("  {}".format(BISMILLAH))


if __name__ == "__main__":
    main()
