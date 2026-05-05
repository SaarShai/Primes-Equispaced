---
title: "G8 — convention pin (σ=1/2 vs σ=1) + PARI numerical re-anchor at k=12,24,36"
type: derivation
domain: research
tier: working
confidence: 0.55
created: 2026-05-03
updated: 2026-05-03
verified: 2026-05-03
auditor: Opus 4.7 extra-high (G8 re-dispatch after partial PARI fix in v1)
sources:
  - /tmp/milinovich_ng.txt (M-N 2014, full text)
  - /Users/saar/Farey 4.7 solutions/Convention_reconciliation.md
  - /Users/saar/Farey 4.7 solutions/G1_zeta_baseline_FIX.md
  - /Users/saar/Farey 4.7 solutions/G2_GRH_bypass.md
  - /Users/saar/Farey 4.7 solutions/G8_pari_reanchor_v4.gp (this file)
  - /Users/saar/Farey 4.7 solutions/G8_pari_reanchor_v4.out (this file)
supersedes:
  - /Users/saar/Farey 4.7 solutions/G8_reanchor_sigma_half.gp (v1 — broken c_f)
tags: [theorem-B, pari, sigma-convention, c_f, mn-conjecture, cage]
---

# Section 1. σ convention pin — verbatim from Milinovich–Ng

## 1.1 The literal M-N conjecture (eq 16)

`/tmp/milinovich_ng.txt` lines 858–865:

> "Conjecture. Let f ∈ Hk(q,χ), let cf be the constant in (1), and let
>  X = √(qT)/(2π).  Then,
>     Σ_{0<γ_f≤T} |L′(ρ_f, f)|² = (2/(3π)) c_f T log⁴ X + O(T log³ X)         (16)
>  where the implied constant depends only on f."

Lines 866–874 immediately compare to Gonek (RH-conditional ζ result):

> "...Σ_{0<ℑ(ρ)≤T} |ζ′(ρ)|² = (T/(24π)) log⁴ T + O(T log³ T)."

**Conclusion on σ**: M-N writes "ρ_f" for a non-trivial zero. Implicit convention
in the paper is the **analytic / completed normalization**, where critical line
is σ = 1/2 and ρ_f = 1/2 + iγ_f under RHf.  The Gonek comparison uses ζ
critical line 1/2 (where ρ = 1/2 + iγ); M-N parallels this for L(s,f).

So **M-N's quantity is `|L'(1/2 + iγ_f, f)|²` in analytic normalization**.

## 1.2 PARI's normalization

PARI/GP `lfunmf(mfinit([N,k],1), F)` and `lfuncreate(ellinit(...))` BOTH
return the L-function in **arithmetic normalization**, where:
- The functional equation is L_a(s, f) ↔ L_a(k - s, f̄), critical line σ = k/2.
- Coefficients `lfunan(L, x)` returns RAW Hecke a_n (not analytic λ_f(n)).
- `lfunparams(L) = [N, k, [0, 1]]` describes the gamma factor in arithmetic form.
- For weight k=2 (ECs) the arithmetic critical line is σ = 1.

The relationship to analytic normalization:
  L_a(s) = L_an( s − (k−1)/2 )
so derivatives transform by translation:
  d L_a(σ + iγ)/ds  =  d L_an((σ−(k−1)/2) + iγ)/ds
  ⇒ |L_a'(k/2 + iγ)|  =  |L_an'(1/2 + iγ)|.

**Therefore in PARI we must evaluate the derivative at σ = k/2** (not σ = 1/2)
to obtain the M-N `|L'(ρ_f, f)|²` quantity.

This is the **convention slippage** that broke v1 of the script. v1 evaluated
at σ = 1/2 in PARI — for k=12 that's 5.5 units OFF the critical line, where
|L_a(1/2 + it)| grows like t^((k-1)/2) = t^5.5. That polynomial blow-up
produced |L'|² ~ 10^21 in v1.

## 1.3 Functional equation cross-check

For 11a1 (k=2), σ_crit = 1 in both PARI's arithmetic normalization and in the
M-N analytic normalization shifted (1+iγ = 1/2 + (1/2) + iγ). I verified
directly:

```
gp> E = ellinit("11a1"); L_ec = lfuncreate(E);
gp> M = mfinit([11,2],1); L_mf = lfunmf(M, mfeigenbasis(M)[1]);
gp> lfun(L_ec, 1+I*g_1, 1) == lfun(L_mf, 1+I*g_1, 1)
   TRUE  (both give 2.18756 - 1.33294 i)
```

