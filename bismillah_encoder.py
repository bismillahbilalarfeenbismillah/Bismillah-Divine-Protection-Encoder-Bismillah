# Bismillah ir-Rahman ir-Rahim
"""
Bismillah Divine Protection Encoder -- 100% File Protection

Seals every file in a directory with the name of Allah subhanahu wa ta'ala
across multiple layers of protection, visible and invisible, so that no
file remains unprotected against shaytan, in sha Allah.

PROTECTION LAYERS:
  Layer 0 -- VISIBLE:        Bismillah ir-Rahman ir-Rahim as first/last line
  Layer 1 -- FILENAME:       Bismillah_[name]_Bismillah.[ext] (optional)
  Layer 3a -- STEGANOGRAPHIC: Zero-width Unicode encoding of the 99 Names (text)
  Layer 3b -- CODE COMMENTS:  99 Names as inline comments (code files)
  Layer 5 -- HASH SEAL:      SHA-256(Bismillah || content || Bismillah)
  Layer 6 -- BINARY METADATA: Bismillah in file metadata (OOXML, PDF, PNG, etc.)
  Layer 6b -- SIDECAR:        .bismillah companion files for resistant binaries

USAGE:
    python bismillah_encoder.py seal <path>            # Seal all files
    python bismillah_encoder.py seal <path> --names    # Seal + embed 99 Names
    python bismillah_encoder.py verify <path>          # Verify protection
    python bismillah_encoder.py manifest <path>        # Generate integrity manifest

"In the name of Allah, the Most Merciful, the Most Compassionate."
"He is Allah, other than whom there is no deity, Knower of the unseen and
the witnessed. He is the Most Merciful, the Most Compassionate." (59:22)

Author: Bilal Syed Arfeen
License: MIT -- free for the ummah, free for all of creation, in sha Allah
"""

import os
import sys
import json
import hashlib
import zipfile
import shutil
import tempfile
import argparse
import unicodedata
from collections import namedtuple
from pathlib import Path

# ═══════════════════════════════════════════════════════════════════════════
#  DIVINE CONSTANTS
# ═══════════════════════════════════════════════════════════════════════════

BISMILLAH = "Bismillah ir-Rahman ir-Rahim"
BISMILLAH_ARABIC = "بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ"

# ═══════════════════════════════════════════════════════════════════════════
#  STRUCTURED SEAL FINDINGS (Graft C04 -- Evolved Language)
#  Errors are data, not strings. Reconciled across all nine model
#  families: filepath (Claude), layer (DeepSeek, L0-L6b taxonomy),
#  code (Claude, GLM-5.3), severity (all families, three-valued),
#  message (all families). The former `operation` field is absorbed
#  into the code string.
# ═══════════════════════════════════════════════════════════════════════════

SealFinding = namedtuple("SealFinding",
                         ["filepath", "layer", "code", "severity", "message"])

SEVERITY_ERROR = "ERROR"
SEVERITY_WARNING = "WARNING"
SEVERITY_INFO = "INFO"
_VALID_SEVERITIES = (SEVERITY_ERROR, SEVERITY_WARNING, SEVERITY_INFO)

# Layer constants (domain-aligned with the encoder's own seal taxonomy)
LAYER_L0 = "L0_VISIBLE"
LAYER_L1 = "L1_FILENAME"
LAYER_L3A = "L3a_STEGANOGRAPHIC"
LAYER_L3B = "L3b_CODE_COMMENTS"
LAYER_L5 = "L5_HASH_SEAL"
LAYER_L6 = "L6_BINARY_METADATA"
LAYER_L6B = "L6b_SIDECAR"
LAYER_MANIFEST = "MANIFEST"
LAYER_SYSTEM = "SYSTEM"


def make_finding(filepath, layer, code, severity, message):
    """Build a SealFinding, rejecting unknown severity levels at construction."""
    if severity not in _VALID_SEVERITIES:
        raise ValueError("unknown severity: {} -- expected one of {}".format(
            severity, _VALID_SEVERITIES))
    return SealFinding(filepath=str(filepath), layer=layer, code=code,
                       severity=severity, message=message)

# Al-Asma ul-Husna -- The 99 Beautiful Names of Allah
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

# ═══════════════════════════════════════════════════════════════════════════
#  ZERO-WIDTH UNICODE STEGANOGRAPHY
# ═══════════════════════════════════════════════════════════════════════════

