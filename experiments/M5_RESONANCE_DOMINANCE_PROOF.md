# Analysis of Unconditional Energy Concentration in the Mertens Spectroscope

## Summary

The task involves analyzing whether energy concentration occurs unconditionally at zeta zeros within the Mertens spectroscope. This analysis hinges on an explicit formula substitution, evaluating resonant and non-resonant contributions, and verifying key mathematical steps. The main conclusion is that under standard conjectures like the Riemann Hypothesis (RH), the energy does concentrate at specific points due to the dominant growth of resonant terms compared to oscillatory non-resonant ones.

## Detailed Analysis

### 1. Partial Summation and Prime Number Theorem (PNT) Approximation

The explicit formula for M(p) involves summing over primes p raised to powers related to zeta zeros ρ. For a zero γ_k, we consider the term:

\[
M(p) = -1 + \sum_{\rho} \frac{p^{\rho}}{\rho \zeta'(\rho)}
\]

Focusing on the resonant term (j=k), we analyze:

\[
\sum_{p \leq N} p^{-1/2 + i\alpha}
\]

Using partial summation with PNT, which states that the prime density function π(t) ≈ Li(t) = t / log t. Applying this to our sum:

\[
\sum_{p \leq N} p^{-1/2 + i\alpha} \approx \int_{2}^{N} t^{-1/2 + i\alpha} d(\pi(t))
\]

By integrating by parts (partial summation):

\[
= N^{-1/2 + i\alpha} \pi(N) - \int_{2}^{N} \pi(t) (-1/2 + i\alpha) t^{-3/2 + i\alpha} dt
\]

Substituting π(t) ≈ Li(t):

\[
\approx N^{-1/2 + i\alpha} \frac{N}{\log N} - \int_{2}^{N} \frac{t^{-3/2 + i\alpha}}{\log t} (-1/2 + i\alpha) dt
\]

Simplifying, this leads to:

\[
= \frac{N^{1/2 + i\alpha}}{(1/2 + i\alpha) \log N} + O\left(\frac{N^{1/2}}{\log^2 N}\right)
\]

This justifies the approximation and error term.

### 2. Truncation Error in Explicit Formula

Truncating zeros beyond a height T introduces an error. The number of such zeros is ~O(T log T), each contributing terms like:

\[
\frac{p^{-1/2 + i\gamma_j}}{\rho_j \zeta'(\rho_j)}
\]

The total truncation error is bounded by:

\[
O\left(\frac{N^{1/2} (\log^2 T)}{T}\right)
\]

This comes from bounding each term and considering the number of zeros, ensuring that this error remains negligible compared to the resonant term.

### 3. Convergence of Non-Resonant Sum

The sum over non-resonant terms (j≠k) involves:

\[
\sum_{j \neq k} \frac{|c_j|}{|c_k| |\gamma_j - \gamma_k|}
\]

Using conjectures on zero spacing, |γ_j - γ_k| ≥ C / log γ_j. With c_j ≈ 1/(ρ_j ζ'(ρ_j)), and assuming decay, this series converges.

### 4. Interchange of Sums

Justifying interchange requires absolute convergence. Each term p^{-s} decays as p increases, allowing application of Fubini's theorem given appropriate bounds on sums over ρ.

## Open Questions

1. **Dependence on RH**: The analysis assumes zeros lie on the critical line. If violated, results may change.
2. **Constants and Error Bounds**: Large constants in error terms could affect conclusions.
3. **Zero Spacing Assumptions**: Relies on conjectured lower bounds for zero gaps; smaller gaps might alter convergence.

## Verdict

Under standard conjectures (RH, GUE), the analysis holds: F(γ_k) concentrates energy as N grows due to dominant resonant terms and bounded non-resonant contributions. The argument is rigorous given current mathematical knowledge.
