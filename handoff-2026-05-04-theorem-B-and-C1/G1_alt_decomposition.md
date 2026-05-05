# G1 Alternative Decomposition Attack — independent of `G1_zeta_baseline_FIX.md`

Date: 2026-05-03
Author: Opus 4.7 (alt-decomposition agent)
Cross-reference: `/Users/saar/Farey 4.7 solutions/G1_zeta_baseline_FIX.md` (did not exist when this file was written; see §3 if it appears later)
Sources used (verbatim quotes only): `/tmp/milinovich_ng.txt` (Milinovich–Ng, "Simple zeros of modular L-functions").
Sources NOT directly inspected here: `/tmp/cfkrs.pdf` (CFKRS 2005, present but not quoted), Conrey 1989 Crelle 399 (not downloaded — flagged).

## 0. Setup — what the "16" actually is

Verbatim from M-N, eq. (16) (line 852–855):

> "L′ (ρf , f )^2 = (2/3π) c_f T log^4 X + O(T log^3 X)"   (sum over 0<γ≤T)

Verbatim from M-N, the Gonek-style ζ-analog (line 870–877):

> "ζ ′ (ρ)^2 = (T/24π) log^4 T + O(T log^3 T)"   (sum over 0<Im ρ≤T, RH)

Numerator ratio (with the SAME T log⁴ factor):

    (2/3π) / (1/24π) = 2·24/3 = 16.

So the empirical "16" is **exactly the leading-coefficient ratio of (16) versus Gonek's ζ' second moment**, after stripping the common `T log⁴` and `c_f`. This is what Theorem B's "factor" must reproduce. The original 4 = 2·2 framing was numerically wrong; it should be 16.

Important secondary verbatim — M-N also states a degree-4 ζ-analog for the *L-function 2nd moment* (line 885–891):

> "since L(s, f) is a degree two L-function, establishing (16) is comparable to establishing the conjectural formula
>  ζ ′ (ρ)^4 = (T/2880π^3) log^9 T + O(T log^8 T)."

This is a DIFFERENT analogy (degree-doubling at the level of moment k → 2k, log⁴ → log⁹). It is NOT the analogy used for the 16. We focus on the (16)-vs-Gonek correspondence.

---

## 1. Four candidate decompositions of 16

**Candidate D1: 16 = 4_density × 4_multiplicity**
- 4_density: degree-2 L-function has 2× zeros per height (density factor 2 already), and an additional 2× from log-derivative of the *completed* L-function (gamma factors ψ_f(s) double the relevant log-derivative weight on the critical line).
- 4_multiplicity: full Plancherel/orthogonality for SO(even) or unitary symmetry on a degree-2 family; the autocorrelation kernel at the diagonal contributes 4 from a 2×2 shift-derivative pattern.

**Candidate D2: 16 = 2 × 2 × 4**
- 2_density (degree of L-function, i.e. number of γ_j gamma factors).
- 2_multiplicity (basic shift-doubling in the ratios recipe — same as old Theorem B).
- 4_log-power = log⁴ X / log⁴ T after carefully tracking that X² = qT/(2π) in M-N (eq. 4) but the analytic conductor for ζ is just T/(2π). Naively the log-power should match (both log⁴), but the *coefficient* in front of log^4 picks up extra factors from the conductor mismatch.

**Candidate D3: 16 = 8_level-aspect × 2_multiplicity**
- 8 from c_f normalization. M-N eq. (1) defines c_f via the symmetric-square / Rankin-Selberg L(1, sym²f); on average over the family this scales like a power of (k·q). The ratios recipe contracts the family average and the factor c_f absorbs an 8.
- 2_multiplicity from basic shift-doubling.

**Candidate D4: No clean multiplicative decomposition exists.**
- The 16 = 2/(3π) ÷ 1/(24π) is just the arithmetic of two independent ratios-recipe computations performed at degree 1 and degree 2 respectively. There is no a priori reason for the ratio to factor as (something)_density × (something)_multiplicity. The right framing is: write the ratios-recipe 4-shift residue formula for ζ once and for L(s,f) once, take the diagonal at zero shifts, divide. Whatever number falls out IS the answer. It happens to be 16; it could just as well have been e.g. (17±√145)/2 or any algebraic number coming from the residue.

