"""Heartbeat utilities shared by the MCP server and autonomy loop."""

from __future__ import annotations

import socket
import time
from typing import Any, Dict


def get_heartbeat_status() -> Dict[str, Any]:
    """Return a lightweight status payload."""
    return {
        "status": "alive",
        "hostname": socket.gethostname(),
        "timestamp": time.time(),
    }


def emit_heartbeat(callback: callable | None = None) -> Dict[str, Any]:
    """Compute heartbeat status and optionally forward it to another sink."""
    payload = get_heartbeat_status()
    if callback:
        callback(payload)
    return payload
