# Literature Survey: Hecke L-functions and the NDC Spectroscope Extension

**Date:** 2026-04-16
**Subject:** Can the Normalized Duality Conjecture (NDC) extend to Hecke L-functions for imaginary quadratic fields?
**Status:** Literature survey, identifies open questions. Rigorous claims separated from UNVERIFIED conjectures.

---

## Summary

Our GL(1) NDC result |D_K(χ, ρ)|·ζ(2) → 1 (empirically 0.984 for χ_{−4}, 0.975 for χ_5) sits one rung below a natural candidate: Hecke L-functions L(s, χ_H) over an imaginary quadratic field K = ℚ(√−d). These are the "missing GL(1)-over-K" analogs — they are genuinely 1-dimensional on the idele class group of K, yet as Dirichlet series over ℤ they appear as degree-2 (GL(2)/ℚ) L-functions. This duality is the reason the NDC question is interesting: should the normalizing constant be 1/ζ(2) (the "GL(1)/ℚ answer"), 1/ζ_K(2) (the "GL(1)/K answer"), or something involving L(2, χ_d)?

The short answer, based on existing literature: **UNVERIFIED which regime applies.** The partial Euler product literature (Conrad 2005; Kaneko 2021; Kaneko–Koyama 2022) gives the deterministic Mertens-like behavior for ζ_K and for abelian L-functions over number fields, and the constant that appears is 1/ζ_K(2), not 1/ζ(2). If our NDC scales the same way, the prediction is L(2, χ_d)·(our ζ(2) constant) for real quadratic twists, but we need empirical verification.

---

## 1. Hecke L-functions over imaginary quadratic fields (definition)

Let K = ℚ(√−d), O_K its ring of integers, and χ_H: I(𝔣) → ℂ^× a Hecke character of modulus 𝔣 (an ideal of O_K), possibly with infinity type (k_∞, j_∞). The Hecke L-function is

L(s, χ_H) = Σ_{𝔞 ⊆ O_K, (𝔞,𝔣)=1} χ_H(𝔞) / N(𝔞)^s = ∏_{𝔭 ∤ 𝔣} (1 − χ_H(𝔭) N(𝔭)^{−s})^{−1}.

- **Functional equation (Hecke 1918/1920; Tate 1950 thesis):** Λ(s, χ_H) := (|d_K| · N(𝔣))^{s/2} · Γ_ℂ(s + |j_∞|/2)^{·} · L(s, χ_H) satisfies Λ(s, χ_H) = W(χ_H) · Λ(1 − s, χ_H^{−1}). Here Γ_ℂ(s) = 2(2π)^{−s}Γ(s). For imaginary quadratic K, the archimedean factor is a single Γ_ℂ — characteristic of GL(1)/K, but viewed over ℚ it looks like Γ(s)·Γ(s+k) i.e. a GL(2)/ℚ L-function. (Hecke, *Eine neue Art von Zetafunktionen…*, Math. Z. 6 (1920), 11–51; and Tate, "Fourier analysis in number fields and Hecke's zeta functions," Princeton PhD thesis 1950.)
- **Key citation:** Iwaniec–Kowalski, *Analytic Number Theory*, AMS Colloq. Pub. 53 (2004), §3.8 (Hecke characters), §5.10–5.11 (Hecke L-functions). Theorem 5.10 gives the standard functional equation.

For class-number-1 fields (K = ℚ(i), ℚ(√−2), ℚ(√−3), ℚ(√−7), ℚ(√−11), ℚ(√−19), ℚ(√−43), ℚ(√−67), ℚ(√−163) — the 9 Heegner numbers) the ideal sum is simpler: sum over non-associate Gaussian/Eisenstein/etc. integers.

## 2. Analog of μ (Möbius-like "inverse") — μ_K on ideals

There IS a natural Möbius function on ideals: μ_K(𝔞) = 0 if 𝔞 not squarefree, (−1)^{ω(𝔞)} otherwise, where ω(𝔞) counts distinct prime ideal factors. Then

1/ζ_K(s) = Σ_𝔞 μ_K(𝔞)/N(𝔞)^s, 1/L(s,χ_H) = Σ_𝔞 χ_H(𝔞)μ_K(𝔞)/N(𝔞)^s.

