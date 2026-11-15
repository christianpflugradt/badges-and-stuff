#!/usr/bin/env python3
"""Render the Pages site from data/*.json: an SVG badge per metric that asks for one, plus an index."""

import json
import shutil
import sys
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHAR_WIDTH = 7
PADDING = 10
UNKNOWN_COLOR = "#9f9f9f"
COUNT_COLOR = "#007ec6"
PERCENT_COLORS = ((50, "#e05d44"), (70, "#fe7d37"), (85, "#dfb317"), (90, "#97ca00"))
PERCENT_TOP_COLOR = "#4c1"


def message(metric):
    value = metric["value"]
    if value is None:
        return "n/a"
    if metric["kind"] == "percent":
        return f"{value:.1f}%"
    if value >= 1000:
        return f"{value / 1000:.1f}".rstrip("0").rstrip(".") + "k"
    return str(int(value)) if float(value).is_integer() else f"{value:.2f}"


def color(metric):
    value = metric["value"]
    if value is None:
        return UNKNOWN_COLOR
    if metric["kind"] == "count":
        return COUNT_COLOR
    return next((c for limit, c in PERCENT_COLORS if value < limit), PERCENT_TOP_COLOR)


def badge(metric):
    label = metric["label"]
    text = message(metric)
    label_width = len(label) * CHAR_WIDTH + PADDING
    value_width = len(text) * CHAR_WIDTH + PADDING
    width = label_width + value_width
    label_x = label_width / 2
    value_x = label_width + value_width / 2
    title = escape(f"{label}: {text}")
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="20" role="img" aria-label="{title}">
  <title>{title}</title>
  <clipPath id="clip"><rect width="{width}" height="20" rx="3" fill="#fff"/></clipPath>
  <g clip-path="url(#clip)">
    <rect width="{label_width}" height="20" fill="#555"/>
    <rect x="{label_width}" width="{value_width}" height="20" fill="{color(metric)}"/>
  </g>
  <g fill="#fff" text-anchor="middle" font-family="Verdana, DejaVu Sans, sans-serif" font-size="11">
    <text x="{label_x}" y="14">{escape(label)}</text>
    <text x="{value_x}" y="14">{escape(text)}</text>
  </g>
</svg>
"""


def index(entries):
    rows = []
    for project, payload in entries:
        items = "".join(
            f'<li><img src="{escape(project)}/{escape(m["id"])}.svg" alt="{escape(m["label"])}"></li>'
            if m["badge"]
            else f"<li>{escape(m['label'])}: {escape(message(m))}</li>"
            for m in payload["metrics"]
        )
        rows.append(
            f"<h2>{escape(project)}</h2><p>Commit {escape(payload['commit'][:7])}, "
            f"{escape(payload['timestamp'])}</p><ul>{items}</ul>"
        )
    return (
        '<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Statistics</title></head>'
        f"<body><h1>Statistics</h1>{''.join(rows)}</body></html>\n"
    )


def main():
    site = ROOT / "site"
    shutil.rmtree(site, ignore_errors=True)
    site.mkdir()
    (site / ".nojekyll").touch()
    entries = []
    for path in sorted((ROOT / "data").glob("*.json")):
        payload = json.loads(path.read_text(encoding="utf-8"))
        project = path.stem
        directory = site / project
        directory.mkdir()
        for metric in (m for m in payload["metrics"] if m["badge"]):
            (directory / f"{metric['id']}.svg").write_text(badge(metric), encoding="utf-8")
        shutil.copyfile(path, directory / "statistics.json")
        entries.append((project, payload))
    (site / "index.html").write_text(index(entries), encoding="utf-8")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as error:  # noqa: BLE001 - every unexpected failure is reported as a technical error
        print(f"error: {error}", file=sys.stderr)
        sys.exit(2)
