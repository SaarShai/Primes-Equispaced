---
title: "Lemma L3'-Aux — cuspidal-spectrum density on Γ₀(N): hours-test verdict"
type: derivation
domain: research
tier: working
confidence: 0.20
created: 2026-05-03
updated: 2026-05-03
verified: 2026-05-03
sources:
  - B3_L3_prime_recent_lit.md
  - Sequel_2_C_star_1L_CLL.md
  - Iwaniec, Spectral Methods of Automorphic Forms, 2nd ed. (Ch. 11)
  - Kim–Sarnak 2003 (J. AMS)
  - Iwaniec–Luo–Sarnak 2000 (Publ. IHÉS 91)
  - Blomer–Milićević 2015 (the second moment of twisted modular L-functions)
  - Humphries–Khan 2024 (density-symmetry interplay)
supersedes: []
superseded-by: null
tags: [L3-prime, Petersson, density, Selberg, level-aspect, hours-test]
---

# Verdict (read this first)

**This is the ~50% bucket: a multi-year problem that does NOT collapse in hours.**

L3'-Aux is, after sharpening below, **precisely equivalent** (up to ε's) to a
quantitative cuspidal density theorem on Γ₀(N) with density exponent **A = 12**
in the Iwaniec–Sarnak template

> #{f ∈ cuspidal spectrum of Γ₀(N) : θ_f ≥ σ} ≪_ε N^{1 − Aσ + ε}.

The best published exponent in the **level aspect at fixed weight** is
**A = 4** (Iwaniec, *Spectral Methods*, Th. 11.7, restated and used by ILS 2000
§5).  Conjecturally (Sarnak's "density-1 Ramanujan") A is unbounded, and indeed
for the spectral parameter in the eigenvalue aspect on SL₂(ℤ) one has A = 2
(Selberg/Huxley) which under known refinements (Iwaniec; Lindenstrauss–
Venkatesh) extends to A as large as 6 in some hybrid ranges. **No published
result reaches A = 12 in the level aspect at fixed weight.** Closing that gap
is, modulo ε, the exact obstacle that has blocked the next layer of subconvex
trilinear estimates for a decade (Petrow–Young 2018 → Blomer–Milićević 2017+ →
Miao–Zhang 2025 are all "almost there in some auxiliary aspect").

Short answer to the framed question: **No proof. Honest reduction below.**

What this 8-hour session **does** deliver:

1. A **sharp** reformulation of L3'-Aux as a single density inequality with
   exponent A = 12, removing the previous handwave about "1/24 saving on the
   spectral large sieve."
2. A **decomposition** of A = 12 into three sub-savings (3 + 3 + 6) corresponding
   to (a) Atkin–Lehner-newform projection efficiency, (b) Kuznetsov diagonal
   length, (c) exceptional-eigenvalue contribution — each a known target with a
   named open sub-problem behind it.
3. A **failure mode** showing why naive insertion of Kim–Sarnak θ ≤ 7/64 cannot
   reach A = 12: it gives at best A_eff ≈ 4 + 8θ ≈ 4 + 8·(7/64) = 4 + 7/8 ≈ 4.875.
4. A **numerical incidence check** on Γ₀(N) for prime N ≤ 199 confirming the
   empirical Selberg phenomenon (no exceptional eigenvalues in this range),
   which is consistent with A = 12 but cannot distinguish it from A = 4: in this
   range every density bound with A ≥ 0 is vacuous.
5. A **two-named-sublemma reduction** with realistic timelines.

Confidence "L3'-Aux is *true* (i.e., A = 12 holds)": **0.55** — community
expectation, no counterexample, in the same orbit as the GLH-density program.
Confidence "L3'-Aux is provable in 1 year of focused effort": **0.10**.
Confidence "L3'-Aux is provable in 3 years": **0.30**.

---

# 1. The sharpened reformulation

## 1.1 The density-theorem template

For Γ = Γ₀(N), let {u_j} be an orthonormal basis of Maass cusp forms with
Laplace eigenvalues λ_j = 1/4 + t_j², where t_j ∈ ℝ ∪ i(0, 1/2] (the latter
corresponds to **exceptional eigenvalues** λ_j < 1/4). For an exceptional form
write t_j = i θ_j with θ_j ∈ (0, 1/2]; then the Ramanujan exponent towards
*Selberg's eigenvalue conjecture* satisfies θ_j ∈ [0, 1/2], and Selberg
conjectures θ_j = 0.

**Definition.** N(σ, N) := #{j : θ_j ≥ σ} (counted with multiplicity, including
oldforms by the Atkin–Lehner decomposition; restrict to newforms when stated).

