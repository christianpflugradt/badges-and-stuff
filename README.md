# Badges and Stuff

Central GitHub Pages site for the statistics of my projects. Each project calculates its own
numbers in CI and sends them here. This repository stores the latest values per project and
renders an SVG badge for each metric that asks for one; other statistics are only stored.

```text
https://christianpflugradt.github.io/badges-and-stuff/<project>/<metric>.svg
```

## How it works

1. A project's `Statistics` workflow sends a `repository_dispatch` event of type `statistics`.
2. The `Pages` workflow validates the payload, commits it to `data/<project>.json`, renders
   the site and deploys it. Runs are queued, so updates apply one after another.

## Payload

The `client_payload` has exactly these fields (GitHub limits a payload to 65 KB and 10
top-level properties):

```json
{
  "project": "pumpbuddy",
  "commit": "<full lowercase SHA>",
  "timestamp": "2026-01-31T12:00:00Z",
  "metrics": [
    { "id": "backend-coverage", "label": "backend branch coverage", "value": 87.3, "kind": "percent", "badge": true }
  ]
}
```

- `project` must be listed in `projects.txt`.
- `id` is lowercase words joined by `-` and unique per payload; `label` is the badge text.
- `kind` is `percent` (0 to 100, colored by range) or `count` (any number zero or above).
- `badge` says whether a badge is rendered; the value is published in `statistics.json` either way.
- `value` may be `null` when a number is not available; the badge then shows `n/a`.

## Onboarding a project

1. Add its name to `projects.txt`.
2. Give the project a repository secret `STATISTICS_TOKEN`: a fine-grained token limited to
   this repository with the permission Contents: write. It expires at most after a year.
3. Add a `Statistics` workflow that sends the payload on pushes to `main`.

## Setup

Enable Pages with the source set to GitHub Actions.
Tests: `python3 -m unittest discover -s scripts`.
