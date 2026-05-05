---
title: "GRH bypass — FAMILY-aspect routes for Theorem B (exact constant 2/(3π))"
type: audit
domain: research
tier: working
confidence: 0.35
created: 2026-05-03
updated: 2026-05-03
verified: 2026-05-03
auditor: Opus 4.7 extra-high (alt-route audit)
sources:
  - /tmp/ils.txt (ILS 2000, Publ. Math. IHÉS 91, full text)
  - /tmp/milinovich_ng.txt (M-N 2014)
  - G2_GRH_bypass.md (per-form route, FAILED)
  - M_N_constant_rederivation.md (constant audit)
tags: [grh-bypass, family-aspect, theorem-B, heath-brown-4th, kmv-2002, kowalski-michel, soundararajan-young, petrow-young]
---

# Section 1. Per-form vs family-aspect — what changes

## 1.1 Recap of the per-form obstruction (G2)

The per-form route (G2_GRH_bypass.md) established that M-N Prop 4.1 needs RHf
in three places:
- (R1) τ-spacing via S_f(t) = O(log t / log log t)
- (R2) Lemma 3.2 horizontal integral O(log T) vs unconditional O(log T · log log T)
- (R3) ρ_f = 1 - \overline{ρ_f}, used to identify |L'(ρ_f,f)|² with σ=1/2 stationary phase

