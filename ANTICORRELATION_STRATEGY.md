# Anticorrelation Lemma: Proof Strategy Analysis

**Date:** Session analysis
**Author:** Aristotle (Harmonic)

## The Problem

For prime p ≥ 19 with M(p) ≤ 0, prove:

$$\sum_{f \in F_{p-1}} D(f) \cdot (\{pf\} - f) < 0$$

where D(f) = rank(f) - |F_{p-1}|·f and {pf} = fractional part of p·f.

---

## NEW DISCOVERY: The δ-cosine identity

**Theorem (NEW):** For any prime p,
$$\sum_{f \in F_{p-1}} (\{pf\} - f) \cdot \cos(2\pi p f) = -1$$

### Proof sketch:
Write δ = {pf} - f and decompose:
- Σ δ·cos = Σ {pf}·cos(2πpf) - Σ f·cos(2πpf)

For **Σ f·cos(2πpf)**: Decompose f = 1/2 + (f - 1/2).
- The constant part gives (1/2)·Σ cos(2πpf) = (M+2)/2
- The antisymmetric part (f-1/2)·cos is antisymmetric (product of antisymmetric and symmetric), so the paired sum vanishes. Boundary: f=0 gives (-1/2)·1 = -1/2, f=1 gives (1/2)·1 = 1/2, which cancel.
- **Result: Σ f·cos = (M+2)/2**

For **Σ {pf}·cos(2πpf)**: Decompose {pf} = 1/2 + ({pf} - 1/2).
- The constant part gives (1/2)·Σ cos = (M+2)/2
- The antisymmetric part ({pf}-1/2)·cos is antisymmetric. For paired interior fractions: ({pf}-1/2)·cos + ({p(1-f)}-1/2)·cos = ({pf}-1/2 + 1/2-{pf})·cos = 0.
- **Boundary terms:** f=0 gives (-1/2)·1 = -1/2; f=1 gives ({p}-1/2)·1 = (0-1/2)·1 = -1/2. Total = -1.
- **Result: Σ {pf}·cos = (M+2)/2 - 1 = M/2**

Therefore: **Σ δ·cos = M/2 - (M+2)/2 = -1** ∎

This identity holds for ALL primes p (verified computationally for p ≤ 97), regardless of M(p).

---

## Key Mathematical Structure

### Decomposition of Σ D·δ

$$\Sigma D \cdot \delta = \sum_j D_j (f_{\pi(j)} - f_j)$$

where π is the permutation induced by f ↦ {pf} (acting within each denominator group via a ↦ pa mod b).

By the rearrangement inequality:
- **A** := Σ j·f_j - Σ j·f_{π(j)} ≥ 0 (rank-value rearrangement deficit)
- **B** := Σ f_j² - Σ f_j·f_{π(j)} ≥ 0 (value-value rearrangement deficit)

Then **Σ D·δ = -A + n·B**, and we need A > n·B.

### Floor decomposition

Since δ = (p-1)f - ⌊pf⌋:

$$\Sigma D \cdot \delta = (p-1) \cdot \Sigma D \cdot f - \Sigma D \cdot \lfloor pf \rfloor$$

And using the indicator decomposition ⌊pf⌋ = Σ_{k=1}^{p-1} 1_{f > k/p}:

$$\Sigma D \cdot \lfloor pf \rfloor = -\sum_{k=1}^{p-1} T(k/p)$$

where T(x) = Σ_{f ≤ x} D(f) is the cumulative displacement function.

**Therefore:**
$$\Sigma D \cdot \delta = (p-1) \Sigma D \cdot f + \sum_{k=1}^{p-1} T(k/p)$$

This expresses the anticorrelation sum in terms of:
1. Σ D·f (a known quantity depending only on the Farey sequence F_{p-1})
2. The values T(k/p) of the cumulative displacement at the new fraction positions

---

## Known Identities (proved or discovered)

| # | Identity | Value | Source |
|---|----------|-------|--------|
| 1 | Σ D = 0 | 0 | Σ rank = n(n-1)/2, Σ f = n/2 |
| 2 | Σ D·cos(2πpf) | -1-M/2 | Displacement-cosine (proved) |
| 3 | Σ D·g (sym g) | -(1/2)Σ g | Master involution (proved) |
| 4 | Σ {pf} | (n-2)/2 | Fractional parts sum (proved) |
| 5 | Σ δ | -1 | From #4 and Σf = n/2 |
| 6 | **Σ δ·cos(2πpf)** | **-1** | **NEW (this session)** |
| 7 | Σ cos(2πpf) | M+2 | Bridge identity (proved) |
| 8 | Σ cos²(2πpf) | n/2 - 2 | From Σ cos(4πpf) and bridge |
| 9 | {pf} + {p(1-f)} = 1 | | Involution (proved) |

