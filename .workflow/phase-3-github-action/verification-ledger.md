# Verification Ledger — phase-3-github-action

| ID | Requirement | Check | Command or Evidence | Expected | Actual | Status |
| --- | --- | --- | --- | --- | --- | --- |
| VERIFY-AC-7 | FR-9 | comment upsert | mocked pytest | one updated comment | — | blocked |
| VERIFY-AC-8 | FR-12 | self-test | workflow dry-run | fail visible, no issue comment | — | blocked |
| VERIFY-P3-001 | INV-4 | label scan | `rg 'labels: write'` | absent | — | blocked |
