#!/usr/bin/env python3
"""Stub script that emulates pulling secrets from Notion and writing them to disk."""

from __future__ import annotations

import os
from pathlib import Path


def main() -> None:
    secrets_path = Path(".env")
    secrets = {
        "NOTION_TOKEN": os.environ.get("NOTION_TOKEN", "stub-notion-token"),
        "SLACK_WEBHOOK": os.environ.get("SLACK_WEBHOOK", "https://example.com/webhook"),
    }
    secrets_blob = "\n".join(f"{key}={value}" for key, value in secrets.items())
    secrets_path.write_text(secrets_blob + "\n", encoding="utf-8")
    print(f"[secrets] wrote {len(secrets)} keys to {secrets_path.resolve()}")


if __name__ == "__main__":
    main()