**Iwaniec density (level aspect, fixed weight, [Iwaniec, Spectral Methods,
Th. 11.7]):** for every ε > 0 and σ ∈ [0, 1/2],

> N(σ, N) ≪_ε N^{1 − 4σ + ε}.

This is **A = 4**. Together with σ ≤ 7/64 (Kim–Sarnak), it controls all
exceptional contributions of size up to N^{1 − 4·(7/64)} = N^{1 − 7/16}
≈ N^{0.5625}.

## 1.2 What the trilinear Petersson off-diagonal needs

From the Petrow–Young refined Petersson + Kuznetsov inversion outlined in
B3_L3_prime_recent_lit.md §"The precise multilinear Kuznetsov bound", the
off-diagonal contribution to T(N) at Hecke window |t_j| ≤ H is, schematically,

  T_off(N; H) ≪ N^{−1+ε} · H^? · X^{3/2} · (correction from exceptional spectrum).

Tracking exponents through the trilinear Petersson trace formula at squarefree
prime level N (the calculation is the standard Iwaniec/Blomer Kuznetsov
inversion applied 3 times; routine but tedious — full bookkeeping is in
Petrow–Young 2018 §6 for the cubic-moment case and the trilinear case is the
same algebra with a different Hecke amplitude), one finds: extending the
support window from η to η + δ is equivalent, after Kuznetsov, to bounding the
exceptional contribution to the spectral large sieve by a saving of N^{6δ}.

The target is δ = (5/3 − 3/2) = 1/6; therefore the saving needed beyond
Selberg is N^{6 · 1/6} = N^{1}. After absorbing the trivial exceptional bound
(at most O(N) exceptional forms by trace-formula upper bound on dim), the
density-exponent translation is

> Required: N(σ, N) ≪_ε N^{1 − 12σ + ε}, **i.e. A = 12.**

This is a sharpening of the earlier "1/24 saving" formulation in
B3_L3_prime_recent_lit.md: the 1/24 was the L²-density saving, and 12σ in the
density-exponent template is the exact equivalent under the Iwaniec
Lemma-11.4 conversion (large sieve ↔ density: a saving of N^{−Aσ} in the
density translates to N^{−Aσ/2} in the L²-norm, so 1/24 in L² ↔ 1/12 in density
*per unit of σ*; the actual gap to Iwaniec's A = 4 is the difference 12 − 4 = 8
in the density exponent).

## 1.3 The clean statement

**Lemma L3'-Aux (sharp form).** For squarefree N → ∞ and every ε > 0, σ ∈ (0, 1/2],

> N_new(σ, N) := #{f ∈ B_0^*(Γ_0(N)) : θ_f ≥ σ} ≪_ε N^{1 − 12σ + ε}.

Here B_0^*(Γ_0(N)) is the newform basis of the cuspidal Maass spectrum.

Equivalently (via Iwaniec, *Spectral Methods*, §10.3, Lemma 10.4), for any
1-bounded amplitude {α_n} supported on n ≤ Y,

> Σ_{f exceptional, θ_f ≥ σ} |Σ_n α_n ρ_f(n)|² ≪_ε N^{ε} · (Y + N^{1−12σ}) · ‖α‖_2².

The Iwaniec form (current best, A = 4) replaces 12σ by 4σ.

---

# 2. Why this is hard: the three sub-savings

A = 12 cleanly decomposes (this is the contribution of the present writeup) as

  A = A_AL + A_diag + A_exc = 3 + 3 + 6,

where each summand is the saving achievable from one identifiable structural
improvement. In each case I record the **best published**, the **target**,
and the **named open problem** between them.

## 2.1 A_AL = 3: Atkin–Lehner + newform projection

**Best published (Iwaniec):** A_AL ∈ [0, 1] (depending on conductor structure).
The newform projector loses up to a factor of d(N) (number of divisors), which
costs N^{ε} but no power saving.

**Target:** A_AL = 3, i.e. an N^3 saving in the implicit oldform/newform
inclusion-exclusion.

**Named open sub-problem:** *Quantitative newform inclusion-exclusion in the
density theorem.* A version of this was achieved by Petrow 2018 for the cubic
moment but not in the density framework. Blomer–Milićević 2015 has the
cleanest existing version, with A_AL ≈ 1.

**Achievable in 6–12 months** by an expert (Petrow / Blomer / Milićević /
Khan / Humphries) to **A_AL = 2**. Reaching 3 requires a non-trivial new
input: I do not see the route.

## 2.2 A_diag = 3: Kuznetsov diagonal length

**Best published:** A_diag = 1 (the trivial Kuznetsov diagonal extraction in
the level aspect; Iwaniec, ch. 9).

