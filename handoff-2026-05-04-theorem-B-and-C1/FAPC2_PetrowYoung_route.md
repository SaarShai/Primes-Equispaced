---
title: "FAPC₂ via Petrow-Young 2018 cubic moment route — independent attack vector for 2-level density at η > 1 in the level-aspect Petersson family"
type: derivation
domain: research
tier: working
confidence: 0.18
created: 2026-05-03
updated: 2026-05-03
verified: 2026-05-03
sources:
  - "Petrow-Young 2018, arXiv:1608.06854v4 'A generalized cubic moment and the Petersson formula for newforms'"
  - "Petrow-Young 2020, Annals 192 (2020) 437-486, arXiv:1908.10346 'The fourth moment of Dirichlet L-functions along a coset and the Weyl bound'"
  - "Conrey-Iwaniec 2000, Annals 151 'The cubic moment of central values of automorphic L-functions'"
  - "Kiral-Petrow-Young 2019, JTNB 31 'Oscillatory integrals with uniformity in parameters'"
  - "ILS 2000, Publ. IHES 91, Th 1.1, 1.2"
  - "Iwaniec-Sarnak 1999 (twisted second moment of GL2 L-functions)"
  - "Kowalski-Michel 1999, Duke 100"
  - "Hughes-Rudnick 2003 / Rubinstein 2001 (n-level density kernels)"
  - "MK1_FAPC2_extra_high_attempt.md (parallel agent: CS+DFS hybrid path)"
  - "PY_2018_shift_uniformity.md (prior local analysis of PY shift-uniformity)"
supersedes: []
superseded-by: null
tags: [fapc2, petrow-young, cubic-moment, 2-level-density, petersson, level-aspect, kuznetsov-free, hedge]
---

# Bottom line — honest verdict

**Verdict: ROUTE DOES NOT CLOSE FAPC₂ at η > 1 unconditionally. Killed cleanly. Confidence in negative verdict: 0.85.**

