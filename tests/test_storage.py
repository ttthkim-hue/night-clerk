from __future__ import annotations

from night_clerk import storage
from night_clerk.schema import JobReceipt


class _FakeDocument:
    def __init__(self) -> None:
        self.payload = None

    def set(self, payload: dict) -> None:
        self.payload = payload


class _FakeCollection:
    def __init__(self, document: _FakeDocument) -> None:
        self._document = document

    def document(self, _job_id: str) -> _FakeDocument:
        return self._document


class _FakeDb:
    def __init__(self, document: _FakeDocument) -> None:
        self._document = document

    def collection(self, _name: str) -> _FakeCollection:
        return _FakeCollection(self._document)


def _receipt() -> JobReceipt:
    return JobReceipt(
        job_id="paper-demo",
        status="completed",
        model="gemini-3.5-flash",
        mode="gcp",
        accepted=1,
        held=1,
        rejected=1,
        claims=[],
        storage_uri="",
        evidence_of_run="receipt-written",
    )


def test_gcp_mode_requires_project(monkeypatch):
    monkeypatch.setenv("NIGHT_CLERK_MODE", "gcp")
    monkeypatch.delenv("GOOGLE_CLOUD_PROJECT", raising=False)
    monkeypatch.delenv("NIGHT_CLERK_BUCKET", raising=False)

    try:
        storage.build_storage()
    except RuntimeError as exc:
        assert "GOOGLE_CLOUD_PROJECT" in str(exc)
    else:
        raise AssertionError("gcp mode must fail closed without a project")


def test_gcp_mode_without_bucket_routes_to_firestore(monkeypatch):
    sentinel = object()
    monkeypatch.setenv("NIGHT_CLERK_MODE", "gcp")
    monkeypatch.setenv("GOOGLE_CLOUD_PROJECT", "demo-project")
    monkeypatch.delenv("NIGHT_CLERK_BUCKET", raising=False)
    monkeypatch.delenv("NIGHT_CLERK_STORAGE_BACKEND", raising=False)
    monkeypatch.setattr(storage, "FirestoreStorage", lambda **_kwargs: sentinel)

    assert storage.build_storage() is sentinel


def test_firestore_storage_writes_full_receipt_without_project_identifier():
    document = _FakeDocument()
    store = object.__new__(storage.FirestoreStorage)
    store.project = "private-project-id"
    store.collection = "night_clerk_jobs"
    store._db = _FakeDb(document)

    receipt = _receipt()
    uri = store.write_receipt(receipt)

    assert uri == "firestore://night_clerk_jobs/paper-demo"
    assert "private-project-id" not in uri
    assert receipt.storage_uri == uri
    assert document.payload is not None
    assert document.payload["model"] == "gemini-3.5-flash"
    assert document.payload["receipt"]["storage_uri"] == uri
