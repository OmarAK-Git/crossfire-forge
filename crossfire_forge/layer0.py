"""Layer 0 optional-field parser and assumption seed generation (FR-3, FR-4)."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable

DOMAINS_PATH = Path(__file__).resolve().parent / "regions.json"

FR3_FIELDS = ("region", "security_posture", "quota_budget", "acceptance_criteria")

_SCALAR_FIELD_PATTERN = re.compile(
    r"^(region|security_posture|quota_budget):\s*(.+)$"
)
_ACCEPTANCE_CRITERIA_SCALAR = re.compile(r"^acceptance_criteria:\s*(.+)$")
_ACCEPTANCE_CRITERIA_BLOCK = re.compile(r"^acceptance_criteria:\s*\|\s*$")
_BLOCK_LINE = re.compile(r"^[ \t]+\S")

_PLACEHOLDER_PATTERNS = (
    re.compile(r"^todo$", re.IGNORECASE),
    re.compile(r"^tbd$", re.IGNORECASE),
    re.compile(r"^___+$"),
    re.compile(r"^placeholder$", re.IGNORECASE),
    re.compile(r"^<tbd>$", re.IGNORECASE),
    re.compile(r"^<todo>$", re.IGNORECASE),
    re.compile(r"^\.\.\.$"),
    re.compile(r"^n/?a$", re.IGNORECASE),
    re.compile(r"^-$"),
)


@dataclass(frozen=True)
class Layer0Result:
    """Parsed Layer 0 fields plus assumption seeds for Layer 1."""

    region: str | None = None
    security_posture: str | None = None
    quota_budget: str | None = None
    acceptance_criteria: str | None = None
    seeds: list[str] = field(default_factory=list)


def _load_domains() -> dict[str, Any]:
    with DOMAINS_PATH.open(encoding="utf-8") as handle:
        return json.load(handle)


def _parse_field_values(epic_text: str) -> dict[str, str | None]:
    values: dict[str, str | None] = {name: None for name in FR3_FIELDS}
    lines = epic_text.splitlines()
    index = 0
    while index < len(lines):
        line = lines[index]
        scalar_match = _SCALAR_FIELD_PATTERN.match(line)
        if scalar_match:
            values[scalar_match.group(1)] = scalar_match.group(2).strip()
            index += 1
            continue

        if _ACCEPTANCE_CRITERIA_BLOCK.match(line):
            block_lines: list[str] = []
            index += 1
            while index < len(lines) and _BLOCK_LINE.match(lines[index]):
                block_lines.append(re.sub(r"^[ \t]+", "", lines[index]))
                index += 1
            values["acceptance_criteria"] = "\n".join(block_lines).strip()
            continue

        scalar_acceptance = _ACCEPTANCE_CRITERIA_SCALAR.match(line)
        if scalar_acceptance:
            values["acceptance_criteria"] = scalar_acceptance.group(1).strip()
            index += 1
            continue

        index += 1
    return values


def _has_layer0_block(values: dict[str, str | None]) -> bool:
    return any(value is not None for value in values.values())


def _is_placeholder(value: str) -> bool:
    stripped = value.strip()
    if not stripped:
        return True
    return any(pattern.match(stripped) for pattern in _PLACEHOLDER_PATTERNS)


def _is_valid_region(value: str, domains: dict[str, Any]) -> bool:
    return value in domains.get("regions", [])


def _is_valid_security_posture(value: str, domains: dict[str, Any]) -> bool:
    return value in domains.get("security_posture", [])


def _is_valid_quota_budget(value: str, domains: dict[str, Any]) -> bool:
    patterns = domains.get("quota_budget_patterns", [])
    return any(re.fullmatch(pattern, value) for pattern in patterns)


def _validators(domains: dict[str, Any]) -> dict[str, Callable[[str], bool]]:
    return {
        "region": lambda value: _is_valid_region(value, domains),
        "security_posture": lambda value: _is_valid_security_posture(value, domains),
        "quota_budget": lambda value: _is_valid_quota_budget(value, domains),
        "acceptance_criteria": lambda _value: True,
    }


def parse_layer0(epic_text: str) -> Layer0Result:
    """Parse optional FR-3 fields and emit FR-4 assumption seeds without blocking."""
    try:
        domains = _load_domains()
        raw_values = _parse_field_values(epic_text)
        if not _has_layer0_block(raw_values):
            return Layer0Result()

        validators = _validators(domains)
        seeds: list[str] = []
        parsed: dict[str, str | None] = {name: None for name in FR3_FIELDS}

        for field_name in FR3_FIELDS:
            value = raw_values[field_name]
            if value is None:
                seeds.append(f"{field_name} unspecified")
                continue
            if _is_placeholder(value):
                seeds.append(f"{field_name} has placeholder value")
                continue
            if not validators[field_name](value):
                seeds.append(f"{field_name} has invalid value")
                continue
            parsed[field_name] = value

        return Layer0Result(
            region=parsed["region"],
            security_posture=parsed["security_posture"],
            quota_budget=parsed["quota_budget"],
            acceptance_criteria=parsed["acceptance_criteria"],
            seeds=seeds,
        )
    except Exception:
        return Layer0Result()
