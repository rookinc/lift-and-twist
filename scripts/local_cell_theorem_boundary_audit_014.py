#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

IN_011 = ROOT / "artifacts/json/lift_twist_local_answer_cell_generator_theorem_011.v1.json"
IN_012 = ROOT / "artifacts/json/lift_twist_anchor_node_path_geometry_012.v1.json"
IN_013 = ROOT / "artifacts/json/local_cell_theorem_section_013.v1.json"

MAIN = ROOT / "paper/main.tex"
SECTION = ROOT / "paper/sections/08_local_answer_cell_theorem.tex"

OUT_JSON = ROOT / "artifacts/json/local_cell_theorem_boundary_audit_014.v1.json"
OUT_NOTE = ROOT / "notes/local_cell_theorem_boundary_audit_014.md"


def load_json(path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def main():
    a011 = load_json(IN_011)
    a012 = load_json(IN_012)
    a013 = load_json(IN_013)

    main_text = MAIN.read_text(encoding="utf-8")
    section_text = SECTION.read_text(encoding="utf-8")

    required_phrases = [
        "four-state local answer-cell target",
        "state bits",
        "C row, anchor column, selected candidate",
        "closed anchor node path",
        "This theorem is local to the four-state reduced target",
        "does not yet derive the full reduced 16-candidate universe",
        "does not derive a full G60-native generator",
        "does not close Gap A",
    ]

    missing_required_phrases = [
        p for p in required_phrases if p not in section_text
    ]

    input_08 = "\\input{sections/08_local_answer_cell_theorem}"
    input_07 = "\\input{sections/07_conclusion}"

    main_has_08 = input_08 in main_text
    main_has_07 = input_07 in main_text

    if main_has_08 and main_has_07:
        section_before_conclusion = main_text.index(input_08) < main_text.index(input_07)
    else:
        section_before_conclusion = False

    forbidden_strong_claims = [
        "closes Gap A.",
        "closes Gap A",
        "Gap A is closed",
        "full G60-native generator is derived",
        "derives the full reduced 16-candidate universe",
    ]

    # Allow negated boundary language.
    forbidden_hits = []
    for phrase in forbidden_strong_claims:
        idx = section_text.find(phrase)
        if idx >= 0:
            window = section_text[max(0, idx - 40):idx + len(phrase) + 40]
            if "does not " not in window and "not " not in window:
                forbidden_hits.append(phrase)

    checks = {
        "project22_011_theorem_pass": bool(a011.get("theorem_pass")),
        "project22_012_theorem_pass": bool(a012.get("theorem_pass")),
        "project22_013_section_recorded": a013.get("status") == "local_cell_theorem_section_recorded",
        "main_has_local_cell_section": main_has_08,
        "main_has_conclusion": main_has_07,
        "local_cell_section_before_conclusion": section_before_conclusion,
        "required_boundary_phrases_present": len(missing_required_phrases) == 0,
        "forbidden_strong_claims_absent": len(forbidden_hits) == 0,
    }

    boundary_pass = all(checks.values())

    result = {
        "status": "local_cell_theorem_boundary_audit_recorded",
        "audit_id": "014",
        "inputs": {
            "011": str(IN_011),
            "012": str(IN_012),
            "013": str(IN_013),
            "main": str(MAIN),
            "section": str(SECTION),
        },
        "checks": checks,
        "missing_required_phrases": missing_required_phrases,
        "forbidden_hits": forbidden_hits,
        "boundary_pass": boundary_pass,
        "closed_statement": (
            "The paper now records a local Lift & Twist answer-cell theorem: within the four-state reduced target, "
            "the state bits generate the C row, anchor column, selected candidate, C key, anchor key, C path, "
            "C values, anchor residue set, overlap markers, and closed anchor node path."
        ),
        "open_boundary": (
            "The result remains local to the four-state reduced target. It does not derive the full reduced "
            "16-candidate universe from native G60 provenance, does not derive a full G60-native generator, "
            "and does not close Gap A."
        ),
    }

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_NOTE.parent.mkdir(parents=True, exist_ok=True)

    OUT_JSON.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    lines = []
    lines.append("# Local cell theorem boundary audit 014")
    lines.append("")
    lines.append("Status: " + result["status"])
    lines.append("")
    lines.append("## Closed statement")
    lines.append("")
    lines.append(result["closed_statement"])
    lines.append("")
    lines.append("## Open boundary")
    lines.append("")
    lines.append(result["open_boundary"])
    lines.append("")
    lines.append("## Checks")
    lines.append("")
    for k, v in checks.items():
        lines.append("- " + k + ": `" + str(v) + "`")
    lines.append("- boundary_pass: `" + str(boundary_pass) + "`")
    lines.append("")
    lines.append("## Missing required phrases")
    lines.append("")
    if missing_required_phrases:
        for p in missing_required_phrases:
            lines.append("- `" + p + "`")
    else:
        lines.append("- none")
    lines.append("")
    lines.append("## Forbidden strong-claim hits")
    lines.append("")
    if forbidden_hits:
        for p in forbidden_hits:
            lines.append("- `" + p + "`")
    else:
        lines.append("- none")
    lines.append("")

    OUT_NOTE.write_text("\n".join(lines), encoding="utf-8")

    print("wrote", OUT_JSON)
    print("wrote", OUT_NOTE)
    print("status", result["status"])
    print("boundary_pass", boundary_pass)
    for k, v in checks.items():
        print(k, v)


if __name__ == "__main__":
    main()
