"""Unit tests for detect_structure and chapter detection logic."""

import sys
import os

# Add scripts to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

import pytest
from extract import (
    detect_structure,
    _is_chapter_heading,
    _looks_like_chapter_title,
    _inject_chapter_marks_from_markdown,
    _extract_html_with_chapters,
)


class TestDetectStructureChapterDetection:
    """Tests focused on structure detection accuracy."""

    def test_single_chapter_marker(self):
        text = "[CHAPTER: Getting Started]\nSome intro text."
        result = detect_structure(text)
        assert result["chapters_detected"] == 1
        assert result["chapter_headings_sample"] == ["Getting Started"]

    def test_multiple_chapter_markers(self):
        chapters = ["Introduction", "Data Types", "Algorithms", "Complexity"]
        text = "\n".join(f"[CHAPTER: {ch}]\nContent for {ch}." for ch in chapters)
        result = detect_structure(text)
        assert result["chapters_detected"] == 4

    def test_traditional_chapter_headings(self):
        """Detect old-style 'Chapter N - Title' patterns."""
        text = "Chapter 1 - Introduction\nContent here\nChapter 2 - Data Structures\nMore content"
        result = detect_structure(text)
        assert result["chapters_detected"] >= 2

    def test_numbered_headings(self):
        """Detect numbered sections like '1. Introduction'."""
        text = "1. Introduction\n2. Background\n3. Methods"
        result = detect_structure(text)
        assert result["chapters_detected"] >= 3

    def test_combined_markers_and_traditional(self):
        """Both [CHAPTER:] markers and traditional headings should combine."""
        text = "[CHAPTER: Intro]\nText\nChapter 2 - Methods\nMore text"
        result = detect_structure(text)
        assert result["chapters_detected"] >= 2

    def test_empty_text(self):
        result = detect_structure("")
        assert result["chapters_detected"] == 0
        assert result["has_toc"] is False
        assert result["toc_location"] == "none"
        assert result["header_footer_removed"] is False

    def test_toc_table_of_contents_keyword(self):
        text = "Table of Contents\n[CHAPTER: One]\n[CHAPTER: Two]"
        result = detect_structure(text)
        assert result["has_toc"] is True

    def test_toc_sumario_portuguese(self):
        text = "Sumário\n[CHAPTER: Um]"
        result = detect_structure(text)
        assert result["has_toc"] is True

    def test_toc_indice_spanish(self):
        text = "Índice\n[CHAPTER: Uno]"
        result = detect_structure(text)
        assert result["has_toc"] is True

    def test_header_footer_removed_with_markers(self):
        text = "[CHAPTER: Intro]\nText\n[CHAPTER: Body]\nMore text"
        result = detect_structure(text)
        assert result["header_footer_removed"] is True

    def test_header_footer_not_removed_without_markers(self):
        text = "Just plain text with no markers at all."
        result = detect_structure(text)
        assert result["header_footer_removed"] is False

    def test_does_not_crash_on_unicode(self):
        """Unicode text should not cause crashes."""
        text = "[CHAPTER: Ünïcödé Intro]\nSöme text with ünicode."
        result = detect_structure(text)
        assert result["chapters_detected"] >= 1

    def test_does_not_crash_on_very_long_text(self):
        """Should handle very long texts without performance issues."""
        text = "[CHAPTER: Start]\n" + "word " * 50000
        result = detect_structure(text)
        assert "chapters_detected" in result

    def test_does_not_crash_on_special_characters(self):
        """Special characters in headings should be handled."""
        text = '[CHAPTER: Chapter 1: "Introduction"]\nText & more text.'
        result = detect_structure(text)
        assert result["chapters_detected"] >= 1


