#!/usr/bin/env python3
import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

IN_006 = ROOT / "artifacts/json/lift_twist_local_answer_cell_target_006.v1.json"
IN_007 = ROOT / "artifacts/json/lift_twist_local_answer_cell_bit_law_007.v1.json"
IN_008 = ROOT / "artifacts/json/lift_twist_payload_overlap_marker_law_008.v1.json"

OUT_JSON = ROOT / "artifacts/json/lift_twist_c_payload_path_law_009.v1.json"
OUT_CSV = ROOT / "artifacts/csv/lift_twist_c_payload_path_law_009.v1.csv"
OUT_NOTE = ROOT / "notes/lift_twist_c_payload_path_law_009.md"


def load_json(path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def ints_from_any(x):
    if isinstance(x, int):
        return [x]
    if isinstance(x, list):
        out = []
        for y in x:
            out.extend(ints_from_any(y))
        return out
    if isinstance(x, dict):
        out = []
        for y in x.values():
            out.extend(ints_from_any(y))
        return out
    if isinstance(x, str):
        return [int(v) for v in re.findall(r"-?\d+", x)]
    return []


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


def c_key_law(b, r):
    return mod15(11 + 6 * b + 2 * r)


def c_path_offsets_law(b, r):
    # First lift offset.
    # O0=6, O1=3, B0=3, B1=1.
    d1 = mod15(6 - 3 * b - 3 * r + b * r)

    # Second/return-marker offset.
    # ordinary: O0=3, O1=12.
    # branch: B0=B1=13.
    d2 = mod15((1 - b) * (3 + 9 * r) + b * 13)

    return [0, d1, d2, 0]


def c_path_law(b, r):
    k = c_key_law(b, r)
    offsets = c_path_offsets_law(b, r)
    path = [mod15(k + d) for d in offsets]
    values = sorted(set(path))
    return k, offsets, path, values


def main():
    a006 = load_json(IN_006)
    a007 = load_json(IN_007)
    a008 = load_json(IN_008)

    rows = []
    for src in a006["target_rows"]:
        state = src["state"]
        b, r = state_bits(state)

        predicted_c_key, predicted_offsets, predicted_path, predicted_values = c_path_law(b, r)

        observed_payload = src["c_payload"]
        observed_path = ints_from_any(observed_payload.get("c_path", []))
        observed_values = sorted(set(int(x) for x in src.get("c_values", [])))
        observed_c_key = int(src["c_rank_key"])
        observed_sum_mod15 = sum(observed_values) % 15
        predicted_sum_mod15 = sum(predicted_values) % 15

        row = {
            "state": state,
            "shell": src["shell"],
            "rank": int(src["rank"]),
            "shell_bit": b,
            "rank_bit": r,
            "observed_c_key": observed_c_key,
            "predicted_c_key": predicted_c_key,
            "observed_c_path": observed_path,
            "predicted_c_path": predicted_path,
            "predicted_offsets": predicted_offsets,
            "observed_c_values": observed_values,
            "predicted_c_values": predicted_values,
            "observed_c_sum_mod15": observed_sum_mod15,
            "predicted_c_sum_mod15": predicted_sum_mod15,
            "c_key_match": observed_c_key == predicted_c_key,
            "c_path_match": observed_path == predicted_path,
            "c_values_match": observed_values == predicted_values,
            "c_sum_match": observed_sum_mod15 == predicted_sum_mod15,
        }
        row["all_c_payload_matches"] = (
            row["c_key_match"]
            and row["c_path_match"]
            and row["c_values_match"]
            and row["c_sum_match"]
        )
        rows.append(row)

    checks = {
        "all_c_keys_match": all(r["c_key_match"] for r in rows),
        "all_c_paths_match": all(r["c_path_match"] for r in rows),
        "all_c_values_match": all(r["c_values_match"] for r in rows),
        "all_c_sums_match": all(r["c_sum_match"] for r in rows),
        "all_c_payload_matches": all(r["all_c_payload_matches"] for r in rows),
        "project22_006_theorem_pass": bool(a006.get("theorem_pass")),
        "project22_007_theorem_pass": bool(a007.get("theorem_pass")),
        "project22_008_theorem_pass": bool(a008.get("theorem_pass")),
    }

    theorem_pass = all(checks.values())

    result = {
        "status": "lift_twist_c_payload_path_law_recorded",
        "audit_id": "009",
        "inputs": {
            "006": str(IN_006),
            "007": str(IN_007),
            "008": str(IN_008),
        },
        "bit_encoding": {
            "ordinary_shell": 0,
            "branch_shell": 1,
            "rank": "0 or 1 from state suffix",
        },
        "laws": {
            "c_key": "k = 11 + 6*b + 2*r mod 15",
            "c_path_offsets": "[0, d1, d2, 0]",
            "d1": "6 - 3*b - 3*r + b*r mod 15",
            "d2": "(1-b)*(3 + 9*r) + 13*b mod 15",
            "c_path": "[k, k+d1, k+d2, k] mod 15",
            "c_values": "unique values of c_path",
        },
        "rows": rows,
        "checks": checks,
        "theorem_pass": theorem_pass,
        "claim": (
            "The C-side payload path of the four-state local answer-cell target is generated by "
            "a compact two-bit law. With shell bit b and rank bit r, k=11+6*b+2*r mod 15, "
            "d1=6-3*b-3*r+b*r mod 15, d2=(1-b)*(3+9*r)+13*b mod 15, and "
            "C path=[k,k+d1,k+d2,k] mod 15. This recovers the full observed C paths and "
            "C value sets for O0,O1,B0,B1."
        ),
        "boundary": (
            "This derives the C-side payload path for the four-state target table. It does not derive "
            "the anchor residue sets, the full reduced 16-candidate universe, or a G60-native generator. "
            "It is not Gap A closure."
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
            "observed_c_key",
            "predicted_c_key",
            "predicted_offsets",
            "observed_c_path",
            "predicted_c_path",
            "observed_c_values",
            "predicted_c_values",
            "all_c_payload_matches",
        ])
        for row in rows:
            w.writerow([
                row["state"],
                row["shell_bit"],
                row["rank_bit"],
                row["observed_c_key"],
                row["predicted_c_key"],
                " ".join(str(x) for x in row["predicted_offsets"]),
                " ".join(str(x) for x in row["observed_c_path"]),
                " ".join(str(x) for x in row["predicted_c_path"]),
                " ".join(str(x) for x in row["observed_c_values"]),
                " ".join(str(x) for x in row["predicted_c_values"]),
                "1" if row["all_c_payload_matches"] else "0",
            ])

    lines = []
    lines.append("# Lift & Twist C payload path law 009")
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
    lines.append("| state | b | r | key | offsets | observed path | predicted path | values | match |")
    lines.append("|---|---:|---:|---:|---|---|---|---|---:|")
    for row in rows:
        offsets = " ".join(str(x) for x in row["predicted_offsets"])
        obs_path = " ".join(str(x) for x in row["observed_c_path"])
        pred_path = " ".join(str(x) for x in row["predicted_c_path"])
        vals = " ".join(str(x) for x in row["predicted_c_values"])
        lines.append(
            "| " + row["state"]
            + " | " + str(row["shell_bit"])
            + " | " + str(row["rank_bit"])
            + " | " + str(row["predicted_c_key"])
            + " | " + offsets
            + " | " + obs_path
            + " | " + pred_path
            + " | " + vals
            + " | " + ("1" if row["all_c_payload_matches"] else "0")
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
            "key", row["predicted_c_key"],
            "offsets", row["predicted_offsets"],
            "path", row["predicted_c_path"],
            "values", row["predicted_c_values"],
            "match", row["all_c_payload_matches"],
        )


if __name__ == "__main__":
    main()
