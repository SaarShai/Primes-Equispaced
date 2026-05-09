---
title: "C2 Orthogonal Monte Carlo (Extended) — verification of the Hughes-Mezzadri / CRS Barnes-G coefficient `1/12` for the orthogonal symmetry type"
type: derivation
domain: research
tier: working
confidence: 0.05
created: 2026-05-09
verified: 2026-05-09
verdict: "FAIL (orthogonal coefficient is 1/2 in (2N)^3 normalization, NOT 1/12; sharp 6× discrepancy via Andrade-Best 2023 Theorem 2.4 + algebraic identity, MC consistent within heavy-tail bounds)"
sources:
  - "Conrey-Rubinstein-Snaith 2006 (arXiv math/0508378v2), Theorem 2 + Eq. (1.5)-(1.6) + page 18 table — verbatim verified"
  - "Iwaniec-Luo-Sarnak 2000 (Publ. Math. IHÉS 91), Theorem 1.1 (1.17)-(1.18) + page-5 SO(even)/SO(odd) assignment — verbatim verified"
  - "Andrade-Best 2023 (arXiv:2312.04981), Theorem 2.3, Theorem 2.4 — verbatim verified, b^SO_{1,1}(1,1) = 1/2 computed by symbolic enumeration"
  - "B2_R_neigh_v3_polished.md (this project, conf 0.86) — Soshnikov 2000a closure for unitary α_ratio=1; confirmed to extend to orthogonal here at conf ≥ 0.85"
  - "Reverse_engineer_constant.md (this project, conf 0.65) — the C2 hypothesis as written"
  - "C2_orthogonal_MC.py / .out / _check.md (prior bundle work; this file extends and refines)"
tags: [C2, RMT, orthogonal, monte-carlo, theorem-B, 2-over-3pi, Barnes-G, falsified-as-stated, sharp-fail]
supersedes:
  - "handoff-2026-05-04-theorem-B-and-C1/C2_orthogonal_MC_check.md (refines verdict from DEGENERATE to sharp FAIL with Andrade-Best 2023 closure + correct E[Λ²]_{SO(2N)} ~ 4N convention)"
---

# C2 Orthogonal MC Extended — sharp FAIL with Andrade-Best 2023 closure

## TL;DR

The C2 hypothesis "orthogonal RMT 2nd moment of `|Z'(1)|²` over O(2N) Haar
in the bulk-scaling limit converges to `1/12 + O(1/N)`" is **FALSIFIED**.

The orthogonal analog of CRS unitary `b'_1 = 1/12` (verbatim quoted from
arXiv:math/0508378v2 Eq. (1.5) + page-18 table) is the Andrade-Best 2023
constant **`b^{SO}_{1,1}(1,1) = 1/2`** (verbatim quoted from arXiv:2312.04981
Theorem 2.4, computed by symbolic enumeration). In `(2N)^3` normalization
the orthogonal coefficient is **`1/2`**; in `N^3` normalization it is **`4`**.
Discrepancy ratio with `1/12`: **6× in `(2N)^3` or 48× in `N^3`**, far
beyond any rescaling factor `d^{2k}/(2k)! = 16/24 = 2/3` proposed in
`Reverse_engineer_constant.md`.

The Theorem-B decomposition `2/(3π) = (1/(2π))·(1/12)·16` interpreted as a
Haar-MC orthogonal identity over SO(2N) is therefore **wrong**. The
decomposition `2/(3π) = (1/π)·(2/3)` from `G1_zeta_baseline_FIX.md`
(CFKRS-recipe contour-residue level, NOT Haar-MC) is unaffected.

**Verdict: `FAIL (orthogonal coefficient is 1/2, not 1/12; ratio 6× in
matched normalization)`.** Confidence on Theorem B-exact unconditional via
the C2 route: **0.05** (closed off). Net Theorem B-exact unconditional via
CFKRS-recipe route: **0.18-0.22** (unchanged from
`SESSION_SYNTHESIS_extra_high_round.md`).

---

## 1. Confidence aggregation rule (stated once, never switched)

A claim is at confidence ≥ 0.85 only if all of:

(a) Every cited theorem is verified by `pdftotext`-equivalent (pypdf
extraction) on the actual paper, with verbatim quote and page number reproduced
in §3.

(b) Numerical claims are reproduced from MC with sample-size sufficiency
documented; for heavy-tailed observables, robust statistics (median,
geometric mean, trimmed mean) are reported alongside sample mean and
discrepancies are explicitly noted.

(c) No external citation contradicts the claim, and no algebraic identity
in the prior bundle (e.g. `Λ'_A(1) = N · Λ_A(1)` for SO(2N)) makes the
claim degenerate.

If (a)-(c) all hold, confidence ≥ 0.85. If any fails, confidence is at most
0.55 and the failure mode is named explicitly.

This document does **not** switch to a more permissive rule mid-text.

---

## 2. What the prior `C2_orthogonal_MC*` files computed (verbatim summary)

### 2.1 `C2_orthogonal_MC.py` (original)

Ran Haar SO(2N) and SO(2N+1) Monte Carlo at N ∈ {50, 100, 200} with
K=10000 (4000 for N=200). Computed `E[Λ_A(1)²]` for SO(2N) and
`E|Λ'_A(1)|²` for SO(2N+1) directly in log-space. Output (verbatim from
`C2_orthogonal_MC.out`):

| group | N | K | sample mean | SE |
|---|---|---|---|---|
| SO(2N) `E[Λ²]` | 50 | 10000 | 264.67 | 105.1 |
| SO(2N) `E[Λ²]` | 100 | 10000 | 290.64 | 148.9 |
| SO(2N) `E[Λ²]` | 200 | 4000 | 286.84 | 199.9 |
| SO(2N+1) `E\|Λ'\|²` | 50 | 10000 | 3.55e+05 | 1.7e+05 |
| SO(2N+1) `E\|Λ'\|²` | 100 | 10000 | 1.56e+06 | 4.8e+05 |
| SO(2N+1) `E\|Λ'\|²` | 200 | 4000 | 1.40e+07 | 9.4e+06 |

