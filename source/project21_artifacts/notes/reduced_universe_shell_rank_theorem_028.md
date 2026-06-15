# Reduced-universe shell-rank theorem 028

Status: reduced_universe_shell_rank_theorem_recorded

## Theorem

In the 16-candidate shared_B reduced universe formed by crossing the four observed C-cycles with the four twisted anchor-cycles, define the C shell by the native C-branch marker C=5 and the anchor shell by the native branch anchor [8,18]. Rank C-cycles inside each shell by ascending C entry / XY.from_C. Rank anchor-cycles inside each shell by ascending anchor_sum_mod15. Then the selector 'same shell and same rank' accepts exactly the four observed shared_B cycles.

## Hypotheses

- H1_reduced_universe_is_4_by_4: `True`
- H2_native_shell_labels_derived: `True`
- H3_c_rank_unambiguous: `True`
- H4_anchor_rank_unambiguous: `True`
- H5_027_target_rank_selector_exact: `True`

## Conclusion

- actual_selected: `[1, 6, 8, 15]`
- predicted_selected: `[1, 6, 8, 15]`
- false_positives: `[]`
- misses: `[]`
- theorem_pass: `True`

## Native ingredients

- native_c_branch_markers: `[5]`
- native_anchor_branch_markers: `['[8,18]']`
- c_rank_rule: `ascending c_entry / XY.from_C within derived shell`
- anchor_rank_rule: `ascending anchor_sum_mod15 within derived shell`

## Rank details

- c_rank_details: `{'branch': [{'index': 2, 'rank': 0, 'key': 2}, {'index': 3, 'rank': 1, 'key': 4}], 'ordinary': [{'index': 0, 'rank': 0, 'key': 11}, {'index': 1, 'rank': 1, 'key': 13}]}`
- anchor_rank_details: `{'branch': [{'index': 0, 'rank': 0, 'key': 4}, {'index': 3, 'rank': 1, 'key': 13}], 'ordinary': [{'index': 1, 'rank': 0, 'key': 0}, {'index': 2, 'rank': 1, 'key': 12}]}`

## Proof table

| candidate | c_row | a_col | actual | predicted | c_shell | a_shell | c_rank | a_rank |
|---|---:|---:|---:|---:|---|---|---:|---:|
| 0 | 0 | 0 | 0 | 0 | ordinary | branch | 0 | 0 |
| 1 | 0 | 1 | 1 | 1 | ordinary | ordinary | 0 | 0 |
| 2 | 0 | 2 | 0 | 0 | ordinary | ordinary | 0 | 1 |
| 3 | 0 | 3 | 0 | 0 | ordinary | branch | 0 | 1 |
| 4 | 1 | 0 | 0 | 0 | ordinary | branch | 1 | 0 |
| 5 | 1 | 1 | 0 | 0 | ordinary | ordinary | 1 | 0 |
| 6 | 1 | 2 | 1 | 1 | ordinary | ordinary | 1 | 1 |
| 7 | 1 | 3 | 0 | 0 | ordinary | branch | 1 | 1 |
| 8 | 2 | 0 | 1 | 1 | branch | branch | 0 | 0 |
| 9 | 2 | 1 | 0 | 0 | branch | ordinary | 0 | 0 |
| 10 | 2 | 2 | 0 | 0 | branch | ordinary | 0 | 1 |
| 11 | 2 | 3 | 0 | 0 | branch | branch | 0 | 1 |
| 12 | 3 | 0 | 0 | 0 | branch | branch | 1 | 0 |
| 13 | 3 | 1 | 0 | 0 | branch | ordinary | 1 | 0 |
| 14 | 3 | 2 | 0 | 0 | branch | ordinary | 1 | 1 |
| 15 | 3 | 3 | 1 | 1 | branch | branch | 1 | 1 |

## Reading

This checkpoint packages 026 and 027 as a reduced-universe theorem. The result is no longer merely a visual radial phase-lock model: within the 16-candidate universe, native shell labels and native shell ranks determine the four selected shared_B cycles exactly.

## Boundary

This theorem is conditional on the reduced 16-candidate universe. It does not derive the full role-labeled shared_B edge universe from first principles, and it does not close Gap A. It proves the selector inside the reduced universe.
