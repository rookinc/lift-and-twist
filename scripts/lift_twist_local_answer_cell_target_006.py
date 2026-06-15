#!/usr/bin/env python3
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

IN_003 = ROOT / "artifacts/json/lift_twist_two_readout_universe_003.v1.json"
IN_005 = ROOT / "artifacts/json/lift_twist_payload_state_reconstruction_005.v1.json"

OUT_JSON = ROOT / "artifacts/json/lift_twist_local_answer_cell_target_006.v1.json"
OUT_CSV = ROOT / "artifacts/csv/lift_twist_local_answer_cell_target_006.v1.csv"
OUT_NOTE = ROOT / "notes/lift_twist_local_answer_cell_target_006.md"


def load_json(path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def as_int_set(x):
    out = set()

    def rec(v):
        if isinstance(v, int):
            out.add(v)
        elif isinstance(v, list):
            for y in v:
                rec(y)
        elif isinstance(v, dict):
            for y in v.values():
                rec(y)

    rec(x)
    return sorted(out)


def main():
    a003 = load_json(IN_003)
    a005 = load_json(IN_005)

    c_by_state = {}
    for row in a005["c_rows"]:
        c_by_state[row["derived_state"]] = row

    anchor_by_state = {}
    for col in a005["anchor_cols"]:
        anchor_by_state[col["derived_state"]] = col

    selected_by_state = {}
    for row in a003["generated_universe"]:
        if bool(row["actual_selected"]):
            selected_by_state[row["c_state"]] = row

    state_order = ["O0", "O1", "B0", "B1"]

    target_rows = []
    for state in state_order:
        c = c_by_state[state]
        a = anchor_by_state[state]
        selected = selected_by_state[state]

        c_payload = c["payload"]
        a_payload = a["payload"]

        c_values = as_int_set(c_payload.get("c_values", []))
        anchor_residues = as_int_set(a_payload.get("residues", []))
        overlap = sorted(set(c_values).intersection(anchor_residues))

        target_rows.append({
            "state": state,
            "shell": c["derived_shell"],
            "rank": int(c["derived_rank"]),
            "selected_candidate_index": int(selected["candidate_index"]),
            "c_row": int(c["visible_index"]),
            "anchor_col": int(a["visible_index"]),
            "c_rank_key": int(c["rank_key"]),
            "anchor_rank_key": int(a["rank_key"]),
            "c_values": c_values,
            "anchor_residues": anchor_residues,
            "c_anchor_value_overlap": overlap,
            "overlap_count": len(overlap),
            "c_payload": c_payload,
            "anchor_payload": a_payload,
        })

    branch_states = [r["state"] for r in target_rows if r["shell"] == "branch"]
    ordinary_states = [r["state"] for r in target_rows if r["shell"] == "ordinary"]

    selected_indices = [r["selected_candidate_index"] for r in target_rows]
    c_rows = [r["c_row"] for r in target_rows]
    anchor_cols = [r["anchor_col"] for r in target_rows]

    checks = {
        "state_order_matches_expected": [r["state"] for r in target_rows] == state_order,
        "selected_indices_match_expected": selected_indices == [1, 6, 8, 15],
        "c_rows_match_expected": c_rows == [0, 1, 2, 3],
        "anchor_cols_match_expected": anchor_cols == [1, 2, 0, 3],
        "ordinary_states_match_expected": ordinary_states == ["O0", "O1"],
        "branch_states_match_expected": branch_states == ["B0", "B1"],
        "project22_003_theorem_pass": bool(a003.get("theorem_pass")),
        "project22_005_theorem_pass": bool(a005.get("theorem_pass")),
    }

    theorem_pass = all(checks.values())

    result = {
        "status": "lift_twist_local_answer_cell_target_recorded",
        "audit_id": "006",
        "inputs": {
            "003": str(IN_003),
            "005": str(IN_005),
        },
        "state_order": state_order,
        "target_rows": target_rows,
        "selected_candidate_indices": selected_indices,
        "c_rows": c_rows,
        "anchor_cols": anchor_cols,
        "ordinary_states": ordinary_states,
        "branch_states": branch_states,
        "checks": checks,
        "theorem_pass": theorem_pass,
        "claim": (
            "The Project 22 reduced Lift & Twist data can be consolidated into one four-state local "
            "answer-cell target. Each hidden state has one C readout payload, one anchor readout payload, "
            "and one selected diagonal candidate. This target table is the object a stronger native "
            "generator must derive."
        ),
        "boundary": (
            "This is a target-table construction, not a native derivation. It organizes the payloads "
            "that must be generated from one local answer cell, but it does not yet derive those payloads "
            "or close Gap A."
        ),
    }

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    OUT_NOTE.parent.mkdir(parents=True, exist_ok=True)

    OUT_JSON.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    with OUT_CSV.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow([
            "state",
            "shell",
            "rank",
            "selected_candidate_index",
            "c_row",
            "anchor_col",
            "c_rank_key",
            "anchor_rank_key",
            "c_values",
            "anchor_residues",
            "c_anchor_value_overlap",
            "overlap_count",
        ])
        for r in target_rows:
            w.writerow([
                r["state"],
                r["shell"],
                r["rank"],
                r["selected_candidate_index"],
                r["c_row"],
                r["anchor_col"],
                r["c_rank_key"],
                r["anchor_rank_key"],
                " ".join(str(x) for x in r["c_values"]),
                " ".join(str(x) for x in r["anchor_residues"]),
                " ".join(str(x) for x in r["c_anchor_value_overlap"]),
                r["overlap_count"],
            ])

    lines = []
    lines.append("# Lift & Twist local answer-cell target 006")
    lines.append("")
    lines.append("Status: " + result["status"])
    lines.append("")
    lines.append("## Claim")
    lines.append("")
    lines.append(result["claim"])
    lines.append("")
    lines.append("## Target table")
    lines.append("")
    lines.append("| state | shell | rank | selected | C row | anchor col | C key | anchor key | overlap |")
    lines.append("|---|---|---:|---:|---:|---:|---:|---:|---|")
    for r in target_rows:
        overlap = " ".join(str(x) for x in r["c_anchor_value_overlap"])
        if not overlap:
            overlap = "none"
        lines.append(
            "| " + r["state"]
            + " | " + r["shell"]
            + " | " + str(r["rank"])
            + " | " + str(r["selected_candidate_index"])
            + " | " + str(r["c_row"])
            + " | " + str(r["anchor_col"])
            + " | " + str(r["c_rank_key"])
            + " | " + str(r["anchor_rank_key"])
            + " | " + overlap
            + " |"
        )
    lines.append("")
    lines.append("## Checks")
    lines.append("")
    for k, v in checks.items():
        lines.append("- " + k + ": `" + str(v) + "`")
    lines.append("- theorem_pass: `" + str(theorem_pass) + "`")
    lines.append("")
    lines.append("## Interpretation")
    lines.append("")
    lines.append("This artifact turns the Lift & Twist representation into a concrete generator target.")
    lines.append("The next problem is no longer to name the four states. The next problem is to derive their payloads.")
    lines.append("")
    lines.append("## Boundary")
    lines.append("")
    lines.append(result["boundary"])
    lines.append("")

    OUT_NOTE.write_text("\n".join(lines), encoding="utf-8")

    print("wrote", OUT_JSON)
    print("wrote", OUT_CSV)
    print("wrote", OUT_NOTE)
    print("status", result["status"])
    print("theorem_pass", theorem_pass)
    print("selected_candidate_indices", selected_indices)
    print("c_rows", c_rows)
    print("anchor_cols", anchor_cols)
    print("ordinary_states", ordinary_states)
    print("branch_states", branch_states)


if __name__ == "__main__":
    main()
