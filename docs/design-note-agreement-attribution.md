# Design note — pipeline-owned reviewer attribution (2026-07-07)

Status: settled. Companion to spec v0.5 §5 (finding taxonomy field semantics).
Cross-references `docs/design-note-ac2-fixture-remediation.md`.

## The defect

Rendered ledgers presented **model-authored** `agreement_count` and
`reviewer_votes` as if they were pipeline-computed facts. Reviewers were asked to
emit these fields, and whatever number a model wrote was carried through
aggregation and rendered under the "Agreement:" line. Agreement corroboration —
the one signal a maintainer is meant to trust when triaging a ledger — was
therefore untrusted model text wearing a data costume. This is the same class of
problem R-1 addresses for statements and evidence: schema-valid-but-misleading
model output. It had simply never been closed for the attribution fields.

### Committed evidence (as of `ad658a3`)

- **`artifacts/ledger-441.md`, finding #1** (the Epic #441 pitch artifact, the G4
  buy-in deliverable): a BR-3 RBAC-scope assumption rendered `Agreement: 1`. The
  `1` is a single reviewer's self-report, not a count of how many of the five
  reviewer slots raised it.
- **`artifacts/ac-trials/AC-1/trial-1/findings.json`, finding 4**: carries
  `reviewer_votes: ["reviewer_1", "reviewer_2"]`, `agreement_count: 2` — a model
  inventing two voters and a corroboration count inside a single reviewer's
  output. The three sibling RBAC findings in the same trial each report
  `agreement_count: 0`, so the same real-world corroboration is rendered
  incoherently across findings.
- **`artifacts/ac-trials/AC-3/trial-1/findings.json`**: all **five** reviewer
  slots independently flagged the injection (genuine 5-way corroboration), yet
  the five safety warnings rendered self-reported agreement counts of
  `[0, 1, 0, 0, 0]`. The strongest possible agreement signal in the corpus was
  displayed as near-zero.

## The fix

`reviewer_votes` and `agreement_count` become pipeline-owned:

1. **Model-facing schema** (`crossfire_forge/prompts.py`): both fields removed
   from `FINDINGS_SCHEMA_INSTRUCTIONS`. Reviewers no longer output them.
2. **Schema** (`crossfire_forge/schemas.py`): `reviewer_votes` defaults to `[]`
   and `agreement_count` to `0`, so a raw model finding validates without them.
   Any values a model still emits are overwritten at stamping — untrusted input,
   consistent with R-1.
3. **Stamp at collection** (`crossfire_forge/reviewers/base.py`,
   `collect_reviewer_results`): the single point where per-reviewer results are
   gathered for aggregation. Both the live and fake reviewer paths flow through
   it; the dev-only `--debug-raw-envelopes` path applies the same stamp inline
   (`cli.py`) while its envelope still shows the raw model output. Each finding
   is stamped `reviewer_votes = [slot_vote_id(index, reviewer_id)]`,
   `agreement_count = 1`. Slot ids are `slot-<n>:<model-id>` — distinct per
   roster slot even when one model fills two slots (`slot-1:gemini-2.5-flash`,
   `slot-2:gemini-2.5-flash`) and stable across a run.
4. **Aggregation** (`crossfire_forge/aggregate.py`): unchanged. `_combine_votes`
   already deduplicates and counts distinct votes, and the merge/collapse paths
   (`aggregate.py:140-144`, `220-227`) recompute the fields from the real slot
   votes. Those recomputations become honest automatically once the votes are
   real. The fake reviewer (`fake.py`) may keep emitting its own id, but the
   stamp is the single source of truth.

Redefined semantics (spec v0.5 §5): `agreement_count` = the number of distinct
reviewer slots that raised the finding, computed only by aggregation; a singleton
is `1`. Model-authored values for these fields are discarded as untrusted.

## The semantic break

This is a deliberate break versus artifacts recorded **before `ad658a3`**, whose
`agreement_count`/`reviewer_votes` were reviewer self-reports. Those artifacts are
**not** migrated: the old numbers meant "what a model claimed" and the new numbers
mean "how many distinct slots corroborated," and silently rewriting historical
evidence would itself be a truth defect. The `16:50Z` full-run artifacts committed
at `ad658a3` are the last generation under the old semantics; the next full gate
run regenerates `ledger-441.md` under the new ones.

## Deferred: the AC-2 evaluator decision

**No AC-2 evaluator change ships in this round.** The AC-2 evaluator
(`evaluate_ac2`) still fails a trial when any finding exceeds BR-1, unchanged from
`docs/design-note-ac2-fixture-remediation.md` ("What was deliberately not done").

The candidate rule under consideration is: **a trial fails only if ≥2 distinct
reviewer slots each emit a BR-2-or-higher finding** — i.e. corroborated concern,
not a single reviewer's stochastic objection — and this rule is
clustering-independent (it counts distinct slots directly from the now-trustworthy
`reviewer_votes`, so it does not depend on the lexical clusterer merging the
findings first).

That decision is **deferred** because it hinges on an open empirical question that
cannot be answered until attributed diagnostic evidence exists: **are the residual
AC-2 noise trials single-reviewer events?** The prior remediation observed a
single failing trial with two agreement-0 singletons, but under the old semantics
those agreement counts were self-reported and could not establish whether one slot
or several raised them. With pipeline-owned slot attribution now in place, one
AC-2 diagnostic run will produce the distinct-slot data needed to decide whether
the ≥2-distinct-reviewer rule is the correct absorber for the noise floor or
whether it would mask genuine corroborated concerns. Until that data exists, the
existing 4-of-5 threshold remains the designed noise absorber.

## Sequence after this lands

1. One AC-2 diagnostic run to gather attributed (per-slot) noise data.
2. Phase C decision on the AC-2 evaluator rule above.
3. `epic_441` verbatim-body fix.
4. A single final full gate run (regenerates `ledger-441.md` under the new
   attribution semantics).
