#!/usr/bin/env python3
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

IN_006 = ROOT / "artifacts/json/lift_twist_local_answer_cell_target_006.v1.json"

OUT_JSON = ROOT / "artifacts/json/lift_twist_local_answer_cell_bit_law_007.v1.json"
OUT_CSV = ROOT / "artifacts/csv/lift_twist_local_answer_cell_bit_law_007.v1.csv"
OUT_NOTE = ROOT / "notes/lift_twist_local_answer_cell_bit_law_007.md"


def load_json(path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def state_bits(state):
    if state.startswith("O"):
        shell_bit = 0
    elif state.startswith("B"):
        shell_bit = 1
    else:
        raise ValueError("unknown state " + state)
    rank_bit = int(state[1:])
    return shell_bit, rank_bit


def mod15(x):
    return x % 15


def predict(shell_bit, rank_bit):
    b = shell_bit
    r = rank_bit

    # C readout rule:
    # ordinary shell first, branch shell second, rank ascending.
    c_row = 2 * b + r

    # Anchor twist rule:
    # B0 wraps to the front, ordinary ranks follow, B1 remains terminal.
    anchor_col = 1 + r + b * (2 * r - 1)

    # Candidate index in the 4x4 reduced universe.
    selected_candidate_index = 4 * c_row + anchor_col

    # Header key laws over Z15.
    # These are the compact two-bit formulas extracted from the 006 target table.
    c_key = mod15(11 + 6 * b + 2 * r)
    anchor_key = mod15(4 * b + 12 * r + 12 * b * r)

    return {
        "predicted_c_row": c_row,
        "predicted_anchor_col": anchor_col,
        "predicted_selected_candidate_index": selected_candidate_index,
        "predicted_c_key": c_key,
        "predicted_anchor_key": anchor_key,
    }


def main():
    a006 = load_json(IN_006)

    rows = []
    for src in a006["target_rows"]:
        state = src["state"]
        b, r = state_bits(state)
        pred = predict(b, r)

        row = {
            "state": state,
            "shell": src["shell"],
            "rank": int(src["rank"]),
            "shell_bit": b,
            "rank_bit": r,
            "observed_c_row": int(src["c_row"]),
            "observed_anchor_col": int(src["anchor_col"]),
            "observed_selected_candidate_index": int(src["selected_candidate_index"]),
            "observed_c_key": int(src["c_rank_key"]),
            "observed_anchor_key": int(src["anchor_rank_key"]),
            **pred,
        }

        row["c_row_match"] = row["observed_c_row"] == row["predicted_c_row"]
        row["anchor_col_match"] = row["observed_anchor_col"] == row["predicted_anchor_col"]
        row["selected_candidate_match"] = (
            row["observed_selected_candidate_index"]
            == row["predicted_selected_candidate_index"]
        )
        row["c_key_match"] = row["observed_c_key"] == row["predicted_c_key"]
        row["anchor_key_match"] = row["observed_anchor_key"] == row["predicted_anchor_key"]
        row["all_header_matches"] = (
            row["c_row_match"]
            and row["anchor_col_match"]
            and row["selected_candidate_match"]
            and row["c_key_match"]
            and row["anchor_key_match"]
        )
        rows.append(row)

    checks = {
        "all_c_rows_match": all(r["c_row_match"] for r in rows),
        "all_anchor_cols_match": all(r["anchor_col_match"] for r in rows),
        "all_selected_candidates_match": all(r["selected_candidate_match"] for r in rows),
        "all_c_keys_match": all(r["c_key_match"] for r in rows),
        "all_anchor_keys_match": all(r["anchor_key_match"] for r in rows),
        "all_header_matches": all(r["all_header_matches"] for r in rows),
        "project22_006_theorem_pass": bool(a006.get("theorem_pass")),
    }

    theorem_pass = all(checks.values())

    result = {
        "status": "lift_twist_local_answer_cell_bit_law_recorded",
        "audit_id": "007",
        "input": str(IN_006),
        "bit_encoding": {
            "ordinary_shell": 0,
            "branch_shell": 1,
            "rank": "0 or 1 from state suffix",
        },
        "laws": {
            "c_row": "2*b + r",
            "anchor_col": "1 + r + b*(2*r - 1)",
            "selected_candidate_index": "4*c_row + anchor_col",
            "c_key_mod15": "11 + 6*b + 2*r mod 15",
            "anchor_key_mod15": "4*b + 12*r + 12*b*r mod 15",
        },
        "rows": rows,
        "checks": checks,
        "theorem_pass": theorem_pass,
        "claim": (
            "The 006 local answer-cell target has an exact two-bit header law. With shell bit b "
            "(ordinary=0, branch=1) and rank bit r, the formulas c_row=2*b+r, "
            "anchor_col=1+r+b*(2*r-1), selected=4*c_row+anchor_col, "
            "c_key=11+6*b+2*r mod 15, and anchor_key=4*b+12*r+12*b*r mod 15 "
            "recover all observed C rows, anchor columns, selected candidate indices, C keys, "
            "and anchor keys."
        ),
        "boundary": (
            "This derives the local answer-cell header from a two-bit state law. It does not derive "
            "the full C payload paths, anchor residue sets, or the reduced 16-candidate universe from "
            "native provenance. It is not Gap A closure."
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
            "shell_bit",
            "rank_bit",
            "observed_c_row",
            "predicted_c_row",
            "observed_anchor_col",
            "predicted_anchor_col",
            "observed_selected_candidate_index",
            "predicted_selected_candidate_index",
            "observed_c_key",
            "predicted_c_key",
            "observed_anchor_key",
            "predicted_anchor_key",
            "all_header_matches",
        ])
        for r in rows:
            w.writerow([
                r["state"],
                r["shell_bit"],
                r["rank_bit"],
                r["observed_c_row"],
                r["predicted_c_row"],
                r["observed_anchor_col"],
                r["predicted_anchor_col"],
                r["observed_selected_candidate_index"],
                r["predicted_selected_candidate_index"],
                r["observed_c_key"],
                r["predicted_c_key"],
                r["observed_anchor_key"],
                r["predicted_anchor_key"],
                "1" if r["all_header_matches"] else "0",
            ])

    lines = []
    lines.append("# Lift & Twist local answer-cell bit law 007")
    lines.append("")
    lines.append("Status: " + result["status"])
    lines.append("")
    lines.append("## Claim")
    lines.append("")
    lines.append(result["claim"])
    lines.append("")
    lines.append("## Bit encoding")
    lines.append("")
    lines.append("- ordinary shell: `b=0`")
    lines.append("- branch shell: `b=1`")
    lines.append("- rank: `r=0 or r=1`")
    lines.append("")
    lines.append("## Laws")
    lines.append("")
    for k, v in result["laws"].items():
        lines.append("- " + k + ": `" + v + "`")
    lines.append("")
    lines.append("## Table")
    lines.append("")
    lines.append("| state | b | r | C row | anchor col | selected | C key | anchor key | match |")
    lines.append("|---|---:|---:|---:|---:|---:|---:|---:|---:|")
    for r in rows:
        lines.append(
            "| " + r["state"]
            + " | " + str(r["shell_bit"])
            + " | " + str(r["rank_bit"])
            + " | " + str(r["predicted_c_row"])
            + " | " + str(r["predicted_anchor_col"])
            + " | " + str(r["predicted_selected_candidate_index"])
            + " | " + str(r["predicted_c_key"])
            + " | " + str(r["predicted_anchor_key"])
            + " | " + ("1" if r["all_header_matches"] else "0")
            + " |"
        )
    lines.append("")
    lines.append("## Checks")
    lines.append("")
    for k, v in checks.items():
        lines.append("- " + k + ": `" + str(v) + "`")
    lines.append("- theorem_pass: `" + str(theorem_pass) + "`")
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
    for r in rows:
        print(
            r["state"],
            "b", r["shell_bit"],
            "r", r["rank_bit"],
            "c_row", r["predicted_c_row"],
            "anchor_col", r["predicted_anchor_col"],
            "selected", r["predicted_selected_candidate_index"],
            "c_key", r["predicted_c_key"],
            "anchor_key", r["predicted_anchor_key"],
            "match", r["all_header_matches"],
        )


if __name__ == "__main__":
    main()
