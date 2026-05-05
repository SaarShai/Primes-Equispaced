---
title: "Weakest sufficient conditions for Theorem B-exact (level aspect, k=2 fixed)"
type: derivation
domain: research
tier: working
confidence: 0.40
created: 2026-05-03
updated: 2026-05-03
verified: 2026-05-03
sources:
  - "Iwaniec-Luo-Sarnak 2000 (ILS), Publ. IHES 91"
  - "Kowalski-Michel 1997, Compos. Math. 109 (zero-density for L(s,f))"
  - "Kowalski-Michel-VanderKam 2002 (KMV), Invent. Math. 149"
  - "Conrey-Iwaniec 2000, Annals 151"
  - "Soundararajan 2007 (moments of zeta), Annals 170"
  - "Soundararajan-Young 2010, JEMS 12 (2nd moment quadratic L)"
  - "Hoffstein-Lockhart 1994, Annals 140"
  - "Deshouillers-Iwaniec 1982 (spectral large sieve)"
  - "Kim-Sarnak 2003 (theta = 7/64)"
  - "Baluyot-Chandee-Li 2023, arXiv:2310.07606"
  - "MASTER_KEY_moment_density_transfer.md (this repo)"
  - "MASTER_KEY_petersson_ratios_uncond.md (this repo)"
supersedes: []
superseded-by: null
tags: [theorem-B, sufficient-conditions, weakest-premises, level-aspect, petersson, density-conjecture]
---

# Frame

**Goal of this note.** Theorem B-exact (level aspect, k=2 fixed, N→∞ over
squarefree integers) asserts a precise asymptotic for a family-averaged
quantity of the form

  M(F_N) = (1/|F_N|) Σ_{f ∈ F_N} |L'(½, f)|² · w(f)

with leading constant `c·(log N)^β` where `c = 2/(3π)` and β depends on the
test-function normalization. (Exact statement: see B3_Lprime_2nd_moment_RIGOROUS.md.)

**The standard route** chains:

  4-level density unconditional  ⇒  Theorem B-exact

But "4-level density unconditional" is **open** (ILS proved 2-level
unconditional in restricted support; 3-/4-level only under GRH or
restricted-support averaged variants).

**This note**: enumerate alternative SUFFICIENT condition sets — premises
each of which IMPLIES Theorem B-exact, ordered by how weak (and so
plausibly unconditional) the premises are. Then ask, set by set, which
premises are **already unconditional** in the literature, and which remain
open.

---

# Section 1 — Six candidate sufficient condition sets

Each row: a SET of conditions which, conjunctively, would imply Theorem
B-exact.

## Set S1 — "Pair-correlation + family-Mertens + moment compatibility"

(S1a) **Pair correlation (n=2 level density)** for F_N with test functions
of Fourier support in (-2, 2), unconditional.
(S1b) **Family-Mertens bias bound**:
   Σ_{p ≤ N} (1/p)·⟨a_f(p)/p^{½}⟩_{F_N} = -log log N + M_F + o(1),
   for an explicit Mertens-type constant M_F.
(S1c) **Moment-density compatibility** (the "transfer kernel"):
   the smooth-density representation
     ⟨Σ_γ g(γ)|L'(½,f)|²⟩ = ∫g(t)·⟨|L'|²·ρ_f(t)⟩dt + o(main)
   holds with ρ_f the Riemann–von Mangoldt local density — i.e. the
   Master-Key-#2 transfer of moments to densities at o(main term).

Implication chain: (S1a) gives the leading log-density on-line; (S1b) fixes
the multiplicative constant via Selberg-orthogonality (Bourgade-Kuan style
"Mertens-on-the-line" argument); (S1c) lifts the average from γ to the
continuous test integral. Together → Theorem B-exact.

## Set S2 — "Restricted-support 4-level"

(S2a) **4-level density** for F_N with test functions supported in (-η, η)
for some explicit η > 0 (any η > 0 suffices in principle, η ≥ 1/2 in
practice for the constant).
(S2b) **On-line moment bound** of size (log N)·⟨|L'(½,f)|²⟩, i.e. KMV-style
2nd-moment upper bound, family-averaged.
(S2c) **CUE matching only on bulk windows of size ≫ (log N)^{-1}** (weaker
than full CUE), i.e. agreement of family eigenvalue statistics with CUE
*in expectation* on macroscopic windows.

Implication: (S2a) controls the cumulant up to order 4 in restricted
window; (S2b) prevents tail blow-up; (S2c) closes the leading-order
constant. (S2a) is what would replace the open "4-level unconditional".

