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

export GOOGLE_CLOUD_PROJECT="${PROJECT}"
export GOOGLE_GENAI_USE_VERTEXAI=false
export NIGHT_CLERK_MODE=gcp
export NIGHT_CLERK_MODEL="${NIGHT_CLERK_MODEL:-gemini-3.5-flash}"
export NIGHT_CLERK_STORAGE_BACKEND=firestore
export NIGHT_CLERK_COLLECTION="${NIGHT_CLERK_COLLECTION:-night_clerk_jobs}"
export NIGHT_CLERK_PUBLIC_DEMO_ONLY=true

# The no-cost lane deliberately does not use Cloud Storage for Firebase because
# Spark projects cannot access Storage buckets without Blaze billing.
unset NIGHT_CLERK_BUCKET || true

python3 -m venv .venv-cloud-shell
source .venv-cloud-shell/bin/activate
python -m pip install --upgrade pip
python -m pip install -e '.[dev]'

pytest
python -m night_clerk.cli run --packet fixtures/inbox/overvoltage-inbox.json

echo "Clean tests and one Gemini+Firestore receipt completed."
echo "Starting the public synthetic demo on port ${PORT:-8080}."
exec python -m uvicorn night_clerk.server:app --host 0.0.0.0 --port "${PORT:-8080}"
