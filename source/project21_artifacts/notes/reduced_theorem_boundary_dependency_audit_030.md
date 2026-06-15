# Reduced theorem boundary dependency audit 030

Status: reduced_theorem_boundary_dependency_audit_recorded

## Verdict

- boundary_pass: `True`
- main_has_section_input: `True`
- paper_missing_required_phrases: `[]`
- closed_item_count: `5`
- open_item_count: `4`

## Proof checks

- 022_reduced_boundary_has_16_candidates: `True`
- 022_observed_edge_filter_exact: `True`
- 026_shell_labels_derived: `True`
- 027_shell_ranks_derived: `True`
- 028_reduced_theorem_pass: `True`
- 029_section_written_from_028: `True`

## Current best statement

The reduced-universe shell-rank selector is proved exactly inside the 16-candidate shared_B reduced universe. Native shell labels and native shell ranks select exactly the four observed shared_B cycles with no false positives and no misses.

## Remaining Gap A problem

Derive the reduced 16-candidate universe, or the full role-labeled shared_B edge universe, from native provenance without using observed C-cycle and anchor-cycle support as an upstream assumption.

## Dependency ledger

- Observed C-cycle support
  - status: `assumed_from_reduced_universe`
  - artifact: `022/024`
  - claim: Four observed C-cycles are used to form the reduced universe.
  - gap_status: `open_upstream_dependency`
- Twisted anchor-cycle support
  - status: `assumed_from_reduced_universe`
  - artifact: `022/024`
  - claim: Four observed twisted anchor-cycles are used to form the reduced universe.
  - gap_status: `open_upstream_dependency`
- Reduced 16-candidate universe
  - status: `bounded_construct`
  - artifact: `022`
  - claim: C-cycle support crossed with twisted anchor-cycle support gives 16 candidates.
  - gap_status: `not_first_principles_native_generation`
- C shell label
  - status: `derived_native_marker`
  - artifact: `026`
  - claim: C branch shell is derived from repeated C-junction marker C=5.
  - gap_status: `closed_inside_reduced_theorem`
- Anchor shell label
  - status: `derived_native_marker`
  - artifact: `026`
  - claim: Anchor branch shell is derived from repeated branch anchor [8,18].
  - gap_status: `closed_inside_reduced_theorem`
- C shell rank
  - status: `derived_native_summary`
  - artifact: `027`
  - claim: C rows rank by ascending C entry / XY.from_C within shell.
  - gap_status: `closed_inside_reduced_theorem`
- Anchor shell rank
  - status: `derived_native_summary`
  - artifact: `027`
  - claim: Anchor columns rank by ascending anchor_sum_mod15 within shell.
  - gap_status: `closed_inside_reduced_theorem`
- Reduced selector
  - status: `proved_exact`
  - artifact: `028`
  - claim: Same shell and same rank selects exactly [1,6,8,15] with no false positives or misses.
  - gap_status: `proved_inside_reduced_universe`
- Full role-labeled shared_B edge universe
  - status: `not_derived`
  - artifact: `boundary`
  - claim: The full edge universe remains upstream of this theorem.
  - gap_status: `Gap_A_open`

## Reading

This audit confirms that the manuscript theorem section preserves the right boundary. The selector inside the reduced universe is theorem-grade; the reduced universe itself remains the open upstream generator problem.
