---
schema_version: 1
title: "All-in wave synthesis"
date: 2026-05-11
type: synthesis
tier: working
status: MEANINGFUL_PROGRESS_NO_THEOREM_PROMOTED
confidence: 0.88
tags: [all-in-wave, gl1, ec-ndc, h1, h2, b-plus, null-controls]
---

# All-In Wave Synthesis

status: `MEANINGFUL_PROGRESS_NO_THEOREM_PROMOTED`

## Verdict

Meaningful progress, but no theorem promoted.

The wave improved three things that matter:

1. EC deterministic controls are no longer weak: the primary smoothstep anchor
   reproduces exactly and passes kernel, rank-permutation, curve-label
   permutation, leave-one-K, leave-one-curve, and tail-stability gates.
2. H1 positive-rank closure has a weaker sufficient target:
   `H1-weighted-l1(E,W,epsilon)`, or unweighted
   `R_E,1(T) <= C_E T^(2-epsilon)`, instead of only the stronger
   `J_E,2(T) <= C_E T^(3-delta)`.
3. The remaining hard gaps are now sharply named: GL1 sharp off-target
   control, EC H1 fixed-weight PV/weighted reciprocal tail, H2 S1/Sym2
   endpoint lemmas, and stochastic EC nulls.

## Packets

| packet | outcome |
|---|---|
| `GL1_SHIFTED_PERRON_PACKET_2026-05-11.md` | Sharp cutoff remains blocked. A named `GL1-Sharp-OffTarget-Control` or fixed-weight PV/off-target theorem closes it, but that is the missing theorem. Smoothed/filtering mode is conditional and claim-safe. |
| `H1_SHELL_ANTI_SMALL_DERIVATIVE_PACKET_2026-05-11.md` | No proof of `J_E,2(T)`. Standard inputs cannot imply anti-small-derivative tails. New reduced positive-rank target: weighted `l1` reciprocal tail. |
| `H1_FIXED_WEIGHT_PV_PACKET_2026-05-11.md` | Pointwise PV closure remains a missing theorem. Spacing plus `l2` moments cannot imply it; profile/Besicovitch/log-Cesaro/product-average modes remain honest substitutes. |
| `H1_WEIGHTED_L1_ATTACK_PACKET_2026-05-11.md` | Refines the reduced H1 target: positive rank only needs weighted finite-box growth `M_W(u)=o(u^r)`. Absolute convergence follows from a log-saving `R_E,1(T)<=T^2(logT)^(-1-delta)`, and finite-box closure can allow controlled polylog losses. |
| `H1_LEGAL_HEIGHT_L1_CLOSURE_2026-05-11.md` | Refines "controlled `T_box`" for the current contour mode. With source-safe `sigma>1/2` and smoothstep `q=2`, moving-box legal heights are exponential in `u`, not polynomial. Conditional on LZ-selected contour heights, the simple-zero target becomes `R_E,1(T)=o(T^2(logT)^(r-1))`; rank one needs `o(T^2)`. No theorem promoted. |
| `H2_SYM2_ENDPOINT_PACKET_2026-05-11.md` | Exact local H2 algebra is closed. Pointwise H2 remains conditional on S1 branch closure and exact Sym2 finite part. Product-average is conditional on joint H1/H2 profile tail extraction. |
| `EC_POINTWISE_THEOREM_SPINE_2026-05-11.md` | Packages the positive-rank conditional theorem spine after the H1 legal-height refinement: H1 legal-height reciprocal-pole control plus H2 S1/Sym2 finite-part closure implies `c_E,W(e^u)P_E,W(e^u)->exp(B_H2)/L^(r)(E,1)`. Rank zero remains profile/product-average. No theorem promoted. |
| `EC_KERNEL_NULL_SUMMARY_2026-05-11.md` | Deterministic C2 gates run here pass; larger/denser holdouts remain unrun. |
| `EC_STOCHASTIC_NULL_REPORT_2026-05-11.md` | Full Sato-Tate G3 run: `0/512` iid and `0/128` shared nulls pass the old or primary gate, but status is `G3_FAIL` because empirical p gates fail (`iid p_ratio=0.062378167641325533`, shared p_score `0.046511627906976744`). |
| `EC_G3_FAILURE_DIAGNOSTIC_2026-05-11.md` | Diagnoses the split: no null passes old/primary or beats real CV, but ratio-only and additive-score empirical tests are not specific enough. EC numerics need a new predeclared diagnostic gate, not promotion. |
| `EC_C2_PRIME_DIAGNOSTIC_PROTOCOL_2026-05-11.md` | Freezes a future-only diagnostic protocol: fresh seeds, CV/Pareto empirical p-values, no retroactive rescue of failed G3, and no theorem promotion without H1/H2. |
| `BPLUS_SIGN_CLUSTER_PACKET_2026-05-11.md` | B+ work should be bounded compute classification. Recommended next run is tier 1B, the dense MR bridge `237733 <= p <= 243799`, not the full 1e6 atlas. |

