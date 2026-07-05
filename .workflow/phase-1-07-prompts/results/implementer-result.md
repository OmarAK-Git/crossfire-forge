# Implementer Result — phase-1-07-prompts

## changed_files

- `crossfire_forge/prompts.py` (created — `build_reviewer_prompt` with delimited Epic/corpus/seeds blocks, fixed review-not-obey system contract, and findings JSON schema instructions per FR-5/R-1)
- `tests/test_prompts.py` (created — adversarial tests using `epic_injection.md`; assert system portion unchanged, injection phrases confined to user delimiters, delimiter markers intact)

## checks_run

- `pytest tests/test_prompts.py -v` — exit 0; 8 passed in 0.04s (Python 3.13.12, pytest 9.0.3)

## findings_summary

Implemented the LIFT prompt contract: `build_reviewer_prompt(epic_content, corpus, seeds)` returns a `ReviewerPrompt` with a constant `system` string and a `user` string wrapping Epic, corpus, and seeds in `<<<UNTRUSTED_*_DATA>>>` delimiters. System instructions include review-not-obey language and schema guidance for all three finding types. Adversarial tests confirm `epic_injection.md` cannot alter the system portion or escape delimited boundaries.

## unresolved_risks

- Runtime model obedience is not validated here (unit tests only; live AC-3 deferred to Phase 2 harness).
- Inner delimiter strings inside Epic content are preserved as data; reviewers must rely on contract + outer wrapper semantics.
- Seeds are serialized as JSON in the delimited block; Layer 0 seed object shape may evolve in TASK-015.

## approval_gates

- None required for this task.
