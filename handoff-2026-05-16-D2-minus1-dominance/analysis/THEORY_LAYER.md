# Theory layer — the −1-dominance hierarchy, with claim provenance

Status labels: **[PROVEN]** classical/established theorem; **[COND]**
established but conditional on a stated hypothesis; **[CONJ]** open
conjecture; **[CIT-UNVERIFIED]** asserted only in Koyama's unpublished
preprint (`nontriv.pdf`), not independently verified; **[OBSERVED]**
our finite-x measurement.

The four layers below are kept deliberately separate; the experimental
study only produces Layer O/F and reads Layer T/I as interpretation.

## Verified primary sources

- **Rubinstein & Sarnak**, "Chebyshev's bias," *Experimental
  Mathematics* **3** (1994), no. 3, 173–197. Verified: Project Euclid
  `em/1048515870`, T&F doi 10.1080/10586458.1994.10504289. [PROVEN
  framework, COND on GRH + LI]
- **Aoki & Koyama**, "Chebyshev's bias against splitting and principal
  primes in global fields," *Journal of Number Theory* **245** (2023)
  233–262; arXiv:2203.12266. Verified: ScienceDirect
  S0022314X22002335, arXiv, author researchmap. [COND on the Deep
  Riemann Hypothesis (DRH)]
- Koyama, "*A Hidden Hierarchy of Chebyshev's Bias and the Dominance
  of −1 (mod N)*" — **unpublished preprint, the unverified
  counterparty's draft**. Every claim sourced only here is
  **[CIT-UNVERIFIED]** and is treated as a conjecture to be tested,
  never as an established fact. (See `correspondence/KOYAMA.md` RISK.)

## Layer T — theoretical bias ordering

Let `N ≥ 3`, `a` coprime to `N`. The prime race compares `π(x;N,a)`
across residues.

- **[PROVEN]** (Dirichlet) each coprime class has the same main term
  `π(x;N,a) ~ Li(x)/φ(N)`; the race is about the second-order term.
- **[PROVEN]** (explicit formula) the normalised difference
  `E(x;N,a,b) = (log x / √x)·(π(x;N,a) − π(x;N,b))` is, up to lower
  order, an almost-periodic function of `log x` whose Fourier
  frequencies are the ordinates `γ` of the non-trivial zeros
  `½ + iγ` of the Dirichlet L-functions `L(s,χ)`, `χ mod N`.
- **[COND: GRH+LI]** (Rubinstein–Sarnak) `E(·;N,a,b)` has a limiting
  logarithmic distribution. Its **mean** is controlled by
  `c(N,a) := #{ t mod N : t² ≡ a (mod N) }`: classes that are squares
  carry an extra `−c` drift, so **quadratic non-residue classes lead
  quadratic-residue classes** ("bias against squares / against the
  principal class `a=1`"). Among non-residues the means are equal
  (all `c=0`); they are separated only by the *shape* (variance,
  skew) of the limiting law, i.e. by the detailed zero data of the
  `L(s,χ)`.
- **[COND: DRH]** (Aoki–Koyama 2023) a DRH-weighted prime counting
  yields an *explicit asymptotic formula* for the magnitude of the
  deflection and a criterion for the bias of primes with a prescribed
  Frobenius element — a new *formulation* of Chebyshev's bias that
  makes the inter-class ordering ("hierarchy") explicit under DRH.

**The "Dominance of −1" hypothesis.** **[CONJ / CIT-UNVERIFIED]**
Koyama's preprint conjectures that within the quadratic non-residues
mod `N`, the class `a ≡ −1 (mod N)` exhibits the *largest* bias
(`π(x;N,−1) − π(x;N,1)` is the top, or in the top group, among
non-residues in the appropriate limiting/weighted sense). This is the
object under study. It is **not** an established theorem; Rubinstein–
Sarnak and Aoki–Koyama supply the framework but not this specific
strong ordering. We test consistency, we do not assert it.

## Layer O — raw observable

`D(x;N,a) := π(x;N,a) − π(x;N,1)`, an integer step function of `x`.
Subtracting the principal class `a=1` cancels the common
`Li(x)/φ(N)` and exposes the bias fluctuation, of size `O(√x/log x)`.
No modelling: this is exactly what the two sieves count.

## Layer F — finite-range evidence (this study)

The dynamic curve `x ↦ D(x;N,a)` for `N ∈ {7,8,11,19,23}`, all coprime
`a`, on a 50-pt/decade grid. We report **[OBSERVED]**: (i) for each
`N`, the smallest `x` past which `−1` is the max non-residue / in the
top group and stays so over the sampled grid ("visibility onset");
(ii) the sign changes of `D` (Littlewood-type oscillations) =
"transient reversals"; (iii) the dominant log-x wavelength of those
oscillations.

## Layer I — asymptotic interpretation (read-only, clearly fenced)

- The Layer-T limiting statement is about **logarithmic density as
  x → ∞**, not any single finite `x`. A finite-range pattern neither
  confirms nor refutes it; we never claim it does.
- A single low-lying zero `½ + iγ_min` of some `L(s,χ mod N)`
  contributes an oscillation of **log-x wavelength `2π/γ_min`**. If
  `γ_min` is unusually small for `N`, that one mode dominates finite
  `x` and can pin the race in a non-asymptotic (reversed) configuration
  until `log x` is large. The onset scale is set by `γ_min`, an
  intrinsic, computable quantity (we compute it independently in
  `lowzeros.py`, NOT relying on the preprint's number).
- **[CIT-UNVERIFIED]** Koyama states that for `N = 23` the dominance
  regime only sets in near `log x ≈ 33.4` (`x ≈ 3.2·10¹⁴`). We treat
  `e^{33.4}` purely as a target to test; the independent test is
  whether our measured dominant wavelength for `N=23` matches
  `2π/γ_min(23)` and whether `−1` is still sub-dominant at `1.3·10¹³`
  but resolving toward `3·10¹⁴`.

## Honest scope ceiling

This is finite experimental number theory at the Experimental-
Mathematics / specialist tier: a high-resolution, doubly-verified
*measurement* of a known phenomenon's finite-x dynamics, framed as the
user's independent verification/extension. It is **not** a proof, not
progress on GRH/DRH/RH, and not a confirmed joint deliverable.
