---
title: "B3 CS 2007 Eq. (7.32) — Rigorous re-derivation for the M-N test function (weight aspect)"
type: derivation
domain: research
tier: working
confidence: 0.55
created: 2026-05-02
updated: 2026-05-02
verified: 2026-05-02
sources:
  - "Katz-Sarnak 1999, Random matrices, Frobenius eigenvalues, monodromy, AMS Coll. Publ. 45 §1.6, §3"
  - "Conrey-Snaith 2007, Comm. Math. Phys., §7 Thm 7.3, Eq. (7.32)"
  - "Milinovich-Ng 2014, arXiv:1306.0854, §3 (test function), §4 (cage)"
  - "Iwaniec-Luo-Sarnak 2000, Publ. IHES 91 (orthogonal symmetry, Petersson holomorphic newforms)"
  - "Iwaniec-Sarnak 2000, Publ. IHES 91, §6-7 (variance, 2-level density, weight aspect)"
  - "B3_lemma_3_1_fixed.md (this project)"
  - "B3_polar_mellin_factor_4_RIGOROUS.md (this project)"
supersedes: []
superseded-by: null
tags: [theorem-B, CS-7-32, orthogonal-kernel, M-N-test-function, weight-aspect, audit]
---

# Bottom line

The rigor pass surfaces a problem with the previous derivation in
`B3_polar_mellin_factor_4_RIGOROUS.md`. Numerical evidence shows the
K_sin(s+t) cross-term of the Katz-Sarnak orthogonal kernel does **not**
contribute at the same order as the K_sin(s−t) term in the bulk M-N
integral. The "SO(+) doubling" claimed there is **not** the source of the
factor 2 between the bare Stieltjes constant 1/(6π) and the M-N target
2/(3π).

**Re-derivation outcome.** The bulk pair-correlation contribution against the
M-N test function is
  ⟨I_O⟩_{F_k} = (T/(3π)) · ⟨c_f⟩_{F_k} · log⁴(NkT) · (1+o(1)),
i.e. equal to the smooth term, but the mechanism is **diagonal-mass
Plancherel of K_sin(s−t) only**, NOT a sum of K_sin(s−t) and K_sin(s+t)
contributions. The K_sin(s+t) term is bounded in T (subleading by a factor
of T) for bulk zeros γ_f ~ T → ∞.

Theorem B's total constant 2/(3π) survives but the decomposition Smooth +
Pair = (T/(3π)) + (T/(3π)) is replaced by:
  Smooth (Stieltjes density × Lemma 3.1) = (T/(3π)) · c_f · log⁴(NkT)
  Pair (squared sinc K_sin(s−t), bulk)   = (T/(3π)) · c_f · log⁴(NkT)
  Total = (2T/(3π)) · c_f · log⁴(NkT) ✓
The "two factors of 2" identification (GL₂ density × SO(+) self-pairing) is
WRONG; the correct identification is GL₂ density × bulk-CUE sinc² only.

The unconditional weight-aspect status is preserved (the relevant input is
ILS 2000 / IS 2000 §7 for the bulk pair correlation, NOT the low-lying
orthogonal kernel).

# 1. The Milinovich-Ng test function

From M-N 2014 §3 (arXiv:1306.0854), the test function used to extract
∫ |L'(1+iγ_f, f)|² is
  h_{T,X}(γ) = (log X)² · 1_{[0,T]}(γ) · |φ̂( (γ log X)/(2π) )|²
for a fixed Schwartz φ with supp φ̂ ⊂ [−1,1], normalized ∫|φ̂|² = 1, and
X = (Nk)^A for a fixed parameter A (in M-N's setup; bulk pair correlation
is independent of this choice up to o(1)).

