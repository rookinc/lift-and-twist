# Lift & Twist two-readout universe 003

Status: lift_twist_two_readout_universe_recorded

## Claim

The reduced 16-candidate universe can be represented as the product of two readouts of the same hidden four-state system. The C readout order is O0,O1,B0,B1. The anchor readout order is B0,O0,O1,B1. The hidden diagonal of this product is exactly the observed selected set [1,6,8,15].

## Readouts

- C readout order: `['O0', 'O1', 'B0', 'B1']`
- anchor readout order: `['B0', 'O0', 'O1', 'B1']`

## Checks

- generated_candidate_count: `16`
- universe_is_full_16: `True`
- hidden_diagonal_indices: `[1, 6, 8, 15]`
- actual_selected_indices: `[1, 6, 8, 15]`
- diagonal_matches_actual: `True`
- all_rows_match: `True`
- theorem_pass: `True`

## Generated universe

| candidate | C state | anchor state | hidden diagonal | actual selected |
|---:|---|---|---:|---:|
| 0 | O0 | B0 | 0 | 0 |
| 1 | O0 | O0 | 1 | 1 |
| 2 | O0 | O1 | 0 | 0 |
| 3 | O0 | B1 | 0 | 0 |
| 4 | O1 | B0 | 0 | 0 |
| 5 | O1 | O0 | 0 | 0 |
| 6 | O1 | O1 | 1 | 1 |
| 7 | O1 | B1 | 0 | 0 |
| 8 | B0 | B0 | 1 | 1 |
| 9 | B0 | O0 | 0 | 0 |
| 10 | B0 | O1 | 0 | 0 |
| 11 | B0 | B1 | 0 | 0 |
| 12 | B1 | B0 | 0 | 0 |
| 13 | B1 | O0 | 0 | 0 |
| 14 | B1 | O1 | 0 | 0 |
| 15 | B1 | B1 | 1 | 1 |

## Boundary

This proves a two-readout representation of the copied Project 21 reduced universe. It does not derive the two readouts from one local answer cell, does not derive the readout payloads natively, and does not close Gap A.
