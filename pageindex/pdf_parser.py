"""
PDF parsing utilities for PageIndex.
"""
import fitz  # pymupdf
from typing import List, Dict, Any, Optional
import re


def extract_text_per_page(pdf_path: str) -> List[Dict[str, Any]]:
    """
    Extract text content from each page of a PDF.
    
    Returns list of dicts with page_num, text, and metadata.
    """
    doc = fitz.open(pdf_path)
    pages = []
    
    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text("text")
        blocks = page.get_text("dict")["blocks"]
        
        pages.append({
            "page_num": page_num + 1,  # 1-indexed
            "text": text,
            "blocks": blocks,
            "width": page.rect.width,
            "height": page.rect.height,
        })
    
    doc.close()
    return pages


def find_toc_pages(pages: List[Dict[str, Any]], max_pages: int = 10) -> List[int]:
    """
    Find pages that likely contain the table of contents.
    
    Checks first N pages for TOC indicators.
    Returns list of page numbers (1-indexed).
    """
    toc_pages = []
    toc_keywords = [
        "table of contents",
        "contents",
        "toc",
        "index",
    ]
    
    for page in pages[:max_pages]:
        text_lower = page["text"].lower()
        for keyword in toc_keywords:
            if keyword in text_lower:
                toc_pages.append(page["page_num"])
                break
    
    return toc_pages


def extract_toc_entries(pages: List[Dict[str, Any]], toc_page_nums: List[int]) -> List[Dict[str, Any]]:
    """
    Extract TOC entries from identified TOC pages.
    
    Returns list of entries with structure, title, page reference.
    """
    entries = []
    
    for page in pages:
        if page["page_num"] not in toc_page_nums:
            continue
        
        lines = page["text"].split("\n")
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Try to match patterns like "1. Chapter Title .......... 5"
            # Structure can be "1", "1.1", "1.2.3" etc.
            struct_match = re.match(r'^(\d+(?:\.\d+)*)\.?\s*(.+)', line)
            if struct_match:
                structure = struct_match.group(1)
                rest = struct_match.group(2)
                
                # Now split rest on dots/separator to get title and page
                parts = re.split(r'\s+\.+\s*', rest)
                if len(parts) >= 2:
                    title = parts[0].strip()
                    try:
                        page_ref = int(parts[-1].strip())
                        entries.append({
                            'structure': structure,
                            'title': title,
                            'page': page_ref,
                            'source_page': page["page_num"]
                        })
                        continue
                    except ValueError:
                        pass
            
            # Try simpler pattern: "Title 5" at end
            match = re.match(r'^(.+?)\s+(\d+)$', line)
            if match:
                title = match.group(1).strip()
                page_ref = int(match.group(2))
                
                # Skip if looks like a header/footer
                if len(title) < 3 or title.lower() in ('contents', 'table of contents', 'index'):
                    continue
                
                entries.append({
                    'structure': '',
                    'title': title,
                    'page': page_ref,
                    'source_page': page["page_num"]
                })
    
    return entries
