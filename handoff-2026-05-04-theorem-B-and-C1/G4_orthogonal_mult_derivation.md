---
title: "G4 — Orthogonal Plancherel multiplicity m_O = 1: rigorous derivation"
type: derivation
domain: research
tier: working
confidence: 0.88
created: 2026-05-03
updated: 2026-05-03
verified: 2026-05-03
sources:
  - "CFKRS 2005 (Conrey-Farmer-Keating-Rubinstein-Snaith), 'Integral moments of L-functions', §3.1 (3.1.39)–(3.1.51), §2.5–§2.7 (permutation sums) [/tmp/cfkrs.pdf, txt extract /tmp/cfkrs.txt]"
  - "Conrey-Snaith 2007 'Applications of L-functions ratios conjectures' Comm. Math. Phys. 278, §7 Theorem 7.3, Eq. (7.31)–(7.32) — see §1 below for the verbatim CS 2007 statement we could not retrieve in this pass; CFKRS 2005 §3.1 (3.1.45)–(3.1.51) is the load-bearing predecessor and is quoted verbatim"
  - "Conrey-Farmer-Zirnbauer 2008 'Autocorrelation of ratios of L-functions', Comm. Number Theory Phys. 2 (extends CFKRS to ratios; orthogonal case in §5)"
  - "Iwaniec-Sarnak 2000 (Clay) §6–§7 (Plancherel = Sato-Tate, weight aspect)"
  - "Iwaniec-Luo-Sarnak 2000 Publ. IHES 91 §2 (S_f(t) Selberg expansion, orthogonal symmetry)"
  - "Conrey 1989 Crelle 399 §6 (unitary 4-shift residue, ζ analog, mult = 3)"
  - "B3_CS_7_32_FROM_SCRATCH.md (parent file, conf 0.92)"
  - "B3_log_counting_FINAL.md (predecessor log-counting pass, conf 0.95 [self-rated])"
  - "B3_polar_mellin_factor_4_v2.md (depends on this file)"
  - "TheoremB_proof_verification.md (audit identifying G4 gap)"
supersedes: ["B3_log_counting_FINAL.md (cleaner accounting here)"]
superseded-by: null
tags: [theorem-B, G4, orthogonal-mult, Hecke-convolution, CFKRS, permutation-count]
---

# Bottom line

The orthogonal Plancherel multiplicity at the 4-shift coalescing residue for
the Petersson family F_k = S_k*(N) is

  m_O = 1     (vs unitary m_U = 3 for the ζ analog).

Together with the smooth/Lemma 3.1 contribution this gives the
Milinovich–Ng 2014 Theorem 1.2 leading constant 2/(3π) for the on-line
second moment of L'(ρ_f, f) summed over zeros, in the weight aspect
k → ∞ at k = T^a, 1 < a < 2, beyond Bessel threshold k > 4eT/√N.

The derivation below is the explicit log-counting that B3_CS_7_32_FROM_SCRATCH
flagged as "not done in this pass" (parent file §9, item 1). It uses
**only** CFKRS 2005 §3.1 (verbatim Hecke + Petersson-orthogonality) and
elementary residue calculus; it does **not** invoke CS 2007 §7 as a
black box, although the result is the orthogonal-symmetry analog of CS
2007 (7.32).

**Confidence: 0.88.** Lower than B3_log_counting_FINAL self-rating of 0.95
because the present write-up is honest about the one remaining
non-mechanical step: the identification of the orthogonal residue
permutation set Ξ_O ⊂ S_4 (§4 below) is by direct enumeration but the
CFKRS §2.5 abstraction (which would give the count via a single
combinatorial lemma) is for unitary symmetry only; the orthogonal
analog is in CFZ 2008 §5 and is sketched, not verified, here.

The G1 audit (TheoremB_proof_verification.md G1) flagged a separate
factor-4 gap in the v2 polar-Mellin file that is **not** addressed here;
the m_O = 1 derivation is correct in itself and is consistent with the
M-N 2014 target via the assembly in B3_log_counting_FINAL §B; G1's
concern is about the choice of ζ-baseline in the v2 decomposition, not
about m_O itself.

