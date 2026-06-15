# Lift & Twist readout order rule 004

Status: lift_twist_readout_order_rule_recorded

## Claim

The two readout orders used in 003 are reproduced by a compact Lift & Twist order rule. The C readout orders states by ordinary-before-branch shell order with ascending rank. The anchor readout is obtained by moving the first branch state B0 to the front, then reading ordinary ranks, then leaving the remaining branch state B1 terminal. This derived order induces the visible permutation [1,2,0,3] and the diagonal candidates [1,6,8,15].

## Readout order rule

- C order rule: `ordinary shell first, branch shell second, ranks ascending inside each shell`
- anchor order rule: `first branch rank wraps to front, ordinary ranks follow, remaining branch ranks stay terminal`

## Orders

- observed C order: `['O0', 'O1', 'B0', 'B1']`
- derived C order: `['O0', 'O1', 'B0', 'B1']`
- observed anchor order: `['B0', 'O0', 'O1', 'B1']`
- derived anchor order: `['B0', 'O0', 'O1', 'B1']`

## Permutation

- observed visible permutation: `[1, 2, 0, 3]`
- derived visible permutation: `[1, 2, 0, 3]`
- permutation cycles: `[[0, 1, 2], [3]]`

## Diagonal

- derived diagonal indices: `[1, 6, 8, 15]`
- observed diagonal indices: `[1, 6, 8, 15]`
- observed actual selected indices: `[1, 6, 8, 15]`

## Checks

- state_sets_match: `True`
- derived_c_order_matches_observed: `True`
- derived_anchor_order_matches_observed: `True`
- derived_permutation_matches_observed: `True`
- derived_diagonal_matches_003_diagonal: `True`
- derived_diagonal_matches_actual_selected: `True`
- project22_002_theorem_pass: `True`
- project22_003_theorem_pass: `True`
- theorem_pass: `True`

## Boundary

This derives the readout order rule inside the four-state representation. It does not yet derive the hidden states or their payloads from one local answer cell, and it does not close Gap A.
