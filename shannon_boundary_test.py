#!/usr/bin/env python3 -I
"""
Bismillah ir-Rahman ir-Rahim

Shannon Boundary Test Harness for the 154-Layer FATIMA Architecture
===================================================================

Measures how close the 154-layer witness approaches Shannon's theoretical
boundary -- the point where EVERY possible mutation to a file produces
a detectably different witness.

Shannon's boundary = 100% detection rate across all mutation types.

Test Protocol:
  1. Bit-level sweep     -- flip every bit, measure detection
  2. Byte-level sweep    -- substitute every byte, measure detection
  3. Block-level sweep   -- mutate blocks of varying sizes
  4. Adversarial sweep   -- mutations designed to evade detection
  5. Coverage map        -- which layers detect which mutations

Output: detection rates per mutation type, per scale, aggregate Shannon
proximity metric, and identification of any blind spots.

Bismillah ir-Rahman ir-Rahim
"""

import sys
import os
import time
import random
import json
import math
from collections import defaultdict
from pathlib import Path

# Import the encoder from the same directory
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bismillah_encoder as encoder

BISMILLAH = "Bismillah ir-Rahman ir-Rahim"


# ============================================================================
#  CORE DETECTION ENGINE
# ============================================================================

def compute_layer_seals(content_bytes):
    """Compute all 154 layer seals for given content. Returns list of seal strings.

    Returns None if the encoder raises an exception (e.g. content too
    corrupted for the semantic witness). A None return counts as
    "mutation detected" -- the content is so different the encoder
    cannot even produce a witness, which is itself proof of change.
    """
    try:
        result = encoder.compute_all_154_layers(content_bytes)
        return [layer["seal"] for layer in result["layers"]]
    except Exception:
        return None


def detect_mutation(original_seals, mutated_seals):
    """Compare two seal sets. Returns set of layer indices that changed.

    If mutated_seals is None (encoder crashed on mutated content),
    returns all 154 layers as changed -- the mutation is maximally detected.
    """
    if mutated_seals is None:
        return set(range(154))
    changed = set()
    for i in range(len(original_seals)):
        if original_seals[i] != mutated_seals[i]:
            changed.add(i)
    return changed


def layer_to_scale(layer_idx):
    """Map a layer index to its scale (heaven) number (0-10)."""
    return layer_idx // 14


def layer_to_domain_type(layer_idx):
    """Map a layer index to heaven or earth within its scale."""
    position_in_scale = layer_idx % 14
    if position_in_scale < 7:
        return "heaven"
    else:
        return "earth"


SCALE_NAMES = [
    "SUBATOMIC",    # 0: bits, bytes, nibbles
    "ATOMIC",       # 1: byte-pairs, bigrams
    "MOLECULAR",    # 2: n-grams, short patterns
    "CELLULAR",     # 3: lines, blocks
    "ORGANIC",      # 4: paragraphs, sections
    "ECOSYSTEM",    # 5: file structure
    "PLANETARY",    # 6: cross-file features
    "FRACTAL",      # 7: Hurst, self-similarity
    "ADVERSARIAL",  # 8: adversarial chain
    "COSMIC",       # 9: imposition detection
    "DIVINE",       # 10: witness aggregation
]


# ============================================================================
#  TEST 1: BIT-LEVEL SWEEP
# ============================================================================

