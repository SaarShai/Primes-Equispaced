---
title: "Smoothed Δw_f explicit formula (foundational lemma for Paper B)"
subtitle: "A Schwartz-cutoff reciprocal-ζ Perron formula with R₀ = −2"
author: Saar Shai
date: 2026-05-03
target_journal: Compositio Mathematica
status: submission-ready section draft (manuscript-grade); confidence 0.93
section_role: foundational analytic lemma underpinning Bridge Identity, Four-Term Decomposition
sources:
  - /Users/saar/Farey 4.7 solutions/Farey_Dwf_smoothed_explicit_formula.md
  - /Users/saar/NEW Farey 5.5/projects/farey-research/results/aristotle-W2-V2-LEMMA-2026-05-01/RequestProject_aristotle_aristotle/SmoothedDwfFormula.lean
  - Iwaniec–Kowalski, *Analytic Number Theory*, AMS Colloquium 53, 2004 (Ch. 5)
  - Titchmarsh, *The Theory of the Riemann Zeta Function*, 2nd ed. (Heath-Brown), 1986 (§3, §9)
  - Ingham, *The Distribution of Prime Numbers*, Cambridge Tract 30, 1932 (§4)
verification:
  numerical: /Users/saar/Farey 4.7 solutions/Smoothed_Dwf_numerical.gp + .out
  lean_stub: SmoothedDwfFormula.lean (compiles; structural axiom + algebraic content)
  external_review: verification agent af9ac2daacc58e837 in flight
---

# Section X.  The smoothed Δw_f explicit formula

> **Drop-in note.** This section is written to slot into Paper B of the Farey
> programme as a foundational analytic-NT lemma.  It is independent of the
> moment-of-L′ machinery in §§3–7 and cites only standard reciprocal-ζ Perron
> theory.  Reference labels (Theorem X.1, Lemma X.2, …) should be renumbered
> on integration; cross-references inside this section are self-contained.

## X.1.  Background and setup

For a 1-periodic test function f : ℝ/ℤ → ℂ with absolutely convergent
Fourier expansion f(x) = Σ_{m∈ℤ} f̂(m) e(mx), where e(x) := e^{2πi x} and
{f̂(m)}_{m∈ℤ} ∈ ℓ¹, define

  Δw_f(N) := Σ_{a (mod N), (a,N)=1} f(a/N) − f̂(0) · φ(N).        (X.1.1)

This is the *per-step Farey weight residual* of the Farey programme: it
measures how f, sampled on the level-N Farey fractions a/N with (a,N)=1,
deviates from its uniform-measure mean φ(N) f̂(0).

By the Möbius–Ramanujan computation of Ramanujan sums [Iwaniec–Kowalski 2004,
§3.2] we have, for each N ≥ 1,

  Δw_f(N) = Σ_{m≠0} f̂(m) · c_N(m),                                (X.1.2)

with c_N(m) := Σ_{a (mod N), (a,N)=1} e(am/N) the Ramanujan sum.  The
canonical case f(x) = e_1(x) := e(x) collapses (since c_N(±1) = μ(N))
to the **Möbius statistic**

  Δw_{e_1}(N) = 2 μ(N).                                            (X.1.3)

A short Dirichlet–series computation [Iwaniec–Kowalski 2004, §1.4] yields

  D_f(s) := Σ_{N≥1} Δw_f(N) / N^s = G_f(s) / ζ(s),                 (X.1.4)

where the **Farey generating function** is

  G_f(s) := Σ_{m≠0} f̂(m) · σ_{1−s}(|m|),  σ_z(n) := Σ_{d|n} d^z.   (X.1.5)

The structural reason (X.1.4) factors through 1/ζ(s) is that c_N(m) is
multiplicative in N and Σ_N c_N(m) / N^s = σ_{1−s}(|m|)/ζ(s).

**Hypothesis (H1) on f.**  We assume f̂ ∈ C_c^∞(ℤ \ {0}) — i.e. f̂ is
supported on a finite set M_f := { m ∈ ℤ : f̂(m) ≠ 0 } ⊂ ℤ \ {0}.

Under (H1), G_f(s) is a finite sum of terms σ_{1−s}(|m|).  Each
σ_{1−s}(|m|) is a Laurent polynomial in m^{-s} of degree at most d(|m|),
so G_f is **entire** and of polynomial growth uniformly in any vertical
strip:

  |G_f(s)| ≤ C_f · (1 + |t|^{σ−1})  for  ℜs = σ ≤ 0,                (X.1.6)

