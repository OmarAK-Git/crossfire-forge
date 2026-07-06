# Crossfire-Forge

A non-blocking spec-review stage for the Forge Factory. Given an Epic markdown file and a standards corpus, Crossfire-Forge runs a deterministic completeness check (Layer 0) and a multi-model adversarial review (Layer 1), then emits one ranked **assumption ledger** — before the factory commits real infrastructure.

**Status:** Phases 0–2 complete. Live Vertex demo ledger and AC-1..AC-3 pass-K-of-N verified. Phase 3 (advisory GitHub Action) blocked on maintainer D-2 approval.

## What it does

1. **Loads** an Epic and ordered corpus files
2. **Scans** inputs for secrets before any model I/O (aborts with a generic message; no leakage)
3. **Parses** Layer 0 optional fields into assumption seeds
4. **Reviews** via N independent reviewers (Vertex live or deterministic fakes for CI)
5. **Aggregates** findings with lexical clustering, judge merge, and conservation accounting
6. **Renders** a sanitized markdown ledger with machine-readable JSON

Finding types are strictly limited to `assumption`, `violation`, and `safety_warning`. Violations require corpus citations. No labels are applied. No factory code is modified.

## Quick start

**Requirements:** Python 3.12+, [Google Cloud SDK](https://cloud.google.com/sdk) with ADC for live Vertex runs

```bash
git clone https://github.com/OmarAK-Git/gcp-foundry-docket-.git
cd gcp-foundry-docket-
pip install -e ".[dev,vertex]"
```

### Run a live review (demo)

```bash
crossfire-forge review tests/fixtures/epic_441.md \
  --provider vertex \
  --reviewer-count 5 \
  --corpus README.md \
  --fixtures-dir tests/fixtures \
  -o artifacts/ledger-441.md
```

Uses your gcloud default project and `gemini-2.5-flash`.

### Run deterministic fake review (CI / offline)

```bash
crossfire-forge review tests/fixtures/epic_441.md \
  --provider fake \
  --reviewer-count 3 \
  --corpus README.md \
  --fixtures-dir tests/fixtures
```

### Run live acceptance trials (AC-1..AC-3)

```bash
python scripts/run_live_ac_trials.py
```

Writes `artifacts/live-ac-summary.json` and regenerates `artifacts/ledger-441.md`.

### Run tests

```bash
python -m pytest tests/ -q
```

## Demo artifact

[`artifacts/ledger-441.md`](artifacts/ledger-441.md) — Epic #441 through the **live Vertex** pipeline. Real BR-3 RBAC scope assumptions (the maintainer "huh, good catch" moment). Evidence: [`artifacts/live-ac-summary.json`](artifacts/live-ac-summary.json) (AC-1 5/5, AC-2 5/5, AC-3 5/5).

## CLI reference

| Command | Description |
| --- | --- |
| `crossfire-forge review <epic>` | End-to-end review; `--provider vertex` or `fake` |
| `crossfire-forge hashes <epic>` | Print stable SHA-256 hashes for Epic and corpus |

Common options:

- `--provider` — `fake` (default, CI) or `vertex` (live, uses gcloud ADC)
- `--reviewer-count` — number of reviewers (default: 3)
- `--corpus` / `--fixtures-dir` / `--output` / `-o`
- `--debug-raw-envelopes` — local dev only (INV-7)

## Project layout

```text
crossfire_forge/       # Python package
scripts/run_live_ac_trials.py  # Live pass-K-of-N harness
tests/fixtures/        # Five Epic fixtures + corpus
artifacts/             # ledger-441.md, live-ac-summary.json
.workflow/port-validation/  # Upstream behavior diff vs Docket/Tumbler
```

## Upstream honesty

`safety.py` and `prompts.py` are **reimplemented from spec description**, not copied Docket/Tumbler modules. See [`.workflow/port-validation/safety-prompts-diff.md`](.workflow/port-validation/safety-prompts-diff.md).

## Roadmap

| Phase | Status | Outcome |
| --- | --- | --- |
| 0 — Evidence audit | Done | `baseline.json`, §13 resolved |
| 1 — Contract harness | Done | Schemas, safety, fixtures |
| 2 — Review engine | Done | Live Vertex ledger + AC-1..AC-3 |
| 3 — GitHub Action | Blocked (D-2) | Comment upsert, self-test |
| 4 — Gate-mode validation | Blocked (D-1, D-3) | Paired sandbox study |

## Maintainer ask (Frank)

1. **D-2** — buy-in + Action secrets for Phase 3
2. **D-1** — ingestion unit answer (Epic vs sub-issue)

## Documentation

- [Specification v0.4](docs/spec-v0.4.md)
- [Live verification report](.workflow/phase-2-review-engine/LIVE-VERIFICATION.md)
- [Phase 0 evidence verification](.workflow/phase-0-evidence-audit/EVIDENCE-VERIFIED.md)

## License

Not specified.
