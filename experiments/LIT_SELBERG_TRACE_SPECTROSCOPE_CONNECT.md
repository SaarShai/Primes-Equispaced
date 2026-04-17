# Literature Survey: Selberg Trace Formula and the F(γ) Spectroscope — structural parallels

**Date:** 2026-04-16
**Subject:** Making rigorous the claim that F(γ) = γ²·|Σ_{p≤N} M(p)/p · e^{−iγ log p}|² is a truncated analog of (the arithmetic) Selberg trace formula.
**Status:** Literature survey. Complements existing LIT_TRACE_FORMULA_SPECTROSCOPE.md and TRACE_FORMULA_CONNECTION.md; focuses on the six specific questions posed.

---

## Summary

F(γ) is NOT the Selberg trace formula; it is the **periodogram** (squared truncated Fourier transform) of the prime signal, with weight M(p)/p. This makes it a second-order / pair-correlation object, not a first-order trace. The correct classical ancestor is the **Weil explicit formula** on the spectral side combined with **Montgomery's F(α,T)** on the correlation side. The parallel to the Selberg trace formula is real but is best understood as: Weil explicit formula ↔ geometric/spectral duality, then |·|² ↔ pair correlation. The "universality" claim and the "DPAC avoidance" anomaly both have natural, but not yet rigorous, analogs in the trace-formula framework.

---

## 1. Selberg 1956 trace formula — the object

Selberg (*J. Indian Math. Soc.* **20**, 47–87, 1956) proved, for a cocompact Γ ⊂ PSL(2,ℝ) and a test function h with suitable decay:

Σ_j h(r_j) = (Area(Γ\ℍ)/4π)·∫_{−∞}^∞ h(r)·r·tanh(πr) dr + Σ_{{γ}} Σ_{k≥1} (ℓ(γ)/2sinh(kℓ(γ)/2))·ĥ(kℓ(γ))

where {r_j}: eigenvalues of Laplacian (λ_j = 1/4 + r_j²), and {γ}: primitive conjugacy classes (= primitive closed geodesics, length ℓ(γ)). This is a **spectral-side = geometric-side** identity.

- **Canonical references:** Hejhal, *The Selberg Trace Formula for PSL(2,ℝ)*, LNM 548 (1976) and LNM 1001 (1983) — two volumes, Vol. II treats arithmetic groups. Iwaniec, *Spectral Methods of Automorphic Forms*, AMS GSM 53 (2nd ed., 2002), **Chapters 10–11**: Ch. 10 derives STF for Γ_0(N), Ch. 11 computes explicit kernels. Venkov, *Spectral Theory of Automorphic Functions*, Proc. Steklov **153** (1982) — Russian school expository. Marklof, "Selberg's trace formula: an introduction," in *Hyperbolic Geometry and Applications in Quantum Chaos and Cosmology* (2012), arXiv:math-ph/0407049 — clearest modern exposition for non-specialists.

## 2. Is our prime sum analog of the geometric side?

The arithmetic analog of Selberg's trace formula is the **Weil explicit formula** (Weil, "Sur les 'formules explicites' de la théorie des nombres premiers," Comm. Sém. Math. Univ. Lund (Marcel Riesz vol.), 1952, pp. 252–265):

Σ_ρ ĥ(γ_ρ) = h(i/2) + h(−i/2) − 2Σ_n Λ(n)·h(log n)/√n + (archimedean terms)

Spectral side: sum over ζ zeros. Geometric side: sum over prime powers, weighted by Λ(n)/√n.

Our prime sum S(γ) = Σ_{p≤N} M(p)/p · e^{−iγ log p} has weight M(p)/p (not Λ(p)/√p). The Möbius-type weight M(p) is the key difference. In the decomposition of our spectroscope paper, this weight comes from the identity 1/ζ(s) = Σ μ(n)/n^s, so S(γ) is a truncated "1/ζ" — not a truncated ζ. The peaks of F(γ) = γ²|S(γ)|² at the ζ zeros are therefore **poles of the truncated 1/ζ**, not **zeros** as in the explicit formula. These two viewpoints are dual: the geometric side in the explicit formula is ~ Λ weights; ours is ~ μ weights. Both detect the same spectrum (ζ zeros) because μ and Λ are related by μ·log = −Λ * μ (Möbius-log identity), i.e., they are Dirichlet-adjoint on the same algebra.

