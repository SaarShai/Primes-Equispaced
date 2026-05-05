# Theorem B — 5 Routes to Unconditional Proof

## Goal
Prove M_F(T) = (2/(3π))·⟨c_f⟩·T·log⁴X family-averaged unconditional for the Petersson weight aspect.

## Where We Are

**Verified unconditional inputs (load-bearing):**
- DFS Lemma 2.4 + ILS Theorem 1.2 (η<1 squarefree, /tmp/ils.txt + /tmp/dfs.txt)
- M-N Conjecture (16) verbatim (/tmp/milinovich_ng.txt)
- Symbolic CFKRS: 16 = 2⁴ confirmed (sympy)
- Reverse-engineer decomposition: **2/(3π) = (1/(2π)) · (1/12) · 16** where 1/12 is Hughes-Mezzadri unitary Barnes-G baseline and 16 is d^{2k} family-lift
- KM 1997 + ILS §8 unconditional family zero-density (cage half-width √145/(12π) preserved)
- Conrey-Snaith 2007 §7 IS unitary not orthogonal (G7 caught miscitation; substantive m_O=1 survives via CFKRS 2005 §3.1)

**The wall (8 independent confirmations):** support-4 level density / 4-parameter ratios off-diagonal / E1+E2+E3 joint closure — all equivalent, all open.

**Most promising near-term leads (from completed agents):**
- **S4 sufficient conditions** (Weakest_sufficient_conditions.md): KMV §5 variance + KMV §4 mean + ILS §3 sign all UC; pending 10-min PARI Mellin check of KMV §5 leading constant. Conf 0.55 → 0.85 if passes.
- **C2 RMT match** (Reverse_engineer_constant.md): orthogonal Barnes-G coefficient = 1/12; testable via Monte Carlo on O(2N) at N=50,100,200.
- **Subset A** (Necessary_conditions_inverse.md): NC₈+NC₁₁+NC₁₂ gives Theorem B under RH(ζ) only (NOT full GRH).
- **NC₁₅ geometric/motivic period** — only unexplored angle (rate-limited mid-flight).

## Tasks (post 8:20pm rate-limit reset)

### Phase 0 — Comprehensive lit research (MUST be first)
- [ ] **T0**: Sonnet 4.6 — Research everything on M-N conjecture, all attempted proofs, all citations of arXiv:1306.0854. Identify where our 8-fold negative convergence places us vs the field. Identify any 2024-2026 results that close E1/E2/E3 partially. → Verify: file `Theorem_B_field_landscape.md` exists with verbatim citations and "where we are ahead / behind" summary.

