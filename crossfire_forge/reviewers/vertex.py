"""Vertex AI generateContent reviewer adapter (FR-5, FR-6)."""

from __future__ import annotations

import httpx

from crossfire_forge.prompts import ReviewerPrompt
from crossfire_forge.reviewers.base import ReviewResult, parse_reviewer_output


def _vertex_generate_url(project: str, location: str, model: str) -> str:
    return (
        f"https://{location}-aiplatform.googleapis.com/v1/"
        f"projects/{project}/locations/{location}/"
        f"publishers/google/models/{model}:generateContent"
    )


def _build_vertex_payload(prompt: ReviewerPrompt) -> dict[str, object]:
    return {
        "systemInstruction": {"parts": [{"text": prompt.system}]},
        "contents": [{"role": "user", "parts": [{"text": prompt.user}]}],
    }


def _extract_vertex_text(response_json: object) -> str:
    if not isinstance(response_json, dict):
        msg = "Vertex response must be a JSON object"
        raise ValueError(msg)
    candidates = response_json.get("candidates")
    if not isinstance(candidates, list) or not candidates:
        msg = "Vertex response missing candidates"
        raise ValueError(msg)
    first = candidates[0]
    if not isinstance(first, dict):
        msg = "Vertex candidate must be an object"
        raise ValueError(msg)
    content = first.get("content")
    if not isinstance(content, dict):
        msg = "Vertex candidate missing content"
        raise ValueError(msg)
    parts = content.get("parts")
    if not isinstance(parts, list) or not parts:
        msg = "Vertex content missing parts"
        raise ValueError(msg)
    part = parts[0]
    if not isinstance(part, dict):
        msg = "Vertex part must be an object"
        raise ValueError(msg)
    text = part.get("text")
    if not isinstance(text, str):
        msg = "Vertex part missing text"
        raise ValueError(msg)
    return text


class VertexReviewer:
    """Reviewer that calls Vertex AI generateContent via httpx."""

    def __init__(
        self,
        project: str,
        location: str,
        model: str = "gemini-1.5-flash",
        *,
        reviewer_id: str = "vertex",
        access_token: str = "",
        client: httpx.Client | None = None,
    ) -> None:
        self.project = project
        self.location = location
        self.model = model
        self.reviewer_id = reviewer_id
        self.access_token = access_token
        self._client = client
        self._owns_client = client is None

    def _get_client(self) -> httpx.Client:
        if self._client is None:
            self._client = httpx.Client()
        return self._client

    def review(self, prompt: ReviewerPrompt) -> ReviewResult:
        url = _vertex_generate_url(self.project, self.location, self.model)
        headers = {"Authorization": f"Bearer {self.access_token}"}
        payload = _build_vertex_payload(prompt)
        client = self._get_client()
        response = client.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return parse_reviewer_output(_extract_vertex_text(response.json()))

    def close(self) -> None:
        if self._owns_client and self._client is not None:
            self._client.close()
            self._client = None

    def __enter__(self) -> VertexReviewer:
        return self

    def __exit__(self, *args: object) -> None:
        self.close()
