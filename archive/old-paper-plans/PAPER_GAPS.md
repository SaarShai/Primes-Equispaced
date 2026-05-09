# Paper Gaps Analysis — What's Missing and Should Be Added
# Created: 2026-04-05

## MISSING FROM PAPER (should add)

### HIGH PRIORITY (core new results)

1. **Farey Spectroscope** (entire Section 5 in paper plan)
   - F(γ) = |Σ R(p)·p^{-1/2-iγ}|² detects zeta zeros
   - γ₁ = 14.05 confirmed, r=0.953 amplitude correlation
   - Multi-character extension detects L-function zeros
   - 6 NEW figures ready (farey_spectroscope, farey_vs_classical, convergence,
     phase_lock, zero_contributions, multi_character_spectroscope)
   - **Figures needed in paper:** All 6 new figures
   - **Tasks to strengthen:** extend data (R_bound running), amplitude verification

2. **Damage/Response Decomposition** (Section 3 enhancement)
   - R₁ (damage) always negative, R₂ (response) always positive
   - Explains WHY ΔW < 0: primes damage, old fractions overcompensate
   - **Figure needed:** Side-by-side visualization of R₁ vs R₂ across primes

3. **D(1/p) = 1 - |F_{p-1}|/p Proposition** (Section 2 addition)
   - PROVED, elementary. D(1/p) ≈ -3p/π². Single fraction = 65% of damage.
   - **No figure needed** — clean formula with verification table

4. **Composites ω(n)≥2 Characterization** (Section 6 addition)
   - ω(n)≥2 conjecture DISPROVED: N=94=2×47, N=146=2×73 have ω=2 and ΔW<0. Correct: statistical tendency only.
   - **Figure needed:** Scatter plot of ΔW(n) colored by ω(n)

5. **GK Concentration** (Section 6 addition)
   - Top 20% of fractions → 94% of |Σ D·δ|
   - **Figure needed:** Cumulative contribution curve vs depth threshold

### MEDIUM PRIORITY (supporting results)

6. **Spectral Amplitude Matching** (Section 5 subsection)
   - F(γ_k)/F(γ₁) ≈ |c_k/c₁|² with r=0.953 correlation
   - **Figure needed:** Predicted vs observed amplitude scatter

7. **Gaussian Farey / Ford Spheres** (Section 7 future directions)
   - 1,344 points enumerated, D*=0.055
   - Dedekind zeros detectable via factorization
   - **Figure exists:** gaussian_farey_N50.png

8. **Goldbach Δr** (Section 7 future directions)
   - Per-step analysis, R²=0.85 for singular series prediction
   - Spectroscope inconclusive at n≤4000
   - No figure needed for future directions

### ALREADY IN PAPER (confirm up-to-date)

- Sign Theorem counterexample at p=243,799 ✅
- Chebyshev bias / phase-lock ✅
- Two δ definitions ✅
- L-function extension ✅ (but needs expansion for multi-character results)
- Entropy monotonicity ✅ (brief mention — could expand with Lean proof)
- Permutation identity ✅ (brief mention)
- Density → 1/2 ✅

### SHOULD REMOVE

- Three-body: Only 1 mention ("orbit's squared displacement"), NOT about 3BP.
  No removal needed — it's mathematical orbit, not three-body.

## FIGURE AUDIT

### Existing figures (10 in paper)
1. fig_circle_farey.png — Farey sequence on circle
2. fig_wobble_circle.png — Wobble visualization
3. fig_void_filling.png — Void filling mechanism
4. fig_universal_formula.png — Universal formula plot
5. fig_bridge_vectors.png — Bridge identity vectors
6. fig_sigmoid.png — Sigmoid fit
7. fig_mertens_violations.png — Mertens violations
8. fig_mertens_bias_circle.png — Mertens bias on circle
9. fig_delta_w_signs.png — ΔW sign pattern
10. fig_shift_map.png — Shift map

### New figures to ADD (6 ready + 4 needed)
11. farey_spectroscope.png — ★ MAIN NEW FIGURE
12. farey_vs_classical_zeros.png — Juxtaposition with Hardy Z(t)
13. farey_spectroscope_convergence.png — Convergence
14. phase_lock_visualization.png — R(p) tracking γ₁
15. zero_contributions.png — Relative zero strengths
16. multi_character_spectroscope.png — Four L-functions

### Figures NEEDED (not yet created)
17. damage_response_comparison.png — R₁ vs R₂ across primes
18. composites_omega_scatter.png — ΔW(n) by ω(n)
19. gk_concentration_curve.png — Cumulative |D·δ| vs depth threshold
20. amplitude_matching_scatter.png — Predicted vs observed |c_k|²

### Figures to CHECK/UPDATE
- fig_delta_w_signs.png: Does it show the Chebyshev bias overlay? If not, update.
- fig_mertens_violations.png: Does it include p=243,799? If not, update.
