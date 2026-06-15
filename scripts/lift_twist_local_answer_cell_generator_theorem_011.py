#!/usr/bin/env python3
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

IN_006 = ROOT / "artifacts/json/lift_twist_local_answer_cell_target_006.v1.json"
IN_007 = ROOT / "artifacts/json/lift_twist_local_answer_cell_bit_law_007.v1.json"
IN_008 = ROOT / "artifacts/json/lift_twist_payload_overlap_marker_law_008.v1.json"
IN_009 = ROOT / "artifacts/json/lift_twist_c_payload_path_law_009.v1.json"
IN_010 = ROOT / "artifacts/json/lift_twist_anchor_residue_set_law_010.v1.json"

OUT_JSON = ROOT / "artifacts/json/lift_twist_local_answer_cell_generator_theorem_011.v1.json"
OUT_CSV = ROOT / "artifacts/csv/lift_twist_local_answer_cell_generator_theorem_011.v1.csv"
OUT_NOTE = ROOT / "notes/lift_twist_local_answer_cell_generator_theorem_011.md"


def load_json(path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def mod15(x):
    return x % 15


def state_name(b, r):
    return ("O" if b == 0 else "B") + str(r)


def c_row_law(b, r):
    return 2 * b + r


def anchor_col_law(b, r):
    return 1 + r + b * (2 * r - 1)


def selected_candidate_law(b, r):
    return 4 * c_row_law(b, r) + anchor_col_law(b, r)


def c_key_law(b, r):
    return mod15(11 + 6 * b + 2 * r)


def anchor_key_law(b, r):
    return mod15(4 * b + 12 * r + 12 * b * r)


def c_offsets_law(b, r):
    d1 = mod15(6 - 3 * b - 3 * r + b * r)
    d2 = mod15((1 - b) * (3 + 9 * r) + 13 * b)
    return [0, d1, d2, 0]


def c_payload_law(b, r):
    k = c_key_law(b, r)
    offsets = c_offsets_law(b, r)
    path = [mod15(k + d) for d in offsets]
    values = sorted(set(path))
    return offsets, path, values


def ordinary_offsets(r):
    shared = {5, 7, 12}
    switched = {
        1 + 3 * (1 - r),
        2 + 6 * (1 - r),
        3 + 6 * (1 - r),
    }
    return shared | switched


def branch_offsets(r):
    shared = {0, 4}
    switched = {
        mod15(11 - 6 * r),
        mod15(13 - 4 * r),
        mod15(14 - 4 * r),
    }
    terminal = {12} if r == 1 else set()
    return shared | switched | terminal


def anchor_offsets_law(b, r):
    if b == 0:
        return sorted(ordinary_offsets(r))
    return sorted(branch_offsets(r))


def anchor_residue_law(b, r):
    key = anchor_key_law(b, r)
    offsets = anchor_offsets_law(b, r)
    residues = sorted({mod15(key + d) for d in offsets})
    return offsets, residues


def generate_state(b, r):
    c_offsets, c_path, c_values = c_payload_law(b, r)
    anchor_offsets, anchor_residues = anchor_residue_law(b, r)
    overlap = sorted(set(c_values).intersection(anchor_residues))
    return {
        "state": state_name(b, r),
        "shell": "ordinary" if b == 0 else "branch",
        "rank": r,
        "shell_bit": b,
        "rank_bit": r,
        "c_row": c_row_law(b, r),
        "anchor_col": anchor_col_law(b, r),
        "selected_candidate_index": selected_candidate_law(b, r),
        "c_key": c_key_law(b, r),
        "anchor_key": anchor_key_law(b, r),
        "c_offsets": c_offsets,
        "c_path": c_path,
        "c_values": c_values,
        "anchor_offsets": anchor_offsets,
        "anchor_residues": anchor_residues,
        "overlap": overlap,
        "overlap_count": len(overlap),
    }


def normalize_target_row(row):
    return {
        "state": row["state"],
        "shell": row["shell"],
        "rank": int(row["rank"]),
        "c_row": int(row["c_row"]),
        "anchor_col": int(row["anchor_col"]),
        "selected_candidate_index": int(row["selected_candidate_index"]),
        "c_key": int(row["c_rank_key"]),
        "anchor_key": int(row["anchor_rank_key"]),
        "c_values": sorted(int(x) for x in row["c_values"]),
        "anchor_residues": sorted(int(x) for x in row["anchor_residues"]),
        "overlap": sorted(int(x) for x in row["c_anchor_value_overlap"]),
        "overlap_count": int(row["overlap_count"]),
    }


def compare(generated, observed):
    checks = {
        "state": generated["state"] == observed["state"],
        "shell": generated["shell"] == observed["shell"],
        "rank": generated["rank"] == observed["rank"],
        "c_row": generated["c_row"] == observed["c_row"],
        "anchor_col": generated["anchor_col"] == observed["anchor_col"],
        "selected_candidate_index": generated["selected_candidate_index"] == observed["selected_candidate_index"],
        "c_key": generated["c_key"] == observed["c_key"],
        "anchor_key": generated["anchor_key"] == observed["anchor_key"],
        "c_values": generated["c_values"] == observed["c_values"],
        "anchor_residues": generated["anchor_residues"] == observed["anchor_residues"],
        "overlap": generated["overlap"] == observed["overlap"],
        "overlap_count": generated["overlap_count"] == observed["overlap_count"],
    }
    return checks


def main():
    a006 = load_json(IN_006)
    a007 = load_json(IN_007)
    a008 = load_json(IN_008)
    a009 = load_json(IN_009)
    a010 = load_json(IN_010)

    generated_rows = []
    for b, r in [(0, 0), (0, 1), (1, 0), (1, 1)]:
        generated_rows.append(generate_state(b, r))

    observed_by_state = {
        row["state"]: normalize_target_row(row)
        for row in a006["target_rows"]
    }

    comparison_rows = []
    for gen in generated_rows:
        obs = observed_by_state[gen["state"]]
        field_checks = compare(gen, obs)
        comparison_rows.append({
            "state": gen["state"],
            "generated": gen,
            "observed": obs,
            "field_checks": field_checks,
            "all_fields_match": all(field_checks.values()),
        })

    selected_candidate_indices = [r["selected_candidate_index"] for r in generated_rows]
    c_rows = [r["c_row"] for r in generated_rows]
    anchor_cols = [r["anchor_col"] for r in generated_rows]
    overlap_signatures = {r["state"]: r["overlap"] for r in generated_rows}

    checks = {
        "all_generated_rows_match_006_target": all(r["all_fields_match"] for r in comparison_rows),
        "selected_candidates_match_expected": selected_candidate_indices == [1, 6, 8, 15],
        "c_rows_match_expected": c_rows == [0, 1, 2, 3],
        "anchor_cols_match_expected": anchor_cols == [1, 2, 0, 3],
        "overlap_signatures_match_expected": overlap_signatures == {
            "O0": [],
            "O1": [13],
            "B0": [0, 2],
            "B1": [2],
        },
        "project22_006_theorem_pass": bool(a006.get("theorem_pass")),
        "project22_007_theorem_pass": bool(a007.get("theorem_pass")),
        "project22_008_theorem_pass": bool(a008.get("theorem_pass")),
        "project22_009_theorem_pass": bool(a009.get("theorem_pass")),
        "project22_010_theorem_pass": bool(a010.get("theorem_pass")),
    }

    theorem_pass = all(checks.values())

    result = {
        "status": "lift_twist_local_answer_cell_generator_theorem_recorded",
        "audit_id": "011",
        "inputs": {
            "006": str(IN_006),
            "007": str(IN_007),
            "008": str(IN_008),
            "009": str(IN_009),
            "010": str(IN_010),
        },
        "generator_domain": [
            {"state": "O0", "b": 0, "r": 0},
            {"state": "O1", "b": 0, "r": 1},
            {"state": "B0", "b": 1, "r": 0},
            {"state": "B1", "b": 1, "r": 1},
        ],
        "laws": {
            "c_row": "2*b + r",
            "anchor_col": "1 + r + b*(2*r - 1)",
            "selected_candidate_index": "4*c_row + anchor_col",
            "c_key": "11 + 6*b + 2*r mod 15",
            "anchor_key": "4*b + 12*r + 12*b*r mod 15",
            "c_offsets": "[0, 6-3*b-3*r+b*r, (1-b)*(3+9*r)+13*b, 0] mod 15",
            "c_path": "[c_key + offset mod 15 for offset in c_offsets]",
            "anchor_offsets": "ordinary and branch offset laws from 010",
            "anchor_residues": "[anchor_key + offset mod 15 for offset in anchor_offsets]",
            "overlap": "intersection(c_values, anchor_residues)",
        },
        "generated_rows": generated_rows,
        "comparison_rows": comparison_rows,
        "selected_candidate_indices": selected_candidate_indices,
        "checks": checks,
        "theorem_pass": theorem_pass,
        "claim": (
            "The four-state local answer-cell target from 006 is generated from the two bits b,r by "
            "the consolidated Lift & Twist laws from 007-010. The generator reproduces the C row, "
            "anchor column, selected candidate, C key, anchor key, C path values, anchor residue set, "
            "and overlap markers for O0,O1,B0,B1."
        ),
        "boundary": (
            "This is a theorem for the four-state local answer-cell target. It still does not derive "
            "the anchor node paths themselves, does not derive the full reduced 16-candidate universe "
            "from native G60 provenance, and does not close Gap A."
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
            "b",
            "r",
            "c_row",
            "anchor_col",
            "selected",
            "c_key",
            "anchor_key",
            "c_path",
            "c_values",
            "anchor_residues",
            "overlap",
            "all_fields_match",
        ])
        for row in comparison_rows:
            gen = row["generated"]
            w.writerow([
                gen["state"],
                gen["shell_bit"],
                gen["rank_bit"],
                gen["c_row"],
                gen["anchor_col"],
                gen["selected_candidate_index"],
                gen["c_key"],
                gen["anchor_key"],
                " ".join(str(x) for x in gen["c_path"]),
                " ".join(str(x) for x in gen["c_values"]),
                " ".join(str(x) for x in gen["anchor_residues"]),
                " ".join(str(x) for x in gen["overlap"]) or "none",
                "1" if row["all_fields_match"] else "0",
            ])

    lines = []
    lines.append("# Lift & Twist local answer-cell generator theorem 011")
    lines.append("")
    lines.append("Status: " + result["status"])
    lines.append("")
    lines.append("## Claim")
    lines.append("")
    lines.append(result["claim"])
    lines.append("")
    lines.append("## Generated table")
    lines.append("")
    lines.append("| state | b | r | C row | anchor col | selected | C key | anchor key | C path | C values | anchor residues | overlap | match |")
    lines.append("|---|---:|---:|---:|---:|---:|---:|---:|---|---|---|---|---:|")
    for row in comparison_rows:
        gen = row["generated"]
        overlap = " ".join(str(x) for x in gen["overlap"]) or "none"
        lines.append(
            "| " + gen["state"]
            + " | " + str(gen["shell_bit"])
            + " | " + str(gen["rank_bit"])
            + " | " + str(gen["c_row"])
            + " | " + str(gen["anchor_col"])
            + " | " + str(gen["selected_candidate_index"])
            + " | " + str(gen["c_key"])
            + " | " + str(gen["anchor_key"])
            + " | " + " ".join(str(x) for x in gen["c_path"])
            + " | " + " ".join(str(x) for x in gen["c_values"])
            + " | " + " ".join(str(x) for x in gen["anchor_residues"])
            + " | " + overlap
            + " | " + ("1" if row["all_fields_match"] else "0")
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
    lines.append("This consolidates artifacts 007-010 into one local answer-cell generator theorem.")
    lines.append("The four-state target is now generated from the two bits b,r, except for the still-open anchor node path geometry.")
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
    print("selected_candidate_indices", selected_candidate_indices)
    for row in comparison_rows:
        gen = row["generated"]
        print(
            gen["state"],
            "selected", gen["selected_candidate_index"],
            "c_path", gen["c_path"],
            "anchor_residues", gen["anchor_residues"],
            "overlap", gen["overlap"],
            "match", row["all_fields_match"],
        )


if __name__ == "__main__":
    main()