---

## Why Standard Approaches Fail

### Cauchy-Schwarz
|Σ D·δ| ≤ √(Σ D² · Σ δ²). At p=23: bound = 75.9, actual = 0.15. Ratio: 500x.
The Pearson correlation is only -0.002 at p=23.

### Gram matrix with cos
Adding the constraint Σ D·cos = -1-M/2 and Σ δ·cos = -1 gives only marginal improvement: bound = 75.87 vs 75.90. The three vectors (D, δ, cos) are nearly orthogonal.

### Master involution
Gives identities for symmetric functions only. δ = {pf}-f is **antisymmetric**, so the involution is blind to it.

---

## Most Promising Approach: HYBRID FINITE + ASYMPTOTIC

### Phase 1: Finite verification (p ≤ B)
For each prime p with 19 ≤ p ≤ B and M(p) ≤ 0, verify Σ D·δ < 0 by exact rational computation.

**Tight cases (computed):**
- p=23: Σ D·δ = -1911041/12697776 ≈ -0.1505 (tightest, Pearson = -0.002)
- p=19: Σ D·δ = -1544259/1361360 ≈ -1.1344
- p=41: Σ D·δ ≈ -2.204 (M=-1 case)

For p ≥ 53, |Σ D·δ|/n > 0.03, giving much more margin.

### Phase 2: Asymptotic bound (p > B)
For large p, use:

1. **Σ D² asymptotics:** Σ D² = O(n² / log n) (from PNT-level bounds on Farey discrepancy)
2. **Σ δ² asymptotics:** Σ δ² = O(n) (each δ ∈ [-1, 1])
3. **The main term:** Σ D·δ = Σ D·{pf} - Σ D·f, where Σ D·f can be expressed in terms of Farey sums

The challenge: for large p, the ratio |Σ D·δ|/n stabilizes around 0.05-0.15, but the Cauchy-Schwarz bound grows as √n, so CS works for p > some threshold.

**Key insight for large p:** The floor decomposition gives
Σ D·δ = (p-1)·Σ D·f + Σ T(k/p)

For large p, the T(k/p) values are approximately T(k/p) ≈ -const · n² · k(p-k)/p² (from the quadratic behavior of the cumulative displacement). The sum Σ T(k/p) ≈ -C · n² · p ≈ -C' · p⁵/π⁴, while (p-1)·Σ D·f = O(p⁴).

This suggests the T-sum dominates for large p, giving Σ D·δ < 0 unconditionally.

---

## Approach 2: Dedekind Sum Connection

The sum Σ f·{pf} is related to Dedekind sums:

For each denominator b, define the "correlation sum":
$$C_b = \frac{1}{b^2} \sum_{\substack{a \text{ coprime to } b \\ 0 < a < b}} a \cdot (pa \bmod b)$$

Then Σ f·{pf} = Σ_b C_b (over denominators 2 ≤ b ≤ p-1, plus boundary).

The Dedekind sum s(p,b) is related to C_b through:
$$C_b = \frac{p}{b^2} \sum a^2 - \frac{1}{b} \sum a \lfloor pa/b \rfloor$$

And the floor sum has an exact formula:
$$\sum_{a=1}^{b-1} a \lfloor pa/b \rfloor = \frac{p(b-1)(2b-1)}{6} - b \cdot s(p,b) - \frac{b(b-1)}{4}$$

Using **Dedekind reciprocity**: s(p,b) + s(b,p) = (p²+b²+1)/(12pb) - 1/4.

This gives an explicit formula for C_b in terms of s(b,p) (the "reversed" Dedekind sum).

**Potential:** If we can bound Σ s(b,p) for b=2,...,p-1, we get a bound on Σ f·{pf}, which is one of the two key terms in Σ D·δ.

**Difficulty:** The other key term Σ rank·{pf} involves the rank function, which depends on the global ordering and doesn't decompose per-denominator.

---

## Approach 3: Second Involution

The involution f ↦ 1-f gives:
- D(f) + D(1-f) = -1
- {pf} + {p(1-f)} = 1

This determines the symmetric part of any bilinear form involving D and functions of {pf}.

**Question:** Is there a SECOND involution on F_{p-1} that gives information about the antisymmetric part?

**Candidates explored:**
1. f ↦ {pf} (multiplication by p): NOT an involution in general (p² ≢ 1 mod b for all b)
2. f ↦ f/(1-f): changes denominator, not closed on F_{p-1} in general
3. f ↦ 1/f: changes range, not applicable
4. Gauss map f ↦ {1/f}: changes denominator

