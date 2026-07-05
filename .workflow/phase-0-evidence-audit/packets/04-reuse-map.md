# Packet 04-reuse-map — Result

**Status:** done  
**Completed:** 2026-07-05  
**Scope:** Finalize `docs/spec-v0.4.md` §13 reuse modes in `memory-bank/traceability.md`  
**Upstream evidence:** `.workflow/phase-0-evidence-audit/packets/03-separability.md`

## Integration summary

Packet 03 audited Docket, Crucible, and Tumbler import surfaces for all ten §13 rows. Upstream repositories are not inspectable via read-only `gh` from this workspace, so every provisional **PORT** row was downgraded to **LIFT** per spec §13 footer (*"a failed port downgrades to LIFT against the same spec item with no spec change"*). **Process reuse** and **BUILD** rows were unchanged.

| Phase 0 resolution | Count | Rows |
| --- | --- | --- |
| LIFT | 8 | FR-2, INV-6, FR-5, FR-7, AC-2, R-1, FR-8, Vertex adapter |
| Process reuse | 1 | Phase gating discipline |
| BUILD | 1 | §10 rubric, FR-3 fields, NFR-4 identity, FR-12 self-test |

## Traceability update

Added `## Section 13 reuse map (Phase 0 resolved)` to `memory-bank/traceability.md` with all ten spec rows, final Phase 0 modes, and per-row evidence citing packet 03 or BUILD rationale.

## Downgrade rationale (PORT → LIFT)

- **Access blocker:** No `docket`, `crucible`, or `tumbler` repos in maintainer public GitHub; code search returned zero indexed hits for upstream modules.
- **ADK coupling risk:** FR-5 fan-out explicitly flagged — implementation plan excludes ADK runtime unless agents separate cleanly (not evidenced).
- **Highest-confidence LIFT targets:** FR-2 secret scanner, FR-8 pre-filter, R-1 prompt isolation — static bytes / prompt contract only.
- **Maintainer unblock:** Export or grant read access to upstream repos to re-run import-surface audit; any row may upgrade from LIFT back to PORT without spec change.

## Verification

```powershell
Select-String -Path memory-bank\traceability.md -Pattern 'section 13','FR-2 pre-prompt secret scanner','Vertex provider adapter','BUILD'
# Expected: matches in Section 13 reuse map table

Select-String -Path .workflow\phase-0-evidence-audit\verification-ledger.md -Pattern 'VERIFY-P0-004'
# Expected: status pass with packet 04 note
```

## Out of scope (this packet)

- Queue / phase exit gate completion → controller + verifier
- `baseline.json` commit (VERIFY-P0-001) → separate track
