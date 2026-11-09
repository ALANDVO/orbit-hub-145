# Changelog

## 1.3.0 — work-in-progress checkpoint

Partial code published for continued development. Known issues: STATUS.md.

## 1.2.0 — work-in-progress checkpoint

Partial code published for continued development. Known issues: STATUS.md.

### Added (public-api)
- Complete public API exports in `pageindex/__init__.py`
  - Core indexing functions: `page_index_main`, `page_index_builder`, `PageIndexOptions`, `detect_page_index`, `tree_parser`
  - Tree utilities: `list_to_tree`, `get_leaf_nodes`, `format_structure`, `is_leaf_node`, `print_tree`
  - MCP components: `PageIndexLocalClient`, `PageIndexMCPServer`, `tool_names`, `mcp_main`
- README updated with public API usage examples and import patterns

## 1.1.0 — work-in-progress checkpoint

Partial code published for continued development. Known issues: STATUS.md.

## 1.0.0 — work-in-progress checkpoint

Partial code published for continued development. Known issues: STATUS.md.

### Added (page-index-builder)
- Page index builder pipeline in `pageindex/page_index.py`
- Async `page_index_builder()` and sync `page_index_main()` entry points
- TOC detection and structure extraction
- Hierarchical tree building from flat TOC entries
- Page offset handling (fixes Issue #153: unsupported operand type for int + NoneType)
- Leaf node extraction for content retrieval

### Fixed
- Issue #153: Page offset calculation handles None page values gracefully
- Issue #330: get_leaf_nodes KeyError on leaf nodes (fixed in tree-building round)

## 1.1.0 — MCP Server Implementation

### Added (mcp-server)
- Standalone local MCP server in `pageindex/mcp_server.py` with stdio transport
- Agent tools module `pageindex/agent_tools.py` with tool specifications and local client
- Console entry point `pageindex-mcp` for easy deployment
- Document storage with JSON persistence
- Six MCP tools: `browse_documents`, `get_document`, `get_document_structure`, `get_page_content`, `index_document`, `remove_document`
- Management tools (`index_document`, `remove_document`) behind `--management` flag
- Tests for MCP server: tool listing, tool calling, error handling, management tools

### Fixed
- Issue #540: Standalone local MCP server so Claude Desktop / Cursor / any MCP client can use a local library

### Updated
- README with MCP server usage documentation and client configuration examples
- Project structure documentation

---

Alan Vo · [alanvo.net](https://alanvo.net) · [X: @alanvoasi](https://x.com/alanvoasi)