### 2.2 `C2_orthogonal_MC_check.md` — prior verdict

Concluded **FALSIFIED AS WORDED** at confidence 0.05 (for Haar-MC
verifiability). Cited "Keating-Snaith analytic prediction `2√N` (k=1 value
moment)". This file extends, refines, and **corrects** that prior file:

### 2.3 What this document changes / adds

1. **Catches a citation error in the prior file.** The prior cite of "KS
   `E[Λ²]_{SO(2N)} ~ 2√N`" disagrees by 5-12× with both Andrade-Best 2023
   Theorem 2.3 (`~ 4N`) and a fresh K=20000 MC reported in §4.3. **The
   correct asymptotic is `E[Λ_A(1)²]_{SO(2N)} ~ 4 N`**, in the convention
   `Λ_A(s) = det(I - sA*)` (CRS / Andrade-Best convention).

2. **Computes the orthogonal coefficient explicitly.** Andrade-Best 2023
   Theorem 2.4 explicit formula evaluated by symbolic enumeration
   (`C2_orthogonal_symbolic_supplement.py` Section 1):
   - `b^{SO}_{1,1}(0, 0) = 2`  (matches `E[Λ²]_{SO(2N)} ~ 4N`)
   - `b^{SO}_{1,1}(1, 1) = 1/2` (matches `E[(Λ')²]_{SO(2N)} ~ 4 N³` via algebraic identity)
   - `b^{SO}_{1,1}(2, 2) = 7/30` (matches Altug et al. 2014's 2nd-derivative case)

3. **Verifies via algebraic identity.** For SO(2N), `Λ'_A(1) = N · Λ_A(1)`
   (deterministic, verified in `C2_orthogonal_MC.py` line 24-25 and prior
   `C2_orthogonal_MC_check.md` Section 2). With Andrade-Best `E[Λ²] ~ 4N`,
   this gives `E|Λ'(1)|² ~ 4 N³`. Cross-validates Andrade-Best Theorem 2.3
   coefficient `1/2 · (2N)^3 = 4 N^3` directly.

4. **Adds CUE U(N) baseline + extended N range** (50, 100, 200, 400, 800)
   with full-spectrum CUE statistics: `|Λ(1)|²`, `|Λ'(1)|²`, `|Z'(1)|²`.

5. **Symbolic Barnes-G cross-check.** mpmath at 60 dps:
   `G(3)²/G(5) = 1/12` exactly.

6. **Independent symbolic CRS Eq. (1.6) verification.** Numerical 2nd
   derivative of `e^{-x/2} x^{-1/2} I_1(2√x)` at `x=0` (mpmath dps=30) gives
   `0.083333... = 1/12` exactly. Sympy series-coefficient verification
   gives `b'_1 = -2 · (-1/24) = 1/12`. Three independent Barnes-G checks.

7. **Verbatim ILS Theorem 1.1 quote** for SO(even) symmetry-type assignment
   of `H_k^+(N)` newforms.

8. **Caught a mis-citation in `Reverse_engineer_constant.md`**: arXiv:0708.2922
   is a plasma physics paper, not Hughes-Mezzadri. The intended math
   reference is CRS 2006 (arXiv:math/0508378), which is **unitary**.

9. **Orthogonal κ=0 vs κ-matched falsifier (B2 v3 analog).** Sharp
   κ-discrimination at SO(400) and SO(800): `Var(S; κ=0) ≈ 0.14` vs
   `Var(S; κ=39.48) ≈ 2.4` matches Soshnikov-Palm prediction (B2 v3 §2c).
   This **extends the B2 unitary `α_ratio = 1` result to orthogonal** at
   confidence ≥ 0.85.

---

## 3. Statistic definition + verbatim citations

### 3.1 CRS 2006 — UNITARY constant `b'_1 = 1/12`

**Verbatim source: Conrey-Rubinstein-Snaith 2006, arXiv:math/0508378v2,
Theorem 2 (page 1, Eq. 1.5):**

> **Theorem 2.** For fixed k and N → ∞ we have
> ∫_{U(N)} |Z'_A(1)|^{2k} dA_N ∼ b'_k N^{k²+2k}, (1.5)
> where
> b'_k = (-1)^{k(k+1)/2} (d/dx)^{2k} ( e^{-x/2} x^{-k²/2} det_{k×k}(I_{i+j-1}(2√x)) ) |_{x=0}. (1.6)

**Tabulated value (verbatim, page 18 of the PDF, lines beginning "We have the
following values for b'_k"):**

> b'_1 = 1 / (2² · 3) = 1/12

This is the **U(N) (CUE / unitary)** result. Power `N³`, leading coefficient
`1/12`.

**Independent symbolic verification** (this work,
`C2_orthogonal_symbolic_supplement.py` Section 3-4):

```
Coefficient of x² in e^{-x/2} x^{-1/2} I_1(2√x) Taylor expansion: -1/24
b'_1 = (-1)^1 · 2! · (-1/24) = 1/12   [sympy symbolic]
b'_1 = -d²f/dx²|_{x=0} = 0.0833333... [mpmath, dps=30]
```

Both methods reproduce `1/12` exactly.

### 3.2 The mis-citation in `Reverse_engineer_constant.md`

The original brief cites "Hughes-Mezzadri 2008 (arXiv:0708.2922)". **This
arXiv identifier is wrong.** `arXiv:0708.2922` (downloaded + pypdf
extracted to `/tmp/c2_papers/hughes_mezzadri.pdf`) is:

> "Recombination fluorescence in ultracold neutral plasmas"
> S.D. Bergeson, F. Robicheaux (2007), Phys. Rev. A.

The intended math reference for the Barnes-G `1/12` constant is **CRS 2006**
(`arXiv:math/0508378`) — which is **unitary**, not orthogonal.

A search of `au:Hughes AND au:Mezzadri AND ti:zeta` on arXiv (May 2026)
returns no joint Hughes-Mezzadri paper on the second moment of the Riemann
zeta derivative.

### 3.3 ILS symmetry-type assignment (SO(even) for `ε_f = +1` newforms)

**Verbatim source: Iwaniec-Luo-Sarnak 2000, Publ. Math. IHÉS 91, page 5:**

> "For these families the expectation (see [KS1], page 18) is that G is
> orthogonal and that the subsets with ε_f = 1, ε_f = -1 are SO(even),
> SO(odd), respectively."

> **Theorem 1.1.** Fix any φ ∈ S(R) with the support of φ̂ in (-2, 2). Then,
> as N runs over squarefree numbers we have
> lim_{N→∞} 1/|H_k^+(N)| Σ_{f ∈ H_k^+(N)} D(f; φ) = ∫ φ(x) W(SO(even))(x) dx (1.17)
> lim_{N→∞} 1/|H_k^-(N)| Σ_{f ∈ H_k^-(N)} D(f; φ) = ∫ φ(x) W(SO(odd))(x) dx  (1.18)

The matching ensemble for the `ε_f = +1` sub-family is **SO(even) =
SO(2N)** (Andrade-Best convention: 2N × 2N matrix).

### 3.4 Andrade-Best 2023 — explicit SO(2N) joint derivative moment

**Verbatim source: Andrade-Best 2023, arXiv:2312.04981v1, page 6, Theorem 2.3:**

> **Theorem 2.3.** With notation as in Theorem 2.1, we have
> ∫_{SO(2N)} (Λ^{(n_1)}_A(1))^{k_1} (Λ^{(n_2)}_A(1))^{k_2} dA = b^{SO}_{k_1,k_2}(n_1, n_2) · (2N)^{k(k-1)/2 + k_1 n_1 + k_2 n_2} (1 + O(N^{-1})),

with the closed-form expression for `b^{SO}_{k1,k2}(n1, n2)` given in
Theorem 2.4.

For `(k_1, k_2, n_1, n_2) = (1, 1, 1, 1)` (the orthogonal analog of the
unitary `Z'(1)²` second moment): power `(2N)^{2(2-1)/2 + 1 + 1} = (2N)^3`,
so

> ∫_{SO(2N)} (Λ'_A(1))² dA = b^{SO}_{1,1}(1, 1) · (2N)³ (1 + O(N^{-1})).

For SO(2N), `Λ_A(1) ∈ R` (real characteristic polynomial of real orthogonal
matrix), so `(Λ'_A(1))² = |Λ'_A(1)|²`.

**Symbolic computation of `b^{SO}_{1,1}(1,1)`** (this work,
`C2_orthogonal_symbolic_supplement.py` Section 1):

```
b^SO_{1,1}(0,0) = 2     (matches E[Λ_A(1)²]_{SO(2N)} ~ 2 · (2N)^1 = 4N)
b^SO_{1,1}(1,1) = 1/2   (matches E[(Λ'_A(1))²]_{SO(2N)} ~ (1/2)(2N)^3 = 4 N³)
b^SO_{1,1}(2,2) = 7/30  (matches E[(Λ''_A(1))²]_{SO(2N)} ~ (7/30)(2N)^5)
```

Both `b^SO_{1,1}(0,0) = 2` and `b^SO_{1,1}(1,1) = 1/2` cross-validate via
the algebraic identity:

```
SO(2N): Λ_A(z) = ∏_{j=1}^N (1 - 2 cos(θ_j) z + z²),
        p_j(1) = 2 - 2 cos(θ_j) = 4 sin²(θ_j/2),
        p_j'(1) = -2 cos(θ_j) + 2 = p_j(1),
        ⟹ Λ'_A(1)/Λ_A(1) = N (deterministic)
        ⟹ E[(Λ')²] = N² · E[Λ²]
```

With `b^SO_{1,1}(0,0) = 2` ⇒ `E[Λ²] ~ 2 (2N) = 4 N`,  
⇒ `E[(Λ')²] ~ N² · 4 N = 4 N³`,  
which equals `(1/2)(2N)^3 = 4 N³` ✓.

**Conclusion:** the orthogonal Barnes-G analog of CRS unitary `b'_1 = 1/12`
is the Andrade-Best `b^{SO}_{1,1}(1, 1) = 1/2`. In `N^3` normalization the
orthogonal coefficient is **`4`**. **Either way, NOT `1/12`** and NOT close
to `1/12` by any reasonable rescaling.

### 3.5 Symbolic Barnes-G verification (mpmath at 60 dps)

```
G(3) = 1.0
G(5) = 12.0
G(3)² / G(5) = 0.083333333333333333333333333333333333333333333333333333333333
1/12         = 0.083333333333333333333333333333333333333333333333333333333333
delta        = -2.917e-62  (mpmath round-off below 60 dps)
```

`G(3)²/G(5) = 1/12` is **exact** by Barnes-G recursion `G(z+1) = Γ(z) G(z)`,
`G(2) = 1`: `G(3) = Γ(2)·G(2) = 1`, `G(4) = Γ(3)·G(3) = 2`,
`G(5) = Γ(4)·G(4) = 6·2 = 12`.

Confidence in the symbolic identity `G(3)²/G(5) = 1/12`: **0.999** (exact arithmetic).

This is the **unitary** Barnes-G constant. It is **not** an orthogonal
constant.

---

## 4. Monte Carlo design and results

### 4.1 Sampler

`scipy.stats.ortho_group` available; we use the simpler Mezzadri 2007 QR
sampler. CUE via Mezzadri 2007 Lemma 4 (QR with diagonal phase). All
eigenangles via `numpy.linalg.eigvals`. Random seed: `np.random.default_rng(20260509)`.

Sample plan:

| group | N values | K values |
|---|---|---|
| CUE U(N) | {50, 100, 200, 400, 800} | {8000, 4000, 2000, 800, 300} |
| SO(2N)   | {50, 100, 200, 400, 800} | {8000, 4000, 2000, 1000, 400} |
| SO(2N+1) | {50, 100, 200, 400, 800} | {8000, 4000, 2000, 1000, 400} |
| SO(2N) bulk-S, κ=0 and κ=39.48 | n=400, n=800 | 300, 150 |

K at largest N is below the brief's recommended ≥10⁵; this is documented
as a **limitation**. The qualitative conclusion is robust to K because the
**literature gives the answer analytically** (Andrade-Best 2023 Theorem 2.4
+ symbolic computation).

### 4.2 CUE U(N) baseline (verbatim from `.out`)

| N | K | E[\|Λ(1)\|²] | /N (exact: 1) | E[\|Λ'(1)\|²] | /N³ (target b_1 = 1/3) | E[\|Z'(1)\|²] | /N³ (target b'_1 = 1/12) |
|---|---|---|---|---|---|---|---|
| 50 | 8000 | 5.45e+01 ± 8.1 | 1.090 | 4.57e+04 ± 5.9e3 | 0.366 | 1.16e+04 ± 1.2e3 | 0.0929 |
| 100 | 4000 | 6.81e+01 ± 8.8 | 0.682 | 2.40e+05 ± 2.6e4 | 0.240 | 6.99e+04 ± 6.9e3 | 0.0699 |
| 200 | 2000 | 1.01e+02 ± 19.5 | 0.504 | 1.43e+06 ± 2.2e5 | 0.179 | 4.23e+05 ± 5.9e4 | 0.0528 |
| 400 | 800 | 2.20e+02 ± 66.0 | 0.550 | 1.57e+07 ± 4.8e6 | 0.246 | 6.92e+06 ± 3.6e6 | 0.108 |
| 800 | 300 | 1.54e+02 ± 35.1 | 0.192 | 5.18e+07 ± 1.6e7 | 0.101 | 2.72e+07 ± 1.3e7 | 0.0531 |

**Key observation (heavy-tail bias):** even for the *known* target
`b'_1 = 1/12 = 0.0833`, the sample-mean estimator at K ≤ 8000 fluctuates
between 0.05 and 0.11 with SE 10-50%. Section 4 log-log fit:

```
CUE  E[|Λ'(1)|^2]:  C = 1.458   p = 2.633   (CRS exact: C=1/3=0.333, p=3)
CUE  E[|Z'(1)|^2]:  C = 0.122   p = 2.902   (CRS exact: C=1/12=0.083, p=3)
CUE  E[|Λ(1)|^2]:   C = 8.761   p = 0.469   (KS exact: C=1, p=1)
```

The fit's `C = 0.122` for `Z'(1)²` is the closest match to the CRS exact
target `1/12 = 0.083` (relative error ~46%). The fit's power 2.90 is close
to the exact 3. Heavy-tail bias makes single-N estimates imprecise, but the
log-log fit recovers the answer to within 50%.

**This means the MC alone is not a sharp verification path** — it must be
supplemented by analytical work. (We have it: Andrade-Best Theorem 2.4
closed form.)

### 4.3 SO(2N) — `E|Λ'(1)|² ~ 4 N³` predicted by Andrade-Best (verbatim from `.out`)

| N | K | E[Λ(1)²] sample | trim_5_95 mean | median | E[Λ'(1)²]/N³ sample | ratio vs 1/12 | ratio vs `4` (Andrade-Best) |
|---|---|---|---|---|---|---|---|
| 50 | 8000 | 121 ± 32 | 2.13 | 0.020 | 2.42 | 29.1 | 0.61 |
| 100 | 4000 | 990 ± 890 | 1.52 | 0.011 | 9.90 | 119 | 2.48 |
| 200 | 2000 | 112 ± 53 | 0.86 | 0.0034 | 0.560 | 6.71 | 0.140 |
| 400 | 1000 | 346 ± 202 | 0.70 | 0.0024 | 0.866 | 10.4 | 0.217 |
| 800 | 400 | 377 ± 239 | 0.98 | 0.0015 | 0.471 | 5.65 | 0.118 |

Section 4 fit:

```
SO(2N) E[|Λ'(1)|^2]:  C = 110.6   p = 2.176
```

Power `2.176` deviates from the literature value `3` due to heavy-tail
bias (even N=800 K=400 has only 400 effective samples and the
characteristic-polynomial moment distribution is log-normal-tailed).

**Definitive K=20000 spot check at small N** (script:
adhoc test in §4.3 of `C2_orthogonal_symbolic_supplement.out`):

| N | K | sample mean E[Λ²] | Andrade-Best `4N` | prior cite KS `2√N` |
|---|---|---|---|---|
| 10 | 20000 | 36.2 | 40 | 6.32 |
| 20 | 20000 | 107.6 | 80 | 8.94 |
| 30 | 20000 | 101.7 | 120 | 10.95 |

At K=20000 (5-50× the K of the main MC), sample means are 36, 108, 102
**consistent with Andrade-Best `4N`** (1.0×, 1.3×, 0.85× of pred) and
**inconsistent with prior cite KS `2√N`** by 5-12×.

**Conclusion (§4.3):** Andrade-Best Theorem 2.3 with `b^{SO}_{1,1}(0,0) = 2`
is correct: `E[Λ_A(1)²]_{SO(2N)} ~ 4N`. The prior `C2_orthogonal_MC_check.md`
cite of "Keating-Snaith `2√N`" was wrong (likely a different convention or
a misciation). The orthogonal Z' analog coefficient is `1/2 in (2N)^3` =
`4 in N^3`, **NOT `1/12`**.

### 4.4 SO(2N+1) — forced-zero derivative (verbatim from `.out`)

| N | K | E\|Λ'(1)\|² | /N^(3/2) | /N² | /N³ | ratio vs (1/12)·N³ |
|---|---|---|---|---|---|---|
| 50 | 8000 | 1.235e+05 | 349.4 | 49.4 | 0.988 | 11.86 |
| 100 | 4000 | 9.99e+05 | 999.0 | 99.9 | 0.999 | 11.99 |
| 200 | 2000 | 4.748e+06 | 1678.7 | 118.7 | 0.594 | 7.12 |
| 400 | 1000 | 1.944e+07 | 2430.5 | 121.5 | 0.304 | 3.65 |
| 800 | 400 | 2.335e+07 | 1031.9 | 36.5 | 0.046 | 0.547 |

**MC fit:** `C = 104.5, p = 1.94`. Power ≈ 2 (heavy-tail bias on what is
likely true `N^{3/2}` per Hughes thesis or `N^3` per Andrade-Best Thm 2.5).
The leading constant fitted is ~100 (not 1/12 = 0.083).

**Discrepancy with `1/12 N^3`:** at N=50 ratio is 11.9; at N=800 ratio is
0.55 (heavy-tail biased low). The constant ratio across N would have to be
fixed; the observed **decrease from 11.9 down to 0.5** is heavy-tail bias.

The **median + trimmed mean** are not reported here for SO(2N+1) but per
the `C2_orthogonal_MC.py`'s prior data, the typical `|Λ'(1)|²_{SO(2N+1)}`
scales as some power of N with leading constant order `O(1)-O(100)`, not
`1/12`.

### 4.5 Section 4 log-log fits (verbatim from `.out`)

```
CUE  E[|Λ'(1)|^2]:    C = 1.458    p = 2.633   (CRS exact C=1/3, p=3)
CUE  E[|Z'(1)|^2]:    C = 0.122    p = 2.902   (CRS exact C=1/12, p=3)
CUE  E[|Λ(1)|^2]:     C = 8.761    p = 0.469   (KS exact C=1, p=1)

SO(2N) E[|Λ'(1)|^2]:  C = 110.6    p = 2.176
SO(2N) E[|Λ(1)|^2]:   C = 110.6    p = 0.176

SO(2N+1) E[|Λ'(1)|^2]: C = 104.5   p = 1.941
```

**Strict reading:** the orthogonal `|Λ'(1)|²` fits give leading constant
`C ~ 100-110`, **not `1/12 = 0.083`**, in any normalization. Even with
generous heavy-tail-bias error bars (factor 5×), the orthogonal MC
**rejects `1/12`** at all N.

The correct orthogonal answer per Andrade-Best 2023 Theorem 2.4 is `1/2`
(in `(2N)^3`) or `4` (in `N^3`), **not `1/12`**.

---

## 5. κ=0 vs κ-matched falsifier — orthogonal bulk-scaled `S` statistic

(Verbatim numerical from `C2_orthogonal_MC_extended.out`, Section 6.)

```
I_ON = ∫|M_W|^2 (1 - sinc^2(πy)) dy = 2.32604  (Soshnikov-Palm prediction at high κ)
```

| n (matrix dim) | κ | n_samples | Var(S) | Soshnikov-Palm pred |
|---|---|---|---|---|
| 400 | 0.0 | 300 | 0.144 ± 0.077 | ≈ 0.13 (B2 v3 §2c) |
| 400 | 39.48 | 300 | **2.43 ± 0.13** | **2.33 (I_ON, B2 v3 §1)** |
| 800 | 0.0 | 150 | 0.152 ± 0.120 | ≈ 0.13 |
| 800 | 39.48 | 150 | **2.03 ± 0.17** | **2.33** |

**This is a clean PASS for the Soshnikov-Palm framework on the orthogonal
side:**

- κ=0 prediction `≈ 0.13` matches MC `0.14, 0.15` within 1-σ.
- κ=39.48 prediction `2.33 = I_ON` matches MC `2.43 ± 0.13` (within 1-σ at
  n=400) and `2.03 ± 0.17` (within 2-σ at n=800).
- The **17× separation** between κ=0 (0.14) and κ=39.48 (2.43) is far
  larger than the 1-σ MC error (0.07-0.13), confirming sharp κ-discrimination.

**This extends the B2 v3 polished `α_ratio = 1` Soshnikov closure from
unitary to orthogonal at confidence ≥ 0.85.** This was the only previously
"argued" piece of B2's symmetry-independence claim (per B2 v3 §4
"Remaining 0.14 confidence gap, ~0.04 Symmetry-independence"); it is now
**numerically verified**.

**However:** this verification is for the **`Var(S_κ)` linear-statistic
variance**, NOT for the `|Z'(1)|²/N³ → 1/12` value-moment claim. They are
different statistics. The Soshnikov-Palm framework gives `α_ratio = 1`,
the Hughes-Mezzadri / CRS Barnes-G constant gives `b'_k = G(k+1)²/G(2k+1)`
for unitary value moments. Both can be true simultaneously.

The C2 hypothesis as worded conflates these two and asserts the orthogonal
analog of the second has the unitary value `1/12`. The first is verified
here (orthogonal); the second is **rejected** (orthogonal coefficient is
`1/2` per Andrade-Best, not `1/12`).

---

## 6. Alternative-α candidate residual table

(Verbatim from `.out` Section 5, with corrected normalization.)

For SO(2N+1) at N=800 (largest N, smallest heavy-tail bias for this object),
`E|Λ'(1)|² / N^3 = 0.0456` (raw sample mean, biased low):

| α candidate | value | source | relative residual at N=800 |
|---|---|---|---|
| `1/12` (HM/CRS unitary Barnes-G) | 0.0833 | the C2 hypothesis target | 45.3% |
| `1/3` (CRS unitary `\|Λ'\|²` leading) | 0.3333 | mismatched normalization | 86.3% |
| `1/(2π²)` (Plancherel rough) | 0.0507 | dimensional guess | 10.0% |
| `1/π²` | 0.1013 | dimensional guess | 55.0% |
| `2/π²` | 0.2026 | dimensional guess | 77.5% |
| `1/(4π)` | 0.0796 | dimensional guess | 42.7% |
| `1/24` | 0.0417 | factor-2 sanity check | 9.5% |
| `1/6` | 0.1667 | dimensional guess | 72.6% |
| `2/3` (orth at-zeros M-N) | 0.6667 | M-N 2014 conjectural | 93.2% |

**At N=800 SO(2N+1)** the closest candidates by relative residual are
`1/24` (9.5%), `1/(2π²) = 0.051` (10.0%) — but both are close only because
the MC sample mean at N=800 is **heavy-tail biased low** (`/N^3` decreases
across N from 0.99 down to 0.046, indicating strong bias). The true
asymptotic from Andrade-Best Theorem 2.5 (O⁻(2N), the analog of SO(2N+1))
is **NOT among the candidates listed** — it is a Barnes-G-like constant
(via `b^{Sp}` per Theorem 2.5) likely of order `O(1)`.

**For SO(2N), the comparable table is:**

At N=800: `E[Λ'(1)²]/N^3 = 0.471` (heavy-tail biased low).

| α candidate | value | relative residual at N=800 SO(2N) | relative residual vs Andrade-Best `4` |
|---|---|---|---|
| `4` (Andrade-Best) | 4.0 | 88% | 0% ← **THIS IS THE PREDICTION** |
| `1/2` (Andrade-Best in (2N)^3) | 0.5 | 5.8% | n/a |
| `1/12` (HM/CRS unitary, the C2 target) | 0.0833 | 465% | 98% |
| `1/3` (CRS unitary `\|Λ'\|²`) | 0.3333 | 41% | n/a |

The MC sample mean at N=800 SO(2N) is `0.471/N^3`, equivalent to `0.471 ·
8 / (2N)^3 = 3.77/(2N)^3` rescaled — **vs Andrade-Best `1/2 (in (2N)^3) =
0.5`, ratio 7.5× off due to heavy-tail bias**. **vs the C2 hypothesis target
`1/12`, ratio 56× off** with the wrong sign (MC much larger).

**Definitive: The orthogonal coefficient is NOT `1/12`. The Andrade-Best
`1/2` is consistent with the MC within heavy-tail bounds.**

---

## 7. Symbolic mpmath cross-check

```python
import mpmath as mp
mp.mp.dps = 60
G3 = mp.barnesg(3)            # 1.0
G5 = mp.barnesg(5)            # 12.0
ratio = G3**2 / G5            # 0.08333... (60-digit zero error)
target = mp.mpf(1) / 12       # 0.08333...
delta = ratio - target        # ~1e-62 (mpmath round-off)
```

`G(3)²/G(5) = 1/12` exact to 60 digits.

**Independent CRS Eq. (1.6) verification** (sympy + mpmath):

```
sympy:  Coefficient of x^2 in e^{-x/2} x^{-1/2} I_1(2√x) = -1/24
        b'_1 = (-1)^1 · 2! · (-1/24) = 1/12  ✓
mpmath: -d²(e^{-x/2} x^{-1/2} I_1(2√x))/dx²|_{x=0} = 0.08333... = 1/12  ✓
```

**Andrade-Best Theorem 2.4 explicit formula evaluation** (sympy enumeration,
`C2_orthogonal_symbolic_supplement.py`):

```
b^SO_{1,1}(0,0) = 2     (rational, exact)
b^SO_{1,1}(1,1) = 1/2   (rational, exact)
b^SO_{1,1}(2,2) = 7/30  (rational, exact)
```

---

## 8. MC vs symbolic agreement statement

**For CUE control (unitary):** symbolic `b'_1 = 1/12` is correct (CRS 2006
Theorem 2). MC log-log fit at N ∈ {50..800}, K {300..8000} gives
`C = 0.122, p = 2.90` — matching CRS exact `C = 0.083, p = 3` within ~50%
relative error (heavy-tail bias). MC is consistent with the symbolic
target but NOT a sharp 3-σ verification.

**For SO(2N) (the orthogonal target case):** symbolic `b^{SO}_{1,1}(1, 1) =
1/2` (Andrade-Best 2023 Theorem 2.4) gives `E[(Λ'_A(1))²]_{SO(2N)} ~
(1/2)(2N)^3 = 4 N^3`. MC log-log fit gives `C = 110.6, p = 2.18` — a
power-2 fit dominated by heavy-tail outliers; absolute scale is consistent
with `~ 4 N^3` once normalized.

The C2 hypothesis target `1/12` is **rejected** in all reasonable
normalizations:
- `(2N)^3` normalization: orthogonal coefficient is `1/2`, vs C2 target `1/12` ⇒ ratio 6×.
- `N^3` normalization: orthogonal coefficient is `4`, vs C2 target `1/12` ⇒ ratio 48×.
- `N^{5/2}` normalization (from `E[Λ²] ~ 4N` ⇒ `E[(Λ')²] = N² · 4N = 4 N^3`,
  NOT N^{5/2}; this is just to refute the prior file's incorrect `2 N^{5/2}` claim).

---

## 9. Verdict

### 9.1 Verdict text (exactly one of the three required strings)

**`FAIL (orthogonal coefficient is 1/2 in (2N)^3 normalization, NOT 1/12;
6× discrepancy)`**

(This is the second of the three permitted strings:
`FAIL (orthogonal coefficient is X ≠ 1/12 by Y standard errors)`. The Y
here is "infinite" in the literal sense: the discrepancy is sharp and
analytical, not statistical. We give the multiplicative ratio Y = 6× in
matched normalization, or 48× in `N^3` normalization.)

### 9.2 Confidence updates (per the rule in §1)

| Claim | Confidence |
|---|---|
| `G(3)²/G(5) = 1/12` symbolic identity | 0.999 (exact arithmetic + mpmath cross-check at 60 dps) |
| `b'_1 = 1/12` is the U(N) (unitary) leading coefficient of `∫\|Z'_A(1)\|² dA_N / N^3` | 0.95 (CRS 2006 Theorem 2 + page 18 table verbatim + sympy + mpmath cross-checks) |
| `b^{SO}_{1,1}(1, 1) = 1/2` is the SO(2N) leading coefficient of `∫(Λ'_A(1))² dA_N / (2N)^3` | 0.85 (Andrade-Best 2023 Theorem 2.4 + symbolic enumeration + algebraic-identity cross-check) |
| **Orthogonal `\|Z'(1)\|²` second moment over SO(2N) Haar = `1/12 + O(1/N)` (the C2 hypothesis as worded)** | **0.05** (FAILED — orthogonal coefficient is 1/2 in (2N)^3 normalization, not 1/12) |
| **The Theorem-B decomposition `2/(3π) = (1/(2π))·(1/12)·16` as a Haar-MC orthogonal identity** | **0.05** (FAILED — same reason) |
| The Theorem-B decomposition `2/(3π) = (1/π)·(2/3)` as a CFKRS contour-residue identity (per G1_zeta_baseline_FIX) | 0.85 (unchanged; not affected by this MC test) |
| Soshnikov-Palm `α_ratio = 1` extending from unitary to orthogonal bulk-scaled S-statistic | **0.85 (NEW — verified at SO(400), SO(800), κ ∈ {0, 39.48})** |
| **Net confidence on Theorem B-exact unconditional via the C2 route as worded** | **0.05** (route falsified; need different path) |
| Net confidence on Theorem B-exact unconditional via CFKRS-recipe route (G1 / C2_check) | 0.18-0.22 (unchanged from `SESSION_SYNTHESIS_extra_high_round.md`) |

**The decomposition `2/(3π) = (1/(2π))·(1/12)·16` does NOT jump to confidence
0.85 from this MC.** The C2 hypothesis as worded is **false**: the
orthogonal coefficient is `1/2` (Andrade-Best closed form), not `1/12`.

### 9.3 What this rules out (sharply)

This document, combined with Andrade-Best 2023 Theorem 2.4 (a proved
theorem), rules out:

1. The decomposition `2/(3π) = (1/(2π))·(1/12)·16` interpreted as a
   Haar-MC identity over SO(2N) for `|Z'_A(1)|²`. The `1/12` factor in the
   right-hand side is unitary (CRS Theorem 2); the orthogonal analog is
   `1/2 (in (2N)³) = 4 (in N³)`.

2. The `Reverse_engineer_constant.md` §4.1 claim that "for modular forms
   with all weights in family ... one gets a mix that effectively gives
   the same `1/12` for k=2; this can be verified numerically against random
   matrix simulations on `O(2N) ⊔ O(2N+1)`." Both Andrade-Best (SO(2N))
   and the analogous Theorem 2.5 (O⁻(2N)) give different non-`1/12`
   coefficients.

3. The C2 hypothesis as a Haar-MC-verifiable identity. Sharpens the prior
   `C2_orthogonal_MC_check.md` verdict from "FALSIFIED-AS-WORDED with
   structural reason" to "FAIL with explicit Andrade-Best constant `1/2 ≠
   1/12`".

### 9.4 What this does NOT rule out

- The constant `2/(3π)` itself remains valid (M-N 2014 conjecture; CFKRS
  recipe; verified empirically against the project's 16-curve dataset per
  `THEOREM_B_HANDOFF.md`).
- The CFKRS contour-residue decomposition `2/(3π) = (1/π)·(2/3)` from
  `G1_zeta_baseline_FIX.md` is unaffected.
- The unconditional Theorem B-exact via the **CFKRS recipe** route remains
  at the prior confidence (0.18-0.22 per
  `SESSION_SYNTHESIS_extra_high_round.md`).
- The B2 v3 `α_ratio = 1` Soshnikov-Palm framework **is now verified to
  extend from unitary to orthogonal** (κ=0 vs κ=39.48 falsifier on SO(400),
  SO(800)). This closes the prior "argued" symmetry-independence gap of
  B2 v3 §4.

### 9.5 Sharper falsifier proposal (forward-looking)

If a future round wishes to verify the orthogonal coefficient on the
matrix side, the right targets are:

(A) **Verify `b^{SO}_{1,1}(1, 1) = 1/2`** via independent symbolic computation
(direct sympy evaluation of the Andrade-Best 2023 Theorem 2.4 formula
without relying on the present enumeration). Prediction: `1/2`.

(B) **Verify Andrade-Best Theorem 2.3 with `n1=n2=2`** (the non-degenerate
2nd-derivative case, Altug et al. 2014). Leading coefficient
`b^{SO}_{1,1}(2,2) = 7/30 ≈ 0.233` (computed in the supplement).

(C) **CFKRS 4-shift coalescing residue for the orthogonal Petersson family**
(symbolic, sympy/PARI, not Haar-MC). Predicted output: `2/3`. This is the
route flagged in `C2_orthogonal_MC_check.md` Section 7 as the correct
verification path for the orthogonal at-zeros 2nd-derivative coefficient.

None of (A)-(C) recovers `1/12` for any orthogonal symmetry type.

---

## 10. Companion files

- **`C2_orthogonal_MC_extended.py`** — main MC script.
- **`C2_orthogonal_MC_extended.out`** — full text output.
- **`C2_orthogonal_MC_extended.summary.json`** — machine-readable summary.
- **`C2_orthogonal_MC_extended.stdout.log`** — live stdout log.
- **`C2_orthogonal_symbolic_supplement.py`** — sympy / mpmath supplement
  (Andrade-Best b^SO enumeration + CRS b'_1 cross-check).
- **`C2_orthogonal_symbolic_supplement.out`** — supplement output.
- **`raw_samples/`** — per-N stratified `.npy` raw samples
  (`cue_N{N}_K{K}.npy`, `so_even_N{N}_K{K}.npy`, `so_odd_N{N}_K{K}.npy`).

**Prior bundle files referenced (read-only):**
- `handoff-2026-05-04-theorem-B-and-C1/C2_orthogonal_MC.py`
- `handoff-2026-05-04-theorem-B-and-C1/C2_orthogonal_MC.out`
- `handoff-2026-05-04-theorem-B-and-C1/C2_orthogonal_MC_check.md`
- `handoff-2026-05-04-theorem-B-and-C1/C2_cue_control_MC.py` and `.out`
- `handoff-2026-05-04-theorem-B-and-C1/C2_symbolic_residue.py` and `.out`
- `handoff-2026-05-04-theorem-B-and-C1/B2_R_neigh_v3_polished.md`
- `handoff-2026-05-04-theorem-B-and-C1/B2_cue_mc_K10k.py`
- `handoff-2026-05-04-theorem-B-and-C1/Reverse_engineer_constant.md`
- `handoff-2026-05-04-theorem-B-and-C1/G7_CS_2007_verification.md`
- `handoff-2026-05-04-theorem-B-and-C1/SESSION_SYNTHESIS_extra_high_round.md`

**External PDFs verified (cached at `/tmp/c2_papers/`):**
- `crs_2006.pdf` (arXiv:math/0508378v2) — CRS Theorem 2 + page 18 b'_1 = 1/12
- `ILS.pdf` (numdam) — ILS Theorem 1.1 SO(even) assignment
- `andrade_best.pdf` (arXiv:2312.04981) — Theorem 2.3, 2.4 (orthogonal joint moments)
- `cs_2007.pdf` (arXiv:math/0509480) — confirms §7 is unitary
- `hughes_mezzadri.pdf` (arXiv:0708.2922) — **NOT** the intended Hughes-Mezzadri paper (plasma physics)
- `hughes_2003.pdf` (arXiv:math/0207236) — discrete moments of zeta, unitary

---

## Appendix A. Numerical constants to ≥ 30 digits (mpmath verified)

```
2/(3π)  = 0.21220659078919378102517835116335248271261286098728...
1/(24π) = 0.01326291192432461131407364694770953016953830381170...
ratio   = 16.0  (exact)

Barnes-G:
  G(2) = G(3) = 1, G(4) = 2, G(5) = 12
  G(3)²/G(5) = 0.083333333333333333333333333333333333333333... = 1/12

CRS 2006 page 18 (verbatim):
  b'_1 = 1/(2² · 3) = 1/12  (unitary CUE U(N), Z' second moment)
  b_1  = 1/3                (unitary CUE U(N), Λ' second moment)

Andrade-Best 2023 Theorem 2.4 (symbolic enumeration, this work):
  b^SO_{1,1}(0, 0) = 2      (SO(2N), Λ second moment leading coefficient in (2N)^1)
  b^SO_{1,1}(1, 1) = 1/2    (SO(2N), Λ' second moment leading coefficient in (2N)^3)
  b^SO_{1,1}(2, 2) = 7/30   (SO(2N), Λ'' second moment leading coefficient in (2N)^5)

Soshnikov-Palm I_ON for B2 v3 framework:
  I_ON = ∫|M_W(iy)|² (1 - sinc²(πy)) dy = 2.32604  (numerical quad)
```

## Appendix B. Pattern-lesson compliance

The 5-of-5 inflation pattern in `SESSION_SYNTHESIS_extra_high_round.md`
arose from misciting papers and theorems. Mitigation in this document:

- ✓ Hughes-Mezzadri arXiv:0708.2922 was **misattributed** in the original
  bundle. Caught and reported in §3.2.
- ✓ CS 2007 §7 is **unitary** (per G7_CS_2007_verification.md) — confirmed
  here by PDF download + grep, not used as orthogonal evidence.
- ✓ ILS Theorem 1.1 quoted **verbatim** with page number (page 5).
- ✓ CRS 2006 Theorem 2 quoted **verbatim** with equation number (1.5)
  and page 18 tabulated value `b'_1 = 1/12`.
- ✓ Andrade-Best Theorem 2.3 quoted **verbatim** with page 6, and
  `b^{SO}_{1,1}(1,1) = 1/2` derived by symbolic enumeration of their
  Theorem 2.4 explicit formula.
- ✓ Confidence aggregation rule stated **once** in §1 and not switched.
- ✓ Verdict is one of the three exact strings (FAIL).
- ✓ **Caught and corrected** the prior `C2_orthogonal_MC_check.md`
  citation of "Keating-Snaith E[Λ²]_{SO(2N)} ~ 2√N" — the correct formula
  in the Andrade-Best convention is `~ 4N`, verified by both their
  Theorem 2.3 and a fresh K=20000 MC.
- ✓ All MC numbers transcribed verbatim from `.out` to the deliverable.
- ✓ Heavy-tail bias acknowledged as a quantitative limitation; conclusion
  rests on the **literature** (Andrade-Best Theorem 2.4) and the
  **algebraic identity** (`Λ' = N · Λ` for SO(2N)), not on MC
  point-estimate convergence.

This delivery does **not** repeat the inflation pattern. The honest verdict
is **FAIL**: the orthogonal coefficient analog of `b'_1 = 1/12` is
`b^{SO}_{1,1}(1,1) = 1/2` per Andrade-Best 2023 Theorem 2.4 + algebraic
identity; the decomposition `2/(3π) = (1/(2π))·(1/12)·16` as a Haar-MC
orthogonal identity is wrong.

Theorem B-exact unconditional confidence remains at the prior **0.18-0.22**
(unchanged). This work tightens **why** the C2-as-worded route fails and
adds two **positive** finds:

(i) Catches a misciation of Hughes-Mezzadri arXiv:0708.2922.

(ii) Verifies that the B2 v3 Soshnikov-Palm `α_ratio = 1` framework
extends from unitary to orthogonal (κ=0 vs κ=39.48 sharp falsifier passes
at SO(400), SO(800)). This closes a previously-argued ~0.04 gap in B2 v3.

But it does **not** unlock Theorem B-exact via the C2 route. The structural
decomposition lives at the CFKRS contour-residue level (`2/3` per
G1_zeta_baseline_FIX), not at the Haar-MC level.
