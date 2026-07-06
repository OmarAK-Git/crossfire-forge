# Tasks

Mirrors `docs/implementation-plan-v0.4.md`. Each phase has a dedicated `.workflow/<slug>/` run directory.

## Phase 0 — Evidence, baseline & separability audit — DONE

Workflow: `.workflow/phase-0-evidence-audit/` — exit gate **passed** (2026-07-05)

- [x] Run `gh` queries: PR 482 checks/commits; closed issues ≤ 500; all PRs with commit counts
- [x] Compute fix-commits-per-PR and time-to-merge → `baseline.json`
- [x] Inspect `sandbox-validation-*.yml` for `paths:` filters
- [x] Separability audit: Docket secret gate + conservation, Crucible merge/anti-sycophancy, Tumbler isolation/pre-filter
- [x] Resolve every spec §13 row to final PORT/LIFT/BUILD mode (8 LIFT, 1 Process reuse, 1 BUILD)
- [x] Mark spec §2 stall line **CONFIRMED**

## Phase 1 — Contract and local harness — DONE

Workflow: `.workflow/phase-1-contract-harness/` — exit gate **passed** (59 pytest)

- [x] **TASK-001** Project skeleton — pytest + `crossfire-forge --help`
- [x] **TASK-002** Core schemas + taxonomy — three finding types, NG7 enforced
- [x] **TASK-003** Hashing and run identity
- [x] **TASK-004** Fixture set — five Epics + README corpus
- [x] **TASK-005** Pre-prompt safety scanner — AC-5
- [x] **TASK-006** Input loader
- [x] **TASK-007** Prompt contract — injection adversarial tests
- [x] **TASK-008** Reviewer interface + fake reviewer
- [x] **TASK-009** Gatekeeper checkpoint

## Phase 2 — Review engine and ledger — DONE

Workflow: `.workflow/phase-2-review-engine/` — exit gate **passed** (117 pytest)

- [x] **TASK-010** Provider adapters — Vertex + second greenfield (mock-tested)
- [x] **TASK-011** Aggregator — INV-6 conservation, rapidfuzz clustering
- [x] **TASK-012** Threshold tuning — pinned in `tests/fixtures/threshold_pairs.json`
- [x] **TASK-013** Renderer + sanitizer — golden tests
- [x] **TASK-014** CLI review command — INV-7 (`--debug-raw-envelopes` local only)
- [x] **TASK-015** Layer 0 full parser — FR-3/FR-4
- [x] **TASK-016** pass-K-of-N harness + demo ledger — `artifacts/ledger-441.md`

**Solo-scope build complete.** Live AC-1..AC-3 verified 2026-07-06 (`artifacts/live-ac-summary.json`).

## Phase 3 — Advisory GitHub Action — BLOCKED (D-2)

Workflow: `.workflow/phase-3-github-action/` (not started)

- [ ] **TASK-017** Comment upsert library — AC-7
- [ ] **TASK-018** Authorization
- [ ] **TASK-019** Workflow — NFR-1, NFR-5, INV-7
- [ ] **TASK-020** Weekly self-test — AC-8

## Phase 4 — Gate-mode design + paired validation — BLOCKED (D-1, D-3)

Workflow: `.workflow/phase-4-gate-mode-validation/` (not started)

- [ ] **TASK-021** Gate-mode design note — INV-4 test
- [ ] **TASK-022** Paired validation study (collaboration-gated)
