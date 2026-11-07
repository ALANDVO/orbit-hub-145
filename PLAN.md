# Product development plan

Each round completes one feature or repair. Future items are planned, not implemented claims.

## Current round

mcp-server

## Roadmap

### mcp-server — Standalone Local MCP Server

Status: done

Acceptance:
- pageindex-mcp console entry point works
- stdio transport for MCP clients
- Six tools: browse_documents, get_document, get_document_structure, get_page_content, index_document, remove_document
- Management tools behind --management flag
- Document storage with JSON persistence
- Tests for tool listing, calling, error handling

Implementation: `pageindex/mcp_server.py`, `pageindex/agent_tools.py`

Tests: `tests/test_mcp_server.py`

### incremental-indexing — Incremental Index Updates for Large Documents

Status: planned

Acceptance:
- Detect changed sections between document versions
- Rebuild only affected branches of the document tree
- Recompute summaries only along impacted paths
- Maintain document version history and change tracking

### pydantic-validation — Pydantic Validation for LLM JSON Outputs

Status: planned

Acceptance:
- Validate LLM responses against explicit Pydantic schemas
- Detect malformed or incomplete responses early
- Fail deterministically instead of silently

### usage-measurement — Per-Call Chat Usage and Measurement Completeness

Status: planned

Acceptance:
- Supported measurement surface shared by chat_completions, responses and messages
- Preserve individual model-call records with call identity
- Distinguish complete, partial and unknown measurements