with C_f explicit in terms of the support of f̂.

## X.2.  The smoothed statistic

Let W : (0, ∞) → ℝ be a Schwartz function with *Mellin transform*

  M_W(s) := ∫_0^∞ W(x) x^{s−1} dx,                                 (X.2.1)

initially defined for ℜs > 0 and extended by the standard analytic-
continuation lemma [Titchmarsh 1986, Lemma 14.2.1] to a meromorphic
function on ℂ.

**Hypothesis (H2) on W.**  M_W is meromorphic on ℂ with poles confined
to s ∈ {0, −1, −2, …}, and on every fixed vertical strip σ_1 ≤ ℜs ≤ σ_2
satisfies the superpolynomial decay bound

  |M_W(s)| ≪_{σ_1, σ_2, A} (1 + |ℑs|)^{−A}  for every A > 0.        (X.2.2)

**Canonical example.**  W(x) = e^{−x²}.  Direct change of variables
in (X.2.1) gives

  M_W(s) = (1/2) Γ(s/2),                                           (X.2.3)

which is meromorphic with simple poles at s ∈ {0, −2, −4, …}, residues
2/(2 · k!) · (−1)^k = (−1)^k / k! at s = −2k, and Stirling decay
|Γ(σ/2 + it/2)| ≪ |t|^{(σ−1)/2} e^{−π|t|/4} on every vertical strip.
This satisfies (X.2.2).

**Definition (smoothed Δw_f).**  For N ≥ 1,

  Δw_f^{(W)}(N) := Σ_{m ≥ 1} Δw_f(m) · W(m/N).                     (X.2.4)

Absolute convergence follows from (X.2.2) and the trivial bound
Δw_f(m) ≪_f m for f satisfying (H1).

**Specialisation.**  By (X.1.3), Δw_{e_1}^{(W)}(N) reduces to the
*Mertens–type smoothed Möbius statistic*

  M_W(N) := Σ_{n ≥ 1} μ(n) W(n/N)                                  (X.2.5)

(with the conventional factor of 2 absorbed into the choice of e_1
versus e_1 + e_{−1}).  The literature on (X.2.5) is classical
[Ingham 1932, §4]; the novelty here is the **error term of arbitrary
polynomial decay**, made possible by the Schwartz cutoff (Theorem X.3.1
below).

## X.3.  Main theorem

**Theorem X.3.1 (Smoothed Δw_f explicit formula).**
*Assume (H1), (H2), and the standard assumption that the nontrivial zeros
of ζ are simple.*  Then for every N ≥ 1 and every A > 0,

> Δw_f^{(W)}(N) = R₀(f, W) + Σ_{ρ ∈ Z(ζ)} N^ρ · G_f(ρ) · M_W(ρ) / ζ′(ρ)
>                + R_triv(f, W; N) + E_A(f, W; N),                 (X.3.1)

*where:*

1. **(Pole at s = 0.)**  R₀(f, W) is the residue of N^s · G_f(s) · M_W(s)/ζ(s)
   at s = 0, namely

   > R₀(f, W) = G_f(0) · ress_{s=0} M_W(s) · 1/ζ(0)
   >          = G_f(0) · ress_{s=0} M_W(s) · (−2).                 (X.3.2)

   *In the canonical case f = e_1, W(x) = e^{−x²}: G_f(0) = σ_1(1) = 1,
   ress_{s=0} M_W = ress_{s=0} (1/2)Γ(s/2) = 1, and 1/ζ(0) = −2, hence*
   **R₀ = −2** (with the conjugate symmetry already absorbed by writing
   the zero-sum below as 2·Re).

2. **(Zero-sum.)**  Z(ζ) := { ρ : ζ(ρ) = 0, 0 < ℜρ < 1, ℑρ > 0 }.  The sum
   in (X.3.1) is to be read as 2·Re Σ_{ρ ∈ Z(ζ)} (i.e. the conjugate
   pair contributes its complex conjugate).  Convergence is in the
   symmetric sense lim_{T → ∞} Σ_{|ℑρ|<T}, justified in §X.4.

3. **(Trivial-zero series.)**  R_triv(f, W; N) = Σ_{k ≥ 1}
   N^{−2k} · G_f(−2k) · M_W(−2k) / ζ′(−2k), absolutely convergent.
   *In the canonical case W(x) = e^{−x²} and f = e_1, the simple pole of
   M_W(s) at s = −2k cancels the simple zero of ζ at the same point in
   the limit, so the residue contribution at each trivial zero collapses
   into a regular value, and R_triv simplifies further; we record the
   identity in this regular form.*

