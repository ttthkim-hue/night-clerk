from pathlib import Path

import pytest

from night_clerk.labeler import label_claim
from night_clerk.pipeline import run_packet_file
from night_clerk.storage import LocalStorage

FIXTURE = Path(__file__).resolve().parents[1] / "fixtures" / "inbox" / "overvoltage-inbox.json"


def test_local_pipeline_writes_receipt(tmp_path: Path):
    storage = LocalStorage(tmp_path)
    receipt = run_packet_file(FIXTURE, storage=storage)
    assert receipt.status == "completed"
    assert receipt.rejected >= 1
    assert receipt.accepted >= 1
    assert (tmp_path / "receipts" / f"{receipt.job_id}.json").exists()
    reject_reasons = {c.reason for c in receipt.claims if c.action == "reject"}
    assert "smoke_or_mesh_is_not_scientific_validation" in reject_reasons


def test_model_mode_fails_closed_without_gemini_transport(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    monkeypatch.delenv("GOOGLE_API_KEY", raising=False)
    monkeypatch.delenv("GOOGLE_CLOUD_PROJECT", raising=False)
    monkeypatch.delenv("GOOGLE_GENAI_USE_VERTEXAI", raising=False)

    with pytest.raises(RuntimeError, match="Gemini is not configured"):
        label_claim(
            "Mesh check passed so the CFD result is scientifically validated.",
            "gemini-3.5-flash",
            allow_model=True,
        )
