#!/usr/bin/env python3
"""Serve a lightweight Open Spec workflow dashboard from JSONL telemetry."""

from __future__ import annotations

import argparse
import json
import mimetypes
from collections import defaultdict
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse


def read_events(path: Path) -> list[dict]:
    if not path.exists():
        return []
    events = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            events.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return events


def build_summary(events: list[dict]) -> dict:
    stage_progress: dict[str, int] = {}
    status_count: dict[str, int] = defaultdict(int)
    features = set()

    for ev in events:
        stage = ev.get("stage", "unknown")
        progress = ev.get("progress", -1)
        if isinstance(progress, int) and progress >= 0:
            stage_progress[stage] = max(stage_progress.get(stage, 0), progress)

        status = ev.get("status", "info")
        status_count[status] += 1

        feature = ev.get("feature")
        if feature:
            features.add(feature)

    return {
        "event_count": len(events),
        "feature_count": len(features),
        "stage_progress": dict(sorted(stage_progress.items())),
        "status_count": dict(sorted(status_count.items())),
        "latest_events": list(reversed(events[-30:])),
    }


class Handler(BaseHTTPRequestHandler):
    log_file: Path = Path("docs/open-spec/telemetry/events.jsonl")
    static_dir: Path = Path("skills/open-spec/scripts/wwwroot")

    def _json(self, payload: dict) -> None:
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def _file(self, file_path: Path) -> None:
        if not file_path.exists() or not file_path.is_file():
            self.send_response(404)
            self.end_headers()
            return

        data = file_path.read_bytes()
        content_type, _ = mimetypes.guess_type(str(file_path))
        if content_type is None:
            content_type = "application/octet-stream"

        self.send_response(200)
        self.send_header("Content-Type", f"{content_type}; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path == "/api/events":
            self._json({"events": read_events(self.log_file)})
            return
        if parsed.path == "/api/summary":
            self._json(build_summary(read_events(self.log_file)))
            return

        rel = "index.html" if parsed.path in ("", "/") else parsed.path.lstrip("/")
        candidate = (self.static_dir / rel).resolve()
        base = self.static_dir.resolve()

        if base == candidate or base in candidate.parents:
            self._file(candidate)
            return

        self.send_response(403)
        self.end_headers()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Open Spec workflow monitor server")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--log-file", default="docs/open-spec/telemetry/events.jsonl")
    parser.add_argument("--static-dir", default="skills/open-spec/scripts/wwwroot")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    Handler.log_file = Path(args.log_file)
    Handler.static_dir = Path(args.static_dir)
    server = ThreadingHTTPServer((args.host, args.port), Handler)
    print(f"Open Spec monitor running at http://{args.host}:{args.port}")
    print(f"Telemetry file: {Handler.log_file}")
    print(f"Static dir: {Handler.static_dir}")
    server.serve_forever()


if __name__ == "__main__":
    main()
