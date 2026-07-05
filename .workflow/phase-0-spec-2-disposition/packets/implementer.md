# Implementation Packet — phase-0-spec-2-disposition

## Objective

Update `docs/spec-v0.4.md` section 2 with Phase 0 evidence: stall story disposition (CONFIRMED or DROPPED) and sandbox-validation path-filter answer.

## Original User Goal

Update docs/spec-v0.4.md section 2 with Phase 0 evidence: stall story disposition and path-filter answer.

## Evidence Sources (read-only)

- `baseline.json` — `stall_story_evidence` block (pr_482_open, issue_479_open, epic_441_open, failed checks)
- `.workflow/phase-0-evidence-audit/packets/01-gh-baseline.md` — PR #482 / #479 / #441 stall story findings
- `.workflow/phase-0-evidence-audit/packets/02-path-filters.md` — path-filter answer (YES, push to main with paths filters)

## Allowed Files (write)

- `docs/spec-v0.4.md` (section 2 only — minimal edit)
- `.workflow/phase-0-evidence-audit/verification-ledger.md` (VERIFY-P0-002 row only)

## Do Not Touch

- Spec sections other than §2 (unless a one-line cross-ref is needed in §2)
- `memory-bank/`, `baseline.json`, queue files
- Full Phase 0 exit gate artifacts

## Acceptance Criteria

1. Mark #479/#482 stall story **CONFIRMED** or **DROPPED** in spec §2 with evidence citation to baseline.json and/or packet 01.
2. Record path-filter answer in spec §2 from packet 02 (workflows ARE path-filtered on push to main).
3. Remove path-filter status from the UNVERIFIED open-dependencies bullet in §2.
4. Update VERIFY-P0-002 in verification-ledger.md with packet-level pass result.

## Stall story guidance

`baseline.json` stall_story_evidence shows PR #482 open, #479 and Epic #441 open, KCC Provision and Circuit Breaker failed → **CONFIRMED** stall story.

## Verification Commands

```powershell
Select-String -Path docs\spec-v0.4.md -Pattern 'CONFIRMED','DROPPED','path-filter'
Select-String -Path .workflow\phase-0-evidence-audit\verification-ledger.md -Pattern 'VERIFY-P0-002'
```

## Expected Result Schema

Return changed_files, checks_run, findings_summary, unresolved_risks, approval_gates.
Do NOT mark queue item complete.
