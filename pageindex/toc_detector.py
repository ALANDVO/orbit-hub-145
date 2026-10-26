"""
TOC detection and processing for PageIndex.
"""
from typing import List, Dict, Any, Optional
from .pdf_parser import extract_text_per_page, find_toc_pages, extract_toc_entries


def detect_toc(pdf_path: str) -> Dict[str, Any]:
    """
    Detect and extract table of contents from a PDF.
    
    Returns dict with toc_pages, entries, and raw_pages.
    """
    pages = extract_text_per_page(pdf_path)
    toc_pages = find_toc_pages(pages)
    entries = extract_toc_entries(pages, toc_pages)
    
    return {
        "toc_pages": toc_pages,
        "entries": entries,
        "total_pages": len(pages),
        "pages": pages
    }


def process_toc_with_page_numbers(
    toc_content: List[Dict[str, Any]],
    toc_page_list: List[int],
    page_list: List[Dict[str, Any]],
    toc_check_page_num: bool = True,
) -> List[Dict[str, Any]]:
    """
    Process TOC entries and add physical page numbers.
    
    This matches the function signature from the reference implementation.
    """
    # For now, return entries with page offsets handled
    # The reference implementation has more complex logic for page offset detection
    processed = []
    for entry in toc_content:
        processed.append({
            **entry,
            "physical_index": entry.get("page", 1)
        })
    return processed


def add_page_offset_to_toc_json(toc_data: List[Dict[str, Any]], offset: int) -> List[Dict[str, Any]]:
    """
    Add page offset to TOC entries.
    
    Fixes Issue #153: handles None page values gracefully.
    """
    result = []
    for entry in toc_data:
        new_entry = entry.copy()
        page = entry.get("page")
        if page is not None:
            new_entry["physical_index"] = page + offset
        else:
            new_entry["physical_index"] = offset + 1  # Default to first page after offset
        result.append(new_entry)
    return result