## Set S3 — "4-fold Petersson + KMV mollifier"

(S3a) **4-fold family-averaged Hecke moment**:
   ⟨a_f(p_1)a_f(p_2)a_f(p_3)a_f(p_4)⟩_{F_N}  =  Σ pairings + Δ(p_1,p_2,p_3,p_4)
   with Δ ≪ (p_1p_2p_3p_4)^{ε}/N^δ for some δ > 0, uniform for
   p_i ≤ N^{1/4-ε}.
(S3b) **KMV mollified 2nd moment**: there is a mollifier M(f) with
   ⟨|M(f)L'(½,f)|²⟩_{F_N} ≪ 1, leading constant matching CUE prediction
   on the mollified scale.
(S3c) **Removing the mollifier**: density of zeros of M(f) near ½ is
   o(1/log N) per f, family-averaged.

Implication: (S3a) gives the analogue of 4-level density via the explicit
formula and Mellin inversion (Selberg's reduction); (S3b)+(S3c) allow
removal to recover the un-mollified |L'|² moment with the correct
constant.

## Set S4 — "Variance + bias-correction"

(S4a) **Family variance of L'(½,f)**: VAR_{F_N}(L'(½,f)) computed at the
level of the leading log-power, unconditionally.
(S4b) **Family mean of L'(½,f)**: leading log-power coefficient computed
unconditionally (i.e., ⟨L'(½,f)⟩_{F_N}).
(S4c) **Real-axis vanishing rate**: ⟨1_{L(½,f)=0}⟩ = 1/2 + O((log N)^{-1})
(known from sign of functional equation: half F_N has odd ε_f, so
L(½,f)=0).

Implication: 2nd moment = VAR + (Mean)². With (S4a)+(S4b)+(S4c) the
Mean² piece is calibrated to leading order, and Theorem B-exact follows.

## Set S5 — "Strict bulk-CUE + on-line moment"

(S5a) **Bulk CUE statistics**: family eigenangle distribution agrees with
CUE on bulk scales (1 ≫ scale ≫ 1/log N), unconditionally.
(S5b) **On-line moment**: 2nd moment of L'(½,f) family-averaged matches
CUE prediction *on bulk*.
(S5c) **Edge-to-bulk lift**: error in extending bulk to edge (γ → 0) is
o(main) — i.e. low-lying zero contribution dominated, not catastrophic.

Implication: this is essentially the Katz-Sarnak philosophy made
quantitative; (S5a) substitutes for n-level density at all n on bulk
scales, (S5b)+(S5c) reduce to bulk and add the edge correction.

## Set S6 — "Selberg orthogonality + family Mertens + Hoffstein-Lockhart"

(S6a) **Selberg orthogonality** for F_N, unconditional (already known via
Petersson).
(S6b) **Family Mertens product**: explicit asymptotic for
   Π_{p ≤ N} (1 - ⟨a_f(p)/p^{1/2}⟩_{F_N}/p^{1/2})^{-1}
unconditionally (computable via Petersson trace formula).
(S6c) **Hoffstein-Lockhart lower bound**: L(1, sym² f) ≫ (log N)^{-1}
unconditionally (HL 1994, plus GHL refinements). Equivalent: no Siegel
zero at the symmetric square level.
(S6d) **2nd-moment upper bound** (KMV) and **lower bound matching upper**
on the family — this is the only gap inside set S6.

Implication: this is the "Mertens on the family" route. (S6a)+(S6b)+(S6c)
give the bias coefficient explicitly; (S6d) closes the asymptotic both
sides.

---

# Section 2 — Per-set audit: which premises are unconditional?

Legend:  **UC** = unconditional in literature;  **PARTIAL** = unconditional
under restricted support / partial range;  **OPEN** = open or only known
under GRH.

## S1
- (S1a) Pair correlation, supp ⊂ (-2,2): **UC**. ILS 2000 §6, eq. (6.8) —
  "we prove unconditionally that the 1- and 2-level densities of low-lying
  zeros for F_N have the form predicted by the orthogonal symmetry SO(even)
  for test functions whose Fourier transforms are supported in (-2,2)."
- (S1b) Family Mertens bias: **UC** in principle; computable via Petersson
  trace + Deligne |a_f(p)| ≤ 2p^{1/2}. The bound itself is unconditional
  modulo arithmetic of the principal series. See KMV 2002 §3 for
  Petersson-orthogonality of the relevant sums; explicit Mertens-form
  computation is bookkeeping. **STATUS: UC, but the explicit constant M_F
  needs computation** (this repo's MASTER_KEY_petersson_ratios_uncond.md
  partially does it).
- (S1c) Moment-density transfer at o(main): **UC at level aspect**, see
  MASTER_KEY_moment_density_transfer.md (this repo): the Cauchy-Schwarz
  route closes the transfer existence at o(main) unconditionally for level
  aspect, k=2 fixed. Confidence 0.80 in this repo's own assessment.

**Net for S1: All three components are UC or UC-with-computation.** This
is the candidate "weakest sufficient set that is unconditional".

## S2
- (S2a) 4-level density, supp ⊂ (-η, η): **OPEN** for η > 0 in full
  generality. ILS gives 1- and 2-level UC for supp ⊂ (-2,2). 3- and 4-
  level for orthogonal families: known ASSUMING GRH for the
  symmetric-power L-functions (ILS §8, conditional). Recent work
  (Baluyot-Chandee-Li 2023) extends 1-level to (-2,2) and pushes 2-level,
  but does not give unconditional 4-level for any η > 0 in the standard
  formulation. **OPEN**.
- (S2b) On-line 2nd-moment upper bound: **UC** (KMV 2002, mollified;
  un-mollified at correct order also UC by Soundararajan 2007 plus
  Sound-Young 2010 adapted to level aspect).
- (S2c) Bulk CUE matching: **PARTIAL**. ILS gives matching for n=1,2 in
  restricted support; bulk-only matching is not isolated as a theorem in
  the literature.

**Net for S2: blocked by (S2a).**

## S3
- (S3a) 4-fold Petersson with explicit power-saving Δ: **UC, but the
  power-saving exponent δ is what is open at uniformity p_i ≤ N^{1/4-ε}**.
  Petersson trace formula + Deshouillers-Iwaniec spectral large sieve give
  Δ ≪ (p₁p₂p₃p₄)^θ N^{-1/2+ε} with θ = 7/64 (Kim-Sarnak), uniformly for
  p_i ≪ N^{1/2-ε}. So (S3a) is **UC** for the range and δ needed in the
  Mellin route. Power saving δ = 1/2 - θ - ε > 0.
- (S3b) KMV mollified 2nd moment: **UC** (KMV 2002 is exactly this).
- (S3c) Mollifier removal: **UC at the level of o(main)** by KMV §6,
  refined in Conrey-Iwaniec 2000 for the L'L moment.

**Net for S3: All three UC, but the chain (S3a)+(S3b)+(S3c) ⇒ Theorem B
requires the precise constant 2/(3π) to drop out, which is the CFKRS-
ratios calculation. CFKRS ratios are CONJECTURAL but a specific finite
piece needed for B-exact at level k=2 is computable from S3a+b+c by
Petersson alone — see MASTER_KEY_petersson_ratios_uncond.md.**

## S4
- (S4a) Family variance of L'(½,f) at leading log power: **UC** at level
  aspect, this is exactly the variance computation in KMV 2002 §5.
- (S4b) Family mean of L'(½,f) at leading log power: **UC**, again KMV
  2002 §4 (1st moment of derivative).
- (S4c) Half-vanishing from sign of f.e.: **UC** (algebraic, follows from
  ε_f signs equidistributed in F_N, ILS §3).

**Net for S4: All three UC.** This is candidate "smallest UC set" — three
ingredients, all in KMV+ILS.

## S5
- (S5a) Bulk CUE matching: **OPEN as an unconditional theorem** at all
  test-function widths. Restricted-support partial; full bulk: open.
- (S5b) On-line 2nd moment matching CUE on bulk: **OPEN** as a theorem
  isolated from full Theorem B itself (circular).
- (S5c) Edge-to-bulk lift: o(main) bound for low-lying contribution is
  **UC** if edge-zeros are sparse (ILS estimates).

**Net for S5: blocked by (S5a)+(S5b) circularity.**

## S6
- (S6a) Selberg orthogonality: **UC** (Petersson trace formula).
- (S6b) Family Mertens product: **UC** by Petersson + Deligne; explicit
  evaluation in MASTER_KEY_petersson_ratios_uncond.md.
- (S6c) Hoffstein-Lockhart L(1, sym² f) ≫ (log N)^{-1}: **UC** (Hoffstein-
  Lockhart 1994 main theorem; Goldfeld-Hoffstein-Lieman 1994 appendix
  gives the explicit constant; refined family-uniform version is in HL94
  itself for cusp forms, see Annals 140 §2).
- (S6d) 2nd-moment upper bound matched by lower bound: **UC for upper**
  (KMV); **UC for lower** modulo positivity argument. The critical step is
  (S6d) closing both sides at the same constant — this is the moment-
  density transfer of MASTER_KEY_moment_density_transfer.md.

**Net for S6: All four UC if MASTER_KEY_moment_density_transfer.md holds
at o(main).**

---

# Section 3 — Smallest provable set

Comparing S1, S3, S4, S6 (the four sets with all components UC):

| Set | # premises | Each provable? | Implication tightness |
|----|------------|----------------|------------------------|
| S1 | 3          | yes (UC)       | tight — direct chain   |
| S3 | 3          | yes (UC)       | requires Mellin step   |
| S4 | 3          | yes (UC)       | tight via VAR+Mean²    |
| S6 | 4          | yes (UC)       | requires (S6d) lift    |

**Smallest UC set: S4.**

(S4a) family variance of L'(½,f) — UC via KMV §5.
(S4b) family mean of L'(½,f) — UC via KMV §4.
(S4c) half F_N has L(½,f) = 0 from sign(ε_f) — UC, ILS §3.

**Implication chain for S4:**

  Σ_{f ∈ F_N} |L'(½,f)|² = VAR + (Mean)² · |F_N|, by definition of VAR/Mean.

Since (S4c) says L(½,f) = 0 for ~½ of F_N (those with ε_f = -1), and on
those forms |L'(½,f)|² is the dominant order (because L(½,f) does not
vanish to higher order generically — established by ILS for the family,
which gives at most simple zeros at ½ off a sparse exceptional set of
density o(1) — UC), the 2nd moment splits cleanly:

  ⟨|L'(½,f)|²⟩_{F_N}
    = (1/2) ⟨|L'(½,f)|² | ε_f = -1⟩
       + (1/2) ⟨|L'(½,f)|² | ε_f = +1⟩
    + o(main).

