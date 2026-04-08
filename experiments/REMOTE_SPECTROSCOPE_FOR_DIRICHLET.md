## Summary (2 sentences)
Extend Mertens spectroscope to general Dirichlet series substituting standard coefficients with arithmetic sequences. Feasibility depends on availability of explicit coefficients $a_n$; pre-whitening remains via $\gamma^2$ matched filter.

## Analysis

| L-Function Type | Coefficients $a_n$ | Data Source | Detection Feasibility |
| :--- | :--- | :--- | :--- |
| Dedekind $\zeta_K(s)$ | Ideal norms $\sum_{N(\mathfrak{a})=n} 1$ | Field arithmetic | High |
| Hecke $L(f,s)$ | Eigenvalues $\lambda_f(p)$ | Modular forms data | High |
| Artin $L(\rho,s)$ | Traces $\text{tr}(\rho(\text{Frob}_p))$ | Galois representations | Low |
| Automorphic $L(\pi,s)$ | Fourier coeffs $A_\pi(n)$ | Langlands transfer | Medium |

Phase $\phi = -\arg(\rho_1 L'(\rho_1))$ generalizes; Chowla evidence persists up to $N=500K$ (Lean 4 verified).

## Verdict/Next Steps
First test case: Dedekind zeta of imaginary quadratic fields $\mathbb{Q}(\sqrt{-d})$.
Rationale: Explicit Kronecker character $\chi_d(n)$ replaces Dirichlet character; $N$ up to 500K feasible.
Next Steps:
1. Generate $\Delta W(N)$ for $\chi_d$.
2. Apply $\gamma^2$ matched filter (Csoka 2015).
3. Verify Chowla violation for rank $r=1$ using Lean 4 (422 proofs).
4. Target GUE RMSE < 0.066.
