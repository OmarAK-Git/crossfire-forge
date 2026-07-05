# Autopilot Task Template

Copy the JSON object below into `.workflow/autopilot-queue.json` under `items`.

```json
{
  "id": "TASK-001-short-slug",
  "status": "pending",
  "tier": "T2",
  "depends_on": [],
  "goal": "Copy the user goal verbatim when possible.",
  "scope": "Describe the allowed work boundary.",
  "files_allowed": [
    "src/",
    "tests/"
  ],
  "acceptance_criteria": [
    "The requested behavior is implemented.",
    "Relevant tests or checks pass."
  ],
  "verification": {
    "scope": "task",
    "commands": [
      "pytest"
    ],
    "manual_checks": []
  },
  "implementation_agent": "gsd-executor",
  "verification_agent": "gsd-verifier",
  "run_dir": ".workflow/TASK-001-short-slug",
  "attempts": 0,
  "max_retries": 1,
  "evidence": []
}
```

Rules:

- Keep task IDs unique and slug-safe.
- Use `pending` for work the loop may pick up.
- Use `depends_on` when a task must wait for earlier queue items.
- Use `blocked` for tasks that require approval, secrets, dependency installs, or scope decisions.
- Use `files_allowed` to keep implementation agents from widening the task.
- Keep `verification.scope` as `task` for normal packet work. Use `phase_exit` only for an explicit final gate task.
- Keep verification commands deterministic. If a command is unavailable, record that as a gap instead of calling the task done.
