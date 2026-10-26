"""
Tests for utils module - tree operations.
"""
import pytest
from pageindex.utils import list_to_tree, clean_node, get_leaf_nodes, is_leaf_node, format_structure


def test_list_to_tree_flat():
    """Test converting flat list to tree."""
    flat = [
        {'structure': '1', 'title': 'Chapter 1', 'page': 1},
        {'structure': '2', 'title': 'Chapter 2', 'page': 10},
    ]
    tree = list_to_tree(flat)
    assert "nodes" in tree
    assert len(tree["nodes"]) == 2
    assert tree["nodes"][0]["title"] == "Chapter 1"
    assert tree["nodes"][1]["title"] == "Chapter 2"


def test_list_to_tree_nested():
    """Test nested structure conversion."""
    flat = [
        {'structure': '1', 'title': 'Chapter 1', 'page': 1},
        {'structure': '1.1', 'title': 'Section 1.1', 'page': 2},
        {'structure': '1.2', 'title': 'Section 1.2', 'page': 5},
        {'structure': '2', 'title': 'Chapter 2', 'page': 10},
    ]
    tree = list_to_tree(flat)
    assert len(tree["nodes"]) == 2
    assert len(tree["nodes"][0]["nodes"]) == 2
    assert tree["nodes"][0]["nodes"][0]["title"] == "Section 1.1"
    assert tree["nodes"][0]["nodes"][1]["title"] == "Section 1.2"


def test_clean_node_removes_empty_nodes():
    """Test that clean_node removes empty nodes key from leaves."""
    node = {"title": "Leaf", "nodes": []}
    clean_node(node)
    assert "nodes" not in node


def test_clean_node_keeps_non_empty():
    """Test that clean_node keeps nodes key for non-leaves."""
    node = {"title": "Parent", "nodes": [{"title": "Child", "nodes": []}]}
    clean_node(node)
    assert "nodes" in node
    assert "nodes" not in node["nodes"][0]


def test_get_leaf_nodes_issue_330():
    """
    Test fix for Issue #330: get_leaf_nodes raises KeyError on leaf nodes
    due to missing 'nodes' key after clean_node().
    """
    flat = [
        {'structure': '1', 'title': 'Chapter 1', 'page': 1},
        {'structure': '2', 'title': 'Chapter 2', 'page': 10},
    ]
    tree = list_to_tree(flat)  # builds tree; leaf nodes have no 'nodes' key
    
    # This should NOT raise KeyError
    leaf_nodes = get_leaf_nodes(tree)
    
    assert len(leaf_nodes) == 2
    assert leaf_nodes[0]["title"] == "Chapter 1"
    assert leaf_nodes[1]["title"] == "Chapter 2"
    # Verify nodes key is not present (was popped)
    assert "nodes" not in leaf_nodes[0]
    assert "nodes" not in leaf_nodes[1]


def test_get_leaf_nodes_nested():
    """Test get_leaf_nodes on nested tree."""
    flat = [
        {'structure': '1', 'title': 'Chapter 1', 'page': 1},
        {'structure': '1.1', 'title': 'Section 1.1', 'page': 2},
        {'structure': '1.2', 'title': 'Section 1.2', 'page': 5},
        {'structure': '2', 'title': 'Chapter 2', 'page': 10},
    ]
    tree = list_to_tree(flat)
    
    leaf_nodes = get_leaf_nodes(tree)
    # Should get Section 1.1, Section 1.2, Chapter 2 (Chapter 1 has children)
    assert len(leaf_nodes) == 3
    titles = [n["title"] for n in leaf_nodes]
    assert "Section 1.1" in titles
    assert "Section 1.2" in titles
    assert "Chapter 2" in titles


def test_is_leaf_node():
    """Test is_leaf_node helper."""
    leaf = {"title": "Leaf"}
    assert is_leaf_node(leaf) is True
    
    parent = {"title": "Parent", "nodes": [{"title": "Child"}]}
    assert is_leaf_node(parent) is False


def test_format_structure():
    """Test tree formatting."""
    flat = [
        {'structure': '1', 'title': 'Chapter 1', 'page': 1},
        {'structure': '1.1', 'title': 'Section 1.1', 'page': 2},
    ]
    tree = list_to_tree(flat)
    output = format_structure(tree)
    assert "Chapter 1" in output
    assert "Section 1.1" in output
