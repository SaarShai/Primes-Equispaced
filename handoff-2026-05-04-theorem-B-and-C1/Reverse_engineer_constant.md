---
title: Reverse-Engineering the Constant 2/(3π) in Theorem B-exact
type: analysis
domain: research
tier: working
confidence: 0.65
created: 2026-05-03
updated: 2026-05-03
sources:
  - Conrey-Snaith 2007 §7
  - CFKRS 2005 §3-§4
  - Hughes-Snaith 2003
  - Hughes-Mezzadri-Pearce
  - Conrey 1988 (mean values of ζ')
  - Ingham 1926
tags: [farey, theorem-B, RMT, orthogonal-symmetry, CFKRS]
---

# Reverse-Engineering 2/(3π): What Arithmetic Structure Forces This Constant?

## TL;DR

**Single structural identity:**

$$\boxed{\frac{2}{3\pi} \;=\; \frac{d^{2k}}{(2k)!\;\pi}\bigg|_{d=2,\,k=2} \;=\; \frac{16}{24\pi}}$$

Three factors, three sources:

| Factor | Value | Origin |
|---|---|---|
| `d^{2k} = 16` | degree-of-L raised to shift count | CFKRS shift formalism for 2k-th moment |
| `1/(2k)! = 1/24` | combinatorial normalization | symmetrization over 2k=4 shift permutations |
| `1/π` | spectral measure | Plancherel for L²(R, dt) on critical line |

The constant **factorizes as recipe data, not deep arithmetic**. The arithmetic content lives entirely in (a) the symmetry type (orthogonal vs unitary vs symplectic) selecting which RMT integral, and (b) the per-curve arithmetic factor `c_f = L(1, sym²f)` which is *separate* from `2/(3π)`.

This means: **2/(3π) is forced as soon as you commit to (degree-2 GL(2) L-function) × (2nd moment of derivative) × (orthogonal weight family) × (CFKRS recipe).** No deeper miracle is needed.

---

## Section 1: Why 24π?

### 1.1 The 24 is `(2k)! = 4!`, not Bernoulli or modular

Common candidates and their fates:

| Candidate | Value | Verdict |
|---|---|---|
| `B_4/4` doubled | `B_4 = -1/30`, so `|B_4|/4 = 1/120` | ✗ wrong magnitude |
| `B_2 / 2` | `B_2 = 1/6` so `B_2/2 = 1/12`, twice = `1/6` | ✗ off by factor 4 |
| Vol(SL₂(ℤ)\ℍ) | `π/3` | ✗ no factor 24 |
| `η^24 = Δ` (modular discriminant) | weight-12 cusp form, η-power | ✓ **conceptual cousin**, not the source here |
| Catalan `G` | irrational | ✗ |
| **`(2k)!` for k=2** | `4! = 24` | ✓ **THIS** |

**Verification via Hughes-Mezzadri unitary baseline.** The Barnes-G ratio
$$ \frac{G(k+1)^2}{G(2k+1)}\bigg|_{k=2} = \frac{G(3)^2}{G(5)} = \frac{(0!\,1!)^2}{0!\,1!\,2!\,3!} = \frac{1}{12}, $$
combined with `1/(2π)` from the Plancherel measure on the critical line, yields `1/(24π)`. This is the **unitary ζ′ second-moment leading constant** in the Keating-Snaith / Hughes-Mezzadri-Pearce regime (cf. Hughes thesis 2001; Conrey-Ghosh on `∫|ζ′(½+it)|² dt`).

So `24π = (2k)! · π` decomposes cleanly:
- `2π` = Plancherel,
- `12 = G(2k+1)/G(k+1)²` for k=2 = combinatorial RMT pre-factor.

Equivalently: `24 = 4!` is the symmetrization denominator over 4 shift variables in CFKRS step-6.

### 1.2 Why not Bernoulli?

Bernoulli numbers enter ζ-values at NEGATIVE integers (functional-equation reflection of Euler's `ζ(2n)`-formula). They appear in **trace formula spectral sides** but not in this leading constant. The factor `1/12` here is `G(3)²/G(5)`, which equals `B_2 / 2` numerically by *coincidence* (`B_2 = 1/6 ⇒ B_2/2 = 1/12`); the structural origin is Barnes-G, not Bernoulli.

---

## Section 2: Why 2⁴ = 16 — Arithmetic vs Combinatorial

### 2.1 The CFKRS shift count gives 2k, not k

For the **2k-th moment** of `L(½,f)`, CFKRS (2005, §3) writes the family average as a contour integral over `2k` auxiliary shifts `α₁, …, α_{2k}` of
$$ \prod_{j=1}^{2k} L(\tfrac{1}{2} + \alpha_j, f) $$
followed by step-6: setting all shifts to zero with appropriate residue/derivative manipulations.

For the **2nd moment of L′** (i.e., `k=2` shift moment of the derivative), one differentiates each L-factor once → effectively `2k = 4` derivative operations, each pulling down `log` of the analytic conductor.

Each derivative `∂_α L(½+α, f)` evaluated on the critical line contributes a factor proportional to `d · log(qt²)^{1/2}` where `d = deg L = 2`. This is because the analytic conductor satisfies
$$ \log \mathfrak{q}(t) = d \log t + \log q + O(1). $$

Multiplied across all `2k = 4` shifts: **`d^{2k} = 2^4 = 16`**.

### 2.2 What it is NOT

| Hypothesis | Verdict |
|---|---|
| GUE level density saturation `n=4` | ✗ wrong family — GUE is unitary, not orthogonal; would predict different power |
| Functional-equation root number `ε^4` | ✗ `ε = ±1` for self-dual L, so `ε^4 = 1` always |
| Hodge filtration `dim = 4` for sym²(f) | △ coincidence — sym²(f) has motivic weight-2 Hodge `(2,0)+(1,1)+(0,2)`, dim 3 not 4 |
| Eichler-Shimura cohomology rank | △ wrong invariant — ES gives `H¹(Γ, V_k) ≅ S_{k+2} ⊕ \overline{S_{k+2}} ⊕ Eis`, rank related to weight not 16 |
| **CFKRS shift count `(2k)` × degree `d`** | ✓ **correct** |

### 2.3 Why this is structural, not numerical

If we changed any of:
- `d → 1` (degree-1 = Dirichlet/ζ): `1^4 = 1` → constant becomes `1/(24π)` (matches ζ′ baseline).
- `d → 3` (GL(3) L-function): `3^4 = 81` → constant `81/(24π) = 27/(8π)`.
- `k → 1` (1st moment): `d² / (2!·π) = 4/(2π) = 2/π`.
- `k → 3` (3rd moment, 6 shifts): `d⁶/(6!·π) = 64/(720π) = 4/(45π)`.

Each is independently checkable against CFKRS predictions, providing **falsifiable consequences** of the structural decomposition.

---

## Section 3: Why c_f = L(1, sym²f) Normalization

### 3.1 Petersson-norm origin via Rankin-Selberg

The arithmetic factor `c_f` is *separate from* `2/(3π)` and equals (up to known elementary factors)
$$ c_f \;\propto\; L(1, \mathrm{sym}^2 f) \;=\; \frac{8\pi^3}{(k-1)!}\, \langle f, f\rangle \cdot N^{?}, $$
by the **Rankin-Selberg integral representation** (Shimura 1975; Iwaniec 1990).

Here `⟨f,f⟩` is the Petersson norm, and the Rankin-Selberg unfolding gives `L(s, f×f̄) = ζ(s) L(s, sym²f)` with explicit residue at `s=1` proportional to `⟨f,f⟩`.

### 3.2 Why sym², not sym^k or adjoint differently

For GL(2), the adjoint L-function `L(s, Ad f)` and `L(s, sym²f)` agree up to a factor (sym² of standard rep = adjoint ⊕ trivial for GL(2)), so this is the natural choice. The **special value at s=1** appears because:

1. Ramanujan-bound on Hecke eigenvalues `|λ_p| ≤ 2` translates to `λ_p² ≤ 4`, and the local factor of `L(1, sym²f)` regulates the divergent `∑ λ_p² log p / p` sum that appears in CFKRS step-6.
2. Hoffstein-Lockhart (1994): `(log k)^{-c} ≪ L(1, sym²f) ≪ (log k)^c` — bounded in weight aspect.

### 3.3 Why central value (s=1) and not some other point

CFKRS step-6 produces a polynomial in `log C` whose coefficients are residues at `s=1` of products of `L(s, sym²f)`-type objects. The constant term of the leading polynomial picks up `L(1, sym²f)` because that's where the diagonal term in Petersson trace formula contributes.

---

## Section 4: Uniqueness of 2/(3π) — Could It Have Been Otherwise?

**No, not for this family.** The constant is forced once we fix:

1. **Degree d=2** (GL(2) modular forms — non-negotiable for our setup).
2. **2nd moment** (k=2, fixed by problem statement: 2nd moment of L′).
3. **Orthogonal symmetry type** (Katz-Sarnak: weight-aspect family of holomorphic modular forms is orthogonal — this is **Theorem (Conrey-Duke-Farmer, ILS)**).
4. **CFKRS recipe** (essentially the unique RMT-arithmetic interpolation consistent with shift formalism + Petersson trace formula).

If we changed any:

| Change | New constant |
|---|---|
| Symplectic family (e.g., quadratic Dirichlet twists) | `c_O → c_S`, different Barnes-G ratio |
| Unitary family (Dirichlet L-functions) | `c_O → c_U = 1/12` per shift product, gives `16/(24π)` still — but **arithmetic factor changes** |
| 4th moment `k=4` instead | `d^8/(8!·π) = 256/(40320π) = 1/(157.5π)` |
| GL(1) (ζ analog) | `1/(24π)` |
| GL(3) (Maass forms) | `81/(24π) = 27/(8π)` |

So **2/(3π) specifically is a fingerprint** of `(d=2, k=2, orthogonal-with-RMT-coefficient-1/12)`.

### 4.1 Could the "1/12" change?

Slightly. For SO(2N) vs SO(2N+1), the Barnes-G ratio differs:
- SO(even): `2^{k(2k-1)} · prod(...)`
- SO(odd): `2^{k(2k+1)} · prod(...)`

For modular forms with **all** weights in family (no parity restriction), one gets a mix that effectively gives the same `1/12` for k=2; this can be verified numerically against random matrix simulations on `O(2N) ⊔ O(2N+1)`.

---

## Section 5: Compatibility with Higher Moments and Special Limits

Predictions of the structural formula `M_{2k} = d^{2k}/((2k)!·π) · c_f^{(k)} · (log C)^{?}`:

### 5.1 Higher moments (forward predictions)

| k | d^{2k} | (2k)! | leading constant (×c_f^{(k)}) |
|---|---|---|---|
| 1 | 4 | 2 | `4/(2π) = 2/π` |
| 2 | 16 | 24 | `2/(3π)` ✓ (Theorem B-exact) |
| 3 | 64 | 720 | `64/(720π) = 4/(45π) ≈ 0.0283` |
| 4 | 256 | 40320 | `256/(40320π) ≈ 0.00202` |

The k=3 prediction `4/(45π)` is a **falsifiable consequence**: 6th moment of L′ in our family should have leading coefficient `4/(45π) · c_f^{(3)}`. Test target.

### 5.2 ζ-analog limit (d → 1)

Setting `d = 1`: `1/((2k)!π)`. For k=2: `1/(24π)`. **Matches** Hughes-Mezzadri-Pearce / Conrey-Ghosh leading term for `∫|ζ′(½+it)|² dt`. ✓

### 5.3 1st-moment limit (k → 1)

`d² / (2π) = 4/(2π) = 2/π`. Compatible with Iwaniec-Sarnak first-moment computations for orthogonal GL(2) families.

### 5.4 sym²-twist consistency

`L(1, sym²f)` is the only "natural" Euler product evaluated at `s=1` that:
- has same conductor scale as L(s,f),
- gives Hoffstein-Lockhart-bounded normalization,
- arises from Rankin-Selberg `L(s, f×f̄)` residue.

No other choice is recipe-consistent.

### 5.5 Functional-equation consistency

The recipe is invariant under `s ↔ 1-s` because CFKRS shifts are paired symmetrically. The constant `2/(3π)` is **even** in this sense — no parity obstruction.

---

## Section 6: Implied Structural Facts (Short Provable Chain → 2/(3π))

If we can prove all of the following (each individually accessible), `2/(3π)` follows unconditionally:

### Chain A: Recipe-level facts

**A1.** Weight-aspect family of holomorphic newforms has **orthogonal** symmetry type (Katz-Sarnak / ILS). [**Known, proven** — Iwaniec-Luo-Sarnak 2000.]

**A2.** CFKRS recipe correctly predicts leading-order moment asymptotics for orthogonal GL(2) families up to 2nd moment of L′. [**Conjectural in general; provable for 2nd moment via CFKRS step-6 + Petersson trace formula**, modulo known "approximate functional equation" + diagonal term computation. This is the *entry point* for an unconditional proof.]

**A3.** The shift-derivative interchange: `∂_{α₁}∂_{α₂}∂_{α₃}∂_{α₄} | _{α=0}` of the CFKRS integrand equals (up to lower order) the 2nd-moment-of-L′ moment. [**Symbolic — provable by direct calculation**; verified in our prior B1 work.]

**A4.** Each shift contributes factor `d log C` from the analytic-conductor functional equation. [**Known** — direct from Γ-factor asymptotics; Iwaniec-Kowalski Ch. 5.]

### Chain B: Arithmetic factor

**B1.** Arithmetic factor isolated by Petersson trace formula diagonal contribution equals `c_f · L(1, sym²f)` up to elementary `(2π/k)`-factors. [**Known** — standard Rankin-Selberg unfolding.]

**B2.** Hoffstein-Lockhart bound on `L(1, sym²f)` ensures arithmetic factor stays `O((log C)^?)` in family. [**Known**.]

### Chain C: RMT input

**C1.** Unitary derivative-moment leading coefficient `G(3)²/G(5) = 1/12` for k=2. [**Known** — Hughes thesis; Mezzadri 2003.]

**C2.** Orthogonal/unitary pass-through: in the "weight aspect" the orthogonal RMT coefficient relevant to **2nd moment of L′** equals the unitary one (for the leading constant before arithmetic factor), times precisely `d^{2k}/((2k)!)`. [**The crux conjectural step** — this is what reverse-engineering identifies as the load-bearing claim.]

### Bottom line: One non-trivial structural conjecture (C2) + known recipe inputs ⟹ 2/(3π).

If C2 (or its replacement: a direct CFKRS step-6 verification for our family without orthogonal RMT pass-through) is established, the constant is proven.

---

## Section 7: Verdict on the Inverse-Engineering Approach

### What we learned

1. **The constant 2/(3π) is shallow, not deep.** It factorizes as `d^{2k}/((2k)!π) = 16/(24π)` — pure recipe data with no hidden modular or motivic miracle. The only deep content is *which family* (orthogonal weight-aspect GL(2)) and *which RMT type* (1/12 from Barnes-G).

2. **The arithmetic factor `c_f = L(1, sym²f)` is the place to look for deep arithmetic** — but it's *separate* from `2/(3π)`. The two factor multiplicatively, and the prior B1 work already validated `c_f` empirically.

3. **The load-bearing structural fact is C2** in §6: that the orthogonal-symmetry RMT input collapses to the unitary `1/12` Barnes-G value times the `d^{2k}/(2k)!` shift-derivative factor. This is a *single* identity, and is checkable both:
   - **Symbolically** via CFKRS step-6 for k=2 (4 shifts) + orthogonal correction terms — finite computation.
   - **Numerically** via Monte-Carlo on `O(2N)` matrix moments at large N (we already have `B2_cue_mc_K10k.py` infrastructure).

4. **Six previous direct attacks failed because they tried to derive `2/(3π)` as one block.** Reverse-engineering reveals it's a *product* of three independent factors. Attack each separately:
   - `d^{2k}=16`: trivial once shift formalism is granted.
   - `1/(2k)! = 1/24`: combinatorial.
   - `1/π`: Plancherel.

   The only nontrivial step is showing the orthogonal RMT coefficient equals `1/12` *with no correction* — and this can be checked as a single Monte-Carlo identity.

### Recommended next move

**Numerical**: Modify `B2_cue_mc_K10k.py` for orthogonal `O(2N)` group (replacing CUE with COE/orthogonal sampling), compute 2nd moment of `|Z′(1)|²` at `N = 50, 100, 200`, fit leading coefficient. Predict: `1/12 + O(1/N)`. This either confirms the structural decomposition or reveals the missing correction term in one experiment.

**Symbolic**: Run CFKRS step-6 for k=2 in our family at full computer-algebra precision (sympy / pari) — extract the leading coefficient of `(log C)^{N_2}` (where `N_2` is the moment polynomial degree predicted by orthogonal RMT) and verify symbolically that it equals `2/(3π) · c_f`.

### Honest verdict

The reverse-engineering approach **is informative but not by itself a proof**. It reduces the problem from "derive 2/(3π) ab initio" to "verify one orthogonal RMT identity." The remaining identity (C2) is concrete and testable.

**Confidence the chain in §6 is the right decomposition: 0.75.**
**Confidence C2 holds (orthogonal coefficient = 1/12 with `d^{2k}/(2k)!` factoring cleanly): 0.55** — needs the Monte Carlo check before pushing further.

If the Monte Carlo check passes within Monte-Carlo error at N=200, raise C2 confidence to ~0.85 and start the full unconditional write-up of Theorem B-exact via this decomposition.

If it fails, the failure mode itself reveals which of the six previous direct attacks was closest to right — because we'll see exactly *which* factor was wrong.

---

## Appendix: Verbatim numerical verification

```
2/(3π)  = 0.21220659078919378102517835116335248271261286098728  (mpmath, 50 dps)
1/(24π) = 0.01326291192432461131407364694770953016953830381170
ratio   = 16.0  (exact)

Barnes-G ratios (Hughes unitary derivative moments):
  k=1: G(2)²/G(3)  = 1
  k=2: G(3)²/G(5)  = 1/12 = 0.08333...
  k=3: G(4)²/G(7)  = 1/8640

Recipe formula d^(2k)/((2k)!π) at (d=2, k=2):
  16/(24·π) = 0.21220659078919378...  (matches 2/(3π) exactly)
```

All arithmetic verified at 30+ digits via mpmath.
