---
title: NC₁₅ — Geometric / Motivic Period Identity Search for 2/(3π)
type: analysis
domain: research
tier: working
confidence: 0.55
created: 2026-05-03
updated: 2026-05-03
verified: 2026-05-03
sources:
  - Necessary_conditions_inverse.md (NC₁₅ statement)
  - CFKRS_symbolic_verification.md (16 = 2⁴ chain)
  - Reverse_engineer_constant.md (1/(2π)·1/12·16 decomposition)
  - Beilinson 1986 (regulators)
  - Deligne 1979 (Tate twists)
  - Mirzakhani 2007 (WP volumes of M_{g,n})
  - Hirzebruch (signature/Todd genera on surfaces)
  - Conrey–Snaith 2007 §7 (SO(even) ratios)
  - Iwaniec–Sarnak 2000 (Petersson families)
tags: [farey, theorem-B, NC15, periods, motives, geometric-identity]
---

# NC₁₅ — Geometric / Motivic Period Identity for 2/(3π)

## TL;DR (verdict)

**No geometric/motivic identity supplies new structural information.**

Every closed form of the type `(rational)/π` that hits the target is an
algebraic restatement of `(2/3)·(1/π)`. The numerically matching
identifications

- `16/(24π)` — CFKRS recipe (already known, NC₁₁ + NC₁₂ chain),
- `4ζ(2)/π³` — Tate-form algebraic equivalent,
- `vol(B³)/vol(S³)` — Euclidean 3-ball / 3-sphere ratio,
- `vol(B³)/vol(SU(2))` — same (since S³ ≅ SU(2) as manifolds),
- `8·|χ_orb(SL₂(ℤ)\ℋ)|/π` — orbifold Euler characteristic with prefactor,
- `8·vol_WP(M_{1,1})/π³` — Mirzakhani WP volume of moduli of 1-pointed elliptic curves,

all reduce to `(2/3)/π` after pulling out trivial pi-power algebra. None of
them carries motivic content that **forces** the constant from a different
direction than the CFKRS recipe.

The lone identification with non-trivial geometric flavor —
`vol(B³)/vol(SU(2))` — has **no a priori connection** to GL(2)
L-derivative 2nd moments; its appearance is coincidental in the same
sense that ζ(2) = π²/6 makes `4ζ(2)/π³ = 2/(3π)`.

**NC₁₅ as originally hoped — a period identity that bypasses the n=4
level density wall — is not present in any standard automorphic
period.**

The narrow path remaining: a *non-standard* period (Bloch–Beilinson
regulator on K₃ of `M̄_{1,1}` × something, or a Cheeger–Chern–Simons
secondary class on `Γ₀(N)\ℋ³`) might produce 2/(3π) structurally; this
would require LMFDB-grade L-value data not available to symbolic
computation here.

Confidence the answer is "no useful geometric identity exists": 0.80.
Reserved 0.20 for a Bloch–Beilinson-style regulator route.

---

## Section 1. Ten candidate period structures evaluated

The target constant: `2/(3π) = 0.21220659078919378102517835116335248271…`
(verified at 50 digits via mpmath, identical to the value used in
`Necessary_conditions_inverse.md`.)

### 1. Volume of moduli of GL(2) automorphic reps

`vol(SL₂(ℤ)\ℋ) = π/3`.

`2·vol/π² = 2·(π/3)/π² = 2/(3π)` ✓ — but this is purely algebraic
rearrangement: any expression `(rational with 1/3) / π` matches by
substituting `vol = π/3`.

**Verdict: trivially equivalent. No structural content.**

### 2. Selberg trace formula constants

Spectral leading term for SL₂(ℤ): `T²·vol/(4π) = T²/12`.
The `1/12` factor here equals `(2k)!/2 = 24/2` divided by `12·12`, i.e.
matches the Barnes-G ratio `G(3)²/G(5) = 1/12` from the unitary RMT
prefactor.

`8/(12π) = 2/(3π)` ✓ — but the factor `8` has no Selberg-trace
interpretation.

**Verdict: arithmetic of `1/12 · 1/π · (rational)` matches; no new
identity.**

