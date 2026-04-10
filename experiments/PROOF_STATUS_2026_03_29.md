# Sign Theorem Proof Status — 2026-03-29

## The Goal
Prove **B + C > 0** for all primes p ≥ 11, equivalently R(p) = ⟨D, δ⟩/||δ||² > -1/2.

## Empirical Status (STRONG)
- **B+C > 0 verified for ALL 1895 primes to p = 99,991** (11,605s computation, 2026-03-28)
- **R(p) ≥ R(11) ≈ -0.259** confirmed for all 164 primes to p = 997 (exact Fraction arithmetic)
- R(11) appears to be the **global minimum** — never violated
- Margin from -1/2: **0.241** (R(11) + 0.5 = 0.241)
- Second worst: R(223) ≈ -0.158

## Analytical Approaches — ALL FAILED

### 1. Cauchy-Schwarz (DEAD)
- ||D||/||δ|| grows as ~√p (2.67 at p=11, 18.3 at p=293)
- CS gives |B| ≤ 2||D||·||δ|| ~ p², but C ~ p^1.5 → CS is 44x too loose at p=11, worse for large p
- **Status: fundamentally impossible**

### 2. Per-denominator decomposition (DEAD for closing per-class)
- B+C = Σ_b [2⟨D_b^osc, δ_b⟩ + ||δ_b||²]
- Need ||D_b^osc||/||δ_b|| < 1/2 per class → FAILS for most denominators (ratios up to 20)
- Negative contributions can reach 66% of positive (p=223)
- **The sum works but individual terms don't** — cancellation across classes is essential

### 3. Dedekind sums (DEAD — definition mismatch)
- D(a/b) ≈ |F_N|·((a/b)) + E(a/b) but |E| ≈ |F_N|·|((a/b))| (error = main term!)
- Decomposition: |F|·Σ((·))·δ and Σ E·δ nearly cancel (ratio 60-1000x to total)
- Reciprocity doesn't help because the sawtooth is NOT our displacement
- **Status: fundamentally inappropriate**

### 4. Character sums / Weil bounds (TRIED, didn't close)
- δ̂(χ) ∝ (1 - χ̄(p)) — clean character structure
- But D̂(χ) depends on global Farey ordering, not just local arithmetic
- Constant in Weil bound grows as p^{1.26}, defeating the purpose
- **Status: might work with tighter analysis of D̂(χ)**

### 5. Large sieve (DEAD)
- R(p) doesn't decay — large sieve gives wrong-type bound

### 6. Erdős-Turán (DEAD)
- Cotangent unbounded

### 7. Ergodic/horocycle (DEAD)
- Weak mixing insufficient for pointwise bound

### 8. Matrix/angle approach (CONDITIONAL, 40% confidence)

### 9. Coupling approach (DEAD)
- Found Dedekind connection but that's dead

## What Works (Partial Results)
- **cos(θ) between D and δ stays ~0.1-0.2**: D and δ are consistently nearly orthogonal
- **Global orthogonality** Σ|⟨D_b,δ_b⟩| / Σ||D_b||·||δ_b|| = 0.15-0.26 across all primes
- **Character factor**: δ̂(χ) ∝ (1 - χ̄(p)) means δ has no energy on characters with χ(p) = 1
- **CRT independence**: for coprime b₁, b₂, the actions of p mod b₁ and p mod b₂ are independent

## Key Structural Insights
1. **Permutation property kills smooth part**: Σ δ(a/b) = 0 per class means ⟨D_smooth, δ⟩ = 0
2. **D and δ live in "orthogonal arithmetic worlds"**: D = additive ordering, δ = multiplicative shift
3. **R(p) → 0 as p → ∞**: cos(θ) ~ 1/√p empirically, compensating ||D||/||δ|| ~ √p
4. **Worst case is smallest prime**: p=11 has fewest fractions, weakest statistical cancellation

## Most Promising Remaining Approaches (from fresh brainstorm)

### A. Second Moment / Concentration (PRIORITY 1)
- B = Σ_b X_b where X_b are weakly correlated (CRT gives independence for coprime b)
- By concentration, |B| = O(√(Var(B))) while C = Θ(Σ_b Var(δ_b))
- This explains WHY R → 0: law of large numbers
- **Needs**: bound Var(B) explicitly, show it's o(C²)

### B. Fourier/Character Analysis (PRIORITY 2)
- ⟨D, δ⟩ = Σ_b Σ_χ D̂_b(χ)·δ̂_b(χ̄)/φ(b)
- δ̂(χ) is clean. Need bounds on D̂_b(χ).
- D̂_b(χ) involves Farey-fractions-in-arcs weighted by characters
- May connect to Boca-Cobeli-Zaharescu pair correlation results

### C. Spectral Gap (AMBITIOUS)
- D in low-frequency eigenmodes of Farey graph Laplacian
- δ in high-frequency modes
- Spectral separation → small inner product
- Connected to Selberg eigenvalue conjecture / Maass forms

## Recommended Strategy
**Asymptotic + Finite Verification:**
1. Prove R(p) > -1/2 for p > P₀ using approach A or B
2. Verify computationally for p ≤ P₀ (already done to 99,991)
3. This is a perfectly standard approach in analytic number theory

## Growth Rates (Empirical)
| Quantity | Growth | p=11 | p=293 |
|----------|--------|------|-------|
| ||D||² | ~p^{2.5} | 21 | 1,390,284 |
| ||δ||² = C | ~p^{1.5} | 2.95 | 4,136 |
| ||D||/||δ|| | ~√p | 2.67 | 18.3 |
| cos(θ) | ~1/√p | -0.097 | 0.195 |
| R = cos(θ)·||D||/||δ|| | bounded | -0.259 | varies |
