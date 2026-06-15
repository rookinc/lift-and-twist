#!/usr/bin/env python3
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

IN_006 = ROOT / "artifacts/json/lift_twist_local_answer_cell_target_006.v1.json"
IN_007 = ROOT / "artifacts/json/lift_twist_local_answer_cell_bit_law_007.v1.json"
IN_008 = ROOT / "artifacts/json/lift_twist_payload_overlap_marker_law_008.v1.json"
IN_009 = ROOT / "artifacts/json/lift_twist_c_payload_path_law_009.v1.json"

OUT_JSON = ROOT / "artifacts/json/lift_twist_anchor_residue_set_law_010.v1.json"
OUT_CSV = ROOT / "artifacts/csv/lift_twist_anchor_residue_set_law_010.v1.csv"
OUT_NOTE = ROOT / "notes/lift_twist_anchor_residue_set_law_010.md"


def load_json(path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def mod15(x):
    return x % 15


def state_bits(state):
    if state.startswith("O"):
        b = 0
    elif state.startswith("B"):
        b = 1
    else:
        raise ValueError("unknown state " + state)
    r = int(state[1:])
    return b, r


def anchor_key_law(b, r):
    return mod15(4 * b + 12 * r + 12 * b * r)


def ordinary_offsets(r):
    # shared ordinary offsets plus rank switch
    shared = {5, 7, 12}
    switched = {
        1 + 3 * (1 - r),
        2 + 6 * (1 - r),
        3 + 6 * (1 - r),
    }
    return shared | switched


def branch_offsets(r):
    # shared branch offsets plus rank switch
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


def anchor_residue_set_law(b, r):
    key = anchor_key_law(b, r)
    offsets = anchor_offsets_law(b, r)
    residues = sorted({mod15(key + d) for d in offsets})
    return key, offsets, residues


def main():
    a006 = load_json(IN_006)
    a007 = load_json(IN_007)
    a008 = load_json(IN_008)
    a009 = load_json(IN_009)

    rows = []
    for src in a006["target_rows"]:
        state = src["state"]
        b, r = state_bits(state)

        predicted_key, predicted_offsets, predicted_residues = anchor_residue_set_law(b, r)

        observed_key = int(src["anchor_rank_key"])
        observed_residues = sorted(int(x) for x in src["anchor_residues"])
        observed_size = len(observed_residues)
        predicted_size = len(predicted_residues)
        observed_sum = sum(observed_residues) % 15
        predicted_sum = sum(predicted_residues) % 15

        row = {
            "state": state,
            "shell": src["shell"],
            "rank": int(src["rank"]),
            "shell_bit": b,
            "rank_bit": r,
            "observed_anchor_key": observed_key,
            "predicted_anchor_key": predicted_key,
            "predicted_offsets": predicted_offsets,
            "observed_anchor_residues": observed_residues,
            "predicted_anchor_residues": predicted_residues,
            "observed_size": observed_size,
            "predicted_size": predicted_size,
            "observed_sum_mod15": observed_sum,
            "predicted_sum_mod15": predicted_sum,
            "anchor_key_match": observed_key == predicted_key,
            "anchor_residue_set_match": observed_residues == predicted_residues,
            "anchor_size_match": observed_size == predicted_size,
            "anchor_sum_match": observed_sum == predicted_sum,
            "selected_candidate_index": int(src["selected_candidate_index"]),
        }
        row["all_anchor_residue_matches"] = (
            row["anchor_key_match"]
            and row["anchor_residue_set_match"]
            and row["anchor_size_match"]
            and row["anchor_sum_match"]
        )
        rows.append(row)

    checks = {
        "all_anchor_keys_match": all(r["anchor_key_match"] for r in rows),
        "all_anchor_residue_sets_match": all(r["anchor_residue_set_match"] for r in rows),
        "all_anchor_sizes_match": all(r["anchor_size_match"] for r in rows),
        "all_anchor_sums_match": all(r["anchor_sum_match"] for r in rows),
        "all_anchor_residue_matches": all(r["all_anchor_residue_matches"] for r in rows),
        "project22_006_theorem_pass": bool(a006.get("theorem_pass")),
        "project22_007_theorem_pass": bool(a007.get("theorem_pass")),
        "project22_008_theorem_pass": bool(a008.get("theorem_pass")),
        "project22_009_theorem_pass": bool(a009.get("theorem_pass")),
    }

    theorem_pass = all(checks.values())

    result = {
        "status": "lift_twist_anchor_residue_set_law_recorded",
        "audit_id": "010",
        "inputs": {
            "006": str(IN_006),
            "007": str(IN_007),
            "008": str(IN_008),
            "009": str(IN_009),
        },
        "bit_encoding": {
            "ordinary_shell": 0,
            "branch_shell": 1,
            "rank": "0 or 1 from state suffix",
        },
        "laws": {
            "anchor_key": "a = 4*b + 12*r + 12*b*r mod 15",
            "ordinary_offsets": "{5,7,12} union {1+3*(1-r), 2+6*(1-r), 3+6*(1-r)}",
            "branch_offsets": "{0,4} union {11-6*r, 13-4*r, 14-4*r} mod 15, plus {12} when r=1",
            "anchor_residues": "{anchor_key + offset mod 15 for offset in offsets}",
        },
        "rows": rows,
        "checks": checks,
        "theorem_pass": theorem_pass,
        "claim": (
            "The anchor-side residue set of the four-state local answer-cell target is generated by "
            "a two-bit offset law. With shell bit b and rank bit r, the anchor key is "
            "4*b+12*r+12*b*r mod 15. Ordinary states use shared offsets {5,7,12} plus a rank switch; "
            "branch states use shared offsets {0,4} plus a branch rank switch. Adding these offsets to "
            "the anchor key mod 15 recovers the full observed anchor residue sets for O0,O1,B0,B1."
        ),
        "boundary": (
            "This derives the anchor residue sets for the four-state target table by an exact two-bit "
            "offset law. It does not yet derive the anchor node paths themselves, the full reduced "
            "16-candidate universe from native provenance, or a G60-native generator. It is not Gap A closure."
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
            "observed_anchor_key",
            "predicted_anchor_key",
            "predicted_offsets",
            "observed_anchor_residues",
            "predicted_anchor_residues",
            "observed_size",
            "predicted_size",
            "all_anchor_residue_matches",
        ])
        for row in rows:
            w.writerow([
                row["state"],
                row["shell_bit"],
                row["rank_bit"],
                row["observed_anchor_key"],
                row["predicted_anchor_key"],
                " ".join(str(x) for x in row["predicted_offsets"]),
                " ".join(str(x) for x in row["observed_anchor_residues"]),
                " ".join(str(x) for x in row["predicted_anchor_residues"]),
                row["observed_size"],
                row["predicted_size"],
                "1" if row["all_anchor_residue_matches"] else "0",
            ])

    lines = []
    lines.append("# Lift & Twist anchor residue set law 010")
    lines.append("")
    lines.append("Status: " + result["status"])
    lines.append("")
    lines.append("## Claim")
    lines.append("")
    lines.append(result["claim"])
    lines.append("")
    lines.append("## Laws")
    lines.append("")
    for k, v in result["laws"].items():
        lines.append("- " + k + ": `" + v + "`")
    lines.append("")
    lines.append("## Table")
    lines.append("")
    lines.append("| state | b | r | anchor key | offsets | observed residues | predicted residues | match |")
    lines.append("|---|---:|---:|---:|---|---|---|---:|")
    for row in rows:
        offsets = " ".join(str(x) for x in row["predicted_offsets"])
        obs = " ".join(str(x) for x in row["observed_anchor_residues"])
        pred = " ".join(str(x) for x in row["predicted_anchor_residues"])
        lines.append(
            "| " + row["state"]
            + " | " + str(row["shell_bit"])
            + " | " + str(row["rank_bit"])
            + " | " + str(row["predicted_anchor_key"])
            + " | " + offsets
            + " | " + obs
            + " | " + pred
            + " | " + ("1" if row["all_anchor_residue_matches"] else "0")
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
    for row in rows:
        print(
            row["state"],
            "b", row["shell_bit"],
            "r", row["rank_bit"],
            "key", row["predicted_anchor_key"],
            "offsets", row["predicted_offsets"],
            "residues", row["predicted_anchor_residues"],
            "match", row["all_anchor_residue_matches"],
        )


if __name__ == "__main__":
    main()