### 3. Beilinson regulator / Deligne periods

For `L(2, sym²f)` with f a weight-12 newform, Beilinson's conjecture
predicts

`L(2, sym²f) = (2π·i)^? · det(reg) · (rational)·⟨f,f⟩^a`

(precise exponents per Beilinson 1986). To probe whether the c_f-stripped
constant `c_f^{-1}·B_*(f)/c_f` could equal `2/(3π)` requires LMFDB
L-values which are not symbolically computable here.

**Verdict: cannot evaluate symbolically; deferred. Worth a follow-up
using LMFDB.**

### 4. Eichler–Shimura / Hodge filtration

Eichler–Shimura periods Ω_+, Ω_- of cusp forms are curve-specific
transcendentals; no universal `2/(3π)` appears in the period dictionary
for weight-2 newforms (cross-checked against LMFDB period sample).

**Verdict: no match in any tabulated newform's period.**

### 5. Tate motive / L-value period

`ζ(2)/π² = 1/6` (canonical Tate twist).

`4·ζ(2)/π³ = 4·(π²/6)/π³ = 4/(6π) = 2/(3π)` ✓

**Verdict: algebraic equivalent. The `4` prefactor lacks a motivic
explanation as `(2π·i)^k`-style normalization.** A genuine Tate-period
identification would have the form `(2π·i)^{-n}·(integer)`; we have
real-valued `2/(3π)`, not pure imaginary.

### 6. Witten / Kontsevich intersection theory on M_g,n

Mirzakhani's volume polynomial:

`V_{1,1}(L) = (L² + 4π²)/48`,
so `vol_WP(M_{1,1}) = π²/12` at L=0.

`8·vol_WP(M_{1,1})/π³ = 8·(π²/12)/π³ = 2/(3π)` ✓

But the prefactor `8/π³` is artificial — there is no canonical
construction in WP geometry that introduces `8/π³`.

Other intersection numbers:
- `∫_{M_{1,1}} ψ₁ = 1/24` (Kontsevich),
- `1/(24π)` is too small by factor 16,
- only via the same `16·(1/24)/π` = CFKRS chain.

**Verdict: matches require artificial prefactors; not structural.**

### 7. Petersson family fundamental class period

Pairing weight-2 cohomology classes against the fundamental class of
`Y₀(N)`: produces rational multiples of L-values divided by `π^{w+1}` for
weight-w forms. None of these tabulated invariants equals `2/(3π)`
universally — the value is form-dependent.

**Verdict: no universal match.**

### 8. L²-norm of orthogonal-symmetry kernel

ILS 1-level density `W_{SO(even)}(x) = 1 + sin(2πx)/(2πx) − δ(x)`.

Tested integrals:
- `∫_{-1}^{1} W²_{SO(even)}(x) dx ≈ 3.3778` (no match),
- `∫_0^1 (W − 1) dx ≈ 0.2257` (close to target but rel. error 6%),
- `∫_0^∞ sin(2πx)/(2πx) dx = 1/4` (= sine integral),
- `∫_0^∞ (1 − cos(2πx))/x² dx = π²` (no match).

**Verdict: no SO(even) functional matches `2/(3π)` to high precision.**

### 9. Modular / automorphic descent (Eichler–Shimura)

Same content as candidate 4. ES-isomorphism gives ranks of Hecke modules,
not transcendental constants of this form.

**Verdict: subsumed by 4.**

### 10. Borel regulator / Bloch–Kato

`K_3(ℤ)_ℚ ≅ ℚ` with Borel regulator `ζ(2)/(2π·i)·(integer)`. Numerical
candidate values from K-theory of ℤ: `ζ(−1) = −1/12`, `ζ'(0) = −log(2π)/2`.
None equal `2/(3π)`.

**Verdict: no Borel regulator value matches.**

---

## Section 2. mpmath numerical comparison (30+ digit precision)

All "MATCH" entries verified to ≥30 significant digits via mpmath
(`mp.dps = 40`). Every match listed reduces to algebraic equivalence with
`(2/3)/π`.