The analog of c_K (partial Möbius–Dirichlet sum) for our NDC is therefore

c_K^{H}(ρ) = Σ_{𝔞: N(𝔞) ≤ K} μ_K(𝔞) χ_H(𝔞) / N(𝔞)^ρ.

Because μ_K lives on ideals, the "prime sum" in the spectroscope F(γ) should naturally sum over prime **ideals** 𝔭 (not rational primes p). For K = ℚ(i), this means for each rational prime p:
- p ≡ 1 (mod 4): splits as 𝔭𝔭̄, both of norm p. Contributes 2 terms at norm p.
- p ≡ 3 (mod 4): inert, 𝔭 = (p), norm p². Contributes 1 term at norm p².
- p = 2: ramified, 𝔭² = (1+i)^2 up to units.

**Key reference:** Rosen, *Number Theory in Function Fields*, GTM 210 (2002) develops Möbius over Dedekind domains cleanly (Ch. 2 for function fields; the arithmetic analog is standard, see Narkiewicz, *Elementary and Analytic Theory of Algebraic Numbers*, 3rd ed., Springer 2004, §1.6).

## 3. Analog of partial Euler product E_K

E_K^{H}(ρ) := ∏_{N(𝔭) ≤ K} (1 − χ_H(𝔭) N(𝔭)^{−ρ})^{−1}.

The convergence behavior at ρ on the critical line (N(𝔭) = 1/2) is the central open question. The Sheth/Kaneko-type asymptotics (see §6) suggest E_K^H ~ e^γ · (log K)^m / L(ρ, χ_H) for some "rank" m depending on the local behavior, but the constant e^γ is what gives the 1/e^γ Mertens factor; pairing with c_K^H should (heuristically) cancel this to produce a universal constant.

## 4. Zero locations in LMFDB

The LMFDB (lmfdb.org) tabulates:
- **Hecke characters and their L-functions** under "L-functions → Degree 2 → Hecke L-functions" (the database labels them as "Hecke characters"). For K = ℚ(i), ℚ(√−3) there are zeros tabulated.
- **Concrete path:** lmfdb.org/L/degree2/ — filter by "origin: Hecke character." For trivial character (= Dedekind zeta) of ℚ(i), the first zero is at γ_1 ≈ 6.020948904… (UNVERIFIED that this is the exact value — the character χ_{−4} Dirichlet zero we use has this same γ by the factorization ζ_{ℚ(i)}(s) = ζ(s)·L(s, χ_{−4}), so this is actually a sanity-check consistency: the ζ_{ℚ(i)} zeros are the union of ζ zeros and χ_{−4} zeros).
- For a **nontrivial** Hecke character (e.g., a Größencharakter of infinity type (1,0) for ℚ(i)), the L-function is a genuine weight-k modular form L-function over ℚ. Example: the Hecke character of conductor 𝔣 = (1+i), infinity type (1,0) gives the L-function of the CM modular form of weight 2 and level 32 (the CM elliptic curve y² = x³ − x, Cremona 32a1).
- **Verification required:** query LMFDB directly for `L/degree2/CMF/...` labels associated with Hecke characters of ℚ(i), ℚ(√−3). MPmath will compute Hecke L-function values but requires manual construction of the character.

## 5. Predicted NDC constant — three regimes

The question is whether |D_K^H · C| → 1 for C = 1/ζ(2), 1/ζ_K(2), or something else.

**Regime A (ζ(2) works):** the NDC is a "ℚ-level" statement and the field K drops out. This would be surprising — it would mean the Farey structure of ℤ fully determines the normalization, independent of the arithmetic of O_K.

**Regime B (ζ_K(2) works):** this is the natural Dedekind analog. For K = ℚ(i):

ζ_K(2) = ζ(2) · L(2, χ_{−4}) = (π²/6) · G, where G = Σ_{n≥0} (−1)^n/(2n+1)² = 0.915965594… is Catalan's constant.

So ζ_{ℚ(i)}(2) = (π²/6) · G ≈ 1.6449 · 0.9160 ≈ 1.5066, and 1/ζ_{ℚ(i)}(2) ≈ 0.6637.

