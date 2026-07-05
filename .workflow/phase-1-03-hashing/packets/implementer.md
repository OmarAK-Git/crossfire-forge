# Implementation Packet — phase-1-03-hashing

## Objective
Implement crossfire_forge/hashing.py: deterministic content hashes and run identity construction.

## Allowed Files
- crossfire_forge/hashing.py
- tests/test_hashing.py
- .workflow/phase-1-contract-harness/verification-ledger.md (optional)

## Do Not Touch
- input_loader.py, fixtures, safety, reviewers

## Acceptance Criteria
1. Content hashing deterministic for identical inputs
2. Run identity stable for same inputs/config
3. Tests cover repeatability

## Verification
pytest tests/test_hashing.py -v

Write .workflow/phase-1-03-hashing/results/implementer-result.md. Do NOT mark queue done.