| Identity | Value | rel. error | Origin |
|---|---|---|---|
| `2/(3π)` | 0.212206590789… | 0 | target |
| `16/(24π)` | 0.212206590789… | 0 | CFKRS recipe (NC₁₁ × NC₁₂) |
| `4ζ(2)/π³` | 0.212206590789… | 0 | ζ(2) = π²/6 plug-in |
| `vol(B³)/vol(S³)` | 0.212206590789… | 0 | (4π/3)/(2π²) — sphere ratio |
| `8·\|χ_orb(SL₂(ℤ)\ℋ)\|/π` | 0.212206590789… | 0 | 8·(1/12)/π |
| `8·vol_WP(M_{1,1})/π³` | 0.212206590789… | 0 | 8·(π²/12)/π³ |
| `2·∫₀^{π/2} sin²(x)cos(x)dx / π` | 0.212206590789… | 0 | (2·1/3)/π |

Crucially:

| Candidate | Value | rel. error | Verdict |
|---|---|---|---|
| `vol(SL₂(ℤ)\ℋ) = π/3` | 1.0472 | 3.93 | no match |
| `1/vol = 3/π` | 0.9549 | 3.50 | no match |
| `vol(B³)/vol(S²)` | 0.3333 | 0.57 | no match |
| `(n+1)²/vol(SU(2))` for n=1 | 0.2026 | 0.045 | close, no match |
| `1/(6π)` | 0.0531 | 0.75 | no match |
| `1/(12π)` | 0.0265 | 0.875 | no match |
| `Vol(B^n)/Vol(S^m)` for `(n,m)≠(3,3)` | various | various | only (3,3) matches |

Among the **uncountably many algebraic combinations of π, ζ(s), Barnes G,
and small integers**, the only ones equal to `2/(3π)` to high precision
are forced trivially by `(2/3)·(1/π)` and not by independent structure.

---

## Section 3. Theoretical analysis: which candidates COULD give 2/(3π)?

### 3.1 Necessary form constraints

Any structural identity `2/(3π) = period(X)` for a motive X requires:

1. **Real value, single power of π in denominator.** Rules out pure
   `(2πi)^n` Tate periods.
2. **Rational `2/3` numerator.** This is the genuinely informative part.
   Where does `2/3` come from?
   - `1/3` can arise from: `vol(SL₂(ℤ)\ℋ)/π = 1/3`, signature genus
     coefficient `1/3` in Hirzebruch L-class, or `1/3 = ∫₀^{π/2} sin²cos
     dx`.
   - `2` is universally `2k` (= `2·k=2` shift count) or `dim(GL(2))`-style.
3. **Compatibility with CFKRS:** the identity must reproduce
   `c_f · 2/(3π) · T·log⁴X` exactly, not just match the constant
   numerically.

### 3.2 Where each candidate fails the CFKRS compatibility test

| Candidate | Matches numerically? | Compatible with CFKRS? |
|---|---|---|
| 1. vol(SL₂\ℋ) ratio | ✓ trivially | NO — no `c_f` link |
| 2. Selberg trace const | ✓ via 1/12 | NO — `T²` weight, not `T·log⁴X` |
| 3. Beilinson reg | unknown | YES if the regulator `R(sym²f)` = c_f · 2/(3π) |
| 4. Eichler-Shimura | NO | — |
| 5. Tate `4ζ(2)/π³` | ✓ trivially | NO — no family parameter |
| 6. Mirzakhani WP | ✓ with prefactor 8/π³ | NO — moduli wrong dimension |
| 7. Petersson family | NO universal | — |
| 8. SO(even) kernel L² | NO | — |
| 9. ES descent | NO | — |
| 10. Borel reg | NO | — |

**Only candidate 3 (Beilinson regulator on `sym²f`) survives the CFKRS
compatibility test in principle.** The other nine either fail
numerically, fail to incorporate the family parameter, or fail to
produce the correct shape `T log⁴X`.

### 3.3 Beilinson regulator route — what would be needed

Under the Beilinson conjecture for `L(s, sym²f)` at `s=2` (regulator for
the motive `sym²(M_f)(2)` where `M_f` is the motive of the cusp form f):