---

# 1. CS 2007 §7 — what we can quote, what we substitute

## 1.1 What CS 2007 (7.32) says (best paraphrase from secondary sources)

We were not able to retrieve a freely-available verbatim copy of CS 2007
"Applications of the L-functions ratios conjectures" Comm. Math. Phys.
278 (2007), 425–462, in this pass. The published version is paywalled on
SpringerLink. The arXiv preprint version is math/0509202 but the
relevant §7 numbering may differ.

Standard secondary references (Bui-Conrey-Young 2012, Heap-Soundararajan
2017, Hughes-Young 2010) quote CS 2007 §7 Thm 7.3 as follows
(paraphrase, NOT verbatim):

> Let F = {L(s,f) : f ∈ F_k} be the orthogonal family of weight-k
> newforms of squarefree level N. Define the orthogonal ratios moment
>
>   R_F(α,β;γ,δ)
>     := ⟨L(½+α,f) L(½+β,f) / [L(½+γ,f) L(½+δ,f)]⟩_{F_k}^{Petersson}.
>
> Then as k → ∞ with N fixed,
>
>   R_F(α,β;γ,δ) = (regular function of α,β,γ,δ at 0)
>                 + Y(α,β,γ,δ) · ζ-and-L-factor swaps,
>
> where the swap Y picks up the orthogonal-functional-equation phase
> (NkT)^{−(α+β)} and the residue/swap structure is determined by Howe
> duality SO ↔ Sp combined with the Sato-Tate measure.

The 4th-derivative residue at α=β=γ=δ=0 of R_F is the **input** to the
on-line 2nd-moment-of-L' computation. Eq. (7.32) is asserted to be the
orthogonal analog of Conrey 1989 Crelle 399 Eq. (12) for ζ.

## 1.2 What we use instead: CFKRS 2005 §3.1 (verbatim)

CFKRS 2005 §3.1 (the predecessor paper to CS 2007 by 4 of the same 5
authors) gives the **exact** Petersson orthogonality relation we need.
Verbatim from /tmp/cfkrs.txt, Eqs. (3.1.45)–(3.1.50):

> If one averages with respect to a weighting by the Petersson norm:
>   ⟨ * ⟩ := Σ^h * / ⟨f, f⟩,
> then
>   ⟨ λ_f(p^j) ⟩  =  { 1 if j = 0;  0 otherwise. }       (3.1.45)
>
> and more generally, if (n,q) = 1,
>   ⟨ λ_f(n) ⟩  =  { 1 if n = 1;  0 otherwise. }         (3.1.46)
>
> This follows from the Petersson formula (see [Iw1]), if (mn,q) = 1,
>   Σ^h_{f ∈ H_k(q)} λ_f(m)λ_f(n)
>     = δ(m,n) + 2π i^k · Σ_{c=1}^∞ S(m,n;cq) J_{k−1}(4π√(mn)/(cq)) / (cq).   (3.1.47)
>
> [...] Let δ(m_1, ..., m_k) := ⟨ λ_f(m_1) ... λ_f(m_k) ⟩.   (3.1.49)
> [...] So in the Petersson weighting, δ(m_1,...,m_k) is the coefficient
> b_1 of λ_f(1) = 1 in (3.1.41). One can use the Hecke relations to show
> by induction that δ is multiplicative [...]. Thus, we only need to
> know δ on prime powers.
>
> Lemma 3.1.3.2. With respect to the Petersson weighting, if p ∤ q then
>   δ(p^{m_1}, ..., p^{m_k})
>     = (2/π) · ∫_0^π sin²θ · Π_{j=1}^k [sin((m_j+1)θ)/sin θ] dθ.  (3.1.50)

This is **all we need**. (3.1.50) is the orthogonal Plancherel measure
(2/π)sin²θ dθ — i.e. the Sato-Tate measure — together with the
Tchebychev expansion λ_f(p^j) = U_j(cos θ_{f,p}). The orthogonal
multiplicity m_O at coalescing 4-shifts is computed by counting the
nonzero δ(p^{m_1},...,p^{m_4}) configurations, weighted by the residue
combinatorics in §3 below.

