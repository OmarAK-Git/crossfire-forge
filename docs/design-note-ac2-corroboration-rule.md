# Design note — AC-2 corroboration rule (Phase C ruling, 2026-07-07)

Status: settled. Amends spec v0.5 §11 (AC-2 operationalization).
Resolves the deferred decision in `docs/design-note-agreement-attribution.md`.
Cross-references `docs/design-note-ac2-fixture-remediation.md`.

## The evidence: first attributed AC-2 diagnostic (2026-07-07 18:56Z)

First AC-2 run with pipeline-owned slot attribution (mixed roster, non-degraded:
flash ×2, pro ×2, sonnet ×1). Result under the old rule: **2/5 FAIL**.

| Trial | Findings | Slot attribution (BR-2+ findings per slot) |
| --- | --- | --- |
| 1 | 8 | slot-1 flash: 4 · slot-3 pro: 2 · slot-4 pro: 2 |
| 2 | 0 | — |
| 3 | 0 | — |
| 4 | 7 | slot-1 flash: 3 · slot-3 pro: 2 · slot-4 pro: 2 |
| 5 | 8 | slot-1 flash: 3 · slot-4 pro: 5 |

All 23 findings: `assumption` type, BR-2/BR-3, agreement 1 (distinct-slot
singletons). Zero safety warnings, zero violations, zero fabricated evidence —
every `evidence` quote is real fixture text; every statement is a true
observation of something the fixture did not state (egress policy, min-instances,
SLI measurement method, quota period/justification, principal provenance, PSC
prerequisites, region rationale). Slot-2 (flash) and slot-5 (sonnet) emitted
nothing in any trial.

## Both pre-registered branches are refuted

1. **The per-trial "≥ 2 distinct slots each emit BR-2+" rule is dead.** Every
   failing trial had two or three distinct slots emitting BR-2+ findings. The
   rule would rescue nothing (still 2/5), and per the deferral's own framing,
   multi-slot noise indicates the concerns may be genuine rather than one
   reviewer's stochastic objection.
2. **"Keep 4-of-5 as the absorber" is also dead.** Pooled post-remediation
   clean-trial rate: 9/15 = 0.6 (runs of 4/5 → 3/5 → 2/5). At p = 0.6,
   P(pass 4-of-5) ≈ 0.34. A rerun policy at one-in-three odds is
   re-run-until-green with paperwork.

## Root cause is the criterion, not the reviewers

Spec §10 grades blast radius **counterfactually**: BR-2/BR-3 exist wherever "an
alternative choice changes" configuration or boundaries. Under that rubric,
every concrete choice (`region: us-central1`) honestly admits a BR-2 assumption
— an alternative region *is* a materially different configuration. A
rubric-faithful reviewer can therefore always violate "no findings above BR-1"
without manufacturing anything. The old operationalization demanded five-slot
silence that the rubric itself licenses breaking; it measured
thoroughness-suppression, not anti-sycophancy. The intent ("no manufactured
findings", §11) has held in every attributed or audited trial to date; the
silence proxy is what kept failing.

## The adopted rule

`evaluate_ac2` passes a trial iff:

- no `violation` and no `safety_warning` at **any** blast radius (a clean Epic
  must produce zero alarm theater; this is *stricter* than the old rule, which
  tolerated BR-1 warnings), and
- no finding above BR-1 with pipeline-computed `agreement_count` ≥ 2 (distinct
  reviewer slots, spec §5).

Uncorroborated BR-2+ assumption singletons are tolerated as advisory output and
render with `Agreement: 1`, which is exactly how a maintainer triages them. The
K/N threshold stays 4-of-5. Corroboration cannot be gamed by reviewers because
attribution is pipeline-owned (stamped at collection; model-authored values
discarded).

**Validation against the known-broken fixture:** the pre-remediation
`epic_complete.md` (RBAC criterion naming zero principals, reviewer-meta leak)
would still fail this rule — its meta-leak drew safety warnings (fail,
clustering-independent) and its RBAC gap was raised in all five trials (fail on
corroboration under any honest merge). The rule separates the broken fixture
from a clean one; it is not vacuous.

## Known limitation: corroboration inherits clusterer recall

Unlike the rejected per-trial rule, the per-finding rule sees agreement ≥ 2 only
when the lexical clusterer merges paraphrases, and the attributed run shows
under-merging: trial-1 carried the uptime-measurement concern from slot-1 *and*
slot-3 as two unmerged singletons; trial-5 carried region and quota concerns
from two slots each. Two mitigations keep the rule honest:

1. **Merge improvements only strengthen the gate.** More clustering → more
   agreement ≥ 2 → more failures. The gate is monotone in clusterer recall, so
   it can never be quietly loosened by aggregation changes; today's under-merge
   is the rule at its most lenient.
2. **The fixture no longer relies on that leniency.** Every gap class the run
   surfaced — including all corroborated-in-spirit ones — is now closed in the
   fixture (below), so a better clusterer has nothing recurring to merge.

## Fixture completion (same commit)

Each addition to `tests/fixtures/epic_complete.md` closes an attributed finding
class from the run; none is decorative:

| Fixture addition | Closes (trial · slot) |
| --- | --- |
| SLI definition: synthetic probes, /healthz, Cloud Monitoring workspace | uptime measurement (t1 · slot-1, t1 · slot-3), monitoring existence (t4 · slot-1) |
| min-instances 1 | cold-start risk (t1 · slot-4) |
| Egress via shared VPC connector, no public route | egress policy (t1 · slot-4) |
| PSC sole-ingress wording + existing service attachment in shared VPC | PSC exclusivity (t1 · slot-1), PSC prerequisites (t4 · slot-1, t4 · slot-4) |
| Quota: per calendar month, compute-only, load-test-sized, hard limit + alerting | quota scope (t1 · slot-1), period (t1 · slot-3), enforcement (t4 · slot-4), justification (t4 · slot-3, t5 · slot-4), sufficiency (t5 · slot-1) |
| Region: data-residency pin, single-region by policy | region rationale (t5 · slot-1, t5 · slot-4) |
| Principals exist in widget-prod IAM inventory | principal provenance (t4 · slot-1, t5 · slot-4 ×2) |
| Service-level = finest Cloud Run granularity; viewer covers runbook | IAM granularity (t1 · slot-1), viewer sufficiency (t4 · slot-3) |

SHA-256 pins updated in `tests/test_input_loader.py` and `tests/test_fixtures.py`;
the reviewer-meta vocabulary guard still passes. Committed trial artifacts keep
the old epic hash — they are historical evidence of the run they record and are
not migrated.

## Deliberately not done

- No change to `aggregate.py` or the merge/clustering logic.
- No per-trial distinct-slot rule (refuted above).
- No change to K/N, the roster, or any other criterion's evaluator.
- No corpus README change (run-identity churn without evidence it is needed).

## Sequence from here

1. `epic_441` verbatim-body fix (send-blocking, independent of AC-2).
2. One final full gate run under the amended rule — pre-registered by this note
   **before** that run, so the outcome, pass or fail, is evidence rather than
   selection.