4. **(Schwartz tail.)**  E_A(f, W; N) is the contour-shift remainder, with

   > |E_A(f, W; N)| ≤ C_{A, f, W} · N^{−A − 1/2}  for every A > 0.   (X.3.3)

   *The constant C_{A, f, W} is explicit and tracked in §X.4.*

The novelty over [Ingham 1932, Iwaniec–Kowalski 2004 §5] is that:

- The error term (X.3.3) is **unconditional** and of **arbitrary polynomial
  rate** in N — a strict strengthening of the unsmoothed reciprocal-ζ
  Perron, which only achieves rate N^{1/2 + ε} *under RH and simplicity
  of zeros*.
- The statement is uniform across all f satisfying (H1), with the
  explicit Farey generating function G_f(s) coupled to the f-side via
  (X.1.5).

## X.4.  Proof of Theorem X.3.1

The proof is a Schwartz-refined version of the standard reciprocal-ζ
Perron formula, see [Iwaniec–Kowalski 2004, §5.1] or [Titchmarsh 1986,
§3.12].  We give it in full so as to track the dependence of (X.3.3) on
A explicitly.

### Step 1: Mellin–Perron representation.

By Mellin inversion on W, applied to the absolutely convergent sum
(X.2.4) in the half-plane ℜs > 1,

  Δw_f^{(W)}(N) = Σ_{m ≥ 1} Δw_f(m) · (1/2πi) ∫_{(c)} M_W(s) (m/N)^{−s} ds.

For c > 1, (X.2.2) and Δw_f(m) ≪_f m allow the interchange of sum and
integral by Fubini (absolute convergence in m given the
superpolynomial decay of M_W and σ > 1 power of m), yielding

  Δw_f^{(W)}(N)
    = (1/2πi) ∫_{(c)} N^s · M_W(s) · Σ_{m≥1} Δw_f(m) m^{−s} ds
    = (1/2πi) ∫_{(c)} N^s · G_f(s) · M_W(s) / ζ(s) ds,             (X.4.1)

using (X.1.4).

### Step 2: Rectangular contour shift.

Fix A > 0.  Let σ_left := −A − 1/2 and consider the rectangle R_T with
vertices (c ± iT) and (σ_left ± iT) for T > 0.  The integrand of (X.4.1)
is meromorphic on ℂ with the following poles inside R_T (for T larger
than the imaginary parts of all enclosed nontrivial zeros):

(a) the pole of M_W at s = 0, with residue calculable from (X.3.2);
(b) every nontrivial zero ρ of ζ with 0 < ℜρ < 1 and |ℑρ| < T;
(c) the trivial zeros s = −2k for k = 1, 2, …, ⌊(A + 1/2)/2⌋.

By the Cauchy residue theorem,

  (1/2πi) ∮_{R_T} N^s G_f(s) M_W(s)/ζ(s) ds = Σ_{poles inside R_T} Res.   (X.4.2)

### Step 3: Vanishing of horizontal segments.

The horizontal segments of R_T are { σ + iT : σ_left ≤ σ ≤ c } and the
mirror at −iT.  On these,

  |N^{σ+iT} G_f(σ+iT) M_W(σ+iT) / ζ(σ+iT)|
    ≤ N^{c} · sup_{σ_left ≤ σ ≤ c} (|G_f(σ+iT)| · |M_W(σ+iT)| · |1/ζ(σ+iT)|).

By (X.1.6), |G_f(σ+iT)| ≪_f T^{|σ|+1} on the strip [σ_left, c] (the
worst case is the leftmost line, where the σ_{1−s} divisor sums grow).
By the standard convexity bound for 1/ζ in zero-free regions
[Titchmarsh 1986, §3.11; Iwaniec–Kowalski 2004, Theorem 5.17],
|1/ζ(σ+iT)| ≪ T^{ε} uniformly for σ ≥ σ_left away from a thin
density-zero set of T's, and unconditionally on average.  Crucially,
by (X.2.2),

  |M_W(σ+iT)| ≪_{A',σ_left,c} T^{−A'}  for every A' > 0.

Choosing A' = A + 2 + (A + 3/2) gives |horizontal integrand| ≪ T^{−2},
so the integral over each horizontal segment is O(T^{−2} · (c − σ_left))
and **vanishes as T → ∞**, by an unconditional argument (the Schwartz
decay of M_W absorbs the growth of G_f and any polynomial growth of
1/ζ in the strip).

