"""Naive in-memory vector store placeholder."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Sequence


@dataclass
class VectorRecord:
    key: str
    values: List[float] = field(default_factory=list)
    metadata: Dict[str, str] | None = None


class VectorStore:
    """Stores vectors in memory so downstream components can depend on it."""

    def __init__(self) -> None:
        self._records: Dict[str, VectorRecord] = {}

    def upsert(self, key: str, values: Sequence[float], metadata: Dict[str, str] | None = None) -> None:
        self._records[key] = VectorRecord(key=key, values=list(values), metadata=metadata or {})

    def get(self, key: str) -> VectorRecord | None:
        return self._records.get(key)

    def all(self) -> list[VectorRecord]:
        return list(self._records.values())
