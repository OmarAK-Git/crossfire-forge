# Implementation Packet — phase-2-16-harness

Implement pass-K-of-N harness with pinned K/N from spec section 11.

Generate artifacts/ledger-441.md by running crossfire-forge review on tests/fixtures/epic_441.md through the fully sanitized fake-reviewer pipeline (same as Task 14). Do NOT call live Vertex/API unless user explicitly approved credentials.

Wire layer0 seeds into CLI review if not already done.

Cover AC-1..AC-6 via tests/harness/ or test_harness.py where feasible (AC-5 can reference Phase 1 safety tests).

If live models required and unavailable: document approval gate in implementer result; still produce ledger-441 via fake pipeline for artifact.

Run pytest tests/test_harness.py -v and ensure Test-Path artifacts/ledger-441.md

Do NOT mark queue complete.