**Conclusion:** No natural second involution found. The Farey sequence has essentially one symmetry (f ↦ 1-f).

---

## Approach 4: Higher Fourier Modes

The sawtooth Fourier series:
$$\{pf\} - \frac{1}{2} = -\frac{1}{\pi} \sum_{k=1}^{\infty} \frac{\sin(2\pi k p f)}{k}$$

gives:
$$\Sigma D \cdot (\{pf\} - 1/2) = -\frac{1}{\pi} \sum_{k=1}^{\infty} \frac{1}{k} \Sigma D \cdot \sin(2\pi k p f)$$

**What we know:** Σ D·cos(2πkpf) = -(1/2)·Σ cos(2πkpf) for all k (master involution).
**What we need:** Σ D·sin(2πkpf) — the antisymmetric displacement-Fourier coefficients.

The involution gives NO information about these sine sums (sin is antisymmetric). Computing them requires knowledge of the rank function, which is global.

**Computational data (p=23):**
- k=1: Σ D·sin(2πpf) = -39.2 (dominates)
- k=2: Σ D·sin(4πpf) = -38.2
- k=3: -26.2, k=5: -10.5, k=10: -3.0

The partial sums converge slowly (as expected from the 1/k coefficients).

---

## Recommended Strategy

### Most feasible path to a complete proof:

1. **Prove Σ δ·cos = -1 formally** (clean, follows from existing identities)

2. **Finite verification for 19 ≤ p ≤ B:**
   - For B ≈ 200-500, verify all primes with M(p) ≤ 0 by exact rational arithmetic
   - In Lean, this could use `native_decide` or a decidable computation

3. **Asymptotic bound for p > B:**
   - Use the decomposition Σ D·δ = (p-1)·Σ D·f + Σ T(k/p)
   - Bound T(k/p) using known bounds on the Farey counting function R(x)
   - The key bound: |R(x) - n·x| ≤ C·N·log(N) for F_N (Franel-level bound)
   - This gives |T(k/p)| ≤ C'·N²·log(N)·|x - something|
   - Sum over k to get Σ T(k/p) and show it dominates (p-1)·Σ D·f

4. **Alternative: Use RH-conditional result + finite verification:**
   - Under RH: |D(f)| = O(√n · log²n), giving |Σ D·δ| = O(n^{3/2} · log²n)
   - The "threshold" for ΔW > 0 is Θ(n²), so RH gives the result for p > C
   - Finite verification handles p ≤ C
   - This approach is conditional on RH but provides a COMPLETE proof under that assumption

### Key open questions:
- Can Σ rank·{pf} be expressed in terms of Dedekind sums or other computable quantities?
- Is there a "level repulsion" phenomenon that prevents Σ D·δ from being near zero?
- Can the M(p) ≤ 0 condition be used more directly (not just through Σ D·cos)?

---

## Data Table: All primes 19 ≤ p < 100 with M(p) ≤ 0

| p | n | M(p) | Σ D·δ | |Σ D·δ|/n | Pearson |
|---|---|------|-------|---------|---------|
| 19 | 103 | -3 | -1.134 | 0.011 | -0.024 |
| 23 | 151 | -2 | -0.151 | 0.001 | -0.002 |
| 29 | 243 | -2 | -5.818 | 0.024 | -0.038 |
| 31 | 279 | -4 | -30.003 | 0.108 | -0.154 |
| 37 | 397 | -2 | -12.160 | 0.031 | -0.038 |
| 41 | 491 | -1 | -2.204 | 0.004 | -0.005 |
| 43 | 543 | -3 | -55.031 | 0.101 | -0.113 |
| 47 | 651 | -3 | -67.241 | 0.103 | -0.116 |
| 53 | 831 | -3 | -83.806 | 0.101 | -0.101 |
| 59 | 1029 | -1 | -39.112 | 0.038 | -0.037 |
| 61 | 1103 | -2 | -116.394 | 0.106 | -0.089 |
| 67 | 1329 | -2 | -129.898 | 0.098 | -0.082 |
| 71 | 1495 | -3 | -196.387 | 0.131 | -0.110 |
| 73 | 1589 | -4 | -364.203 | 0.229 | -0.174 |
| 79 | 1857 | -4 | -351.673 | 0.189 | -0.146 |
| 83 | 2061 | -4 | -432.790 | 0.210 | -0.157 |
| 89 | 2369 | -2 | -349.668 | 0.148 | -0.105 |

**Pattern:** Σ D·δ < 0 for ALL primes ≥ 19 with M(p) ≤ 0. The tightest case is p=23.
The ratio |Σ D·δ|/n appears to be bounded below by ~|M|·f(p) for some increasing function.
