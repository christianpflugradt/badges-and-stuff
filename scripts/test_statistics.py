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
    def test_blends_percentages_along_the_scale(self):
        metric = {"label": "coverage", "kind": "percent"}
        self.assertEqual(render.color({**metric, "value": 0}), "#e05d44")
        self.assertEqual(render.color({**metric, "value": 85}), "#97ca00")
        self.assertEqual(render.color({**metric, "value": 100}), "#44cc11")
        self.assertNotEqual(render.color({**metric, "value": 84}), render.color({**metric, "value": 86}))

    def test_colors_counts_by_kind(self):
        count = {"label": "x", "value": 5}
        self.assertEqual(render.color({**count, "kind": "tests"}), "#00897b")
        self.assertEqual(render.color({**count, "kind": "loc"}), "#8e44ad")
        self.assertEqual(render.color({**count, "kind": "count"}), "#546e7a")

    def test_abbreviates_counts_from_one_thousand(self):
        count = {"label": "loc", "kind": "loc"}
        self.assertEqual(render.message({**count, "value": 999}), "999")
        self.assertEqual(render.message({**count, "value": 1000}), "1k")
        self.assertEqual(render.message({**count, "value": 18340}), "18.3k")

    def test_shows_unknown_values_as_not_available(self):
        metric = {"label": "coverage", "kind": "percent", "value": None}
        self.assertEqual(render.message(metric), "n/a")
        self.assertIn("n/a", render.badge(metric))

    def test_escapes_labels(self):
        metric = {"label": "a<b", "kind": "count", "value": 3}
        self.assertNotIn("a<b", render.badge(metric))


if __name__ == "__main__":
    unittest.main()
