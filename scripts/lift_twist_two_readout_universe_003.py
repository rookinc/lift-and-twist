#!/usr/bin/env python3
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

IN_024 = ROOT / "source/project21_artifacts/json/sharedB_selection_matrix_024.v1.json"
IN_027 = ROOT / "source/project21_artifacts/json/native_shell_rank_derivation_027.v1.json"
IN_028 = ROOT / "source/project21_artifacts/json/reduced_universe_shell_rank_theorem_028.v1.json"
IN_002 = ROOT / "artifacts/json/lift_twist_coordinate_straightening_002.v1.json"

OUT_JSON = ROOT / "artifacts/json/lift_twist_two_readout_universe_003.v1.json"
OUT_CSV = ROOT / "artifacts/csv/lift_twist_two_readout_universe_003.v1.csv"
OUT_NOTE = ROOT / "notes/lift_twist_two_readout_universe_003.md"


def load_json(path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def state_name(shell, rank):
    return ("O" if shell == "ordinary" else "B") + str(rank)


def parse_rank_details(rank_details):
    out = {}
    for shell, rows in rank_details.items():
        for r in rows:
            idx = int(r["index"])
            rank = int(r["rank"])
            out[idx] = {
                "index": idx,
                "shell": shell,
                "rank": rank,
                "key": r["key"],
                "state": state_name(shell, rank),
            }
    return out


def main():
    a024 = load_json(IN_024)
    a027 = load_json(IN_027)
    a028 = load_json(IN_028)
    a002 = load_json(IN_002)

    c_state_by_row = parse_rank_details(a027["target_c_rank_details"])
    a_state_by_col = parse_rank_details(a027["target_anchor_rank_details"])

    c_readout = []
    for row in sorted(c_state_by_row):
        src = next(x for x in a024["c_rows"] if int(x["row_index"]) == row)
        c_readout.append({
            "kind": "C",
            "visible_index": row,
            "state": c_state_by_row[row]["state"],
            "shell": c_state_by_row[row]["shell"],
            "rank": c_state_by_row[row]["rank"],
            "rank_key": c_state_by_row[row]["key"],
            "payload": {
                "c_path": src["c_path"],
                "c_values": src["c_values"],
                "c_sum_mod15": src["c_sum_mod15"],
            },
        })

    anchor_readout = []
    for col in sorted(a_state_by_col):
        src = next(x for x in a024["anchor_cols"] if int(x["col_index"]) == col)
        anchor_readout.append({
            "kind": "anchor",
            "visible_index": col,
            "state": a_state_by_col[col]["state"],
            "shell": a_state_by_col[col]["shell"],
            "rank": a_state_by_col[col]["rank"],
            "rank_key": a_state_by_col[col]["key"],
            "payload": {
                "anchor_path": src["anchor_path"],
                "anchor_nodes": src["anchor_nodes"],
                "residues": src["residues"],
                "anchor_sum_mod15": src["anchor_sum_mod15"],
            },
        })

    candidate_index_matrix = a024["candidate_index_matrix"]
    selection_matrix = a024["selection_matrix"]

    generated = []
    generated_indices = []

    for c in c_readout:
        for a in anchor_readout:
            c_row = int(c["visible_index"])
            a_col = int(a["visible_index"])
            candidate_index = int(candidate_index_matrix[c_row][a_col])
            hidden_diagonal = c["state"] == a["state"]
            actual_selected = selection_matrix[c_row][a_col] == "S"

            generated_indices.append(candidate_index)
            generated.append({
                "candidate_index": candidate_index,
                "c_row": c_row,
                "a_col": a_col,
                "c_state": c["state"],
                "anchor_state": a["state"],
                "c_shell": c["shell"],
                "anchor_shell": a["shell"],
                "c_rank": c["rank"],
                "anchor_rank": a["rank"],
                "hidden_diagonal": hidden_diagonal,
                "actual_selected": actual_selected,
                "diagonal_matches_actual": hidden_diagonal == actual_selected,
                "c_payload": c["payload"],
                "anchor_payload": a["payload"],
            })

    generated_indices_sorted = sorted(generated_indices)
    expected_indices = list(range(16))

    diagonal_indices = sorted(x["candidate_index"] for x in generated if x["hidden_diagonal"])
    actual_selected_indices = sorted(x["candidate_index"] for x in generated if x["actual_selected"])

    universe_is_full_16 = generated_indices_sorted == expected_indices
    diagonal_matches_actual = diagonal_indices == actual_selected_indices
    all_rows_match = all(x["diagonal_matches_actual"] for x in generated)

    project21_actual = a028.get("conclusion", {}).get("actual_selected", [])
    project21_predicted = a028.get("conclusion", {}).get("predicted_selected", [])

    theorem_pass = (
        universe_is_full_16
        and diagonal_matches_actual
        and all_rows_match
        and bool(a002.get("theorem_pass"))
        and bool(a028.get("theorem_pass"))
    )

    result = {
        "status": "lift_twist_two_readout_universe_recorded",
        "audit_id": "003",
        "inputs": {
            "024": str(IN_024),
            "027": str(IN_027),
            "028": str(IN_028),
            "002": str(IN_002),
        },
        "c_readout_order": [x["state"] for x in c_readout],
        "anchor_readout_order": [x["state"] for x in anchor_readout],
        "c_readout": c_readout,
        "anchor_readout": anchor_readout,
        "generated_candidate_count": len(generated),
        "generated_indices_sorted": generated_indices_sorted,
        "expected_indices": expected_indices,
        "universe_is_full_16": universe_is_full_16,
        "hidden_diagonal_indices": diagonal_indices,
        "actual_selected_indices": actual_selected_indices,
        "diagonal_matches_actual": diagonal_matches_actual,
        "all_rows_match": all_rows_match,
        "project21_028_actual_selected": project21_actual,
        "project21_028_predicted_selected": project21_predicted,
        "project21_028_theorem_pass": bool(a028.get("theorem_pass")),
        "project22_002_theorem_pass": bool(a002.get("theorem_pass")),
        "theorem_pass": theorem_pass,
        "generated_universe": generated,
        "claim": (
            "The reduced 16-candidate universe can be represented as the product of two readouts "
            "of the same hidden four-state system. The C readout order is O0,O1,B0,B1. The anchor "
            "readout order is B0,O0,O1,B1. The hidden diagonal of this product is exactly the "
            "observed selected set [1,6,8,15]."
        ),
        "boundary": (
            "This proves a two-readout representation of the copied Project 21 reduced universe. "
            "It does not derive the two readouts from one local answer cell, does not derive the "
            "readout payloads natively, and does not close Gap A."
        ),
    }

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    OUT_NOTE.parent.mkdir(parents=True, exist_ok=True)

    OUT_JSON.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    with OUT_CSV.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow([
            "candidate_index",
            "c_row",
            "a_col",
            "c_state",
            "anchor_state",
            "c_shell",
            "anchor_shell",
            "c_rank",
            "anchor_rank",
            "hidden_diagonal",
            "actual_selected",
            "diagonal_matches_actual",
        ])
        for r in sorted(generated, key=lambda x: x["candidate_index"]):
            w.writerow([
                r["candidate_index"],
                r["c_row"],
                r["a_col"],
                r["c_state"],
                r["anchor_state"],
                r["c_shell"],
                r["anchor_shell"],
                r["c_rank"],
                r["anchor_rank"],
                "1" if r["hidden_diagonal"] else "0",
                "1" if r["actual_selected"] else "0",
                "1" if r["diagonal_matches_actual"] else "0",
            ])

    lines = []
    lines.append("# Lift & Twist two-readout universe 003")
    lines.append("")
    lines.append("Status: " + result["status"])
    lines.append("")
    lines.append("## Claim")
    lines.append("")
    lines.append(result["claim"])
    lines.append("")
    lines.append("## Readouts")
    lines.append("")
    lines.append("- C readout order: `" + str(result["c_readout_order"]) + "`")
    lines.append("- anchor readout order: `" + str(result["anchor_readout_order"]) + "`")
    lines.append("")
    lines.append("## Checks")
    lines.append("")
    lines.append("- generated_candidate_count: `" + str(result["generated_candidate_count"]) + "`")
    lines.append("- universe_is_full_16: `" + str(result["universe_is_full_16"]) + "`")
    lines.append("- hidden_diagonal_indices: `" + str(result["hidden_diagonal_indices"]) + "`")
    lines.append("- actual_selected_indices: `" + str(result["actual_selected_indices"]) + "`")
    lines.append("- diagonal_matches_actual: `" + str(result["diagonal_matches_actual"]) + "`")
    lines.append("- all_rows_match: `" + str(result["all_rows_match"]) + "`")
    lines.append("- theorem_pass: `" + str(result["theorem_pass"]) + "`")
    lines.append("")
    lines.append("## Generated universe")
    lines.append("")
    lines.append("| candidate | C state | anchor state | hidden diagonal | actual selected |")
    lines.append("|---:|---|---|---:|---:|")
    for r in sorted(generated, key=lambda x: x["candidate_index"]):
        lines.append(
            "| " + str(r["candidate_index"])
            + " | " + r["c_state"]
            + " | " + r["anchor_state"]
            + " | " + ("1" if r["hidden_diagonal"] else "0")
            + " | " + ("1" if r["actual_selected"] else "0")
            + " |"
        )
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
    print("c_readout_order", result["c_readout_order"])
    print("anchor_readout_order", result["anchor_readout_order"])
    print("generated_candidate_count", len(generated))
    print("universe_is_full_16", universe_is_full_16)
    print("hidden_diagonal_indices", diagonal_indices)
    print("actual_selected_indices", actual_selected_indices)
    print("diagonal_matches_actual", diagonal_matches_actual)


if __name__ == "__main__":
    main()
