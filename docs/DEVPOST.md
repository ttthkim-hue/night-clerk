# Devpost submission draft

**Category:** Taskmaster

**Project name:** Night Clerk

**Tagline:** Overnight research-inbox clerk that writes evidence receipts.

## Description

Night Clerk takes a messy research inbox packet and finishes the job while you are away. It labels each note with an evidence type, holds numeric claims that lack a label, and rejects the common lie that a mesh check or smoke test is scientific validation. The output is a signed receipt in Cloud Storage plus a Firestore job record. There is no chat product path.

This entry is newly built for the All Things Agentic Hackathon. It reuses a public idea from scientific evidence labeling; it does not submit the older `scientific-llm-orchestrator` repository.

## Features

- Autonomous job: `POST /jobs` runs the full pipeline
- Gemini 3.5 Flash labels claims
- Deterministic gate cannot be overridden by the model
- Cloud Run + Cloud Storage + Firestore
- Credential-free local dry-run and pytest

## Technologies

Gemini 3.5 Flash, Google ADK, Google GenAI SDK, Cloud Run, Cloud Storage, Firestore, FastAPI, Python 3.12

## Spin-up

See the repository README.
