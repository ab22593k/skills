#!/usr/bin/env python3
"""
Extract text from a PDF or EPUB file for book-to-skill processing.

PDF extraction tries methods in order:
  1. PyMuPDF (fitz) — best quality for text-heavy books, header/footer removal
  2. pdftotext (poppler-utils) — fast fallback
  3. PyPDF2 — common Python library
  4. pdfminer.six — thorough fallback

EPUB extraction tries methods in order:
  1. ebooklib + BeautifulSoup4 — best quality
  2. zipfile + html.parser — stdlib fallback (no extra deps)

Outputs:
  /tmp/booqs/full_text.txt  — full extracted text
  /tmp/booqs/metadata.json  — stats and metadata
"""

import html
import html.parser
import json
import os
import re
import shutil
import subprocess
import sys
import unicodedata
import zipfile
from pathlib import Path

OUTPUT_DIR = Path("/tmp/booqs")
OUTPUT_TEXT = OUTPUT_DIR / "full_text.txt"
OUTPUT_META = OUTPUT_DIR / "metadata.json"

WORDS_PER_TOKEN = 0.75  # approximate


def estimate_tokens(text: str) -> int:
    """Estimate token count from word count using a 0.75 words/token ratio."""
    return int(len(text.split()) / WORDS_PER_TOKEN)


def _extract_block_text(block: dict) -> str:
    """Extract text from a PyMuPDF text block."""
    parts = []
    for line in block.get("lines", []):
        for span in line.get("spans", []):
            parts.append(span["text"])
    return " ".join(parts)


def _is_chapter_heading(block: dict, text: str) -> bool:  # pylint: disable=too-many-return-statements,too-many-branches
    """Check if a text block is a chapter/section heading."""
    max_font = 0
    has_bold = False
    for line in block.get("lines", []):
        for span in line.get("spans", []):
            if span["size"] > max_font:
                max_font = span["size"]
            if span["flags"] & 2:
                has_bold = True

    if not (has_bold or max_font > 14):
        return False

    text = text.strip()

    skip_patterns = [
        r"^(acknowledgments?|acknowledgement|dedication|preface|foreword|"
        r"introduction|about|abstract|copyright|table\s+of\s+contents|contents|"
        r"index|references|bibliography|appendix(?:\s+\w+)?|appendices|"
        r"author|bio(?:\s+the\s+author)?|about\s+the\s+author)$",
        r"^(notes|endnotes|footnotes)$",
    ]
    for pattern in skip_patterns:
        if re.match(pattern, text, re.IGNORECASE):
            return False

    patterns = [
        r"^chapter\s+\d+",
        r"^ch\.\s*\d+",
        r"^\d+\.\s+\w+",
        r"^[IVXLCDM]+\.",
        r"^[IVXLCDM]+\s",
    ]
    for pattern in patterns:
        if re.match(pattern, text, re.IGNORECASE):
            return True

    if has_bold and len(text) < 100:
        if re.search(r"\d", text):
            return True
        chapter_words = [
            "chapter",
            "part",
            "section",
            "introduction",
            "conclusion",
            "summary",
        ]
        if any(
            re.search(r"\b" + w + r"\b", text, re.IGNORECASE) for w in chapter_words
        ):
            return True
        if (
            text.isupper()
            and 3 <= len(text) <= 30
            and not re.match(r"^[A-Z\s]{3,}$", text)
        ):
            return True
        if text.isupper() and 3 <= len(text) <= 30:
            non_headings = {
                "ACKNOWLEDGMENTS",
                "DEDICATION",
                "PREFACE",
                "FOREWORD",
                "INTRODUCTION",
                "ABOUT",
                "ABSTRACT",
                "COPYRIGHT",
                "NOTES",
                "ENDNOTES",
                "FOOTNOTES",
                "INDEX",
                "REFERENCES",
                "BIBLIOGRAPHY",
            }
            if text not in non_headings and len(text.split()) <= 3:
                return True

    return False


