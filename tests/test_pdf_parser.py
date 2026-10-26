"""
Tests for PDF parser module.
"""
import pytest
import tempfile
import os
from pageindex.pdf_parser import extract_text_per_page, find_toc_pages, extract_toc_entries


def test_extract_text_per_page_empty():
    """Test extraction from a minimal PDF."""
    # Create a simple PDF for testing
    import fitz
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((72, 72), "Test content\nPage 1")
    doc.new_page()
    page2 = doc[-1]
    page2.insert_text((72, 72), "Table of Contents\n1. Introduction .......... 3\n2. Methods .............. 5")
    
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
        doc.save(f.name)
        doc.close()
        
        try:
            pages = extract_text_per_page(f.name)
            assert len(pages) == 2
            assert pages[0]["page_num"] == 1
            assert "Test content" in pages[0]["text"]
            assert pages[1]["page_num"] == 2
            assert "Table of Contents" in pages[1]["text"]
        finally:
            os.unlink(f.name)


def test_find_toc_pages():
    """Test TOC page detection."""
    pages = [
        {"page_num": 1, "text": "Title Page"},
        {"page_num": 2, "text": "Table of Contents\n1. Chapter One ... 3"},
        {"page_num": 3, "text": "Chapter One content"},
        {"page_num": 4, "text": "Contents\n2. Chapter Two ... 10"},
    ]
    
    toc_pages = find_toc_pages(pages, max_pages=4)
    assert 2 in toc_pages
    assert 4 in toc_pages
    assert 1 not in toc_pages
    assert 3 not in toc_pages


def test_extract_toc_entries():
    """Test TOC entry extraction."""
    pages = [
        {"page_num": 2, "text": "Table of Contents\n1. Introduction .......... 3\n2. Methods .............. 5\n3. Results .............. 8"},
    ]
    
    entries = extract_toc_entries(pages, [2])
    assert len(entries) == 3
    assert entries[0]["structure"] == "1"
    assert entries[0]["title"] == "Introduction"
    assert entries[0]["page"] == 3
    assert entries[1]["structure"] == "2"
    assert entries[1]["title"] == "Methods"
    assert entries[1]["page"] == 5


def test_extract_toc_entries_simple_format():
    """Test TOC entry extraction with simple 'Title 5' format."""
    pages = [
        {"page_num": 2, "text": "Introduction 3\nMethods 5\nResults 8"},
    ]
    
    entries = extract_toc_entries(pages, [2])
    assert len(entries) == 3
    assert entries[0]["title"] == "Introduction"
    assert entries[0]["page"] == 3
    assert entries[0]["structure"] == ""
