# Implementation Packet — phase-0-02-path-filters

## Objective

Inspect `sandbox-validation-*.yml` workflows in upstream repo `fkc1e100/gcp-template-forge` for `paths:` filters and record findings with file:line evidence.

## Original User Goal

Complete Phase 0 packet 02-path-filters: inspect sandbox-validation workflows for paths filters and record the answer with evidence.

## Relevant Docs and State

- `.workflow/phase-0-evidence-audit/plan.md` (packet 02-path-filters)
- `.workflow/phase-0-evidence-audit/packets/01-gh-baseline.md` (upstream repo reference)
- `.workflow/phase-0-evidence-audit/verification-ledger.md` (VERIFY-P0-003)
- `docs/spec-v0.4.md` §2 UNVERIFIED item: whether sandbox-validation workflows are path-filtered

## Allowed Files (write)

- `.workflow/phase-0-evidence-audit/packets/02-path-filters.md` (create)
- `.workflow/phase-0-evidence-audit/state.json` (update packet 02 status only)
- `.workflow/phase-0-evidence-audit/verification-ledger.md` (update VERIFY-P0-003 row only)

## Do Not Touch

- `docs/spec-v0.4.md`
- `memory-bank/`
- `baseline.json`
- Any `.codex` / `.claude` files
- Full Phase 0 exit gate artifacts

## Acceptance Criteria

1. Inspect `sandbox-validation-kcc.yml` and `sandbox-validation-tf.yml` (upstream) for `on:` trigger `paths:` filters.
2. Record answer in `02-path-filters.md` with file:line or command-output evidence.
3. Update VERIFY-P0-003 in verification-ledger.md with packet-level result (pass/partial — not full phase exit).
4. Update phase-0-evidence-audit state.json packet 02 status to `done`.

## Verification Commands

```powershell
Test-Path .workflow\phase-0-evidence-audit\packets\02-path-filters.md
Select-String -Path .workflow\phase-0-evidence-audit\verification-ledger.md -Pattern 'VERIFY-P0-003'
```

## Upstream Read-Only Commands (approved pattern from packet 01)

```powershell
gh api repos/fkc1e100/gcp-template-forge/contents/.github/workflows --jq '.[].name'
# Fetch raw content:
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/fkc1e100/gcp-template-forge/main/.github/workflows/sandbox-validation-kcc.yml" -UseBasicParsing
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/fkc1e100/gcp-template-forge/main/.github/workflows/sandbox-validation-tf.yml" -UseBasicParsing
```

## Expected Result Schema

Return:
- `changed_files`: list of paths written
- `checks_run`: commands executed
- `findings_summary`: one-paragraph path-filter answer
- `unresolved_risks`: any blockers
- `approval_gates`: any gates hit (should be none if gh works)

Do NOT mark the queue item complete. Controller + verifier handle completion.