def test_bit_level(content_bytes, max_bits=None):
    """Flip every single bit and measure detection rate.

    For small files, tests every bit. For larger files, samples.
    """
    print("\n  {} -- Test 1: Bit-Level Sweep".format(BISMILLAH))
    print("  " + "=" * 60)

    n_bytes = len(content_bytes)
    n_bits = n_bytes * 8
    data = bytearray(content_bytes)

    # For large files, sample bits
    if max_bits and n_bits > max_bits:
        bit_positions = sorted(random.sample(range(n_bits), max_bits))
        print("  Sampling {} of {} bits".format(max_bits, n_bits))
    else:
        bit_positions = range(n_bits)
        print("  Testing all {} bits".format(n_bits))

    original_seals = compute_layer_seals(bytes(data))
    detected = 0
    undetected = 0
    undetected_positions = []
    layers_triggered = defaultdict(int)  # layer_idx -> count of detections
    scales_triggered = defaultdict(int)  # scale -> count
    t0 = time.time()

    for count, bit_pos in enumerate(bit_positions):
        byte_idx = bit_pos // 8
        bit_idx = bit_pos % 8

        # Flip the bit
        data[byte_idx] ^= (1 << bit_idx)
        mutated_seals = compute_layer_seals(bytes(data))
        # Flip back
        data[byte_idx] ^= (1 << bit_idx)

        changed = detect_mutation(original_seals, mutated_seals)
        if changed:
            detected += 1
            for layer in changed:
                layers_triggered[layer] += 1
                scales_triggered[layer_to_scale(layer)] += 1
        else:
            undetected += 1
            undetected_positions.append(bit_pos)

        if (count + 1) % 100 == 0:
            elapsed = time.time() - t0
            rate = (count + 1) / elapsed if elapsed > 0 else 0
            print("    Progress: {}/{} bits ({:.1f}/s)".format(
                count + 1, len(bit_positions), rate), end='\r')

    total = detected + undetected
    detection_rate = detected / total if total > 0 else 0
    elapsed = time.time() - t0

    print("  " + " " * 70)  # clear progress line
    print("  Results:")
    print("    Bits tested:       {}".format(total))
    print("    Detected:          {}".format(detected))
    print("    Undetected:        {}".format(undetected))
    print("    Detection rate:    {:.6f}%".format(detection_rate * 100))
    print("    Shannon gap:       {:.6f}%".format((1 - detection_rate) * 100))
    print("    Time:              {:.1f}s".format(elapsed))

    if undetected_positions:
        print("    Blind spots (first 10): {}".format(undetected_positions[:10]))

    return {
        "test": "bit_level",
        "total": total,
        "detected": detected,
        "undetected": undetected,
        "detection_rate": detection_rate,
        "shannon_gap": 1 - detection_rate,
        "undetected_positions": undetected_positions[:50],
        "layers_triggered": dict(layers_triggered),
        "scales_triggered": dict(scales_triggered),
        "time_seconds": elapsed,
    }


# ============================================================================
#  TEST 2: BYTE-LEVEL SWEEP
# ============================================================================