ZW_ZERO = '​'      # ZERO WIDTH SPACE = bit 0
ZW_ONE = '‌'       # ZERO WIDTH NON-JOINER = bit 1
ZW_SEP = '‍'       # ZERO WIDTH JOINER = character separator
ZW_BOUNDARY = '﻿'  # BYTE ORDER MARK = message boundary

# ═══════════════════════════════════════════════════════════════════════════
#  FILE TYPE CLASSIFICATIONS
# ═══════════════════════════════════════════════════════════════════════════

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

# Structured formats -- Bismillah prepended text would break parsers.
# Parser-sensitive and version-controlled fixtures get sidecar-only protection.
# .furqan_history: Furqan tokenizer test fixtures -- ZWC injection breaks lexer tests.
SIDECAR_ONLY_EXTENSIONS = {
    '.json', '.jsonl', '.csv', '.tsv', '.lock', '.sum', '.mod',
    '.furqan_history',
}

OOXML_EXTENSIONS = {'.docx', '.xlsx', '.pptx'}

SELF_NAME = 'bismillah_encoder.py'

# ═══════════════════════════════════════════════════════════════════════════
#  CORE ENCODING FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════

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
    """NFC-normalize text bytes so equivalent Unicode sequences hash identically.

    Binary content that fails UTF-8 decoding is returned unchanged --
    normalization applies only to text.
    """
    try:
        text = data.decode('utf-8')
        return unicodedata.normalize('NFC', text).encode('utf-8')
    except (UnicodeDecodeError, AttributeError):
        return data


def compute_seal(content_bytes):
    """Compute Bismillah-anchored integrity seal.

    Content is NFC-normalized before hashing so that equivalent Unicode
    sequences (e.g. precomposed vs decomposed Arabic) produce the same seal.
    """
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
    """Return True if this extension uses comment-based protection."""
    return ext in COMMENT_STYLES


# ═══════════════════════════════════════════════════════════════════════════
#  LAYER 0 + 3: TEXT/CODE FILE SEALING
# ═══════════════════════════════════════════════════════════════════════════

def _has_zwc_payload(content):
    """Check if content already contains a ZWC watermark payload."""
    return ZW_BOUNDARY in content


def seal_text_content(content, ext):
    """Apply Bismillah seal to text content (visible + invisible layers).

    Idempotent -- re-running on an already-sealed file is a no-op for
    both Layer 0 (visible) and Layer 3a (steganographic).
    """
    lines = content.split('\n')

    # LAYER 0 -- Visible Bismillah at start and end (idempotent)
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

    # LAYER 3a -- Steganographic watermark (idempotent -- skip if ZWC already present)
    if not is_code_file(ext) and not _has_zwc_payload(content):
        # Text/markdown: invisible zero-width encoding
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
    # Idempotency guard -- skip if already embedded
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
    """Apply the full Bismillah seal to a text/code file."""
    result = {"file": filepath, "layers": [], "findings": []}
    p = Path(filepath)
    ext = p.suffix.lower()

    if p.name == SELF_NAME:
        result["findings"].append(make_finding(
            filepath, LAYER_L0, "SEAL-TEXT-SKIPPED-SELF", SEVERITY_INFO,
            "encoder self-file is not sealed"))
        result["skipped"] = "self"
        return result

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        sealed = seal_text_content(content, ext)
        result["layers"].append("L0_VISIBLE")

        if is_code_file(ext):
            if embed_names:
                sealed = embed_99_names_code(sealed, ext)
                result["layers"].append("L3b_99_NAMES_COMMENTS")
        else:
            result["layers"].append("L3a_STEGANOGRAPHIC")
            if embed_names:
                sealed = embed_99_names_text(sealed)
                result["layers"].append("L3a_99_NAMES_ZWC")

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(sealed)

    except (UnicodeDecodeError, ValueError, OSError) as e:
        # Kimi k2.8: OSError (including PermissionError) previously
        # propagated unhandled and aborted the whole seal_directory walk.
        if isinstance(e, UnicodeDecodeError):
            code, detail = "SEAL-TEXT-SKIPPED-BINARY-CONTENT", "not UTF-8 decodable"
        elif isinstance(e, ValueError):
            code, detail = "SEAL-TEXT-SKIPPED-UNSEALABLE-CONTENT", "value error during seal"
        else:
            code, detail = "SEAL-TEXT-UNREADABLE", "unreadable"
        result["findings"].append(make_finding(
            filepath, LAYER_L0, code, SEVERITY_WARNING,
            "{}: {} ({})".format(detail, e, type(e).__name__)))
        result["skipped"] = "binary_content" if isinstance(e, (UnicodeDecodeError, ValueError)) else "unreadable"

    return result


