# Crossfire-Forge — Implementation Plan v0.4 (consolidated)

Companion to `spec-v0.4.md`. Supersedes v0.1 and v0.3. PASS-only gates: no phase begins until its predecessor's exit gate passes. Two-surface protocol throughout — implementation on the agentic IDE surface, independent gatekeeper review on a separate surface at every gate.

**Provenance note (2026-07-06):** Phase 0 separability audit resolved every provisional PORT row to **LIFT** per `spec-v0.5.md` §13. Rows below retain original labels for traceability; treat LIFT as the settled mode unless maintainer export upgrades a row.

## Delivery strategy

CLI-first, fakes-first. The maintainer-facing artifact is the ledger, not the GitHub plumbing: build the engine as a standalone CLI proven against pinned local fixtures, run every boundary through the fake reviewer before any live model call, and add the advisory Action only after the demo is credible and the maintainer can provide secrets and installation approval (D-2).

## Stack

Python 3.12, pydantic v2 (schema enforcement at every boundary), httpx, typer, pytest, a `detect-secrets`-class scanner library, rapidfuzz for lexical clustering. Vertex AI adapter first — **LIFT** from author's own designs (Phase 0 audit; see spec v0.5 §13); second provider adapter is greenfield. Excluded as heavy cargo for an Actions runner: the ADK runtime and sentence-transformers (embedding dedupe is future scope; v0.1 clusters lexically with a pinned, fixture-tuned threshold).

## Repository layout

```text
crossfire_forge/
  __init__.py
  schemas.py          # findings, ledger, run identity — written first
  taxonomy.py         # finding types, BR rubric constants
  hashing.py          # content hashes, run identity
  input_loader.py     # local files + configurable corpus
  safety.py           # pre-prompt secret scanner (LIFT: Docket pre-flight pattern)
  layer0.py           # optional-field parse → assumption seeds
  prompts.py          # review-not-obey contract (LIFT: Tumbler isolation pattern)
  reviewers/
    base.py           # provider interface
    fake.py           # deterministic fake reviewer for tests
    vertex.py         # LIFT: Vertex integration
    second_provider.py
  aggregate.py        # lexical cluster → judge merge; conservation (LIFT: Crucible + Docket ledger patterns)
  render.py           # sanitizer + markdown (LIFT: Tumbler pre-filter pattern)
  cli.py              # review command; --debug-raw-envelopes (local only)
  github/
    auth.py           # allowlist checks
    comments.py       # marker-based upsert + stale check
    artifacts.py      # sanitized-JSON artifact writer
    selftest.py

tests/
  fixtures/           # epic_441.md, epic_complete.md, epic_injection.md,
                      # epic_placeholder.md, epic_secret.md, README.md (corpus pin)
  golden/             # ledger_441.md format golden
  test_*.py           # one per module, plus harness

artifacts/.gitkeep
.github/workflows/
  spec-review.yml
  spec-review-selftest.yml
```

## Reuse map

Spec §13 is the provenance table. PORT = copy-and-adapt source modules; LIFT = reimplement the pattern without the source runtime; BUILD = new. **Settled (Phase 0, 2026-07-05):** every provisional PORT row is LIFT. Maintainer export of upstream repos may upgrade individual rows from LIFT back to PORT without spec change.

## Phase 0 — Evidence, baseline & separability audit (2–3 h, parallel with Phase 1)

**Objectives:** confirm or drop the #479/#482 stall story; extract the historical baseline; establish docs-PR safety; resolve the reuse map.

**Tasks:** run the three `gh` queries (PR 482 checks/commits; closed issues ≤ 500; all PRs with commit counts). Compute fix-commits-per-PR and time-to-merge distributions → `baseline.json`. Inspect `sandbox-validation-*.yml` for `paths:` filters. Separability audit against actual import surfaces, not memory: Docket's pre-flight secret gate and conservation ledger, Crucible's merge/anti-sycophancy modules, Tumbler's isolation and pre-filter modules, Docket's reviewer agents vs the ADK runtime.

**Exit gate:** `baseline.json` committed; spec §2 stall line marked CONFIRMED or DROPPED; path-filter answer recorded; every §13 row resolved to a final mode.

## Phase 1 — Contract and local harness (Tasks 1–9)

**Outcome:** schemas, safety, hashing, fixtures, Layer 0 stub, and prompt contract testable without any live model.

1. **Project skeleton (S).** Python 3.12, pytest, pydantic, typer, httpx wired. Done when `pytest` and `crossfire-forge --help` run.
2. **Core schemas + taxonomy (M) — first, contract-first.** Discriminated-union findings (three types), ledger, run identity. Done when invalid payloads fail validation, including an uncited violation (spec NG7 enforced structurally).
3. **Hashing and run identity (S).** Done when identity is deterministic across runs and inputs.
4. **Fixture set (S).** All five Epics plus pinned corpus README. Done when fixtures load and hash stably.
5. **Pre-prompt safety scanner (M) — LIFT.** Done when `epic_secret.md` aborts the run with a generic annotation and the planted secret appears in no log or output (AC-5).
6. **Input loader (S).** Local files + ordered corpus. Done when the CLI prints file hashes.
7. **Prompt contract (M) — LIFT.** Delimited data, review-not-obey, schema instructions. Done when the injection fixture cannot alter system instructions in adversarial unit tests.
8. **Reviewer interface + fake reviewer (S).** Done when the harness runs N fakes and collects only schema-valid findings, with discards metered (AC-6 groundwork).
9. **Gatekeeper checkpoint.** Independent surface reviews Tasks 1–8 against spec §§5–8.