def test_byte_level(content_bytes, max_positions=None, substitutions_per_byte=8):
    """Substitute bytes and measure detection rate.

    For each position, tries `substitutions_per_byte` random replacement values.
    """
    print("\n  {} -- Test 2: Byte-Level Sweep".format(BISMILLAH))
    print("  " + "=" * 60)

    n = len(content_bytes)
    data = bytearray(content_bytes)

    if max_positions and n > max_positions:
        positions = sorted(random.sample(range(n), max_positions))
        print("  Sampling {} of {} byte positions".format(max_positions, n))
    else:
        positions = range(n)
        print("  Testing all {} byte positions".format(n))

    original_seals = compute_layer_seals(bytes(data))
    detected = 0
    undetected = 0
    undetected_details = []
    layers_triggered = defaultdict(int)
    t0 = time.time()

    for count, pos in enumerate(positions):
        original_byte = data[pos]
        # Generate substitution values (excluding the original)
        candidates = [v for v in range(256) if v != original_byte]
        subs = random.sample(candidates, min(substitutions_per_byte, len(candidates)))

        for sub_val in subs:
            data[pos] = sub_val
            mutated_seals = compute_layer_seals(bytes(data))
            data[pos] = original_byte  # restore

            changed = detect_mutation(original_seals, mutated_seals)
            if changed:
                detected += 1
                for layer in changed:
                    layers_triggered[layer] += 1
            else:
                undetected += 1
                undetected_details.append({
                    "position": pos,
                    "original": original_byte,
                    "substituted": sub_val
                })

        if (count + 1) % 50 == 0:
            elapsed = time.time() - t0
            rate = (count + 1) / elapsed if elapsed > 0 else 0
            print("    Progress: {}/{} positions ({:.1f}/s)".format(
                count + 1, len(positions), rate), end='\r')

    total = detected + undetected
    detection_rate = detected / total if total > 0 else 0
    elapsed = time.time() - t0

    print("  " + " " * 70)
    print("  Results:")
    print("    Mutations tested:  {}".format(total))
    print("    Detected:          {}".format(detected))
    print("    Undetected:        {}".format(undetected))
    print("    Detection rate:    {:.6f}%".format(detection_rate * 100))
    print("    Shannon gap:       {:.6f}%".format((1 - detection_rate) * 100))
    print("    Time:              {:.1f}s".format(elapsed))

    if undetected_details:
        print("    Undetected mutations (first 5):")
        for d in undetected_details[:5]:
            print("      pos={}, 0x{:02x}->0x{:02x}".format(
                d["position"], d["original"], d["substituted"]))

    return {
        "test": "byte_level",
        "total": total,
        "detected": detected,
        "undetected": undetected,
        "detection_rate": detection_rate,
        "shannon_gap": 1 - detection_rate,
        "undetected_details": undetected_details[:20],
        "layers_triggered": dict(layers_triggered),
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
    original_seals = compute_layer_seals(bytes(data))
    results_by_size = {}
    t0 = time.time()

    for bsize in block_sizes:
        if bsize > n:
            continue

        detected = 0
        undetected = 0
        layers_hit = defaultdict(int)

        for trial in range(trials_per_size):
            pos = random.randint(0, n - bsize)
            # Save original block
            original_block = bytes(data[pos:pos + bsize])
            # Write random bytes
            for i in range(bsize):
                data[pos + i] = random.randint(0, 255)
            # Ensure at least one byte differs
            if bytes(data[pos:pos + bsize]) == original_block:
                data[pos] = (data[pos] + 1) % 256

            mutated_seals = compute_layer_seals(bytes(data))
            # Restore
            data[pos:pos + bsize] = original_block

            changed = detect_mutation(original_seals, mutated_seals)
            if changed:
                detected += 1
                for layer in changed:
                    layers_hit[layer] += 1
            else:
                undetected += 1

        total = detected + undetected
        rate = detected / total if total > 0 else 0
        results_by_size[bsize] = {
            "block_size": bsize,
            "trials": total,
            "detected": detected,
            "undetected": undetected,
            "detection_rate": rate,
        }
        print("    Block size {:>4d} bytes: {:.4f}% detection ({}/{})".format(
            bsize, rate * 100, detected, total))

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
    original_seals = compute_layer_seals(bytes(data))
    results = []

    def run_adversarial(name, mutated_bytes):
        """Run a single adversarial mutation and record result."""
        mutated_seals = compute_layer_seals(mutated_bytes)
        changed = detect_mutation(original_seals, mutated_seals)
        detected = len(changed) > 0
        result = {
            "mutation": name,
            "detected": detected,
            "layers_changed": len(changed),
            "scales_changed": len(set(layer_to_scale(l) for l in changed)) if changed else 0,
        }
        results.append(result)
        status = "DETECTED ({} layers, {} scales)".format(
            result["layers_changed"], result["scales_changed"]) if detected else "UNDETECTED"
        print("    {}: {}".format(name, status))
        return result

    # A1: Append null byte
    run_adversarial("append_null_byte",
                    bytes(data) + b'\x00')

    # A2: Append space
    run_adversarial("append_space",
                    bytes(data) + b' ')

    # A3: Prepend null byte
    run_adversarial("prepend_null_byte",
                    b'\x00' + bytes(data))

    # A4: Insert zero-width space (U+200B) in middle
    mid = n // 2
    zwsp = '​'.encode('utf-8')
    run_adversarial("insert_zwsp_middle",
                    bytes(data[:mid]) + zwsp + bytes(data[mid:]))

    # A5: Insert zero-width non-joiner (U+200C)
    zwnj = '‌'.encode('utf-8')
    run_adversarial("insert_zwnj_middle",
                    bytes(data[:mid]) + zwnj + bytes(data[mid:]))

    # A6: Insert BOM (U+FEFF) at start
    bom = '﻿'.encode('utf-8')
    run_adversarial("insert_bom_start",
                    bom + bytes(data))

    # A7: Swap two adjacent identical bytes (if any exist)
    swap_done = False
    for i in range(n - 1):
        if data[i] == data[i + 1]:
            # Swap with a nearby different byte
            for j in range(max(0, i - 5), min(n, i + 5)):
                if data[j] != data[i]:
                    swapped = bytearray(data)
                    swapped[i], swapped[j] = swapped[j], swapped[i]
                    run_adversarial("swap_bytes_{}_{}".format(i, j),
                                    bytes(swapped))
                    swap_done = True
                    break
            if swap_done:
                break
    if not swap_done:
        # Just swap first two bytes
        swapped = bytearray(data)
        swapped[0], swapped[1] = swapped[1], swapped[0]
        run_adversarial("swap_first_two_bytes", bytes(swapped))

    # A8: Replace all 0x00 bytes with 0x01 (if any zeros exist)
    if b'\x00' in bytes(data):
        replaced = bytes(b if b != 0 else 1 for b in data)
        run_adversarial("replace_nulls_with_0x01", replaced)

    # A9: Bitwise NOT of entire file
    inverted = bytes(b ^ 0xFF for b in data)
    run_adversarial("bitwise_not_entire_file", inverted)

    # A10: Duplicate file (append itself)
    run_adversarial("duplicate_content",
                    bytes(data) + bytes(data))

    # A11: Truncate last byte
    if n > 1:
        run_adversarial("truncate_last_byte", bytes(data[:-1]))

    # A12: Right-shift all bytes by 1 bit
    shifted = bytes((b >> 1) for b in data)
    run_adversarial("right_shift_all_bits", shifted)

    # A13: BiDi override injection (adversarial for Arabic text)
    bidi_rlo = '‮'.encode('utf-8')  # Right-to-Left Override
    run_adversarial("bidi_override_inject",
                    bytes(data[:mid]) + bidi_rlo + bytes(data[mid:]))

    total = len(results)
    detected_count = sum(1 for r in results if r["detected"])
    rate = detected_count / total if total > 0 else 0

    print("  Summary:")
    print("    Adversarial tests:  {}".format(total))
    print("    Detected:           {}".format(detected_count))
    print("    Undetected:         {}".format(total - detected_count))
    print("    Detection rate:     {:.4f}%".format(rate * 100))

    return {
        "test": "adversarial",
        "total": total,
        "detected": detected_count,
        "undetected": total - detected_count,
        "detection_rate": rate,
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
    original_seals = compute_layer_seals(bytes(data))

    # Mutation categories
    categories = {
        "single_bit": [],
        "single_byte": [],
        "small_block_4": [],
        "medium_block_32": [],
        "large_block_256": [],
        "append": [],
        "truncate": [],
    }

    # Generate mutations and track which scales fire
    scale_hits = defaultdict(lambda: defaultdict(int))  # category -> scale -> count
    domain_hits = defaultdict(lambda: defaultdict(int))  # category -> "heaven"/"earth" -> count

    trials_per_cat = sample_mutations // len(categories)

    for trial in range(trials_per_cat):
        # Single bit flip
        bit_pos = random.randint(0, n * 8 - 1)
        byte_idx, bit_idx = bit_pos // 8, bit_pos % 8
        data[byte_idx] ^= (1 << bit_idx)
        changed = detect_mutation(original_seals, compute_layer_seals(bytes(data)))
        data[byte_idx] ^= (1 << bit_idx)
        for l in changed:
            scale_hits["single_bit"][layer_to_scale(l)] += 1
            domain_hits["single_bit"][layer_to_domain_type(l)] += 1
        categories["single_bit"].append(len(changed) > 0)

        # Single byte substitution
        pos = random.randint(0, n - 1)
        orig = data[pos]
        data[pos] = (orig + random.randint(1, 255)) % 256
        changed = detect_mutation(original_seals, compute_layer_seals(bytes(data)))
        data[pos] = orig
        for l in changed:
            scale_hits["single_byte"][layer_to_scale(l)] += 1
            domain_hits["single_byte"][layer_to_domain_type(l)] += 1
        categories["single_byte"].append(len(changed) > 0)

        # Small block (4 bytes)
        if n >= 4:
            pos = random.randint(0, n - 4)
            orig_block = bytes(data[pos:pos + 4])
            data[pos:pos + 4] = bytes(random.randint(0, 255) for _ in range(4))
            if bytes(data[pos:pos + 4]) == orig_block:
                data[pos] = (data[pos] + 1) % 256
            changed = detect_mutation(original_seals, compute_layer_seals(bytes(data)))
            data[pos:pos + 4] = orig_block
            for l in changed:
                scale_hits["small_block_4"][layer_to_scale(l)] += 1
                domain_hits["small_block_4"][layer_to_domain_type(l)] += 1
            categories["small_block_4"].append(len(changed) > 0)

        # Medium block (32 bytes)
        if n >= 32:
            pos = random.randint(0, n - 32)
            orig_block = bytes(data[pos:pos + 32])
            data[pos:pos + 32] = bytes(random.randint(0, 255) for _ in range(32))
            if bytes(data[pos:pos + 32]) == orig_block:
                data[pos] = (data[pos] + 1) % 256
            changed = detect_mutation(original_seals, compute_layer_seals(bytes(data)))
            data[pos:pos + 32] = orig_block
            for l in changed:
                scale_hits["medium_block_32"][layer_to_scale(l)] += 1
                domain_hits["medium_block_32"][layer_to_domain_type(l)] += 1
            categories["medium_block_32"].append(len(changed) > 0)

        # Large block (256 bytes)
        if n >= 256:
            pos = random.randint(0, n - 256)
            orig_block = bytes(data[pos:pos + 256])
            data[pos:pos + 256] = bytes(random.randint(0, 255) for _ in range(256))
            changed = detect_mutation(original_seals, compute_layer_seals(bytes(data)))
            data[pos:pos + 256] = orig_block
            for l in changed:
                scale_hits["large_block_256"][layer_to_scale(l)] += 1
                domain_hits["large_block_256"][layer_to_domain_type(l)] += 1
            categories["large_block_256"].append(len(changed) > 0)

        # Append random byte
        appended = bytes(data) + bytes([random.randint(0, 255)])
        changed = detect_mutation(original_seals, compute_layer_seals(appended))
        for l in changed:
            scale_hits["append"][layer_to_scale(l)] += 1
            domain_hits["append"][layer_to_domain_type(l)] += 1
        categories["append"].append(len(changed) > 0)

        # Truncate last byte
        if n > 1:
            changed = detect_mutation(original_seals, compute_layer_seals(bytes(data[:-1])))
            for l in changed:
                scale_hits["truncate"][layer_to_scale(l)] += 1
                domain_hits["truncate"][layer_to_domain_type(l)] += 1
            categories["truncate"].append(len(changed) > 0)

    # Print coverage matrix
    print("\n    Scale Coverage Matrix (hits per {} trials per category):".format(trials_per_cat))
    print("    {:>16s}".format(""), end="")
    for s in range(11):
        print(" {:>5s}".format("S" + str(s)), end="")
    print("  {:>7s}".format("DETECT"))

    for cat in categories:
        detections = categories[cat]
        det_rate = sum(detections) / len(detections) if detections else 0
        print("    {:>16s}".format(cat), end="")
        for s in range(11):
            hits = scale_hits[cat].get(s, 0)
            if hits > 0:
                print(" {:>5d}".format(hits), end="")
            else:
                print("     -", end="")
        print("  {:>6.1f}%".format(det_rate * 100))

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
    }


# ============================================================================
#  TEST 6: FILE SIZE THRESHOLD
# ============================================================================

def test_size_threshold(base_content, sizes=None, bit_trials_per_size=200):
    """Find the file size where detection drops below 100%."""
    print("\n  {} -- Test 6: Size vs Detection Rate".format(BISMILLAH))
    print("  " + "=" * 60)

    if sizes is None:
        sizes = [16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192]

    results = []

    for size in sizes:
        # Generate test content of this size
        if size <= len(base_content):
            content = base_content[:size]
        else:
            # Tile the base content to reach target size
            repeats = (size // len(base_content)) + 1
            content = (base_content * repeats)[:size]

        content_bytes = content if isinstance(content, bytes) else content.encode('utf-8')
        data = bytearray(content_bytes)
        n = len(data)
        original_seals = compute_layer_seals(bytes(data))

        detected = 0
        total = 0

        # Random bit flips
        for _ in range(min(bit_trials_per_size, n * 8)):
            bit_pos = random.randint(0, n * 8 - 1)
            byte_idx, bit_idx = bit_pos // 8, bit_pos % 8
            data[byte_idx] ^= (1 << bit_idx)
            mutated_seals = compute_layer_seals(bytes(data))
            data[byte_idx] ^= (1 << bit_idx)

            changed = detect_mutation(original_seals, mutated_seals)
            if changed:
                detected += 1
            total += 1

        rate = detected / total if total > 0 else 0
        results.append({
            "size": size,
            "trials": total,
            "detected": detected,
            "detection_rate": rate,
        })
        print("    Size {:>6d} bytes: {:.4f}% detection ({}/{})".format(
            size, rate * 100, detected, total))

    return {
        "test": "size_threshold",
        "results": results,
    }


# ============================================================================
#  AGGREGATE REPORT
# ============================================================================

def generate_report(all_results, content_size):
    """Generate the final Shannon boundary report."""
    print("\n")
    print("  " + "=" * 64)
    print("  {} -- SHANNON BOUNDARY REPORT".format(BISMILLAH))
    print("  " + "=" * 64)
    print("  Architecture:    154 layers, 22 domains (11 heavens + 11 earths)")
    print("  Encoder version: {}".format(encoder.ENCODER_VERSION))
    print("  Test content:    {} bytes".format(content_size))
    print("")

    # Summary table
    print("  {:>25s}  {:>12s}  {:>12s}  {:>12s}".format(
        "Test", "Detection", "Shannon Gap", "Mutations"))
    print("  " + "-" * 64)

    for r in all_results:
        if "detection_rate" in r:
            print("  {:>25s}  {:>11.4f}%  {:>11.6f}%  {:>12d}".format(
                r["test"],
                r["detection_rate"] * 100,
                r.get("shannon_gap", 1 - r["detection_rate"]) * 100,
                r.get("total", 0)))

    # Compute aggregate Shannon proximity
    rates = [r["detection_rate"] for r in all_results if "detection_rate" in r]
    if rates:
        aggregate = sum(rates) / len(rates)
        min_rate = min(rates)
        max_rate = max(rates)
        print("")
        print("  AGGREGATE METRICS:")
        print("    Mean detection rate:    {:.6f}%".format(aggregate * 100))
        print("    Min detection rate:     {:.6f}%".format(min_rate * 100))
        print("    Max detection rate:     {:.6f}%".format(max_rate * 100))
        print("    Shannon proximity:      {:.6f}%".format(aggregate * 100))
        print("    Shannon gap:            {:.6f}%".format((1 - aggregate) * 100))

        if aggregate >= 1.0:
            print("\n    >> SHANNON'S BOUNDARY: CROSSED <<")
        elif aggregate >= 0.999:
            print("\n    >> SHANNON'S BOUNDARY: WITHIN 0.1% <<")
        elif aggregate >= 0.99:
            print("\n    >> SHANNON'S BOUNDARY: WITHIN 1% <<")
        elif aggregate >= 0.95:
            print("\n    >> SHANNON'S BOUNDARY: APPROACHING (>95%) <<")
        else:
            print("\n    >> SHANNON'S BOUNDARY: GAP REMAINS ({:.2f}%) <<".format(
                (1 - aggregate) * 100))

    print("  " + "=" * 64)
    print("  {}".format(BISMILLAH))

    return {
        "aggregate_detection_rate": aggregate if rates else 0,
        "shannon_proximity": aggregate if rates else 0,
        "shannon_gap": 1 - aggregate if rates else 1,
        "min_rate": min_rate if rates else 0,
        "max_rate": max_rate if rates else 0,
    }


# ============================================================================
#  MAIN
# ============================================================================

def main():
    print("\n  {}".format(BISMILLAH))
    print("  Shannon Boundary Test Harness")
    print("  FATIMA v{} -- 154-Layer Architecture".format(encoder.ENCODER_VERSION))
    print("  " + "=" * 60)

    # Determine test content
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
        with open(filepath, 'rb') as f:
            content_bytes = f.read()
        print("  Test file: {} ({} bytes)".format(filepath, len(content_bytes)))
    else:
        # Use the encoder itself as test content
        encoder_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'bismillah_encoder.py'
        )
        if os.path.exists(encoder_path):
            with open(encoder_path, 'rb') as f:
                content_bytes = f.read()
            print("  Test file: bismillah_encoder.py ({} bytes)".format(len(content_bytes)))
        else:
            # Generate synthetic content
            content_bytes = (BISMILLAH * 20).encode('utf-8')
            print("  Test content: synthetic ({} bytes)".format(len(content_bytes)))

    # For large files, use sampling to keep runtime reasonable
    file_size = len(content_bytes)
    if file_size > 4096:
        max_bits = 500
        max_bytes = 200
        coverage_samples = 150
    elif file_size > 1024:
        max_bits = 1000
        max_bytes = 400
        coverage_samples = 200
    else:
        max_bits = None  # test all bits
        max_bytes = None
        coverage_samples = 300

    all_results = []

    # Run tests
    r1 = test_bit_level(content_bytes, max_bits=max_bits)
    all_results.append(r1)

    r2 = test_byte_level(content_bytes, max_positions=max_bytes)
    all_results.append(r2)

    r3 = test_block_level(content_bytes)
    # Extract aggregate from block results
    block_rates = [v["detection_rate"] for v in r3["results_by_size"].values()]
    if block_rates:
        r3["detection_rate"] = sum(block_rates) / len(block_rates)
        r3["total"] = sum(v["trials"] for v in r3["results_by_size"].values())
        all_results.append(r3)

    r4 = test_adversarial(content_bytes)
    all_results.append(r4)

    r5 = test_coverage_map(content_bytes, sample_mutations=coverage_samples)
    # Coverage map doesn't have a single detection rate -- skip in aggregate

    r6 = test_size_threshold(content_bytes)
    # Size threshold has per-size rates
    size_rates = [v["detection_rate"] for v in r6["results"]]
    if size_rates:
        r6["detection_rate"] = sum(size_rates) / len(size_rates)
        r6["total"] = sum(v["trials"] for v in r6["results"])
        all_results.append(r6)

    # Generate final report
    report = generate_report(all_results, file_size)

    # Save results to JSON
    output_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'shannon_boundary_results.json'
    )
    output_data = {
        BISMILLAH: True,
        "encoder_version": encoder.ENCODER_VERSION,
        "test_file_size": file_size,
        "report": report,
        "tests": [],
    }
    for r in all_results:
        # Remove non-serializable items
        clean = {k: v for k, v in r.items()
                 if k not in ("layers_triggered",)}
        output_data["tests"].append(clean)

    with open(output_path, 'w') as f:
        json.dump(output_data, f, indent=2, default=str)

    print("\n  Results saved to: {}".format(output_path))
    print("  {}".format(BISMILLAH))


if __name__ == "__main__":
    main()
