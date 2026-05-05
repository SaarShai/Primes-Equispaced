---
title: "Theorem B (Petersson family weight aspect) — proof verification"
type: audit
domain: research
tier: working
confidence: 0.42
created: 2026-05-03
updated: 2026-05-03
verified: 2026-05-03
auditor: Opus 4.7 extra-high (verification pass, ≤30 min budget)
sources_audited:
  - B3_unconditional_attempt.md
  - B3_polar_mellin_factor_4_v2.md (claims conf 0.95)
  - B3_polar_mellin_factor_4_RIGOROUS.md (predecessor, conf 0.82)
  - B3_lemma_3_1_fixed.md
  - B3_lemma_3_2_fixed.md
  - B3_lemma_3_3_fixed.md
  - B3_section_3_4_fixed.md
  - B3_Lprime_2nd_moment_RIGOROUS.md
  - B3_CS_7_32_FROM_SCRATCH.md
  - Convention_reconciliation.md
  - B_prime_numerator_PROOF.md
  - B3_pari_higher_k_results.md
  - /tmp/milinovich_ng.txt (M-N 2014, full PDF text)
  - /tmp/dfs.txt (DFS — Deshouillers-Iwaniec)
  - /tmp/ils.txt (ILS 2000)
tags: [theorem-B, audit, verification, petersson, weight-aspect]
---

# Section 1. Theorem statement (claimed)

For F_k = S_k*(N), N squarefree fixed, k → ∞ with k = T^a (1 < a < 2):

  M_{F_k}(T) := ⟨ Σ_{0<γ_f≤T} |L'(½+iγ_f, f)|² ⟩_{F_k}
              = (2/(3π)) · ⟨c_f⟩_{F_k} · T · log⁴(NkT) · (1 + o(1))

unconditionally, where c_f = L(1, sym²f)/ζ(2).

(Note: the proof files freely move between writing the moment with `1+iγ_f`
and `½+iγ_f`. The arithmetic-normalisation critical line is Re s = ½ in
M-N 2014; the at-edge L'(1+it,f) used in Lemma 3.1 is in a different
normalisation. This dual-convention slippage is one of the verification
issues — see §5.)

# Section 2. Proof outline as it appears in the files

The proof is assembled from these claimed pieces:

1. **Stieltjes split.** Σ_γ |L'|² = ∫|L'|²·dN_f = ∫|L'|²·⟨dN_f/dt⟩dt
   + ∫|L'|² dS_f =: Smooth_f + Fluct_f.

2. **Lemma 3.1 (on-line 2nd moment).**
   ⟨∫₀^T |L'(1+it,f)|² dt⟩_{F_k} = (T/3)·⟨c_f⟩·log³(NkT)·(1+o(1)),
   the constant **A=1/3** sourced from the elementary identity
   Σ_{n≤X}(log n)²/n ~ (1/3)log³X (Stieltjes constants).
   Off-diagonal Petersson killed by Bessel decay J_{k-1}((4π√mn)/c) for
   k > 4eT/√N.

3. **GL₂ Riemann-von Mangoldt density.** ⟨dN_f/dt⟩ = (1/π)·log(NkT)
   (Iwaniec-Kowalski Eq. 5.7; degree d=2 Riemann-von Mangoldt).

4. **Smooth term assembly.** Smooth = (T/(3π))·⟨c_f⟩·log⁴(NkT).

5. **Pair-correlation enhancement.** Claim: pair-correlation contribution
   = m_O · Smooth where m_O = 1 (orthogonal Plancherel multiplicity vs
   m_U = 3 for unitary ζ analog). Derived from Hecke convolution +
   Sato-Tate orthogonality (B3_CS_7_32_FROM_SCRATCH §§3-5).

6. **Total.** Smooth + PairCorr = 2 · (T/(3π))·⟨c_f⟩·log⁴ = (2/(3π))·…

