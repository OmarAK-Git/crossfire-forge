"""Contract tests for Vertex and second-provider reviewer adapters (Phase 2 Task 10)."""

import json

import httpx
import pytest

from crossfire_forge.prompts import ReviewerPrompt
from crossfire_forge.reviewers.base import FINDING_ADAPTER
from crossfire_forge.reviewers.second_provider import SecondProviderReviewer
from crossfire_forge.reviewers.vertex import VertexReviewer

VALID_FINDING = {
    "type": "assumption",
    "statement": "Deployment region is unspecified.",
    "evidence": "Epic omits a region field.",
    "alternative": "Specify us-central1 before rollout.",
    "blast_radius": "BR-2",
    "reviewer_votes": ["vertex"],
    "agreement_count": 1,
}

SAMPLE_PROMPT = ReviewerPrompt(
    system="You are a spec reviewer. Respond with JSON findings only.",
    user="Review this epic for missing region.",
)


def _vertex_response(text: str) -> dict[str, object]:
    return {
        "candidates": [
            {
                "content": {
                    "parts": [{"text": text}],
                }
            }
        ]
    }


def _chat_response(content: str) -> dict[str, object]:
    return {
        "choices": [
            {
                "message": {
                    "role": "assistant",
                    "content": content,
                }
            }
        ]
    }


def test_vertex_reviewer_posts_generate_content_shape() -> None:
    captured: dict[str, object] = {}

    def handler(request: httpx.Request) -> httpx.Response:
        captured["url"] = str(request.url)
        captured["payload"] = json.loads(request.content)
        captured["auth"] = request.headers.get("Authorization")
        return httpx.Response(
            200,
            json=_vertex_response(json.dumps([VALID_FINDING])),
        )

    transport = httpx.MockTransport(handler)
    client = httpx.Client(transport=transport)
    reviewer = VertexReviewer(
        "test-project",
        "us-central1",
        model="gemini-1.5-flash",
        access_token="test-token",
        client=client,
    )

    result = reviewer.review(SAMPLE_PROMPT)

    assert "generateContent" in captured["url"]
    assert "test-project" in captured["url"]
    assert "us-central1" in captured["url"]
    assert captured["auth"] == "Bearer test-token"
    payload = captured["payload"]
    assert payload["generationConfig"] == {"responseMimeType": "application/json"}
    assert payload["systemInstruction"] == {
        "parts": [{"text": SAMPLE_PROMPT.system}]
    }
    assert payload["contents"] == [
        {"role": "user", "parts": [{"text": SAMPLE_PROMPT.user}]}
    ]
    assert len(result.findings) == 1
    assert result.discard_count == 0
    FINDING_ADAPTER.validate_python(result.findings[0].model_dump())


def test_vertex_reviewer_discards_invalid_model_json() -> None:
    def handler(_request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=_vertex_response("{not valid json"))

    transport = httpx.MockTransport(handler)
    client = httpx.Client(transport=transport)
    reviewer = VertexReviewer("p", "loc", client=client)

    result = reviewer.review(SAMPLE_PROMPT)

    assert result.findings == []
    assert result.discard_count == 1


def test_second_provider_posts_chat_completions_shape() -> None:
    captured: dict[str, object] = {}

    def handler(request: httpx.Request) -> httpx.Response:
        captured["url"] = str(request.url)
        captured["payload"] = json.loads(request.content)
        captured["auth"] = request.headers.get("Authorization")
        return httpx.Response(
            200,
            json=_chat_response(json.dumps([VALID_FINDING])),
        )

    transport = httpx.MockTransport(handler)
    client = httpx.Client(transport=transport)
    reviewer = SecondProviderReviewer(
        base_url="https://api.example.com",
        model="generic-model",
        api_key="sk-test",
        client=client,
    )

    result = reviewer.review(SAMPLE_PROMPT)

    assert captured["url"] == "https://api.example.com/v1/chat/completions"
    assert captured["auth"] == "Bearer sk-test"
    payload = captured["payload"]
    assert payload["model"] == "generic-model"
    assert payload["messages"] == [
        {"role": "system", "content": SAMPLE_PROMPT.system},
        {"role": "user", "content": SAMPLE_PROMPT.user},
    ]
    assert len(result.findings) == 1
    assert result.discard_count == 0
    FINDING_ADAPTER.validate_python(result.findings[0].model_dump())


def test_second_provider_discards_invalid_model_json() -> None:
    def handler(_request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=_chat_response("not a json array"))

    transport = httpx.MockTransport(handler)
    client = httpx.Client(transport=transport)
    reviewer = SecondProviderReviewer(client=client)

    result = reviewer.review(SAMPLE_PROMPT)

    assert result.findings == []
    assert result.discard_count == 1


def test_vertex_reviewer_discards_schema_invalid_findings() -> None:
    invalid_payload = [{"type": "violation", "statement": "x", "evidence": "y"}]

    def handler(_request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            json=_vertex_response(json.dumps(invalid_payload)),
        )

    transport = httpx.MockTransport(handler)
    client = httpx.Client(transport=transport)
    reviewer = VertexReviewer("p", "loc", client=client)

    result = reviewer.review(SAMPLE_PROMPT)

    assert result.findings == []
    assert result.discard_count == 1
