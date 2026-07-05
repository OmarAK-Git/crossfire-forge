# Packet 03-separability — Result

**Status:** done  
**Completed:** 2026-07-05  
**Scope:** docs/spec-v0.4.md §13 (10 reuse rows)  
**Upstream systems audited:** Docket, Crucible, Tumbler (import surfaces)

## Access posture

| Check | Command | Result |
| --- | --- | --- |
| Maintainer public repos | `gh repo list fkc1e100 --limit 30` | 16 public repos; **no** `docket`, `crucible`, or `tumbler` (case-insensitive name match) |
| Repo name search | `gh search repos "docket" user:fkc1e100 --limit 10` (and crucible, tumbler) | **0 results** |
| Code search — secrets | `gh search code "secret" user:fkc1e100 --limit 20` | **0 indexed hits** (API returned empty) |
| Code search — conservation | `gh search code "conservation" user:fkc1e100 --limit 20` | **0 indexed hits** |
| Code search — crossfire / anti-sycophancy / review-not-obey | same pattern | **0 indexed hits** |
| Public Forge Factory repo | `fkc1e100/gcp-template-forge` | Accessible (packets 01–02); **does not contain** Docket/Crucible/Tumbler modules |

**Blocker:** Docket, Crucible, and Tumbler source repositories are **not inspectable** via read-only `gh` from this workspace. No file:line import-surface evidence is available. Findings below combine (a) command-output access evidence, (b) target-module mapping from `docs/implementation-plan-v0.4.md`, and (c) architectural separability analysis with explicit **UNVERIFIED** flags wherever upstream code was not read.

## Target module map (Crossfire-Forge v0.4)

From `docs/implementation-plan-v0.4.md` repository layout and reuse map:

| Upstream | Planned Crossfire module | Spec tie-in |
| --- | --- | --- |
| Docket pre-flight | `crossfire_forge/safety.py` | FR-2 |
| Docket conservation ledger | `crossfire_forge/aggregate.py` (conservation half) | INV-6 |
| Docket fan-out / agents | orchestration layer (no dedicated module yet) | FR-5 |
| Docket Vertex adapter | `crossfire_forge/reviewers/vertex.py` | Vertex row |
| Crucible merge | `crossfire_forge/aggregate.py` (merge half) | FR-7 |
| Crucible anti-sycophancy | prompts/tests (no single named upstream file in plan) | AC-2 |
| Tumbler isolation | `crossfire_forge/prompts.py` | R-1 |
| Tumbler pre-filter | `crossfire_forge/render.py` | FR-8 |
| Crucible → Tumbler gating | phase exit gates in plan (PASS-only) | Process reuse |
| — | `schemas.py`, `taxonomy.py`, `hashing.py`, `cli.py`, `github/selftest.py`, etc. | BUILD row |

Stack note (implementation plan line 11): **ADK runtime excluded** unless Phase 0 audit shows Docket agents separate cleanly from ADK. ADK coupling is the primary separability risk for FR-5 and any PORT row that reuses Docket orchestration code.

## Per-system separability findings

### Docket

| Surface | Planned port | Separability hypothesis | Evidence grade |
| --- | --- | --- | --- |
| Pre-flight secret gate | `safety.py` | **High** — spec FR-2 and plan call for a `detect-secrets`-class scanner over static Epic/corpus bytes before any model I/O; no ADK or multi-agent runtime required in the target design | **UNVERIFIED** (upstream module not read) |
| Conservation ledger | `aggregate.py` | **High** — INV-6 is accounting metadata (merged / rendered / collapsed / discarded-with-reason); plan treats ledger logic as distinct from reviewer fan-out | **UNVERIFIED** |
| Multi-reviewer fan-out | orchestration | **Low for PORT** — plan explicitly ties fan-out to Docket/Crossfire practice and flags ADK as excluded cargo; agent code likely shares ADK imports unless proven otherwise | **UNVERIFIED**; ADK coupling **assumed** pending maintainer export |
| Vertex provider adapter | `reviewers/vertex.py` | **Medium** — httpx + pydantic adapter pattern in plan is separable from ADK, but actual Docket adapter may import shared GCP/agent helpers | **UNVERIFIED** |

**Import-surface audit:** Not performed — repository inaccessible.

### Crucible

| Surface | Planned port | Separability hypothesis | Evidence grade |
| --- | --- | --- | --- |
| Merge + agreement counting | `aggregate.py` | **Medium–high** — plan specifies rapidfuzz lexical clustering + judge merge with schema-or-discard; algorithmic, not ADK-shaped | **UNVERIFIED** |
| Anti-sycophancy (AC-2) | prompt contract + tests | **Medium** — spec §5 design (no `risk` type, schema-or-discard) is structural anti-sycophancy; Crucible prompts/tests may be entangled with multi-model debate runtime | **UNVERIFIED** |
| Phase gating discipline | process | **N/A (process)** — PASS-only phase gates already encoded in `docs/implementation-plan-v0.4.md` § Delivery strategy / Phase exit gates | **Verified (local plan text)** |

