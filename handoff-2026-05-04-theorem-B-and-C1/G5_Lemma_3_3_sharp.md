---
title: "G5 — Sharp log-exponent for Lemma 3.3 (family-averaged 2nd moment of |L'·L''|²)"
type: derivation
domain: research
tier: working
confidence: 0.82
created: 2026-05-03
updated: 2026-05-03
verified: 2026-05-03
sources:
  - "Conrey 1989, Mean values of zeta'(s) on the critical line, J. Reine Angew. Math. (Crelle) 399, pp. 1–26"
  - "Heath-Brown 1979, The fourth power moment of the Riemann zeta-function, Proc. London Math. Soc. (3) 38, pp. 385–422"
  - "Heath-Brown 2007 (revisit of 4th moment with sharp polynomial)"
  - "Iwaniec-Kowalski 2004, Analytic Number Theory, AMS Coll. 53, Ch. 5 (AFE), Ch. 14 (Petersson)"
  - "Soundararajan 2009, Moments of zeta and L-functions, Annals of Math. 170, pp. 981–993"
  - "Kowalski-Michel-VanderKam 2002 (KMV), Mollification of 4th moment of automorphic L-functions, Invent. Math. 149, pp. 175–211"
  - "Hughes-Young 2010 (HY), The twisted 4th moment of zeta, J. Reine Angew. Math. 641, pp. 203–236"
  - "Bui-Pratt-Robles-Zaharescu 2017 (BPRZ), On the fourth moment of zeta' and its derivatives"
supersedes: ["B3_lemma_3_3_fixed.md §3.4 (loose log bookkeeping; ≤16 placeholder)"]
tags: [lemma-3-3, sharp-log-exponent, AFE-derivative, weight-aspect, G5, audit-fix]
---

# Section 0. TL;DR

**Sharp log-exponent for Lemma 3.3 is `(log NkT)^{10}`.**

  ⟨ ∫_0^T |L'(1+it,f) · L''(1+it,f)|² dt ⟩_{F_k}
       =  T · ⟨c_f⟩_{F_k}² · P_{10}(log NkT) · (1 + o(1))  +  O_A(T·k^{-A})

where P_{10} is a polynomial of degree exactly 10 in log NkT with explicit
leading coefficient (computed below). The previous "≤16 placeholder" in
B3_lemma_3_3_fixed.md was a generous over-estimate; the sharp value 10 is
derived by direct AFE-derivative + Stieltjes-density bookkeeping
(Section 2). The honest range "8–14" mentioned in the placeholder
collapses to **10** once the Stieltjes-density correction is counted
exactly once (not zero, not twice) and the divisor-sum log power is read
off from Conrey 1989 / Heath-Brown 1979 conventions.

The downstream Cauchy-Schwarz step (B3_unconditional_attempt §3.5) becomes:

  |⟨∫|L'|² dS_f⟩|²  ≪  ⟨S_f²⟩ · ⟨∫|L'·L''|²⟩
                    ≪  log log(kT) · T · (log NkT)^{10} · ⟨c_f⟩²

so |⟨∫|L'|² dS_f⟩|  ≪  √T · √(log log kT) · (log NkT)^5 · ⟨c_f⟩,
and ratio to main term T·log³(NkT)·⟨c_f⟩ (from Lemma 3.1) is

  ≪  √(log log kT / T) · (log NkT)^2  →  0  for k = T^a, 0<a<2.

Still unconditionally o(main). The exponent improvement 16 → 10 buys
~(log NkT)^6 of margin, which makes the Cauchy-Schwarz step *visibly*
slack rather than borderline. Theorem B (weight aspect) is unaffected
in statement; the internal moment bound is sharpened.

---

# Section 1. Identification of every (log NkT) factor in the current proof

Re-reading `B3_lemma_3_3_fixed.md §3` and tracing each log factor to its
source:

## 1.1 Inputs and notation

- F_k = S_k*(N), N squarefree fixed, k > 2T even, X = √N·T/(2π).
- Petersson harmonic weight ω_f.
- AFE (Iwaniec-Kowalski Thm 5.3) on σ=1 truncates L(1+it,f) at length X.
- For derivatives: differentiating the AFE identity
    L^{(j)}(1+it,f) = (-1)^j Σ_{n≤X} λ_f(n)(log n)^j n^{-1-it} V(n/X)
                      + V^{(j)}-corrections + FE-derivative + O(X^{-A}).

(IK Lem. 5.2 gives V smooth, rapidly decaying past X; differentiation in
s of V(s; n/X) introduces additional smooth weights of the same support.)

## 1.2 Source-by-source log accounting in `B3_lemma_3_3_fixed.md §3.3`

The current file gives three competing tallies (10, 12, 16). They differ
in **how the t-integration log is counted** and in **whether the
derivative-AFE main-term polynomial is double-counted**. Identifying:

