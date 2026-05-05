# Analysis: arXiv:2601.06292 (Durkan–Hughes–Pearce-Crump, 2026)

**Verdict up front: NOT TRANSFERABLE to GL(2) Petersson family Theorem B-exact. The "unconditional" character is a standard zero-free-region argument applied to a contour integral whose poles are residues at s=1, NOT a GRH bypass for the underlying L-function. This route does not give unconditional Theorem B-exact.**

---

## Section 1: Verbatim main theorem and method overview

**Title (verbatim):** "THE DISCRETE SECOND MOMENT OF MIXED DERIVATIVES OF THE RIEMANN ZETA FUNCTION"

**Authors:** Benjamin Durkan, Christopher Hughes, Andrew Pearce-Crump.

**Object studied** (1.1, verbatim):
> I(µ, ν) := I(µ, ν; T) = Σ_{0<γ≤T} ζ^(µ)(ρ) ζ^(ν)(1−ρ)

**Theorem 1 (verbatim, p.2-3, lines 188-397):**
> "For positive integers µ, ν, we have
> Σ_{0<γ≤T} ζ^(µ)(ρ) ζ^(ν)(1−ρ) = (T/2π) P_{µ,ν}(log T/2π) + O(T e^{−C√log T})
> as T → ∞, where C is a positive constant and where P_{µ,ν}(x) is the polynomial of degree µ + ν + 2 given by [explicit formula in terms of Laurent coefficients of (ζ'/ζ)(s)·ζ^(µ)(s)·ζ^(k)(s)/s and ζ^(ν)(s)·ζ^(k)(s)/s around s=1]…
> If one assumes the Riemann Hypothesis, the error term may be replaced with O(T^{1/2+ε}) for arbitrary ε > 0."

**Method (Section 3, "Brief outline of the proof", verbatim):**
> "For c = 1 + 1/log T and R the rectangular contour with vertices c+i, c+iT, 1−c+iT, and 1−c+i, we may use Cauchy's theorem to write
> I(µ, ν) = (1/2πi) ∮_R (ζ'/ζ)(s) ζ^(µ)(s) ζ^(ν)(1−s) ds = I_1 + I_2 + I_3 + I_4."

The integrand has poles **at the zeros ρ of ζ** (from ζ'/ζ) inside R; residues give ζ^(µ)(ρ)ζ^(ν)(1−ρ). Then they evaluate the four contour pieces via functional equation + Perron + zero-free region.

---

## Section 2: Tools used (with verbatim PDF quotes)

**Tool 1: Functional equation for ζ^(ν)(1−s)** (Lemma 1, lines 542-565, citing Hughes–Pearce-Crump [13, Lemma 4]):
> "ζ^(ν)(1−s) = (−1)^ν χ(1−s) Σ_{k=0}^ν (ν choose k) (log t/2π)^{ν−k} ζ^(k)(s) + O(t^{σ−3/2}(log t)^ν)"

This is the **classical Riemann functional equation** for ζ.

**Tool 2: Classical zero-free region (Titchmarsh)** — this is the crux of the "unconditional" claim (lines 1062-1064, verbatim):
> "As noted in Titchmarsh [22, p.54], there exists some absolute constant C > 0 such that for c' = 1 − C/log V, any zero of ζ(s) lies a distance ≫ 1/log V away from the line between c' − iV and c' + iV."

Then the unconditional choice V = exp(√(C log Y)) gives error Y·exp(−C̃√log Y) (Vinogradov–Korobov-style optimization, lines 1172-1178 verbatim):
> "In the unconditional case, we can choose V = exp(√(C log Y)) to optimise the error terms. This then gives an error term of R_1(Y,V) + E_1(V,Y) ≪ Y·e^{−√(C log Y)} (log Y)^{(µ+k+5)/2} ≪ Y·exp(−C̃√log Y)"

**Tool 3: Convexity bounds and Cauchy's estimate** for ζ^(µ) (line 1077-1081):
> "ζ^(µ)(σ ± iV) ≪ V^{(1/2)(1−σ)} (log V)^{µ+1} if 0 ≤ σ ≤ 1; (log V)^{µ+1} if σ ≥ 1"

**Tool 4: Gonek [9, §2] bound** ζ'/ζ(σ ± iV) ≪ (log V)^2 between zeros (line 1067-1068).

**Tool 5: Perron's formula** for the Dirichlet series sum after functional-equation rewrite.

---

## Section 3: Transferability assessment to GL(2) Petersson family

### 3a. What "unconditional" means here vs. what we need

**Critical observation:** This paper's "unconditional" theorem is NOT a GRH bypass for ζ in any sense relevant to Farey/Theorem B. It evaluates a **single object** Σ_{γ≤T} ζ^(µ)(ρ)ζ^(ν)(1−ρ). The unconditional error e^{−C√log T} comes from the **classical Vinogradov–Korobov zero-free region of ζ**.

The architecture:
1. The sum equals a contour integral by **Cauchy's theorem**, where ρ are the poles of ζ'/ζ inside the contour. **All ζ-zeros up to height T are automatically captured by the contour, regardless of whether they lie on Re(s)=1/2 or not.** No GRH assumed.
2. The contour is then evaluated as a residue at s=1 (ordinary pole of ζ) plus three line integrals.
3. The line-integral error uses the **classical zero-free region** of ζ near σ=1, which has been known unconditionally since Vinogradov–Korobov.

**The paper does NOT bypass GRH for any moment of ζ that previously required GRH.** GRH improves the error from e^{−C√log T} to T^{−1/2+ε}; the leading asymptotic was already known unconditionally only as the leading term (Gonek 1984), and getting the **full polynomial** unconditionally is the new contribution. But this works only because:

- The contour integral identity (residues = sum over zeros) is **identity-level**, not requiring zero-location info;
- The leading-term polynomial comes from the residue at s=1, which is **independent of zero locations**;
- The error term needs only a classical zero-free region near σ=1.

### 3b. ζ-specific structure used

**Two ζ-specific ingredients:**
1. **Riemann functional equation** ζ(s) = χ(s)ζ(1−s) — the functional-equation rewrite (Lemma 1) is the engine that converts ζ^(ν)(1−s) on the left contour into a Dirichlet series on the right.
2. **Classical zero-free region for ζ** (Vinogradov–Korobov) used for the unconditional contour shift to c' = 1 − C/log V.

The functional equation has a direct GL(2) analog (Hecke). **However**, the second ingredient is the obstruction (see 3c).

### 3c. What changes for GL(2) Petersson family

For Farey/Theorem B-exact we need (per prior failed-routes documentation):

**Goal:** Σ_{f ∈ B_k(N)} ω_f^h |L'(1/2, f)|^2 with full polynomial expansion in log k, **unconditionally**, with power-saving error.

The natural Durkan–Hughes–Pearce-Crump (DHP-C) analog would be:
$$ J(µ, ν; f) := \sum_{0<γ≤T} L^{(µ)}(ρ_f, f) L^{(ν)}(1−ρ_f, f), $$
**summed over zeros of L(s,f)**. This is NOT what Theorem B-exact requires. Theorem B-exact is a **family second moment of L'(1/2, f)** averaged over f at the central point, not over zeros of an individual L(s,f).

**Even granting the analogy** (treat the family-average as "the analog of summing over zeros"), the technique requires:

1. **Functional equation:** OK, GL(2) has Hecke functional equation.
2. **Classical Vinogradov–Korobov-style zero-free region for L(s,f):** **AVAILABLE** for individual GL(2) L-functions (Iwaniec, Kim–Sarnak, etc. give zero-free regions of the form σ > 1 − c/log(k(1+|t|))).
3. **Residue at s=1 of (L'/L)·L^(µ)·L^(ν):** L(s,f) has **NO POLE at s=1** for cuspidal f. The residue picks up the structure differently.
4. **Crucially: the analog of the discrete sum.** The DHP-C technique gives Σ over **zeros of one L-function**. For a GL(2) family second moment at the central point, we would instead have a **family sum**, requiring Petersson trace formula or similar.

### 3d. The structural mismatch

The DHP-C theorem is, in spirit, an evaluation of **one Dirichlet polynomial sum** via contour integration (an "explicit formula" calculation in disguise). The unconditionality is automatic once one has:
- a functional equation,
- a classical zero-free region near σ=1,
- a residue calculation at s=1.

A GL(2) Petersson **family** L'-second-moment requires, in addition:
- **The Petersson/Kuznetsov trace formula** to convert the family sum to off-diagonal Kloosterman sums.
- Control of the off-diagonal contribution, which in the standard treatment (ILS, KMV) needs **moment estimates** of the form 4-th moment / 4-level density / large-sieve-type input.

The DHP-C contour technique does **nothing** about the Petersson/Kuznetsov off-diagonal — it's orthogonal to the family-aspect difficulty that scuttled the prior 5 routes.

---

## Section 4: GL(2) Petersson family derivation attempt

Per the assessment in §3, this would require a transfer that does not work. Let me document precisely what fails.

**Proposed analog**, mimicking DHP-C:
$$ I_f(µ,ν) := \sum_{0<γ_f≤T} L^{(µ)}(ρ_f, f)\, L^{(ν)}(1−ρ_f, f) $$
for a fixed cusp form f. By Cauchy:
$$ I_f(µ,ν) = \frac{1}{2\pi i} \oint_R \frac{L'}{L}(s,f)\, L^{(µ)}(s,f)\, L^{(ν)}(1−s,f)\, ds. $$

This goes through (the techniques are standard; see Hughes–Pearce-Crump and Conrey–Snaith analogs for L-functions in Selberg class), and one obtains an asymptotic of the form
$$ I_f(µ,ν) = \frac{T}{2\pi} P_{µ,ν,f}\!\left(\log \frac{T}{2\pi}\right) + O\!\left(T e^{−C\sqrt{\log T}}\right) $$
**for fixed f**, with implicit constants depending polynomially on k(f), N(f), since L(s,f) has a Vinogradov–Korobov-type zero-free region.

**This is not Theorem B-exact.** Theorem B-exact requires
$$ \sum_{f \in B_k(N)} \omega_f^h \,|L'(1/2,f)|^2 = \text{polynomial}(\log k) + \text{error}, $$
which is a **single point** (s=1/2, the central value) summed over f, not a sum over zeros of a single f.

**No discrete-zero-sum identity gives this directly.** The path Sonnet's lit research suggested would only work if one of:
- (a) DHP-C's per-f result could be averaged over the family with adequate uniformity, AND the zero-sum I_f(µ,ν) at fixed T were related to L'(1/2,f) — neither of which holds. A discrete sum over **zeros of f** is unrelated to the **central value** L'(1/2,f).
- (b) DHP-C's contour technique were applied to a **family-averaged Dirichlet series** rather than a single L. This would be a new construction, NOT what DHP-C did.

**Both (a) and (b) fail. (a) is structurally wrong (different objects). (b) requires Petersson/Kuznetsov machinery and recovers the same off-diagonal-control problem that killed the 5 prior routes.**

---

## Section 5: Precise obstruction

The DHP-C technique is a **single-L, sum-over-zeros, contour-residue** technique. Theorem B-exact is a **family-averaged, central-value, second-moment** problem.

The obstruction is structural and three-fold:
1. **Wrong object:** sum over zeros of f ≠ central value at s=1/2.
2. **No family aspect:** DHP-C operates on a single L; it does not exchange the difficulty for a family-aspect difficulty.
3. **Family-aspect bottleneck unchanged:** any attempt to bring DHP-C into a Petersson family setting reintroduces Kuznetsov off-diagonal terms / 4-level density / 4th-moment input, which is exactly what blocked the 5 prior routes (per `GRH_bypass_FAMILY_aspect.md`).

The "unconditional" in DHP-C is a Vinogradov–Korobov error-term improvement on a **leading-asymptotic** problem whose **leading asymptotic was already unconditional at leading order** (Gonek 1984). It is not a moment-bypass at all; it is a polynomial-expansion result for a known leading-order-unconditional moment.

**Sonnet's lit-research summary appears to have misread the abstract.** The abstract says "unconditional and conditional error terms" — meaning the leading polynomial is given unconditionally, with two grades of error. This is the standard meaning, not a GRH-bypass for a previously-GRH-only result.

---

## Section 6: Honest verdict on Theorem B-exact unconditional via this route

**Verdict: ROUTE DEAD.** This paper does not provide an unconditional path to Theorem B-exact. The methodology:

- Does NOT bypass GRH for any moment that previously required GRH.
- Uses ζ-functional-equation + classical zero-free region — both have GL(2) analogs, but applying them gives the per-f sum-over-zeros analog, which is **not** Theorem B-exact's family-averaged central-value second moment.
- Does NOT touch the family-aspect bottleneck (Petersson/Kuznetsov off-diagonal control / 4-level density), which is the actual blocker for unconditional Theorem B-exact.

**Scenario classification (per task brief):** Closest to **Scenario A** (technique uses ζ-specific tools — but more accurately, it uses *single-L-function* tools that have GL(2) analogs but solve a *different problem*). The technique is generalizable to single GL(2) L-functions, but doing so gives a useless analog (sum over zeros of f, not central-value family moment).

**Two-paper plan unchanged.** Theorem B-exact stays conditional on GRH (or partial-GRH in the form of 4-level density, etc.). The unconditional route via this paper does not exist.

**Recommendation:** add this to `GRH_bypass_FAMILY_aspect.md` as failed route #6 ("DHP-C 2026 — single-L sum-over-zeros, wrong object for family central-value moment").

**Cross-check vs. Farey error patterns:** the prior pattern "cite paper+theorem# with wrong content" applies — Sonnet appears to have confused "unconditional polynomial expansion with V-K error" with "unconditional GRH-free moment evaluation." These are different. Verbatim quotes above prevent that error here.