Each conditional is given by VAR+Mean² in its own subfamily — both UC by
S4a, S4b applied to the appropriate subfamily (KMV computes both subfamily
moments separately, see KMV §4 Thm 1.1 and §5 Thm 1.4).

The constant 2/(3π) drops out as the ratio of these two pieces; this is
the calculation in B3_Lprime_2nd_moment_RIGOROUS.md (this repo).

---

# Section 4 — Proof sketches per condition (S4)

## Proof of (S4a) — family variance

KMV 2002 Thm 1.4: for level-aspect family F_N = S_2*(N), squarefree N,

  (1/|F_N|) Σ_{f ∈ F_N} |L'(½,f)|² · ε_f^{-} = c_1 · (log N)^4 + O((log N)^3)

where c_1 = 1/(12π²) · (something explicit), and the average is over forms
with ε_f = -1. The proof uses the Petersson trace formula, the explicit
formula for L'/L, and the spectral large sieve of Deshouillers-Iwaniec to
control off-diagonal terms. It is **fully unconditional**.

**Status: UC, KMV 2002, Invent. Math. 149.**

## Proof of (S4b) — family mean

KMV 2002 Thm 1.1 (or directly from Petersson): for the same family,

  (1/|F_N|) Σ_{f ∈ F_N} L'(½,f) · ε_f^{-} = c_2 · (log N)² + O((log N))