**Import-surface audit:** Not performed — repository inaccessible.

### Tumbler

| Surface | Planned port | Separability hypothesis | Evidence grade |
| --- | --- | --- | --- |
| Injection separation (R-1) | `prompts.py` | **High** — delimited-data + review-not-obey contract is prompt-layer only; plan Phase 1 task 7 validates with adversarial unit tests without live models | **UNVERIFIED** (upstream module not read) |
| Final secret pre-filter (FR-8) | `render.py` | **High** — post-render scan over sanitized markdown; same scanner family as FR-2; no model runtime | **UNVERIFIED** |
| Vertex provider adapter | `reviewers/vertex.py` (shared) | **Medium** — same adapter concern as Docket row | **UNVERIFIED** |

**Import-surface audit:** Not performed — repository inaccessible. Spec labels Tumbler as “Phase 3” provenance; upstream may not exist as a standalone repo name in maintainer’s public GitHub.

## §13 recommendations (audit resolution)

Per spec §13 footer: *“Reuse modes are hypotheses pending the Phase 0 separability audit; a failed port downgrades to LIFT against the same spec item with no spec change.”*

Because upstream import surfaces could not be inspected, **every provisional PORT row is downgraded to LIFT** except rows already non-PORT or verified as process/BUILD.

| # | Spec item | Source | Spec mode | Audit recommendation | Rationale |
| --- | --- | --- | --- | --- | --- |
| 1 | FR-2 pre-prompt secret scanner | Docket | PORT | **LIFT** | Upstream `safety`/pre-flight module **UNVERIFIED**; target `safety.py` + `detect-secrets`-class lib is architecturally standalone |
| 2 | INV-6 conservation accounting | Docket | PORT | **LIFT** | Conservation ledger in `aggregate.py` **UNVERIFIED**; pattern is local accounting, not ADK-dependent in plan |
| 3 | FR-5 independent multi-reviewer fan-out | Docket / Crossfire practice | LIFT (PORT pending) | **LIFT** | Confirmed — ADK runtime excluded in plan; no evidence Docket agents separate from ADK |
| 4 | FR-7 merge + agreement counting | Crucible | PORT | **LIFT** | Crucible merge module **UNVERIFIED**; reimplement rapidfuzz cluster + judge merge per plan |
| 5 | AC-2 no manufactured findings | Crucible | PORT | **LIFT** | Anti-sycophancy prompts/tests **UNVERIFIED**; spec §5 structural controls (no `risk` type) ship as BUILD anyway |
| 6 | R-1 injection separation, schema-or-discard | Tumbler | PORT | **LIFT** | Tumbler isolation module **UNVERIFIED**; `prompts.py` contract is greenfield-liftable |
| 7 | FR-8 final secret pre-filter | Tumbler | PORT | **LIFT** | Tumbler pre-filter **UNVERIFIED**; mirror FR-2 scanner over rendered output in `render.py` |
| 8 | Phase gating discipline | Crucible → Tumbler | Process reuse | **Process reuse** | PASS-only gates documented in implementation plan; no code port required |
| 9 | Vertex provider adapter | Docket / Tumbler | PORT | **LIFT** | Shared `vertex.py` **UNVERIFIED**; httpx Vertex client reimplemented per plan stack |
| 10 | §10 rubric, FR-3 fields, NFR-4 identity, FR-12 self-test | — | BUILD | **BUILD** | New to Crossfire-Forge; no upstream source named in §13 |

## Separability summary

- **Posture:** All §13 PORT hypotheses **fail the import-surface audit** due to upstream inaccessibility, not due to confirmed ADK entanglement in readable code. Downgrade path is **LIFT** for nine rows; **Process reuse** and **BUILD** unchanged.
- **Highest-confidence LIFT targets (architectural):** FR-2 secret scanner, FR-8 pre-filter, R-1 prompt isolation — static bytes / prompt contract only.
- **Highest-risk PORT hypothesis:** FR-5 fan-out (ADK runtime explicitly excluded in plan line 11).
- **Maintainer unblock:** Export or grant read access to Docket/Crucible/Tumbler repos (or named paths within private monorepo) to re-run this audit with file:line import graphs; any row may upgrade from LIFT back to PORT without spec change.

## Verification commands (packet)

```powershell
Test-Path .workflow\phase-0-evidence-audit\packets\03-separability.md
# True

Select-String -Path .workflow\phase-0-evidence-audit\packets\03-separability.md -Pattern 'Docket','Crucible','Tumbler','PORT','LIFT','BUILD'
# Matches: Docket, Crucible, Tumbler, PORT, LIFT, BUILD (Process reuse in table)
```

## Out of scope (this packet)

- `memory-bank/traceability.md` finalization → packet 04-reuse-map
- VERIFY-P0-004 ledger row → packet 04
- Queue / phase exit gate completion → controller + verifier
