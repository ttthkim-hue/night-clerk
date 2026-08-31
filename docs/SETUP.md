# Setup and submission checklist

Night Clerk targets the **Taskmaster** category of the All Things Agentic Hackathon 2026.

The official baseline requirements are:

- a project newly created during the Aug 3–31, 2026 submission period;
- Gemini 3.5 or newer through Gemini API or Vertex AI;
- at least one Google agent framework (Night Clerk uses Google ADK and the Google Gen AI SDK);
- at least one Google Cloud infrastructure service;
- one selected contest category;
- a repository URL with reproducible spin-up instructions;
- an architecture diagram;
- a public YouTube or Vimeo demo, at most 4 minutes, in English or with English subtitles;
- visible proof in the demo that the backend is running on Google Cloud.

The submission deadline is **Aug 31, 2026 at 5:00 PM PT**.

## 1. Devpost

1. Open the All Things Agentic Hackathon page on Devpost.
2. Join/register if the account has not already joined.
3. Create or open the Night Clerk submission draft.
4. Select **Taskmaster** as the single category.
5. Do not mark the entry submitted until every observed-evidence gate in `docs/SUBMISSION_CHECKLIST.md` is complete.

## 2. Local reproducibility

Python 3.11+:

```powershell
git clone https://github.com/ttthkim-hue/night-clerk.git
cd night-clerk
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e .[dev]
pytest
python -m night_clerk.cli run --packet fixtures\inbox\overvoltage-inbox.json
```

The local dry-run is intentionally credential-free and uses the deterministic fallback labeler. It proves the evidence gate and receipt path, not the mandatory Gemini runtime.

## 3A. Zero-spend Google Cloud proof path

Use this path when no active Cloud Billing account or contest/research credit is available. Do **not** add a payment method solely for the submission.

The zero-spend lane uses:

- **Google Cloud Shell** as the Google-hosted Linux execution environment;
- **Firebase Spark / Cloud Firestore** as the required Google Cloud infrastructure service;
- **Gemini Developer API free tier** for the real `gemini-3.5-flash` call;
- Google ADK / Gen AI SDK from this repository.

Cloud Storage for Firebase is deliberately excluded from this path because current Spark projects require Blaze billing for Storage access.

Prerequisites:

1. Sign in to Google Cloud/Firebase.
2. Create or select one no-billing project.
3. Create exactly one free Firestore database for that project.
4. Open Cloud Shell and select that project.
5. Make an already-authorized Gemini Developer API free-tier key available only in the Cloud Shell session as `GEMINI_API_KEY` or `GOOGLE_API_KEY`. Never commit it.

Then in Cloud Shell:

```bash
git clone https://github.com/ttthkim-hue/night-clerk.git
cd night-clerk
git checkout work/issue-1-night-clerk-submission
export GOOGLE_CLOUD_PROJECT="$(gcloud config get-value project)"
# export GEMINI_API_KEY="..."  # set only in the private shell session
bash scripts/run_cloud_shell_firestore.sh
```

The script runs the full test suite, performs one real Gemini-backed synthetic receipt using Firestore-only persistence, and starts the FastAPI demo on port 8080. Use Cloud Shell Web Preview if useful for the recording.

For the video, visibly show Cloud Shell/Google Cloud Console, the live backend process, the `gemini-3.5-flash` receipt, and the corresponding Firestore document. Do **not** describe this path as Cloud Run. The contest requires proof that the backend is running on Google Cloud; if organizer guidance or the submission UI requires a stronger deployment surface, treat that as a blocker rather than overstating the evidence.

## 3B. Cloud Run / Vertex AI path — only with already-active no-cost credit

Use this path only if an already-active free trial, contest credit, or research-credit billing account is independently available. Do not reactivate a closed billing account merely for the hackathon.

```powershell
gcloud auth login
gcloud config set project <project-id>
gcloud services enable run.googleapis.com firestore.googleapis.com storage.googleapis.com aiplatform.googleapis.com cloudbuild.googleapis.com artifactregistry.googleapis.com
gcloud firestore databases create --location=us-central1
$env:GOOGLE_CLOUD_PROJECT = "<project-id>"
$env:NIGHT_CLERK_BUCKET = "<globally-unique-bucket-name>"
gsutil mb -l us-central1 "gs://$env:NIGHT_CLERK_BUCKET"
```

Cloud Run uses Application Default Credentials to call Vertex AI / Gemini 3.5 Flash. Grant only the minimum required runtime roles and never place service-account keys in this repository.

## 4. Deploy Cloud Run when 3B is eligible

```powershell
$env:NIGHT_CLERK_MODE = "gcp"
$env:GOOGLE_CLOUD_PROJECT = "<project-id>"
$env:NIGHT_CLERK_BUCKET = "<globally-unique-bucket-name>"
$env:NIGHT_CLERK_MODEL = "gemini-3.5-flash"
$env:GOOGLE_CLOUD_LOCATION = "global"
.\scripts\deploy_cloud_run.ps1
```

The deployment script sets `GOOGLE_GENAI_USE_VERTEXAI=true`. Cloud mode fails closed if a Gemini transport is not actually configured.

## 5. Live proof

For Cloud Run, record the generated `.run.app` URL and verify `/health`, then run the exact synthetic public demo packet.

For the zero-spend Cloud Shell path, show the Cloud Shell/Google Cloud Console execution, Web Preview when available, the real Gemini-backed receipt, and Firestore write/readback. The receipt should show rejection of the false statement that a mesh check scientifically validates a CFD result.

Never substitute a deterministic local-only run for the required Gemini proof.

## 6. Submission package

Use `docs/DEVPOST.md` for the contest write-up and `docs/SUBMISSION_CHECKLIST.md` for the final gate. The demo must be publicly visible on YouTube or Vimeo and no longer than four minutes; only observed live behavior should be presented as proof of action.

After the submission deadline, do not modify the submitted repository/video/live site during judging unless the organizer explicitly permits it. If continued development is needed, work from a separate fork or branch that is not the submitted artifact.