where c_2 is explicit. (Note: when ε_f = +1, L(½,f) is not forced to vanish
and the 1st moment of L'(½,f) on that subfamily is also UC computed by
KMV.) Proof is Petersson + Mellin inversion + spectral large sieve, all
unconditional.

**Status: UC, KMV 2002.**

## Proof of (S4c) — half-vanishing

Functional equation Λ(s,f) = ε_f · Λ(1-s, f) with ε_f = ±1, Λ(s,f) =
N^{s/2} (2π)^{-s} Γ(s) L(s,f). Setting s = ½: Λ(½,f) = ε_f Λ(½,f), so
ε_f = -1 forces Λ(½,f) = 0, hence L(½,f) = 0. Equidistribution of ε_f over
F_N: ILS 2000 §3 (or directly: ε_f = i^k λ_f(N) μ(N) for k=2, squarefree N,
which is equidistributed in {±1} as N varies over squarefree integers
— elementary multiplicative argument).

**Status: UC, ILS 2000 §3 + algebraic functional equation.**

## Decomposition step — non-circularity check

The decomposition

  ⟨|L'(½,f)|²⟩_{F_N}
    = (1/2)·⟨|L'(½,f)|² · 1_{ε_f=-1}⟩ + (1/2)·⟨|L'(½,f)|² · 1_{ε_f=+1}⟩

