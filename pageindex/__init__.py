"""
PageIndex: Document Index for Vectorless, Reasoning-based RAG
"""
__version__ = "0.1.0"

from .agent_tools import PageIndexLocalClient, tool_names
from .mcp_server import PageIndexMCPServer, main as mcp_main

__all__ = [
    "PageIndexLocalClient",
    "tool_names",
    "PageIndexMCPServer",
    "mcp_main",
]
