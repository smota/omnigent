# Fork-local workflow notes

<!-- fork-local: multi-agent-sdlc enablement; exclude from upstream functionality PRs -->

This file documents process-only enablement for the `smota/omnigent` fork. It is
not part of functionality intended for upstream PRs to `omnigent-ai/omnigent`.

## Why this exists

The fork uses `multi-agent-sdlc` to manage issue-scoped development and review
while keeping upstream functionality PRs focused on product code changes.

## Enabled defaults

- Agents: Claude and Codex only.
- Execution mode: single-agent by default, optional routed subagents when useful.
- Branches: one issue branch per task, e.g. `feat/windows-issue-1-psmux-backend`.
- GitHub automation: use issues and the existing PR template; do not add new
  workflows during onboarding.

## Keeping fork-local process edits out of upstream PRs

Use one of these strategies before opening a PR to `omnigent-ai/omnigent`:

1. **Preferred: start functionality branches from upstream.**

   ```bash
   git fetch upstream
   git switch -c feat/windows-issue-1-psmux-backend upstream/main
   ```

   Implement only functionality on that branch, then push it to the fork and
   open the PR against `omnigent-ai/omnigent:main`.

2. **If work started from the fork-local onboarding branch, rebase it off.**

   Keep the onboarding/process commit separate, then rebase only functionality
   commits onto upstream main:

   ```bash
   git fetch upstream
   git rebase --onto upstream/main <fork-local-onboarding-commit> <feature-branch>
   ```

3. **For already-mixed branches, cherry-pick functionality commits.**

   ```bash
   git fetch upstream
   git switch -c upstream-pr/windows-issue-1 upstream/main
   git cherry-pick <functionality-commit>...
   ```

Before opening an upstream PR, verify that process-only files are absent from the
diff:

```bash
git diff --name-only upstream/main...HEAD | grep -E '^(AGENTS.md|CLAUDE.md|CODEX.md|docs/fork-local-workflow.md)$' && \
  echo "Remove fork-local files before upstream PR"
```