## EC Control Upgrade

The new deterministic EC control suite wrote:

```text
EC_KERNEL_NULL_SUITE_2026-05-11.py
EC_KERNEL_NULL_RAW_2026-05-11.csv
EC_KERNEL_NULL_METRICS_2026-05-11.csv
EC_KERNEL_NULL_CONTROL_SUMMARY_2026-05-11.csv
EC_KERNEL_NULL_SUMMARY_2026-05-11.md
```

Verified anchor:

```text
ratio = 1.3473754929960748
max CV = 0.063297427334436704
score = 0.3614560483477629
```

Passed deterministic gates:

```text
G0 reproducibility
G1 primary survival
G2 kernel robustness: none / continuous / discrete_both
G4 rank specificity: 0/5 nonidentity rank permutations pass
G4 curve-label specificity: 0/5 nonidentity curve permutations pass
G5 tail stability
```

Interpretation: this repairs the earlier "old gate is not load-bearing"
diagnosis in a limited way. The original ablation failure remains real, but
the broader deterministic controls now support the finite pattern as
rank/curve-aligned and kernel-robust. It still cannot be promoted: the full
stochastic G3 run failed the empirical p gates, and holdout curves plus
denser/larger `K` remain unrun.

## Full Stochastic Null Run

The stochastic null runner wrote:

```text
EC_STOCHASTIC_NULLS_2026-05-11.py
EC_STOCHASTIC_NULL_RAW_2026-05-11.csv
EC_STOCHASTIC_NULL_METRICS_2026-05-11.csv
EC_STOCHASTIC_NULL_SUMMARY_2026-05-11.csv
EC_STOCHASTIC_NULL_REPORT_2026-05-11.md
```

Full-G3 results for the predeclared primary group
`smoothstep, all, alpha=0.75, match=none`:

```text
st_iid:    512/512 seeds run; 0 old-gate passes; 0 primary-gate passes; p_ratio=0.062378167641325533; p_score=0.0019493177387914229; status=FAIL
st_shared: 128/128 seeds run; 0 old-gate passes; 0 primary-gate passes; p_ratio=0.16279069767441862; p_score=0.046511627906976744; status=FAIL
```

Best nulls:

```text
st_iid best ratio    = 1.0454966645724264, max CV 2.7868034997817701
st_iid best score    = 0.36358888733909978
st_shared best ratio = 1.0305984856846804, max CV 0.34043459577751245
st_shared best score = 0.24592503586956727
```

Interpretation: random EC-sized local factors do not literally pass the old
or primary two-component gate in this run, but the full predeclared G3 gate
does not pass because empirical specificity is too weak. In particular, iid
has too many null ratios at least as good as the real ratio, and the shared
family has too many null scores at least as good as the real score.

The follow-up diagnostic sharpens this:

```text
st_iid:    31/512 nulls beat the real ratio; 0/512 beat real CV; 0/512 pass old/primary.
st_shared: 20/128 nulls beat the real ratio; 5/128 beat the real score; 0/128 beat real CV; 0/128 pass old/primary.
```

So the old/primary two-component gate is not literally passed by Sato-Tate
nulls, but the empirical ratio/score gate is not separated enough for
promotion. Any C2-prime continuation must be predeclared and diagnostic,
using Pareto/CV empirical tests or a score where ratio cannot buy a CV miss.

