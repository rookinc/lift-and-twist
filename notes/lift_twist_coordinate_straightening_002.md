# Lift & Twist coordinate straightening 002

Status: lift_twist_coordinate_straightening_recorded

## Claim

The visible selector permutation [1,2,0,3] is induced by identity in lifted shell/rank coordinates. The C readout orders hidden states as O0,O1,B0,B1; the anchor readout orders the same states as B0,O0,O1,B1. Therefore the hidden identity map appears visibly as [1,2,0,3] = (0 1 2)(3).

## Readout orders

- C readout order: `['O0', 'O1', 'B0', 'B1']`
- anchor readout order: `['B0', 'O0', 'O1', 'B1']`

## Visible selector

- visible_selected_col_by_row: `{'0': 1, '1': 2, '2': 0, '3': 3}`
- visible_permutation_list: `[1, 2, 0, 3]`
- induced_visible_permutation_list: `[1, 2, 0, 3]`
- permutation_cycles: `[[0, 1, 2], [3]]`

## Checks

- readout_state_sets_match: `True`
- hidden_identity_all_match: `True`
- visible_matches_induced: `True`
- project21_028_theorem_pass: `True`
- theorem_pass: `True`

## Straightening rows

- row `0` -> col `1`
  - c_state: `O0`
  - anchor_state: `O0`
  - hidden_identity_match: `True`
  - visible_matches_induced: `True`
- row `1` -> col `2`
  - c_state: `O1`
  - anchor_state: `O1`
  - hidden_identity_match: `True`
  - visible_matches_induced: `True`
- row `2` -> col `0`
  - c_state: `B0`
  - anchor_state: `B0`
  - hidden_identity_match: `True`
  - visible_matches_induced: `True`
- row `3` -> col `3`
  - c_state: `B1`
  - anchor_state: `B1`
  - hidden_identity_match: `True`
  - visible_matches_induced: `True`

## Boundary

This proves coordinate straightening for the copied Project 21 reduced universe. It does not derive the reduced 16-candidate universe itself and does not close Gap A.
