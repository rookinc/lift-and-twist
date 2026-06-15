# Shared_B selection matrix 024

Status: sharedB_selection_matrix_recorded

## Counts

- candidate_count: `16`
- c_row_count: `4`
- anchor_col_count: `4`
- selected_count: `4`
- is_permutation: `True`
- selected_col_by_row: `{'0': 1, '1': 2, '2': 0, '3': 3}`
- permutation_cycles: `[[0, 1, 2], [3]]`
- permutation_cycle_lengths: `[3, 1]`
- permutation_order: `3`

## Selection matrix

Rows are C-cycles. Columns are twisted anchor-cycles.

| c_row | a0 | a1 | a2 | a3 |
|---|---|---|---|---|
| 0 | 0 | S1 | 2 | 3 |
| 1 | 4 | 5 | S6 | 7 |
| 2 | S8 | 9 | 10 | 11 |
| 3 | 12 | 13 | 14 | S15 |

## C-cycle rows

- c_row `0`
  - transitions: `[['XY', 11, 2], ['IW', 2, 14], ['ZT', 14, 11]]`
  - c_path: `[11, 2, 14, 11]`
  - c_values: `[2, 11, 14]`
  - c_sum_mod15: `12`
  - selected_anchor_col: `1`
- c_row `1`
  - transitions: `[['XY', 13, 1], ['IW', 1, 10], ['ZT', 10, 13]]`
  - c_path: `[13, 1, 10, 13]`
  - c_values: `[1, 10, 13]`
  - c_sum_mod15: `9`
  - selected_anchor_col: `2`
- c_row `2`
  - transitions: `[['XY', 2, 5], ['IW', 5, 0], ['ZT', 0, 2]]`
  - c_path: `[2, 5, 0, 2]`
  - c_values: `[0, 2, 5]`
  - c_sum_mod15: `7`
  - selected_anchor_col: `0`
- c_row `3`
  - transitions: `[['XY', 4, 5], ['IW', 5, 2], ['ZT', 2, 4]]`
  - c_path: `[4, 5, 2, 4]`
  - c_values: `[2, 4, 5]`
  - c_sum_mod15: `11`
  - selected_anchor_col: `3`

## Anchor-cycle columns

- a_col `0`
  - anchor_path: `['[0,4]', '[2,17]', '[8,18]', '[0,4]']`
  - anchor_nodes: `['[0,4]', '[2,17]', '[8,18]']`
  - residues: `[0, 2, 3, 4, 8]`
  - anchor_sum_mod15: `4`
  - has_branch_anchor_8_18: `True`
  - selected_c_row: `2`
- a_col `1`
  - anchor_path: `['[23,24]', '[7,12]', '[4,5]', '[23,24]']`
  - anchor_nodes: `['[23,24]', '[7,12]', '[4,5]']`
  - residues: `[4, 5, 7, 8, 9, 12]`
  - anchor_sum_mod15: `0`
  - has_branch_anchor_8_18: `False`
  - selected_c_row: `0`
- a_col `2`
  - anchor_path: `['[28,29]', '[0,2]', '[4,9]', '[28,29]']`
  - anchor_nodes: `['[28,29]', '[0,2]', '[4,9]']`
  - residues: `[0, 2, 4, 9, 13, 14]`
  - anchor_sum_mod15: `12`
  - has_branch_anchor_8_18: `False`
  - selected_c_row: `1`
- a_col `3`
  - anchor_path: `['[7,10]', '[8,18]', '[13,17]', '[7,10]']`
  - anchor_nodes: `['[7,10]', '[8,18]', '[13,17]']`
  - residues: `[2, 3, 7, 8, 10, 13]`
  - anchor_sum_mod15: `13`
  - has_branch_anchor_8_18: `True`
  - selected_c_row: `3`

## Selected pair rows

- candidate `1`: c_row=`0`, a_col=`1`
  - c_path: `[11, 2, 14, 11]`
  - anchor_path: `['[23,24]', '[7,12]', '[4,5]', '[23,24]']`
  - intersection: `[]`
  - c_sum_mod15: `12`, anchor_sum_mod15: `0`
  - has_branch_anchor_8_18: `False`
- candidate `6`: c_row=`1`, a_col=`2`
  - c_path: `[13, 1, 10, 13]`
  - anchor_path: `['[28,29]', '[0,2]', '[4,9]', '[28,29]']`
  - intersection: `[13]`
  - c_sum_mod15: `9`, anchor_sum_mod15: `12`
  - has_branch_anchor_8_18: `False`
- candidate `8`: c_row=`2`, a_col=`0`
  - c_path: `[2, 5, 0, 2]`
  - anchor_path: `['[0,4]', '[2,17]', '[8,18]', '[0,4]']`
  - intersection: `[0, 2]`
  - c_sum_mod15: `7`, anchor_sum_mod15: `4`
  - has_branch_anchor_8_18: `True`
- candidate `15`: c_row=`3`, a_col=`3`
  - c_path: `[4, 5, 2, 4]`
  - anchor_path: `['[7,10]', '[8,18]', '[13,17]', '[7,10]']`
  - intersection: `[2]`
  - c_sum_mod15: `11`, anchor_sum_mod15: `13`
  - has_branch_anchor_8_18: `True`

## Interpretation

The 16-candidate shared_B boundary is a 4 x 4 pairing problem: four C-cycles crossed with four twisted anchor-cycles. The observed selection picks one cell in each row and one cell in each column, so it is a permutation rather than a scalar threshold. In the recovered row/column order, the selected permutation is row -> col [1, 2, 0, 3]. This reframes the missing selector as a coupling/permutation between C-cycle phase and anchor-cycle phase.

## Boundary

This audit does not derive the permutation. It identifies the reduced 4 x 4 selection shape that a future native generator must explain.
