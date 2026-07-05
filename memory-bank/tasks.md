# Tasks

Mirrors `docs/implementation-plan-v0.4.md`. Each phase has a dedicated `.workflow/<slug>/` run directory.

## Phase 0 — Evidence, baseline & separability audit

Workflow: `.workflow/phase-0-evidence-audit/`

- [x] Run `gh` queries: PR 482 checks/commits; closed issues ≤ 500; all PRs with commit counts
- [x] Compute fix-commits-per-PR and time-to-merge → `baseline.json`
- [ ] Inspect `sandbox-validation-*.yml` for `paths:` filters
- [ ] Separability audit: Docket secret gate + conservation, Crucible merge/anti-sycophancy, Tumbler isolation/pre-filter, Docket agents vs ADK
- [ ] Resolve every spec §13 row to final PORT/LIFT/BUILD mode
- [ ] Mark spec §2 stall line CONFIRMED or DROPPED

**Exit gate:** `baseline.json` committed; §13 resolved; path-filter answer recorded.

## Phase 1 — Contract and local harness

Workflow: `.workflow/phase-1-contract-harness/`

- [ ] **TASK-001** Project skeleton (S) — pytest + `crossfire-forge --help`
- [ ] **TASK-002** Core schemas + taxonomy (M) — three finding types, NG7 enforced
- [ ] **TASK-003** Hashing and run identity (S)
- [ ] **TASK-004** Fixture set (S) — five Epics + README corpus
- [ ] **TASK-005** Pre-prompt safety scanner (M) — AC-5
- [ ] **TASK-006** Input loader (S)
- [ ] **TASK-007** Prompt contract (M) — injection adversarial tests
- [ ] **TASK-008** Reviewer interface + fake reviewer (S)
- [ ] **TASK-009** Gatekeeper checkpoint (Tasks 1–8 vs spec §§5–8)

**Exit gate:** pytest green; AC-5 demonstrated; gatekeeper PASS.

## Phase 2 — Review engine and ledger

Workflow: `.workflow/phase-2-review-engine/`

- [ ] **TASK-010** Provider adapters (L) — Vertex PORT, second greenfield
- [ ] **TASK-011** Aggregator (L) — INV-6 conservation, rapidfuzz clustering
- [ ] **TASK-012** Threshold tuning (S)
- [ ] **TASK-013** Renderer + sanitizer (L) — golden tests
- [ ] **TASK-014** CLI review command (M) — INV-7
- [ ] **TASK-015** Layer 0 full parser (M) — FR-3/FR-4
- [ ] **TASK-016** pass-K-of-N harness + demo ledger (M) — AC-1–AC-6, `ledger-441.md`

**Exit gate:** AC-1–6 green; gatekeeper PASS; `ledger-441.md` for DM draft. **Ends solo-scope build.**

## Phase 3 — Advisory GitHub Action — BLOCKED (D-2)

Workflow: `.workflow/phase-3-github-action/`

- [ ] **TASK-017** Comment upsert library (M) — AC-7
- [ ] **TASK-018** Authorization (M)
- [ ] **TASK-019** Workflow (L) — NFR-1, NFR-5, INV-7
- [ ] **TASK-020** Weekly self-test (M) — AC-8

**Exit gate:** AC-7, AC-8 green; gatekeeper PASS.

## Phase 4 — Gate-mode design + paired validation — BLOCKED (D-1, D-3)

Workflow: `.workflow/phase-4-gate-mode-validation/`

- [ ] **TASK-021** Gate-mode design note (S) — INV-4 test
- [ ] **TASK-022** Paired validation study (collaboration-gated)
