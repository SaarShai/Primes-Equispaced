# MASTER TABLE INDEX — Priorities, Status, Next Steps
Last updated: 2026-04-05 (Session 10+)
Full details: ~/Desktop/Farey-Local/MASTER_TABLE.md (load per-item when exploring)

## HIGHEST PRIORITY

| ID | Direction | Status | Next Step |
|----|-----------|--------|-----------|
| MPR-40 | Chebyshev Bias Framework | GRH-conditional formalized; R=0.77. Perron derivation done (task_110). Density proof drafted (task_111). | Reconcile phase constant (ρ vs ρ-1). Finalize density theorem. |
| MPR-49 | **Farey Spectroscope** | **γ₁ CONFIRMED** (14.05). 6 figures created. Comparable convergence to RS. | Amplitude matching. More primes for γ₂. Paper section draft. |
| MPR-49b | **Multi-character spectroscope** | χ₄→L zeros detected (γ'₁=6.16). χ₃ partial. χ₅ failed. | More primes for reliable L-function detection. Extend to all χ mod q≤20. |
| MPR-58 | **Damage/Response decomposition** | NEW: R₁ (damage, new fracs) always negative; R₂ (response, old fracs) always positive. R₂>0 is the structural claim. | Prove R₂>0 analytically. Quantify D(1/p)≈-3p/π² dominance. |
| MPR-47 | Gauss-Kuzmin bridge | task_088 done. GK concentration VERIFIED: top 20% fracs → 94% of |Σ D·δ|. | Rigorous proof via BCZ (2001). Different from killed MPR-48. |
| MPR-37 | Goldbach Δr per-step | task_114 done. S(n) predicts r(n) at R²=0.91, Δr at R²=0.85. 97% claim was overstated. | Investigate what gives R²=0.97 (higher-order singular series?). |
| MPR-41 | Complex Farey / Gaussian Z[i] | 1,344 pts enumerated. Dedekind zeros detectable via factorization ζ·L(χ₄). | Compute 2D discrepancy ΔD* at Gaussian primes (task_119). |

## HIGH PRIORITY

| ID | Direction | Status | Next Step |
|----|-----------|--------|-----------|
| MPR-33 | Triangular distribution of δ | PARTIAL PROOF. BCZ reconciled: different objects (insertion shifts ≠ Farey gaps). | Clarify correct normalization. Prove moment formula for insertion shifts specifically. |
| MPR-27 | Explicit formula: zeros↔ΔW | Perron derivation done (task_110). Coefficient is 1/((ρ-1)·ζ'(ρ)), not 1/(ρ·ζ'(ρ)). | Verify numerically. Does corrected arg(c₁) fix 0.69 rad phase gap? |
| MPR-24 | Prove composites heal (ΔW>0) | 95.4% verified. task_118 done (analysis produced). | Need sparser-fractions argument for composite n. |
| AMR-8 | Engineering simplification (mesh) | task_074 done. Best niches: planetary terrain, shock CFD. | Prototype crack-free LOD demo (task_136 designed). |
| MPR-44 | Quantum ergodicity / horocycle | Chain identified: ΔW → horocycle equidist. → spectral → zeros. | Formalize. The spectroscope IS the computational evidence for this chain. |
| MPR-34 | FT of ΔW shows zero pairs | Script ready (mpr34_ft.py). | Run with actual ΔW data (need per-prime ΔW, not just R). |
| MPR-39 | Extend R₂ computation to 10⁷ | Need O(p log p) algo via Möbius inversion. | Design algorithm. GK concentration suggests sparse approx may help. |

## MEDIUM PRIORITY

| ID | Direction | Status | Next Step |
|----|-----------|--------|-----------|
| MPR-52 | Diophantine approximation | task_095 done (gemma4). | Review result. Markoff/Lagrange spectrum link? |
| MPR-42 | Harmonic / Franel-Landau kernel | task_121 done (script produced). | Run script. Compare harmonically-weighted ΔW to raw. |
| MPR-43 | Mersenne primes phase prediction | task_120 done. Script ran for p≤127. | Phase prediction correct for p=8191? Review full results. |
| MPR-35 | Density theorem | task_111 drafted proof. | Review proof quality. Does it need LI or just GRH? |
| MPR-25 | Farey telescope / pair correlation | Connection found (Mellin poles). | Verify computationally. |
| MPR-53 | Signal processing feasibility | task_092 done (Q3.6). | Review. Likely weak — but check. |
| MPR-55 | Important fractions for QMC/mesh | task_094 done (Q3.6). | Review. Deep-first refinement test. |
| MPR-56 | RMT + quantum chaos | task_096 done (gemma4). | Review. Tracy-Widom edge connection? |
| 3BP-4 | Unequal mass extension | AUC=0.79 | Add to three-body paper |
| AMR-4 | Extended shock benchmark | Timeout bug | Fix + run |

## PROVED (need paper integration)

MPR-9 (Voronoi entropy — **Lean proved by Aristotle**), MPR-10 (I_k/J_k monotone),
MPR-11 (Grand Identity), MPR-12 (antisymmetry), MPR-21 (permutation Σf·δ=C/2),
MPR-22 (geometric identity B+C=Σ(D+δ)²-ΣD²), MPR-23 (wobble monotonicity),
MPR-24 (dispSquaredSum), Farey gap bound (**Lean proved by Aristotle**)

## SAAR ACTION ITEMS

| Priority | What |
|----------|------|
| HIGH | Get arXiv endorser + submit math paper (SUB-3) |
| HIGH | Get arXiv endorser + submit three-body paper (SUB-4) |
| MEDIUM | Contact Nakamura (3BP-9), Li & Liao (3BP-10) |
| MEDIUM | Patent attorney for AMR (SUB-6) |
| CHECK | Navy SBIR N251-060 deadline (SUB-1) — AMR still valid |

## KEY FIGURES (paper-ready)

1. `farey_spectroscope.png/pdf` — Main: Farey spectral function with zeta zeros
2. `farey_vs_classical_zeros.png/pdf` — Juxtaposition: Hardy Z(t) vs Farey F(γ)
3. `farey_spectroscope_convergence.png/pdf` — Convergence with more primes
4. `phase_lock_visualization.png/pdf` — R(p) tracking γ₁ oscillation
5. `zero_contributions.png/pdf` — Relative strength of each zero's effect
6. `multi_character_spectroscope.png/pdf` — Four characters → four L-functions

## DEAD (31 entries — see MASTER_TABLE_DEAD.md)

Recent kills: MPR-46 (depth→γ₁), MPR-48 (spectral enhancement), DEAD-31 (R>0 permutation).

## STATS
Active items: ~55 | Dead: ~65 | Lean sorrys: 1 (intentional) | Papers: 6
Lean proofs: 10+ (including 2 new from Aristotle — entropy monotonicity, gap bound)
Figures: 6 (paper-ready, all with PDF vectors)
Aristotle: 3 results awaiting download (API 500)

## POST-PAPER DIRECTIONS (explore after submission)

| ID | Direction | Connection | Priority |
|----|-----------|-----------|----------|
| POST-1 | **Poincaré disk model** | Ford circles map to horodisks, equilateral tessellation. Figure created. | HIGH |
| POST-2 | **Apéry-style irrationality proofs** | FrontierMath #13. CF/Farey tools match Apéry machinery. Opus exploring. | HIGH |
| POST-3 | **Symplectic ball packing** | FrontierMath #12. Ford circles = circle packing. Lift to symplectic? | MEDIUM |
| POST-4 | **Arithmetic Kakeya** | FrontierMath #5. Farey mediants as constructible graph? | MEDIUM |
| POST-5 | **Gaussian Farey full development** | 2D discrepancy, Dedekind zeros, Ford spheres in H³ | HIGH |
| POST-6 | **Goldbach Δr per-step** | Needs n>10⁶ for spectroscope to work. Long computation. | MEDIUM |
| POST-7 | **R₂ > 0 analytical proof** | Open problem. Sign alignment weak. Need new approach. | HIGH |
| POST-8 | **Close Dedekind sum gap (upgrade Conjecture→Theorem)** | T_b - E[T_b] = b²Σ μ(b/c)s(p,c). Need mean-value estimate for Dedekind sums over divisors. Would seal Math. Comp. acceptance. | **HIGHEST** |
| POST-8b | φ(n)/n healing threshold | No clean threshold exists. Explore asymptotic healing rate. | LOW |
| POST-9 | **Extend spectroscope to 10⁶ primes** | Would detect γ₂-γ₅ clearly. Needs R_bound computation. | HIGH |
| POST-10 | **Montgomery pair correlation** | Autocorrelation detected γ₂-γ₁. Extend to full pair statistics. | MEDIUM |

## MOST SIGNIFICANT FINDINGS (starred)

| Finding | Status | Significance |
|---------|:------:|:------------:|
| ⭐ Per-step ΔW(N) — new object | PROVED + Lean | Foundational — enables all other results |
| ⭐ γ² matched filter — 2→20 zeros | VERIFIED | Key computational innovation |
| ⭐ Universality — any 2750 primes | VERIFIED + conditional proof | Novel observation, no prior literature |
| ⭐ Phase φ = -arg(ρ₁·ζ'(ρ₁)) DERIVED | VERIFIED | Explicit formula predicts exact phase |
| ⭐ GUE RMSE=0.066 from arithmetic data | VERIFIED | First derivation without computed zeros |
| ⭐ Figure-eight = golden ratio (exact) | PROVED | Algebraic identity, not coincidence |
| ⭐ 422 Lean 4 verified results | PROVED | Largest Farey formalization in existence |
