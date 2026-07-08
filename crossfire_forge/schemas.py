"""Pydantic v2 schemas for findings, ledger, and run identity (spec §5, NFR-4)."""

from typing import Annotated, Literal, Union

from pydantic import BaseModel, Field

from crossfire_forge.taxonomy import BlastRadius, FindingType


class FindingBase(BaseModel):
    statement: str = Field(min_length=1)
    evidence: str = Field(min_length=1)
    blast_radius: BlastRadius
    # Pipeline-owned attribution (spec v0.5 §5): reviewers never author these.
    # Raw model findings validate without them; any model-emitted values are
    # untrusted (R-1) and overwritten when per-reviewer results are collected.
    reviewer_votes: list[str] = Field(default_factory=list)
    agreement_count: int = Field(default=0, ge=0)


class AssumptionFinding(FindingBase):
    type: Literal[FindingType.ASSUMPTION] = FindingType.ASSUMPTION
    alternative: str = Field(min_length=1)


class ViolationFinding(FindingBase):
    type: Literal[FindingType.VIOLATION] = FindingType.VIOLATION
    standards_ref: str = Field(min_length=1)


class SafetyWarningFinding(FindingBase):
    type: Literal[FindingType.SAFETY_WARNING] = FindingType.SAFETY_WARNING


Finding = Annotated[
    Union[AssumptionFinding, ViolationFinding, SafetyWarningFinding],
    Field(discriminator="type"),
]


class CorpusHash(BaseModel):
    path: str = Field(min_length=1)
    content_hash: str = Field(min_length=1)


class RunIdentity(BaseModel):
    epic_hash: str = Field(min_length=1)
    corpus_hashes: list[CorpusHash] = Field(min_length=1)
    model_roster: list[str] = Field(min_length=1)
    tool_version: str = Field(min_length=1)


class RosterResolution(BaseModel):
    roster_label: str = Field(min_length=1)
    degraded: bool
    resolved_slots: list[str] = Field(min_length=1)
    distinct_model_families: list[str] = Field(min_length=1)


class Ledger(BaseModel):
    identity: RunIdentity
    findings: list[Finding]
    roster_resolution: RosterResolution | None = None
