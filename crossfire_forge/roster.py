"""Pinned mixed-model reviewer roster (FR-5, remediation R1)."""

from __future__ import annotations

import os
import sys
from dataclasses import dataclass
from typing import Any, Literal

from crossfire_forge.reviewers.anthropic import resolve_anthropic_sonnet_model

ProviderKind = Literal["vertex", "anthropic"]

DEGRADED_ROSTER_BANNER = (
    "*** DEGRADED ROSTER: Vertex-only (flash + pro). "
    "Anthropic slot omitted — cross-family diversity reduced. ***"
)

_PROVIDER_FAMILY: dict[ProviderKind, str] = {
    "vertex": "gemini",
    "anthropic": "claude",
}


@dataclass(frozen=True)
class RosterSlot:
    """One reviewer slot: provider backend and canonical model ID."""

    provider: ProviderKind
    model_id: str


@dataclass(frozen=True)
class ResolvedRoster:
    """Explicit roster resolution for ledger metadata and AC summary."""

    slots: tuple[RosterSlot, ...]
    roster_label: str
    degraded: bool
    resolved_slots: tuple[str, ...]
    distinct_model_families: tuple[str, ...]

    def to_metadata(self) -> dict[str, Any]:
        return {
            "roster_label": self.roster_label,
            "degraded": self.degraded,
            "resolved_slots": list(self.resolved_slots),
            "distinct_model_families": list(self.distinct_model_families),
        }


def _vertex_mixed_slots() -> tuple[RosterSlot, ...]:
    return (
        RosterSlot("vertex", "gemini-2.5-flash"),
        RosterSlot("vertex", "gemini-2.5-flash"),
        RosterSlot("vertex", "gemini-2.5-pro"),
        RosterSlot("vertex", "gemini-2.5-pro"),
        RosterSlot("vertex", "gemini-2.5-pro"),
    )


def _full_mixed_slots(anthropic_model_id: str) -> tuple[RosterSlot, ...]:
    return (
        RosterSlot("vertex", "gemini-2.5-flash"),
        RosterSlot("vertex", "gemini-2.5-flash"),
        RosterSlot("vertex", "gemini-2.5-pro"),
        RosterSlot("vertex", "gemini-2.5-pro"),
        RosterSlot("anthropic", anthropic_model_id),
    )


def _resolve_from_slots(
    slots: tuple[RosterSlot, ...],
    *,
    roster_label: str,
    degraded: bool,
) -> ResolvedRoster:
    resolved = tuple(slot.model_id for slot in slots)
    seen_families: set[str] = set()
    families: list[str] = []
    for slot in slots:
        family = _PROVIDER_FAMILY[slot.provider]
        if family not in seen_families:
            seen_families.add(family)
            families.append(family)
    return ResolvedRoster(
        slots=slots,
        roster_label=roster_label,
        degraded=degraded,
        resolved_slots=resolved,
        distinct_model_families=tuple(families),
    )


def resolve_live_roster(*, allow_vertex_only: bool = False) -> ResolvedRoster:
    """Resolve mixed roster; fail loudly unless degraded mode is explicitly allowed."""
    if os.environ.get("ANTHROPIC_API_KEY"):
        anthropic_model = resolve_anthropic_sonnet_model()
        return _resolve_from_slots(
            _full_mixed_slots(anthropic_model),
            roster_label="mixed",
            degraded=False,
        )

    if not allow_vertex_only:
        msg = (
            "ANTHROPIC_API_KEY not set — full mixed roster unavailable. "
            "Set ANTHROPIC_API_KEY or pass --allow-vertex-only for degraded "
            "Vertex-only roster (gemini-2.5-flash + gemini-2.5-pro)."
        )
        raise RuntimeError(msg)

    print(DEGRADED_ROSTER_BANNER, file=sys.stderr, flush=True)
    return _resolve_from_slots(
        _vertex_mixed_slots(),
        roster_label="degraded-vertex-only",
        degraded=True,
    )


def roster_model_ids(resolved: ResolvedRoster) -> list[str]:
    return list(resolved.resolved_slots)


def distinct_model_families(resolved: ResolvedRoster) -> list[str]:
    return list(resolved.distinct_model_families)
