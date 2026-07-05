# Verification Ledger - Autopilot Loop

| ID | Requirement | Check | Command or Evidence | Expected | Actual | Status |
| --- | --- | --- | --- | --- | --- | --- |
| VERIFY-AUTO-001 | Run structure | `verify_run.py` | `python awesome-ai-workflow/ultimate-agentic-workflow/scripts/verify_run.py --run-dir .workflow/autopilot-loop` | pass | blocked: `python` shim failed before launch; `py -3` reported no installed Python | blocked |
| VERIFY-AUTO-002 | Queue JSON | parse queue | `Get-Content .workflow/autopilot-queue.json \| ConvertFrom-Json` | pass | parsed; schema_version returned 1 | pass |
| VERIFY-AUTO-003 | Command wiring | command references queue and state | `rg "autopilot-queue\|autopilot-loop/state" .cursor/commands/gsd-autopilot-loop.md` | matches | matched queue and state references | pass |
| VERIFY-AUTO-004 | Core untouched | no edits to generated GSD core | `git status --short -- .cursor/gsd-core awesome-ai-workflow/ultimate-agentic-workflow` | empty | empty output | pass |
| VERIFY-AUTO-005 | Structure fallback | required plan headings and state keys | `Select-String` checks on plan/state | pass | required headings and keys present | pass |
