"""Anthropic Messages API reviewer adapter (FR-5, remediation R1)."""

from __future__ import annotations

import os
import re

import httpx

from crossfire_forge.prompts import ReviewerPrompt
from crossfire_forge.reviewers.base import ReviewResult, parse_reviewer_output

_SONNET_MODEL_RE = re.compile(r"^claude-(?:[\w-]+-)?sonnet-", re.IGNORECASE)


def _extract_message_text(response_json: object) -> str:
    if not isinstance(response_json, dict):
        msg = "Anthropic response must be a JSON object"
        raise ValueError(msg)
    content = response_json.get("content")
    if not isinstance(content, list) or not content:
        msg = "Anthropic response missing content"
        raise ValueError(msg)
    texts: list[str] = []
    for block in content:
        if not isinstance(block, dict) or block.get("type") != "text":
            continue
        text = block.get("text")
        if isinstance(text, str):
            texts.append(text)
    if not texts:
        msg = "Anthropic content block missing text"
        raise ValueError(msg)
    return "".join(texts)


def _parse_model_ids(response_json: object) -> list[str]:
    if not isinstance(response_json, dict):
        msg = "Anthropic models response must be a JSON object"
        raise ValueError(msg)
    data = response_json.get("data")
    if not isinstance(data, list):
        msg = "Anthropic models response missing data array"
        raise ValueError(msg)
    ids: list[str] = []
    for entry in data:
        if isinstance(entry, dict):
            model_id = entry.get("id")
            if isinstance(model_id, str) and model_id:
                ids.append(model_id)
    return ids


def resolve_anthropic_sonnet_model(
    *,
    api_key: str | None = None,
    client: httpx.Client | None = None,
) -> str:
    """Resolve current Claude Sonnet model ID via Anthropic models API."""
    key = api_key if api_key is not None else os.environ.get("ANTHROPIC_API_KEY", "")
    if not key:
        msg = "ANTHROPIC_API_KEY required to resolve Anthropic Sonnet model"
        raise RuntimeError(msg)

    owns_client = client is None
    http = client or httpx.Client(timeout=30.0)
    try:
        response = http.get(
            "https://api.anthropic.com/v1/models",
            headers={
                "x-api-key": key,
                "anthropic-version": "2023-06-01",
            },
        )
        response.raise_for_status()
        model_ids = _parse_model_ids(response.json())
    finally:
        if owns_client:
            http.close()

    sonnet_models = sorted(
        model_id for model_id in model_ids if _SONNET_MODEL_RE.match(model_id)
    )
    if not sonnet_models:
        msg = (
            "Anthropic models API returned no claude-sonnet model; "
            f"available ids: {model_ids!r}"
        )
        raise RuntimeError(msg)
    return sonnet_models[-1]


class AnthropicReviewer:
    """Reviewer backed by the Anthropic Messages API."""

    def __init__(
        self,
        model: str | None = None,
        *,
        reviewer_id: str | None = None,
        api_key: str | None = None,
        client: httpx.Client | None = None,
    ) -> None:
        resolved = model or resolve_anthropic_sonnet_model(api_key=api_key, client=client)
        self.model = resolved
        self.reviewer_id = reviewer_id or resolved
        self.api_key = api_key if api_key is not None else os.environ.get("ANTHROPIC_API_KEY", "")
        self._client = client
        self._owns_client = client is None

    def _get_client(self) -> httpx.Client:
        if self._client is None:
            self._client = httpx.Client(timeout=120.0)
        return self._client

    def review(self, prompt: ReviewerPrompt) -> ReviewResult:
        if not self.api_key:
            msg = "ANTHROPIC_API_KEY not set"
            raise RuntimeError(msg)
        url = "https://api.anthropic.com/v1/messages"
        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        }
        payload = {
            "model": self.model,
            "max_tokens": 4096,
            "system": prompt.system,
            "messages": [{"role": "user", "content": prompt.user}],
        }
        client = self._get_client()
        response = client.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return parse_reviewer_output(_extract_message_text(response.json()))

    def close(self) -> None:
        if self._owns_client and self._client is not None:
            self._client.close()
            self._client = None

    def __enter__(self) -> AnthropicReviewer:
        return self

    def __exit__(self, *args: object) -> None:
        self.close()
