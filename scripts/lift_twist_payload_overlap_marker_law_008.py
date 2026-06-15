#!/usr/bin/env python3
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

IN_006 = ROOT / "artifacts/json/lift_twist_local_answer_cell_target_006.v1.json"
IN_007 = ROOT / "artifacts/json/lift_twist_local_answer_cell_bit_law_007.v1.json"

OUT_JSON = ROOT / "artifacts/json/lift_twist_payload_overlap_marker_law_008.v1.json"
OUT_CSV = ROOT / "artifacts/csv/lift_twist_payload_overlap_marker_law_008.v1.csv"
OUT_NOTE = ROOT / "notes/lift_twist_payload_overlap_marker_law_008.md"


def load_json(path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def state_bits(state):
    if state.startswith("O"):
        b = 0
    elif state.startswith("B"):
        b = 1
    else:
        raise ValueError("unknown state " + state)
    r = int(state[1:])
    return b, r


def predicted_overlap_markers(b, r):
    markers = []

    # ordinary rank-1 return marker
    if (1 - b) * r == 1:
        markers.append(13)

    # branch shared hinge marker
    if b == 1:
        markers.append(2)

    # branch rank-0 base marker
    if b * (1 - r) == 1:
        markers.append(0)

    return sorted(markers)


def predicted_overlap_count(b, r):
    return r + 2 * b - 2 * b * r


def main():
    a006 = load_json(IN_006)
    a007 = load_json(IN_007)

    rows = []
    for src in a006["target_rows"]:
        state = src["state"]
        b, r = state_bits(state)

        observed = sorted(int(x) for x in src["c_anchor_value_overlap"])
        pred = predicted_overlap_markers(b, r)
        pred_count = predicted_overlap_count(b, r)

        row = {
            "state": state,
            "shell": src["shell"],
            "rank": int(src["rank"]),
            "shell_bit": b,
            "rank_bit": r,
            "observed_overlap": observed,
            "predicted_overlap": pred,
            "observed_overlap_count": len(observed),
            "predicted_overlap_count": pred_count,
            "overlap_set_match": observed == pred,
            "overlap_count_match": len(observed) == pred_count,
            "c_values": src["c_values"],
            "anchor_residues": src["anchor_residues"],
            "selected_candidate_index": int(src["selected_candidate_index"]),
            "c_key": int(src["c_rank_key"]),
            "anchor_key": int(src["anchor_rank_key"]),
        }
        row["all_overlap_matches"] = row["overlap_set_match"] and row["overlap_count_match"]
        rows.append(row)

    checks = {
        "all_overlap_sets_match": all(r["overlap_set_match"] for r in rows),
        "all_overlap_counts_match": all(r["overlap_count_match"] for r in rows),
        "all_overlap_matches": all(r["all_overlap_matches"] for r in rows),
        "project22_006_theorem_pass": bool(a006.get("theorem_pass")),
        "project22_007_theorem_pass": bool(a007.get("theorem_pass")),
    }

    theorem_pass = all(checks.values())

    result = {
        "status": "lift_twist_payload_overlap_marker_law_recorded",
        "audit_id": "008",
        "inputs": {
            "006": str(IN_006),
            "007": str(IN_007),
        },
        "bit_encoding": {
            "ordinary_shell": 0,
            "branch_shell": 1,
            "rank": "0 or 1 from state suffix",
        },
        "laws": {
            "overlap_count": "r + 2*b - 2*b*r",
            "marker_13": "present iff (1-b)*r = 1",
            "marker_2": "present iff b = 1",
            "marker_0": "present iff b*(1-r) = 1",
        },
        "rows": rows,
        "checks": checks,
        "theorem_pass": theorem_pass,
        "claim": (
            "The local answer-cell payload overlap markers obey an exact two-bit law. "
            "With shell bit b and rank bit r, the overlap count is r+2*b-2*b*r. "
            "Marker 13 appears exactly for ordinary rank 1; marker 2 appears exactly for branch states; "
            "marker 0 appears exactly for branch rank 0. This recovers the observed overlaps: "
            "O0 none, O1 {13}, B0 {0,2}, B1 {2}."
        ),
        "boundary": (
            "This derives the overlap markers between C payload values and anchor residues for the 006 target table. "
            "It does not derive the full C payload paths, full anchor residue sets, the reduced 16-candidate universe, "
            "or Gap A closure."
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
            "observed_overlap",
            "predicted_overlap",
            "observed_overlap_count",
            "predicted_overlap_count",
            "overlap_set_match",
            "overlap_count_match",
        ])
        for r in rows:
            w.writerow([
                r["state"],
                r["shell_bit"],
                r["rank_bit"],
                " ".join(str(x) for x in r["observed_overlap"]) or "none",
                " ".join(str(x) for x in r["predicted_overlap"]) or "none",
                r["observed_overlap_count"],
                r["predicted_overlap_count"],
                "1" if r["overlap_set_match"] else "0",
                "1" if r["overlap_count_match"] else "0",
            ])

    lines = []
    lines.append("# Lift & Twist payload overlap marker law 008")
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
    lines.append("| state | b | r | observed overlap | predicted overlap | count | match |")
    lines.append("|---|---:|---:|---|---|---:|---:|")
    for r in rows:
        obs = " ".join(str(x) for x in r["observed_overlap"]) or "none"
        pred = " ".join(str(x) for x in r["predicted_overlap"]) or "none"
        lines.append(
            "| " + r["state"]
            + " | " + str(r["shell_bit"])
            + " | " + str(r["rank_bit"])
            + " | " + obs
            + " | " + pred
            + " | " + str(r["predicted_overlap_count"])
            + " | " + ("1" if r["all_overlap_matches"] else "0")
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
    lines.append("This is the first payload-coupling law. It derives the overlap signature of each local state from the two state bits.")
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
            "observed", r["observed_overlap"],
            "predicted", r["predicted_overlap"],
            "match", r["all_overlap_matches"],
        )


if __name__ == "__main__":
    main()
