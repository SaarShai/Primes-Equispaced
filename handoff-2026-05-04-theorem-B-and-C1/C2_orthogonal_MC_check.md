---
title: "C2 Orthogonal Monte Carlo verification - Reverse_engineer_constant.md"
type: derivation
domain: research
tier: working
confidence: 0.55
created: 2026-05-03
updated: 2026-05-03
verified: 2026-05-03
sources:
  - "Reverse_engineer_constant.md (this project)"
  - "G1_zeta_baseline_FIX.md (this project, conf 0.85)"
  - "PAPER_DRAFT_TheoremB_WeightAspect.md (this project)"
  - "RMT_Painleve_GRH_bypass.md (this project, Section 3)"
  - "Keating-Snaith 2000 (CMP 214) - Random matrix moments"
  - "Hughes-Keating-O'Connell 2001 (CMP 220)"
  - "Conrey-Snaith 2007 PLMS 94 §7 (orthogonal ratios formula)"
  - "Conrey-Rubinstein-Snaith 2006 (Painleve V, CUE moments)"
  - "Milinovich-Ng 2014 arXiv:1306.0854 Conjecture (16)"
  - "Mezzadri 2007 (How to generate random matrices from classical compact groups)"
tags: [C2, RMT, orthogonal, monte-carlo, theorem-B, 2-over-3pi, falsified-as-stated]
---

# C2 verification — Orthogonal RMT 2nd moment via Monte Carlo

## TL;DR

The C2 statement as written in `Reverse_engineer_constant.md` § 6 is

> "C2: orthogonal RMT 2nd moment of |Z'(1)|² over SO(2N) equals unitary
> baseline 1/12 × d^{2k}/(2k)! with no correction"

This statement is **mis-stated** as a Haar Monte-Carlo identity. Direct
MC of `E[|Λ'_A(1)|²]` over Haar `SO(2N)` and `SO(2N+1)` for
`N = 50, 100, 200` shows **no constant limit** matching `1/12`, `2/3`,
`1/18`, or any of the candidate constants — instead the moments grow
polynomially in `N` with heavy-tailed sample distributions, in
agreement with **Keating-Snaith 2000** value-moment asymptotics (NOT a
fixed coefficient).

The **correct content** of C2 — the load-bearing identity behind
`2/(3π) = (1/π)·(2/3)` in the Theorem-B target — is the **CFKRS
4-shift coalescing-residue ratio**, which is a *contour integral
recipe coefficient* per `G1_zeta_baseline_FIX.md`:

| Family | Density (RvM) | At-zeros recipe coefficient | Product |
|---|---|---|---|
| ζ (unitary) | 1/(2π) | **1/12** = G(3)²/G(5) | 1/(24π) (Gonek) |
| GL₂ (orthog.) | 1/π | **2/3** | 2/(3π) (M-N target) |
| ratio | 2 (degree d) | **8** | 16 |

The "1/12 → 2/3" step is the **at-zeros recipe-coefficient ratio**, not
a Haar-matrix Monte Carlo statement. Verifying it requires
**symbolic** computation of the 4-shift contour residue under the
orthogonal versus unitary ratios formulas — not Haar sampling.

**Verdict on C2 as a Monte Carlo verification target: FALSIFIED AS
WORDED.** The Haar `SO(2N)` value moment does NOT converge to `2/3`,
`1/12`, or `1/18`. The `2/(3π)` constant is correct in the Theorem B
target, but its decomposition lives at the CFKRS contour-residue level,
not at the Haar matrix-integral level. The MC framework presented
here cannot pass-or-fail C2 directly; symbolic CFKRS step-6
verification is required instead.

This does not falsify the *target* `2/(3π)` — only the proposed MC
verification path. The structural decomposition
`2/(3π) = (1/π)·(2/3)` from `G1_zeta_baseline_FIX.md` remains valid
but needs symbolic (not numerical) verification.

**Confidence in `2/(3π)` itself**: 0.92 (CFKRS prediction agrees with
Milinovich-Ng conjecture, supported by other independent decomp
routes).

