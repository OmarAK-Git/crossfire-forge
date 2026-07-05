# Crossfire-Forge

A non-blocking spec-review stage for the Forge Factory. Given an Epic markdown file and a standards corpus, Crossfire-Forge runs a deterministic completeness check (Layer 0) and a multi-model adversarial review (Layer 1), then emits one ranked **assumption ledger** — before the factory commits real infrastructure.

**Status:** Phases 0–2 complete (CLI + 117-test harness). Phase 3 (advisory GitHub Action) is blocked on maintainer approval.

## What it does

1. **Loads** an Epic and ordered corpus files
2. **Scans** inputs for secrets before any model I/O (aborts with a generic message; no leakage)
3. **Parses** Layer 0 optional fields into assumption seeds
4. **Reviews** via N independent reviewers (deterministic fakes by default; Vertex adapter wired for live trials)
5. **Aggregates** findings with lexical clustering, judge merge, and conservation accounting (INV-6)
6. **Renders** a sanitized markdown ledger with machine-readable JSON

Finding types are strictly limited to `assumption`, `violation`, and `safety_warning`. Violations require corpus citations. No labels are applied. No factory code is modified.

## Quick start

**Requirements:** Python 3.12+

```bash
git clone https://github.com/OmarAK-Git/gcp-foundry-docket-.git
cd gcp-foundry-docket-
pip install -e ".[dev]"
```

### Run a review

```bash
crossfire-forge review tests/fixtures/epic_441.md \
  --corpus README.md \
  --fixtures-dir tests/fixtures \
  --fake-count 5 \
  -o artifacts/ledger-441.md
```

### Print content hashes

```bash
crossfire-forge hashes tests/fixtures/epic_441.md \
  --corpus README.md \
  --fixtures-dir tests/fixtures
```

### Run tests

```bash
python -m pytest tests/ -q
```

## CLI reference

| Command | Description |
| --- | --- |
| `crossfire-forge review <epic>` | End-to-end review pipeline; writes ledger to stdout or `--output` |
| `crossfire-forge hashes <epic>` | Print stable SHA-256 hashes for Epic and corpus files |

Common options:

- `--corpus` — corpus file paths relative to `--fixtures-dir` (default: `README.md`)
- `--fixtures-dir` — base directory for corpus files (default: `tests/fixtures`)
- `--fake-count` — number of deterministic fake reviewers (default: 3)
- `--output` / `-o` — write ledger markdown to a file
- `--debug-raw-envelopes` — print raw reviewer envelopes to stderr (local dev only; not used in Action mode)

## Project layout

```text
crossfire_forge/       # Python package
  schemas.py           # Pydantic finding/ledger contracts
  safety.py            # Pre-prompt secret scanner
  layer0.py            # Completeness parser → assumption seeds
  prompts.py           # Review-not-obey prompt contract
  reviewers/           # Fake, Vertex, and second-provider adapters
  aggregate.py         # Clustering, merge, conservation ledger
  render.py            # Sanitizer + markdown renderer
  harness.py           # Pass-K-of-N acceptance evaluators (AC-1..AC-6)
  cli.py               # Typer CLI entrypoint

tests/
  fixtures/            # Five Epic fixtures + pinned corpus
  golden/              # Ledger format golden files

artifacts/
  ledger-441.md        # Demo ledger from Epic #441 fixture

docs/
  spec-v0.4.md         # Full specification
  implementation-plan-v0.4.md

baseline.json          # Phase 0 historical factory baseline
memory-bank/           # Agent context projections
.workflow/             # Phase verification ledgers and gatekeeper reviews
```

## Demo artifact

[`artifacts/ledger-441.md`](artifacts/ledger-441.md) is the maintainer-facing demo output: Epic #441 run through the fully sanitized fake-reviewer pipeline. It proves format, identity hashing, and safety controls — not live model semantic quality.

## Current scope and limits

| Delivered | Not yet built |
| --- | --- |
| CLI review engine | GitHub Action (comment upsert, self-test) |
| 117 pytest cases | Live Vertex pass-K-of-N trials (needs maintainer credentials) |
| Fake-reviewer E2E pipeline | Gate-mode validation study |
| Provider adapters (mock-tested) | |

Semantic acceptance criteria AC-1..AC-3 have evaluators and unit tests; live 4-of-5 / 5-of-5 trials are deferred until maintainer provides Vertex credentials (`LIVE_MODEL_APPROVAL_REQUIRED` in `harness.py`).

## Roadmap

| Phase | Status | Outcome |
| --- | --- | --- |
| 0 — Evidence audit | Done | `baseline.json`, §13 reuse map resolved |
| 1 — Contract harness | Done | Schemas, safety, fixtures, fake reviewer |
| 2 — Review engine | Done | Aggregation, renderer, CLI, demo ledger |
| 3 — GitHub Action | Blocked (D-2) | Advisory comment upsert, weekly self-test |
| 4 — Gate-mode validation | Blocked (D-1, D-3) | Design note + paired sandbox study |

## Documentation

- [Specification v0.4](docs/spec-v0.4.md)
- [Implementation plan v0.4](docs/implementation-plan-v0.4.md)
- [Phase 2 gatekeeper review](.workflow/phase-2-review-engine/gatekeeper-review.md)

## License

Not specified.
