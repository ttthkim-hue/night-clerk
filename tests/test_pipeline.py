from pathlib import Path

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
