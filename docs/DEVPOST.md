# Devpost submission draft

**Category:** Taskmaster

**Project name:** Night Clerk

**Tagline:** An overnight research-inbox clerk that turns messy evidence into auditable receipts.

## Inspiration

A research inbox is not just text. It mixes literature claims, simulation results, scenario assumptions, protected literals, and quick engineering checks. The dangerous failure mode is treating a weak check — for example, “the mesh check passed” — as if it scientifically validated the model.

Night Clerk was built to finish that boring but high-consequence cleanup job without becoming another chatbot. It processes the packet, labels the evidence, applies a deterministic safety gate, persists a receipt, and stops for human review.

## What it does

A user or upstream system submits one inbox packet to Night Clerk. The workflow:

1. reads and normalizes the notes;
2. asks **Gemini 3.5 Flash** for an evidence label from a closed set;
3. passes every proposed label through a deterministic scientific-safety gate;
4. accepts, holds, or rejects each claim;
5. writes the full receipt to **Cloud Storage** and a compact job record to **Firestore**;
6. returns the receipt to the caller for morning review.

The model never gets final authority over scientific validation. The deterministic gate rejects a statement that treats a mesh check, smoke test, compile success, or visualization success as scientific proof. Protected literals and numeric claims that remain unverified are held for a human.

## How we built it

- **Gemini 3.5 Flash** through the Google Gen AI SDK on Vertex AI for evidence classification.
- **Google Gen AI SDK** as the mandatory Google agent framework in the deployed path.
- **Google ADK** root agent exposing the same bounded Night Clerk workflow tools for ADK-compatible execution.
- **Cloud Run** for the public FastAPI service and demo UI.
- **Cloud Storage** for durable JSON receipts.
- **Firestore** for compact job status and receipt metadata.
- **FastAPI + Pydantic** for the typed HTTP/job boundary.
- A deterministic Python evidence gate that is deliberately outside model authority.

The public demo uses only a synthetic fixture. No private research inbox, credentials, or confidential data are required to reproduce it.

## Architecture

`Inbox packet -> Cloud Run -> Gemini 3.5 Flash / Gen AI SDK -> deterministic evidence gate -> Cloud Storage receipt + Firestore job record -> human review`

The repository includes a Mermaid architecture diagram and full spin-up instructions.

## Proof of action

Hosted project: `[LIVE_CLOUD_RUN_URL]`

Repository: `https://github.com/ttthkim-hue/night-clerk`

Demo video: `[PUBLIC_YOUTUBE_OR_VIMEO_URL]`

In the live demo, press **Run public demo packet**. The packet contains a deliberately false sentence claiming that a mesh check scientifically validates a CFD result. Gemini proposes evidence labels; the deterministic gate rejects that false-validation claim and the service returns a persisted receipt.

The final video should visibly show the `.run.app` URL or Cloud Run dashboard/logs plus the live receipt and its Firestore/GCS evidence. Do not replace these placeholders until the corresponding links have been verified.

## Data sources

The submission demo uses one repository fixture, `fixtures/inbox/overvoltage-inbox.json`. It is synthetic public-safe data created for the project. One note references OpenDSS as a public network-template concept, but Night Clerk does not retrieve external OpenDSS data during the demo.

No private datasets or third-party paid APIs are needed for the contest demo.

## Challenges we ran into

The main design challenge was authority, not prompting. A model is useful for ambiguous classification, but allowing it to declare a scientific conclusion would recreate the original problem. We therefore separated the workflow into a probabilistic labeling step and a deterministic accept/hold/reject gate.

A second challenge was making local tests easy without weakening the contest deployment. Local mode is intentionally credential-free and deterministic. Cloud mode is different: it fails closed unless Gemini is actually configured, so a deterministic-only run cannot silently masquerade as the required Gemini-backed deployment.

## Accomplishments

- A complete job path rather than a conversational UI.
- Deterministic enforcement of the “mesh/smoke check is not scientific validation” rule.
- Typed receipts that make every decision reviewable.
- A synthetic, reproducible public demo packet.
- A deployment architecture that connects Gemini to Cloud Run, Cloud Storage, and Firestore without putting service-account keys in the repository.

## What we learned

For agentic scientific workflows, “human in the loop” is not enough by itself. The system needs an explicit authority boundary. Night Clerk uses Gemini where semantic judgment helps, but moves the high-consequence decision into code that can be tested and audited.

We also learned that production-readiness proof matters as much as architecture: the contest demo should show the real Cloud Run URL, a live job, and the durable receipt rather than relying on screenshots or claims about what should be running.

## What's next

After the hackathon, the natural extension is not a larger chatbot. It is a controlled inbox adapter that can ingest authorized research notes, schedule jobs, and route held/rejected claims to a review queue while preserving the same deterministic authority boundary.

## Project lineage disclosure

Night Clerk is new contest work created during the 2026 submission period. Its problem framing is informed by earlier work on scientific evidence labeling and orchestration, including `scientific-llm-orchestrator`; this repository is a separate contest implementation and is not a resubmission of that project.
