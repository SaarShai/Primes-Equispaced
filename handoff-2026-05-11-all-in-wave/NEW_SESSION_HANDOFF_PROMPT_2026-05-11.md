# New Session Handoff Prompt

Use this prompt to continue the primes-equispaced/Farey/Koyama/EC-NDC work in a fresh project session.

```text
You are continuing the Farey NOW / primes-equispaced research project.

Working roots:
- Wiki/root: /Users/za/Documents/Farey NOW
- Active project: /Users/za/Documents/Farey NOW/primes-equispaced
- Current date in prior session: 2026-05-11

First steps:
1. Start in /Users/za/Documents/Farey NOW.
2. Read AGENTS.md, then start.md.
3. Run ./te doctor.
4. Read token-economy.yaml, L0_rules.md, L1_index.md.
5. Then move to primes-equispaced and read:
   - HANDOFF.md
   - L2_facts/farey-claim-ledger.md
   - log.md, top entries only
   - handoff-2026-05-11-all-in-wave/ALL_IN_WAVE_SYNTHESIS_2026-05-11.md
   - handoff-2026-05-11-all-in-wave/EC_STOCHASTIC_NULL_REPORT_2026-05-11.md
   - handoff-2026-05-11-all-in-wave/EC_KERNEL_NULL_SUMMARY_2026-05-11.md

Hard boundary:
- Do not edit Koyama email/correspondence drafts unless the user explicitly asks.
- In particular do not edit:
  - correspondence/KOYAMA.md
  - projects/farey-research/koyama-correspondence.md
  - handoff-2026-05-09-followup/Koyama_email_to_Koyama_claimsafe_draft_2026-05-11.md
- Existing dirty correspondence files are preexisting state; do not clean or revert them.

Current high-level status:
- No theorem is currently promoted.
- Progress is meaningful, mostly by closing false exits and sharpening exact targets.
- The EC smoothing numerical front improved materially, but remains non-theorem evidence until full controls and theory close.

Most recent all-in wave artifacts:
- handoff-2026-05-11-all-in-wave/ALL_IN_WAVE_SYNTHESIS_2026-05-11.md
- handoff-2026-05-11-all-in-wave/GL1_SHIFTED_PERRON_PACKET_2026-05-11.md
- handoff-2026-05-11-all-in-wave/H1_SHELL_ANTI_SMALL_DERIVATIVE_PACKET_2026-05-11.md
- handoff-2026-05-11-all-in-wave/H1_FIXED_WEIGHT_PV_PACKET_2026-05-11.md
- handoff-2026-05-11-all-in-wave/H1_WEIGHTED_L1_ATTACK_PACKET_2026-05-11.md
- handoff-2026-05-11-all-in-wave/H2_SYM2_ENDPOINT_PACKET_2026-05-11.md
- handoff-2026-05-11-all-in-wave/BPLUS_SIGN_CLUSTER_PACKET_2026-05-11.md
- handoff-2026-05-11-all-in-wave/EC_KERNEL_NULL_SUITE_2026-05-11.py
- handoff-2026-05-11-all-in-wave/EC_KERNEL_NULL_SUMMARY_2026-05-11.md
- handoff-2026-05-11-all-in-wave/EC_STOCHASTIC_NULLS_2026-05-11.py
- handoff-2026-05-11-all-in-wave/EC_STOCHASTIC_NULL_REPORT_2026-05-11.md
- handoff-2026-05-11-all-in-wave/EC_G3_FAILURE_DIAGNOSTIC_2026-05-11.md
- handoff-2026-05-11-all-in-wave/EC_C2_PRIME_DIAGNOSTIC_PROTOCOL_2026-05-11.md

EC smoothing controls, exact current state:
- Deterministic C2 controls now pass.
- Primary anchor:
  - ratio = 1.3473754929960748
  - max CV = 0.063297427334436704
  - score = 0.3614560483477629
- Passed deterministic gates:
  - G0 reproducibility
  - G1 primary survival
  - G2 kernel robustness for none / continuous / discrete_both
  - G4 rank specificity: 0/5 nonidentity rank permutations pass
  - G4 curve-label specificity: 0/5 nonidentity curve permutations pass
  - G5 tail stability
- Full stochastic Sato-Tate G3:
  - st_iid: 512/512 seeds run; 0 old-gate passes; 0 primary-gate passes
  - st_shared: 128/128 seeds run; 0 old-gate passes; 0 primary-gate passes
  - st_iid p_ratio = 0.062378167641325533 > 0.01; p_score = 0.0019493177387914229
  - st_shared p_score = 0.046511627906976744 > 0.02; p_ratio = 0.16279069767441862
  - best iid score = 0.36358888733909978; real score = 0.3614560483477629
  - best shared score = 0.24592503586956727
- Interpretation:
  - random EC-sized local factors do not literally pass the old/primary two-component gates.
  - nevertheless G3_FAIL: empirical specificity is too weak under the predeclared p gates.
  - diagnostic split: no null beats real CV, but 31/512 iid and 20/128 shared nulls beat real ratio; 5/128 shared nulls beat real additive score.
  - additive score is not equivalent to the old conjunctive gate; low ratio can buy a CV miss.
  - still not theorem evidence.
- Before EC holdout/larger-K promotion attempts, predeclare a C2-prime diagnostic gate or pivot to theory-first work.
- C2-prime is future-only: fresh seeds 512..1023 iid and 128..255 shared, CV/Pareto empirical p-values, no retroactive G3 rescue.

EC scripts/verification commands:
- Compile:
  python3 -m py_compile handoff-2026-05-11-all-in-wave/EC_KERNEL_NULL_SUITE_2026-05-11.py handoff-2026-05-11-all-in-wave/EC_STOCHASTIC_NULLS_2026-05-11.py
- Deterministic rerun:
  python3 handoff-2026-05-11-all-in-wave/EC_KERNEL_NULL_SUITE_2026-05-11.py --force
- Stochastic pilot rerun:
  python3 handoff-2026-05-11-all-in-wave/EC_STOCHASTIC_NULLS_2026-05-11.py --iid-seeds 64 --shared-seeds 32 --force
- Full stochastic G3 rerun:
  python3 handoff-2026-05-11-all-in-wave/EC_STOCHASTIC_NULLS_2026-05-11.py --iid-seeds 512 --shared-seeds 128 --force
- Last full G3 runtime: 1723.058 seconds. The 64/32 pilot took about 260 seconds after the recurrence speedup.

EC theorem status:
- Simple universality D_K^E*zeta(2)->1 is falsified.
- Sharp-cutoff and finite bad-prime/per-curve constant fixes do not promote.
- Smoothed proxy is now a serious finite pattern, but not theorem evidence.
- Theory still needs:
  - H1 reciprocal derivative/Laurent control or profile/average mode;
  - exact S1 branch-contour theorem;
  - exact good-prime S_sym,W finite-part theorem;
  - joint H1/H2 profile tail extraction for product-average modes.
- Do not describe finite smoothing as BSD or L(E,2) evidence.

H1 status:
- Central algebra is fixed: normalized kernels give leading central term
  (log K)^r / L^(r)(E,1), not r! times that.
- Positive-rank H1 no longer only has the stronger shell-moment route.
- Weaker sufficient target:
  H1-weighted-l1(E,W,epsilon):
    sum_{T<|gamma|<=2T} |W_hat(i gamma)| |L'(E,1+i gamma)|^{-1}
    <= C_E,W T^{-epsilon}.
- For smoothstep-scale |W_hat(it)| << |t|^{-2}, it suffices to prove:
  R_E,1(T) = sum |L'(E,1+i gamma)|^{-1} <= C_E T^(2-epsilon).
- Further refinement:
  - exact positive-rank finite-box need is weighted partial growth M_W(u)=o(u^r)
    along the legal Perron height T_box(u);
  - absolute convergence for q=2 follows from R_E,1(T) <= C_E T^2(logT)^(-1-delta);
  - finite-box closure can allow R_E,1(T) <= C_E T^2(logT)^B when
    (log T_box(u))^(B+1)=o(u^r).
- Legal-height refinement after Relay[01]:
  - in the source-safe q=2 moving-box contour mode, sigma>1/2 forces exponential
    legal heights T_box(u)~exp(Cu), not polynomial heights;
  - the simple-zero positive-rank target sharpens to
    R_E,1(T)=o(T^2(logT)^(r-1));
  - rank one needs R_E,1(T)=o(T^2);
  - see H1_LEGAL_HEIGHT_L1_CLOSURE_2026-05-11.md.
- The old J_E,2(T) <= C_E T^(3-delta) target remains sufficient but stronger than needed for positive-rank absolute residue control.
- Fixed-weight PV remains a separate missing theorem. Spacing plus square moments cannot imply it; model sum cos(nu)/n shows resonance obstruction.
- Rank zero remains profile/product-average unless residues die, are killed/subtracted, or averaged.

H1 contour status:
- H-left closes if shifted line uses Re z = -eta with eta > 1/2.
- Horizontal H-height(A<2) is conditionally source-routed via Li-Zaharescu selected heights under normalized EC/newform RH/no-right-half-zero.
- This height route does not control residues, PV sums, shell moments, or Laurent coefficients.

H2/Sym2 status:
- Exact local H2 algebra for the Agent-3 factors is closed.
- Pointwise H2 remains conditional on:
  - S1 branch-contour continuation for the endpoint-smoothed W;
  - exact good-prime S_sym,W finite part and kappa_sym convention/value;
  - weighted good-prime Mertens for the same W;
  - zero/branch summability and contour tails.
- EC_POINTWISE_THEOREM_SPINE_2026-05-11.md packages the positive-rank conditional theorem spine:
  H1 legal-height reciprocal-pole control plus H2 finite-part closure gives
  c_E,W(e^u)P_E,W(e^u)->exp(B_H2)/L^(r)(E,1). No theorem promoted.
- Product-average can be stated only with joint H1/H2 profiles and tail extraction.
- Averaged log P alone does not imply arithmetic product-average stabilization.

GL(1)/Koyama status:
- Local target-zero residue is proved:
  Res_{w=0} K^w/(w L(rho+w,chi))
    = log K/L'(rho,chi) - L''(rho,chi)/(2L'(rho,chi)^2).
- Sharp cutoff remains blocked.
- Missing theorem is now named:
  GL1-Sharp-OffTarget-Control / GL1-Sharp-FixedWeightPV
  plus rectangle/trivial-residue control.
- Target-zero simplicity is insufficient:
  - off-target multiple zeros can create log K-scale or larger residues;
  - even all off-target simple zeros leave the fixed-weight PV aggregate.
- Smoothed/filtering mode is conditional and claim-safe:
  target-normalized smooth kernels and finite Mellin zeros can kill finite off-target sets,
  but this does not transfer to sharp cutoff without uniform off-target estimates.
- Do not state D_K -> e^{-gamma} as closed; it remains conditional on shifted Perron-leading.

B+ status:
- Conjecture B+ Mertens-restricted positivity is false.
- Lean-canonical counterexamples:
  - p = 237733, M(p) = -20, B(p) < 0
  - p = 243799, M(p) = -3, B(p) < 0
- Useful target is sign-cluster classification, not positivity.
- T(p-1) is not a sign proxy; p=243799 has T(p-1)<0 and B(p)<0.
- Recommended next compute:
  - tier 1B dense MR bridge, 237733 <= p <= 243799
  - 468 MR rows
  - about 9.94 core-hours at current verifier rate
- Do not run the full 1e6 atlas before tier 1B.

Best next tasks, in priority order:
1. H1 anti-small-derivative theorem:
   attack H1-legal-l1-rank-threshold; for rank one prove R_E,1(T)=o(T^2), and
   for general positive rank prove R_E,1(T)=o(T^2(logT)^(r-1)).
2. H2 endpoint theorem closure:
   close S1 branch-contour, exact good-prime S_sym,W finite part, and weighted
   good-prime Mertens for the same W.
3. EC numerical diagnostics:
   G3 is already failed by empirical p gates; only run C2-prime with fresh seeds
   and CV/Pareto p-values as future-only diagnostics, not promotion.
4. B+ tier 1B runner:
   build canonical dense MR bridge sweep using B_plus_direct_verify.c conventions.
5. Holdout EC curves / denser K:
   only after a new predeclared diagnostic gate exists; no rescue of failed G3.

Verification discipline:
- Use rg first.
- Use apply_patch for edits.
- Do not revert unrelated dirty files.
- Run py_compile for changed Python scripts.
- Run git diff --check over edited files before final.
- Update log.md for meaningful durable state changes.
- Keep claims conservative: no theorem promotion unless dependencies are actually closed.

Known dirty worktree caveat:
- The worktree already has many modified/untracked files from prior waves.
- Treat correspondence/KOYAMA.md and projects/farey-research/koyama-correspondence.md as preexisting dirty state unless explicitly asked to edit.
- Do not clean, reset, or revert unrelated files.
```
