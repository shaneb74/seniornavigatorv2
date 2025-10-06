"""Lightweight documents + exports registry for the simplified flows."""
from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable, List, MutableMapping, Optional
import uuid

import streamlit as st

EXPORTS_DIR = Path("documents/exports")
EXPORTS_DIR.mkdir(parents=True, exist_ok=True)


@dataclass
class DocumentEntry:
    doc_id: str
    kind: str
    title: str
    path: Path
    created_at: str
    metadata: MutableMapping[str, object]

    def to_dict(self) -> dict:
        return {
            "doc_id": self.doc_id,
            "kind": self.kind,
            "title": self.title,
            "path": str(self.path),
            "created_at": self.created_at,
            "metadata": dict(self.metadata),
        }

    def __post_init__(self) -> None:
        if isinstance(self.path, str):
            self.path = Path(self.path)
        if not isinstance(self.metadata, dict):
            self.metadata = dict(self.metadata)


def _registry() -> MutableMapping[str, dict]:
    from .state import ensure_base_state

    ensure_base_state()
    return st.session_state.setdefault("documents_registry", {})


def register_document(
    doc_id: str,
    *,
    kind: str,
    title: str,
    content_bytes: bytes,
    metadata: Optional[MutableMapping[str, object]] = None,
) -> DocumentEntry:
    """Register or update a document export on disk and in session."""

    EXPORTS_DIR.mkdir(parents=True, exist_ok=True)
    safe_doc_id = doc_id.replace("/", "-")
    suffix = metadata.get("ext", "json") if metadata else "json"
    filename = f"{safe_doc_id}.{suffix}"
    path = EXPORTS_DIR / filename
    path.write_bytes(content_bytes)

    entry = {
        "doc_id": safe_doc_id,
        "kind": kind,
        "title": title,
        "path": str(path),
        "created_at": datetime.utcnow().isoformat(timespec="seconds") + "Z",
        "metadata": dict(metadata or {}),
    }
    registry = _registry()
    registry[safe_doc_id] = entry
    st.session_state.documents_registry = registry
    return DocumentEntry(**entry)  # type: ignore[arg-type]


def list_documents() -> List[DocumentEntry]:
    registry = _registry()
    entries = [DocumentEntry(**data) for data in registry.values()]  # type: ignore[arg-type]
    return sorted(entries, key=lambda e: e.created_at, reverse=True)


def get_document(doc_id: str) -> Optional[DocumentEntry]:
    registry = _registry()
    data = registry.get(doc_id)
    if not data:
        return None
    return DocumentEntry(**data)  # type: ignore[arg-type]


def register_json(doc_id: str, *, kind: str, title: str, payload: dict) -> DocumentEntry:
    return register_document(
        doc_id,
        kind=kind,
        title=title,
        content_bytes=json.dumps(payload, indent=2, sort_keys=True).encode("utf-8"),
        metadata={"ext": "json"},
    )


def register_user_upload(name: str, data: bytes, *, mime_type: str | None = None) -> DocumentEntry:
    doc_id = f"user_upload_{uuid.uuid4().hex}"
    metadata = {"ext": Path(name).suffix.lstrip("."), "mime": mime_type or "application/octet-stream"}
    if not metadata["ext"]:
        metadata["ext"] = "bin"
    return register_document(doc_id, kind="user_upload", title=name, content_bytes=data, metadata=metadata)
