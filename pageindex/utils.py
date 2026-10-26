"""
Utility functions for PageIndex tree operations.
"""
import copy
from typing import List, Dict, Any, Optional


def list_to_tree(flat_list: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Convert flat list of TOC entries to hierarchical tree structure.
    
    Each entry should have 'structure' (e.g., '1.2.3'), 'title', 'page', etc.
    """
    if not flat_list:
        return {}
    
    root = {"nodes": []}
    
    for entry in flat_list:
        structure = entry.get("structure", "")
        if not structure:
            # No structure number, add as top-level
            node = {k: v for k, v in entry.items() if k != "structure"}
            node["nodes"] = []
            root["nodes"].append(node)
            continue
        
        parts = structure.split(".")
        current = root
        
        for i, part in enumerate(parts):
            # Find or create node at this level
            found = False
            for node in current.get("nodes", []):
                if node.get("structure") == ".".join(parts[:i+1]):
                    current = node
                    found = True
                    break
            
            if not found:
                new_node = {k: v for k, v in entry.items() if k != "structure"}
                new_node["structure"] = ".".join(parts[:i+1])
                new_node["nodes"] = []
                current.setdefault("nodes", []).append(new_node)
                current = new_node
    
    clean_node(root)
    return root


def clean_node(node: Dict[str, Any]) -> None:
    """
    Recursively clean node by removing empty 'nodes' key from leaf nodes.
    
    This is called after tree construction to remove empty children arrays.
    """
    if "nodes" in node:
        if not node["nodes"]:
            del node["nodes"]
        else:
            for child in node["nodes"]:
                clean_node(child)


def get_leaf_nodes(structure: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Get all leaf nodes from a tree structure.
    
    Fixed Issue #330: Use .get('nodes') to safely handle leaf nodes
    that don't have a 'nodes' key (deleted by clean_node).
    """
    if not isinstance(structure, dict):
        return []
    
    # Check if this is a leaf node (no 'nodes' key or empty nodes)
    nodes = structure.get("nodes")
    if not nodes:
        # This is a leaf node
        structure_node = copy.deepcopy(structure)
        structure_node.pop("nodes", None)
        return [structure_node]
    
    # Recursively collect leaf nodes from children
    leaf_nodes = []
    for child in nodes:
        leaf_nodes.extend(get_leaf_nodes(child))
    return leaf_nodes


def is_leaf_node(node: Dict[str, Any]) -> bool:
    """Check if a node is a leaf (no children)."""
    return not node.get("nodes")


def format_structure(structure: Dict[str, Any], indent: int = 0) -> str:
    """Format tree structure for display."""
    lines = []
    prefix = "  " * indent
    
    title = structure.get("title", structure.get("structure", "Root"))
    lines.append(f"{prefix}- {title}")
    
    nodes = structure.get("nodes")
    if nodes:
        for child in nodes:
            lines.append(format_structure(child, indent + 1))
    
    return "\n".join(lines)


def print_tree(structure: Dict[str, Any]) -> None:
    """Print tree structure to stdout."""
    print(format_structure(structure))
