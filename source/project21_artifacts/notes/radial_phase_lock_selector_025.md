# Radial phase-lock selector 025

Status: radial_phase_lock_selector_recorded

## Counts

- candidate_count: `16`
- selected_count: `4`
- selected_permutation: `{'0': 1, '1': 2, '2': 0, '3': 3}`
- permutation_cycles: `[[0, 1, 2], [3]]`
- permutation_order: `3`

## Shells

- c_shell_members: `{'ordinary': [0, 1], 'branch': [2, 3]}`
- anchor_shell_members: `{'branch': [0, 3], 'ordinary': [1, 2]}`

## Selector scores

- literal_024_permutation_lookup: exact=`True`, accepted=`4`, fp=`0`, miss=`0`, accepted_indices=`[1, 6, 8, 15]`
- order3_plus_fixed_from_024_permutation_shape: exact=`True`, accepted=`4`, fp=`0`, miss=`0`, accepted_indices=`[1, 6, 8, 15]`
- radial_phase_lock_shell_and_rank: exact=`True`, accepted=`4`, fp=`0`, miss=`0`, accepted_indices=`[1, 6, 8, 15]`
- sum_delta_mod15_eq_3: exact=`False`, accepted=`2`, fp=`0`, miss=`2`, accepted_indices=`[1, 6]`
- sum_delta_mod15_eq_12: exact=`False`, accepted=`1`, fp=`0`, miss=`3`, accepted_indices=`[8]`
- sum_delta_mod15_eq_2: exact=`False`, accepted=`1`, fp=`0`, miss=`3`, accepted_indices=`[15]`
- affine_mod4_col_eq_1_row_plus_1: exact=`False`, accepted=`4`, fp=`2`, miss=`2`, accepted_indices=`[1, 6, 11, 12]`
- affine_mod4_col_eq_2_row_plus_0: exact=`False`, accepted=`4`, fp=`2`, miss=`2`, accepted_indices=`[0, 6, 8, 14]`
- affine_mod4_col_eq_2_row_plus_1: exact=`False`, accepted=`4`, fp=`2`, miss=`2`, accepted_indices=`[1, 7, 9, 15]`
- affine_mod4_col_eq_3_row_plus_2: exact=`False`, accepted=`4`, fp=`2`, miss=`2`, accepted_indices=`[2, 5, 8, 15]`
- branch_gate_only_shell_match: exact=`False`, accepted=`8`, fp=`4`, miss=`0`, accepted_indices=`[1, 2, 5, 6, 8, 11, 12, 15]`
- shell_rank_match_only: exact=`False`, accepted=`8`, fp=`4`, miss=`0`, accepted_indices=`[0, 1, 6, 7, 8, 9, 14, 15]`
- sum_delta_mod15_eq_0: exact=`False`, accepted=`1`, fp=`1`, miss=`4`, accepted_indices=`[2]`
- sum_delta_mod15_eq_10: exact=`False`, accepted=`1`, fp=`1`, miss=`4`, accepted_indices=`[4]`
- sum_delta_mod15_eq_5: exact=`False`, accepted=`1`, fp=`1`, miss=`4`, accepted_indices=`[10]`
- sum_delta_mod15_eq_7: exact=`False`, accepted=`1`, fp=`1`, miss=`4`, accepted_indices=`[0]`
- intersection_size_eq_0: exact=`False`, accepted=`3`, fp=`2`, miss=`3`, accepted_indices=`[1, 4, 5]`
- sum_delta_mod15_eq_1: exact=`False`, accepted=`2`, fp=`2`, miss=`4`, accepted_indices=`[3, 14]`
- sum_delta_mod15_eq_4: exact=`False`, accepted=`2`, fp=`2`, miss=`4`, accepted_indices=`[7, 13]`
- sum_delta_mod15_eq_6: exact=`False`, accepted=`2`, fp=`2`, miss=`4`, accepted_indices=`[5, 11]`
- sum_delta_mod15_eq_8: exact=`False`, accepted=`2`, fp=`2`, miss=`4`, accepted_indices=`[9, 12]`
- affine_mod4_col_eq_0_row_plus_0: exact=`False`, accepted=`4`, fp=`3`, miss=`3`, accepted_indices=`[0, 4, 8, 12]`
- affine_mod4_col_eq_0_row_plus_1: exact=`False`, accepted=`4`, fp=`3`, miss=`3`, accepted_indices=`[1, 5, 9, 13]`
- affine_mod4_col_eq_0_row_plus_2: exact=`False`, accepted=`4`, fp=`3`, miss=`3`, accepted_indices=`[2, 6, 10, 14]`
- affine_mod4_col_eq_0_row_plus_3: exact=`False`, accepted=`4`, fp=`3`, miss=`3`, accepted_indices=`[3, 7, 11, 15]`
- intersection_size_eq_1: exact=`False`, accepted=`6`, fp=`4`, miss=`2`, accepted_indices=`[0, 3, 6, 9, 11, 15]`
- intersection_size_eq_2: exact=`False`, accepted=`7`, fp=`6`, miss=`3`, accepted_indices=`[2, 7, 8, 10, 12, 13, 14]`