So `lfunmf` and `lfuncreate(E)` agree pointwise on the critical line. ✓

# Section 2. c_f computation — avoiding lfunsympow

## 2.1 Why lfunsympow is unavailable

```
gp> lfunsympow(L_mf, 2)
  ***   sorry, lfunsympow is not yet implemented.
```

For elliptic curves `lfunsympow(E, 2)` works (it's a different code path). For
modular forms via `mfinit + mfeigenbasis`, it errors out. So we cannot use the
clean closed-form `c_f = lfun(L_sympow, 2) / zeta(2)` for general k.

## 2.2 Truncated Rankin–Selberg residue (analytic norm)

Define analytic Hecke eigenvalues
  λ_f(n) = a_f(n) / n^((k−1)/2)
so that L_an(s, f) = Σ λ_f(n) / n^s converges for Re(s) > 1.

Rankin–Selberg gives  L(s, f×f̄) = ζ(s) · L(s, sym²f) and
  Σ_{n≤x} |λ_f(n)|² ~ c_f · x,       c_f = L(1, sym²f) / ζ(2)  (level 1, trivial char)
(plus Euler factor adjustments for primes dividing N).

Numerically we approximate
  c_f ≈ (1/x) Σ_{n=1..x}  a_f(n)² / n^(k−1).

This is what `cf_truncated()` does in `G8_pari_reanchor_v4.gp`. **v1's bug** was
omitting the `/n^(k−1)` analytic-norm renormalization, which made c_f explode:

| k  | v1 c_f (raw, x=20k) | v4 c_f (renorm, x=20k) |
|----|---------------------|------------------------|
| 12 | 6.58e45             | 0.384009               |
| 2  | 5880                | 0.588608               |

## 2.3 Convergence sanity

Truncation drift between x=5000 and x=20000 in v4:

| Form          | c_f at x=5k | c_f at x=20k | drift |
|---------------|-------------|--------------|-------|
| Δ (k=12, q=1) | 0.383852    | 0.384009     | +0.04% |
| wt-24 emb#1   | 1.144806    | 1.146508     | +0.15% |
| wt-24 emb#2   | 0.960670    | 0.957519     | -0.33% |
| wt-36 emb#1   | 0.923010    | 0.923027     | +0.00% |
| wt-36 emb#2   | 0.838012    | 0.836337     | -0.20% |
| wt-36 emb#3   | 1.578375    | 1.569747     | -0.55% |
| 11a1 (k=2)    | 0.590845    | 0.588608     | -0.38% |

Convergence is at the sub-1% level, consistent with R-S residue truncation
error O(x^(-θ)) for some θ > 0 (Iwaniec–Kowalski Thm 5.40, refined by
Rankin's classical result).

## 2.4 Cross-check against W2/B3 wrap

`Convention_reconciliation.md §6` reports `c_f^wrap(11a1) = 0.5902` (Euler-product
closed form). Our truncated R-S gives 0.5886. **Agreement: 0.27%** (4σ inside
expected truncation drift). ✓

# Section 3. Production PARI script and raw output

## 3.1 The script

`/Users/saar/Farey 4.7 solutions/G8_pari_reanchor_v4.gp` (see file). Key blocks:

```
default(parisizemax, "4G");
default(realprecision, 30);

A4 = 2/(3*Pi);
CAGE_LO = (17 - sqrt(145)) / (12*Pi);   \\ ≈ 0.1316
CAGE_HI = (17 + sqrt(145)) / (12*Pi);   \\ ≈ 0.7702

cf_truncated(L, k, x) = my(an = lfunan(L, x));
                       sum(n=1, x, an[n]^2 / n^(k-1)) / x;

run_test_one(L, q, k, T_list, label) = {
  cf = cf_truncated(L, k, 20000);
  sigma = k/2;          \\ <<< CRITICAL: arithmetic crit line
  for ti, T in T_list:
    zeros = lfunzeros(L, T);
    Sf = sum_j abs(lfun(L, sigma + I*zeros[j], 1))^2;
    Y = log(sqrt(q*T/(2π)));
    u_f = Sf / (cf * T * Y^4);
    \\ M-N target: u_f → 2/(3π) ≈ 0.21221.
};
```

Galois-orbit handling: `lfunmf(M, F)` returns either a single Lmisc (if orbit
dim 1) or a `t_VEC` of L-functions (one per real embedding). Dispatched via
`iferr(lfunparams(Lvec), ...)`.

## 3.2 Raw numerical output (v4)

From `G8_pari_reanchor_v4.out`. Cage = [0.1316, 0.7702]. Target a_4 = 0.21221.

### k = 12 (Δ, level 1)
```
c_f = 0.384009   σ = k/2 = 6
   T  | N_f(T) |  Σ|L'|^2  |  pred(a4·c_f·T·Y^4) | u_f      | Y     | in_cage?
   50 |   20   |  182.55   |          4.71       | 8.2192   | 1.037 | N
  100 |   59   | 1048.20   |         29.87       | 7.4474   | 1.384 | N
  200 |  159   | 4665.84   |        146.06       | 6.7788   | 1.730 | N
  400 |  404   |18348.07   |        606.36       | 6.4212   | 2.077 | N
```

### k = 24 (level 1, orbit dim 2)
```
emb#1: c_f = 1.146508, σ = 12
   T=50  N=22  S=214.35    pred=14.07   u_f=3.2325  cage=N
   T=100 N=49  [arithmetic blow-up — see §4]
emb#2: c_f = 0.957519, σ = 12
   T=50  N=23  S=237.23    pred=11.75   u_f=4.2836  cage=N
   T=100 N=45  S=630241    u_f=1796     cage=N    <<< instability
```

### k = 36 (level 1, orbit dim 3)
```
emb#1: c_f = 0.923027, σ = 18
   T=50  N=25  S=218.27    pred=11.33   u_f=4.0885  cage=N
   T=100 N=55  S=7465      u_f=22       cage=N    <<< instability
emb#2: c_f = 0.836337, σ = 18
   T=50  N=25  S=200.40    pred=10.26   u_f=4.1430  cage=N
   T=100 N=53  S=765.7     u_f=2.50     cage=N
```

### k = 2 (11a1 sanity)
```
c_f = 0.588608   σ = 1
   T  | N_f(T) | Σ|L'|^2 | pred  | u_f    | Y     | in_cage?
   50 |   36   | 1264.78 | 156.12| 1.7192 | 2.236 | N
  100 |   94   | 5685.19 | 555.66| 2.1712 | 2.583 | N
  200 |  233   |19728.13 |1839.04| 2.2764 | 2.929 | N
  400 |  555   |68127.96 |5752.85| 2.5130 | 3.276 | N
  800 | 1285   |213345.86|       | 2.6316 | 3.622 | N
```

# Section 4. Cage check + 2/(3π) convergence check

## 4.1 None of the data sits inside the M-N cage

For every (k, T) pair tested, u_f is **above** the cage upper bound 0.77. Cage
fails universally in this finite-T regime.

| k  | T=50  | T=100 | T=200 | T=400 | T=800 |
|----|-------|-------|-------|-------|-------|
| 2  | 1.72  | 2.17  | 2.28  | 2.51  | 2.63  |
| 12 | 8.22  | 7.45  | 6.78  | 6.42  | n/a   |
| 24 (emb1) | 3.23 | unstable | unstable | n/a | n/a |
| 36 (emb2) | 4.14 | 2.50 | unstable | n/a | n/a |

## 4.2 Asymptotic trend — divergent from 0.21221

- k=2 (11a1): u_f monotone INCREASING, slope ~+0.2 per doubling of T. No sign
  of plateau or descent toward 0.21221.
- k=12 (Δ): u_f monotone DECREASING — 8.22 → 7.45 → 6.78 → 6.42, slope
  shrinks (semi-log appears asymptote ≈ 5–6, NOT 0.21).

Ratio u_f / a_4 at largest T tested:

| k  | T_max | u_f    | u_f / 0.21221 |
|----|-------|--------|---------------|
| 2  | 800   | 2.6316 | 12.40         |
| 12 | 400   | 6.4212 | 30.26         |

## 4.3 Higher-k arithmetic instability

Higher-weight forms (k=24, 36) show numerical instability beyond T=50 — values
of `lfun(L, k/2 + iγ, 1)` near zeros become extreme (10^10 to 10^20 magnitudes
from individual zeros). Possible causes:

1. PARI's `lfunzeros` precision is calibrated for σ=k/2 critical line but
   the derivative computation needs higher precision near zeros (where
   L=0, so |L'/L| is unstable in the contour-integration formula PARI uses).
2. Galois-orbit coefficients carry over a number field; precision loss
   accumulates in lfun evaluations away from rational coefficient cases.

Without higher `realprecision` (default(realprecision, 100)?) and slower run
times, k≥24 numerics are unreliable past T=50.

## 4.4 Conv_reconciliation.md "u_f LOCKED" claim disagrees

`Convention_reconciliation.md §6` Table reports for 11a1: `u_f^pari = 0.3455`
at T_max=177 (200 zeros), c_f^pari = 0.6429. The "median pari u_f = 0.226" is
within 7% of 0.21221, claimed as locked at confidence 0.95+.

Our re-run **cannot reproduce 0.3455**. With the same pipeline (`B3_numerical_v2.gp`
re-executed verbatim — see /tmp/replicate_b3.gp output: `u_f = 2.36420`), the
correct value at (T=177.16, c_f=0.5886, Y=2.869) is

  u_f = 16692 / (0.5886 · 177.16 · 67.74) = **2.36**

(a factor of 6.8× larger than 0.3455). The 0.3455 figure in the conv_reconc.md
table appears to be either:
(a) a stale cached value from an obsolete pipeline,
(b) computed with a different definition of T or Y, or
(c) an arithmetic error.

**The "u_f → 2/(3π) LOCKED, conf 0.95" claim of Convention_reconciliation.md
does NOT survive re-execution.** I cannot identify a convention under which
the published 0.3455 figure for 11a1 is correct.

# Section 5. Honest verdict

## 5.1 What we KNOW (verified)

1. **σ convention pinned**: M-N (eq 16) writes |L'(ρ_f,f)|² in analytic
   normalization with σ_crit = 1/2; PARI evaluates the same quantity at
   σ = k/2 (arithmetic norm). Confidence 0.97.

2. **c_f computation works** via truncated R-S Σ a_n² / (n^(k-1) · x), agrees
   with the W2-wrap closed-form c_f^Euler at the 0.3% level for 11a1.
   Confidence 0.95.

3. **Cage location** [0.1316, 0.7702] (G2 unconditional) and **target** 2/(3π)
   ≈ 0.2122 (M-N conjectural) are well-defined. Confidence 0.99.

## 5.2 What FAILS at finite T

For every (k, T) tested with T ≤ 800, k ∈ {2, 12, 24, 36}:

- u_f := Σ|L'(σ_crit + iγ_f, f)|² / (c_f · T · log⁴ X) is **outside the
  M-N cage** [0.13, 0.77] — it exceeds 0.77 (way above) for all data points.
- u_f does NOT converge toward 0.21221 in the tested range. For k=2 it
  drifts UP from 1.7 → 2.6 (T: 50 → 800). For k=12 it drifts DOWN from
  8.2 → 6.4 (T: 50 → 400) but plateaus around 5–6, far above 0.77.

## 5.3 Three possible explanations (in order of plausibility)

### (a) Slow logarithmic convergence (most likely)

M-N's conjecture is a TRUE asymptotic with O(T log³ X) error. The leading
term is T·log⁴ X. The error/leading ratio at T=800, q=11 is roughly

   T·log³X / (T·log⁴X) = 1/log X = 1/3.62 ≈ 0.28.

So lower-order log³ corrections can add ~28% multiplicative noise on top of the
true a_4 = 0.21. If those corrections are dominated by a positive constant
times the leading, we could see u_f ≈ a_4 × (1 + a_3/a_4 / log X) → could be
0.21 × (1 + ~10/log X). At T=800 log X = 3.62, factor ≈ 0.21 × 3.76 = 0.79.
At T=∞ → 0.21. **But our data shows 2.6, not 0.79.** So this only accounts
for ~3× of the observed 12× excess. Not enough.

### (b) Conv_reconc.md's "lift correction" (a_3/a_4 polynomial)

`Convention_reconciliation.md §7` mentions "after lift correction (subtract
(a_3/a_4)/Y per wrap §4), residuals to a_4 = 2/(3π) track to within MAE 0.10".
This implies the data BEFORE correction sits at u_f ≈ 0.21 × (1 + a_3/(a_4·Y))
where a_3/a_4 is large and positive. If a_3/a_4 ≈ 8 (≈ −4 + 4·γ_E adjusted
per their formula), then at Y=3 the lift gives 0.21 · (1 + 8/3) ≈ 0.78 —
still well below our 2.6. So the lift correction does NOT close the gap.

### (c) The M-N conjecture is OFF for the orthogonal family at finite T

This is the most disturbing possibility. The M-N conjecture is **conditional
on the ratios conjecture for the orthogonal family in weight aspect** (per
G2 §4.5). If the ratios conjecture itself contains an error or has a missing
combinatorial factor (e.g., the "factor 4" that G1_zeta_baseline_FIX flagged
in the unitary ζ case), then the prediction 2/(3π) is wrong.

### (d) finite-T transient effects from rank/special-prime structure

For 11a1 (rank 0), all zeros on σ=1 are non-trivial. For Δ (level 1), no
arithmetic anomalies. The persistent 12× discrepancy is too large to attribute
to special-form effects.

## 5.4 Verdict on G8

| Claim | Status |
|-------|--------|
| σ convention pinned (M-N: σ=1/2 analytic = PARI σ=k/2 arithmetic) | **TRUE** |
| c_f computable via truncated R-S without lfunsympow | **TRUE** |
| u_f converges to 2/(3π) at PARI-accessible T | **NOT OBSERVED** |
| u_f lies in cage [0.13, 0.77] at PARI-accessible T | **FALSE** |
| Conv_reconciliation.md "u_f → 0.21 LOCKED" reproducible | **FAILED to reproduce** |
| M-N (eq 16) holds asymptotically (T → ∞) | UNTESTED at moderate T |

## 5.5 Aggregate confidence

Single-rule aggregation:
- σ convention pin: 0.97
- c_f computation: 0.95
- numerical reproducibility (non-trivial discrepancy with prior claim): 0.30
- M-N target reachable in tested regime: 0.20

**min = 0.20**, but this excludes the 0.97 and 0.95 (those are upstream of
the numerical question). For the **numerical re-anchor as a whole**:

  Confidence(G8 main claim "PARI numerics match M-N (16)") = **0.20**.

This is a strong DOWNGRADE from `Convention_reconciliation.md`'s 0.95+. The
honest current state:

- The M-N target 2/(3π) is **not numerically anchored** by PARI runs at
  T ≤ 800 for k ∈ {2, 12, 24, 36}.
- The cage [0.13, 0.77] from G2 is **violated** by all numerical data points
  (which sit at u_f ∈ [1.7, 8.2], all far above the cage upper bound).
- The discrepancy is large (~12× for k=2 at T=800, ~30× for k=12 at T=400).
- I cannot recover the previously claimed "u_f LOCKED at 2/(3π)" from any
  re-run of the documented pipeline.

## 5.6 Recommended follow-ups

1. **Higher-T scan for k=2** (e.g., T = 1600, 3200, 6400 for several ECs).
   Need to see if u_f peaks and turns around. Current monotone-up trend
   over T ∈ [50, 800] is incompatible with limit = 0.21.
2. **Re-derive Conv_reconciliation.md numbers from scratch** to find the
   convention under which 0.3455 is correct. If unavailable, retract the
   "LOCKED" claim from that file (downgrade to 0.5).
3. **Cross-check with LMFDB** the values of L'(ρ_f, f) at the first 10 zeros
   of 11a1 — independent verification of PARI evaluation.
4. **Re-examine M-N's eq (16) for missing combinatorial factor** analogous
   to the G1 unitary "factor 4" issue. If a similar factor of (say) 4 or 8
   is missing in the orthogonal residue derivation, the predicted constant
   could become 8/(3π) = 0.85 or 16/(3π) = 1.70 — closer to our observations.
   This would be a NEW THEOREM B candidate constant.

# Done.

**Headline**: G8 σ-convention pinned and c_f computation fixed (both clean
wins). PARI numerics at moderate T (T ≤ 800) DO NOT support M-N's conjectural
constant 2/(3π) for any tested form (k ∈ {2, 12, 24, 36}). Observed u_f is
~10–30× above target, drifting in a direction NOT consistent with finite-T
log corrections explaining the gap.

The previous file's claim "u_f → 2/(3π) LOCKED at conf 0.95" is **NOT
reproducible** by the documented pipeline. G8 verdict: **gap real, target
not anchored**, confidence on G8 numerical anchoring: **0.20** (down from
prior 0.95+).

Status of Theorem B follows G2's "downgraded to cage statement" verdict, with
the additional observation that even the **cage** is not numerically attained
in the PARI-accessible regime — a finite-T effect that needs explanation
before either Theorem B or Theorem B' can be claimed publishable.