### Phase 1 — Most likely routes (parallel)
- [ ] **T1 (most likely #1)**: Opus 4.7 high — S4 sufficient conditions verification. Run PARI/GP Mellin computation of KMV §5 leading constant in level-aspect normalization. If c_1 = 4/(3π), Theorem B-exact uncond via S4. Provide: KMV 2002 PDF download (curl + pdftotext at /tmp/kmv2002.pdf), Weakest_sufficient_conditions.md context, MANDATORY no-fabrication protocol, single agg rule. → Verify: `S4_KMV_Mellin_verify.md` with PARI output + verdict.

- [ ] **T2 (most likely #2)**: Opus 4.7 high — C2 RMT Monte Carlo. Adapt B2_cue_mc_K10k.py for O(2N) sampling, predict 2nd moment of |Z'(1)|² at N=50,100,200, check 1/12 + O(1/N). If passes, decomposition jumps to 0.85; combined with S4 → unconditional Theorem B. Provide: Reverse_engineer_constant.md context, existing Monte Carlo code path, mandatory no-fab. → Verify: `C2_orthogonal_MC_check.md` with raw N=50/100/200 outputs.

- [ ] **T3 (most likely #3)**: Opus 4.7 high — Subset A RH(ζ)-only formalize (retry, was rate-limited). Provide: Necessary_conditions_inverse.md NC₈+NC₁₁+NC₁₂ exact statements, /tmp/milinovich_ng.txt, /tmp/cfkrs.pdf, mandatory no-fab. → Verify: `Subset_A_RH_zeta_only.md` 2-page proof + companion verification file.

### Phase 2 — Creative routes (parallel)
- [ ] **T4 (creative #1)**: Opus 4.7 high — NC₁₅ geometric/motivic period (retry, was rate-limited). 2/(3π) as Beilinson regulator / Selberg trace coefficient / vol-fundamental-domain identity. Provide: Necessary_conditions_inverse.md NC₁₅ detail, mpmath access, mandatory verbatim citations + no-fab protocol. → Verify: `NC15_geometric_motivic_period.md` with 10+ candidates evaluated.

- [ ] **T5 (creative #2)**: Opus 4.7 high — Aristotle Lean cage formalization (retry, was rate-limited). Mertens decomposition Lemma 3.1 + cage half-width algebra are decide-style. Lean-verified cage gives ground truth regardless of analytic concerns. Provide: Mertens_restricted_B_positivity.md, CrossTermPositive.lean path, harmonic.fun Aristotle access, mandatory no-fab. → Verify: `CageHalfWidth.lean` + `MertensDecomposition.lean` compile in Mathlib; report file confirms.

### Phase 3 — Quick parallel small tasks (Sonnet)
- [ ] **T6**: Sonnet 4.6 — S-Y 2010 → Li 2024 citation audit (retry, rate-limited). Edit 8 files to mark conditional/uncond status correctly. → Verify: `SY_Li_citation_corrections.md` with diff summary.

- [ ] **T7**: Sonnet 4.6 — Family-averaged PARI numerical at T=10³ on 14-curve squarefree ladder with finite-T inflation correction. → Verify: `family_avg_finite_T_fix_REPORT.md` with raw outputs + verdict.

- [ ] **T8**: Sonnet 4.6 — ζ' calibration (retry, rate-limited). Compute Σ |ζ'(ρ)|²/(T·log⁴T) at T=10³, 10⁴, 10⁵; check approach to 1/(24π). Tests possibility (a) slow convergence universal. → Verify: `zeta_prime_calibration_REPORT.md`.

### Phase 4 — Verification (last)
- [ ] **T9**: Adversarial-reviewer agent on every Phase 1-2 success. Hostile review of any "this works" claim. → Verify: per-result audit file with LANDS/LANDS-WITH-CAVEATS/BREAKS verdict.

## Mandatory protocol for every agent (embedded in prompt)
1. **NO fabrication**: every cited theorem must be verified by curl + pdftotext on the actual paper. Quote verbatim with page/eq number.
2. **Single confidence aggregation rule**: state at start, never switch mid-document.
3. **Honest verdict**: if route fails, state precisely why; if succeeds, identify gaps.
4. **Cross-reference prior failures**: read /Users/saar/Farey 4.7 solutions/{RMT_Painleve_GRH_bypass.md, RankinSelberg_trace_attack.md, Voronoi_Kuznetsov_GRH_bypass.md, arxiv_2601_06292_analysis.md, Theta_lift_GRH_bypass.md, FirstPrinciples_creative_attack.md, E1_E2_E3_barrier_attack.md, Necessary_conditions_inverse.md, Disprove_attempt.md} so as not to repeat work.
5. **Don't switch families**: weight aspect Petersson family F_k = S_k*(N) squarefree N, k → ∞ along k = T^a, 1<a<2.

## Done When
- [ ] Either: T1 + T2 succeed → unconditional Theorem B-exact (Annals)
- [ ] OR: T3 succeeds → Theorem B under RH(ζ) only (publishable progress)
- [ ] OR: T4 succeeds → geometric identity for 2/(3π) (Compositio-tier novel result)
- [ ] OR: T5 succeeds → Lean-verified cage statement (rigorous credit regardless)

## Notes
- Rate limit resets 8:20pm Europe/London. Defer Phase 1 Opus dispatch until then.
- T0 (Sonnet) can run before reset.
- T1 is the **single highest-leverage task**: 10-min PARI verification with potential to deliver unconditional proof.
- Multiple parallel routes hedge against any single one failing.
- The user has explicitly directed: NO submission until full unconditional proof.
