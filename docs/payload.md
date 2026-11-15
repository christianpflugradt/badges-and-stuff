# Payload

A project sends one payload per run. It has exactly these fields:

```json
{
  "project": "example",
  "commit": "<full lowercase SHA>",
  "timestamp": "2026-01-31T12:00:00Z",
  "metrics": [
    { "id": "branch-coverage", "label": "branch coverage", "value": 87.3, "kind": "percent", "badge": true }
  ]
}
```

- `project` must be listed in `projects.txt`.
- `metrics` holds 1 to 50 entries with unique `id`s (lowercase words joined by `-`).
- `label` is the badge text, at most 60 printable characters.
- `kind` is `percent` (0 to 100, colored by range) or `count` (zero or above, shown as `18.3k` from 1000).
- `value` may be `null`; the badge then shows `n/a`.
- `badge` says whether a badge is rendered at `<project>/<id>.svg`. The value is published in `<project>/statistics.json` either way.

GitHub limits a dispatch payload to 65 KB and 10 top-level properties.
