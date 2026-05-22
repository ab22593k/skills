"""Unit tests for extract.py — extraction functions and type signatures."""

import sys
import os

# Add scripts to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

import pytest
from extract import (
    detect_structure,
    _is_chapter_heading,
    _looks_like_chapter_title,
    estimate_tokens,
    count_pages,
    extract_with_pdftotext,
    extract_with_pypdf2,
    extract_with_pdfminer,
    extract_with_docling,
    _inject_chapter_markers_from_soup,
    _inject_chapter_marks_from_markdown,
    _extract_html_with_chapters,
    _HTMLTextExtractorWithChapters,
)


class TestEstimateTokens:
    def test_simple_text(self):
        """75 words ≈ 100 tokens at 0.75 words/token."""
        text = "word " * 75
        result = estimate_tokens(text)
        assert result == 100

    def test_empty_text(self):
        assert estimate_tokens("") == 0

    def test_single_word(self):
        assert estimate_tokens("hello") == 1


class TestDetectStructure:
    def test_basic_chapter_markers(self):
        """Should detect [CHAPTER: ...] markers."""
        text = (
            "[CHAPTER: Introduction]\nSome text\n[CHAPTER: Data Structures]\nMore text"
        )
        result = detect_structure(text)
        assert result["chapters_detected"] == 2
        assert "Introduction" in result["chapter_headings_sample"]

    def test_no_toc_keywords(self):
        """No ToC keywords → toc_location is 'none'."""
        text = "[CHAPTER: Intro]\nJust some text here."
        result = detect_structure(text)
        assert result["has_toc"] is False
        assert result["toc_location"] == "none"

    def test_toc_location_start(self):
        """ToC near the beginning → 'start'."""
        text = "Table of Contents\n[CHAPTER: Intro]\n" + "text " * 1000
        result = detect_structure(text)
        assert result["has_toc"] is True
        assert result["toc_location"] == "start"

    def test_toc_location_middle(self):
        """ToC in the middle → 'middle'."""
        # detect_structure uses 20%/80% thresholds of total text length
        prefix = "text " * 1500  # 7500 chars
        text = (
            prefix + "Table of Contents\n" + "text " * 5000
        )  # total ~32.5K; 20%=6.5K, 80%=26K
        result = detect_structure(text)
        assert result["has_toc"] is True
        assert result["toc_location"] == "middle"

    def test_toc_location_end(self):
        """ToC near the end → 'end'."""
        text = "text " * 1000 + "Table of Contents\n" + "text " * 100
        result = detect_structure(text)
        assert result["has_toc"] is True
        assert result["toc_location"] == "end"

    def test_toc_empty_keyword_result_no_crash(self):
        """Regression: detect_structure must not crash when ToC keywords
        appear in the text but the filtered list is empty somehow.

        This was a real bug: min() on empty sequence raises ValueError.
        """
        # Text containing "contents" but with edge case
        text = "Some text about contents and more stuff " * 200
        result = detect_structure(text)
        assert "toc_location" in result
        # Should not raise ValueError

    def test_chapter_headings_sample_capped(self):
        """chapter_headings_sample should have at most 10 entries."""
        text = "\n".join(f"[CHAPTER: Ch {i}]" for i in range(15))
        result = detect_structure(text)
        assert len(result["chapter_headings_sample"]) <= 10

    def test_header_footer_removed_heuristic(self):
        """Presence of [CHAPTER: markers → header_footer_removed is True."""
        text = "[CHAPTER: Intro]\nSome text\n[CHAPTER: Body]\nMore text"
        result = detect_structure(text)
        assert result["header_footer_removed"] is True

    def test_no_chapter_markers(self):
        """No chapter markers → 0 chapters detected."""
        text = "Just some plain text without any structure."
        result = detect_structure(text)
        assert result["chapters_detected"] == 0


