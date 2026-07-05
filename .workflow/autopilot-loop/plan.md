# Autopilot Loop Setup

## Goal

Set up a bounded Cursor loop that keeps task state in files, dispatches an implementation subagent for each queued task, and requires an independent verification run before a task can be marked complete.

Original user goal: "set up a loop inside cursor to keep creating subagents for every task + a verification run."

## Success Criteria

- Cursor command exists for the bounded autopilot loop.
- Queue schema exists for task goal, scope, allowed files, acceptance criteria, verification commands, attempts, and evidence.
- Loop state exists under `.workflow/autopilot-loop/`.
- The loop requires an implementer artifact and a fresh-context verifier artifact before marking a task done.
- Stop conditions cover budget caps, approval gates, empty diffs, repeated failures, missing verification, and human verification needs.
- The run directory passes the repo's `verify_run.py` structural check.

## Constraints

- Do not install dependencies.
- Do not edit `.codex` or `.claude`.
- Do not clone repositories or write outside the workspace.
- Do not alter existing phase workflow state while adding this setup.
- Default to one task per loop invocation until the user explicitly increases `--max-tasks`.
- Treat implementer output as a claim, not evidence.

## Risks

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Loop keeps going after a bad task | Repeated broken edits | Default `max_tasks_per_run` is 1; stop on failed verification or repeated failure. |
| Implementer and verifier share assumptions | Soft self-review | Require fresh-context verifier and separate result artifact. |
| Task scope widens silently | Unrelated churn | Queue item has `files_allowed`; controller blocks unexpected writes. |
| Verification command is missing or weak | False completion | Queue stores explicit commands; missing verification blocks completion. |
| Permissioned setup happens without approval | Config or network risk | Command stops before dependency installs, `.codex`/`.claude` edits, clones, external writes, deploys, or migrations. |

## Work Packets

| ID | Objective | Ownership | Status |
| --- | --- | --- | --- |
| 01-loop-command | Add Cursor command that drives the bounded loop. | orchestrator | done |
| 02-queue-contract | Add machine-readable queue and human task template. | orchestrator | done |
| 03-run-state | Add durable `.workflow/autopilot-loop/` state and orchestration docs. | orchestrator | done |
| 04-verify-setup | Run structural validation and JSON checks. | verifier | pending |

## Verification

| ID | Requirement | Check | Expected |
| --- | --- | --- | --- |
| VERIFY-AUTO-001 | Run structure | `python awesome-ai-workflow/ultimate-agentic-workflow/scripts/verify_run.py --run-dir .workflow/autopilot-loop` | pass |
| VERIFY-AUTO-002 | Queue JSON | `python -m json.tool .workflow/autopilot-queue.json` | pass |
| VERIFY-AUTO-003 | Command present | `.cursor/commands/gsd-autopilot-loop.md` exists and references queue/state files | pass |
| VERIFY-AUTO-004 | No generated core edits | GSD core files remain untouched by this setup | pass |
