# The Farey Telescope: Combining Multi-Prime Spectral Data to Probe L-Functions

**Date:** 2026-03-30
**Status:** Exploratory analysis
**Connects to:** N1 (per-step framework), N2 (Mertens-discrepancy connection), N5 (ABCD decomposition), N11 (permutation identity), N12.5 (Dedekind connection)
**Classification:** Unrated (exploration phase)

---

## 0. The Core Idea

Each prime p, when inserted into the Farey sequence F_{p-1} to form F_p, provides a "measurement" of arithmetic structure through the per-step discrepancy DeltaW(p). The key formula (N12.5) connects this to Dedekind sums:

    D_q(r) = q(q-1)(q-2)/12 - q^2 * s(r,q)

where s(r,q) is the Dedekind sum and D_q is the per-denominator shift deficit.

Different primes p give different "views" because:
- The Mertens function M(floor(N/a)) changes with N=p
- The set of denominators in F_p changes
- The Dedekind kernel Lambda_p(chi) = Sum_{a coprime to p} chi(a) * s(a,p) depends on p

**Metaphor:** Each prime is a "detector" sensitive to different frequency components. By combining many primes, we build a "telescope" that might resolve finer structure than any single prime reveals.

---

## 1. Summing the Spectral Formula Over Many Primes

### 1.1 What the Per-Prime Spectral Data Looks Like

For each prime p, the four-term decomposition gives:

    n'^2 * DeltaW(p) = A(p) - B(p) - C(p) - D(p)

where n' = |F_p| and A, B, C, D are the dilution, cross-term, shift-squared, and new-fraction terms. The empirical finding (N2) is:

    DeltaW(p) * p^2 ~ c * M(p) / sqrt(p)

with correlation r = 0.915 (pink noise findings, 9588 primes to p = 99991).

### 1.2 The Multi-Prime Sum

Define the "telescope sum":

    T(X) = Sum_{p <= X, p prime} DeltaW(p) * p^2

By the correlation with Mertens:

    T(X) ~ c * Sum_{p <= X} M(p) / sqrt(p)

