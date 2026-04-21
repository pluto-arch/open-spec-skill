#!/usr/bin/env python3
"""Append Open Spec workflow telemetry events to a JSONL file."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Emit one Open Spec workflow event")
    parser.add_argument("--feature", required=True, help="Feature slug")
    parser.add_argument("--stage", required=True, help="Stage name")
    parser.add_argument("--role", required=True, help="Role name")
    parser.add_argument("--event", required=True, help="Event type, e.g. stage_start/stage_end/task_update/gate_result")
    parser.add_argument("--status", default="info", help="Status: in_progress/completed/failed/info")
    parser.add_argument("--progress", type=int, default=-1, help="Progress percentage 0-100; -1 for unknown")
    parser.add_argument("--message", default="", help="Human-readable event message")
    parser.add_argument("--ids", default="", help="Comma-separated IDs like FR-001,TASK-002")
    parser.add_argument(
        "--log-file",
        default="docs/open-spec/telemetry/events.jsonl",
        help="Target JSONL file",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    event = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "feature": args.feature,
        "stage": args.stage,
        "role": args.role,
        "event": args.event,
        "status": args.status,
        "progress": args.progress,
        "message": args.message,
        "ids": [item.strip() for item in args.ids.split(",") if item.strip()],
    }

    out_path = Path(args.log_file)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")

    print(f"Event appended: {out_path}")


if __name__ == "__main__":
    main()
