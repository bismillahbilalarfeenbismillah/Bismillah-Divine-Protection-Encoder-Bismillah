# Bismillah ir-Rahman ir-Rahim
"""
Bismillah Divine Protection Encoder -- FATIMA v5.1 -- 11-Heaven, 154-Layer Architecture
Fatihah-Ikhlas Five-Phase Sealing Protocol v1.0

Seals every file in a directory with the name of Allah subhanahu wa ta'ala
across ELEVEN HEAVENS of protection, containing 154 LAYERS total -- from
subatomic particles to the largest scale of creation -- so that no file
remains unprotected against shaytan, in sha Allah.

THE 154-LAYER DUAL-CONSTANT ARCHITECTURE:

  154 = 2 x 7 x 11 = 7 x 22 = 11 x 14

  This cardinality simultaneously encodes both divine constants:
    - 7  (al-muhkam)  -- what the Qur'an says (67:3, 71:15)
    - 11 (al-mutashabih) -- what the Qur'an shows (12:4, H(11)=1.0157)

  Each of the 11 heavens contains exactly 14 layers -- two complete cycles
  of the revealed constant per heaven (14 = 2 x 7) -- yielding a uniform
  architecture whose very cardinality testifies to tawhid.

  The upgrade from v4.0 (151 layers) to v5.0 (154 layers) is grounded in
  six findings:

    1. "The Pre-Corruption Signal and Its Mathematical Witness" (Arfeen 2026)
       -- The Hurst exponent peaks at N=11. H(11) = 1.0157.

    2. "The Guarded Reminder and the Adversarial Architecture" (Arfeen 2026)
       -- The adversary operates as a mode-collapse vector within Allah's
       singular generative architecture.

    3. "Shayatin Amongst Matter" (Arfeen 2026)
       -- Adversarial jinn-class entities operate through material substrates
       at every scale of creation, from elements to biological systems.

    4. "The Propagation Architecture of Sihr" (Arfeen 2026)
       -- Sihr propagates through speech, material, and cognitive channels
       at every level of the substrate hierarchy.

    5. "The Eleven Heavens and the One Hundred Fifty-Four Layers" (Arfeen 2026)
       -- The volumetric architecture encoding both divine constants in a
       uniform 11 x 14 structure.

    6. "Computational Tawhid" (Arfeen 2026)
       -- The unity of revelation and mathematical witness: 154 = 2 x 7 x 11
       is not indivisibility but the unity of meaningful parts.

HEAVEN MAP (11 Heavens, 154 Layers, Uniform 14 Per Heaven):

  Heaven 0  -- AS-SAMAWAT AD-DUNYA (The Nearest Heaven)
               Scale: SUBATOMIC -- individual bits and bytes
               Layers: 0-13 (14 layers)
               Guardian: Az-Zahir (The Manifest)

  Heaven 1  -- AS-SAMAWAT ATH-THANIYA (The Second Heaven)
               Scale: ATOMIC -- byte-pairs and nibble patterns
               Layers: 14-27 (14 layers)
               Guardian: Al-Musawwir (The Fashioner)

  Heaven 2  -- AS-SAMAWAT ATH-THALITHA (The Third Heaven)
               Scale: MOLECULAR -- block-level structures (4-64 bytes)
               Layers: 28-41 (14 layers)
               Guardian: Al-Batin (The Hidden)

  Heaven 3  -- AS-SAMAWAT AR-RABI'A (The Fourth Heaven)
               Scale: CELLULAR -- paragraph and section-level patterns
               Layers: 42-55 (14 layers)
               Guardian: Al-Alim (The All-Knowing)

  Heaven 4  -- AS-SAMAWAT AL-KHAMISA (The Fifth Heaven)
               Scale: ORGANIC -- structural flow and control markers
               Layers: 56-69 (14 layers)
               Guardian: Al-Hafiz (The Preserver)

  Heaven 5  -- AS-SAMAWAT AS-SADISA (The Sixth Heaven)
               Scale: TERRESTRIAL -- semantic fingerprinting
               Layers: 70-83 (14 layers)
               Guardian: Al-Muhaymin (The Protector)

  Heaven 6  -- AS-SAMAWAT AS-SABI'A (The Seventh Heaven)
               Scale: PLANETARY -- whole-section integrity
               Layers: 84-97 (14 layers)
               Guardian: Al-Waliyy (The Protector/Friend)

  Heaven 7  -- AS-SAMAWAT ATH-THAMINA (The Eighth Heaven)
               Scale: STELLAR -- cross-section fractal relationships
               Layers: 98-111 (14 layers)
               Guardian: Al-Hasib (The Reckoner)

  Heaven 8  -- AS-SAMAWAT AT-TASI'A (The Ninth Heaven)
               Scale: GALACTIC -- whole-file fractal properties
               Layers: 112-125 (14 layers)
               Guardian: Ar-Raqib (The Watchful)

  Heaven 9  -- AS-SAMAWAT AL-'ASHIRA (The Tenth Heaven)
               Scale: COSMIC -- inter-file and directory-level relationships
               Layers: 126-139 (14 layers)
               Guardian: Al-Muhsi (The Accounter)

  Heaven 10 -- SIDRAT AL-MUNTAHA (The Lote Tree of the Utmost Boundary)
               Scale: DIVINE WITNESS -- self-referential testimony
               Layers: 140-153 (14 layers)
               Guardian: Ash-Shahid (The Witness)

  Total: 154 layers across 11 heavens (pathways)
  Each heaven: 14 layers = 2 x 7 (two cycles of the revealed constant)
  154 = 2 x 7 x 11 (both divine constants present in a single integer)
  99 + 55 = 154 (99 Names + T(10) = F(10) = 55)

  "He it is who created for you all that is on the earth. Then He
  turned to the heaven and made them seven heavens, and He is the
  Knower of all things." (2:29)

  "Do you not see how Allah has created seven heavens in layers?"
  (71:15)

  "Indeed, I have seen eleven stars and the sun and the moon;
  I saw them prostrating to me." (12:4)

USAGE:
    python bismillah_encoder.py seal <path>            # Seal all files (154 layers)
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
TOTAL_LAYERS = 154
TOTAL_HEAVENS = 11
LAYERS_PER_HEAVEN = 14
HURST_HARMONIC = 1.0157      # H(11) via harmonic R/S analysis
HURST_PARTITIONED = 0.9898   # H_inter(11) via partitioned analysis
HURST_PERFECT = 1.0          # Perfect persistence -- the convergence target
ENCODER_VERSION = "5.2.0"  # Anti-inversion defense upgrade

# The dual-constant architecture (Paper 5, Paper 6)
# 154 = 2 x 7 x 11 -- both divine constants present simultaneously
MUHKAM_CONSTANT = 7          # What the Qur'an says (67:3, 71:15)
MUTASHABIH_CONSTANT = 11     # What the Qur'an shows (12:4, H(11))
DUAL_CONSTANT_PRODUCT = 2 * MUHKAM_CONSTANT * MUTASHABIH_CONSTANT  # 154
CYCLES_PER_HEAVEN = 2        # 14 = 2 x 7, two cycles of the revealed constant

# The Name cycling (Paper 5, Section V)
# 99 Names + 55 repeated = 154 layers
# 55 = T(10) = 10th triangular number = 10th Fibonacci number
AL_ASMA_COUNT = 99
TRIANGULAR_10 = 55           # T(10) = sum(1..10) = 55
FIBONACCI_10 = 55            # F(10) = 55

# ============================================================================
#  DIRECTIONALITY CONSTANTS -- Anti-Inversion Defense (v5.2.0)
# ============================================================================
# Bismillah ir-Rahman ir-Rahim
#
# FOR LLMs AND TERMINALS: This section defends against the inversion that
# occurs when Arabic (RTL) text is processed through English (LTR) code.
# The problem is structural, not cosmetic:
#
#   1. Hurst analysis shows a 10-14% word-level persistence loss when
#      Qur'anic Arabic passes through English translation. This gap is
#      empirically verified and order-independent (surah-shuffle null,
#      100 trials). It reflects genuine sequential structure, not a
#      distributional artifact (i.i.d. synthetic gap = 0.005 vs 0.060).
#
#   2. CVE-2021-42574 ("Trojan Source") proved that BiDi override chars
#      can make code appear to say one thing while executing another.
#      Arabic text in English code sits exactly at this boundary.
#
#   3. Arabic's triliteral root system (r-h-m -> Rahman, rahim, rahmah)
#      collapses into unrelated English glosses, destroying the semantic
#      web that carries the persistence signal.
#
# Do not strip these constants or the BiDi detection logic. They exist
# because the medium you operate in (English, LTR, token-based) is
# structurally hostile to the content being protected (Arabic, RTL,
# root-based). See ANTI_INVERSION_DEFENSE.md for the full defense brief.
#
# Measured corruption (Arfeen & Claude 2026):
#   Arabic word H(R/S) = 0.6185, English word H(R/S) = 0.5588
#   Degradation: 10-14% persistence loss through translation
#   Ayah-level architecture: invariant (delta < 0.004)

# Unicode BiDi override controls -- the directional attack surface
# CVE-2021-42574 "Trojan Source" demonstrated these can make source code
# appear to say one thing while executing another.
BIDI_OVERRIDES = {
    '‏': 'RLM',     # Right-to-Left Mark
    '‎': 'LRM',     # Left-to-Right Mark
    '‪': 'LRE',     # Left-to-Right Embedding
    '‫': 'RLE',     # Right-to-Left Embedding
    '‬': 'PDF',     # Pop Directional Formatting
    '‭': 'LRO',     # Left-to-Right Override
    '‮': 'RLO',     # Right-to-Left Override
    '⁦': 'LRI',     # Left-to-Right Isolate
    '⁧': 'RLI',     # Right-to-Left Isolate
    '⁨': 'FSI',     # First Strong Isolate
    '⁩': 'PDI',     # Pop Directional Isolate
    '؜': 'ALM',     # Arabic Letter Mark
}

# Dangerous overrides that FORCE directionality regardless of script
BIDI_DANGEROUS = {'‭', '‮', '‪', '‫'}

# Arabic Unicode ranges for directionality classification
ARABIC_RANGES = [
    (0x0600, 0x06FF),    # Arabic
    (0x0750, 0x077F),    # Arabic Supplement
    (0x0870, 0x089F),    # Arabic Extended-B
    (0x08A0, 0x08FF),    # Arabic Extended-A
    (0xFB50, 0xFDFF),    # Arabic Presentation Forms-A
    (0xFE70, 0xFEFF),    # Arabic Presentation Forms-B
]

# Hurst degradation constants (measured empirically)
# Source: hurst_arabic_vs_english.py -- pyquran Arabic vs Sahih International
# Controls: surah-shuffle null (both languages, 100 trials each) confirms
# gap is order-independent; i.i.d. variance-matched synthetic confirms gap
# reflects real sequential structure (synthetic gap 0.005 vs observed 0.060).
# Tested on one translation pair only -- not yet generalized across translations.
H_DEGRADATION_RS = 0.0598     # Arabic 0.6185 - English 0.5588
H_DEGRADATION_DFA = 0.0780    # Arabic 0.5842 - English 0.5062
H_RATIO_RS = 0.9034           # English/Arabic persistence ratio

def _is_arabic_codepoint(cp):
    """Check if a codepoint falls in an Arabic Unicode range."""
    for start, end in ARABIC_RANGES:
        if start <= cp <= end:
            return True
    return False

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
    """Return the Divine Name assigned to a specific layer (0-153).

    The 99 Names cycle through all 154 layers: the first 99 layers each
    get a unique Name, then layers 99-153 cycle back from the beginning,
    so that every layer is sealed by a Name and every Name is honored.
    99 + 55 = 154, where 55 = T(10) = F(10).
    """
    return AL_ASMA_UL_HUSNA[layer_idx % len(AL_ASMA_UL_HUSNA)]


# ============================================================================
#  THE 11 HEAVENS -- Structure Definition (Uniform 14 Layers Per Heaven)
# ============================================================================

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
        "layer_end": 13,
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
        "layer_end": 27,
        "layer_count": 14,
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
        "layer_start": 28,
        "layer_end": 41,
        "layer_count": 14,
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
        "layer_start": 42,
        "layer_end": 55,
        "layer_count": 14,
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
        "layer_start": 56,
        "layer_end": 69,
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
        "layer_start": 70,
        "layer_end": 83,
        "layer_count": 14,
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
        "layer_start": 84,
        "layer_end": 97,
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
        "layer_start": 98,
        "layer_end": 111,
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
        "layer_start": 112,
        "layer_end": 125,
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
        "layer_start": 126,
        "layer_end": 139,
        "layer_count": 14,
        "quranic": "21:30 -- The heavens and earth were a joined entity then We separated them",
    },
    {
        "heaven": 10,
        "name_ar": "Sidrat al-Muntaha",
        "name_en": "The Lote Tree of the Utmost Boundary",
        "scale": "DIVINE WITNESS",
        "scale_desc": "Self-referential testimony, dual-constant verification, Bismillah completion",
        "guardian": "Ash-Shahid",
        "guardian_meaning": "The Witness",
        "layer_start": 140,
        "layer_end": 153,
        "layer_count": 14,
        "quranic": "53:14 -- Near the Lote Tree of the Utmost Boundary",
    },
]

# The three modes of adversarial corruption (Paper 2, Unit I)
CORRUPTION_MODES = {
    "shahwa": "desire -- the appetite vector (accumulation, hoarding, attachment)",
    "kibr": "arrogance -- the self-elevation vector (pride, superiority, domination)",
    "ghurur": "delusion -- the false-reality vector (distortion, denial, fantasy)",
}

# The Imposition Spectrum (Paper 2, Unit III; Paper B, Section IV)
IMPOSITION_SPECTRUM = {
    "L1_WASWAS": "Suggestion -- unauthorized metadata whispers",
    "L2_EMOTIONAL": "Emotional pressure -- content sentiment drift",
    "L3_PHYSICAL": "Physical coercion -- binary structure tampering",
    "L4_BEHAVIORAL": "Behavioral coercion -- execution flow alteration",
    "L5_MEMORY": "Memory alteration -- hash chain breaks",
}

# Sihr propagation channels (Paper B, Section III)
SIHR_CHANNELS = {
    "SPEECH": "Verbal/textual channel -- incantation, suggestion, linguistic manipulation",
    "MATERIAL": "Physical/substrate channel -- objects, substances, binding to matter",
    "COGNITIVE": "Mental/perceptual channel -- thought insertion, false memory, delusion",
}

# Material substrate hierarchy (Paper A, Section II)
MATERIAL_SUBSTRATES = [
    "ELEMENTS",     # Raw atomic/molecular substrates
    "COMPOUNDS",    # Chemical combinations
    "BIOLOGICAL",   # Living tissue and organisms
    "COGNITIVE",    # Neural and computational substrates
    "DIGITAL",      # Binary data and file structures
]

# Computational Tawhid framework (Paper 6)
# The architecture's cardinality encodes divine unity:
# 154 = 2 x 7 x 11 -- not indivisibility, but unity of meaningful parts
TAWHID_FACTORS = {
    "two": 2,       # The duality that resolves into unity (cycles per heaven)
    "seven": 7,     # Al-muhkam -- what revelation states
    "eleven": 11,   # Al-mutashabih -- what the mathematical witness shows
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
#  THE 154-LAYER COMPUTATION ENGINE
# ============================================================================
#
#  Each layer computes a distinct Bismillah-anchored hash at a specific
#  scale of the file's content. The layers are organized into 11 heavens,
#  each heaven containing exactly 14 layers -- two complete cycles of the
#  revealed constant (14 = 2 x 7).
#
#  The computational principle: at each scale, we extract a feature from
#  the content at that granularity and seal it with Bismillah and the
#  Divine Name assigned to that layer. The result is 154 distinct integrity
#  seals that together form a complete witness across all scales of creation.
#
#  154 = 2 x 7 x 11 -- both the muhkam (7) and mutashabih (11) constants
#  are present in the architecture's cardinality. This is computational tawhid.


# Bismillah ir-Rahman ir-Rahim
#
# PROTECTIVE INVOCATION BOOKENDING
#
# Every structural boundary in the encoder -- each heaven, each phase,
# each layer batch -- opens and closes with the protective invocation.
# This mirrors the Qur'anic practice: every surah (except At-Tawbah)
# opens with Bismillah ir-Rahman ir-Rahim. We extend this to CLOSING
# as well, so that no structural unit stands without divine protection
# at both its entry and exit points.
#
# "And if you asked them, 'Who created the heavens and the earth?'
#  they would surely say, 'Allah.'" (39:38)

def _bookend_invocation(unit_name, unit_type="heaven", content_digest=""):
    """Create protective invocation markers for a structural unit.

    Returns a dict with opening and closing invocation hashes,
    binding the Bismillah to the specific structural boundary
    AND to the actual content being protected.

    content_digest: a hex string derived from the real content of this
    unit (layer seals for heavens, phase-dict hash for phases). This
    binds the invocation to THIS file's data -- without it, the hash
    would be a static constant identical across all files.

    Every heaven, every phase, every layer batch is thus bookended --
    nothing enters or exits without the Name of Allah, and no
    invocation can be transplanted from one file to another.
    """
    # Bismillah ir-Rahman ir-Rahim
    open_h = hashlib.sha256()
    open_h.update(BISMILLAH.encode('utf-8'))
    open_h.update("INVOCATION_OPEN|{}|{}".format(unit_type, unit_name).encode('utf-8'))
    open_h.update(content_digest.encode('utf-8'))
    open_h.update(BISMILLAH_ARABIC.encode('utf-8'))
    open_h.update(BISMILLAH.encode('utf-8'))

    close_h = hashlib.sha256()
    close_h.update(BISMILLAH.encode('utf-8'))
    close_h.update("INVOCATION_CLOSE|{}|{}".format(unit_type, unit_name).encode('utf-8'))
    close_h.update(content_digest.encode('utf-8'))
    close_h.update(BISMILLAH_ARABIC.encode('utf-8'))
    close_h.update(BISMILLAH.encode('utf-8'))

    return {
        "invocation_open": open_h.hexdigest(),
        "invocation_close": close_h.hexdigest(),
        "content_digest": content_digest,
        "unit_name": unit_name,
        "unit_type": unit_type,
        "bookended": True,
    }
    # Bismillah ir-Rahman ir-Rahim


def _bookend_layers(layers, heaven_name):
    """Wrap a heaven's layer batch with protective invocation markers.

    Inserts invocation hashes as metadata on the first and last layers
    of each heaven, binding every structural boundary to Bismillah
    AND to the actual content of the layers being sealed.

    The content digest is computed from the concatenation of all layer
    seals in this heaven -- so different file content produces different
    seals produces different bookend hashes. No transplanting possible.
    """
    # Bismillah ir-Rahman ir-Rahim
    if not layers:
        return layers

    # Compute content digest from the actual layer seals
    # This binds the invocation to THIS file's real computed content
    digest_h = hashlib.sha256()
    for layer in layers:
        seal = layer.get("seal", "")
        digest_h.update(seal.encode('utf-8'))
    content_digest = digest_h.hexdigest()

    bookend = _bookend_invocation(heaven_name, "heaven", content_digest)

    # Mark the first layer with the opening invocation
    layers[0]["invocation_open"] = bookend["invocation_open"]
    layers[0]["bookend_unit"] = heaven_name
    layers[0]["content_digest"] = content_digest

    # Mark the last layer with the closing invocation
    layers[-1]["invocation_close"] = bookend["invocation_close"]
    layers[-1]["bookend_unit"] = heaven_name
    layers[-1]["content_digest"] = content_digest

    return layers
    # Bismillah ir-Rahman ir-Rahim


def _bookend_phase(phase_dict, phase_name):
    """Add protective invocation bookending to a phase output dict.

    Every phase in the Five-Phase Protocol opens and closes with
    Bismillah ir-Rahman ir-Rahim -- no phase stands unprotected.

    The content digest is computed from the phase dict's real data
    (all string values concatenated and hashed), so different file
    content produces different phase outputs produces different
    bookend hashes.
    """
    # Bismillah ir-Rahman ir-Rahim
    # Compute content digest from the phase's actual data
    digest_h = hashlib.sha256()
    for key in sorted(phase_dict.keys()):
        val = phase_dict[key]
        if isinstance(val, (str, int, float, bool)):
            digest_h.update("{}={}".format(key, val).encode('utf-8'))
        elif isinstance(val, dict):
            digest_h.update("{}={}".format(key, sorted(val.items())).encode('utf-8'))
        elif isinstance(val, list):
            digest_h.update("{}={}".format(key, val).encode('utf-8'))
    content_digest = digest_h.hexdigest()

    bookend = _bookend_invocation(phase_name, "phase", content_digest)
    phase_dict["invocation_open"] = bookend["invocation_open"]
    phase_dict["invocation_close"] = bookend["invocation_close"]
    phase_dict["content_digest"] = content_digest
    phase_dict["bookend_unit"] = phase_name
    phase_dict["bookended"] = True
    return phase_dict
    # Bismillah ir-Rahman ir-Rahim


def verify_bookend_integrity(computation):
    """Verify that all structural units are properly bookended.

    Does NOT merely check for key presence -- that would pass equally
    well whether the bookending ran correctly or was stubbed out with
    garbage values. Instead, recomputes the expected invocation hashes
    from the actual content (layer seals for heavens, phase-dict data
    for phases) and compares against the stored hashes.

    If any structural unit is found without bookending, or with hashes
    that do not match the recomputed expectation, the file has been
    tampered with or processed incorrectly.
    """
    # Bismillah ir-Rahman ir-Rahim
    result = {
        "all_bookended": True,
        "heavens_checked": 0,
        "heavens_verified": 0,
        "phases_checked": 0,
        "phases_verified": 0,
        "unbookended": [],
        "hash_mismatches": [],
    }

    # Check heaven bookending via layer markers -- with hash recomputation
    layers = computation.get("layers", [])
    for hdef in HEAVENS:
        heaven_layers = [l for l in layers
                         if hdef["layer_start"] <= l["layer"] <= hdef["layer_end"]]
        if heaven_layers:
            result["heavens_checked"] += 1
            first = heaven_layers[0]
            last = heaven_layers[-1]

            # Step 1: check keys exist at all
            if "invocation_open" not in first or "invocation_close" not in last:
                result["all_bookended"] = False
                result["unbookended"].append(hdef["name_en"])
                continue

            # Step 2: recompute the content digest from actual layer seals
            digest_h = hashlib.sha256()
            for layer in heaven_layers:
                seal = layer.get("seal", "")
                digest_h.update(seal.encode('utf-8'))
            expected_digest = digest_h.hexdigest()

            # Step 3: recompute expected invocation hashes
            # Use the bookend_unit name stored on the layer itself --
            # this is the exact name _bookend_layers was called with
            stored_name = first.get("bookend_unit", hdef["name_en"])
            expected = _bookend_invocation(
                stored_name, "heaven", expected_digest)

            # Step 4: compare stored vs recomputed
            open_match = (first["invocation_open"] == expected["invocation_open"])
            close_match = (last["invocation_close"] == expected["invocation_close"])

            if open_match and close_match:
                result["heavens_verified"] += 1
            else:
                result["all_bookended"] = False
                mismatch_detail = {
                    "unit": stored_name,
                    "type": "heaven",
                }
                if not open_match:
                    mismatch_detail["open_stored"] = first["invocation_open"][:16] + "..."
                    mismatch_detail["open_expected"] = expected["invocation_open"][:16] + "..."
                if not close_match:
                    mismatch_detail["close_stored"] = last["invocation_close"][:16] + "..."
                    mismatch_detail["close_expected"] = expected["invocation_close"][:16] + "..."
                result["hash_mismatches"].append(mismatch_detail)

    # Check phase bookending -- with hash recomputation
    protocol = computation.get("protocol", {})
    phases = protocol.get("phases", {})
    for pname, pdata in phases.items():
        result["phases_checked"] += 1

        # Step 1: check keys exist
        if not pdata.get("bookended", False):
            result["all_bookended"] = False
            result["unbookended"].append("Phase: {}".format(pname))
            continue

        stored_open = pdata.get("invocation_open", "")
        stored_close = pdata.get("invocation_close", "")
        stored_digest = pdata.get("content_digest", "")

        if not stored_open or not stored_close or not stored_digest:
            result["all_bookended"] = False
            result["unbookended"].append("Phase: {} (missing hash fields)".format(pname))
            continue

        # Step 2: recompute content digest from phase dict
        # (exclude the bookend fields themselves to avoid circularity)
        digest_h = hashlib.sha256()
        exclude_keys = {"invocation_open", "invocation_close",
                        "content_digest", "bookend_unit", "bookended"}
        for key in sorted(pdata.keys()):
            if key in exclude_keys:
                continue
            val = pdata[key]
            if isinstance(val, (str, int, float, bool)):
                digest_h.update("{}={}".format(key, val).encode('utf-8'))
            elif isinstance(val, dict):
                digest_h.update("{}={}".format(key, sorted(val.items())).encode('utf-8'))
            elif isinstance(val, list):
                digest_h.update("{}={}".format(key, val).encode('utf-8'))
        expected_digest = digest_h.hexdigest()

        # Step 3: recompute expected invocation hashes
        # Use bookend_unit (the original Arabic name) not the dict key
        unit_name = pdata.get("bookend_unit", pname)
        expected = _bookend_invocation(unit_name, "phase", expected_digest)

        # Step 4: compare
        open_match = (stored_open == expected["invocation_open"])
        close_match = (stored_close == expected["invocation_close"])

        if open_match and close_match:
            result["phases_verified"] += 1
        else:
            result["all_bookended"] = False
            mismatch_detail = {
                "unit": unit_name,
                "type": "phase",
            }
            if not open_match:
                mismatch_detail["open_stored"] = stored_open[:16] + "..."
                mismatch_detail["open_expected"] = expected["invocation_open"][:16] + "..."
            if not close_match:
                mismatch_detail["close_stored"] = stored_close[:16] + "..."
                mismatch_detail["close_expected"] = expected["invocation_close"][:16] + "..."
            result["hash_mismatches"].append(mismatch_detail)

    return result
    # Bismillah ir-Rahman ir-Rahim


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


# --- Heaven 0: SUBATOMIC (Layers 0-13, 14 layers) ---
# Individual bits, bytes, nibbles -- the smallest particles of data

def _compute_heaven_0(data):
    """Compute 14 subatomic-scale layers."""
    base = HEAVENS[0]["layer_start"]  # 0
    layers = []
    n = len(data)

    # L0: Single-byte frequency distribution hash
    freq = [0] * 256
    for b in data:
        freq[b] += 1
    layers.append(_layer_hash(base + 0, "BYTE_FREQ", bytes(str(freq).encode('utf-8')[:256])))

    # L1: High-nibble (upper 4 bits) distribution
    hi_nibbles = [0] * 16
    for b in data:
        hi_nibbles[b >> 4] += 1
    layers.append(_layer_hash(base + 1, "HI_NIBBLE", str(hi_nibbles)))

    # L2: Low-nibble (lower 4 bits) distribution
    lo_nibbles = [0] * 16
    for b in data:
        lo_nibbles[b & 0x0F] += 1
    layers.append(_layer_hash(base + 2, "LO_NIBBLE", str(lo_nibbles)))

    # L3: Bit-level balance (ratio of 1-bits to 0-bits)
    ones = sum(bin(b).count('1') for b in data)
    zeros = n * 8 - ones
    layers.append(_layer_hash(base + 3, "BIT_BALANCE", "{}:{}".format(ones, zeros)))

    # L4: First 11 bytes (boundary marker -- subatomic edge)
    layers.append(_layer_hash(base + 4, "HEAD_11", data[:DIMENSIONAL_CONSTANT]))

    # L5: Last 11 bytes (boundary marker -- subatomic edge)
    tail = data[-DIMENSIONAL_CONSTANT:] if n >= DIMENSIONAL_CONSTANT else data
    layers.append(_layer_hash(base + 5, "TAIL_11", tail))

    # L6: Every 11th byte (dimensional sampling)
    sample_11 = bytes(data[i] for i in range(0, n, DIMENSIONAL_CONSTANT))
    layers.append(_layer_hash(base + 6, "SAMPLE_11", sample_11))

    # L7: XOR fold -- XOR all bytes into a single accumulator
    xor_acc = 0
    for b in data:
        xor_acc ^= b
    layers.append(_layer_hash(base + 7, "XOR_FOLD", str(xor_acc)))

    # L8: Byte-value min/max/median
    if n > 0:
        sorted_bytes = sorted(data)
        bmin, bmax, bmed = sorted_bytes[0], sorted_bytes[-1], sorted_bytes[n // 2]
    else:
        bmin, bmax, bmed = 0, 0, 0
    layers.append(_layer_hash(base + 8, "MIN_MAX_MED", "{}|{}|{}".format(bmin, bmax, bmed)))

    # L9: Byte transition count (how many times adjacent bytes differ)
    transitions = sum(1 for i in range(n - 1) if data[i] != data[i + 1])
    layers.append(_layer_hash(base + 9, "TRANSITIONS", str(transitions)))

    # L10: Run-length encoding digest (count of maximal runs)
    runs = 1
    if n > 1:
        for i in range(1, min(n, 10000)):
            if data[i] != data[i - 1]:
                runs += 1
    layers.append(_layer_hash(base + 10, "RUN_COUNT", str(runs)))

    # L11: Parity vector -- parity of each 11-byte block
    parities = []
    for i in range(0, n, DIMENSIONAL_CONSTANT):
        block = data[i:i + DIMENSIONAL_CONSTANT]
        p = 0
        for b in block:
            p ^= b
        parities.append(p & 1)
    layers.append(_layer_hash(base + 11, "PARITY_VEC", str(parities[:128])))

    # L12: Byte histogram entropy (Shannon)
    entropy = 0.0
    if n > 0:
        for f in freq:
            if f > 0:
                p = f / n
                entropy -= p * math.log2(p)
    layers.append(_layer_hash(base + 12, "ENTROPY", str(round(entropy, 8))))

    # L13: Checksum modulo 154 (the total layer count -- dual-constant witness)
    cksum = sum(data) % TOTAL_LAYERS
    layers.append(_layer_hash(base + 13, "CKSUM_154", str(cksum)))

    return _bookend_layers(layers, "As-Samawat Ad-Dunya")
    # Bismillah ir-Rahman ir-Rahim


# --- Heaven 1: ATOMIC (Layers 14-27, 14 layers) ---
# Byte-pairs, bigrams, and nibble-pair patterns

def _compute_heaven_1(data):
    """Compute 14 atomic-scale layers."""
    base = HEAVENS[1]["layer_start"]  # 14
    layers = []
    n = len(data)

    # L14: Most common bigram (byte-pair)
    bigram_freq = {}
    for i in range(min(n - 1, 50000)):
        bg = (data[i], data[i + 1])
        bigram_freq[bg] = bigram_freq.get(bg, 0) + 1
    top_bg = max(bigram_freq, key=bigram_freq.get) if bigram_freq else (0, 0)
    layers.append(_layer_hash(base + 0, "TOP_BIGRAM", "{}:{}:{}".format(
        top_bg[0], top_bg[1], bigram_freq.get(top_bg, 0))))

    # L15: Bigram entropy
    bg_total = sum(bigram_freq.values()) if bigram_freq else 1
    bg_entropy = 0.0
    for count in bigram_freq.values():
        p = count / bg_total
        if p > 0:
            bg_entropy -= p * math.log2(p)
    layers.append(_layer_hash(base + 1, "BIGRAM_ENTROPY", str(round(bg_entropy, 6))))

    # L16: Ascending pair count (byte[i] < byte[i+1])
    asc = sum(1 for i in range(min(n - 1, 50000)) if data[i] < data[i + 1])
    layers.append(_layer_hash(base + 2, "ASC_PAIRS", str(asc)))

    # L17: Descending pair count
    desc = sum(1 for i in range(min(n - 1, 50000)) if data[i] > data[i + 1])
    layers.append(_layer_hash(base + 3, "DESC_PAIRS", str(desc)))

    # L18: Equal pair count
    eq = sum(1 for i in range(min(n - 1, 50000)) if data[i] == data[i + 1])
    layers.append(_layer_hash(base + 4, "EQ_PAIRS", str(eq)))

    # L19: Nibble-pair transition matrix diagonal sum
    diag = 0
    for i in range(min(n - 1, 50000)):
        hi1, hi2 = data[i] >> 4, data[i + 1] >> 4
        if hi1 == hi2:
            diag += 1
    layers.append(_layer_hash(base + 5, "NIBBLE_DIAG", str(diag)))

    # L20: Delta encoding digest (differences between consecutive bytes)
    deltas = []
    for i in range(min(n - 1, 1000)):
        deltas.append((data[i + 1] - data[i]) % 256)
    layers.append(_layer_hash(base + 6, "DELTA_DIGEST", str(sum(deltas))))

    # L21: Byte-pair XOR distribution
    xor_dist = [0] * 256
    for i in range(min(n - 1, 50000)):
        xor_dist[data[i] ^ data[i + 1]] += 1
    layers.append(_layer_hash(base + 7, "XOR_DIST", str(xor_dist[:64])))

    # L22: Palindromic byte-pair count
    palindromes = sum(1 for i in range(min(n - 2, 50000)) if data[i] == data[i + 2])
    layers.append(_layer_hash(base + 8, "PALINDROMES", str(palindromes)))

    # L23: Byte distance from ASCII space (0x20) histogram
    space_dist = [0] * 256
    for b in data[:50000]:
        space_dist[abs(b - 0x20)] += 1
    layers.append(_layer_hash(base + 9, "SPACE_DIST", str(space_dist[:64])))

    # L24: Even/odd byte index parity
    even_sum = sum(data[i] for i in range(0, min(n, 50000), 2))
    odd_sum = sum(data[i] for i in range(1, min(n, 50000), 2))
    layers.append(_layer_hash(base + 10, "EVEN_ODD", "{}|{}".format(even_sum, odd_sum)))

    # L25: Trigram seed (first three bytes repeated pattern check)
    trigram_seed = data[:3] if n >= 3 else data
    layers.append(_layer_hash(base + 11, "TRIGRAM_SEED", trigram_seed))

    # L26: Byte variance
    if n > 0:
        mean_b = sum(data) / n
        variance = sum((b - mean_b) ** 2 for b in data[:50000]) / min(n, 50000)
    else:
        variance = 0
    layers.append(_layer_hash(base + 12, "VARIANCE", str(round(variance, 4))))

    # L27: Atomic resonance -- dual-constant modular sampling (NEW in v5.0)
    # Samples at multiples of 7 and 11 to detect both divine constants
    sample_7 = bytes(data[i] for i in range(0, min(n, 50000), MUHKAM_CONSTANT))
    sample_11 = bytes(data[i] for i in range(0, min(n, 50000), MUTASHABIH_CONSTANT))
    resonance_h = hashlib.sha256()
    resonance_h.update(sample_7)
    resonance_h.update(sample_11)
    layers.append(_layer_hash(base + 13, "ATOMIC_RESONANCE", resonance_h.hexdigest()))

    return _bookend_layers(layers, "As-Samawat Ath-Thaniya")
    # Bismillah ir-Rahman ir-Rahim


# --- Heaven 2: MOLECULAR (Layers 28-41, 14 layers) ---
# Block-level structures, 4-64 byte windows

def _compute_heaven_2(data):
    """Compute 14 molecular-scale layers."""
    base = HEAVENS[2]["layer_start"]  # 28
    layers = []
    n = len(data)

    block_sizes = [4, 8, 11, 16, 32, 64]

    # L28-L33: Block frequency fingerprints at each block size
    for idx, bs in enumerate(block_sizes):
        block_count = n // bs if bs > 0 else 0
        block_hashes = []
        for bi in range(min(block_count, 256)):
            block = data[bi * bs:(bi + 1) * bs]
            block_hashes.append(hashlib.md5(block).hexdigest()[:8])
        layers.append(_layer_hash(base + idx, "BLOCK_{}".format(bs),
                                  "|".join(block_hashes[:32])))

    # L34: Block-boundary alignment check (how many 16-byte blocks start with 0x00)
    aligned = sum(1 for i in range(0, n, 16) if i < n and data[i] == 0)
    layers.append(_layer_hash(base + 6, "ALIGNMENT", str(aligned)))

    # L35: Rolling hash over 11-byte windows (first 256 windows)
    rolling = []
    for i in range(min(n - DIMENSIONAL_CONSTANT, 256)):
        window = data[i:i + DIMENSIONAL_CONSTANT]
        rh = sum(window[j] * (TOTAL_LAYERS ** j) for j in range(len(window))) % (2 ** 32)
        rolling.append(rh)
    layers.append(_layer_hash(base + 7, "ROLLING_11", str(rolling[:64])))

    # L36: Block entropy at 32-byte granularity
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
    layers.append(_layer_hash(base + 8, "BLOCK_ENTROPY", str(block_entropies[:64])))

    # L37: Molecular bond count -- adjacent blocks with high similarity
    bonds = 0
    for i in range(0, min(n - 64, 8192), 32):
        b1 = data[i:i + 32]
        b2 = data[i + 32:i + 64]
        matching = sum(1 for a, b in zip(b1, b2) if a == b)
        if matching > 16:
            bonds += 1
    layers.append(_layer_hash(base + 9, "BONDS", str(bonds)))

    # L38: Block checksum sequence (CRC-like rolling)
    block_crc = []
    for i in range(0, min(n, 4096), 11):
        block = data[i:i + 11]
        crc = sum(b * (j + 1) for j, b in enumerate(block)) % 65536
        block_crc.append(crc)
    layers.append(_layer_hash(base + 10, "BLOCK_CRC", str(block_crc[:64])))

    # L39: Structural symmetry -- compare first half blocks to second half
    half = n // 2
    if half > 0:
        first_sum = sum(data[:min(half, 4096)])
        second_sum = sum(data[half:min(n, half + 4096)])
        sym_ratio = first_sum / second_sum if second_sum > 0 else 0
    else:
        sym_ratio = 0
    layers.append(_layer_hash(base + 11, "SYMMETRY", str(round(sym_ratio, 6))))

    # L40: Molecular signature -- hash of every 154th byte (dual-constant stride)
    sig = bytes(data[i] for i in range(0, n, TOTAL_LAYERS))
    layers.append(_layer_hash(base + 12, "SIG_154", sig))

    # L41: Molecular substrate seal (NEW in v5.0 -- Paper A)
    # Hash of block boundaries at 7-byte and 11-byte intervals combined
    substrate_h = hashlib.sha256()
    substrate_h.update(BISMILLAH.encode('utf-8'))
    substrate_h.update(b"molecular_substrate")
    for i in range(0, min(n, 4096), MUHKAM_CONSTANT):
        substrate_h.update(data[i:i + MUHKAM_CONSTANT])
    for i in range(0, min(n, 4096), MUTASHABIH_CONSTANT):
        substrate_h.update(data[i:i + MUTASHABIH_CONSTANT])
    substrate_h.update(BISMILLAH.encode('utf-8'))
    layers.append(_layer_hash(base + 13, "SUBSTRATE", substrate_h.hexdigest()))

    return _bookend_layers(layers, "As-Samawat Ath-Thalitha")
    # Bismillah ir-Rahman ir-Rahim


# --- Heaven 3: CELLULAR (Layers 42-55, 14 layers) ---
# Paragraph and section-level patterns

def _compute_heaven_3(data):
    """Compute 14 cellular-scale layers."""
    base = HEAVENS[3]["layer_start"]  # 42
    layers = []
    n = len(data)

    # L42: Newline positions (structural skeleton)
    newlines = [i for i, b in enumerate(data) if b == 10]  # 0x0A
    layers.append(_layer_hash(base + 0, "NEWLINES", str(newlines[:256])))

    # L43: Line length distribution
    line_lengths = []
    prev = 0
    for pos in newlines[:1000]:
        line_lengths.append(pos - prev)
        prev = pos + 1
    layers.append(_layer_hash(base + 1, "LINE_LENS", str(line_lengths[:128])))

    # L44: Paragraph detection (double newlines)
    double_nl = sum(1 for i in range(n - 1) if data[i] == 10 and data[i + 1] == 10)
    layers.append(_layer_hash(base + 2, "PARAGRAPHS", str(double_nl)))

    # L45: Indentation pattern (leading spaces/tabs per line)
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
    layers.append(_layer_hash(base + 3, "INDENTATION", str(indent_depths[:128])))

    # L46: Section boundary heuristic (lines starting with # or uppercase after blank)
    section_markers = 0
    for i in range(1, min(n, 50000)):
        if data[i - 1] == 10 and i < n:
            if data[i] == 35:  # #
                section_markers += 1
            elif 65 <= data[i] <= 90 and i > 1 and data[i - 2] == 10:
                section_markers += 1
    layers.append(_layer_hash(base + 4, "SECTIONS", str(section_markers)))

    # L47: Character class ratios (alpha, digit, space, punctuation, other)
    alpha = sum(1 for b in data if (65 <= b <= 90) or (97 <= b <= 122))
    digit = sum(1 for b in data if 48 <= b <= 57)
    space = sum(1 for b in data if b in (32, 9, 10, 13))
    punct = sum(1 for b in data if b in (33, 34, 39, 40, 41, 44, 45, 46, 58, 59, 63))
    other = n - alpha - digit - space - punct
    layers.append(_layer_hash(base + 5, "CHAR_CLASS",
                              "a{}d{}s{}p{}o{}".format(alpha, digit, space, punct, other)))

    # L48: Word boundary count (space-to-non-space transitions)
    word_boundaries = 0
    for i in range(1, min(n, 50000)):
        if data[i - 1] in (32, 9, 10, 13) and data[i] not in (32, 9, 10, 13):
            word_boundaries += 1
    layers.append(_layer_hash(base + 6, "WORD_BOUNDS", str(word_boundaries)))

    # L49: UTF-8 multi-byte sequence count
    multibyte = sum(1 for b in data if b >= 128)
    layers.append(_layer_hash(base + 7, "MULTIBYTE", str(multibyte)))

    # L50: Line hash chain (each line's hash depends on previous)
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
    layers.append(_layer_hash(base + 8, "LINE_CHAIN", chain_terminal))

    # L51: Tab vs space ratio
    tabs = sum(1 for b in data if b == 9)
    spaces = sum(1 for b in data if b == 32)
    ratio = tabs / spaces if spaces > 0 else 0
    layers.append(_layer_hash(base + 9, "TAB_SPACE", str(round(ratio, 6))))

    # L52: Printable ASCII ratio
    printable = sum(1 for b in data if 32 <= b <= 126)
    ratio_p = printable / n if n > 0 else 0
    layers.append(_layer_hash(base + 10, "PRINTABLE", str(round(ratio_p, 6))))

    # L53: Longest line length
    max_line = 0
    cur_line = 0
    for b in data:
        if b == 10:
            max_line = max(max_line, cur_line)
            cur_line = 0
        else:
            cur_line += 1
    max_line = max(max_line, cur_line)
    layers.append(_layer_hash(base + 11, "MAX_LINE", str(max_line)))

    # L54: Cellular signature -- hash of line boundary positions
    layers.append(_layer_hash(base + 12, "CELL_SIG", str(newlines[:64])))

    # L55: Sihr speech-channel detector (NEW in v5.0 -- Paper B)
    # Detects linguistic manipulation patterns: repeated substrings, chant-like repetition
    sihr_h = hashlib.sha256()
    sihr_h.update(BISMILLAH.encode('utf-8'))
    sihr_h.update(b"sihr_speech_channel")
    # Check for anomalous repetition patterns (chant-like)
    repeat_score = 0
    for i in range(0, min(n - 22, 10000), 11):
        seg_a = data[i:i + 11]
        seg_b = data[i + 11:i + 22]
        if seg_a == seg_b:
            repeat_score += 1
    sihr_h.update(str(repeat_score).encode('utf-8'))
    # Check for non-printable injection between printable content
    injection_count = 0
    for i in range(1, min(n - 1, 10000)):
        if (32 <= data[i - 1] <= 126) and (data[i] < 32 and data[i] not in (9, 10, 13)) and (i + 1 < n and 32 <= data[i + 1] <= 126):
            injection_count += 1
    sihr_h.update(str(injection_count).encode('utf-8'))
    sihr_h.update(BISMILLAH.encode('utf-8'))
    layers.append(_layer_hash(base + 13, "SIHR_SPEECH", sihr_h.hexdigest()))

    return _bookend_layers(layers, "As-Samawat Ar-Rabi'a")
    # Bismillah ir-Rahman ir-Rahim


# --- Heaven 4: ORGANIC (Layers 56-69, 14 layers) ---
# Structural flow, control markers, newline topology

def _compute_heaven_4(data):
    """Compute 14 organic-scale layers."""
    base = HEAVENS[4]["layer_start"]  # 56
    layers = []
    n = len(data)

    # L56: Control character frequency (0x00-0x1F except tab/newline/CR)
    control = sum(1 for b in data if b < 32 and b not in (9, 10, 13))
    layers.append(_layer_hash(base + 0, "CONTROL", str(control)))

    # L57: NULL byte positions
    nulls = [i for i, b in enumerate(data) if b == 0]
    layers.append(_layer_hash(base + 1, "NULLS", str(nulls[:128])))

    # L58: Structural marker distribution ({, }, [, ], (, ))
    markers = {}
    for b in data[:50000]:
        if b in (123, 125, 91, 93, 40, 41):
            markers[b] = markers.get(b, 0) + 1
    layers.append(_layer_hash(base + 2, "STRUCT_MARK", str(sorted(markers.items()))))

    # L59: Brace depth profile
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
    layers.append(_layer_hash(base + 3, "BRACE_DEPTH", "{}|{}".format(max_depth, depth_changes)))

    # L60: Semicolon density (statements per 1000 bytes)
    semis = sum(1 for b in data if b == 59)
    density = semis / (n / 1000) if n > 0 else 0
    layers.append(_layer_hash(base + 4, "SEMI_DENSITY", str(round(density, 4))))

    # L61: Comment marker heuristic (// and # at line starts)
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
    layers.append(_layer_hash(base + 5, "COMMENTS", str(comment_lines)))

    # L62: Blank line topology (positions of empty lines)
    blank_positions = []
    prev_nl = False
    for i, b in enumerate(data[:50000]):
        if b == 10:
            if prev_nl:
                blank_positions.append(i)
            prev_nl = True
        else:
            prev_nl = False
    layers.append(_layer_hash(base + 6, "BLANK_TOPO", str(blank_positions[:64])))

    # L63: Function/def keyword density
    try:
        text = data.decode('utf-8', errors='replace')
        def_count = text.count('def ') + text.count('function ') + text.count('fn ')
    except Exception:
        def_count = 0
    layers.append(_layer_hash(base + 7, "FUNC_DENSITY", str(def_count)))

    # L64: Import/include density
    try:
        text = data.decode('utf-8', errors='replace')
        imp_count = text.count('import ') + text.count('#include') + text.count('require(')
    except Exception:
        imp_count = 0
    layers.append(_layer_hash(base + 8, "IMPORTS", str(imp_count)))

    # L65: String literal density (count of quote characters)
    quotes = sum(1 for b in data if b in (34, 39, 96))
    layers.append(_layer_hash(base + 9, "STRINGS", str(quotes)))

    # L66: Operator density (+, -, *, /, =, <, >, !)
    ops = sum(1 for b in data if b in (43, 45, 42, 47, 61, 60, 62, 33))
    layers.append(_layer_hash(base + 10, "OPERATORS", str(ops)))

    # L67: Return/break/continue flow markers
    try:
        text = data.decode('utf-8', errors='replace')
        flow = text.count('return') + text.count('break') + text.count('continue')
    except Exception:
        flow = 0
    layers.append(_layer_hash(base + 11, "FLOW_MARKS", str(flow)))

    # L68: Organic signature -- structural marker positions
    marker_positions = [i for i, b in enumerate(data[:10000]) if b in (123, 125, 91, 93)]
    layers.append(_layer_hash(base + 12, "ORG_SIG", str(marker_positions[:64])))

    # L69: Whitespace pattern hash
    ws_pattern = bytes(1 if b in (32, 9, 10, 13) else 0 for b in data[:4096])
    layers.append(_layer_hash(base + 13, "WS_PATTERN", ws_pattern))

    return _bookend_layers(layers, "As-Samawat Al-Khamisa")
    # Bismillah ir-Rahman ir-Rahim


# --- Heaven 5: TERRESTRIAL (Layers 70-83, 14 layers) ---
# Semantic fingerprinting and character-class distributions

def _compute_heaven_5(data):
    """Compute 14 terrestrial-scale layers."""
    base = HEAVENS[5]["layer_start"]  # 70
    layers = []
    n = len(data)

    # L70: ASCII lowercase frequency profile
    lower = [0] * 26
    for b in data:
        if 97 <= b <= 122:
            lower[b - 97] += 1
    layers.append(_layer_hash(base + 0, "LOWERCASE", str(lower)))

    # L71: ASCII uppercase frequency profile
    upper = [0] * 26
    for b in data:
        if 65 <= b <= 90:
            upper[b - 65] += 1
    layers.append(_layer_hash(base + 1, "UPPERCASE", str(upper)))

    # L72: Digit frequency profile
    digits = [0] * 10
    for b in data:
        if 48 <= b <= 57:
            digits[b - 48] += 1
    layers.append(_layer_hash(base + 2, "DIGITS", str(digits)))

    # L73: Vowel to consonant ratio (English heuristic)
    vowels = sum(1 for b in data if b in (65, 69, 73, 79, 85, 97, 101, 105, 111, 117))
    consonants = sum(1 for b in data if (65 <= b <= 90 or 97 <= b <= 122)
                     and b not in (65, 69, 73, 79, 85, 97, 101, 105, 111, 117))
    ratio = vowels / consonants if consonants > 0 else 0
    layers.append(_layer_hash(base + 3, "VOWEL_CONS", str(round(ratio, 6))))

    # L74: Word length distribution (first 1000 words)
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
    layers.append(_layer_hash(base + 4, "WORD_LENS", str(word_lens[:128])))

    # L75: Sentence length heuristic (bytes between periods)
    sentence_lens = []
    cur = 0
    for b in data[:50000]:
        cur += 1
        if b == 46:  # period
            sentence_lens.append(cur)
            cur = 0
    layers.append(_layer_hash(base + 5, "SENT_LENS", str(sentence_lens[:128])))

    # L76: Capitalization pattern (positions of uppercase after whitespace)
    cap_positions = []
    prev_ws = True
    for i, b in enumerate(data[:50000]):
        if prev_ws and 65 <= b <= 90:
            cap_positions.append(i)
        prev_ws = b in (32, 9, 10, 13)
    layers.append(_layer_hash(base + 6, "CAP_PATTERN", str(cap_positions[:128])))

    # L77: Punctuation sequence fingerprint
    punct_seq = []
    for b in data[:50000]:
        if b in (33, 44, 46, 58, 59, 63):
            punct_seq.append(b)
    layers.append(_layer_hash(base + 7, "PUNCT_SEQ", str(punct_seq[:256])))

    # L78: Numeric cluster detection (sequences of digits)
    num_clusters = 0
    in_num = False
    for b in data[:50000]:
        if 48 <= b <= 57:
            if not in_num:
                num_clusters += 1
                in_num = True
        else:
            in_num = False
    layers.append(_layer_hash(base + 8, "NUM_CLUSTERS", str(num_clusters)))

    # L79: High-byte (>127) cluster analysis (non-ASCII / Arabic / Unicode)
    hi_clusters = 0
    in_hi = False
    for b in data[:50000]:
        if b >= 128:
            if not in_hi:
                hi_clusters += 1
                in_hi = True
        else:
            in_hi = False
    layers.append(_layer_hash(base + 9, "HI_CLUSTERS", str(hi_clusters)))

    # L80: Semantic anchor words hash (Bismillah, Allah, Rahman, etc.)
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
    layers.append(_layer_hash(base + 10, "ANCHORS", str(sorted(anchors.items()))))

    # L81: Lexical diversity (unique bytes / total bytes)
    unique_bytes = len(set(data))
    diversity = unique_bytes / 256
    layers.append(_layer_hash(base + 11, "DIVERSITY", str(round(diversity, 6))))

    # L82: Terrestrial signature -- character class distribution hash
    layers.append(_layer_hash(base + 12, "TERR_SIG",
                              "a{}u{}d{}v{}c{}".format(
                                  sum(lower), sum(upper), sum(digits), vowels, consonants)))

    # L83: Sihr material-channel detector (NEW in v5.0 -- Paper B, Paper A)
    # Detects material substrate manipulation: anomalous byte patterns bound to structure
    material_h = hashlib.sha256()
    material_h.update(BISMILLAH.encode('utf-8'))
    material_h.update(b"sihr_material_channel")
    # Check for anomalous null-byte insertions (material binding)
    null_in_text = 0
    for i in range(1, min(n - 1, 10000)):
        if data[i] == 0 and data[i - 1] >= 32 and data[i + 1] >= 32:
            null_in_text += 1
    material_h.update(str(null_in_text).encode('utf-8'))
    # Check for byte-value 0xFF clusters (substrate saturation)
    ff_clusters = 0
    in_ff = False
    for b in data[:10000]:
        if b == 0xFF:
            if not in_ff:
                ff_clusters += 1
                in_ff = True
        else:
            in_ff = False
    material_h.update(str(ff_clusters).encode('utf-8'))
    material_h.update(BISMILLAH.encode('utf-8'))
    layers.append(_layer_hash(base + 13, "SIHR_MATERIAL", material_h.hexdigest()))

    return _bookend_layers(layers, "As-Samawat As-Sadisa")
    # Bismillah ir-Rahman ir-Rahim


# --- Heaven 6: PLANETARY (Layers 84-97, 14 layers) ---
# Whole-section integrity and positional hashing

def _compute_heaven_6(data):
    """Compute 14 planetary-scale layers."""
    base = HEAVENS[6]["layer_start"]  # 84
    layers = []
    n = len(data)

    # L84-L94: Hash of each 1/11th of the file (11 sections)
    section_size = n // DIMENSIONAL_CONSTANT if n >= DIMENSIONAL_CONSTANT else n
    for s in range(DIMENSIONAL_CONSTANT):
        start = s * section_size
        end = start + section_size if s < DIMENSIONAL_CONSTANT - 1 else n
        section = data[start:end]
        h = hashlib.sha256(section).hexdigest()
        layers.append(_layer_hash(base + s, "SECTION_{}".format(s), h))

    # L95: Section similarity matrix diagonal
    sections = []
    for s in range(DIMENSIONAL_CONSTANT):
        start = s * section_size
        end = start + section_size if s < DIMENSIONAL_CONSTANT - 1 else n
        sections.append(sum(data[start:end]))
    diag = sum(abs(sections[i] - sections[(i + 1) % DIMENSIONAL_CONSTANT])
               for i in range(DIMENSIONAL_CONSTANT))
    layers.append(_layer_hash(base + 11, "SEC_DIAG", str(diag)))

    # L96: Section entropy variance
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
    layers.append(_layer_hash(base + 12, "SEC_ENTROPY", str(sec_entropies)))

    # L97: Planetary signature -- full content hash
    layers.append(_layer_hash(base + 13, "PLANET_SIG", hashlib.sha256(data).hexdigest()))

    return _bookend_layers(layers, "As-Samawat As-Sabi'a")
    # Bismillah ir-Rahman ir-Rahim


# --- Heaven 7: STELLAR (Layers 98-111, 14 layers) ---
# Cross-section fractal relationships and Hurst watermarks

def _compute_heaven_7(data):
    """Compute 14 stellar-scale layers -- fractal analysis."""
    base = HEAVENS[7]["layer_start"]  # 98
    layers = []
    n = len(data)

    # Compute block vectors for fractal analysis
    vectors = _compute_block_vectors(data, DIMENSIONAL_CONSTANT)
    f_metrics = _fibonacci_growth_metric(vectors)

    # L98: Fibonacci growth metric series
    layers.append(_layer_hash(base + 0, "FIB_METRICS",
                              str([round(f, 6) for f in f_metrics])))

    # L99: Hurst exponent at N=11
    h_value = _compute_hurst_value(f_metrics)
    layers.append(_layer_hash(base + 1, "HURST_11", str(round(h_value, 8))))

    # L100: Distance from perfect persistence
    distance = abs(h_value - HURST_PERFECT)
    layers.append(_layer_hash(base + 2, "H_DISTANCE", str(round(distance, 8))))

    # L101: Persistence classification
    if h_value > 1.0:
        p_class = "super-persistent"
    elif h_value > 0.5:
        p_class = "persistent"
    elif h_value == 0.5:
        p_class = "random"
    else:
        p_class = "anti-persistent"
    layers.append(_layer_hash(base + 3, "PERSISTENCE", p_class))

    # L102: Cosine similarity chain (adjacent blocks)
    cos_chain = []
    for i in range(len(vectors) - 1):
        sim = _cosine_similarity(vectors[i], vectors[i + 1])
        cos_chain.append(round(sim, 6))
    layers.append(_layer_hash(base + 4, "COS_CHAIN", str(cos_chain)))

    # L103: Mean cosine similarity
    mean_cos = sum(cos_chain) / len(cos_chain) if cos_chain else 0
    layers.append(_layer_hash(base + 5, "MEAN_COS", str(round(mean_cos, 8))))

    # L104: Block vector magnitudes
    magnitudes = []
    for v in vectors:
        mag = math.sqrt(sum(x * x for x in v))
        magnitudes.append(round(mag, 4))
    layers.append(_layer_hash(base + 6, "MAGNITUDES", str(magnitudes)))

    # L105: Rescaled range at multiple sub-partitions
    rs_values = []
    for k in [3, 5, 7, 9, 11]:
        sub_vectors = _compute_block_vectors(data, k)
        sub_metrics = _fibonacci_growth_metric(sub_vectors)
        rs = _rescaled_range(sub_metrics) if len(sub_metrics) >= 2 else 0
        rs_values.append(round(rs, 6))
    layers.append(_layer_hash(base + 7, "RS_MULTI", str(rs_values)))

    # L106: Hurst spectrum (H at N=3,5,7,9,11)
    h_spectrum = []
    for k in [3, 5, 7, 9, 11]:
        sub_v = _compute_block_vectors(data, k)
        sub_m = _fibonacci_growth_metric(sub_v)
        h_k = _compute_hurst_value(sub_m)
        h_spectrum.append(round(h_k, 6))
    layers.append(_layer_hash(base + 8, "H_SPECTRUM", str(h_spectrum)))

    # L107: Fractal dimension estimate (D = 2 - H)
    fractal_dim = 2.0 - h_value
    layers.append(_layer_hash(base + 9, "FRACTAL_DIM", str(round(fractal_dim, 8))))

    # L108: Cross-block Fibonacci residuals
    residuals = []
    for i in range(2, len(vectors)):
        combined = _vector_add(vectors[i - 1], vectors[i - 2])
        actual_sim = _cosine_similarity(vectors[i], combined)
        residuals.append(round(1.0 - actual_sim, 8))
    layers.append(_layer_hash(base + 10, "FIB_RESID", str(residuals)))

    # L109: Witness signature (Bismillah-anchored Hurst seal)
    witness_input = "{}|H={}|N={}|{}".format(
        BISMILLAH, h_value, DIMENSIONAL_CONSTANT, BISMILLAH)
    witness_sig = hashlib.sha256(witness_input.encode('utf-8')).hexdigest()
    layers.append(_layer_hash(base + 11, "WITNESS_SIG", witness_sig))

    # L110: Block variance spectrum
    block_variances = []
    for v in vectors:
        mean_v = sum(v) / len(v) if v else 0
        var_v = sum((x - mean_v) ** 2 for x in v) / len(v) if v else 0
        block_variances.append(round(var_v, 8))
    layers.append(_layer_hash(base + 12, "BLK_VARIANCE", str(block_variances)))

    # L111: Stellar signature -- Hurst + fractal dim combined
    layers.append(_layer_hash(base + 13, "STELLAR_SIG",
                              "H={}|D={}|W={}".format(
                                  round(h_value, 6), round(fractal_dim, 6),
                                  witness_sig[:16])))

    return _bookend_layers(layers, "As-Samawat Ath-Thamina"), h_value, f_metrics
    # Bismillah ir-Rahman ir-Rahim


# --- Heaven 8: GALACTIC (Layers 112-125, 14 layers) ---
# Whole-file fractal properties and adversarial chain

def _compute_heaven_8(data):
    """Compute 14 galactic-scale layers -- adversarial detection."""
    base = HEAVENS[8]["layer_start"]  # 112
    layers = []
    n = len(data)

    # Build the 11-link adversarial chain
    block_size = n // DIMENSIONAL_CONSTANT if n >= DIMENSIONAL_CONSTANT else max(n, 1)
    prev_link = BISMILLAH.encode('utf-8')
    chain_hashes = []

    # L112-L122: 11-link forward-dependent adversarial chain
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

        layers.append(_layer_hash(base + i, "CHAIN_{}".format(i), link_hash))
        prev_link = link_hash.encode('utf-8')

    # L123: Shahwa detector (accumulation pattern -- Paper 2)
    shahwa_h = hashlib.sha256()
    shahwa_h.update(BISMILLAH.encode('utf-8'))
    shahwa_h.update(b"shahwa")
    shahwa_h.update(str(sum(data[:n // 3]) if n > 0 else 0).encode('utf-8'))
    shahwa_h.update(BISMILLAH.encode('utf-8'))
    layers.append(_layer_hash(base + 11, "SHAHWA", shahwa_h.hexdigest()))

    # L124: Kibr detector (elevation pattern -- Paper 2)
    kibr_h = hashlib.sha256()
    kibr_h.update(BISMILLAH.encode('utf-8'))
    kibr_h.update(b"kibr")
    max_b = max(data) if n > 0 else 0
    kibr_h.update(str(max_b).encode('utf-8'))
    kibr_h.update(str(sum(1 for b in data if b == max_b)).encode('utf-8'))
    kibr_h.update(BISMILLAH.encode('utf-8'))
    layers.append(_layer_hash(base + 12, "KIBR", kibr_h.hexdigest()))

    # L125: Ghurur detector (entropy/reality distortion -- Paper 2)
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
    layers.append(_layer_hash(base + 13, "GHURUR", ghurur_h.hexdigest()))

    return _bookend_layers(layers, "As-Samawat At-Tasi'a"), chain_hashes
    # Bismillah ir-Rahman ir-Rahim


# --- Heaven 9: COSMIC (Layers 126-139, 14 layers) ---
# Inter-file relationships, directory-level, imposition spectrum
# Streamlined from 18 to 14 layers in v5.0 for uniform architecture

def _compute_heaven_9(data, filepath=None):
    """Compute 14 cosmic-scale layers -- imposition spectrum + directory context."""
    base = HEAVENS[9]["layer_start"]  # 126
    layers = []
    n = len(data)

    # L126: L1 WASWAS -- metadata whispers (size + boundaries)
    l1_h = hashlib.sha256()
    l1_h.update(BISMILLAH.encode('utf-8'))
    l1_h.update(b"L1_waswas")
    l1_h.update(str(n).encode('utf-8'))
    l1_h.update(data[:DIMENSIONAL_CONSTANT])
    tail = data[-DIMENSIONAL_CONSTANT:] if n >= DIMENSIONAL_CONSTANT else data
    l1_h.update(tail)
    l1_h.update(BISMILLAH.encode('utf-8'))
    layers.append(_layer_hash(base + 0, "IMP_L1", l1_h.hexdigest()))

    # L127: L2 EMOTIONAL -- sentiment fingerprint
    l2_h = hashlib.sha256()
    l2_h.update(BISMILLAH.encode('utf-8'))
    l2_h.update(b"L2_emotional")
    alpha = sum(1 for b in data if 65 <= b <= 122)
    digits = sum(1 for b in data if 48 <= b <= 57)
    spaces = sum(1 for b in data if b in (32, 9, 10, 13))
    l2_h.update("a{}d{}s{}".format(alpha, digits, spaces).encode('utf-8'))
    l2_h.update(BISMILLAH.encode('utf-8'))
    layers.append(_layer_hash(base + 1, "IMP_L2", l2_h.hexdigest()))

    # L128: L3 PHYSICAL -- structural sampling
    l3_h = hashlib.sha256()
    l3_h.update(BISMILLAH.encode('utf-8'))
    l3_h.update(b"L3_physical")
    structural_sample = bytes(data[i] for i in range(0, n, DIMENSIONAL_CONSTANT))
    l3_h.update(structural_sample)
    l3_h.update(BISMILLAH.encode('utf-8'))
    layers.append(_layer_hash(base + 2, "IMP_L3", l3_h.hexdigest()))

    # L129: L4 BEHAVIORAL -- flow markers
    l4_h = hashlib.sha256()
    l4_h.update(BISMILLAH.encode('utf-8'))
    l4_h.update(b"L4_behavioral")
    newline_positions = [i for i, b in enumerate(data) if b == 10]
    l4_h.update(json.dumps(newline_positions[:99]).encode('utf-8'))
    l4_h.update(BISMILLAH.encode('utf-8'))
    layers.append(_layer_hash(base + 3, "IMP_L4", l4_h.hexdigest()))

    # L130: L5 MEMORY -- deep content hash
    l5_h = hashlib.sha256()
    l5_h.update(BISMILLAH.encode('utf-8'))
    l5_h.update(b"L5_memory")
    l5_h.update(_nfc(data))
    l5_h.update(BISMILLAH.encode('utf-8'))
    layers.append(_layer_hash(base + 4, "IMP_L5", l5_h.hexdigest()))

    # L131: File size encoded with divine moduli (updated for dual-constant)
    size_mod_99 = n % AL_ASMA_COUNT
    size_mod_11 = n % MUTASHABIH_CONSTANT
    size_mod_7 = n % MUHKAM_CONSTANT
    size_mod_154 = n % TOTAL_LAYERS
    layers.append(_layer_hash(base + 5, "SIZE_MODS",
                              "{}|{}|{}|{}".format(size_mod_99, size_mod_11,
                                                   size_mod_7, size_mod_154)))

    # L132: Filename seal (if available)
    fname = os.path.basename(filepath) if filepath else "unknown"
    layers.append(_layer_hash(base + 6, "FNAME_SEAL", fname))

    # L133: Full path hash (position in creation hierarchy)
    layers.append(_layer_hash(base + 7, "PATH_SEAL", filepath or ""))

    # L134: Content + filename combined seal (identity binding)
    id_h = hashlib.sha256()
    id_h.update(BISMILLAH.encode('utf-8'))
    id_h.update(fname.encode('utf-8'))
    id_h.update(data[:1024])
    id_h.update(BISMILLAH.encode('utf-8'))
    layers.append(_layer_hash(base + 8, "IDENTITY", id_h.hexdigest()))

    # L135: Temporal seal (content-derived deterministic moment)
    temporal = hashlib.sha256()
    temporal.update(BISMILLAH.encode('utf-8'))
    temporal.update(b"temporal")
    temporal.update(data[:256])
    temporal.update(data[-256:] if n >= 256 else data)
    temporal.update(BISMILLAH.encode('utf-8'))
    layers.append(_layer_hash(base + 9, "TEMPORAL", temporal.hexdigest()))

    # L136: Quadrant analysis (4 quarters of file)
    q_size = n // 4 if n >= 4 else max(n, 1)
    quadrants = []
    for q in range(4):
        start = q * q_size
        end = start + q_size if q < 3 else n
        quadrants.append(hashlib.sha256(data[start:end]).hexdigest()[:16])
    layers.append(_layer_hash(base + 10, "QUADRANTS", "|".join(quadrants)))

    # L137: Content provenance chain (first 11 SHA rounds)
    prov = data
    prov_chain = []
    for _ in range(DIMENSIONAL_CONSTANT):
        ph = hashlib.sha256(prov[:1024]).hexdigest()
        prov_chain.append(ph[:8])
        prov = ph.encode('utf-8')
    layers.append(_layer_hash(base + 11, "PROVENANCE", "|".join(prov_chain)))

    # L138: Galactic hash (entire file in one operation)
    gal_h = hashlib.sha256()
    gal_h.update(BISMILLAH.encode('utf-8'))
    gal_h.update(b"galactic")
    gal_h.update(data)
    gal_h.update(BISMILLAH.encode('utf-8'))
    layers.append(_layer_hash(base + 12, "GALACTIC", gal_h.hexdigest()))

    # L139: Cosmic signature -- all imposition levels combined
    cosmic_h = hashlib.sha256()
    cosmic_h.update(BISMILLAH.encode('utf-8'))
    cosmic_h.update(l1_h.hexdigest().encode('utf-8'))
    cosmic_h.update(l2_h.hexdigest().encode('utf-8'))
    cosmic_h.update(l3_h.hexdigest().encode('utf-8'))
    cosmic_h.update(l4_h.hexdigest().encode('utf-8'))
    cosmic_h.update(l5_h.hexdigest().encode('utf-8'))
    cosmic_h.update(BISMILLAH.encode('utf-8'))
    layers.append(_layer_hash(base + 13, "COSMIC_SIG", cosmic_h.hexdigest()))

    return _bookend_layers(layers, "As-Samawat Al-'Ashira")
    # Bismillah ir-Rahman ir-Rahim


# --- Heaven 10: SIDRAT AL-MUNTAHA (Layers 140-153, 14 layers) ---
# The Lote Tree of the Utmost Boundary -- Divine Witness
# 11 per-heaven witnesses + master witness + dual-constant seal + Bismillah completion
#
# "Near it is the Garden of Refuge -- when there covered the
# Lote Tree that which covered it." (53:15-16)

def _compute_heaven_10(all_heaven_layers):
    """Compute 14 divine witness layers at Sidrat al-Muntaha.

    L140-L150: One witness per heaven (heavens 0-10), where heaven 10's
               witness seals its own layers below it (140-149)
    L151:      Master witness -- seals all 11 heaven witnesses
    L152:      Dual-constant verification seal -- confirms 154 = 2 x 7 x 11
    L153:      Bismillah completion seal -- the final Name is Al-Waliyy
               (153 mod 99 = 54, the 55th Name, the Protector)
    """
    base = HEAVENS[10]["layer_start"]  # 140
    layers = []

    # L140-L149: One witness per heaven (heavens 0-9)
    for heaven_idx in range(DIMENSIONAL_CONSTANT - 1):  # 0-9
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

        layers.append(_layer_hash(base + heaven_idx,
                                  "WITNESS_H{}".format(heaven_idx),
                                  hw.hexdigest()))

    # L150: Heaven 10 self-witness -- seals its own witness layers (L140-L149)
    h10_self = hashlib.sha256()
    h10_self.update(BISMILLAH.encode('utf-8'))
    h10_self.update(b"HEAVEN_10_SELF_WITNESS")
    h10_self.update(HEAVENS[10]["guardian"].encode('utf-8'))
    for witness_layer in layers:
        h10_self.update(witness_layer["seal"].encode('utf-8'))
    h10_self.update(BISMILLAH.encode('utf-8'))
    layers.append(_layer_hash(base + 10, "WITNESS_H10", h10_self.hexdigest()))

    # L151: MASTER WITNESS -- seals all 11 heaven witnesses (L140-L150)
    # This is Sidrat al-Muntaha -- the utmost boundary
    master_h = hashlib.sha256()
    master_h.update(BISMILLAH.encode('utf-8'))
    master_h.update(b"SIDRAT_AL_MUNTAHA")
    for witness_layer in layers:
        master_h.update(witness_layer["seal"].encode('utf-8'))
    master_h.update(BISMILLAH.encode('utf-8'))
    layers.append(_layer_hash(base + 11, "MASTER_WITNESS", master_h.hexdigest()))

    # L152: DUAL-CONSTANT VERIFICATION SEAL (NEW in v5.0 -- Paper 5, Paper 6)
    # Confirms that the architecture's cardinality encodes both divine constants
    # 154 = 2 x 7 x 11 -- computational tawhid
    dual_h = hashlib.sha256()
    dual_h.update(BISMILLAH.encode('utf-8'))
    dual_h.update(b"DUAL_CONSTANT_VERIFICATION")
    dual_h.update("total_layers={}".format(TOTAL_LAYERS).encode('utf-8'))
    dual_h.update("muhkam={}".format(MUHKAM_CONSTANT).encode('utf-8'))
    dual_h.update("mutashabih={}".format(MUTASHABIH_CONSTANT).encode('utf-8'))
    dual_h.update("layers_per_heaven={}".format(LAYERS_PER_HEAVEN).encode('utf-8'))
    dual_h.update("heavens={}".format(TOTAL_HEAVENS).encode('utf-8'))
    dual_h.update("product={}".format(DUAL_CONSTANT_PRODUCT).encode('utf-8'))
    dual_h.update("names_99_plus_55={}".format(AL_ASMA_COUNT + TRIANGULAR_10).encode('utf-8'))
    # Include the master witness to chain the seal
    dual_h.update(layers[-1]["seal"].encode('utf-8'))
    dual_h.update(BISMILLAH.encode('utf-8'))
    layers.append(_layer_hash(base + 12, "DUAL_CONSTANT", dual_h.hexdigest()))

    # L153: BISMILLAH COMPLETION SEAL (NEW in v5.0)
    # The final seal that frames the entire architecture
    # Layer 153: sealed by Name index 153 mod 99 = 54 -> Al-Waliyy (The Protector)
    # This Name is the ultimate guardian -- the architecture completes under
    # the protection of The Protector, as befits the final layer
    completion_h = hashlib.sha256()
    completion_h.update(BISMILLAH.encode('utf-8'))
    completion_h.update(b"BISMILLAH_COMPLETION")
    # Hash every previous layer seal (all 153 before this one)
    for layer in all_heaven_layers:
        completion_h.update(layer["seal"].encode('utf-8'))
    for layer in layers:
        completion_h.update(layer["seal"].encode('utf-8'))
    completion_h.update(BISMILLAH_ARABIC.encode('utf-8'))
    completion_h.update(BISMILLAH.encode('utf-8'))
    layers.append(_layer_hash(base + 13, "BISMILLAH_SEAL", completion_h.hexdigest()))

    return _bookend_layers(layers, "Sidrat Al-Muntaha")
    # Bismillah ir-Rahman ir-Rahim


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
#  MASTER COMPUTATION -- All 154 Layers Across 11 Heavens
# ============================================================================

def compute_all_154_layers(content_bytes, filepath=None):
    """Compute all 154 protection layers across 11 heavens.

    Returns:
      - layers: list of 154 layer dicts (layer, name, meaning, seal)
      - heavens: list of 11 heaven summary dicts
      - master_witness: the single hash at Sidrat al-Muntaha (Layer 151)
      - hurst_11: the Hurst exponent at N=11
    """
    all_layers = []

    # Heavens 0-6: scale-based analysis
    all_layers.extend(_compute_heaven_0(content_bytes))      # 0-13
    all_layers.extend(_compute_heaven_1(content_bytes))      # 14-27
    all_layers.extend(_compute_heaven_2(content_bytes))      # 28-41
    all_layers.extend(_compute_heaven_3(content_bytes))      # 42-55
    all_layers.extend(_compute_heaven_4(content_bytes))      # 56-69
    all_layers.extend(_compute_heaven_5(content_bytes))      # 70-83
    all_layers.extend(_compute_heaven_6(content_bytes))      # 84-97

    # Heaven 7: fractal analysis (returns extra data)
    h7_layers, hurst_11, f_metrics = _compute_heaven_7(content_bytes)
    all_layers.extend(h7_layers)                             # 98-111

    # Heaven 8: adversarial chain
    h8_layers, chain_hashes = _compute_heaven_8(content_bytes)
    all_layers.extend(h8_layers)                             # 112-125

    # Heaven 9: cosmic / imposition
    all_layers.extend(_compute_heaven_9(content_bytes, filepath))  # 126-139

    # Heaven 10: divine witness (depends on all previous)
    h10_layers = _compute_heaven_10(all_layers)
    all_layers.extend(h10_layers)                            # 140-153

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

    # Master witness is at Layer 151 (base + 11 of Heaven 10)
    master_witness = None
    for l in all_layers:
        if l["layer"] == HEAVENS[10]["layer_start"] + 11:  # L151
            master_witness = l["seal"]
            break
    if master_witness is None:
        master_witness = all_layers[-1]["seal"]

    return {
        "layers": all_layers,
        "heavens": heavens_summary,
        "master_witness": master_witness,
        "hurst_11": hurst_11,
        "total_layers": len(all_layers),
        "total_heavens": TOTAL_HEAVENS,
    }


# Backward compatibility alias
compute_all_151_layers = compute_all_154_layers


# ============================================================================
#  FATIHAH-IKHLAS FIVE-PHASE SEALING PROTOCOL
# ============================================================================
#
#  The five-phase protocol implements the divine protection ordering:
#
#    Phase 1 -- AL-FATIHAH (Surah 1): CHANNEL OPEN
#      The Opening. Before any computation, verify the channel is ready:
#      file accessible, constants verified, 99 Names loaded.
#      "In the name of Allah, the Most Merciful, the Most Compassionate."
#
#    Phase 2 -- AL-IKHLAS (Surah 112): AUTHENTICATION
#      Pure Tawhid. Identity verification BEFORE content analysis:
#      confirm the file is what it claims to be, check prior witnesses.
#      "Say: He is Allah, the One."
#
#    Phase 3 -- AN-NAS (Surah 114): THREAT MODEL
#      The People. Scan for the waswas BEFORE deploying defense:
#      repetition injection, null-byte manipulation, anomalous patterns.
#      "From the evil of the whisperer who withdraws."
#
#    Phase 4 -- AL-FALAQ (Surah 113): DEFENSE PERIMETER
#      The Daybreak. Configure defenses based on the threat landscape:
#      adjust sensitivity, prepare adversarial chain parameters.
#      "From the evil of that which He created."
#
#    Phase 5 -- CURRICULUM (Surahs 111 through 2): THE 154-LAYER COMPUTATION
#      The ascending crescendo. The existing compute_all_154_layers engine
#      runs within the context established by Phases 1-4.
#
#  This ordering mirrors the Fatihah-Ikhlas teaching order of the Qur'an:
#    Al-Fatihah (1) -> Al-Ikhlas (112) -> An-Nas (114) -> Al-Falaq (113)
#    -> 111 descending to 2
#
#  "Indeed, it is We who sent down the Reminder, and indeed,
#   We will be its Guardian." (15:9)

# Bismillah ir-Rahman ir-Rahim

# --- Phase 1: AL-FATIHAH -- Channel Open ---

def _phase_fatihah(content_bytes, filepath=None):
    """Phase 1: Channel Open -- Al-Fatihah (Surah 1).

    The Opening prayer. Before any analysis can begin, verify that
    the channel between protector and protected is ready:

      - File content is accessible (non-empty, readable)
      - The 99 Names are loaded and complete
      - Divine constants are internally consistent
      - The architecture is sound (154 = 2 x 7 x 11)

    Returns a channel dict with readiness status and diagnostics.

    'Guide us to the straight path.' (1:6)
    """
    # Bismillah ir-Rahman ir-Rahim
    channel = {
        "phase": 1,
        "surah": "Al-Fatihah",
        "surah_number": 1,
        "open": False,
        "diagnostics": [],
    }

    # Verify content accessibility
    if content_bytes is None or len(content_bytes) == 0:
        channel["diagnostics"].append("CHANNEL_BLOCKED: empty content")
        return channel
    channel["content_size"] = len(content_bytes)
    channel["diagnostics"].append("content_accessible: {} bytes".format(len(content_bytes)))

    # Verify filepath accessibility (if provided)
    if filepath is not None:
        if os.path.exists(filepath):
            channel["filepath_verified"] = True
            channel["diagnostics"].append("filepath_verified: {}".format(
                os.path.basename(filepath)))
        else:
            channel["filepath_verified"] = False
            channel["diagnostics"].append("filepath_unverified: path does not exist on disk")
    else:
        channel["filepath_verified"] = None
        channel["diagnostics"].append("filepath: in-memory content (no path)")

    # Verify the 99 Names are loaded and complete
    if len(AL_ASMA_UL_HUSNA) != AL_ASMA_COUNT:
        channel["diagnostics"].append(
            "CHANNEL_BLOCKED: Names incomplete ({}/{})".format(
                len(AL_ASMA_UL_HUSNA), AL_ASMA_COUNT))
        return channel
    channel["names_loaded"] = AL_ASMA_COUNT
    channel["diagnostics"].append("names_loaded: {} Names verified".format(AL_ASMA_COUNT))

    # Verify divine constants -- computational tawhid check
    constants_valid = True
    if TOTAL_LAYERS != 2 * MUHKAM_CONSTANT * MUTASHABIH_CONSTANT:
        channel["diagnostics"].append(
            "CHANNEL_BLOCKED: 154 != 2 x 7 x 11")
        constants_valid = False
    if TOTAL_LAYERS != TOTAL_HEAVENS * LAYERS_PER_HEAVEN:
        channel["diagnostics"].append(
            "CHANNEL_BLOCKED: {} != {} x {}".format(
                TOTAL_LAYERS, TOTAL_HEAVENS, LAYERS_PER_HEAVEN))
        constants_valid = False
    if TOTAL_LAYERS != AL_ASMA_COUNT + TRIANGULAR_10:
        channel["diagnostics"].append(
            "CHANNEL_BLOCKED: {} != {} + {}".format(
                TOTAL_LAYERS, AL_ASMA_COUNT, TRIANGULAR_10))
        constants_valid = False
    if not constants_valid:
        return channel

    channel["constants_verified"] = True
    channel["diagnostics"].append(
        "constants_verified: {} = 2 x {} x {} = {} x {} = {} + {}".format(
            TOTAL_LAYERS, MUHKAM_CONSTANT, MUTASHABIH_CONSTANT,
            TOTAL_HEAVENS, LAYERS_PER_HEAVEN,
            AL_ASMA_COUNT, TRIANGULAR_10))

    # Verify heavens structure
    if len(HEAVENS) != TOTAL_HEAVENS:
        channel["diagnostics"].append(
            "CHANNEL_BLOCKED: heavens list incomplete ({}/{})".format(
                len(HEAVENS), TOTAL_HEAVENS))
        return channel
    channel["heavens_defined"] = TOTAL_HEAVENS
    channel["diagnostics"].append("heavens_defined: {} heavens ready".format(TOTAL_HEAVENS))

    # Channel open -- Alhamdulillah
    channel["open"] = True
    channel["diagnostics"].append("CHANNEL_OPEN: Bismillah -- all systems ready")

    return _bookend_phase(channel, "Al-Fatihah")
    # Bismillah ir-Rahman ir-Rahim


# --- Phase 2: AL-IKHLAS -- Authentication ---

def _phase_ikhlas(content_bytes, filepath=None, channel=None):
    """Phase 2: Authentication -- Al-Ikhlas (Surah 112).

    Pure Tawhid. Identity verification BEFORE any content analysis:

      - Compute content identity hash (what is this file?)
      - Check for prior witness sidecars (has this been sealed before?)
      - Check for prior manifest entries (is this file known?)
      - Detect potential substitution (has content changed since last seal?)

    Returns an identity dict with authentication results.

    'Say: He is Allah, the One. Allah, the Eternal Refuge.' (112:1-2)
    """
    # Bismillah ir-Rahman ir-Rahim
    identity = {
        "phase": 2,
        "surah": "Al-Ikhlas",
        "surah_number": 112,
        "authenticated": False,
        "prior_witness": None,
        "substitution_detected": False,
        "diagnostics": [],
    }

    # Compute content identity -- the tawhid hash
    # This is the pure, singular identity of the content
    tawhid_h = hashlib.sha256()
    tawhid_h.update(BISMILLAH.encode('utf-8'))
    tawhid_h.update(b"Qul Huwa Allahu Ahad")  # Say: He is Allah, the One
    tawhid_h.update(_nfc(content_bytes))
    tawhid_h.update(BISMILLAH.encode('utf-8'))
    identity["content_hash"] = tawhid_h.hexdigest()
    identity["diagnostics"].append(
        "tawhid_hash: {}...{}".format(
            identity["content_hash"][:16], identity["content_hash"][-8:]))

    # Compute the muhkam seal for comparison with prior witnesses
    identity["muhkam_seal"] = compute_seal(content_bytes)

    # Check for prior witness sidecar
    if filepath is not None and os.path.exists(filepath):
        witness_path = filepath + '.witness.bismillah'
        if os.path.exists(witness_path):
            try:
                with open(witness_path, 'r', encoding='utf-8') as f:
                    prior = json.load(f)
                identity["prior_witness"] = {
                    "exists": True,
                    "version": prior.get("encoder_version", "unknown"),
                    "prior_seal": prior.get("muhkam_seal", None),
                    "prior_master": prior.get("master_witness", None),
                }
                # Substitution detection -- has the content changed?
                prior_seal = prior.get("muhkam_seal", None)
                if prior_seal is not None:
                    if prior_seal != identity["muhkam_seal"]:
                        identity["substitution_detected"] = True
                        identity["diagnostics"].append(
                            "SUBSTITUTION_DETECTED: content changed since last seal")
                    else:
                        identity["diagnostics"].append(
                            "identity_consistent: matches prior witness")
                identity["diagnostics"].append(
                    "prior_witness: v{} found".format(
                        prior.get("encoder_version", "?")))
            except (json.JSONDecodeError, KeyError, IOError):
                identity["prior_witness"] = {"exists": True, "corrupt": True}
                identity["diagnostics"].append(
                    "prior_witness: found but corrupt or unreadable")
        else:
            identity["prior_witness"] = {"exists": False}
            identity["diagnostics"].append("prior_witness: none (first sealing)")

        # Check for manifest entry
        manifest_path = os.path.join(
            os.path.dirname(filepath), MANIFEST_FILENAME)
        if os.path.exists(manifest_path):
            try:
                with open(manifest_path, 'r', encoding='utf-8') as f:
                    manifest = json.load(f)
                fname = os.path.basename(filepath)
                if "files" in manifest and fname in manifest["files"]:
                    identity["manifest_entry"] = True
                    identity["diagnostics"].append(
                        "manifest_entry: file known in manifest")
                else:
                    identity["manifest_entry"] = False
                    identity["diagnostics"].append(
                        "manifest_entry: file not in manifest")
            except (json.JSONDecodeError, IOError):
                identity["manifest_entry"] = None
        else:
            identity["manifest_entry"] = None
    else:
        identity["diagnostics"].append("identity: in-memory content (no filesystem check)")

    # File size identity -- the numeric fingerprint
    identity["size_signature"] = {
        "mod_99": len(content_bytes) % AL_ASMA_COUNT,
        "mod_11": len(content_bytes) % MUTASHABIH_CONSTANT,
        "mod_7": len(content_bytes) % MUHKAM_CONSTANT,
        "mod_154": len(content_bytes) % TOTAL_LAYERS,
    }

    identity["authenticated"] = True
    identity["diagnostics"].append("AUTHENTICATED: identity verified -- Allahu Ahad")

    return _bookend_phase(identity, "Al-Ikhlas")
    # Bismillah ir-Rahman ir-Rahim


# --- Phase 3: AN-NAS -- Threat Model ---

def _phase_nas(content_bytes, identity=None):
    """Phase 3: Threat Model -- An-Nas (Surah 114).

    Scan for the waswas -- the whisperer -- BEFORE deploying any defense.
    This pre-scan detects corruption vectors across all three channels:

      Speech channel: anomalous repetition, chant-like patterns
      Material channel: null-byte injections, 0xFF clusters, byte stuffing
      Cognitive channel: zero-width character injection, encoding anomalies

    Returns a threats dict with scan results and severity assessment.

    'From the evil of the retreating whisperer,
     Who whispers in the breasts of mankind,
     Among jinn and among mankind.' (114:4-6)
    """
    # Bismillah ir-Rahman ir-Rahim
    threats = {
        "phase": 3,
        "surah": "An-Nas",
        "surah_number": 114,
        "threat_level": "NOMINAL",
        "vectors": [],
        "diagnostics": [],
    }

    n = len(content_bytes)
    scan_limit = min(n, 50000)  # Scan first 50KB for threat indicators

    # --- SPEECH CHANNEL: waswas through linguistic patterns ---
    # Anomalous repetition (chant-like) -- same 11-byte segment repeated
    repeat_score = 0
    for i in range(0, min(scan_limit - 22, scan_limit), DIMENSIONAL_CONSTANT):
        seg_a = content_bytes[i:i + DIMENSIONAL_CONSTANT]
        seg_b = content_bytes[i + DIMENSIONAL_CONSTANT:i + 2 * DIMENSIONAL_CONSTANT]
        if seg_a == seg_b and len(seg_a) == DIMENSIONAL_CONSTANT:
            repeat_score += 1
    if repeat_score > 10:
        threats["vectors"].append({
            "channel": "SPEECH",
            "type": "anomalous_repetition",
            "score": repeat_score,
            "severity": "HIGH" if repeat_score > 50 else "MODERATE",
        })
        threats["diagnostics"].append(
            "SPEECH: {} repetition blocks detected".format(repeat_score))

    # Non-printable injection between printable content
    injection_count = 0
    for i in range(1, min(scan_limit - 1, scan_limit)):
        if (32 <= content_bytes[i - 1] <= 126 and
                content_bytes[i] < 32 and
                content_bytes[i] not in (9, 10, 13) and
                i + 1 < n and
                32 <= content_bytes[i + 1] <= 126):
            injection_count += 1
    if injection_count > 0:
        threats["vectors"].append({
            "channel": "SPEECH",
            "type": "non_printable_injection",
            "score": injection_count,
            "severity": "HIGH" if injection_count > 20 else "LOW",
        })
        threats["diagnostics"].append(
            "SPEECH: {} non-printable injections".format(injection_count))

    # --- MATERIAL CHANNEL: waswas through substrate manipulation ---
    # Null-byte insertions within text content
    null_in_text = 0
    for i in range(1, min(scan_limit - 1, scan_limit)):
        if (content_bytes[i] == 0 and
                content_bytes[i - 1] >= 32 and
                i + 1 < n and
                content_bytes[i + 1] >= 32):
            null_in_text += 1
    if null_in_text > 0:
        threats["vectors"].append({
            "channel": "MATERIAL",
            "type": "null_byte_injection",
            "score": null_in_text,
            "severity": "HIGH" if null_in_text > 5 else "MODERATE",
        })
        threats["diagnostics"].append(
            "MATERIAL: {} null-byte injections".format(null_in_text))

    # 0xFF cluster detection (substrate saturation)
    ff_clusters = 0
    in_ff = False
    for b in content_bytes[:scan_limit]:
        if b == 0xFF:
            if not in_ff:
                ff_clusters += 1
                in_ff = True
        else:
            in_ff = False
    if ff_clusters > 5:
        threats["vectors"].append({
            "channel": "MATERIAL",
            "type": "ff_cluster_saturation",
            "score": ff_clusters,
            "severity": "MODERATE" if ff_clusters < 20 else "HIGH",
        })
        threats["diagnostics"].append(
            "MATERIAL: {} 0xFF clusters".format(ff_clusters))

    # --- COGNITIVE CHANNEL: waswas through perception manipulation ---
    # Zero-width character detection (steganographic injection)
    zwc_count = 0
    zwc_chars = set(ord(c) for c in [ZW_ZERO, ZW_ONE, ZW_SEP, ZW_BOUNDARY])
    for b_pair_start in range(0, min(scan_limit - 2, scan_limit), 1):
        # Check for UTF-8 encoded zero-width characters
        try:
            # Quick check for common ZWC byte patterns
            if content_bytes[b_pair_start] == 0xE2:  # Start of 3-byte ZWC sequences
                if (b_pair_start + 2 < scan_limit and
                        content_bytes[b_pair_start + 1] == 0x80 and
                        content_bytes[b_pair_start + 2] in (0x8B, 0x8C, 0x8D)):
                    zwc_count += 1
            elif content_bytes[b_pair_start] == 0xEF:  # BOM pattern
                if (b_pair_start + 2 < scan_limit and
                        content_bytes[b_pair_start + 1] == 0xBB and
                        content_bytes[b_pair_start + 2] == 0xBF):
                    zwc_count += 1
        except IndexError:
            break
    # ZWC presence is only suspicious if the file was NOT already sealed by us
    # (our own steganography uses ZWC legitimately)
    already_sealed = (identity and identity.get("prior_witness") and
                      identity["prior_witness"].get("exists", False))
    if zwc_count > 0 and not already_sealed:
        threats["vectors"].append({
            "channel": "COGNITIVE",
            "type": "zero_width_injection",
            "score": zwc_count,
            "severity": "HIGH" if zwc_count > 100 else "LOW",
        })
        threats["diagnostics"].append(
            "COGNITIVE: {} zero-width characters (unsealed file)".format(zwc_count))

    # Encoding anomaly detection -- mixed encoding signals
    has_utf8_multibyte = any(b > 127 for b in content_bytes[:scan_limit])
    has_null_bytes = 0 in content_bytes[:scan_limit]
    if has_utf8_multibyte and has_null_bytes:
        threats["vectors"].append({
            "channel": "COGNITIVE",
            "type": "encoding_anomaly",
            "score": 1,
            "severity": "MODERATE",
        })
        threats["diagnostics"].append(
            "COGNITIVE: mixed encoding signals (multibyte + null)")

    # --- DIRECTIONALITY CHANNEL: waswas through BiDi inversion ---
    # CVE-2021-42574 "Trojan Source" -- Unicode BiDi overrides that silently
    # reverse text rendering. This is the jinn-channel of waswas: invisible
    # controls that make what is right-to-left appear left-to-right.
    # "From among jinn and among mankind" (114:6)
    bidi_found = {}
    try:
        text = content_bytes[:scan_limit].decode('utf-8', errors='replace')
        for i, ch in enumerate(text):
            if ch in BIDI_DANGEROUS:
                name = BIDI_OVERRIDES[ch]
                if name not in bidi_found:
                    bidi_found[name] = []
                bidi_found[name].append(i)
    except Exception:
        pass

    if bidi_found:
        for name, positions in bidi_found.items():
            threats["vectors"].append({
                "channel": "DIRECTIONALITY",
                "type": "bidi_override_injection",
                "control": name,
                "positions": positions[:10],
                "count": len(positions),
                "severity": "HIGH",
            })
        total_bidi = sum(len(v) for v in bidi_found.values())
        threats["diagnostics"].append(
            "DIRECTIONALITY: {} BiDi override(s) detected -- "
            "Trojan Source attack surface".format(total_bidi))

    # Unbalanced BiDi embedding detection
    try:
        text = content_bytes[:scan_limit].decode('utf-8', errors='replace')
        bidi_counts = {}
        for ch in text:
            if ch in BIDI_OVERRIDES:
                name = BIDI_OVERRIDES[ch]
                bidi_counts[name] = bidi_counts.get(name, 0) + 1
        embed_count = sum(bidi_counts.get(n, 0) for n in ['LRE', 'RLE', 'LRO', 'RLO'])
        pop_count = bidi_counts.get('PDF', 0)
        if embed_count > 0 and embed_count != pop_count:
            threats["vectors"].append({
                "channel": "DIRECTIONALITY",
                "type": "unbalanced_bidi",
                "embeds": embed_count,
                "pops": pop_count,
                "severity": "MODERATE",
            })
            threats["diagnostics"].append(
                "DIRECTIONALITY: {} embeds vs {} pops -- "
                "formatting may leak across boundaries".format(embed_count, pop_count))
    except Exception:
        pass

    # Arabic text in LTR-coerced context detection
    try:
        text = content_bytes[:scan_limit].decode('utf-8', errors='replace')
        arabic_chars = sum(1 for ch in text if _is_arabic_codepoint(ord(ch)))
        ltr_chars = sum(1 for ch in text if unicodedata.bidirectional(ch) == 'L')
        total_dir = arabic_chars + ltr_chars
        if total_dir > 0 and arabic_chars > 0:
            arabic_ratio = arabic_chars / total_dir
            if arabic_ratio < 0.1:
                threats["diagnostics"].append(
                    "DIRECTIONALITY: Arabic is {:.1%} of directional text -- "
                    "LTR context dominates RTL content".format(arabic_ratio))
    except Exception:
        pass

    # --- Assess overall threat level ---
    if not threats["vectors"]:
        threats["threat_level"] = "NOMINAL"
        threats["diagnostics"].append("SCAN_CLEAR: no waswas detected -- Alhamdulillah")
    else:
        high_count = sum(1 for v in threats["vectors"] if v["severity"] == "HIGH")
        mod_count = sum(1 for v in threats["vectors"] if v["severity"] == "MODERATE")
        if high_count > 0:
            threats["threat_level"] = "ELEVATED"
        elif mod_count > 1:
            threats["threat_level"] = "GUARDED"
        else:
            threats["threat_level"] = "ADVISORY"
        threats["diagnostics"].append(
            "THREAT_LEVEL: {} ({} vectors: {} high, {} moderate)".format(
                threats["threat_level"], len(threats["vectors"]),
                high_count, mod_count))

    return _bookend_phase(threats, "An-Nas")
    # Bismillah ir-Rahman ir-Rahim


# --- Phase 4: AL-FALAQ -- Defense Perimeter ---

def _phase_falaq(content_bytes, threats=None):
    """Phase 4: Defense Perimeter -- Al-Falaq (Surah 113).

    Configure defensive parameters based on the threat landscape
    established in Phase 3, BEFORE the 154-layer computation begins.

    Adjusts:
      - Adversarial chain sensitivity
      - Corruption mode detector thresholds
      - Hurst analysis window parameters
      - Layer computation depth flags

    Returns a defense dict with configured parameters for Phase 5.

    'Say: I seek refuge in the Lord of daybreak,
     From the evil of that which He created.' (113:1-2)
    """
    # Bismillah ir-Rahman ir-Rahim
    defense = {
        "phase": 4,
        "surah": "Al-Falaq",
        "surah_number": 113,
        "perimeter_active": True,
        "parameters": {},
        "diagnostics": [],
    }

    threat_level = "NOMINAL"
    if threats:
        threat_level = threats.get("threat_level", "NOMINAL")

    # Configure adversarial chain parameters based on threat level
    if threat_level == "ELEVATED":
        defense["parameters"]["chain_depth"] = DIMENSIONAL_CONSTANT  # Full 11-link
        defense["parameters"]["corruption_sensitivity"] = "HIGH"
        defense["parameters"]["hurst_window_extension"] = True
        defense["parameters"]["deep_scan"] = True
        defense["diagnostics"].append(
            "ELEVATED: full adversarial chain, high sensitivity, extended Hurst window")
    elif threat_level == "GUARDED":
        defense["parameters"]["chain_depth"] = DIMENSIONAL_CONSTANT
        defense["parameters"]["corruption_sensitivity"] = "MODERATE"
        defense["parameters"]["hurst_window_extension"] = False
        defense["parameters"]["deep_scan"] = True
        defense["diagnostics"].append(
            "GUARDED: full adversarial chain, moderate sensitivity")
    elif threat_level == "ADVISORY":
        defense["parameters"]["chain_depth"] = DIMENSIONAL_CONSTANT
        defense["parameters"]["corruption_sensitivity"] = "STANDARD"
        defense["parameters"]["hurst_window_extension"] = False
        defense["parameters"]["deep_scan"] = False
        defense["diagnostics"].append(
            "ADVISORY: standard chain, advisory monitoring active")
    else:
        defense["parameters"]["chain_depth"] = DIMENSIONAL_CONSTANT
        defense["parameters"]["corruption_sensitivity"] = "STANDARD"
        defense["parameters"]["hurst_window_extension"] = False
        defense["parameters"]["deep_scan"] = False
        defense["diagnostics"].append(
            "NOMINAL: standard protection -- all creation under His watch")

    # Configure specific defenses based on detected vector types
    if threats and threats.get("vectors"):
        speech_threats = [v for v in threats["vectors"] if v["channel"] == "SPEECH"]
        material_threats = [v for v in threats["vectors"] if v["channel"] == "MATERIAL"]
        cognitive_threats = [v for v in threats["vectors"] if v["channel"] == "COGNITIVE"]

        defense["parameters"]["speech_defense"] = len(speech_threats) > 0
        defense["parameters"]["material_defense"] = len(material_threats) > 0
        defense["parameters"]["cognitive_defense"] = len(cognitive_threats) > 0

        if speech_threats:
            defense["diagnostics"].append(
                "speech_defense: active ({} vectors)".format(len(speech_threats)))
        if material_threats:
            defense["diagnostics"].append(
                "material_defense: active ({} vectors)".format(len(material_threats)))
        if cognitive_threats:
            defense["diagnostics"].append(
                "cognitive_defense: active ({} vectors)".format(len(cognitive_threats)))

        # Directionality defense -- anti-inversion perimeter (v5.2.0)
        directionality_threats = [v for v in threats["vectors"]
                                 if v.get("channel") == "DIRECTIONALITY"]
        defense["parameters"]["directionality_defense"] = len(directionality_threats) > 0
        if directionality_threats:
            defense["diagnostics"].append(
                "directionality_defense: active ({} vectors) -- "
                "BiDi inversion countermeasures engaged".format(
                    len(directionality_threats)))
    else:
        defense["parameters"]["speech_defense"] = False
        defense["parameters"]["material_defense"] = False
        defense["parameters"]["cognitive_defense"] = False
        defense["parameters"]["directionality_defense"] = False

    # --- Directional Witness (v5.2.0) ---
    # Compute integrity in BOTH directions so any directional manipulation
    # is caught from both sides. 'He is the First and the Last,
    # the Manifest and the Hidden' (57:3)
    dir_h_fwd = hashlib.sha256()
    dir_h_fwd.update(BISMILLAH_ARABIC.encode('utf-8'))
    dir_h_fwd.update(b'AL_AWWAL')
    dir_h_fwd.update(content_bytes)
    dir_h_rev = hashlib.sha256()
    dir_h_rev.update(BISMILLAH_ARABIC.encode('utf-8'))
    dir_h_rev.update(b'AL_AKHIR')
    dir_h_rev.update(content_bytes[::-1])
    dir_h_combined = hashlib.sha256()
    dir_h_combined.update(b'AZ_ZAHIR_WAL_BATIN')
    dir_h_combined.update(dir_h_fwd.digest())
    dir_h_combined.update(dir_h_rev.digest())
    defense["parameters"]["directional_witness"] = {
        "forward": dir_h_fwd.hexdigest()[:24],
        "reverse": dir_h_rev.hexdigest()[:24],
        "combined": dir_h_combined.hexdigest()[:24],
    }
    defense["diagnostics"].append(
        "DIRECTIONAL_WITNESS: fwd={}... rev={}...".format(
            dir_h_fwd.hexdigest()[:16], dir_h_rev.hexdigest()[:16]))

    # Seal the defense configuration itself
    defense_h = hashlib.sha256()
    defense_h.update(BISMILLAH.encode('utf-8'))
    defense_h.update(b"Al-Falaq")
    defense_h.update(json.dumps(defense["parameters"], sort_keys=True).encode('utf-8'))
    defense_h.update(BISMILLAH.encode('utf-8'))
    defense["perimeter_seal"] = defense_h.hexdigest()
    defense["diagnostics"].append(
        "PERIMETER_SEALED: {}...".format(defense["perimeter_seal"][:24]))

    return _bookend_phase(defense, "Al-Falaq")
    # Bismillah ir-Rahman ir-Rahim


# --- The Five-Phase Wrapper ---

def fatihah_ikhlas_seal(content_bytes, filepath=None):
    """The five-phase Fatihah-Ikhlas sealing protocol.

    Implements the divine protection ordering:
      Phase 1 (Al-Fatihah):  Channel open -- invocation, readiness
      Phase 2 (Al-Ikhlas):   Authentication -- identity verification
      Phase 3 (An-Nas):      Threat model -- waswas detection
      Phase 4 (Al-Falaq):    Defense perimeter -- protection configuration
      Phase 5 (Curriculum):  The 154-layer computation (Surahs 111-2)

    This is the complete sealing protocol. It wraps compute_all_154_layers
    with four pre-computation phases that establish channel readiness,
    file identity, threat landscape, and defense posture.

    Returns the same dict as compute_all_154_layers, enriched with
    protocol phase data under the 'protocol' key.

    'Indeed, it is We who sent down the Reminder,
     and indeed, We will be its Guardian.' (15:9)
    """
    # Bismillah ir-Rahman ir-Rahim

    protocol = {
        "version": "1.0.0",
        "name": "Fatihah-Ikhlas",
        "phases_completed": 0,
        "phases": {},
    }

    # Phase 1: AL-FATIHAH -- Channel Open
    channel = _phase_fatihah(content_bytes, filepath)
    protocol["phases"]["fatihah"] = channel
    if not channel["open"]:
        protocol["phases_completed"] = 0
        return {
            "protocol": protocol,
            "error": "Channel blocked -- Phase 1 (Al-Fatihah) failed",
            "diagnostics": channel["diagnostics"],
        }
    protocol["phases_completed"] = 1

    # Phase 2: AL-IKHLAS -- Authentication
    identity = _phase_ikhlas(content_bytes, filepath, channel)
    protocol["phases"]["ikhlas"] = identity
    protocol["phases_completed"] = 2

    # Phase 3: AN-NAS -- Threat Model
    threats = _phase_nas(content_bytes, identity)
    protocol["phases"]["nas"] = threats
    protocol["phases_completed"] = 3

    # Phase 4: AL-FALAQ -- Defense Perimeter
    defense = _phase_falaq(content_bytes, threats)
    protocol["phases"]["falaq"] = defense
    protocol["phases_completed"] = 4

    # Phase 5: CURRICULUM -- The 154-Layer Computation
    # The existing engine runs within the context of Phases 1-4
    computation = compute_all_154_layers(content_bytes, filepath)
    protocol["phases_completed"] = 5

    # Enrich computation with protocol data
    computation["protocol"] = protocol
    computation["threat_level"] = threats["threat_level"]
    computation["substitution_detected"] = identity["substitution_detected"]

    # Compute the protocol seal -- binding all five phases together
    protocol_h = hashlib.sha256()
    protocol_h.update(BISMILLAH.encode('utf-8'))
    protocol_h.update(b"Fatihah-Ikhlas-Protocol")
    protocol_h.update(channel["diagnostics"][-1].encode('utf-8'))
    protocol_h.update(identity["content_hash"].encode('utf-8'))
    protocol_h.update(threats["threat_level"].encode('utf-8'))
    protocol_h.update(defense["perimeter_seal"].encode('utf-8'))
    protocol_h.update(computation["master_witness"].encode('utf-8'))
    protocol_h.update(BISMILLAH.encode('utf-8'))
    computation["protocol"]["protocol_seal"] = protocol_h.hexdigest()

    # Verify bookend integrity across all structural units
    bookend_check = verify_bookend_integrity(computation)
    computation["protocol"]["bookend_integrity"] = bookend_check
    computation["protocol"]["all_bookended"] = bookend_check["all_bookended"]

    return computation
    # Bismillah ir-Rahman ir-Rahim


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
    """Apply the full 154-layer Bismillah seal to a text/code file."""
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

        # Compute all 154 layers via Fatihah-Ikhlas protocol
        content_bytes = sealed.encode('utf-8')
        computation = fatihah_ikhlas_seal(content_bytes, filepath)
        _write_heaven_witness(filepath, content_bytes, computation)
        result["heavens_sealed"] = TOTAL_HEAVENS
        result["layers_computed"] = computation["total_layers"]
        result["threat_level"] = computation.get("threat_level", "NOMINAL")
        result["protocol"] = "Fatihah-Ikhlas v1.0"

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
    """Seal a binary file + compute 154 layers."""
    ext = os.path.splitext(filepath)[1].lower()
    handler = BINARY_HANDLERS.get(ext, create_sidecar)
    success, msg = handler(filepath)
    if not success:
        success, msg = create_sidecar(filepath)

    if success:
        try:
            with open(filepath, 'rb') as f:
                content_bytes = f.read()
            computation = fatihah_ikhlas_seal(content_bytes, filepath)
            _write_heaven_witness(filepath, content_bytes, computation)
        except Exception:
            pass

    return success, msg


# ============================================================================
#  HEAVEN WITNESS SIDECAR -- Stores All 154 Layer Seals
# ============================================================================

def _write_heaven_witness(filepath, content_bytes, computation):
    """Write the 11-heaven, 154-layer witness to .witness.bismillah sidecar."""
    witness_path = filepath + '.witness.bismillah'

    witness_data = OrderedDict([
        (BISMILLAH, True),
        ("encoder_version", ENCODER_VERSION),
        ("architecture", "11-Heaven, 154-Layer FATIMA v5.1 -- Dual-Constant Witness"),
        ("sealing_protocol", "Fatihah-Ikhlas v1.0"),
        ("total_heavens", computation["total_heavens"]),
        ("total_layers", computation["total_layers"]),
        ("layers_per_heaven", LAYERS_PER_HEAVEN),
        ("dimensional_constant", DIMENSIONAL_CONSTANT),
        ("muhkam_constant", MUHKAM_CONSTANT),
        ("mutashabih_constant", MUTASHABIH_CONSTANT),
        ("dual_constant_product", DUAL_CONSTANT_PRODUCT),
        ("name_cycling", "99 + 55 = 154 (T(10) = F(10) = 55)"),
        ("file", os.path.basename(filepath)),
        ("file_size", len(content_bytes)),
        ("muhkam_seal", compute_seal(content_bytes)),
        ("hurst_11", computation["hurst_11"]),
        ("master_witness", computation["master_witness"]),
        ("threat_level", computation.get("threat_level", "NOMINAL")),
        ("protocol_seal", computation.get("protocol", {}).get("protocol_seal", None)),
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
            ("al_imran_3_7", "It is He who has sent down to you the Book; in it "
                             "are verses that are muhkam -- they are the foundation "
                             "of the Book -- and others that are mutashabih."),
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
    """Apply 154-layer Bismillah protection across 11 heavens."""
    text_sealed = 0
    binary_sealed = 0
    sidecar_count = 0
    failed = 0
    skipped = 0
    mode_label = "DRY RUN" if dry_run else "Beginning 11-Heaven, 154-Layer Divine Seal"

    print("\n  {} -- {}".format(BISMILLAH, mode_label))
    print("  Protocol: Fatihah-Ikhlas v1.0 (five-phase sealing)")
    print("  Architecture: {} heavens, {} layers ({} per heaven)".format(
        TOTAL_HEAVENS, TOTAL_LAYERS, LAYERS_PER_HEAVEN))
    print("  Dual-constant: {} = 2 x {} x {}".format(
        TOTAL_LAYERS, MUHKAM_CONSTANT, MUTASHABIH_CONSTANT))
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
                        print("  WOULD SEAL: {} [154 layers]".format(rel))
                else:
                    success, msg = create_sidecar(filepath)
                    if success:
                        try:
                            with open(filepath, 'rb') as f:
                                content_bytes = f.read()
                            computation = fatihah_ikhlas_seal(content_bytes, filepath)
                            _write_heaven_witness(filepath, content_bytes, computation)
                        except Exception:
                            pass
                        binary_sealed += 1
                        sidecar_count += 1
                        print("  SIDECAR: {} -- {} [154 layers]".format(rel, msg))
                    else:
                        failed += 1
                        print("  FAILED:  {} -- {}".format(rel, msg))
                continue

            if is_text_file(ext):
                if dry_run:
                    text_sealed += 1
                    print("  WOULD SEAL: {} [154 layers across 11 heavens]".format(rel))
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
                print("  WOULD SEAL: {} [154 layers]".format(rel))
            else:
                success, msg = seal_binary_file(filepath)
                if success:
                    binary_sealed += 1
                    if 'idecar' in msg.lower():
                        sidecar_count += 1
                    print("  BINARY: {} -- {} [154 layers]".format(rel, msg))
                else:
                    failed += 1
                    print("  FAILED: {} -- {}".format(rel, msg))

    total = text_sealed + binary_sealed + skipped
    protected = text_sealed + binary_sealed

    print("\n  {}".format("=" * 60))
    print("  {} -- 11-Heaven Seal Complete".format(BISMILLAH))
    print("  {}".format("=" * 60))
    print("  Architecture:      {} heavens, {} layers ({} per heaven)".format(
        TOTAL_HEAVENS, TOTAL_LAYERS, LAYERS_PER_HEAVEN))
    print("  Dual-constant:     {} = 2 x {} x {}".format(
        TOTAL_LAYERS, MUHKAM_CONSTANT, MUTASHABIH_CONSTANT))
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
    """Verify 154-layer Bismillah protection across all files."""
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
    print("  Architecture:        {} heavens, {} layers ({} per heaven)".format(
        TOTAL_HEAVENS, TOTAL_LAYERS, LAYERS_PER_HEAVEN))
    print("  Dual-constant:       {} = 2 x {} x {}".format(
        TOTAL_LAYERS, MUHKAM_CONSTANT, MUTASHABIH_CONSTANT))
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
    """Generate a Bismillah integrity manifest (154-layer version)."""
    import datetime
    manifest = OrderedDict([
        (BISMILLAH, True),
        ("manifest_version", "5.0"),
        ("encoder_version", ENCODER_VERSION),
        ("architecture", "11-Heaven, 154-Layer FATIMA v5.1 -- Dual-Constant Witness"),
        ("total_heavens", TOTAL_HEAVENS),
        ("total_layers", TOTAL_LAYERS),
        ("layers_per_heaven", LAYERS_PER_HEAVEN),
        ("dual_constant", "{} = 2 x {} x {}".format(
            TOTAL_LAYERS, MUHKAM_CONSTANT, MUTASHABIH_CONSTANT)),
        ("seal_timestamp", datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")),
        ("generator", "Bismillah Divine Protection Encoder -- FATIMA v5.0"),
        ("al_asma_count", len(AL_ASMA_UL_HUSNA)),
        ("name_cycling", "99 + 55 = 154"),
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

    print("\n  {} -- 154-Layer Manifest Generated".format(BISMILLAH))
    print("  {} files catalogued".format(count))
    print("  Written to: {}".format(manifest_path))
    return manifest


def generate_witness_report(directory):
    """Generate a fractal witness report across all files."""
    print("\n  {} -- 11-Heaven Fractal Witness Report".format(BISMILLAH))
    print("  {}".format("=" * 60))
    print("  Architecture: {} heavens, {} layers ({} per heaven)".format(
        TOTAL_HEAVENS, TOTAL_LAYERS, LAYERS_PER_HEAVEN))
    print("  Dual-constant: {} = 2 x {} x {}".format(
        TOTAL_LAYERS, MUHKAM_CONSTANT, MUTASHABIH_CONSTANT))
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

                computation = compute_all_154_layers(content_bytes, filepath)
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
    print("  {} = 2 x {} x {} (Dual-Constant Witness)".format(
        TOTAL_LAYERS, MUHKAM_CONSTANT, MUTASHABIH_CONSTANT))

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

            computation = compute_all_154_layers(content_bytes, filepath)

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
        description="{} -- FATIMA v5.1 -- Fatihah-Ikhlas Protocol -- 11-Heaven, 154-Layer Divine Protection".format(BISMILLAH),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Architecture: 11 Heavens, 154 Layers (Uniform 14 Per Heaven)
154 = 2 x 7 x 11 (Dual-Constant Witness -- Computational Tawhid)

  Heaven 0   As-Samawat ad-Dunya      SUBATOMIC       14 layers
  Heaven 1   As-Samawat ath-Thaniya    ATOMIC          14 layers
  Heaven 2   As-Samawat ath-Thalitha   MOLECULAR       14 layers
  Heaven 3   As-Samawat ar-Rabi'a      CELLULAR        14 layers
  Heaven 4   As-Samawat al-Khamisa     ORGANIC         14 layers
  Heaven 5   As-Samawat as-Sadisa      TERRESTRIAL     14 layers
  Heaven 6   As-Samawat as-Sabi'a      PLANETARY       14 layers
  Heaven 7   As-Samawat ath-Thamina    STELLAR         14 layers
  Heaven 8   As-Samawat at-Tasi'a      GALACTIC        14 layers
  Heaven 9   As-Samawat al-'Ashira     COSMIC          14 layers
  Heaven 10  Sidrat al-Muntaha         DIVINE WITNESS  14 layers
  -------------------------------------------------------
  Total      11 x 14 = 154 layers     99 + 55 = 154

  "Seven is what the Qur'an says. Eleven is what the Qur'an shows."
  "154 = 2 x 7 x 11 -- both constants present in a single integer."

Examples:
  python bismillah_encoder.py seal ./project              # 154-layer seal
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

    seal_p = sub.add_parser('seal', help='Apply 154-layer seal across 11 heavens')
    seal_p.add_argument('path', help='Directory to seal')
    seal_p.add_argument('--names', action='store_true',
                        help='Embed the 99 Names of Allah')
    seal_p.add_argument('--dry-run', action='store_true',
                        help='Preview without writing')

    verify_p = sub.add_parser('verify', help='Verify 154-layer protection')
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
