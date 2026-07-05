"""Finding types and blast-radius rubric constants (spec §5, §10)."""

from enum import StrEnum


class FindingType(StrEnum):
    ASSUMPTION = "assumption"
    VIOLATION = "violation"
    SAFETY_WARNING = "safety_warning"


class BlastRadius(StrEnum):
    BR1 = "BR-1"
    BR2 = "BR-2"
    BR3 = "BR-3"
