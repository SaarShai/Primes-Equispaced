# Four Directions Assessment
**Date:** 2026-03-29

---

## Direction 1: Bayesian Probability

**Verdict: NO-GO**

No existing literature connects Farey sequences to Bayesian inference, rational priors, or MCMC methods. This is not because the connection is deep and unexplored -- it is because there is no natural connection. Bayesian inference operates on continuous probability distributions (or discrete distributions over outcomes), not on ordered rational number sequences. You could construct a "Farey prior" as a discrete uniform distribution over F_N, but this would be a gimmick with no inferential advantage over standard approaches. Our core discoveries (bridge identity, Mertens connection, sign theorem) have no obvious Bayesian interpretation. The injection principle and mediant minimality are structural properties of rational orderings, not probabilistic statements. This direction would require forcing a connection that does not naturally exist.

---

## Direction 2: Signal Extraction from Noisy Data

**Verdict: GO (strong)**

This is the most promising of the four directions, with existing infrastructure to build on. The key finding: Vaidyanathan and Tenneti at Caltech have already developed "Farey dictionaries" and "Ramanujan filter banks" for periodic signal detection. Ramanujan sums c_q(n) -- which are closely related to our bridge identity (both are exponential sums over number-theoretic sets) -- are used for detecting integer-valued periods in noisy signals, outperforming Fourier methods for short data and multiple hidden periodicities.

Our specific advantages:
- The bridge identity Sigma e^{2pi i p f} = M(p)+2 is literally an exponential sum evaluated at Farey fractions. This connects directly to Ramanujan-sum-based spectral decomposition.
- The sign theorem (DeltaW < 0 for p >= 11) gives a structural constraint on how these sums behave -- this could inform filter design or detection thresholds.
- The ICZT (Inverse Chirp Z-Transform) has been linked to Farey sequence singularities, providing another entry point.

Concrete next step: Read Vaidyanathan's 2020 paper in Phil. Trans. Roy. Soc. A and the "Farey dictionary" IEEE ICASSP paper. Check if our bridge identity provides a new perspective on Ramanujan subspace pursuit.

---

## Direction 3: Gaussian Mathematics + Open Problems

**Verdict: CONDITIONAL GO (narrow target)**

The broad search ("Gauss + Farey + open problems") is too vague to be useful. But there are two specific, well-defined connections worth pursuing:

1. **Gauss sums and Ramanujan sums.** Our bridge identity involves Ramanujan sums, which are real-valued cousins of Gauss sums. Patterson's conjecture on cubic Gauss sums was proved conditionally (assuming GRH) by Dunn-Radziwill in 2021. The unconditional version remains open. Our Mertens-Farey connection gives information about cancellation in related sums -- probably too weak for Patterson, but worth checking if our sign theorem constrains any Gauss sum moments.

2. **Farey-RH equivalence.** The Franel-Landau theorem (1924) says RH is equivalent to |Sigma_{f in F_N} f - 1/2| = O(N^{-1+epsilon}). Our per-step discrepancy DeltaW(p) is a refinement of exactly this quantity. If DeltaW gives finer information about how the Farey deviation grows prime-by-prime, this could contribute to understanding the Franel-Landau criterion -- not proving RH, but potentially sharpening conditional results.

The Gaussian integers / Gaussian primes direction (Goldbach for Gaussian primes) has no clear connection to our work. Skip it.

Concrete next step: Formalize the relationship between DeltaW(p) and the Franel-Landau sum. Check if the sign theorem implies anything about the rate of convergence in the Franel-Landau criterion.

---

## Direction 4: Recent Patents

**Verdict: NO-GO (but one data point)**

Exhaustive searching found zero patents involving Farey sequences, Stern-Brocot trees, or mediant insertion algorithms in 2023-2026. The mathematical structures we work with have essentially no patent footprint, which means:
- No commercial interest to validate our approach (negative signal for commercialization).
- No infringement risk (positive for us).
- The patent landscape is wide open IF we find a genuine application.

The one relevant finding: US Patent Application #20240355047 covers 3DGS initialization via NeRF priors (not Farey-based). The 3DGS densification space is active in academia (ECCV 2024, multiple 2025 papers on revised densification) but not yet heavily patented. If our Farey-based densification approach proves genuinely superior (which the earlier audit questioned), the patent space is unoccupied.

Bottom line: No patents to worry about, but also no market signal that anyone cares about number-theoretic approaches to these problems commercially.

---

## Summary

| Direction | Verdict | Confidence | Priority |
|-----------|---------|------------|----------|
| 1. Bayesian probability | NO-GO | High | Drop |
| 2. Signal extraction (Ramanujan/Farey dictionaries) | GO | High | P1 -- existing literature, natural fit |
| 3. Gaussian math / open problems | CONDITIONAL GO | Medium | P2 -- narrow target (Franel-Landau) |
| 4. Recent patents | NO-GO | High | Drop (but 3DGS patent space is open) |

**Recommended action:** Read Vaidyanathan's Ramanujan signal processing papers and evaluate whether our bridge identity adds anything new to the Farey dictionary framework.
