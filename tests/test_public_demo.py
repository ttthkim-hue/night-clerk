import pytest
from fastapi import HTTPException

from night_clerk.schema import InboxPacket
from night_clerk.server import JobRequest, _validate_public_demo_request


def test_public_demo_rejects_non_synthetic_source(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("NIGHT_CLERK_PUBLIC_DEMO_ONLY", "true")
    req = JobRequest(
        packet=InboxPacket(
            job_id="unsafe-demo",
            source="private-upload",
            notes=["hello"],
        )
    )
    with pytest.raises(HTTPException) as exc:
        _validate_public_demo_request(req)
    assert exc.value.status_code == 403


def test_public_demo_accepts_bounded_synthetic_packet(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("NIGHT_CLERK_PUBLIC_DEMO_ONLY", "true")
    req = JobRequest(
        packet=InboxPacket(
            job_id="safe-demo",
            source="synthetic-public-fixture",
            notes=["This is a scenario_or_assumption."],
        )
    )
    _validate_public_demo_request(req)


def test_public_demo_disables_packet_path(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("NIGHT_CLERK_PUBLIC_DEMO_ONLY", "true")
    with pytest.raises(HTTPException) as exc:
        _validate_public_demo_request(JobRequest(packet_path="/etc/passwd"))
    assert exc.value.status_code == 403
