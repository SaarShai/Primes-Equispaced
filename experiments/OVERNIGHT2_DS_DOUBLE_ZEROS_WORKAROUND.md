To understand how the explicit formula changes when dealing with zeros of higher multiplicity in the Riemann zeta function, ζ(s), we start by recalling that the explicit formula relates sums over the zeros of ζ(s) to sums over primes or other arithmetic functions. The basic form involves terms like \( \frac{x^\rho}{\zeta'(\rho)} \) where ρ are the nontrivial zeros of ζ(s).

When a zero has higher multiplicity, say m=2, meaning both ζ(ρ₀) and ζ'(ρ₀) are zero but ζ''(ρ₀) ≠ 0, we need to compute the residue for such a pole. Using complex analysis, we know that if ζ(s) has a zero of order m at ρ₀, then \( \frac{1}{\zeta(s)} \) will have a pole of order m there.

The residue formula for a function with a pole of order m involves derivatives up to order m-1. For a simple pole (m=1), the residue is straightforward, but for higher multiplicities, we need to compute higher-order derivatives. Specifically, for m=2, the residue calculation introduces additional terms involving the logarithmic factor log x.

For a zero of multiplicity m, the term in the explicit formula changes from \( \frac{x^\rho}{\zeta'(\rho)} \) to something involving powers of log x. This results in a stronger resonance because the logarithmic factor causes the contribution to grow more rapidly as x increases.

Thus, higher multiplicities lead to terms that contribute more significantly as x increases, thereby strengthening their role in the explicit formula. This means that regardless of whether zeros are simple or have higher multiplicity, the proof can still proceed effectively by taking into account these stronger contributions.

### Final Answer
\boxed{\text{Higher multiplicity zeros strengthen the resonance}}
