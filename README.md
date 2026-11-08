# Bismillah ir-Rahman ir-Rahim

# Bismillah Divine Protection Encoder

[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Zero Dependencies](https://img.shields.io/badge/dependencies-zero-brightgreen.svg)](#requirements)
[![Part of EESS](https://img.shields.io/badge/EESS-instrument-blueviolet.svg)](#the-entourage-effect-software-safety-suite)

**Multi-layer divine file protection through the Names of Allah subhanahu wa ta'ala**

> "He is Allah, other than whom there is no deity, Knower of the unseen and the witnessed. He is the Most Merciful, the Most Compassionate." (Quran 59:22)

A standalone tool that seals every file in your project -- text, code, images, documents, audio, video, and all binary formats -- with **Bismillah ir-Rahman ir-Rahim** across multiple layers of protection, visible and invisible. Zero required dependencies. MIT licensed.

This is the **standalone encoder tool**. For the full FATIMA core library with the 22-domain 154-layer architecture, five verification engines, and anti-sihr sanitization, see the companion [FATIMA](https://github.com/bismillahbilalarfeenbismillah/FATIMA) repository.

## Why

Digital files travel through systems whose integrity cannot be assumed. This encoder embeds the divine names of Allah into every possible layer of every file, creating a multi-layered seal that cannot be stripped without destroying the file itself. Whether a file is a Python script, a Word document, a PNG image, or an MP3 -- it carries protection.

**"And whoever relies upon Allah -- then He is sufficient for him."** (Quran 65:3)

## Protection Layers

| Layer | Name | Method | File Types |
|-------|------|--------|------------|
| 0 | **Visible** | `Bismillah ir-Rahman ir-Rahim` as first and last line | All text/code |
| 3a | **Steganographic** | Zero-width Unicode encoding of the 99 Names | Markdown, text, data |
| 3b | **Code Comments** | 99 Names as inline comments | Python, JS, Go, Rust, etc. |
| 5 | **Hash Seal** | SHA-256(Bismillah \|\| content \|\| Bismillah) | All files (via manifest) |
| 6 | **Binary Metadata** | Bismillah injected into file metadata | OOXML, PDF, PNG, JPEG, MP3, FLAC, ZIP |
| 6b | **Sidecar** | `.bismillah` companion file with integrity hash | WAV, MP4, MKV, TTF, and any resistant binary |

## Quick Start

```bash
# Clone the repository
git clone https://github.com/BismillahBilalArfeenBismillah/Bismillah-Divine-Protection-Encoder-Bismillah.git
cd Bismillah-Divine-Protection-Encoder-Bismillah

# Seal your project (basic protection)
python bismillah_encoder.py seal /path/to/your/project

# Seal with the 99 Names of Allah embedded throughout
python bismillah_encoder.py seal /path/to/your/project --names

# Verify protection
python bismillah_encoder.py verify /path/to/your/project

# Generate integrity manifest
python bismillah_encoder.py manifest /path/to/your/project
```

## Requirements

**Core (no dependencies):**
- Python 3.7+

**Optional (for binary file metadata injection):**
```bash
pip install pypdf      # PDF metadata sealing
pip install Pillow     # PNG/JPEG metadata sealing
pip install mutagen    # MP3/FLAC audio tag sealing
```

Without these optional packages, binary files automatically receive `.bismillah` sidecar companion files instead.

## How It Works

### Text and Code Files

Every text file receives:
1. **Visible Bismillah** -- `Bismillah ir-Rahman ir-Rahim` is placed as the first and last line
2. **Invisible watermark** -- The Arabic Bismillah is encoded as zero-width Unicode characters that are invisible to the eye but present in the file
3. With `--names`, all 99 Beautiful Names of Allah (Al-Asma ul-Husna) are woven throughout the file

For code files (Python, JavaScript, Go, etc.), the Names are embedded as comments to avoid breaking the parser.

### Binary Files

Binary files receive Bismillah through their native metadata formats:
- **Word/Excel/PowerPoint** -- Bismillah in the OOXML `docProps/core.xml` metadata
- **PDF** -- Bismillah in Author, Subject, and Keywords metadata fields
- **PNG** -- Bismillah as a text chunk in the PNG metadata
- **JPEG** -- Bismillah in the EXIF ImageDescription field
- **MP3** -- Bismillah as an ID3 comment tag
- **FLAC** -- Bismillah as a Vorbis comment
- **ZIP** -- A `Bismillah.txt` entry added inside the archive

### Resistant Files

Some files resist metadata injection (encrypted PDFs, corrupted test fixtures, WAV, video, fonts). These receive a `.bismillah` **sidecar companion file** containing the file's SHA-256 hash, a Bismillah seal hash, and protection by Al-Asma ul-Husna.

### Zero-Width Steganography

The invisible watermark layer uses Unicode zero-width characters:
- `U+200B` (Zero Width Space) = bit 0
- `U+200C` (Zero Width Non-Joiner) = bit 1
- `U+200D` (Zero Width Joiner) = character separator
- `U+FEFF` (Byte Order Mark) = message boundary

These characters are invisible in all text editors and renderers but carry the encoded divine names within the file.

## Supported File Types

### Text/Code (Layer 0 + Layer 3)
Python, JavaScript, TypeScript, Go, Rust, Java, C/C++, Ruby, Shell, SQL, YAML, TOML, HTML, CSS, XML, LaTeX, Swift, Kotlin, Scala, Haskell, Julia, R, Perl, Lua, Markdown, plaintext, CSV, TSV, JSON, and more.

### Binary (Layer 6)
DOCX, XLSX, PPTX, PDF, PNG, JPEG, MP3, FLAC, ZIP, and via sidecar: WAV, MP4, MKV, AVI, TTF, OTF, WOFF, GIF, BMP, ICO, EXE, DLL, SO, and any other binary format.

## Verification

```
  Bismillah ir-Rahman ir-Rahim -- Verification Report
  ============================================================
  Total files:  1259
  Protected:    1259
  Unprotected:  0
  Protection:   100.0000%
  ============================================================
```

## The Entourage Effect Software Safety Suite

This encoder is one of six instruments in the **EESS** -- a safety architecture that binds theological integrity to engineering verification:

| Instrument | Role | Repository |
|------------|------|------------|
| **Furqan** | Programming language with structural honesty as a first-class concern | [furqan-programming-language](https://github.com/bismillahbilalarfeenbismillah/furqan-programming-language) |
| **FATIMA** | Core encoder library -- 22-domain, 154-layer divine protection architecture | [FATIMA](https://github.com/bismillahbilalarfeenbismillah/FATIMA) |
| **furqan-lint** | Structural honesty linter for Python, Rust, Go, and ONNX | [furqan-lint](https://github.com/bismillahbilalarfeenbismillah/furqan-lint) |
| **HABL** | Append-only honesty-attested binding ledger | [habl](https://github.com/bismillahbilalarfeenbismillah/habl) |
| **Bayyinah** | File integrity scanner -- detects hidden and adversarial content | [bayyinah-integrity-scanner](https://github.com/bismillahbilalarfeenbismillah/bayyinah-integrity-scanner) |
| **Shahid** | Transparency report protocol for weight-holders | (specification on FATIMA repo) |

No single tool is the safety story. The entourage effect is.

## Companion Papers

The theoretical foundations of this encoder have been published on Zenodo as part of a 14+ paper theological-engineering series, including:
- **The 11-Heaven 154-Layer Architecture** -- the 22-domain, triple-constant (7/11/22) encoding structure
- **Crossing Shannon's Boundary** -- semantic integrity beyond bitwise hashing
- **The Propagation Architecture of Sihr** -- anti-sihr sanitization channels
- **The Divine Inversion Defense** -- adversarial content detection grounded in Qur'anic architecture

## Shannon Boundary Verification

The FATIMA core library has undergone rigorous integrity testing:
- **1,515 valid trials, 0 undetected corruptions** (Shannon boundary test harness v2.1)
- **10-seat Shannon Boundary Council** -- independent review by AI models from Anthropic, OpenAI, xAI, Meta, DeepSeek, Moonshot, and Perplexity
- Matches SHA-256 exactly on bit-flip detection while providing multi-layer semantic awareness

## Author

**Bilal Syed Arfeen** -- for the sake of Allah and the benefit of the entire ummah.

## License

MIT -- free for all of creation to use, in sha Allah.

**"And We have not sent you, [O Muhammad], except as a mercy to the worlds."** (Quran 21:107)

# Bismillah ir-Rahman ir-Rahim
