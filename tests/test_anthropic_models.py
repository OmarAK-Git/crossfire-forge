"""Anthropic model resolution tests."""

from __future__ import annotations

import httpx
import pytest

from crossfire_forge.reviewers.anthropic import _extract_message_text, resolve_anthropic_sonnet_model


def test_extract_message_text_skips_thinking_blocks() -> None:
    payload = {
        "content": [
            {"type": "thinking", "thinking": "internal", "signature": "sig"},
            {"type": "text", "text": '[{"type": "assumption"}]'},
        ]
    }
    assert _extract_message_text(payload) == '[{"type": "assumption"}]'


def test_resolve_anthropic_sonnet_model_from_api_list() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/v1/models"
        return httpx.Response(
            200,
            json={
                "data": [
                    {"id": "claude-3-5-haiku-20241022"},
                    {"id": "claude-sonnet-4-20250514"},
                    {"id": "claude-sonnet-4-20250515"},
                ]
            },
        )

    transport = httpx.MockTransport(handler)
    client = httpx.Client(transport=transport)
    model = resolve_anthropic_sonnet_model(api_key="sk-test", client=client)
    assert model == "claude-sonnet-4-20250515"


def test_resolve_anthropic_sonnet_model_fails_when_none_listed() -> None:
    def handler(_request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json={"data": [{"id": "claude-3-5-haiku-20241022"}]})

    transport = httpx.MockTransport(handler)
    client = httpx.Client(transport=transport)
    with pytest.raises(RuntimeError, match="no claude-sonnet model"):
        resolve_anthropic_sonnet_model(api_key="sk-test", client=client)