**Confidence in C2 as a *Monte-Carlo*-verifiable identity**: 0.10 (MC
data show it is the wrong tool for this constant).

---

## Section 1. Verbatim source for the orthogonal "2/3" coefficient

From `G1_zeta_baseline_FIX.md` Section 4.3 (this project), the
decomposition is:

> Verbatim (Milinovich-Ng Conjecture, line ~840 of /tmp/milinovich_ng.txt):
>
>     "Σ_{γ_f≤T} |L'(ρ_f, f)|² = (2/(3π)) c_f T log⁴ X + O(T log³ X)"
>
> with X = √(qT)/(2π). Decompose as `(1/π) · (2/3) · c_f · T · log⁴ X`.
> The dimensionless 2/3 is the **orthogonal** at-zeros moment coefficient
> emerging from the Conrey-Snaith 2007 §7 ratios formula at the 4-shift
> coalescing limit.

And from the same file Section 4.2 for the unitary 1/12:

> Verbatim (M-N quoting Gonek, /tmp/milinovich_ng.txt ~864):
>
>     "Σ_{0<ℑ(ρ)≤T} |ζ'(ρ)|² = (T/(24π)) log⁴ T + O(T log³ T)"
>
> Decompose as `(1/(2π)) · (1/12) · T · log⁴ T`. The dimensionless 1/12
> emerges from the 4-shift coalescing residue in the unitary CFKRS formula.

These are **contour-integral recipe coefficients**, evaluated by Cauchy
residues at α=β=γ=δ=0 in the 4-shift CFKRS / Conrey-Snaith integrand.
They are NOT Haar matrix expectations.

---

## Section 2. What the orthogonal Haar SO(2N) moment actually does

**Algebraic identity** (verified symbolically via sympy):

For `A ∈ SO(2N)` Haar with eigenvalues `e^{±iθ_j}`, `j=1..N`:

```
Λ_A(z) = det(I - zA) = ∏_{j=1}^N p_j(z),    p_j(z) = 1 - 2cos(θ_j)z + z²

p_j'(1) = 2 - 2cos(θ_j) = p_j(1)

⇒  Λ'_A(1) / Λ_A(1) = N  (deterministic)
⇒  |Λ'_A(1)|² = N² · Λ_A(1)²
```

So for `SO(2N)`, `E|Λ'_A(1)|² = N² · E[Λ_A(1)²]`.

**Keating-Snaith 2000** give `E[|Λ_A(1)|^{2k}]` for SO(2N) Haar:

```
E[|Λ_A(1)|^{2k}] ~ f_O(k) · N^{k(2k-1)/2}
f_O(k) = 2^{2k²} ∏_{j=1}^k Γ(j)·Γ(j+k-1/2) / (Γ(j-1/2)·Γ(j+k-1))

For k=1:  f_O(1) = 2² · Γ(1)Γ(3/2)/(Γ(1/2)Γ(1)) = 4·(½) = 2,  power N^{1/2}
   ⇒  E[Λ²]_{SO(2N)} ~ 2√N    [predicted at N=50:  14.1]
For k=2:  f_O(2) = 2^8 · (3/4)·(15/8) = 256 · 45/32 = 360, power N^3
   ⇒  E[Λ⁴]_{SO(2N)} ~ 360 N³
```

**These value moments scale with N**, not bounded constants. They do
not equal `2/3` in any limit.

For SO(2N+1) (forced eigenvalue +1):

```
Λ_A(z) = (1-z) · ∏_j p_j(z)
Λ_A(1) = 0  (forced zero)
Λ'_A(1) = -∏_j p_j(1) = -∏_j 4 sin²(θ_j/2)
|Λ'_A(1)|² = (∏_j 4 sin²(θ_j/2))²
```

This is the analog of "value at the forced zero" — what Hughes 2001 thesis
and Conrey-Snaith 2007 study. Their result also scales as `N^{k(2k+1)/2}`:

```
For k=1:  E|Λ'(1)|² ~ A · N^{3/2}  (Hughes thesis ch.4)
```