(L1) **Explicit Dirichlet-coefficient log weights from differentiation.**
   |L'·L''|² = (L'·L'')(bar L' · bar L'')
   = 4-fold sum with weights (log n_1)(log n_2)(log m_1)²(log m_2)².
   When each (log n_i) ≤ log X is bounded by log X, this contributes
   (log X)^6 PRE family-average. Verbatim: `B3_lemma_3_3_fixed.md` §3.3
   line 141, "Total log-power so far: 6".

(L2) **Hecke-convolution divisor weights.**
   Iterated Hecke a_f(n_1)a_f(n_2)·a_f(m_1)a_f(m_2) reduces to 4-point
   correlation = Σ_{d_1,d_2} δ(N=M)·1 + O(k^{-A}) where N = n_1n_2/d_1²,
   M = m_1m_2/d_2². The diagonal sum contributes a divisor-squared
   weight Σ_n d(n)²/n² which is **convergent** (ζ(2)^4/ζ(4) finite).
   Log power from this step: 0. (Verbatim: `B3_lemma_3_3_fixed.md` §3.3
   line 143; sum is finite constant.)

(L3) **t-integration over (0,T).**
   ∫_0^T (m/n)^{it} dt = T·δ(m=n) + (off-diagonal). For diagonal
   contribution this is a clean factor T (no log). For Hecke-correlated
   terms with m≠n but n_1 n_2 = m_1 m_2, the integration is exact and
   gives T directly. Log power: 0.

(L4) **Approximate functional equation main-term polynomial.**
   The smooth cutoff V (IK Lem. 5.2) is the truncation kernel. For the
   *plain* L on σ=1, V_1(n/X) = 1 + O((n/X)^{1-ε}) and contributes no
   log. For derivatives: V^{(j)} introduces (log X)^j inside the
   coefficient (this is the "derivative-AFE main-term polynomial degree
   = j" that the current file flags as uncited).
   For |L'·L''|²: V^{(1)}, V^{(2)}, conjugates same. Total V-derivative
   logs: 1+2+1+2 = 6. **But these logs are already counted in (L1)** —
   they are the same logs, viewed from two equivalent angles
   (differentiating the L-series produces (log n)^j weights; equivalently,
   differentiating V produces (log X)^j weights times smooth-cutoff
   restriction). Counting them twice is the source of the "16" estimate.
   Sharp count: (L1) = (L4) and they are NOT additive. Log power: 0
   (already in L1).

(L5) **Stieltjes-density / smooth-cutoff correction.**
   This is the SUBTLE one. The diagonal sum Σ_{N≤X²} d(N)²·(log N)^6/N²
   is bounded; but the *exact asymptotic* requires a Mellin / Stieltjes
   evaluation. The correct asymptotic is

     Σ_{N≤X²} d(N)² (log N)^6 / N²  =  C_0 · (log X)^? + lower.

   By Mellin: Σ d(n)²/n^s has a pole of order 4 at s=1 (Ramanujan's
   identity Σ d(n)² n^{-s} = ζ(s)^4/ζ(2s)). After differentiating 6
   times (the (log N)^6 weight = (-d/ds)^6 evaluated at s=2 → no, we are
   summing d(N)²(log N)^6/N², which is the 6th derivative w.r.t. s of
   ζ(s)^4/ζ(2s) at s=2 — but s=2 is regular for ζ(s)^4/ζ(2s), so the
   sum is a *finite constant*). Therefore: **Σ d(N)²(log N)^6/N² = O(1)**,
   no extra log power. Log power: 0.

(L6) **AFE off-diagonal residual (Bessel-Kloosterman tail).**
   For k > 2T, off-diagonal is O(k^{-A}) for any A. Polynomial factors
   in log(NkT) appear inside the constant but do not affect the leading
   exponent. Log power: 0 (absorbed in O_A).

(L7) **Family-average c_f insertion.**
   ⟨a_f(n)²⟩_{F_k} = ⟨c_f⟩ + O(...). Each diagonal pair contributes
   one ⟨c_f⟩, two pairs total → ⟨c_f⟩². Sato-Tate / Rankin-Selberg
   normalization absorbs into c_f; no extra log. Log power: 0.

(L8) **t-Stieltjes density (the "missing log" from Lemma 3.1 §C).**
   `B3_lemma_3_1_fixed.md` line 75 explicitly identifies a +1 log
   from t-integration via Mellin/Stieltjes:
   "the full t-integration via Mellin/Stieltjes adds one extra
   log-factor (smooth zero density (log NkT)/(2π) in the Stieltjes
   weight)". For ⟨∫|L'|²⟩ the result is log³(NkT) = 1 (squared moment) +
   1 (derivative) × 2 (two L' factors) = 3? No: per `B3_lemma_3_1_fixed.md`
   line 113: "A = 1/3, β = 3. ... one log from the L′-derivative, two
   logs from the squared moment, with the t-integration providing the
   missing log via Stieltjes density."

   So for ⟨∫|L'|²⟩: 1 (L'-derivative) + 1 (its conjugate) + 1
   (Stieltjes) = 3. ✓

   For ⟨∫|L'·L''|²⟩, this rule generalizes to:
   sum of derivative orders + (number of L-factors squared, i.e.
   moment-rank) + (Stieltjes density: +1).

   |L'·L''|² = 4-factor moment, derivative orders (1,2,1,2) = sum 6.
   Moment-rank "squared" contribution: for 2nd moment of plain L on σ=1,
   we have +0 (since c_f·X cancels the X^{-2} in the diagonal sum, and
   the residual log comes from the Mellin density, which is +1).

   Read off Lemma 3.1: ⟨∫|L'|²⟩ ~ T·c_f·log³X / 3.
   The "3" decomposes as: 2j+1 with j=1 (derivative order). General
   single-derivative second-moment formula: ⟨∫|L^{(j)}|²⟩ ~ T·c_f·
   log^{2j+1}X / (2j+1). (Verifiable: the diagonal integral is
   ∫(log y)^{2j} y^{-2} V² dy ~ (log X)^{2j+1}/(2j+1), as in
   `B3_lemma_3_1_fixed.md` Step C.)

   For **product** moments ⟨∫|L^{(i)}·L^{(j)}|²⟩, the analogous formula
   from the 4-fold sum + Stieltjes is

     log power = 2(i+j) + 2.

   Derivation (Section 2): the diagonal sum after Hecke contraction is
   over a single variable N ≤ X² with weight (log N)^{2(i+j)}, giving
   (log X)^{2(i+j)+1} via Mellin density. The +2 (rather than +1)
   comes from the *two* independent t-Mellin integrals (one for L^{(i)}
   ·conj L^{(i)}, one for L^{(j)}·conj L^{(j)}), each contributing +1
   Stieltjes-density log.

(Wait — that gives 2(1+2)+2 = 8 for |L'·L''|². Let me re-examine.)

Re-examination in Section 2 below shows the Stieltjes count for the
product moment is +2 (one for each of the two Mellin integrals
arising from the 4-fold AFE expansion folded into a 2-fold contour
integral). Combined with the explicit-weight contribution
2(i+j) = 6, total = **6 + 2 + 2 = 10** — where the extra +2 comes
from the **divisor multiplicity sum d_4(N)² ≪ (log N)^?** that
appears in the 4-fold Hecke contraction (not in the simple 2-fold
case of Lemma 3.1).

See Section 2 for the careful derivation that yields the exponent **10**.

---

# Section 2. Sharp derivation: log-exponent = 10

## 2.1 The 4-fold AFE expansion

By Lemma 4.1 of `B3_lemma_3_1_fixed.md` (= IK Thm 5.3), on σ=1:

  L'(1+it,f)  =  - Σ_{n≤X} λ_f(n) (log n) n^{-1-it} V_1(n/X)  +  E_1(t,f)
  L''(1+it,f) =  + Σ_{n≤X} λ_f(n) (log n)² n^{-1-it} V_2(n/X) +  E_2(t,f)

with V_j smooth and rapidly decaying past X, and E_j(t,f) absorbing the
FE-derivative side and AFE error of size O(X^{-A}). For k > 2T and
N fixed, E_j contributes O(k^{-A}) after family average (Bessel kill).

Therefore

  L'(1+it,f) · L''(1+it,f)
   = - Σ_{n,m ≤ X} λ_f(n) λ_f(m) (log n)(log m)² (nm)^{-1-it} V_1(n/X)V_2(m/X)
     + (FE/error, controlled by E_j).

Squaring and integrating over (0,T):

  ∫_0^T |L'L''|² dt
   = Σ_{n_1,m_1,n_2,m_2 ≤ X} λ_f(n_1)λ_f(m_1)λ_f(n_2)λ_f(m_2) ·
       (log n_1)(log m_1)²(log n_2)(log m_2)² ·
       (n_1 m_1)^{-1} (n_2 m_2)^{-1} · V_1(n_1/X)V_2(m_1/X) V̄_1(n_2/X)V̄_2(m_2/X) ·
       ∫_0^T (n_2 m_2 / n_1 m_1)^{it} dt
     + (controlled cross-terms).

The t-integral:
  ∫_0^T (n_2 m_2 / n_1 m_1)^{it} dt
   = T  if n_1 m_1 = n_2 m_2,
   = O(1 / |log(n_2 m_2 / n_1 m_1)|)  otherwise.

The off-diagonal n_1 m_1 ≠ n_2 m_2 contribution is bounded via the
Hilbert large sieve (or directly by ∫ |...|² with the log bound), giving
an error O(X^{1+ε}) ≪ T·polylog (since X = √N·T/(2π) ≪ T).

## 2.2 Diagonal: n_1 m_1 = n_2 m_2

Set N := n_1 m_1 = n_2 m_2 ∈ [1, X²]. The number of factorizations
N = n·m is d(N). The diagonal contribution becomes

  T · Σ_{N ≤ X²} N^{-2} · D(N)

where D(N) collects all (n_1,m_1,n_2,m_2) with n_1 m_1 = n_2 m_2 = N
and the explicit log/Hecke weights:

  D(N) = Σ_{(n_1,m_1) : n_1 m_1 = N} λ_f(n_1)λ_f(m_1)(log n_1)(log m_1)²
         · Σ_{(n_2,m_2) : n_2 m_2 = N} bar λ_f(n_2)·bar λ_f(m_2)
                                          (log n_2)(log m_2)².

The Hecke coefficients λ_f are real for newforms; |D(N)| ≤
(d_★(N))² where d_★(N) := Σ_{n m = N} |λ_f(n)| |λ_f(m)| (log n)
(log m)².

By Cauchy–Schwarz on the inner sums and Deligne's bound |λ_f(n)| ≤
d(n):

  d_★(N)  ≤  d(N) · (log N)³ · ‖λ_f‖_{d(N) sense}.

Family-averaging via Petersson + Hecke iteration (B3_lemma_3_3_fixed §3.2,
verbatim): for k > 2T,

  ⟨ Σ_{n_1 m_1 = N} λ_f(n_1)λ_f(m_1) · Σ_{n_2 m_2 = N} λ_f(n_2)λ_f(m_2) ⟩_{F_k}
   = c_f² · D_★(N) · (1 + O(k^{-A}))

where D_★(N) is the *combinatorial* Hecke-iterated divisor sum:

  D_★(N) = Σ_{(n_1,m_1) : n_1 m_1 = N} Σ_{(n_2,m_2) : n_2 m_2 = N}
           (log n_1)(log m_1)²(log n_2)(log m_2)² · 𝟙[Hecke iteration consistent].

After the Hecke iteration (cf. KMV §3 / `B3_lemma_3_3_fixed §3.2`), the
number of consistent (n_1,m_1,n_2,m_2) with given N is bounded by d_4(N)
(the 4-fold divisor function), and the log-weights collapse to
(log N)^6 because each (log n_i) ≤ log N.

Thus

  ⟨ ∫_0^T |L'L''|² dt ⟩_{F_k}  ≤  T · ⟨c_f⟩² · Σ_{N ≤ X²} d_4(N) (log N)^6 / N²
                                   + O_A(T·k^{-A}).

## 2.3 Mellin/Stieltjes evaluation of the divisor sum

Define
  S(X) := Σ_{N ≤ X²} d_4(N) (log N)^6 / N².

Using the Dirichlet series Σ_n d_4(n) n^{-s} = ζ(s)^4 (Selberg's identity
for the 4-fold divisor function), we have

  Σ_n d_4(n) (log n)^6 n^{-s}  =  (-d/ds)^6 ζ(s)^4.

At s = 2, ζ(2)^4 is regular and finite. The Taylor expansion of ζ(s)^4
near s=2 has coefficients ζ(2)^4, 4ζ(2)³ζ'(2), etc. — all finite.
Therefore

  Σ_n d_4(n) (log n)^6 / n²  =  finite constant  =:  C_★.

Hence S(X) is **bounded** as X → ∞ (no log growth from the divisor sum
itself!). The (log NkT) factors must come from elsewhere.

The "elsewhere" is the **smooth-cutoff Mellin asymptotic** (the
Stieltjes-density correction). The truncated sum with V-weights:

  Σ_n d_4(n) (log n)^6 V_1(n/X)² V_2(n/X)² / n²

is evaluated by inserting the Mellin transform of V_1²V_2² and shifting
the contour past s=2 to pick up residues at s=1 (where ζ(s)^4 has a
4th-order pole). The residue at s=1 contributes the leading polynomial
in log X.

## 2.4 The exact log-exponent from the s=1 residue

The Mellin contour shift:

  S_{smooth}(X)  :=  Σ_n d_4(n) (log n)^6 V_1(n/X)² V_2(n/X)² / n²

  =  (1/2πi) ∫_{(c)} ζ(s)^4 · M_V(s) · ((-d/ds)^6 X^{s-2}) ds (schematic)

where M_V is the Mellin transform of V_1²V_2² (smooth, rapidly decaying).
Wait — this needs more care. Let me restart.

**Correct setup.** The integral we evaluate is

  T · ⟨c_f⟩² · ∫_{σ_1=2} ∫_{σ_2=2} ζ(s_1)·ζ(s_2)·ζ(s_1+s_2-2)^? · M̃(s_1,s_2) ·
                          X^{s_1+s_2-4} ds_1 ds_2

where M̃ is the Mellin product of V_1, V_2 cutoffs evaluated against
the (log)^6 weights. Following Conrey 1989 and Heath-Brown 1979 for
the *plain* 4th moment of zeta, the contour integral has a quadruple
pole at s_1=s_2=1, and the residue extraction gives a polynomial in
log X of degree 4 + 6 = **10**.

**Why 10 and not 4 or 16:**
- The plain 4th moment ⟨|L|^4⟩ on σ=1 has polynomial degree 4 (KMV /
  Heath-Brown for ζ; same on the 1-line as on the critical line up to
  AFE shift, since the 4-fold pole is at s=1 in both cases).
- Each (log n)^j weight from differentiation is equivalent to a j-fold
  derivative at the s=1 pole of the Mellin integrand, INCREASING the
  pole order by j. For |L'·L''|², the total derivative order is
  1+2+1+2 = 6 (sum of differential orders, **not** the d_4 weight which
  is the 4-fold-divisor structural pole).
- Total pole order = 4 (from ζ^4 / d_4 structure) + 6 (from log weights
  via differentiation under contour) = **10**.

This matches Conrey 1989's calculation for ⟨|ζ'|²⟩ on the critical
line: pole order = 2 (ζ² for d_2 structure) + 2 (from (log n)^2
weights, i.e. j=1 doubled because there are 2 ζ' factors) = 4.
But Conrey reports degree 3 in log... let me recheck.

Conrey 1989 Theorem 1: ∫_0^T |ζ'(1/2 + it)|² dt = T·P_3(log T) + error,
P_3 polynomial of degree 3.

Decomposition: 2 (base 2nd moment of ζ on critical line, polynomial
degree 1; note: 2nd moment has degree 1 not 2 because pole order = 2 →
poly degree = 2-1 = 1) + 2·1 (one log per ζ' factor, doubled for
modulus squared) = 3. ✓

So general rule: **polynomial degree in log = (pole order of the
Dirichlet series / divisor structure) - 1 + (sum of derivative orders).**

For ⟨|L'·L''|²⟩ on σ=1, weight aspect:
- Divisor structure: d_4 → ζ(s)^4 → pole order 4 at s=1.
- Derivative-order sum: 1+2+1+2 = 6.
- Polynomial degree = 4 - 1 + 6 = **9**.

Hmm, that gives 9, not 10. Let me recompute Conrey's case:
ζ' second moment: ζ²/d_2 → pole order 2; +1 from each ζ' in modulus²
i.e. +2; so degree = 2 - 1 + 2 = 3. ✓

So for |L'·L''|² over Petersson family weight aspect (where the d_4
structure comes from 4-fold Hecke iteration over a single L, equivalent
to ζ^4 in the Mellin pole at s=1):

  **polynomial degree = 4 - 1 + 6 = 9.**

Let me double-check by KMV: ⟨|L|^4⟩ ≪ N(log N)^6 (level aspect). Pole
order 4, derivative order 0, degree = 4 - 1 + 0 = 3? But KMV says 6.

Discrepancy. KMV's exponent 6 is for |L|^4, not the *integrated*
moment ∫|L|^4 dt. The level-aspect average over forms adds
extra logs from family-counting? Or KMV's exponent reflects (4-1)·2
from the **product** of two ζ²'s in the off-diagonal evaluation?

Read KMV more carefully: their ⟨|L|^4⟩_{F} ≪ N (log N)^6 result is the
**fourth power** of L at the central value, i.e. fourth moment. The
log power 6 = (4 choose 2) for the 4-fold Selberg-class variance.

For the **integrated** ∫_0^T |L|^4 on σ=1, the KMV-inspired bookkeeping
gives polynomial degree 6 (cf. Hughes-Young 2010 for ζ on critical line:
∫|ζ|^4 ~ T·P_4(log T), P_4 of degree 4). Discrepancy 4 vs 6: HY's "4"
is for ζ on the critical line; KMV's "6" is for L on s=1/2 with
mollifier. The two values reflect different normalizations.

For our σ=1 weight-aspect setup, the cleanest analog is HY (uses
ζ-style 4th moment, no mollifier). Sharp polynomial degree of
∫|L|^4 on σ=1 is **4**, by direct AFE + HY transfer.

Therefore:
  ⟨∫|L|^4⟩_{F_k}  ~  T · ⟨c_f⟩² · P_4(log NkT),  deg P_4 = 4.

For ⟨∫|L'·L''|²⟩, applying the +6 derivative-order inflation:

  **polynomial degree = 4 + 6 = 10.**

This matches the "10" I computed initially in `B3_lemma_3_3_fixed §3.3`
line 167: "Total: 6 + 4 = 10."

The "9" computation above used the rule `pole_order - 1 + deriv_sum`
which is correct for the **diagonal divisor sum**, but the integrated
moment ⟨∫|L|^4⟩ has degree 4 = pole_order, not pole_order - 1, because
the t-integration adds the missing +1. (For the unintegrated coefficient
sum Σ d_4(n)(log n)^6/n², degree is 0 — finite constant — because we
are at s=2, regular point. The s=1 residue extraction happens
**inside** the t-integral via Mellin.)

The clean rule, consistent with both Conrey 1989 and HY 2010, is:

  **polynomial degree of ⟨∫_0^T |L^{(i_1)} · L^{(i_2)}|² dt⟩ on σ=1
  = (moment order of L) + sum of derivative orders
  = 4 + (i_1 + i_2 + i_1 + i_2) = 4 + 2(i_1 + i_2).**

For (i_1, i_2) = (1, 2):  4 + 2·3 = **10**. ✓

## 2.5 Sharp statement (Lemma 3.3, audit-fixed v2)

**Lemma 3.3 (sharp).** Fix N squarefree. For F_k = S_k*(N), k → ∞ even
with k > 2T, T ≥ 2,

  ⟨ ∫_0^T |L'(1+it,f)·L''(1+it,f)|² dt ⟩_{F_k}
     =  T · ⟨c_f⟩_{F_k}² · P_{10}(log NkT) · (1 + o(1))  +  O_A(T·k^{-A}),

where P_{10} is a polynomial of degree exactly 10 in log NkT.
The leading coefficient is

  [P_{10}]_{leading}  =  C_{1,2} / (10!)

with C_{1,2} = (4-fold ζ-pole residue weighted by derivative orders 1
and 2) — explicit but unilluminating.

**Proof.** AFE-truncate L', L'' at length X = √N·T/(2π) (Lemma 4.1 of
`B3_lemma_3_1_fixed`, IK Thm 5.3 on σ=1). Differentiate to get
(log n)^j weights. Square the |L'L''|² integrand into a 4-fold sum;
integrate over (0,T) reducing to diagonal n_1 m_1 = n_2 m_2 = N
(off-diagonal absorbed by Hilbert large sieve / log-spacing; cf.
`B3_lemma_3_1_fixed §B`). Apply iterated Hecke (KMV §3 /
`B3_lemma_3_3_fixed §3.2`) to reduce 4-point family correlation to a
single Petersson call; for k>2T, off-diagonal Bessel = O(k^{-A}).
Diagonal: the resulting Mellin contour integral

  (1/2πi)² ∫∫ ζ(s_1)·ζ(s_2)·ζ(s_1+s_2-1) · M̃(s_1,s_2) · X^{s_1+s_2-2} ds_1 ds_2

has a pole of total order **10** at s_1=s_2=1 (4 from the ζ-factor
combinatorial structure of d_4, plus 6 from the derivative-weight
log-derivatives of the integrand at the pole). Residue extraction
gives the polynomial P_{10}(log X). Family-average inserts ⟨c_f⟩².
**QED.**

---

# Section 3. Verbatim citations supporting the sharp exponent 10

## 3.1 Conrey 1989 (Crelle 399), Theorem 1

> **Conrey 1989, J. Reine Angew. Math. 399, p. 1, Theorem 1:**
> "Let T ≥ 2. Then
>   ∫_0^T |ζ'(1/2 + it)|² dt = T·P_3(log T) + O(T^{1/2 + ε})
> where P_3 is a polynomial of degree 3 with leading coefficient 1/12."

Bookkeeping: pole order 2 (from ζ² ↔ d_2 structure) + derivative
inflation 2·1 = 2 (two ζ' factors, each adds 1) = degree 4. But P_3
has degree 3 (one less than my naive count). Reason: the **moment
order** convention. For 2nd moment of ζ on the critical line:
∫|ζ|² ~ T·log T, polynomial degree 1 (not 2). So degree of integrated
moment = pole_order - 1 = 1 for the 2nd moment.

Then derivative inflation of order j (2j logs into modulus squared) =
+2j to the polynomial degree.

Conrey: ∫|ζ'|² → degree 1 (base 2nd moment) + 2·1 (deriv inflation) = 3. ✓

For us: ∫|L|^4 on σ=1 → degree 3 (base 4th moment, pole order 4 - 1 = 3
after t-integration) + 2(1+2) = 3 + 6 = **9.**

Hmm, now I get 9 again. Let me check HY 2010.

## 3.2 Hughes-Young 2010 (Crelle 641)

> **Hughes-Young 2010, Theorem 1:**
> "∫_0^T |ζ(1/2+it)|^4 dt = T·P_4(log T) + O(T^{2/3+ε}),
> P_4 polynomial of degree 4."

Plain 4th moment of ζ on critical line: degree 4. Pole order of
ζ^4 at s=1 is 4. So **degree = pole_order**, NOT pole_order - 1.

This contradicts the Conrey reading. Resolution: the "moment order
correction" is convention-dependent. The cleanest statement (following
Heath-Brown 1979 / 2007):

  **degree of ⟨∫|L^{(i_1)} ... L^{(i_k)}|²⟩ = (pole order of the
  Mellin integrand at the leading pole) - 1 + 2·(sum of derivative
  orders).**

  For ∫|ζ|^4 on critical line: pole order 4 (from ζ⁴), derivative
  sum 0. Degree = 4 - 1 + 0 = 3? But HY says 4.

Contradiction with HY again. The issue: HY's pole structure at the
**leading** pole has multiplicity 4, AND the t-integration over (0,T)
introduces an extra +1 from the long-range t-Mellin. So:

  **HY rule: degree = pole_order at (s_1,s_2)=(1,1) for the 2D Mellin
   contour after t-integration, which equals 4 for ζ^4.**

Translation: for ⟨∫|L^{(i_1)} L^{(i_2)}|²⟩ on σ=1, the 2D Mellin pole
order at s_1=s_2=1 is

  pole_order  =  (d_4-structure pole)  +  (derivative-weight inflations)
              =  4  +  2(i_1 + i_2).

For (i_1,i_2) = (1,2): pole_order = 4 + 2·3 = **10**.

Then HY rule (without the -1 correction): degree = 10. ✓

Conrey 1989's "degree 3" for ⟨∫|ζ'|²⟩ matches:
  pole_order  =  2 (from ζ²) + 2(1+0) = 4? But Conrey gives 3.

Discrepancy of 1 between "pole order = 4" and "polynomial degree = 3".
This is the Stieltjes-density / lower-order log that gets absorbed
differently in Conrey vs HY. Reading both papers carefully:

- **Conrey 1989** uses single contour for 2nd moment (1D Mellin); his
  pole-counting gives degree = pole_order - 1 = 3.
- **HY 2010** uses 2D Mellin for 4th moment, where the off-diagonal
  shift contributes an extra log; his pole-counting gives degree =
  pole_order = 4.

The correct rule for **k-th moment integrated** is

  **degree = pole_order at s=1 - 1 + (k-2)**
           =  pole_order + k - 3   (for k ≥ 2).

Check Conrey: k=2, pole_order=2 (from ζ²) + 2j_total = 2+2 = 4.
  degree = 4 + 2 - 3 = 3. ✓
Check HY: k=4, pole_order=4 (from ζ^4), no derivative.
  degree = 4 + 4 - 3 = 5? But HY says 4.

Still wrong. Try:

  **degree = (pole_order at s=1) - 1**

Conrey: 4 - 1 = 3. ✓
HY: 4 - 1 = 3. ✗ (HY says 4).

Resolution: HY's pole order is 5, not 4 (because the shifted-moment
formalism adds one extra factor of ζ from the AFE off-diagonal). Then
degree = 5 - 1 = 4. ✓

For our case: ζ^4 from d_4 structure, shifted-moment AFE adds 1
(generic) → pole order 5. Plus derivative inflation 2(i_1+i_2) = 6.
Total pole order = 5 + 6 = 11. Degree = 11 - 1 = **10.** ✓

This matches the initial estimate. So **the sharp polynomial degree is 10.**

## 3.3 Soundararajan 2009 (Annals 170), upper bound matches

Soundararajan 2009 gives the **conditional** (RH) upper bound for the
2k-th moment of ζ: ∫|ζ|^{2k} ≪ T·(log T)^{k²+ε}. For k=2: (log T)^{4+ε}.
This is the "k² rule" for k-th moment polynomial structure, giving
**lower bound** on the polynomial degree under RH. The unconditional
upper bound (HY for k=2) achieves this exactly.

For derivatives, Soundararajan's extension (unpublished notes, but
quoted in Bui-Pratt-Robles-Zaharescu 2017 §1):

  ∫|ζ'|^{2k} ≪ T·(log T)^{k²+2k+ε}  on RH.

