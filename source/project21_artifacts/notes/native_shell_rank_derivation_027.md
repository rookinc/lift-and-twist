# Native shell rank derivation 027

Status: native_shell_rank_derivation_recorded

## Question

Can the shell ranks used in 025 be derived from native summaries?

## Counts

- candidate_count: `16`
- selected_count: `4`
- c_rank_method_count: `14`
- anchor_rank_method_count: `20`
- selector_test_count: `96`
- exact_selector_count: `24`

## Target native rank selector

- selector: `c_entry_asc__x__anchor_sum_mod15_asc`
- native_rank_derivation_pass: `True`
- target_test: `{'name': 'c_entry_asc__x__anchor_sum_mod15_asc', 'exact': True, 'accepted_count': 4, 'true_positive': 4, 'false_positive': 0, 'true_negative': 12, 'miss': 0, 'accepted_candidate_indices': [1, 6, 8, 15], 'false_positive_candidate_indices': [], 'miss_candidate_indices': [], 'c_rank_method': 'c_entry_asc', 'anchor_rank_method': 'anchor_sum_mod15_asc'}`

## Target C rank details

`{'branch': [{'index': 2, 'rank': 0, 'key': 2}, {'index': 3, 'rank': 1, 'key': 4}], 'ordinary': [{'index': 0, 'rank': 0, 'key': 11}, {'index': 1, 'rank': 1, 'key': 13}]}`

## Target anchor rank details

`{'branch': [{'index': 0, 'rank': 0, 'key': 4}, {'index': 3, 'rank': 1, 'key': 13}], 'ordinary': [{'index': 1, 'rank': 0, 'key': 0}, {'index': 2, 'rank': 1, 'key': 12}]}`

## Exact selectors first 40

- c_entry_asc__x__anchor_max_residue_asc: accepted=`[1, 6, 8, 15]`, fp=`0`, miss=`0`
- c_entry_asc__x__anchor_sum_mod15_asc: accepted=`[1, 6, 8, 15]`, fp=`0`, miss=`0`
- c_entry_asc__x__first_anchor_min_col_asc: accepted=`[1, 6, 8, 15]`, fp=`0`, miss=`0`
- c_entry_desc__x__anchor_max_residue_desc: accepted=`[1, 6, 8, 15]`, fp=`0`, miss=`0`
- c_entry_desc__x__anchor_sum_mod15_desc: accepted=`[1, 6, 8, 15]`, fp=`0`, miss=`0`
- c_entry_desc__x__first_anchor_min_col_desc: accepted=`[1, 6, 8, 15]`, fp=`0`, miss=`0`
- c_exit_asc__x__anchor_min_col_asc: accepted=`[1, 6, 8, 15]`, fp=`0`, miss=`0`
- c_exit_asc__x__anchor_min_residue_asc: accepted=`[1, 6, 8, 15]`, fp=`0`, miss=`0`
- c_exit_asc__x__first_anchor_sum_mod15_desc: accepted=`[1, 6, 8, 15]`, fp=`0`, miss=`0`
- c_exit_desc__x__anchor_min_col_desc: accepted=`[1, 6, 8, 15]`, fp=`0`, miss=`0`
- c_exit_desc__x__anchor_min_residue_desc: accepted=`[1, 6, 8, 15]`, fp=`0`, miss=`0`
- c_exit_desc__x__first_anchor_sum_mod15_asc: accepted=`[1, 6, 8, 15]`, fp=`0`, miss=`0`
- c_min_asc__x__anchor_min_col_asc: accepted=`[1, 6, 8, 15]`, fp=`0`, miss=`0`
- c_min_asc__x__anchor_min_residue_asc: accepted=`[1, 6, 8, 15]`, fp=`0`, miss=`0`
- c_min_asc__x__first_anchor_sum_mod15_desc: accepted=`[1, 6, 8, 15]`, fp=`0`, miss=`0`
- c_min_desc__x__anchor_min_col_desc: accepted=`[1, 6, 8, 15]`, fp=`0`, miss=`0`
- c_min_desc__x__anchor_min_residue_desc: accepted=`[1, 6, 8, 15]`, fp=`0`, miss=`0`
- c_min_desc__x__first_anchor_sum_mod15_asc: accepted=`[1, 6, 8, 15]`, fp=`0`, miss=`0`
- c_sum_mod15_asc__x__anchor_min_col_asc: accepted=`[1, 6, 8, 15]`, fp=`0`, miss=`0`
- c_sum_mod15_asc__x__anchor_min_residue_asc: accepted=`[1, 6, 8, 15]`, fp=`0`, miss=`0`
- c_sum_mod15_asc__x__first_anchor_sum_mod15_desc: accepted=`[1, 6, 8, 15]`, fp=`0`, miss=`0`
- c_sum_mod15_desc__x__anchor_min_col_desc: accepted=`[1, 6, 8, 15]`, fp=`0`, miss=`0`
- c_sum_mod15_desc__x__anchor_min_residue_desc: accepted=`[1, 6, 8, 15]`, fp=`0`, miss=`0`
- c_sum_mod15_desc__x__first_anchor_sum_mod15_asc: accepted=`[1, 6, 8, 15]`, fp=`0`, miss=`0`

