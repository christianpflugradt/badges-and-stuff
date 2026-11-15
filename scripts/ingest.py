#!/usr/bin/env python3
"""Validate a statistics payload and store it as data/<project>.json."""
import json
import math
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NAME = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
COMMIT = re.compile(r"^[0-9a-f]{40}$")
TIMESTAMP = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
KINDS = ("percent", "count")
MAX_METRICS = 50
MAX_LABEL = 60


def is_number(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def validate_metric(metric):
    if not isinstance(metric, dict) or set(metric) != {"id", "label", "value", "kind", "badge"}:
        raise ValueError("a metric needs exactly the fields id, label, value, kind and badge")
    if not isinstance(metric["id"], str) or not NAME.match(metric["id"]):
        raise ValueError(f"invalid metric id: {metric['id']!r}")
    label = metric["label"]
    if not isinstance(label, str) or not 0 < len(label) <= MAX_LABEL or not label.isprintable():
        raise ValueError(f"invalid label for {metric['id']}")
    if not isinstance(metric["badge"], bool):
        raise ValueError(f"badge must be true or false for {metric['id']}")
    if metric["kind"] not in KINDS:
        raise ValueError(f"invalid kind for {metric['id']}")
    value = metric["value"]
    if value is None:
        return
    if not is_number(value) or value < 0 or (metric["kind"] == "percent" and value > 100):
        raise ValueError(f"invalid value for {metric['id']}")


def validate(payload, projects):
    if not isinstance(payload, dict) or set(payload) != {"project", "commit", "timestamp", "metrics"}:
        raise ValueError("the payload needs exactly the fields project, commit, timestamp and metrics")
    if payload["project"] not in projects:
        raise ValueError(f"unknown project: {payload['project']!r}")
    if not isinstance(payload["commit"], str) or not COMMIT.match(payload["commit"]):
        raise ValueError("commit must be a full lowercase SHA")
    if not isinstance(payload["timestamp"], str) or not TIMESTAMP.match(payload["timestamp"]):
        raise ValueError("timestamp must look like 2026-01-31T12:00:00Z")
    metrics = payload["metrics"]
    if not isinstance(metrics, list) or not 0 < len(metrics) <= MAX_METRICS:
        raise ValueError(f"metrics must hold 1 to {MAX_METRICS} entries")
    for metric in metrics:
        validate_metric(metric)
    ids = [metric["id"] for metric in metrics]
    if len(set(ids)) != len(ids):
        raise ValueError("metric ids must be unique")


def read_projects():
    lines = (ROOT / "projects.txt").read_text(encoding="utf-8").splitlines()
    return {line.strip() for line in lines if line.strip()}


def main(argv):
    if len(argv) != 2:
        print("usage: ingest.py <payload.json>", file=sys.stderr)
        return 2
    try:
        payload = json.loads(Path(argv[1]).read_text(encoding="utf-8"))
        validate(payload, read_projects())
    except (OSError, ValueError) as error:
        print(f"invalid payload: {error}", file=sys.stderr)
        return 1
    target = ROOT / "data" / f"{payload['project']}.json"
    target.parent.mkdir(exist_ok=True)
    target.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(payload["project"])
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv))
    except Exception as error:  # noqa: BLE001 - every unexpected failure is reported as a technical error
        print(f"error: {error}", file=sys.stderr)
        sys.exit(2)
