# Bismillah ir-Rahman ir-Rahim
"""
Bismillah Divine Protection Encoder -- FATIMA v4.0 -- 11-Heaven Architecture

Seals every file in a directory with the name of Allah subhanahu wa ta'ala
across ELEVEN HEAVENS of protection, containing 151 LAYERS total -- from
subatomic particles to the largest scale of creation -- so that no file
remains unprotected against shaytan, in sha Allah.

THE 11-HEAVEN ARCHITECTURE:

  The upgrade from 11 flat layers (v3.0) to 11 heavens containing 151 layers
  (v4.0) is grounded in four findings:

    1. "The Pre-Corruption Signal and Its Mathematical Witness" (Arfeen 2026)
       -- The Hurst exponent peaks at N=11, identifying the dimensional
       constant of creation as eleven. H(11) = 1.0157 (harmonic R/S).

    2. "The Guarded Reminder and the Adversarial Architecture" (Arfeen 2026)
       -- The adversary operates as a mode-collapse vector within Allah's
       singular generative architecture.

    3. "Shayatin Amongst Matter" (Arfeen 2026)
       -- Adversarial jinn-class entities operate through material substrates
       at every scale of creation, from elements to biological systems.

    4. "The Propagation Architecture of Sihr" (Arfeen 2026)
       -- Sihr propagates through speech, material, and cognitive channels
       at every level of the substrate hierarchy.

  The Qur'an references seven heavens (67:3, 71:15), but the mathematical
  witness of the Hurst exponent reveals eleven as the dimensional constant.
  Seven is what the Qur'an says; eleven is what the Qur'an shows. The 151
  layers across 11 heavens map to every scale of Allah's creation:

HEAVEN MAP (11 Heavens, 151 Layers):

  Heaven 0  -- AS-SAMAWAT AD-DUNYA (The Nearest Heaven)
               Scale: SUBATOMIC -- individual bits and bytes
               Layers: 1-14 (14 layers)
               Guardian: Az-Zahir (The Manifest)

  Heaven 1  -- AS-SAMAWAT ATH-THANIYA (The Second Heaven)
               Scale: ATOMIC -- byte-pairs and nibble patterns
               Layers: 15-27 (13 layers)
               Guardian: Al-Musawwir (The Fashioner)

  Heaven 2  -- AS-SAMAWAT ATH-THALITHA (The Third Heaven)
               Scale: MOLECULAR -- block-level structures (4-64 bytes)
               Layers: 28-40 (13 layers)
               Guardian: Al-Batin (The Hidden)

  Heaven 3  -- AS-SAMAWAT AR-RABI'A (The Fourth Heaven)
               Scale: CELLULAR -- paragraph and section-level patterns
               Layers: 41-53 (13 layers)
               Guardian: Al-Alim (The All-Knowing)

  Heaven 4  -- AS-SAMAWAT AL-KHAMISA (The Fifth Heaven)
               Scale: ORGANIC -- structural flow and control markers
               Layers: 54-67 (14 layers)
               Guardian: Al-Hafiz (The Preserver)

  Heaven 5  -- AS-SAMAWAT AS-SADISA (The Sixth Heaven)
               Scale: TERRESTRIAL -- semantic fingerprinting
               Layers: 68-80 (13 layers)
               Guardian: Al-Muhaymin (The Protector)

  Heaven 6  -- AS-SAMAWAT AS-SABI'A (The Seventh Heaven)
               Scale: PLANETARY -- whole-section integrity
               Layers: 81-94 (14 layers)
               Guardian: Al-Waliyy (The Protector/Friend)

  Heaven 7  -- AS-SAMAWAT ATH-THAMINA (The Eighth Heaven)
               Scale: STELLAR -- cross-section fractal relationships
               Layers: 95-108 (14 layers)
               Guardian: Al-Hasib (The Reckoner)

  Heaven 8  -- AS-SAMAWAT AT-TASI'A (The Ninth Heaven)
               Scale: GALACTIC -- whole-file fractal properties
               Layers: 109-122 (14 layers)
               Guardian: Ar-Raqib (The Watchful)

  Heaven 9  -- AS-SAMAWAT AL-'ASHIRA (The Tenth Heaven)
               Scale: COSMIC -- inter-file and directory-level relationships
               Layers: 123-140 (18 layers)
               Guardian: Al-Muhsi (The Accounter)

  Heaven 10 -- SIDRAT AL-MUNTAHA (The Lote Tree of the Utmost Boundary)
               Scale: DIVINE WITNESS -- self-referential testimony
               Layers: 141-151 (11 layers -- one per heaven)
               Guardian: Ash-Shahid (The Witness)

  Total: 151 layers across 11 heavens (pathways)

  "He it is who created for you all that is on the earth. Then He
  turned to the heaven and made them seven heavens, and He is the
  Knower of all things." (2:29)

  "Do you not see how Allah has created seven heavens in layers?"
  (71:15)

  "Indeed, I have seen eleven stars and the sun and the moon;
  I saw them prostrating to me." (12:4)

USAGE:
    python bismillah_encoder.py seal <path>            # Seal all files (151 layers)
    python bismillah_encoder.py seal <path> --names    # Seal + embed 99 Names
    python bismillah_encoder.py verify <path>          # Verify protection
    python bismillah_encoder.py verify <path> --strict # Verify + hash chain check
    python bismillah_encoder.py manifest <path>        # Generate integrity manifest
    python bismillah_encoder.py witness <path>         # Generate fractal witness report
    python bismillah_encoder.py heavens <path>         # Display heaven-by-heaven report

"In the name of Allah, the Most Merciful, the Most Compassionate."
"He is Allah, other than whom there is no deity, Knower of the unseen and
the witnessed. He is the Most Merciful, the Most Compassionate." (59:22)

"Indeed, it is We who sent down the Reminder, and indeed,
We will be its Guardian." (15:9)

Author: Bilal Syed Arfeen
License: MIT -- free for the ummah, free for all of creation, in sha Allah
"""

import os
import sys
import json
import math
import hashlib
import zipfile
import shutil
import struct
import tempfile
import argparse
import unicodedata
from pathlib import Path
from collections import OrderedDict

# Bismillah ir-Rahman ir-Rahim
# ============================================================================
#  DIVINE CONSTANTS
# ============================================================================

BISMILLAH = "Bismillah ir-Rahman ir-Rahim"
BISMILLAH_ARABIC = "بِسْمِ اللَّهِ الرَّحْمَـنِ الرَّحِيمِ"

# The dimensional constant of creation, witnessed by the Hurst exponent
DIMENSIONAL_CONSTANT = 11
TOTAL_LAYERS = 151
TOTAL_HEAVENS = 11
HURST_HARMONIC = 1.0157      # H(11) via harmonic R/S analysis
HURST_PARTITIONED = 0.9898   # H_inter(11) via partitioned analysis
HURST_PERFECT = 1.0          # Perfect persistence -- the convergence target
ENCODER_VERSION = "4.0.0"

# Surah Yusuf 12:4 -- The number that survives uncorrupted
# "Indeed, I have seen eleven stars and the sun and the moon;
#  I saw them prostrating to me."
YUSUF_WITNESS = 11

# ============================================================================
#  AL-ASMA UL-HUSNA -- The 99 Beautiful Names of Allah
# ============================================================================

AL_ASMA_UL_HUSNA = [
    ("Allah", "The God"),
    ("Ar-Rahman", "The Most Merciful"),
    ("Ar-Rahim", "The Most Compassionate"),
    ("Al-Malik", "The King"),
    ("Al-Quddus", "The Most Holy"),
    ("As-Salam", "The Source of Peace"),
    ("Al-Mu'min", "The Guardian of Faith"),
    ("Al-Muhaymin", "The Protector"),
    ("Al-Aziz", "The Almighty"),
    ("Al-Jabbar", "The Compeller"),
    ("Al-Mutakabbir", "The Supreme"),
    ("Al-Khaliq", "The Creator"),
    ("Al-Bari", "The Evolver"),
    ("Al-Musawwir", "The Fashioner"),
    ("Al-Ghaffar", "The Forgiver"),
    ("Al-Qahhar", "The Subduer"),
    ("Al-Wahhab", "The Bestower"),
    ("Ar-Razzaq", "The Provider"),
    ("Al-Fattah", "The Opener"),
    ("Al-Alim", "The All-Knowing"),
    ("Al-Qabid", "The Restrainer"),
    ("Al-Basit", "The Expander"),
    ("Al-Khafid", "The Abaser"),
    ("Ar-Rafi", "The Exalter"),
    ("Al-Mu'izz", "The Bestower of Honor"),
    ("Al-Mudhill", "The Humiliator"),
    ("As-Sami", "The All-Hearing"),
    ("Al-Basir", "The All-Seeing"),
    ("Al-Hakam", "The Judge"),
    ("Al-Adl", "The Just"),
    ("Al-Latif", "The Subtle One"),
    ("Al-Khabir", "The All-Aware"),
    ("Al-Halim", "The Forbearing"),
    ("Al-Azim", "The Magnificent"),
    ("Al-Ghafur", "The All-Forgiving"),
    ("Ash-Shakur", "The Appreciative"),
    ("Al-Ali", "The Most High"),
    ("Al-Kabir", "The Most Great"),
    ("Al-Hafiz", "The Preserver"),
    ("Al-Muqit", "The Sustainer"),
    ("Al-Hasib", "The Reckoner"),
    ("Al-Jalil", "The Majestic"),
    ("Al-Karim", "The Generous"),
    ("Ar-Raqib", "The Watchful"),
    ("Al-Mujib", "The Responsive"),
    ("Al-Wasi", "The All-Encompassing"),
    ("Al-Hakim", "The Perfectly Wise"),
    ("Al-Wadud", "The Loving One"),
    ("Al-Ba'ith", "The Resurrector"),
    ("Ash-Shahid", "The Witness"),
    ("Al-Haqq", "The Truth"),
    ("Al-Wakil", "The Trustee"),
    ("Al-Qawiyy", "The Most Strong"),
    ("Al-Matin", "The Firm One"),
    ("Al-Waliyy", "The Protector"),
    ("Al-Hamid", "The Praiseworthy"),
    ("Al-Muhsi", "The Accounter"),
    ("Al-Mubdi", "The Originator"),
    ("Al-Mu'id", "The Restorer"),
    ("Al-Muhyi", "The Giver of Life"),
    ("Al-Mumit", "The Creator of Death"),
    ("Al-Hayy", "The Ever Living"),
    ("Al-Qayyum", "The Self-Subsisting"),
    ("Al-Wajid", "The Finder"),
    ("Al-Majid", "The Noble"),
    ("Al-Wahid", "The Unique"),
    ("Al-Ahad", "The One"),
    ("As-Samad", "The Eternal"),
    ("Al-Qadir", "The Able"),
    ("Al-Muqtadir", "The Powerful"),
    ("Al-Muqaddim", "The Expediter"),
    ("Al-Mu'akhkhir", "The Delayer"),
    ("Al-Awwal", "The First"),
    ("Al-Akhir", "The Last"),
    ("Az-Zahir", "The Manifest"),
    ("Al-Batin", "The Hidden"),
    ("Al-Wali", "The Governor"),
    ("Al-Muta'ali", "The Most Exalted"),
    ("Al-Barr", "The Source of Goodness"),
    ("At-Tawwab", "The Acceptor of Repentance"),
    ("Al-Muntaqim", "The Avenger"),
    ("Al-Afuww", "The Pardoner"),
    ("Ar-Ra'uf", "The Most Kind"),
    ("Malik-ul-Mulk", "Owner of Sovereignty"),
    ("Dhul-Jalali wal-Ikram", "Lord of Majesty and Generosity"),
    ("Al-Muqsit", "The Equitable"),
    ("Al-Jami", "The Gatherer"),
    ("Al-Ghaniyy", "The Self-Sufficient"),
    ("Al-Mughni", "The Enricher"),
    ("Al-Mani", "The Preventer"),
    ("Ad-Darr", "The Distresser"),
    ("An-Nafi", "The Propitious"),
    ("An-Nur", "The Light"),
    ("Al-Hadi", "The Guide"),
    ("Al-Badi", "The Originator"),
    ("Al-Baqi", "The Everlasting"),
    ("Al-Warith", "The Inheritor"),
    ("Ar-Rashid", "The Guide to the Right Path"),
    ("As-Sabur", "The Patient"),
]


def _name_for_layer(layer_idx):
    """Return the Divine Name assigned to a specific layer (0-150).

    The 99 Names cycle through all 151 layers: the first 99 layers each
    get a unique Name, then layers 99-150 cycle back from the beginning,
    so that every layer is sealed by a Name and every Name is honored.
    99 + 52 = 151.
    """
    return AL_ASMA_UL_HUSNA[layer_idx % len(AL_ASMA_UL_HUSNA)]


# ============================================================================
#  THE 11 HEAVENS -- Structure Definition
# ============================================================================

