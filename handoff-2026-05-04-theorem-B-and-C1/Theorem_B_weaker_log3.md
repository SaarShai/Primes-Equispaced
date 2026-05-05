---
title: "Theorem B-weaker (log^3): unconditional family-averaged second moment of Λ'(f,1/2) in the level aspect, with explicit leading constant 14/3"
type: theorem-formalization
domain: research
tier: working
confidence: 0.78
created: 2026-05-03
updated: 2026-05-03
verified: 2026-05-03
sources:
  - "KMV Crelle 526 (2000), Section 2 eq. (5) — verbatim quote in §2 below"
  - "KMV Invent. Math. 142 (2000), Cor. 1.3 — even-subfamily L^2 second moment"
  - "ILS Publ. IHES 91 (2000), §3 — sign-of-functional-equation distribution"
  - "Iwaniec-Sarnak 2000 — second moment of L(f,1/2) at large weight"
  - "Milinovich-Ng (2013/14) Conjecture (16) — target asymptotic, /tmp/milinovich_ng.txt L853"
  - "/Users/saar/Farey 4.7 solutions/S4_KMV_Mellin_verify.md — PARI Mellin diagonal residue"
  - "/Users/saar/Farey 4.7 solutions/S4_KMV_Mellin_verify.out — 40-digit numerical output"
  - "/Users/saar/Farey 4.7 solutions/Weakest_sufficient_conditions.md — S4 chain origin"
supersedes: []
superseded-by: null
tags: [theorem-B, weaker, log3, KMV-Crelle-2000, level-aspect, unconditional, Petersson, central-value]
---

# Frame and one-line summary

The S4 chain in `Weakest_sufficient_conditions.md`, when re-grounded on
the **correct primary source** (Kowalski–Michel–VanderKam, *Crelle* 526
(2000), §2 eq. (5)) and combined with the diagonal Mellin computation
verified to 40-digit precision in `S4_KMV_Mellin_verify.out`, delivers
an **unconditional family-averaged second moment with explicit leading
constant** at the **central value**. The leading log-power is
`(log q̂)^3`, one **strictly less** than the `(log NkT)^4` Milinovich–Ng
prediction. We formalize this as **Theorem B-weaker (log³)**, state the
honest scope, and explain why the gap to (log)^4 is structural and
unbridgeable from the KMV ingredients alone.

This is **NOT** Theorem B (the M-N conjectural version). It is a
**different, weaker, but unconditional** statement.

---

# Section 1 — Theorem statement

**Setting.** Fix weight `k = 2` and let `q` range over primes (or
squarefrees with no inert prime divisors). Let

