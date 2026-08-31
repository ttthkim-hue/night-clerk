# Night Clerk submission gate

Deadline: **Aug 31, 2026 at 5:00 PM PT**.

Do not mark a gate PASS from intent or documentation. Require observed evidence.

## Gate status

- `LOCAL_GATE` — run `pytest` and one credential-free CLI dry-run from a clean environment.
- `GOOGLE_TECH_GATE` — live cloud run must return a receipt whose `model` is `gemini-3.5-flash`; deterministic-only `model: not-run` is not sufficient for the contest.
- `CLOUD_GATE` — deployed `.run.app` URL responds to `/health`; one `/jobs` call writes a Cloud Storage receipt and Firestore record.
- `DEMO_GATE` — public demo packet completes end to end; the mesh-validation claim is rejected; the video visibly proves Google Cloud execution.
- `SUBMISSION_PACKAGE_GATE` — Devpost draft has Taskmaster selected, text description, repo URL, architecture diagram, hosted URL if available, and a public YouTube/Vimeo video no longer than 4 minutes.

## Owner-interactive steps

These cannot be completed by repository automation:

1. Sign in to Devpost and confirm the account has joined the All Things Agentic Hackathon.
2. Create/open the Night Clerk submission draft and accept any required official rules/entry terms.
3. Upload the final continuous demo to **YouTube or Vimeo as publicly visible**.
4. Paste the live URL, repository URL, video URL, and final description into Devpost.
5. Press the final submission button before the deadline and verify the submitted entry page/confirmation.

## Four-minute demo storyboard

Aim for roughly 3:00–3:30 so upload/playback variance does not threaten the 4-minute evaluation limit.

### 0:00–0:25 — friction and promise

- Show the Night Clerk landing page.
- State the problem: research inbox notes mix literature, simulation, scenarios, and weak engineering checks; people can accidentally treat a mesh/smoke check as scientific validation.
- One sentence value proposition: Night Clerk finishes the classification job and writes an auditable receipt instead of chatting.

### 0:25–0:55 — architecture and authority

- Show the Mermaid architecture diagram in the repository.
- Point out Cloud Run -> Gemini 3.5 Flash on Vertex AI -> deterministic gate -> Cloud Storage + Firestore.
- State the authority boundary: Gemini proposes the evidence label; deterministic code owns accept/hold/reject.

### 0:55–1:15 — undeniable cloud proof

Show at least one of these while recording:

- the live `.run.app` URL in the browser address bar;
- Cloud Run service dashboard/logs.

Do not rely only on a slide saying it is deployed.

### 1:15–2:30 — live proof of action

- Press **Run public demo packet** on the live Cloud Run page.
- Keep the run continuous.
- When the receipt appears, show:
  - `model: gemini-3.5-flash`;
  - at least one accepted claim;
  - the false mesh-validation sentence rejected with `smoke_or_mesh_is_not_scientific_validation`;
  - the `gs://...` receipt URI if safe to show.
- Briefly show the corresponding Firestore job record or Cloud Storage object to prove durable state.

### 2:30–3:10 — reproducibility and safety

- Show README setup commands, architecture diagram, and synthetic fixture.
- Mention that local dry-run is credential-free, while cloud mode fails closed if Gemini is not configured.
- State that the public demo uses synthetic data only.

### 3:10–3:30 — close

- Reiterate: Night Clerk is a bounded Taskmaster workflow, not a generic chatbot.
- End on the live receipt or architecture.

## Video rules to preserve

- Maximum 4 minutes; only the first 4 minutes are evaluated.
- Publicly visible on YouTube or Vimeo.
- English, or include English subtitles.
- Show a genuine live execution. A continuous uniform speed-up is acceptable only if it remains a real single run; add an on-screen note if sped up.
- Do not fabricate Cloud Run, Firestore, GCS, Gemini, or submission evidence.

## Final readback

Before pressing Submit, verify all links from a logged-out/incognito browser where possible:

- live app / `.run.app` URL;
- public GitHub repository;
- public YouTube/Vimeo video;
- architecture diagram renders;
- README setup instructions are complete;
- no private paths, credentials, account identifiers, or research-confidential content are present.

After the deadline, leave submitted artifacts unchanged during judging unless organizers explicitly permit a correction.