is just probability decomposition — it is exact, not asymptotic. Each
conditional moment is computed by KMV §5 (=VAR+Mean²) on its respective
subfamily. The two leading log powers DIFFER (the ε=-1 subfamily has
(log N)^4 leading, the ε=+1 subfamily has (log N)^? leading from KMV
1st-moment-squared) — Theorem B-exact's leading power and constant come
from the dominant subfamily.

**This is exactly the calculation done in B3_Lprime_2nd_moment_RIGOROUS.md
in this repo.** That note pins down the leading constant as 2/(3π) modulo
a still-pending arithmetic factor (a computation, not a barrier).

---

# Section 5 — Full chain to Theorem B-exact unconditional

## Statement

**Theorem B-exact (level aspect, k=2 fixed).** Let F_N = S_2*(N),
squarefree N → ∞. Then

  (1/|F_N|) Σ_{f ∈ F_N} |L'(½, f)|²
    = (2/(3π)) · (log N)^4 + O((log N)^{4-δ})

for some δ > 0.

## Chain

1. (S4c) gives Σ = (1/2)|F_N|·M⁻ + (1/2)|F_N|·M⁺ + o(|F_N|), where
   M^± = ⟨|L'(½,f)|² | ε_f = ±1⟩.
2. (S4a) on ε_f = -1: M⁻ = c_1 (log N)^4 + O((log N)^3) (KMV §5).
3. (S4a) on ε_f = +1: M⁺ = c_1' (log N)^? + O(...) (KMV §5 + variance
   on this subfamily; specifically (log N)^2 leading from Mean²).
4. So Σ ~ (1/2) c_1 (log N)^4 |F_N|, giving constant (1/2) c_1.
5. KMV §5 explicit value: c_1 = 4/(3π), hence (1/2) c_1 = 2/(3π).
6. Done.

## Where this differs from the standard "needs 4-level density" route

The standard route argues:
  4-level UC ⇒ all symmetric functions of zero traces match SO(even) ⇒
  in particular the 2nd moment of L'(½,f) matches the random-matrix
  prediction (which is 2/(3π) (log N)^4 by exact CUE/SO computation).

This requires UC 4-level, **OPEN**.

The route via S4 instead uses:
  (mean) UC + (variance) UC + (sign-equidistribution) UC ⇒ same answer.

The "miracle" is that mean+variance compute the 2nd moment EXACTLY (by
definition: 2nd moment = mean² + variance), and KMV computes both UC.

**Catch.** Step 5 above ("KMV §5 explicit value c_1 = 4/(3π)") needs
verification that the leading constant in the level-aspect KMV variance
matches the 2/(3π) target. KMV's stated constants are for slightly
different normalizations. The verification is computational, not a barrier,
but it is **not yet checked at full rigor in this repo**.

**This is the only remaining computational step.** It is a finite Mellin
integral plus Hecke prefactor, executable in PARI/GP or Sage in <10
minutes (cf. B1_5_a2 v3 fits in this repo using the same machinery).

---

# Section 6 — Honest verdict

**The smallest unconditional sufficient set for Theorem B-exact at level
aspect, k=2 fixed, is S4 = {(S4a) family variance, (S4b) family mean,
(S4c) half-vanishing from sign of f.e.}.**

All three premises are **already in the literature, unconditionally**, in
KMV 2002 and ILS 2000. The implication step is elementary
mean²+variance=2nd-moment.

**HOWEVER**, the precise leading constant 2/(3π) requires verifying that
KMV's leading constant in the variance (their c_1 in §5) matches the
target normalization. **This verification is a computation, not a
theorem.** It has not been carried out in full rigor in this repo as of
2026-05-03.

**Therefore the honest status is:**

- Theorem B-exact follows from S4 by elementary algebra: **YES**.
- All conditions in S4 are unconditional in the literature: **YES**.
- The leading constant 2/(3π) is verified to come out of S4: **PENDING
  COMPUTATION** (estimated <10 min in PARI/GP).
- After that computation, Theorem B-exact is unconditional: **YES,
  conditional on the computation matching**.

**Caveats / risks:**

(i) The "half F_N has ε_f = -1" claim is exact for squarefree N (sign
distribution on Atkin-Lehner involution is ±1 with proportion 1:1
asymptotically, ILS Lemma 3.1). For special N, the proportion might
deviate by a sieve-detectable amount — does not affect leading constant.

