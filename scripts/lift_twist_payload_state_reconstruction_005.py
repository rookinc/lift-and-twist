#!/usr/bin/env python3
import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

IN_003 = ROOT / "artifacts/json/lift_twist_two_readout_universe_003.v1.json"
IN_004 = ROOT / "artifacts/json/lift_twist_readout_order_rule_004.v1.json"

OUT_JSON = ROOT / "artifacts/json/lift_twist_payload_state_reconstruction_005.v1.json"
OUT_CSV = ROOT / "artifacts/csv/lift_twist_payload_state_reconstruction_005.v1.csv"
OUT_NOTE = ROOT / "notes/lift_twist_payload_state_reconstruction_005.md"


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


def contains_pair(payload, a, b):
    items = []
    for key in ["anchor_path", "anchor_nodes"]:
        value = payload.get(key, [])
        if isinstance(value, list):
            items.extend(value)
        else:
            items.append(value)

    for item in items:
        vals = ints_from_any(item)
        if len(vals) >= 2 and a in vals and b in vals:
            return True
    return False


def state_name(shell, rank):
    return ("O" if shell == "ordinary" else "B") + str(rank)


def c_entry(c_payload):
    path = c_payload.get("c_path", [])
    vals = ints_from_any(path)
    if vals:
        return vals[0]
    cvals = c_payload.get("c_values", [])
    vals = ints_from_any(cvals)
    return min(vals) if vals else None


def derive_c_states(c_readout):
    rows = []
    for row in c_readout:
        payload = row["payload"]
        c_values = set(ints_from_any(payload.get("c_values", [])))
        shell = "branch" if 5 in c_values else "ordinary"
        rows.append({
            "visible_index": int(row["visible_index"]),
            "observed_state": row["state"],
            "derived_shell": shell,
            "rank_key": c_entry(payload),
            "payload": payload,
        })

    for shell in ["ordinary", "branch"]:
        shell_rows = sorted(
            [r for r in rows if r["derived_shell"] == shell],
            key=lambda r: (r["rank_key"], r["visible_index"]),
        )
        for rank, r in enumerate(shell_rows):
            r["derived_rank"] = rank
            r["derived_state"] = state_name(shell, rank)

    return sorted(rows, key=lambda r: r["visible_index"])


def derive_anchor_states(anchor_readout):
    cols = []
    for col in anchor_readout:
        payload = col["payload"]
        shell = "branch" if contains_pair(payload, 8, 18) else "ordinary"
        cols.append({
            "visible_index": int(col["visible_index"]),
            "observed_state": col["state"],
            "derived_shell": shell,
            "rank_key": int(payload.get("anchor_sum_mod15")),
            "payload": payload,
        })

    for shell in ["ordinary", "branch"]:
        shell_cols = sorted(
            [r for r in cols if r["derived_shell"] == shell],
            key=lambda r: (r["rank_key"], r["visible_index"]),
        )
        for rank, r in enumerate(shell_cols):
            r["derived_rank"] = rank
            r["derived_state"] = state_name(shell, rank)

    return sorted(cols, key=lambda r: r["visible_index"])


