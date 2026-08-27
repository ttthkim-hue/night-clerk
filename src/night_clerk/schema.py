from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

EvidenceLabel = Literal[
    "measured_internal",
    "calculated_or_simulated",
    "literature_reported",
    "interpolated_or_fitted",
    "scenario_or_assumption",
    "unverified",
]

Action = Literal["accept", "hold", "reject"]


class InboxPacket(BaseModel):
    job_id: str
    source: str = "synthetic-public-fixture"
    notes: list[str] = Field(default_factory=list)
    protected_literals: list[str] = Field(default_factory=list)


class ClaimRecord(BaseModel):
    text: str
    evidence: EvidenceLabel
    action: Action
    reason: str
    contains_number: bool = False


class JobReceipt(BaseModel):
    job_id: str
    status: Literal["completed", "failed"]
    model: str
    mode: str
    accepted: int
    held: int
    rejected: int
    claims: list[ClaimRecord]
    storage_uri: str
    evidence_of_run: str
