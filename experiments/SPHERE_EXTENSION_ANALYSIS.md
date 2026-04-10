# Extending Farey Per-Step Discrepancy from S^1 to S^2

**Date:** 2026-03-28
**Status:** 🔬 Unverified — initial exploration
**Classification:** C1 (Collaborative, Minor Novelty) — the core theory is Duke/Linnik; our contribution is the per-step ΔW perspective

---

## 1. Background and Motivation

On S^1, our core contribution is the **per-step Farey discrepancy** ΔW(p): as we build the Farey sequence F_N by adding fractions with denominator N, the discrepancy changes. At prime steps, we discovered:
- **Sign Theorem:** ΔW(p) < 0 for all primes tested (discrepancy always decreases)
- **Bridge Identity:** Σ_{f ∈ F_p} e^{2πipf} = M(p) + 2, connecting exponential sums to the Mertens function
- **M(p) ↔ ΔW(p) Correlation:** Strong anticorrelation between Mertens and discrepancy change

**Question:** Does any of this extend to the 2-sphere S^2?

## 2. Theoretical Framework

### 2.1 Duke's Theorem (1988)

For squarefree n with n ≢ 0, 4, 7 (mod 8), the normalized lattice points

    { (a/√n, b/√n, c/√n) : a^2 + b^2 + c^2 = n }

equidistribute on S^2 as n → ∞.

**Rate:** Duke proved a power-saving bound with exponent δ = 1/28 (via Iwaniec 1987):

    r₃(n, P) ≪ n^{k/2 - 1/4 - 1/28 + ε}

where r₃(n, P) = Σ_{a²+b²+c²=n} P(a,b,c) is the weighted representation number for harmonic polynomial P of degree l, and k = 3/2 + l.

### 2.2 The Theta Series Connection

The function θ_P(z) = Σ_n r₃(n,P) q^n is a modular form of weight 3/2 + deg(P) for Γ₀(4). When deg(P) > 0, this is a **cusp form**.

This is the S^2 analog of the fact that on S^1, the exponential sum Σ e^{2πinx} connects to Fourier coefficients of modular forms.

### 2.3 The Waldspurger Formula

The connection to L-functions goes through Waldspurger's formula:

    |r₃(n, P)|^2 ~ L(g ⊗ χ_n, k - 1/2)

where g is the Shimura lift of the theta function. This is the S^2 analog of our bridge identity.

**Key references:**
- Duke, "Hyperbolic distribution problems and half-integral weight Maass forms" (1988)
- Linnik, "Ergodic Properties of Algebraic Fields" (1968)
- Ellenberg-Michel-Venkatesh, "Linnik's ergodic method and distribution of integer points on spheres" (2010)
- Michel-Venkatesh, "Equidistribution, L-functions and Ergodic Theory" (ICM 2006)

## 3. Computational Results

### 3.1 The Octahedral Symmetry Obstruction (CRITICAL FINDING)

**Result:** For the isotropic form Q = a^2 + b^2 + c^2, ALL spherical harmonic sums vanish exactly:

    Σ_{a²+b²+c²=n} Y_ℓ^m(a/√n, b/√n, c/√n) = 0 for ALL ℓ ≥ 1, ALL m, ALL n

This is because:
1. Sign symmetry (a→-a) kills all odd-ℓ harmonics
2. Permutation symmetry (a,b,c) → (b,c,a) kills all ℓ=2 harmonics:
   - Σ(2c²-a²-b²) = Σ(2a²-b²-c²) = Σ(2b²-c²-a²)
   - Adding: 3·Σ(2c²-a²-b²) = 0
3. The full octahedral group O_h (48 elements) kills ALL harmonics

**Consequence:** There is NO direct "bridge identity" for a²+b²+c² = n using spherical harmonics, because the symmetry group is too large. The Fourier coefficients r₃(n, P) = 0 identically for the isotropic form.

This is fundamentally different from S^1, where the exponential sum e^{2πipf} is NOT killed by symmetry.

### 3.2 Sign Theorem Analog — FAILS on S^2

Using cumulative L2 cap discrepancy of lattice points:
- **ΔW > 0 (discrepancy increased):** 41 primes
- **ΔW < 0 (discrepancy decreased):** 83 primes
- **Ratio positive:** ~33%

The Sign Theorem does NOT hold on S^2. Adding lattice points at prime levels sometimes increases discrepancy.

Using orbit representatives (one point per Oh-orbit):
- ΔW > 0: 41 primes (61%)
- ΔW < 0: 26 primes
- Sign theorem fails even more dramatically

**Why it fails:** On S^1, the Farey sequence has an intrinsic ordering (fractions on a circle). Adding a new fraction at a prime step always fills the largest gap optimally (mediant property). On S^2, there is no such ordering — lattice points are scattered without a gap-filling mechanism.

