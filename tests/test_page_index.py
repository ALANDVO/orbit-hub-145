"""
Tests for page index builder pipeline.
"""
import pytest
import tempfile
import os
import fitz

from pageindex.page_index import (
    PageIndexOptions,
    page_index_builder,
    page_index_main,
    detect_page_index,
    tree_parser,
)
from pageindex.utils import list_to_tree


def create_test_pdf() -> str:
    """Create a test PDF with TOC and content."""
    doc = fitz.open()
    
    # Page 1: Title page
    page = doc.new_page()
    page.insert_text((72, 72), "Test Document\n\nVersion 1.0")
    
    # Page 2: Table of Contents
    page = doc.new_page()
    page.insert_text((72, 72), "Table of Contents\n\n1. Introduction .......... 3\n2. Methods .............. 5\n3. Results .............. 8\n4. Discussion ........... 12")
    
    # Page 3: Introduction
    page = doc.new_page()
    page.insert_text((72, 72), "1. Introduction\n\nThis is the introduction chapter.")
    
    # Page 4: Methods
    page = doc.new_page()
    page.insert_text((72, 72), "2. Methods\n\nThis chapter describes methods.")
    
    # Page 5: Results
    page = doc.new_page()
    page.insert_text((72, 72), "3. Results\n\nThis chapter presents results.")
    
    # Page 6: Discussion
    page = doc.new_page()
    page.insert_text((72, 72), "4. Discussion\n\nThis chapter discusses findings.")
    
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
        doc.save(f.name)
        doc.close()
        return f.name


@pytest.fixture
def test_pdf():
    """Fixture providing a test PDF path."""
    pdf_path = create_test_pdf()
    yield pdf_path
    os.unlink(pdf_path)


@pytest.mark.asyncio
async def test_detect_page_index(test_pdf):
    """Test page index detection from PDF."""
    from pageindex.pdf_parser import extract_text_per_page
    
    pages = extract_text_per_page(test_pdf)
    opt = PageIndexOptions()
    
    result = await detect_page_index(pages, opt)
    
    assert "toc_pages" in result
    assert "entries" in result
    assert "has_toc" in result
    assert result["has_toc"] is True
    assert len(result["entries"]) > 0


@pytest.mark.asyncio
async def test_tree_parser():
    """Test flat to tree conversion."""
    flat = [
        {"structure": "1", "title": "Chapter 1", "page": 1},
        {"structure": "1.1", "title": "Section 1.1", "page": 2},
        {"structure": "1.2", "title": "Section 1.2", "page": 3},
        {"structure": "2", "title": "Chapter 2", "page": 4},
    ]
    
    opt = PageIndexOptions()
    tree = await tree_parser(flat, opt)
    
    assert "nodes" in tree
    assert len(tree["nodes"]) == 2
    assert tree["nodes"][0]["title"] == "Chapter 1"
    assert len(tree["nodes"][0]["nodes"]) == 2
    assert tree["nodes"][1]["title"] == "Chapter 2"


@pytest.mark.asyncio
async def test_page_index_builder(test_pdf):
    """Test complete page index builder pipeline."""
    opt = PageIndexOptions()
    result = await page_index_builder(test_pdf, opt)
    
    assert "pdf_path" in result
    assert "total_pages" in result
    assert "toc_pages" in result
    assert "entries" in result
    assert "tree" in result
    assert "leaf_nodes" in result
    assert "structure_text" in result
    
    assert result["total_pages"] == 6
    assert len(result["toc_pages"]) > 0
    assert len(result["entries"]) > 0
    assert len(result["leaf_nodes"]) > 0


def test_page_index_main_sync(test_pdf):
    """Test synchronous entry point."""
    result = page_index_main(test_pdf)
    
    assert "tree" in result
    assert "leaf_nodes" in result
    assert "structure_text" in result


def test_page_offset_handling():
    """Test page offset handling (Issue #153 fix)."""
    from pageindex.toc_detector import add_page_offset_to_toc_json
    
    # Entry with None page (simulates the bug condition)
    entries = [
        {"structure": "1", "title": "Chapter 1", "page": 3},
        {"structure": "2", "title": "Chapter 2", "page": None},
    ]
    
    result = add_page_offset_to_toc_json(entries, 2)
    
    assert result[0]["physical_index"] == 5  # 3 + 2
    assert result[1]["physical_index"] == 3  # offset + 1 default


def test_list_to_tree_integration():
    """Test list_to_tree used in page_index."""
    flat = [
        {"structure": "1", "title": "Chapter 1", "start_index": 1, "end_index": 10},
        {"structure": "1.1", "title": "Section 1.1", "start_index": 2, "end_index": 5},
        {"structure": "2", "title": "Chapter 2", "start_index": 11, "end_index": 20},
    ]
    
    tree = list_to_tree(flat)
    
    assert "nodes" in tree
    assert len(tree["nodes"]) == 2
    assert tree["nodes"][0]["title"] == "Chapter 1"
    assert "nodes" in tree["nodes"][0]
    assert len(tree["nodes"][0]["nodes"]) == 1