class TestIsChapterHeading:
    """Tests for the PyMuPDF block-level heading detector."""

    def _make_block(self, text, font_size=16, bold=True):
        """Helper to create a minimal block dict."""
        return {
            "lines": [
                {
                    "spans": [
                        {
                            "text": text,
                            "size": font_size,
                            "flags": 2 if bold else 0,
                        }
                    ]
                }
            ]
        }

    def test_chapter_number(self):
        block = self._make_block("Chapter 5")
        assert _is_chapter_heading(block, "Chapter 5") is True

    def test_ch_dot_number(self):
        block = self._make_block("Ch. 3")
        assert _is_chapter_heading(block, "Ch. 3") is True

    def test_numbered_heading(self):
        block = self._make_block("1. Introduction")
        assert _is_chapter_heading(block, "1. Introduction") is True

    def test_roman_numeral(self):
        block = self._make_block("I.")
        assert _is_chapter_heading(block, "I.") is True

    def test_skip_acknowledgments(self):
        block = self._make_block("Acknowledgments")
        assert _is_chapter_heading(block, "Acknowledgments") is False

    def test_skip_dedication(self):
        block = self._make_block("Dedication")
        assert _is_chapter_heading(block, "Dedication") is False

    def test_skip_table_of_contents(self):
        block = self._make_block("Table of Contents")
        assert _is_chapter_heading(block, "Table of Contents") is False

    def test_skip_preface(self):
        block = self._make_block("Preface")
        assert _is_chapter_heading(block, "Preface") is False

    def test_skip_notes(self):
        block = self._make_block("Notes")
        assert _is_chapter_heading(block, "Notes") is False

    def test_small_font_not_heading(self):
        """Font too small without bold → not a heading."""
        block = self._make_block("Some text", font_size=8, bold=False)
        assert _is_chapter_heading(block, "Some text") is False


class TestLooksLikeChapterTitle:
    """Tests for the standalone chapter title classifier."""

    def test_h1_always_chapter(self):
        assert _looks_like_chapter_title("Introduction", "h1") is True

    def test_h2_with_chapter_pattern(self):
        assert _looks_like_chapter_title("Chapter 1: Getting Started", "h2") is True

    def test_h2_numbered(self):
        assert _looks_like_chapter_title("1. First Things First", "h2") is True

    def test_h2_roman_numeral(self):
        assert _looks_like_chapter_title("I. Preliminaries", "h2") is True

    def test_skip_acknowledgments(self):
        assert _looks_like_chapter_title("Acknowledgments", "h2") is False

    def test_skip_dedication(self):
        assert _looks_like_chapter_title("Dedication", "h2") is False

    def test_skip_preface(self):
        assert _looks_like_chapter_title("Preface", "h2") is False

    def test_skip_foreword(self):
        assert _looks_like_chapter_title("Foreword", "h2") is False

    def test_short_h2_generic(self):
        """Short h2 without explicit markers should still match."""
        assert _looks_like_chapter_title("Performance", "h2") is True
        assert _looks_like_chapter_title("Security", "h2") is True

    def test_long_h2_no_pattern(self):
        """Long h2 without patterns — still matches since < 80 chars."""
        assert (
            _looks_like_chapter_title(
                "This is a very long section heading without numbers", "h2"
            )
            is True
        )

    def test_empty_text(self):
        assert _looks_like_chapter_title("", "h2") is False


class TestCountPages:
    def test_returns_dict_structure(self):
        """count_pages should return a dict with 'count' and 'method'."""
        result = count_pages("/non/existent/file.pdf")
        assert isinstance(result, dict)
        assert "count" in result
        assert "method" in result

    def test_nonexistent_file_returns_negative_one(self):
        result = count_pages("/non/existent/file.pdf")
        assert result["count"] == -1
        assert result["method"] is None