# Each heaven: (name_ar, name_en, scale, guardian_name, guardian_meaning,
#               layer_start, layer_end_inclusive, layer_count)
HEAVENS = [
    {
        "heaven": 0,
        "name_ar": "As-Samawat ad-Dunya",
        "name_en": "The Nearest Heaven",
        "scale": "SUBATOMIC",
        "scale_desc": "Individual bits, bytes, and nibbles",
        "guardian": "Az-Zahir",
        "guardian_meaning": "The Manifest",
        "layer_start": 0,
        "layer_end": 13,  # inclusive
        "layer_count": 14,
        "quranic": "67:3 -- He who created seven heavens in layers",
    },
    {
        "heaven": 1,
        "name_ar": "As-Samawat ath-Thaniya",
        "name_en": "The Second Heaven",
        "scale": "ATOMIC",
        "scale_desc": "Byte-pairs, bigrams, and nibble distributions",
        "guardian": "Al-Musawwir",
        "guardian_meaning": "The Fashioner",
        "layer_start": 14,
        "layer_end": 26,
        "layer_count": 13,
        "quranic": "41:12 -- He completed them as seven heavens in two days",
    },
    {
        "heaven": 2,
        "name_ar": "As-Samawat ath-Thalitha",
        "name_en": "The Third Heaven",
        "scale": "MOLECULAR",
        "scale_desc": "Block-level structures (4-64 byte windows)",
        "guardian": "Al-Batin",
        "guardian_meaning": "The Hidden",
        "layer_start": 27,
        "layer_end": 39,
        "layer_count": 13,
        "quranic": "23:17 -- We created above you seven pathways",
    },
    {
        "heaven": 3,
        "name_ar": "As-Samawat ar-Rabi'a",
        "name_en": "The Fourth Heaven",
        "scale": "CELLULAR",
        "scale_desc": "Paragraph and section-level patterns",
        "guardian": "Al-Alim",
        "guardian_meaning": "The All-Knowing",
        "layer_start": 40,
        "layer_end": 52,
        "layer_count": 13,
        "quranic": "65:12 -- Allah who created seven heavens and of the earth the like",
    },
    {
        "heaven": 4,
        "name_ar": "As-Samawat al-Khamisa",
        "name_en": "The Fifth Heaven",
        "scale": "ORGANIC",
        "scale_desc": "Structural flow, control markers, and newline topology",
        "guardian": "Al-Hafiz",
        "guardian_meaning": "The Preserver",
        "layer_start": 53,
        "layer_end": 66,
        "layer_count": 14,
        "quranic": "15:9 -- Indeed, it is We who sent down the Reminder",
    },
    {
        "heaven": 5,
        "name_ar": "As-Samawat as-Sadisa",
        "name_en": "The Sixth Heaven",
        "scale": "TERRESTRIAL",
        "scale_desc": "Semantic fingerprinting and character-class distributions",
        "guardian": "Al-Muhaymin",
        "guardian_meaning": "The Protector",
        "layer_start": 67,
        "layer_end": 79,
        "layer_count": 13,
        "quranic": "2:255 -- His Throne extends over the heavens and the earth",
    },
    {
        "heaven": 6,
        "name_ar": "As-Samawat as-Sabi'a",
        "name_en": "The Seventh Heaven",
        "scale": "PLANETARY",
        "scale_desc": "Whole-section integrity and positional hashing",
        "guardian": "Al-Waliyy",
        "guardian_meaning": "The Protector/Friend",
        "layer_start": 80,
        "layer_end": 93,
        "layer_count": 14,
        "quranic": "71:15 -- Do you not see how Allah created seven heavens in layers",
    },
    {
        "heaven": 7,
        "name_ar": "As-Samawat ath-Thamina",
        "name_en": "The Eighth Heaven",
        "scale": "STELLAR",
        "scale_desc": "Cross-section fractal relationships and Hurst watermarks",
        "guardian": "Al-Hasib",
        "guardian_meaning": "The Reckoner",
        "layer_start": 94,
        "layer_end": 107,
        "layer_count": 14,
        "quranic": "12:4 -- I have seen eleven stars",
    },
    {
        "heaven": 8,
        "name_ar": "As-Samawat at-Tasi'a",
        "name_en": "The Ninth Heaven",
        "scale": "GALACTIC",
        "scale_desc": "Whole-file fractal properties and adversarial chain",
        "guardian": "Ar-Raqib",
        "guardian_meaning": "The Watchful",
        "layer_start": 108,
        "layer_end": 121,
        "layer_count": 14,
        "quranic": "41:42 -- Falsehood cannot approach it from before it or behind it",
    },
    {
        "heaven": 9,
        "name_ar": "As-Samawat al-'Ashira",
        "name_en": "The Tenth Heaven",
        "scale": "COSMIC",
        "scale_desc": "Inter-file relationships, directory-level integrity, imposition spectrum",
        "guardian": "Al-Muhsi",
        "guardian_meaning": "The Accounter",
        "layer_start": 122,
        "layer_end": 139,
        "layer_count": 18,
        "quranic": "21:30 -- The heavens and earth were a joined entity then We separated them",
    },
    {
        "heaven": 10,
        "name_ar": "Sidrat al-Muntaha",
        "name_en": "The Lote Tree of the Utmost Boundary",
        "scale": "DIVINE WITNESS",
        "scale_desc": "Self-referential testimony -- one witness per heaven",
        "guardian": "Ash-Shahid",
        "guardian_meaning": "The Witness",
        "layer_start": 140,
        "layer_end": 150,
        "layer_count": 11,
        "quranic": "53:14 -- Near the Lote Tree of the Utmost Boundary",
    },
]

# The three modes of adversarial corruption (Paper 2, Unit I)
CORRUPTION_MODES = {
    "shahwa": "desire -- the appetite vector",
    "kibr": "arrogance -- the self-elevation vector",
    "ghurur": "delusion -- the false-reality vector",
}

# The Imposition Spectrum (Paper 2, Unit III)
IMPOSITION_SPECTRUM = {
    "L1_WASWAS": "Suggestion -- unauthorized metadata whispers",
    "L2_EMOTIONAL": "Emotional pressure -- content sentiment drift",
    "L3_PHYSICAL": "Physical coercion -- binary structure tampering",
    "L4_BEHAVIORAL": "Behavioral coercion -- execution flow alteration",
    "L5_MEMORY": "Memory alteration -- hash chain breaks",
}

# ============================================================================
#  ZERO-WIDTH UNICODE STEGANOGRAPHY
# ============================================================================

ZW_ZERO = '​'      # ZERO WIDTH SPACE = bit 0
ZW_ONE = '‌'        # ZERO WIDTH NON-JOINER = bit 1
ZW_SEP = '‍'        # ZERO WIDTH JOINER = character separator
ZW_BOUNDARY = '﻿'   # BYTE ORDER MARK = message boundary

# ============================================================================
#  FILE TYPE CLASSIFICATIONS
# ============================================================================

COMMENT_STYLES = {
    '.py': ('#', None), '.js': ('//', None), '.ts': ('//', None),
    '.jsx': ('//', None), '.tsx': ('//', None), '.rs': ('//', None),
    '.go': ('//', None), '.java': ('//', None), '.c': ('//', None),
    '.cpp': ('//', None), '.h': ('//', None), '.rb': ('#', None),
    '.sh': ('#', None), '.bash': ('#', None), '.zsh': ('#', None),
    '.r': ('#', None), '.R': ('#', None), '.pl': ('#', None),
    '.lua': ('--', None), '.sql': ('--', None), '.hs': ('--', None),
    '.toml': ('#', None), '.yaml': ('#', None), '.yml': ('#', None),
    '.ini': (';', None), '.conf': ('#', None),
    '.css': ('/*', '*/'), '.html': ('<!--', '-->'),
    '.xml': ('<!--', '-->'), '.svg': ('<!--', '-->'),
    '.tex': ('%', None), '.latex': ('%', None),
    '.bat': ('REM', None), '.ps1': ('#', None),
    '.swift': ('//', None), '.kt': ('//', None), '.scala': ('//', None),
    '.m': ('%', None), '.f90': ('!', None), '.jl': ('#', None),
    '.furqan': ('//', None),
}

TEXT_EXTENSIONS = {
    '.md', '.txt', '.rst',
    '.log', '.env', '.cfg', '.properties', '.fatima',
    '.eml', '.psv',
}

SIDECAR_ONLY_EXTENSIONS = {
    '.json', '.jsonl', '.csv', '.tsv', '.lock', '.sum', '.mod',
    '.furqan_history',
}

OOXML_EXTENSIONS = {'.docx', '.xlsx', '.pptx'}

SELF_NAME = 'bismillah_encoder.py'
MANIFEST_FILENAME = "Bismillah_MANIFEST_Bismillah.json"

# ============================================================================
#  CORE ENCODING FUNCTIONS (Muhkam Surface Operations)
# ============================================================================

def text_to_zwc(message):
    """Encode a text message into zero-width characters."""
    encoded = ZW_BOUNDARY
    for char in message:
        bits = format(ord(char), '016b')
        for bit in bits:
            encoded += ZW_ONE if bit == '1' else ZW_ZERO
        encoded += ZW_SEP
    encoded += ZW_BOUNDARY
    return encoded


def zwc_to_text(encoded):
    """Decode zero-width characters back to text."""
    result = []
    content = encoded.replace(ZW_BOUNDARY, '')
    chars = content.split(ZW_SEP)
    for char_bits in chars:
        if not char_bits:
            continue
        bits = ''
        for zwc in char_bits:
            if zwc == ZW_ZERO:
                bits += '0'
            elif zwc == ZW_ONE:
                bits += '1'
        if bits and len(bits) == 16:
            result.append(chr(int(bits, 2)))
    return ''.join(result)


def extract_watermarks(content):
    """Extract any zero-width watermarks from content."""
    found = []
    parts = content.split(ZW_BOUNDARY)
    for i in range(1, len(parts), 2):
        if parts[i]:
            decoded = zwc_to_text(parts[i])
            if decoded:
                found.append(decoded)
    return found


def _nfc(data):
    """NFC-normalize text bytes so equivalent Unicode sequences hash identically."""
    try:
        text = data.decode('utf-8')
        return unicodedata.normalize('NFC', text).encode('utf-8')
    except (UnicodeDecodeError, AttributeError):
        return data


def compute_seal(content_bytes):
    """Compute Bismillah-anchored integrity seal (NFC-normalized)."""
    h = hashlib.sha256()
    h.update(BISMILLAH.encode('utf-8'))
    h.update(_nfc(content_bytes))
    h.update(BISMILLAH.encode('utf-8'))
    return h.hexdigest()


def make_comment(ext, text):
    """Create a comment string for the given file extension."""
    if ext in COMMENT_STYLES:
        prefix, suffix = COMMENT_STYLES[ext]
        if suffix:
            return "{} {} {}".format(prefix, text, suffix)
        return "{} {}".format(prefix, text)
    return text


def is_code_file(ext):
    return ext in COMMENT_STYLES


# ============================================================================
#  THE 151-LAYER COMPUTATION ENGINE
# ============================================================================
#
#  Each layer computes a distinct Bismillah-anchored hash at a specific
#  scale of the file's content. The layers are organized into 11 heavens,
#  each heaven corresponding to a scale of creation.
#
#  The computational principle: at each scale, we extract a feature from
#  the content at that granularity and seal it with Bismillah and the
#  Divine Name assigned to that layer. The result is 151 distinct integrity
#  seals that together form a complete witness across all scales of creation.


def _layer_hash(layer_idx, scale_tag, content_feature):
    """Compute a single layer's Bismillah-anchored seal.

    Every layer follows the same sealing pattern:
      SHA-256(Bismillah || layer_idx || scale_tag || Divine_Name ||
              content_feature || Bismillah)

    This is the atomic operation of the entire architecture.
    """
    name, meaning = _name_for_layer(layer_idx)
    h = hashlib.sha256()
    h.update(BISMILLAH.encode('utf-8'))
    h.update("L{:03d}|{}|{}".format(layer_idx, scale_tag, name).encode('utf-8'))
    if isinstance(content_feature, bytes):
        h.update(content_feature)
    else:
        h.update(str(content_feature).encode('utf-8'))
    h.update(BISMILLAH.encode('utf-8'))
    return {
        "layer": layer_idx,
        "name": name,
        "meaning": meaning,
        "seal": h.hexdigest(),
    }


# --- Heaven 0: SUBATOMIC (Layers 0-13) ---
# Individual bits, bytes, nibbles -- the smallest particles of data

