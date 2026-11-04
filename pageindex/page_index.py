"""
Page Index Builder - Main pipeline for building document indexes from PDFs.
"""
import asyncio
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

from .pdf_parser import extract_text_per_page
from .toc_detector import detect_toc, process_toc_with_page_numbers, add_page_offset_to_toc_json
from .utils import list_to_tree, get_leaf_nodes, format_structure


@dataclass
class PageIndexOptions:
    """Options for page index building."""
    toc_check_page_num: bool = True
    model: str = "gpt-4o-mini"
    logger: Optional[Any] = None


async def detect_page_index(
    pages: List[Dict[str, Any]],
    opt: PageIndexOptions
) -> Dict[str, Any]:
    """
    Detect page index structure from PDF pages.
    
    This identifies table of contents pages and extracts structure.
    """
    from .toc_detector import find_toc_pages, extract_toc_entries
    
    toc_pages = find_toc_pages(pages)
    if opt.logger:
        opt.logger.info(f"TOC pages found: {toc_pages}")
    
    if not toc_pages:
        return {"toc_pages": [], "entries": [], "has_toc": False}
    
    entries = extract_toc_entries(pages, toc_pages)
    
    return {
        "toc_pages": toc_pages,
        "entries": entries,
        "has_toc": True
    }


async def tree_parser(
    flat_structure: List[Dict[str, Any]],
    opt: PageIndexOptions,
    doc: Optional[Any] = None,
    logger: Optional[Any] = None
) -> Dict[str, Any]:
    """
    Parse flat TOC structure into hierarchical tree.
    
    Converts flat list of TOC entries to nested tree structure.
    """
    if logger:
        logger.info(f"Parsing {len(flat_structure)} TOC entries into tree")
    
    tree = list_to_tree(flat_structure)
    
    if logger:
        logger.info("Tree parsing complete")
    
    return tree


async def page_index_builder(
    pdf_path: str,
    opt: Optional[PageIndexOptions] = None
) -> Dict[str, Any]:
    """
    Build complete page index from PDF.
    
    Main pipeline:
    1. Extract text per page
    2. Detect TOC and extract entries
    3. Process page numbers with offsets
    4. Build hierarchical tree
    5. Return complete document structure
    """
    if opt is None:
        opt = PageIndexOptions()
    
    if opt.logger:
        opt.logger.info(f"Starting page index build for {pdf_path}")
    
    # Step 1: Detect TOC and extract raw data
    toc_data = detect_toc(pdf_path)
    pages = toc_data["pages"]
    toc_pages = toc_data["toc_pages"]
    entries = toc_data["entries"]
    
    if opt.logger:
        opt.logger.info(f"Found {len(entries)} TOC entries on pages {toc_pages}")
    
    # Step 2: Process TOC with page numbers
    if entries:
        processed_entries = process_toc_with_page_numbers(
            entries, toc_pages, pages, opt.toc_check_page_num
        )
        
        # Handle page offset (fix for Issue #153)
        # Calculate offset from first TOC page
        offset = toc_pages[0] if toc_pages else 0
        processed_entries = add_page_offset_to_toc_json(processed_entries, offset)
    else:
        processed_entries = []
    
    # Step 3: Build hierarchical tree
    tree = await tree_parser(processed_entries, opt, doc=None, logger=opt.logger)
    
    # Step 4: Get leaf nodes for content retrieval
    leaf_nodes = get_leaf_nodes(tree)
    
    if opt.logger:
        opt.logger.info(f"Built tree with {len(leaf_nodes)} leaf nodes")
    
    return {
        "pdf_path": pdf_path,
        "total_pages": toc_data["total_pages"],
        "toc_pages": toc_pages,
        "entries": processed_entries,
        "tree": tree,
        "leaf_nodes": leaf_nodes,
        "structure_text": format_structure(tree)
    }


def page_index_main(pdf_path: str, opt: Optional[PageIndexOptions] = None) -> Dict[str, Any]:
    """
    Synchronous entry point for page index building.
    
    Runs the async pipeline in an event loop.
    """
    return asyncio.run(page_index_builder(pdf_path, opt))


# Export main functions
__all__ = [
    "PageIndexOptions",
    "detect_page_index",
    "tree_parser",
    "page_index_builder",
    "page_index_main",
]