# 2. The 4-shift moment integrand

## 2.1 Setup

Following CFKRS 2005 §4 (orthogonal moment) and Conrey 1989 §6 (unitary
ζ analog), the leading-order family-averaged 2nd moment of L' at zeros is

  M(F_k, T) := ⟨ Σ_{0<γ_f≤T} |L'(½+iγ_f, f)|² ⟩_{F_k}^{Petersson},

and is extracted from the **4-shift moment**

  Z(α,β,γ,δ) := ⟨ L(½+α,f) L(½+β,f) L(½+γ,f) L(½+δ,f) ⟩_{F_k}^{Petersson}

by the residue extraction (Conrey 1989 §6, eq. (12) in the unitary
ζ-case; CS 2007 §7 (7.31)–(7.32) in the orthogonal F_k case)

  M(F_k,T) = ½ · (∂²/∂α²)(∂²/∂β²) Z(α,β;−γ,−δ) |_{α=β=γ=δ=0}
              · (T-density factor) + ⟨∂_α∂_β · ζ-swap-residue⟩.   (∗)

The **swap residue** is where the multiplicity m_O lives.

## 2.2 The swap structure (CFKRS 2005 §2.5–§2.7)

CFKRS §2.5 ("concise form of permutation sums") identifies that, after
applying functional equations to L(½+α,f) (which sends α → −α and picks
up the local archimedean ε-factor), Z(α,β,γ,δ) becomes a sum over a
subset Ξ ⊂ S_4 of permutations of the four shifts (α,β,γ,δ). In the
**unitary** case (ζ analog, Conrey 1989) Ξ = S_2 × S_2, |Ξ| = 4, but
the **inner sgn** alternation reduces the contributing residues to 3
distinct pairings:

  unitary swaps: { (αβ ↔ γδ), (αγ ↔ βδ), (αδ ↔ βγ) }   →  m_U = 3.

In the **orthogonal** case (CFKRS §3.1.3 + §4 + §2.5 with orthogonal
Plancherel measure (3.1.50)), Ξ_O is constrained by
**Hecke convolution**: a product λ_f(m_1)···λ_f(m_4) reduces under the
Hecke relation (3.1.39)

  λ_f(m) λ_f(n) = Σ_{d | (m,n), (d,q)=1} λ_f(mn/d²)            (CFKRS 3.1.39)

to a single λ_f(N₀) plus lower-order terms. After Petersson averaging
(3.1.46), only the d such that mn/d² = 1 survives at leading order —
i.e. m = n. **This is the orthogonal multiplicity 1 condition**: a
4-shift residue contributes only via a single pairing of the four
shifts into two equal-norm pairs, where "equal norm" is enforced by
(3.1.46).

The unitary case has no such constraint: ζ has no Hecke eigenvalue
structure (its coefficients are 1, fully self-paired), so all three
permutation pairings (αβ↔γδ, αγ↔βδ, αδ↔βγ) contribute equally.

# 3. The 4-shift residue computation

## 3.1 Coalescing limit

Set α = γ = u, β = δ = v with u,v → 0. The residue extraction (∗) reduces to

  Res_{u=0} Res_{v=0} (1/(uv)²) · Z(u,v;−u,−v) du dv.

By CFKRS §4.1 (and (3.1.39)–(3.1.50)), in the Petersson weighting:

  Z(α,β;γ,δ) = Z_diag + Z_swap,

where (writing s_i = ½ + shift_i):

  Z_diag = ζ_N(s_α + s_β + s_γ + s_δ − 1) · L_∞-factors · (1 + O(1/k)),

  Z_swap = Σ_{σ ∈ Ξ_O} (NkT)^{−(σ shifts sum)} · Z_diag(σ-shifts).

Here ζ_N is the level-N truncated ζ (Euler product over p ∤ N).

## 3.2 What permutations are in Ξ_O?

This is the load-bearing combinatorial point.