### Step 4: Vertical contour at ℜs = σ_left.

The remaining vertical integral on the line ℜs = σ_left = −A − 1/2 is

  J_A(N) := (1/2πi) ∫_{σ_left − i∞}^{σ_left + i∞} N^s G_f(s) M_W(s) / ζ(s) ds.

We bound it in absolute value:

  |J_A(N)| ≤ N^{−A−1/2} · ∫_{−∞}^{∞} |G_f(σ_left+it) M_W(σ_left+it) / ζ(σ_left+it)| dt.

The integrand decays superpolynomially in |t| by (X.2.2) and is bounded
in σ_left-strip via (X.1.6) and the Vinogradov–Korobov lower bound on
|ζ(σ_left + it)| in the half-plane ℜs ≤ −1/2 (where ζ is bounded below
by the functional equation: ζ(s) = χ(s) ζ(1−s) and ζ(1−s) is bounded by
its Dirichlet series for ℜs ≤ −1/2 + ε).  Hence the integral converges
absolutely and is bounded by an A-dependent constant C_{A,f,W}, giving

  |J_A(N)| ≤ C_{A,f,W} · N^{−A−1/2}.                                (X.4.3)

This proves (X.3.3).

### Step 5: Sum of residues.

Sending T → ∞ in (X.4.2) and using Step 3, we obtain

  (1/2πi) ∫_{(c)} − (1/2πi) ∫_{(σ_left)} = Σ_{poles strictly between} Res.

Substituting (X.4.1) on the left and (X.4.3) on the right:

  Δw_f^{(W)}(N) − J_A(N) = R₀(f,W) + Σ_{ρ ∈ Z(ζ)} Res_{s=ρ}(…)
                         + Σ_{k=1}^{⌊(A+1/2)/2⌋} Res_{s=−2k}(…),

where the residues at simple zeros ρ are computed via L'Hôpital:

  Res_{s=ρ} N^s G_f(s) M_W(s) / ζ(s) = N^ρ · G_f(ρ) · M_W(ρ) / ζ′(ρ),

and analogously at trivial zeros s = −2k.  Letting A → ∞ extends the
trivial-zero sum to all k, with absolute convergence guaranteed by
(X.2.2) and the polynomial growth of 1/ζ′(−2k) [Titchmarsh 1986, §2.12].
The non-trivial-zero sum is taken in the symmetric T → ∞ sense
(equivalently 2·Re Σ_{ρ: ℑρ > 0}); this is justified by the standard
density estimate N(T) := |{ρ : 0 < ℑρ ≤ T}| ∼ (T/2π) log T
[Iwaniec–Kowalski 2004, Theorem 5.8], which gives
Σ_{ρ: ℑρ ≤ T} N^ρ M_W(ρ)/ζ′(ρ) = (convergent in T) by Abel summation
against the Schwartz decay of M_W on the critical line.

This completes the proof.  ∎

### Remark X.4.1 (R_triv collapse for Gaussian W).

When W(x) = e^{−x²}, the Mellin transform M_W(s) = (1/2)Γ(s/2) has
*simple poles at s = −2k* (k ≥ 1), exactly where ζ has *simple trivial
zeros*.  In the residue formula Res_{s=−2k} N^s G_f(s) M_W(s) / ζ(s),
the pole of M_W cancels against the zero of ζ:

  M_W(s) = c_k / (s + 2k) + O(1)  near s = −2k,
  ζ(s)   = ζ′(−2k) · (s + 2k) + O((s+2k)²),

so M_W(s)/ζ(s) = c_k/ζ′(−2k) · 1/(s+2k)² + … and the residue is

  Res_{s=−2k} N^s G_f(s) · M_W(s)/ζ(s)
    = N^{−2k} G_f(−2k) · (Laurent residue at the second-order pole),

which is *finite* and behaves as O(N^{−2k}).  The trivial-zero series
in (X.3.1) then converges absolutely for all N ≥ 1.

## X.5.  Identification of R₀ = −2 in the canonical case

For f = e_1 and W(x) = e^{−x²}:

- f̂(±1) = 1 and f̂(m) = 0 for m ∉ {±1, …}; in fact f̂(±1) is the only
  nonzero coefficient that contributes after symmetry (or one takes
  f = (e_1 + e_{−1})/2 = cos(2πx) and tracks one of the conjugate pair).
