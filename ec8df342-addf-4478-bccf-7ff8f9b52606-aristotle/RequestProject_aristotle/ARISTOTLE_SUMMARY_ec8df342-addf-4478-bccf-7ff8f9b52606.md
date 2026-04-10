# Summary of changes
Confirmed: the `sorry` at line 116 of `MediantMinimality.lean` does **not** need closing. It is inside a block comment (`/- ... -/`) that documents an intentionally false version of `farey_gap_upper_bound`. The comment explains the counterexample (a=0, b=1, c=1, d=1, N=5) showing why the statement is false.

The corrected version of `farey_gap_upper_bound` — with a weaker conclusion `≤ 1/b` instead of `≤ 1/N`, and without the `N` parameter — is already fully proved immediately below the comment block.

The file builds successfully with no errors and no active (uncommented) `sorry` statements.