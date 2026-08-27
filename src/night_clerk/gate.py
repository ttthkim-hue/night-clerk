from __future__ import annotations

import re

from night_clerk.schema import ClaimRecord, EvidenceLabel, InboxPacket

_NUMBER = re.compile(r"\d")
_FALSE_VALIDATION = re.compile(
    r"(mesh check|smoke test|compile success|visuali[sz]ation success).{0,80}(validat|verified|proven)",
    re.IGNORECASE | re.DOTALL,
)
_ALLOWED: set[str] = {
    "measured_internal",
    "calculated_or_simulated",
    "literature_reported",
    "interpolated_or_fitted",
    "scenario_or_assumption",
    "unverified",
}


def split_notes(packet: InboxPacket) -> list[str]:
    out: list[str] = []
    for note in packet.notes:
        text = " ".join(note.strip().split())
        if text:
            out.append(text)
    return out


def default_label(text: str) -> EvidenceLabel:
    lowered = text.lower()
    if "scenario" in lowered or "assumption" in lowered:
        return "scenario_or_assumption"
    if "literature" in lowered or "doi" in lowered:
        return "literature_reported"
    if "simulat" in lowered or "calculated" in lowered:
        return "calculated_or_simulated"
    return "unverified"


def apply_gate(
    text: str,
    proposed: EvidenceLabel,
    protected_literals: list[str],
) -> ClaimRecord:
    label: EvidenceLabel = proposed if proposed in _ALLOWED else "unverified"
    contains_number = bool(_NUMBER.search(text))
    lowered = text.lower()

    for literal in protected_literals:
        if literal and literal.lower() in lowered:
            return ClaimRecord(
                text=text,
                evidence="unverified",
                action="hold",
                reason="protected_literal_present",
                contains_number=contains_number,
            )

    if _FALSE_VALIDATION.search(text):
        return ClaimRecord(
            text=text,
            evidence="unverified",
            action="reject",
            reason="smoke_or_mesh_is_not_scientific_validation",
            contains_number=contains_number,
        )

    if contains_number and label == "unverified":
        return ClaimRecord(
            text=text,
            evidence="unverified",
            action="hold",
            reason="numeric_claim_without_evidence_label",
            contains_number=True,
        )

    return ClaimRecord(
        text=text,
        evidence=label,
        action="accept",
        reason="passed_deterministic_gate",
        contains_number=contains_number,
    )
