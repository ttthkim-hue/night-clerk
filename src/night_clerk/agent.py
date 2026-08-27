"""Google ADK agent for Night Clerk.

The agent is not a chatbot. Tools exist so the model can run the overnight
inbox workflow: load a packet, label claims, apply the gate, write a receipt.
The Python orchestrator in `pipeline.py` is the source of truth and can run
without the ADK runtime.
"""

from __future__ import annotations

import json
import os
from pathlib import Path

from night_clerk.pipeline import run_packet_file
from night_clerk.storage import build_storage


def run_night_shift(packet_path: str) -> str:
    """Run the full Night Clerk workflow on one inbox packet and write a receipt.

    Args:
        packet_path: Path to a JSON inbox packet.

    Returns:
        JSON string of the written receipt.
    """
    receipt = run_packet_file(packet_path, storage=build_storage())
    return receipt.model_dump_json(indent=2)


def list_fixture_packets() -> str:
    """List bundled public-safe inbox fixtures.

    Returns:
        JSON array of fixture paths.
    """
    root = Path(__file__).resolve().parents[2] / "fixtures" / "inbox"
    files = sorted(str(p) for p in root.glob("*.json"))
    return json.dumps(files)


def build_root_agent():
    from google.adk.agents import Agent

    model = os.getenv("NIGHT_CLERK_MODEL", "gemini-3.5-flash")
    return Agent(
        name="night_clerk",
        model=model,
        description="Overnight research-inbox clerk that writes evidence receipts.",
        instruction=(
            "You are Night Clerk. Do not chat. Do not invent numbers. "
            "Call list_fixture_packets if the user did not give a path. "
            "Then call run_night_shift on one packet. Return the receipt JSON."
        ),
        tools=[list_fixture_packets, run_night_shift],
    )


try:
    root_agent = build_root_agent()
except Exception:  # pragma: no cover - ADK optional for local tests
    root_agent = None
