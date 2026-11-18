"""
Incremental indexing utilities.

Provides functionality to detect changes between document versions
and compute node hashes for efficient comparison.
"""
import json
import hashlib
from typing import List, Dict, Any


def compute_node_hash(node: Dict[str, Any]) -> str:
    """Compute deterministic hash of a node based on its content.

    The hash is computed from a canonical JSON representation of the node
    (sorted keys, deterministic spacing). This allows consistent comparison
    across runs and Python versions.
    """
    # Create a copy to avoid mutating input
    canonical = json.dumps(node, sort_keys=True, separators=(',', ':'))
    return hashlib.sha256(canonical.encode('utf-8')).hexdigest()


def detect_changed_sections(old_doc: Dict[str, Any], new_doc: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Detect changed sections between two document versions.

    Compares leaf nodes (sections) of the two documents and returns a list
    of changed leaf nodes. A leaf node is considered changed if its hash
    differs between the two versions.

    The detection is based on the ``leaf_nodes`` field stored in the
    document dictionary, which is produced by :func:`pageindex.utils.get_leaf_nodes`.

    Returns:
        List of changed leaf node dictionaries.
    """
    old_leaves = old_doc.get('leaf_nodes', [])
    new_leaves = new_doc.get('leaf_nodes', [])

    # Build hash-to-node maps for fast lookup
    old_hashes = {compute_node_hash(node): node for node in old_leaves}
    new_hashes = {compute_node_hash(node): node for node in new_leaves}

    changed = []
    # Leaves present in old but missing in new (deleted sections)
    for hash_val, node in old_hashes.items():
        if hash_val not in new_hashes:
            changed.append(node)
    # Leaves present in new but missing in old (added sections)
    for hash_val, node in new_hashes.items():
        if hash_val not in old_hashes:
            changed.append(node)

    return changed