def extract_with_pdftotext(pdf_path: str) -> tuple[str | None, str]:  # pylint: disable=too-many-return-statements
    # pylint: disable=import-outside-toplevel
    """Extract text using pdftotext (poppler-utils).
    Returns (text, error_message_or_None)."""
    if not shutil.which("pdftotext"):
        return None, "pdftotext not found (install poppler-utils)"
    try:
        result = subprocess.run(
            ["pdftotext", "-layout", pdf_path, "-"],
            capture_output=True,
            text=True,
            timeout=120,
            check=False,
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout, None
        if result.returncode != 0:
            return (
                None,
                f"pdftotext exited with code {result.returncode}: "
                f"{result.stderr.strip()}",
            )
        return None, "pdftotext produced empty output"
    except FileNotFoundError:
        return None, "pdftotext not found (install poppler-utils)"
    except subprocess.TimeoutExpired:
        return None, "pdftotext timed out after 120s"
    except Exception as e:  # pylint: disable=broad-exception-caught
        return None, str(e)


def extract_with_pypdf2(pdf_path: str) -> tuple[str | None, str]:
    # pylint: disable=import-outside-toplevel
    """Extract text using PyPDF2.
    Returns (text, error_message_or_None)."""
    try:
        import PyPDF2  # pylint: disable=import-outside-toplevel
    except ImportError:
        return None, "PyPDF2 not installed (pip3 install PyPDF2)"

    try:
        text_parts = []
        with open(pdf_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                try:
                    text_parts.append(page.extract_text() or "")
                except Exception:  # pylint: disable=broad-exception-caught
                    text_parts.append("")
        result = "\n".join(text_parts)
        if result.strip():
            return result, None
        return None, "PyPDF2 extracted no text"
    except Exception as e:  # pylint: disable=broad-exception-caught
        return None, str(e)


def extract_with_pdfminer(pdf_path: str) -> tuple[str | None, str]:
    # pylint: disable=import-outside-toplevel
    """Extract text using pdfminer.six.
    Returns (text, error_message_or_None)."""
    try:
        from pdfminer.high_level import extract_text  # noqa: E402
    except ImportError:
        return None, "pdfminer.six not installed (pip3 install pdfminer.six)"

    try:
        result = extract_text(pdf_path)
        if result and result.strip():
            return result, None
        return None, "pdfminer.six extracted no text"
    except ImportError:
        return None, "pdfminer.six not installed (pip3 install pdfminer.six)"
    except Exception as e:  # pylint: disable=broad-exception-caught
        return None, str(e)


def extract_with_pymupdf(
    pdf_path: str, remove_headers_footers: bool = True
) -> tuple[str | None, str]:
    # pylint: disable=import-outside-toplevel
    # pylint: disable=too-many-locals,too-many-branches,too-many-nested-blocks
    # pylint: disable=broad-exception-caught
    """Extract text using PyMuPDF (fitz) with structure preservation.
    Returns (text, error_message_or_None)."""
    try:
        import fitz  # pylint: disable=import-outside-toplevel
    except ImportError:
        return None, None

    try:
        doc = fitz.open(pdf_path)
        all_text_parts = []

        # First pass: detect headers/footers
        header_footer_texts = set()
        if remove_headers_footers and len(doc) > 3:
            # pylint: disable=import-outside-toplevel
            from collections import Counter

            candidates = []
            for page in doc:
                page_height = page.rect.height
                blocks = page.get_text("dict")["blocks"]
                for block in blocks:
                    if block["type"] != 0:
                        continue
                    y0 = block["bbox"][1]
                    y_rel = y0 / page_height
                    if y_rel < 0.05 or y_rel > 0.95:
                        block_text = _extract_block_text(block)
                        if block_text.strip():
                            candidates.append(block_text.strip())
            freq = Counter(candidates)
            header_footer_texts = {text for text, count in freq.items() if count >= 3}

        prev_ends_mid = False
        for page in doc:
            page_parts = []
            page_height = page.rect.height
            blocks = sorted(
                [b for b in page.get_text("dict")["blocks"] if b["type"] == 0],
                key=lambda b: b["bbox"][1],
            )

            for block in blocks:
                y0 = block["bbox"][1]
                y_rel = y0 / page_height
                block_text = _extract_block_text(block)

                if not block_text.strip():
                    continue

                # Skip headers/footers
                if remove_headers_footers:
                    if block_text.strip() in header_footer_texts:
                        continue
                    if y_rel < 0.05 or y_rel > 0.95:
                        continue

                # Detect chapter headings
                is_chapter = _is_chapter_heading(block, block_text)
                if is_chapter:
                    page_parts.append(f"\n[CHAPTER: {block_text.strip()}]")
                else:
                    # Paragraph reconstruction
                    if prev_ends_mid and block_text[0].islower():
                        page_parts.append(" " + block_text)
                    else:
                        page_parts.append("\n\n" + block_text)

                prev_ends_mid = bool(
                    block_text.strip() and block_text.strip()[-1] not in ".!?:\"'"
                )

            if page_parts:
                all_text_parts.append("".join(page_parts))

        doc.close()
        return "\n".join(all_text_parts), None
    except Exception as e:  # pylint: disable=broad-exception-caught
        return None, str(e)


def extract_with_ebooklib(epub_path: str) -> tuple[str | None, str]:
    # pylint: disable=import-outside-toplevel
    """Extract text using ebooklib + BeautifulSoup4 with chapter markers.
    Returns (text, error_message_or_None)."""
    try:
        import ebooklib  # noqa: E402
        from bs4 import BeautifulSoup  # noqa: E402
        from ebooklib import epub  # noqa: E402
    except ImportError:
        return (
            None,
            "ebooklib or beautifulsoup4 not installed "
            "(pip3 install ebooklib beautifulsoup4)",
        )

    try:
        book = epub.read_epub(epub_path)
        parts = []
        chapter_num = 0
        for item in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
            soup = BeautifulSoup(item.get_content(), "html.parser")
            chapter_num = _inject_chapter_markers_from_soup(soup, chapter_num, parts)
            text = soup.get_text(separator="\n")
            if text.strip():
                parts.append(text)
        result = "\n\n".join(parts)
        if result.strip():
            return result, None
        return None, "ebooklib extracted no text"
    except Exception as e:  # pylint: disable=broad-exception-caught
        return None, str(e)


def _inject_chapter_markers_from_soup(soup, chapter_num: int, parts: list):
    """Detect h1/h2/h3 tags in BeautifulSoup and add [CHAPTER:] markers.
    Returns updated chapter_num."""
    for heading in soup.find_all(["h1", "h2", "h3"]):
        heading_text = heading.get_text().strip()
        if heading_text and len(heading_text) < 200:
            if _looks_like_chapter_title(heading_text, heading.name):
                chapter_num += 1
                parts.append(f"\n[CHAPTER: {heading_text}]")
                heading.decompose()
    return chapter_num


def _looks_like_chapter_title(text: str, tag: str) -> bool:  # pylint: disable=too-many-return-statements
    """Determine if a heading element looks like a chapter/section title."""
    # h1 tags are very likely chapter headings — accept them
    if tag == "h1":
        non_chapter_h1 = {
            "copyright",
            "about",
            "abstract",
            "preface",
            "dedication",
            "acknowledgments",
            "acknowledgement",
            "foreword",
            "notes",
            "endnotes",
            "footnotes",
            "index",
            "bibliography",
            "appendix",
            "appendices",
            "author",
            "bio",
            "table of contents",
        }
        return text.strip().lower() not in non_chapter_h1

    text = text.strip()
    if not text:
        return False

    # Common non-chapter headings to skip for h2/h3
    skip_patterns = [
        r"^(acknowledgments?|acknowledgement|dedication|preface|foreword|"
        r"introduction|about|abstract|copyright|table\s+of\s+contents|contents|"
        r"index|references|bibliography|appendix(?:\s+\w+)?|appendices|"
        r"author|bio(?:\s+the\s+author)?|about\s+the\s+author)$",
        r"^(notes|endnotes|footnotes)$",
        r"^(part\s+\w+|section\s+\w+)$",
    ]
    for pattern in skip_patterns:
        if re.match(pattern, text, re.IGNORECASE):
            return False

    # h2/h3 with chapter-like patterns
    chapter_patterns = [
        r"^chapter\s+\d+",
        r"^ch\.\s*\d+",
        r"^\d+\.\s+\w+",
        r"^\d+[:\s]\s+\w+",
        r"^[IVXLCDM]+\.",
    ]
    for pattern in chapter_patterns:
        if re.match(pattern, text, re.IGNORECASE):
            return True

    # h2/h3 that are short (likely section headings)
    if tag in ("h2", "h3") and len(text) < 80:
        if re.match(r"^\d+$", text.strip()):
            return False
        return True

    return False


class _HTMLTextExtractor(html.parser.HTMLParser):
    """Minimal HTML -> plain text converter using stdlib only."""

    SKIP_TAGS = {"script", "style", "head"}

    def __init__(self):
        super().__init__()
        self._parts: list[str] = []
        self._skip_depth = 0
        self._current_skip: str | None = None

    def handle_starttag(self, tag, attrs):
        if tag in self.SKIP_TAGS:
            self._skip_depth += 1
        if tag in ("p", "br", "h1", "h2", "h3", "h4", "h5", "h6", "li", "div"):
            self._parts.append("\n")

    def handle_endtag(self, tag):
        if tag in self.SKIP_TAGS and self._skip_depth:
            self._skip_depth -= 1

    def handle_data(self, data):
        if not self._skip_depth:
            self._parts.append(data)

    def get_text(self) -> str:
        """Return the extracted text with HTML entities unescaped."""
        return html.unescape("".join(self._parts))


def extract_with_zipfile(epub_path: str) -> tuple[str | None, str]:
    """stdlib-only EPUB extractor: unzip -> parse HTML files with chapter markers.
    Returns (text, error_message_or_None)."""
    try:
        with zipfile.ZipFile(epub_path) as zf:
            names = zf.namelist()
            spine_order: list[str] = []
            opf_files = [n for n in names if n.endswith(".opf")]
            if opf_files:
                opf_text = zf.read(opf_files[0]).decode("utf-8", errors="replace")
                spine_order = re.findall(
                    r'href=["\']([^"\']+\.(?:xhtml|html))["\']', opf_text
                )

            html_files = spine_order or sorted(
                n for n in names if n.endswith((".html", ".xhtml"))
            )
            if not html_files:
                return None, "No HTML files found in EPUB"

            parts = []
            chapter_num = 0
            for name in html_files:
                try:
                    raw = zf.read(name).decode("utf-8", errors="replace")
                    chapter_num, extracted = _extract_html_with_chapters(
                        raw, chapter_num
                    )
                    if extracted:
                        parts.append(extracted)
                except Exception:  # pylint: disable=broad-exception-caught
                    continue
            result = "\n\n".join(parts)
            return (result if result.strip() else None), None
    except zipfile.BadZipFile:
        return None, "Invalid EPUB file (bad zip)"
    except Exception as e:  # pylint: disable=broad-exception-caught
        return None, str(e)


def _extract_html_with_chapters(
    raw_html: str, chapter_num: int
) -> tuple[int, str | None]:
    """Parse HTML and inject [CHAPTER:] markers for heading elements.
    Returns (updated_chapter_num, extracted_text)."""
    parser = _HTMLTextExtractorWithChapters(chapter_num)
    parser.feed(raw_html)
    return parser.chapter_num, parser.get_text()


class _HTMLTextExtractorWithChapters(html.parser.HTMLParser):
    """HTML -> plain text with [CHAPTER:] markers for heading elements."""

    SKIP_TAGS = {"script", "style", "head"}
    HEADING_TAGS = {"h1", "h2", "h3", "h4"}

    def __init__(self, start_chapter: int = 0):
        super().__init__()
        self._parts: list[str] = []
        self._skip_depth = 0
        self._current_section: list[str] = []
        self._heading_buffer: list[str] = []
        self._in_heading = False
        self.chapter_num = start_chapter

    def handle_starttag(self, tag, attrs):
        if tag in self.SKIP_TAGS:
            self._skip_depth += 1
        elif tag in self.HEADING_TAGS:
            self._flush_section()
            self._in_heading = True
            self._heading_buffer = []
        elif not self._in_heading:
            if tag in ("p", "br", "li", "div"):
                self._current_section.append("\n")

    def handle_endtag(self, tag):
        if tag in self.SKIP_TAGS and self._skip_depth:
            self._skip_depth -= 1
        elif tag in self.HEADING_TAGS and self._in_heading:
            self._in_heading = False
            heading_text = "".join(self._heading_buffer).strip()
            if heading_text and _looks_like_chapter_title(heading_text, tag):
                self.chapter_num += 1
                self._parts.append(f"[CHAPTER: {heading_text}]")

    def handle_data(self, data):
        if self._skip_depth:
            return
        if self._in_heading:
            self._heading_buffer.append(data)
        else:
            self._current_section.append(data)

    def _flush_section(self):
        text = "".join(self._current_section).strip()
        if text:
            self._parts.append(text)
        self._current_section = []

    def get_text(self) -> str:
        """Return the extracted text with HTML entities unescaped."""
        self._flush_section()
        return html.unescape("\n\n".join(self._parts))


def extract_epub(epub_path: str) -> tuple[str, str]:
    """Return (text, method) for an EPUB file."""
    print("Trying ebooklib + BeautifulSoup4...", end=" ", flush=True)
    text, err = extract_with_ebooklib(epub_path)
    if text and text.strip():
        print("OK")
        return text, "ebooklib"

    print(f"not available ({err})")
    print("Trying stdlib zipfile parser...", end=" ", flush=True)
    text, err = extract_with_zipfile(epub_path)
    if text and text.strip():
        print("OK")
        return text, "zipfile"

    print(f"FAILED ({err})")
    print(
        "\nERROR: Could not extract text from EPUB.\n"
        "Install ebooklib + beautifulsoup4 for best results:\n"
        "  pip3 install ebooklib beautifulsoup4",
        file=sys.stderr,
    )
    sys.exit(1)


def count_epub_chapters(epub_path: str) -> int:
    """Count spine items (approximate chapter count) without dependencies."""
    try:
        with zipfile.ZipFile(epub_path) as zf:
            opf_files = [n for n in zf.namelist() if n.endswith(".opf")]
            if not opf_files:
                return 0
            opf_text = zf.read(opf_files[0]).decode("utf-8", errors="replace")
            return len(re.findall(r"<itemref\b", opf_text))
    except OSError:
        return 0


def count_pages(pdf_path: str) -> dict:
    """Count pages in a PDF file.
    Returns dict with 'count' (int, -1 if unknown) and 'method' (str or None)."""
    if shutil.which("pdfinfo"):
        try:
            result = subprocess.run(
                ["pdfinfo", pdf_path],
                capture_output=True,
                text=True,
                timeout=15,
                check=False,
            )
            for line in result.stdout.splitlines():
                if line.startswith("Pages:"):
                    count_str = line.split(":")[1].strip()
                    try:
                        return {"count": int(count_str), "method": "pdfinfo"}
                    except ValueError:
                        pass
        except OSError:
            pass
    # Fallback: use PyPDF2
    try:
        # pylint: disable=import-outside-toplevel
        import PyPDF2

        with open(pdf_path, "rb") as f:
            page_count = len(PyPDF2.PdfReader(f).pages)
            return {"count": page_count, "method": "PyPDF2"}
    except OSError:
        return {"count": -1, "method": None}


def _strip_accents(text: str) -> str:
    """Remove accent marks from text using NFD decomposition."""
    nfkd = unicodedata.normalize("NFD", text)
    return "".join(c for c in nfkd if unicodedata.category(c) != "Mn")


def detect_structure(text: str) -> dict:
    """Detect chapter count and table of contents presence."""
    # Parse [CHAPTER: ...] markers from PyMuPDF extraction
    chapter_markers = re.findall(r"\[CHAPTER:\s*(.+?)\]", text)

    # Also look for traditional chapter headings in first 50K chars
    lines = text[:50000].splitlines()
    chapter_pattern = re.compile(
        r"^\s*(chapter\s+\d+|CHAPTER\s+\d+"
        r"|ch\.\s*\d+|\d+\.\s+[A-Z])",
        re.IGNORECASE,
    )
    chapters_found = [
        line.strip() for line in lines if chapter_pattern.match(line)
    ]

    # Combine both detection methods
    all_chapters = list(chapter_markers) + chapters_found

    # Look for ToC indicators (accent-normalized) in first 10K chars
    toc_keywords = ["table of contents", "contents", "indice", "sumario"]
    text_accent_free = _strip_accents(text[:10000].lower())
    has_toc = any(kw in text_accent_free for kw in toc_keywords)

# Detect ToC location
    toc_location = "none"
    if has_toc:
        toc_positions = [
            text_accent_free.find(kw)
            for kw in toc_keywords
            if text_accent_free.find(kw) >= 0
        ]
        if toc_positions:
            toc_pos = min(toc_positions)
            if toc_pos < len(text) * 0.2:
                toc_location = "start"
            elif toc_pos > len(text) * 0.8:
                toc_location = "end"
            else:
                toc_location = "middle"

    # Check if headers/footers were removed (heuristic: repeating markers)
    header_footer_removed = "[CHAPTER:" in text

    return {
        "chapters_detected": len(all_chapters),
        "chapter_headings_sample": all_chapters[:10],
        "has_toc": has_toc,
        "toc_location": toc_location,
        "header_footer_removed": header_footer_removed,
    }


def _inject_chapter_marks_from_markdown(text: str) -> str:
    """Insert [CHAPTER:] markers before markdown heading lines (## and ###)."""
    lines = text.splitlines()
    output = []
    for line in lines:
        stripped = line.strip()
        if re.match(r"^#{2,3}\s", stripped):
            heading_text = stripped.lstrip("#").strip()
            if (
                heading_text
                and len(heading_text) < 200
                and not _is_skip_heading(heading_text)
            ):
                output.append(f"\n[CHAPTER: {heading_text}]")
                continue
        output.append(line)
    return "\n".join(output)


def extract_with_docling(pdf_path: str) -> tuple[str | None, str]:
    # pylint: disable=import-outside-toplevel
    """Extract text using Docling (layout-aware, best for technical books).
    Returns (text, error_message_or_None)."""
    try:
        from docling.datamodel.base_models import InputFormat  # noqa: E402
        from docling.datamodel.pipeline_options import PdfPipelineOptions  # noqa: E402
        from docling.document_converter import (
            DocumentConverter,  # noqa: E402
            PdfFormatOption,  # noqa: E402
        )
    except ImportError:
        return None, "docling not installed (pip3 install docling)"

    try:
        pipeline_options = PdfPipelineOptions()
        pipeline_options.do_ocr = False
        pipeline_options.do_table_structure = True

        converter = DocumentConverter(
            format_options={
                InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
            }
        )
        result = converter.convert(pdf_path)
        markdown_text = result.document.export_to_markdown()
        markdown_text = _inject_chapter_marks_from_markdown(markdown_text)
        if markdown_text.strip():
            return markdown_text, None
        return None, "Docling exported empty markdown"
    except ImportError as e:
        return None, f"Docling import error: {e}"
    except Exception as e:  # pylint: disable=broad-exception-caught
        return None, str(e)


def _is_skip_heading(text: str) -> bool:
    """Check if a heading should be skipped (not a real chapter)."""
    skip_patterns = [
        r"^(acknowledgments|acknowledgement|dedication|preface|foreword|"
        r"introduction|about|abstract|copyright|"
        r"table\s+of\s+contents|contents|index|references|"
        r"bibliography|appendix|appendices|author|"
        r"bio|about\s+the\s+author)$",
        r"^(notes|endnotes|footnotes)$",
    ]
    for pattern in skip_patterns:
        if re.match(pattern, text, re.IGNORECASE):
            return True
    return False


def _handle_pdf_extraction(
    input_path: str, extraction_mode: str
) -> tuple[str, str, dict]:
    """Run PDF extraction pipeline. Returns (text, method, pages_info)."""
    text = None
    method = None
    err_msg = None

    if extraction_mode == "technical":
        print(
            "Mode: technical -- using Docling (layout-aware)...",
            end=" ",
            flush=True,
        )
        text, err_msg = extract_with_docling(input_path)
        if text:
            method = "docling"
            print("OK")
        else:
            print(f"not available ({err_msg}), falling back to pdftotext")
            extraction_mode = "text"

    if extraction_mode == "text":
        print(
            "Mode: text -- using PyMuPDF (header/footer removal, chapter detection)..."
        )
        print("Trying PyMuPDF...", end=" ", flush=True)
        text, err_msg = extract_with_pymupdf(input_path)
        if text:
            method = "pymupdf"
            print("OK")
        else:
            print(f"not available ({err_msg})")
            print("Trying pdftotext...", end=" ", flush=True)
            text, err_msg = extract_with_pdftotext(input_path)
            if text:
                method = "pdftotext"
                print("OK")
            else:
                print(f"not available ({err_msg})")
                print("Trying PyPDF2...", end=" ", flush=True)
                text, err_msg = extract_with_pypdf2(input_path)
                if text:
                    method = "PyPDF2"
                    print("OK")
                else:
                    print(f"not available ({err_msg})")
                    print("Trying pdfminer.six...", end=" ", flush=True)
                    text, err_msg = extract_with_pdfminer(input_path)
                    if text:
                        method = "pdfminer"
                        print("OK")
                    else:
                        print(f"FAILED ({err_msg})")
                        print(
                            "\nERROR: Could not extract text from PDF.\n"
                            "Install one of: poppler-utils (pdftotext), "
                            "PyPDF2, or pdfminer.six\n"
                            "  sudo apt install poppler-utils\n"
                            "  pip3 install PyPDF2\n"
                            "  pip3 install pdfminer.six",
                            file=sys.stderr,
                        )
                        sys.exit(1)

    pages_info = count_pages(input_path)
    return text, method, pages_info


def main():  # pylint: disable=too-many-locals,too-many-branches,too-many-statements
    """Entry point for the book-to-skill extraction CLI."""
    if len(sys.argv) < 2:
        print(
            "Usage: extract.py <path-to-pdf-or-epub> [--mode technical|text]",
            file=sys.stderr,
        )
        sys.exit(1)

    input_path = sys.argv[1]

    # Parse --mode flag
    extraction_mode = "text"
    if "--mode" in sys.argv:
        idx = sys.argv.index("--mode")
        if idx + 1 < len(sys.argv):
            extraction_mode = sys.argv[idx + 1].lower()
    if extraction_mode not in ("technical", "text"):
        extraction_mode = "text"

    if not os.path.exists(input_path):
        print(f"ERROR: File not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    ext = Path(input_path).suffix.lower()
    is_epub = ext == ".epub"
    is_pdf = ext == ".pdf"
    is_txt = ext in (".txt", ".md")

    if not is_epub and not is_pdf and not is_txt:
        # Sniff magic bytes as fallback
        with open(input_path, "rb") as f:
            header = f.read(8)
        if header[:4] == b"%PDF":
            is_pdf = True
        elif header[:2] == b"PK":  # ZIP magic -> likely EPUB
            is_epub = True
        else:
            print(
                f"ERROR: Unsupported format '{ext}'. Supported: .pdf, .epub, .txt, .md",
                file=sys.stderr,
            )
            sys.exit(1)

    # Warn about --mode for non-PDF formats
    if extraction_mode == "technical" and not is_pdf:
        print(
            "WARNING: --mode technical is only applicable to PDF files. "
            "For EPUB/TXT files, extraction is always text-based.",
            file=sys.stderr,
        )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    if is_txt:
        print(f"Reading text file: {input_path}")
        text = Path(input_path).read_text(encoding="utf-8", errors="replace")
        method = "text"
        pages_info = {
            "count": len(text.splitlines()) // 30,
            "method": "estimated",
        }
        pages_label = "pages"
    elif is_epub:
        print(f"Extracting EPUB: {input_path}")
        text, err = extract_epub(input_path)
        if not text:
            print(f"FAILED: {err}", file=sys.stderr)
            sys.exit(1)
        method = "ebooklib"
        pages_info = {
            "count": count_epub_chapters(input_path),
            "method": "spine",
        }
        pages_label = "spine_items"
    else:
        print(f"Extracting PDF: {input_path}")
        text, method, pages_info = _handle_pdf_extraction(input_path, extraction_mode)
        pages_label = "pages"

    # Get pages count, using -1 to indicate unknown
    pages = pages_info["count"]

    # Write full text
    OUTPUT_TEXT.write_text(text, encoding="utf-8")

    tokens = estimate_tokens(text)
    structure = detect_structure(text)
    file_size_mb = os.path.getsize(input_path) / (1024 * 1024)

    metadata = {
        "source_file": str(Path(input_path).resolve()),
        "filename": Path(input_path).name,
        "format": "epub" if is_epub else "pdf",
        "extraction_method": method,
        "extraction_mode": extraction_mode,
        "file_size_mb": round(file_size_mb, 2),
        pages_label: pages,
        "pages_method": pages_info.get("method"),
        "chars": len(text),
        "words": len(text.split()),
        "estimated_tokens": tokens,
        "estimated_tokens_human": f"~{tokens // 1000}K",
        "output_text": str(OUTPUT_TEXT),
        **structure,
    }

    OUTPUT_META.write_text(json.dumps(metadata, indent=2, ensure_ascii=False))

    page_line = f"   {'Spine items' if is_epub else 'Pages'}: {pages}"
    print("\n📖 Extraction complete:")
    print(f"   Format  : {'EPUB' if is_epub else 'PDF'}")
    print(f"   Method  : {method}")
    print(page_line)
    print(f"   Words   : {len(text.split()):,}")
    print(f"   Tokens  : ~{tokens // 1000}K")
    print(f"   Chapters: {structure['chapters_detected']} detected")
    print(
        f"   ToC     : {structure['toc_location']}"
        if structure["has_toc"]
        else "   ToC     : not detected"
    )
    print(
        f"   Headers : "
        f"{'removed' if structure.get('header_footer_removed') else 'kept'}"
    )
    print(f"\n   Text -> {OUTPUT_TEXT}")
    print(f"   Meta -> {OUTPUT_META}")


if __name__ == "__main__":
    main()
