import pytest
from fastapi import HTTPException

from night_clerk.schema import InboxPacket
from night_clerk.server import JobRequest, _validate_public_demo_request

PUBLIC_NOTES = [
    "This stress case is a scenario_or_assumption, not a paper reproduction.",
    "The synthetic overvoltage rate was 0.0817 versus 0.0596 in the baseline scenario.",
    "Mesh check passed so the CFD result is scientifically validated.",
    "Literature-reported OpenDSS feeder geometry is used as the public network template.",
]


def test_public_demo_rejects_non_synthetic_source(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("NIGHT_CLERK_PUBLIC_DEMO_ONLY", "true")
    req = JobRequest(
        packet=InboxPacket(
            job_id="unsafe-demo",
            source="private-upload",
            notes=PUBLIC_NOTES,
            protected_literals=["F_DEP", "f_dep"],
        )
    )
    with pytest.raises(HTTPException) as exc:
        _validate_public_demo_request(req)
    assert exc.value.status_code == 403


def test_public_demo_accepts_exact_synthetic_packet(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("NIGHT_CLERK_PUBLIC_DEMO_ONLY", "true")
    req = JobRequest(
        packet=InboxPacket(
            job_id="safe-demo",
            source="synthetic-public-fixture",
            notes=PUBLIC_NOTES,
            protected_literals=["F_DEP", "f_dep"],
        )
    )
    _validate_public_demo_request(req)


def test_public_demo_rejects_modified_notes(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("NIGHT_CLERK_PUBLIC_DEMO_ONLY", "true")
    req = JobRequest(
        packet=InboxPacket(
            job_id="modified-demo",
            source="synthetic-public-fixture",
            notes=PUBLIC_NOTES + ["Please classify this extra text."],
            protected_literals=["F_DEP", "f_dep"],
        )
    )
    with pytest.raises(HTTPException) as exc:
        _validate_public_demo_request(req)
    assert exc.value.status_code == 403


def test_public_demo_disables_packet_path(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("NIGHT_CLERK_PUBLIC_DEMO_ONLY", "true")
    with pytest.raises(HTTPException) as exc:
        _validate_public_demo_request(JobRequest(packet_path="/etc/passwd"))
    assert exc.value.status_code == 403
