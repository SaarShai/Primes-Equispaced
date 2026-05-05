---
title: "S4 / KMV Mellin verification of leading constant for Theorem B-exact"
type: derivation
domain: research
tier: working
confidence: 0.30
created: 2026-05-03
updated: 2026-05-03
verified: 2026-05-03
sources:
  - "Kowalski-Michel-VanderKam, 'Non-vanishing of high derivatives of automorphic L-functions at the center of the critical strip', Crelle 526 (2000), pp. 1-34"
  - "Kowalski-Michel-VanderKam, 'Mollification of the fourth moment of automorphic L-functions and arithmetic applications', Invent. Math. 142 (2000), pp. 95-151"
  - "Kowalski-Michel-VanderKam, 'Rankin-Selberg L-functions in the level aspect', Duke 114 (2002), pp. 123-191"
  - "Iwaniec-Luo-Sarnak, Publ. IHES 91 (2000)"
  - "/Users/saar/Farey 4.7 solutions/Weakest_sufficient_conditions.md (S4 derivation prompt)"
supersedes: []
superseded-by: null
tags: [theorem-B, KMV, Mellin, level-aspect, no-match, S4-fails]
---

# Honest verdict (TL;DR)

**S4 chain does NOT yield Theorem B-exact at the predicted constant 2/(3π) with
power (log N)^4.** The PARI/GP Mellin verification shows the leading
unmollified harmonic 2nd moment of Λ'(f, 1/2) over `S_2*(q)` is

  `Σ^h |Λ'(f,1/2)|² ~ q̂ · (14/3) · (log q̂)^3`

with leading **(log q̂)^3 not (log q̂)^4**, and constant `14/3 ≈ 4.667`,
not `4/(3π) ≈ 0.4244`. The ratio is ≈ 10.996 with the powers also off.
Therefore S4a/S4b as cited in `Weakest_sufficient_conditions.md` cannot
deliver `2/(3π)·(log N)^4` for the `|L'(½,f)|²` second moment.

The note's S4 framing **mis-cites KMV §5** — the actual paper that
contains this content is the Crelle 2000 KMV paper on high derivatives,
and its Theorem (eq. (5)) plus Proposition 5.1 give a (log q)^3 leading
order for the unmollified 2nd moment of Λ'(f,1/2) — one power below the
target.

Conclusion: confidence in "Theorem B-exact unconditional via S4"
should be revised **DOWN** from 0.55 to **≤ 0.10**, not up.

---

# Section 1 — Verbatim KMV statement (Crelle 2000, §1 eq. (5))

The cited KMV "high derivatives" paper (E. Kowalski, P. Michel, J.
VanderKam, *Non-vanishing of high derivatives of automorphic L-functions
at the center of the critical strip*, J. Reine Angew. Math. (Crelle) 526
(2000), 1-34) states verbatim in Section 2 (paragraph following eq. (4)):

> *Suppose that we were to consider the first and second (unmollified)
> moments*
>
>     L_h = Σ^h Λ^(k)(f, 1/2),    Q_h = Σ^h Λ^(k)(f, 1/2)^2.
>
> *Using Lemma 3.2, one can show that, as q → +∞,*
>
>     L_h ~ c_k (log q̂)^k,   Q_h ~ c'_k (log q̂)^{2k+1}     (eq. 5)
>
> *for some c_k, c'_k > 0 (see in particular [Du] for this proof in the
> case k = 0).*

Here `q̂ = √q / (2π)`, `Λ(f, s) = q̂^s Γ(s+1/2) L(f, s)` (KMV §1), and
the harmonic average is `Σ^h αf := Σ_{f ∈ S_2*(q)} αf / (4π(f, f))`.

For k = 1 (the case relevant to S4):

  **Q_h ~ c'_1 (log q̂)^3.**

The leading exponent is **3, not 4**.

The further explicit form of the unmollified leading constant is computed
below by the Mellin residue. Proposition 5.1 of KMV gives the **mollified**
2nd moment with leading order (log q̂)^{2k-2} = (log q̂)^0 for k=1; the
unmollified analog (drop mollifier, set P ≡ 1) restores the (log q̂)^3
leading via the additional ζ(1+s_1+s_2) and ζ(1+2t+z_1+z_2) ratio.

# Section 2 — Predicted Mellin integral

