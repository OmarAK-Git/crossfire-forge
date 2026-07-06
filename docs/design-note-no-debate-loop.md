# Design note — why there is no inter-reviewer debate loop

Status: settled decision. Rationale recorded 2026-07-06; the decision itself predates spec v0.4 (FR-5 has required independent fan-out since at least that version). Reopening requires new evidence — specifically, live mixed-roster ledger-quality data showing the independent ensemble under-delivers.

## Context

The author's prior systems (Docket, Crucible) hardened a single contested answer with adversarial multi-model debate. Crossfire-Forge deliberately did not carry the debate runtime over. The record of the cut:

- `docs/spec-v0.4.md` FR-5 (and v0.5 unchanged): reviewers "run **independently** — no shared context."
- Spec §13 lifts from Crucible only the **merge + agreement-counting** stage — the aggregation that sits *after* a debate — rebuilt as `crossfire_forge/aggregate.py`. The debate loop was never a §13 row.
- The implementation plan excludes the ADK runtime as heavy cargo for an Actions runner; the Phase 0 separability audit (`.workflow/phase-0-evidence-audit/packets/03-separability.md`) flagged Crucible's debate machinery as entangled with that runtime and downgraded every PORT row to LIFT.

## Rationale

1. **The task is recall, not verdict.** Debate hardens a single contested answer — precision. This product's output is a ranked **union** of silent assumptions; there is no single answer to converge on. Each model family's blind spots mirror the silent inferences a generating agent would make, so diversity-then-dedupe (FR-7 lexical clustering) maximizes coverage, while debate would prune exactly the divergent findings the ledger exists to surface.

2. **`agreement_count` is a load-bearing ranking signal, and it only means anything if votes are independent.** After a debate round, agreement measures who capitulated to whom — the same hollow-agreement failure FR-5 already rejects for N instances of one model. Independence is what makes "4 of 5 flagged this at BR-3" evidence rather than echo.

3. **Injection containment (R-1/R-2).** The Epic is hostile input. A debate loop feeds model output back into model input, reopening precisely the channel this architecture closes. In fan-out, a compromised reviewer is quarantined to one schema-validated vote; in a debate, it gets a persuasion channel to every other reviewer.

4. **Anti-sycophancy (AC-2).** A deliberately complete Epic must yield silence. Debate structurally pressures models to defend and escalate findings rather than drop them; it is the worst topology for producing nothing.

5. **Operational fit.** NFR-3's 5-minute ceiling (debate rounds are sequential wall-clock multipliers), INV-6 conservation accounting (tractable over one generation round, murky over mutating transcripts), and the quiet-tenant posture (fewer moving parts in a fail-open advisory Action).

## Current implementation, stated plainly

As wired in v0.1, the pipeline is a pure independent ensemble: generation → schema-or-discard → lexical clustering → first-of-cluster representative + vote count. The CLI judge (`_FirstFindingJudge`, `crossfire_forge/cli.py`) is a deterministic mock; FR-7's judge-model synthesis is specified but not in the live path. The "adversarial" in the design is aimed at the Epic (review-not-obey contract), not between reviewers.

## Compatible future upgrade — not debate

If live trials show weak ledger quality, the upgrade that preserves the invariants above is a **structured challenge pass**: reviewers still generate independently; a separate skeptic pass challenges each *merged* finding against the corpus, schema-or-discard, with no shared free-text context. That preserves vote independence and injection containment. An open inter-reviewer debate loop does not, and stays rejected absent evidence that outweighs points 1–5.
