"""Simple agent activation stub."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass
class AgentProfile:
    name: str
    capabilities: list[str]


def activate_agents() -> List[AgentProfile]:
    """Returns a static list of demo agents."""
    return [
        AgentProfile(name="Navigator", capabilities=["plan", "route"]),
        AgentProfile(name="Scribe", capabilities=["log", "summarize"]),
    ]