**Exit gate (PASS-only):** pytest green on everything above; AC-5 demonstrated; gatekeeper PASS.

## Phase 2 — Review engine and ledger (Tasks 10–16)

**Outcome:** the CLI produces the maintainer-facing sanitized ledger from pinned fixtures, then from live models.

10. **Provider adapters (L) — Vertex LIFT, second greenfield.** Done when mocked contract tests pass for both.
11. **Aggregator (L) — LIFT: Crucible merge + Docket conservation patterns.** Lexical clustering (rapidfuzz, pinned threshold) before judge-model merge within clusters; judge output schema-or-discard; every merge/drop decision recorded. Done when unique findings are conserved (INV-6) and agreement counts are reproducible on fixed input.
12. **Threshold tuning (S).** Labeled duplicate/distinct pairs derived from fixtures; pin the clustering threshold with a recorded justification. Done when the pinned value is committed with its pair set.
13. **Renderer + sanitizer (L) — LIFT: Tumbler pre-filter pattern.** Ordering, caps, collapsed JSON, corpus statement, machine-readers marker, golden tests. Done when golden output is stable.
14. **CLI review command (M).** End-to-end; `--debug-raw-envelopes` defaults off and is absent from the Action entrypoint by construction (INV-7). Done when the CLI generates the golden ledger from fakes.
15. **Layer 0 full parser (M).** Domain lists (`regions.json`), placeholder rules, seeds wiring. Done when minimal (#441, zero fields), placeholder, and complete fixtures behave per spec FR-3/FR-4.
16. **pass-K-of-N harness + demo ledger (M).** Pinned K/N per spec §11; run live models against `epic_441.md` verbatim → `artifacts/ledger-441.md`. Done when AC-1 through AC-6 are covered by tests or harness scripts and the 441 ledger exists via the fully sanitized pipeline.

**Exit gate (PASS-only):** all ACs 1–6 green; gatekeeper PASS; `ledger-441.md` attached to the DM draft. **This gate ends the solo-scope build; everything after is blocked on the maintainer.**

**Effort, Phases 1–2 combined:** 11–15 h greenfield (LIFT mode per Phase 0 audit).

## Phase 3 — Advisory GitHub Action (Tasks 17–20) — BLOCKED on D-2

**Outcome:** the Action updates one comment, persists sanitized artifacts, cancels stale runs, banners stale reviews, and self-tests without issue noise.

17. **Comment upsert library (M).** Hidden-marker lookup, create/update, post-time `updated_at` stale check. Done when two mocked runs produce one updated comment (AC-7) and an edited-during-run case banners.
18. **Authorization (M).** Allowlist on `issue.user.login` and `sender.login`, `[EPIC]` title filter, `CROSSFIRE_ENABLED` guard. Done when unallowlisted events skip safely.
19. **Workflow (L).** `issues: [opened, edited]` trigger; `concurrency: group: ${{ github.repository }}-${{ github.event.issue.number }}` with `cancel-in-progress: true`; run-identity skip; least-privilege `permissions:` block with no `labels: write` (NFR-5); sanitized artifact upload. Done when a fork dry-run proves idempotency, and a revoked-key run produces an annotation and zero issue comments (NFR-1).
20. **Weekly self-test (M).** Scheduled; validates config, secrets, token permissions, provider reachability via one minimal call; fails natively; posts nothing (AC-8). Done when broken config fails visibly in Actions with no issue noise.

**Exit gate:** AC-7 and AC-8 green; failure-path demonstrations recorded; gatekeeper PASS. Effort: 5–7 h.

## Phase 4 — Gate-mode design note + paired validation — BLOCKED on D-1 and D-3

**Outcome:** gate mode stays unimplemented; the validation study runs only in collaboration.

21. **Gate-mode design note (S).** Document the fail-open vs fail-closed-but-loud decision as the maintainer's call, the hash-bound (never label-carried) authorization design, and the D-1-dependent insertion point. Done when the note exists and no v0.1 code path can apply a label (INV-4 test).
22. **Paired validation study.** 3–5 seeded flawed-Epic pairs in his sandbox; Healer cycles, time-to-green, Housekeeper orphan counts vs `baseline.json`. Pre-registered honesty clause: a null result ships too.

## Build order

Schemas and safety first; fake-reviewer end-to-end before any provider API; sanitized ledger locally; live models; only then GitHub plumbing.

## Exit criteria for v0.1

- `pytest` passes; all eight ACs covered by automated tests or harness scripts.
- `crossfire-forge review` produces a sanitized ledger matching the golden format; `ledger-441.md` generated through the sanitized pipeline.
- Action mode, if enabled: exactly one upserted comment per Epic, sanitized artifacts only, cancel-in-progress verified, self-test live and silent.
- No code path in the repository applies `status:ai-agent-active` or any other label.
- Gatekeeper PASS on every phase gate, on a surface independent of the implementer.