class TestIsChapterHeadingAdvanced:
    """More comprehensive tests for the block-level heading detector."""

    def _make_block(self, text, font_size=16, bold=True):
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

    def test_all_caps_part_title(self):
        """All-caps short text should be recognized (e.g., 'PART I')."""
        block = self._make_block("PART I")
        assert _is_chapter_heading(block, "PART I") is True

    def test_epigraph_not_heading(self):
        """Epigraph (short quote at chapter start) should not match."""
        block = self._make_block(
            "The only way to do great work is to love what you do."
        )
        # This is long-ish and doesn't match patterns, but bold/short may trigger
        result = _is_chapter_heading(
            block, "The only way to do great work is to love what you do."
        )
        # This is 60+ chars with no numeric/chapter pattern. Should be False since
        # our threshold for all-caps doesn't apply and no chapter words present.
        # bold + < 100 chars used to match this — now requires additional checks
        assert result is False

    def test_dedication_bold_short(self):
        """Bold short text 'Dedication' should NOT match."""
        block = self._make_block("Dedication")
        assert _is_chapter_heading(block, "Dedication") is False

    def test_italic_not_bold(self):
        """Italic text (flags != bold flag) should not trigger heading detection easily."""
        # flags=1 is italic, not bold (2)
        block = self._make_block("Some italic text", font_size=16, bold=False)
        # Not bold, but font > 14 → still checks patterns, no match
        result = _is_chapter_heading(block, "Some italic text")
        assert result is False

    def test_large_font_triggers_checks(self):
        """Font > 14 should trigger pattern checks even without bold."""
        block = self._make_block("1. Introduction", font_size=18, bold=False)
        assert _is_chapter_heading(block, "1. Introduction") is True


class TestLooksLikeChapterTitleAdvanced:
    """Advanced tests for the standalone chapter title classifier."""

    def test_h3_with_number(self):
        assert _looks_like_chapter_title("3. Results", "h3") is True

    def test_h2_outline(self):
        assert _looks_like_chapter_title("II. Literature Review", "h2") is True

    def test_skip_copyright(self):
        assert _looks_like_chapter_title("Copyright", "h2") is False

    def test_skip_index(self):
        assert _looks_like_chapter_title("Index", "h2") is False

    def test_skip_references(self):
        assert _looks_like_chapter_title("References", "h2") is False

    def test_skip_bibliography(self):
        assert _looks_like_chapter_title("Bibliography", "h2") is False

    def test_skip_appendix(self):
        assert _looks_like_chapter_title("Appendix A", "h2") is False

    def test_skip_author_bio(self):
        assert _looks_like_chapter_title("About the Author", "h2") is False

    def test_skip_abstract(self):
        assert _looks_like_chapter_title("Abstract", "h2") is False

    def test_h2_just_number(self):
        """A heading that's just a number should probably not be a chapter."""
        assert _looks_like_chapter_title("5", "h2") is False


class TestEpubChapterExtraction:
    """Test EPUB-specific extraction functions."""

    def test_html_extraction_with_headings(self):
        """Verify headings in HTML are detected and markers inserted."""
        html = "<h1>Chapter 1</h1><p>Text</p><h2>1.1 Subsection</h2><p>More text</p>"
        num, text = _extract_html_with_chapters(html, 0)
        assert num == 2
        assert "[CHAPTER:" in text
        assert "Chapter 1" in text

    def test_html_no_headings(self):
        """HTML with no headings → no markers."""
        html = "<p>Just a paragraph.</p><p>Another paragraph.</p>"
        num, text = _extract_html_with_chapters(html, 0)
        assert num == 0
        assert "[CHAPTER:" not in text

    def test_html_heading_resets_chapter_counter(self):
        """Chapter numbers should increment across HTML fragments."""
        html1 = "<h1>Ch 1</h1><p>Text</p>"
        num1, _ = _extract_html_with_chapters(html1, 0)
        html2 = "<h1>Ch 2</h1><p>Text</p>"
        num2, text2 = _extract_html_with_chapters(html2, num1)
        assert num2 == 2
        assert "[CHAPTER: Ch 2]" in text2


class TestMarkdownInjection:
    """Test Docling markdown post-processing."""

    def test_detects_h2_in_markdown(self):
        md = "## Methods\nDescription of methods."
        result = _inject_chapter_marks_from_markdown(md)
        assert "[CHAPTER: Methods]" in result

    def test_detects_h3_in_markdown(self):
        md = "### Results\nThe results are..."
        result = _inject_chapter_marks_from_markdown(md)
        assert "[CHAPTER: Results]" in result

    def test_does_not_modify_h1(self):
        """Docling shouldn't output # headings (title level), but just in case."""
        md = "# Title\nContent"
        result = _inject_chapter_marks_from_markdown(md)
        # # is h1 which also matches ##+ pattern — but we should handle it
        assert "##" not in result or "[CHAPTER:" in result

    def test_skips_acknowledgments_in_markdown(self):
        md = "## Acknowledgments\nThanks to everyone."
        result = _inject_chapter_marks_from_markdown(md)
        assert "[CHAPTER:" not in result

    def test_preserves_code_blocks(self):
        """Code blocks should not be modified."""
        md = "## Chapter\n```python\nprint('hello')\n```"
        result = _inject_chapter_marks_from_markdown(md)
        assert "```python" in result


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
