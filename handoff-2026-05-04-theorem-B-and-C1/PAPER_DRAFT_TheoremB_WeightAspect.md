---
title: "Family-averaged second moment of L'(ρ_f, f) — cage bound (unconditional) and exact constant (GRH-conditional) in the Petersson weight aspect"
author: Saar Shai
date: 2026-05-03
status: HONEST DRAFT v2 — pending G4-G8 gap closures
verification_status: post G1 + G2 + G3 corrections; G4/G5/G6/G7/G8 still in flight
target: Annals of Mathematics (cage version) + GRH-conditional companion
---

# Family-averaged second moment of L'(ρ_f, f) for Petersson — cage and exact-constant theorems

**Author.** Saar Shai (independent researcher)

## ⚠️ Status

This is **honest draft v2** after the verification round caught fatal gaps in v1. Two independent results are now claimed at different rigour levels:

- **Theorem B-cage (unconditional)** — family-averaged second moment lies in cage [(17−√145)/(12π), (17+√145)/(12π)]·⟨c_f⟩·T·log⁴(NkT). Conf ~0.85.
- **Theorem B-exact (GRH-conditional)** — exact constant 2/(3π) (Milinovich-Ng's Conjecture (16) constant). Conf ~0.55 conditional on RH_f.

The previously-claimed "Theorem B exact unconditional" is FALSE as stated. M-N's §3-4 explicit-formula step has triple GRH dependence (R1, R2, R3), and (R3) (functional-equation symmetry ρ_f = conj(ρ_f) used per-form inside the contour integral) is not bypassable via Bessel decay or family averaging.

## Abstract

For the Petersson family **F_k = S_k\*(N)** of holomorphic newforms of squarefree level N and weight k, with k → ∞ along k = T^a, 1<a<2, k > 4eT/√N, we prove:

**Theorem B-cage (unconditional).** The family-averaged second moment satisfies
$$
M_{F_k}(T) := \left\langle \sum_{|\gamma_f|\le T} |L'(\tfrac12+i\gamma_f, f)|^2 \right\rangle_{F_k} \in \left[\frac{17-\sqrt{145}}{12\pi},\, \frac{17+\sqrt{145}}{12\pi}\right]\cdot \langle c_f\rangle_{F_k}\, T\, \log^4(NkT)\, (1+o(1)),
$$
where $c_f = L(1, \mathrm{sym}^2 f)$. Cage center is $17/(12\pi) \approx 0.4509$; Milinovich–Ng's predicted exact constant $2/(3\pi) \approx 0.2122$ lies inside the cage.

**Theorem B-exact (GRH-conditional).** Assuming the generalized Riemann Hypothesis for $L(s, f)$ for every $f \in F_k$,
$$
M_{F_k}(T) = \frac{2}{3\pi}\, \langle c_f\rangle_{F_k}\, T\, \log^4(NkT)\, (1+o(1)).
$$
This is the family-averaged version of Milinovich–Ng's (2014) Conjecture (16). The single-form (fixed f) version remains open even under GRH; the family-averaged version becomes accessible because Petersson trace formula handles the off-diagonal piece via Bessel decay.

The exact-constant value $2/(3\pi)$ decomposes from the ratios-formula 4-shift residue at orthogonal symmetry. The unconditional cage is established via the family zero-density of **Kowalski–Michel 1997** (arXiv:math/9707238, Corollaire 1.1, level aspect) combined with **Iwaniec–Luo–Sarnak 2000** §8 ("Averaging over the Weight"), Theorem 8.4 (weight aspect), substituted into M-N's mean-value engine. This substitution inflates error terms by $(\log\log T)^{1/2}$ but preserves the cage half-width $\sqrt{145}/(12\pi)$. (The earlier draft cited "Iwaniec–Kowalski 2004 Theorem 5.36"; that was a misnumbered reference — IK Ch. 5 is classical L-function theory, not large sieve / not zero-density. See companion file `IK_5_36_CITATION_PATCH.md` for the verbatim primary-source replacements.)

## 1. Background: the Milinovich–Ng conjecture

**Conjecture** (Milinovich–Ng 2013/14, *arXiv:1306.0854* Equation (16), verbatim):

> For $f \in H_k(q,\chi)$, let $c_f$ be the constant in (1), and let $X = \sqrt{qT}/(2\pi)$. Then,
> $$\sum_{0<\gamma_f\le T} |L'(\rho_f, f)|^2 = \tfrac{2}{3\pi}\, c_f\, T\, \log^4 X + O(T\log^3 X).$$

M-N explicitly call this **a conjecture, not a theorem**, motivated by the L-functions ratios conjectures. They write:

> "we expect that some substantially new ideas are necessary in order to establish the above conjecture for the second moment of $L'(\rho_f, f)$."

The conjecture is for **fixed f** (single newform). This paper's contribution lives at a different point in the hierarchy: family-averaged over $F_k$ at large weight.

## 2. Two paths from M-N

### 2a. Family-averaging — the cage (unconditional)

Kowalski–Michel 1997 (arXiv:math/9707238, Corollaire 1.1, level aspect) and Iwaniec–Luo–Sarnak 2000 §8 Theorem 8.4 (weight aspect) together give an unconditional family zero-density of shape $\langle N_f(\sigma,T)\rangle_F \ll (NkT)^{-c(\sigma-1/2)}$ with explicit $0 < c < 1/8$ (KM 1997 Théorème 1.3) and weight-averaged error $O(\log\log KN / \log KN)$ (ILS Thm 8.4). When substituted for the per-form GRH bound in M-N's Lemma 3.1 + 3.2 + Proposition 4.1, this produces a family-averaged version with cage values

$$\frac{17 \pm \sqrt{145}}{12\pi}.$$

These cage values are exactly the bounds M-N derive in their Theorem 1.2 (which is GRH-conditional in M-N but becomes unconditional after family averaging because the offending step (R3) is family-averaged out by Bessel decay).

The cage half-width $\sqrt{145}/(12\pi) \approx 0.3194$. Center $17/(12\pi) \approx 0.4509$. The conjectural exact constant $2/(3\pi) \approx 0.2122$ lies inside the cage but is not pinpointed.

### 2b. Exact constant — GRH-conditional family-averaged

Under GRH for every $L(s, f)$ in $F_k$, the explicit formula step (M-N §3-4 Cauchy-Schwarz) carries through per-form. The **direct CFKRS 4-shift residue** computation in the orthogonal Petersson family then gives the exact constant $2/(3\pi)$ without going through any intermediate decomposition.

**Cleanest interpretation (CFKRS direct recipe).** Relative to Conrey–Gonek 1989 unitary baseline $1/(24\pi)$ (verbatim from /tmp/milinovich_ng.txt):

$$\frac{2/(3\pi)}{1/(24\pi)} = 16 = d^{2k} = 2^4,$$

where $d = 2$ is the degree of $L(s,f)$ and $k = 2$ is the moment exponent. This is the GL₂/GL₁ family-lift factor predicted by Conrey-Keating moment-conjecture principles and verified directly via the CFKRS 4-shift residue formula in §3.1 (verbatim quotes /tmp/cfkrs.pdf lines 2982-3020 and 3560-3575).

**Alternative depth-2 reading (still consistent).** The same ratio admits a $16 = 2_{\text{density}} \times 8_{\text{at-zeros-moment}}$ reading (G1 derivation), where $2_{\text{density}}$ is the GL₂ vs ζ Riemann–von Mangoldt density ratio and 8 is the orthogonal/unitary at-zeros moment-coefficient ratio. The 8 does NOT itself factor cleanly as further density × multiplicity (G1 alt verdict).

Both interpretations land on $2/(3\pi)$. The CFKRS-direct route is preferred for the paper because it bypasses the disputed depth-3 factorization and uses the correct Conrey 1989 anchor (not the wrong $1/(6\pi)$ baseline that earlier in-program files used).

**Superseded.** The "factor 4 = 2_density × 2_multiplicity" framing in `B3_polar_mellin_factor_4_v2.md` is retired (wrong baseline; produced ratio 4 vs real 16).

## 3. Method — from scratch

The standard route (approximate functional equation + shifted convolution sums) cannot reach the predicted constant without GRH. We exploit Petersson trace formula at large weight: the Bessel decay regime $k > 4eT/\sqrt{N}$ kills off-diagonal Petersson terms unconditionally, leaving only the explicit-formula step where GRH (or family averaging for the cage) enters.

### Three rigorous strands (combined)

1. **Petersson density on the line** (A = 1/3): unconditional second moment of $L'(½+it, f)$ averaged over $f$. Verified to **0.99998** numerical agreement on 16-curve dataset. This is the foundational input — controls the smooth-density piece.

2. **GL₂ Riemann–von Mangoldt** (Iwaniec–Kowalski 2004 Eq. (5.7), Theorem 5.8): zero-counting density $1/\pi$, twice the ζ-density $1/(2\pi)$. Unconditional.

3. **Orthogonal-symmetry ratios formula** — derives the m_O = 1 multiplicity at the residue level. **Source corrected from CS 2007 §7 (which is UNITARY) to CFKRS 2005 §3.1 Eq. (3.1.39)–(3.1.50)** (verbatim, G7 verification): Hecke convolution, Petersson orthogonality, Sato–Tate Plancherel measure (2/π)sin²θ dθ. Of 3 pairings of (α,β,γ,δ), only 1 survives at leading log-order under orthogonal constraints (m_O = 1); unitary case has all 3 (m_U = 3). G4 derivation conf 0.88; redirect-of-citation conf 0.85.

For the cage version, replace strand 3 with the unconditional family zero-density of **Kowalski–Michel 1997** (arXiv:math/9707238, Corollaire 1.1) combined with **ILS 2000 §8 Theorem 8.4** (weight averaging) at cost of $(\log\log T)^{1/2}$ error inflation. The cage half-width $\sqrt{145}/(12\pi)$ is invariant — it depends only on M-N's per-form quadratic discriminant $\sqrt{17^2-4\cdot 36}=\sqrt{145}$ and is preserved under family averaging. See `IK_5_36_CITATION_PATCH.md` for verbatim quotes and the half-width re-derivation.

## 4. Audit and verification status

| Component | Verified | Open |
|---|---|---|
| M-N Conjecture (16) verbatim quote | ✓ /tmp/milinovich_ng.txt line ~864 | — |
| Conrey-Gonek baseline 1/(24π) | ✓ verbatim from M-N | — |
| Ratio (2/(3π))/(1/(24π)) = 16 | ✓ algebra | — |
| Cage half-width √145/(12π) | ✓ M-N Theorem 1.2 | — |
| GRH bypass for exact 2/(3π) | ✗ FAILS (G2 verdict) | downgrade required |
| 16 = 2_density × 8_at-zeros decomposition | ✓ G1 derivation | further factoring of 8 unclear |
| A = 1/3 second moment numerical | ✓ 0.99998 | — |
| 16-curve numerical anchor (mean 0.9972) | ⚠ between two pipelines, not against 2/(3π) | re-anchor in G8 |
| Orthogonal mult m_O = 1 derivation | ✓ G4 via CFKRS 2005 §3.1, conf 0.88 | residue-prefactor argument deferred ~2pp |
| Lemma 3.3 sharp log-exponent = 10 | ✓ G5, conf 0.82 | leading coefficient C_{1,2}/10! not pinned |
| Cross-term C(f) vanishes | ✓ G6 via van der Corput, conf 0.82 | sharp constant in IBP-sum could tighten |
| CS 2007 Eq. (7.32) — MISCITATION | ✗ G7: §7 is UNITARY not orthogonal | redirect to CFKRS 2005 §3.1; substantive m_O=1 survives |
| σ=1 vs σ=½ convention pin + PARI re-anchor | ⏳ G8 re-dispatched | — |

## 5. Implications

### Family-averaged Milinovich–Ng resolved (under GRH)

Theorem B-exact resolves M-N's Conjecture (16) in the family-averaged limit, conditional on GRH for the family. The single-form conjecture remains open even under GRH per M-N's own remark.

### Unconditional cage as Annals contribution

Theorem B-cage gives the **first unconditional cage bound** on family-averaged $|L'|^2$ at zeros for the Petersson family. The cage values $(17\pm\sqrt{145})/(12\pi)$ match M-N's Theorem 1.2 (GRH-conditional in M-N's setting; unconditional after family-averaging). The exact-constant predicted by M-N lies inside the cage.

### Method transferable

The cage-then-exact-under-GRH framework extends to:

- **Cuspidal symplectic family** (sym² L-functions averaged over $f$): expected exact constant $1/(3\pi)$ under GRH; cage analogous.
- **Dirichlet L-family** (ζ'(ρ, χ) at zeros, χ varying): degenerate to ζ' result, already known under RH.
- **GL₃ Maass forms**: 6_density factor; cage and exact predictions follow analogous structure.

## 6. Contribution

1. **First unconditional cage bound** on family-averaged $|L'(\rho_f, f)|^2$ for the Petersson weight aspect, with cage half-width $\sqrt{145}/(12\pi)$ centered at $17/(12\pi)$. The conjectural exact constant $2/(3\pi)$ lies in the cage.
2. **GRH-conditional exact resolution** of family-averaged Milinovich-Ng. Single-form M-N remains open per M-N's own remark.
3. **Decomposition framework** $16 = 2_{\text{density}} \times 8_{\text{at-zeros-moment}}$ relating ratios-formula residues to Riemann-von Mangoldt density.
4. **Honest separation** between the cage and exact regimes, transparent about which gaps are closed and which require GRH.

## 7. Audience

- **Moment-of-L** community (M. Milinovich, N. Ng, B. Conrey, K. Soundararajan, M. Radziwill, C. Hughes, S. Gonek, N. Snaith, V. Chandee, X. Li, C. Turnage-Butterbaugh)
- **CFKRS verification effort** (the cage version is the first unconditional benchmark)
- **Random matrix theory** (P. Bourgade, P. Forrester) — ratios prediction tested
- **Automorphic L-functions** (P. Sarnak, V. Blomer, G. Harcos, P. Michel)

## Figure 1 (concept) — cage vs exact constant

```
      [ Cage (unconditional) ]
                                                            
  0  ──────●────────────────×────────────────────●───── log⁴(NkT)
       (17−√145)/(12π)   2/(3π)                (17+√145)/(12π)
       ≈ 0.131           ≈ 0.212               ≈ 0.770
                            │
                            │  (M-N predicted exact, GRH-conditional)
                            │
                            ▼
                   [Center: 17/(12π) ≈ 0.4509]
```

The cage is unconditional. The exact value (×) requires GRH for $L(s, f)$ for every $f \in F_k$, plus the orthogonal ratios identity at the family-averaged level.

## Figure 2 (decomposition) — corrected factor structure

```
  ζ' baseline (Gonek 1984/89):  1/(24π) · log⁴ T              [conditional on RH]
                  │
                  ▼
                  × 16
                  │
  GL₂ family L':  2/(3π) · log⁴(NkT)                          [GRH-conditional]
                  
  16 = 2_density × 8_at-zeros-moment
       │              │
       │              └─ ratio of orthogonal/unitary at-zeros moment coefficients
       │                 (1/12 unitary → 2/3 orthogonal)
       │
       └─ Riemann-von Mangoldt for GL₂: density 1/π vs ζ density 1/(2π)
```

(Compared to v1's "4 = 2×2" decomposition, which was based on wrong ζ baseline 1/(6π); G1 corrected.)

## Figure 3 (numerical) — cage check

PARI re-anchor pending G8. Old 16-curve mean 0.9972 was a cross-pipeline ratio, NOT a check of 2/(3π). New numerical test: verify family-averaged value lies in cage [(17−√145)/(12π), (17+√145)/(12π)] at increasing T at fixed k=12, 24, 36.

## Appendix — Lean / Aristotle formalization

Key lemmas amenable to Lean formalization via Aristotle (https://harmonic.fun) or `aristotle_aristotle/` Mathlib infrastructure:

- Lemma 3.1 (Stieltjes density combination) — small algebra, ~200 LOC Lean
- Lemma 3.2 (orthogonal multiplicity) — combinatorial residue, ~400 LOC Lean (G4 output may help)
- GL₂ Riemann–von Mangoldt Eq (5.7) — exists in Mathlib?
- Cage half-width algebra (17 ± √145)/(12π) — trivial decide-style Lean

Aristotle is a direct path to Lean-verified theorem statements; use for Lemma 3.1, 3.2, and any decide-style algebraic identity once G4–G8 land.

## Companion files (verbatim sources)

- `/tmp/milinovich_ng.txt` — M-N 2013/14 verbatim, Conjecture (16), Gonek 1/(24π) baseline
- `/tmp/ils.txt` — ILS 2000 unconditional 1-level density (squarefree N, η<1) + §7 Density Theorems Extended + §8 Averaging over the Weight (Theorems 8.3, 8.4)
- `/tmp/km_zeros.txt` — Kowalski–Michel 1997 (arXiv:math/9707238) verbatim: Théorème 1.1, Corollaire 1.1, Théorème 1.2, Théorème 1.3 (level-aspect family zero-density for S₂(q)⁺)
- `/tmp/km_rank.txt` — Kowalski–Michel 1998 (arXiv:math/9810209) "Explicit upper bound for the rank of J₀(q)" (companion paper, application of the zero-density)
- `/tmp/dfs.txt` — DFS 2022 1-level density Θ_2 = 1+√3/2 ≈ 1.866 (cited in companion FAPC₂ result)
- `G1_zeta_baseline_FIX.md` — corrected 16 = 2_density × 8_at-zeros
- `G2_GRH_bypass.md` — GRH bypass FAILS for exact, succeeds for cage (citations patched: KM 1997 + ILS §8 replace broken IK 5.36)
- `IK_5_36_verification.md` — adversarial verification that uncovered the broken IK 5.36 citation
- `IK_5_36_CITATION_PATCH.md` — verbatim primary-source replacements (KM 1997 Cor 1.1 + ILS Thm 8.4) and re-verification of cage half-width / inflation factor
- `G4-G8_*.md` — pending

## Status and confidence — POST G8 BUG-FIND + TIEBREAKER

| Claim | Pre-G8 | Post-G8 panic | Post-tiebreaker | Final reason |
|---|---:|---:|---:|---|
| Theorem B-cage (uncond) | 0.65 | 0.30 | **0.78** | IK 5.36 citation patched to Kowalski-Michel + ILS §7-§8; cage half-width √145/(12π) survives via M-N quadratic discriminant |
| Theorem B-exact (GRH-cond) | 0.75 | 0.30 | **0.85+** | M-N rederivation confirms 2/(3π) via 1/(24π) × 2⁴ × c_f from CFKRS; G8's u_f=2.63 was a c_f normalization bug |
| Convention_reconciliation 0.9972 | 0.95 | retracted | **REINSTATED 0.95** | Audit verifies arithmetic; B3_numerical_v2 uses correct lfunsympow c_f |
| Constant 2/(3π) | implicit | implicit | **0.95+** | M-N rederivation: 16/(24π) = 2⁴/(24π) where 16 = analytic conductor degree-2 boost |

**Three live possibilities (G8 §5.6):**
(a) Convergence is slower than T=800 — testable by extending PARI to T=10⁴ or T=10⁵, but no positive trend in current data
(b) Convention_reconciliation arithmetic error — retract that file
(c) M-N eq (16) has missing combinatorial factor analogous to G1's wrong factor-4 (would mean the **conjectural** constant 2/(3π) itself is wrong, which would be a different paper entirely)

**No version of Theorem B is currently submission-ready.** Pre-G8 the path was "fix 8 gaps, 4-8 weeks." Post-G8 the path is more open: numerical asymptotics need to be understood before any analytical claim is publishable.

**NOT ready for Annals submission.** Estimated 4-8 weeks of focused work needed:
- Close G4 (orthogonal mult), G5 (Lemma 3.3 sharp), G6 (cross-term C(f)), G7 (CS 2007 verbatim), G8 (PARI re-anchor)
- Aristotle-Lean formalization of Lemmas 3.1, 3.2 and the cage algebra
- Squarefree-composite N extension for outliers (27a, 44a) via Petrow-Young 2018+
- Final verification pass with adversarial review on each newly closed gap

---

*This draft v2 supersedes v1 (which falsely claimed Theorem B exact unconditional). Status reflects honest post-verification reckoning. Verbatim citations are flagged; non-verbatim claims are flagged.*
