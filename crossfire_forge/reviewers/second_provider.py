"""OpenAI-compatible chat-completions reviewer adapter (greenfield)."""

from __future__ import annotations

import httpx

from crossfire_forge.prompts import ReviewerPrompt
from crossfire_forge.reviewers.base import ReviewResult, parse_reviewer_output


def _build_chat_payload(model: str, prompt: ReviewerPrompt) -> dict[str, object]:
    return {
        "model": model,
        "messages": [
            {"role": "system", "content": prompt.system},
            {"role": "user", "content": prompt.user},
        ],
    }


def _extract_chat_content(response_json: object) -> str:
    if not isinstance(response_json, dict):
        msg = "Chat response must be a JSON object"
        raise ValueError(msg)
    choices = response_json.get("choices")
    if not isinstance(choices, list) or not choices:
        msg = "Chat response missing choices"
        raise ValueError(msg)
    first = choices[0]
    if not isinstance(first, dict):
        msg = "Chat choice must be an object"
        raise ValueError(msg)
    message = first.get("message")
    if not isinstance(message, dict):
        msg = "Chat choice missing message"
        raise ValueError(msg)
    content = message.get("content")
    if not isinstance(content, str):
        msg = "Chat message missing content"
        raise ValueError(msg)
    return content


class SecondProviderReviewer:
    """Reviewer that calls an OpenAI-compatible /v1/chat/completions endpoint."""

    def __init__(
        self,
        base_url: str = "https://api.example.com",
        model: str = "generic-model",
        *,
        reviewer_id: str = "second-provider",
        api_key: str = "",
        client: httpx.Client | None = None,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.reviewer_id = reviewer_id
        self.api_key = api_key
        self._client = client
        self._owns_client = client is None

    def _get_client(self) -> httpx.Client:
        if self._client is None:
            self._client = httpx.Client()
        return self._client

    def review(self, prompt: ReviewerPrompt) -> ReviewResult:
        url = f"{self.base_url}/v1/chat/completions"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        payload = _build_chat_payload(self.model, prompt)
        client = self._get_client()
        response = client.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return parse_reviewer_output(_extract_chat_content(response.json()))

    def close(self) -> None:
        if self._owns_client and self._client is not None:
            self._client.close()
            self._client = None

    def __enter__(self) -> SecondProviderReviewer:
        return self

    def __exit__(self, *args: object) -> None:
        self.close()
