#!/usr/bin/env bash
set -euo pipefail

PROJECT="${GOOGLE_CLOUD_PROJECT:-$(gcloud config get-value project 2>/dev/null || true)}"
if [[ -z "${PROJECT}" || "${PROJECT}" == "(unset)" ]]; then
  echo "GOOGLE_CLOUD_PROJECT is required; select the no-billing Firebase/Google Cloud project first." >&2
  exit 2
fi
if [[ -z "${GEMINI_API_KEY:-${GOOGLE_API_KEY:-}}" ]]; then
  echo "A Gemini Developer API free-tier key must already be present in GEMINI_API_KEY or GOOGLE_API_KEY." >&2
  exit 2
fi

python3 -m venv .venv-cloud-shell
source .venv-cloud-shell/bin/activate
python -m pip install --upgrade pip
python -m pip install -e '.[dev]'

# First prove the repository gate deterministically and without cloud/model I/O.
# This preserves the same local-gate semantics as CI even though a Gemini key is
# present in the private Cloud Shell session for the later live proof.
export NIGHT_CLERK_MODE=local
export NIGHT_CLERK_PUBLIC_DEMO_ONLY=true
python -m pytest -q
python -m night_clerk.cli run --packet fixtures/inbox/overvoltage-inbox.json

# Only after the deterministic gate passes, switch to the real zero-spend lane.
export GOOGLE_CLOUD_PROJECT="${PROJECT}"
export GOOGLE_GENAI_USE_VERTEXAI=false
export NIGHT_CLERK_MODE=gcp
export NIGHT_CLERK_MODEL="${NIGHT_CLERK_MODEL:-gemini-3.5-flash}"
export NIGHT_CLERK_STORAGE_BACKEND=firestore
export NIGHT_CLERK_COLLECTION="${NIGHT_CLERK_COLLECTION:-night_clerk_jobs}"

# The no-cost lane deliberately does not use Cloud Storage for Firebase because
# Spark projects cannot access Storage buckets without Blaze billing.
unset NIGHT_CLERK_BUCKET || true

LIVE_RECEIPT_JSON="$(python -m night_clerk.cli run --packet fixtures/inbox/overvoltage-inbox.json)"
printf '%s\n' "${LIVE_RECEIPT_JSON}"
export NIGHT_CLERK_LIVE_RECEIPT_JSON="${LIVE_RECEIPT_JSON}"

# Fail closed unless the live receipt is really Gemini 3.5 Flash and includes the
# deterministic rejection used in the submission story. Then read the exact
# persisted document back from Firestore and print only sanitized proof fields.
python - <<'PY'
import json
import os

from google.cloud import firestore

receipt = json.loads(os.environ["NIGHT_CLERK_LIVE_RECEIPT_JSON"])
expected_model = os.environ.get("NIGHT_CLERK_MODEL", "gemini-3.5-flash")
if receipt.get("model") != expected_model:
    raise SystemExit(f"Live model proof mismatch: {receipt.get('model')!r} != {expected_model!r}")

rejected = receipt.get("rejected") or []
if not any(item.get("reason") == "smoke_or_mesh_is_not_scientific_validation" for item in rejected):
    raise SystemExit("Deterministic false mesh-validation rejection was not observed")

job_id = receipt.get("job_id")
if not job_id:
    raise SystemExit("Live receipt did not contain job_id")

project = os.environ["GOOGLE_CLOUD_PROJECT"]
collection = os.environ["NIGHT_CLERK_COLLECTION"]
snapshot = firestore.Client(project=project).collection(collection).document(job_id).get()
if not snapshot.exists:
    raise SystemExit("Firestore readback failed: document does not exist")

data = snapshot.to_dict() or {}
if data.get("job_id") != job_id:
    raise SystemExit("Firestore readback failed: job_id mismatch")
if data.get("model") != expected_model:
    raise SystemExit("Firestore readback failed: model mismatch")

print("FIRESTORE_READBACK_OK")
print(json.dumps({
    "job_id": data.get("job_id"),
    "status": data.get("status"),
    "model": data.get("model"),
    "storage_uri": data.get("storage_uri"),
    "accepted_count": len(data.get("accepted") or []),
    "held_count": len(data.get("held") or []),
    "rejected_count": len(data.get("rejected") or []),
}, indent=2))
PY
unset NIGHT_CLERK_LIVE_RECEIPT_JSON

echo "Deterministic local gate, one real Gemini receipt, and Firestore write/readback completed."
echo "Starting the public synthetic demo on port ${PORT:-8080}."
exec python -m uvicorn night_clerk.server:app --host 0.0.0.0 --port "${PORT:-8080}"