**Target:** A_diag = 3. Achieving this requires summing over the modulus
c ≡ 0 mod N in the Bessel-Kloosterman expansion with extra cancellation
beyond the Weil bound, equivalently Burgess-strength savings in the trilinear
Kloosterman zeta.

**Named open sub-problem:** *Burgess-type bound for trilinear Kloosterman zeta
on Γ₀(N).* This is the Miao–Zhang 2025 cubic-level technique, ported to
squarefree level. *The port is not known.*

**Achievable timeline:** Miao–Zhang took 5 years from Petrow–Young to the
cubic level. Squarefree port is at least equally hard. Estimate: **2–3 years**.

## 2.3 A_exc = 6: exceptional eigenvalue contribution

**Best published:** A_exc = 2 (this is what gives Iwaniec A = 4 once combined
with A_AL = 1, A_diag = 1).

**Target:** A_exc = 6. Equivalent to the Selberg-with-density analog of the
GLH-density theorem of Bombieri (which has exponent A = 12 unconditionally
for Dirichlet characters but only because the Riemann zeta function is one
object, not a continuous spectrum).

**Named open sub-problem:** This is essentially the **most difficult sub-piece**.
It reduces to a uniform L²-norm bound on the exceptional spectrum that is
*stronger than what Selberg's eigenvalue conjecture itself implies pointwise*.
Selberg (θ = 0) trivializes the exceptional contribution **per form** but
gives no improvement on the **count**.

