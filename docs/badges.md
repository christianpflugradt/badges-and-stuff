# Badges

Reference for the badges that projects show in their README.

## Layout

Group badges in rows, one Markdown paragraph per row, separated by a blank line:

1. Project row: `build`, `release`, `license`.
2. One row per component: `tests`, `coverage`, `LOC`. A project with a single component has one such row.

Projects that release several components together show one `release` badge.

## Names

Labels are lowercase and short; the label alone must be understandable.

- Prefix the component only when a project has several: `backend tests`, `renderer coverage`.
- `LOC` stands for production lines of code, without tests and generated code.
- Name the coverage by what it measures when a project reports several kinds, for example `branch coverage` and `instr. coverage`. Otherwise use `coverage`.

## Colors

| Badge | Kind | Color |
| --- | --- | --- |
| `build` | GitHub status badge | GitHub's own |
| `release` | shields.io | `#007ec6` (default blue) |
| `license` | shields.io | `#3949ab` |
| `tests` | `tests` | `#00897b` |
| `LOC` | `loc` | `#8e44ad` |
| other counts | `count` | `#546e7a` |
| unknown value | any | `#9f9f9f` |

Percentages follow one scale for every project. The color is blended linearly between these points:

| Value | Color |
| --- | --- |
| 0 | `#e05d44` |
| 50 | `#fe7d37` |
| 70 | `#dfb317` |
| 85 | `#97ca00` |
| 100 | `#44cc11` |

Red, orange, yellow and green are reserved for percentages and build status; use none of them for other badges.

## Width

A badge is as wide as its text: 6 px per character, plus 10 px padding for the label and 10 px for the value.

## Shields.io badges

Set the license color in the URL, for example `https://img.shields.io/badge/license-Apache%202.0-3949ab.svg`. Keep the release badge at its default color.