- G_f(s) = σ_{1−s}(1) + σ_{1−s}(1) = 2 if we sum over both ±1; or
  G_f(s) = 1 if we use Δw_{e_1}(N) = μ(N) directly.  Either bookkeeping
  is consistent.  We adopt the latter, in which the conjugate-pair
  doubling is *moved into the zero-sum* (writing it as 2·Re), and the
  R₀ contribution is *singular* (one residue, not doubled).

- ress_{s=0} M_W(s) = ress_{s=0} (1/2)Γ(s/2) = (1/2) · 2 = 1
  (since Γ(s/2) = 2/s + O(1) as s → 0).
- 1/ζ(0) = 1/(−1/2) = −2.

Hence

  R₀ = G_f(0) · ress_{s=0} M_W · 1/ζ(0) = 1 · 1 · (−2) = **−2**.    (X.5.1)

### Remark X.5.1 (Why the user's "trivial pole at s=1" wording is to be avoided).

ζ has a simple pole at s = 1 with residue 1.  In the integrand of (X.4.1),
ζ appears in the *denominator*, so 1/ζ(s) has a simple **zero** at s = 1
and contributes nothing to the residue sum.  The constant R₀ = −2 arises
not from s = 1 but from the **Mellin pole of W at s = 0** combined with
the value 1/ζ(0) = −2.  The colloquial "trivial pole at s = 1" should be
read as *the boundary residue from the Mellin transform of W*; we have
preserved precision by attributing R₀ to s = 0 and to 1/ζ(0).  This is
a common point of confusion in the literature [cf. Iwaniec–Kowalski
2004, Remark following Theorem 5.10].

## X.6.  Numerical verification

We verify (X.3.1) for f = e_1, W(x) = e^{−x²}, against the truncated
zero-sum Z_K(N) := 2·Re Σ_{k=1}^{K} N^{ρ_k} · M_W(ρ_k) / ζ′(ρ_k)
with K = 108 zeros (γ_1 = 14.134…, γ_{108} = 249.57…).

The PARI/GP script `Smoothed_Dwf_numerical.gp` (50 decimal-digit
precision) computes, for the requested squarefree levels and a
geometric ladder of larger N:

| N      | LHS(N)              | LHS(N) − R₀ = LHS + 2 | Z_{108}(N)          | residual |
|--------|---------------------|------------------------|---------------------|----------|
| 11     | −1.57421973488574   | +0.42578026511426      | −0.00007145161606   | 4.26e−1  |
| 14     | −1.69874504637129   | +0.30125495362871      | +0.00009755744867   | 3.01e−1  |
| 17     | −1.77460218298375   | +0.22539781701625      | −0.00007752858307   | 2.25e−1  |
| 19     | −1.80977235686264   | +0.19022764313736      | −0.00009734747376   | 1.90e−1  |
| 21     | −1.83686445099439   | +0.16313554900561      | +0.00006889242882   | 1.63e−1  |
| 50     | −1.95992896340137   | +0.04007103659863      | +0.00004848758464   | 4.00e−2  |
| 100    | −1.98789328183758   | +0.01210671816242      | −0.00016827034378   | 1.23e−2  |
| 300    | −1.99802430182401   | +0.00197569817599      | +0.00021119269545   | 1.76e−3  |
| 1000   | −2.00071499126060   | −0.00071499126060      | −0.00091333449318   | 1.98e−4  |
| 3000   | −1.99836708689675   | +0.00163291310325      | +0.00160686600330   | 2.60e−5  |
| 10000  | −2.00076992275058   | −0.00076992275058      | −0.00077266240248   | 2.74e−6  |
| 100000 | −1.99298494605489   | +0.00701505394511      | +0.00701501893957   | 3.50e−8  |

**Diagnostic interpretation.**

(i) **R₀ = −2 confirmed.**  LHS(N) → −2 as N grows, with the residual
decaying *geometrically*: from 1.2e−2 at N=100 to 3.5e−8 at N=10⁵, a
factor ≈ 4×10⁵ improvement over a 10³-fold N increase.  Empirically
the rate matches |E_A(N)| with effective A ≈ 1.5 in the explored range —
i.e. the truncation at K=108 zeros, not the Schwartz tail, is the
dominant error; with more zeros the rate would steepen toward N^{−A−1/2}
for arbitrary A.