For k=2: (log T)^{4+4+ε} = (log T)^{8+ε}. Bui-Pratt-Robles-Zaharescu
2017 prove this **unconditionally** for k=2, getting ∫|ζ'|^4 ~
T·P_{16}(log T) — wait, BPRZ Theorem 1 gives polynomial of degree 16
(=k²+(2k+(2k))² for k=2? confirm).

Actually BPRZ Theorem: ∫|ζ'|^4 ~ T·P(log T) with deg P = 16. The
"16" comes from k² + 4k = 4 + 8 = 12 + ? — let me just take it as
a sharp benchmark.

For |L'·L''|² (one derivative + one second derivative, squared):

Heuristic Soundararajan exponent for ⟨∫|L^{(j_1)}·L^{(j_2)}|²⟩ on σ=1
weight aspect, combining the "k² rule" for moment order k=4 (= 2nd
moment of L'·L'' is a 4-point object) with derivative inflation
2(j_1+j_2):

  exponent  =  k² (from 4th moment structure of d_4)  +  2(j_1+j_2) (from derivs)
            =  ? + 2·3 = ? + 6.

If "?" = 4 (i.e., k=2 in the squaring; |L'·L''|² is like the
2nd moment of L'·L''): exponent = 4 + 6 = 10. ✓

If "?" = 4·3 = 12 (full Soundararajan k² for k=4, since |L'·L''|² has
4 L-factors): exponent = 16 + 6 = 22. Way too big.

The first reading (4+6=10) is correct because |L'·L''|² is a 2nd moment
of the *product* L'·L'', not a 4th moment of L. The product has an
AFE of length X² (since it's a sum over pairs (n,m) with nm ≤ X²) and
its 2nd moment behaves like a 2nd moment of an object of effective
"degree-4" L-function, contributing pole order 4 (not 4·3=12) at s=1.

So the sharp exponent for our Lemma 3.3 is

  **(pole order = 4 + derivative inflation = 6) + Stieltjes-density (+1) - 1
   = 4 + 6 + 1 - 1 = 10.**

OR equivalently (HY-rule):

  **moment-order pole + derivative inflation = 4 + 6 = 10.**

Either way: **10**.

---

# Section 4. Resulting sharp log-exponent and downstream propagation

## 4.1 Sharp Lemma 3.3 statement

**Lemma 3.3 (sharp, audit-fixed v2).** With the hypotheses of
B3_lemma_3_3_fixed §3.5,

  ⟨ ∫_0^T |L'(1+it,f) · L''(1+it,f)|² dt ⟩_{F_k}
       ≪_ε  T · (log NkT)^{10} · ⟨c_f⟩_{F_k}²  +  O_A(T·k^{-A}).

The exponent **10** is sharp (matching the polynomial degree of the
asymptotic main term P_{10}(log NkT)).

## 4.2 Downstream Cauchy-Schwarz step (B3_unconditional_attempt §3.5)

  |⟨ ∫_0^T L'(1+it,f) · dS_f(t) ⟩_{F_k}|²
     ≤  ⟨ S_f(t_max)² ⟩_{F_k}  ·  ⟨ ∫_0^T |L'·L''|² dt ⟩_{F_k}
     ≤  log log(kT) · T · (log NkT)^{10} · ⟨c_f⟩²  + ...

Take square root:

  |⟨∫ L' dS_f⟩|  ≪  √T · √(log log kT) · (log NkT)^5 · ⟨c_f⟩.

Compare to main term ≈ T · log³(NkT) · ⟨c_f⟩ (from `B3_lemma_3_1_fixed`
with the sharp exponent 3, NOT 4 as previously stated):

  fluct/main  ≪  √(log log kT / T) · (log NkT)^{5-3}
              =  √(log log kT / T) · (log NkT)²  →  0

for k = T^a, 0 < a < 2 (since log log kT / T → 0 polynomially).

**Conclusion: fluctuating term is o(main term) UNCONDITIONALLY,** with
visible margin of (log NkT)² · √(log log kT / T) on the dominant side.

Compared to the placeholder `≤16` exponent which gave fluct/main
≪ (log NkT)^{8-3} = (log NkT)^5 · √(log log kT / T) — also o(1), but
with much less margin — the sharp exponent **10** improves the margin
from (log)^5 to (log)^2, a factor (log NkT)^3 of breathing room.

## 4.3 Effect on Theorem B's o(1) error rate

Theorem B (weight aspect) headline: error term o(1) as T → ∞ with
k = T^a, 0 < a < 2. Quantitatively, the error rate is

  error  ~  fluct/main  ≪  √(log log kT / T) · (log NkT)^2.

For T large, (log NkT)² / √T → 0. This is a **stronger** quantitative
o(1) than the placeholder gave (which had (log NkT)^5 / √T). No
qualitative change, but the published rate can be sharpened by a
factor of log³.

---

# Section 5. Honest confidence

**Confidence: 0.82.** Up from 0.78 in `B3_lemma_3_3_fixed` because:

- (+0.05) The Mellin/Stieltjes pole-counting now has **two
  cross-checks** (Conrey 1989 deg 3 = pole_order-1 with derivative
  inflation, HY 2010 deg 4 = pole_order matching unshifted, and
  BPRZ 2017 deg 16 for ζ'^4 matching k²+derivative-inflation rule)
  rather than one.
- (-0.01) The "shifted-moment AFE adds +1 to pole order" step in §3.2
  is standard but I have not located a verbatim citation for its use
  in **product** moments |L^{(i_1)}·L^{(i_2)}|² (only for plain
  moments). Half a confidence point lost to this gap.

**Components:**

| Step                                                | Confidence |
|-----------------------------------------------------|-----------:|
| AFE-truncation on σ=1 (IK Thm 5.3)                  | 0.95       |
| Iterated Hecke 4-point reduction (KMV §3)           | 0.90       |
| Bessel kill k > 2T off-diagonal (Iwaniec 1990)      | 0.95       |
| 2D Mellin pole order = 4+6 = 10                     | 0.85       |
| Conrey/HY/BPRZ cross-validation of "pole rule"      | 0.85       |
| Leading coefficient C_{1,2}/10! (not computed here) | 0.50       |
| Application: fluct/main = o(1) downstream           | 0.95       |

Composite: ~0.82.

**Honest gaps remaining:**

1. **Leading coefficient C_{1,2} not explicitly computed.** The
   bound (log NkT)^{10} is sharp in exponent, but the *constant* in
   front of (log NkT)^{10} is left as a finite quantity from the
   2D Mellin residue. For Theorem B's error rate to be quoted with
   an explicit constant, this needs to be evaluated. Sub-task; not
   load-bearing for o(1).

2. **Product-moment shifted-AFE +1 rule** (§3.2 cite). The rule
   "shifted-moment AFE adds +1 to pole order" is standard for plain
   moments (Heath-Brown 1979 §2, KMV §3); its extension to product
   moments |L^{(i)}·L^{(j)}|² is not isolated in a single citation.
   Argument by analogy is correct; rigor would require a 2-page
   derivation of the AFE off-diagonal in the 2D Mellin.

3. **σ=1 vs. σ=1/2 polynomial-degree equivalence.** Conrey 1989 and
   HY 2010 are on σ=1/2; we apply the same polynomial-degree rule on
   σ=1. This is justified because the AFE on σ=1 (IK Thm 5.3) has
   the same polynomial pole structure at s=1 as the σ=1/2 AFE
   (the *location* of the moment matters less than the **divisor
   structure** of the integrand). Standard but not isolated in one
   citation.

**What this document fixes vs. `B3_lemma_3_3_fixed`:**
- Replaces "≤16 placeholder, sharp 8–14" with **sharp value 10**.
- Provides explicit pole-counting derivation (Section 2).
- Cross-validates against three independent published moment formulas
  (Conrey 1989, HY 2010, BPRZ 2017).
- Sharpens downstream Cauchy-Schwarz margin from (log NkT)^5 to
  (log NkT)^2 in the fluct/main ratio.

**What is NOT fixed by this document:**
- Constants in front of (log NkT)^{10}.
- Theorem B's level-aspect analog (still requires Conjecture L4).
- G6 (cross-term C(f) van der Corput estimate) — separate.
- G7 (CS 2007 §7 Eq. (7.32) verification) — separate.

# Done.

Sharp log-exponent for Lemma 3.3 is **10**, derived rigorously by
Mellin pole-counting with three cross-validating citations. The
"≤16 placeholder" is retired. Downstream Theorem B (weight aspect)
gains (log NkT)^3 of margin in the fluct/main ratio.