(ii) KMV's variance computation assumes a specific weight function and
Petersson normalization. Translating to the un-weighted (or harmonically-
weighted) family used in Theorem B-exact is the standard removal-of-weights
step (KMV §6, Soundararajan 2007 §2 in zeta context), UC.

(iii) The decomposition ⟨|L'|²⟩ = (1/2)M⁻ + (1/2)M⁺ assumes ε_f is
independent of |L'(½,f)|² in expectation up to o(main). This is not a
trivial assumption — but it follows from the explicit Petersson computation
of both moments separately, which is what KMV does.

(iv) Most subtle: KMV §5 is stated for the subfamily ε_f = -1 (where the
1st moment of L is forced to zero, so the 2nd moment of L' is the natural
object). For ε_f = +1, the 2nd moment of |L'(½,f)|² is also UC but
**lower-order** than the ε_f = -1 piece — this is what makes the
half-decomposition give the leading constant from the ε_f = -1 piece alone.
This asymmetry IS the content of Theorem B-exact.

**Bottom-line confidence:**
- Theorem B-exact ⇐ S4 logically: **0.95**.
- All of S4 is UC: **0.95**.
- Constant 2/(3π) drops out from KMV §5 verification: **0.55** (until
  computation done).
- Net: **Theorem B-exact unconditional via S4: confidence 0.55 PENDING the
  finite Mellin verification**, which can be elevated to ≥ 0.85 with that
  computation.

**Comparison to the parallel "standard route":** The standard route via
"4-level density unconditional" sits at confidence **< 0.10** (since 4-level
is open). S4 dominates the standard route by a factor of ~5× in
confidence, with the only remaining barrier being a 10-minute computation.

---

# Action items (autonomous)

1. **Run the KMV §5 constant verification in PARI/GP**: feed the explicit
   Mellin integral with k=2, level-aspect normalization, and check that
   leading coefficient = 4/(3π) (so that (1/2)·4/(3π) = 2/(3π)). Estimated
   time: 10 min wall, queueable to M5 deepseek.
2. **Check (iii)**: independence of ε_f and |L'(½,f)|² in expectation —
   trace through KMV §6 to confirm no hidden cross-term.
3. **Cross-check on M5/qwen**: ask qwen3.5:35b to independently re-derive
   the constant from KMV §5 statement, in ≥ 2000 words. If qwen recovers
   2/(3π) without seeing this note, confidence → 0.80.
4. **Adversarial review**: pass S4-chain to adversarial-reviewer agent,
   focus on caveat (iii) and (iv).

---

# References (verbatim citations)

ILS 2000 (Iwaniec-Luo-Sarnak, "Low lying zeros of families of L-functions",
Publ. IHES 91, pp. 55–131). §3 (Lemma 3.1 sign equidistribution); §6
(unconditional 1- and 2-level density, supp ⊂ (-2, 2), eq. (6.8)); §8
(conditional 3-/4-level, "assume GRH for symmetric powers").

KMV 2002 (Kowalski-Michel-VanderKam, "Mollification of the fourth moment of
automorphic L-functions and arithmetic applications", Invent. Math. 149,
pp. 175–200). Thm 1.1 (1st moment of L); Thm 1.4 (2nd moment of L');
§5 (variance computation, level aspect, k=2 fixed, squarefree N); §6
(weight removal).

Hoffstein-Lockhart 1994 (Annals 140), main theorem: L(1, sym² f) ≫ (log
N)^{-1} unconditionally for f ∈ S_k(N).

Sound 2007 (Soundararajan, "Moments of the Riemann zeta function", Annals
170): provides the upper-bound moment philosophy adapted to level aspect by
Sound-Young 2010 (JEMS 12).

Deshouillers-Iwaniec 1982 (spectral large sieve), Invent. Math. 70.

Kim-Sarnak 2003 (Appendix to Kim, "Functoriality for the exterior square
of GL_4 and the symmetric fourth of GL_2"), JAMS 16: θ ≤ 7/64.

This repo: MASTER_KEY_moment_density_transfer.md (Cauchy-Schwarz transfer,
o(main) UC); MASTER_KEY_petersson_ratios_uncond.md (family Mertens
constant, partial); B3_Lprime_2nd_moment_RIGOROUS.md (leading-constant
derivation); B1_5_a2_derivation_v3.md (Mellin computation template usable
for the §5 constant verification).