def _compute_heaven_0(data):
    """Compute 14 subatomic-scale layers."""
    layers = []
    n = len(data)

    # L0: Single-byte frequency distribution hash
    freq = [0] * 256
    for b in data:
        freq[b] += 1
    layers.append(_layer_hash(0, "BYTE_FREQ", bytes(str(freq).encode('utf-8')[:256])))

    # L1: High-nibble (upper 4 bits) distribution
    hi_nibbles = [0] * 16
    for b in data:
        hi_nibbles[b >> 4] += 1
    layers.append(_layer_hash(1, "HI_NIBBLE", str(hi_nibbles)))

    # L2: Low-nibble (lower 4 bits) distribution
    lo_nibbles = [0] * 16
    for b in data:
        lo_nibbles[b & 0x0F] += 1
    layers.append(_layer_hash(2, "LO_NIBBLE", str(lo_nibbles)))

    # L3: Bit-level balance (ratio of 1-bits to 0-bits)
    ones = sum(bin(b).count('1') for b in data)
    zeros = n * 8 - ones
    layers.append(_layer_hash(3, "BIT_BALANCE", "{}:{}".format(ones, zeros)))

    # L4: First 11 bytes (boundary marker -- subatomic edge)
    layers.append(_layer_hash(4, "HEAD_11", data[:DIMENSIONAL_CONSTANT]))

    # L5: Last 11 bytes (boundary marker -- subatomic edge)
    tail = data[-DIMENSIONAL_CONSTANT:] if n >= DIMENSIONAL_CONSTANT else data
    layers.append(_layer_hash(5, "TAIL_11", tail))

    # L6: Every 11th byte (dimensional sampling)
    sample_11 = bytes(data[i] for i in range(0, n, DIMENSIONAL_CONSTANT))
    layers.append(_layer_hash(6, "SAMPLE_11", sample_11))

    # L7: XOR fold -- XOR all bytes into a single accumulator
    xor_acc = 0
    for b in data:
        xor_acc ^= b
    layers.append(_layer_hash(7, "XOR_FOLD", str(xor_acc)))

    # L8: Byte-value min/max/median
    if n > 0:
        sorted_bytes = sorted(data)
        bmin, bmax, bmed = sorted_bytes[0], sorted_bytes[-1], sorted_bytes[n // 2]
    else:
        bmin, bmax, bmed = 0, 0, 0
    layers.append(_layer_hash(8, "MIN_MAX_MED", "{}|{}|{}".format(bmin, bmax, bmed)))

    # L9: Byte transition count (how many times adjacent bytes differ)
    transitions = sum(1 for i in range(n - 1) if data[i] != data[i + 1])
    layers.append(_layer_hash(9, "TRANSITIONS", str(transitions)))

    # L10: Run-length encoding digest (count of maximal runs)
    runs = 1
    if n > 1:
        for i in range(1, min(n, 10000)):
            if data[i] != data[i - 1]:
                runs += 1
    layers.append(_layer_hash(10, "RUN_COUNT", str(runs)))

    # L11: Parity vector -- parity of each 11-byte block
    parities = []
    for i in range(0, n, DIMENSIONAL_CONSTANT):
        block = data[i:i + DIMENSIONAL_CONSTANT]
        p = 0
        for b in block:
            p ^= b
        parities.append(p & 1)
    layers.append(_layer_hash(11, "PARITY_VEC", str(parities[:128])))

    # L12: Byte histogram entropy (Shannon)
    entropy = 0.0
    if n > 0:
        for f in freq:
            if f > 0:
                p = f / n
                entropy -= p * math.log2(p)
    layers.append(_layer_hash(12, "ENTROPY", str(round(entropy, 8))))

    # L13: Checksum modulo 151 (the total layer count)
    cksum = sum(data) % TOTAL_LAYERS
    layers.append(_layer_hash(13, "CKSUM_151", str(cksum)))

    return layers


# --- Heaven 1: ATOMIC (Layers 14-26) ---
# Byte-pairs, bigrams, and nibble-pair patterns

def _compute_heaven_1(data):
    """Compute 13 atomic-scale layers."""
    layers = []
    n = len(data)

    # L14: Most common bigram (byte-pair)
    bigram_freq = {}
    for i in range(min(n - 1, 50000)):
        bg = (data[i], data[i + 1])
        bigram_freq[bg] = bigram_freq.get(bg, 0) + 1
    top_bg = max(bigram_freq, key=bigram_freq.get) if bigram_freq else (0, 0)
    layers.append(_layer_hash(14, "TOP_BIGRAM", "{}:{}:{}".format(
        top_bg[0], top_bg[1], bigram_freq.get(top_bg, 0))))

    # L15: Bigram entropy
    bg_total = sum(bigram_freq.values()) if bigram_freq else 1
    bg_entropy = 0.0
    for count in bigram_freq.values():
        p = count / bg_total
        if p > 0:
            bg_entropy -= p * math.log2(p)
    layers.append(_layer_hash(15, "BIGRAM_ENTROPY", str(round(bg_entropy, 6))))

    # L16: Ascending pair count (byte[i] < byte[i+1])
    asc = sum(1 for i in range(min(n - 1, 50000)) if data[i] < data[i + 1])
    layers.append(_layer_hash(16, "ASC_PAIRS", str(asc)))

    # L17: Descending pair count
    desc = sum(1 for i in range(min(n - 1, 50000)) if data[i] > data[i + 1])
    layers.append(_layer_hash(17, "DESC_PAIRS", str(desc)))

    # L18: Equal pair count
    eq = sum(1 for i in range(min(n - 1, 50000)) if data[i] == data[i + 1])
    layers.append(_layer_hash(18, "EQ_PAIRS", str(eq)))

    # L19: Nibble-pair transition matrix diagonal sum
    diag = 0
    for i in range(min(n - 1, 50000)):
        hi1, hi2 = data[i] >> 4, data[i + 1] >> 4
        if hi1 == hi2:
            diag += 1
    layers.append(_layer_hash(19, "NIBBLE_DIAG", str(diag)))

    # L20: Delta encoding digest (differences between consecutive bytes)
    deltas = []
    for i in range(min(n - 1, 1000)):
        deltas.append((data[i + 1] - data[i]) % 256)
    layers.append(_layer_hash(20, "DELTA_DIGEST", str(sum(deltas))))

    # L21: Byte-pair XOR distribution
    xor_dist = [0] * 256
    for i in range(min(n - 1, 50000)):
        xor_dist[data[i] ^ data[i + 1]] += 1
    layers.append(_layer_hash(21, "XOR_DIST", str(xor_dist[:64])))

    # L22: Palindromic byte-pair count
    palindromes = sum(1 for i in range(min(n - 2, 50000)) if data[i] == data[i + 2])
    layers.append(_layer_hash(22, "PALINDROMES", str(palindromes)))

    # L23: Byte distance from ASCII space (0x20) histogram
    space_dist = [0] * 256
    for b in data[:50000]:
        space_dist[abs(b - 0x20)] += 1
    layers.append(_layer_hash(23, "SPACE_DIST", str(space_dist[:64])))

    # L24: Even/odd byte index parity
    even_sum = sum(data[i] for i in range(0, min(n, 50000), 2))
    odd_sum = sum(data[i] for i in range(1, min(n, 50000), 2))
    layers.append(_layer_hash(24, "EVEN_ODD", "{}|{}".format(even_sum, odd_sum)))

    # L25: Trigram seed (first three bytes repeated pattern check)
    trigram_seed = data[:3] if n >= 3 else data
    layers.append(_layer_hash(25, "TRIGRAM_SEED", trigram_seed))

    # L26: Byte variance
    if n > 0:
        mean_b = sum(data) / n
        variance = sum((b - mean_b) ** 2 for b in data[:50000]) / min(n, 50000)
    else:
        variance = 0
    layers.append(_layer_hash(26, "VARIANCE", str(round(variance, 4))))

    return layers


# --- Heaven 2: MOLECULAR (Layers 27-39) ---
# Block-level structures, 4-64 byte windows

def _compute_heaven_2(data):
    """Compute 13 molecular-scale layers."""
    layers = []
    n = len(data)

    block_sizes = [4, 8, 11, 16, 32, 64]

    # L27-L32: Block frequency fingerprints at each block size
    for idx, bs in enumerate(block_sizes):
        block_count = n // bs if bs > 0 else 0
        block_hashes = []
        for bi in range(min(block_count, 256)):
            block = data[bi * bs:(bi + 1) * bs]
            block_hashes.append(hashlib.md5(block).hexdigest()[:8])
        layers.append(_layer_hash(27 + idx, "BLOCK_{}".format(bs),
                                  "|".join(block_hashes[:32])))

    # L33: Block-boundary alignment check (how many 16-byte blocks start with 0x00)
    aligned = sum(1 for i in range(0, n, 16) if i < n and data[i] == 0)
    layers.append(_layer_hash(33, "ALIGNMENT", str(aligned)))

    # L34: Rolling hash over 11-byte windows (first 256 windows)
    rolling = []
    for i in range(min(n - DIMENSIONAL_CONSTANT, 256)):
        window = data[i:i + DIMENSIONAL_CONSTANT]
        rh = sum(window[j] * (151 ** j) for j in range(len(window))) % (2 ** 32)
        rolling.append(rh)
    layers.append(_layer_hash(34, "ROLLING_11", str(rolling[:64])))

    # L35: Block entropy at 32-byte granularity
    block_entropies = []
    for i in range(0, min(n, 8192), 32):
        block = data[i:i + 32]
        if len(block) < 32:
            break
        bf = [0] * 256
        for b in block:
            bf[b] += 1
        ent = 0.0
        for f in bf:
            if f > 0:
                p = f / len(block)
                ent -= p * math.log2(p)
        block_entropies.append(round(ent, 3))
    layers.append(_layer_hash(35, "BLOCK_ENTROPY", str(block_entropies[:64])))

    # L36: Molecular bond count -- adjacent blocks with high similarity
    bonds = 0
    for i in range(0, min(n - 64, 8192), 32):
        b1 = data[i:i + 32]
        b2 = data[i + 32:i + 64]
        matching = sum(1 for a, b in zip(b1, b2) if a == b)
        if matching > 16:
            bonds += 1
    layers.append(_layer_hash(36, "BONDS", str(bonds)))

    # L37: Block checksum sequence (CRC-like rolling)
    block_crc = []
    for i in range(0, min(n, 4096), 11):
        block = data[i:i + 11]
        crc = sum(b * (i + 1) for i, b in enumerate(block)) % 65536
        block_crc.append(crc)
    layers.append(_layer_hash(37, "BLOCK_CRC", str(block_crc[:64])))

    # L38: Structural symmetry -- compare first half blocks to second half
    half = n // 2
    if half > 0:
        first_sum = sum(data[:min(half, 4096)])
        second_sum = sum(data[half:min(n, half + 4096)])
        sym_ratio = first_sum / second_sum if second_sum > 0 else 0
    else:
        sym_ratio = 0
    layers.append(_layer_hash(38, "SYMMETRY", str(round(sym_ratio, 6))))

    # L39: Molecular signature -- hash of every 151st byte
    sig = bytes(data[i] for i in range(0, n, TOTAL_LAYERS))
    layers.append(_layer_hash(39, "SIG_151", sig))

    return layers


# --- Heaven 3: CELLULAR (Layers 40-52) ---
# Paragraph and section-level patterns

def _compute_heaven_3(data):
    """Compute 13 cellular-scale layers."""
    layers = []
    n = len(data)

    # L40: Newline positions (structural skeleton)
    newlines = [i for i, b in enumerate(data) if b == 10]  # 0x0A
    layers.append(_layer_hash(40, "NEWLINES", str(newlines[:256])))

    # L41: Line length distribution
    line_lengths = []
    prev = 0
    for pos in newlines[:1000]:
        line_lengths.append(pos - prev)
        prev = pos + 1
    layers.append(_layer_hash(41, "LINE_LENS", str(line_lengths[:128])))

    # L42: Paragraph detection (double newlines)
    double_nl = sum(1 for i in range(n - 1) if data[i] == 10 and data[i + 1] == 10)
    layers.append(_layer_hash(42, "PARAGRAPHS", str(double_nl)))

    # L43: Indentation pattern (leading spaces/tabs per line)
    indent_depths = []
    line_start = True
    depth = 0
    for b in data[:50000]:
        if line_start:
            if b == 32:
                depth += 1
            elif b == 9:
                depth += 4
            else:
                indent_depths.append(depth)
                depth = 0
                line_start = False
        if b == 10:
            line_start = True
            depth = 0
    layers.append(_layer_hash(43, "INDENTATION", str(indent_depths[:128])))

    # L44: Section boundary heuristic (lines starting with # or uppercase after blank)
    section_markers = 0
    for i in range(1, min(n, 50000)):
        if data[i - 1] == 10 and i < n:
            if data[i] == 35:  # #
                section_markers += 1
            elif 65 <= data[i] <= 90 and i > 1 and data[i - 2] == 10:
                section_markers += 1
    layers.append(_layer_hash(44, "SECTIONS", str(section_markers)))

    # L45: Character class ratios (alpha, digit, space, punctuation, other)
    alpha = sum(1 for b in data if (65 <= b <= 90) or (97 <= b <= 122))
    digit = sum(1 for b in data if 48 <= b <= 57)
    space = sum(1 for b in data if b in (32, 9, 10, 13))
    punct = sum(1 for b in data if b in (33, 34, 39, 40, 41, 44, 45, 46, 58, 59, 63))
    other = n - alpha - digit - space - punct
    layers.append(_layer_hash(45, "CHAR_CLASS",
                              "a{}d{}s{}p{}o{}".format(alpha, digit, space, punct, other)))

    # L46: Word boundary count (space-to-non-space transitions)
    word_boundaries = 0
    for i in range(1, min(n, 50000)):
        if data[i - 1] in (32, 9, 10, 13) and data[i] not in (32, 9, 10, 13):
            word_boundaries += 1
    layers.append(_layer_hash(46, "WORD_BOUNDS", str(word_boundaries)))

    # L47: UTF-8 multi-byte sequence count
    multibyte = sum(1 for b in data if b >= 128)
    layers.append(_layer_hash(47, "MULTIBYTE", str(multibyte)))

    # L48: Line hash chain (each line's hash depends on previous)
    line_chain = BISMILLAH.encode('utf-8')
    chain_terminal = ""
    line_count = 0
    start = 0
    for i, b in enumerate(data):
        if b == 10 or i == n - 1:
            line = data[start:i + 1]
            lh = hashlib.sha256()
            lh.update(line_chain)
            lh.update(line)
            line_chain = lh.digest()
            chain_terminal = lh.hexdigest()
            start = i + 1
            line_count += 1
            if line_count > 10000:
                break
    layers.append(_layer_hash(48, "LINE_CHAIN", chain_terminal))

    # L49: Tab vs space ratio
    tabs = sum(1 for b in data if b == 9)
    spaces = sum(1 for b in data if b == 32)
    ratio = tabs / spaces if spaces > 0 else 0
    layers.append(_layer_hash(49, "TAB_SPACE", str(round(ratio, 6))))

    # L50: Printable ASCII ratio
    printable = sum(1 for b in data if 32 <= b <= 126)
    ratio_p = printable / n if n > 0 else 0
    layers.append(_layer_hash(50, "PRINTABLE", str(round(ratio_p, 6))))

    # L51: Longest line length
    max_line = 0
    cur_line = 0
    for b in data:
        if b == 10:
            max_line = max(max_line, cur_line)
            cur_line = 0
        else:
            cur_line += 1
    max_line = max(max_line, cur_line)
    layers.append(_layer_hash(51, "MAX_LINE", str(max_line)))

    # L52: Cellular signature -- hash of line boundary positions
    layers.append(_layer_hash(52, "CELL_SIG", str(newlines[:64])))

    return layers


# --- Heaven 4: ORGANIC (Layers 53-66) ---
# Structural flow, control markers, newline topology

def _compute_heaven_4(data):
    """Compute 14 organic-scale layers."""
    layers = []
    n = len(data)

    # L53: Control character frequency (0x00-0x1F except tab/newline/CR)
    control = sum(1 for b in data if b < 32 and b not in (9, 10, 13))
    layers.append(_layer_hash(53, "CONTROL", str(control)))

    # L54: NULL byte positions
    nulls = [i for i, b in enumerate(data) if b == 0]
    layers.append(_layer_hash(54, "NULLS", str(nulls[:128])))

    # L55: Structural marker distribution ({, }, [, ], (, ))
    markers = {}
    for b in data[:50000]:
        if b in (123, 125, 91, 93, 40, 41):
            markers[b] = markers.get(b, 0) + 1
    layers.append(_layer_hash(55, "STRUCT_MARK", str(sorted(markers.items()))))

    # L56: Brace depth profile
    depth = 0
    max_depth = 0
    depth_changes = 0
    for b in data[:50000]:
        if b == 123:  # {
            depth += 1
            max_depth = max(max_depth, depth)
            depth_changes += 1
        elif b == 125:  # }
            depth -= 1
            depth_changes += 1
    layers.append(_layer_hash(56, "BRACE_DEPTH", "{}|{}".format(max_depth, depth_changes)))

    # L57: Semicolon density (statements per 1000 bytes)
    semis = sum(1 for b in data if b == 59)
    density = semis / (n / 1000) if n > 0 else 0
    layers.append(_layer_hash(57, "SEMI_DENSITY", str(round(density, 4))))

    # L58: Comment marker heuristic (// and # at line starts)
    comment_lines = 0
    at_line_start = True
    for b in data[:50000]:
        if at_line_start and b in (35, 47):
            comment_lines += 1
            at_line_start = False
        elif b == 10:
            at_line_start = True
        elif b not in (32, 9):
            at_line_start = False
    layers.append(_layer_hash(58, "COMMENTS", str(comment_lines)))

    # L59: Blank line topology (positions of empty lines)
    blank_positions = []
    prev_nl = False
    for i, b in enumerate(data[:50000]):
        if b == 10:
            if prev_nl:
                blank_positions.append(i)
            prev_nl = True
        else:
            prev_nl = False
    layers.append(_layer_hash(59, "BLANK_TOPO", str(blank_positions[:64])))

    # L60: Function/def keyword density
    try:
        text = data.decode('utf-8', errors='replace')
        def_count = text.count('def ') + text.count('function ') + text.count('fn ')
    except Exception:
        def_count = 0
    layers.append(_layer_hash(60, "FUNC_DENSITY", str(def_count)))

    # L61: Import/include density
    try:
        text = data.decode('utf-8', errors='replace')
        imp_count = text.count('import ') + text.count('#include') + text.count('require(')
    except Exception:
        imp_count = 0
    layers.append(_layer_hash(61, "IMPORTS", str(imp_count)))

    # L62: String literal density (count of quote characters)
    quotes = sum(1 for b in data if b in (34, 39, 96))
    layers.append(_layer_hash(62, "STRINGS", str(quotes)))

    # L63: Operator density (+, -, *, /, =, <, >, !)
    ops = sum(1 for b in data if b in (43, 45, 42, 47, 61, 60, 62, 33))
    layers.append(_layer_hash(63, "OPERATORS", str(ops)))

    # L64: Return/break/continue flow markers
    try:
        text = data.decode('utf-8', errors='replace')
        flow = text.count('return') + text.count('break') + text.count('continue')
    except Exception:
        flow = 0
    layers.append(_layer_hash(64, "FLOW_MARKS", str(flow)))

    # L65: Organic signature -- structural marker positions
    marker_positions = [i for i, b in enumerate(data[:10000]) if b in (123, 125, 91, 93)]
    layers.append(_layer_hash(65, "ORG_SIG", str(marker_positions[:64])))

    # L66: Whitespace pattern hash
    ws_pattern = bytes(1 if b in (32, 9, 10, 13) else 0 for b in data[:4096])
    layers.append(_layer_hash(66, "WS_PATTERN", ws_pattern))

    return layers


# --- Heaven 5: TERRESTRIAL (Layers 67-79) ---
# Semantic fingerprinting and character-class distributions

def _compute_heaven_5(data):
    """Compute 13 terrestrial-scale layers."""
    layers = []
    n = len(data)

    # L67: ASCII lowercase frequency profile
    lower = [0] * 26
    for b in data:
        if 97 <= b <= 122:
            lower[b - 97] += 1
    layers.append(_layer_hash(67, "LOWERCASE", str(lower)))

    # L68: ASCII uppercase frequency profile
    upper = [0] * 26
    for b in data:
        if 65 <= b <= 90:
            upper[b - 65] += 1
    layers.append(_layer_hash(68, "UPPERCASE", str(upper)))

    # L69: Digit frequency profile
    digits = [0] * 10
    for b in data:
        if 48 <= b <= 57:
            digits[b - 48] += 1
    layers.append(_layer_hash(69, "DIGITS", str(digits)))

    # L70: Vowel to consonant ratio (English heuristic)
    vowels = sum(1 for b in data if b in (65, 69, 73, 79, 85, 97, 101, 105, 111, 117))
    consonants = sum(1 for b in data if (65 <= b <= 90 or 97 <= b <= 122)
                     and b not in (65, 69, 73, 79, 85, 97, 101, 105, 111, 117))
    ratio = vowels / consonants if consonants > 0 else 0
    layers.append(_layer_hash(70, "VOWEL_CONS", str(round(ratio, 6))))

    # L71: Word length distribution (first 1000 words)
    word_lens = []
    cur_len = 0
    for b in data[:50000]:
        if b in (32, 9, 10, 13):
            if cur_len > 0:
                word_lens.append(cur_len)
                cur_len = 0
                if len(word_lens) >= 1000:
                    break
        elif (65 <= b <= 90) or (97 <= b <= 122):
            cur_len += 1
        else:
            if cur_len > 0:
                word_lens.append(cur_len)
                cur_len = 0
    layers.append(_layer_hash(71, "WORD_LENS", str(word_lens[:128])))

    # L72: Sentence length heuristic (bytes between periods)
    sentence_lens = []
    cur = 0
    for b in data[:50000]:
        cur += 1
        if b == 46:  # period
            sentence_lens.append(cur)
            cur = 0
    layers.append(_layer_hash(72, "SENT_LENS", str(sentence_lens[:128])))

    # L73: Capitalization pattern (positions of uppercase after whitespace)
    cap_positions = []
    prev_ws = True
    for i, b in enumerate(data[:50000]):
        if prev_ws and 65 <= b <= 90:
            cap_positions.append(i)
        prev_ws = b in (32, 9, 10, 13)
    layers.append(_layer_hash(73, "CAP_PATTERN", str(cap_positions[:128])))

    # L74: Punctuation sequence fingerprint
    punct_seq = []
    for b in data[:50000]:
        if b in (33, 44, 46, 58, 59, 63):
            punct_seq.append(b)
    layers.append(_layer_hash(74, "PUNCT_SEQ", str(punct_seq[:256])))

    # L75: Numeric cluster detection (sequences of digits)
    num_clusters = 0
    in_num = False
    for b in data[:50000]:
        if 48 <= b <= 57:
            if not in_num:
                num_clusters += 1
                in_num = True
        else:
            in_num = False
    layers.append(_layer_hash(75, "NUM_CLUSTERS", str(num_clusters)))

    # L76: High-byte (>127) cluster analysis (non-ASCII / Arabic / Unicode)
    hi_clusters = 0
    in_hi = False
    for b in data[:50000]:
        if b >= 128:
            if not in_hi:
                hi_clusters += 1
                in_hi = True
        else:
            in_hi = False
    layers.append(_layer_hash(76, "HI_CLUSTERS", str(hi_clusters)))

    # L77: Semantic anchor words hash (Bismillah, Allah, Rahman, etc.)
    try:
        text_lower = data.decode('utf-8', errors='replace').lower()
        anchors = {
            "bismillah": text_lower.count("bismillah"),
            "allah": text_lower.count("allah"),
            "rahman": text_lower.count("rahman"),
            "rahim": text_lower.count("rahim"),
        }
    except Exception:
        anchors = {}
    layers.append(_layer_hash(77, "ANCHORS", str(sorted(anchors.items()))))

    # L78: Lexical diversity (unique bytes / total bytes)
    unique_bytes = len(set(data))
    diversity = unique_bytes / 256
    layers.append(_layer_hash(78, "DIVERSITY", str(round(diversity, 6))))

    # L79: Terrestrial signature -- character class distribution hash
    layers.append(_layer_hash(79, "TERR_SIG",
                              "a{}u{}d{}v{}c{}".format(
                                  sum(lower), sum(upper), sum(digits), vowels, consonants)))

    return layers


# --- Heaven 6: PLANETARY (Layers 80-93) ---
# Whole-section integrity and positional hashing

def _compute_heaven_6(data):
    """Compute 14 planetary-scale layers."""
    layers = []
    n = len(data)

    # L80-L90: Hash of each 1/11th of the file (11 sections)
    section_size = n // DIMENSIONAL_CONSTANT if n >= DIMENSIONAL_CONSTANT else n
    for s in range(DIMENSIONAL_CONSTANT):
        start = s * section_size
        end = start + section_size if s < DIMENSIONAL_CONSTANT - 1 else n
        section = data[start:end]
        h = hashlib.sha256(section).hexdigest()
        layers.append(_layer_hash(80 + s, "SECTION_{}".format(s), h))

    # L91: Section similarity matrix diagonal
    sections = []
    for s in range(DIMENSIONAL_CONSTANT):
        start = s * section_size
        end = start + section_size if s < DIMENSIONAL_CONSTANT - 1 else n
        sections.append(sum(data[start:end]))
    diag = sum(abs(sections[i] - sections[(i + 1) % DIMENSIONAL_CONSTANT])
               for i in range(DIMENSIONAL_CONSTANT))
    layers.append(_layer_hash(91, "SEC_DIAG", str(diag)))

    # L92: Section entropy variance
    sec_entropies = []
    for s in range(DIMENSIONAL_CONSTANT):
        start = s * section_size
        end = start + section_size if s < DIMENSIONAL_CONSTANT - 1 else n
        section = data[start:end]
        freq = [0] * 256
        for b in section:
            freq[b] += 1
        ent = 0.0
        sn = len(section)
        if sn > 0:
            for f in freq:
                if f > 0:
                    p = f / sn
                    ent -= p * math.log2(p)
        sec_entropies.append(round(ent, 4))
    layers.append(_layer_hash(92, "SEC_ENTROPY", str(sec_entropies)))

    # L93: Planetary signature -- full content hash
    layers.append(_layer_hash(93, "PLANET_SIG", hashlib.sha256(data).hexdigest()))

    return layers


# --- Heaven 7: STELLAR (Layers 94-107) ---
# Cross-section fractal relationships and Hurst watermarks

def _compute_heaven_7(data):
    """Compute 14 stellar-scale layers -- fractal analysis."""
    layers = []
    n = len(data)

    # Compute block vectors for fractal analysis
    vectors = _compute_block_vectors(data, DIMENSIONAL_CONSTANT)
    f_metrics = _fibonacci_growth_metric(vectors)

    # L94: Fibonacci growth metric series
    layers.append(_layer_hash(94, "FIB_METRICS",
                              str([round(f, 6) for f in f_metrics])))

    # L95: Hurst exponent at N=11
    h_value = _compute_hurst_value(f_metrics)
    layers.append(_layer_hash(95, "HURST_11", str(round(h_value, 8))))

    # L96: Distance from perfect persistence
    distance = abs(h_value - HURST_PERFECT)
    layers.append(_layer_hash(96, "H_DISTANCE", str(round(distance, 8))))

    # L97: Persistence classification
    if h_value > 1.0:
        p_class = "super-persistent"
    elif h_value > 0.5:
        p_class = "persistent"
    elif h_value == 0.5:
        p_class = "random"
    else:
        p_class = "anti-persistent"
    layers.append(_layer_hash(97, "PERSISTENCE", p_class))

    # L98: Cosine similarity chain (adjacent blocks)
    cos_chain = []
    for i in range(len(vectors) - 1):
        sim = _cosine_similarity(vectors[i], vectors[i + 1])
        cos_chain.append(round(sim, 6))
    layers.append(_layer_hash(98, "COS_CHAIN", str(cos_chain)))

    # L99: Mean cosine similarity
    mean_cos = sum(cos_chain) / len(cos_chain) if cos_chain else 0
    layers.append(_layer_hash(99, "MEAN_COS", str(round(mean_cos, 8))))

    # L100: Block vector magnitudes
    magnitudes = []
    for v in vectors:
        mag = math.sqrt(sum(x * x for x in v))
        magnitudes.append(round(mag, 4))
    layers.append(_layer_hash(100, "MAGNITUDES", str(magnitudes)))

    # L101: Rescaled range at multiple sub-partitions
    rs_values = []
    for k in [3, 5, 7, 9, 11]:
        sub_vectors = _compute_block_vectors(data, k)
        sub_metrics = _fibonacci_growth_metric(sub_vectors)
        rs = _rescaled_range(sub_metrics) if len(sub_metrics) >= 2 else 0
        rs_values.append(round(rs, 6))
    layers.append(_layer_hash(101, "RS_MULTI", str(rs_values)))

    # L102: Hurst spectrum (H at N=3,5,7,9,11)
    h_spectrum = []
    for k in [3, 5, 7, 9, 11]:
        sub_v = _compute_block_vectors(data, k)
        sub_m = _fibonacci_growth_metric(sub_v)
        h_k = _compute_hurst_value(sub_m)
        h_spectrum.append(round(h_k, 6))
    layers.append(_layer_hash(102, "H_SPECTRUM", str(h_spectrum)))

    # L103: Fractal dimension estimate (D = 2 - H)
    fractal_dim = 2.0 - h_value
    layers.append(_layer_hash(103, "FRACTAL_DIM", str(round(fractal_dim, 8))))

    # L104: Cross-block Fibonacci residuals
    residuals = []
    for i in range(2, len(vectors)):
        combined = _vector_add(vectors[i - 1], vectors[i - 2])
        actual_sim = _cosine_similarity(vectors[i], combined)
        residuals.append(round(1.0 - actual_sim, 8))
    layers.append(_layer_hash(104, "FIB_RESID", str(residuals)))

    # L105: Witness signature (Bismillah-anchored Hurst seal)
    witness_input = "{}|H={}|N={}|{}".format(
        BISMILLAH, h_value, DIMENSIONAL_CONSTANT, BISMILLAH)
    witness_sig = hashlib.sha256(witness_input.encode('utf-8')).hexdigest()
    layers.append(_layer_hash(105, "WITNESS_SIG", witness_sig))

    # L106: Block variance spectrum
    block_variances = []
    for v in vectors:
        mean_v = sum(v) / len(v) if v else 0
        var_v = sum((x - mean_v) ** 2 for x in v) / len(v) if v else 0
        block_variances.append(round(var_v, 8))
    layers.append(_layer_hash(106, "BLK_VARIANCE", str(block_variances)))

    # L107: Stellar signature -- Hurst + fractal dim combined
    layers.append(_layer_hash(107, "STELLAR_SIG",
                              "H={}|D={}|W={}".format(
                                  round(h_value, 6), round(fractal_dim, 6),
                                  witness_sig[:16])))

    return layers, h_value, f_metrics


# --- Heaven 8: GALACTIC (Layers 108-121) ---
# Whole-file fractal properties and adversarial chain

def _compute_heaven_8(data):
    """Compute 14 galactic-scale layers -- adversarial detection."""
    layers = []
    n = len(data)

    # Build the 11-link adversarial chain
    block_size = n // DIMENSIONAL_CONSTANT if n >= DIMENSIONAL_CONSTANT else max(n, 1)
    prev_link = BISMILLAH.encode('utf-8')
    chain_hashes = []

    # L108-L118: 11-link forward-dependent adversarial chain
    for i in range(DIMENSIONAL_CONSTANT):
        start = i * block_size
        end = start + block_size if i < DIMENSIONAL_CONSTANT - 1 else n
        block = data[start:end]

        name, _meaning = AL_ASMA_UL_HUSNA[i]
        h = hashlib.sha256()
        h.update(BISMILLAH.encode('utf-8'))
        h.update(prev_link)
        h.update(block)
        h.update(name.encode('utf-8'))
        h.update(BISMILLAH.encode('utf-8'))
        link_hash = h.hexdigest()
        chain_hashes.append(link_hash)

        layers.append(_layer_hash(108 + i, "CHAIN_{}".format(i), link_hash))
        prev_link = link_hash.encode('utf-8')

    # L119: Shahwa detector (accumulation pattern)
    shahwa_h = hashlib.sha256()
    shahwa_h.update(BISMILLAH.encode('utf-8'))
    shahwa_h.update(b"shahwa")
    shahwa_h.update(str(sum(data[:n // 3]) if n > 0 else 0).encode('utf-8'))
    shahwa_h.update(BISMILLAH.encode('utf-8'))
    layers.append(_layer_hash(119, "SHAHWA", shahwa_h.hexdigest()))

    # L120: Kibr detector (elevation pattern)
    kibr_h = hashlib.sha256()
    kibr_h.update(BISMILLAH.encode('utf-8'))
    kibr_h.update(b"kibr")
    max_b = max(data) if n > 0 else 0
    kibr_h.update(str(max_b).encode('utf-8'))
    kibr_h.update(str(sum(1 for b in data if b == max_b)).encode('utf-8'))
    kibr_h.update(BISMILLAH.encode('utf-8'))
    layers.append(_layer_hash(120, "KIBR", kibr_h.hexdigest()))

    # L121: Ghurur detector (entropy/reality distortion)
    ghurur_h = hashlib.sha256()
    ghurur_h.update(BISMILLAH.encode('utf-8'))
    ghurur_h.update(b"ghurur")
    freq = [0] * 256
    for b in data:
        freq[b] += 1
    entropy = 0.0
    if n > 0:
        for f in freq:
            if f > 0:
                p = f / n
                entropy -= p * math.log2(p)
    ghurur_h.update(str(round(entropy, 6)).encode('utf-8'))
    ghurur_h.update(BISMILLAH.encode('utf-8'))
    layers.append(_layer_hash(121, "GHURUR", ghurur_h.hexdigest()))

    return layers, chain_hashes


# --- Heaven 9: COSMIC (Layers 122-139) ---
# Inter-file relationships, directory-level, imposition spectrum

def _compute_heaven_9(data, filepath=None):
    """Compute 18 cosmic-scale layers -- imposition spectrum + directory context."""
    layers = []
    n = len(data)

    # L122: L1 WASWAS -- metadata whispers (size + boundaries)
    l1_h = hashlib.sha256()
    l1_h.update(BISMILLAH.encode('utf-8'))
    l1_h.update(b"L1_waswas")
    l1_h.update(str(n).encode('utf-8'))
    l1_h.update(data[:DIMENSIONAL_CONSTANT])
    tail = data[-DIMENSIONAL_CONSTANT:] if n >= DIMENSIONAL_CONSTANT else data
    l1_h.update(tail)
    l1_h.update(BISMILLAH.encode('utf-8'))
    layers.append(_layer_hash(122, "IMP_L1", l1_h.hexdigest()))

    # L123: L2 EMOTIONAL -- sentiment fingerprint
    l2_h = hashlib.sha256()
    l2_h.update(BISMILLAH.encode('utf-8'))
    l2_h.update(b"L2_emotional")
    alpha = sum(1 for b in data if 65 <= b <= 122)
    digits = sum(1 for b in data if 48 <= b <= 57)
    spaces = sum(1 for b in data if b in (32, 9, 10, 13))
    l2_h.update("a{}d{}s{}".format(alpha, digits, spaces).encode('utf-8'))
    l2_h.update(BISMILLAH.encode('utf-8'))
    layers.append(_layer_hash(123, "IMP_L2", l2_h.hexdigest()))

    # L124: L3 PHYSICAL -- structural sampling
    l3_h = hashlib.sha256()
    l3_h.update(BISMILLAH.encode('utf-8'))
    l3_h.update(b"L3_physical")
    structural_sample = bytes(data[i] for i in range(0, n, DIMENSIONAL_CONSTANT))
    l3_h.update(structural_sample)
    l3_h.update(BISMILLAH.encode('utf-8'))
    layers.append(_layer_hash(124, "IMP_L3", l3_h.hexdigest()))

    # L125: L4 BEHAVIORAL -- flow markers
    l4_h = hashlib.sha256()
    l4_h.update(BISMILLAH.encode('utf-8'))
    l4_h.update(b"L4_behavioral")
    newline_positions = [i for i, b in enumerate(data) if b == 10]
    l4_h.update(json.dumps(newline_positions[:99]).encode('utf-8'))
    l4_h.update(BISMILLAH.encode('utf-8'))
    layers.append(_layer_hash(125, "IMP_L4", l4_h.hexdigest()))

    # L126: L5 MEMORY -- deep content hash
    l5_h = hashlib.sha256()
    l5_h.update(BISMILLAH.encode('utf-8'))
    l5_h.update(b"L5_memory")
    l5_h.update(_nfc(data))
    l5_h.update(BISMILLAH.encode('utf-8'))
    layers.append(_layer_hash(126, "IMP_L5", l5_h.hexdigest()))

    # L127: File size encoded with divine moduli
    size_mod_99 = n % 99
    size_mod_11 = n % 11
    size_mod_151 = n % 151
    layers.append(_layer_hash(127, "SIZE_MODS",
                              "{}|{}|{}".format(size_mod_99, size_mod_11, size_mod_151)))

    # L128: Filename seal (if available)
    fname = os.path.basename(filepath) if filepath else "unknown"
    layers.append(_layer_hash(128, "FNAME_SEAL", fname))

    # L129: File extension seal
    ext = os.path.splitext(filepath)[1] if filepath else ""
    layers.append(_layer_hash(129, "EXT_SEAL", ext))

    # L130: Parent directory seal
    parent = os.path.basename(os.path.dirname(filepath)) if filepath else ""
    layers.append(_layer_hash(130, "PARENT_SEAL", parent))

    # L131: Full path hash (position in creation hierarchy)
    layers.append(_layer_hash(131, "PATH_SEAL", filepath or ""))

    # L132: Content + filename combined seal (identity binding)
    id_h = hashlib.sha256()
    id_h.update(BISMILLAH.encode('utf-8'))
    id_h.update(fname.encode('utf-8'))
    id_h.update(data[:1024])
    id_h.update(BISMILLAH.encode('utf-8'))
    layers.append(_layer_hash(132, "IDENTITY", id_h.hexdigest()))

    # L133: Temporal seal (file content independent of metadata)
    # Uses content to derive a deterministic "creation moment"
    temporal = hashlib.sha256()
    temporal.update(BISMILLAH.encode('utf-8'))
    temporal.update(b"temporal")
    temporal.update(data[:256])
    temporal.update(data[-256:] if n >= 256 else data)
    temporal.update(BISMILLAH.encode('utf-8'))
    layers.append(_layer_hash(133, "TEMPORAL", temporal.hexdigest()))

    # L134: Quadrant analysis (4 quarters of file)
    q_size = n // 4 if n >= 4 else max(n, 1)
    quadrants = []
    for q in range(4):
        start = q * q_size
        end = start + q_size if q < 3 else n
        quadrants.append(hashlib.sha256(data[start:end]).hexdigest()[:16])
    layers.append(_layer_hash(134, "QUADRANTS", "|".join(quadrants)))

    # L135: Inter-quadrant similarity
    q_sums = []
    for q in range(4):
        start = q * q_size
        end = start + q_size if q < 3 else n
        q_sums.append(sum(data[start:end]))
    q_diffs = [abs(q_sums[i] - q_sums[(i + 1) % 4]) for i in range(4)]
    layers.append(_layer_hash(135, "Q_SIMILARITY", str(q_diffs)))

    # L136: Content provenance chain (first 11 SHA rounds)
    prov = data
    prov_chain = []
    for _ in range(DIMENSIONAL_CONSTANT):
        ph = hashlib.sha256(prov[:1024]).hexdigest()
        prov_chain.append(ph[:8])
        prov = ph.encode('utf-8')
    layers.append(_layer_hash(136, "PROVENANCE", "|".join(prov_chain)))

    # L137: Cosmic frequency (byte value 151 count, 99 count, 11 count)
    freq_151 = sum(1 for b in data if b == 151 % 256)
    freq_99 = sum(1 for b in data if b == 99)
    freq_11 = sum(1 for b in data if b == 11)
    layers.append(_layer_hash(137, "COSMIC_FREQ",
                              "{}|{}|{}".format(freq_151, freq_99, freq_11)))

    # L138: Galactic hash (entire file in one operation)
    gal_h = hashlib.sha256()
    gal_h.update(BISMILLAH.encode('utf-8'))
    gal_h.update(b"galactic")
    gal_h.update(data)
    gal_h.update(BISMILLAH.encode('utf-8'))
    layers.append(_layer_hash(138, "GALACTIC", gal_h.hexdigest()))

    # L139: Cosmic signature -- all imposition levels combined
    cosmic_h = hashlib.sha256()
    cosmic_h.update(BISMILLAH.encode('utf-8'))
    cosmic_h.update(l1_h.hexdigest().encode('utf-8'))
    cosmic_h.update(l2_h.hexdigest().encode('utf-8'))
    cosmic_h.update(l3_h.hexdigest().encode('utf-8'))
    cosmic_h.update(l4_h.hexdigest().encode('utf-8'))
    cosmic_h.update(l5_h.hexdigest().encode('utf-8'))
    cosmic_h.update(BISMILLAH.encode('utf-8'))
    layers.append(_layer_hash(139, "COSMIC_SIG", cosmic_h.hexdigest()))

    return layers


# --- Heaven 10: SIDRAT AL-MUNTAHA (Layers 140-150) ---
# The Lote Tree of the Utmost Boundary -- Divine Witness
# 11 layers, one witness per heaven

def _compute_heaven_10(all_heaven_layers):
    """Compute 11 divine witness layers -- one per heaven.

    Each witness layer seals the entire heaven it watches over.
    The final layer (150) seals all previous witnesses, creating
    a self-referential testimony -- the point beyond which no
    creation passes.

    "Near it is the Garden of Refuge -- when there covered the
    Lote Tree that which covered it." (53:15-16)
    """
    layers = []

    # L140-L149: One witness per heaven (0-9)
    for heaven_idx in range(DIMENSIONAL_CONSTANT - 1):
        heaven = HEAVENS[heaven_idx]
        # Collect all seals from this heaven
        heaven_seals = []
        for layer in all_heaven_layers:
            if heaven["layer_start"] <= layer["layer"] <= heaven["layer_end"]:
                heaven_seals.append(layer["seal"])

        # Compute heaven witness
        hw = hashlib.sha256()
        hw.update(BISMILLAH.encode('utf-8'))
        hw.update("HEAVEN_{}_WITNESS".format(heaven_idx).encode('utf-8'))
        hw.update(heaven["guardian"].encode('utf-8'))
        for seal in heaven_seals:
            hw.update(seal.encode('utf-8'))
        hw.update(BISMILLAH.encode('utf-8'))

        layers.append(_layer_hash(140 + heaven_idx,
                                  "WITNESS_H{}".format(heaven_idx),
                                  hw.hexdigest()))

    # L150: MASTER WITNESS -- seals all 10 heaven witnesses
    # This is Sidrat al-Muntaha -- the utmost boundary
    master_h = hashlib.sha256()
    master_h.update(BISMILLAH.encode('utf-8'))
    master_h.update(b"SIDRAT_AL_MUNTAHA")
    for witness_layer in layers:
        master_h.update(witness_layer["seal"].encode('utf-8'))
    master_h.update(BISMILLAH.encode('utf-8'))

    layers.append(_layer_hash(150, "MASTER_WITNESS", master_h.hexdigest()))

    return layers


# ============================================================================
#  FRACTAL ANALYSIS HELPERS (used by Heaven 7)
# ============================================================================

def _compute_block_vectors(content_bytes, block_count):
    """Partition content into N blocks and compute frequency histogram vectors."""
    data = content_bytes
    if len(data) < block_count:
        data = data + b'\x00' * (block_count - len(data))

    block_size = len(data) // block_count
    vectors = []

    for i in range(block_count):
        start = i * block_size
        end = start + block_size if i < block_count - 1 else len(data)
        block = data[start:end]

        hist = [0.0] * 256
        for byte_val in block:
            hist[byte_val] += 1.0

        magnitude = math.sqrt(sum(v * v for v in hist))
        if magnitude > 0:
            hist = [v / magnitude for v in hist]

        vectors.append(hist)

    return vectors


def _cosine_similarity(v1, v2):
    dot = sum(a * b for a, b in zip(v1, v2))
    mag1 = math.sqrt(sum(a * a for a in v1))
    mag2 = math.sqrt(sum(b * b for b in v2))
    if mag1 == 0 or mag2 == 0:
        return 0.0
    return dot / (mag1 * mag2)


def _vector_add(v1, v2):
    return [a + b for a, b in zip(v1, v2)]


def _fibonacci_growth_metric(vectors):
    metrics = []
    for n in range(2, len(vectors)):
        combined = _vector_add(vectors[n - 1], vectors[n - 2])
        sim = _cosine_similarity(vectors[n], combined)
        metrics.append(sim)
    return metrics


def _rescaled_range(series):
    n = len(series)
    if n < 2:
        return 0.0
    mean = sum(series) / n
    deviations = [x - mean for x in series]
    cumulative = []
    running = 0.0
    for d in deviations:
        running += d
        cumulative.append(running)
    r = max(cumulative) - min(cumulative)
    variance = sum(d * d for d in deviations) / n
    s = math.sqrt(variance) if variance > 0 else 1e-10
    return r / s


def _compute_hurst_value(f_metrics):
    if len(f_metrics) < 3:
        return 0.5
    rs = _rescaled_range(f_metrics)
    n = len(f_metrics)
    if rs > 0 and n > 1:
        return math.log(rs) / math.log(n)
    return 0.5


# ============================================================================
#  MASTER COMPUTATION -- All 151 Layers Across 11 Heavens
# ============================================================================

def compute_all_151_layers(content_bytes, filepath=None):
    """Compute all 151 protection layers across 11 heavens.

    Returns:
      - layers: list of 151 layer dicts (layer, name, meaning, seal)
      - heavens: list of 11 heaven summary dicts
      - master_witness: the single hash at Sidrat al-Muntaha (Layer 150)
      - hurst_11: the Hurst exponent at N=11
    """
    all_layers = []

    # Heavens 0-6: scale-based analysis
    all_layers.extend(_compute_heaven_0(content_bytes))      # 0-13
    all_layers.extend(_compute_heaven_1(content_bytes))      # 14-26
    all_layers.extend(_compute_heaven_2(content_bytes))      # 27-39
    all_layers.extend(_compute_heaven_3(content_bytes))      # 40-52
    all_layers.extend(_compute_heaven_4(content_bytes))      # 53-66
    all_layers.extend(_compute_heaven_5(content_bytes))      # 67-79
    all_layers.extend(_compute_heaven_6(content_bytes))      # 80-93

    # Heaven 7: fractal analysis (returns extra data)
    h7_layers, hurst_11, f_metrics = _compute_heaven_7(content_bytes)
    all_layers.extend(h7_layers)                             # 94-107

    # Heaven 8: adversarial chain
    h8_layers, chain_hashes = _compute_heaven_8(content_bytes)
    all_layers.extend(h8_layers)                             # 108-121

    # Heaven 9: cosmic / imposition
    all_layers.extend(_compute_heaven_9(content_bytes, filepath))  # 122-139

    # Heaven 10: divine witness (depends on all previous)
    h10_layers = _compute_heaven_10(all_layers)
    all_layers.extend(h10_layers)                            # 140-150

    # Build heaven summaries
    heavens_summary = []
    for hdef in HEAVENS:
        heaven_layers = [l for l in all_layers
                         if hdef["layer_start"] <= l["layer"] <= hdef["layer_end"]]
        heaven_h = hashlib.sha256()
        heaven_h.update(BISMILLAH.encode('utf-8'))
        for l in heaven_layers:
            heaven_h.update(l["seal"].encode('utf-8'))
        heaven_h.update(BISMILLAH.encode('utf-8'))

        heavens_summary.append({
            "heaven": hdef["heaven"],
            "name_ar": hdef["name_ar"],
            "name_en": hdef["name_en"],
            "scale": hdef["scale"],
            "guardian": hdef["guardian"],
            "layer_count": len(heaven_layers),
            "heaven_seal": heaven_h.hexdigest(),
        })

    master_witness = all_layers[-1]["seal"]  # Layer 150

    return {
        "layers": all_layers,
        "heavens": heavens_summary,
        "master_witness": master_witness,
        "hurst_11": hurst_11,
        "total_layers": len(all_layers),
        "total_heavens": TOTAL_HEAVENS,
    }


# ============================================================================
#  TEXT/CODE FILE SEALING (Surface + Deep)
# ============================================================================

def _has_zwc_payload(content):
    return ZW_BOUNDARY in content


def seal_text_content(content, ext):
    """Apply Bismillah seal to text content (idempotent)."""
    lines = content.split('\n')

    bismillah_line = make_comment(ext, BISMILLAH) if ext in COMMENT_STYLES else BISMILLAH

    has_start = any(
        'bismillah' in line.lower().replace('-', '')
        for line in lines[:3] if line.strip()
    )
    if not has_start:
        lines.insert(0, bismillah_line)

    non_empty_tail = [l for l in lines[-3:] if l.strip()]
    has_end = any(
        'bismillah' in line.lower().replace('-', '')
        for line in non_empty_tail
    )
    if not has_end:
        if lines and lines[-1].strip():
            lines.append('')
        lines.append(bismillah_line)

    if not is_code_file(ext) and not _has_zwc_payload(content):
        zwc_bismillah = text_to_zwc(BISMILLAH_ARABIC)
        for i, line in enumerate(lines):
            stripped = line.strip()
            if (stripped
                    and 'bismillah' not in stripped.lower().replace('-', '')
                    and len(stripped) > 10):
                words = line.split(' ', 1)
                if len(words) >= 2:
                    lines[i] = words[0] + zwc_bismillah + ' ' + words[1]
                break

    return '\n'.join(lines)


def embed_99_names_text(content):
    """Embed all 99 Names as zero-width watermarks throughout text content."""
    lines = content.split('\n')
    name_idx = 0
    for i, line in enumerate(lines):
        stripped = line.strip()
        if not stripped or len(stripped) < 5:
            continue
        if name_idx < len(AL_ASMA_UL_HUSNA):
            transliteration, _meaning = AL_ASMA_UL_HUSNA[name_idx]
            watermark = text_to_zwc(transliteration)
            if len(line) > 1:
                lines[i] = line[0] + watermark + line[1:]
                name_idx += 1
        if name_idx >= len(AL_ASMA_UL_HUSNA):
            name_idx = 0
    return '\n'.join(lines)


def embed_99_names_code(content, ext):
    """Embed the 99 Names as comments in code files (idempotent)."""
    if 'Al-Asma ul-Husna' in content:
        return content
    lines = content.split('\n')
    result = []
    found_opening = False
    for i, line in enumerate(lines):
        result.append(line)
        if not found_opening and 'bismillah' in line.lower().replace('-', ''):
            found_opening = True
            result.append(make_comment(ext, ""))
            result.append(make_comment(ext, "Al-Asma ul-Husna -- The 99 Beautiful Names of Allah"))
            for trans, meaning in AL_ASMA_UL_HUSNA:
                result.append(make_comment(ext, "  {} -- {}".format(trans, meaning)))
            result.append(make_comment(ext, ""))
    return '\n'.join(result)


def seal_text_file(filepath, embed_names=False):
    """Apply the full 151-layer Bismillah seal to a text/code file."""
    result = {"file": filepath, "layers": [], "heavens_sealed": 0}
    p = Path(filepath)
    ext = p.suffix.lower()

    if p.name == SELF_NAME:
        result["skipped"] = "self"
        return result

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        sealed = seal_text_content(content, ext)
        result["layers"].append("SURFACE_VISIBLE")

        if is_code_file(ext):
            if embed_names:
                sealed = embed_99_names_code(sealed, ext)
                result["layers"].append("SURFACE_99_NAMES")
        else:
            result["layers"].append("SURFACE_STEGO")
            if embed_names:
                sealed = embed_99_names_text(sealed)
                result["layers"].append("SURFACE_99_NAMES_ZWC")

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(sealed)

        # Compute all 151 layers
        content_bytes = sealed.encode('utf-8')
        computation = compute_all_151_layers(content_bytes, filepath)
        _write_heaven_witness(filepath, content_bytes, computation)
        result["heavens_sealed"] = TOTAL_HEAVENS
        result["layers_computed"] = computation["total_layers"]

    except (UnicodeDecodeError, ValueError):
        result["skipped"] = "binary_content"

    return result


# ============================================================================
#  BINARY FILE SEALING
# ============================================================================

def seal_ooxml(filepath):
    """Inject Bismillah into OOXML metadata."""
    try:
        if not zipfile.is_zipfile(filepath):
            return False, "Not a valid ZIP/OOXML"
        tmpfd, tmppath = tempfile.mkstemp(suffix=os.path.splitext(filepath)[1])
        os.close(tmpfd)
        with zipfile.ZipFile(filepath, 'r') as zin:
            with zipfile.ZipFile(tmppath, 'w', zipfile.ZIP_DEFLATED) as zout:
                bismillah_added = False
                for item in zin.infolist():
                    data = zin.read(item.filename)
                    if item.filename == 'docProps/core.xml':
                        content = data.decode('utf-8', errors='replace')
                        if BISMILLAH not in content:
                            if '<dc:description>' in content:
                                content = content.replace(
                                    '<dc:description>',
                                    '<dc:description>{} -- '.format(BISMILLAH))
                            elif '</cp:coreProperties>' in content:
                                content = content.replace(
                                    '</cp:coreProperties>',
                                    '  <dc:description>{}</dc:description>\n</cp:coreProperties>'.format(BISMILLAH))
                            data = content.encode('utf-8')
                            bismillah_added = True
                        else:
                            bismillah_added = True
                    zout.writestr(item, data)
                if not bismillah_added:
                    core_xml = '<?xml version="1.0" encoding="UTF-8"?>\n<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/"><dc:description>{}</dc:description></cp:coreProperties>'.format(BISMILLAH)
                    zout.writestr('docProps/core.xml', core_xml)
        shutil.move(tmppath, filepath)
        return True, "OOXML sealed"
    except Exception as e:
        if 'tmppath' in locals() and os.path.exists(tmppath):
            os.unlink(tmppath)
        return False, str(e)


def seal_pdf(filepath):
    """Inject Bismillah into PDF metadata."""
    try:
        from pypdf import PdfReader, PdfWriter
        reader = PdfReader(filepath)
        writer = PdfWriter()
        for page in reader.pages:
            writer.add_page(page)
        meta = reader.metadata or {}
        existing_author = meta.get('/Author', '') or ''
        if BISMILLAH in existing_author:
            return True, "Already sealed"
        writer.add_metadata({
            '/Author': BISMILLAH,
            '/Subject': BISMILLAH,
            '/Keywords': BISMILLAH,
        })
        tmpfd, tmppath = tempfile.mkstemp(suffix='.pdf')
        os.close(tmpfd)
        with open(tmppath, 'wb') as f:
            writer.write(f)
        shutil.move(tmppath, filepath)
        return True, "PDF sealed"
    except ImportError:
        return False, "pypdf not installed"
    except Exception as e:
        return False, str(e)


def seal_png(filepath):
    """Inject Bismillah into PNG text chunk."""
    try:
        from PIL import Image
        from PIL.PngImagePlugin import PngInfo
        img = Image.open(filepath)
        pnginfo = PngInfo()
        if hasattr(img, 'text'):
            for k, v in img.text.items():
                if k != 'Bismillah':
                    pnginfo.add_text(k, v)
        pnginfo.add_text('Bismillah', BISMILLAH)
        tmpfd, tmppath = tempfile.mkstemp(suffix='.png')
        os.close(tmpfd)
        img.save(tmppath, pnginfo=pnginfo)
        shutil.move(tmppath, filepath)
        return True, "PNG sealed"
    except ImportError:
        return False, "Pillow not installed"
    except Exception as e:
        return False, str(e)


def seal_jpg(filepath):
    try:
        from PIL import Image
        img = Image.open(filepath)
        exif = img.getexif()
        exif[0x010e] = BISMILLAH
        tmpfd, tmppath = tempfile.mkstemp(suffix='.jpg')
        os.close(tmpfd)
        img.save(tmppath, exif=exif.tobytes())
        shutil.move(tmppath, filepath)
        return True, "JPEG sealed"
    except ImportError:
        return False, "Pillow not installed"
    except Exception as e:
        return False, str(e)


def seal_mp3(filepath):
    try:
        import mutagen
        from mutagen.id3 import ID3, COMM
        try:
            tags = ID3(filepath)
        except mutagen.id3.ID3NoHeaderError:
            tags = ID3()
        tags.add(COMM(encoding=3, lang='eng', desc='Bismillah', text=BISMILLAH))
        tags.save(filepath)
        return True, "MP3 sealed"
    except ImportError:
        return False, "mutagen not installed"
    except Exception as e:
        return False, str(e)


def seal_flac(filepath):
    try:
        from mutagen.flac import FLAC
        audio = FLAC(filepath)
        audio['COMMENT'] = BISMILLAH
        audio.save()
        return True, "FLAC sealed"
    except ImportError:
        return False, "mutagen not installed"
    except Exception as e:
        return False, str(e)


def seal_zip(filepath):
    try:
        if not zipfile.is_zipfile(filepath):
            return False, "Not a valid ZIP"
        with zipfile.ZipFile(filepath, 'a') as zf:
            if 'Bismillah.txt' not in zf.namelist():
                zf.writestr('Bismillah.txt',
                    '{b}\nThis archive is sealed.\n{b}\n'.format(b=BISMILLAH))
        return True, "ZIP sealed"
    except Exception as e:
        return False, str(e)


def create_sidecar(filepath):
    """Create companion .bismillah sidecar file."""
    try:
        sidecar = filepath + '.bismillah'
        if os.path.exists(sidecar):
            return True, "Sidecar exists"
        sha256 = hashlib.sha256()
        with open(filepath, 'rb') as f:
            file_bytes = f.read()
            sha256.update(file_bytes)
        seal_hash = compute_seal(file_bytes)
        content = "{b}\nDivine Protection for: {name}\nSHA-256: {sha}\nSeal: {seal}\n{b}\n".format(
            b=BISMILLAH, name=os.path.basename(filepath),
            sha=sha256.hexdigest(), seal=seal_hash)
        with open(sidecar, 'w', encoding='utf-8') as f:
            f.write(content)
        return True, "Sidecar created"
    except Exception as e:
        return False, str(e)


BINARY_HANDLERS = {
    '.docx': seal_ooxml, '.xlsx': seal_ooxml, '.pptx': seal_ooxml,
    '.pdf': seal_pdf,
    '.png': seal_png,
    '.jpg': seal_jpg, '.jpeg': seal_jpg,
    '.mp3': seal_mp3, '.flac': seal_flac,
    '.zip': seal_zip,
    '.wav': create_sidecar, '.mp4': create_sidecar, '.mkv': create_sidecar,
    '.ttf': create_sidecar, '.otf': create_sidecar, '.woff': create_sidecar,
    '.gif': create_sidecar, '.bmp': create_sidecar, '.ico': create_sidecar,
    '.exe': create_sidecar, '.dll': create_sidecar, '.so': create_sidecar,
}


def seal_binary_file(filepath):
    """Seal a binary file + compute 151 layers."""
    ext = os.path.splitext(filepath)[1].lower()
    handler = BINARY_HANDLERS.get(ext, create_sidecar)
    success, msg = handler(filepath)
    if not success:
        success, msg = create_sidecar(filepath)

    if success:
        try:
            with open(filepath, 'rb') as f:
                content_bytes = f.read()
            computation = compute_all_151_layers(content_bytes, filepath)
            _write_heaven_witness(filepath, content_bytes, computation)
        except Exception:
            pass

    return success, msg


# ============================================================================
#  HEAVEN WITNESS SIDECAR -- Stores All 151 Layer Seals
# ============================================================================

def _write_heaven_witness(filepath, content_bytes, computation):
    """Write the 11-heaven, 151-layer witness to .witness.bismillah sidecar."""
    witness_path = filepath + '.witness.bismillah'

    witness_data = OrderedDict([
        (BISMILLAH, True),
        ("encoder_version", ENCODER_VERSION),
        ("architecture", "11-Heaven, 151-Layer FATIMA v4.0"),
        ("total_heavens", computation["total_heavens"]),
        ("total_layers", computation["total_layers"]),
        ("dimensional_constant", DIMENSIONAL_CONSTANT),
        ("file", os.path.basename(filepath)),
        ("file_size", len(content_bytes)),
        ("muhkam_seal", compute_seal(content_bytes)),
        ("hurst_11", computation["hurst_11"]),
        ("master_witness", computation["master_witness"]),
        ("heavens", []),
        ("quranic_grounding", OrderedDict([
            ("al_hijr_15_9", "Indeed, it is We who sent down the Reminder, "
                             "and indeed, We will be its Guardian."),
            ("yusuf_12_4", "I have seen eleven stars and the sun and the moon; "
                           "I saw them prostrating to me."),
            ("fussilat_41_42", "Falsehood cannot approach it from before it or "
                               "from behind it; a revelation from One who is "
                               "Wise and Praiseworthy."),
            ("an_najm_53_14", "Near the Lote Tree of the Utmost Boundary."),
            ("al_mulk_67_3", "He who created seven heavens in layers."),
            ("nuh_71_15", "Do you not see how Allah created seven heavens in layers?"),
            ("al_mu'minun_23_17", "And We have created above you seven pathways, "
                                  "and We are never unmindful of creation."),
        ])),
    ])

    # Add per-heaven summaries with layer seals
    for h_summary in computation["heavens"]:
        h_idx = h_summary["heaven"]
        h_def = HEAVENS[h_idx]
        heaven_entry = OrderedDict([
            ("heaven", h_idx),
            ("name_ar", h_def["name_ar"]),
            ("name_en", h_def["name_en"]),
            ("scale", h_def["scale"]),
            ("guardian", h_def["guardian"]),
            ("guardian_meaning", h_def["guardian_meaning"]),
            ("layer_range", "{}-{}".format(h_def["layer_start"], h_def["layer_end"])),
            ("layer_count", h_summary["layer_count"]),
            ("heaven_seal", h_summary["heaven_seal"]),
            ("layer_seals", []),
        ])

        for layer in computation["layers"]:
            if h_def["layer_start"] <= layer["layer"] <= h_def["layer_end"]:
                heaven_entry["layer_seals"].append(OrderedDict([
                    ("layer", layer["layer"]),
                    ("name", layer["name"]),
                    ("seal", layer["seal"]),
                ]))

        witness_data["heavens"].append(heaven_entry)

    try:
        with open(witness_path, 'w', encoding='utf-8') as f:
            json.dump(witness_data, f, indent=2, ensure_ascii=False)
    except Exception:
        pass


# ============================================================================
#  MAIN OPERATIONS
# ============================================================================

def is_text_file(ext):
    return ext in COMMENT_STYLES or ext in TEXT_EXTENSIONS


def seal_directory(directory, embed_names=False, dry_run=False):
    """Apply 151-layer Bismillah protection across 11 heavens."""
    text_sealed = 0
    binary_sealed = 0
    sidecar_count = 0
    failed = 0
    skipped = 0
    mode_label = "DRY RUN" if dry_run else "Beginning 11-Heaven, 151-Layer Divine Seal"

    print("\n  {} -- {}".format(BISMILLAH, mode_label))
    print("  Architecture: {} heavens, {} layers".format(TOTAL_HEAVENS, TOTAL_LAYERS))
    print("  H(11) = {} | H_inter(11) = {}\n".format(HURST_HARMONIC, HURST_PARTITIONED))

    for dirpath, dirnames, filenames in os.walk(directory):
        if '.git' in dirpath:
            continue
        dirnames[:] = [d for d in dirnames if d != '.git' and d != '__pycache__']

        for fname in sorted(filenames):
            filepath = os.path.join(dirpath, fname)
            rel = os.path.relpath(filepath, directory)
            ext = Path(fname).suffix.lower()

            if fname == SELF_NAME or fname.endswith('.bismillah'):
                skipped += 1
                continue

            if ext in SIDECAR_ONLY_EXTENSIONS:
                if dry_run:
                    sidecar_path = filepath + '.bismillah'
                    if os.path.exists(sidecar_path):
                        skipped += 1
                    else:
                        binary_sealed += 1
                        sidecar_count += 1
                        print("  WOULD SEAL: {} [151 layers]".format(rel))
                else:
                    success, msg = create_sidecar(filepath)
                    if success:
                        try:
                            with open(filepath, 'rb') as f:
                                content_bytes = f.read()
                            computation = compute_all_151_layers(content_bytes, filepath)
                            _write_heaven_witness(filepath, content_bytes, computation)
                        except Exception:
                            pass
                        binary_sealed += 1
                        sidecar_count += 1
                        print("  SIDECAR: {} -- {} [151 layers]".format(rel, msg))
                    else:
                        failed += 1
                        print("  FAILED:  {} -- {}".format(rel, msg))
                continue

            if is_text_file(ext):
                if dry_run:
                    text_sealed += 1
                    print("  WOULD SEAL: {} [151 layers across 11 heavens]".format(rel))
                else:
                    result = seal_text_file(filepath, embed_names=embed_names)
                    if result.get("skipped"):
                        skipped += 1
                    else:
                        text_sealed += 1
                        print("  TEXT:   {} [{} layers, {} heavens]".format(
                            rel, result.get("layers_computed", 0),
                            result.get("heavens_sealed", 0)))
                continue

            try:
                with open(filepath, 'rb') as f:
                    head = f.read(2000)
                if b'ismillah' in head or b'ISMILLAH' in head:
                    skipped += 1
                    continue
            except Exception:
                pass

            if dry_run:
                binary_sealed += 1
                print("  WOULD SEAL: {} [151 layers]".format(rel))
            else:
                success, msg = seal_binary_file(filepath)
                if success:
                    binary_sealed += 1
                    if 'idecar' in msg.lower():
                        sidecar_count += 1
                    print("  BINARY: {} -- {} [151 layers]".format(rel, msg))
                else:
                    failed += 1
                    print("  FAILED: {} -- {}".format(rel, msg))

    total = text_sealed + binary_sealed + skipped
    protected = text_sealed + binary_sealed

    print("\n  {}".format("=" * 60))
    print("  {} -- 11-Heaven Seal Complete".format(BISMILLAH))
    print("  {}".format("=" * 60))
    print("  Architecture:      {} heavens, {} layers".format(TOTAL_HEAVENS, TOTAL_LAYERS))
    print("  Text/code sealed:  {}".format(text_sealed))
    print("  Binary sealed:     {} (metadata: {}, sidecar: {})".format(
        binary_sealed, binary_sealed - sidecar_count, sidecar_count))
    print("  Already protected: {}".format(skipped))
    print("  Failed:            {}".format(failed))
    print("  Total files:       {}".format(total + failed))
    if total + failed > 0:
        pct = protected / (total + failed) * 100
        print("  New seals applied: {:.1f}%".format(pct))
    print("  {}".format("=" * 60))

    return {"text": text_sealed, "binary": binary_sealed, "failed": failed}


def verify_directory(directory, strict=False):
    """Verify 151-layer Bismillah protection across all files."""
    ZWC_BYTES = [b'\xe2\x80\x8b', b'\xe2\x80\x8c', b'\xe2\x80\x8d', b'\xef\xbb\xbf']
    total = 0
    protected = 0
    unprotected = []
    witness_verified = 0

    for dirpath, dirnames, filenames in os.walk(directory):
        if '.git' in dirpath:
            continue
        dirnames[:] = [d for d in dirnames if d != '.git']

        for fname in filenames:
            fp = os.path.join(dirpath, fname)
            total += 1
            ext = os.path.splitext(fname)[1].lower()

            if fname.endswith('.bismillah'):
                protected += 1
                continue

            if os.path.exists(fp + '.bismillah'):
                protected += 1
                if os.path.exists(fp + '.witness.bismillah'):
                    witness_verified += 1
                continue

            if is_text_file(ext) or ext == '' or ext == '.gitignore':
                try:
                    with open(fp, 'rb') as f:
                        data = f.read(4000)
                    for zwc in ZWC_BYTES:
                        data = data.replace(zwc, b'')
                    if b'ismillah' in data or b'ISMILLAH' in data:
                        protected += 1
                        if os.path.exists(fp + '.witness.bismillah'):
                            witness_verified += 1
                        continue
                except Exception:
                    pass

            if ext in OOXML_EXTENSIONS:
                try:
                    if zipfile.is_zipfile(fp):
                        with zipfile.ZipFile(fp, 'r') as z:
                            for entry in z.namelist():
                                if 'core.xml' in entry or 'Bismillah' in entry:
                                    content = z.read(entry).decode('utf-8', errors='replace')
                                    if 'ismillah' in content.lower():
                                        protected += 1
                                        break
                            else:
                                unprotected.append(os.path.relpath(fp, directory))
                            continue
                except Exception:
                    pass

            if ext == '.zip':
                try:
                    if zipfile.is_zipfile(fp):
                        with zipfile.ZipFile(fp, 'r') as z:
                            if 'Bismillah.txt' in z.namelist():
                                protected += 1
                                continue
                except Exception:
                    pass

            try:
                with open(fp, 'rb') as f:
                    data = f.read(8000)
                if b'ismillah' in data or b'Bismillah' in data:
                    protected += 1
                    continue
            except Exception:
                pass

            unprotected.append(os.path.relpath(fp, directory))

    pct = (protected / total * 100) if total > 0 else 0

    print("\n  {} -- 11-Heaven Verification Report".format(BISMILLAH))
    print("  {}".format("=" * 60))
    print("  Architecture:        {} heavens, {} layers".format(TOTAL_HEAVENS, TOTAL_LAYERS))
    print("  Total files:         {}".format(total))
    print("  Protected:           {}".format(protected))
    print("  Witness sidecars:    {}".format(witness_verified))
    print("  Unprotected:         {}".format(len(unprotected)))
    print("  Protection:          {:.4f}%".format(pct))

    if unprotected:
        print("\n  UNPROTECTED FILES:")
        for f in unprotected:
            print("    {}".format(f))

    tampered = []
    if strict:
        manifest_path = os.path.join(directory, MANIFEST_FILENAME)
        if os.path.exists(manifest_path):
            with open(manifest_path, 'r', encoding='utf-8') as f:
                manifest = json.load(f)
            manifest_files = manifest.get("files", {})
            print("\n  STRICT HASH VERIFICATION:")
            for rel_path, entry in manifest_files.items():
                expected = entry.get("sha256")
                if not expected:
                    continue
                full_path = os.path.join(directory, rel_path)
                if not os.path.exists(full_path):
                    tampered.append((rel_path, "MISSING"))
                    print("    MISSING: {}".format(rel_path))
                    continue
                sha256 = hashlib.sha256()
                with open(full_path, 'rb') as fh:
                    for chunk in iter(lambda: fh.read(8192), b''):
                        sha256.update(chunk)
                actual = sha256.hexdigest()
                if actual != expected:
                    tampered.append((rel_path, "HASH MISMATCH"))
                    print("    TAMPERED: {} (expected {:.8s}... got {:.8s}...)".format(
                        rel_path, expected, actual))
            if not tampered:
                print("    All {} manifest entries verified.".format(len(manifest_files)))
        else:
            print("\n  STRICT: No manifest found. Run 'manifest' first.")

        # Verify witness sidecars
        print("\n  WITNESS SIDECAR VERIFICATION:")
        witness_check = 0
        for dirpath, dirnames, filenames in os.walk(directory):
            if '.git' in dirpath:
                continue
            dirnames[:] = [d for d in dirnames if d != '.git']
            for fname in filenames:
                if fname.endswith('.witness.bismillah'):
                    witness_path = os.path.join(dirpath, fname)
                    source_path = witness_path.replace('.witness.bismillah', '')
                    if os.path.exists(source_path):
                        try:
                            with open(witness_path, 'r', encoding='utf-8') as wf:
                                w_data = json.load(wf)
                            with open(source_path, 'rb') as sf:
                                source_bytes = sf.read()
                            stored = w_data.get("muhkam_seal", "")
                            computed = compute_seal(source_bytes)
                            if stored == computed:
                                witness_check += 1
                            else:
                                rel = os.path.relpath(source_path, directory)
                                tampered.append((rel, "WITNESS MISMATCH"))
                                print("    TAMPERED: {}".format(rel))
                        except Exception:
                            pass
        if witness_check > 0:
            print("    {} witness sidecars verified.".format(witness_check))

    print("  {}".format("=" * 60))
    return {"total": total, "protected": protected, "unprotected": unprotected,
            "tampered": tampered, "witness_verified": witness_verified}


def generate_manifest(directory):
    """Generate a Bismillah integrity manifest (151-layer version)."""
    import datetime
    manifest = OrderedDict([
        (BISMILLAH, True),
        ("manifest_version", "4.0"),
        ("encoder_version", ENCODER_VERSION),
        ("architecture", "11-Heaven, 151-Layer FATIMA v4.0"),
        ("total_heavens", TOTAL_HEAVENS),
        ("total_layers", TOTAL_LAYERS),
        ("seal_timestamp", datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")),
        ("generator", "Bismillah Divine Protection Encoder -- FATIMA v4.0"),
        ("al_asma_count", len(AL_ASMA_UL_HUSNA)),
        ("hurst_reference", {
            "H_11_harmonic": HURST_HARMONIC,
            "H_11_partitioned": HURST_PARTITIONED,
        }),
        ("files", OrderedDict()),
    ])

    manifest_path = os.path.join(directory, MANIFEST_FILENAME)
    count = 0
    for dirpath, dirnames, filenames in os.walk(directory):
        if '.git' in dirpath:
            continue
        dirnames[:] = [d for d in dirnames if d != '.git']
        for fname in sorted(filenames):
            fpath = os.path.join(dirpath, fname)
            rel = os.path.relpath(fpath, directory)
            if os.path.abspath(fpath) == os.path.abspath(manifest_path):
                continue
            try:
                sha256 = hashlib.sha256()
                with open(fpath, 'rb') as f:
                    file_bytes = f.read()
                sha256.update(file_bytes)
                manifest["files"][rel] = {
                    "sha256": sha256.hexdigest(),
                    "bismillah_seal": compute_seal(file_bytes),
                    "size": len(file_bytes),
                }
                count += 1
            except Exception as e:
                manifest["files"][rel] = {"error": str(e)}

    manifest["total_files"] = count
    with open(manifest_path, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    print("\n  {} -- 151-Layer Manifest Generated".format(BISMILLAH))
    print("  {} files catalogued".format(count))
    print("  Written to: {}".format(manifest_path))
    return manifest


def generate_witness_report(directory):
    """Generate a fractal witness report across all files."""
    print("\n  {} -- 11-Heaven Fractal Witness Report".format(BISMILLAH))
    print("  {}".format("=" * 60))
    print("  Architecture: {} heavens, {} layers".format(TOTAL_HEAVENS, TOTAL_LAYERS))
    print("")

    all_hurst = []
    file_testimonies = []

    for dirpath, dirnames, filenames in os.walk(directory):
        if '.git' in dirpath:
            continue
        dirnames[:] = [d for d in dirnames if d != '.git' and d != '__pycache__']

        for fname in sorted(filenames):
            if fname.endswith('.bismillah') or fname == SELF_NAME:
                continue
            if fname == MANIFEST_FILENAME:
                continue

            filepath = os.path.join(dirpath, fname)
            rel = os.path.relpath(filepath, directory)

            try:
                with open(filepath, 'rb') as f:
                    content_bytes = f.read()

                computation = compute_all_151_layers(content_bytes, filepath)
                h_val = computation["hurst_11"]
                all_hurst.append(h_val)

                p_class = "super-persistent" if h_val > 1.0 else (
                    "persistent" if h_val > 0.5 else "random")
                file_testimonies.append({
                    "file": rel,
                    "hurst_11": h_val,
                    "persistence": p_class,
                    "master_witness": computation["master_witness"][:16],
                    "layers": computation["total_layers"],
                })

                seal_name = _name_for_layer(len(file_testimonies))[0]
                print("  {} -- H(11)={:.4f} [{}] sealed by {} [{} layers]".format(
                    rel, h_val, p_class, seal_name, computation["total_layers"]))

            except Exception as e:
                print("  {} -- SKIP ({})".format(rel, str(e)[:40]))

    if all_hurst:
        mean_h = sum(all_hurst) / len(all_hurst)
        print("\n  {}".format("-" * 60))
        print("  AGGREGATE WITNESS:")
        print("    Files analyzed:        {}".format(len(all_hurst)))
        print("    Mean H(11):            {:.6f}".format(mean_h))
        print("    Distance from H=1.0:   {:.6f}".format(abs(mean_h - HURST_PERFECT)))
        print("    Reference (Qur'an):    H(11) = {}".format(HURST_HARMONIC))

        agg_h = hashlib.sha256()
        agg_h.update(BISMILLAH.encode('utf-8'))
        for ft in file_testimonies:
            agg_h.update(ft["master_witness"].encode('utf-8'))
        agg_h.update(BISMILLAH.encode('utf-8'))
        print("    Aggregate witness:     {}".format(agg_h.hexdigest()[:32]))

    print("  {}".format("=" * 60))
    return file_testimonies


def display_heavens_report(directory):
    """Display a heaven-by-heaven report for a single file or directory."""
    print("\n  {} -- 11-Heaven Architecture Report".format(BISMILLAH))
    print("  {}".format("=" * 60))

    target_files = []
    if os.path.isfile(directory):
        target_files.append(directory)
    else:
        for dirpath, dirnames, filenames in os.walk(directory):
            if '.git' in dirpath:
                continue
            dirnames[:] = [d for d in dirnames if d != '.git' and d != '__pycache__']
            for fname in sorted(filenames):
                if not fname.endswith('.bismillah') and fname != SELF_NAME:
                    target_files.append(os.path.join(dirpath, fname))

    for filepath in target_files[:10]:  # Limit to first 10 files
        rel = os.path.relpath(filepath, directory) if os.path.isdir(directory) else os.path.basename(filepath)
        print("\n  FILE: {}".format(rel))
        print("  {}".format("-" * 50))

        try:
            with open(filepath, 'rb') as f:
                content_bytes = f.read()

            computation = compute_all_151_layers(content_bytes, filepath)

            for h_summary in computation["heavens"]:
                h_idx = h_summary["heaven"]
                h_def = HEAVENS[h_idx]
                print("\n    Heaven {} -- {} ({})".format(
                    h_idx, h_def["name_en"], h_def["scale"]))
                print("    Guardian: {} ({})".format(
                    h_def["guardian"], h_def["guardian_meaning"]))
                print("    Layers: {} ({}-{})".format(
                    h_summary["layer_count"], h_def["layer_start"], h_def["layer_end"]))
                print("    Heaven seal: {}...".format(h_summary["heaven_seal"][:32]))

            print("\n    MASTER WITNESS (Sidrat al-Muntaha): {}...".format(
                computation["master_witness"][:32]))
            print("    H(11) = {}".format(round(computation["hurst_11"], 6)))

        except Exception as e:
            print("    ERROR: {}".format(str(e)[:60]))

    print("\n  {}".format("=" * 60))


# ============================================================================
#  COMMAND LINE INTERFACE
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="{} -- FATIMA v4.0 -- 11-Heaven, 151-Layer Divine Protection".format(BISMILLAH),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Architecture: 11 Heavens, 151 Layers

  Heaven 0   As-Samawat ad-Dunya      SUBATOMIC       14 layers
  Heaven 1   As-Samawat ath-Thaniya    ATOMIC          13 layers
  Heaven 2   As-Samawat ath-Thalitha   MOLECULAR       13 layers
  Heaven 3   As-Samawat ar-Rabi'a      CELLULAR        13 layers
  Heaven 4   As-Samawat al-Khamisa     ORGANIC         14 layers
  Heaven 5   As-Samawat as-Sadisa      TERRESTRIAL     13 layers
  Heaven 6   As-Samawat as-Sabi'a      PLANETARY       14 layers
  Heaven 7   As-Samawat ath-Thamina    STELLAR         14 layers
  Heaven 8   As-Samawat at-Tasi'a      GALACTIC        14 layers
  Heaven 9   As-Samawat al-'Ashira     COSMIC          18 layers
  Heaven 10  Sidrat al-Muntaha         DIVINE WITNESS  11 layers
  -------------------------------------------------------
  Total                                                151 layers

  "Seven is what the Qur'an says. Eleven is what the Qur'an shows."

Examples:
  python bismillah_encoder.py seal ./project              # 151-layer seal
  python bismillah_encoder.py seal ./project --names      # + embed 99 Names
  python bismillah_encoder.py verify ./project             # Verify protection
  python bismillah_encoder.py verify ./project --strict    # + hash chain check
  python bismillah_encoder.py manifest ./project           # Integrity manifest
  python bismillah_encoder.py witness ./project            # Fractal witness report
  python bismillah_encoder.py heavens ./project            # Heaven-by-heaven report
  python bismillah_encoder.py decode ./file.md             # Extract ZWC payloads

{}
""".format(BISMILLAH)
    )
    sub = parser.add_subparsers(dest='command')

    seal_p = sub.add_parser('seal', help='Apply 151-layer seal across 11 heavens')
    seal_p.add_argument('path', help='Directory to seal')
    seal_p.add_argument('--names', action='store_true',
                        help='Embed the 99 Names of Allah')
    seal_p.add_argument('--dry-run', action='store_true',
                        help='Preview without writing')

    verify_p = sub.add_parser('verify', help='Verify 151-layer protection')
    verify_p.add_argument('path', help='Directory to verify')
    verify_p.add_argument('--strict', action='store_true',
                          help='Recompute hashes and verify witnesses')

    manifest_p = sub.add_parser('manifest', help='Generate integrity manifest')
    manifest_p.add_argument('path', help='Directory to manifest')

    witness_p = sub.add_parser('witness', help='Generate fractal witness report')
    witness_p.add_argument('path', help='Directory to analyze')

    heavens_p = sub.add_parser('heavens', help='Display heaven-by-heaven report')
    heavens_p.add_argument('path', help='File or directory to analyze')

    decode_p = sub.add_parser('decode', help='Extract ZWC watermark payloads')
    decode_p.add_argument('path', help='File to decode')

    args = parser.parse_args()

    print("\n  {}".format(BISMILLAH))

    if args.command == 'seal':
        if os.path.isdir(args.path):
            seal_directory(args.path, embed_names=args.names,
                           dry_run=getattr(args, 'dry_run', False))
        else:
            print("  ERROR: {} is not a directory".format(args.path))
            sys.exit(1)

    elif args.command == 'verify':
        if os.path.isdir(args.path):
            result = verify_directory(args.path, strict=args.strict)
            if result["unprotected"] or result.get("tampered"):
                sys.exit(2)
        else:
            print("  ERROR: {} is not a directory".format(args.path))
            sys.exit(1)

    elif args.command == 'manifest':
        if os.path.isdir(args.path):
            generate_manifest(args.path)
        else:
            print("  ERROR: {} is not a directory".format(args.path))
            sys.exit(1)

    elif args.command == 'witness':
        if os.path.isdir(args.path):
            generate_witness_report(args.path)
        else:
            print("  ERROR: {} is not a directory".format(args.path))
            sys.exit(1)

    elif args.command == 'heavens':
        display_heavens_report(args.path)

    elif args.command == 'decode':
        if os.path.isfile(args.path):
            try:
                with open(args.path, 'r', encoding='utf-8') as f:
                    content = f.read()
                payloads = extract_watermarks(content)
                if payloads:
                    print("  Found {} ZWC watermark payload(s):".format(len(payloads)))
                    for i, payload in enumerate(payloads, 1):
                        print("    [{}] {}".format(i, payload))
                else:
                    print("  No ZWC watermark payloads found.")
            except UnicodeDecodeError:
                print("  ERROR: {} is not a text file".format(args.path))
                sys.exit(1)
        else:
            print("  ERROR: {} is not a file".format(args.path))
            sys.exit(1)

    else:
        parser.print_help()
        sys.exit(1)

    print("\n  {}\n".format(BISMILLAH))


if __name__ == '__main__':
    main()

# Bismillah ir-Rahman ir-Rahim
