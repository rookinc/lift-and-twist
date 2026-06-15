#!/usr/bin/env python3
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

IN_002 = ROOT / "artifacts/json/lift_twist_coordinate_straightening_002.v1.json"
IN_003 = ROOT / "artifacts/json/lift_twist_two_readout_universe_003.v1.json"

OUT_JSON = ROOT / "artifacts/json/lift_twist_readout_order_rule_004.v1.json"
OUT_CSV = ROOT / "artifacts/csv/lift_twist_readout_order_rule_004.v1.csv"
OUT_NOTE = ROOT / "notes/lift_twist_readout_order_rule_004.md"


def load_json(path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def parse_state(s):
    shell = "ordinary" if s.startswith("O") else "branch"
    rank = int(s[1:])
    return {"state": s, "shell": shell, "rank": rank}


def state_sort_key_c(s):
    x = parse_state(s)
    shell_order = {"ordinary": 0, "branch": 1}
    return (shell_order[x["shell"]], x["rank"])


def derive_c_order(states):
    return sorted(states, key=state_sort_key_c)


def derive_anchor_order_from_lift_twist(c_order):
    parsed = [parse_state(s) for s in c_order]

    branch = [x["state"] for x in parsed if x["shell"] == "branch"]
    ordinary = [x["state"] for x in parsed if x["shell"] == "ordinary"]

    branch_sorted = sorted(branch, key=lambda s: parse_state(s)["rank"])
    ordinary_sorted = sorted(ordinary, key=lambda s: parse_state(s)["rank"])

    if not branch_sorted:
        return ordinary_sorted

    # Lift & Twist readout rule:
    # The first branch state wraps to the front.
    # Ordinary states remain in ascending rank order.
    # Any remaining branch states stay at the terminal boundary in ascending rank order.
    return [branch_sorted[0]] + ordinary_sorted + branch_sorted[1:]


def induced_permutation(c_order, anchor_order):
    pos = {state: i for i, state in enumerate(anchor_order)}
    return [pos[state] for state in c_order]


def cycles_from_perm(perm):
    seen = set()
    cycles = []
    for i in range(len(perm)):
        if i in seen:
            continue
        cur = i
        cyc = []
        while cur not in seen:
            seen.add(cur)
            cyc.append(cur)
            cur = perm[cur]
        cycles.append(cyc)
    return cycles


def main():
    a002 = load_json(IN_002)
    a003 = load_json(IN_003)

    observed_c_order = list(a003["c_readout_order"])
    observed_anchor_order = list(a003["anchor_readout_order"])
    states = sorted(set(observed_c_order) | set(observed_anchor_order), key=state_sort_key_c)

    derived_c_order = derive_c_order(states)
    derived_anchor_order = derive_anchor_order_from_lift_twist(derived_c_order)

    observed_perm = list(a002["visible_permutation_list"])
    derived_perm = induced_permutation(derived_c_order, derived_anchor_order)
    cycles = cycles_from_perm(derived_perm)

    # Reconstruct universe from derived orders and compare to 003.
    generated = []
    for c_pos, c_state in enumerate(derived_c_order):
        for a_pos, a_state in enumerate(derived_anchor_order):
            hidden_diagonal = c_state == a_state
            generated.append({
                "c_pos": c_pos,
                "a_pos": a_pos,
                "candidate_index": c_pos * len(derived_anchor_order) + a_pos,
                "c_state": c_state,
                "anchor_state": a_state,
                "hidden_diagonal": hidden_diagonal,
            })

    derived_diagonal_indices = [
        row["candidate_index"] for row in generated if row["hidden_diagonal"]
    ]

    observed_diagonal_indices = list(a003["hidden_diagonal_indices"])
    observed_actual_selected = list(a003["actual_selected_indices"])

    checks = {
        "state_sets_match": set(observed_c_order) == set(observed_anchor_order) == set(states),
        "derived_c_order_matches_observed": derived_c_order == observed_c_order,
        "derived_anchor_order_matches_observed": derived_anchor_order == observed_anchor_order,
        "derived_permutation_matches_observed": derived_perm == observed_perm,
        "derived_diagonal_matches_003_diagonal": derived_diagonal_indices == observed_diagonal_indices,
        "derived_diagonal_matches_actual_selected": derived_diagonal_indices == observed_actual_selected,
        "project22_002_theorem_pass": bool(a002.get("theorem_pass")),
        "project22_003_theorem_pass": bool(a003.get("theorem_pass")),
    }

    theorem_pass = all(checks.values())

    result = {
        "status": "lift_twist_readout_order_rule_recorded",
        "audit_id": "004",
        "inputs": {
            "002": str(IN_002),
            "003": str(IN_003),
        },
        "states": states,
        "observed_c_order": observed_c_order,
        "observed_anchor_order": observed_anchor_order,
        "derived_c_order": derived_c_order,
        "derived_anchor_order": derived_anchor_order,
        "readout_order_rule": {
            "c_order_rule": "ordinary shell first, branch shell second, ranks ascending inside each shell",
            "anchor_order_rule": "first branch rank wraps to front, ordinary ranks follow, remaining branch ranks stay terminal",
        },
        "observed_visible_permutation": observed_perm,
        "derived_visible_permutation": derived_perm,
        "permutation_cycles": cycles,
        "derived_diagonal_indices": derived_diagonal_indices,
        "observed_diagonal_indices": observed_diagonal_indices,
        "observed_actual_selected_indices": observed_actual_selected,
        "checks": checks,
        "theorem_pass": theorem_pass,
        "generated_universe_from_derived_orders": generated,
        "claim": (
            "The two readout orders used in 003 are reproduced by a compact Lift & Twist order rule. "
            "The C readout orders states by ordinary-before-branch shell order with ascending rank. "
            "The anchor readout is obtained by moving the first branch state B0 to the front, then "
            "reading ordinary ranks, then leaving the remaining branch state B1 terminal. This derived "
            "order induces the visible permutation [1,2,0,3] and the diagonal candidates [1,6,8,15]."
        ),
        "boundary": (
            "This derives the readout order rule inside the four-state representation. It does not yet "
            "derive the hidden states or their payloads from one local answer cell, and it does not close Gap A."
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
            "c_pos",
            "a_pos",
            "c_state",
            "anchor_state",
            "hidden_diagonal",
        ])
        for r in generated:
            w.writerow([
                r["candidate_index"],
                r["c_pos"],
                r["a_pos"],
                r["c_state"],
                r["anchor_state"],
                "1" if r["hidden_diagonal"] else "0",
            ])

    lines = []
    lines.append("# Lift & Twist readout order rule 004")
    lines.append("")
    lines.append("Status: " + result["status"])
    lines.append("")
    lines.append("## Claim")
    lines.append("")
    lines.append(result["claim"])
    lines.append("")
    lines.append("## Readout order rule")
    lines.append("")
    lines.append("- C order rule: `" + result["readout_order_rule"]["c_order_rule"] + "`")
    lines.append("- anchor order rule: `" + result["readout_order_rule"]["anchor_order_rule"] + "`")
    lines.append("")
    lines.append("## Orders")
    lines.append("")
    lines.append("- observed C order: `" + str(observed_c_order) + "`")
    lines.append("- derived C order: `" + str(derived_c_order) + "`")
    lines.append("- observed anchor order: `" + str(observed_anchor_order) + "`")
    lines.append("- derived anchor order: `" + str(derived_anchor_order) + "`")
    lines.append("")
    lines.append("## Permutation")
    lines.append("")
    lines.append("- observed visible permutation: `" + str(observed_perm) + "`")
    lines.append("- derived visible permutation: `" + str(derived_perm) + "`")
    lines.append("- permutation cycles: `" + str(cycles) + "`")
    lines.append("")
    lines.append("## Diagonal")
    lines.append("")
    lines.append("- derived diagonal indices: `" + str(derived_diagonal_indices) + "`")
    lines.append("- observed diagonal indices: `" + str(observed_diagonal_indices) + "`")
    lines.append("- observed actual selected indices: `" + str(observed_actual_selected) + "`")
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
    print("derived_visible_permutation", derived_perm)
    print("derived_diagonal_indices", derived_diagonal_indices)


if __name__ == "__main__":
    main()
