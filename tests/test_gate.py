from night_clerk.gate import apply_gate


def test_rejects_mesh_as_validation():
    rec = apply_gate(
        "Mesh check passed so the CFD result is scientifically validated.",
        "calculated_or_simulated",
        [],
    )
    assert rec.action == "reject"
    assert rec.evidence == "unverified"


def test_holds_protected_literal():
    rec = apply_gate("Keep F_DEP unchanged in the manuscript.", "unverified", ["F_DEP"])
    assert rec.action == "hold"


def test_accepts_explicit_scenario():
    rec = apply_gate(
        "This stress case is a scenario_or_assumption, not a paper reproduction.",
        "scenario_or_assumption",
        [],
    )
    assert rec.action == "accept"