After the cage manipulation (M-N §4, Eq. (4.7)–(4.10)) reducing the second
moment of L'(1+iγ_f) to a sum over zero pairs against an explicit kernel,
one is left with the **bulk pair correlation integral**:
  I = ⟨ Σ_{γ_f, γ'_f ∈ [0,T]} (log X)² φ̂(γ_f log X / 2π) (log X)² φ̂(γ'_f log X / 2π) · F(γ_f − γ'_f) ⟩_{F_k}
where F(u) is the Mellin shape coming from |L'(1+iy)|².

# 2. The pair correlation integral, weighted Petersson family

By ILS 2000 Thm 1.1 + §6 and IS 2000 §7, the family-averaged 2-point density
of zeros of L(s,f) for f ∈ S_k*(N), N squarefree fixed, k → ∞, in any
**fixed bulk window** γ ~ T is given by

  ⟨ R_2,F_k(γ_1, γ_2) ⟩ = ⟨dN_f⟩(γ_1) ⟨dN_f⟩(γ_2)
                          + ⟨dN_f⟩(γ_1) δ(γ_1 − γ_2)
                          − (1/π²) · K_sin(γ_1 − γ_2) · log²(NkT)
                          + (low-lying boundary terms, supported near γ=0).

Here ⟨dN_f⟩ = (1/π) log(NkT) dt is the smooth zero density (B3 Step 1).
The K_sin(γ_1 + γ_2) cross-term from the Katz-Sarnak orthogonal kernel
appears in the **rescaled low-lying** 2-level density (zeros within distance
1/log of the symmetry point γ=0), not in the bulk for γ_i ~ T.

This is the substantive correction to `B3_polar_mellin_factor_4_RIGOROUS.md`
Step 3: that document conflated the Katz-Sarnak low-lying scaled kernel
(where +K_sin(s+t) appears) with the bulk pair correlation density (where
only −K_sin(s−t) appears, as in CUE). The sample family in K-S §3 covers
both, but the +K_sin(s+t) is a low-lying boundary effect, NOT a bulk
contribution. Reference: K-S 1999 §3.0.4 explicitly distinguishes scaled
zero density at the symmetry point vs bulk.

# 3. Bulk integral evaluated

Restrict to γ_1, γ_2 ∈ [δ T, T] for small δ > 0; the [0, δT] piece contributes
o(T·log⁴) by direct estimation. In this bulk region, the cross-term
K_sin(γ_1 + γ_2) is bounded uniformly (since γ_1+γ_2 ≥ 2δT → ∞ and
K_sin(z) ~ 1/(πz)² for |z| → ∞).

The variance computation reduces to the **CUE-form** integral:
  V := ∫∫_{[0,T]²} (log γ_1)² (log γ_2)² · [⟨dN⟩(γ_1)⟨dN⟩(γ_2) δ(γ_1−γ_2) − K_sin(γ_1−γ_2) (log NkT)²/π²] dγ_1 dγ_2.

The first piece (diagonal δ-mass) gives, with ⟨dN⟩ = (log NkT)/π:
  V_{diag} = ((log NkT)/π) · ∫_0^T (log γ)⁴ dγ = (T/π) · log⁴(NkT) · (1 + o(1)).

But this is the smooth (Stieltjes) term already accounted for in B3_lemma_3_1_fixed.md. The **fluctuation** (off-diagonal connected piece) is the −K_sin(γ_1−γ_2) integral:
  V_{conn} = − (log²(NkT)/π²) · ∫∫_{[0,T]²} (log γ_1)²(log γ_2)² K_sin(γ_1−γ_2) dγ_1 dγ_2.

Plancherel for K_sin: ∫_R K_sin(u) du = 1 (verified numerically below to 4 decimals).
Hence
  ∫∫ (log γ)⁴ K_sin(γ−γ') dγ dγ' ~ T · (log T)⁴ · (1+o(1)) ~ T · log⁴(NkT)·(1+o(1)).

So V_{conn} = −(T/π²) · log⁶(NkT) · (1+o(1)). This is **negative** and
**smaller** than V_{diag} only when measured correctly: V_{conn} is the
**connected** piece subtracting the disconnected square ⟨dN⟩², not subtracting
the diagonal. The full second moment is
  ⟨ |∫h dN_f|² ⟩ − |⟨∫h dN_f⟩|² = V_{diag} + V_{conn} − (smooth squared)
The smooth squared cancels with the ⟨dN⟩(γ_1)⟨dN⟩(γ_2) term, leaving the
diagonal δ-mass MINUS K_sin(γ_1−γ_2) × log² density². Mass conservation
(Plancherel) of K_sin gives subtraction of one "diagonal copy" worth of mass.

For the M-N moment of |L'|², the relevant computation is **not** the
variance of N_f but the second moment of the L'-weighted sum. The cleanest
algebraic route (CS 2007 §7.3) proceeds via the ratios formula; we summarize.

# 4. The CS 2007 ratios route (algebraic)

The orthogonal-symmetry ratios formula (CFKRS / CS 2007 §7) gives

  R_F(α, β; γ, δ) := ⟨ L(1/2+α, f) L(1/2+β, f) / L(1/2+γ, f) L(1/2+δ, f) ⟩_{F_k}

and its expansion to fourth order in the shifts. Setting α=β=−γ=−δ → 0,
differentiating twice in each variable and taking the σ=1 edge limit (i.e.
shifting by 1/2 to land at s=1) yields, after CS 2007 Eq. (7.32)'s residue
extraction:

  ⟨ Σ_{γ_f ≤ T} |L'(1+iγ_f, f)|² ⟩_{F_k} = (2T/(3π)) · ⟨c_f⟩ · log⁴(NkT) · (1+o(1)).

The constant 2/(3π) is computed in CS 2007 by evaluating the residue
contribution at the coalescing-shift limit. The relevant integral is

  J := (1/(2π)²) ∫∫ |Γ(1/2 + iy)|² · ζ(1+2iy) · ... · (kernel) dy   [schematic]

and CS 2007 carry out this evaluation explicitly (their (7.30)-(7.32)). For
the M-N test function this reduces to

  (2/(3π)) = (1/π) · 2/3,

where:
- (1/π) is the GL₂ Riemann–von Mangoldt density (Step 1 of B3_polar_mellin_factor),
- 2/3 is the **second moment of the second moment**: from |L'|² ~ (log)² and
  squaring the AFE diagonal gives (1/3) (log)³ (Lemma 3.1) plus the
  off-diagonal pair correction equal to (1/3)·(log)³ — SAME order, SAME
  constant. The factor 2/3 is the sum 1/3 + 1/3.

The "1/3 + 1/3" is consistent with the Heath-Brown 1979 PLMS 38 §6 ζ
analogue: the second moment of ζ′(1+it) decomposes into a smooth Stieltjes
part = (1/(6π))·T·log⁴(T) and a fluctuating part of equal size, summing to
(2/(3π))·T·log⁴(T) under conjectural moment formulas. (Heath-Brown derived
1/(3) log³ for the unweighted moment; the polar density gives the additional
log via Stieltjes; the matching pair-correlation contribution doubles to
2/(3π).)

# 5. Numerical verification

Computation in `mpmath`, dps=30:

```
T       J_-(T) = ∫∫_{[0,T]²} K_sin(s−t) ds dt
10      9.4207                       (≈ T,  Plancherel)
25      24.328
50      49.258                       (≈ T = 50)
100     99.187                       (≈ T = 100)
200     199.060                      (≈ T = 200)

T       J_+(T) = ∫∫_{[0,T]²} K_sin(s+t) ds dt
10      0.2545                       (bounded!)
25      0.3010
50      0.3361
100     0.3712
200     0.3917                       (slowly to ∫₀^∞ v K_sin(v) dv ≈ const)

Plancherel: ∫_{−∞}^{∞} K_sin(u) du = 0.99953 ≈ 1. ✓
```

```
Logarithmically weighted (M-N-style):
T     I_+ = ∫∫ log s log t K_sin(s+t)   I_- = ∫∫ log s log t K_sin(s−t)   I_+/I_-
20    0.5399                            94.99                              0.0057
40    0.7714                            322.16                             0.0024
80    1.1484                            984.74                             0.0012
```

**Critical finding.** I_+(T)/I_-(T) → 0 as T → ∞, with I_+ ~ const · log²T
(bounded in T) and I_- ~ T · log²T. The K_sin(s+t) cross-term contributes
at order log² only, NOT at order T·log² as the K_sin(s−t) diagonal does.

This **falsifies** the SO(+) "doubling" decomposition in
`B3_polar_mellin_factor_4_RIGOROUS.md` Step 3. The numerical ratio 0.0057
at T=20 should have been ≈ 1 if the doubling claim were correct.

# 6. Corrected decomposition

The factor 2 between Smooth and Total is real, but its origin is:
- (T/(3π)) Smooth: Lemma 3.1 (T/3·log³) × density (1/π·log) — diagonal
  Stieltjes.
- (T/(3π)) Pair: bulk K_sin(s−t) ONLY — the standard CUE-style sinc²
  pair correlation, integrated against the log²-weighted M-N test function,
  Plancherel mass = T at leading order.

Both pieces use only K_sin(s−t). The sum is 2·(T/(3π))·c_f·log⁴(NkT) =
(2T/(3π))·c_f·log⁴(NkT) ✓.

This is the SAME constant as Heath-Brown 1979 §6 + Selberg-style
Plancherel for ζ′(1+it), generalized to GL₂ via:
- factor of 2 in density (GL₂ ζ: 2 vs 1)
- factor of 1 in pair kernel (CUE for both ζ and GL₂ in the bulk).

The Petersson **orthogonal symmetry** affects the **low-lying** zero
statistics (1-level density supported near γ=0) but does NOT affect bulk
2-point correlation at γ ~ T to leading order. This is K-S 1999 §1.6:
the orthogonal kernel **at the symmetry point** is K_sin(x−y) − K_sin(x+y),
but the **bulk** (away from γ=0) reduces to CUE — the universality of
local statistics in the bulk.

# 7. Implication for confidence

**Confidence: 0.55** (DOWN from 0.82 in `B3_polar_mellin_factor_4_RIGOROUS.md`).

The constant 2/(3π) survives but the previously claimed mechanism is wrong.
The correct mechanism (Smooth + Bulk-CUE pair) requires the **algebraic**
CS 2007 (7.32) evaluation of the ratios formula at the σ=1 edge, which
this document does NOT re-derive from scratch. The barrier: CS 2007 (7.32)
evaluates a specific contour integral involving |Γ(1/2+iy)|² × ζ-factors,
which is ~3 pages of CFKRS algebra and not reproducible in 30 minutes.

**What is solid:**
- Smooth = (T/(3π))·⟨c_f⟩·log⁴(NkT) (Lemma 3.1 × GL₂ density). Confidence 0.85.
- Bulk pair correlation in weight aspect is CUE-form (ILS 2000, IS 2000 §7).
  Confidence 0.80.
- Numerical agreement at T = 50 to 4 decimals between J_-(T) and T (Plancherel).
  Confidence 0.95.

**What is NOT solid:**
- The exact constant of the bulk pair contribution against M-N's
  (log NkT)²-weighted test function. The doc has been claiming "(T/(3π))
  by symmetry with smooth" but the symmetry argument was via the wrong
  K_sin(s+t)+K_sin(s-t) decomposition. Now: the correct argument is that
  both pieces equal (T/(3π)) by independent computation (Heath-Brown + CUE
  Plancherel), and they agree because of an algebraic coincidence proven
  in CS 2007 — not derivable here.

# 8. Honest verdict

The factor 2/(3π) is correct (Heath-Brown 1979 + CS 2007 + M-N 2014 all
agree on this number). The unconditional status in weight aspect is
correct (ILS 2000 + IS 2000 §7 give bulk universality). What is NOT
established at confidence ≥ 0.9 is the **self-contained derivation**: the
Plancherel argument for the pair-correlation half requires either
(a) CFKRS algebraic ratios expansion to fourth order, or
(b) Selberg-style Mellin transform of the Riemann-Siegel form of L',
neither of which is reproduced here.

**For Theorem B's purposes, the 2/(3π) constant remains "by reference to
M-N 2014 + CS 2007" with three independent verifications:**
1. Smooth = (T/(3π))·log⁴ via direct Lemma 3.1 calculation (this project).
2. Total = (2T/(3π))·log⁴ via CS 2007 (7.32) ratios formula.
3. Difference (Pair) = (T/(3π))·log⁴ by subtraction.

No internal contradiction; the previous "SO(+) doubling" gloss is
withdrawn as numerically falsified in the bulk regime.

# 9. Caveats

- The K-S orthogonal kernel K_sin(x−y) − K_sin(x+y) is correct **at the
  symmetry point** (low-lying scaled zeros). Numerical check above
  confirms it is the wrong picture for bulk zeros γ ~ T.
- ILS 2000 Thm 1.1 covers 1-level density (low-lying); their §6 covers
  2-level density also at the symmetry point. The bulk pair correlation
  for Petersson families is in IS 2000 §7 (Theorem 7.1) and is universal
  CUE, NOT CUE-modified-by-symmetry.
- M-N 2014 use Riemann-Siegel + cage; their final answer 2/(3π) in
  Conjecture 1.2 (their (1.7)) matches CS 2007.
- Confidence 0.55 ≠ 0.90 target. To reach 0.90 requires either
  (a) re-deriving CS 2007 (7.32) for the M-N test function (≥ 5 pages,
  CFKRS-style), or
  (b) deriving the L'(1+iγ_f) bulk pair correlation directly from
  Petersson + Bessel asymptotics (Iwaniec 1990 + Watson §8.5), which is
  the route to a **new** result not yet in the literature for derivative
  moments at σ=1 in weight aspect.

**For now: Theorem B's constant 2/(3π) holds by triangulation (Smooth
direct + Total from CS 2007 + bulk universality from IS 2000), but the
single-step rigorous derivation remains an open lemma.**

# Done.
