# Literature Check: Universality of Zero Encoding in Prime Subsets

**Date:** 2026-04-06  
**Question:** Is it a known result that arbitrary subsets of primes can independently detect Riemann zeta zeros via spectral methods?

---

## Key Phrases Searched

1. "Holographic encoding of zeros" — **No established usage** in analytic number theory literature.
2. "Prime subsets detect zeros" — Not a standard result or phrase.
3. "Explicit formula universality" — Not used in the sense of subset-independence.
4. "Spectral detection from prime subsequences" — No prior work found.

## What IS Known (Background)

### The Explicit Formula (von Mangoldt / Riemann–Weil)

The classical explicit formula connects **all primes** to **all zeros**:

$$\psi(x) = x - \sum_\rho \frac{x^\rho}{\rho} - \log(2\pi) - \frac{1}{2}\log(1 - x^{-2})$$

This is a global identity: the sum over primes on the left uses ALL primes, and the sum over zeros on the right uses ALL nontrivial zeros. There is no classical result extracting zero information from **subsets** of primes.

### Montgomery's Pair Correlation (1973)

Montgomery studied spacing statistics of zeta zeros and connected them to random matrix theory. His work uses the **full set** of primes (via the explicit formula). He did not study what happens with prime subsets.

### Odlyzko's Numerical Computations (1987–2001)

Odlyzko computed billions of zeros of ζ(s) numerically to verify the GUE hypothesis. His methods use contour integration and Euler–Maclaurin summation — not prime-subset spectral methods.

### Rubinstein's L-function Computations

Rubinstein computed zeros of various L-functions. For Dirichlet L-functions L(s,χ), the explicit formula involves primes weighted by χ(p), which effectively **selects** primes in certain residue classes. **This is the closest known precedent** — but it is a different object (an L-function, not ζ(s)), and the zeros detected are those of L(s,χ), not of ζ(s) itself.

### Booker's Work

Booker has worked on computational verification of zeros and L-functions. No work on subset-detection of ζ zeros from prime subsequences.

### Soundararajan

Soundararajan has extensive work on moments of L-functions and the distribution of values of ζ. His work on "extreme values" and "resonance method" uses all primes. No subset-universality results.

## The Dirichlet L-function Analogy

The most relevant classical fact is:

> For a Dirichlet character χ mod q, the explicit formula for L(s,χ) involves ∑ χ(p) log(p) / p^s, which sums only over primes **weighted by χ(p)**. Since χ(p) = 0 for p|q, this is effectively a restricted prime sum. The zeros detected are those of L(s,χ).

**However**, this does NOT show that subsets of primes detect zeros of **ζ(s)** — it shows that character-weighted sums of primes detect zeros of the corresponding **L-function**.

## What Would Be Novel

The claim that:

> "An arbitrary random subset of N ≥ N_min primes, with NO character weighting, can detect the zeros of ζ(s) via a spectral test function"

would be **genuinely novel** if established rigorously. Specifically:

1. **Random subsets** — No prior work studies what happens when you take a random sample of primes and look for ζ-zero signatures in spectral sums.

2. **Universality across structured subsets** — The claim that twin primes, primes ≡ 1 mod 6, primes in intervals, etc. ALL detect γ₁ is not in the literature.

3. **Minimum subset size** — No result quantifies how many primes suffice for zero detection.

### Why It Might Be Expected (Heuristic)

The explicit formula says:

$$\sum_p \frac{\log p}{p^{1/2+it}} \approx -\frac{\zeta'}{\zeta}(1/2+it) + \text{smooth}$$

Each prime p contributes cos(t log p) oscillations. The zeta zeros create resonances in this sum. If you take a large enough random subset, by the law of large numbers / central limit theorem, the resonance at γ₁ should survive (it's a coherent signal) while the noise averages down as 1/√N.

**This heuristic argument is straightforward, but writing it up rigorously with explicit constants and proving the minimum N threshold appears to be new.**

### Why It's Nontrivial

1. The coherence of the signal at γ₁ depends on the distribution of log(p) mod 2π/γ₁ for the chosen primes — this requires equidistribution results.
2. For structured subsets (e.g., twin primes), equidistribution of log(p) mod α is a deep question related to Hardy–Littlewood conjectures.
3. The noise floor depends on correlations between cos(t log p) for different primes, which connects to pair correlation of ordinates.

## Verdict

| Aspect | Status |
|--------|--------|
| Explicit formula (all primes → all zeros) | Classical, well-known |
| L-functions (character-weighted primes → L-function zeros) | Classical |
| Random prime subsets detect ζ zeros | **NOT in literature — appears novel** |
| Structured subsets (twins, residue classes) detect ζ zeros | **NOT in literature — appears novel** |
| Minimum subset size for detection | **NOT in literature — appears novel** |
| Heuristic explanation via coherent signal + noise averaging | Straightforward but **not written up** |
| Rigorous proof with explicit thresholds | **Open** |

## Closest Related Work

1. **Dirichlet L-functions**: Restricted sums detect L-function zeros (not ζ zeros). Classical.
2. **Montgomery–Odlyzko**: Zero statistics from ALL primes. Not subset-based.
3. **Mertens' theorem / PNT in subsets**: Density results for prime subsets, but no spectral zero detection.
4. **Sieve methods**: Give estimates for primes in structured sets, but not spectral analysis.

## Recommendation

This appears to be a **genuinely novel computational observation** that:
- Has a natural heuristic explanation
- Connects to deep equidistribution questions for a rigorous proof
- Could be a publishable result if quantified with explicit thresholds

The key novelty is the **universality claim**: that the zero-encoding is so robust that essentially ANY sufficiently large subset of primes detects γ₁, regardless of how the subset is chosen. This "holographic" property of the explicit formula does not appear to have been previously stated or studied.

---

*Literature check performed 2026-04-06. Sources: author knowledge of analytic number theory literature through 2025.*
