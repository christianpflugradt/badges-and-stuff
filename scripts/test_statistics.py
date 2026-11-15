import unittest

import ingest
import render

PROJECTS = {"pumpbuddy"}


def payload(**changes):
    result = {
        "project": "pumpbuddy",
        "commit": "a" * 40,
        "timestamp": "2026-01-31T12:00:00Z",
        "metrics": [
            {"id": "backend-coverage", "label": "backend coverage", "value": 87.34, "kind": "percent", "badge": True}
        ],
    }
    result.update(changes)
    return result


class IngestTest(unittest.TestCase):
    def test_accepts_a_valid_payload(self):
        ingest.validate(payload(), PROJECTS)

    def test_accepts_an_unknown_value(self):
        metrics = [{"id": "tests", "label": "tests", "value": None, "kind": "count", "badge": True}]
        ingest.validate(payload(metrics=metrics), PROJECTS)

    def test_rejects_an_unlisted_project(self):
        with self.assertRaises(ValueError):
            ingest.validate(payload(project="other"), PROJECTS)

    def test_rejects_a_percentage_above_100(self):
        metrics = [{"id": "coverage", "label": "coverage", "value": 100.1, "kind": "percent", "badge": True}]
        with self.assertRaises(ValueError):
            ingest.validate(payload(metrics=metrics), PROJECTS)

    def test_rejects_duplicate_metric_ids(self):
        metric = {"id": "tests", "label": "tests", "value": 1, "kind": "count", "badge": False}
        with self.assertRaises(ValueError):
            ingest.validate(payload(metrics=[metric, metric]), PROJECTS)

    def test_rejects_extra_fields(self):
        with self.assertRaises(ValueError):
            ingest.validate({**payload(), "extra": 1}, PROJECTS)


class RenderTest(unittest.TestCase):
    def test_colors_percentages_by_range(self):
        metric = {"label": "coverage", "kind": "percent"}
        self.assertEqual(render.color({**metric, "value": 10}), "#e05d44")
        self.assertEqual(render.color({**metric, "value": 95}), "#4c1")

    def test_shows_unknown_values_as_not_available(self):
        metric = {"label": "coverage", "kind": "percent", "value": None}
        self.assertEqual(render.message(metric), "n/a")
        self.assertIn("n/a", render.badge(metric))

    def test_escapes_labels(self):
        metric = {"label": "a<b", "kind": "count", "value": 3}
        self.assertNotIn("a<b", render.badge(metric))


if __name__ == "__main__":
    unittest.main()
