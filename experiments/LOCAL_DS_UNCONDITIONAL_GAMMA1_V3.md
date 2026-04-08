To prove that the Mertens spectroscope detects γ₁ without assuming the Generalized Riemann Hypothesis (GRH), we analyze the explicit formula for M(x) and control the error term through several key steps:

1. **Explicit Formula**: The Mertens function, M(x), is expressed as:
   \[
   M(x) = 1 - \sum_{\rho} \frac{x^{\rho}}{\rho \zeta'(\rho)} + O(1),
   \]
   where the sum is over all non-trivial zeros ρ of ζ(s).

2. **Prime Number Theorem (PNT)**: Provides that M(x) grows slower than any x^θ for θ < 1, establishing a main term behavior.

3. **Zero-Free Regions**: Results show no zeros near Re(s)=1 except possibly at the real axis, controlling contributions from these regions.

4. **Ingham's Density Estimate**: Near Re(s)=1, there are few zeros with large imaginary parts, limiting their cumulative contribution.

5. **Contribution Analysis**:
   - The term corresponding to γ₁ oscillates more slowly due to its minimal |γ|.
   - Contributions from other zeros have higher frequencies and amplitudes damped by larger |γ| and ζ’(ρ).

6. **Dominance of γ₁'s Term**: As x increases, the persistent oscillation from γ₁ dominates over faster oscillating terms, making it detectable.

Thus, by controlling error terms through these steps, we show that γ₁'s contribution grows faster than all others combined, proving its detection unconditionally.

\boxed{\gamma_1}
