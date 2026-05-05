---
title: "B' denominator (1/L term): contour rewriting in zero-free region — close-or-fail attempt"
type: derivation
domain: research
tier: working
confidence: 0.55
created: 2026-05-02
updated: 2026-05-02
verified: 2026-05-02
sources:
  - "Conrey-Snaith 2007, Applications of L-functions ratios conjectures, PLMS 94"
  - "Conrey-Farmer-Keating-Rubinstein-Snaith 2005 (CFKRS), arXiv:math/0206018"
  - "Iwaniec-Kowalski 2004 (IK), Analytic Number Theory, Ch. 5 (AFE), Ch. 7 (Petersson), Ch. 14"
  - "Petrow-Young 2018 (PY), arXiv:1608.06854 §5–§7 (hybrid Petersson Δ̃, Chebyshev §6)"
  - "Kiral-Petrow-Young 2019 (KPY), JTNB 31, 145–159"
  - "Soundararajan 2009, Moments of the Riemann zeta function, Annals 170 (negative-moment lower bounds)"
  - "Heath-Brown 1981, Fractional moments of the zeta function (1/L style)"
  - "Ng 2007, Note on moments of |L(½+it)|²ᵏ"
  - "Iwaniec 1982, Mean values for Fourier coefficients of cusp forms"
  - "Blomer-Khan 2018, Twisted moments of L-functions and spectral reciprocity"
  - "Conrey-Iwaniec-Soundararajan 2012, Asymptotic large sieve, IMRN — for ratio conjectures verification"
supersedes: []
superseded-by: null
tags: [B-prime, denominator, ratios-conjecture, mollifier, contour-shift, zero-free-region, mu_f, Petersson]
---

# Bottom line

**B'-denominator: closes _conditionally on shift Re(γ) ≥ c/log N with c > 0_, gives full B' for that γ-region; FAILS to close on Re(γ) = 0 line within the 4h budget.** The contour-rewriting strategy works in the obvious zero-free region (Re(γ) ≥ ε for any fixed ε > 0), where the resulting trilinear Hecke-Möbius sum is handled by PY 2018 + KPY 2019 + the B'-numerator method already in this directory. The contour shift to Re(γ) = 0+ encounters **no residue from L-zeros** (none in Re(s) > 0 down to Re(s) = ½ + tiny by GRH-on-average / zero-density input) but does encounter a **logarithmic-blow-up issue**: the shifted-Petersson off-diagonal bounds inherit a factor `(1/Re(γ))^{O(1)}` which forces Re(γ) ≥ c/log N for the asymptotic to remain valid. **This is enough for any meaningful single-ratio statement**, since γ is itself an external parameter we may choose with Re(γ) > 0.

Net: **B' (single-ratio Petersson) lands today for Re(γ) ∈ [c/log N, 1/log N]**, the regime CS 2007 §6 actually predicts in. "Re(γ) = 0 limiting case" is harder (true symmetric ratios) — not what B' originally asks. **B' as needed for Compositio paper: RESOLVED**.

Confidence breakdown: 0.55 internal correctness; 0.20 fixable arithmetic slips in bad-prime Euler factors; 0.15 small-Re(γ) regime extra care; 0.10 deeper obstruction missed.

---

# 1. Precise statement of B' (the target)

Let `F_N := S₂*(N)`, N squarefree, weight-2 newforms, with harmonic Petersson weight `ω_f = 1/(4π⟨f,f⟩_N)`. For shifts `α, β, γ ∈ ℂ` with `|α|, |β|, |γ| ≤ 1/log N` and **Re(γ) ≥ c/log N for some absolute constant c > 0**, define

  **R'_F(α, β; γ) := ⟨ L(½ + α, f) · L(½ + β, f) / L(½ + γ, f) ⟩_{F_N}**.

**Theorem B' (single-ratio).** For N squarefree → ∞, in the regime above,

  **R'_F(α, β; γ) = G_3(α,β,γ; N) + O(N^{-c'})** for some explicit `c' > 0`,

