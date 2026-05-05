---
title: "GRH in Milinovich–Ng 2014: Where and Can Petersson Averaging Remove It?"
type: source-summary
domain: research
tier: working
confidence: 0.40
created: 2026-05-02
updated: 2026-05-02
verified: 2026-05-02
sources:
  - "Milinovich & Ng 2014, Simple zeros of modular L-functions, PLMS 109, arXiv:1306.0854"
  - "Booker, Milinovich, Ng 2019, Quantitative estimates for simple zeros, arXiv:1806.01959"
  - "Iwaniec & Sarnak 2000, Perspectives on the analytic theory of L-functions"
tags:
  - GRH
  - modular-L-functions
  - simple-zeros
  - petersson-averaging
  - zero-density
---

## Motivation

The Milinovich–Ng 2014 theorem on simple zeros of modular L-functions is conditional on GRH. The question: **where exactly does GRH enter**, and **can a Petersson family average (unconditional second-moment bound) bypass it?**

---

## Reviewed Sources

### 1. Milinovich & Ng 2014: Simple zeros of modular L-functions
**PLMS 109, 1465–1506; arXiv:1306.0854**

**Status**: **Abstract and general scope verified; full proof inspection incomplete.** Paper is 46 pages.

**Theorem statement (from abstract)**:
> Assuming the generalized Riemann hypothesis, we prove quantitative estimates for the number of simple zeros on the critical line for L-functions attached to classical holomorphic newforms.

**Key result (expected from title)**:
- Let S_k(q) denote newforms of weight k and level q.
- For f ∈ S_k(q), let N_simple(f, T) = number of simple zeros of L(s,f) with 0 < ℜ(s) < T on the critical line.
- **Claimed**: N_simple(f, T) ≫ T(log T)^{−ε} for any ε > 0 and sufficiently large T (assuming GRH).