## Exact selectors

- literal_024_permutation_lookup: accepted_indices=`[1, 6, 8, 15]`
- order3_plus_fixed_from_024_permutation_shape: accepted_indices=`[1, 6, 8, 15]`
- radial_phase_lock_shell_and_rank: accepted_indices=`[1, 6, 8, 15]`

## Shell table

- `{'kind': 'c_row', 'index': 0, 'shell': 'ordinary', 'shell_rank': 0, 'contains_C5': False, 'c_values': [2, 11, 14], 'c_sum_mod15': 12}`
- `{'kind': 'c_row', 'index': 1, 'shell': 'ordinary', 'shell_rank': 1, 'contains_C5': False, 'c_values': [1, 10, 13], 'c_sum_mod15': 9}`
- `{'kind': 'c_row', 'index': 2, 'shell': 'branch', 'shell_rank': 0, 'contains_C5': True, 'c_values': [0, 2, 5], 'c_sum_mod15': 7}`
- `{'kind': 'c_row', 'index': 3, 'shell': 'branch', 'shell_rank': 1, 'contains_C5': True, 'c_values': [2, 4, 5], 'c_sum_mod15': 11}`
- `{'kind': 'anchor_col', 'index': 0, 'shell': 'branch', 'shell_rank': 0, 'has_branch_anchor_8_18': True, 'anchor_nodes': ['[0,4]', '[2,17]', '[8,18]'], 'residues': [0, 2, 3, 4, 8], 'anchor_sum_mod15': 4}`
- `{'kind': 'anchor_col', 'index': 1, 'shell': 'ordinary', 'shell_rank': 0, 'has_branch_anchor_8_18': False, 'anchor_nodes': ['[23,24]', '[7,12]', '[4,5]'], 'residues': [4, 5, 7, 8, 9, 12], 'anchor_sum_mod15': 0}`
- `{'kind': 'anchor_col', 'index': 2, 'shell': 'ordinary', 'shell_rank': 1, 'has_branch_anchor_8_18': False, 'anchor_nodes': ['[28,29]', '[0,2]', '[4,9]'], 'residues': [0, 2, 4, 9, 13, 14], 'anchor_sum_mod15': 12}`
- `{'kind': 'anchor_col', 'index': 3, 'shell': 'branch', 'shell_rank': 1, 'has_branch_anchor_8_18': True, 'anchor_nodes': ['[7,10]', '[8,18]', '[13,17]'], 'residues': [2, 3, 7, 8, 10, 13], 'anchor_sum_mod15': 13}`

## Candidate rows

