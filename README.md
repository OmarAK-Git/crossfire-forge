# Crossfire-Forge

Crossfire-Forge is a contract-first Epic review harness for the Forge Factory: it runs Layer 0 completeness checks and multi-model adversarial review over an Epic plus standards corpus, then emits one sanitized **assumption ledger** — before any factory infrastructure is committed.

```bash
pip install -e ".[dev,vertex]"
crossfire-forge review tests/fixtures/epic_441.md --provider mixed --reviewer-count 5 \
  --corpus README.md --fixtures-dir tests/fixtures -o artifacts/ledger-441.md
python scripts/run_live_ac_trials.py   # AC-1..AC-3 pass-K-of-N (live APIs)
python -m pytest tests/ -q
```

The `.workflow/` directory is the unedited engineering audit trail — phase plans, verification ledgers, and post-live remediation post-mortems — included by design as a credibility asset.

**Gate status:** CONTESTED (structural PASS; mixed-roster semantic trials + independent R6 review pending).

## What it does

1. **Loads** an Epic and ordered corpus files
2. **Scans** inputs for secrets before any model I/O (aborts with a generic message; no leakage)
3. **Parses** Layer 0 optional fields into assumption seeds
4. **Reviews** via independent reviewers across **≥2 model families** (`--provider mixed`: Vertex flash + pro + Anthropic)
5. **Aggregates** findings with lexical clustering, judge merge, and conservation accounting
6. **Renders** a sanitized markdown ledger with machine-readable JSON

Finding types: `assumption`, `violation`, `safety_warning` only. No labels applied. No factory code modified.

## Quick start

**Requirements:** Python 3.12+, Google Cloud SDK (ADC) for Vertex, `ANTHROPIC_API_KEY` for full mixed roster (`--allow-vertex-only` for degraded Vertex-only)

```bash
git clone https://github.com/OmarAK-Git/crossfire-forge.git
cd crossfire-forge
copy .env.example .env   # add ANTHROPIC_API_KEY, then:
pip install -e ".[dev,vertex]"
```

### Live mixed-roster review (demo)

```bash
crossfire-forge review tests/fixtures/epic_441.md \
  --provider mixed \
  --reviewer-count 5 \
  --corpus README.md \
  --fixtures-dir tests/fixtures \
  -o artifacts/ledger-441.md
```

Roster: `gemini-2.5-flash` ×2, `gemini-2.5-pro` ×2, Anthropic Sonnet (resolved at runtime from the Models API).

### Offline / CI (deterministic fakes)

```bash
crossfire-forge review tests/fixtures/epic_441.md \
  --provider fake --reviewer-count 3 \
  --corpus README.md --fixtures-dir tests/fixtures
```

### Live acceptance trials

```bash
python scripts/run_live_ac_trials.py
# or degraded Vertex-only when Anthropic key unavailable:
python scripts/run_live_ac_trials.py --allow-vertex-only
```

Writes `artifacts/live-ac-summary.json` (sanitized aggregates only) and regenerates `artifacts/ledger-441.md`.

### Tests

```bash
python -m pytest tests/ -q
```

## Demo artifacts

| Artifact | Description |
| --- | --- |
| [`artifacts/ledger-441.md`](artifacts/ledger-441.md) | Epic #441 demo ledger (placeholder until mixed-roster live run) |
| [`artifacts/live-ac-summary.json`](artifacts/live-ac-summary.json) | Mixed-roster AC-1..AC-3 pass-K-of-N (placeholder until live run) |
| [`artifacts/single-family-baseline.json`](artifacts/single-family-baseline.json) | Prior single-family interim evidence |

## CLI reference

| Command | Description |
| --- | --- |
| `crossfire-forge review <epic>` | End-to-end review; `--provider fake`, `vertex`, or `mixed` |
| `crossfire-forge hashes <epic>` | Stable SHA-256 hashes for Epic and corpus |

## Spec and workflow

- [`docs/spec-v0.5.md`](docs/spec-v0.5.md) — current specification
- [`.workflow/`](.workflow/) — phase evidence and remediation audit trail

## Project status

| Phase | Status |
| --- | --- |
| 0 — Evidence audit | verified |
| 1 — Contract harness | passed |
| 2 — Review engine | CONTESTED (R6 independent review pending) |
| 3 — GitHub Action | blocked (D-2) |
| 4 — Paired study | blocked (D-1, D-3) |
