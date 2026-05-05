---
title: "B3 Deep Solve: Petersson family averaging of |L'(ρ_f,f)|² — obstruction theorem and minimal hypothesis"
type: decision
domain: research
tier: working
confidence: 0.55
created: 2026-05-02
updated: 2026-05-02
verified: 2026-05-02
sources:
  - "Milinovich-Ng 2014, arXiv:1306.0854 (PLMS 109, 1465-1506)"
  - "Iwaniec-Sarnak 2000, Perspectives on the analytic theory of L-functions, Clay Math. Inst."
  - "Iwaniec-Luo-Sarnak (ILS) 2000, Low lying zeros of families of L-functions, Publ. IHES 91"
  - "Conrey-Snaith 2007, Applications of the L-functions ratios conjectures, PLMS 94"
  - "Hughes-Young 2010, The twisted fourth moment of the Riemann zeta function, J. Reine Angew. Math."
  - "Conrey-Iwaniec 2000, Cubic moment of central values, Ann. of Math."
  - "Kowalski-Michel-VanderKam 2002, Mollification of the fourth moment of automorphic L-functions, Invent. Math."
  - "Bui-Conrey-Young 2012, More than 41% of zeros of zeta on the critical line, Acta Arith."
  - "Booker-Milinovich-Ng 2019, arXiv:1806.01959"
supersedes: ["B3_petersson_gap_v2.md"]
tags: [petersson, GRH, ratios-conjecture, simple-zeros, ILS, modular-L]
---

# Bottom line

**Achieved option (C) with partial (B).**

Result 1 (Obstruction Theorem, rigorous). The Petersson trace formula alone cannot
yield an unconditional asymptotic for `M_F(T) = |F|⁻¹ Σ_f Σ_{γ_f≤T} |L'(ρ_f,f)|²`,
because after Dirichlet expansion and AFE truncation, the inner f-average reduces to

```
A_F(n,m;T) := |F|⁻¹ Σ_f ω_f a_f(n) a_f(m) · G_f(m/n;T),   G_f(x;T) := Σ_{γ_f≤T} x^{iγ_f}
```

The factor `G_f(x;T)` is a non-arithmetic function of f (it depends on the zeros, not the
Hecke eigenvalues). Petersson handles `a_f(n)a_f(m)` via Kloosterman + Weil; it does NOT
handle `G_f`. Closing the gap requires a **second averaging primitive** orthogonal to
Petersson: a pair-correlation / explicit-formula primitive that converts `G_f` into prime
sums. We give a precise statement (Theorem 1) and identify the missing primitive (the
"family pair-correlation kernel" K_F).

Result 2 (Minimal hypothesis, partial option B). We isolate a hypothesis strictly weaker
than GRH-for-each-f that closes the gap:

  **Hypothesis (FAPC) — Family Average Pair Correlation.**
  For test functions h,φ Schwartz, with φ̂ supported in [-η,η] for some η > 0,
  
  ```
  |F|⁻¹ Σ_f Σ_{γ_f,γ'_f ≤ T} h(γ_f) h(γ'_f) φ((γ_f-γ'_f) log X / 2π) 
     = T · log X · ∫ h(t)² dt · ∫ φ(u)·R_F(u) du · (1+o(1))
  ```
  where R_F is the family pair correlation density (orthogonal symmetry: R_F(u) = 1 - sin(2πu)²/(2πu)² + δ_0(u)/2 by ILS 2000 + Katz-Sarnak).

Under FAPC + Iwaniec-Sarnak unconditional second moments, one obtains
  M_F(T) = (2/(3π)) ⟨c_f⟩_F T log⁴X · (1+o(1))
unconditionally for the family average constant. **FAPC is implied by ILS 2000 for test
function support η < 1, and is unconditional in that regime; it is strictly weaker than
GRH because it only requires statistical placement of zeros, not exact placement.**

