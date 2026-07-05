# Workflow Runs

Every phase and multi-step task uses a dedicated run directory:

```text
.workflow/<slug>/
├── plan.md              # human source of truth
├── state.json           # canonical machine state
├── orchestration.md     # dispatch decisions
├── verification-ledger.md
├── packets/             # subagent packet specs
├── results/             # structured packet returns
└── final-report.md      # written at phase completion
```

## Active runs

| Slug | Phase | Status |
| --- | --- | --- |
| `phase-0-evidence-audit` | 0 | in_progress |
| `phase-1-contract-harness` | 1 | pending |
| `phase-2-review-engine` | 2 | pending |
| `phase-3-github-action` | 3 | blocked (D-2) |
| `phase-4-gate-mode-validation` | 4 | blocked (D-1, D-3) |

Validate before execution:

```bash
python .claude/skills/ultimate-agentic-workflow/scripts/verify_run.py --run-dir .workflow/<slug>
```

Live projections: `memory-bank/` (see `memory-bank/README.md`).
