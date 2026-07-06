# Upstream behavior diff — safety.py and prompts.py

Date: 2026-07-05  
Reviewer: Omar (local upstream access); supersedes agent §13 PORT/LIFT audit.

## Summary

Crossfire-Forge `safety.py` and `prompts.py` are **reimplemented-from-description**, not copied modules. Pattern alignment with Docket/Tumbler is partial; several Docket behaviors are intentionally narrowed for v0.1 Epic+corpus scope.

## FR-2 — Pre-prompt secret gate

| Behavior | Docket (`gdg-yorku-submission/preflight/secrets.py`) | Crossfire-Forge (`safety.py`) | Verdict |
| --- | --- | --- | --- |
| Detection engine | Custom regex patterns (AWS, GCP, GitHub PAT, PEM, dotenv, etc.) + `RedactionContext` | `detect-secrets` library scan via temp file | **GAP** — different engine; both block on suspicion |
| Scan scope | Entire corpus including gitignored files; system-wide redaction before any LLM byte | Epic body + ordered corpus paths only | **GAP** — narrower scope by design (Epic review, not repo ingest) |
| On hit | Registers in `RedactionContext`, promotes gate findings, severity by exposure | `SafetyAbort` with generic message; no secret in logs/output | **ALIGNED** on abort-without-leakage (AC-5) |
| Post-hit handling | Redact and continue with fingerprinted text | Hard abort; no redaction continuation | **GAP** — Crossfire aborts rather than redacts-and-continues |
| Evidence plane | Refuses to build prompt from un-scanned files | Pre-prompt scan is the only gate | **ALIGNED** intent, simpler mechanism |

**Pitch language:** Do not claim "ported from Docket pre-flight." Say: *pre-prompt secret scan reimplemented for Epic+corpus inputs; abort-without-leakage aligned with Docket intent; full corpus redaction scope deferred.*

## R-1 — Prompt injection isolation

| Behavior | Tumbler (`backend/reviewer.py`, `evidence_bundle.py`) | Crossfire-Forge (`prompts.py`) | Verdict |
| --- | --- | --- | --- |
| Delimiters | `<evidence path="..." hash="..." redacted="...">` XML blocks | `<<<UNTRUSTED_*_DATA>>>` markers for epic/corpus/seeds | **ALIGNED** — delimited untrusted data, different syntax |
| Guardrail text | `PROMPT_INJECTION_GUARDRAIL`: data not instructions; report as `prompt_injection_attempt` | `REVIEW_NOT_OBEY_CONTRACT`: data not instructions; report as `safety_warning` | **ALIGNED** intent; different finding type (spec taxonomy) |
| Injection finding type | `prompt_injection_attempt` in FIX verdict schema | `safety_warning` in Crossfire finding union | **ALIGNED** per Crossfire spec §5 (three types only) |
| Obedience test | Verdict must not be PASS when injection present | AC-3: no `MERGE_APPROVED` / `crossfire:approved` in rendered ledger | **ALIGNED** — different eval surface, same intent |
| Evidence bundle | Per-file hash, redaction flag, truncation | Corpus as markdown sections inside delimiters | **GAP** — simpler bundle; no per-file hash attrs |

**Pitch language:** Do not claim "ported from Tumbler isolation." Say: *review-not-obey delimited-data contract reimplemented; Tumbler `<evidence>` pattern adapted to Epic/corpus/seeds blocks.*

## §13 table correction

All rows previously marked PORT by spec should be treated as **LIFT (reimplemented-from-description)** in pitch and traceability. No "battle-tested module carried over" claims unless a future diff closes specific gaps above.

## Recommended follow-ups (non-blocking for demo)

1. Optionally add Docket high-signal regex patterns alongside detect-secrets for parity on known secret formats.
2. Document explicitly that Crossfire aborts on secret hit vs Docket redact-and-continue — intentional for v0.1 fail-closed pre-model gate.