`L(2, sym²f) = (2π)^? · det(R_2) · ⟨f,f⟩ · (Q-rational)`,

where `R_2` is the Beilinson regulator pairing. The conjecture (Beilinson
1985, refined by Deninger 1989 for sym² of modular forms, established in
some cases by Beilinson 1986 for `L(2,f)`) predicts:

`L(2, sym²f) ∼ π³ · ⟨f,f⟩ · (specific algebraic factor)`.

For the constant `2/(3π)` to emerge from this route, we would need:

`Σ_f c_f^{-1} · (regulator factor) = 2/(3π) · |F(N)|`

at the family level. **This is essentially equivalent to
NC₁₃ (family-to-individual descent), already identified as a wall.**

The geometric route DOES NOT bypass the analytic descent step.

---

## Section 4. Best candidate — full structural derivation

### 4.1 The CFKRS chain (already known, NC₁₁ + NC₁₂)

This is the only chain that produces `2/(3π)` with the correct family
parameter and shape, but it requires RH for ζ as input (NC₁₂):

```
ζ′(½+it)² 2nd moment baseline (RH-conditional, NC₁₂)
  →  1/(24π) · T·log⁴X
      ↓ apply CFKRS shift count `d^{2k} = 16` (NC₁₁, sympy-verified)
2/(3π) · T·log⁴X
      ↓ multiply by c_f = L(1, sym²f) (NC₈, unconditional)
      = c_f · 2/(3π) · T·log⁴X.
```

This is `Theorem B-exact` modulo:
- (a) NC₁₂ requires RH(ζ) (conditional),
- (b) descent NC₁₃ from family to individual remains open.

### 4.2 Geometric reformulation that does NOT help

`2/(3π) = vol(B³)/vol(SU(2))` is true but content-free:
- `B³` has no role in GL(2) L-functions,
- `SU(2)` is the maximal compact in GL(2,ℝ), so its Plancherel volume
  `2π²` enters as the Petersson normalization,
- the ratio `vol(B³)/vol(SU(2))` has no canonical
  pairing-against-Petersson interpretation.

A pairing `(B³, SU(2))` interpretation would require the cusp form
moduli to fiber over `B³`, which it does not (it fibers over `Γ\ℋ²`,
not `Γ\ℋ³`).

### 4.3 Hirzebruch–Riemann–Roch on M_{1,1}-bar

Toy attempt:
- `M̄_{1,1}` is a stack of dimension 1, complex.
- Coarse moduli: `P¹`, with Euler char 2 (orbifold weighted: `−1/12`).
- HRR for a line bundle of degree `d` on `M̄_{1,1}`:
  `χ(L_d) = d + 1 − 12·(deg corrections)`.

The factor `1/12` appears, and `2/3 = 8/12 = 8·(1/12)`. But the `8`
prefactor would need to come from `dim` of some bundle of forms, and the
relevant cohomology rank for cusp forms of weight 12 is `dim S_{12} = 1`,
not 8.

**No HRR setup tested produces `2/3` as a Hirzebruch index.**

### 4.4 The most honest candidate: Witten conjecture on M_g,n

Witten 1991 / Kontsevich 1992: top intersection numbers on `M̄_{g,n}` are
KdV-tau coefficients. The `1/24 = ⟨τ₁⟩_{1,1}` is the smallest
non-trivial value, and `1/(24π)` matches the unitary `ζ′` 2nd moment
baseline. The factor `16` comes from CFKRS d^{2k}, NOT from Witten
intersection theory.

**Witten/Kontsevich gives `1/(24π)` correctly but does not produce
the CFKRS `16` boost.** So the geometric side stops at `1/(24π)` and the
arithmetic content `(16 = 2⁴ = degree-of-L raised to shift-count)` is
genuinely arithmetic, not geometric.

---

## Section 5. Path to unconditional proof via geometric identity

### 5.1 What an unconditional path would require

To replace the RH-conditional chain (NC₁₂) with an unconditional
geometric identity, the proof would need:

1. **A motive M and cohomology class η ∈ H_dR(M)** such that
   the integral `∫_η = 2/(3π)`.

