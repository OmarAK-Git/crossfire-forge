# Orchestration - Autopilot Loop

## Dispatch Policy

The controller is `.cursor/commands/gsd-autopilot-loop.md`.

For each runnable queue item:

1. The controller creates a scoped task run under `item.run_dir`.
2. The controller writes an implementation packet to `packets/implementer.md`.
3. One implementation subagent runs against that packet.
4. The controller records implementation output in `results/implementer-result.md`.
5. A separate fresh-context verifier runs against only the task goal, acceptance criteria, changed files, and task verification commands.
6. The controller records verifier output in `results/verifier-result.md` or the task `VERIFICATION.md`.
7. The controller updates `.workflow/autopilot-queue.json` only after verifier status is known.

## Agent Roles

| Role | Preferred Agent | Writes | Completion Authority |
| --- | --- | --- | --- |
| Controller | main Cursor agent | queue and workflow state | no task completion without task-scoped verifier evidence |
| Implementer | `gsd-executor` | task-scoped files only | none |
| Verifier | `gsd-verifier` | verification artifact only | can pass, block, or request human verification |

## Loop Bounds

- Default behavior: drain every currently runnable `pending` or `retry` task.
- Optional cap: `--max-tasks N`.
- Default `max_retries_per_task`: 1.
- Default `allow_parallel_implementation`: false.
- Stop after any `blocked` or `human_needed` task.
- Stop when the same task-scoped verifier gap repeats for the same task.
- Stop when implementation produces an empty or irrelevant diff.
- Stop before destructive, externally visible, or permissioned setup actions.
- Stop cleanly when remaining tasks are waiting on `depends_on`.

## Approval Gates

The loop must stop and ask before:

- installing dependencies
- editing `.codex` or `.claude`
- cloning GitHub repositories
- writing outside the workspace
- deployments, migrations, publishes, or external service mutations
- destructive git actions or broad resets
- widening files beyond `files_allowed`

## Queue Status Transitions

| From | Event | To |
| --- | --- | --- |
| `pending` | selected by controller | `in_progress` |
| `in_progress` | implementation result recorded | `verifying` |
| `verifying` | verifier passed | `done` |
| `verifying` | verifier found gaps and retry remains | `retry` |
| `retry` | selected by controller | `in_progress` |
| `verifying` | verifier found gaps and retry cap reached | `blocked` |
| `verifying` | verifier needs human check | `human_needed` |
| any runnable | approval gate or malformed result | `blocked` |

Queue items with `depends_on` are skipped until every dependency item is `done`.

## Evidence Contract

A task is not done unless all of these exist:

- task `plan.md` with the original goal
- implementation packet
- implementer result
- verifier result
- queue item `status: done`
- queue item evidence path pointing at verifier output

Phase and milestone gates are explicit queue items. Routine packet tasks must not run full phase exit verification and must not fail because later packets are still pending.

## Packet Contract

Each implementation packet must include:

- objective
- original user goal
- relevant docs and state files
- allowed files
- do-not-touch boundaries
- acceptance criteria
- verification commands
- expected result schema

Each verifier packet must include:

- original user goal
- acceptance criteria
- changed files or diff summary
- verification commands
- implementation result path
- instruction to treat implementer claims as unevidenced until checked
- instruction to ignore phase-level gaps unless the queue item sets `verification.scope` to `phase_exit` or `milestone_exit`
