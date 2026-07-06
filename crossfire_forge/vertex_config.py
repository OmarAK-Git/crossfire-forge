"""Resolve Vertex AI settings from gcloud defaults and Application Default Credentials."""

from __future__ import annotations

import os
import platform
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class VertexConfig:
    """Runtime Vertex AI connection settings (SDK owns auth end-to-end)."""

    project: str
    location: str
    model: str


def _gcloud_executable() -> str:
    found = shutil.which("gcloud")
    if found:
        return found
    if platform.system() == "Windows":
        candidate = (
            Path.home()
            / "AppData/Local/Google/Cloud SDK/google-cloud-sdk/bin/gcloud.cmd"
        )
        if candidate.is_file():
            return str(candidate)
    msg = "gcloud CLI not found; install Google Cloud SDK and authenticate"
    raise RuntimeError(msg)


def _run_gcloud(args: list[str]) -> str:
    try:
        result = subprocess.run(
            [_gcloud_executable(), *args],
            check=True,
            capture_output=True,
            text=True,
        )
    except subprocess.CalledProcessError as exc:
        msg = f"gcloud {' '.join(args)} failed: {exc.stderr.strip() or exc.stdout.strip()}"
        raise RuntimeError(msg) from exc
    return result.stdout.strip()


def load_vertex_config(
    *,
    project: str | None = None,
    location: str | None = None,
    model: str | None = None,
) -> VertexConfig:
    """Load Vertex config from env vars with gcloud fallbacks (no bearer token capture)."""
    resolved_project = (
        project
        or os.environ.get("VERTEX_PROJECT")
        or os.environ.get("GOOGLE_CLOUD_PROJECT")
        or _run_gcloud(["config", "get-value", "project"])
    )
    resolved_location = (
        location
        or os.environ.get("VERTEX_LOCATION")
        or os.environ.get("GOOGLE_CLOUD_REGION")
        or _run_gcloud(["config", "get-value", "ai/region"])
        or "us-central1"
    )
    if resolved_location == "(unset)":
        resolved_location = "us-central1"
    resolved_model = model or os.environ.get("VERTEX_MODEL", "gemini-2.5-flash")
    if not resolved_project or resolved_project == "(unset)":
        msg = "Vertex project not configured; set gcloud project or VERTEX_PROJECT"
        raise RuntimeError(msg)
    return VertexConfig(
        project=resolved_project,
        location=resolved_location,
        model=resolved_model,
    )
