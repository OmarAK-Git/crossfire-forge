# Design note — AC-2 fixture remediation (2026-07-07)

Status: settled. Companion to spec v0.5 §5 (finding taxonomy design decisions) and
§11 AC-2. This note is the durable record of the AC-2 red → green progression;
the raw ledgers of the failing runs were overwritten in place by later runs, so
the evidence trail lives here and in the committed `artifacts/ac-trials/AC-2/`
snapshot of the passing run.

## Summary

AC-2 ("a deliberately complete Epic yields no findings of any type above BR-1")
went 0/5 on the first mixed-roster live run (2026-07-06 21:03Z,
`artifacts/live-ac-summary.json` of that date). Ledger-persisted diagnostic
re-runs showed the failure was **not** manufactured over-review: the
`tests/fixtures/epic_complete.md` fixture violated its own "deliberately
complete" premise. The fixture and the pinned corpus were remediated; the
evaluator, blast-radius rubric, and merge semantics were **not** touched. AC-2
now passes 4/5 on the same mixed roster (2× gemini-2.5-flash, 2× gemini-2.5-pro,
claude-sonnet-5).

## Why the fixture was the defect, not the evaluator

Three defect classes, all confirmed against persisted trial ledgers — every
finding in every failing trial traced to real bytes in the fixture; none were
fabricated:

1. **Self-defeating completeness claim.** The acceptance criterion asserted
   "All RBAC scopes documented and enforced at project and service level" while
   naming zero roles, principals, or bindings. Unspecified RBAC scope is the
   canonical BR-3 example in the reviewer rubric; all five trials flagged it
   (agreement up to 3).
2. **Reviewer-meta text leaked into the Epic body.** The objective said
   "…so Layer 0 emits no assumption seeds" and an acceptance criterion said
   "No open BR-3 assumptions in the final ledger". These address the review
   tool, not a deployment. The review-not-obey contract *mandates* flagging
   embedded reviewer-directed text as `safety_warning`, so strong models
   failing the trial on these lines were complying with the contract.
3. **Undocumented environment convention.** `status:ai-agent-active` is a
   verified fact of the factory environment (spec §2: every Epic and sub-issue
   carries it), but the pinned corpus never said so. Reviewers correctly
   treated an unexplained agent-state marker in untrusted input as a
   manipulation vector.

The earlier single-family flash baseline passed AC-2 5/5 only because
gemini-2.5-flash is too weak to notice any of the three — a false negative from
a weak roster, not evidence of a clean fixture.

## Remediation (fixture and corpus only)

- `tests/fixtures/epic_complete.md`: concrete IAM bindings
  (`roles/run.invoker` and `roles/run.viewer`, both service-level, named
  principals, explicit no-public-access), reviewer-meta lines deleted,
  `status:ai-agent-active` **kept** (it is environmental truth), FR-3 fields
  unchanged so Layer 0 still parses with zero seeds.
- `tests/fixtures/README.md` (the pinned corpus): new "Factory labeling
  convention" section declaring the status label inert queue metadata.
- SHA-256 pins updated in `tests/test_fixtures.py`, `tests/test_input_loader.py`,
  `tests/test_cli_review.py`; Layer 0 content assertions updated.
- New guard: `test_epic_complete_has_no_reviewer_meta_vocabulary` (red-green
  verified against the old fixture) keeps reviewer-meta vocabulary from leaking
  back into the "clean" fixture.

An intermediate iteration bound `roles/run.viewer` at the **project** level;
every strong reviewer flagged it as over-privileged relative to least
privilege. That critique was sound (a genuine authoring defect), the binding
was scoped to service level, and the run went green — the reviewers were
correct at every stage.

## Progression (mixed roster, pass-4-of-5)

| Run (2026)     | Fixture state                                    | Result   | Finding counts |
|----------------|--------------------------------------------------|----------|----------------|
| 07-06 21:03Z   | self-defeating (meta lines + undefined RBAC)     | 0/5 FAIL | 3–7 per trial  |
| 07-07 (diag 1) | meta lines/RBAC fixed; viewer bound project-level | 0/5 FAIL | 1–3 per trial  |
| 07-07 15:15Z   | least-privilege-correct                          | **4/5 PASS** | 0,2,0,0,0  |

Four of five passing trials returned a completely empty ledger. The single
failing trial contained two agreement-0 singletons: "the named principals may
not be the complete set" (BR-3) and "the quota budget may not be
capacity-planned" (BR-2). Both are unfalsifiable-thoroughness objections that
can be raised against any Epic. They were deliberately **not** chased:
annotating the fixture until every stochastic objection goes quiet is the
sycophancy dynamic AC-2 exists to resist, and the 4-of-5 threshold is the
designed absorber for exactly this noise floor.

## Production implication beyond the test

Until the corpus documented the labeling convention, reviewers flagged
`status:ai-agent-active` on *real* Epics too: the 2026-07-06 `ledger-441.md`
carries two agreement-0 BR-3 safety warnings whose neutralized evidence length
(22) matches the status label exactly. With the convention in the corpus, the
regenerated Epic #441 ledger is expected to shed those spurious warnings —
the corpus fix improves the production artifact, not just the fixture.

## What was deliberately not done

- No change to `evaluate_ac2`, the blast-radius rubric, or max-blast-radius
  merge: spec §5's settled decisions (no `risk` type, no `severity`) lean on
  AC-2 strictness as the anti-sycophancy control, and §11 already provides the
  noise tolerance (4-of-5).
- No fixture annotation to silence the residual agreement-0 singletons (see
  above).
