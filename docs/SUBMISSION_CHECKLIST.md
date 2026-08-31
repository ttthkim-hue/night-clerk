# Night Clerk submission gate

Deadline: **Aug 31, 2026 at 5:00 PM PT**.

Do not mark a gate PASS from intent or documentation. Require observed evidence.

## Gate status

- `LOCAL_GATE` — run `pytest` and one credential-free CLI dry-run from a clean environment.
- `GOOGLE_TECH_GATE` — live Google-hosted run must return a receipt whose `model` is `gemini-3.5-flash`; deterministic-only `model: not-run` is not sufficient.
- `CLOUD_GATE` — prove at least one Google Cloud infrastructure service and visibly prove the backend is running on Google Cloud. Preferred proof is Cloud Run/Vertex when already-funded. Zero-spend fallback may use Cloud Shell + one free Firestore database only when the video clearly shows the Google Cloud execution and Firestore readback; do not claim Cloud Run.
- `DEMO_GATE` — public synthetic demo packet completes end to end; the mesh-validation claim is rejected; the video visibly proves Google Cloud execution and a real Gemini-backed result.
- `SUBMISSION_PACKAGE_GATE` — Devpost draft has Taskmaster selected, text description, repo URL, architecture diagram, hosted URL if one actually exists, and a public YouTube/Vimeo video no longer than 4 minutes.

## Interactive steps

If an authenticated product browser is unavailable, the smallest manual UI steps are:

1. Sign in to Google Cloud/Firebase and open the no-billing project.
2. Create exactly one free Firestore database if absent, then open Cloud Shell.
3. Record the final Google Cloud execution and Firestore evidence.
4. Upload the final continuous demo to YouTube or Vimeo as publicly visible.
5. Paste the repo/video/description and any observed live URL into Devpost, then submit before the deadline.

Do not add or update a payment method solely to satisfy these steps.

## Four-minute demo storyboard

Aim for roughly 3:00–3:30 so upload/playback variance does not threaten the 4-minute evaluation limit.

### 0:00–0:25 — friction and promise

- Show the Night Clerk landing page or Web Preview.
- State the problem: research inbox notes mix literature, simulation, scenarios, and weak engineering checks; people can accidentally treat a mesh/smoke check as scientific validation.
- One sentence value proposition: Night Clerk finishes the classification job and writes an auditable receipt instead of chatting.

### 0:25–0:55 — architecture and authority

- Show the Mermaid architecture diagram in the repository.
- Point out Gemini 3.5 Flash / Gen AI SDK -> deterministic gate -> durable Google Cloud state.
- If the actual run uses zero-spend Firestore-only persistence, say so explicitly and do not narrate Cloud Storage as live proof.
- State the authority boundary: Gemini proposes the evidence label; deterministic code owns accept/hold/reject.

### 0:55–1:15 — undeniable cloud proof

Preferred evidence when available:

- live `.run.app` URL in the browser address bar;
- Cloud Run service dashboard/logs;
- Vertex AI logs.

Zero-spend fallback evidence:

- Google Cloud Shell/Console visibly running the backend;
- Cloud Shell Web Preview if available;
- active Firestore project/database visible in Google Cloud/Firebase console.

Do not rely only on a slide saying it is deployed.

### 1:15–2:30 — live proof of action

- Run the exact bundled synthetic public demo packet.
- Keep the run continuous.
- When the receipt appears, show:
  - `model: gemini-3.5-flash`;
  - at least one accepted claim;
  - the false mesh-validation sentence rejected with `smoke_or_mesh_is_not_scientific_validation`;
  - a Firestore-backed `storage_uri` or Cloud Storage URI only if that backend was actually used.
- Briefly show the corresponding Firestore document or Cloud Storage object to prove durable state.

### 2:30–3:10 — reproducibility and safety

- Show README/setup commands, architecture diagram, and synthetic fixture.
- Mention that local dry-run is credential-free, while cloud mode fails closed if Gemini is not configured.
- State that the public demo uses synthetic data only.

### 3:10–3:30 — close

- Reiterate: Night Clerk is a bounded Taskmaster workflow, not a generic chatbot.
- End on the live receipt or architecture.

## Video rules to preserve

- Maximum 4 minutes; only the first 4 minutes are evaluated.
- Publicly visible on YouTube or Vimeo.
- English, or include English subtitles.
- Show a genuine live execution.
- Do not fabricate Cloud Run, Firestore, Cloud Storage, Gemini, or submission evidence.

## Final readback

Before pressing Submit, verify all available links from a logged-out/incognito browser where possible:

- live app URL if one actually exists;
- public GitHub repository;
- public YouTube/Vimeo video;
- architecture diagram renders;
- README setup instructions are complete;
- no private paths, credentials, account identifiers, or research-confidential content are present.

After the deadline, leave submitted artifacts unchanged during judging unless organizers explicitly permit a correction.