7. **Fluctuating-term Cauchy-Schwarz control** (Lemmas 3.2 + 3.3).
   ⟨S_f²⟩ ≪ log log(kT) (Selberg/Goldston-Gonek + Bessel diag); 4th moment
   on derivatives ≪ T·(log NkT)^{≤16}. Yields Fluct = o(main) via C-S.

# Section 3. Verbatim quotes from cited references

## Milinovich-Ng 2014 (arXiv:1306.0854) — direct extraction

**Theorem 1.2 (M-N), full statement [verbatim from PDF text /tmp/milinovich_ng.txt]:**

> Let f ∈ H_k(q,χ) and assume the generalized Riemann hypothesis for
> L(s,f). Then [...]
>   (A_f + o(1)) T log⁴(√q T/(2π)) ≤ Σ_{0<γ_f≤T} |L'(ρ_f,f)|²
>                              ≤ (B_f + o(1)) T log⁴(√q T/(2π))
> where A_f = ((17 − √145)/(12π)) c_f and B_f = ((17 + √145)/(12π)) c_f.
> c_f = (4π)^k · ‖f‖² / (Γ(k) · vol(Γ₀(q)\h)).

**Conjecture (M-N, eq. (16)) [verbatim]:**

> Σ_{0<γ_f≤T} |L'(ρ_f,f)|² = (2/(3π)) · c_f · T · log⁴ X + O(T·log³ X)
> [...] we expect that some substantially new ideas are necessary in order
> to establish the above conjecture.

**Findings:**
- (a) M-N Theorem 1.2 is **conditional on GRH** (stated explicitly).
- (b) The cage [(17±√145)/(12π)] is per-form, not family-averaged.
- (c) The constant 2/(3π) is a **conjecture** in M-N, not a theorem;
      M-N call it "comparable to" Gonek's analogous ζ-result and state
      "substantially new ideas are necessary."
- (d) M-N's c_f differs from c_f := L(1,sym²f)/ζ(2) used throughout the
      proof files; M-N use c_f = (4π)^k‖f‖²/(Γ(k)vol(Γ₀(q)\h)). These two
      conventions are PROPORTIONAL (the Iwaniec-Kowalski conversion
      L(1,sym²f) = const·(4π)^k‖f‖²/Γ(k)·…) but the proportionality
      constant matters at leading order. The proof files do not pin
      this conversion; B3_pari_higher_k_results.md §"Verdict" explicitly
      flags "whether the c_f convention divides by ζ(2)" as OPEN.

## Gonek (cited inside M-N) — ζ' baseline

M-N quote (verbatim from /tmp/milinovich_ng.txt):

>  Σ_{0<Im ρ ≤ T} |ζ'(ρ)|² = (T/(24π)) log⁴ T + O(T log³ T)
>  assuming RH.

**Finding:** The ζ' baseline is **T/(24π)·log⁴T = 1/(24π)·T·log⁴T**.

## Conrey-Snaith 2007 §7 Eq. (7.32) — orthogonal kernel

