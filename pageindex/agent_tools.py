"""
Agent tools for PageIndex local client.
Provides tool specifications and implementations for MCP server.
"""
import json
from typing import List, Dict, Any, Optional, Callable, Tuple
from dataclasses import dataclass

from .page_index import PageIndexOptions, page_index_main
from .utils import list_to_tree, get_leaf_nodes, format_structure


@dataclass
class ToolSpec:
    """Specification for an MCP tool."""
    name: str
    description: str
    schema: Dict[str, Any]
    invoke: Callable[[Dict[str, Any]], Any]


class PageIndexLocalClient:
    """Local PageIndex client for document indexing and retrieval."""
    
    def __init__(self, storage_path: str, include_management: bool = False):
        self.storage_path = storage_path
        self.include_management = include_management
        self._documents: Dict[str, Dict[str, Any]] = {}
        self._load_documents()
    
    def _load_documents(self) -> None:
        """Load existing indexed documents from storage."""
        import os
        import json
        if not os.path.exists(self.storage_path):
            os.makedirs(self.storage_path, exist_ok=True)
            return
        
        for filename in os.listdir(self.storage_path):
            if filename.endswith(".json"):
                doc_id = filename[:-5]
                filepath = os.path.join(self.storage_path, filename)
                with open(filepath, "r") as f:
                    self._documents[doc_id] = json.load(f)
    
    def _save_document(self, doc_id: str, doc_data: Dict[str, Any]) -> None:
        """Save document to storage."""
        import os
        import json
        os.makedirs(self.storage_path, exist_ok=True)
        filepath = os.path.join(self.storage_path, f"{doc_id}.json")
        with open(filepath, "w") as f:
            json.dump(doc_data, f, indent=2)
    
    def browse_documents(self) -> List[Dict[str, Any]]:
        """List all indexed documents."""
        return [
            {
                "id": doc_id,
                "title": doc_data.get("title", doc_id),
                "total_pages": doc_data.get("total_pages", 0),
                "has_toc": doc_data.get("has_toc", False),
            }
            for doc_id, doc_data in self._documents.items()
        ]
    
    def get_document(self, document_id: str) -> Dict[str, Any]:
        """Get full document index by ID."""
        if document_id not in self._documents:
            raise ValueError(f"Document not found: {document_id}")
        return self._documents[document_id]
    
    def get_document_structure(self, document_id: str) -> Dict[str, Any]:
        """Get hierarchical structure of a document."""
        doc = self.get_document(document_id)
        return doc.get("structure", {})
    
    def get_page_content(self, document_id: str, page_num: int) -> str:
        """Get text content of a specific page."""
        doc = self.get_document(document_id)
        pages = doc.get("pages", [])
        for page in pages:
            if page.get("page_num") == page_num:
                return page.get("text", "")
        raise ValueError(f"Page {page_num} not found in document {document_id}")
    
    def index_document(self, pdf_path: str, title: Optional[str] = None) -> Dict[str, Any]:
        """Index a new PDF document."""
        import os
        doc_id = os.path.splitext(os.path.basename(pdf_path))[0]
        if not title:
            title = doc_id
        
        opt = PageIndexOptions()
        result = page_index_main(pdf_path, opt)
        
        doc_data = {
            "id": doc_id,
            "title": title,
            "pdf_path": pdf_path,
            "total_pages": result.get("total_pages", 0),
            "has_toc": result.get("has_toc", False),
            "structure": result.get("structure", {}),
            "leaf_nodes": result.get("leaf_nodes", []),
            "structure_text": result.get("structure_text", ""),
            "pages": result.get("pages", []),
            "toc_pages": result.get("toc_pages", []),
        }
        
        self._documents[doc_id] = doc_data
        self._save_document(doc_id, doc_data)
        
        return {"id": doc_id, "title": title, "status": "indexed"}
    
    def remove_document(self, document_id: str) -> Dict[str, Any]:
        """Remove a document from the index."""
        import os
        if document_id not in self._documents:
            raise ValueError(f"Document not found: {document_id}")
        
        del self._documents[document_id]
        filepath = os.path.join(self.storage_path, f"{document_id}.json")
        if os.path.exists(filepath):
            os.unlink(filepath)
        
        return {"id": document_id, "status": "removed"}


def _tool_specs(client: PageIndexLocalClient, include_management: bool = False) -> List[ToolSpec]:
    """Return tool specifications for the MCP server."""
    specs = [
        ToolSpec(
            name="browse_documents",
            description="List all indexed documents with basic metadata",
            schema={
                "type": "object",
                "properties": {},
                "additionalProperties": False,
            },
            invoke=lambda args: client.browse_documents(),
        ),
        ToolSpec(
            name="get_document",
            description="Get full document index including structure and metadata",
            schema={
                "type": "object",
                "properties": {
                    "document_id": {"type": "string", "description": "ID of the document to retrieve"},
                },
                "required": ["document_id"],
                "additionalProperties": False,
            },
            invoke=lambda args: client.get_document(args["document_id"]),
        ),
        ToolSpec(
            name="get_document_structure",
            description="Get hierarchical structure tree of a document",
            schema={
                "type": "object",
                "properties": {
                    "document_id": {"type": "string", "description": "ID of the document"},
                },
                "required": ["document_id"],
                "additionalProperties": False,
            },
            invoke=lambda args: client.get_document_structure(args["document_id"]),
        ),
        ToolSpec(
            name="get_page_content",
            description="Get text content of a specific page in a document",
            schema={
                "type": "object",
                "properties": {
                    "document_id": {"type": "string", "description": "ID of the document"},
                    "page_num": {"type": "integer", "description": "Page number (1-indexed)"},
                },
                "required": ["document_id", "page_num"],
                "additionalProperties": False,
            },
            invoke=lambda args: client.get_page_content(args["document_id"], args["page_num"]),
        ),
    ]
    
    if include_management:
        specs.append(
            ToolSpec(
                name="index_document",
                description="Index a new PDF document",
                schema={
                    "type": "object",
                    "properties": {
                        "pdf_path": {"type": "string", "description": "Path to the PDF file"},
                        "title": {"type": "string", "description": "Optional title for the document"},
                    },
                    "required": ["pdf_path"],
                    "additionalProperties": False,
                },
                invoke=lambda args: client.index_document(args["pdf_path"], args.get("title")),
            )
        )
        specs.append(
            ToolSpec(
                name="remove_document",
                description="Remove a document from the index",
                schema={
                    "type": "object",
                    "properties": {
                        "document_id": {"type": "string", "description": "ID of the document to remove"},
                    },
                    "required": ["document_id"],
                    "additionalProperties": False,
                },
                invoke=lambda args: client.remove_document(args["document_id"]),
            )
        )
    
    return specs


def tool_names(include_management: bool = False) -> List[str]:
    """Return list of tool names."""
    names = ["browse_documents", "get_document", "get_document_structure", "get_page_content"]
    if include_management:
        names.extend(["index_document", "remove_document"])
    return names


__all__ = [
    "PageIndexLocalClient",
    "ToolSpec",
    "_tool_specs",
    "tool_names",
]