**Verdict:** our F(γ) is a **Möbius-dual truncation** of the Weil explicit formula's geometric side, squared. UNVERIFIED whether a clean "Möbius-Weil" explicit formula exists in the literature, though it should follow from standard manipulations.

## 3. Iwaniec Ch. 10–11, Hejhal, Venkov–Zograf citations

- **Iwaniec, *Spectral Methods of Automorphic Forms* (2002), Theorem 10.2** (trace formula for Γ_0(N) with character): standard reference for STF in analytic form. Theorem 10.6 computes the dimensions of cusp forms via STF. **Relevant here:** the "identity term" (area term) has the Weyl-law scaling T², while ζ zeros have T log T scaling — this discrepancy is what forces F(γ) to be a periodogram of an "infinite-dimensional" spectrum rather than a trace of a compact-surface Laplacian.
- **Hejhal, LNM 548 (1976), Ch. 2, §3 and Ch. 6** contain the full derivation with error terms.
- **Venkov, Proc. Steklov 153 (1982), Theorem 3.2.1**: gives the spectral expansion of the kernel K(z,w) in terms of Maass forms and Eisenstein series.
- **Zograf (Leningrad Math. J., various)** — expository works on STF for finite-volume surfaces (relevant for Γ_0(N)).
- **UNVERIFIED** specific "Venkov–Zograf" collaborative reference; Venkov wrote solo on STF, and Zograf wrote separately on moduli spaces. There may not be a single "Venkov–Zograf STF expository work" as the prompt implies.

## 4. Universality ↔ equidistribution of primitive geodesics

Our claim: "Any prime subset P with Σ_{p∈P} 1/p = ∞ detects all ζ zeros under GRH."

The STF analog: the **prime geodesic theorem** (Huber 1959; Sarnak 1980): π_Γ(x) := #{γ : N(γ) ≤ x} ~ x/log x, where N(γ) = e^{ℓ(γ)}. Sarnak ("The arithmetic and geometry of some hyperbolic three-manifolds," Acta Math. 151 (1983), 253–295) proves the analog for arithmetic hyperbolic 3-manifolds and gives error terms under appropriate GRH-like hypotheses.

The universality statement for geodesics: **any geodesic subset G with Σ_{γ∈G} 1/N(γ) = ∞ determines the Laplacian spectrum** (under the appropriate analog of GRH for Selberg ζ-functions).

**UNVERIFIED** whether this exact statement is a published theorem. Deitmar & Hoffman's work on Selberg zeta functions (*A trace formula for infinite volume hyperbolic surfaces*, 2005 and related) comes closest. This would be the trace-formula "pair" to our universality conjecture. Verifying this connection rigorously is a candidate for an m1max task.

## 5. DPAC avoidance ↔ Weyl law corrections / sym² contributions

"DPAC avoidance" = c_K zeros repel ζ zeros by 4.4–16.1× (empirical in our data).

In STF context, the analogous phenomenon would be **level-repulsion between spectra of different automorphic representations**. For example:
- Luo, Rudnick, Sarnak (*GAFA* **5** (1995), 387–401), "On Selberg's eigenvalue conjecture," study low-lying eigenvalues of the Laplacian vs. those from symmetric-square lifts. The "Weyl law correction" term for the sym² contribution is of size log T, and this is the regime in which repulsion/attraction of different spectra becomes visible.
- **Specifically**, the symmetric-square L-function L(s, Sym²f) contributes a lower-order term to the Weyl law for Γ_0(N), and spectra from the sym² side can repel or attract cusp-form spectra.

