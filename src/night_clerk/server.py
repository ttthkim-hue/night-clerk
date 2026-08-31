from __future__ import annotations

import json
import os
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from night_clerk.pipeline import orchestrate, run_packet_file
from night_clerk.schema import InboxPacket
from night_clerk.storage import LocalStorage, build_storage

app = FastAPI(title="Night Clerk", version="0.1.0")
STATIC = Path(__file__).resolve().parents[2] / "static"
_TRUTHY = {"1", "true", "yes", "on"}
_PUBLIC_SOURCES = {"synthetic-public-fixture", "synthetic-public-submission-canary"}


class JobRequest(BaseModel):
    packet_path: str | None = None
    packet: InboxPacket | None = None


def _public_demo_only() -> bool:
    return os.getenv("NIGHT_CLERK_PUBLIC_DEMO_ONLY", "").strip().lower() in _TRUTHY


def _validate_public_demo_request(req: JobRequest) -> None:
    if not _public_demo_only():
        return
    if req.packet_path is not None:
        raise HTTPException(status_code=403, detail="packet_path is disabled on the public demo")
    if req.packet is None:
        return
    if req.packet.source not in _PUBLIC_SOURCES:
        raise HTTPException(status_code=403, detail="public demo accepts synthetic fixtures only")
    if len(req.packet.notes) > 8 or sum(len(note) for note in req.packet.notes) > 4000:
        raise HTTPException(status_code=413, detail="public demo packet is too large")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "night-clerk"}


@app.post("/jobs")
def create_job(req: JobRequest) -> dict:
    _validate_public_demo_request(req)
    storage = build_storage()
    if req.packet is not None:
        receipt = orchestrate(req.packet, storage=storage)
    elif req.packet_path:
        receipt = run_packet_file(req.packet_path, storage=storage)
    else:
        raise HTTPException(status_code=400, detail="packet or packet_path required")
    return receipt.model_dump()


@app.get("/jobs/{job_id}")
def get_job(job_id: str) -> dict:
    storage = build_storage()
    if not isinstance(storage, LocalStorage):
        raise HTTPException(status_code=501, detail="Use Firestore console for GCP jobs")
    path = storage.root / "receipts" / f"{job_id}.json"
    if not path.exists():
        raise HTTPException(status_code=404, detail="job not found")
    return json.loads(path.read_text(encoding="utf-8"))


@app.get("/", response_class=HTMLResponse)
def dashboard() -> str:
    index = STATIC / "index.html"
    if index.exists():
        return index.read_text(encoding="utf-8")
    return "<h1>Night Clerk</h1><p>POST /jobs</p>"
