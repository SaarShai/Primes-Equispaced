---
type: derivation
domain: research
tier: working
confidence: 0.78
created: 2026-05-02
updated: 2026-05-02
verified: 2026-05-02
sources:
  - arXiv:1608.06854v4 (Petrow-Young 2018)
  - arXiv:math/9810182 (Conrey-Iwaniec 2000)
  - JTNB 31 (2019) 145-159 (Kiral-Petrow-Young, oscillatory uniformity)
  - arXiv:2006.05984 (Petrow-Young 2020 weight aspect)
  - Blomer-Milicevic, GAFA 2015 (second moment twisted)
tags: [B-prime, cubic-moment, shift-uniformity, petersson-trace, G1]
supersedes: []
superseded-by: null
---

# PY 2018 §5–6 shift-uniformity assessment for Theorem B′

## Verdict (TL;DR)

**G1 NOT resolved by PY 2018 as written.** The premise of the request — that PY §5–6 contain a "trilinear spectral large sieve" whose shift-uniformity could be inspected — is **architecturally incorrect**. PY 2018 has no Kuznetsov / Maass / Kim–Sarnak chain. §5 is "Hybrid formulas" interpolating Δ_N and Δ\*_N (holomorphic Petersson Δ); §6 is Chebyshev-coefficient combinatorics for newform projection. The cubic structure comes from cubing L(1/2, f⊗χ_q) inside an AFE and applying the **Petersson trace formula on H_κ\*(rq′)** — not from a spectral large sieve.

However, the answer to the underlying question — *can the proof be lifted to shifts ε ~ 1/log N?* — is **yes, with bounded extra work**. PY explicitly flag this in §8.4:

> "It would be better to study the main terms in the style of [CFKRS] using shifts, which for the sake of brevity we leave for another occasion." (line 1786)

The deferred step is **only** for the main term. The off-diagonal/error-term machinery (§8.5–§11) is already shift-tolerant up to the precision we need for B′.

## What §5–6 actually contain

§5 ("Hybrid formulas"). Defines a hybrid Δ̃_{A,B}(m,n) (eq. 5.1) interpolating between Δ\*_{AB} (newform-only Petersson) and Δ_{AB} (full Hecke-basis Petersson). The output (eq. 5.3) is a Möbius/Hecke-relation identity expressing Δ̃_{N,q}(m,n) as a multiplicative-function-weighted sum of standard Δ_{Mq}'s evaluated at shifted divisor-arguments md₁/(a²e₁²(u,v)), nd₂/(b²e₂²(u,v)).

§6 ("Chebyshev coefficients"). Bounds on c_{j,n} (= matrix elements of Hecke operators in the Chebyshev/Sato–Tate basis), Lemmas 6.1–6.3 and Cor. 6.4. Pure combinatorics; no L-function shift parameters appear.

**Neither section is a spectral large sieve.** No Kuznetsov, no Maass spectrum, no Kim–Sarnak input. The relevant tool is the holomorphic Petersson trace formula via Δ̃, which gives the diagonal δ(m=n) plus a Kloosterman/Bessel off-diagonal (eq. 8.25):

  S_{N₁N₂N₃,C} = Σ_{c≡0 (mod q̃R)} w_C(c) Σ_{n_i} χ_q(n₁n₂n₃) S(An₁n₂, Bn₃; c) · J_{κ−1}(4π√(ABn₁n₂n₃)/c) · w_{N₁N₂N₃}(n_i).