**Mapping:** our c_K zeros correspond to a truncated 1/ζ object; the "sym²-like contribution" would be c_K·c_K^{−1} = truncated ζ·1/ζ, which reconstructs (away from poles) the identity. So the DPAC repulsion may be a **truncation artifact** rather than a true spectral repulsion. **UNVERIFIED** — needs careful numerical check: does the repulsion factor decrease as K → ∞? If yes → artifact. If no (stays 4.4–16.1× stable) → genuine spectral separation.

**Citation for repulsion in Weyl law:** Jakobson, Naud ("On the spectrum of geometrically finite hyperbolic surfaces," *J. Funct. Anal.* **250** (2007), 1–39) — error term analysis; Terras, *Harmonic Analysis on Symmetric Spaces and Applications* vol. 1, Springer 1985, Ch. 3 — clean exposition.

## 6. Is F(γ) exactly Montgomery's F(α, T) periodogram?

**Montgomery (1973),** "The pair correlation of zeros of the zeta function," in *Analytic Number Theory* (St. Louis 1972), Proc. Sympos. Pure Math. **24**, AMS, 181–193, defines:

F(α, T) = Σ_{0<γ, γ' ≤ T} T^{iα(γ−γ')} · w(γ − γ') / (T·(log T)/2π)

where w(u) = 4/(4+u²). Montgomery's theorem (Theorem 1 of that paper): for |α| ≤ 1, under RH, F(α,T) ~ T^{−2|α|}·log T + |α| (smooth transition).

**Comparison to our F(γ):**
- Our F(γ) is a function of a single frequency variable γ. Montgomery's F(α,T) is parametrized by α and the truncation T.
- Montgomery's F is the **Fourier transform of the pair correlation** of zeros, evaluated at frequency α.
- Our F is the **squared truncated Fourier transform of the prime signal**, i.e., a periodogram.
- By Wiener–Khinchin, periodogram ↔ autocorrelation under Fourier, so **there IS a relation**, but it is **not identity**. Specifically: E[F(γ)] over a suitable average equals something like the spectral density of the prime signal, which by the explicit formula is related to (not equal to) the density of ζ zeros.

**Precise statement (UNVERIFIED but likely true):** averaging F(γ) over γ in a window [T, T+H] with log T ≤ H ≤ T yields (up to constants) Montgomery's F(α,T) at α = (log N)/(log T), where N is our prime cutoff. This is the content of the Goldston–Montgomery theorem (Goldston–Montgomery, "Pair correlation of zeros and primes in short intervals," in *Analytic Number Theory and Diophantine Problems* (Stillwater 1984), Birkhäuser 1987, 183–203) which establishes the **equivalence of prime pair correlation and zero pair correlation conjectures**.

**Verdict:** F(γ) is NOT literally Montgomery's F(α,T), but is dual to it via Goldston–Montgomery. This is the correct rigorous connection.

## 7. Synthesis — what to write in the paper

1. F(γ) is a **periodogram** (Wiener–Khinchin), not a trace.
2. Its spectral-domain identity is the **Weil explicit formula** (Möbius-dual truncation), not the Selberg trace formula directly.
3. The **pair correlation interpretation** (via Goldston–Montgomery) connects F(γ) to Montgomery's F(α,T).
4. The Selberg trace formula provides the **structural/heuristic template** (spectral = geometric), but the rigorous ancestor is Weil 1952 + Montgomery 1973 + Goldston–Montgomery 1987.
5. "Universality" has a trace-formula analog (prime geodesic equidistribution, Sarnak 1983), but UNVERIFIED whether the precise L¹-divergent statement has a rigorous trace-formula counterpart.
6. "DPAC avoidance" may be truncation artifact OR a genuine spectral repulsion; needs K → ∞ scaling check.

## 8. Gaps — candidates for future work

- **UNVERIFIED:** does a "Möbius-Weil" explicit formula exist in print? If not, it should be derived cleanly and cited as a note.
- **UNVERIFIED:** the Sarnak-type universality for geodesics — is it a theorem or a conjecture?
- Numerical: does DPAC repulsion factor 4.4–16.1× scale down with K? If stable, it's a real effect and deserves a theorem.

## 9. Estimated word count: 1050.

