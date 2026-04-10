# Summary of changes
Proved the theorem `mul_p_perm` in `MulPPerm.lean`. The proof works by:

1. Rewriting `p * a` as `(p * a) % b + b * ((p * a) / b)` using `Nat.mod_add_div`.
2. Simplifying the coprimality condition with `simp_all` to reduce it to showing coprimality of the components.
3. Concluding with `Nat.Coprime.mul_left hp ha`, which combines the coprimality of `p` and `a` with `b`.

The proof compiles cleanly with no warnings and only uses standard axioms (propext, Classical.choice, Quot.sound).