- candidate=`0`, selected=`False`, c_row=`0`, a_col=`0`, c_shell=`ordinary`, anchor_shell=`branch`, c_rank=`0`, a_rank=`0`, radial_phase_lock=`False`
- candidate=`1`, selected=`True`, c_row=`0`, a_col=`1`, c_shell=`ordinary`, anchor_shell=`ordinary`, c_rank=`0`, a_rank=`0`, radial_phase_lock=`True`
- candidate=`2`, selected=`False`, c_row=`0`, a_col=`2`, c_shell=`ordinary`, anchor_shell=`ordinary`, c_rank=`0`, a_rank=`1`, radial_phase_lock=`False`
- candidate=`3`, selected=`False`, c_row=`0`, a_col=`3`, c_shell=`ordinary`, anchor_shell=`branch`, c_rank=`0`, a_rank=`1`, radial_phase_lock=`False`
- candidate=`4`, selected=`False`, c_row=`1`, a_col=`0`, c_shell=`ordinary`, anchor_shell=`branch`, c_rank=`1`, a_rank=`0`, radial_phase_lock=`False`
- candidate=`5`, selected=`False`, c_row=`1`, a_col=`1`, c_shell=`ordinary`, anchor_shell=`ordinary`, c_rank=`1`, a_rank=`0`, radial_phase_lock=`False`
- candidate=`6`, selected=`True`, c_row=`1`, a_col=`2`, c_shell=`ordinary`, anchor_shell=`ordinary`, c_rank=`1`, a_rank=`1`, radial_phase_lock=`True`
- candidate=`7`, selected=`False`, c_row=`1`, a_col=`3`, c_shell=`ordinary`, anchor_shell=`branch`, c_rank=`1`, a_rank=`1`, radial_phase_lock=`False`
- candidate=`8`, selected=`True`, c_row=`2`, a_col=`0`, c_shell=`branch`, anchor_shell=`branch`, c_rank=`0`, a_rank=`0`, radial_phase_lock=`True`
- candidate=`9`, selected=`False`, c_row=`2`, a_col=`1`, c_shell=`branch`, anchor_shell=`ordinary`, c_rank=`0`, a_rank=`0`, radial_phase_lock=`False`
- candidate=`10`, selected=`False`, c_row=`2`, a_col=`2`, c_shell=`branch`, anchor_shell=`ordinary`, c_rank=`0`, a_rank=`1`, radial_phase_lock=`False`
- candidate=`11`, selected=`False`, c_row=`2`, a_col=`3`, c_shell=`branch`, anchor_shell=`branch`, c_rank=`0`, a_rank=`1`, radial_phase_lock=`False`
- candidate=`12`, selected=`False`, c_row=`3`, a_col=`0`, c_shell=`branch`, anchor_shell=`branch`, c_rank=`1`, a_rank=`0`, radial_phase_lock=`False`
- candidate=`13`, selected=`False`, c_row=`3`, a_col=`1`, c_shell=`branch`, anchor_shell=`ordinary`, c_rank=`1`, a_rank=`0`, radial_phase_lock=`False`
- candidate=`14`, selected=`False`, c_row=`3`, a_col=`2`, c_shell=`branch`, anchor_shell=`ordinary`, c_rank=`1`, a_rank=`1`, radial_phase_lock=`False`
- candidate=`15`, selected=`True`, c_row=`3`, a_col=`3`, c_shell=`branch`, anchor_shell=`branch`, c_rank=`1`, a_rank=`1`, radial_phase_lock=`True`

## Reading

This audit tests the radial phase-lock reading suggested by the hand sketch. The 024 permutation is modeled as a shell gate plus a phase-rank lock: C-cycles containing C=5 pair with anchor-cycles containing the branch anchor [8,18], while ordinary C-cycles pair with ordinary anchor-cycles. Within each shell, the recovered matrix order supplies a phase rank. The radial phase-lock selector accepts exactly the four observed cells. This is a compact model of the 4-of-16 selection, but it is still conditional because the shell order/rank must be derived from native register provenance rather than read from the reduced matrix.

## Boundary

This does not close Gap A. It derives an exact selector only after accepting the shell markers and matrix-order phase ranks from the reduced 024 representation. The next step is to derive those shell/rank labels natively.
