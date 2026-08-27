from __future__ import annotations

import json
import os
import re

from night_clerk.gate import default_label
from night_clerk.schema import EvidenceLabel

_JSON_BLOCK = re.compile(r"\{.*\}", re.DOTALL)


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


def label_with_gemini(text: str, model: str) -> EvidenceLabel:
    from google import genai

    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
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


def label_claim(text: str, model: str, allow_model: bool) -> tuple[EvidenceLabel, str]:
    if allow_model and os.getenv("GEMINI_API_KEY"):
        return label_with_gemini(text, model), model
    return default_label(text), "not-run"