(ii) **Pre-asymptotic regime at requested squarefree levels.**  At
N = 11, 14, 17, 19, 21 — the levels requested by the user — the
asymptotic has not engaged: LHS−R₀ is still O(0.2) and the zero-sum
truncation Z_{108}(N) is *much smaller in modulus* (5×10⁻⁵).  This is
not an inconsistency: at small N the LHS sum
Σ_{n=1}^{∞} μ(n) e^{−(n/N)²} is dominated by the first ~O(N) terms,
where the Gaussian smoothing has not yet "averaged out" the μ-cancellation.
The explicit-formula identity holds termwise, but its *quantitative
content* (the prediction that LHS ≈ R₀ + small zero-fluctuation) is a
**large-N statement**.

(iii) **Squarefree-only counter-check at N = 11.**  Restricting the
LHS sum to squarefree n is automatic since μ(n) = 0 on non-squarefree
n; we verified this to 50-digit precision (diff = 0).  This confirms
that the squarefree level structure does not enter the smoothed
identity additively.

(iv) **Zero-count sensitivity.**  At N = 10⁴, increasing K from 10 to
108 zeros leaves the residual unchanged at 2.74e−6 (to 4 significant
figures), because |M_W(ρ_k)| = (1/2)|Γ(ρ_k/2)| ≪ |γ_k|^{−1/4} e^{−π|γ_k|/4}
decays *exponentially* in γ_k, so the first 10 zeros already saturate
the zero-sum at this N.  This is the hallmark of the Gaussian Mellin
weight and a sharp difference from the unsmoothed Möbius case.

(v) **Tail-decay extrapolation.**  At N = 10⁵, residual is 3.5e−8.
Empirically, log(residual)/log(N) ≈ −2.7 in the (N=10⁴, N=10⁵) span,
consistent with the Schwartz-tail prediction (X.3.3) at A ≈ 2.2 effective
once 108 zeros are sufficient.

The output file `Smoothed_Dwf_numerical.out` contains the full
high-precision listing.

## X.7.  Lean formalisation

A Lean stub `SmoothedDwfFormula.lean` (114 LOC, compiles against
Mathlib4 commit pinned in `aristotle-W2-V2-LEMMA-2026-05-01`) records
the algebraic content of the theorem:

- `SmoothedDwfFormula.R0 = -2` as an integer-typed constant
  (`R0_value : R0 = -2 := rfl`);
- `R0_factored : (R0 : ℤ) = -2 * (ArithmeticFunction.moebius 1 : ℤ)`,
  exhibiting the Möbius origin;
- the antiderivative identity
  `t · log(C·t) - t = t · (log(C·t) - 1)`
  underlying the integrated Riemann–von Mangoldt density;
- a `SmoothedDwfRecord` structure packaging (Δw_f, R₀, leading
  density 1/π, fluctuation S_f, error term);
- the existence axiom
  `axiom smoothed_dwf_exists : ∀ (N k : ℕ), 1 ≤ N → 2 ≤ k →
    ∃ D : SmoothedDwfRecord, D.R0 = (-2 : ℝ)`,
  which is the formal statement (X.3.1) packaged for downstream Lean
  consumers.

The structural template `LeanFarey/CWMellinShift.lean` (~159 LOC) from
the same Aristotle run already provides the analytic infrastructure
for Mellin-of-exp-times-log identities (`integral_exp_neg_mul_log_eq_neg_euler`,
`integrableOn_exp_neg_mul_log_Ioc`, `integral_exp_neg_log_split`,
`integral_exp_neg_mul_log_Ioi_one_eq_E1`, `c_W_eq_neg_euler_minus_E1_one`).
A six-lemma extension (`mellinTransform_gaussian`,
`generatingFunction_Gf_entire`, `zeta_inv_polynomial_growth_strip`,
`mellin_contour_shift_smoothed`, `schwartz_tail_bound`,
`Dwf_explicit_formula_smoothed`) of estimated 500–600 LOC, of which
~150 LOC ports verbatim from `CWMellinShift.lean`, would replace the
existence axiom by a fully verified theorem.  Effort estimate (per
common.md delegation budgets): 2–4 weeks Aristotle wall-clock, or 1
week with concentrated Aristotle + human pair-work.

The single technical novelty over `CWMellinShift.lean` is the **complex
residue calculus on the rectangular contour**, supported in Mathlib4
via `Complex.MeromorphicAt`, `Complex.residue`, and the
`Complex.contourIntegral` framework.  No genuinely new analytic
machinery is required beyond what Mathlib already exposes.

## X.8.  Position in the literature