This is a Kloosterman + Bessel sum, not a spectral large sieve. The "trilinear" form is present but **at the arithmetic level** (three n_i's, three λ_f after cubing AFE).

## How shifts would enter, and where uniformity matters

The B′ object you want is

  ⟨ L(½+α, f) L(½+β, f) / L(½+γ, f) ⟩_F.

The denominator is the dangerous part — that's a separate issue from PY's machinery (PY only cubes; never divides). Set that aside and consider the **numerator-only triple-shifted moment** Σ_f ω_f L(½+α,f⊗χ_q) L(½+β,f⊗χ_q) L(½+γ,f⊗χ_q) at shifts |α|,|β|,|γ| ≤ 1/log N. The map from PY 2018 is:

| Step | PY at s=½ | What changes at shifts ≤ ε=1/log N |
|---|---|---|
| AFE for L(½+α,f) | V₁(n/√(qr¹/²)) cutoff at length ~q√r | V₁(n/√(qr¹/²); α): now an α-dependent inverse Mellin of γ-factor ratio. Bounded smooth, but *cutoff length shifts by exp(O(α log·)) = 1+O(ε log·)* |
| Square of AFE → divisor | τ(m) appears | τ_{α,β}(m) = Σ_{ab=m} a^{−α}b^{−β}; uniform on |α|,|β|≤ε since (·)^{±ε} factor is 1+O(ε log m) on dyadic ranges m ≪ qr |
| Petersson Δ̃ (§5) | mn unrestricted | **completely shift-blind**: Δ̃ depends only on (m,n,N,q), no L-function shift parameter |
| §6 Chebyshev bounds | independent of s | **completely shift-blind** |
| Off-diagonal Kloosterman + Bessel (§8.5, §10–11) | J_{κ−1}(x) | Mellin-Barnes weight functions W_i(u_i) acquire Γ-shifts; J_{κ−1} unchanged. Stationary-phase / oscillatory-integral analysis in §10 (KPY) is **already proven uniformly in auxiliary parameters** [Kiral-Petrow-Young 2019, JTNB] — this is exactly the uniformity result built for this purpose |
| Diagonal main term M₀ (§8.4) | residue at u₁=u₂=0, double pole | **THE ONE GAP**: PY say "would be better in style of [CFKRS] using shifts, leave for another occasion" |

So PY's machinery decomposes into:

1. **§5 hybrid Petersson Δ̃** — shift-independent, no work needed.
2. **§6 Chebyshev** — shift-independent, no work needed.
3. **§7 Approximate Petersson** — shift-independent.
4. **§8.5–§11 off-diagonal** — shift-tolerant. The KPY 2019 paper "Oscillatory Integrals with Uniformity in Parameters" was written precisely to make the stationary-phase steps uniform in auxiliary parameters. Their Proposition 10.x machinery already accepts a parameter family.
5. **§8.4 diagonal main term** — **the one place PY explicitly defer the shifted version**. They get a polynomial in log(q²r) of degree ≤ 3 in the s=½ case via residues of W₁(u₁)W₂(u₂)ζ²(1+u₁+u₂)ζ(1+2u₂)F(u₁,u₂) at u₁=u₂=0. With shifts α,β,γ the residue computation moves to u₁=−α−β, u₂=−γ (or similar configuration), and the polynomial-in-log gets replaced by a **CFKRS-type rational function** in α,β,γ with poles at α+β=0, β+γ=0, etc. CFKRS (Conrey-Farmer-Keating-Rubinstein-Snaith 2005) handles exactly this; the technology is standard.

## The honest verdict

**Hours-of-work estimate to upgrade PY to shifts |α|,|β|,|γ| ≤ 1/log N, *numerator only*: ~20–40 hours.** Concretely:

(a) Re-run §8.2 AFE with three shifts. Standard. (~4 h)
(b) §8.3–§8.4 main-term residue calculation in CFKRS style. The polar configuration is well-known: F(u₁,u₂,u₃) Mellin transform has zeta factors ζ(1+u_i+u_j+α_i+α_j+...) and one shifts contours to extract the residues at the canonical CFKRS-symmetric points. PY did the unshifted special case; CFKRS+Bui–Florea-style writeups give the recipe. (~16 h) — this is the "ONE step" PY explicitly deferred.
(c) §8.5–§11 off-diagonal: trace through and verify each weight function W₁,W₂ inherits an O((qr)^{O(ε)}) factor uniformly in shifts. KPY 2019 oscillatory-uniformity gives this for free. (~8 h)
(d) Numerical sanity check on small N. (~4 h)

**This handles the numerator triple-product. It does NOT handle the L(½+γ,·) in the denominator** — that is a separate, much harder problem (no moment method gives 1/L; it requires either zero-density input or a CFKRS-with-quotient extension à la Conrey-Snaith, which has its own analytic continuation issues). G1 in B′ as stated has TWO sub-problems; PY-shift-uniformity addresses only one.

## Cross-check with related literature

- **Conrey-Iwaniec 2000 (Annals)**: original cubic moment, level 1 + Maass case, central value **only**. No shifts.
- **Petrow-Young 2020 (Inventiones; arXiv:2006.05984)**: weight-aspect cubic moment. Subconvexity at central point, **no shifts**.
- **Blomer-Milićević 2015 (GAFA)**: SECOND moment, twisted, allows some shift uniformity but is the wrong moment (second, not third) and wrong family (twists by Dirichlet χ mod q, not newforms in the level aspect).
- **Soundararajan moment bounds**: upper bounds for arbitrary moments via GRH-conditional log-moment inequalities; **not the asymptotic** needed for B′ closure with constants.
- **Kiral-Petrow-Young 2019 (JTNB)**: the uniform stationary phase tool. Existence of this tool is exactly what makes step (c) above easy rather than 100h hard.

**No published paper gives a uniform-in-shift cubic large sieve / cubic moment in the B′-required form.** The closest is "PY 2018 + KPY 2019 oscillatory uniformity + CFKRS main-term recipe", which is a 20–40h synthesis, not a citation.

## Recommendation

1. **Do not** claim the shift-uniformity falls out of PY 2018 §5–6. It does not — those sections are not the right sections, and the shifted main-term computation is explicitly deferred.
2. **Do** claim that lifting PY 2018 to numerator-shifts of size 1/log N is a tractable 20–40h task using standard CFKRS technology + KPY 2019 uniformity. State it as a derived lemma in the B′ writeup, not as a citation.
3. **Separately address** the L(½+γ,·) in the denominator. That is the real obstruction in B′, not the numerator shifts. If the denominator can be removed (e.g. via a positivity argument à la Iwaniec-Sarnak, or by rewriting the ratio as a contour integral over zero-free region), B′ closes via (1)+(2). Otherwise this is the bottleneck, not PY-shift-uniformity.

## One-line bottom line

PY 2018 §5–6 do not contain the alleged spectral large sieve; the actual machinery is holomorphic Petersson + KPY 2019 oscillatory uniformity, and the only genuinely-deferred step (CFKRS-style main term with shifts) is ~16 hours of standard residue computation. **G1 numerator: hours, not weeks. G1 denominator: separate problem, not in PY's scope.**