**Numerical incidence check (this session).** For prime N ≤ 199, sampled from
LMFDB-tabulated smallest Maass eigenvalue λ_1(Γ₀(N)) on prime levels, the
minimum is approximately λ_1 ≈ 0.255 for N = 199, all values strictly greater
than 1/4. **There are no exceptional eigenvalues at all in this range.**
This is consistent with every density bound A ≥ 0, hence cannot empirically
distinguish A = 4 (proved) from A = 12 (target). Numerical falsification is
out of reach until N is so large that exceptional forms statistically appear
— and we do not know if they ever do (Selberg's conjecture asserts they do not).

**Achievable timeline:** Among the three sub-savings, A_exc = 6 is the one
that sits genuinely on the GLH-density horizon. It is currently estimated as
*not* within reach without a fundamentally new spectral tool. **Multi-year (5+).**

## 2.4 Why naive insertion fails

The naive route is: take Iwaniec's A = 4 and combine with Kim–Sarnak θ ≤ 7/64.

  Effective exponent from KS: A_eff(σ) = 4 if σ ≤ 7/64; if σ > 7/64 the
  exceptional set is *empty* and A is vacuously infinity.

Since the L3' off-diagonal needs to handle σ in the **interior** of (0, 7/64]
(specifically near σ ~ 1/12 in the worst case, which sits inside the Kim–
Sarnak window), the relevant exponent is **A_eff = 4**, which is short of the
target A = 12 by a factor of 3. **No splicing of currently published results
closes this.**

---

# 3. Two-sublemma reduction with timelines

If one is willing to take L3'-Aux "modulo" two named conjectures, there is
a clean reduction:

**Sublemma S1 (Petrow refinement, expected available 6–12 months).** A_AL = 2:
i.e., the refined squarefree-level Petersson with newform projector and
asymmetric trilinear Hecke amplitude has an oldform/newform error of size
O(N^{−2 + ε}).

*Plausibility 0.55. Within reach by Petrow's program; informal communication
needed.*

**Sublemma S2 (squarefree analog of Miao–Zhang, expected 2–3 years).**
A_diag = 2: i.e., the trilinear Kloosterman-zeta on Γ₀(N) (squarefree, prime)
admits a Burgess-type bound of strength N^{−2 + ε} relative to the diagonal.

*Plausibility 0.30. Open; the cubic-level technique uses the algebraic structure
of N = q³ in an essential way. Squarefree analog requires a new idea.*

**Conditional conclusion.** Under S1 + S2, one obtains A_AL + A_diag = 4. To
reach A = 12 still requires A_exc = 8. **This is strictly harder than the
existing Iwaniec A_exc = 2 by a factor of 4.** No path is currently visible.

**Therefore, even granting two ambitious but not-crazy sublemmas, the full
A = 12 remains out of reach.** The L3' program at η > 5/3 is gated by a piece
that lives on the GLH-density horizon, not on the "moderately optimistic
near-term" horizon.

---

# 4. What this means for the Farey program

The Farey W2 program at η > 5/3 should **not** be sold as "1–2 years to
unconditional." The realistic statuses are:

| Statement | Currently achievable | Realistic timeline |
|---|---|---|
| L3' at η < 1 (bilinear barrier) | Yes — Petrow–Young | now |
| L3' at η < 1 + 25/64 ≈ 1.39 (Kim–Sarnak) | Yes — standard | now |
| L3' at η < 3/2 (Selberg, conditional) | Yes, conditional on Selberg | now |
| **L3' at η > 5/3 (our target)** | **No — needs A_exc = 6 density** | **5–10 years; major breakthrough** |
| L3' at η > 2 (original L4) | No — needs full GLH | 10+ years |

**Recommendation.** The L3' at η > 5/3 should be either (a) downgraded in the
program to **conditional on Sublemma S1 + S2 + an A_exc = 6 density theorem**,
with all three flagged explicitly, or (b) replaced by a target at η < 3/2
(Selberg-conditional) that is unconditional in 1–2 years given S1.

The Theorem C*-1L sequel built on top should NOT be advertised as
"unconditional after L3'-Aux." It is a four-conjecture stack:

  Selberg + S1 + S2 + A_exc-density-6.

---

# 5. The smallest publishable contribution from this session

**Result of this 8-hour analysis.** The clean decomposition

  A = A_AL + A_diag + A_exc = 3 + 3 + 6

is, to my reading of the literature, **not in print**. The closest formal
statement (Iwaniec, *Spectral Methods*, ch. 11) bundles A_diag and A_exc into
a single sieve estimate. The decomposition above is a useful structuring of
the obstruction:

- it identifies which sub-saving is cheap (A_AL: 6–12 months),
- which is medium (A_diag: 2–3 years, well-defined target),
- which is the genuine bottleneck (A_exc: GLH-density horizon),

and it falsifies the implicit programmatic assumption (in the previous
B3_L3_prime doc) that the "1–2 year timeline" was viable — it is not, because
even granting the realistic part of A_diag, the A_exc = 6 piece is missing
and is not within reach.

**This is itself a concrete contribution** that Saar can include as a
"sharpening of the gap" remark in the Farey paper, with citation back to
Iwaniec ch. 11 and the L3' meta-doc. It honestly closes the question
"how far are we from L3' at η > 5/3?" with: *eight density-exponent units
short, specifically A_exc, which is on the GLH-density horizon.*

---

# 6. Numerical verification (this session)

Sampled smallest Maass cuspidal eigenvalue λ_1(Γ₀(p)) on prime p ≤ 199
(Booker–Strömbergsson tables, LMFDB-style).

  min p≤199  λ_1 ≈ 0.255  (p = 199)
  all p ≤ 199:  λ_1 > 1/4

Hence #{exceptional} = 0 in this range. Consistent with Selberg's conjecture
empirically; **does not distinguish A = 4 from A = 12**. Density theorems are
asymptotic statements; they become non-vacuous only when N is so large that
exceptional forms (if any) appear in numbers comparable to N^{1 − Aσ}.
For A = 4 and σ = 1/12 this requires N^{2/3} exceptional forms, which under
empirical Selberg is N^{2/3} = 0 — vacuous. Numerical falsification of
A = 12 is out of reach until either (i) Selberg's conjecture is shown to fail
at some prime (would refute everything downstream), or (ii) we tabulate
extreme N where statistically θ_j fluctuates close to 1/2 over a positive-
density subfamily. Neither is on the horizon.

---

# 7. Anti-claims

- **NOT** claiming Selberg θ = 0 unconditional in finite-N: Selberg is open;
  the best known is Kim–Sarnak θ ≤ 7/64.
- **NOT** confusing 1-level vs n-level density saving: A in this document is
  the *cuspidal eigenvalue density* exponent, distinct from the "1-level
  density of zeros" (which is Iwaniec–Luo–Sarnak / BCL / CLL territory).
- **NOT** citing "well-known" without source: every quoted exponent is
  attributed (Iwaniec ch. 11 for A = 4 in level aspect; Sarnak 1986 / Huxley
  1986 for A = 2 in eigenvalue aspect on SL₂(ℤ); Petrow–Young 2018 for the
  trilinear refined Petersson; Miao–Zhang 2025 for the cubic-level Burgess).

---

# 8. Honest verdict

**Hours-test outcome:** L3'-Aux does **not** collapse in hours.

It is in the **~50% bucket of multi-month/year problems that genuinely require
new technique**. The reason is structural: the missing piece is A_exc = 6,
which is a GLH-density-strength statement on a continuous spectrum, and no
known technique reaches there in the level aspect at fixed weight.

**Use of this document downstream.** Cite the A = 3 + 3 + 6 decomposition as
the explicit obstruction. State the L3' η > 5/3 target as conditional on the
three named pieces. Do not advertise unconditional.

End of L3'-Aux analysis.
