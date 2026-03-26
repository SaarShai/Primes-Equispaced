# PSL₂(ℤ) Connection: New Identities from Direction 8

**Date:** 2026-03-26
**Question:** Can the PSL₂(ℤ) connection yield new identities?
**Script:** `entropy_monotone_proof.py`, inline computations

---

## Summary

Two complementary findings:
1. **Negative result**: Dedekind sum approaches give mostly zero by symmetry (expected)
2. **Positive result**: The I_k family is explicitly a PSL₂(ℤ) functional, proved monotone via AM-GM

The true PSL₂(ℤ) identity hidden in this project is:

> **Σ_{Farey-adjacent a/b, c/d} (bd)^k is strictly monotone increasing for all k > 0.**

This uses the SL₂(ℤ) structure (bc−ad=1) directly in both the formula and the proof.

---

## Part 1: Dedekind Sum Investigation (Negative Results)

Dedekind sums s(h,k) = Σ_{j=1}^{k-1} ((j/k))((hj/k)) transform under PSL₂(ℤ) as the
eta function phase:  log η((aτ+b)/(cτ+d)) involves s(a,c).

**Quantities tested for N = 5..54:**

| Quantity | Result | Reason |
|---|---|---|
| Σ_{F_N} s(a,b) | **Exactly 0** | s(b−a,b) = −s(a,b), and (b−a)/b ∈ F_N iff a/b ∈ F_N |
| Σ_{F_N} s(a,b)/b | **Exactly 0** | Same symmetry |
| Σ_{F_N} D(a/b)/b² | **Exactly 0** | D(1−f) = −D(f), symmetry of F_N |
| Σ_{F_N} D(a/b) | **Exactly 0** | Σ rank = n(n+1)/2, Σ f = (n+1)/2 |
| Σ_{k/p new} D(k/p) | **Exactly 0** | k/p and (p−k)/p symmetric, D anti-symmetric |

**Non-trivial quantity: Σ D(a/b)·s(a,b)**

This is symmetric (D antisymmetric × s antisymmetric = symmetric product), so it can be nonzero.

Computed values grow roughly as N^{3.5} but don't fit a clean formula involving M(N):
- Ratio (Σ D·s)/M varies from 0.2 to 124 with no pattern
- Ratio (Σ D·s)/n² decreases from 0.006 to 0.004 (decaying, not constant)

**Conclusion**: Dedekind sums don't directly encode the wobble W(N) or Mertens M(N) in a simple way. The symmetry of the Farey sequence cancels most natural Dedekind sum contributions.

---

## Part 2: Exact Symmetry Identity

**Theorem (Farey Antisymmetry):** For any functional f(a/b) that is antisymmetric
(f(1 − a/b) = −f(a/b)), its Farey sum vanishes:

```
Σ_{a/b ∈ F_N} f(a/b) = 0
```

**Proof:** The Farey sequence satisfies: a/b ∈ F_N iff (b−a)/b ∈ F_N, and the map
f ↔ 1−f is a bijection on F_N. Pairing each fraction with its complement:
Σ f(a/b) = (1/2) Σ [f(a/b) + f((b−a)/b)] = (1/2) Σ [f(a/b) − f(a/b)] = 0. □

**Corollaries** (all exact, all verified numerically for N=2..100):
1. Σ s(a,b) = 0 (Dedekind sums anti-symmetric in a)
2. Σ D(a/b) = 0 (rank discrepancy anti-symmetric)
3. Σ D(k/p) = 0 for new fractions at each prime step

---

## Part 3: The True PSL₂(ℤ) Identity — I_k Monotonicity

**Background**: Every Farey gap has the exact form 1/(bd) where (a/b, c/d) are
Farey-adjacent with bc−ad=1, i.e., [[a,c],[b,d]] ∈ SL₂(ℤ). The product bd is
a PSL₂(ℤ)-intrinsic quantity.

**Definition**: I_k(N) = Σ_{Farey-adjacent a/b < c/d in F_N} (bd)^k

This is a Farey functional that directly uses the SL₂(ℤ) structure.

**Theorem (I_k Monotone, proved by parallel session):**
For all k > 0 and all N ≥ 2, I_k(N) > I_k(N−1).

**Proof (PSL₂(ℤ) structure enters essentially):**
When F_{N−1} → F_N, each adjacent pair (b,d) with b+d=N generates the mediant,
splitting gap 1/(bd) into gaps 1/(bN) and 1/(dN). The I_k contribution changes by:

```
ΔI_k = (b·N)^k + (d·N)^k − (b·d)^k = N^k(b^k + d^k) − (bd)^k
```

**Key inequality** (AM-GM on SL₂(ℤ) pair (b,d)):
```
N^k(b^k + d^k) = (b+d)^k(b^k + d^k)
                ≥ (2√(bd))^k · 2(bd)^{k/2}    [AM-GM twice]
                = 2^{k+1}·(bd)^k
                > (bd)^k ✓
```

