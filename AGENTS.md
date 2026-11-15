# Working on Badges and Stuff

## Purpose

Central GitHub Pages site for statistics that my projects calculate in CI and send here. It stores
the latest values per project and renders badges for the metrics that ask for one. `docs/payload.md` is
the single reference for the payload.

## Principles

- Prefer the smallest coherent solution. The scripts use only the Python standard library; add no
  dependencies, services or abstractions for hypothetical needs.
- The payload is a contract with every project's `Statistics` workflow. Change it only together
  with `docs/payload.md`, the validation, the tests and, when needed, the projects.
- `data/*.json` is written by the `Pages` workflow only; never edit it by hand.
- Keep source, documentation and user-facing output in English. State each fact once.
- Never commit credentials.
- Review the complete change for contradictions, stale references and unnecessary additions.

## Repository governance

- Use the published Please Behave version pinned in `mise.toml`. Renovate owns the pins of tools,
  actions and the shared rule revisions; do not bump them by hand.
- Git hooks are the authoritative validation gates. `pre-commit` checks formatting and documentation;
  `pre-push` runs the complete local suite. Do not manually repeat the complete gate. Targeted tests
  and source formatting are permitted. Fix failures and retry the Git operation; inspect saved
  reports with `please status --details`. Never bypass hooks.
- Local rules live in `.please/checks/<rule>/`; shared rules come from the imports in
  `.please/config.toml`. Commit scopes are listed in `.please/commit-scopes.txt`.
- Prepare tools with `mise install` and dependencies with `mise run setup`; checks never install them.
- Work on `main`, preserve unrelated edits and commit and push coherent changes. Stop after a
  successful push; monitoring remote workflows belongs to the user.