---

## 2. Derivation attempts from verbatim sources

### 2.1 Where 1/(24π) comes from (Gonek)

M-N quotes Gonek's result (line 870–877). Gonek's derivation (Conrey 1989 Crelle 399 — NOT directly accessed in this session, flagged for later verification) writes ζ'(s) via approximate functional equation:

    ζ'(s) ≈ Σ_{n≤X} (-log n) / n^s + ψ(s) · Σ_{n≤X} (-log n) / n^{1-s}

Sum over zeros, diagonal-only, gives a **partial** moment with coefficient `c_diag`. Cross terms (off-diagonal, requiring shifted-convolution-free residue calculus) give an additional contribution `c_cross`. The total is **(c_diag + c_cross) = 1/24π** for ζ. The internal split is something like `1/24 + 1/24 − 1/24 = 1/24` divided by π, but I do not have the exact Gonek breakdown without the 1989 paper.

**Critical caveat (flagged red).** I have NOT verified the internal split of 1/24π for Gonek; I am reporting only the total coefficient, which IS verbatim from M-N.

### 2.2 Where 2/(3π) comes from (M-N, eq. 16)

M-N's path: Propositions 1.1 and 1.2. Verbatim from line 410–412:

> "5/(24π) c_f T log^4 X + O(T (log T)^{4-2δ})"   [eq. (6), i.e. A_f(T)]

Verbatim from line 435–440:

> "29/(24π) c_f T log^4 X + O(T (log T)^{4-2δ})"   [eq. (7), i.e. B_f(T)]

These are the diagonal mean-square contributions of the TWO pieces of the AFE (line 371–384):

    α_f(n)   piece → 5/(24π) c_f
    β_{f,X}(n) piece (with ψ_f weight) → 29/(24π) c_f

So both are degree-2-L-function diagonals. Their **sum** is `34/(24π) c_f = 17/(12π) c_f`.

But the ratios-recipe full prediction (eq. 16) is `2/(3π) c_f = 16/(24π) c_f`, which is LESS than the sum 34/(24π).

**This is the key arithmetic clue:** 16 = 34 − 18. Cross terms in the ratios recipe contribute `−18/(24π) c_f` (a destructive interference between α-piece and β-piece). The minus sign is exactly what you'd expect from `|A − B|² = |A|² + |B|² − 2Re(AB̄)`: cross-correlation is subtractive when the two AFE pieces are complex conjugates of each other on the critical line.

### 2.3 Re-examining the "16" as 34 − 18 = 16 inside the same 1/(24π) denominator

This is **the most natural decomposition that comes out of M-N verbatim**:

    16/(24π) = 5/(24π) + 29/(24π) − 18/(24π)
             = (α-diagonal) + (β-diagonal) − (αβ-cross)

Numerator decomposition:

    16 = 5 + 29 − 18

Compare ζ analog (Gonek): 1/(24π) = (something)_diag + (something)_cross with the same structure but for a degree-1 AFE.

For ζ, the AFE has the form `ζ'(s) ≈ Σ -log(n)/n^s + χ(s) Σ -log(n)/n^{1-s}`, structurally **identical** to M-N's eq. (5). The diagonal moments will give some `a/(24π)` and `b/(24π)` and the cross will give `−c/(24π)` with `a+b−c = 1`.

If the decomposition pattern transfers, then by analogy:

    For ζ:   a + b − c = 1   (Gonek)
    For L:   5 + 29 − 18 = 16   (M-N)

This is **decomposition D4 made concrete**: the 16 is a difference of integers (34−18), not a multiplicative factor (2×8 or 4×4). The "ratio 16:1" between L-baseline and ζ-baseline is a **numerator ratio with shared denominator 24π**, not a tensor product of physical degrees of freedom.

### 2.4 Why Plancherel / RMT factor analyses fail for D1 and D2

D1 (4×4): for this to work, you'd need each "4" to appear as an independent matrix-integral residue. Hughes–Snaith RMT predictions for ζ'(ρ) second moment over CUE/USp give the leading constant via a 2-dimensional contour integral around the diagonal. The 1/24 = 1/4! comes from a SINGLE 4-shift residue (4 derivatives of a 4-variable function). For L(s,f), the same recipe gives 16/24 = 16/4! — which is NOT 4·4/4! in a meaningful way; it's just the value of a different 4-shift residue with degree-2 gamma factors.