# ═══════════════════════════════════════════════════════════════════════════
#  LAYER 6: BINARY FILE SEALING
# ═══════════════════════════════════════════════════════════════════════════

def seal_ooxml(filepath):
    """Inject Bismillah into OOXML (docx/xlsx/pptx) metadata."""
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
                                    '<dc:description>{} -- '.format(BISMILLAH)
                                )
                            elif '</cp:coreProperties>' in content:
                                content = content.replace(
                                    '</cp:coreProperties>',
                                    '  <dc:description>{}</dc:description>\n</cp:coreProperties>'.format(BISMILLAH)
                                )
                            data = content.encode('utf-8')
                            bismillah_added = True
                        else:
                            bismillah_added = True
                    zout.writestr(item, data)

                if not bismillah_added:
                    core_xml = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties"
                   xmlns:dc="http://purl.org/dc/elements/1.1/"
                   xmlns:dcterms="http://purl.org/dc/terms/">
  <dc:description>{b}</dc:description>
  <dc:subject>{b}</dc:subject>
</cp:coreProperties>'''.format(b=BISMILLAH)
                    zout.writestr('docProps/core.xml', core_xml)

        shutil.move(tmppath, filepath)
        return True, "OOXML metadata sealed"
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
        existing_subject = meta.get('/Subject', '') or ''

        if BISMILLAH in existing_author or BISMILLAH in existing_subject:
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
        return True, "PDF metadata sealed"
    except ImportError:
        return False, "pypdf not installed (pip install pypdf)"
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
        pnginfo.add_text('Description', BISMILLAH)

        tmpfd, tmppath = tempfile.mkstemp(suffix='.png')
        os.close(tmpfd)
        img.save(tmppath, pnginfo=pnginfo)
        shutil.move(tmppath, filepath)
        return True, "PNG text chunk sealed"
    except ImportError:
        return False, "Pillow not installed (pip install Pillow)"
    except Exception as e:
        return False, str(e)


def seal_jpg(filepath):
    """Inject Bismillah into JPEG EXIF."""
    try:
        from PIL import Image
        img = Image.open(filepath)
        exif = img.getexif()
        exif[0x010e] = BISMILLAH  # ImageDescription

        tmpfd, tmppath = tempfile.mkstemp(suffix='.jpg')
        os.close(tmpfd)
        img.save(tmppath, exif=exif.tobytes())
        shutil.move(tmppath, filepath)
        return True, "JPEG EXIF sealed"
    except ImportError:
        return False, "Pillow not installed (pip install Pillow)"
    except Exception as e:
        return False, str(e)


def seal_mp3(filepath):
    """Inject Bismillah into MP3 ID3 tags."""
    try:
        import mutagen
        from mutagen.id3 import ID3, COMM

        try:
            tags = ID3(filepath)
        except mutagen.id3.ID3NoHeaderError:
            tags = ID3()

        tags.add(COMM(encoding=3, lang='eng', desc='Bismillah', text=BISMILLAH))
        tags.save(filepath)
        return True, "MP3 ID3 sealed"
    except ImportError:
        return False, "mutagen not installed (pip install mutagen)"
    except Exception as e:
        return False, str(e)


def seal_flac(filepath):
    """Inject Bismillah into FLAC Vorbis comments."""
    try:
        from mutagen.flac import FLAC
        audio = FLAC(filepath)
        audio['COMMENT'] = BISMILLAH
        audio['DESCRIPTION'] = BISMILLAH
        audio.save()
        return True, "FLAC Vorbis comment sealed"
    except ImportError:
        return False, "mutagen not installed (pip install mutagen)"
    except Exception as e:
        return False, str(e)


def seal_zip(filepath):
    """Add Bismillah.txt inside ZIP archive."""
    try:
        if not zipfile.is_zipfile(filepath):
            return False, "Not a valid ZIP"

        with zipfile.ZipFile(filepath, 'a') as zf:
            if 'Bismillah.txt' not in zf.namelist():
                zf.writestr('Bismillah.txt',
                    '{b}\n\nThis archive is sealed with the divine protection of '
                    'Allah\'s Names.\n{b}\n'.format(b=BISMILLAH))
        return True, "ZIP entry sealed"
    except Exception as e:
        return False, str(e)


def create_sidecar(filepath):
    """Create companion .bismillah sidecar file with integrity hash."""
    try:
        sidecar = filepath + '.bismillah'
        if os.path.exists(sidecar):
            return True, "Sidecar already exists"

        sha256 = hashlib.sha256()
        with open(filepath, 'rb') as f:
            for chunk in iter(lambda: f.read(8192), b''):
                sha256.update(chunk)

        seal_hash = hashlib.sha256(
            (BISMILLAH + sha256.hexdigest() + BISMILLAH).encode('utf-8')
        ).hexdigest()

        content = """{b}

Divine Protection Companion for: {name}
SHA-256: {sha}
Bismillah Seal: {seal}
Protected by Al-Asma ul-Husna (The 99 Beautiful Names of Allah)

{b}
""".format(b=BISMILLAH, name=os.path.basename(filepath), sha=sha256.hexdigest(), seal=seal_hash)
        with open(sidecar, 'w', encoding='utf-8') as f:
            f.write(content)
        return True, "Sidecar created"
    except Exception as e:
        return False, str(e)


# Binary handler dispatch
BINARY_HANDLERS = {
    '.docx': seal_ooxml, '.xlsx': seal_ooxml, '.pptx': seal_ooxml,
    '.pdf': seal_pdf,
    '.png': seal_png,
    '.jpg': seal_jpg, '.jpeg': seal_jpg,
    '.mp3': seal_mp3,
    '.flac': seal_flac,
    '.zip': seal_zip,
    '.wav': create_sidecar,
    '.mp4': create_sidecar, '.mkv': create_sidecar, '.avi': create_sidecar,
    '.ttf': create_sidecar, '.otf': create_sidecar, '.woff': create_sidecar,
    '.gif': create_sidecar, '.bmp': create_sidecar, '.ico': create_sidecar,
    '.exe': create_sidecar, '.dll': create_sidecar, '.so': create_sidecar,
}


def seal_binary_file(filepath, findings=None):
    """Seal a binary file with Bismillah metadata or sidecar.

    Emits structured SealFinding entries (Graft C04, Evolved Language)
    when a findings list is supplied.

    Contract: returns (success, msg) -- same 2-tuple as v2.0.0.
    Side effect: appends to the findings list if provided. This avoids
    a return-arity change; the single caller in seal_directory passes
    its collected findings list.
    """
    ext = os.path.splitext(filepath)[1].lower()
    handler = BINARY_HANDLERS.get(ext, create_sidecar)
    success, msg = handler(filepath)
    if not success:
        primary_cause = msg  # Copilot: preserve primary cause through fallback
        if findings is not None:
            findings.append(make_finding(
                filepath, LAYER_L6, "SEAL-BINARY-FALLBACK", SEVERITY_WARNING,
                "Binary handler for {} failed ({}); falling back to sidecar".format(
                    ext or "<binary>", msg)))
        # Fall back to sidecar if metadata injection fails
        success, msg = create_sidecar(filepath)
        if success:
            msg = "Sidecar (fallback after: {})".format(primary_cause)
        elif findings is not None:
            findings.append(make_finding(
                filepath, LAYER_L6B, "SEAL-BINARY-ERROR", SEVERITY_ERROR,
                "Failed to seal binary file: {}".format(msg)))
    return success, msg


# ═══════════════════════════════════════════════════════════════════════════
#  MAIN OPERATIONS
# ═══════════════════════════════════════════════════════════════════════════

def is_text_file(ext):
    """Check if extension is a text/code file."""
    return ext in COMMENT_STYLES or ext in TEXT_EXTENSIONS


def _sorted_walk(directory, exclusions=None):
    """Deterministic os.walk wrapper with sorted dirnames and filenames.

    Yields (root, dirnames, filenames) with both lists sorted in-place.
    Applies exclusion filtering (Anti-M3 declared exclusions) when provided.

    Source: Kimi k2.8 (determinism finding -- unsorted os.walk traversal
    is a reproducibility defect) + Claude (Anti-M3 exclusions).
    """
    for root, dirnames, filenames in os.walk(directory):
        dirnames.sort()   # deterministic traversal order
        filenames.sort()  # deterministic traversal order
        if exclusions is not None:
            # Anti-M3: skip excluded directories with declared reason
            dirnames[:] = [d for d in dirnames if d not in exclusions]
        yield root, dirnames, filenames


def seal_directory(directory, embed_names=False, dry_run=False):
    """Apply complete Bismillah protection to all files in a directory.

    If dry_run=True, report what would change without writing anything.
    """
    text_sealed = 0
    binary_sealed = 0
    sidecar_count = 0
    failed = 0
    skipped = 0
    findings = []
    mode_label = "DRY RUN" if dry_run else "Beginning Divine Seal"

    print("\n  {} -- {}\n".format(BISMILLAH, mode_label))

    for dirpath, dirnames, filenames in _sorted_walk(
            directory, exclusions={'.git', '__pycache__'}):

        for fname in filenames:
            filepath = os.path.join(dirpath, fname)
            rel = os.path.relpath(filepath, directory)
            ext = Path(fname).suffix.lower()

            # Skip self and sidecar files
            if fname == SELF_NAME or fname.endswith('.bismillah'):
                skipped += 1
                continue

            # Structured formats -- sidecar only (no text injection)
            if ext in SIDECAR_ONLY_EXTENSIONS:
                if dry_run:
                    sidecar_path = filepath + '.bismillah'
                    if os.path.exists(sidecar_path):
                        skipped += 1
                        print("  SKIP:    {} -- sidecar already exists".format(rel))
                    else:
                        binary_sealed += 1
                        sidecar_count += 1
                        print("  WOULD SIDECAR: {}".format(rel))
                else:
                    success, msg = create_sidecar(filepath)
                    if success:
                        binary_sealed += 1
                        sidecar_count += 1
                        print("  SIDECAR: {} -- {}".format(rel, msg))
                    else:
                        failed += 1
                        print("  FAILED:  {} -- {}".format(rel, msg))
                continue

            # Text/code files
            if is_text_file(ext):
                if dry_run:
                    text_sealed += 1
                    layers = ["L0_VISIBLE"]
                    if is_code_file(ext):
                        if embed_names:
                            layers.append("L3b_99_NAMES_COMMENTS")
                    else:
                        layers.append("L3a_STEGANOGRAPHIC")
                        if embed_names:
                            layers.append("L3a_99_NAMES_ZWC")
                    print("  WOULD SEAL: {} [{}]".format(rel, ', '.join(layers)))
                else:
                    result = seal_text_file(filepath, embed_names=embed_names)
                    findings.extend(result.get("findings", []))
                    if result.get("skipped"):
                        skipped += 1
                    else:
                        text_sealed += 1
                        layers = result.get('layers', [])
                        print("  TEXT:   {} [{}]".format(rel, ', '.join(layers)))
                continue

            # Binary files
            # First check if already has Bismillah in raw content
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
                handler_name = "metadata" if ext in BINARY_HANDLERS else "sidecar"
                print("  WOULD SEAL: {} [{}]".format(rel, handler_name))
            else:
                success, msg = seal_binary_file(filepath, findings)
                if success:
                    binary_sealed += 1
                    if 'idecar' in msg.lower():
                        sidecar_count += 1
                    print("  BINARY: {} -- {}".format(rel, msg))
                else:
                    failed += 1
                    print("  FAILED: {} -- {}".format(rel, msg))

    total = text_sealed + binary_sealed + skipped
    protected = text_sealed + binary_sealed

    print("\n  {}".format("=" * 60))
    print("  {} -- Seal Complete".format(BISMILLAH))
    print("  {}".format("=" * 60))
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

    return {"text": text_sealed, "binary": binary_sealed, "failed": failed,
            "findings": findings}


ENCODER_VERSION = "2.0.0"
MANIFEST_FILENAME = "Bismillah_MANIFEST_Bismillah.json"


def verify_directory(directory, strict=False):
    """Verify Bismillah protection across all files.

    If strict=True, also recompute SHA-256 hashes and compare against
    the manifest (Bismillah_MANIFEST_Bismillah.json).
    """
    ZWC_BYTES = [b'\xe2\x80\x8b', b'\xe2\x80\x8c', b'\xe2\x80\x8d', b'\xef\xbb\xbf']
    total = 0
    protected = 0
    unprotected = []
    findings = []

    for dirpath, dirnames, filenames in _sorted_walk(directory, exclusions={'.git'}):

        for fname in filenames:
            fp = os.path.join(dirpath, fname)
            total += 1
            ext = os.path.splitext(fname)[1].lower()

            # Sidecar files are themselves protection
            if fname.endswith('.bismillah'):
                protected += 1
                continue

            # Has a sidecar companion
            if os.path.exists(fp + '.bismillah'):
                protected += 1
                continue

            # Text file: check for Bismillah
            if is_text_file(ext) or ext == '' or ext == '.gitignore':
                try:
                    with open(fp, 'rb') as f:
                        data = f.read(4000)
                    for zwc in ZWC_BYTES:
                        data = data.replace(zwc, b'')
                    if b'ismillah' in data or b'ISMILLAH' in data:
                        protected += 1
                        continue
                except Exception as e:
                    findings.append(make_finding(
                        fp, LAYER_SYSTEM, "VERIFY-UNREADABLE", SEVERITY_ERROR, str(e)))

            # OOXML: check inside ZIP
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
                except Exception as e:
                    findings.append(make_finding(
                        fp, LAYER_SYSTEM, "VERIFY-UNREADABLE", SEVERITY_ERROR, str(e)))

            # ZIP: check for Bismillah.txt entry
            if ext == '.zip':
                try:
                    if zipfile.is_zipfile(fp):
                        with zipfile.ZipFile(fp, 'r') as z:
                            if 'Bismillah.txt' in z.namelist():
                                protected += 1
                                continue
                except Exception as e:
                    findings.append(make_finding(
                        fp, LAYER_SYSTEM, "VERIFY-UNREADABLE", SEVERITY_ERROR, str(e)))

            # Binary strings check
            try:
                with open(fp, 'rb') as f:
                    data = f.read(8000)
                if b'ismillah' in data or b'Bismillah' in data:
                    protected += 1
                    continue
            except Exception as e:
                findings.append(make_finding(
                    fp, LAYER_SYSTEM, "VERIFY-UNREADABLE", SEVERITY_ERROR, str(e)))

            unprotected.append(os.path.relpath(fp, directory))

    pct = (protected / total * 100) if total > 0 else 0

    print("\n  {} -- Verification Report".format(BISMILLAH))
    print("  {}".format("=" * 60))
    print("  Total files:  {}".format(total))
    print("  Protected:    {}".format(protected))
    print("  Unprotected:  {}".format(len(unprotected)))
    print("  Protection:   {:.4f}%".format(pct))

    if unprotected:
        print("\n  UNPROTECTED FILES:")
        for f in unprotected:
            print("    {}".format(f))

    # Strict mode -- recompute hashes against manifest
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
            print("\n  STRICT: No manifest found at {}".format(manifest_path))
            print("  Run 'manifest' command first to generate one.")

    print("  {}".format("=" * 60))
    return {"total": total, "protected": protected, "unprotected": unprotected,
            "tampered": tampered, "findings": findings}


def verify_zahir(filepath):
    """Verify the visible surface (zahir) layers of a file (Layer 0, Layer 1, Layer 3b).

    Checks:
      - Layer 0: Visible Bismillah invocation at the start and end of text/code files
      - Layer 1: Filename follows Bismillah_..._Bismillah convention
      - Layer 3b: Al-Asma ul-Husna comment header present in code files

    Companion to the batin verification path; not yet wired into
    verify_directory (Phase 2 integration pending).
    """
    findings = []
    layers = []
    fname = os.path.basename(filepath)
    filename_sealed = fname.startswith("Bismillah") and ("Bismillah" in fname[len("Bismillah"):])
    if filename_sealed:
        layers.append(LAYER_L1)
    ext = os.path.splitext(fname)[1].lower()
    has_start = False
    has_end = False
    comments_sealed = False
    if (is_text_file(ext) or ext in ("", ".gitignore")) and ext not in SIDECAR_ONLY_EXTENSIONS:
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            for zw in (ZW_ZERO, ZW_ONE, ZW_SEP, ZW_BOUNDARY):
                content = content.replace(zw, "")
            # Boundary check: the FIRST and LAST non-empty lines. The
            # head match is never reused as the tail match -- a
            # start-only Bismillah stays one-sided even on short files.
            non_empty = [l for l in content.split("\n") if l.strip()]
            has_start = bool(non_empty) and any(
                "bismillah" in l.lower().replace("-", "") for l in non_empty[:1])
            has_end = bool(non_empty) and any(
                "bismillah" in l.lower().replace("-", "") for l in non_empty[-1:])
            if has_start and has_end:
                layers.append(LAYER_L0)
            elif has_start or has_end:
                findings.append(make_finding(
                    filepath, LAYER_L0, "SEAL-L0-ONE-SIDED", SEVERITY_WARNING,
                    "Layer 0 visible Bismillah present on only one boundary"))
            else:
                findings.append(make_finding(
                    filepath, LAYER_L0, "SEAL-L0-MISSING", SEVERITY_ERROR,
                    "Layer 0 visible Bismillah absent from start and end"))
            if "Al-Asma ul-Husna" in content:
                comments_sealed = True
                layers.append(LAYER_L3B)
        except (UnicodeDecodeError, OSError) as e:
            # PermissionError is a subclass of OSError -- caught here
            findings.append(make_finding(
                filepath, LAYER_L0, "SEAL-ZAHIR-READ-ERR", SEVERITY_WARNING,
                "Unable to inspect zahir text surface: {} ({})".format(
                    type(e).__name__, e)))
    else:
        sidecar_path = str(filepath) + ".bismillah"
        if os.path.exists(sidecar_path):
            # Sidecar existence alone is not verification -- the sidecar
            # must carry Bismillah content, and the primary must exist.
            try:
                with open(sidecar_path, "r", encoding="utf-8") as f:
                    sidecar_content = f.read()
                if "bismillah" not in sidecar_content.lower():
                    findings.append(make_finding(
                        filepath, LAYER_L6B, "SEAL-ZAHIR-SIDECAR-EMPTY",
                        SEVERITY_WARNING,
                        "Sidecar exists but carries no Bismillah content"))
                elif not os.path.exists(filepath):
                    findings.append(make_finding(
                        filepath, LAYER_L6B, "SEAL-ZAHIR-ORPHAN-SIDECAR",
                        SEVERITY_WARNING,
                        "Sidecar exists but the primary file is missing"))
                else:
                    has_start = True
                    has_end = True
                    layers.append(LAYER_L6B)
            except (UnicodeDecodeError, OSError) as e:
                findings.append(make_finding(
                    filepath, LAYER_L6B, "SEAL-ZAHIR-READ-ERR", SEVERITY_WARNING,
                    "Unable to inspect sidecar surface: {} ({})".format(
                        type(e).__name__, e)))
    passed = bool(has_start and has_end)
    return {
        "passed": passed,
        "has_start": has_start,
        "has_end": has_end,
        "filename_sealed": filename_sealed,
        "comments_sealed": comments_sealed,
        "layers": layers,
        "findings": findings,
    }


def generate_manifest(directory):
    """Generate a Bismillah integrity manifest.

    The manifest file itself is excluded from hashing -- a file can never
    contain its own hash. This exclusion is declared in the manifest header.
    """
    import datetime
    manifest = {
        BISMILLAH: True,
        "manifest_version": "2.0",
        "encoder_version": ENCODER_VERSION,
        "seal_timestamp": datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "generator": "Bismillah Divine Protection Encoder",
        "al_asma_count": len(AL_ASMA_UL_HUSNA),
        "self_exclusion": "The manifest file ({}) is excluded from hashing -- "
                          "a file cannot contain its own hash.".format(MANIFEST_FILENAME),
        "files": {}
    }

    manifest_path = os.path.join(directory, MANIFEST_FILENAME)
    count = 0
    for dirpath, dirnames, filenames in _sorted_walk(directory, exclusions={'.git'}):

        for fname in filenames:
            fpath = os.path.join(dirpath, fname)
            rel = os.path.relpath(fpath, directory)

            # Self-exclusion -- manifest cannot hash itself
            if os.path.abspath(fpath) == os.path.abspath(manifest_path):
                continue

            try:
                sha256 = hashlib.sha256()
                with open(fpath, 'rb') as f:
                    file_bytes = f.read()
                sha256.update(file_bytes)
                file_hash = sha256.hexdigest()
                manifest["files"][rel] = {
                    "sha256": file_hash,
                    "bismillah_seal": compute_seal(file_bytes),
                    "size": len(file_bytes)
                }
                count += 1
            except Exception as e:
                finding = make_finding(fpath, LAYER_MANIFEST,
                                       "MANIFEST-READ-FAILED", SEVERITY_ERROR, str(e))
                manifest["files"][rel] = {"finding": finding._asdict()}

    manifest["total_files"] = count

    with open(manifest_path, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    print("\n  {} -- Manifest Generated".format(BISMILLAH))
    print("  {} files catalogued (manifest self-excluded)".format(count))
    print("  Encoder version: {}".format(ENCODER_VERSION))
    print("  Written to: {}".format(manifest_path))

    return manifest


# ═══════════════════════════════════════════════════════════════════════════
#  COMMAND LINE INTERFACE
# ═══════════════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description="{} -- Divine Protection Encoder".format(BISMILLAH),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python bismillah_encoder.py seal ./my-project            # Seal all files
  python bismillah_encoder.py seal ./my-project --names    # Seal + embed 99 Names
  python bismillah_encoder.py verify ./my-project          # Verify protection
  python bismillah_encoder.py verify ./my-project --strict # Verify + hash check
  python bismillah_encoder.py manifest ./my-project        # Generate manifest
  python bismillah_encoder.py seal ./my-project --dry-run  # Preview without writing
  python bismillah_encoder.py decode ./my-project/README.md # Extract ZWC payloads

{}
""".format(BISMILLAH)
    )
    sub = parser.add_subparsers(dest='command')

    seal_p = sub.add_parser('seal', help='Apply Bismillah seal to all files')
    seal_p.add_argument('path', help='Directory to seal')
    seal_p.add_argument('--names', action='store_true',
                        help='Embed the 99 Names of Allah throughout all files')
    seal_p.add_argument('--dry-run', action='store_true',
                        help='Show what would change without writing anything')

    verify_p = sub.add_parser('verify', help='Verify Bismillah protection')
    verify_p.add_argument('path', help='Directory to verify')
    verify_p.add_argument('--strict', action='store_true',
                          help='Recompute SHA-256 hashes and compare against manifest')

    manifest_p = sub.add_parser('manifest', help='Generate integrity manifest')
    manifest_p.add_argument('path', help='Directory to manifest')

    decode_p = sub.add_parser('decode', help='Extract and print ZWC watermark payloads')
    decode_p.add_argument('path', help='File to decode')

    args = parser.parse_args()

    print("\n  {}".format(BISMILLAH))

    if args.command == 'seal':
        target = args.path
        if os.path.isdir(target):
            seal_directory(target, embed_names=args.names,
                           dry_run=getattr(args, 'dry_run', False))
        else:
            print("  ERROR: {} is not a directory".format(target))
            sys.exit(1)

    elif args.command == 'verify':
        target = args.path
        if os.path.isdir(target):
            result = verify_directory(target, strict=args.strict)
            # Nonzero exit when unprotected or tampered files found
            if result["unprotected"] or result.get("tampered"):
                print("\n  {}\n".format(BISMILLAH))
                sys.exit(2)
        else:
            print("  ERROR: {} is not a directory".format(target))
            sys.exit(1)

    elif args.command == 'manifest':
        target = args.path
        if os.path.isdir(target):
            generate_manifest(target)
        else:
            print("  ERROR: {} is not a directory".format(target))
            sys.exit(1)

    elif args.command == 'decode':
        target = args.path
        if os.path.isfile(target):
            try:
                with open(target, 'r', encoding='utf-8') as f:
                    content = f.read()
                payloads = extract_watermarks(content)
                if payloads:
                    print("  Found {} ZWC watermark payload(s):".format(len(payloads)))
                    for i, payload in enumerate(payloads, 1):
                        print("    [{}] {}".format(i, payload))
                else:
                    print("  No ZWC watermark payloads found in {}".format(target))
            except UnicodeDecodeError:
                print("  ERROR: {} is not a text file".format(target))
                sys.exit(1)
        else:
            print("  ERROR: {} is not a file".format(target))
            sys.exit(1)

    else:
        parser.print_help()
        sys.exit(1)

    print("\n  {}\n".format(BISMILLAH))


if __name__ == '__main__':
    main()

# Bismillah ir-Rahman ir-Rahim
