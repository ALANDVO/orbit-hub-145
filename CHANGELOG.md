# Changelog

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

