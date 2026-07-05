# Implementation Packet — phase-2-14-cli-review

Wire `crossfire-forge review` E2E: safety scan -> load inputs -> build prompts -> N fake reviewers -> aggregate (mock judge) -> render ledger.

## Acceptance
1. `crossfire-forge review` runs E2E with fake reviewers on pinned fixtures
2. `--debug-raw-envelopes` defaults off, local-only (INV-7 groundwork)
3. CLI output matches golden ledger format from fake pipeline
4. pytest tests/test_cli_review.py -v passes

Use existing modules: safety, input_loader, prompts, reviewers.fake, aggregate, render, hashing.

Do NOT mark queue complete.
