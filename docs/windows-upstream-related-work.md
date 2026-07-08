# Windows parity: upstream related work review

<!-- fork-local: planning note for smota/omnigent; exclude from upstream functionality PRs -->

This note maps open `smota/omnigent` Windows-parity issues to likely related open
work in `omnigent-ai/omnigent`. Use it before implementation so fork work can
cherry-pick, rebase, or wait for upstream changes instead of reworking the same
areas.

Reviewed on 2026-07-08:

- Fork issues: <https://github.com/smota/omnigent/issues>
- Upstream open PRs: <https://github.com/omnigent-ai/omnigent/pulls>
- Upstream open issues: <https://github.com/omnigent-ai/omnigent/issues>

## Highest-priority upstream work to consider first

| Upstream item | Why it matters for Windows parity | Suggested fork action |
| --- | --- | --- |
| PR [omnigent-ai#1993](https://github.com/omnigent-ai/omnigent/pull/1993) `fix(setup): avoid termios setup crash on Windows` | Direct Windows startup/setup fix. It routes setup menus away from POSIX `termios` and removes remaining `os.getuid()` assumptions from native bridge temp-root setup. This directly affects fork issues #2 and #4 and partially de-risks #1. | Bring into the fork before new Windows setup/dev work. Test natively on Windows first. |
| Issue [omnigent-ai#16](https://github.com/omnigent-ai/omnigent/issues/16) `Is native Windows support in scope, or should docs recommend WSL2?` | Existing upstream scope discussion for the whole Windows effort. | Reference in fork planning; keep fork issues framed as a concrete implementation track. |
| Issue [omnigent-ai#2003](https://github.com/omnigent-ai/omnigent/issues/2003) `Pluggable terminal multiplexer backend (tmux / herdr / zellij)` | Directly overlaps the fork psmux backend idea. It already generalizes the terminal layer beyond tmux. | Align fork issue #1 with this abstraction rather than building psmux as a one-off. |
| Issue [omnigent-ai#1930](https://github.com/omnigent-ai/omnigent/issues/1930) `omni host crash-loops on Windows: os.getuid() in *_native_bridge.py modules` | Direct Windows host crash/root cause. PR #1993 appears to address part of this. | Verify whether #1993 closes enough of this before starting fork issue #2. |
| PR [omnigent-ai#2033](https://github.com/omnigent-ai/omnigent/pull/2033) `test(terminal): RED specs for adopt-don't-reap on runner restart` | Terminal lifecycle/reaper behavior is adjacent to replacing tmux assumptions and may affect a psmux backend. | Review before changing `omnigent.terminals.*` or runner terminal adoption code. |
| PR [omnigent-ai#2031](https://github.com/omnigent-ai/omnigent/pull/2031) `fix(sessions): auto-respawn orphaned host-bound runners` | Runner/host resilience work; Windows host parity will rely on robust respawn behavior. | Consider after #1993 if fork issue #5 touches runner startup/transport. |
| PR [omnigent-ai#1923](https://github.com/omnigent-ai/omnigent/pull/1923) `fix(runner): per-uid harness tmp parent on POSIX for multi-user hosts` | POSIX-specific temp-parent work may conflict conceptually with Windows temp-root decisions. | Check for assumptions before porting temp path / socket code. |
| Issue [omnigent-ai#2113](https://github.com/omnigent-ai/omnigent/issues/2113) `Multi-user hosts: shared /tmp/omnigent socket parent breaks...` | Socket/temp-parent isolation problem; not Windows-specific, but relevant to fork issue #5. | Use as prior art for transport/temp-root design. |
| Issue [omnigent-ai#561](https://github.com/omnigent-ai/omnigent/issues/561) `runner: orphaned codex app-server groups and tmux servers accumulate...` | Native terminal teardown/reaper stability. | Review before implementing psmux close/reap semantics. |
| Issue [omnigent-ai#1694](https://github.com/omnigent-ai/omnigent/issues/1694) `Reliability: parallel code-fix missions fail silently... 5s tmux timeout...` | Highlights tmux timeout and orphan behavior that a new mux backend should avoid. | Fold lessons into psmux acceptance tests. |

## Mapping by fork issue

### Fork #1 — psmux-backed native terminal backend

Fork issue: <https://github.com/smota/omnigent/issues/1>

Most related upstream:

- [omnigent-ai#2003](https://github.com/omnigent-ai/omnigent/issues/2003) —
  pluggable terminal multiplexer backend. This is the closest conceptual match.
  The fork should prefer a general `TerminalMuxBackend`-style design rather than
  hard-coding psmux into existing tmux call sites.
- [omnigent-ai#561](https://github.com/omnigent-ai/omnigent/issues/561) —
  orphaned codex app-server groups and tmux servers. Important for psmux close
  and crash cleanup semantics.
- [omnigent-ai#1694](https://github.com/omnigent-ai/omnigent/issues/1694) —
  tmux timeout/reliability failures in large worktrees. Useful as negative test
  scenarios for a psmux backend.
- [omnigent-ai#2033](https://github.com/omnigent-ai/omnigent/pull/2033) —
  terminal adoption/reaper RED specs.
- [omnigent-ai#394](https://github.com/omnigent-ai/omnigent/issues/394) —
  first-class native terminal support for another terminal family. Not Windows
  specific, but relevant to backend extensibility.

Suggested sequence:

1. Bring/test #1993 first so Windows imports/setup are less broken.
2. Read #2003 and decide whether to make the fork implementation a direct
   implementation of that broader abstraction.
3. Add psmux smoke tests around launch, send, capture, resize, close, and
   crash/reap.

### Fork #2 — native Windows development/test workflow

Fork issue: <https://github.com/smota/omnigent/issues/2>

Most related upstream:

- [omnigent-ai#1993](https://github.com/omnigent-ai/omnigent/pull/1993) — direct
  Windows setup/import fix.
- [omnigent-ai#1930](https://github.com/omnigent-ai/omnigent/issues/1930) —
  Windows crash loop from `os.getuid()` in native bridge modules.
- [omnigent-ai#1314](https://github.com/omnigent-ai/omnigent/issues/1314) —
  backend-only local dev docs. Not Windows-specific, but helps define a smaller
  core/server validation path.
- [omnigent-ai#523](https://github.com/omnigent-ai/omnigent/issues/523) —
  pexpect E2E starvation; relevant because Windows excludes pexpect/PTY tests and
  needs a separate test story.

Suggested sequence:

1. Import or cherry-pick #1993.
2. Run the focused Windows tests named in #1993, then define the fork's
   `windows_core` subset.
3. Only after core setup works, attempt pre-commit and broader pytest parity.

### Fork #3 — Windows sandbox and egress parity beyond Job Objects

Fork issue: <https://github.com/smota/omnigent/issues/3>

Most related upstream:

- [omnigent-ai#659](https://github.com/omnigent-ai/omnigent/issues/659) —
  microVM backend for sandbox. Not Windows-native, but relevant to sandbox
  backend abstraction.
- [omnigent-ai#963](https://github.com/omnigent-ai/omnigent/issues/963) — Declaw
  sandbox provider. Relevant to adding non-bwrap/non-seatbelt sandbox options.
- [omnigent-ai#1542](https://github.com/omnigent-ai/omnigent/issues/1542) — trust
  boundary for credential proxy file/command sources. Important if Windows
  egress/credential proxy support is partial.
- [omnigent-ai#2070](https://github.com/omnigent-ai/omnigent/issues/2070) — file
  tools hard-confined to workspace despite sandbox grants. Relevant to how much
  sandbox policy is enforced in tools vs OS backend.
- [omnigent-ai#1951](https://github.com/omnigent-ai/omnigent/pull/1951) and
  [omnigent-ai#2049](https://github.com/omnigent-ai/omnigent/issues/2049) —
  existing bwrap/seatbelt edge cases. Useful prior art for error messages and
  fallback behavior.

Suggested sequence:

1. Do not implement Windows egress enforcement until the current Windows core
   setup and terminal plan are stable.
2. First document exact `windows_job` guarantees and validation errors.
3. Split filesystem isolation and network egress into separate implementation
   issues once a backend choice is made.

### Fork #4 — native PowerShell installer and dependency checks

Fork issue: <https://github.com/smota/omnigent/issues/4>

Most related upstream:

- [omnigent-ai#1993](https://github.com/omnigent-ai/omnigent/pull/1993) — setup
  must not crash on Windows before a Windows installer is useful.
- [omnigent-ai#548](https://github.com/omnigent-ai/omnigent/issues/548) — missing
  dependency install suggestions in UI. Relevant to installer/dependency
  messaging.
- [omnigent-ai#890](https://github.com/omnigent-ai/omnigent/issues/890) — npm
  install permission failure for Claude CLI. Dependency-install UX prior art.
- Existing repo `tests/scripts/test_install_oss.py` — POSIX installer test model
  to mirror for PowerShell.

Suggested sequence:

1. Bring/test #1993 first.
2. Implement a read-only Windows dependency doctor before an installer.
3. Add `install_oss.ps1` only after the dependency story is stable.

### Fork #5 — cross-platform runner transport fallback

Fork issue: <https://github.com/smota/omnigent/issues/5>

Most related upstream:

- [omnigent-ai#2113](https://github.com/omnigent-ai/omnigent/issues/2113) — shared
  `/tmp/omnigent` socket parent breaks multi-user hosts.
- [omnigent-ai#1923](https://github.com/omnigent-ai/omnigent/pull/1923) — per-uid
  harness tmp parent on POSIX.
- [omnigent-ai#2031](https://github.com/omnigent-ai/omnigent/pull/2031) —
  auto-respawn orphaned host-bound runners.
- [omnigent-ai#2039](https://github.com/omnigent-ai/omnigent/issues/2039) — host
  exits on transient 4xx during server restart.
- [omnigent-ai#1857](https://github.com/omnigent-ai/omnigent/issues/1857) and
  [omnigent-ai#2067](https://github.com/omnigent-ai/omnigent/pull/2067) — host
  tunnel reconnect/offline status.
- [omnigent-ai#1730](https://github.com/omnigent-ai/omnigent/issues/1730) — TLS
  verification in websocket tunnels. Not UDS-specific, but transport-related.

Suggested sequence:

1. Audit `omnigent.runner.transports.uds` and terminal socket identifiers after
   applying any upstream runner/host resilience PRs we choose to import.
2. Prefer an opaque transport locator abstraction rather than exposing Windows
   named-pipe/TCP details into higher layers.
3. Add Windows tests for runner start/connect/health before psmux integration
   depends on it.

### Fork #6 — Windows CI and manual QA matrix

Fork issue: <https://github.com/smota/omnigent/issues/6>

Most related upstream:

- [omnigent-ai#1993](https://github.com/omnigent-ai/omnigent/pull/1993) — gives a
  focused Windows regression test list to seed the matrix.
- [omnigent-ai#16](https://github.com/omnigent-ai/omnigent/issues/16) — scope
  framing for Windows support.
- [omnigent-ai#1969](https://github.com/omnigent-ai/omnigent/pull/1969) and
  [omnigent-ai#1622](https://github.com/omnigent-ai/omnigent/issues/1622) —
  cross-harness evaluation runner. Could later validate cross-harness parity, but
  probably not a prerequisite for initial Windows CI.
- [omnigent-ai#2066](https://github.com/omnigent-ai/omnigent/pull/2066) — CI
  cache change; low direct relevance but shows active CI churn.

Suggested sequence:

1. Start with a native Windows core job that only covers known-supported paths.
2. Keep psmux tests manual/optional until psmux installation is reliable in CI.
3. Avoid changing upstream workflows in the fork until the test subset is known
   to be stable locally.

## Potentially relevant but lower priority

These are not direct prerequisites for Windows parity, but may affect the same
files or test areas:

- [omnigent-ai#2193](https://github.com/omnigent-ai/omnigent/pull/2193) —
  claude-native sub-agent background task delivery. Touches native forwarder and
  session status semantics; relevant if psmux work tests native subagents.
- [omnigent-ai#2192](https://github.com/omnigent-ai/omnigent/pull/2192) — policy
  hook reauth logging. Touches native policy hooks used by multiple harnesses.
- [omnigent-ai#2077](https://github.com/omnigent-ai/omnigent/pull/2077) and
  [omnigent-ai#2055](https://github.com/omnigent-ai/omnigent/issues/2055) —
  elicitation delivery timing. Relevant if Windows tests include approval flows.
- [omnigent-ai#2044](https://github.com/omnigent-ai/omnigent/pull/2044) and
  [omnigent-ai#2020](https://github.com/omnigent-ai/omnigent/pull/2020) — human
  approval waits/watchdogs. Adjacent to native terminal long waits.
- [omnigent-ai#1935](https://github.com/omnigent-ai/omnigent/pull/1935) — host
  re-exec via login shell for GUI launch. POSIX/macOS-focused but conceptually
  similar to Windows PATH problems.
- [omnigent-ai#1896](https://github.com/omnigent-ai/omnigent/pull/1896) — thread
  session workspace cwd into spawned harness subprocesses. Relevant to Windows
  subprocess cwd correctness.
- [omnigent-ai#1860](https://github.com/omnigent-ai/omnigent/issues/1860) — runner
  PYTHONPATH injection shadows project packages. Could affect Windows dev tests.

## Recommended import strategy before fork implementation

1. **Import/test PR #1993 first.** It is the clearest direct dependency for
   Windows setup and native import stability.
2. **Decide terminal backend design against issue #2003.** If upstream is likely
   to accept a pluggable mux abstraction, implement psmux as a backend under that
   design instead of a Windows-only patch series.
3. **Defer installer and CI changes until the core Windows test subset passes.**
   Installer/CI should encode known-good behavior, not discover it.
4. **Keep fork-local planning/process files separate from upstream functionality
   branches.** Start upstream PR branches from `upstream/main` and cherry-pick
   only functionality commits.
