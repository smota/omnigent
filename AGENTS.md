# Agent guidance

Guidance for AI agents (Claude Code, Copilot, Cursor, etc.) working in this
repository. See `CONTRIBUTING.md` for the full contributor workflow.

## Multi-agent SDLC workflow (fork-local enablement)

<!-- fork-local: multi-agent-sdlc enablement; exclude from upstream functionality PRs -->

This fork uses `multi-agent-sdlc` for issue-scoped development while preserving
this repository's existing contributor rules. Treat this section as fork-local
process guidance: when opening functionality PRs to `omnigent-ai/omnigent`, base
work on `upstream/main` or cherry-pick only functionality commits so these
process-only edits are not included.

- Enabled agents: Claude and Codex only.
- Default execution: single-agent per issue, with optional routed subagents when
  they add clear value.
- Branch strategy: one issue branch per task, e.g.
  `feat/windows-issue-1-psmux-backend`.
- Scratch artifacts such as `.agent-runs/` are local workflow state and must not
  be committed.
- Preserve existing instructions in this file, `CLAUDE.md`, `CODEX.md`, and the
  PR template; merge process updates instead of overwriting project guidance.

## Committing

Run the `pre-commit` hook before committing (`pre-commit run --all-files`, or
let it run on staged files via `git commit`). Fix any issues it reports so the
commit lands clean — CI runs the same checks.

## Pull requests

When you open a pull request, fill in the repo's PR template at
`.github/pull_request_template.md` (case-sensitive on Linux — note the lowercase
filename). Keep every section and checkbox row so reviewers can skim them.

- **Summary** — what changed and why.
- **Test Plan** — how you verified it.
- **Demo** — a **video or images** showing the change. Expected on contributor
  PRs for UI / frontend changes (check the "UI / frontend change" box under
  *Type of change*) so reviewers can see the new behaviour without checking out
  the branch. Use `N/A` for non-visual changes.
- **Type of change** / **Test coverage** — check all that apply (at least one
  each).
- **Coverage notes** — required if you checked "Manual verification completed"
  or "Not applicable".

Generate the description from the actual diff and this session's context — lead
with the motivation, then the change. Don't pass a `--body` that skips these
sections.

## Code comments

Keep comments short and focused on the code, not on the change history.

- **Keep them brief** — prefer one or two lines. Avoid comments longer than
  three lines; if you need more, the code likely needs refactoring or a doc
  string, not a wall of inline commentary.
- **Describe the scenario, not the PR** — explain *what* the code handles or
  *why* it exists, in terms a future reader needs. Don't reference PR numbers,
  issue numbers, or ticket IDs (e.g. `#1646`, `fixes JIRA-123`); the scenario
  should be clear without chasing external links.