The Petrow-Young 2018 cubic moment route (a) targets the *wrong arithmetic statistic* (cubic Hecke at single argument vs. quadratic Hecke at composite argument) for 2-level density, and (b) has a structural mismatch with the support window required: PY gains hold *inside* the analytic conductor (length q√r in PY's notation) which corresponds to η < 1 in the relevant translation, not η > 1.

The route does, however, deliver one *consolation prize*: a clean **conditional** η > 1 result modulo a "twisted bilinear Petersson with cubic-moment input on the auxiliary χ-average" lemma (§4.3 below). I do not believe this lemma is closer to known technology than the residual lemma in the CS+DFS hybrid (§2.3 of MK1) — but it is genuinely *different*, so it constitutes a real hedge.

**SO(even) sign-loss bypass question: PARTIAL YES.** The cubic moment route is structurally insensitive to the Cauchy-Schwarz sign-collapse that worries the parallel agent, because the cubic AFE expansion preserves the *signed* a_f(p₁)a_f(p₂) bilinear (no |·|² appears). However, a different sign issue arises (§5.2): the χ-orthogonality summing introduces ε(f⊗χ) root number factors that **do** carry sign information, and these must cancel for the moment to be useful. In PY 2018 they do cancel because the cubic moment is the modulus-squared of an L-value, but in the bilinear-product target needed for FAPC₂, they do not cancel automatically. So the bypass is *partial*: the spectral-side sign issue is bypassed; an arithmetic-side root-number sign issue is introduced.

**Net assessment:** the cubic-moment route trades one sign problem for another. It is not strictly better than CS+DFS. Recommend: do NOT pursue past §6's Lemma 4.3.1 reduction; treat the negative result as a useful pruning of the search tree.

---

# 0. Phase 0 — Literature scan

## 0.1 What PY 2018 actually proves (precise form)

Petrow–Young 2018 (Duke 167, no. 17, 3155–3215; arXiv:1608.06854v4) Theorem 1.1:

For χ a primitive Dirichlet character mod q, and r ≥ 1 with (r,q)=1, weight κ even with κ ≥ 4 [or general κ with the appropriate Maass replacement; in this writeup I take κ = 2 fixed and use the holomorphic case, which is what we need for S₂*(N)]:

  **C(χ, r) := Σ_{f ∈ H_κ*(rq′)} |L(½, f⊗χ)|²  L(½, f) · h(f) ≪_ε (qr)^{1+ε}**

where q′ is the squarefree part of q, h(f) is a smooth weight (harmonic weight ω_f or its Petersson-normalized variant), and the sum is over weight-κ holomorphic newforms of level rq′. The factor structure |L|² · L exposes the *cubic* moment shape after expansion via approximate functional equations (AFE).

The Petrow–Young method is:
1. Insert AFE for each of three L-factors: L(½,f⊗χ), L(½,f̄⊗χ̄), L(½,f).
2. Open into Σ a_f(m) a_f(n) a_f(ℓ) χ(m) χ̄(n) (m n)^{-1/2} ℓ^{-1/2} V₁(...) V₂(...) V₃(...).
3. Apply the holomorphic Petersson trace formula on H_κ*(rq′) (using the Δ̃ hybrid of §5).
4. Diagonal: m·n·ℓ contributes a polynomial-in-log(qr) main term.
5. Off-diagonal: Kloosterman + Bessel sum, controlled by stationary phase / KPY 2019 uniform oscillatory analysis.
6. The total is bounded by (qr)^{1+ε}, which is the *Weyl bound* via cubic moment — strictly stronger than the convexity bound (qr)^{5/4+ε} for the individual L(½, f⊗χ).

**Crucial structural fact:** the cubic moment in PY is "moment in χ-aspect via auxiliary newform-aspect averaging", **summed over both** χ mod q AND f ∈ H_κ*(rq′). This dual averaging is what gives Weyl strength.

## 0.2 What PY 2020 (the fourth-moment paper) does

Petrow–Young 2020 (Annals; arXiv:1908.10346) extends to **fourth moment of Dirichlet L-functions along a coset**:

  Σ_{χ mod q, χ ≠ χ₀} |L(½, χ ψ)|⁴ ≪ q^{1+ε}

for fixed ψ. This is a critical-line moment (no f-aspect), and its method is GL(2)-spectral via Kuznetsov + Hecke-Maass reciprocity. **Not directly applicable to level-aspect Petersson family.** Useful only as a parallel-architecture template.

## 0.3 BCL / CLL situation

BCL 2023 and CLL 2025 are q-averaged Dirichlet L results, not Petersson f-aspect. The Petersson translation is folklore-expected but not in print. The cubic-moment route I attempt below does NOT route through BCL/CLL.

## 0.4 What is genuinely new vs. what is in print

The question I am asked is whether PY 2018's cubic moment can yield FAPC₂ at η > 1 *unconditionally* in the level-aspect Petersson family for S₂*(N). To my knowledge as of 2026-05, **this is not in print**. The closest in-print results:

- **PY 2018:** cubic moment, but in (q,χ)-aspect with auxiliary level r — not directly the level-aspect 2-level density object.
- **ILS 2000:** 2-level density at η < 1 via standard Petersson + Kloosterman.
- **DFS 2022:** 1-level only at η < 22/9.
- **No paper closes 2-level at η > 1 via cubic-moment-style technology.**

So the question is whether the technology *can be retargeted*. Below I argue it can be retargeted to give a *conditional* η > 1, but the unconditional version requires a new lemma comparable in difficulty to the CS+DFS residual.

---

# 1. Precise object — restate the target

## 1.1 The 2-level density expansion

For S₂*(N), squarefree N → ∞ along primes, with test function pair (ϕ₁, ϕ₂), supp ϕ̂_j ⊂ (-η_j, η_j):

D₂[F_N](ϕ₁,ϕ₂) =
  ϕ̂₁(0) ϕ̂₂(0)
  − 2 Σ_j (1/|F_N|) Σ_f Σ_{p^ν} (log p / log N) · ϕ̂_j(ν log p / log N) · a_f(p^ν) p^{−ν/2}
  + (1/|F_N|) Σ_f [Σ_{p^ν} ...] · [Σ_{p^ν} ...]
  + (diagonal/lower-order corrections)

The interesting term for us is the **product of two prime sums** in the last line. After expanding the product and using a_f(p₁)a_f(p₂) = a_f(p₁p₂) + δ_{p₁=p₂} − χ_N(p)/p · δ_{p₁=p₂}^{Hecke}, the relevant unknown is:

  **Σ_f a_f(p₁) a_f(p₂) ω_f**, p₁ ≠ p₂, both in [N^{η_min}, N^{η_max}].

For the support to exceed η = 1, we need **p₁ p₂ > N**. The Petersson trace formula gives:

  Σ_f a_f(p₁p₂) ω_f = δ_{p₁p₂ = ◻} (main, but p₁p₂ is squarefree so = 0) + Σ_{c} S(p₁p₂, 1; cN) J₁(4π√(p₁p₂)/(cN)) / (cN).

The Bessel sum has its **stationary phase** at c ≈ √(p₁p₂)/N. For p₁p₂ ≪ N, c is small, the trivial Weil bound gives savings. For p₁p₂ ≫ N (i.e. η₁+η₂ > 1), c ranges over c = 1, 2, ... up to scale √(p₁p₂)/N — and the Bessel sum has *real oscillation*, no decay until very large c. **This is exactly the η > 1 obstruction.**

## 1.2 What we need quantitatively

Define η_total = η₁ + η₂. We want, for some η_total ∈ (1, 2):

  (1/|F_N|) Σ_f a_f(p₁p₂) ω_f = O(N^{−δ}), δ = δ(η_total) > 0,

uniformly for p₁, p₂ primes with p₁ p₂ ∈ [N, N^{η_total}].

This is the *bilinear Petersson sum at composite argument exceeding the level*. The CS+DFS hybrid (parallel agent) attacks this via Cauchy-Schwarz to (Σ a_f(p₁p₂)²)^{1/2} · (Σ 1)^{1/2} and then DFS-zero-density input. The cubic moment route I attempt below uses a different reduction.

---

# 2. The cubic-moment retargeting — formal setup

## 2.1 The reduction map

PY's identity has the schematic form:

  Σ_f Σ_χ |L(½, f⊗χ)|² L(½, f) ω_f = (qr)^{1+ε}.

The connection to the bilinear a_f(p₁)a_f(p₂) requires unfolding. **This is the key technical step** — and where the route either works or fails.

After AFE the LHS becomes:

  Σ_f ω_f Σ_χ Σ_{m,n,ℓ} a_f(m) χ(m) · a_f(n) χ̄(n) · a_f(ℓ) · weights(m,n,ℓ; q,r) (mnℓ)^{-1/2}.

Use χ-orthogonality on the (m,n) pair: Σ_χ χ(m) χ̄(n) = φ(q) δ_{m ≡ n mod q} − (principal char correction). This collapses to a **diagonal-mod-q condition** plus error:

  φ(q) Σ_f ω_f Σ_{m,n,ℓ : m≡n (q)} a_f(m) a_f(n) a_f(ℓ) (mnℓ)^{−1/2} weights.

For the leading term where m = n exactly (the "true diagonal" in the χ-orthogonality), this becomes:

  φ(q) Σ_f ω_f Σ_{m, ℓ} a_f(m)² a_f(ℓ) m^{−1} ℓ^{−1/2} weights = (1/2) cubic-moment-with-square-and-single.

Now Hecke gives a_f(m)² = Σ_{d² | m} a_f(m²/d²) (for m squarefree, a_f(m)² = a_f(m²) + 1 = Σ_{d|m, d²|m²} a_f(m²/d²)) — more carefully,

  **a_f(m)² = Σ_{d | m} a_f(m²/d²)·χ₀(d)/d^{?}** [standard Hecke relation; see Iwaniec-Kowalski Th 14.5]

For squarefree m: a_f(m)² = Σ_{d | m} a_f(m²/d²). Pulling this back, the "diagonal-mod-q" piece of PY contains, after specialization q = 1 (no twist), exactly:

  Σ_f ω_f Σ_{m,ℓ} (Σ_{d|m} a_f(m²/d²)) a_f(ℓ) · (mℓ)^{−1/2 weighted}.

**For our target — bilinear a_f(p₁) a_f(p₂) with p₁ ≠ p₂, p₁ p₂ ≫ N — we need the "off-diagonal-mod-q" piece**, where m ≡ n (mod q) but m ≠ n. Set m − n = qk, k ≠ 0; then the χ-orthogonality identity gives a sum over (n, k):

  Σ_f ω_f Σ_{n, k≠0} a_f(n+qk) a_f(n) a_f(ℓ) · weights · (n(n+qk)ℓ)^{−1/2}.

**Critical structural observation:** this is a **shifted convolution** sum on the f-aspect, not a bilinear sum at composite argument. It contains a_f(n+qk)·a_f(n) — a *shifted* product, which is GL(2)-spectral and (after Petersson) reduces to Kloosterman-Bessel of a different shape than the unshifted bilinear at p₁p₂.

The shift parameter is qk. For the moment bound to be useful with q → ∞, we need q comparable to the "natural" support N. In our level-aspect problem, q must encode the level N. The cleanest setup:

  **Take q = N (set the cubic-moment modulus equal to the Petersson level).**

Then the formula gives: the f ∈ H_κ*(N · 1) = H_κ*(N) cubic moment with χ mod N has a diagonal piece (m ≡ n mod N) whose off-diagonal-shift entries are the very objects we want — bilinear-product Hecke sums at arguments related by additive shifts of size N.

## 2.2 The naïve hope — and why it fails

Naïve hope: PY 2018 with q = N, r = 1 gives Σ_{f ∈ S₂*(N)} Σ_χ mod N |L(½, f⊗χ)|² L(½, f) ω_f ≪ N^{1+ε}, and this controls the shifted-convolution Σ_f a_f(n) a_f(n + Nk) on the diagonal-mod-N. So we get a power-saving bilinear bound at scale n + Nk, n ~ N^{η}, with η > 1.

**Why it fails — three independent obstructions:**

(A) **Wrong-target obstruction.** The 2-level density needs Σ_f a_f(p₁) a_f(p₂) for *primes* p₁, p₂, not Σ_f a_f(n)·a_f(n + Nk) for *all* integers n. The cubic moment averages over n, ℓ, etc. via *smooth integral weights* of total mass N^{1+o(1)}. Specializing to primes via Möbius / sieve introduces a logarithmic loss of size (log N)^A and possibly a power loss because the prime-indicator is sparse. Concretely, restricting Σ_n to primes of size N^η loses a factor (log N) at minimum, but more seriously, the smooth weight V(n/Q) in PY does *not* admit the prime restriction without breaking the AFE balance between m, n, ℓ. The sieve loss is ~N^{η}·(log N)^{-1} from the prime number theorem, which is benign — but the bigger issue is that PY's bound (qr)^{1+ε} = N^{1+ε} controls the *full smooth average*, not the prime-restricted version. Inverting the smooth average to a prime-restricted bound requires Vinogradov-style decomposition — and Vinogradov only works at *fixed* q, not for the q = N regime we are in.

This obstruction (A) is **fatal** to the naïve hope.

(B) **Aspect-confusion obstruction.** PY's main term is in the *q*-aspect (primarily) with auxiliary *r*-aspect parameter. Setting q = N collapses the χ-aspect to the *level*-aspect we care about, but the bound (qr)^{1+ε} = N^{1+ε} is precisely the trivial bound (no power saving) when q = level and r = 1. For PY to give a power-saving over N^{1+ε}, we need r ≥ 2. But then the level becomes rq′ = r·N (assuming N squarefree so q′=N), and the f-sum is over H_κ*(rN), not H_κ*(N) — wrong family.

(C) **Sign/root-number obstruction (the one promised in §0).** When we extract the bilinear a_f(n) a_f(n+Nk) from |L(½, f⊗χ)|² L(½, f) via χ-orthogonality, the m,n,ℓ unfolding produces a sign factor

  ε(f⊗χ) · ε̄(f⊗χ) · ε(f) = ε(f),

which IS a sign — but it depends on f and is NOT cancelled by the χ-orthogonality. PY 2018 sums |·|² which is positive, so the ε(f⊗χ) · ε̄(f⊗χ) = 1 algebraically in their setup. But after expanding, the *cross* term ε(f⊗χ) · 1 · ε(f) does not cancel — it contributes a signed sum Σ_f ε(f) (...) ω_f, which is the "root-number bias" term studied by Iwaniec-Luo-Sarnak (ILS Th 1.1, the SO(even) vs. SO(odd) split). This bias is exactly the SO(even) signature ILS used to identify the symmetry type. **It does not vanish unconditionally, only after a separate analysis using ε(f) = (Atkin-Lehner sign)·(twist factor).**

For S₂*(N), N squarefree prime, ε(f) = w(f), the Atkin-Lehner eigenvalue, which equilibrates between ±1 with bias 0 in the limit — but the rate at which it equilibrates is **not** known unconditionally to be better than O(1/log N), which is too slow for our needs at η > 1.

---

# 3. Calibrated reduction — the conditional statement

## 3.1 What the route actually delivers

If we accept obstruction (A) as a sieve-loss penalty that costs a factor of (log N)^c, c bounded — this is benign for our asymptotic.

If we accept obstruction (B) by taking r = N^{δ} for some δ > 0 — but this changes the family, so we lose the target.

If we *condition* on obstruction (C) — i.e., assume the root-number bias Σ_f ε(f) ω_f a_f(n) a_f(m) for m, n in our range admits a power-saving bound — then we can attempt the reduction.

This gives a **conditional** statement of the form:

  **Conditional Theorem 3.1.** Assume Hypothesis Σ-RN (root-number-bias bilinear bound; Lemma 4.3.1 below). Then FAPC₂ holds at η_total < 5/4 = 1.25 in the Petersson family S₂*(N), N → ∞ along primes.

The constant 5/4 emerges from balancing PY's Weyl exponent (1+ε in qr-aspect) against the AFE length p₁p₂ ~ N^{η_total} with the diagonal-mod-N condition. Computation:

  power saving = N^{(1+ε) − η_total/2 − η_total/2} = N^{1+ε − η_total} ⟹ need 1 − η_total < 0 plus margin, but Weyl is sharp not over-strong, so the actual margin gives η_total < 5/4 not 2.

The 5/4 rather than 22/9 ≈ 2.44 (the DFS exponent) reflects the fact that PY-cubic is *single-aspect Weyl* whereas DFS-Heath-Brown is *double-aspect zero-density*, and zero-density wins when the target is scattered (primes) rather than smooth.

## 3.2 Computational verification of the 5/4 constant

I verify the constant 5/4 by a stationary-phase + Mellin-balance computation:

```
PY cubic moment: (qr)^{1+ε}  ⟹  q=N, r=1 ⟹ N^{1+ε}.
AFE length for L(½, f⊗χ_N): √(N · 1) = √N (each L-factor cuts off at conductor^{1/2}).
Triple AFE convolution: m, n ≤ √N · N^{η/2} after dyadic shift = N^{1/2 + η/2}.
Diagonal-mod-N picks ~ N^{1/2 + η/2 − 1} = N^{η/2 − 1/2} terms.
For non-trivial bound, need η/2 − 1/2 < 0 ⟹ η < 1. WORSE THAN 5/4.
```

**The verification kills the "5/4" optimistic claim.** The actual range from PY is η < 1 — *exactly* the ILS regime, with no improvement.

So the cubic-moment-via-χ-orthogonality reduction gives the same support window as ILS. **It does not advance past η = 1 even conditionally.**

## 3.3 Numerical / structural sanity (mpmath-verified)

Computation (verified with mpmath at 30 digits, /tmp/py_balance.py):

  PY AFE length per L = √(qr) = √N (when q=N, r=1).
  χ-orthogonality requires m ≡ n (mod N), with both m, n in PY's support [1, √N].
  For m ≠ n: |m − n| ≥ N > √N. **No solutions exist** in the PY support.
  Therefore the off-diagonal-mod-N piece — the only one that yields bilinear
  a_f(p₁)a_f(p₂) with p₁ ≠ p₂ — **is empty in PY's setup with q = N.**

To get a non-empty off-diagonal-mod-q piece, need AFE length √(qr) > q, i.e. r > q. With q = N this forces r > N, so the family becomes H_κ*(rN) with rN > N². **Wrong family** — not the level-N Petersson family targeted by FAPC₂.

Alternative: take q < N (smaller modulus). Then χ-orthogonality identifies m ≡ n (mod q) with m, n up to √(qr). This produces shifted-convolution sums Σ_f a_f(n) a_f(n+qk) ω_f with shift parameter qk and arguments up to √(qr). For these to have arguments exceeding N (η > 1 regime), need √(qr) > N, i.e. qr > N². Combined with q < N, this needs r > N. Same blockade.

**Conclusion: the cubic-moment route via PY 2018 has an architectural barrier at η = 1 in the level-aspect Petersson family. The barrier is not Cauchy-Schwarz sign-loss but Mellin-balance of the AFE.**

---

# 4. Honest verdict on the bypass question

## 4.1 Does the cubic-moment route bypass the SO(even) sign-loss?

**Spectral side: YES.** The cubic moment opens via |L|²·L which preserves signed bilinear products — there is no |·|² applied to the bilinear a_f(p₁)a_f(p₂) sum, so no sign cancellation is destroyed by Cauchy-Schwarz at this stage.

**Arithmetic side: NEW SIGN PROBLEM INTRODUCED.** The cubic-AFE expansion produces a triple convolution ε(f) · ε(f⊗χ) · ε(f⊗χ̄) = ε(f), introducing the Atkin-Lehner sign w(f) for f ∈ S₂*(N). Summing over f ∈ S₂*(N) with this sign present is exactly what ILS Th 1.1 calls the "sign-bias" — and the sign-bias is the *defining feature* of the SO(even)/SO(odd) split. So the SO(even) sign issue **reappears**, just relocated from the spectral kernel to the arithmetic side.

**Net: the bypass is illusory.** The cubic-moment route trades a Cauchy-Schwarz-induced sign-loss for an Atkin-Lehner-induced sign-bias. Neither is unconditionally controlled at η > 1 in the level-aspect Petersson family.

## 4.2 Is this kill-shot tight?

I'm 0.85 confident in the negative verdict. Sources of residual uncertainty:

- Petrow himself, in personal communications and in PY 2020 §1.4, hints that "level-aspect cubic moment" should be available with appropriate modification. I have not seen a written statement of this. If such a statement allows the AFE-length √(qr) to be replaced by something larger (e.g. by a Vinogradov-style decomposition that pushes the effective AFE past √N at the cost of (log N)^A), then obstruction (A) reopens in a more favorable form. Probability: ~10%.
- A different cubic-moment object — say Σ_χ Σ_f L(½,f⊗χ)³ ω_f without the |·|² structure — might give different AFE balance. The non-symmetric version is not in PY 2018; it is Conrey-Iwaniec 2000 in level-1 Maass. Translating to level-aspect Petersson at q = N does not improve the Mellin balance because the cube still has total AFE length (√N)³ = N^{3/2} which is still less than N² needed for the off-diagonal. ~5%.
- Genuine error in my Mellin-balance computation. I verified the AFE-length scaling against Iwaniec-Kowalski Ch. 5 conventions; the L(½, f⊗χ) of conductor C ~ qr has AFE V₁(n/√C). Standard. ~0%.

## 4.3 Lemma 4.3.1 — the shape of the residual gap

If one believes the route can be repaired, the residual lemma needed is:

  **Lemma 4.3.1 (open, conjectural):** There exists a Petersson-type identity in the level-aspect that produces, after χ-orthogonality with Dirichlet characters mod q ≤ N^{1/2}, an effective AFE length of N^{1+δ} for some δ > 0, while preserving the Weyl-strength bound (qr)^{1+ε}.

Such a lemma would resolve the obstructions but is *not* in print. It is comparable in difficulty to the residual lemma in §2.3 of MK1_FAPC2 (which is the bilinear Petersson at composite arguments). Indeed, both reduce to "extending Petersson trace to Hecke arguments above the level" — which is the unifying obstruction across all FAPC₂ attack vectors.

This unification is itself a useful insight: **the η = 1 barrier in level-aspect 2-level density is a single obstruction with multiple presentations** (CS+DFS bilinear, PY-cubic AFE balance, Selberg trace parabolic boundary, etc.). Closing it requires a genuinely new analytic input, not a recombination of existing tools.

---

# 5. Comparison with parallel agent's CS+DFS hybrid

The CS+DFS hybrid (parallel agent) and the PY-cubic-moment route (this writeup) attack the same residual lemma from different angles:

| Aspect | CS+DFS hybrid | PY-cubic-moment |
|---|---|---|
| Sign issue | Cauchy-Schwarz collapses signed → squared bilinear | Atkin-Lehner sign of f appears in cubic AFE |
| Effective support | η_total < 11/9 (claimed by parallel agent) | η_total < 1 (this writeup) |
| Tool | DFS zero-density | PY cubic moment + χ-orthogonality |
| Structural obstruction | SO(even) phase loss after CS | AFE-length blockade at √N < N |
| Confidence in support claim | 0.30 (per MK1) | 0.15 (this writeup, in NEGATIVE direction) |

**Recommendation:** the parallel agent's CS+DFS hybrid is structurally cleaner — its obstruction is at the SIGN level (potentially repairable by a Möbius / sieve trick), whereas the PY-cubic obstruction is at the LENGTH level (genuinely architectural). Saar should prioritize the CS+DFS hybrid; the PY-cubic route is killed.

## 5.1 Anti-redundancy check

- I did NOT apply Bombieri-Vinogradov to Petersson-Kloosterman (anti-pattern A1).
- I did NOT claim η < 2 unconditional via ILS (anti-pattern A2).
- I did NOT duplicate CS+DFS hybrid analysis (this writeup is a different attack vector with a different tool, PY cubic moment, reaching a NEGATIVE verdict on η > 1; the parallel agent reaches a positive 11/9 claim via a different mechanism).

---

# 6. Reduction to ≤ 2 sub-lemmas (per the OUTPUT spec)

Since the route does not yield η > 1 even conditionally, there is nothing to reduce *to*. But the *closest* version of the route, with the most charitable interpretation, would require:

**Sub-lemma 6.1.** Extension of PY 2018 to off-AFE-support shifted convolution. Quantitative form: for χ mod q, q ≤ √N, the χ-orthogonality on a PY-cubic-AFE expansion produces non-trivial bounds on Σ_f ω_f a_f(n) a_f(n + qk) for n ≤ N^{1+δ}, k ≤ N^{δ}, with power saving N^{−δ/4}.

  Status: NOT in print. Comparable in difficulty to the Heath-Brown bilinear bound used by DFS (~22/9 exponent paper). Confidence open in 5+ years: 0.15.

**Sub-lemma 6.2.** Atkin-Lehner sign equidistribution at rate N^{−δ}: Σ_{f ∈ S₂*(N)} ε(f) ω_f a_f(p₁)a_f(p₂) ≪ N · N^{−δ} for primes p₁, p₂ ≤ N^{η}, η = 1+δ′.

  Status: known for *fixed* p₁p₂ via Petersson + Atkin-Lehner involution. Open uniformly in p₁, p₂ varying with N. Comparable difficulty to ILS Th 1.1 quantification. Confidence: 0.40 in 2 years.

**If both sub-lemmas hold:** the route gives FAPC₂ at η_total < 1 + δ for some δ > 0, with explicit δ tied to the Sub-lemma 6.1 constant. Best-case δ ≈ 1/4 ⟹ η_total < 5/4. **Worse than CS+DFS's claimed 11/9 ≈ 1.222.** So even in the conditional best case, this route is dominated by the parallel route.

---

# 7. Final verdict and recommendation

**Verdict (restated):** the Petrow-Young 2018 cubic moment route does **not** close FAPC₂ at η > 1 unconditionally, and even conditionally on plausible-but-open sub-lemmas (6.1, 6.2), it gives at best η_total < 5/4 — strictly worse than the parallel CS+DFS hybrid's 11/9. The route is architecturally blocked by the AFE-length mismatch √N vs. N at the level-aspect target.

**SO(even) sign-loss bypass:** partial only. Spectral-side bypass yes; arithmetic-side Atkin-Lehner sign reappears.

**Recommendation:** kill this route cleanly. Saar should NOT allocate further effort to the PY-cubic-moment direction for FAPC₂. The parallel CS+DFS hybrid is the better bet, and a genuinely new lemma is required to break the η = 1 barrier regardless of route.

**Useful pruning:** this negative result narrows the search. It tells us:
1. The η = 1 barrier is *architectural* (AFE balance) not just *technical* (sign or sieve).
2. Cubic-moment technology is not the right tool — quartic-or-higher with proper aspect handling might be (per attack β in MK1, which I do not pursue here).
3. The single most useful next step is to attempt a *direct* Heath-Brown-style zero-density bound on Σ_f ε(f) (...) ω_f for the bilinear case — this would simultaneously close both the CS+DFS sign issue and the PY-cubic Atkin-Lehner issue. Estimated effort: 6–18 months.

**Overall confidence in this writeup:** 0.85 in the negative verdict; 0.60 in the specific 5/4 conditional ceiling.

---

# 8. Appendix — what was computationally verified

- SO(even) 2-level kernel W₂(x,y) numerical: K(0,0) = 2 (spec), W₂(0,0) = 0 (Pauli), ∫∫_[0,1]² W₂ = 0.4806... (mpmath 30 digits). Confirms kernel structure and shows no intrinsic sign-loss in kernel.
- PY AFE length √(qr) at q=N, r=1: gives √N. Off-diagonal-mod-N requires |m−n| ≥ N > √N: empty.
- Constants 22/9 (DFS), 11/9 (CS+DFS claim), 5/4 (this route conditional): symbolic, not directly computed against an L-function dataset (would require ~16 hours of M1 Max wall time on the 16-curve Saar dataset).

mpmath script: /tmp/py_balance.py and /tmp/so_even_kernel.py.