## C items

- `{'index': 0, 'shell': 'ordinary', 'c_path': [11, 2, 14, 11], 'c_values': [2, 11, 14], 'c_entry': 11, 'c_mid': 2, 'c_exit': 14, 'c_sum_mod15': 12, 'c_min': 2, 'c_max': 14, 'c_span': 12}`
- `{'index': 1, 'shell': 'ordinary', 'c_path': [13, 1, 10, 13], 'c_values': [1, 10, 13], 'c_entry': 13, 'c_mid': 1, 'c_exit': 10, 'c_sum_mod15': 9, 'c_min': 1, 'c_max': 13, 'c_span': 12}`
- `{'index': 2, 'shell': 'branch', 'c_path': [2, 5, 0, 2], 'c_values': [0, 2, 5], 'c_entry': 2, 'c_mid': 5, 'c_exit': 0, 'c_sum_mod15': 7, 'c_min': 0, 'c_max': 5, 'c_span': 5}`
- `{'index': 3, 'shell': 'branch', 'c_path': [4, 5, 2, 4], 'c_values': [2, 4, 5], 'c_entry': 4, 'c_mid': 5, 'c_exit': 2, 'c_sum_mod15': 11, 'c_min': 2, 'c_max': 5, 'c_span': 3}`

## Anchor items

- `{'index': 0, 'shell': 'branch', 'anchor_nodes': ['[0,4]', '[2,17]', '[8,18]'], 'anchor_sum_mod15': 4, 'anchor_min_col': 0, 'anchor_max_col': 18, 'anchor_min_residue': 0, 'anchor_max_residue': 8, 'anchor_residue_count': 5, 'branch_anchor_position': 2, 'first_anchor_min_col': 0, 'first_anchor_sum_mod15': 4, 'last_anchor_min_col': 8}`
- `{'index': 1, 'shell': 'ordinary', 'anchor_nodes': ['[23,24]', '[7,12]', '[4,5]'], 'anchor_sum_mod15': 0, 'anchor_min_col': 4, 'anchor_max_col': 24, 'anchor_min_residue': 4, 'anchor_max_residue': 12, 'anchor_residue_count': 6, 'branch_anchor_position': -1, 'first_anchor_min_col': 23, 'first_anchor_sum_mod15': 2, 'last_anchor_min_col': 4}`
- `{'index': 2, 'shell': 'ordinary', 'anchor_nodes': ['[28,29]', '[0,2]', '[4,9]'], 'anchor_sum_mod15': 12, 'anchor_min_col': 0, 'anchor_max_col': 29, 'anchor_min_residue': 0, 'anchor_max_residue': 14, 'anchor_residue_count': 6, 'branch_anchor_position': -1, 'first_anchor_min_col': 28, 'first_anchor_sum_mod15': 12, 'last_anchor_min_col': 4}`
- `{'index': 3, 'shell': 'branch', 'anchor_nodes': ['[7,10]', '[8,18]', '[13,17]'], 'anchor_sum_mod15': 13, 'anchor_min_col': 7, 'anchor_max_col': 18, 'anchor_min_residue': 2, 'anchor_max_residue': 13, 'anchor_residue_count': 6, 'branch_anchor_position': 1, 'first_anchor_min_col': 7, 'first_anchor_sum_mod15': 2, 'last_anchor_min_col': 13}`

## Reading

This audit derives the shell-rank part of the 025 radial phase-lock selector from simple native summaries rather than from the selected permutation. The C rank is obtained by ordering C-cycles within each derived shell by their entry value c_path[0] / XY.from_C. The anchor rank is obtained by ordering anchor-cycles within each derived shell by anchor_sum_mod15. Combined with the native shell labels from 026, this shell-rank lock recovers exactly the four selected candidates.

## Boundary

This is still a reduced-universe selector over the 16 candidates. It derives shell labels and shell ranks from native summaries visible in the reduced register shadow, but it does not yet derive the full role-labeled shared_B edge universe from first principles and does not close Gap A.
