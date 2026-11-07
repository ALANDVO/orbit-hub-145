# PageIndex (orbit-hub-145) — Alan Vo

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
- **MCP Server**: Standalone local MCP server for Claude Desktop, Cursor, and other MCP clients (implements Issue #540)

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

## Running the MCP Server

The `pageindex-mcp` console script provides a standalone MCP server over stdio transport:

```bash
# Start the MCP server with a storage directory
pageindex-mcp --storage-path ./index_store

# Enable management tools (index_document, remove_document)
pageindex-mcp --storage-path ./index_store --management
```

### Client Configuration

Configure your MCP client (Claude Desktop, Cursor, etc.) to connect to the local server:

```json
{
  "mcpServers": {
    "pageindex-local": {
      "command": "pageindex-mcp",
      "args": ["--storage-path", "/path/to/index_store"]
    }
  }
}
```

With management tools enabled:

```json
{
  "mcpServers": {
    "pageindex-local": {
      "command": "pageindex-mcp",
      "args": ["--storage-path", "/path/to/index_store", "--management"]
    }
  }
}
```

### Available Tools

- `browse_documents` - List all indexed documents with basic metadata
- `get_document` - Get full document index including structure and metadata
- `get_document_structure` - Get hierarchical structure tree of a document
- `get_page_content` - Get text content of a specific page in a document
- `index_document` - Index a new PDF document (requires `--management`)
- `remove_document` - Remove a document from the index (requires `--management`)

## Project Structure

```
pageindex/
├── __init__.py
├── agent_tools.py     # Tool specifications for MCP server
├── mcp_server.py      # Standalone MCP server (stdio transport)
├── pdf_parser.py      # PDF text extraction and TOC parsing
├── toc_detector.py    # TOC detection and processing
├── utils.py           # Tree operations (list_to_tree, get_leaf_nodes, etc.)
tests/
├── test_mcp_server.py
├── test_page_index.py
├── test_pdf_parser.py
└── test_utils.py
```

## Fixed Issues

- **Issue #330**: `get_leaf_nodes` raises KeyError on leaf nodes due to missing `nodes` key
  - Fixed by using `.get('nodes')` instead of direct key access
- **Issue #153**: Page offset calculation handles None page values gracefully
- **Issue #540**: Standalone local MCP server for Claude Desktop, Cursor, and other MCP clients

## License

MIT

Maintainer: Alan Vo <alanvo@gmail.com>

---

Alan Vo · [alanvo.net](https://alanvo.net)