**Where GRH enters (expected, requires PDF verification)**:
- Step 1: Prove that most zeros are simple (requires lower bound on Z'(ρ_f) away from zero, uses zero-free region or explicit bounds valid under GRH).
- Step 2: Relate simplicity to spacing statistics; may use sum-bound techniques that require GRH-like zero density conditions.

**Missing details** (need full PDF to extract):
- Exact section and theorem number.
- Precise equation/identity where GRH is invoked.
- Whether alternative zero-density hypothesis (e.g., Ingham-Karamata) could substitute.

---

### 2. Booker, Milinovich, Ng 2019: Quantitative estimates for simple zeros
**arXiv:1806.01959 (v1 submitted June 2018)**

**Status**: **Title and abstract confirmed; detailed comparison with 2014 version not extracted.**

**Expected contribution**:
- Extends M-N 2014 framework.
- May remove GRH or relax to weaker hypothesis (e.g., average-case zero-density bounds).

**Caveat**: Search results reference this paper as existing, but full technical comparison not verified in review.

---

### 3. Iwaniec & Sarnak: Perspectives on analytic theory of L-functions
**Proceedings of the Clay Mathematics Institute, 2000**

**Status**: **Foundational reference; specific Petersson-family sections not extracted.**

**Expected content**:
- Theorems on unconditional second moments of L-functions: E_f[ |L(1/2, f)|² ] averaged over weight-2 newforms f at level q.
- Petersson trace formula: ∑_f |a_n(f)|² = ... (explicit formula without GRH).
- Application to density of zeros (unconditional bounds on proportion of simple zeros in average sense).

**Relevance**: If a Petersson average of |L'(ρ_f, f)|² exists unconditionally, it could provide an alternative to the M-N argument.

---

### 4. Kowalski, Michel, VanderKam: Second-moment formulas for weight-2 newforms
**Multiple papers; specific citation for S_2 not extracted in search.**

**Expected relevance**:
- Explicit asymptotic for ∑_{f ∈ S_2(q)} |L(1/2 + it, f)|² ds (or derivative second-moment analogue).
- Unconditional proof using Petersson duality and Kloosterman sums.

**Status**: Referenced in context but not directly verified.

---

### 5. Hughes & Young 2010, Soundararajan: Moment bounds without GRH
**Fourth-moment methods; zero-density alternatives**

**Status**: **Located in search results; specific applications to simple-zero counts not extracted.**

**Expected content**:
- Bounds on ∑ |L'(ρ_f)|² without GRH, using power-saving in fourth moments.
- Soundararajan's omega results on moments of L-functions: upper/lower bounds independent of GRH.

---

### 6. de Faveri 2024: Power lower bound for simple-zero counts
**Cited in project HANDOFF docs**

**Status**: **Not found in web search; trust HANDOFF reference.**

**Expected relevance**:
- Offers unconditional (GRH-free) lower bound on the count of simple zeros, possibly at a weaker power of log.
- May use zero-density ζ(σ, T) bounds instead of GRH.

---

## Key Findings

### Finding 1: GRH in M-N 2014 is likely at the "most zeros are simple" step
The theorem requires showing that for most f, most zeros of L(s,f) are **simple** (multiplicity 1). This step typically invokes GRH or a strong zero-spacing hypothesis. **Without GRH**, the proof would fall back to an average result: "most f have most zeros simple," weaker than the statement for each individual f.

### Finding 2: Petersson averaging may give unconditional bounds on average simplicity
The Iwaniec–Sarnak framework provides **unconditional** second moments: ∑_f |a_n(f)|² computed via trace formulas (no GRH). Analogously, **if** an average-case formula for ∑_f 1_{ρ simple}(f) · |L'(ρ_f, f)|² exists, it could give an unconditional lower bound on the *proportion* of simple zeros in a family, bypassing GRH.

**Caveat**: The M-N 2014 statement is for **each individual f**, not an average. Family-averaging weakens the conclusion.

### Finding 3: Zero-density ζ-N(σ,T) vs. GRH dichotomy
- **GRH**: All non-trivial zeros on ℜ(s) = 1/2.
- **Alternative (zero-density bound)**: N(σ, T) (count of zeros in σ < ℜ(s) < 1) satisfies N(σ, T) ≪ T^{a(σ)(1−σ)+ε} for some exponent a(σ) (e.g., from Ingham–Karamata or Borel–Carathéodory).

**Feasibility of substitution**: For some applications (e.g., density of simple zeros in average), a strong zero-density bound may suffice. For tight quantitative control (T(log T)^{−ε}), GRH or near-GRH assumptions are often unavoidable.

### Finding 4: de Faveri 2024 likely offers the "unconditional path"
If de Faveri gives an unconditional power lower bound (e.g., T^{1−δ} simple zeros for δ > 0 small), this could be the first **GRH-free** result in this direction. Search did not retrieve the paper; verify via arXiv or project notes.

---

## Open Questions / Gaps

1. **Exact location of GRH in M-N 2014 proof:**
   - Which section, theorem, and equation?
   - Answer requires: Full PDF of arXiv:1306.0854.

2. **Can the M-N argument be converted to a Petersson average?**
   - Replace "for each f" with "∑_f (count of simple zeros)."
   - Resulting bound: ∑_f N_simple(f, T) ≥ ... T(log T)^{−ε} [unconditional?].
   - Answer requires: Explicit M-N proof + comparison with Petersson duality machinery.

3. **Is there a published unconditional (GRH-free) lower bound on simple-zero density?**
   - de Faveri 2024: unknown details.
   - Alternative sources: Soundararajan, Hughes–Young, or recent work on zero multiplicity?

4. **What is the weakest hypothesis that replaces GRH in the M-N argument?**
   - Candidate: Strong zero-density for L(s,f) (all f in family).
   - Candidate: Omega bounds on moments (Soundararajan).
   - Candidate: Average-case zero-distribution (Petersson).

---

## Candidate Replacement Hypothesis

If GRH cannot be avoided entirely, the following weaker assumptions may suffice:

1. **Explicit zero-free region** (classical):
   - L(s,f) has no zeros for ℜ(s) ≥ 1 − c/log q (or similar, depending on f).
   - **Pro**: Unconditional, available from analytic techniques.
   - **Con**: Weaker than GRH; may lose ε in the exponent.

2. **Petersson-averaged zero-density bound**:
   - ∑_f N(σ_0 + it, f; T) ≪ T^{2+ε} (or better, depending on σ_0).
   - **Pro**: Unconditional; captures average-case behavior.
   - **Con**: Result is average-case, not per-f.

3. **Power bound on non-simple zeros** (de Faveri / similar):
   - Unconditional: ∑_{ρ non-simple} |L'(ρ_f)|² ≪ T^α for α < 1.
   - **Pro**: Directly quantifies the error; asymptotically negligible.
   - **Con**: Requires new technique; may not exist in published form.

---

## Confidence & Caveats

**Confidence: 0.40**

- ✓ M-N 2014 exists and uses GRH; general framework confirmed.
- ✗ Exact section/equation where GRH is invoked: **not extracted**; requires full PDF.
- ✗ Petersson-family reduction: theoretical feasibility seems high, but no explicit formula located in search.
- ✗ de Faveri 2024: mentioned in HANDOFF, not independently verified.
- ✗ Alternative zero-density formulations: general knowledge, not cross-checked against specific M-N constraints.

**Action**: 
1. Download arXiv:1306.0854 PDF; mark sections and equations where GRH or zero-density bounds are assumed.
2. Check arXiv:1806.01959 (Booker et al. 2019) for whether GRH is removed or relaxed.
3. Locate and review de Faveri 2024 (check HANDOFF or arXiv).
4. If Petersson averaging is feasible, sketch the adaptation with explicit Trace Formula machinery.

**Caveat**: This is a bounded review. A definitive answer requires close reading of proofs (not abstracts) and may require original calculation to adapt M-N to unconditional setting.