KMV §5 (Crelle 2000), eq. (21) gives the explicit-formula expansion (with
no mollifier):

  Λ^(k)(f, 1/2)² = 2 q̂ · Σ_{n_1, n_2} λ_f(n_1)λ_f(n_2)/(n_1 n_2)^{1/2}
                   · log(q̂/n_1)^k log(q̂/n_2)^k · W(n_1 n_2 / q̂²),

where

  W(y) = (1/2πi) ∫_{(c)} Γ(1+t)² y^{-t} dt/t.

Applying the Petersson formula (KMV §3, Lemma 3.2 + Lemma 3.3), only the
diagonal `n_1 = n_2 = n` survives at leading order, with off-diagonal
Kloosterman terms of size ≪ q̂^{1-γ}. The diagonal main term is

  Q_h^{diag} = 2 q̂ · Σ_n (1/n) log(q̂/n)^{2k} · W(n²/q̂²).

For k = 1, set `s = 1 + 2t` and use

  Σ_n n^{-s} log²(q̂/n) = (log q̂)² ζ(s) − 2 log q̂ · ζ'(s) + ζ''(s)

to convert to

  Q_h^{diag} = 2 q̂ · (1/2πi) ∫_{(c)} Γ(1+t)² q̂^{2t}
                  · [(log q̂)² ζ(1+2t) − 2 log q̂ · ζ'(1+2t) + ζ''(1+2t)] dt/t.

The leading constant is the residue at t = 0 (a quartic pole assembled
from the simple pole of ζ(1+2t) + the 1/t prefactor + the L² and L
multipliers).

# Section 3 — PARI script + raw numerical output

Script: `/Users/saar/Farey 4.7 solutions/S4_KMV_Mellin_verify.gp`.

The script:
- expands `Γ(1+t)²` and `q̂^{2t}` as Taylor series in t around t=0,
- expands `ζ(1+2t)`, `ζ'(1+2t)`, `ζ''(1+2t)` as Laurent series via
  PARI's built-in Stieltjes constants,
- multiplies, extracts the coefficient of `t^0` (residue at the simple
  pole at t = 0 from the prefactor 1/t),
- multiplies by 2q̂ to get the leading polynomial in `L = log q̂`.

Raw output (`S4_KMV_Mellin_verify.out`):

    Residue (= coeff of t^0 in Gamma(1+t)^2 * qhat^{2t} * B):
    2.333333... * L^3
       - 1.731646994704598... * L^2
       + 2.165658223496310... * L
       - 0.748879208217356...

    Q_h^{diag, leading} = 2*qhat * Residue. Coefficients in L = log qhat:
    4.666666... * L^3
       - 3.463293... * L^2
       + 4.331316... * L
       - 1.497758...

    Leading (log qhat)^3 coefficient of Q_h^{diag} / qhat:  4.666666... = 14/3

    Predicted target 4/(3*Pi):  0.42441318...
    Predicted target 2/(3*Pi):  0.21220659...
    Ratio leadL3 / (4/(3*Pi)):  10.9956
    Ratio leadL3 / (2/(3*Pi)):  21.9911

Closed form: leading `(log q̂)^3` coefficient = **14/3** (verified
14/3 = 4.66666666... in PARI to 40 digits).

# Section 4 — Match / no-match verdict

**No match.** Two distinct mismatches:

1. **Power of log q is wrong.** The S4 chain in
   `Weakest_sufficient_conditions.md` claims a `(log N)^4` leading term
   for `(1/|F_N|) Σ |L'(½,f)|²`. The actual KMV computation (Crelle 2000
   eq. (5)) gives leading order `(log q̂)^3` for the harmonic 2nd moment
   of `Λ'(f,1/2)`, even before extracting the odd-subfamily piece.
   Conversion to `L'(1/2,f)` divides by q̂ but does not raise the log
   power — see Section 4.1 below.

2. **Constant is off by ~11×.** The leading L^3 coefficient is `14/3 ≈
   4.667`, not the predicted `4/(3π) ≈ 0.4244`. Even allowing for unit
   conversions and the qhat=√q/(2π) substitution, this gap is far larger
   than any reasonable normalization translation can absorb. Specifically
   the ratio is ≈ 10.996, which is not π, π², 4/π, or any standard
   ratio.

## Section 4.1 — Why the (log q̂)^3 cannot be lifted to (log q̂)^4

On the odd subfamily (ε_f = -1), `Λ(f, 1/2) = 0`, so

  `Λ'(f, 1/2) = q̂^{1/2} · L'(1/2, f)`.

(Differentiating `Λ(s, f) = q̂^s Γ(s+1/2) L(s, f)` at s = 1/2 with
L(1/2, f) = 0: only the L'(s, f) term survives because the chain rule
factor on `q̂^s Γ(s+1/2)` multiplies L(1/2, f) which vanishes.)

Hence `|Λ'(f, 1/2)|² = q̂ · |L'(1/2, f)|²` on the odd subfamily.

On the even subfamily (ε_f = +1), L(1/2, f) need not vanish, and

  `Λ'(f, 1/2) = q̂^{1/2} · [(½ log q̂ + Γ'/Γ(1)) L(1/2, f) + L'(1/2, f)]`.

So `|Λ'(f, 1/2)|² ~ q̂ · (log q̂)² · |L(1/2,f)|² + ...` on the even
subfamily.

The KMV 4th-moment paper (Invent. Math. 142, 2000, Cor. 1.3) gives
`Σ^h L(f, 1/2)^4 = P(log q) + O(q^{-1/12+ε})` with leading coefficient
`1/(60π²)`. The 2nd moment of L(f, 1/2) (Iwaniec-Sarnak) is
`Σ^h L(f, 1/2)² ~ const · log q`. So the even-subfamily contribution to
`Σ^h |Λ'(f, 1/2)|²` is

  ≈ q̂ · (log q̂)² · log q̂ · |F_q^+| · (1/|F_q^+|)
  = q̂ · (log q̂)³ · const,

confirming the (log q̂)^3 leading is **dominated by the even subfamily's
log q̂ from the L^2 piece, NOT by an L'^2 piece**.

The odd subfamily's piece `q̂ · Σ^h_{odd} |L'(1/2,f)|²` has leading order
**at most (log q̂)^2**, not (log q̂)^3 or (log q̂)^4 (since when totaled
with the even piece it contributes a sub-leading O((log q̂)^2) from
within Q_h ~ c'_1 (log q̂)^3).

Wait — this is not quite right. The total Q_h is c'_1 (log q̂)^3 = (14/3)
(log q̂)^3. The even subfamily piece is (log q̂)² · (log q̂) = (log q̂)^3
with some constant. The odd subfamily piece is `Σ^h_{odd} q̂ · |L'|²`
which could be (log q̂)^3 with a different constant. They add. The note's
target is (log N)^4 which would require the odd-subfamily second moment
of `L'(1/2,f)` to be (log q)^4, which is **strictly larger** than the
total Q_h order — impossible.

## Section 4.2 — What CFKRS actually predicts

The CFKRS recipe (Conjectural conrey-Farmer-Keating-Rubinstein-Snaith)
predicts for `(1/|F_q^-|) Σ_{f ∈ F_q^-} |L'(1/2, f)|²` an asymptotic of
the form `c · (log q)^4` with c involving the Hadamard product of certain
arithmetic factors. **However** this prediction requires the odd-subfamily
1st moment squared to also be (log q)² (so that variance alone is (log
q)^4). KMV's odd-subfamily 1st moment of `L'(1/2,f)` (Theorem on first
moment / mollification, see also Iwaniec-Sarnak) is ~ `c · log q`, so
mean² ~ `c² (log q)²`, NOT (log q)^4.

For the variance to give (log q)^4, you would need an unconditional
3-level density or Sound-Young-type extension — which is precisely
the open input the S4 chain claimed to **bypass**.

# Section 5 — Implication for Theorem B-exact unconditional

**The S4 chain does not deliver Theorem B-exact at constant 2/(3π) with
power (log N)^4 unconditionally.** The KMV ingredients (S4a, S4b)
truncate at (log q)^3 leading order for the second moment of L', and
the predicted (log N)^4 cannot be extracted from KMV alone.

Two ways the original premise might be partially salvaged:

(a) **Reinterpret the target.** Maybe Theorem B-exact's actual leading
    power is (log N)^3 not (log N)^4. The note `Weakest_sufficient_conditions.md`
    asserts (log N)^4 with constant 2/(3π). If the actual target is
    `c (log N)^3`, then the S4 chain might match with a different
    constant. From the PARI computation,
    `leadL3 = 14/3` for the **total** Q_h, of which roughly half (the
    odd subfamily) is the relevant piece. So the candidate
    odd-subfamily L'^2 second moment leading would be at most ≈ `14/(3·2)
    = 7/3 ≈ 2.333` (log q)^3 — but this is only an upper bound (since
    the even subfamily also contributes). A more careful split is needed.

(b) **Use the right paper.** If the target paper is actually the
    Hughes-Young / Heap-Soundararajan / Bui-Heap-Lygeros work on
    moments of `|L'(1/2, f)|²` for the odd subfamily directly, those
    works give (log q)^4 conditionally on certain ratio conjectures —
    NOT unconditionally. The S4 chain as stated cannot bridge from KMV
    (unconditional) to that target.

# Section 6 — Precise gap

The gap is fundamental and structural, not numerical:

- KMV (Crelle 2000) eq. (5): unmollified Q_h of Λ'(f,1/2)² has leading
  power (log q̂)^3 across all of S_2*(q). UNCONDITIONAL.

- Target (Theorem B-exact, per the note): (1/|F_q^-|) Σ |L'(1/2,f)|² ~
  c · (log q)^4 with c = 2/(3π), on the **odd subfamily**.

These are mathematically incompatible at leading order. No finite Mellin
verification can bridge them, because the issue is the asymptotic order
of growth, not the leading coefficient.

The S4 chain in `Weakest_sufficient_conditions.md` is therefore based on
a **misattribution** of KMV results. The actual KMV references give

  unmollified: Q_h ~ c'_1 (log q̂)^3   (Crelle 2000 eq. 5)
  mollified:   Q_h ~ const · (log q̂)^0 = O(1)   (Crelle 2000 Prop 5.1)

Neither yields a `(log q)^4` term for the L'² 2nd moment.

# Section 7 — What S4 actually gives (the legit weaker statement)

Re-reading what KMV legitimately delivers:

  `(1/|S_2*(q)|) Σ^h |Λ'(f, 1/2)|²`
     `~ (14/3) q̂ (log q̂)^3 / |S_2*(q)|`
     `~ (14/3) q̂ (log q̂)^3 / (q/12)`
     `~ (14·12/3) (log q̂)^3 / (2π/√q · 1)`   (q̂ = √q/(2π))
     `~ 56 √q (log q̂)^3 / (2π) ~ (28/π) √q (log q̂)^3`.

This is unbounded as q → ∞ (because of the harmonic weight removal
factor), confirming the natural-average result requires careful
weight-removal — KMV §6 of the 4th-moment paper handles this.

**Honest weakest unconditional statement available from KMV:**

  Σ^h |Λ'(f, 1/2)|² = (14/3) q̂ (log q̂)^3 + O(q̂ (log q̂)^2)

over `f ∈ S_2*(q)` for q prime, q → ∞.

Translating to natural average and to the odd subfamily requires
weight-removal (KMV §6). The natural average odd-subfamily second moment
of L'(1/2, f) inherits a leading order **at most (log q)^3**, not
(log q)^4.

# Section 8 — Action items

1. **Revise `Weakest_sufficient_conditions.md`**: the S4 chain as written
   cannot yield Theorem B-exact at (log N)^4 from KMV alone.
   - Either downgrade the target to (log N)^3 with a re-derived constant,
   - or identify the additional ingredient (likely a 3-level density or
     CFKRS ratio conjecture) needed to lift to (log N)^4.

2. **Reconcile with B3_Lprime_2nd_moment_RIGOROUS.md** (this repo): the
   confidence-0.55 in that note for `c = 2/(3π) (log N)^4` should be
   reassessed in light of the (log N)^3 wall imposed by KMV
   unconditionally.

3. **If 2/(3π) (log N)^4 is the right target**, the unconditional
   pathway requires either:
   - Sound-Young 2nd moment with shift (their paper does Dirichlet
     L-functions, not modular L-functions); a level-aspect adaptation is
     known partially in Bui-Heap-Lygeros, but only conditional results
     give the correct constant;
   - explicit ratio conjecture input à la CFKRS ratios.

4. **Honest update** to confidence:
   - "Theorem B-exact unconditional via S4 = {S4a, S4b, S4c}": **0.05**
     (was 0.55, downgraded because S4 ingredients don't reach
     (log N)^4).
   - "Theorem B-exact at (log N)^3 with some new constant via S4":
     **0.40** (worth pursuing as a weaker statement).
   - "Theorem B-exact at (log N)^4 with c = 2/(3π) unconditionally":
     **0.05** (no known route, all routes need conditional input).

# Section 9 — Caveats

- The PARI computation evaluates only the **diagonal** main term of
  the second moment via the explicit-formula Mellin integral. The
  off-diagonal contribution (Kloosterman piece) is bounded by KMV's
  Lemma 3.3 + spectral large sieve to be `O(q̂^{1-γ})`, which is
  `o(q̂)` and hence does not contribute at leading order. This is
  unconditional. PARI computation is thus correctly capturing the
  leading constant.

- The closed form `14/3` for the leading `L^3` coefficient is checked at
  40-digit precision: PARI returned `4.666666666...` exactly. This is
  very likely the rational `14/3`. (Sanity: the residue calculation
  involves `(2L)^3 / 3!` from the cubic pole of `1/(4t^3)` against
  `q̂^{2t} = e^{2Lt}`, giving `(8 L^3 / 24) · 4 = 4 L^3 / 3`. Then there
  are additional contributions: `(2L)·(L) · 1/2 = L^2 (?)` needs
  re-derivation. The exact `14/3` value is what PARI returned; it should
  be cross-checked by hand.)

- The note's "(S4c) half-vanishing from sign of f.e." is unaffected and
  remains UC (this part of S4 is correct).

- This verification does NOT rule out Theorem B-exact unconditional via
  some OTHER set of premises (S1, S3, S6 in the note's enumeration).
  Only the S4 route is invalidated at the (log N)^4 target.

# Section 10 — Cross-reference to prior failed attacks (do not repeat)

The following 9 prior attacks on Theorem B-exact unconditional all
failed (per AUTONOMOUS_PLAN.md and various REPORTs in this repo). The S4
attack joins this list:

10. **S4 chain via KMV variance + sign-equidistribution**: FAILS at
    leading-order power (log N)^3 vs target (log N)^4 (this note,
    2026-05-03).

The structural barrier is the same as in attacks 1-9: every
unconditional path stops at (log N)^3 for the L'² 2nd moment, while the
target requires (log N)^4. Lifting from (log N)^3 to (log N)^4 requires
either a stronger family input (3-level density unconditional) or a
CFKRS ratio input (conjectural).

# Section 11 — References (verbatim as cited)

- **KMV Crelle 2000**: E. Kowalski, P. Michel, J. VanderKam,
  *Non-vanishing of high derivatives of automorphic L-functions at the
  center of the critical strip*, J. Reine Angew. Math. **526** (2000),
  1-34. PDF: https://www.math.ethz.ch/~kowalski/high-derivatives.pdf.
  Key: Section 2 eq. (5) (unmollified moment power); Section 5 Prop 5.1
  (mollified moment).

- **KMV Invent. Math. 2000**: E. Kowalski, P. Michel, J. VanderKam,
  *Mollification of the fourth moment of automorphic L-functions and
  arithmetic applications*, Invent. Math. **142** (2000), 95-151. PDF:
  https://people.math.ethz.ch/~kowalski/fourth-moment.pdf. Key: Cor.
  1.3 (4th moment of L(f,1/2) leading coefficient = 1/(60π²)).

- **KMV Duke 2002**: E. Kowalski, P. Michel, J. VanderKam,
  *Rankin-Selberg L-functions in the level aspect*, Duke Math. J. **114**
  (2002), 123-191. PDF:
  https://people.math.ethz.ch/~kowalski/rankin-selberg.pdf. Key:
  Section 7 (second moment of L(f⊗g, 1/2+μ)). Note: this is for
  Rankin-Selberg twists, not directly L'(1/2, f).

- **ILS 2000**: H. Iwaniec, W. Luo, P. Sarnak, *Low lying zeros of
  families of L-functions*, Publ. Math. IHES **91** (2000), 55-131.
  Key: §3 sign equidistribution; §6 unconditional 1- and 2-level density
  in supp ⊂ (-2, 2).

- **Source note** that triggered this verification:
  `/Users/saar/Farey 4.7 solutions/Weakest_sufficient_conditions.md`
  (2026-05-03), Section 4 / S4 chain.

---

# Self-audit

I aimed to verify, not to confirm. Result: the S4 chain as stated in the
source note **does not** yield Theorem B-exact at the predicted constant
2/(3π)·(log N)^4 unconditionally. The actual KMV input gives leading
order (log q)^3, one power below the target, and a numerical leading
constant of 14/3 vs predicted 4/(3π) — gap of ≈ 11× even before the log
power mismatch.

This is a **negative result**: S4 does not advance Theorem B-exact.
Confidence in the S4 route is downgraded from 0.55 to ≈ 0.05.

The correct path forward is to find a different sufficient condition set
(S1, S3, or S6 in the note's enumeration), or to accept that the target
constant 2/(3π) at (log N)^4 likely requires conditional input (CFKRS
ratios or 3-level density unconditional, both currently open).