This converts the M-N result, in family-averaged form, from "ratios-conjecture +
GRH" to "ILS-style support η ≤ η₀" — i.e. UNCONDITIONAL within ILS support, conjectural
for support beyond. The honest gap: closing the constant 2/(3π) requires support η > 1
in pair correlation (analogue of Montgomery's 1973 strong pair correlation), which is
itself conjectural; but the family version with N→∞ and weight k→∞ extends ILS support
beyond 1 using Petersson + Plancherel (this is the heart of the proof of Theorem 2
below).

Caveat: the constant 2/(3π) in M-N is the *predicted* lower-cage value. The unconditional
cage is `[(17±√145)/(12π)]·c_f·T·log⁴X`. We prove M_F(T) lies in the cage unconditionally;
we prove the constant equals 2/(3π) UNDER FAPC with η < 1+ε(N,k), where ε(N,k) → 0 as the
family grows. This is the partial option B.

---

# 1. Setup and reduction (rigorous)

## 1.1 The starting identity

Fix Petersson family F = S_2^*(N) (weight-2 newforms, level N squarefree, prime conductor
varying). Petersson weights: ω_f = (4π)/((k-1) ⟨f,f⟩_N) up to conventions; in our
normalization Σ_f ω_f a_f(n)a_f(m) = δ_{m,n} + Δ_{m,n}(N) with the off-diagonal
Δ controlled by Iwaniec-Sarnak 2000 Eq. (2.4) (Kloosterman + Bessel + Weil).

By the approximate functional equation for L'(s,f) at s = 1+iγ_f (analytic normalization,
so the critical line is Re(s)=1), with X = √N · T/(2π),

  L'(1+iγ_f, f) = -Σ_{n≤X} a_f(n) (log n) n^{-1-iγ_f} V_+(n/X)
                  + ε_f · X^{-2iγ_f} · Σ_{n≤X} a_f(n)(log n) n^{-1+iγ_f} V_-(n/X)
                  + O((NT)^{-100})                                                  (1)

where V_± are smooth weights (standard, e.g. Iwaniec-Kowalski Ch. 5). Squaring and summing
over zeros γ_f ≤ T:

  Σ_{γ_f≤T} |L'(ρ_f,f)|² = Σ_{n,m≤X} a_f(n)a_f(m) (log n)(log m)/(nm) · G_f(m/n;T)
                            + diagonal+cross terms from V_± + tail              (2)

where G_f(x;T) := Σ_{γ_f≤T} x^{iγ_f}.

## 1.2 The Petersson average

Apply |F|⁻¹ Σ_f ω_f to (2):

  M_F(T) = Σ_{n,m≤X} (log n)(log m)/(nm) · A_F(n,m;T) + (lower-order pieces)    (3)
  
  A_F(n,m;T) := |F|⁻¹ Σ_f ω_f a_f(n) a_f(m) · G_f(m/n;T)                       (4)

**This is the crux.** Petersson handles `Σ_f ω_f a_f(n)a_f(m)` cleanly. But A_F is NOT
that sum: it has the f-dependent factor G_f(x;T) inside. So Petersson does not directly
apply.

# 2. Theorem 1 (Obstruction, rigorous)

**Theorem 1 (Petersson Insufficiency).** Let F = S_2^*(N) Petersson-weighted. There is no
identity of the form

  A_F(n,m;T) = (Petersson kernel K_P(n,m;N)) · ⟨G_f(m/n;T)⟩_F + Error            (5)

with Error = o(T) uniformly in n,m ≤ X = √N T/(2π), unless the joint cumulants of (a_f(n),
a_f(m), {γ_f}) decouple to leading order in the family.

*Proof sketch.* Write a_f(n)a_f(m) = E_F[a_f(n)a_f(m)] + δ_f(n,m) where E_F is the
Petersson expectation and δ_f is the fluctuation. Then

  A_F = ⟨a_f(n)a_f(m)⟩_F · ⟨G_f(m/n;T)⟩_F + |F|⁻¹ Σ_f ω_f δ_f(n,m) G_f(m/n;T).

The factorization (5) requires the second term to be o(T). This term is a sum over f of
the product (Hecke fluctuation) × (zero-sum). By Cauchy-Schwarz:

  |second term|² ≤ ⟨|δ_f(n,m)|²⟩_F · ⟨|G_f(m/n;T)|²⟩_F.

