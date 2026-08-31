# Setup and submission checklist

Night Clerk targets the **Taskmaster** category of the All Things Agentic Hackathon 2026.

The official baseline requirements are:

- a project newly created during the Aug 3–31, 2026 submission period;
- Gemini 3.5 or newer through Gemini API or Vertex AI;
- at least one Google agent framework (Night Clerk uses Google ADK and the Google Gen AI SDK);
- at least one Google Cloud infrastructure service (Night Clerk uses Cloud Run, Cloud Storage, and Firestore);
- one selected contest category;
- a repository URL with reproducible spin-up instructions;
- an architecture diagram;
- a public YouTube or Vimeo demo, at most 4 minutes, in English or with English subtitles;
- visible proof in the demo that the backend is running on Google Cloud.

The submission deadline is **Aug 31, 2026 at 5:00 PM PT**.

## 1. Devpost — owner UI required

1. Open the All Things Agentic Hackathon page on Devpost.
2. Join/register if the account has not already joined.
3. Create or open the Night Clerk submission draft.
4. Select **Taskmaster** as the single category.
5. Do not press the final submit button until every gate in `docs/SUBMISSION_CHECKLIST.md` is complete.

Devpost registration, acceptance of the official rules, public video upload, and final submission are owner-interactive actions.

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

## 3. Google Cloud project

Use an existing project or a no-cost/free-trial project that you are authorized to use. The hackathon credit-request deadline was Aug 28, 2026; do not wait for credits before finishing the submission if an existing no-cost account is available.

Authenticate `gcloud`, select the target project, and enable the required APIs:

```powershell
gcloud auth login
gcloud config set project <project-id>
gcloud services enable run.googleapis.com firestore.googleapis.com storage.googleapis.com aiplatform.googleapis.com cloudbuild.googleapis.com artifactregistry.googleapis.com
```

Create Firestore once if the project does not already have a database:

```powershell
gcloud firestore databases create --location=us-central1
```

Create a globally unique bucket name:

```powershell
$env:GOOGLE_CLOUD_PROJECT = "<project-id>"
$env:NIGHT_CLERK_BUCKET = "<globally-unique-bucket-name>"
gsutil mb -l us-central1 "gs://$env:NIGHT_CLERK_BUCKET"
```

Cloud Run uses Application Default Credentials to call **Vertex AI / Gemini 3.5 Flash**. The Cloud Run runtime service account therefore needs permission to call Vertex AI and write the Firestore/GCS receipt. If the first live request returns a permission error, grant only the minimum required roles to the runtime service account (typically Vertex AI User plus Firestore/Storage write access) and retry. Do not place service-account keys in this repository.

## 4. Deploy Cloud Run

```powershell
$env:NIGHT_CLERK_MODE = "gcp"
$env:GOOGLE_CLOUD_PROJECT = "<project-id>"
$env:NIGHT_CLERK_BUCKET = "<globally-unique-bucket-name>"
$env:NIGHT_CLERK_MODEL = "gemini-3.5-flash"
$env:GOOGLE_CLOUD_LOCATION = "global"
.\scripts\deploy_cloud_run.ps1
```

The deployment script sets `GOOGLE_GENAI_USE_VERTEXAI=true`. Cloud mode now fails closed if a Gemini transport is not actually configured; it must not silently present a deterministic-only run as a Gemini-backed cloud run.

## 5. Live proof

After deployment, record the generated `.run.app` URL and verify:

```powershell
curl.exe https://<service>.run.app/health
```

Then open the root page in a browser and use **Run public demo packet**. The resulting receipt should show at least one accepted claim and rejection of the false statement that a mesh check scientifically validates a CFD result.

For the contest demo, also capture one unambiguous Google Cloud proof frame: the `.run.app` URL in the browser address bar or the Cloud Run dashboard/logs.

## 6. Submission package

Use `docs/DEVPOST.md` for the contest write-up and `docs/SUBMISSION_CHECKLIST.md` for the final gate. The demo must be publicly visible on YouTube or Vimeo and no longer than four minutes; only a real live run should be presented as proof of action.

After the submission deadline, do not modify the submitted repository/video/live site during judging unless the organizer explicitly permits it. If continued development is needed, work from a separate fork or branch that is not the submitted artifact.
