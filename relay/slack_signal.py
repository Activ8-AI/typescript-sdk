"""Placeholder relay for Slack notifications."""

from __future__ import annotations


def send_slack_signal(message: str, channel: str = "#codex-heartbeat") -> None:
    print(f"[slack:{channel}] {message}")
