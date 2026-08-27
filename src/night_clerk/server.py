from __future__ import annotations

import json
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from night_clerk.pipeline import orchestrate, run_packet_file
from night_clerk.schema import InboxPacket
from night_clerk.storage import LocalStorage, build_storage

app = FastAPI(title="Night Clerk", version="0.1.0")
STATIC = Path(__file__).resolve().parents[2] / "static"


class JobRequest(BaseModel):
    packet_path: str | None = None
    packet: InboxPacket | None = None


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "night-clerk"}


@app.post("/jobs")
def create_job(req: JobRequest) -> dict:
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