class TestExtractWithPdftotext:
    def test_nonexistent_tool(self):
        """Should return (None, error_string) when pdftotext is unavailable."""
        text, err = extract_with_pdftotext("/non/existent/file.pdf")
        # Either None with an error message, or file-not-found error
        assert text is None
        assert err is not None

    def test_returns_tuple(self):
        """Always returns a tuple (text_or_None, err_or_None)."""
        result = extract_with_pdftotext("/non/existent/file.pdf")
        assert isinstance(result, tuple)
        assert len(result) == 2


class TestExtractWithPypdf2:
    def test_nonexistent_file(self):
        text, err = extract_with_pypdf2("/non/existent/file.pdf")
        assert text is None
        assert err is not None

    def test_returns_tuple(self):
        result = extract_with_pypdf2("/non/existent/file.pdf")
        assert isinstance(result, tuple)
        assert len(result) == 2


class TestExtractWithPdfminer:
    def test_nonexistent_file(self):
        text, err = extract_with_pdfminer("/non/existent/file.pdf")
        assert text is None
        assert err is not None

    def test_returns_tuple(self):
        result = extract_with_pdfminer("/non/existent/file.pdf")
        assert isinstance(result, tuple)
        assert len(result) == 2


class TestExtractWithDocling:
    def test_nonexistent_file(self):
        text, err = extract_with_docling("/non/existent/file.pdf")
        assert text is None
        assert err is not None

    def test_returns_tuple(self):
        result = extract_with_docling("/non/existent/file.pdf")
        assert isinstance(result, tuple)
        assert len(result) == 2


class TestEpubChapterMarkers:
    def test_inject_chapter_markers_from_soup(self):
        """Test that _inject_chapter_markers_from_soup detects h1/h2/h3 headings."""
        try:
            from bs4 import BeautifulSoup
        except ImportError:
            pytest.skip("beautifulsoup4 not installed")

        soup = BeautifulSoup(
            "<h1>Chapter One</h1><p>Text</p><h2>Section 1.1</h2>", "html.parser"
        )
        parts = []
        num = _inject_chapter_markers_from_soup(soup, 0, parts)
        assert num == 2
        assert any("Chapter One" in p for p in parts)

    def test_looks_like_chapter_skips_preface(self):
        assert _looks_like_chapter_title("Preface", "h1") is False

    def test_looks_like_chapter_accepts_h1(self):
        """h1 tags are always treated as chapters regardless of text."""
        assert _looks_like_chapter_title("About This Book", "h1") is True


class TestHtmlChapterExtraction:
    def test_extract_html_with_chapters(self):
        """Test that _extract_html_with_chapters inserts [CHAPTER:] markers."""
        html = "<h1>Chapter 1: Start</h1><p>Paragraph one.</p><h2>Section 1.1</h2><p>Details.</p>"
        num, text = _extract_html_with_chapters(html, 0)
        assert "[CHAPTER:" in text
        assert "Chapter 1: Start" in text
        assert num == 2  # Two headings detected

    def test_html_text_extractor_with_chapters(self):
        """Test the HTMLTextExtractorWithChapters class directly."""
        html = "<h1>Introduction</h1><p>First paragraph.</p>"
        parser = _HTMLTextExtractorWithChapters(0)
        parser.feed(html)
        text = parser.get_text()
        assert "[CHAPTER:" in text or "Introduction" in text


class TestMarkdownChapterInjection:
    def test_inject_chapter_marks_from_markdown(self):
        """Test that ## headings get [CHAPTER:] markers."""
        md = "## Chapter One\nSome text\n### Section 1.1\nMore text"
        result = _inject_chapter_marks_from_markdown(md)
        assert "[CHAPTER: Chapter One]" in result

    def test_skips_non_chapter_headings_in_md(self):
        md = "## Acknowledgments\nSome text"
        result = _inject_chapter_marks_from_markdown(md)
        assert "[CHAPTER:" not in result

    def test_handles_preface_heading(self):
        md = "## Preface\nIntroductory notes"
        result = _inject_chapter_marks_from_markdown(md)
        assert "[CHAPTER:" not in result
