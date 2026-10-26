# Product development plan

Each round completes one feature or repair. Future items are planned, not implemented claims.

## Current round

core-pdf-parsing

## Roadmap

### core-pdf-parsing — Core PDF Parsing and TOC Detection

Status: done

Acceptance:
- Parse PDF and extract text content per page
- Detect table of contents pages
- Extract TOC structure with page numbers

Implementation: `pageindex/pdf_parser.py`, `pageindex/toc_detector.py`

Tests: `tests/test_pdf_parser.py`, `tests/test_utils.py`

### tree-building — Hierarchical Tree Building from Flat Structure

Status: done

Acceptance:
- Convert flat TOC entries to hierarchical tree
- Clean leaf nodes (remove empty nodes key)
- Fix get_leaf_nodes KeyError bug (Issue #330)

Implementation: `pageindex/utils.py`

Tests: `tests/test_utils.py`

### page-index-builder — Page Index Builder Pipeline

Status: planned

Acceptance:
- Build complete page index from PDF
- Handle page offsets correctly (fix Issue #153)
- Generate document structure with summaries

Implementation: `pageindex/page_index.py`

Tests: `tests/test_page_index.py`

### agent-tools — Agent Tools for Document Browsing

Status: planned

Acceptance:
- Implement browse_documents, get_document, get_document_structure, get_page_content
- Support MCP tool specs

Implementation: `pageindex/agent_tools.py`

Tests: `tests/test_agent_tools.py`

### local-chat — Local Chat with Usage Tracking

Status: planned

Acceptance:
- Chat completions and responses protocol support
- Per-call usage tracking with completeness (Issue #557)
- Streaming and non-streaming support

Implementation: `pageindex/local_chat.py`

Tests: `tests/test_local_chat.py`

### mcp-server — Standalone MCP Server

Status: planned

Acceptance:
- stdio transport MCP server
- pageindex-mcp console entry point
- Connects to local PageIndexClient

Implementation: `pageindex/mcp_server.py`

Tests: `tests/test_mcp_server.py`

