"""Structural writer for sanitized live AC summary artifacts (R0/R3)."""

from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

# Relative artifact path only — never absolute.
LEDGER_441_REL_PATH = "artifacts/ledger-441.md"

_FORBIDDEN_KEYS = frozenset(
    {
        "vertex_project",
        "project_id",
        "google_cloud_project",
        "access_token",
        "api_key",
        "prompt",
        "completion",
        "raw_completion",
        "transcript",
    }
)

_ABSOLUTE_PATH_RE = re.compile(
    r"(?:[A-Za-z]:\\|/Users/|/home/|\\\\)",
)
_GCP_PROJECT_ID_RE = re.compile(r"\b\d{12}\b")


@dataclass(frozen=True)
class TrialSummary:
    criterion: str
    k: int
    n: int
    trial_results: tuple[bool, ...]
    passed: bool
    finding_counts: tuple[int, ...] | None = None
    trial_artifact_dirs: tuple[str, ...] | None = None
    provisional: bool = False
    provisional_reason: str | None = None


def _assert_relative_artifact_path(path: str) -> None:
    if Path(path).is_absolute():
        msg = f"artifact path must be relative, got absolute: {path!r}"
        raise ValueError(msg)
    if ".." in Path(path).parts:
        msg = f"artifact path must not contain '..': {path!r}"
        raise ValueError(msg)


def assert_summary_sanitized(payload: dict[str, Any]) -> None:
    """Raise if payload contains forbidden keys or sensitive-shaped values."""
    def walk(obj: object, key: str = "") -> None:
        if isinstance(obj, dict):
            for k, v in obj.items():
                if k in _FORBIDDEN_KEYS:
                    msg = f"forbidden summary key: {k!r}"
                    raise ValueError(msg)
                walk(v, k)
        elif isinstance(obj, list):
            for item in obj:
                walk(item, key)
        elif isinstance(obj, str):
            if key in {"ledger_441_path", "trials_base_dir"} or key.endswith("_dirs"):
                _assert_relative_artifact_path(obj)
            if _ABSOLUTE_PATH_RE.search(obj):
                msg = f"absolute path in summary field {key!r}: {obj!r}"
                raise ValueError(msg)
            if _GCP_PROJECT_ID_RE.search(obj) and key not in {"generated_at"}:
                msg = f"GCP project ID pattern in summary field {key!r}: {obj!r}"
                raise ValueError(msg)

    walk(payload)


def build_ac_summary_payload(
    *,
    roster_label: str,
    roster_resolution: dict[str, Any],
    trials: list[TrialSummary],
    all_passed: bool,
    epic_fixtures: dict[str, str] | None = None,
    include_ledger_441: bool = True,
    trials_base_dir: str | None = None,
) -> dict[str, Any]:
    """Build a sanitized live-ac-summary payload (structural guarantees only)."""
    payload: dict[str, Any] = {
        "generated_at": datetime.now(UTC)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z"),
        "roster_label": roster_label,
        "roster_resolution": roster_resolution,
        "model_roster": list(roster_resolution["resolved_slots"]),
        "distinct_model_families": list(roster_resolution["distinct_model_families"]),
        "trials": [asdict(t) for t in trials],
        "all_passed": all_passed,
    }
    if include_ledger_441:
        payload["ledger_441_path"] = LEDGER_441_REL_PATH
    if trials_base_dir is not None:
        payload["trials_base_dir"] = trials_base_dir
    if epic_fixtures:
        payload["epic_fixtures"] = epic_fixtures
    assert_summary_sanitized(payload)
    return payload


def write_ac_summary(path: Path, payload: dict[str, Any]) -> None:
    """Validate and write live-ac-summary.json."""
    assert_summary_sanitized(payload)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def read_ac_summary(path: Path) -> dict[str, Any]:
    """Read and validate an on-disk summary artifact."""
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert_summary_sanitized(payload)
    return payload
