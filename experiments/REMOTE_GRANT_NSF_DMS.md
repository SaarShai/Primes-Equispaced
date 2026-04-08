## Summary (2 sentences)

Spectroscopic methods leverage compensated periodograms & local z-scores to detect L-function zeros via Farey sequence discrepancies. Proposal targets 50K budget, Lean-verified GRH pipeline, and extension to degree-2 L-functions using 422 identities.

## Analysis

| Category | Specification / Innovation | Status |
| :--- | :--- | :--- |
| **Core Method** | Compensated periodogram (alpha-tunable pre-whitening) | Novel |
| **Filter** | gamma^2 matched filter (Csoka 2015 cited) | Applied |
| **Normalization** | Local z-score + Universality theorem (conditional) | Implemented |
| **Test** | Chowla spectroscopic test (N=500K, RMSE=0.066) | Positive |
| **Phase** | phi = -arg(rho_1*zeta'(rho_1)) | SOLVED |
| **Verification** | 422 Lean 4 identities (Mathlib formalization) | 100% Verified |
| **Pipeline** | GRH verification for 17 characters | Active |
| **Scale** | Extend to degree-2 L-functions, N=10^8 | Target |
| **Computing** | Three-body: 695 orbits, CF periodic table | Data |
| **Budget** | 50K/2yr (Personnel, Compute, Travel) | DMS Compliant |

## Verdict/Next Steps

*   Authorize computational methodology track (DMS-2400000 series).
*   Integrate Csoka 2015 classical reference into formalism.
*   Deploy phase phi calculation in GRH pipeline immediately.
*   Commence N=10^8 scaling tests Q3 2024.
*   Finalize Lean library submission to Mathlib Month 6.
*   Submit full grant package to NSF.
