from __future__ import annotations

import json
import os
import re

from night_clerk.gate import default_label
from night_clerk.schema import EvidenceLabel

_JSON_BLOCK = re.compile(r"\{.*\}", re.DOTALL)
_TRUTHY = {"1", "true", "yes", "on"}


def _parse_label(raw: str) -> EvidenceLabel | None:
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        match = _JSON_BLOCK.search(raw)
        if not match:
            return None
        try:
            data = json.loads(match.group(0))
        except json.JSONDecodeError:
            return None
    label = data.get("evidence")
    allowed = {
        "measured_internal",
        "calculated_or_simulated",
        "literature_reported",
        "interpolated_or_fitted",
        "scenario_or_assumption",
        "unverified",
    }
    if label in allowed:
        return label
    return None


def _vertex_enabled() -> bool:
    return os.getenv("GOOGLE_GENAI_USE_VERTEXAI", "").strip().lower() in _TRUTHY


def _gemini_transport_configured() -> bool:
    if os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY"):
        return True
    return _vertex_enabled() and bool(os.getenv("GOOGLE_CLOUD_PROJECT"))


def _build_genai_client():
    from google import genai

    if _vertex_enabled():
        project = os.environ["GOOGLE_CLOUD_PROJECT"]
        location = os.getenv("GOOGLE_CLOUD_LOCATION", "global")
        return genai.Client(vertexai=True, project=project, location=location)

    api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("Gemini transport is not configured")
    return genai.Client(api_key=api_key)


def label_with_gemini(text: str, model: str) -> EvidenceLabel:
    client = _build_genai_client()
    try:
        prompt = (
            "Return JSON only: {\"evidence\": <one label>}.\n"
            "Labels: measured_internal, calculated_or_simulated, literature_reported, "
            "interpolated_or_fitted, scenario_or_assumption, unverified.\n"
            "Never invent a number. If the sentence claims validation from a smoke test, "
            "mesh check, compile, or image render, use unverified.\n"
            f"Sentence: {text}"
        )
        response = client.models.generate_content(model=model, contents=prompt)
        raw = getattr(response, "text", None) or str(response)
        parsed = _parse_label(raw)
        return parsed or "unverified"
    finally:
        close = getattr(client, "close", None)
        if close:
            close()


def label_claim(text: str, model: str, allow_model: bool) -> tuple[EvidenceLabel, str]:
    if allow_model:
        if not _gemini_transport_configured():
            raise RuntimeError(
                "NIGHT_CLERK_MODE enables model execution, but Gemini is not configured. "
                "Set GOOGLE_GENAI_USE_VERTEXAI=true with GOOGLE_CLOUD_PROJECT, or provide "
                "GEMINI_API_KEY/GOOGLE_API_KEY."
            )
        return label_with_gemini(text, model), model
    return default_label(text), "not-run"