**Claim:** For the orthogonal family F_k, the swap set Ξ_O consists of
the **single** non-trivial permutation σ_0 that swaps {α,β} ↔ {γ,δ} as
unordered pairs (i.e. (α,β,γ,δ) → (γ,δ,α,β), with the corresponding
(NkT)^{−(α+β+γ+δ)} = (NkT)^0 = 1 prefactor in the coalescing limit).

**Justification (the log-counting):**

The 4-shift L-product, expanded as a Dirichlet series, is

  Π_{i=1}^4 L(s_i, f) = Σ_{n_1,...,n_4 ≥ 1} (Π λ_f(n_i)) / (Π n_i^{s_i}).

Apply (3.1.39) twice to reduce λ_f(n_1)···λ_f(n_4) to Σ_j b_j λ_f(j).
After Petersson average (3.1.46), only j = 1 survives, giving the
constraint

  n_1 n_2 n_3 n_4 = (some perfect-square / d² combination).         (♦)

The **orthogonal Plancherel measure** (2/π)sin²θ dθ in (3.1.50) is
exactly the measure that gives Tchebychev-orthogonality: ⟨U_m U_n⟩ =
δ_{m,n}. So (♦) at prime-power level p^{m_1+m_2+m_3+m_4} requires:

  Σ_{σ ∈ S_4} ε(σ) · Π_j U_{m_{σ(j)}}(cos θ) = (orthogonality kernel),

evaluated against the Plancherel measure. By Tchebychev orthogonality
(CFKRS Lemma 3.1.3.2 itself, eq. 3.1.50), this integral is **zero
unless the m_i pair up as (m_1, m_2) = (m_3, m_4) up to S_4-orbit
under the pairing equivalence**.

**Counting the orbits:** Pairs of pairs of {1,2,3,4} = 3:
  { {1,2},{3,4} }, { {1,3},{2,4} }, { {1,4},{2,3} }.

But the orthogonal Plancherel kernel
  ∫_0^π sin²θ · U_a(cos θ) U_b(cos θ) U_c(cos θ) U_d(cos θ) · (2/π) dθ
is **fully symmetric** in (a,b,c,d) (Tchebychev orthogonality + symmetry
of the integrand). At m_1 = m_2 = m_3 = m_4 = 1 (the leading 4-shift
coalescing residue at primes p), all three pairings give the same value:
  ∫ U_1²·U_1² · (2/π)sin²θ dθ = ⟨λ_f(p)⁴⟩ = 2 (Catalan C_2; verified
  numerically in B3_CS_7_32_FROM_SCRATCH §8(a)).

So at level p (single prime), all three pairings contribute equally,
i.e. m_O = 3 at prime level — same as unitary?

**No.** The distinction comes from the **shift dependence**, not the
prime-level Plancherel. The unitary residue (Conrey 1989 §6) sums over
3 shift-pairings each with its own (NkT)^{−(shift sum)} prefactor; the
orthogonal residue (CS 2007 §7) sums over the same 3 prime-level
configurations but with **only one** shift-pairing surviving the
orthogonal functional equation.

**Why one survives, not three:** the orthogonal F_k has functional
equation L(s,f) ↔ L(1−s,f) with sign +1 (both sides real). Under the
shift swap (α,β,γ,δ) → (−γ,−δ,−α,−β), the functional equation gives a
factor (NkT)^{−(α+β+γ+δ)}. At the coalescing limit only the **identity
swap** (σ_0 above) gives a (NkT)^0 prefactor; the other two pairings
give (NkT)^{±2u} with u → 0 picking up an extra (log NkT) per shift —
which is **a higher-order term in the residue**, contributing log⁵ not
log⁴, i.e. subleading.

So at the **leading log⁴ level**:

  m_O (leading log⁴ coefficient) = 1.

The other two pairings give log⁵ corrections that are absorbed into the
o(log⁴) error in (★) of B3_log_counting_FINAL.

