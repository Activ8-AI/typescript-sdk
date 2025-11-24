#!/usr/bin/env python3
"""Simple autonomy loop that records ledger entries."""

from __future__ import annotations

import os
import time
import sys
from pathlib import Path
from typing import Any, Dict

import yaml

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from agent_hub.activate import activate_agents
from custody.custodian_ledger import CustodianLedger
from relay.slack_signal import send_slack_signal
from telemetry.emit_heartbeat import emit_heartbeat

CONFIG_PATH = ROOT_DIR / "configs" / "global_config.yaml"


def load_config() -> Dict[str, Any]:
    if CONFIG_PATH.exists():
        return yaml.safe_load(CONFIG_PATH.read_text(encoding="utf-8"))
    raise FileNotFoundError("missing configs/global_config.yaml")


def main() -> None:
    config = load_config()
    ledger = CustodianLedger(config["storage"]["ledger_path"])
    agents = activate_agents()
    send_slack_signal("Autonomy loop starting with agents: " + ", ".join(a.name for a in agents))

    iterations = int(os.environ.get("AUTONOMY_LOOP_ITERATIONS", "3"))
    for iteration in range(1, iterations + 1):
        heartbeat = emit_heartbeat()
        ledger.record_event(
            "AUTONOMY_LOOP",
            {
                "iteration": iteration,
                "agents": [agent.name for agent in agents],
                "heartbeat": heartbeat,
            },
        )
        print(f"[loop] iteration {iteration} recorded")
        time.sleep(0.5)

    send_slack_signal("Autonomy loop completed")


if __name__ == "__main__":
    main()
