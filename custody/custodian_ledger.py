"""Custodian ledger built on top of the SqlStore."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

from memory.sql_store.sql_store import SqlStore


class CustodianLedger:
    """Records important events so the autonomy loop can be audited."""

    def __init__(self, db_path: str | Path | None = None) -> None:
        db_path = db_path or "data/custodian_ledger.db"
        self.store = SqlStore(db_path)

    def record_event(self, event_type: str, payload: Dict[str, Any] | None = None) -> None:
        serialized = json.dumps(payload or {})
        self.store.execute(
            "INSERT INTO ledger_entries (event_type, payload) VALUES (?, ?)",
            (event_type, serialized),
        )

    def list_events(self, limit: int = 25) -> List[Dict[str, Any]]:
        rows = self.store.fetchall(
            "SELECT id, event_type, payload, created_at FROM ledger_entries ORDER BY id DESC LIMIT ?",
            (limit,),
        )
        events: List[Dict[str, Any]] = []
        for row in rows:
            events.append(
                {
                    "id": row["id"],
                    "event_type": row["event_type"],
                    "created_at": row["created_at"],
                    "payload": json.loads(row["payload"] or "{}"),
                }
            )
        return events