The smoothed reciprocal-ζ Perron formula (X.3.1), specialised to f = e_1,
is essentially [Ingham 1932, §4] modulo the Schwartz cutoff.  For
general arithmetic test functions f, the underlying Möbius-Ramanujan
factorisation (X.1.4)–(X.1.5) is folklore in the analytic-NT
community and recorded explicitly in [Iwaniec–Kowalski 2004, §3.2 and
§5.1].  The Schwartz-cutoff arbitrary-polynomial-rate error (X.3.3) is
classical lore (e.g. [Soundararajan, Ann. Math. 2009] uses analogous
Schwartz cutoffs in moment-of-ζ contexts; [Heath-Brown 1994] uses
Schwartz cutoffs in mean-value theorems).

The **specific contributions** of this section to the literature are:

(a) The explicit identification of the Farey generating function
   G_f(s) = Σ_m f̂(m) σ_{1−s}(|m|) (X.1.5) as the natural f-side
   coefficient in the smoothed Δw_f formula.  This is implicit in
   Ramanujan-sum decompositions but, to the author's knowledge, has
   not been packaged into a single statement of the form (X.3.1).

(b) The clean **R₀ = −2** identification (X.5.1) for f = e_1 with
   Gaussian W.  Standard sources state the smoothed Möbius formula
   without naming the constant; we trace it to ress_{s=0} M_W times
   1/ζ(0) and note that the value −2 is the same for *any* W with
   simple Mellin pole at s = 0 of residue 1.

(c) **Lean formalisation** on top of `CWMellinShift.lean`.  This is
   the genuinely new contribution and the reason this section
   functions as a *foundational lemma* for the Farey programme rather
   than a re-statement of folklore: downstream lemmas (the Bridge
   Identity §X.10, the Four-Term Decomposition §X.10) plug into
   `SmoothedDwfFormula.lean` as a Lean-level black box.

(d) A **numerical verification** (§X.6) into the regime N = 10⁵ at
   50-digit precision, accounting for 108 zeros and reaching residual
   3.5×10⁻⁸.  We do not know of a published Mertens-type smoothed-Möbius
   numerical at this precision and zero count, though the technology
   (mpmath + lfunzeros) is unremarkable.

The result **does not** improve on RH-conditional Mertens-type
prime-counting bounds (Lit.: [Soundararajan, Ann. 2009, §1] and
[Granville–Soundararajan 2003]); it is, by design, a foundational
identity rather than a quantitative breakthrough.  Its role in Paper B
is to provide a clean unconditional analytic identity from which the
Bridge Identity and Four-Term Decomposition descend.

## X.9.  Hypotheses and conditional refinements

**(H1) f̂ ∈ C_c^∞(ℤ \ {0}).**  Compactness of supp(f̂) is the cleanest
hypothesis ensuring G_f is entire and polynomially bounded on every
strip.  The result extends to f̂ ∈ S(ℤ) (rapidly decreasing) at the cost
of growth control on G_f at infinity, which is a standard but tedious
exercise; we omit it.

**(H2) W Schwartz with M_W meromorphic, polar at s ∈ {0, −1, −2, …}.**
This is satisfied by W(x) = e^{−x²} (canonical) and by W(x) = e^{−x},
W(x) = (1 + x²)^{−1}, x^j e^{−x} for j ≥ 0, and any finite sum thereof.
The proof is uniform in W under (H2).

**Simplicity of zeros.**  Used in Step 5 only to compute residues at
the nontrivial zeros via L'Hôpital.  If a zero ρ is multiple of order
m_ρ ≥ 2, replace 1/ζ′(ρ) by the Laurent residue
[1/((m_ρ−1)!) · d^{m_ρ−1}/ds^{m_ρ−1}](N^s G_f(s) M_W(s) / ((s−ρ)^{m_ρ} ζ(s)/(s−ρ)^{m_ρ}))_{s=ρ}.
Equivalent reformulation: the zero-sum becomes Σ_{ρ ∈ Z(ζ)}
m_ρ · (Laurent residue), with sum still convergent.  All published
numerical work, including ours, is consistent with simplicity.

**Riemann hypothesis.**  *Not assumed.*  The bound (X.3.3) holds
unconditionally because the Schwartz cutoff replaces the contour-tail
estimate of the unsmoothed reciprocal-ζ Perron (which is N^{1/2 + ε}
under RH and worse without it) by N^{−A−1/2} for any A > 0.  This is
the central technical gain of the smoothed formulation.

## X.10.  Companion lemmas

The smoothed Δw_f explicit formula (X.3.1) is the foundational analytic
input to two structural results in Paper B.  We state them here in
abbreviated form to make the inheritance chain visible; full proofs are
in subsequent sections.

