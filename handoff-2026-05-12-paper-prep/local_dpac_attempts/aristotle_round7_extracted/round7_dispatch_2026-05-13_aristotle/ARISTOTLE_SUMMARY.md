# Summary of changes for run 0873e8c7-b210-43a4-b2d1-d723f727e6cd
## Completed: Ramanujan Sum Formalization + Unconditional Farey Bridge Identity

### New file: `formal-conjectures/RamanujanSum.lean`

This file contains a complete, sorry-free formalization of the Ramanujan sum theory needed for the Farey Bridge Identity:

1. **Geometric sum identity** (`geom_sum_roots_of_unity`): For q ≥ 1, ∑_{j=0}^{q-1} exp(2πi j k / q) = 0 when q ∤ k.

2. **Primitive roots sum = Möbius** (`primRootsSum_eq_moebius`): The sum of all primitive q-th roots of unity equals μ(q). Proved by strong induction, showing both sides satisfy the same Dirichlet-convolution recurrence (S * ζ = 1 = μ * ζ).

3. **Ramanujan sum at coprime arguments** (`ramanujanSum_eq_moebius_of_coprime`): c_q(n) = μ(q) when gcd(n,q) = 1. Proved via the permutation argument: multiplication by n permutes coprime residues mod q.

4. **FareySet decomposition** (`farey_ramanujan_decomp`): For prime p, the exponential sum over FareySet(p−1) decomposes as 1 + ∑_{b=1}^{p-1} μ(b). This directly discharges the `h_ramanujan_decomp` hypothesis from `FareyBridgeIdentity.lean`.

### Modified file: `formal-conjectures/FareyBridgeIdentity.lean`

Added `import RamanujanSum` and the new theorem:

- **`farey_bridge_identity_unconditional`**: The Farey Bridge Identity (Lemma 3.1 of Shai 2026) is now fully unconditional — it requires only `Nat.Prime p` with no additional hypotheses. The `h_ramanujan_decomp` hypothesis is discharged using `RamanujanSum.farey_ramanujan_decomp`.

### Modified file: `lakefile.toml`

Added `RamanujanSum` as a build target and included it in the `FormalConjectures` roll-up.

### Verification

- **No `sorry`** in either file.
- **No `axiom` declarations** added.
- **Standard axioms only**: `propext`, `Classical.choice`, `Quot.sound` (verified via `#print axioms`).
- **Full project builds successfully** (8036 jobs, no errors).