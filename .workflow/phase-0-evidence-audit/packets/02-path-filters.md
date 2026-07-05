# Packet 02-path-filters — Result

**Status:** done  
**Completed:** 2026-07-05  
**Repository:** `fkc1e100/gcp-template-forge`

## Queries executed

| Query | Command / API | Result |
| --- | --- | --- |
| List sandbox-validation workflows | `gh api repos/fkc1e100/gcp-template-forge/contents/.github/workflows --jq '.[].name'` | `sandbox-validation-kcc.yml`, `sandbox-validation-tf.yml` |
| KCC workflow triggers | `Invoke-WebRequest` → `raw.githubusercontent.com/.../sandbox-validation-kcc.yml` | `on.push` to `main` with 3 path filters; no `pull_request` |
| TF workflow triggers | `Invoke-WebRequest` → `raw.githubusercontent.com/.../sandbox-validation-tf.yml` | `on.push` to `main` with 2 path filters; no `pull_request` |

## Key findings (path filters)

### sandbox-validation-kcc.yml

**Answer:** Path-filtered — runs on `push` to `main` only when files under listed paths change.

| Line | Evidence |
| --- | --- |
| 3–11 | `on:` → `push:` → `branches: [ main ]` → `paths:` with three globs |

```yaml
on:
  # Post-merge only - validate-kcc.yml handles PR validation.
  # Running both on PRs causes duplicate KCC resource provisioning.
  push:
    branches: [ main ]
    paths:
      - 'templates/**/config-connector/**'
      - 'templates/**/config-connector-workload/**'
      - 'agent-infra/**'
```

- **No `pull_request` trigger** in the `on:` block (lines 3–11).
- Inline comment (lines 4–5) states post-merge-only design; `validate-kcc.yml` handles PR validation.

### sandbox-validation-tf.yml

**Answer:** Path-filtered — runs on `push` to `main` only when files under listed paths change.

| Line | Evidence |
| --- | --- |
| 3–10 | `on:` → `push:` → `branches: [ main ]` → `paths:` with two globs |

```yaml
on:
  # Post-merge only - validate-tf.yml handles PR validation.
  # Running both on PRs causes duplicate cluster provisioning.
  push:
    branches: [ main ]
    paths:
      - 'templates/**/terraform-helm/**'
      - 'agent-infra/**'
```

- **No `pull_request` trigger** in the `on:` block (lines 3–10).
- Inline comment (lines 4–5) states post-merge-only design; `validate-tf.yml` handles PR validation.

## Spec §2 UNVERIFIED question

**Question (spec §2):** whether `sandbox-validation-*.yml` workflows are path-filtered.

**Answer: YES — both sandbox-validation workflows are path-filtered.**

| Workflow | Trigger | Path globs |
| --- | --- | --- |
| `sandbox-validation-kcc.yml` | `push` → `main` | `templates/**/config-connector/**`, `templates/**/config-connector-workload/**`, `agent-infra/**` |
| `sandbox-validation-tf.yml` | `push` → `main` | `templates/**/terraform-helm/**`, `agent-infra/**` |

Both workflows are **post-merge only** (no PR trigger). PR-stage validation is delegated to companion `validate-kcc.yml` / `validate-tf.yml` workflows per inline comments.

**Note:** This packet records evidence only. `docs/spec-v0.4.md` §2 UNVERIFIED line is unchanged per Phase 0 scope — gatekeeper/orchestrator resolves spec update at phase exit.