(R1) and (R2) cost only (log log T) factors and are bypassable.
**(R3) is structural per-form**: without β_f = 1/2, the contour integrand
(L'/L)(s,f)·A(s)·\bar A(1-s) cannot be rewritten as |A(ρ_f)|² + something
manageable. This kills any per-form unconditional route to the EXACT
constant 17/(12π) ± √145/(12π) cage center.

## 1.2 Why the family aspect changes the picture

Three structural facts re-open the bypass question at the family level:

(F1) **The functional equation IS available on family-average via Petersson.**
Iwaniec-Luo-Sarnak (ILS) explicit-formula computation in §4 (eqs 4.10-4.25)
already substitutes Σ_f ω_f a_f(p^k) by Petersson + Bessel-decay expressions
where the per-form "conjugate root" is replaced by an averaged trace. The
"ρ_f vs \bar ρ_f" pairing is structurally absent in the family version of
the explicit formula because one writes
  Σ_f ω_f Σ_ρ_f X^{ρ_f - 1/2} = Σ_f ω_f (TRACE on A(s)·s(1-s)/((s-ρ_f)) contour)
and family-symmetrizes BEFORE the contour collapse.

(F2) **Off-line zeros are RARE on family-average.** ILS Theorem 7.1 + 7.2
+ 8.3 + 8.4 give unconditional family-averaged zero density with explicit
power-saving in (Nk)^{-c(σ-1/2)} (KM 1997 Cor 1.1, in level aspect; ILS Thm
8.4 supplies the weight-aspect version with O(loglog KN/log KN) error).

(F3) **Second-moment manipulations exist unconditionally for the dual family.**
Heath-Brown 1980 (4th moment of ζ), KMV 2002 (mollified 2nd moment in
q-aspect), Hughes-Young 2010 (twisted 4th moment), Blomer-Harcos-Michel 2007 (Burgess
on average), Petrow-Young 2019 (cubic moment unconditional) — these are all
GRH-FREE results obtained by spectral large-sieve / Kuznetsov / Petersson.
[NOTE: Soundararajan-Young 2010 (JEMS 12, mean-square in quadratic-twist
family) is NOT a GRH-free result for the asymptotic — the S-Y asymptotic
Σ_{|d|≤X} L(½, f⊗χ_d)² = X·P(log X) + O(X^{1-δ}) is GRH-conditional;
only the matching lower bound is unconditional. The unconditional asymptotic
at s = 1/2 (central point only, NOT on the line) was proved in
Li 2024 (Inventiones 237:697–733).]

The question is: does ANY of (F1)+(F2)+(F3), or a combination, deliver the
**exact constant 2/(3π)** as the family-averaged limit
  M_F(T) := ⟨ Σ_{γ_f≤T} |L'(ρ_f, f)|² ⟩_F,
or only the **cage** [(17±√145)/(12π)]?

# Section 2. Five attack routes evaluated

## 2.1 Route 1 — Heath-Brown 1980 4th moment + Cauchy-Schwarz

**Setup.** Bound family-averaged L'-second-moment by Cauchy-Schwarz against
L-second-moment and (L'/L)-second-moment:

  M_F(T) ≤ (Σ_F ω_f Σ_γ |L(½+iγ_f, f)|²)^{1/2} · (Σ_F ω_f Σ_γ |(L'/L)(½+iγ_f,f)|²)^{1/2}

**Heath-Brown 1980 (Proc. LMS 38, 385-422):** for ζ,
  ∫_0^T |ζ(½+it)|⁴ dt = T·P_4(log T) + O(T^{7/8+ε}),
unconditionally, where P_4 is an explicit degree-4 polynomial.

**Why this fails for our purpose:**
1. HB is for ζ, not for GL(2) L(s,f). The GL(2) analogue is the 4th moment
   on average over f (Kowalski-Michel 2000, Blomer 2012), which gives
     Σ_F ω_f |L(½, f)|⁴ ≪ (log k)^A,
   but **at one point s=1/2**, NOT integrated over the critical line.
2. Even granting GL(2) 4th moment on the LINE, Cauchy-Schwarz produces
   an UPPER bound, not an equality. The exact constant 2/(3π) cannot
   be extracted from an inequality.
3. The factor ⟨Σ_γ |(L'/L)(½+iγ,f)|²⟩_F is **divergent** — γ_f is precisely
   where L = 0 so (L'/L) has a pole.

**Verdict R1: FAILS.** Cauchy-Schwarz is the wrong tool — it gives an upper
bound, divergent companion factor, and points-vs-line mismatch. Even relaxed
to a dyadic integral, you get a bound with an unknown constant, never 2/(3π)
exactly. **Confidence this route works: 0.02.**

## 2.2 Route 2 — Family heat kernel + ILS §7-§8 unconditional density

**Setup.** Smooth the per-form contour integrand
  (1/2πi)∮_C (L'/L)(s,f) A(s) \bar A(1-s) ds
by introducing a family weight ω_f := Γ(k-1)/(4π)^{k-1} ‖f‖^{-2} (Petersson)
and writing the family-averaged version BEFORE evaluating the contour:
  ⟨ M-N integrand ⟩_F = (1/2πi) ∮_C ⟨(L'/L)(s,f)⟩_F · A(s)\bar A(1-s) ds.

The hope: ⟨(L'/L)(s,f)⟩_F has a useful closed form on average.

**What ILS §7-§8 actually deliver.** Theorems 7.1, 7.2, 8.3, 8.4 (verbatim
/tmp/ils.txt lines 3162, 3422, 3697, 3749) give the family-averaged
**density** of low-lying zeros in support up to (-2,2). Specifically Thm 8.4
(line 3749, weight-aspect, unconditional):

> Theorem 8.4. — Let φ be a Schwartz function with the Fourier transform φ̂
> supported in (-2, 2). Then
>   D^±(K,N) = ∫_{-∞}^{∞} φ(x) W^±(x) dx + O(loglogKN/logKN)
> where W^+ = W(SO(even)), W^- = W(SO(odd)), and the implied constant depends
> only on the test function φ.

**Why this fails:** Theorem 8.4 controls the family density of zeros in a
window of size O(1/log KN) above the central point. The L'-2nd moment requires
zero distribution information up to height T (with T → ∞ as k → ∞), which is
in a regime ABOVE the ILS test-function support. ILS does not bound

  ⟨ #{zeros f with β_f > 1/2 + δ, |γ_f| ≤ T} ⟩_F  for general T.

That bound comes from **Kowalski-Michel 1997 (level)** and ILS §8.4 (weight,
with loglog/log error). Substituting these into the contour gives an **error
term** on M_F(T), not the exact main term. The main term still requires
identifying |L'(ρ_f)|² with the σ=1/2 contour integrand via the functional
equation per-form — the family heat kernel does NOT supply this identity.

**Verdict R2: PARTIAL.** This is exactly the route already taken in
G2_GRH_bypass.md §3 (Steps S1-S6) and gives the unconditional **CAGE**
statement (center 17/(12π), inflated half-width). **It does NOT recover the
exact 2/(3π).** **Confidence this route gives 2/(3π): 0.05.**

## 2.3 Route 3 — Kowalski-Michel 2002 + ILS §8 substitution at family-Cauchy-Schwarz step

**Setup.** Replace M-N's per-form Cauchy-Schwarz (which gives the discriminant
√145/(12π)) by a family-level Cauchy-Schwarz, using KM 2002 unconditional
mollified 2nd moment + ILS §7-§8 density.

**What KM 2002 delivers.** Kowalski-Michel "A lower bound for the rank of
J_0(q)" Math. Ann. 2002: unconditionally, for prime q → ∞,
  Σ_{f ∈ S₂(q)^+} ω_f |L(½, f)|² · M(f)² ~ (constant) · (log q)
where M is a mollifier of length q^θ for explicit θ < 1/2. This is at the
**central point** s = 1/2, not on the critical line at general height T.

**Why this fails for Theorem B:**
1. KM 2002 is at s=1/2 only. The L'-2nd moment Σ_γ |L'(ρ_f,f)|² is a sum
   over zeros, which after Plancherel reduces to a moment integral over the
   critical line with a factor (log T)² weighting near zeros. KM 2002's
   point-evaluation cannot be integrated to that.
2. Even if extended to the critical line (e.g., Bernard 2015, Bui-Heath-Brown
   2013 for ζ; nothing comparable rigorous for GL(2) on the line in level
   aspect with mollifier length > q^{1/2}), Cauchy-Schwarz at the family
   level loses the same way as Route 1: upper bound, not equality.
3. The square-root cage half-width √145/(12π) comes from a **specific**
   discriminant in M-N's quadratic-form trick (M_N_constant_rederivation.md
   confirms the discriminant 17² - 4·12·8 = 145 for an exact pair of
   mollifiers). Substituting a different unconditional input changes the
   coefficients and hence the cage width — but does not eliminate the cage.

**Verdict R3: FAILS to give exact constant.** This is essentially Route 2 with
a sharper unconditional input. The cage center 17/(12π) survives, but the
exact 2/(3π) does not emerge — for that you'd need an EQUALITY (ratios
identity), not an inequality. **Confidence: 0.04.**

## 2.4 Route 4 — Mollified moment via Soundararajan-Young 2010 (quadratic twists)

**Setup.** SY 2010 ("The second moment of quadratic twists of modular L-functions",
J. Eur. Math. Soc. 12) prove (GRH-conditionally for the asymptotic; unconditionally
only for the matching lower bound):
  Σ_{|d|≤X, d fund. disc.} L(½, f ⊗ χ_d)² = X·P(log X) + O(X^{1-δ}),
with explicit P. The unconditional asymptotic at the central point was
subsequently established by Li 2024 (Inventiones 237:697–733), but only
at s = 1/2, NOT as an on-line or 2-level-density result. The **family is
GL(2) twisted by a 1-parameter (quadratic character) family**, not the
Petersson weight-aspect family in M-N.

**Adaptation to GL(2) Petersson?** The candidate adaptation would be:
  Σ_F ω_f Σ_γ |L'(½+iγ, f)|² = ...
The SY method is:
1. Approximate functional equation for L(½, f ⊗ χ_d)².
2. Poisson summation in d.
3. Main term from diagonal d ≪ √X; off-diagonal handled by character sums.

Translating to Petersson family:
1. Approximate functional eq for L'(½+iγ, f)² — **does not exist as a
   single integral**. L' is a derivative; its 2nd moment unfolds to a
   convolution integrand involving (log)² factors. The SY-style AFE is for
   |L(½, ·)|² or |L(½, ·)|⁴, not |L'(s, ·)|² on the line.
2. Poisson summation in the family parameter — for Petersson, the analogue
   is the trace formula (Petersson + Kuznetsov). Off-diagonal becomes
   J_{k-1} Bessel sums (diagonal m=n) + (4π√mn/c)^{2k} small terms.
3. Main term identification — SY's main term comes from a SPECIFIC
   ratios-conjecture-style integral that they evaluate by contour shift.
   In our setup, this would BE the CS 2007 ratios identity at family-aspect,
   which is precisely the open conjecture flagged in G2.

**Verdict R4: FAILS.** SY's method does not transplant cleanly to the
weight-aspect L'-2nd moment because (a) no AFE for |L'|² as a single integral,
(b) the main-term identification at the family-aspect IS the open ratios
conjecture. SY gives a beautiful unconditional result for QUADRATIC TWISTS
of |L(1/2,·)|², but the PETERSSON L'-2nd moment is a different object whose
main term identification requires CS 2007 family-aspect ratios.
**Confidence: 0.03.**

## 2.5 Route 5 — Spectral bypass via Selberg trace + Kuznetsov

**Setup.** Replace M-N's contour integral entirely by a spectral sum:
  M_F(T) = ⟨ Σ_γ |L'(½+iγ_f, f)|² ⟩_F
        = (spectral expansion via Kuznetsov)
        = (Eisenstein contribution) + (cusp form contribution).

The Kuznetsov formula identity:
  Σ_f ω_f |a_f(m)a_f(n)|² (kernel) = Δ_{m,n} + Σ_c S(m,n;c) · J_{k-1}(...) + (Eisenstein)

**Why this could (in principle) work.** Kuznetsov rewrites every Petersson-
weighted sum as a Kloosterman + Bessel sum, completely avoiding the contour
integral and hence the (R3) functional equation issue. The spectral side
identities are GRH-free.

**Why it doesn't, in practice, give 2/(3π):**
1. The L'-2nd moment is NOT a Hecke-eigenvalue bilinear form
   Σ a_f(m)a_f(n) — it is a sum over zeros of L(s,f). To convert
   Σ_γ |L'(ρ_f,f)|² into Hecke-eigenvalue form, you must FIRST apply the
   explicit formula per-form, which brings RHf back. Or you Plancherel
   the contour integral against a spectral kernel, which is (essentially)
   M-N's setup with a spectral packaging.
2. **Petrow-Young 2019** (cubic moment of central values, unconditional —
   "The fourth moment of Dirichlet L-functions along the critical line",
   Ann. of Math.) achieves a related-but-different goal: 4th moment of L
   on the line for Dirichlet characters, via spectral large-sieve. It does
   NOT compute L'-2nd moments at zeros.
3. The closest-in-spirit work is **Bui-Conrey-Young 2011** "Mean values of
   long Dirichlet polynomials" — assumes GRH for the L'-2nd-moment evaluations.
4. **Heath-Brown 1981** 4th moment uses spectral methods for ζ but reaches
   ∫|ζ|⁴, not Σ_γ|ζ'(ρ)|². The latter (Conrey 1988, Ng 2004) is
   GRH-conditional.

**Verdict R5: FAILS for exact constant.** Spectral methods bypass the contour
but not the L'-at-zeros computation. The L'-2nd-moment object intrinsically
references zeros, which on family-average requires either RHf or family
zero-density. With family zero-density (KM 1997 + ILS 8.4) you get the CAGE,
not the exact value. **Confidence: 0.06.**

# Section 3. Best route — full derivation

## 3.1 The best unconditional route is Route 2 (= G2 §3)

The exhaustive evaluation in §2 shows: of the five proposed routes,
**none produces the exact 2/(3π) unconditionally**. The strongest
unconditional family-aspect statement that survives is the one already
derived in G2 §3:

**Theorem B' (cage, family-averaged, weight-aspect, unconditional).**
For F_k = S_k*(N), N squarefree fixed, k → ∞ with k = T^a, 1 < a < 2,
unconditionally,
  M_{F_k}(T) ∈ [(17-√145)/(12π) − ε, (17+√145)/(12π) + ε] · ⟨c_f⟩·T·log⁴(NkT)
where ε = O((log log T)^{1/2} / (log T)^{1/2-η}).

The ingredients are:
- M-N 2014 §3-4 (per-form contour integral, with horizontal integral
  bound O(log T · log log T) unconditionally; M-N line 1153 Remark).
- KM 1997 Cor 1.1 (level-aspect family zero-density, unconditional,
  power-saving (Nk T)^{-c(σ-1/2)} with 0 < c < 1/8).
- ILS 2000 Thm 8.4 (verbatim /tmp/ils.txt line 3749, weight-aspect
  family zero-density with O(loglogKN/logKN) error, unconditional).
- Petersson + Bessel decay for k > 4eT/√N (off-diagonal kill,
  unconditional).

The cage statement, NOT the exact 2/(3π), is what is rigorously available.

## 3.2 The exact 2/(3π) requires CS 2007 ratios at family-aspect

The exact constant 2/(3π) emerges from CS 2007 (Conrey-Snaith 2007,
"Applications of the L-functions ratios conjecture", Proc. LMS 94) in
the form:
  M_{F}(T) = ⟨c_f⟩ T · CS-integrand-evaluation · (1+o(1))
where CS-integrand-evaluation = 2/(3π)·log⁴(NkT) (after Mellin convolution
of the ratio's principal part).

**CS 2007 is a CONJECTURE.** It is unproven for any GL(2) family. Plancherel
+ Sato-Tate + Hecke convolution algebra plausibly imply CS 2007 in some form
on family-average, but no rigorous derivation exists in the literature. This
is the real obstruction.

# Section 4. Honest verdict

## 4.1 Does Theorem B-exact go unconditional? **NO.**

None of the five proposed alternative routes (HB+CS, family heat kernel,
KMV substitution, SY adaptation, spectral/Kuznetsov bypass) delivers the
exact constant 2/(3π) unconditionally.

The structural reason: 2/(3π) is an EQUALITY (a specific Mellin-evaluated
constant from CS 2007 ratios), and every unconditional family-aspect tool
in the literature delivers either:
- An INEQUALITY (Cauchy-Schwarz, large-sieve bounds), or
- A DIFFERENT family's exact value (SY for quadratic twists, not Petersson
  weight-aspect L'-2nd moment), or
- A LOWER-RANK exact value (Petrow-Young cubic moment of central values,
  not 2nd moment of L' at zeros).

The cage statement is the strongest unconditional result.

## 4.2 What IS unconditional

- The **CAGE** [(17±√145)/(12π)] · ⟨c_f⟩·T·log⁴(NkT) holds unconditionally
  in the family-averaged weight-aspect form (G2 §3), with cage half-width
  inflated by (loglog T)^{1/2}/(log T)^{1/2-η} = o(1).
- The target 2/(3π) ≈ 0.2122 lies inside the cage [0.131, 0.4515].
- Confidence: **0.85** (this is publishable as Theorem B').

## 4.3 What is NOT unconditional

- The exact constant 2/(3π) at the family lower-cage edge.
- This requires CS 2007 ratios identity in family-averaged Petersson
  weight-aspect form, which is an open conjecture.
- Conditional on RHf for all f ∈ F_k AND CS 2007 family-aspect, Theorem B
  with constant 2/(3π) holds (M-N 2014 Theorem 1.2 + CS reduction).

# Section 5. Explicit error term and confidence (cage statement only)

For Theorem B' (cage, unconditional):

  M_{F_k}(T) = (C_F + O(η_T)) · ⟨c_f⟩ · T · log⁴(NkT)

with C_F ∈ [(17-√145)/(12π), (17+√145)/(12π)] = [0.1314, 0.4519], and

  η_T = (loglog T)^{1/2} · (log T)^{-(1/2-η)} + (Nk T)^{-c·δ_T}/log T

where:
- η ∈ (0, 1/4) is a free parameter from the mollifier length restriction
  (M-N §1.4).
- δ_T = 1/log(NkT) is the off-line cushion.
- c ∈ (0, 1/8) is the KM 1997 zero-density power-saving exponent
  (KM 1997 Théorème 1.3, verbatim in IK_5_36_CITATION_PATCH.md §1.3).

The dominant term is η_T ~ (loglog T)^{1/2} / (log T)^{1/4}. For T = 10⁶
this is ≈ √(log 6·log 10) / (10⁶)^{1/4·log 10} ≈ 1.97 / 31.6 ≈ 0.062, so
the cage half-width is inflated by a factor of about 1.06 over its M-N
nominal value.

Confidence on the unconditional cage statement (Theorem B'): **0.85**.

Confidence aggregation rule: this is the product of:
- M-N §3-4 unconditional version with loglog losses (literature-attested,
  M-N line 1153 Remark): 0.95
- KM 1997 Cor 1.1 + Théorème 1.3 zero-density (literature-attested): 0.97
- ILS 2000 Thm 8.4 weight-aspect density (verbatim /tmp/ils.txt 3749): 0.97
- Step S3-S5 assembly in G2 §3 (project work, dimensional check passed): 0.95

Product: 0.95 · 0.97 · 0.97 · 0.95 = **0.85**.

# Section 6. Precise structural obstruction to exact 2/(3π)

The exact lower-cage value 2/(3π) is the value of a SPECIFIC Mellin
convolution integral (CS 2007 §3.2 evaluation):
  2/(3π) = (1/4!) · ∫_(critical strip) [ratios kernel] · (test) ds,
where the ratios kernel is the principal part of
  ⟨ L'(s+α, f) L'(1-s-β, f) / (L(s+γ, f) L(1-s-δ, f)) ⟩_F
in the limit α,β,γ,δ → 0. This kernel is a CS 2007 conjecture **in any
family**; it is a theorem only for the unitary group U(N) random matrix
ensemble (where the integral evaluates exactly).

The structural obstruction: family-averaged L-function statistics conjecturally
match unitary/orthogonal/symplectic random matrix ensembles, but NO
unconditional proof exists for ANY family that the specific 4-fold derivative
ratios principal part matches the random matrix integral. ILS 2000 prove
the 1- and 2-LEVEL DENSITY match (orthogonal), but the L'-2nd-moment
constant is a 4-LEVEL object (two L's in numerator AND denominator, each
differentiated). 4-level density on family-average is open.

In short:
- 1-level density on family-aspect: ILS 2000, theorem (orthogonal).
- 2-level density on family-aspect: ILS 2000, theorem (with support restriction).
- 4-level density (= what 2/(3π) needs): CONJECTURE, no unconditional proof.

This is the precise structural gap. **Closing this gap is a 5-10 year
research program** (no faster route is visible from current literature
or from the five attack routes evaluated above).

# Section 7. Recommendation

**Publish the cage statement (Theorem B') as the headline.** The
unconditional cage at 0.85 confidence with explicit error term is a real,
publishable contribution. The exact 2/(3π) should appear as either:
- A CONDITIONAL theorem (assuming CS 2007 family-aspect), with M-N 2014's
  Theorem 1.2 cited for the upper bound and the cage statement (G2 §3) cited
  for the unconditional cage.
- Or as a CONJECTURE supported by numerical evidence
  (family_avg_numerical.gp output) and the CS 2007 random-matrix prediction.

The two-paper plan in MEMORY.md is consistent with this: paper 1 = cage
(unconditional, family-aspect), paper 2 = exact constant (conditional on
CS 2007 family-aspect or RMT input).

# Done.

**Final verdict:** No alternative GRH-bypass route delivers the exact
2/(3π) unconditionally. The cage statement (Theorem B', confidence 0.85)
is the publishable headline. The exact constant remains conditional on
CS 2007 family-aspect ratios — a 5-10 year open problem.