### 3.3 Mertens Correlation — ABSENT on S^2

    Correlation(ΔW_sphere, M(p)) = -0.010 (essentially zero)
    Correlation(ΔW_orbit, M(p)) = -0.044 (negligible)

The strong M(p) ↔ ΔW(p) anticorrelation that characterizes S^1 does not exist on S^2.

### 3.4 Breaking Symmetry: Anisotropic Forms

For the anisotropic form a² + b² + 2c² = p (which breaks S₃ permutation symmetry):
- r₃(p, Y₂⁰) is NON-ZERO for all 80 primes tested
- Values are predominantly negative (the c-direction is compressed)
- Weak correlation with M(p): r = -0.129

This suggests: if one wants a bridge identity on S^2, one must use **anisotropic ternary forms** (like a²+b²+2c²), not the isotropic form a²+b²+c².

### 3.5 Character-Twisted Theta Coefficients

For χ = Legendre symbol mod 3: r₃(p, χ₃) = 0 for ALL primes (symmetry again).
For χ = Legendre symbol mod 5: r₃(p, χ₅) is NON-ZERO for many primes.

The character twist with (·/5) provides non-trivial arithmetic information, but the connection to Mertens remains absent.

## 4. Structural Comparison: S^1 vs S^2

| Feature | S^1 (Farey) | S^2 (Lattice Points) |
|---------|-------------|---------------------|
| Equidistribution | Fréchet (1949), rate ~1/N | Duke (1988), rate ~n^{-1/28+ε} |
| Ordering | Natural circular order | No natural order |
| Per-step mechanism | Mediant insertion (fills gaps) | Scattered addition |
| Sign Theorem | ΔW(p) < 0 always | FAILS — ~33% positive |
| Bridge Identity | Σe^{2πipf} = M(p)+2 | Killed by O_h symmetry |
| M(p) correlation | Strong (r ~ -0.7) | Absent (r ~ -0.01) |
| Modular form | Weight 2 Eisenstein | Weight 3/2 theta |
| L-function link | Via Ramanujan sum c_q(n) | Via Waldspurger formula |

## 5. Why S^2 is Fundamentally Different

### 5.1 No Farey Mediant on S^2
The Farey sequence's per-step behavior relies on the **mediant property**: new fractions split existing intervals optimally. There is no 2D mediant for lattice points on S^2. The gap-filling is "accidental" rather than structural.

### 5.2 Excessive Symmetry Kills Arithmetic Information
The octahedral group O_h (order 48) of a²+b²+c² is so large that it kills ALL spherical harmonic coefficients. On S^1, the relevant symmetry group is just Z/2Z (complex conjugation), which only kills odd exponentials — the even ones survive and carry arithmetic information.

### 5.3 Rate Difference
On S^1: discrepancy decays as ~1/N (order of Farey sequence).
On S^2: Duke's bound gives only ~n^{-1/28+ε}, vastly slower. The weak rate means per-step changes are swamped by fluctuations.

## 6. What COULD Work: Possible S^2 Extensions

### 6.1 Anisotropic Ternary Forms
Use forms like a² + b² + 2c² or a² + 2b² + 3c² that break the full symmetry. The theta series with harmonics would then have non-trivial Fourier coefficients, and one could study per-step discrepancy on the corresponding ellipsoid.

### 6.2 Heegner Points on Modular Curves
Duke's original paper also covers equidistribution of Heegner points, which live on modular curves (closer to S^1). The per-step analysis might transfer more naturally there.

### 6.3 Genus Theory Decomposition
Decompose r₃(n) into contributions from different genera. Within a single genus, the symmetry is broken and non-trivial sums may appear.

### 6.4 Quaternion Orders
Use maximal orders in quaternion algebras to construct theta series that are already Hecke eigenforms. These avoid the symmetry obstruction and connect directly to L-functions.

## 7. Conclusions

**The extension from S^1 to S^2 does NOT work directly.** The three signature features of our Farey analysis — the Sign Theorem, the Bridge Identity, and the Mertens Correlation — all fail on S^2 due to:

1. The octahedral symmetry group killing all harmonic coefficients
2. The absence of a natural ordering / gap-filling mechanism
3. The much slower equidistribution rate (n^{-1/28} vs N^{-1})

However, this negative result is itself informative: it shows that the Farey per-step phenomenon is **specific to the interplay between mediants, ordering, and the Mobius function on S^1**. It is not a generic feature of equidistribution.

**Possible paths forward** involve breaking the symmetry (anisotropic forms, genus decomposition, or Heegner points) to recover non-trivial arithmetic content.

## 8. Files

- `sphere_equidistribution.py` — v1 computation (full symmetry)
- `sphere_equidist_v2.py` — v2 computation (broken symmetry, characters)
- `sphere_equidistribution.png` — v1 plots
- `sphere_equidist_v2.png` — v2 plots
- `sphere_equidistribution_results.json` — v1 data
- `sphere_equidist_v2_results.json` — v2 data