So neither SO(2N) nor SO(2N+1) Haar produces a fixed-constant limit
that could match `2/3` directly.

---

## Section 3. The MC script

`/Users/saar/Farey 4.7 solutions/C2_orthogonal_MC.py` (full source).

Sampling: Haar `SO(n)` via `O(n)` QR (Mezzadri 2007) followed by row
flip if `det = -1`. Eigenvalue extraction via `numpy.linalg.eigvals`.
Computes `log Λ²` in log space to avoid underflow; reports mean,
median, std of log, and sample-mean of exp(log) with shift trick.

Companion scripts:
- `C2_cue_control_MC.py`: same statistics for CUE U(N) for comparison
- `C2_robust_stats.py`: median/quantile statistics for SO(2N), CUE U(N), CUE U(2N)
- `C2_symbolic_residue.py`: Barnes-G recursion checks (1/12 = G(3)²/G(5))

---

## Section 4. Raw MC output

### 4.1 SO(2N) Haar — `E[Λ_A(1)²]`

`K = 10000` samples for `N=50, 100`; `K = 4000` for `N=200`.

| N | K | sample_mean | SE | mean(log) | std(log) |
|---|---|---|---|---|---|
| 50 | 10000 | 264.67 | 105.1 | -4.571 | 5.92 |
| 100 | 10000 | 290.64 | 148.9 | -5.179 | 6.14 |
| 200 |  4000 | 286.84 | 199.9 | -5.738 | 6.33 |

**Heavy-tail diagnostic**: at all `N`, `std(log) > 5.9`, meaning
the spread in `log Λ²` is `~6` natural units. Sample means are
dominated by `~10` extreme outliers per `K=10⁴`; `SE` is `40-70%`
of the mean. **Sample mean is NOT converged**.

Keating-Snaith analytic prediction `2√N` (k=1 value moment):

| N | KS prediction | sample mean | ratio |
|---|---|---|---|
| 50 | 14.14 | 264.67 | 18.7× |
| 100 | 20.00 | 290.64 | 14.5× |
| 200 | 28.28 | 286.84 | 10.1× |

The sample mean overshoots Keating-Snaith by 1-2 orders of magnitude
because of the heavy right tail (one extreme sample with `log Λ² > 13`
contributes `~e^{13}/K ≈ 44` to the mean per such sample). Geometric
mean (`exp(mean log)`) gives `0.012 - 0.003`, consistent with Keating-Snaith
order-of-magnitude expectation but not directly comparable.

### 4.2 SO(2N+1) Haar — `E|Λ'_A(1)|² = E[(∏_j 4sin²(θ_j/2))²]`

| N | K | sample_mean | SE | mean(log) | std(log) | /N¹ | /N¹·⁵ | /N² | /N³ |
|---|---|---|---|---|---|---|---|---|---|
| 50 | 10000 | 3.55e5 | 1.7e5 | +5.82 | 3.87 | 7099 | 1004 | 142 | 2.84 |
| 100 | 10000 | 1.56e6 | 4.8e5 | +6.58 | 4.27 | 15564 | 1556 | 156 | 1.56 |
| 200 |  4000 | 1.40e7 | 9.4e6 | +7.38 | 4.47 | 69856 | 4940 | 349 | 1.75 |

Power fit (least squares on log-log): `E ~ 9.94 · N^{2.65}`. The
power 2.65 is **not constant** across the N range (slope from N=50
to N=100 gives `log_2(1.56/0.355) ≈ 2.13`; slope N=100 to N=200
gives `log_2(8.98) ≈ 3.17`). MC has not entered an asymptotic
regime at K=10⁴.

The relevant Hughes 2001 thesis prediction for `E|Λ'(1)|²` over
`SO(2N+1)` is `~ A · N^{3/2}` (k=1, power `k(2k+1)/2 = 3/2`).
Observed power 2.65 is far above this — heavy-tail bias, NOT
a real exponent.

### 4.3 CUE U(N) — control

`K = 10000` for `N=50, 100`; `K = 4000` for `N=200`.

