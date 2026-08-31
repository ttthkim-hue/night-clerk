# Devpost submission draft

**Category:** Taskmaster

**Project name:** Night Clerk

**Tagline:** An overnight research-inbox clerk that turns messy evidence into auditable receipts.

> **Submission-state guard:** This file is a draft until the live proof is recorded. Before submitting, keep only claims that match the observed Google Cloud run. Do not claim Cloud Run, Cloud Storage, Vertex AI, a hosted URL, or a public video unless that exact evidence exists.

## Inspiration

A research inbox is not just text. It mixes literature claims, simulation results, scenario assumptions, protected literals, and quick engineering checks. The dangerous failure mode is treating a weak check — for example, “the mesh check passed” — as if it scientifically validated the model.

Night Clerk was built to finish that boring but high-consequence cleanup job without becoming another chatbot. It processes the packet, labels the evidence, applies a deterministic safety gate, persists a receipt, and stops for human review.

## What it does

A user or upstream system submits one inbox packet to Night Clerk. The workflow:

1. reads and normalizes the notes;
2. asks **Gemini 3.5 Flash** for an evidence label from a closed set;
3. passes every proposed label through a deterministic scientific-safety gate;
4. accepts, holds, or rejects each claim;
5. writes an auditable receipt to the configured Google Cloud persistence backend;
6. returns the receipt to the caller for morning review.

The model never gets final authority over scientific validation. The deterministic gate rejects a statement that treats a mesh check, smoke test, compile success, or visualization success as scientific proof. Protected literals and numeric claims that remain unverified are held for a human.

## How we built it

- **Gemini 3.5 Flash** through the Google Gen AI SDK for evidence classification.
- **Google Gen AI SDK** as a required Google agent framework in the executable pipeline.
- **Google ADK** root agent exposing the same bounded Night Clerk workflow tools for ADK-compatible execution.
- **FastAPI + Pydantic** for the typed HTTP/job boundary.
- A deterministic Python evidence gate that is deliberately outside model authority.
- Two implemented Google Cloud execution/persistence paths:
  - funded/credit path: **Cloud Run + Vertex AI + Cloud Storage + Firestore**;
  - zero-spend fallback: backend process in **Google Cloud Shell + Gemini Developer API free tier + Firestore-only persistence**.

The final submission must describe only the path actually demonstrated in the video. Cloud Shell is not Cloud Run, and the draft must not imply otherwise.

The public demo uses only a synthetic fixture. No private research inbox, credentials, or confidential data are required to reproduce it.

## Architecture

Core authority flow:

`Inbox packet -> Gemini 3.5 Flash / Gen AI SDK -> deterministic evidence gate -> Google Cloud receipt state -> human review`

Runtime/persistence is selected by the demonstrated lane:

- Cloud Run lane: `Cloud Run -> Vertex AI -> deterministic gate -> Cloud Storage + Firestore`.
- Zero-spend lane: `Cloud Shell -> Gemini Developer API -> deterministic gate -> Firestore`.

The repository includes a Mermaid architecture diagram and full spin-up instructions.

## Proof of action

Repository: `https://github.com/ttthkim-hue/night-clerk`

Observed Google Cloud runtime / hosted project: `[REPLACE_ONLY_AFTER_LIVE_EVIDENCE]`

Demo video: `[PUBLIC_YOUTUBE_OR_VIMEO_URL]`

The final continuous demo should show:

- the backend visibly running on Google Cloud;
- a real `gemini-3.5-flash` result;
- the bundled synthetic packet running end to end;
- the deliberately false sentence claiming that a mesh check scientifically validates a CFD result being rejected by the deterministic gate;
- the corresponding durable Firestore document, plus Cloud Storage only if that backend was actually used.

If the zero-spend path is used, show Google Cloud Shell/Console and Firestore and state explicitly that the runtime is Cloud Shell, not Cloud Run. If Cloud Run is actually used, show the `.run.app` URL or Cloud Run dashboard/logs. Do not replace placeholders until the corresponding evidence has been verified.

## Data sources

The submission demo uses one repository fixture, `fixtures/inbox/overvoltage-inbox.json`. It is synthetic public-safe data created for the project. One note references OpenDSS as a public network-template concept, but Night Clerk does not retrieve external OpenDSS data during the demo.

No private datasets or third-party paid APIs are needed for the contest demo.

## Challenges we ran into

The main design challenge was authority, not prompting. A model is useful for ambiguous classification, but allowing it to declare a scientific conclusion would recreate the original problem. We therefore separated the workflow into a probabilistic labeling step and a deterministic accept/hold/reject gate.

A second challenge was making local tests easy without weakening the contest deployment. Local mode is intentionally credential-free and deterministic. Google-backed mode is different: it fails closed unless Gemini is actually configured, so a deterministic-only run cannot silently masquerade as the required Gemini-backed execution.

A third challenge was producing valid Google Cloud proof without adding new paid billing. The repository therefore contains a Firestore-only Cloud Shell lane in addition to the Cloud Run/Vertex path; the final submission will use only the lane that is actually evidenced.

## Accomplishments

- A complete job path rather than a conversational UI.
- Deterministic enforcement of the “mesh/smoke check is not scientific validation” rule.
- Typed receipts that make every decision reviewable.
- A synthetic, reproducible public demo packet.
- Google Cloud execution paths that fail closed instead of silently replacing Gemini with a local fallback.
- Reproducible clean CI validation for the local gate.

## What we learned

For agentic scientific workflows, “human in the loop” is not enough by itself. The system needs an explicit authority boundary. Night Clerk uses Gemini where semantic judgment helps, but moves the high-consequence decision into code that can be tested and audited.

We also learned that proof matters as much as architecture: the submission video must show the real Google Cloud execution, live job, and durable receipt rather than relying on screenshots or claims about what should be running.

## What's next

After the hackathon, the natural extension is not a larger chatbot. It is a controlled inbox adapter that can ingest authorized research notes, schedule jobs, and route held/rejected claims to a review queue while preserving the same deterministic authority boundary.

## Project lineage disclosure

Night Clerk is new contest work created during the 2026 submission period. Its problem framing is informed by earlier work on scientific evidence labeling and orchestration, including `scientific-llm-orchestrator`; this repository is a separate contest implementation and is not a resubmission of that project.