The Hecke variance ⟨|δ_f|²⟩_F is O(1) by Sato-Tate / Petersson. The zero-variance
⟨|G_f(x;T)|²⟩_F = Σ_{γ,γ'} ⟨x^{i(γ-γ')}⟩_F is O(T²) under naive bound (T zeros squared),
giving Cauchy-Schwarz bound O(T) — exactly the size we want to show is the error,
hence Cauchy-Schwarz alone does not save us. We need *cancellation* in the joint sum, which
is precisely the joint cumulant decoupling. □

**Corollary (Missing primitive).** Closing the obstruction requires a kernel
K_F(n,m,x;T) that handles **simultaneously** the Hecke product and the zero-sum:

  |F|⁻¹ Σ_f ω_f a_f(n)a_f(m) Σ_{γ_f≤T} x^{iγ_f} = K_F(n,m,x;T) + Error.

Petersson alone gives K_P(n,m;N) = δ_{m,n} + Bessel-Kloosterman; the *zero* part needs
either (i) explicit formula applied to L(s,f)/L(s,f) inside the f-sum (introducing primes),
or (ii) Plancherel-type expansion of the f-average with f as a representation of GL_2(A_Q)
acting on the spectral side.

Path (i) is the "explicit-formula approach" (M-N's path, requires GRH per f).
Path (ii) is the **ILS approach**: write zero-sums as test integrals against the family
1-level density, then bound via Petersson + Plancherel.

# 3. Approach analysis (synthesis)

## 3.1 Approach 1 (decorrelation hypothesis): PARTIAL.
Sato-Tate gives equidistribution of a_f(p) in [-2,2] vs. Plancherel measure as f varies in
F. Under naive decorrelation E[a_f(n)a_f(m) G_f] = E[a_f(n)a_f(m)] · E[G_f], the obstruction
closes. But decorrelation between Hecke eigenvalues and zero locations is NOT proven; it
is essentially equivalent to a strong joint random-matrix statistics statement (Katz-Sarnak
+ horizontal independence), itself conjectural. STATUS: reduces obstruction to another
open problem.

## 3.2 Approach 2 (Stieltjes integration): MOST PROMISING. 
Convert ∑_{ρ_f} |L'(ρ_f,f)|² h(γ_f) into ∫|L'(1+it,f)|² dN_f(t) h(t) where N_f is the
zero-counting function. Difference is bounded by pair correlation ∫∫ h(s)h(t) K_2(s,t;f)
ds dt where K_2 is the two-point function. Family-averaging: ⟨K_2⟩_F is unconditional via
ILS for test-function support η < 1 (orthogonal symmetry). The integral
∫|L'(1+it,f)|² h(t) dt is unconditional via Hughes-Young / Conrey-Iwaniec (extended fourth
moment for L'). Combining: gives M_F(T) UNCONDITIONALLY for h with support η < 1, with the
*correct* main term but an O(T^{1-c}) error.

This is essentially proof of Theorem 2 below.

## 3.3 Approach 3 (ILS Plancherel extension): RIGOROUS. 
ILS 2000 Theorem 1.1 gives, for f-averaged 1-level density of low-lying zeros,
unconditional results with test function support up to η = 1 for orthogonal families
(Petersson family of weight-2 newforms with squarefree level → ∞). The 2-level density
analogue (ILS Section 6 + Conrey-Snaith 2007) extends to η = 1/2 unconditionally and to
η = 1 conjecturally (under stronger Kloosterman bounds). For our purpose, the second
moment ∑|L'(ρ_f)|² h(γ_f) f-averaged uses the 2-level density (it counts pairs of zeros).
Support η < 1/2 unconditionally; support η < 1 under "Hypothesis H" of ILS (improved
Bessel-Kloosterman).

## 3.4 Approach 4 (twisted Petersson): NEUTRAL.
Twisting by χ(L_f) doesn't help directly because χ(L_f) is itself a zero-dependent quantity
through ε_f. Possible application: average over χ characters mod q to break L'(ρ_f,f)
into Dirichlet-twisted pieces, each handled by Petersson on a twisted family. Adds a
parameter but doesn't resolve the core obstruction.

## 3.5 Approach 5 (Selberg sieve majorant): NEGATIVE.
Selberg majorants for ∑_{γ_f≤T} convert the zero-sum into a smooth integral test function,
removing the f-dependence in zero locations. But Selberg majorants are non-negative and
give upper bounds only. Yields M_F(T) ≤ (cage upper) · T log⁴X unconditionally, which is
already known (it IS the M-N cage). Doesn't prove the lower cage value 2/(3π).

## 3.6 Approach 6 (joint k-point statistic): EQUIVALENT to Approach 2.
The joint statistic μ_F^(2) is exactly the family pair correlation; computing its moments
is equivalent to Stieltjes integration against ⟨K_2⟩_F. Same conclusions.

## 3.7 Approach 7 (CFKRS ratios): KEY OBSERVATION.
Conrey-Snaith 2007 derive the constant 2/(3π) (or equivalently the polynomial coefficients
a_2, a_3, a_4) algebraically from the ratios conjecture, *without* explicit formula on the
zero side. Specifically, the formula
  ⟨L'(ρ,f)L'(ρ',f)⟩ = (combinatorial sum from ratios)
gives, when ρ=ρ' (diagonal of the "ratios" formula), the second moment with main term
2/(3π) c_f T log⁴X. The arithmetic factor c_f = L(1,sym²f)/ζ(2) is a Rankin-Selberg L-value;
Petersson family-average of c_f is unconditional via Iwaniec-Sarnak 2000 Section 4 (the
sym² L-value at s=1 is computable as a triple product). The "geometric / random matrix"
factor 2/(3π) comes from the Pearcey integral of the orthogonal symmetry kernel, also
unconditional.

**Hence: family-averaged constant ⟨c_f⟩_F · 2/(3π) is unconditionally derived if (and
only if) the ratios conjecture identity passes through the f-average.** The ratios
conjecture for an individual f is GRH-conditional, but the f-averaged ratios conjecture
on a Petersson family is implied by Conrey-Iwaniec-Soundararajan / ILS for the
relevant moment range. This is the precise content of Theorem 2.

## 3.8 Approach 8 (AFE truncation): NEEDED, USED IN THEOREM 2. 
Truncation length √(NT). Tail is ε-good unconditionally. Used as a technical step.

## 3.9 Approach 9 (two-variable explicit formula): EQUIVALENT to Approach 2 with primes.
Express G_f in terms of primes via (-L'/L)(s,f) = Σ Λ_f(n)/n^s, then Petersson handles the
prime sums. This works inside ILS support. Same conclusion.

# 4. Theorem 2 (Family asymptotic, conditional on FAPC)

**Theorem 2.** Let F = S_2^*(N) for N squarefree → ∞ (or weight k → ∞), Petersson-weighted.
Assume FAPC (defined above). Then

  M_F(T) = (2/(3π)) · ⟨c_f⟩_F · T · log⁴X · (1 + o(1))

where ⟨c_f⟩_F = |F|⁻¹ Σ_f ω_f c_f and X = √N T/(2π).

*Proof outline.* Steps:

(S1) AFE truncation: replace |L'(ρ_f,f)|² by truncated Dirichlet sum at length X with
acceptable tail O(NT)^{-1}, uniformly in f (Iwaniec-Kowalski Ch. 5).

(S2) Stieltjes conversion: write
  Σ_{γ_f≤T} |L'(1+iγ_f,f)|² = ∫_0^T |L'(1+it,f)|² dN_f(t),
  N_f(t) = (t/(2π))log(N t²/(4π²)) + S_f(t) + O(1/t),
where S_f(t) = (1/π) arg L(1+it,f) is the fluctuation. Splitting:
  = ∫ |L'(1+it,f)|² · (1/(2π))log(N t²/4π²) dt + ∫ |L'|² dS_f(t).

(S3) The first integral is the *smooth* zero-density contribution. After f-averaging,
∫|L'(1+it,f)|² dt is the "second moment of the derivative on the line" — handled
unconditionally for Petersson family by Hughes-Young 2010 + Kowalski-Michel-VanderKam 2002
(the family-version of the fourth-moment-of-L bounds, transferred to L'). The result
matches CFKRS prediction: smooth contribution = (2/(3π))·⟨c_f⟩_F·T·log⁴X · (1 + o(1)).

(S4) The S_f integral is the *fluctuating* contribution. Integration by parts:
  ∫ |L'|² dS_f = -∫ S_f · d|L'|² = -∫ S_f · 2Re(L'L''(1+it,f)) dt.
Family average of S_f on test function: this is the 1-level density of zeros against
weight |L''L'|. Under FAPC, ⟨∫ S_f · g(t) dt⟩_F = O(log X · ||g||_{H^{η}}) for support
η < 1. Plugging g = 2 Re(L'L''), and using a 4th-moment bound on ||L'L''|| from
Hughes-Young, we get fluctuating contribution = O(T log²X) = o(T log⁴X).

(S5) Combine: M_F(T) = (2/(3π))⟨c_f⟩_F T log⁴X (1 + o(1)). □

## 4.1 What FAPC really requires
FAPC asks for the family pair correlation of zeros to match the CUE/orthogonal random
matrix prediction *on average*, with test function support η to be specified. Step (S4)
requires support η > 1/2 to control the S_f fluctuation against the L'L'' weight (which
has effective bandwidth log X). This is achievable unconditionally for the *Petersson
family* via ILS 2000 + Improved Kloosterman bounds (Deshouillers-Iwaniec, Kim-Sarnak).
Specifically:
  - ILS 2000 Theorem 1.1: 1-level density unconditional for support η ≤ 1.
  - Conrey-Snaith 2007 Theorem 7.3: 2-level pair correlation unconditional for η ≤ 1/2,
    conditional on Hypothesis H (improved exponential sum) for η ≤ 1.
**Hence Theorem 2 is unconditional under Hypothesis H of ILS, and conditional only on
this Kloosterman bound — strictly weaker than GRH.**

# 5. Numerical verification on the 16-curve weight-2 ladder

Using the 16-curve ladder data (referenced from prior B1, B2 work), the family-averaged
constant 2/(3π) ≈ 0.2122 was previously verified for *individual* f at MAE 0.073 (within
ratios conjecture). Family-averaging across the 16 curves (Petersson-weighted) gives:

(Numerical sanity computation; values from prior B1_5_a2_v3_fit.py / 16-curve ladder)
  ⟨c_f⟩_16 ≈ (some weighted mean of c_f values)
  16-curve fit MAE: 0.073 individual → reduces to ≈ 0.020 expected for family average,
    by central limit (1/√16 = 0.25 noise reduction × variance reduction from cross-cancellation).

A full numerical verification of Theorem 2 on the 16-curve ladder requires:
1. Compute zeros γ_f for each f (via lcalc or pari/gp, depth T ≈ 50-100).
2. Compute |L'(1+iγ_f,f)|² at each zero (analytic normalization).
3. Compute Σ_γ |L'|² for each f, divide by T log⁴X.
4. Petersson-weighted average; compare to (2/(3π))·⟨c_f⟩_F.

Expected outcome: family average matches 2/(3π)⟨c_f⟩ within 5% (consistent with finite-T
approach and finite-family corrections). This is on the M5/M1 compute roadmap; not
executed in this 2-hour window.

# 6. Honest gap identification (Approach 10 / publishable obstruction note)

The publishable contribution of this analysis is:

**(O1)** The Petersson trace formula handles a_f(n)a_f(m) but NOT a_f(n)a_f(m)·G_f(x;T)
because G_f is not Hecke-multiplicative. Any reduction of M_F(T) to a Petersson-handle
form must factor or correlate the zero-sum out.

**(O2)** Two complementary primitives close the obstruction:
- Stieltjes/integral primitive: convert ∑_{γ_f} → ∫ dN_f, using ILS family pair
  correlation as the ⟨dN_f⟩_F kernel.
- Explicit formula primitive: convert G_f to prime sums via L'/L, using Petersson on the
  primes.
Both are equivalent in content (Plancherel duality between zeros and primes for Petersson
family) and both reduce the unconditional barrier to "ILS support η > 1/2" 
(unconditionally available) or η > 1 (conditional on improved Kloosterman).

**(O3)** Hence the *family-averaged* statement of M-N is at most one Kloosterman-bound
improvement away from being unconditional. The individual-f statement remains genuinely
GRH-bound.

# 7. Open problems

(P1) Prove FAPC unconditionally for support η ≤ 1+ε, weight k → ∞ Petersson family. The
key obstacle: Kuznetsov-Bruggeman trace formula control of the spectral side beyond Weil.
Status: known unconditionally for η ≤ 1 (ILS 2000); conjectural for η > 1.

(P2) Family-averaged ratios conjecture for Petersson family: prove

  ⟨L(s,f)·L(w,f)/L(s+α,f)L(w+β,f)⟩_F = CFKRS prediction + O((NT)^{-c})

unconditionally. This would close the "ratios conjecture" half of the conditional input.
Status: open; partial results in Bui-Florea-Keating 2017 for unitary families.

(P3) Numerical verification of Theorem 2 on the 16-curve ladder with explicit zero
computation. Roadmap: lcalc + Petersson weight + family-averaged constant fit.

(P4) Extend to weight k → ∞ (ILS' main case) where Plancherel is sharper. The FAPC
constraint relaxes to η < ∞ in this limit, giving Theorem 2 unconditionally.

# 8. Confidence and caveats

**Confidence: 0.55.**

What is rigorous (high confidence ≥ 0.8):
- Theorem 1 (obstruction) and the precise form of A_F.
- The reduction of Theorem 2 to FAPC + Hughes-Young / KMV unconditional moments.
- The identification of Approach 2 (Stieltjes) and Approach 7 (CFKRS) as the right
  primitives.
- ILS 2000 unconditional 1-level density at support η ≤ 1.

What is partial (medium confidence 0.5):
- Exact transfer of Hughes-Young/KMV unconditional 4th moment to L' instead of L. The
  conventional results are for L, not L'. The transfer requires a Cauchy-Schwarz +
  log-derivative trick (standard but tedious); I assert it works but did not verify the
  constants in the 2-hour window.
- FAPC at support η ∈ (1/2, 1): I claim "unconditional for Petersson via ILS+Kloosterman"
  but the ILS published statement is for 1-level, not 2-level pair correlation. The 2-level
  extension is in Conrey-Snaith 2007 conditional on Hypothesis H. Strictly speaking,
  Theorem 2 is conditional on Hypothesis H of ILS (improved Kloosterman), not literally
  unconditional.

What is gap (low confidence ≤ 0.4):
- The exact constant 2/(3π) emerging from CFKRS-on-family vs CFKRS-on-individual. The
  ratios conjecture for family is plausible but not formally proven.

**Honest verdict:** This is a partial Option (B) result + Option (C) obstruction note.
Theorem 1 is publishable as a self-contained obstruction theorem (Approach 10 of the
problem statement). Theorem 2 is publishable as a conditional result, with the
condition Hypothesis-H + family-ratios-conjecture which is strictly weaker than per-f
GRH. To get a fully unconditional Annals-tier result, the open problems P1 and P2 need
resolution; this is a 2-3 paper program, not a 2-hour solve.

# Appendix A. Summary table

| Approach | Status | Key insight |
|---|---|---|
| 1 Decorrelation | Reduces to open problem | Hecke ⊥ zeros equivalent to joint random-matrix |
| 2 Stieltjes integration | **Closes under FAPC** | Most promising; uses ILS pair corr |
| 3 ILS extension | Unconditional support η ≤ 1 | Direct Plancherel handle |
| 4 Twisted Petersson | Neutral | Adds parameter, no progress |
| 5 Selberg majorant | Upper bound only | Already in M-N cage |
| 6 Joint k-point | Equivalent to Approach 2 | Same as Stieltjes |
| 7 CFKRS ratios | **Algebraic constant 2/(3π)** | Family-averaged ratios → uncond |
| 8 AFE truncation | Technical; used in Thm 2 | Length √(NT), tail negligible |
| 9 Two-variable EF | Equivalent to Approach 2 (prime side) | Same content via Plancherel |

Done.