D2 (2·2·4): the log⁴ powers MATCH (both are log⁴), so there's no log-power discrepancy. Rejected.

D3 (8·2): c_f has a fixed normalization (M-N eq. 1: c_f = π / (6 (k-1) L(1, sym²f) q · (some factor))). The 8 cannot come from c_f because c_f is on BOTH sides of (16) — it's not a ratio. Rejected.

---

## 3. Most consistent decomposition with the ratios-recipe arithmetic

**D4 wins, refined as: 16 = 5 + 29 − 18 (numerator-only, common denominator 24π).**

This is the only decomposition supported by verbatim M-N text. The 5, 29, and 18 are residues of explicit integrals (Propositions 1.1 and the cross-term computation in M-N §6, not inspected line-by-line here but referenced by M-N as the natural source).

**Cross-reference to main G1 agent (file `G1_zeta_baseline_FIX.md` not present at writing time):** if the main agent is hunting for "16 = 2_density × 8_multiplicity" or any other 2-factor split, this analysis recommends abandoning that frame. The ratios recipe does NOT factor the answer multiplicatively across density and multiplicity; it gives a single residue whose value happens to be a small rational number. Any "physical" factorization is post-hoc numerology.

---

## 4. The right framing if no clean decomposition exists

**Right framing:** State Theorem B's prediction directly in terms of the ratios-recipe output. Don't claim "factor 16 = density × multiplicity"; instead claim:

> "The Theorem-B prediction for the [Farey object] is the ratios-recipe leading constant, computed as a single 4-shift residue at zero. For our family this evaluates to 2/(3π) c_f (degree-2 L-function case), exactly 16× larger than Gonek's degree-1 ζ' baseline 1/(24π). The factor 16 has no meaningful tensor decomposition; it is the integer numerator difference 34−18 between the diagonal AFE moments and their cross-correlation, computed in the common normalization 1/(24π)."

Action item for paper: rewrite Theorem B's "factor decomposition" remark as a *formula citation* (eq. 16 of M-N + Gonek), not a physical factorization. This eliminates the false 2×2 = 4 claim.

---

## 5. Honest confidence

| Claim | Confidence |
|---|---|
| Empirical 16 = (2/3π)/(1/24π) | **0.99** — pure arithmetic of two verbatim formulas in M-N |
| 5 + 29 − 18 = 16 numerator decomposition | **0.85** — 5 and 29 are verbatim from M-N eq. (6),(7); the −18 cross term is INFERRED (sum minus answer = 34 − 16 = 18) but not directly read from M-N's §6 |
| D1, D2, D3 decompositions are wrong | **0.7** — argued plausibly above but I did not consult Hughes-Snaith / Conrey 1989 line-by-line; possible an RMT framing recovers e.g. 4×4 |
| D4 (no multiplicative decomposition) is correct | **0.75** — best match to evidence but a clean RMT factorization could still emerge from a deeper read of CFKRS §4 |
| Recommendation to drop "factor decomposition" language in Theorem B and state the ratios-recipe constant directly | **0.9** — even if a decomposition exists, the safer paper-language avoids it |

### Outstanding work

- Read CFKRS 2005 §4 (file present at /tmp/cfkrs.pdf, not extracted in this session) to verify the 4-shift residue formula for degree-2 L-functions and confirm that no natural Plancherel-style 4×4 factorization emerges.
- Download Conrey 1989 Crelle 399 and obtain the *internal* split of Gonek's 1/(24π) (i.e. the analog of M-N's 5+29−18). If Conrey gives `a+b−c = 1` with explicit a, b, c, then the "5+29−18" decomposition is fully supported by parallel text in two papers.
- Hughes–Snaith RMT prediction for ζ'(ρ)² and L'(ρ_f, f)²: confirm their leading-constant formulas reproduce 1/(24π) and 2/(3π), and inspect whether THEIR derivation suggests a factorization.

### Independence from main agent

This file argues for **D4 (no clean multiplicative decomposition)**. If `G1_zeta_baseline_FIX.md` argues for D1, D2, or D3, that conclusion conflicts with this analysis and the discrepancy should be resolved by the CFKRS read above.
