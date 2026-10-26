# PageIndex (orbit-hub-145)

> Work in progress. This checkpoint may be incomplete or fail tests. See PLAN.md and STATUS.md before use.


📚 Document Index for Vectorless, Reasoning-based RAG

## Overview

PageIndex builds hierarchical document indexes from PDFs, enabling reasoning-based retrieval without vector embeddings. The system parses document structure (table of contents), builds a tree representation, and provides tools for browsing and querying documents.

## Features Implemented

- **PDF Parsing**: Extract text content per page using PyMuPDF
- **TOC Detection**: Automatically find table of contents pages
- **TOC Extraction**: Parse TOC entries with structure numbers and page references
- **Tree Building**: Convert flat TOC entries to hierarchical tree structure
- **Leaf Node Operations**: Safe leaf node extraction (fixed Issue #330)

## Installation

```bash
python3 -m venv venv
./venv/bin/pip install -e .
```

Or with development dependencies:

```bash
./venv/bin/pip install -e ".[dev]"
```

## Running Tests

```bash
./venv/bin/python -m pytest tests/ -v
```

## Project Structure

```
pageindex/
├── __init__.py
├── pdf_parser.py      # PDF text extraction and TOC parsing
├── toc_detector.py    # TOC detection and processing
├── utils.py           # Tree operations (list_to_tree, get_leaf_nodes, etc.)
tests/
├── test_pdf_parser.py
└── test_utils.py
```

## Fixed Issues

- **Issue #330**: `get_leaf_nodes` raises KeyError on leaf nodes due to missing `nodes` key
  - Fixed by using `.get('nodes')` instead of direct key access

## License

MIT

Maintainer: Alan Vo <alanvo@gmail.com>