NOT extracted in available /tmp files (only the longer CFKRS 2005 PDF is
present, /tmp/cfkrs.pdf, which is a DIFFERENT paper — "Integral moments
of L-functions"). The proof files repeatedly cite "CS 2007 §7 Theorem 7.3,
Eq. (7.31)–(7.32)" as a black box for the orthogonal symmetry kernel
evaluation = 2/(3π). **NOT independently verified in this audit.**

## ILS 2000 (Iwaniec-Luo-Sarnak)

/tmp/ils.txt confirms the existence of Theorem 1.1 (1-level density,
Petersson family) and §6 Kloosterman bounds. The proof files cite ILS
correctly in shape; ILS does NOT contain a 2/(3π) family-averaged
asymptotic for Σ|L'|² — it gives 1-level density, not at-zero
derivative moments.

# Section 4. Numerical verification

## 4.1 Internal identity Σ(log n)²/n ~ (1/3)log³X

Independently re-verified at dps=30 via mpmath:

```
X=   100: ratio sum/(1/3 log³X) = 1.002956
X= 1,000: ratio                   = 1.000129
X=10,000: ratio                   = 0.999979  ← matches the file's claim
X=100,000: ratio                  = 0.999982
```

**STATUS: VERIFIED.** This is just an elementary Stieltjes-constants
identity; no L-function content. It does establish **A=1/3** in the
schema A·⟨c_f⟩·T·log³X, IF the surrounding argument (Petersson diagonal
+ Rankin-Selberg residue conversion + smooth Mellin) is rigorous.

## 4.2 Cage values

Re-verified:
- (17 − √145)/(12π) = 0.13153
- 17/(12π)         = 0.45094
- (17 + √145)/(12π) = 0.77035
- 2/(3π)           = 0.21221

The conjectural target sits in the **lower 25% of the cage**, much closer
to the lower edge than the center. The "naive symmetric CLT" cannot move
the family mean from center to target — flagged correctly in
B3_unconditional_attempt §2.

## 4.3 ζ' BASELINE — DISCREPANCY

Proof file `B3_polar_mellin_factor_4_v2.md` line 47 and table line 178
states:

> "ζ at-zeros (Conrey 1989) = 1/(6π) baseline"
> "Ratio (GL₂/ζ) = (2/(3π)) / (1/(6π)) = 4"

But verbatim M-N quote of Gonek's RH-conditional result is **1/(24π)·T·log⁴T**.

  1/(24π) = 0.013263
  1/(6π)  = 0.053052    [proof file claim]
  ratio   = 4

**The proof file's "Conrey 1989" baseline 1/(6π) is OFF BY A FACTOR OF 4
from the actual Gonek 1989 / Conrey-Ghosh-Gonek result quoted in M-N.**

This silently inflates the "factor 4 = 2_density × 2_multiplicity"
decomposition by exactly 4. The actual ratio (2/(3π)) / (1/(24π)) = **16**,
not 4.

If the "factor of 4" in the proof files is wrong, then the chain
"density ×2, multiplicity ×2 → ×4 over ζ" is internally inconsistent:
two factors of 2 cannot give a factor of 16 unless there is an additional
unmodeled factor of 4 somewhere.

This is precisely the "off-by-O(1) constant gap" the parent file
`B3_unconditional_attempt §3.7` candidly flags (lines 247–264), and the
v2 polar-Mellin file claims to have "resolved" it via the
density-×-multiplicity decomposition. **The decomposition does not match
the actual literature ζ baseline.** The proof files have the wrong target
to compare against.

## 4.4 PARI numerical, higher k (B3_pari_higher_k_results.md)

The own-project PARI run at k=12, k=24 produces:

| Case | u_norm(log T)⁴ | target 2/(3π) | ratio |
|------|----------------|----------------|-------|
| Δ (k=12, T=49) | 0.0417 | 0.2122 | 0.20 |
| level 37 wt 24 orbit 1 | 0.1627 | 0.2122 | 0.77 |
| level 37 wt 24 orbit 2 | 0.1105 | 0.2122 | 0.52 |

After ad-hoc post-multiplication by ζ(2)=π²/6 to "correct the c_f
convention":

| Case | u·ζ(2) | target | ratio |
|------|---------|---------|-------|
| Δ | 0.069 | 0.212 | 0.32 |
| orbit 1 | 0.268 | 0.212 | 1.26 |
| orbit 2 | 0.182 | 0.212 | 0.86 |

**The PARI numerics do NOT confirm 2/(3π) at any single set of conventions.**
The own author of the file writes: "neither orbit lands within 20% of the
target on any single (cf, log) convention." The proof files cite the
"16-curve mean ratio 0.9972" as the empirical anchor, but
`Convention_reconciliation.md` reveals this ratio is between **two
compute pipelines** (their `R_derived/R_wrap`), NOT agreement with 2/(3π).
Per-curve `R_finite` in that file ranges 0.84 → 2.20 — i.e., factor of 2.6
spread around the asymptotic.

## 4.5 Σ_p sin²(t log p)/p ↔ (1/(2π²)) log log

Independently verified the file's claim: at t=50, P=10⁵, ratio = 0.996.
**STATUS: VERIFIED.** This supports Lemma 3.2's revised bound
⟨S_f²⟩ ≪ log log(kT).

# Section 5. Honest gaps and weak links

## (G1) The 1/(6π) ζ baseline is wrong by a factor of 4

The "factor 4 = 2_density × 2_multiplicity" decomposition in
`B3_polar_mellin_factor_4_v2.md` (claimed conf 0.95) compares the GL₂
target 2/(3π) to a baseline 1/(6π) attributed to "Conrey 1989" / "ζ
at-zeros". Verbatim M-N 2014 quotes Gonek's actual ζ'-baseline as
**1/(24π)** under RH. The actual ratio is 16, not 4. The proof file's
decomposition is **internally inconsistent with the literature it cites**.

This invalidates the §5 "clean accounting" table (lines 178–198 of v2),
and the "2_multiplicity = (1+m_O) = 2" identification — because the
identification was done by FORCING the answer to come out to 4 over a
wrong baseline.

**Confidence drop: −0.20.** This is the single largest gap.

## (G2) M-N is conditional on GRH; "unconditional" claim depends on
  bypassing this

M-N's Theorem 1.2 cage [(17±√145)/(12π)] is **GRH-conditional**, stated
verbatim. The proof files claim the *family-averaged weight-aspect*
analog is unconditional via Bessel decay killing off-diagonal. This is
plausible for the **off-diagonal in the Petersson trace** (Bessel decay
J_{k-1} ≪ (ex/(2k))^{k-1} is genuinely unconditional). But M-N's GRH
hypothesis enters in ways NOT just at the off-diagonal Petersson level —
specifically:
- (a) The explicit formula relating Σ|L'(ρ)|² to integrals of |L'|² along
      σ=½ requires control of zero-locations off the line, traditionally
      via GRH.
- (b) The cage-discriminant Cauchy-Schwarz inequality (M-N §§3-4) uses
      RHf to write zeros as ½+iγ_f, not on more general vertical lines.

The proof files (e.g. B3_unconditional_attempt §3.4) claim "k → ∞ Plancherel
suppresses 2-level pair correlation defects unconditionally." This is the
Iwaniec-Sarnak 2000 §7 Plancherel-Sato-Tate result, which IS unconditional
in weight aspect. But mapping this to the M-N second-moment problem
*without* a GRH-equivalent for the f's involves the unproven step
**(P)**: "Stieltjes integration on Re s = ½ vs Re s = 1 commutes with
family averaging modulo Bessel-decay error".

This step P is where the proof files' "polar correction factor of 4"
(file `B3_lemma_3_1_fixed.md §8`) is described as **"Sketched in §8;
needs line-by-line derivation through the Mellin transform of Σ_γ x^{iγ_f}
including conjugate pole pairs"** with confidence 0.5.

**Confidence drop: −0.15.**

## (G3) The convention-reconciliation 0.9972 mean ratio is between two
  pipelines, not agreement with 2/(3π)

The headline "16-curve mean ratio 0.9972, max 2.0%" in
Convention_reconciliation.md compares pari `u_f^pari` to wrap `R_finite`
through the identity `u_f^pari · c_f^pari = R_finite · (2/(3π)) ·
c_f^wrap`. They agree because both are computing the SAME observable; the
ratio is essentially a check that two scripts agree on
Σ|L'(ρ)|²/(c_f T Y⁴), nothing more.

The file's own §7 admits: "Median pari u_f = 0.226; conjectural a_4
= 0.212; Ratio 1.07" and "Median wrap R_finite = 1.665, i.e. M_obs is on
average 67% above asymptotic." The 67% over-shoot is attributed to
"sub-leading a₃/Y lift" — but this LIFT IS RATIOS-CONJECTURE-CONDITIONAL
(file §8 admits: "a_3 lift correction is itself ratios-conjecture-
conditional").

So the empirical "anchor" is: under a ratios-conjectural lift correction,
residuals fit `a_4 = 2/(3π)` with R²=0.97 and MAE=0.10 over 16 curves —
and this is on rank-0 elliptic curves at *small* T (~10² zeros), not in
the weight-aspect k → ∞ regime of Theorem B.

**Confidence drop: −0.05** (the empirical evidence is broadly consistent
with 2/(3π) but does not lock it).

## (G4) Constant-2 multiplicity from Hecke convolution: not airtight

`B3_CS_7_32_FROM_SCRATCH.md §4` derives "orthogonal multiplicity m_O = 1"
from Hecke (4a)+(4b) + Sato-Tate ⟨λ_f(p)²⟩=1. The file admits:
"the explicit log-counting in §5–6 (~1 page, mechanical) is not done in
this pass". Without that log-counting, §5's "outer Plancherel cyclic
factor 3" giving the 1/3 Mellin integral is asserted without derivation.

The "ratio (1+m_U)/(1+m_O) = 4/2 = 2" is then the **second** factor of 2
in the v2 decomposition. As (G1) shows, the underlying baseline is wrong,
so the overall decomposition does not in fact reproduce the M-N literature
target.

**Confidence drop: −0.10.**

## (G5) Lemma 3.3 has unverified log-power exponent

`B3_lemma_3_3_fixed.md` states the file's audit: "I gave 16 as a safe
upper bound; sharp is 8–14, but for the application any A < ∞ suffices."
This is acceptable for the *qualitative* o(main) Cauchy-Schwarz step, but
the file quotes BPRZ 2017 / KMV 2002 then admits "I have not located a
single citation that does derivative-AFE on the 1-line for GL_2 newforms
with explicit polynomial degree."

So Lemma 3.3 is a synthesis with no single load-bearing citation. For an
**Annals submission**, this is unacceptable as currently written. Fixable
in 1–2 weeks of careful AFE bookkeeping.

**Confidence drop: −0.05.**

## (G6) Cross-term and AFE-dual handling sketched, not done

`B3_Lprime_2nd_moment_RIGOROUS.md §5` bounds the AFE cross-term C(f) by
"O(T·log²c) by van der Corput" without writing out the stationary-phase
estimate. The file calls this caveat (C1).

`B_prime_numerator_PROOF.md §4` numerical sanity at small N shows
ratio LHS/RHS rising from 0.038 (N=23) toward 1 at N=127 (ratio 0.36) —
a 25× error at small N. The file acknowledges: "Numerical sanity is
order-of-magnitude only, not 5% precision." This is fine for a separate
result (B-prime numerator) but indicates the 2-shift Petersson identity
underlying the moment computation is itself unverified at the 5% level
in any regime accessible to direct PARI.

**Confidence drop: −0.05.**

## (G7) Citation for "CS 2007 Eq. (7.32)" is a black box

The proof files repeatedly invoke CS 2007 §7 Thm 7.3, Eq. (7.32) as the
algebraic source of 2/(3π). This paper was NOT extracted/verified in the
available /tmp files. Without verifying that CS 2007 actually evaluates
the relevant orthogonal kernel integral to 2/(3π) for the Petersson
weight aspect, the constant 2/(3π) — even if everything else is rigorous
— rests on an uninspected citation.

**Confidence drop: −0.05.** (Partial; CS 2007 is a real reputable paper
and likely contains the claimed identity, but verification was not done.)

# Section 6. Final unconditional confidence

Aggregation rule: starting from the highest claimed file confidence
(0.95, B3_polar_mellin_factor_4_v2.md), apply each confidence drop
multiplicatively in log-odds (each "−0.X" subtracted from the surviving
probability):

  start                      0.95
  − G1 (wrong ζ baseline)    0.75
  − G2 (GRH bypass not airtight)  0.60
  − G3 (anchor not in regime)     0.55
  − G4 (multiplicity not airtight) 0.45
  − G5 (Lemma 3.3 imprecise)      0.40
  − G6 (cross-term sketched)      0.35
  − G7 (CS 2007 unverified)       0.30 ?

But (G7) is partial since CS 2007 likely contains the result. Recombine:

**Aggregate unconditional confidence: 0.40 ± 0.05.**

This is *substantially below* the file-claimed confidences:
- B3_polar_mellin_factor_4_v2.md: 0.95
- B3_CS_7_32_FROM_SCRATCH.md: 0.92
- B3_Lprime_2nd_moment_RIGOROUS.md: 0.86
- B3_unconditional_attempt.md: 0.62
- Convention_reconciliation.md: 0.97 (only for the pipeline-identity
  claim, which IS solid; not for 2/(3π) itself)

The lowest of these (0.62 in the parent file) is closer to the audit
verdict (0.40). The successive "rigorous" files raised the confidence by
adding mechanical sub-derivations that did not address the underlying
load-bearing gaps (especially G1, G2).

# Section 7. Recommendation

## Annals submission readiness: **NO**.

What the proof currently is: A coherent, well-organised heuristic
argument that the **family-averaged weight-aspect M-N second moment of
L' at zeros is plausibly (2/(3π))·c_f·T·log⁴(NkT)·(1+o(1))**, with
several individual lemmas (3.1, 3.2, 3.4) derived rigorously, and the
core obstruction localised to: (a) the orthogonal symmetry kernel
evaluation = 2/(3π), and (b) the Stieltjes/Mellin "polar factor 4"
reconciliation.

What is missing for Annals:
1. **Fix the ζ baseline.** The "1/(6π) Conrey 1989" baseline used in the
   factor-4 decomposition is wrong (actual is Gonek's 1/(24π)). Either
   provide the correct citation for 1/(6π) (and explain how it differs
   from Gonek), or redo the decomposition with the correct 1/(24π)
   baseline.
2. **Verify CS 2007 Eq. (7.32).** Get the PDF, quote the orthogonal
   kernel integral, confirm it evaluates to 2/(3π) for the M-N test
   function class.
3. **Pin the c_f convention.** The proof files variously use c_f =
   L(1,sym²f)/ζ(2), c_f = L(1,sym²f), and M-N's
   c_f = (4π)^k‖f‖²/(Γ(k)·vol). Single convention, conversion lemma,
   numerical re-test under that convention.
4. **Lemma 3.3 sharp exponent.** Replace "≤16" with the actual sharp
   bound; provide AFE-derivative citation or full self-contained proof.
5. **Polar/Mellin factor 4** — do the line-by-line Mellin transform of
   Σ_γ x^{iγ_f} including conjugate pole pairs, as the file itself flags
   (B3_lemma_3_1_fixed §8, conf 0.5).
6. **Bypass GRH explicitly.** Prove that the substitution of the
   Stieltjes integral on σ=1 (Lemma 3.1) for the at-zeros sum
   (M-N target) commutes with family-averaging without GRH —
   currently a sketch in §3.7 / §8.
7. **Numerical re-anchor.** Run higher-T/k PARI numerics (say k=24,
   T=200, or k=40, T=100) under FIXED (c_f, log) convention and
   confirm convergence toward 0.21221 to better than 5%.

Items (1)–(3) and (6) are 1–2 weeks each; (4) is similar; (5) and (7)
are 1–2 days. **Total: ~2 months of focused work** to bring the proof
to Annals submission quality from current state.

## Plausibility verdict

The PROOF DIRECTION is plausible and several individual lemmas are real.
The constant 2/(3π) is consistent with M-N's conjecture and with the CS
2007 ratios prediction. The Bessel-decay route IS the right approach in
the weight aspect.

However, the *current* writeup contains a load-bearing arithmetic error
in the ζ-baseline comparison (G1), an unverified citation chain through
CS 2007 (G7), and an unfilled "polar factor 4" gap (G5/G6) — all of which
the project files internally flag at lower confidence than the headline
0.95 number. The headline 0.95 is unjustified; aggregate honest
confidence is **~0.40**.

**Status: Promising research-grade derivation; not a closed proof.**
**Not ready for Annals submission as currently written.**
**The author's own most-honest file (B3_unconditional_attempt §9.5,
"Confidence: 0.62") is the most accurate self-assessment in the file
collection.**

# Done.