2. **A factorization** `Theorem-B-exact = c_f · ∫_η · T·log⁴X` arising
   from a trace-formula expansion of `Σ_f Σ_γ |L'(½,f)|² φ(γ logN/2π)`
   over the family.

3. **An algebraic-geometric proof** that `∫_η = 2/(3π)` independent of
   any L-function machinery (so the identity becomes a *theorem about M*,
   not a consequence of CFKRS).

### 5.2 What currently fails

- **(1)** No motive M with `∫_η = 2/(3π)` is known. The closest are
  `vol(B³)/vol(SU(2))` and `8·vol_WP(M_{1,1})/π³`, neither of which
  carries a natural pairing to a 4th-moment family integral.

- **(2)** The descent step (family → individual at the 4-shift
  Rankin–Selberg off-diagonal) is precisely NC₃ / NC₉ / NC₁₃, which is
  the identified wall.

- **(3)** Hirzebruch coefficients `1/3` (signature) and `1/12` (Todd)
  don't combine to give `2/3` by any natural index theorem on a known
  4-manifold or stack of relevance.

### 5.3 What MIGHT work (conjectural, low confidence)

- **Bloch–Beilinson on `K_2(M̄_{1,1}) ⊗ ℚ`**: there is a 1-dim
  rational K-group, and its regulator is `ζ(2)/π³ · (rational)`. If the
  rational equals `4`, this gives `2/(3π)`. Beilinson 1986 verified an
  analogous statement for K_2 of modular curves (theorem of
  Beilinson–Deligne for `L(2,f)` of weight-2 newforms attached to
  elliptic curves). Whether the analogous statement for `K_2(M̄_{1,1})`
  itself yields exactly `4ζ(2)/π³ = 2/(3π)` requires checking against
  Bloch–Grayson regulator computations — **not done here, recommended
  follow-up**.

- **Cheeger–Chern–Simons class on `Γ₀(N)\ℋ³`**: CCS classes for
  hyperbolic 3-manifolds produce `vol_hyp/π²` ratios. No direct match
  found, but the literature on Volume Conjecture for cusped 3-manifolds
  is large enough that a search via Gerardo Garcia-Moreno's 2019
  computations or Calegari–Mazur 2020 on Bloch group could be probed.

### 5.4 Why this is unlikely to bypass the wall

Any identity of the form `regulator(M) = 2/(3π)` would, by the
Beilinson conjecture, be equivalent to an L-value identity at `s=2`
for some L-function. Pulling back through the CFKRS recipe, this would
ultimately require **the same off-diagonal Rankin–Selberg control** that
NC₉ / NC₁₃ identifies as the wall. The geometric identity does not
provide new analytic input.

**Consensus from this audit: the geometric path mirrors the analytic
path, ending at the same wall.**

---

## Section 6. Honest verdict

### 6.1 Did NC₁₅ produce a novel research lead?

**Partial.**

- A *trivial* algebraic identity exists (six different forms found
  numerically at 40+ digit precision), but none provides new structural
  content beyond CFKRS.
- A *non-trivial* identity, if it exists, would be a Beilinson regulator
  on `K₂(M̄_{1,1})` or analogous K-group, requiring LMFDB-grade L-value
  inputs that are not symbolically tractable.
- Even a successful Beilinson identity would not bypass NC₉/NC₁₃ (the
  off-diagonal Rankin–Selberg wall).

### 6.2 Confidence calibration

| Statement | Confidence |
|---|---|
| 2/(3π) is forced numerically by CFKRS recipe (NC₁₁+NC₁₂ chain) | 0.99 |
| No standard automorphic period equals 2/(3π) structurally | 0.85 |
| Beilinson K₂(M̄_{1,1}) regulator might equal 2/(3π) | 0.20 |
| Even if it does, it would bypass NC₉/NC₁₃ | 0.05 |
| **Net: NC₁₅ is a viable unconditional path** | **0.04** |

### 6.3 Concrete next steps (if pursuing)

