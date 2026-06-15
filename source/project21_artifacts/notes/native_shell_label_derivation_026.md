# Native shell label derivation 026

Status: native_shell_label_derivation_recorded

## Question

Can the shell labels used in 025 be derived natively?

## C branch shell

- xy_to_C_counts: `{'1': 1, '2': 1, '5': 2}`
- iw_from_C_counts: `{'1': 1, '2': 1, '5': 2}`
- native_c_branch_markers: `[5]`
- derived_c_shell_members: `{'ordinary': [0, 1], 'branch': [2, 3]}`
- expected_c_shell_members_from_025: `{'branch': [2, 3], 'ordinary': [0, 1]}`
- c_shell_match_025: `True`

## Anchor branch shell

- repeated_anchor_markers: `['[8,18]']`
- motion_branch_markers: `['[8,18]']`
- native_anchor_branch_markers: `['[8,18]']`
- derived_anchor_shell_members: `{'branch': [0, 3], 'ordinary': [1, 2]}`
- expected_anchor_shell_members_from_025: `{'branch': [0, 3], 'ordinary': [1, 2]}`
- anchor_shell_match_025: `True`

## Verdict

- shell_label_derivation_pass: `True`

## C row derivations

- `{'row_index': 0, 'c_values': [2, 11, 14], 'contains_native_c_branch_marker': False, 'derived_shell': 'ordinary', 'c_sum_mod15': 12, 'selected_anchor_col': 1}`
- `{'row_index': 1, 'c_values': [1, 10, 13], 'contains_native_c_branch_marker': False, 'derived_shell': 'ordinary', 'c_sum_mod15': 9, 'selected_anchor_col': 2}`
- `{'row_index': 2, 'c_values': [0, 2, 5], 'contains_native_c_branch_marker': True, 'derived_shell': 'branch', 'c_sum_mod15': 7, 'selected_anchor_col': 0}`
- `{'row_index': 3, 'c_values': [2, 4, 5], 'contains_native_c_branch_marker': True, 'derived_shell': 'branch', 'c_sum_mod15': 11, 'selected_anchor_col': 3}`

## Anchor column derivations

- `{'col_index': 0, 'anchor_nodes': ['[0,4]', '[2,17]', '[8,18]'], 'contains_native_anchor_branch_marker': True, 'derived_shell': 'branch', 'anchor_sum_mod15': 4, 'selected_c_row': 2}`
- `{'col_index': 1, 'anchor_nodes': ['[23,24]', '[7,12]', '[4,5]'], 'contains_native_anchor_branch_marker': False, 'derived_shell': 'ordinary', 'anchor_sum_mod15': 0, 'selected_c_row': 0}`
- `{'col_index': 2, 'anchor_nodes': ['[28,29]', '[0,2]', '[4,9]'], 'contains_native_anchor_branch_marker': False, 'derived_shell': 'ordinary', 'anchor_sum_mod15': 12, 'selected_c_row': 1}`
- `{'col_index': 3, 'anchor_nodes': ['[7,10]', '[8,18]', '[13,17]'], 'contains_native_anchor_branch_marker': True, 'derived_shell': 'branch', 'anchor_sum_mod15': 13, 'selected_c_row': 3}`

## Reading

This audit derives the shell labels used in the 025 radial phase-lock selector from native observed structure rather than from the reduced matrix by hand. The C branch shell is detected by the repeated XY-to-IW C-junction marker C=5. The anchor branch shell is detected by the repeated column-motion branch anchor [8,18], which is both reused across anchor cycles and branch-like in the shared_B motion graph. These native markers reproduce the 025 shell split exactly.

## Boundary

This derives shell labels, not shell ranks. The radial phase-lock selector still depends on phase-rank order within each shell. Gap A remains open until the ranks, and ultimately the role-labeled shared_B edge selector, are derived from native provenance.
