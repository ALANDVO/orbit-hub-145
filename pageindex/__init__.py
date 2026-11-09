"""
PageIndex: Document Index for Vectorless, Reasoning-based RAG
"""
__version__ = "0.1.0"

from .agent_tools import PageIndexLocalClient, tool_names
from .mcp_server import PageIndexMCPServer, main as mcp_main
from .page_index import PageIndexOptions, page_index_main, page_index_builder, detect_page_index, tree_parser
from .utils import list_to_tree, get_leaf_nodes, format_structure, is_leaf_node, print_tree

__all__ = [
    "PageIndexLocalClient",
    "tool_names",
    "PageIndexMCPServer",
    "mcp_main",
    "PageIndexOptions",
    "page_index_main",
    "page_index_builder",
    "detect_page_index",
    "tree_parser",
    "list_to_tree",
    "get_leaf_nodes",
    "format_structure",
    "is_leaf_node",
    "print_tree",
]
__version__ = "0.1.0"

from .agent_tools import PageIndexLocalClient, tool_names
from .mcp_server import PageIndexMCPServer, main as mcp_main

__all__ = [
    "PageIndexLocalClient",
    "tool_names",
    "PageIndexMCPServer",
    "mcp_main",
]
