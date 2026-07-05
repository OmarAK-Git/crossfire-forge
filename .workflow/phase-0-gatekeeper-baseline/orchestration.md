# Orchestration — phase-0-gatekeeper-baseline

1. Code reviewer (`gsd-code-reviewer`) performs independent gatekeeper review — must NOT be the packet 01 author.
2. Write `.workflow/phase-0-evidence-audit/gatekeeper-review.md` with PASS or FAIL.
3. Update VERIFY-P0-005 in verification-ledger.md.
4. Fresh-context verifier checks task acceptance only.

## Do NOT

- Commit baseline.json
- Run full Phase 0 exit gate
