from __future__ import annotations

import os
from pathlib import Path

from night_clerk.gate import apply_gate, split_notes
from night_clerk.labeler import label_claim
from night_clerk.schema import InboxPacket, JobReceipt
from night_clerk.storage import Storage, build_storage


def orchestrate(
    packet: InboxPacket,
    storage: Storage | None = None,
    allow_model: bool | None = None,
) -> JobReceipt:
    storage = storage or build_storage()
    model = os.getenv("NIGHT_CLERK_MODEL", "gemini-3.5-flash")
    if allow_model is None:
        allow_model = os.getenv("NIGHT_CLERK_MODE", "local") != "local"

    claims = []
    used_model = "not-run"
    for text in split_notes(packet):
        evidence, used_model = label_claim(text, model, allow_model=allow_model)
        claims.append(apply_gate(text, evidence, packet.protected_literals))

    accepted = sum(1 for c in claims if c.action == "accept")
    held = sum(1 for c in claims if c.action == "hold")
    rejected = sum(1 for c in claims if c.action == "reject")
    receipt = JobReceipt(
        job_id=packet.job_id,
        status="completed",
        model=used_model if allow_model else "not-run",
        mode="gcp" if os.getenv("NIGHT_CLERK_MODE") == "gcp" else "local",
        accepted=accepted,
        held=held,
        rejected=rejected,
        claims=claims,
        storage_uri="",
        evidence_of_run="receipt-written",
    )
    uri = storage.write_receipt(receipt)
    receipt.storage_uri = uri
    return receipt


def run_packet_file(path: str | Path, storage: Storage | None = None) -> JobReceipt:
    storage = storage or build_storage()
    packet = storage.load_packet(path)
    return orchestrate(packet, storage=storage)
