#!/usr/bin/env python3
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

IN_024 = ROOT / "source/project21_artifacts/json/sharedB_selection_matrix_024.v1.json"
IN_026 = ROOT / "source/project21_artifacts/json/native_shell_label_derivation_026.v1.json"
IN_027 = ROOT / "source/project21_artifacts/json/native_shell_rank_derivation_027.v1.json"
IN_028 = ROOT / "source/project21_artifacts/json/reduced_universe_shell_rank_theorem_028.v1.json"

OUT_JSON = ROOT / "artifacts/json/lift_twist_coordinate_straightening_002.v1.json"
OUT_CSV = ROOT / "artifacts/csv/lift_twist_coordinate_straightening_002.v1.csv"
OUT_NOTE = ROOT / "notes/lift_twist_coordinate_straightening_002.md"


def load_json(path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def state_name(shell, rank):
    prefix = "O" if shell == "ordinary" else "B"
    return prefix + str(rank)


def parse_rank_details(rank_details):
    out = {}
    for shell, rows in rank_details.items():
        for r in rows:
            idx = int(r["index"])
            out[idx] = {
                "shell": shell,
                "rank": int(r["rank"]),
                "key": r["key"],
                "state": state_name(shell, int(r["rank"])),
            }
    return out


def permutation_cycles(mapping):
    seen = set()
    cycles = []
    for start in sorted(mapping):
        if start in seen:
            continue
        cur = start
        cyc = []
        while cur not in seen:
            seen.add(cur)
            cyc.append(cur)
            cur = mapping[cur]
        cycles.append(cyc)
    return cycles


def main():
    a024 = load_json(IN_024)
    a026 = load_json(IN_026)
    a027 = load_json(IN_027)
    a028 = load_json(IN_028)

    visible_selected = {int(k): int(v) for k, v in a024["selected_col_by_row"].items()}

    c_state_by_row = parse_rank_details(a027["target_c_rank_details"])
    a_state_by_col = parse_rank_details(a027["target_anchor_rank_details"])

    c_readout_order = []
    for i in sorted(c_state_by_row):
        c_readout_order.append(c_state_by_row[i]["state"])

    anchor_readout_order = []
    for j in sorted(a_state_by_col):
        anchor_readout_order.append(a_state_by_col[j]["state"])

    anchor_col_by_state = {}
    for col, data in a_state_by_col.items():
        anchor_col_by_state[data["state"]] = col

    induced_visible_permutation = {}
    straightening_rows = []

    for row in sorted(c_state_by_row):
        c_state = c_state_by_row[row]["state"]
        induced_col = anchor_col_by_state[c_state]
        visible_col = visible_selected[row]
        anchor_state = a_state_by_col[visible_col]["state"]

        induced_visible_permutation[row] = induced_col

        straightening_rows.append({
            "c_row": row,
            "visible_selected_col": visible_col,
            "induced_col_from_hidden_identity": induced_col,
            "c_shell": c_state_by_row[row]["shell"],
            "c_rank": c_state_by_row[row]["rank"],
            "c_state": c_state,
            "anchor_shell": a_state_by_col[visible_col]["shell"],
            "anchor_rank": a_state_by_col[visible_col]["rank"],
            "anchor_state": anchor_state,
            "hidden_identity_match": c_state == anchor_state,
            "visible_matches_induced": visible_col == induced_col,
        })

    induced_list = [induced_visible_permutation[i] for i in sorted(induced_visible_permutation)]
    visible_list = [visible_selected[i] for i in sorted(visible_selected)]

    hidden_identity_all_match = all(r["hidden_identity_match"] for r in straightening_rows)
    visible_matches_induced = all(r["visible_matches_induced"] for r in straightening_rows)
    readout_state_sets_match = set(c_readout_order) == set(anchor_readout_order)

    cycles = permutation_cycles(induced_visible_permutation)

    actual_028 = a028.get("conclusion", {}).get("actual_selected", [])
    predicted_028 = a028.get("conclusion", {}).get("predicted_selected", [])

    theorem_pass = (
        hidden_identity_all_match
        and visible_matches_induced
        and readout_state_sets_match
        and visible_list == induced_list
        and bool(a028.get("theorem_pass"))
    )

    result = {
        "status": "lift_twist_coordinate_straightening_recorded",
        "audit_id": "002",
        "inputs": {
            "024": str(IN_024),
            "026": str(IN_026),
            "027": str(IN_027),
            "028": str(IN_028),
        },
        "visible_selected_col_by_row": {str(k): v for k, v in sorted(visible_selected.items())},
        "visible_permutation_list": visible_list,
        "c_readout_order": c_readout_order,
        "anchor_readout_order": anchor_readout_order,
        "induced_visible_permutation": {str(k): v for k, v in sorted(induced_visible_permutation.items())},
        "induced_visible_permutation_list": induced_list,
        "permutation_cycles": cycles,
        "hidden_identity_all_match": hidden_identity_all_match,
        "visible_matches_induced": visible_matches_induced,
        "readout_state_sets_match": readout_state_sets_match,
        "project21_028_theorem_pass": bool(a028.get("theorem_pass")),
        "project21_028_actual_selected": actual_028,
        "project21_028_predicted_selected": predicted_028,
        "theorem_pass": theorem_pass,
        "straightening_rows": straightening_rows,
        "claim": (
            "The visible selector permutation [1,2,0,3] is induced by identity in lifted "
            "shell/rank coordinates. The C readout orders hidden states as O0,O1,B0,B1; "
            "the anchor readout orders the same states as B0,O0,O1,B1. Therefore the hidden "
            "identity map appears visibly as [1,2,0,3] = (0 1 2)(3)."
        ),
        "boundary": (
            "This proves coordinate straightening for the copied Project 21 reduced universe. "
            "It does not derive the reduced 16-candidate universe itself and does not close Gap A."
        ),
    }

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    OUT_NOTE.parent.mkdir(parents=True, exist_ok=True)

    OUT_JSON.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    with OUT_CSV.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow([
            "c_row",
            "visible_selected_col",
            "induced_col_from_hidden_identity",
            "c_state",
            "anchor_state",
            "c_shell",
            "anchor_shell",
            "c_rank",
            "anchor_rank",
            "hidden_identity_match",
            "visible_matches_induced",
        ])
        for r in straightening_rows:
            w.writerow([
                r["c_row"],
                r["visible_selected_col"],
                r["induced_col_from_hidden_identity"],
                r["c_state"],
                r["anchor_state"],
                r["c_shell"],
                r["anchor_shell"],
                r["c_rank"],
                r["anchor_rank"],
                "1" if r["hidden_identity_match"] else "0",
                "1" if r["visible_matches_induced"] else "0",
            ])

    lines = []
    lines.append("# Lift & Twist coordinate straightening 002")
    lines.append("")
    lines.append("Status: " + result["status"])
    lines.append("")
    lines.append("## Claim")
    lines.append("")
    lines.append(result["claim"])
    lines.append("")
    lines.append("## Readout orders")
    lines.append("")
    lines.append("- C readout order: `" + str(c_readout_order) + "`")
    lines.append("- anchor readout order: `" + str(anchor_readout_order) + "`")
    lines.append("")
    lines.append("## Visible selector")
    lines.append("")
    lines.append("- visible_selected_col_by_row: `" + str(result["visible_selected_col_by_row"]) + "`")
    lines.append("- visible_permutation_list: `" + str(visible_list) + "`")
    lines.append("- induced_visible_permutation_list: `" + str(induced_list) + "`")
    lines.append("- permutation_cycles: `" + str(cycles) + "`")
    lines.append("")
    lines.append("## Checks")
    lines.append("")
    lines.append("- readout_state_sets_match: `" + str(readout_state_sets_match) + "`")
    lines.append("- hidden_identity_all_match: `" + str(hidden_identity_all_match) + "`")
    lines.append("- visible_matches_induced: `" + str(visible_matches_induced) + "`")
    lines.append("- project21_028_theorem_pass: `" + str(bool(a028.get("theorem_pass"))) + "`")
    lines.append("- theorem_pass: `" + str(theorem_pass) + "`")
    lines.append("")
    lines.append("## Straightening rows")
    lines.append("")
    for r in straightening_rows:
        lines.append("- row `" + str(r["c_row"]) + "` -> col `" + str(r["visible_selected_col"]) + "`")
        lines.append("  - c_state: `" + r["c_state"] + "`")
        lines.append("  - anchor_state: `" + r["anchor_state"] + "`")
        lines.append("  - hidden_identity_match: `" + str(r["hidden_identity_match"]) + "`")
        lines.append("  - visible_matches_induced: `" + str(r["visible_matches_induced"]) + "`")
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
    print("c_readout_order", c_readout_order)
    print("anchor_readout_order", anchor_readout_order)
    print("visible_permutation_list", visible_list)
    print("induced_visible_permutation_list", induced_list)
    print("permutation_cycles", cycles)


if __name__ == "__main__":
    main()