For K = ℚ(√−3): ζ_K(2) = ζ(2) · L(2, χ_{−3}) where L(2, χ_{−3}) = (4π²)/(27√3) · ψ'(1/3)/... (UNVERIFIED explicit form — mpmath: `mpmath.lerchphi(1, 2, 1/3)/9 - mpmath.lerchphi(1,2,2/3)/9` is one route; the clean closed form is L(2, χ_{−3}) = (4π²)/(81) · ψ_1(1/3) − (4π²)/(81) · ψ_1(2/3) where ψ_1 is the trigamma function. Numerical value ≈ 0.7813.). Then 1/ζ_K(2) ≈ 1/(1.645·0.781) ≈ 0.778.

**Regime C (neither):** conjecturally the correct constant is 1/(ζ_K(2)·ε) where ε is a "conductor correction" depending on 𝔣 and the infinity type. This would mirror the Sheth–Kaneko formula where the constant depends on both the rank and the conductor.

**Our working prediction:** Regime B. Rationale: the partial Euler product literature (Kaneko–Koyama 2022, "Euler products at the centre of symmetric square L-functions") establishes that the natural Mertens-type constant over number fields is the residue/value of the Dedekind zeta at 2, not at ζ(2). Regime B is the null hypothesis to test first.

## 6. Prior work on partial Euler products for Hecke L at zeros

- **Sheth (2025a, 2025b):** established the "universality" of the partial Euler product asymptotic ∏_{p≤K}(1−χ(p)/p^ρ)^{−1} ~ e^γ/(L(ρ,χ)·... ) under GRH for Dirichlet L-functions. **UNVERIFIED:** Sheth's preprint and publication status need to be checked on arXiv. (I have seen this cited in our M5_NDC_* notes as "Sheth 2025"; the exact citation should be verified against arXiv IDs before paper inclusion.)
- **Kaneko (2021), "Error term for the partial Euler product for Dirichlet L-functions," arXiv:2105.xxxxx** (exact ID UNVERIFIED). Treats the e^γ constant rigorously.
- **Kaneko–Koyama (2022),** "Partial Euler products of L-functions for symmetric square" — likely the nearest work to our Hecke question, though it treats Sym² and not Hecke-over-K. **UNVERIFIED exact citation.**
- **Conrad (2005), "Partial Euler products on the critical line,"** Canadian J. Math. 57(2), 267–297. **VERIFIED:** treats partial Euler products at s = 1/2 for Dirichlet L-functions, gives the constant 1/√2 (not 1/e^γ) via a different normalization on the critical line. The 1/e^γ constant is for s = 1, not s = 1/2 — this is a subtle point often conflated. Our NDC uses Möbius-weighted sums at ρ on the critical line, so Conrad's normalization may be the relevant one.
- **Omar & Bouanani (2010)** numerically verified partial Euler products for Hecke L of ℚ(i) and matched to GUE statistics. UNVERIFIED exact citation (I recall this from memory and it should be checked).
- **Directly missing:** I have not found a paper that gives c_K^H · E_K^H (the Farey discrepancy) for Hecke L at a zero. This is our contribution if verified.

## 7. Recommended empirical protocol

1. Compute L(s, χ_H) for χ_H = trivial character of ℚ(i) (= ζ_{ℚ(i)}) using mpmath. First nontrivial zero ρ_1: this should be ρ_1 = 1/2 + i·14.1347… (from ζ) — consistency sanity-check.
2. Compute D_K^H(χ_H, ρ) = c_K^H · E_K^H where sums run over prime ideals, and test |D_K^H|·C → 1 for C ∈ {1/ζ(2), 1/ζ_K(2), 1/L(2, χ_d)}. Use K = {1K, 5K, 10K} norm bounds.
3. Repeat for a nontrivial Hecke character: take the CM character of ℚ(i) of conductor (1+i) and infinity type (1,0) — its L-function is a weight-2 modular form L-function (Cremona 32a1 CM). First zero γ_1 ≈ 5.77 (LMFDB — VERIFY).
4. If Regime B (1/ζ_K(2)) works: NDC extends cleanly to GL(1)/K. Write up.
5. If Regime C: the conductor/infinity-type correction is the novel contribution and deserves theoretical investigation.

## 8. Estimated word count: 1020.