Now, M(p) has the explicit formula (sum over nontrivial zeros rho of zeta):

    M(p) = Sum_rho p^rho / (rho * zeta'(rho)) + smaller terms

So:

    T(X) ~ c * Sum_{p <= X} Sum_rho p^{rho - 1/2} / (rho * zeta'(rho))

Interchanging (formally):

    T(X) ~ c * Sum_rho [1 / (rho * zeta'(rho))] * Sum_{p <= X} p^{rho - 1/2}

### 1.3 The Inner Sum: Sum_{p <= X} p^{rho - 1/2}

Write rho = 1/2 + i*gamma (assuming RH for now). Then p^{rho-1/2} = p^{i*gamma} = exp(i * gamma * log p).

This is a prime exponential sum:

    Sum_{p <= X} p^{i*gamma} = Sum_{p <= X} exp(i * gamma * log p)

By the prime number theorem in arithmetic progressions / explicit formula for primes:

    Sum_{p <= X} p^{i*gamma} ~ li(X^{1 + i*gamma}) / (1 + i*gamma) + lower-order terms

For large X, this sum oscillates with amplitude ~ X / (gamma * log X) when gamma is a zero, and has cancellation otherwise. This is essentially a "prime-weighted" test for zeros.

### 1.4 What T(X) Reveals

Combining:

    T(X) ~ c * Sum_rho [1 / (rho * zeta'(rho))] * [li(X^{1+i*gamma}) / (1+i*gamma)]

This is a sum over ALL zeros, weighted by 1/(rho * zeta'(rho)). The dominant contribution comes from zeros with small |gamma| (low-lying zeros).

**Key question:** Does T(X) converge to something expressible purely in terms of zeta zeros?

**Answer (preliminary):** T(X) is essentially a doubly-smoothed version of the explicit formula. The first smoothing is through M(p) (which already involves all zeros). The second smoothing is the sum over primes. This double averaging makes T(X) extremely smooth but also makes it hard to extract individual zeros -- they are all superimposed.

**Honest assessment:** This is NOT a new way to detect zeros. It is the explicit formula applied twice (once for M, once for the prime sum). The information content is not amplified; it is diluted by the double averaging. This is consistent with the pink noise finding: the DeltaW spectrum is a smooth continuum, not discrete peaks.

---

## 2. An Explicit Formula for W(N) in Terms of Zeros

### 2.1 The Starting Point: Franel-Landau

The classical connection (Identity 4 from PSL2Z_IDENTITIES.md):

    RH <=> Sum_{a/b in F_N} (f_j - j/(n-1))^2 = O(N^{-1+eps})

More precisely, the Franel sum:

    F(N) = Sum_{j=1}^{n} (f_j - j/n) = related to M(N)

The squared Franel sum (our W(N) up to normalization) satisfies:

    Sum (f_j - j/n)^2 = (1/n^2) Sum_{m=1}^{N} |c_m|^2

where c_m = Sum_{d|m, d<=N} d * mu(N/d) ... (Franel's original formulation).

### 2.2 The Mellin Transform Approach

Define the "Farey zeta function":

    Z_F(s) = Sum_{N=1}^{infty} W(N) * N^{-s}

or more usefully, the per-step version:

    Z_Delta(s) = Sum_{p prime} DeltaW(p) * p^{-s}

Using DeltaW(p) ~ c * M(p) / p^2 * 1/sqrt(p):

    Z_Delta(s) ~ c * Sum_p M(p) * p^{-s-5/2}

The Mertens function has the Mellin-type representation:

    Sum_{n=1}^{infty} M(n) * n^{-s} = 1 / (s * zeta(s))   (for Re(s) > 1)

But summing over primes only (not all n) changes things fundamentally. We need:

    Sum_{p prime} M(p) * p^{-s}

This does NOT have a simple closed form because the restriction to primes introduces the prime-counting measure. Using PNT heuristics:

    Sum_{p <= X} M(p) ~ integral_2^X M(t) / (t * log t) dt + error terms

And via partial summation + explicit formula for M(t):

    ~ integral M(t) d(li(t)) = integral [Sum_rho t^rho / (rho zeta'(rho))] * dt / (t log t)

This integral converges (each zero contributes a finite amount), giving:

    Sum_p M(p) * p^{-s} ~ Sum_rho [something involving rho, s, and zeta'(rho)]

**The poles of Z_Delta(s):** If this formal manipulation is valid, Z_Delta(s) would have singularities related to the zeros of zeta. Specifically, for each zero rho = beta + i*gamma:

    The contribution to Z_Delta(s) involves a term like 1/((s + 5/2 - rho) * rho * zeta'(rho))

These are simple poles at s = rho - 5/2 = (beta - 5/2) + i*gamma.

Under RH (beta = 1/2): the poles are at s = -2 + i*gamma, all in the half-plane Re(s) = -2.

**Conclusion:** Z_Delta(s) would have poles encoding ALL zeta zeros, shifted to Re(s) = -2 (under RH). This is technically correct but not useful for proving anything about zeros -- it is a reformulation, not new information. The poles of Z_Delta(s) are in 1-to-1 correspondence with zeta zeros by construction.

### 2.3 Direct Formula for W(N)

A more direct route. The Franel-Landau identity gives (in one formulation):

    Sum_{j} (f_j - j/n)^2 = (1/12n^2) + (1/4pi^2 n^2) Sum_{h=1}^{infty} (1/h^2) |Sum_{a/b in F_N} e(h*a/b)|^2

The inner exponential sum Sum_{a/b in F_N} e(h*a/b) is a Ramanujan-type sum that connects to:

    Sum_{a/b in F_N} e(h*a/b) = Sum_{b=1}^{N} c_b(h)

where c_b(h) = Sum_{a=1, (a,b)=1}^{b} e(ah/b) is the Ramanujan sum.

And Ramanujan sums have the explicit representation:

    c_b(h) = Sum_{d | gcd(b,h)} d * mu(b/d)

So:

    |Sum_b c_b(h)|^2 = |Sum_{b<=N} Sum_{d|gcd(b,h)} d * mu(b/d)|^2

This involves the Mertens function at various arguments. Specifically, for h=1:

    Sum_{b<=N} c_b(1) = Sum_{b<=N} mu(b) = M(N)

recovering the Franel-Landau theorem.

For general h:

    Sum_{b<=N} c_b(h) = Sum_{d|h} d * M(N/d)

This is the key identity: the h-th Fourier coefficient of the Farey sequence is a **divisor-weighted Mertens sum**.

### 2.4 The W(N) Explicit Formula

Combining:

    W(N) ~ (1/(4pi^2 n^2)) Sum_{h=1}^{H} (1/h^2) |Sum_{d|h} d * M(N/d)|^2 + O(1/H)

Using the explicit formula M(x) = Sum_rho x^rho / (rho zeta'(rho)) + ...:

    Sum_{d|h} d * M(N/d) = Sum_rho [Sum_{d|h} d * (N/d)^rho] / (rho zeta'(rho))
                          = Sum_rho [N^rho / (rho zeta'(rho))] * Sum_{d|h} d^{1-rho}
                          = Sum_rho [N^rho / (rho zeta'(rho))] * sigma_{1-rho}(h)

where sigma_s(h) = Sum_{d|h} d^s is the divisor function.

Therefore:

    W(N) ~ (1/(4pi^2 n^2)) Sum_h (1/h^2) |Sum_rho N^rho * sigma_{1-rho}(h) / (rho zeta'(rho))|^2

**This is the explicit formula for W(N) in terms of zeta zeros.**

Expanding the square:

    W(N) ~ (1/(4pi^2 n^2)) Sum_{rho, rho'} [N^{rho+rho'_bar} / (rho * rho'_bar * zeta'(rho) * zeta'(rho')_bar)] * Sum_h sigma_{1-rho}(h) * sigma_{1-rho'_bar}(h) / h^2

The inner h-sum is a Dirichlet series that can be evaluated:

    Sum_h sigma_{1-rho}(h) * sigma_{1-rho'}(h) / h^2 = zeta(2) * zeta(rho+rho'-1) * zeta(rho) * zeta(rho') / zeta(rho+rho')

(This is a standard multiplicative identity for convolutions of divisor functions, valid in appropriate half-planes.)

**Under RH** (rho = 1/2 + i*gamma, rho' = 1/2 + i*gamma'):

The "diagonal" terms (rho = rho') give N^{2*Re(rho)} = N, and the cross terms oscillate.

**Assessment:** This explicit formula is real and correct in principle, but:
- It involves ALL pairs of zeros (rho, rho'), making it a double sum over zeros
- The convergence requires careful analysis of the divisor-function Dirichlet series
- It is essentially a known (to experts) consequence of combining Franel-Landau with the explicit formula
- It does not provide a practical computational tool for detecting individual zeros

---

## 3. Can Individual Zeros Be Detected from DeltaW Data?

### 3.1 Previous Findings (pink_noise_findings.md)

The direct test was already performed:

**Method B: Dirichlet sum F(t) = Sum DeltaW*p^2 * exp(i*t*log p)**

Results:
- gamma_1 = 14.135: SNR 3.11 (the only notable peak)
- gamma_2 through gamma_15: SNR 0-1.7 (no significant detection)
- Random frequencies: mean SNR 1.20 (higher than mean at zeros: 0.91)

**Verdict from that analysis:** No systematic detection of individual zeros. The first zero gamma_1 = 14.13 shows a mild signal, but this is likely because it dominates the low-frequency content of M(p)/sqrt(p).

### 3.2 Why Detection is Hard: The Interference Problem

The explicit formula for M(p) involves ALL zeros simultaneously:

    M(p) ~ Sum_rho p^{rho} / (rho * zeta'(rho))

When we form DeltaW(p) * p^2 ~ M(p)/sqrt(p), and then take a Fourier transform in log-prime space:

    F(t) = Sum_p DeltaW(p) * p^2 * p^{it} ~ Sum_rho [1/(rho zeta'(rho))] * Sum_p p^{rho - 1/2 + it}

The inner sum Sum_p p^{sigma + i(gamma+t)} has a "resonance" when t = -gamma (aligning with a zero), but the resonance width is broad (order 1/log X for primes up to X). Since zeros have average spacing 2*pi/log(gamma/(2*pi)), which is roughly 1-2 for the first few hundred zeros, the resonances overlap massively.

**To resolve individual zeros, we would need primes up to X where:**

    1/log X << 2*pi / log(gamma/(2*pi))

For gamma ~ 14 (first zero): need log X >> 1, so X >> e, easily satisfied.
For gamma ~ 1000: need log X >> log(1000/6.28) ~ 5, so X >> 150.
For gamma ~ 10^6: need log X >> 14, so X >> 10^6.

So in principle, with enough primes (X large enough), individual zeros can be resolved. But:

1. We already know where the zeros are (from direct computation of zeta)
2. The "telescope" provides no advantage over computing zeta directly
3. The DeltaW data adds noise (through the ABCD decomposition) rather than amplifying signal

### 3.3 A Theoretically Sharper Approach: Weighted Telescope

Instead of the raw sum, consider a weighted version designed to isolate a single zero:

    T_gamma(X) = Sum_{p <= X} DeltaW(p) * p^2 * p^{-1/2 + i*gamma} * w(p)

where w(p) is a smooth weight function. If we choose w to match the "natural" weight from the explicit formula, this becomes:

    T_gamma(X) ~ [1/(rho_0 * zeta'(rho_0))] * Sum_p p^{2i*gamma_0} * w(p) + Sum_{rho != rho_0} [cross terms]

The main term grows like X * w(X) / log X (from PNT) while cross terms oscillate. Taking X -> infinity and dividing by the main term growth:

    lim T_gamma(X) / [X * w(X) / log X] = 1/(rho_0 * zeta'(rho_0))   if gamma hits a zero
                                          = 0                           if gamma misses

**This is a valid zero-detection principle**, but it requires:
- Knowing DeltaW(p) to sufficient precision for ALL primes up to very large X
- Computing a weighted sum that is equivalent in difficulty to computing zeta directly
- The convergence rate is no better than standard explicit formula methods

**Honest assessment:** The Farey telescope CAN detect zeros in principle, but it is strictly less efficient than computing zeta(1/2 + i*t) directly. It adds the overhead of computing all Farey sequences up to F_X, which is enormously more expensive than evaluating zeta.

---

## 4. The Mellin Transform of W(N)

### 4.1 Definition and Convergence

Define:

    W_tilde(s) = Sum_{N=2}^{infty} W(N) * N^{-s}

Since W(N) = O(1/N) (from equidistribution), this converges for Re(s) > 0.

Using W(N) ~ c / N (Franel-Landau rate under RH):

    W_tilde(s) ~ c * Sum N^{-s-1} ~ c * zeta(s+1)   for Re(s) > 0

More precisely, using the explicit formula from Section 2.4:

    W_tilde(s) has singularities where the N^{rho+rho'_bar} terms in the W(N) formula produce poles.

The dominant singularity comes from the diagonal rho = rho' terms:

    N^{2*Re(rho)} = N^{2*beta}

Under RH: 2*beta = 1, so the sum Sum N^{1-s} diverges at s = 1. This gives W_tilde(s) a pole at s = 1 (trivially, from the W(N) ~ c/N behavior).

The off-diagonal terms (rho != rho') contribute:

    N^{rho + rho'_bar} = N^{beta + beta' + i(gamma - gamma')}

Under RH: N^{1 + i(gamma-gamma')}, giving poles at s = 1 + i(gamma - gamma') for all pairs of zeros.

### 4.2 Poles of W_tilde(s)

**Under RH, W_tilde(s) has poles at:**

    s = 1 + i(gamma - gamma')   for all pairs (rho, rho') of nontrivial zeros

This means:
- A pole at s = 1 (from rho = rho', i.e., gamma = gamma')
- Poles at s = 1 +/- i(gamma_1 - gamma_2), s = 1 +/- i(gamma_1 - gamma_3), etc.

The imaginary parts of these poles are the **differences** of zeta zero heights, not the heights themselves.

**Connection to pair correlation:** The density of poles at s = 1 + it is:

    Sum_{gamma, gamma'} delta(t - (gamma - gamma'))

which is exactly the **pair correlation function** of zeta zeros! Montgomery's pair correlation conjecture predicts this density approaches 1 - (sin(pi*u)/(pi*u))^2 (in suitable normalization).

**This is an interesting structural observation:** The Mellin transform of W(N) encodes the pair correlation of zeta zeros, not individual zeros.

### 4.3 The Per-Step Mellin Transform

For the per-step version:

    Z_Delta(s) = Sum_p DeltaW(p) * p^{-s}

Using DeltaW(p) ~ M(p) / p^{5/2}:

    Z_Delta(s) ~ Sum_p M(p) * p^{-s-5/2}

The connection to 1/(s * zeta(s)) (Mellin transform of Mertens over all integers) breaks because we sum over primes only. The prime restriction introduces log zeta(s) (the prime zeta function) as a complication.

Formally:

    Z_Delta(s) has singularities at s = rho - 5/2 for each zero rho

These are all in Re(s) = -2 (under RH), deep in the left half-plane. To analytically continue Z_Delta(s) to see these poles would require knowing Z_Delta(s) in Re(s) > 0 and then continuing -- which is equivalent in difficulty to knowing all the zeros.

---

## 5. What IS Novel Here (Honest Assessment)

### Genuinely interesting observations:

1. **W_tilde(s) encodes pair correlations.** The Mellin transform of the cumulative Farey discrepancy has poles at s = 1 + i(gamma - gamma'), directly encoding the pair correlation of zeta zeros. This is a clean structural statement that connects Farey equidistribution to Montgomery's conjecture. Whether this is known to experts is unclear -- it follows from combining standard ingredients (Franel-Landau + explicit formula + Ramanujan sums), but the explicit statement may not appear in the literature.

2. **The divisor-weighted explicit formula.** The identity

    Sum_{b<=N} c_b(h) = Sum_{d|h} d * M(N/d)

combined with the explicit formula for M, gives the explicit formula for W(N) in Section 2.4. The individual ingredients are known, but assembling them into a formula for W(N) involving sigma_{1-rho}(h) may be a useful reference result.

3. **The first zero dominance.** The empirical finding that gamma_1 = 14.13 produces the only detectable signal in the DeltaW Dirichlet sum (SNR 3.11 vs < 1.7 for all others) has a clean explanation: the first zero has the largest 1/|rho * zeta'(rho)| weight and the longest-range oscillation in log-prime space.

### What is NOT novel:

1. **The telescope sum T(X) does not amplify zero information.** It is a doubly-smoothed explicit formula with no advantage over direct computation.

2. **Z_Delta(s) having poles at shifted zeros** is a tautology -- it follows immediately from DeltaW ~ M/p^{5/2} and the explicit formula for M.

3. **Detection of individual zeros from DeltaW** is possible in principle but strictly inferior to computing zeta directly.

### What could become novel with more work:

1. **The pair correlation connection (Section 4.2)** deserves rigorous development. If one could show that the pole structure of W_tilde(s) reproduces Montgomery's pair correlation function with the correct normalization, that would give a new proof (or at least a new perspective) on the pair correlation conjecture starting from Farey sequence data. This would require:
   - Making the explicit formula in Section 2.4 rigorous
   - Controlling the off-diagonal terms carefully
   - Computing the pole residues and showing they match the pair correlation density

2. **The sigma_{1-rho}(h) weights in the W(N) formula** might have interesting number-theoretic properties. The divisor function sigma_{1-rho}(h) at a zeta zero rho is a multiplicative function whose behavior at primes is:

    sigma_{1-rho}(q) = 1 + q^{1-rho} = 1 + q^{1/2 - i*gamma}   (under RH)

This is an oscillating multiplicative weight on primes. How it averages over h could reveal structure.

3. **Multi-prime cross-correlations.** Instead of T(X) = Sum_p DeltaW(p), consider:

    C(p, p') = corr(DeltaW(p), DeltaW(p'))

as a function of |p - p'| or p'/p. If this correlation function has oscillations at frequencies matching zero gaps (gamma_2 - gamma_1, etc.), that would be the pair correlation showing up directly in Farey data. The pink noise analysis showed the ACF of DeltaW does NOT have Montgomery-type oscillations, but the normalization and variable might not have been optimal.

---

## 6. Proposed Next Steps

### Priority 1: Rigorous pair correlation connection (theoretical)
- State precisely: for which definition of W_tilde(s) do the poles encode pair correlation?
- Compute the pole residues and check against Montgomery's prediction
- This is a pen-and-paper / Lean formalization task, not computational

### Priority 2: Cross-correlation test (computational, quick)
- Compute C(p, p') = corr between DeltaW at primes p and p' as function of log(p'/p)
- Compare to the pair correlation kernel 1 - (sin(pi*u)/(pi*u))^2
- Already have the data (wobble_primes_100000.csv); just need the right analysis

### Priority 3: Literature search (verification)
- Search for "Farey sequence Mellin transform" and "Franel sum pair correlation"
- Determine if the pair correlation observation is already known

### DO NOT pursue:
- More computation of DeltaW at larger primes (already have enough data)
- Trying to "detect" individual zeros (confirmed inferior to direct methods)
- The telescope sum T(X) (confirmed to be a doubly-smoothed explicit formula with no advantage)

---

## 7. Connection to Existing Insights

| Insight | How this connects |
|---------|------------------|
| N1 (per-step framework) | DeltaW(p) is the fundamental "measurement" in the telescope |
| N2 (Mertens connection) | The r=0.915 correlation IS the telescope's signal path |
| N5 (ABCD decomposition) | Provides the algebraic structure relating DeltaW to Dedekind sums |
| N11 (permutation identity) | Simplifies B+C to a linear form, potentially useful for the pair correlation analysis |
| N12.5 (Dedekind connection) | The Dedekind kernel is the "lens" through which each prime views L-function structure |

---

## Summary

The "Farey telescope" idea is partially validated: the per-step discrepancy DeltaW(p) does carry information about zeta zeros, but only through the intermediary of the Mertens function. The genuinely interesting finding is that the **Mellin transform of the cumulative discrepancy W(N) has poles encoding the pair correlation of zeta zeros**, not individual zeros. This connects Farey equidistribution directly to Montgomery's pair correlation conjecture.

The telescope metaphor is apt but needs refinement: it is not a telescope that resolves individual stars (zeros), but rather one that measures the statistical clustering of stars (pair correlation). This is still valuable -- pair correlation is one of the deepest unsolved problems about zeta zeros -- but it requires rigorous development to determine whether the Farey perspective offers any advantage over existing approaches.
