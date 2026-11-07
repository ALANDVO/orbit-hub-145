"""
Standalone MCP server for PageIndex local client.
Provides stdio transport for MCP clients like Claude Desktop, Cursor, etc.
"""
import asyncio
import sys
import os
import argparse
import json
from typing import Any, Dict, List, Optional, Awaitable, Callable

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp import types

from .agent_tools import PageIndexLocalClient, _tool_specs


class PageIndexMCPServer:
    """MCP server for PageIndex local document index."""
    
    def __init__(self, storage_path: str, include_management: bool = False):
        self.client = PageIndexLocalClient(storage_path, include_management)
        self.include_management = include_management
        self.server = Server("pageindex-local")
        self._register_tools()
    
    def _register_tools(self) -> None:
        """Register all tools with the MCP server."""
        specs = _tool_specs(self.client, self.include_management)
        
        # Build tool list for list_tools
        tool_list = [
            types.Tool(
                name=spec.name,
                description=spec.description,
                inputSchema=spec.schema,
            )
            for spec in specs
        ]
        
        # Create a mapping for quick lookup
        spec_map = {spec.name: spec for spec in specs}
        
        # Register list_tools handler
        async def list_tools_handler(_request: types.ListToolsRequest) -> types.ListToolsResult:
            return types.ListToolsResult(tools=tool_list)
        
        self.server.add_request_handler(
            "tools/list",
            types.ListToolsRequest,
            list_tools_handler
        )
        
        # Register call_tool handler
        async def call_tool_handler(request: types.CallToolRequest) -> types.CallToolResult:
            name = request.params.name
            arguments = request.params.arguments or {}
            
            spec = spec_map.get(name)
            if not spec:
                return types.CallToolResult(
                    content=[types.TextContent(type="text", text=f"Unknown tool: {name}")],
                    isError=True
                )
            
            try:
                result = spec.invoke(arguments)
                # Handle async invoke functions
                if asyncio.iscoroutine(result):
                    result = await result
                
                # Convert result to text content
                if isinstance(result, (dict, list)):
                    text = json.dumps(result, indent=2)
                else:
                    text = str(result)
                
                return types.CallToolResult(
                    content=[types.TextContent(type="text", text=text)],
                    isError=False
                )
            except Exception as e:
                return types.CallToolResult(
                    content=[types.TextContent(type="text", text=f"Error: {str(e)}")],
                    isError=True
                )
        
        self.server.add_request_handler(
            "tools/call",
            types.CallToolRequest,
            call_tool_handler
        )
    
    async def run(self) -> None:
        """Run the MCP server over stdio transport."""
        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                self.server.create_initialization_options(),
            )


def main() -> None:
    """Main entry point for the pageindex-mcp console script."""
    parser = argparse.ArgumentParser(description="PageIndex Local MCP Server")
    parser.add_argument(
        "--storage-path",
        required=True,
        help="Path to the document storage directory",
    )
    parser.add_argument(
        "--management",
        action="store_true",
        help="Enable management tools (index_document, remove_document)",
    )
    
    args = parser.parse_args()
    
    # Expand user path
    storage_path = os.path.expanduser(args.storage_path)
    
    server = PageIndexMCPServer(storage_path, args.management)
    
    try:
        asyncio.run(server.run())
    except KeyboardInterrupt:
        sys.exit(0)


if __name__ == "__main__":
    main()


__all__ = ["PageIndexMCPServer", "main"]