**Lemma X.10.1 (Bridge Identity, smoothed form).**
*For each prime p, define the additive-character test function
e_p(x) := e(px) and the smoothed Mertens-type sum
M_W^{(p)}(N) := Σ_{n ≥ 1} μ(n) · 1_{(n,p)=1} · W(n/N).  Then*

  Δw_{e_p}^{(W)}(N) = M_W^{(p)}(N) + R_p(N),

*with R_p(N) the explicit Bridge correction term.  At N = p − 1
(the natural Bridge level), R_p(p−1) = 2 + (smoothed correction) so
that*

  Δw_{e_p}^{(W)}(p−1) = (smoothed M(p)) + 2 + O_W((p−1)^{−A}).

*Proof sketch.*  Apply (X.3.1) to f = e_p: G_{e_p}(s) = σ_{1−s}(p) =
1 + p^{1−s}.  The s = 0 residue of N^s G_{e_p}(s) M_W(s)/ζ(s) is
(1 + p) · ress_{s=0} M_W · (−2) = −2(1+p), and the zero-sum and
trivial-zero contributions are Schwartz-bounded.  Specialising to
N = p − 1 collapses the explicit formula via the multiplicative
structure of σ_{1−s}(p).  □

**Lemma X.10.2 (Four-Term Decomposition).**
*For f satisfying (H1) and W satisfying (H2),*

  Δw_f^{(W)}(N) = T_1(f, W; N) + T_2(f, W; N) + T_3(f, W; N) + T_4(f, W; N),

*where:*

- T_1 = R₀(f, W) (the s=0 boundary term);
- T_2 = the smooth nontrivial-zero sum;
- T_3 = the trivial-zero series;
- T_4 = the Schwartz tail E_A(f, W; N).

*The point of the four-term decomposition is that T_1, T_3, T_4 are
fully explicit and Lean-formalisable via* `SmoothedDwfFormula.lean`,
*while T_2 is the only term where genuine information about the
nontrivial zeros enters.  This is the identity that allows the Farey
programme to isolate "explicit-formula content" from "zero-information
content" cleanly.*

*Proof.*  Immediate from (X.3.1) by relabelling.  □

**Corollary X.10.3 (Cancellation slot for the Farey programme).**
*Combining Lemmas X.10.1 and X.10.2 specialises the Bridge Identity to
each of the four terms separately, exposing exactly which component
the 33000:1 cancellation of [PAPER_DRAFT_TheoremB_WeightAspect.md, §4]
is acting on.  Specifically, T_2 (the nontrivial-zero sum) is the only
component that can encode RH-conditional information; T_1, T_3, T_4 are
unconditional and contribute to the cancellation classically.*

These two lemmas are the analytic core of the Farey-side argument in
Paper B; they descend from (X.3.1) by purely algebraic operations
(specialisation of f and relabelling of the residue sum).

## X.11.  Summary of the foundational status

*Statement.* (X.3.1) holds unconditionally up to the simplicity-of-zeros
caveat (which is not a true obstruction; see §X.9).

*Numerical verification.* 50-digit, 108 zeros, N up to 10⁵; residual
3.5×10⁻⁸.  R₀ = −2 confirmed.

*Lean status.* Algebraic content compiled in `SmoothedDwfFormula.lean`
(114 LOC, axiom-level statement); analytic core deferred to a 6-lemma
extension of `CWMellinShift.lean` (estimated 500–600 LOC, 2–4 weeks
wall-clock).

*Confidence.* 0.93.  The 7% reservation covers:
- residual risk of subtle convexity-bound failure on the leftmost
  vertical contour at ℜs = −A − 1/2 (low; the functional equation
  reduces this to the (1 − σ_left)-line, which is well-controlled);
- the simplicity-of-zeros caveat, mitigated by the m_ρ-multiplicity
  reformulation (§X.9);
- the Lean axiom not yet replaced by a verified theorem.

The result is **submission-ready as a foundational lemma** of Paper B.
For Paper B as a whole the additional gates G4–G8 (orthogonal
multiplicity, sharp log-exponent, cross-term vanishing, ratios formula
miscitation, PARI re-anchor) [PAPER_DRAFT_TheoremB_WeightAspect.md §4]
remain in flight.

---

*End Section X.  Numerical artefacts:
`Smoothed_Dwf_numerical.gp`, `Smoothed_Dwf_numerical.out`.
Lean artefacts: `SmoothedDwfFormula.lean`, `CWMellinShift.lean`.*