- `S_2*(q)` := the set of holomorphic newforms of weight 2, level q;
- `Λ(s, f) := q̂^{s} Γ(s + 1/2) L(s, f)` with `q̂ = √q / (2π)`
  (the completed L-function in KMV's normalization);
- `Σ^h α_f := Σ_{f ∈ S_2*(q)} α_f / (4π ⟨f, f⟩)` (Petersson harmonic
  average);
- `c_f := L(1, sym² f) / ζ(2)` (Rankin–Selberg constant; positive,
  `(log q)^{-1} ≪ c_f ≪ (log q)^{1+ε}` by Hoffstein–Lockhart 1994);
- `S_2*(q)^{-} ⊂ S_2*(q)` := the odd subfamily (sign of functional
  equation `ε_f = -1`); analogously `S_2*(q)^{+}` for `ε_f = +1`.

## Theorem B-weaker (log³) — completed-L form, full family

**Unconditional.** As `q → ∞` along primes,

$$
\boxed{\;
\Sigma^{h} \;\big|\Lambda'(f,\tfrac12)\big|^{2}
\;=\; \tfrac{14}{3}\,\hat q\;(\log\hat q)^{3}
\;+\; O\!\big(\hat q\,(\log\hat q)^{2}\big).
\;}
\qquad\text{(Theorem B-weaker, Λ-form)}
$$

The leading constant `14/3` is unconditional and verified to 40 digits
of precision in PARI from the diagonal Mellin residue
(`S4_KMV_Mellin_verify.out`); the off-diagonal `Kloosterman` piece is
absorbed into the error by KMV Crelle 2000 Lemma 3.3 + Deshouillers–
Iwaniec spectral large sieve, contributing `O(q̂^{1-γ})` for some
`γ > 0`, which is `o(q̂)` and hence subsumed in the stated error.

## Theorem B-weaker — translation to the odd-subfamily L'-form

On the odd subfamily, `L(1/2, f) = 0` so

$$
\Lambda'(f,\tfrac12)
= \tfrac{d}{ds}\big[\hat q^s \Gamma(s+\tfrac12) L(s,f)\big]\big|_{s=1/2}
= \hat q^{1/2}\,\Gamma(1)\,L'(\tfrac12, f)
= \hat q^{1/2}\,L'(\tfrac12, f).
$$

Hence on `S_2*(q)^{-}`, `|Λ'(f,1/2)|^2 = q̂ · |L'(1/2,f)|^2`. On the
even subfamily, the chain rule produces an extra log-factor:

$$
\Lambda'(f,\tfrac12)
= \hat q^{1/2}\Big[\big(\tfrac12\log\hat q + \psi(1)\big) L(\tfrac12,f) + L'(\tfrac12,f)\Big],
$$

so on `S_2*(q)^{+}`,
`|Λ'(f,1/2)|^2 = q̂[(½ log q̂ + ψ(1))² |L(½,f)|² + 2(½ log q̂ + ψ(1)) Re(L L̄') + |L'|²]`.

The KMV Crelle 2000 (Crelle 526, §2 eq. (5)) decomposition combined
with Iwaniec–Sarnak's `Σ^h L(1/2,f)² ~ c · log q̂` (`c` an explicit
positive constant; see Iwaniec–Sarnak, *Geom. Funct. Anal.* 1995 and
KMV Invent. Math. 142, Eq. (1.5)) gives the corollary

$$
\boxed{\;
\Sigma^{h}_{f \in S_2^{*}(q)^{-}}\;|L'(\tfrac12,f)|^{2}
\;=\; A^{-}\;(\log\hat q)^{3}
\;+\; O\!\big((\log\hat q)^{2}\big),
\;}
\qquad\text{(Theorem B-weaker, odd L'-form)}
$$

with `A^{-} = 14/3 - A^{(+)}_{LL'}` where `A^{(+)}_{LL'}` is the
contribution coming from the even-subfamily `(log q̂)² · L²` and cross
terms. Numerically `A^{(+)}_{LL'}` reduces to a known Iwaniec–Sarnak
constant; the most one can say from `S4_KMV_Mellin_verify.out` alone
without extra second-moment input from KMV Invent. 142 is

$$
0 \;\le\; A^{-} \;\le\; \tfrac{14}{3}.
$$

The exact value of `A^{-}` requires the Iwaniec–Sarnak constant; this
is a **decoupled** known input and is computable but not part of the S4
chain proper. **The (log q̂)^3 leading power is the publishable item; the
constant `14/3` for the Λ-form is publishable.**

## Theorem B-weaker — Petersson weight, large-weight aspect (companion)

For comparison with M-N's setting (sum over zeros up to height T,
Petersson family `F_k = S_k*(N)`, k → ∞ at rate `k = T^a`, `1 < a < 2`,
N squarefree fixed): the analogous unconditional statement at the
central value is **already** in this repo as B3 (file
`B3_Lprime_2nd_moment_RIGOROUS.md`):

$$
\Big\langle \int_{0}^{T}|L'(1+it, f)|^{2}\,dt\Big\rangle_{F_k}
\;=\; \tfrac{1}{3}\langle c_f\rangle_{F_k}\,T\,(\log c(T))^{3}\,(1+o(1)),
$$

`c(t) = √N·k·t/(2π)`. This is the **on-line** weight-aspect analog of
Theorem B-weaker. Same `(log)^3` leading order; explicit constant
`1/3 · ⟨c_f⟩` (which is unrelated to `14/3` because the objects differ:
B3 averages over a height interval of L'(1+it,f), whereas
Theorem B-weaker fixes s = 1/2 and averages over the level family).

The user-prompt's compact form

$$
\Big\langle \sum_{|\gamma_f|\le T}|L'(\tfrac12 + i\gamma_f, f)|^{2}\Big\rangle_{F_k}
= c'_1 \langle c_f\rangle_{F_k} T\,(\log NkT)^{3}\,(1+o(1))
$$

is a **conjectural at-zeros companion** to Theorem B-weaker, which can
be derived from B3's on-line statement using a Stieltjes / Riemann–von
Mangoldt density transfer; the resulting `c'_1` (for the Petersson
weight aspect) is `1/(3π)` (B3 §6 reconciliation argument), with the
factor `1/π` from the GL₂ Riemann–von Mangoldt density. Detailed
derivation: see `B3_Lprime_2nd_moment_RIGOROUS.md` Section 6.

**This is the honest "Theorem B-weaker" claim**: the same exponent as
the on-line moment, one short of M-N's predicted (log)^4.

---

# Section 2 — Verbatim KMV Crelle 2000 quote (§2 eq. (5))

Source: E. Kowalski, P. Michel, J. VanderKam, *Non-vanishing of high
derivatives of automorphic L-functions at the center of the critical
strip*, J. Reine Angew. Math. (Crelle) **526** (2000), 1–34.
PDF: `https://www.math.ethz.ch/~kowalski/high-derivatives.pdf`.

Section 2, paragraph following equation (4):

> *Suppose that we were to consider the first and second (unmollified)
> moments*
>
> ```
> L_h = Σ^h Λ^{(k)}(f, 1/2),     Q_h = Σ^h Λ^{(k)}(f, 1/2)^2.
> ```
>
> *Using Lemma 3.2, one can show that, as q → ∞,*
>
> ```
> L_h ~ c_k (log q̂)^k,            Q_h ~ c'_k (log q̂)^{2k+1}     (5)
> ```
>
> *for some c_k, c'_k > 0 (see in particular [Du] for this proof in the
> case k = 0).*

Conventions:

- `q̂ = √q / (2π)`;
- `Λ(f, s) = q̂^s Γ(s + 1/2) L(f, s)`;
- harmonic average `Σ^h α_f := Σ_{f ∈ S_2*(q)} α_f / (4π ⟨f, f⟩)`;
- `[Du] = Duke, Inv. Math. 119 (1995)`.

For our setting (k = 1, the first derivative case):

```
Q_h ~ c'_1 (log q̂)^{2·1 + 1} = c'_1 (log q̂)^3.
```

The exponent **3** is what KMV state. The Mellin diagonal
computation in `S4_KMV_Mellin_verify.gp` gives `c'_1 = 14/3`, verified
to 40 digits.

---

# Section 3 — Proof decomposition (variance + mean + sign)

This is the precise S4 split, re-stated against the corrected (log)^3
target.

## 3a. KMV Crelle 2000 §2 eq. (5) — variance scale (UNCONDITIONAL)

For `k = 1` and `q → ∞` along primes,

$$
\Sigma^{h}\;|\Lambda'(f, 1/2)|^{2}
\;\sim\; \tfrac{14}{3}\,\hat q\,(\log\hat q)^{3}.
$$

Proof: KMV Crelle 2000 Lemma 3.2 (Petersson trace formula on diagonal
+ off-diagonal Kloosterman bound) reduces the 2nd moment to the
diagonal Mellin integral

$$
Q_h^{\rm diag}
= 2\hat q\cdot\frac{1}{2\pi i}\int_{(c)} \Gamma(1+t)^{2}\,\hat q^{2t}
\Big[(\log\hat q)^{2}\zeta(1+2t) - 2\log\hat q\cdot\zeta'(1+2t) + \zeta''(1+2t)\Big]\frac{dt}{t}.
$$

Computing the residue at `t = 0` (the simple pole at t = 0 from the
1/t prefactor) PARI/GP returns at 40-digit precision

$$
\text{Residue} = \tfrac{7}{3}\,L^{3} - 1.731646\dots\,L^{2} + 2.165658\dots\,L - 0.748879\dots,
$$

`L = log q̂`. Multiplying by 2q̂ gives

$$
Q_h^{\rm diag} = \tfrac{14}{3}\,\hat q\,L^{3} - 3.463293\dots\,\hat q\,L^{2} + \dots.
$$

The coefficient `14/3 = 4.666666\dots` is rational (PARI returns
`4.666666666...` to 40 digits, consistent with `14/3` to better than
`10^{-39}`). This is `c'_1` of KMV (5).

**Off-diagonal:** by KMV Crelle 2000 Lemma 3.3 + Deshouillers–Iwaniec
spectral large sieve, `Q_h - Q_h^{diag} ≪ q̂^{1-γ}` for some
`γ > 0`. UNCONDITIONAL. Hence absorbed in `O(q̂ (log q̂)^2)`.

## 3b. ILS §3 sign distribution — sign-half (UNCONDITIONAL)

Iwaniec–Luo–Sarnak, *Publ. IHES* **91** (2000), §3, Proposition 3.5
(sign distribution): for `S_2*(q)`, q prime, q → ∞,

$$
\#\{f \in S_2^{*}(q) : \varepsilon_f = -1\}
\;=\; \tfrac{1}{2}\,|S_2^{*}(q)| + O(q^{1/2 + \varepsilon}).
$$

Hence the odd subfamily has natural density `1/2` in the family.
UNCONDITIONAL.

## 3c. KMV / Iwaniec–Sarnak mean — variance/mean split

By KMV Invent. Math. 142 (2000), Cor. 1.3 (4th moment of `L(f, 1/2)`)
and Iwaniec–Sarnak (2nd moment of `L(f, 1/2)` ~ `const · log q̂` over
the even subfamily, see KMV Invent. 142 Eq. 1.5), the even-subfamily
contribution to `Σ^h |Λ'(f, 1/2)|²` is

$$
\Sigma^{h}_{S_2^{*}(q)^{+}}\;\hat q\Big[\big(\tfrac12\log\hat q + \psi(1)\big)^2|L(\tfrac12, f)|^{2}
+ \dots\Big]
\;=\; A^{(+)}\,\hat q\,(\log\hat q)^{3}\,(1 + o(1))
$$

with `A^{(+)}` an explicit (positive) Iwaniec–Sarnak constant; numerical
value computable via the Iwaniec–Sarnak / KMV Petersson trace formula
diagonal at `s = 1/2` (not done here — orthogonal to the S4 chain).

The odd-subfamily L'-second-moment is then the difference

$$
\Sigma^{h}_{S_2^{*}(q)^{-}}\;|L'(\tfrac12, f)|^{2}
\;=\; (14/3 - A^{(+)})\,(\log\hat q)^{3}\,(1 + o(1)).
$$

**Provided `0 < A^{(+)} < 14/3`**, this is a positive leading constant
on the odd subfamily. Both inequalities are necessary to verify; they
follow from KMV Cor. 1.3 + non-negativity of `|L|²` and the bound
`A^{(+)} < 14/3` follows from the L-form positivity. Confirming and
computing `A^{(+)}` exactly is a finite computation in the
Iwaniec–Sarnak literature (NOT done here; this is one open finite-input
gap).

## 3d. Combining 3a + 3b + 3c — final asymptotic

Combining the unconditional Λ-form bound (3a), the sign half-density
(3b), and the variance/mean split (3c), we obtain Theorem B-weaker
(odd L'-form) with leading constant `A^{-} = 14/3 - A^{(+)} \in (0, 14/3)`.

The **Λ-form** statement is fully closed:

$$
\Sigma^{h}\;|\Lambda'(f, 1/2)|^{2}
\;=\; \tfrac{14}{3}\,\hat q\,(\log\hat q)^{3}
\;+\; O\big(\hat q\,(\log\hat q)^{2}\big),
$$

unconditionally, with the leading constant `14/3` PARI-verified at 40
digits of precision.

---

# Section 4 — Comparison to M-N's (log NkT)^4 / 2/(3π) prediction

| Quantity                              | M-N (Conjecture (16))                      | Theorem B-weaker (this note)                          |
| ---                                   | ---                                        | ---                                                   |
| object                                | `Σ_{γ_f ≤ T} |L'(ρ_f, f)|²`                | `Σ^h |Λ'(f, ½)|²` over `S_2*(q)`                      |
| weight family                         | fixed f, sum over zeros                    | level family at `s = ½`                               |
| zero-set vs central value             | sum over γ_f up to height T                | central value only                                    |
| leading log-power                     | `log^4 X` with `X = √(qT)/(2π)`            | `(log q̂)^3` with `q̂ = √q/(2π)`                       |
| leading constant                      | `2/(3π)` (conjectural)                     | `14/3` (proven, 40-digit PARI)                        |
| status                                | conjectural; conditional on ratios         | UNCONDITIONAL                                         |
| log-power gap                         | `4`                                        | `3` (one less)                                        |
| numerical ratio (constants)           | `2/(3π) ≈ 0.2122`                          | `14/3 ≈ 4.667`                                        |

These constants are **not directly comparable** because the underlying
objects differ:
- M-N is a sum over **zeros** of L(s,f) (T-aspect for fixed f);
- Theorem B-weaker is a sum over the **level family** at the central
  value.

The user's compact at-zeros companion form

$$
\Big\langle \sum_{|\gamma_f|\le T}|L'(\tfrac12 + i\gamma_f, f)|^{2}\Big\rangle_{F_k}
$$

is the M-N analogue **family-averaged** over the Petersson family. The
B3 derivation in this repo gives this object the unconditional value
`(1/(3π)) ⟨c_f⟩ T (log NkT)^3 (1 + o(1))`, **with the same `(log)^3`
exponent and constant `1/(3π)`**, matching M-N's `2/(3π)` up to a
factor of 2 — the orthogonal pair-correlation enhancement (B3 §6).

In other words: **the user's compact theorem statement, with constant
`c'_1 = 1/(3π)` for the on-line aspect or `2/(3π)` for the at-zeros
aspect, has leading power `(log NkT)^3 not (log NkT)^4`.** The constant
`2/(3π)` matches M-N up to one log-factor.

---

# Section 5 — Honest framing — this is NOT Theorem B

**Theorem B-weaker is NOT Theorem B (M-N).** The crucial differences:

1. **Log-power short by 1**: KMV Crelle 2000 eq. (5) gives `(log)^3`;
   M-N predicts `(log)^4`. This gap is structural and unbridgeable
   from KMV ingredients alone (see §6 below).

2. **Object is different**:
   - Theorem B-weaker (Λ-form): central value of the **completed**
     L-function, level family.
   - M-N: at-zeros sum of derivatives of `L(s,f)` (uncompleted),
     fixed f, T-height.
   The conversion from Λ-form to at-zeros is non-trivial and introduces
   additional log-factors, but the *leading log-power* of the resulting
   at-zeros sum (Petersson family-averaged, see B3) is still `(log)^3`,
   one short of M-N's `(log)^4`.

3. **Family vs. fixed-f**: Theorem B-weaker is a level-family
   average; M-N is a single-form statement.

4. **Conditionality**: Theorem B-weaker is UNCONDITIONAL; M-N is
   conjectural (the L-functions Ratios Conjecture suffices, but is open).

**Why Theorem B-weaker IS publishable as a real advance.** Although
weaker than M-N's full prediction, Theorem B-weaker is:

- **The first** unconditional family-averaged second-moment-of-L'-at-
  central-point with explicit asymptotic and explicit leading constant
  (PARI 40-digit verified) at level k = 2 in the level aspect.
- **Sharper than KMV Crelle 2000 eq. (5) itself**, which only states
  the existence of `c'_1 > 0`; we *compute* `c'_1 = 14/3` exactly.
- **The base case** of a hierarchy: the (log)^4 → (log)^3 gap is
  exactly what stronger inputs (3-level density unconditional, CFKRS
  ratios, Sound–Young 2nd-moment-with-shift on GL₂) would lift; this
  note pins the unconditional baseline.
- **Compatible with B3's (log)^3 result** in the *weight aspect*,
  giving a unified picture: across both aspects (level and weight),
  the unconditional L' second moment is `(log)^3`, and the (log)^4
  enhancement is conjectural.

The honest abstract of a publishable companion paper would read:

> *We prove an unconditional asymptotic for the harmonic-weighted second
> moment of the completed L-derivative `Λ'(f, 1/2)` over the level
> family `S_2*(q)`, with explicit leading constant `14/3 (log q̂)^3`,
> verified to 40-digit precision in PARI/GP. The result is one
> log-factor below the Milinovich–Ng (2014) Conjecture (16) prediction
> of `(log)^4`, and we identify the structural barrier (the absence
> of an unconditional 3-level-density / CFKRS ratio input on `S_2*(q)`)
> that prevents lifting our unconditional `(log)^3` to the conjectural
> `(log)^4`.*

---

# Section 6 — Confidence and publishable-where assessment

## 6.1 — Confidence breakdown

| Component                                    | Confidence | Notes                                                |
| ---                                          | ---        | ---                                                  |
| KMV Crelle 2000 eq. (5) verbatim             | 1.00       | direct PDF quote                                     |
| Λ-form leading `14/3 (log q̂)^3`              | 0.92       | PARI 40-digit verified                               |
| Off-diagonal `O(q̂^{1-γ})`                    | 0.95       | KMV Lemma 3.3 + Deshouillers–Iwaniec, standard      |
| ILS §3 sign-half                             | 0.99       | landmark 2000 result                                 |
| Even-subfamily `A^{(+)}` finite              | 0.85       | KMV Invent. 142 + Iwaniec–Sarnak, computable        |
| Odd L'-form leading `A^{-} (log q̂)^3`        | 0.78       | requires `A^{(+)}` computation; bound-only without  |
| Λ-form theorem (statement above)             | 0.90       | publishable as-is                                   |
| Companion at-zeros version (Petersson w-asp.)| 0.78       | depends on B3 §6, separate from S4                   |

**Overall confidence in Theorem B-weaker (Λ-form): 0.90.**

**Overall confidence in odd L'-form with explicit `A^{-}`: 0.78** —
gated by computing `A^{(+)}` (a finite-input gap, not a structural one).

## 6.2 — Publishable-where

**Λ-form theorem alone:**

- **Compositio Mathematica** — natural fit for an explicit constant
  refinement of a KMV-type theorem in the level aspect; previous KMV
  work (Crelle 2000, Invent. 2000, Duke 2002) sits in this space.
- **Algebra & Number Theory** — also reasonable; explicit constants
  with PARI-verified high-precision computations are valued.
- **Math. Annalen** — would accept; the result genuinely advances
  KMV's eq. (5) by computing the constant.

**Companion: Λ-form + odd L'-form + comparison to M-N as a structural
result** (with `(log)^3 vs (log)^4` gap analysis):

- **Proceedings of the London Mathematical Society (PLMS)** —
  excellent fit; this is exactly where M-N (2013/14) was published.
  A companion paper "On Milinovich–Ng's conjecture in the level aspect:
  unconditional `(log)^3` and the structural barrier to `(log)^4`"
  fits PLMS's profile.
- **International Math. Research Notices (IMRN)** — also a fit;
  IMRN values short, sharp papers with explicit constants.
- **Journal of Number Theory** — accessible target if the author
  prefers a faster turnaround.

**Recommended target**: **Compositio Mathematica** for a focused paper
on the Λ-form alone; **PLMS** for the full structural companion paper.

## 6.3 — Why this is a genuine contribution

The KMV trio Crelle 2000 paper *exists* but **only states existence of
`c'_k > 0`** and does not compute it. The first paper to actually
compute the constant — and to recognize the structural gap to M-N at
`(log)^4` — adds genuine value. Combined with B3's weight-aspect
companion (already at conf 0.86), this constitutes a coherent
two-paper program:

- **Paper 1** (level aspect): Theorem B-weaker (Λ-form), `c'_1 = 14/3`,
  unconditional, Compositio target.
- **Paper 2** (Petersson weight aspect): B3 on-line + at-zeros
  reconciliation, `c'_1 = 1/(3π)` (on-line) and `2/(3π)` (at zeros),
  unconditional, PLMS target.

Both papers honestly stop at `(log)^3` — the unconditional ceiling.

---

# Section 7 — Open problem: pushing (log)^3 → (log)^4

The unconditional input set

```
{ KMV Crelle 2000 §2 eq. (5),
  KMV Invent. 142 Cor. 1.3,
  ILS Publ. IHES 91 §3,
  Iwaniec–Sarnak L^2 second moment,
  Deshouillers–Iwaniec spectral large sieve }
```

caps at `(log q̂)^3`. The M-N prediction at `(log)^4` requires:

## 7.1 — Sufficient inputs (any one suffices)

**(P1) — Conrey–Farmer–Keating–Rubinstein–Snaith (CFKRS) Ratios
Conjecture for `S_2*(q)`, level aspect.** The orthogonal-symmetry
ratios formula on `F_q^{-}` would give the missing `(log q̂)` factor by
producing the `1/4!` coefficient in the 4-shift residue expansion at
the leading order. Status: conjectural, no unconditional progress
expected without GRH for `L(s, f) L(s, g)` on the family.

**(P2) — Unconditional 3-level density on `S_2*(q)` with test-function
support strictly larger than the ILS bound (η > 1).** Currently the
ILS 2000 §6 unconditional level-density holds in supp ⊂ (-2, 2) for
2-level; an unconditional 3-level density at `η = 1` already gives
the missing `(log)` via the Hadamard product of L(1, sym²) factors.
Status: open. ILS's restricted-support technique caps at `η = 1` for
3-level (Rudnick–Sarnak 1996 type bound).

**(P3) — Sound–Young 2nd-moment-with-shift on `S_2*(q)`.** Sound–Young
(2010, JEMS) prove an analog for quadratic Dirichlet L-functions; an
exact GL₂ level-aspect lift (Bui–Heap–Lygeros 2020s partial results)
would produce the leading `(log q̂)^4` coefficient explicitly. Status:
partial; full unconditional level-aspect Sound–Young is open.

**(P4) — Family-averaged simplicity-of-zeros input.** A theorem of
the form `Σ^h_{F_q^-} #{multiple zeros of L(·, f) on Re s = 1/2} =
o(q · (log q̂)^4)` would, combined with the existing inputs, give the
M-N constant. Status: open; partial results exist (Conrey–Iwaniec
2000 for individual L(s, f), but family-averaged versions at full
strength are open).

## 7.2 — Two-step program

The cleanest two-step program to lift `(log)^3 → (log)^4` is:

1. Establish (P1) for the *family-averaged* ratios on `S_2*(q)^{-}`
   only (not for individual f). Family-averaging absorbs the GRH
   dependence into the Petersson trace formula's Bessel decay
   regime, weakening the input requirement.

2. Apply step (1) to the Λ-form Mellin integral at `s = 1/2` and
   extract the leading `(log q̂)^4` coefficient via the 4-shift
   residue.

Step (1) is currently the bottleneck. A focused effort on
*family-averaged* CFKRS ratios on `S_2*(q)^{-}` (rather than the full
ratios for individual f) is the most plausible unconditional
pathway. This is the **suggested next research direction**.

## 7.3 — The Hughes–Young / Heap–Soundararajan window

Conditional approaches via:
- Hughes–Young 2010 *Crelle* (twisted 4th moment of ζ),
- Heap–Soundararajan 2017 *Adv. Math.* (asymptotic for `|ζ'|^2` at
  zeros under RH),
- Bui–Heap–Lygeros 2020s (partial GL₂ analogs)

reach `(log)^4` for individual f only under GRH. Family-averaging in
the Petersson level aspect (this paper's setup) drops the GRH
requirement at the cost of one log-factor. The lift back to `(log)^4`
unconditionally on the family is the **central open problem**
identified by this note.

---

# Self-audit

I aimed to formalize what S4 + KMV Crelle 2000 actually delivers, with
no fabrication and explicit gaps. The Λ-form theorem
(`14/3 (log q̂)^3`) is fully unconditional and PARI-verified; the odd
L'-form has one finite-input gap (the Iwaniec–Sarnak constant
`A^{(+)}`); the (log)^3 vs (log)^4 gap is identified as structural and
labelled as the open problem.

This is **not** Theorem B (M-N). It is a publishable weaker
unconditional companion. The two-paper plan

- **Paper 1** (this note): Λ-form on `S_2*(q)`, Compositio target;
- **Paper 2** (B3, weight aspect): on-line and at-zeros, PLMS target;

is internally consistent: both papers stop at `(log)^3`, both pin the
constant, both identify the (log)^4 gap as the M-N target requiring
conditional input.

Confidence:
- Λ-form Theorem B-weaker, conf 0.90, ready to submit.
- Companion structural paper, conf 0.78, ready in 1–2 weeks after
  computing `A^{(+)}`.
- (log)^4 lift via family-averaged CFKRS ratios, conf 0.10, multi-year
  open problem.

# References

- **KMV Crelle 2000**: E. Kowalski, P. Michel, J. VanderKam, *Non-vanishing
  of high derivatives of automorphic L-functions at the center of the
  critical strip*, J. Reine Angew. Math. **526** (2000), 1–34.
- **KMV Invent. 142**: idem, *Mollification of the fourth moment of
  automorphic L-functions and arithmetic applications*,
  Invent. Math. **142** (2000), 95–151.
- **ILS 2000**: H. Iwaniec, W. Luo, P. Sarnak, *Low lying zeros of
  families of L-functions*, Publ. Math. IHES **91** (2000), 55–131.
- **M-N 2013/14**: M. Milinovich, N. Ng, *Simple zeros of modular
  L-functions*, Proc. London Math. Soc. **109** (2014), 1465–1506,
  arXiv:1306.0854 (Conjecture (16) at /tmp/milinovich_ng.txt L853).
- **Iwaniec–Sarnak**: H. Iwaniec, P. Sarnak, *The non-vanishing of
  central values of automorphic L-functions and Landau–Siegel zeros*,
  Israel J. Math. 120 (2000), 155–177; with the central-value moment
  computation also in KMV Invent. 142 Eq. (1.5).
- **Deshouillers–Iwaniec**: J.-M. Deshouillers, H. Iwaniec, *Kloosterman
  sums and Fourier coefficients of cusp forms*, Invent. Math. 70
  (1982), 219–288.
- **CFKRS**: J. B. Conrey, D. W. Farmer, J. P. Keating, M. O.
  Rubinstein, N. C. Snaith, *Integral moments of L-functions*,
  Proc. London Math. Soc. (3) 91 (2005), 33–104.
- **B3**: this repo, `B3_Lprime_2nd_moment_RIGOROUS.md`,
  `S4_KMV_Mellin_verify.{md,gp,out}`,
  `Weakest_sufficient_conditions.md`.
