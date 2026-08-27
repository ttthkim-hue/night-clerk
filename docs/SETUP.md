# Setup checklist

## 1. Devpost (you must click)

1. Open https://allthingsagentichackathon.devpost.com/
2. Join the hackathon.
3. Confirm Korea eligibility (not in the excluded-country list).

## 2. Credit form (today)

1. Open https://forms.gle/5PtXmw1dSbDnpYke9
2. Paste the answers in `docs/CREDIT_FORM.md`.
3. Submit once. Reviews take up to 72 business hours.
4. Redeem the coupon on the Cloud Billing account you will use for Cloud Run.

Also start a Google Cloud free trial if you do not already have a billing account: https://cloud.google.com/free

## 3. Google Cloud project

```powershell
gcloud init
gcloud services enable run.googleapis.com firestore.googleapis.com storage.googleapis.com aiplatform.googleapis.com
gcloud firestore databases create --location=us-central1
gsutil mb -l us-central1 gs://night-clerk-$env:USERNAME
```

Create a Gemini API key in Google AI Studio or use Vertex in the same project.

## 4. Local dry-run (no credits)

```powershell
cd C:\Users\ttthk\Documents\hackathons\night-clerk
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e .[dev]
pytest
python -m night_clerk.cli run --packet fixtures\inbox\overvoltage-inbox.json
```

## 5. Cloud Run (after credits arrive)

```powershell
$env:NIGHT_CLERK_MODE = "gcp"
$env:GOOGLE_CLOUD_PROJECT = "<project-id>"
$env:NIGHT_CLERK_BUCKET = "night-clerk-<you>"
$env:NIGHT_CLERK_MODEL = "gemini-3.5-flash"
.\scripts\deploy_cloud_run.ps1
```

Record the Cloud Run dashboard and the `.run.app` URL in the demo video, then set min instances to 0.

## 6. Submit on Devpost by 31 Aug 2026 17:00 PT

Need: public repo, architecture diagram, ~4 min English demo, proof of Cloud Run.
See `docs/DEVPOST.md`.