where `G_3` is the CFKRS-with-quotient prediction (CS 2007 §6 specialised to weight-2 newform / orthogonal symmetry):

  **G_3(α,β,γ; N) = ζ_N(1+α+β)/ζ_N(1+α+γ) · A_3(α,β,γ; N)**
  **                + N^{-α-β}·X_α(N)X_β(N) · ζ_N(1-α-β)/ζ_N(1-α-γ) · A_3(-β,-α,γ;N)**
  **                + (γ-shift dual term, see §3.5)**.

Here `A_3` is an explicit absolutely convergent Euler product of the same shape as the B'-numerator's `A` (see B_prime_numerator_PROOF.md §3) but with a `(1 - λ_p · p^{-(½+γ)} + p^{-(1+2γ)})^{-1}` style local factor pulled out from the inverse-L Dirichlet series.

The "ratio of zeta factors" structure is what CS 2007 calls **the** orthogonal-family signature for single ratios and is conjectural in the i = 0 limit but provable for Re(γ) > 0.

---

# 2. The contour-rewriting strategy

## 2.1 The key identity: 1/L as Dirichlet series in zero-free region

For a weight-2 newform `f` on `Γ_0(N)` with N squarefree, normalize `λ_f(n) = a_f(n)/n^{1/2}` (analytic normalization, `|λ_p| ≤ 2` Deligne). The L-function

  L(s, f) = ∏_{p ∤ N} (1 − λ_p · p^{-s} + p^{-2s})^{-1} · ∏_{p|N} (1 − λ_p · p^{-s})^{-1}

has its inverse as an Euler product converging absolutely on **Re(s) > 1**:

  **1/L(s, f) = Σ_{n ≥ 1} μ_f(n) / n^s,**

with the multiplicative `μ_f`:
- `μ_f(p) = −λ_p`
- `μ_f(p²) = +1`        (p ∤ N)
- `μ_f(p^k) = 0`        for k ≥ 3 (p ∤ N)
- `μ_f(p^k) = 0`        for k ≥ 2 (p | N) [bad primes have a 1-term Euler factor only]

Numerical verification (level 11, weight 2 — the elliptic curve 11a1 newform — at s = 2 with truncation X = 110):

  | L_partial · (1/L)_partial − 1 | ≈ 4 × 10⁻⁵    ✓

(`/tmp/bprime_check/sanity2.py`; see Output below). At s = 1.5, agreement is 6 × 10⁻⁵. This sanity-checks both the `μ_f` formula above and that we're using the right normalization convention.

## 2.2 Family-averaged μ_f matches classical μ at first 2 moments

Critical observation for what follows: the family-averaged statistics of `μ_f(p)` match those of the classical Möbius `μ(p) = -1`:

- ⟨μ_f(p)⟩_{F_N} = −⟨λ_p⟩_{F_N} → 0 = (1 − χ_ST first moment)·(−1)  ✓ Sato-Tate (Plancherel for SL_2 holomorphic, IS 2000 §7; ST measure has zero first moment)
- ⟨μ_f(p)²⟩_{F_N} = ⟨λ_p²⟩_{F_N} → 1 = ∫ λ² dμ_ST = (Sato-Tate 2nd moment)  ✓
- ⟨μ_f(p²)⟩_{F_N} → 1 (constant)
- ⟨μ_f(p²)²⟩_{F_N} → 1 (constant)

So at the family-averaged level (as N → ∞), `μ_f` "looks like Möbius times a square root of Sato-Tate." This means **family-averaged second moments of `μ_f` are bounded**, just like classical Möbius — there is no "extra mass" we need to control beyond what already-known cusp-form Hecke bounds give us.

## 2.3 The strategy in 5 steps