def main():
    a003 = load_json(IN_003)
    a004 = load_json(IN_004)

    c_rows = derive_c_states(a003["c_readout"])
    anchor_cols = derive_anchor_states(a003["anchor_readout"])

    c_state_by_row = {r["visible_index"]: r["derived_state"] for r in c_rows}
    anchor_state_by_col = {r["visible_index"]: r["derived_state"] for r in anchor_cols}

    derived_c_order = [c_state_by_row[i] for i in sorted(c_state_by_row)]
    derived_anchor_order = [anchor_state_by_col[i] for i in sorted(anchor_state_by_col)]

    observed_c_order = list(a003["c_readout_order"])
    observed_anchor_order = list(a003["anchor_readout_order"])

    generated = []
    for item in a003["generated_universe"]:
        c_row = int(item["c_row"])
        a_col = int(item["a_col"])
        c_state = c_state_by_row[c_row]
        anchor_state = anchor_state_by_col[a_col]
        hidden_diagonal = c_state == anchor_state
        actual_selected = bool(item["actual_selected"])
        generated.append({
            "candidate_index": int(item["candidate_index"]),
            "c_row": c_row,
            "a_col": a_col,
            "derived_c_state": c_state,
            "derived_anchor_state": anchor_state,
            "hidden_diagonal_from_payload_states": hidden_diagonal,
            "actual_selected": actual_selected,
            "matches_actual": hidden_diagonal == actual_selected,
        })

    derived_diagonal_indices = sorted(
        r["candidate_index"] for r in generated if r["hidden_diagonal_from_payload_states"]
    )
    actual_selected_indices = sorted(
        r["candidate_index"] for r in generated if r["actual_selected"]
    )

    c_state_matches_observed = all(r["derived_state"] == r["observed_state"] for r in c_rows)
    anchor_state_matches_observed = all(r["derived_state"] == r["observed_state"] for r in anchor_cols)

    checks = {
        "derived_c_order_matches_observed": derived_c_order == observed_c_order,
        "derived_anchor_order_matches_observed": derived_anchor_order == observed_anchor_order,
        "c_state_matches_observed": c_state_matches_observed,
        "anchor_state_matches_observed": anchor_state_matches_observed,
        "derived_diagonal_matches_actual": derived_diagonal_indices == actual_selected_indices,
        "all_candidate_matches_actual": all(r["matches_actual"] for r in generated),
        "project22_003_theorem_pass": bool(a003.get("theorem_pass")),
        "project22_004_theorem_pass": bool(a004.get("theorem_pass")),
    }

    theorem_pass = all(checks.values())

    result = {
        "status": "lift_twist_payload_state_reconstruction_recorded",
        "audit_id": "005",
        "inputs": {
            "003": str(IN_003),
            "004": str(IN_004),
        },
        "payload_state_rules": {
            "c_shell_rule": "branch iff c_values contains 5; otherwise ordinary",
            "c_rank_rule": "rank by ascending c_entry within shell",
            "anchor_shell_rule": "branch iff anchor payload contains node [8,18]; otherwise ordinary",
            "anchor_rank_rule": "rank by ascending anchor_sum_mod15 within shell",
        },
        "c_rows": c_rows,
        "anchor_cols": anchor_cols,
        "observed_c_order": observed_c_order,
        "derived_c_order": derived_c_order,
        "observed_anchor_order": observed_anchor_order,
        "derived_anchor_order": derived_anchor_order,
        "derived_diagonal_indices": derived_diagonal_indices,
        "actual_selected_indices": actual_selected_indices,
        "checks": checks,
        "theorem_pass": theorem_pass,
        "generated_universe_from_payload_states": generated,
        "claim": (
            "The hidden four states used by Lift & Twist can be reconstructed from readout payload markers. "
            "On the C side, branch states are exactly those whose C payload contains 5, ranked by C entry. "
            "On the anchor side, branch states are exactly those whose anchor payload contains [8,18], ranked "
            "by anchor_sum_mod15. These payload-derived states reproduce the two readout orders and recover "
            "the selected diagonal [1,6,8,15]."
        ),
        "boundary": (
            "This reconstructs hidden state labels from the copied reduced-universe payloads. It does not derive "
            "the payloads themselves from one local answer cell, does not derive the reduced 16-candidate universe "
            "from native provenance, and does not close Gap A."
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
            "derived_c_state",
            "derived_anchor_state",
            "hidden_diagonal_from_payload_states",
            "actual_selected",
            "matches_actual",
        ])
        for r in sorted(generated, key=lambda x: x["candidate_index"]):
            w.writerow([
                r["candidate_index"],
                r["c_row"],
                r["a_col"],
                r["derived_c_state"],
                r["derived_anchor_state"],
                "1" if r["hidden_diagonal_from_payload_states"] else "0",
                "1" if r["actual_selected"] else "0",
                "1" if r["matches_actual"] else "0",
            ])

    lines = []
    lines.append("# Lift & Twist payload state reconstruction 005")
    lines.append("")
    lines.append("Status: " + result["status"])
    lines.append("")
    lines.append("## Claim")
    lines.append("")
    lines.append(result["claim"])
    lines.append("")
    lines.append("## Payload state rules")
    lines.append("")
    for k, v in result["payload_state_rules"].items():
        lines.append("- " + k + ": `" + v + "`")
    lines.append("")
    lines.append("## Orders")
    lines.append("")
    lines.append("- observed C order: `" + str(observed_c_order) + "`")
    lines.append("- derived C order: `" + str(derived_c_order) + "`")
    lines.append("- observed anchor order: `" + str(observed_anchor_order) + "`")
    lines.append("- derived anchor order: `" + str(derived_anchor_order) + "`")
    lines.append("")
    lines.append("## Diagonal")
    lines.append("")
    lines.append("- derived diagonal indices: `" + str(derived_diagonal_indices) + "`")
    lines.append("- actual selected indices: `" + str(actual_selected_indices) + "`")
    lines.append("")
    lines.append("## C state reconstruction")
    lines.append("")
    for r in c_rows:
        lines.append(
            "- row `" + str(r["visible_index"]) + "` observed `" + r["observed_state"]
            + "` derived `" + r["derived_state"] + "` shell `" + r["derived_shell"]
            + "` rank_key `" + str(r["rank_key"]) + "`"
        )
    lines.append("")
    lines.append("## Anchor state reconstruction")
    lines.append("")
    for r in anchor_cols:
        lines.append(
            "- col `" + str(r["visible_index"]) + "` observed `" + r["observed_state"]
            + "` derived `" + r["derived_state"] + "` shell `" + r["derived_shell"]
            + "` rank_key `" + str(r["rank_key"]) + "`"
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
    print("derived_c_order", derived_c_order)
    print("derived_anchor_order", derived_anchor_order)
    print("derived_diagonal_indices", derived_diagonal_indices)
    print("actual_selected_indices", actual_selected_indices)


if __name__ == "__main__":
    main()
