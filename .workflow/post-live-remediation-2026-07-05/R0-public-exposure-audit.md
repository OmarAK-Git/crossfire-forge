# R0 — Public exposure audit (2026-07-05)

**Status:** REMEDIATED locally — history rewrite pending owner approval  
**Auditor:** remediation agent (spec-author surface)

## Scope

Full pushed tree through commit `d3d6fc5` on `https://github.com/OmarAK-Git/gcp-foundry-docket-.git`.

## Findings

| Category | Present in history? | Location | Action |
| --- | --- | --- | --- |
| Raw model transcripts / reviewer envelopes | **No** | — | None |
| API tokens / credential-shaped strings | **No** (code patterns only) | `second_provider.py` Bearer header template; tests use `sk-test` | None |
| GCP project ID | **Yes** | `d3d6fc5`: `artifacts/live-ac-summary.json`, `.workflow/phase-2-review-engine/LIVE-VERIFICATION.md` | Scrub + filter-repo |
| Local absolute paths (owner home prefix) | **Yes** | `d3d6fc5`: `live-ac-summary.json`; `9647d91`/`32d3681`: `.cursor/` GSD install paths | Scrub + filter-repo |
| `.env` with real values | **No** | — | None |
| Raw trial log | **Untracked only** | `artifacts/live-ac-run.log` | Added to `.gitignore` |

## Remediation applied (local)

1. `.gitignore` excludes `artifacts/live-ac-run.log`, raw envelopes, trial transcripts, and `.cursor/`.
2. `crossfire_forge/ac_summary.py` — structural writer; never emits project IDs or absolute paths (`assert_summary_sanitized` enforced at write time).
3. **Prior `live-ac-summary.json` was a manual file edit** — replaced with writer-only path via `write_ac_summary()`.

## History rewrite (owner approval required)

**Replacements file lives OUTSIDE the repo** (contains redacted literals; must never be committable):

`<repo-parent>/GCP_forge_docket-filter-repo-replacements.txt` (owner-local; do not commit)

```powershell
git filter-repo --force `
  --replace-text "<absolute-path-to-filter-repo-replacements.txt>" `
  --path .cursor --invert-paths
git push --force origin main
```

`.gitignore` cannot retroactively protect committed `.cursor/` — history excision is required.

## Post-rewrite verification

Use the exact redacted search literals from the out-of-repo replacements file
(project ID and local path prefix). Run `git log -S` for each; expect no hits.
Also verify `.cursor/` is absent from history:

```powershell
git log --all -- .cursor   # expect empty
```

## Gate impact

R0 reads **PASS** only after rewrite + verification above.
