# Crossfire-Forge

An autonomous template factory builds whatever the Epic says — including everything the Epic *doesn't* say. Crossfire-Forge is a non-blocking spec-review stage for the Forge Factory (`gcp-template-forge` ): a deterministic completeness check (Layer 0) plus independent adversarial review by ≥2 frontier-model families (Layer 1), run over an Epic and its standards corpus **before any infrastructure is committed**. Output is one sanitized **assumption ledger** per Epic. No factory code is touched, no labels applied, nothing blocked.

**Why the front of the pipeline:** the factory's CI validates lint and deployability, not intent; its healer verifies that what deployed is healthy, not that the right thing deployed. The spec is the one unguarded input. Run against the verbatim body of Epic #441, this tool surfaced the assumptions the factory would otherwise resolve silently — among them that the RBAC manager would default to cluster-scoped `ClusterRoleBinding`s, a trust-boundary decision the Epic never actually makes. See [artifacts/ledger-441.md](artifacts/ledger-441.md).

**Gate status:** PASS (structural + mixed-roster semantic AC-1..AC-3; R6 recorded 2026-07-08).

```bash
pip install -e ".[dev,vertex]"
crossfire-forge review tests/fixtures/epic_441.md --provider mixed --reviewer-count 5 \
  --corpus README.md --fixtures-dir tests/fixtures -o artifacts/ledger-441.md
python scripts/run_live_ac_trials.py   # AC-1..AC-3 pass-K-of-N (live APIs)
python -m pytest tests/ -q
```



## What a run does

1. **Loads** an Epic and an ordered, hash-pinned corpus
2. **Scans** all input for secret-like patterns **before any model call** — on suspicion, aborts with a generic message; no output may quote or locate the secret
3. **Parses** Layer 0 optional fields (`region`, `security_posture`, `quota_budget`, `acceptance_criteria`) into assumption seeds; the zero-field minimal Epic parses cleanly
4. **Fans out** to independent reviewers across ≥2 model families (`--provider mixed`: Gemini Flash ×2, Gemini Pro ×2, Anthropic Sonnet resolved at runtime) — no shared context, no tools, delimited-data review-not-obey contract
5. **Aggregates** deterministically first: lexical clustering, judge merge within clusters only, conservation accounting (every finding is merged, rendered, collapsed, or discarded-with-reason — nothing vanishes silently)
6. **Renders** one sanitized markdown ledger with machine-readable JSON



## Reading a ledger

Three finding types, nothing else:


| Type             | Meaning                                                               | Required fields                                                        |
| ---------------- | --------------------------------------------------------------------- | ---------------------------------------------------------------------- |
| `assumption`     | A decision the spec leaves open that the factory would infer silently | A stated `alternative`                                                 |
| `violation`      | A direct conflict with the standards corpus                           | A `standards_ref` citation — uncited violations fail schema validation |
| `safety_warning` | A prompt-injection attempt or embedded instruction in the input       | Rendered defanged: digest and length only, never the verbatim payload  |


**Blast radius** is the single ranking dimension:

- **BR-3** — an alternative choice changes which resources exist or moves a trust, security, tenancy, or exposure boundary (ClusterRole vs namespaced Role; public vs internal load balancer)
- **BR-2** — same resources, materially different configuration (region, machine class, autoscaling bounds, retention)
- **BR-1** — cosmetic (naming, ordering, docs); collapsed in the rendered ledger

**Agreement** (`agreement_count`) is pipeline-computed — the number of distinct reviewer slots raising a finding within one merged cluster. Model-authored values for attribution fields are discarded as untrusted input. Because clustering is deterministic-lexical, semantic paraphrases may render as separate findings: agreement can **understate** cross-model corroboration, never overstate it. Ranking therefore leans on blast radius first.

## Design decisions

- **Independent reviewers, no debate loop.** Debate correlates votes (hollowing `agreement_count`) and feeds model output back into model input, reopening the injection channel the pipeline closes. Rationale: [docs/design-note-no-debate-loop.md](docs/design-note-no-debate-loop.md).
- **≥2 distinct model families, enforced per run.** Family diversity is the invariant; model names are config. A retired model ID is a one-line roster change plus a rerun of the pinned AC harness.
- **Deterministic aggregation before any judge.** The judge merges only within lexical clusters and is itself schema-or-discard, so corroboration cannot be fabricated by a model. The cost — under-merged paraphrases — errs conservative by construction.
- **Fail-open, never silent.** No component failure may block or delay the factory. Liveness is guaranteed by a weekly no-comment self-test that exercises config, secrets, permissions, and provider reachability and fails the workflow natively on breakage: a dead reviewer announces itself without posting noise to any issue.
- **No silent budget caps.** Spend is bounded structurally — disabled by default, one run per Epic per 10 minutes, identity-based skip on unchanged input, cancel-in-progress, 90 s per model, 5 minute ceiling per run. A quiet budget-skip is itself a silent-failure mode; any future hard cap will be cap-and-annotate-loudly. A full mixed-roster run of Epic #441 costs cents.
- **Advisory-only in v0.1.** Never edits an Epic body, never applies a label, never inserts a human-blocking step. The Action token holds `issues:write` only — the absence of `labels:write` is a structural control, not a policy. Uninstalling is one repo variable plus one workflow file.



