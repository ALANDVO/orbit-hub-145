"""
Tests for MCP server module.
"""
import pytest
import tempfile
import os
import asyncio
import json
from mcp import types
from mcp.server import Server

from pageindex.agent_tools import PageIndexLocalClient, tool_names, _tool_specs
from pageindex.mcp_server import PageIndexMCPServer


def test_tool_names():
    """Test tool names list."""
    names = tool_names()
    assert "browse_documents" in names
    assert "get_document" in names
    assert "get_document_structure" in names
    assert "get_page_content" in names
    assert "index_document" not in names
    assert "remove_document" not in names
    
    names_mgmt = tool_names(include_management=True)
    assert "index_document" in names_mgmt
    assert "remove_document" in names_mgmt


def test_page_index_local_client():
    """Test PageIndexLocalClient basic operations."""
    with tempfile.TemporaryDirectory() as tmpdir:
        client = PageIndexLocalClient(tmpdir)
        
        # Initially empty
        docs = client.browse_documents()
        assert docs == []
        
        # Test error handling
        with pytest.raises(ValueError, match="Document not found"):
            client.get_document("nonexistent")


def test_tool_specs():
    """Test tool specifications."""
    with tempfile.TemporaryDirectory() as tmpdir:
        client = PageIndexLocalClient(tmpdir)
        specs = _tool_specs(client, include_management=False)
        
        assert len(specs) == 4
        spec_names = [s.name for s in specs]
        assert "browse_documents" in spec_names
        assert "get_document" in spec_names
        assert "get_document_structure" in spec_names
        assert "get_page_content" in spec_names
        
        # Check schemas
        for spec in specs:
            assert "type" in spec.schema
            assert spec.schema["type"] == "object"
            assert "properties" in spec.schema
        
        # Test management tools
        specs_mgmt = _tool_specs(client, include_management=True)
        assert len(specs_mgmt) == 6
        spec_names_mgmt = [s.name for s in specs_mgmt]
        assert "index_document" in spec_names_mgmt
        assert "remove_document" in spec_names_mgmt


@pytest.mark.asyncio
async def test_mcp_server_list_tools():
    """Test MCP server lists tools correctly."""
    with tempfile.TemporaryDirectory() as tmpdir:
        server = PageIndexMCPServer(tmpdir, include_management=False)
        
        # Get the handler from internal _request_handlers
        entry = server.server._request_handlers.get("tools/list")
        assert entry is not None
        
        result = await entry.handler(types.ListToolsRequest())
        
        assert isinstance(result, types.ListToolsResult)
        assert len(result.tools) == 4
        tool_names_list = [t.name for t in result.tools]
        assert "browse_documents" in tool_names_list
        assert "get_document" in tool_names_list
        assert "get_document_structure" in tool_names_list
        assert "get_page_content" in tool_names_list
        
        # Check tool schemas
        for tool in result.tools:
            assert isinstance(tool, types.Tool)
            assert tool.name
            assert tool.description
            assert tool.input_schema  # snake_case in mcp 2.x


@pytest.mark.asyncio
async def test_mcp_server_call_tool_browse():
    """Test MCP server call_tool for browse_documents."""
    with tempfile.TemporaryDirectory() as tmpdir:
        server = PageIndexMCPServer(tmpdir, include_management=False)
        
        entry = server.server._request_handlers.get("tools/call")
        assert entry is not None
        
        # Call browse_documents
        request = types.CallToolRequest(params=types.CallToolRequestParams(name="browse_documents", arguments={}))
        result = await entry.handler(request)
        
        assert isinstance(result, types.CallToolResult)
        assert len(result.content) == 1
        assert isinstance(result.content[0], types.TextContent)
        assert result.content[0].type == "text"
        # Should return empty list
        content = json.loads(result.content[0].text)
        assert content == []
        assert result.is_error is False  # snake_case


@pytest.mark.asyncio
async def test_mcp_server_call_tool_unknown():
    """Test MCP server call_tool with unknown tool."""
    with tempfile.TemporaryDirectory() as tmpdir:
        server = PageIndexMCPServer(tmpdir, include_management=False)
        
        entry = server.server._request_handlers.get("tools/call")
        assert entry is not None
        
        request = types.CallToolRequest(params=types.CallToolRequestParams(name="unknown_tool", arguments={}))
        result = await entry.handler(request)
        
        assert isinstance(result, types.CallToolResult)
        assert len(result.content) == 1
        assert isinstance(result.content[0], types.TextContent)
        assert result.is_error is True  # snake_case
        assert "Unknown tool" in result.content[0].text


@pytest.mark.asyncio
async def test_mcp_server_management_tools():
    """Test MCP server with management tools enabled."""
    with tempfile.TemporaryDirectory() as tmpdir:
        server = PageIndexMCPServer(tmpdir, include_management=True)
        
        entry = server.server._request_handlers.get("tools/list")
        assert entry is not None
        
        request = types.ListToolsRequest()
        result = await entry.handler(request)
        
        assert isinstance(result, types.ListToolsResult)
        assert len(result.tools) == 6
        tool_names_list = [t.name for t in result.tools]
        assert "index_document" in tool_names_list
        assert "remove_document" in tool_names_list


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
