# Summary of changes
Proved `perm_preserves_sum_of_sq` in `PermSum.lean`. The proof works as follows:

1. **Show `s.image sigma = s`**: Since `sigma` maps every element of `s` back into `s` (hypothesis `hs`), the image is a subset of `s`. Since `sigma` is injective (it's a permutation), the image has the same cardinality as `s`. A subset of a finset with equal cardinality must be equal.

2. **Rewrite the sum**: Using `Finset.sum_image` (which says summing over an image equals summing with the function composed, when the map is injective on the set), we rewrite `∑ x ∈ s, f x` as `∑ x ∈ s, f (sigma x)`.

The proof only uses standard axioms (`propext`, `Classical.choice`, `Quot.sound`).