The C2-prime protocol is future-only: use fresh seeds `512..1023` for iid and
`128..255` for shared, test CV/Pareto p-values, and do not reclassify the seen
G3 data as a pass.

## H1 Target Refinement

Old sufficient target:

```text
J_E,2(T) =
  sum_{T<|gamma|<=2T} |L'(E,1+i gamma)|^(-2)
  <= C_E T^(3-delta)
```

New weaker sufficient positive-rank target:

```text
H1-weighted-l1(E,W,epsilon):
  sum_{T<|gamma|<=2T}
    |W_hat(i gamma)| |L'(E,1+i gamma)|^(-1)
  <= C_E,W T^(-epsilon).
```

For smoothstep-scale `|W_hat(it)| << (1+|t|)^(-2)`, this follows from:

```text
R_E,1(T) =
  sum_{T<|gamma|<=2T} |L'(E,1+i gamma)|^(-1)
  <= C_E T^(2-epsilon).
```

This is still a genuine anti-small-derivative theorem. It is just weaker and
more directly aligned with what positive-rank H1 needs: absolute convergence
of the offcentral residue profile, hence `O(1)=o(u^r)` for `r>=1`.

Further refinement: absolute convergence for smoothstep-scale `q=2` already
follows from the log-saving target

```text
R_E,1(T) <= C_E T^2 (log T)^(-1-delta).
```

For positive rank only, the actual finite-box condition is weaker still. If

```text
M_W(u) =
  sum_{2^j <= T_box(u)}
    sum_{2^j<|gamma|<=2^(j+1)}
      |W_hat(i gamma)| |L'(E,1+i gamma)|^(-1)
  = o(u^r),
```

then simple offcentral residues are harmless at the central scale. Thus
`R_E,1(T)<=T^2(logT)^B` can be enough whenever
`(log T_box(u))^(B+1)=o(u^r)`. This does not close H1; it narrows the target
to reciprocal-derivative growth along the same legal Perron heights.

Legal-height refinement after this synthesis: in the current source-safe H1
moving-box contour mode, the start line is `sigma>1/2` and the kernel has
`q=2`, so original-line truncation forces exponential legal heights
`T_box(u)~exp(Cu)` with `C>sigma`. Under the conditional LZ-selected
horizontal-height input, this turns the finite-box target into the
rank-thresholded condition

```text
R_E,1(T)=o(T^2(logT)^(r-1)).
```

Equivalently, a bound `R_E,1(T)<=C T^2(logT)^B` suffices only for
`B<r-1` in this mode. The earlier polynomial-`T_box` observation is still a
valid algebraic implication, but it requires a different Perron theorem mode
not supplied by the checked packets.

## No-Promotion Line

Do not claim any of the following from this wave:

- sharp GL1 `c_K = log K/L'(rho)+o(log K)` unconditionally;
- EC pointwise fixed-curve smoothing theorem;
- rank-zero pointwise constant stabilization;
- BSD or `L(E,2)` evidence from the finite EC smoothing pattern;
- B+ positivity.

Claim-safe next moves:

- diagnose the full stochastic G3 empirical-p failure before any EC holdout
  promotion attempt;
- if EC numerics continue, predeclare a C2-prime diagnostic gate rather than
  retrofitting this G3 failure into a pass;
- attack the refined `H1-l1-growth` target along legal Perron heights;
- write the H2 S1/Sym2 endpoint lemmas as explicit conditional theorem
  statements;
- run B+ tier 1B only after a canonical sweep runner is ready.

## Verification

- `python3 -m py_compile handoff-2026-05-11-all-in-wave/EC_KERNEL_NULL_SUITE_2026-05-11.py`
- `python3 handoff-2026-05-11-all-in-wave/EC_KERNEL_NULL_SUITE_2026-05-11.py`
- `python3 -m py_compile handoff-2026-05-11-all-in-wave/EC_STOCHASTIC_NULLS_2026-05-11.py`
- `python3 handoff-2026-05-11-all-in-wave/EC_STOCHASTIC_NULLS_2026-05-11.py --iid-seeds 64 --shared-seeds 32 --force`
- `git diff --check` over all new all-in packet files
- read worker packets for GL1, H1 shell, H1 PV, H2/Sym2, and B+.

No Koyama email or correspondence draft was edited in this integration.
