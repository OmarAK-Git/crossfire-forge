# Orchestration — phase-0-02-path-filters

## Dispatch Policy

1. Implementer (`gsd-executor`) inspects upstream `sandbox-validation-*.yml` workflows.
2. Implementer writes `.workflow/phase-0-evidence-audit/packets/02-path-filters.md`.
3. Implementer updates VERIFY-P0-003 in `.workflow/phase-0-evidence-audit/verification-ledger.md`.
4. Fresh-context verifier (`gsd-verifier`) checks task acceptance only.

## Upstream Source

- Repository: `fkc1e100/gcp-template-forge` (same as packet 01-gh-baseline)
- Workflow files: `sandbox-validation-kcc.yml`, `sandbox-validation-tf.yml`
- Read-only access: `gh api` or raw.githubusercontent.com

## Do Not Touch

- `docs/spec-v0.4.md` (full Phase 0 integration is out of scope)
- `memory-bank/` files
- Any file outside `files_allowed`
