#!/usr/bin/env python3
"""FastAPI server that exposes MCP relay health + heartbeat endpoints."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Dict

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import uvicorn
import yaml
from fastapi import FastAPI

from custody.custodian_ledger import CustodianLedger
from telemetry.emit_heartbeat import emit_heartbeat

CONFIG_PATH = ROOT_DIR / "configs" / "global_config.yaml"


def load_config() -> Dict[str, Any]:
    if CONFIG_PATH.exists():
        return yaml.safe_load(CONFIG_PATH.read_text(encoding="utf-8"))
    return {
        "app": {"name": "codex-core-pack", "environment": "development"},
        "mcp": {"host": "0.0.0.0", "port": 8000},
        "heartbeat": {"enabled": True, "interval_seconds": 5},
        "storage": {"ledger_path": "data/custodian_ledger.db"},
    }


config = load_config()
app = FastAPI(title=config["app"]["name"])
ledger = CustodianLedger(config["storage"]["ledger_path"])


@app.get("/health")
def health() -> Dict[str, Any]:
    return {
        "status": "ok",
        "app": config["app"]["name"],
        "environment": config["app"]["environment"],
    }


@app.get("/heartbeat")
def heartbeat() -> Dict[str, Any]:
    payload = emit_heartbeat()
    ledger.record_event("HEARTBEAT", payload)
    return payload


def main() -> None:
    host = config["mcp"]["host"]
    port = int(config["mcp"]["port"])
    print(f"[mcp] starting relay server on {host}:{port}")
    uvicorn.run("orchestration.MCP.relay_server:app", host=host, port=port, reload=False)


if __name__ == "__main__":
    main()
