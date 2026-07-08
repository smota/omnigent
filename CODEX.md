# CODEX.md — Codex guidance

Codex agents must read `AGENTS.md` first. `AGENTS.md` remains the shared
repository guidance and this file is only the Codex-specific adapter.

## Multi-agent SDLC workflow (fork-local enablement)

<!-- fork-local: multi-agent-sdlc enablement; exclude from upstream functionality PRs -->

This fork uses `multi-agent-sdlc` for issue-scoped development while preserving
this repository's existing contributor rules. Treat this file as fork-local
process guidance: when opening functionality PRs to `omnigent-ai/omnigent`, base
work on `upstream/main` or cherry-pick only functionality commits so these
process-only edits are not included.

- Enabled agents: Claude and Codex only.
- Default execution: single-agent per issue, with optional routed subagents when
  they add clear value.
- Branch strategy: one issue branch per task, e.g.
  `feat/windows-issue-1-psmux-backend`.
- Follow the PR template at `.github/pull_request_template.md`.
- Run the same validation expected by `AGENTS.md` and `CONTRIBUTING.md`.
- Scratch artifacts such as `.agent-runs/` are local workflow state and must not
  be committed.

## Validation defaults

Use the repository-standard checks unless the active issue documents a narrower
scope:

```bash
uv run pytest
uv run ruff check .
uv run ruff format --check .
pre-commit run --all-files
```

When touching `web/`, also run:

```bash
cd web
npm run lint
npm run build
```