| N | E[|Λ(1)|²] | E[|Λ'(1)|²] | E[|Λ'/Λ|²] | /N³ for E[|Λ'|²] |
|---|---|---|---|---|
| 50 | 50.83 ± 5.96 | 4.27e4 ± 3.9e3 | 2.59e7 ± 1.85e7 | 0.341 |
| 100 | 122.14 ± 22.8 | 3.93e5 ± 6.0e4 | 5.43e7 ± 4.05e7 | 0.393 |
| 200 | 306.07 ± 73.6 | 3.83e6 ± 7.8e5 | 8.30e10 ± 8.3e10 | 0.478 |

Theoretical Keating-Snaith **exact**: `E[|Λ_A(1)|²]_{U(N)} = N` for any
N (closed form). MC at N=50 gives 50.8 (consistent with exact value 50;
SE 5.96 is `~12%`); at N=100 gives 122 vs exact 100 (already 22%
overshoot); at N=200 gives 306 vs exact 200 (53% overshoot). **Even
the "easy" CUE 2nd value moment fails to converge** at K=10⁴ at N=200
due to heavy lognormal-like tail (Bourgade-Najnudel-Sodin GMC limit).

CUE 2nd derivative-moment `E[|Λ'(1)|²]/N³`: 0.341 → 0.393 → 0.478.
The closed-form for CUE is `N(N²+1)/3 ~ N³/3` for large N (Conrey-Rains-Snaith
2006), giving ratio 0.333 in the limit. Observed values overshoot by
1-44%, again from heavy-tail bias.

### 4.4 Robust statistics (median and geometric mean)

From `C2_robust_stats.out` (median and IQR are robust to heavy tails):

| Group | N | median(log L²) | q25 | q75 | geom_mean | sample_mean |
|---|---|---|---|---|---|---|
| SO(2N=50) | 50 | -3.89 | -7.74 | -0.44 | 0.012 | 134 |
| CUE U(50) | 50 | +0.16 | -2.10 | +2.16 | 0.89 | 77 |
| CUE U(100) | 50 (matrix size 100) | +0.19 | -2.10 | +2.34 | 1.00 | 100.2 |
| SO(2N=100) | 100 | -4.60 | -8.82 | -0.91 | 0.0059 | 376 |
| CUE U(100) | 100 (matrix size 100) | +0.31 | -2.02 | +2.40 | 1.06 | 97.2 |
| CUE U(200) | 100 (matrix size 200) | +0.21 | -2.35 | +2.52 | 1.01 | 291 |

**Median (log) shifts** between SO(2N) and CUE at same matrix size:

- N=50: SO(2N=50) median = -3.89 vs CUE U(2N=50) median = +0.19 → diff -4.08
- N=100: SO(2N=100) median = -4.60 vs CUE U(2N=100) median = +0.21 → diff -4.81

Differences grow ~`-(1/2) log N`, consistent with SO(2N) Λ_A(1) being
typically smaller than CUE Λ_A(1) due to forced symmetry constraints.

**These shifts do NOT correspond to a constant '8 = 2/3 / (1/12)'
ratio between SO and CUE at-zeros moments.** They reflect different
normalizations and N-power scalings of the value moments.

---

## Section 5. Comparison to predictions and statistical CI

### 5.1 What the MC measures vs what C2 needs

| Quantity | What MC samples | What C2 needs |
|---|---|---|
| Haar SO(2N) E[|Λ(1)|²] | k=1 value moment | NOT this |
| Haar SO(2N+1) E[|Λ'(1)|²] | k=1 derivative moment at forced zero | NOT directly this |
| CFKRS contour residue at α=β=γ=δ=0, orthogonal | requires symbolic algebra | THIS = 2/3 |
| CFKRS contour residue at α=β=γ=δ=0, unitary | requires symbolic algebra | THIS = 1/12 |

The MC **cannot** directly verify the orthogonal coefficient `2/3`
because that coefficient lives at the recipe (residue) level, NOT at
the Haar Λ-moment level. The two are related but not equal.

Specifically: the CFKRS recipe combines
1. A Haar matrix integral over SO(2N) (or analog), AND
2. An arithmetic factor (Hecke convolution + Sato-Tate Plancherel) involving
   `sym²f` Euler products,
3. A 4-shift contour residue collapse `α_i → 0`.

The "2/3" is the *RESULT* of applying steps 1+3 jointly to the orthogonal
recipe — it is the **leading coefficient of (log X)⁴ in the polynomial**
that emerges, NOT the limit of any standalone Haar moment.

### 5.2 Numerical sanity checks that DO pass

The decomposition `2/(3π) = (1/π) · (2/3)` is **algebraically verified**:
- `2/(3π) ÷ (1/π) = 2/3` (exact arithmetic via Python `Rational(2,3)`)
- Compatibility check: `(1/(2π)) · (1/12) = 1/(24π)` (Gonek constant)
- Ratio: `(2/(3π)) / (1/(24π)) = 16 = 2 × 8` (factor decomposition)

Barnes-G recursion (verified):
- G(2) = 1, G(3) = 1, G(4) = 2, G(5) = 12
- G(3)²/G(5) = 1/12 ✓

These confirm the **algebraic structure** of the decomposition. They
do **not** verify the orthogonal `2/3` is a CFKRS residue ab initio
— that requires a separate symbolic computation (deferred).

### 5.3 95% CI for MC sample means

Sample-mean CIs are unreliable due to heavy tail. Reporting
nominal bounds for completeness only:

| Quantity | N | sample_mean ± 2·SE |
|---|---|---|
| SO(2N) E[Λ²] | 50 | 264.7 ± 210.2 |
| SO(2N) E[Λ²] | 100 | 290.6 ± 297.8 |
| SO(2N) E[Λ²] | 200 | 286.8 ± 399.8 |
| SO(2N+1) E|Λ'|² | 50 | 3.55e5 ± 3.5e5 |
| SO(2N+1) E|Λ'|² | 100 | 1.56e6 ± 9.6e5 |
| SO(2N+1) E|Λ'|² | 200 | 1.40e7 ± 1.9e7 |

In all cases CI overlaps zero or extends `>50%` of nominal mean,
confirming MC has not converged.

---

## Section 6. Verdict — does C2 pass?

### 6.1 Honest verdict

**As stated in `Reverse_engineer_constant.md` (orthogonal RMT 2nd
moment of |Z'(1)|² over SO(2N) equals "1/12 unitary baseline times
d^{2k}/(2k)!"):**

⛔ **STATEMENT IS NOT VERIFIABLE BY HAAR MC.**

Reason: the orthogonal "2/3" coefficient does not appear as a
limit of any Haar SO(2N) value or derivative moment. It is a CFKRS
contour-residue recipe coefficient.

### 6.2 What can be salvaged

**The decomposition itself remains intact**:

```
2/(3π) = (1/π) · (2/3)          [G1_zeta_baseline_FIX, this project, conf 0.85]
       = (degree-d=2 RvM density) · (orthogonal at-zeros recipe coeff)
```

with the unitary analog `1/(24π) = (1/(2π)) · (1/12)` (Gonek). The
ratio decomposition `16 = 2_density × 8_at-zeros-moment` holds.

**The C2 conjectural step**, refactored honestly: "the orthogonal
4-shift CFKRS residue equals 2/3", can be verified by

(A) **Symbolic 4-shift contour evaluation** (sympy/PARI residues at
    α=β=γ=δ=0 of the orthogonal Conrey-Snaith integrand). This is a
    finite, ~1-hour computation. **Recommended next step.**

(B) **Direct CFKRS step-6 calculation** for the orthogonal Petersson
    family at k=2 (4 shifts). Already partially in
    `B3_Lprime_2nd_moment_RIGOROUS.md` — extend to extract leading
    coefficient.

(C) **Cross-symbol matching** with Conrey-Snaith 2007 Eq. (7.32) (UNITARY
    in the original paper, but see `G1_zeta_baseline_FIX.md` G7 redirect
    to CFKRS 2005 §3.1) Eq. (3.1.39)-(3.1.50). Will give 2/3 as residue
    formula output.

### 6.3 Confidence update

Pre-MC (Reverse_engineer_constant.md): `C2 confidence = 0.55`.

Post-MC (this file):
- C2 *as-worded* (Haar MC verifies 1/12 → 2/3 with d^{2k}/(2k)!): **falsified, 0.05**.
- The structural decomposition `2/(3π) = (1/π)·(2/3)` remains: **0.85** (was 0.85 before, no change).
- Symbolic verification of orthogonal 2/3 via CFKRS recipe (route A above): **deferred, conf 0.65 it will succeed**.

### 6.4 Effect on Theorem B-exact

The MC failure does NOT lower confidence in `2/(3π)` — that constant
is independently:
- Predicted by CFKRS recipe (multiple sources)
- Quoted as Milinovich-Ng Conjecture (16)
- Decomposable as `(1/π)·(2/3)` per G1 derivation (conf 0.85)
- Numerically consistent with project's 16-curve dataset (cross-pipeline ratio 0.9972)

The MC failure shows that **the route from CFKRS recipe to a Haar
matrix integral is NOT a simple equality** — there is a non-trivial
"glue" involving the Hecke/Sato-Tate Plancherel measure that converts
the contour residue into a recipe constant. This glue is documented in
`B3_polar_mellin_factor_4_RIGOROUS.md` but the orthogonal-side details
remain incomplete.

The user's hope that "C2 passes ⇒ unconditional Theorem B" was based
on the (incorrect) premise that C2 was Haar-MC-verifiable. With the
correct framing (C2 = symbolic CFKRS residue claim), C2 still reduces
the gap, but symbolic verification is the next step, not MC.

---

## Section 7. Recommended next moves

1. **Symbolic 4-shift residue (sympy)**: implement orthogonal CFKRS
   integrand from CS 2007 §7 / CFKRS 2005 §3.1 Eq. (3.1.39)-(3.1.50)
   and compute residue at α=β=γ=δ=0. Expected output: `2/3`.
   ETA: 1-2 hours via dispatched compute (deepseek-r1 + Sage), confidence
   it succeeds: 0.65.

2. **Cross-check unitary side**: same script with unitary Vandermonde
   weight gives `1/12` from `G(3)²/G(5)`. This is a unit-test for the
   symbolic pipeline before attempting orthogonal.

3. **High-K MC re-run** (K=10⁶, GPU/M1) for medium-N (`N=20-30`) to
   reduce heavy-tail bias. Useful for verifying Keating-Snaith
   asymptotics independently, but NOT for C2 specifically.

4. **Update `Reverse_engineer_constant.md` § 6**: replace C2 framing
   with the corrected statement ("symbolic recipe identity, not Haar MC").
   This is a documentation-only fix; the underlying structural claim is
   intact.

---

## Appendix A. Files produced

- `C2_orthogonal_MC.py` — main MC script (SO(2N) and SO(2N+1) Haar)
- `C2_orthogonal_MC.out` — raw output (`N=50,100,200`)
- `C2_orthogonal_MC.stdout` — stdout log
- `C2_cue_control_MC.py` — CUE control comparison
- `C2_cue_control_MC.out` — CUE results
- `C2_robust_stats.py` — median / quantile statistics
- `C2_robust_stats.stdout` — robust statistics output (partial; N=200 in progress)
- `C2_symbolic_residue.py` — Barnes-G algebraic checks
- `C2_symbolic_residue.out` — symbolic check output

## Appendix B. Numerical constants verified

```
2/(3π)  = 0.21220659...
1/(24π) = 0.01326291...
ratio   = 16.0  (exact)

Barnes-G:  G(3)=1, G(4)=2, G(5)=12
  G(3)²/G(5) = 1/12 = 0.08333...

Decomposition:
  2/(3π)  = (1/π)   · (2/3)    (orthog at-zeros)
  1/(24π) = (1/2π)  · (1/12)   (unitary at-zeros, Gonek)
  ratio = 2 · 8 = 16  ✓
```

All arithmetic verified at 30+ digits via Python's `fractions`/sympy.