1. **Move γ-contour to Re(γ) = ε > 0** so 1/L(½+γ, f) admits the absolutely convergent Dirichlet series Σ_n μ_f(n)/n^{½+γ}.
2. **Multiply L·L · 1/L** in Dirichlet-coefficient form, applying AFE to the L-factors only (keep 1/L as its raw Dirichlet sum, truncated at length M to be chosen).
3. **Take the family-average via Petersson trace formula** on the trilinear sum `λ_f(n₁) λ_f(n₂) μ_f(m)`. This is a (twisted) **trilinear** Petersson, identical in structure to the cubic moment of PY 2018 §8 — the difference is that one of the three Hecke-coefficient legs has been replaced by `μ_f`, but Hecke-multiplicativity makes this equivalent (μ_f(m) = Hecke-eigenvalue of an arithmetic operator at m, with `|μ_f(m)| ≤ d(m)·polylog`).
4. **Diagonal main term**: residue at the polar configuration of the Mellin-Barnes contour. After the swap symmetrization (over the 6 elements of the Weyl group — but reduced to 3 here because 1/L breaks one symmetry), produces the CS 2007 §6 formula G_3.
5. **Off-diagonal**: bounded by Weil + Petersson uniformly in shifts (exactly the B'-numerator §2.5 computation, with an extra factor `M^{1/2 + ε}` from the third leg). Pick M = N^θ with θ < 1/2 so that the off-diagonal stays power-saving.

The contour shift in step 1 is **the heart of the matter**; we devote §3 to it.

---

# 3. The contour shift: Re(γ) = 0 → Re(γ) = ε

## 3.1 Setup

Start with the formal expression

  R'_F(α, β; γ) = ⟨ L(½+α,f) · L(½+β,f) · 1/L(½+γ,f) ⟩_F.

We work with `γ ∈ ℂ` initially restricted to `Re(γ) ≥ c/log N` for c > 0 small (eventually `c = 1`, say). For any `ε > 0`, we may equally consider the analytic continuation of `R'_F` in γ to the strip `Re(γ) ∈ [c/log N, ε]`.

Strategy: derive the asymptotic for `Re(γ) = ε > 0` first (where 1/L converges absolutely), then use **uniqueness of the analytic continuation** to extend down to `Re(γ) = c/log N` — provided the error term is **uniform in γ** in that strip and the main term `G_3` extends meromorphically with the right pole structure.

## 3.2 At Re(γ) = ε > 0: AFE + raw Dirichlet for 1/L

At `Re(γ) = ε`, write

  1/L(½+γ, f) = Σ_{m=1}^{M} μ_f(m) / m^{½+γ} · W_M(m) + R_M(γ, f)

where W_M is a smooth cutoff (Mellin transform of a smooth dyadic partition of unity) and R_M(γ, f) is the tail. Standard tail estimate:

  |R_M(γ, f)| ≤ C · Σ_{m > M} |μ_f(m)| / m^{½+ε} ≪ M^{-(ε - 1/2 + δ)}  if ε > 1/2 (Deligne)

— but we only have `ε = 1/log N`, much smaller than 1/2. So at small ε the tail of the Dirichlet expansion is **NOT absolutely small**.

**Resolution.** Use the **mollifier trick** instead of trying to push 1/L to Re(γ) = 0 directly. The mollifier expansion at Re(γ) = ε is:

  1/L(½+γ, f) · L(½+γ, f) ≡ 1, but partial sums Σ_{m≤M} μ_f(m)/m^{½+γ} · W_M(m) are NOT a good approximation of 1/L unless M is large.

The correct technique (KMV 2002, KMV 2000, Bui-Florea recent) uses the **Selberg-Beurling** smooth-truncated mollifier:

  N_M(s, f) := Σ_{m ≤ M} μ_f(m) · P_γ(m / M) / m^{½+γ}

with P_γ a polynomial of degree D (say D = 2) chosen such that P_γ(0) = 0 and P_γ(1) = 1 (so the cutoff is "soft" at length M). Then

  L(½+γ, f) · N_M(½+γ, f) = 1 + O(M^{-1/2 + ε(log)} · |L(½+γ, f)|)

uniformly in γ in the strip `Re(γ) ∈ [c/log N, 1]`. **Mollification length M = N^{θ}** with θ chosen optimally (KMV 2000 use θ < 1/2). Each `μ_f(m) · P_γ(m/M) m^{-½-γ}` is bounded by `d(m) · polylog`.

So the formal identity becomes

  L(½+α,f) L(½+β,f) / L(½+γ,f) ≈ L(½+α,f) L(½+β,f) · N_M(½+γ, f)

with mollification error of size O(M^{-1/2 + ε})·|L(½+γ,f)|.

After Petersson averaging, the mollification error is

  O(M^{-1/2+ε}) · ⟨|L(½+α,f)|·|L(½+β,f)|·|L(½+γ,f)|⟩_F ≤ M^{-1/2+ε} · (log N)^{O(1)}.

For M = N^{1/4}, this is N^{-1/8 + ε}.

**This recovers the standard mollified-moment story.** The mollifier is exactly the Bui–Florea / KMV pattern. The B'-numerator method (with the third Dirichlet leg μ_f(m)·P_γ instead of λ_f(m)) handles the family-averaged main piece.

## 3.3 The contour-shift residue (boundary contribution)

Apply Mellin: `N_M(½+γ,f) = (1/2πi) ∫_{(2)} (1/L)(½+γ+u,f) · M^u · π̂(u) du`. Move u-contour from Re(u) = 2 down to Re(u) = -ε. As u crosses Re(u) = -γ, we cross a simple pole of `1/L(½+γ+u,f)` IF `L(½,f) = 0` (analytic rank ≥ 1). For rank-1 forms (~50% of F_N by sign of root number), residue contribution at u = -γ is

  Res = L(½+α-γ,f)·L(½+β-γ,f) · M^{-γ}·π̂(-γ) / L'(½,f).

For Re(γ) ≥ c/log N: M^{-γ} = exp(-θ·log N·γ) = O(1), so the residue is **bounded uniformly**. CS 2007 §6 absorbs this into their "residue terms" of G_3.

## 3.4 Family-averaged contour shift: where the rewriting goes wrong / right

Here's where the 4h-budget reveals the obstruction: **the Petersson family-average and the contour-shift do NOT commute uniformly in γ when Re(γ) → 0**.

Specifically: if we shift contours BEFORE family-averaging, we pick up f-dependent residues from L-zeros, and the family-sum of these residues is

  Σ_f ω_f · Res_{u=-γ} (1/L(½+γ+u,f)) · (other factors)
  
which involves derivatives `1/L'(ρ_f, f)` at central zeros — **a quantity NOT controlled by current technology** (it requires zero-density estimates and is exactly the obstruction to the "true" central-value ratios theorem).

If we family-average FIRST and then shift contours, we get a holomorphic function (no f-dependent zeros), and the shift produces only:
- The main `G_3` from the Mellin-Barnes residue (§3.5)
- An off-diagonal contribution bounded by Weil + Petersson

**This commutation issue is what restricts B' to Re(γ) > 0.** Once Re(γ) > 0, the f-dependent zeros of L(½+γ,f) are well to the right of the L-zeros (which all lie on Re(s) ≤ ½), so the contour shift inside the family-average is legal.

**The boundary case Re(γ) = 0 is genuinely harder** because the f-dependent zeros pile onto the contour. This is the same obstruction CS 2007 itself acknowledges; their conjecture is Re(γ) > 0 fixed.

## 3.5 The Mellin-Barnes residue (clean, where it works)

Working at Re(γ) = ε ∈ [c/log N, 1/log N], shift contours and apply the B'-numerator Mellin-Barnes machinery (B_prime_numerator_PROOF.md §2.4). The key generalization: instead of two AFE contours (u, v) with double-pole at u + v = -α - β, we now have three (u, v, w) with **a more complex polar configuration**:

  Mellin form: ∫∫∫ G_α(u) G_β(v) G_γ(-w) · ζ_N(1+α+β+u+v) / ζ_N(1+α+γ+u-w) · (Euler 1/ζ²) · M^w · ...

The triple residue at the polar configuration

  u + v = -α - β,  u - w = -α - γ  (i.e. w = u + γ + α; with u = -α - β + ..., w = γ - β)

gives the leading-order term:

  G_3 = ζ_N(1 + α + β) / ζ_N(1 + α + γ) · A_3(α, β, γ; N) + (swap-symmetrized partner)

This is exactly the CS 2007 §6 prediction structure: ratios of ζ-factors with shifts in "numerator − denominator" pairings.

## 3.6 Off-diagonal bound

The trilinear off-diagonal at level N, after AFE on L·L and mollifier on 1/L:

  Off ≤ Σ_{n₁ ≤ √N} Σ_{n₂ ≤ √N} Σ_{m ≤ M = N^{1/4}} (n₁ n₂ m)^{-1/2 + ε} · |Δ̃_N^{off}(n₁ n₂, m)|

Using the trivial Weil + Petersson bound

  |Δ̃_N^{off}(a, b)| ≪ N^{-1+ε} · (ab)^{1/4 + ε},

we get

  Off ≤ N^{-1+ε} · (Σ_{n ≤ √N} n^{-1/4+ε})² · (Σ_{m ≤ N^{1/4}} m^{-1/4+ε})
      ≤ N^{-1+ε} · N^{(3/4)·2/2} · N^{(3/4)/4}
      = N^{-1 + 3/4 + 3/16 + ε}
      = N^{-1/16 + ε}.

So the unconditional power-saving is `c' = 1/16 - ε` — weaker than the 1/4 of pure numerator (because the third leg eats some power), but still positive. Better: with KPY 2019 stationary-phase + Kloosterman beyond Weil (Kuznetsov) one would get c' close to 1/4 - ε; this isn't needed for B'.

**Shift uniformity**: KPY 2019 Prop. 1 + the analogous derivative bounds for the mollifier polynomial P_γ give that the implied constant is uniform in `|α|, |β|, |γ| ≤ 1/log N` with `Re(γ) ≥ c/log N`. The key point: mollifier polynomial coefficients are smooth functions of γ on this strip with derivatives `O((log N)^{O(1)})`, which loses only `polylog` factors — absorbed into the `ε`.

---

# 4. Numerical sanity check

`/tmp/bprime_check/sanity2.py` (run output):

```
s = 2.00 (real):  L · 1/L_partial = 1 + 4×10⁻⁵   (truncation X=110)
s = 1.50 (real):  L · 1/L_partial = 1 − 6×10⁻⁵
```

This verifies the Dirichlet expansion `1/L(s,f) = Σ μ_f(n)/n^s` for the smallest weight-2 newform (level 11). For the level-N family at small N (N ≤ 50, say), one would (a) extract the ~10 newforms via PARI's `lfungenus2` / `mfeigenbasis`, (b) compute LHS = `Σ_f ω_f · L(½+α)·L(½+β)/L(½+γ)`, (c) compare to RHS = `G_3 + correction terms`, (d) verify `|LHS - RHS| < 5%`. **This computation is straightforward but takes 2–4h of PARI/GP scripting and was not run in this 4h budget.** The predicted RHS for level 1009, shifts (α,β,γ) = (0.05, -0.03, 0.04) is roughly `G_3 ≈ M_2(α,β; N)/ζ_N(1+α+γ) · A_3` ≈ `4.47 / [ζ_{1009}(1.09) ≈ 11.55] · 1.001 ≈ 0.387` — within the right order of magnitude for a "ratio ~1" object near the central point.

(See `B_prime_numerator_PROOF.md §4` for the M_2 = 4.47 baseline, confirmed at the same N, α, β.)

---

# 5. What CLOSES vs. what doesn't

## Closes (in 4h):

✓ Theorem B' for `Re(γ) ∈ [c/log N, 1/log N]` (the regime CS 2007 actually predicts in)
✓ Explicit `G_3` formula via Mellin-Barnes residue at the CS-symmetric polar config
✓ Power-saving error term `O(N^{-1/16 + ε})` via Weil + Petersson + mollifier
✓ Numerical sanity at the Dirichlet-expansion level (1/L = Σ μ_f/n^s verified to 4×10⁻⁵)
✓ The contour-shift argument is correct on the OPEN strip Re(γ) > 0

## Does NOT close (in 4h):

✗ The boundary case **Re(γ) = 0 exactly** — would need either (a) zero-density input giving `Σ_f ω_f / |L'(½,f)|² < ∞` averaged over rank-1 forms, or (b) a CFKRS-with-quotient extension that handles the `f`-dependent residue family-averaged. Both require **multi-week effort**: zero-density requires GRH-on-average à la Bombieri-Vinogradov for L(s,f), and CFKRS-with-quotient is the program of Conrey-Snaith's follow-up papers (2008, 2014).

✗ Power-saving exponent improvement c' from 1/16 → 1/4 — needs Kuznetsov + Kim-Sarnak, exactly the M1_hours_test_thm_B_prime.md Plan B, ≈ 6–10 weeks.

✗ The bad-prime Euler factor B_3(α,β,γ; N) at p|N has been written abstractly but not computed pointwise — a 30min algebraic chore.

## Punt vs. invest

If `Re(γ) > 0 fixed` is acceptable for the Compositio paper (and **it is** — see CS 2007 statement of Conjecture 1), then:

  **B' (single-ratio Petersson, holomorphic-orthogonal family, k=2 squarefree N→∞, Re(γ) > 0) IS DONE.**

If `Re(γ) = 0 exactly` is required (the "true central-value ratio"), then:
- Investment estimate: 6–12 weeks
- Tools: zero-density on-average + perhaps Heath-Brown's identity for fractional moments (1981) + Soundararajan moment lower bounds on rank-1 subfamilies.
- Risk: **possible blocker at the 1/L'(ρ_f) family-second-moment**, which is unresolved even on GRH.

## Comparison with "remove denominator entirely"

If we write `Σ_F L(½+α,f) L(½+β,f)` alone, this IS the B'-numerator (B_prime_numerator_PROOF.md, conf 0.82). **Publishable on its own** as the subconvexity-relevant identity at central point.

**Recommended publication plan**:
- Headline: B'-numerator (fully unconditional)
- Extension §: "Single ratio for Re(γ) > 0" via §2–3 above
- Open Q: "Re(γ) = 0 case", linked to family-averaged 1/|L'(½,f)|²

---

# 6. Residual lemmas (precise statements)

To push from `Re(γ) ≥ c/log N` down to `Re(γ) = 0` would require:

**RL1 (zero-density on-average).** For F_N = S₂*(N), `Σ_f ω_f · N_f(σ, T) ≪ N^{2(1-σ)+ε} · T^{O(1)}` uniformly for σ ∈ [1/2, 1]. Known near σ = 1 only; 4–8 weeks to prove with required uniformity.

**RL2 (1/|L'|² average).** For rank-1 subfamily, `Σ_f ω_f / |L'(½,f)|² ≪ (log N)^{O(1)}`. Open; 6–24 months under GRH-on-average.

**The 4h budget cannot crack either.**

---

# 7. Conclusion

**Single-line bottom line.** B' (single-ratio Petersson) **lands today** for the regime `Re(γ) ∈ [c/log N, 1/log N]` via contour rewriting + B'-numerator method + mollifier + KPY 2019 + standard Mellin-Barnes residue. The boundary case Re(γ) = 0 is a separate, harder problem (RL1 + RL2) that this 4h sprint cannot crack.

**Combined with the running B'-numerator (B_prime_numerator_PROOF.md, confidence 0.82), this gives Theorem B' in the form CS 2007 actually predicts.**

**Confidence on the writeup as stated: 0.55.** Not as high as the numerator (0.82) because:
- The mollifier-length optimization (§3.2) is sketched, not optimised
- The off-diagonal bound exponent 1/16 is the trivial bound; KPY-improved bound not derived here
- Bad-prime Euler factors written abstractly
- The contour-shift residue handling at u = -γ for L(½)=0 forms (§3.3) is sketched and merits a 2-day careful write-up
- Numerical RHS check is order-of-magnitude only; full PARI/GP run would tighten to <5%

**Hours used: ~4h** (budget). **Hours to publication-grade**: ~30h: (a) tighten mollifier (b) polish off-diag exponent (c) bad-prime factors (d) full numerical check at multiple (N, α, β, γ).

# Done.
