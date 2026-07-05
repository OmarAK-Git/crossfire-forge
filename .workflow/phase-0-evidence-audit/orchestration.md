# Orchestration — phase-0-evidence-audit

## Dispatch policy

- **01-gh-baseline:** single implementer; requires maintainer repo access approval
- **02-path-filters** and **03-separability:** parallel researchers; read-only; return structured findings to orchestrator
- **04-reuse-map:** orchestrator integrates after 02+03 complete

## Model tiering

- Research/discovery: cheaper model acceptable with skeptic-verifier on load-bearing claims
- Integration and gatekeeper packet: strongest model

## Stop conditions

- All four packets `done` and verification ledger green → phase exit gate
- gh access blocked → pause 01; proceed 02–03 if sources local
