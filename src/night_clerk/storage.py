from __future__ import annotations

import json
import os
from pathlib import Path

from night_clerk.schema import InboxPacket, JobReceipt


class Storage:
    def load_packet(self, path: str | Path) -> InboxPacket:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        return InboxPacket.model_validate(data)

    def write_receipt(self, receipt: JobReceipt) -> str:
        raise NotImplementedError


class LocalStorage(Storage):
    def __init__(self, root: Path | None = None) -> None:
        self.root = root or Path.cwd() / ".night-clerk"
        (self.root / "receipts").mkdir(parents=True, exist_ok=True)
        (self.root / "jobs").mkdir(parents=True, exist_ok=True)

    def write_receipt(self, receipt: JobReceipt) -> str:
        path = self.root / "receipts" / f"{receipt.job_id}.json"
        path.write_text(receipt.model_dump_json(indent=2), encoding="utf-8")
        job_path = self.root / "jobs" / f"{receipt.job_id}.json"
        job_path.write_text(
            json.dumps({"job_id": receipt.job_id, "status": receipt.status}, indent=2),
            encoding="utf-8",
        )
        uri = path.resolve().as_uri()
        receipt.storage_uri = uri
        path.write_text(receipt.model_dump_json(indent=2), encoding="utf-8")
        return uri


class FirestoreStorage(Storage):
    """Firestore-only receipt persistence for billing-free Spark/Cloud Shell demos."""

    def __init__(self, project: str, collection: str) -> None:
        from google.cloud import firestore

        self.project = project
        self.collection = collection
        self._db = firestore.Client(project=project)

    def write_receipt(self, receipt: JobReceipt) -> str:
        # Keep the public receipt free of project/account identifiers. The actual
        # project remains available only to the authenticated Firestore client.
        uri = f"firestore://{self.collection}/{receipt.job_id}"
        receipt.storage_uri = uri
        self._db.collection(self.collection).document(receipt.job_id).set(
            {
                "job_id": receipt.job_id,
                "status": receipt.status,
                "storage_uri": uri,
                "accepted": receipt.accepted,
                "held": receipt.held,
                "rejected": receipt.rejected,
                "model": receipt.model,
                "receipt": receipt.model_dump(mode="json"),
            }
        )
        return uri


class GcpStorage(Storage):
    def __init__(self, project: str, bucket: str, collection: str) -> None:
        from google.cloud import firestore, storage as gcs

        self.project = project
        self.bucket_name = bucket
        self.collection = collection
        self._db = firestore.Client(project=project)
        self._gcs = gcs.Client(project=project)

    def write_receipt(self, receipt: JobReceipt) -> str:
        blob_name = f"receipts/{receipt.job_id}.json"
        bucket = self._gcs.bucket(self.bucket_name)
        blob = bucket.blob(blob_name)
        uri = f"gs://{self.bucket_name}/{blob_name}"
        receipt.storage_uri = uri
        payload = receipt.model_dump_json(indent=2)
        blob.upload_from_string(payload, content_type="application/json")
        self._db.collection(self.collection).document(receipt.job_id).set(
            {
                "job_id": receipt.job_id,
                "status": receipt.status,
                "storage_uri": uri,
                "accepted": receipt.accepted,
                "held": receipt.held,
                "rejected": receipt.rejected,
                "model": receipt.model,
            }
        )
        return uri


def build_storage() -> Storage:
    project = os.getenv("GOOGLE_CLOUD_PROJECT", "").strip()
    bucket = os.getenv("NIGHT_CLERK_BUCKET", "").strip()
    mode = os.getenv("NIGHT_CLERK_MODE", "local").strip().lower()
    collection = os.getenv("NIGHT_CLERK_COLLECTION", "night_clerk_jobs")
    backend = os.getenv("NIGHT_CLERK_STORAGE_BACKEND", "").strip().lower()

    if mode == "local":
        return LocalStorage()
    if mode != "gcp":
        raise RuntimeError(f"Unsupported NIGHT_CLERK_MODE: {mode}")
    if not project:
        raise RuntimeError("NIGHT_CLERK_MODE=gcp requires GOOGLE_CLOUD_PROJECT")

    if backend in {"firestore", "firestore-only"} or not bucket:
        return FirestoreStorage(project=project, collection=collection)
    if backend not in {"", "gcs", "gcs+firestore"}:
        raise RuntimeError(f"Unsupported NIGHT_CLERK_STORAGE_BACKEND: {backend}")

    return GcpStorage(
        project=project,
        bucket=bucket,
        collection=collection,
    )