## Security posture

Untrusted input is assumed hostile end to end: secrets are stopped before model I/O; all model output — including the judge's — is schema-or-discard, never repaired; injection attempts surface as defanged `safety_warning` findings; rendered output passes markdown escaping, unsafe-link stripping, and a final secret pre-filter; raw model I/O is never persisted to artifacts, caches, or runner logs in Action mode. The full threat model, including named residual risks and their backstops, is [docs/spec-v0.5.md §9](docs/spec-v0.5.md#9-threat-model).

## Quick start

**Requirements:** Python 3.12+, Google Cloud SDK (ADC) for Vertex, `ANTHROPIC_API_KEY` for the full mixed roster (`--allow-vertex-only` runs a degraded Vertex-only roster on existing ADC — no new credentials).

```bash
git clone https://github.com/OmarAK-Git/crossfire-forge.git
cd crossfire-forge
cp .env.example .env   # Windows: copy .env.example .env — then add ANTHROPIC_API_KEY
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



### Offline / CI (deterministic fakes — no keys, no network)

```bash
crossfire-forge review tests/fixtures/epic_441.md \
  --provider fake --reviewer-count 3 \
  --corpus README.md --fixtures-dir tests/fixtures
```



### Live acceptance trials

```bash
python scripts/run_live_ac_trials.py
# degraded Vertex-only when no Anthropic key:
python scripts/run_live_ac_trials.py --allow-vertex-only
```

Writes `artifacts/live-ac-summary.json` (sanitized aggregates only) and regenerates `artifacts/ledger-441.md`.

### Tests

```bash
python -m pytest tests/ -q
```



## Demo artifacts


| Artifact                                                                         | Description                                      |
| -------------------------------------------------------------------------------- | ------------------------------------------------ |
| [artifacts/ledger-441.md](artifacts/ledger-441.md)                             | Epic #441 live mixed-roster ledger (2026-07-08)  |
| [artifacts/live-ac-summary.json](artifacts/live-ac-summary.json)               | Mixed-roster AC-1..AC-3 pass-K-of-N (2026-07-08) |
| [artifacts/single-family-baseline.json](artifacts/single-family-baseline.json) | Prior single-family interim evidence             |




## CLI reference


| Command                         | Description                                                |
| ------------------------------- | ---------------------------------------------------------- |
| `crossfire-forge review <epic>` | End-to-end review; `--provider fake`, `vertex`, or `mixed` |
| `crossfire-forge hashes <epic>` | Stable SHA-256 hashes for Epic and corpus                  |




## Project status


| Phase                | Status                                                |
| -------------------- | ----------------------------------------------------- |
| 0 — Evidence audit   | verified                                              |
| 1 — Contract harness | passed                                                |
| 2 — Review engine    | passed (mixed-roster semantic AC-1..AC-3, 2026-07-08) |
| 3 — GitHub Action    | collaboration-gated (D-2)                             |
| 4 — Paired study     | collaboration-gated (D-1, D-3)                        |


Phases 3 and 4 are deliberately gated on the upstream maintainer's decisions, not on missing engineering: **D-1** — confirm the factory's ingestion unit (Epic vs sub-issue) and decomposition mechanics; **D-2** — buy-in plus secrets configuration for an in-repo Action (fork PRs receive no secrets by platform construction); **D-3** — the paired deploy-run study requires the maintainer's sandbox. Solo scope ends at ledger-quality evidence, by design.

## Spec and audit trail

- [docs/spec-v0.5.md](docs/spec-v0.5.md) — consolidated specification: requirements, invariants, threat model, blast-radius rubric, acceptance criteria
- [.workflow/](.workflow/) — the unedited engineering audit trail: phase plans, verification ledgers, and post-live remediation post-mortems, included so every claim above can be checked rather than taken on faith

Components lifted from prior systems (secret scanning and conservation accounting from Docket, merge and anti-sycophancy protocol from Crucible, injection isolation from Tumbler) are inventoried with provenance in [spec §13](docs/spec-v0.5.md#13-prior-art--provenance).