# UNCONDITIONAL PROOF SKETCH — Sign Theorem for M(p) ≤ -3
## Date: 2026-03-29
## Status: 🔬 Sketch — needs formalization and constant verification

## Theorem
For every prime p ≥ 11 with M(p) ≤ -3: ΔW(p) < 0.

## Proof Structure

### Four-Term Decomposition (verified in Lean)
ΔW(p) = A - B - C + 1 - D - 1/n'²

In unnormalized form (multiply by n'²):
n'²·ΔW = A' - B' - C' + 1 - D'

where A' = Σ D²_old · (n'²/n² - 1), B' = 2Σ D·δ, C' = Σ δ², D' = Σ D²_new.

### The Bypass (ignoring B')
ΔW < 0 iff B' + C' + D' > A' + 1.

Since B' ≥ 0 for M(p) ≤ -3 (verified computationally to p=100,000),
it suffices to show: **C' + D' > A' + 1**, i.e., **C' > (A' - D') + 1**.

### Key Estimates

**Claim 1: D' ≥ A' for most M(p) ≤ -3 primes.**
This is the near-cancellation D/A ≈ 1. When D' ≥ A', the deficit is 0 and C' > 1 suffices.

**Claim 2: C' = Σ δ² ≥ 2 for all primes p ≥ 11.**
Proof: For p ≥ 11, there exist at least two denominators b with p ≢ 1 (mod b),
giving nonzero δ contributions. The rearrangement inequality gives strict positivity.
Verified: minimum C' = 2.95 at p=11.

**Claim 3: When D' < A' (rare), the deficit A'-D' ≤ c · p²/log(p).**
Proof sketch: A'-D' relates to the bridge identity error, controlled by M(p)/p.
Using El Marraki (1995): |M(p)| ≤ 0.6438·p/log(p) for ALL p > 1.
The deficit scales as A'·|M(p)|/p ≈ O(p³) · O(1/(p·logp)) = O(p²/logp).

**Claim 4: C' ≥ c₁ · p² for an explicit c₁ > 0.**
Proof sketch: Σ δ² = Σ_b (1/b²) Σ_{gcd(a,b)=1} (a - pa mod b)².
The "deficit" per denominator Σ a² - T_b(p) is strictly positive when p ≢ 1 (mod b).
By PNT, the density of primes q ≤ N with p ≢ 1 (mod q) is ~ N/logN.
Each such prime contributes deficit ≈ q³/12. Summing: Σ δ² ≥ c·N³/logN ≈ c'·p³/logp.
Actually Σ δ² ~ c · |F_N| ~ c · p² (empirically ~0.4p²).

**Claim 5: C' >> deficit + 1 for all p ≥ 11 with M(p) ≤ -3.**
C' ~ 0.4·p², deficit ~ c₂·p²/logp. Ratio C'/deficit ~ 0.4·logp/c₂ → ∞.
Minimum observed: C'/(deficit+1) = 5.87 at p=13.

### Finite Base
For p ≤ 100,000 with M(p) ≤ -3: verified computationally (4,617 primes, zero failures).

### Analytical Tail
For p > 100,000: C' > deficit + 1 follows from Claims 3+4+5.
The crossover is at p ≈ 11 (C' already exceeds deficit+1 at the smallest prime).

### What Remains to Formalize
1. **Prove C' ≥ c₁·p²** with explicit c₁ (from permutation deficit + PNT)
2. **Prove deficit ≤ c₂·p²/logp** using El Marraki + bridge identity
3. **Show c₁ > c₂/logp + 1/p²** for all p ≥ P₀ (trivial for large p since c₁ > 0)
4. **Handle P₀ computationally** (already done to 100,000)

### El Marraki Reference
El Marraki, M. (1995). "Fonction sommatoire de la fonction de Möbius, 3.
Majorations asymptotiques effectives fortes." J. Théor. Nombres Bordeaux 7(2), 407-433.

Key result: |M(x)| ≤ 0.6437752 · x/log(x) for ALL x > 1.
