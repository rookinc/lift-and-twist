# Lift & Twist payload state reconstruction 005

Status: lift_twist_payload_state_reconstruction_recorded

## Claim

The hidden four states used by Lift & Twist can be reconstructed from readout payload markers. On the C side, branch states are exactly those whose C payload contains 5, ranked by C entry. On the anchor side, branch states are exactly those whose anchor payload contains [8,18], ranked by anchor_sum_mod15. These payload-derived states reproduce the two readout orders and recover the selected diagonal [1,6,8,15].

## Payload state rules

- c_shell_rule: `branch iff c_values contains 5; otherwise ordinary`
- c_rank_rule: `rank by ascending c_entry within shell`
- anchor_shell_rule: `branch iff anchor payload contains node [8,18]; otherwise ordinary`
- anchor_rank_rule: `rank by ascending anchor_sum_mod15 within shell`

## Orders

- observed C order: `['O0', 'O1', 'B0', 'B1']`
- derived C order: `['O0', 'O1', 'B0', 'B1']`
- observed anchor order: `['B0', 'O0', 'O1', 'B1']`
- derived anchor order: `['B0', 'O0', 'O1', 'B1']`

## Diagonal

- derived diagonal indices: `[1, 6, 8, 15]`
- actual selected indices: `[1, 6, 8, 15]`

## C state reconstruction

- row `0` observed `O0` derived `O0` shell `ordinary` rank_key `11`
- row `1` observed `O1` derived `O1` shell `ordinary` rank_key `13`
- row `2` observed `B0` derived `B0` shell `branch` rank_key `2`
- row `3` observed `B1` derived `B1` shell `branch` rank_key `4`

## Anchor state reconstruction

- col `0` observed `B0` derived `B0` shell `branch` rank_key `4`
- col `1` observed `O0` derived `O0` shell `ordinary` rank_key `0`
- col `2` observed `O1` derived `O1` shell `ordinary` rank_key `12`
- col `3` observed `B1` derived `B1` shell `branch` rank_key `13`

## Checks

- derived_c_order_matches_observed: `True`
- derived_anchor_order_matches_observed: `True`
- c_state_matches_observed: `True`
- anchor_state_matches_observed: `True`
- derived_diagonal_matches_actual: `True`
- all_candidate_matches_actual: `True`
- project22_003_theorem_pass: `True`
- project22_004_theorem_pass: `True`
- theorem_pass: `True`

## Boundary

This reconstructs hidden state labels from the copied reduced-universe payloads. It does not derive the payloads themselves from one local answer cell, does not derive the reduced 16-candidate universe from native provenance, and does not close Gap A.