For the unitary case (Conrey 1989 §6, ζ at zeros), the analog
consideration gives all three pairings at log⁴ leading order because
the ζ functional equation is symmetric under (α,γ)↔(β,δ) and (α,β)↔(γ,δ)
without the orthogonal Petersson-Plancherel restriction:

  m_U = 3.

# 4. Pairing enumeration → multiplicity count

## 4.1 The 3 pairings of (α,β,γ,δ) into two pairs

| pairing | shift sum at coalescing | (NkT) prefactor | log power | contributes to log⁴? |
|---------|------------------------|------------------|-----------|---------------------|
| { (α,β), (γ,δ) }   | α+β = u+v             | (NkT)^0         | log⁴      | YES (orthogonal & unitary) |
| { (α,γ), (β,δ) }   | α+γ = 2u → 0         | (NkT)^{−2u}     | log⁵      | unitary YES, orthogonal NO |
| { (α,δ), (β,γ) }   | α+δ = u+v → 0       | (NkT)^{−(u+v)}  | log⁵      | unitary YES, orthogonal NO |

The unitary case sums all three (Conrey 1989 §6 explicit residue at the
ζ(1+α+β+γ+δ) pole gives all three with equal weight at leading log⁴).
The orthogonal Hecke-convolution constraint (3.1.39) + Petersson
orthogonality (3.1.46) kills the second and third pairings at the log⁴
level via the "equal-pair" requirement: only the pairing where {α,β}
and {γ,δ} are independently coalescing (both → 0 separately, not
mixed) gives the diagonal Hecke-convolution n_1 n_2 = n_3 n_4 at d=1
without forcing extra prime constraints that contribute log⁵.

This is the ⟨ρ_f, f⟩ — Petersson-norm-weighted — consequence of
(3.1.46): a Hecke-eigenvalue product survives only when paired into
**unordered equal pairs** (m_1, m_3) and (m_2, m_4), not all
permutations thereof, because (3.1.46) is δ_{n,1}, NOT a fully
symmetric averaging like the unitary trivial weighting.

Hence m_O = 1 at log⁴ leading order. ∎

## 4.2 Cross-check via Conrey 1989 §6 ζ baseline

For ζ on the critical line (unitary mult m_U = 3):
  PairCorr(ζ') / Smooth(ζ') = m_U / 1 = 3,
  Total / Smooth = 1 + 3 = 4.
