# Implementer Result — phase-2-10-providers

## changed_files

- `crossfire_forge/reviewers/vertex.py` (new)
- `crossfire_forge/reviewers/second_provider.py` (new)
- `crossfire_forge/reviewers/__init__.py` (exports)
- `tests/test_providers.py` (new)

## checks_run

```powershell
python -m pytest tests/test_providers.py -v
```

```
============================= test session starts =============================
platform win32 -- Python 3.13.12, pytest-9.0.3, pluggy-1.5.0
rootdir: .
configfile: pyproject.toml
collected 5 items

tests/test_providers.py::test_vertex_reviewer_posts_generate_content_shape PASSED [ 20%]
tests/test_providers.py::test_vertex_reviewer_discards_invalid_model_json PASSED [ 40%]
tests/test_providers.py::test_second_provider_posts_chat_completions_shape PASSED [ 60%]
tests/test_providers.py::test_second_provider_discards_invalid_model_json PASSED [ 80%]
tests/test_providers.py::test_vertex_reviewer_discards_schema_invalid_findings PASSED [100%]

============================== 5 passed in 0.27s ==============================
```

## findings_summary

Implemented two httpx-based `Reviewer` adapters. `VertexReviewer` POSTs to the Vertex AI `generateContent` URL (`projects/{project}/locations/{location}/publishers/google/models/{model}:generateContent`) with `systemInstruction` and user `contents`, extracts model text from `candidates[0].content.parts[0].text`, and passes it through `parse_reviewer_output`. `SecondProviderReviewer` uses a distinct OpenAI-compatible `/v1/chat/completions` shape with `messages` (system + user roles) and extracts `choices[0].message.content`. Both accept an injectable `httpx.Client` for test isolation. Contract tests use `httpx.MockTransport` to assert request URL/payload/auth headers and verify valid findings parse, invalid JSON increments `discard_count`, and schema-invalid items are discarded.

## unresolved_risks

- Live Vertex/GCP auth (Application Default Credentials, token refresh) is not wired; adapters expect a caller-supplied bearer token.
- HTTP error paths (4xx/5xx) raise via `response.raise_for_status()` rather than metering as discards; acceptable for harness use but may need policy if wired into pass-K-of-N.
- No retry/backoff or timeout configuration on httpx clients yet.

## approval_gates

None. No pip install required (httpx and pytest already in pyproject.toml).
