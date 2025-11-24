"""Lightweight SQLite-backed store used by the Core Pack ledger."""

from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Iterable, Sequence


class SqlStore:
    """Minimal helper around sqlite3 with automatic path management."""

    def __init__(self, db_path: str | Path) -> None:
        self.db_path = Path(db_path)
        if self.db_path.parent:
            self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    def _initialize(self) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS ledger_entries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    event_type TEXT NOT NULL,
                    payload TEXT DEFAULT '{}',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            conn.commit()

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_path, check_same_thread=False)

    def execute(self, query: str, params: Sequence | None = None) -> None:
        with self._connect() as conn:
            conn.execute(query, params or [])
            conn.commit()

    def executemany(self, query: str, param_set: Iterable[Sequence]) -> None:
        with self._connect() as conn:
            conn.executemany(query, param_set)
            conn.commit()

    def fetchall(self, query: str, params: Sequence | None = None) -> list[sqlite3.Row]:
        with self._connect() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(query, params or [])
            return cursor.fetchall()

    def fetchone(self, query: str, params: Sequence | None = None) -> sqlite3.Row | None:
        with self._connect() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(query, params or [])
            return cursor.fetchone()