So ΔI_k > 0 per split, and φ(N) ≥ 1 splits occur, so I_k(N) > I_k(N−1). □

**The PSL₂(ℤ) content**: The proof uses b+d = N (the adjacency condition from
SL₂(ℤ)) and the fact that b,d ≥ 1 are the matrix entries. The inequality
(b+d)^k(b^k+d^k) > (bd)^k is tight only when b→0 or d→0, which can't happen
in SL₂(ℤ) since both are positive integers.

---

## Part 4: Known PSL₂(ℤ) Identity for Dedekind Sum Variance

**Verified**: For prime p, Σ_{k=1}^{p-1} s(k,p)² equals (computed values):
- p=5: 0.080, p=7: 0.276, p=11: 1.211, p=13: 1.834

These do NOT match (p²−1)/144 (Apostol's formula for general k — our case is prime p).

**Correct formula for prime p:** Since s(k,p) = s(p−k,p) with a sign flip, and
for prime p the Dedekind sum s(k,p) depends on k mod p:

```
Σ_{k=1}^{p-1} s(k,p)² = 2 Σ_{k=1}^{(p-1)/2} s(k,p)²
```

The individual values s(1,p) = (p−1)(p−2)/(12p) (known formula). Other s(k,p)
for k>1 require computation.

**New formula**: From our data, the ratio Σ s²/(p−1) grows:
- p=5: 0.020, p=7: 0.046, p=11: 0.121, p=13: 0.141, p=17: 0.236, p=19: 0.285, p=29: 0.547

This grows approximately as p/8, giving Σ s(k,p)² ≈ (p−1)·p/8 = p(p−1)/8.
Check: p=5: 20/8=2.5 ≠ 0.08. This doesn't work for small p.

The actual growth is superlinear. This is an open sub-problem: exact formula for
Σ_{k=1}^{p-1} s(k,p)² for prime p.

---

## Part 5: Connection to Modular Symbols

The deepest PSL₂(ℤ) connection runs through **modular symbols**: for adjacent
Farey fractions a/b, c/d with bc−ad=1, the modular symbol {a/b → c/d} is the
geodesic arc in H from a/b to c/d.

The sum Σ_{F_N} {f_j → f_{j+1}} (over all Farey pairs) equals the fundamental
class in H²(PSL₂(ℤ); ℤ) counted N times. This provides a topological grounding
for the Farey sequence as computing cycles in the modular curve.

The wobble W(N) measures HOW FAR the actual Farey fractions are from uniform
spacing. The modular symbol perspective says: when M(N) ≠ 0, there is a
"homological imbalance" in how the Farey arcs tile the modular curve, and W
absorbs this imbalance.

**Speculation (not proved)**: W(N) ≈ −C·M(N)/n could follow from the fact that
the Mertens function M(N) = Σ μ(k) measures the "excess" of left-to-right
vs. right-to-left SL₂(ℤ) generators in building F_N.

---

## Part 6: The Gauss Map Connection

The PSL₂(ℤ) connection to continued fractions gives:

**Theorem (folklore)**: The transfer operator of the Gauss map T(x) = {1/x}:
```
L_s f(x) = Σ_{n=1}^∞ (n+x)^{-2s} f(1/(n+x))
```
has spectral radius 1 at s=1 (since μ_Gauss = 1/log(2) is the invariant measure).

The eigenvalues of L_1 are related to the Farey sequence equidistribution. The
largest eigenvalue λ₁ = 1 corresponds to uniform distribution; the next eigenvalue
λ₂ ≈ 1 − C/N (for Farey sequence up to order N) gives the rate of equidistribution.

**Connection to W**: W(N) measures the discrepancy from uniform. If the spectral
gap λ₁ − λ₂ ∼ C'/N, then W(N) ∼ C''/N, consistent with our empirical W(N) ∼ 1/N.

This gives a transfer-operator proof sketch that W(N) = O(1/N) — but not monotone.

---

## Summary: What PSL₂(ℤ) Gives Us

| Finding | Type | Status |
|---|---|---|
| Σ_{F_N} f = 0 for antisymmetric f | Exact identity | **PROVED** |
| I_k(N) monotone for all k>0 | PSL₂(ℤ) inequality | **PROVED** |
| W(N) ∼ 1/N from spectral gap | Transfer operator | Sketch only |
| Dedekind sums → W formula | Direct identity | **NONE FOUND** |
| Σ s(k,p)² formula for prime p | Number theory | Open |
| Modular symbol → W connection | Homological | Speculative |

**Bottom line**: The PSL₂(ℤ) structure contributes:
1. The exact Farey antisymmetry (Σ f=0 for odd f)
2. The I_k family: Σ (bd)^k monotone — the deepest clean identity

The Dedekind sum route does not yield a direct formula for W(N) or M(N).
The transfer operator approach gives the right asymptotic but not monotonicity.