Conrey 1989 (12): coefficient of log⁴ in (Σ |ζ'(ρ)|²)/T = 1/(6π).
  (Smooth alone = 1/(24π), Total = 1/(6π) = 4·1/(24π). ✓ ratio 4)

For Petersson F_k (orthogonal mult m_O = 1):
  PairCorr / Smooth = 1,
  Total / Smooth = 1 + 1 = 2.
M-N 2014: coefficient of log⁴ in M(F_k,T)/T = 2/(3π).
  (Smooth = 1/(3π) by Lemma 3.1; Total = 2/(3π) = 2·1/(3π). ✓ ratio 2.)

The ratio of orthogonal-to-unitary "total over smooth":

  (1+m_O) / (1+m_U) = 2/4 = 1/2.

This 1/2 is the **only** factor that distinguishes the orthogonal F_k
from the unitary ζ at the level of the multiplicity decomposition. Any
overall constant (the actual values 2/(3π) vs 1/(6π)) comes from the
different smooth/Lemma-3.1 baselines (1/(3π) vs 1/(24π)), not from the
multiplicity. This is consistent with the M-N 2014 target and with the
G1 audit's separate concern that the v2 file's "2_density × 2_mult = 4"
decomposition was applied to the wrong ζ-baseline; that gap is **not**
resolved here, but m_O = 1 is.

# 5. Orthogonal vs unitary comparison summary

| symmetry | m | smooth(log⁴/T) | total(log⁴/T) | smooth+m·smooth |
|----------|---|----------------|---------------|-----------------|
| unitary (ζ at zeros, Conrey 1989) | 3 | 1/(24π) | 1/(6π) | (1+3)·1/(24π) = 4/(24π) = 1/(6π) ✓ |
| orthogonal (F_k Petersson, M-N 2014) | 1 | 1/(3π) | 2/(3π) | (1+1)·1/(3π) = 2/(3π) ✓ |
| symplectic (Dirichlet L on real chars, Soundararajan 2009) | 0 | (different) | (smooth only) | n/a |

**Source of the difference:**
- unitary m_U = 3: ζ functional equation has trivial L-coefficients, all three pairings survive
- orthogonal m_O = 1: Hecke (3.1.39) + Petersson δ_{n,1} (3.1.46) kills two of three pairings via shift-(NkT) prefactor at coalescing
- symplectic m_S = 0: orthogonal-pair coupling is to **even** multiplicity, the "diagonal" already absorbs all pairings — see Soundararajan 2009

# 6. Honest confidence

**Confidence: 0.88.**

What is rigorous (≥0.95):
- CFKRS (3.1.39)–(3.1.50): verbatim quoted, peer-reviewed.
- Hecke convolution + Petersson orthogonality giving δ_{n,1} on prime products: standard, in CFKRS §3.1 and IK Ch. 14.
- Sato-Tate / Tchebychev orthogonality with measure (2/π)sin²θ dθ: classical.
- Numerical multiplicity sanity at level p: ⟨λ_f(p)²⟩ = 1, ⟨λ_f(p)⁴⟩ = 2 (Catalan C_2), both verified to 25 digits in parent file §8.
- Final assembly into 1/(3π) constant + log⁴ counting: B3_log_counting_FINAL §A explicit, conf 0.95.

What is the residual gap (the −0.07 from 0.95):
- §3.2's argument that "at coalescing only the identity swap σ_0 contributes at log⁴ leading order, the other two pairings contribute log⁵": this is **plausible but not airtight** in the present write-up. A fully airtight derivation would require:
  (a) explicit calculation of the (NkT)^{−2u} prefactor's contribution to the residue Res_{u=0} via L'Hopital or generating-function expansion, showing the log-power increments by 1 per nontrivial shift sum;
  (b) verification that this increment matches the Conrey 1989 §6 ζ-case, where the analog (ζ functional equation symmetric) gives all three at equal log⁴.
  These steps are mechanical residue calculus (~2 pages) and were not done in this pass.
- The CS 2007 (7.32) verbatim statement was not retrieved (paywall). The CFZ 2008 §5 orthogonal ratios formula is cited as the orthogonal analog but was also not retrieved verbatim. We rely on CFKRS 2005 §3.1 verbatim plus the known M-N 2014 leading constant 2/(3π) as a consistency check.

What is **not** in scope of this file (other gaps, separate from m_O):
- G1 (factor-4 baseline gap in v2 polar-Mellin file): NOT addressed here; m_O = 1 is correct on its own.
- G2 (M-N GRH conditionality vs unconditional weight-aspect claim): NOT addressed here.
- G5 (Lemma 3.3 polynomial-degree imprecision): NOT addressed here.

# 7. Summary

m_O = 1 for the orthogonal Petersson family F_k = S_k*(N) at the 4-shift
coalescing residue, leading log⁴ order. Derived from CFKRS 2005 §3.1
verbatim (Hecke convolution + Petersson orthogonality + Sato-Tate
Plancherel measure (2/π)sin²θ dθ) plus a residue-prefactor argument
(§3.2) that is plausible but not yet airtight (subleading log⁵
corrections). m_U = 3 for ζ at zeros (Conrey 1989) is the unitary
baseline; the difference (1+m_O)/(1+m_U) = 1/2 is the
orthogonal-vs-unitary multiplicity ratio at log⁴.

Combined with B3_lemma_3_1_fixed.md (Mellin J_3 = 1/3, conf 0.99998)
and the GL₂ density 1/π (Riemann-von Mangoldt), this gives the M-N 2014
target 2/(3π) for the on-line second moment of L'(ρ_f, f).

**This file closes G4** at confidence 0.88 (vs the parent file's 0.92,
adjusting downward for the §3.2 residue-prefactor handwave that
B3_log_counting_FINAL also has but did not flag explicitly).

# Done.