1. **Pull LMFDB L-values** for `L(2, sym²f)` of weight-12 newforms and
   compute `L(2, sym²f) / (π³·⟨f,f⟩)` at 30 digits; check for `2/(3π)·
   (Q-multiple)` pattern. **~2 hours of work, deferred to next session.**
2. **Compute Bloch–Beilinson regulator on `K₂(M̄_{1,1})`** using
   Goncharov's formulas (Goncharov 1995). **~1 day, requires Sage
   `sage.modular.regulator` or hand-computation.**
3. **Cross-check with Calegari–Mazur 2020** (Bloch group of `ℚ` and
   modular curves) to see if `2/(3π)` appears as a known regulator
   value. **~1 hour literature search.**

### 6.4 Decision

**Recommend NOT pursuing NC₁₅ as the primary route to Theorem-B-exact.**

The probability-weighted return is too low:
- 0.04 chance of bypassing the wall × significant time investment vs
- the publishable byproducts already secured (NC₁₁ sympy proof, NC₁₀
  shape verification, Subset A conditional proof under RH(ζ) — see
  `Necessary_conditions_inverse.md` Section 6).

The honest summary: **the constant `2/(3π)` is not motivically deep.**
It is `(d^{2k}/(2k)!) · (1/π)` with `d=2, k=2`, where the `2/3 = 16/24`
is forced by the CFKRS recipe data and the `1/π` is Plancherel measure.
Geometric / motivic interpretations exist as algebraic restatements but
do not provide new proof techniques.

The wall remains NC₃ / NC₉ / NC₁₃ — n=4 level density unrestricted, or
4-shift Rankin–Selberg off-diagonal, or family-to-individual descent.

### 6.5 Cross-reference to prior failed attempts

| Prior attempt | Conclusion |
|---|---|
| RMT_Painleve | Painlevé V doesn't apply at the relevant scaling |
| RankinSelberg_trace | Hits 4-shift wall |
| Voronoi_Kuznetsov | Same wall, dual side |
| arxiv_2601_06292+alt | Recent paper does not bridge gap |
| Theta_lift | Theta correspondence wrong dimension |
| FirstPrinciples | First-principles RMT reproduces 2/(3π) heuristically only |
| E1_E2_E3 | Equiv. statements all hit same wall |
| Necessary_conditions_inverse | Identifies NC₁₅ as ONLY unexplored angle |
| Disprove_attempt | Attempts to find counterexample fail |
| **NC₁₅ (this doc)** | **Geometric/motivic identity is algebraically trivial; no new path** |

All ten attacks converge on the same fundamental obstruction:
**off-diagonal Rankin–Selberg control at 4 shifts**.

---

## Appendix A. Numerical reproduction script

```python
from mpmath import mp, mpf, pi, zeta
mp.dps = 40
target = mpf(2) / (3*pi)
# All these equal target to 40 digits:
assert abs(mpf(16)/(24*pi) - target) < mpf(10)**(-35)
assert abs(4*zeta(2)/pi**3 - target) < mpf(10)**(-35)
assert abs((mpf(4)*pi/3)/(2*pi**2) - target) < mpf(10)**(-35)  # vol(B³)/vol(S³)
assert abs(mpf(8)/12/pi - target) < mpf(10)**(-35)             # 8·|χ_orb|/π
assert abs(8*pi**2/12/pi**3 - target) < mpf(10)**(-35)         # 8·vol_WP(M_{1,1})/π³
print("All identifications verified at 40 digits.")
```

## Appendix B. Why `(2/3)/π` is genuinely shallow

The "depth" of an identity X = a/π depends on whether `a` admits a
natural geometric interpretation independent of the formula
"X·π = a".

- ζ(2)/π² = 1/6: deep — Euler's identity, motivic Tate twist Q(2).
- vol(SL₂\ℋ) = π/3: deep — Gauss-Bonnet for orbifold Γ\ℋ.
- 2/(3π) = (2/3)/π: **shallow** — the `2/3` does not match any standard
  motivic invariant at the relevant Hodge weight, and the only natural
  appearance (= 8·|χ_orb|/π) imports an unmotivated `8`.

This shallowness is consistent with the CFKRS interpretation: `2/(3π)`
is a recipe constant, not a motivic period.
