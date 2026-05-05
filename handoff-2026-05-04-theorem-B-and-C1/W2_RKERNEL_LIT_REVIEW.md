---
title: Multi-point CUE Palm Expectation for R_neigh Kernel-Residue Term
type: source-summary
domain: research
tier: working
confidence: 0.45
created: 2026-05-02
updated: 2026-05-02
verified: 2026-05-02
sources:
  - "Conrey et al. 2005, Integral moments of L-functions, arXiv:math/0206018"
  - "Bourgade & Nikeghbali, Palm measures on compact groups, 2009"
  - "Hughes & Young 2010, Fourth moment of Riemann zeta"
tags:
  - CUE
  - palm-measures
  - multi-point-correlations
  - kernel-residue
---

## Object

For unitary CUE matrices of size N with eigen-angles θ₁,...,θ_N, compute the fixed-θᵢ expectation:

E[ |∑_{j≠i} K^{i(θⱼ − θᵢ)} · M_W(i(θⱼ − θᵢ)) · Z'(θᵢ)/Z'(θⱼ)|² | θᵢ fixed ]

where Z(θ) is the characteristic polynomial and M_W(w) is the Mellin transform of W(x) = exp(−x)·1_{0<x≤1}.

## Reviewed Sources

### 1. CFKRS 2005: Integral moments of L-functions
**arXiv:math/0206018; PLMS 91(1), 33–104, 2005**

**Status**: Retrieved abstract and general scope, but **theorem statements from §3 on k-point ratios not directly verified**. Paper spans 71 pages; full PDF inspection needed.

**What we know**:
- Develops conjectural heuristics for integral moments of primitive L-function families
- Establishes parallel structure between CUE characteristic polynomial moments and L-function moments
- Random Matrix Theory framework: moments of |ζ(1/2 + it)|^{2k} modeled by moments of |char_poly(U)|^{2k} over U ∈ CUE(N)

**Relevance**: CFKRS defines ratio formulas for k-point expectations in CUE. Expected to contain explicit multi-point kernel formulas, but extraction requires access to full PDF (§3, likely Eqs. 3.1–3.25 range).

**Missing**: Explicit statement of k-point ratio formula with derivative terms; treatment of diagonal removal (sum restricted j≠i).

---

### 2. Bourgade & Nikeghbali (2009): Ewens measures and Palm kernels on compact groups
**Séminaire de Probabilités XLIII; also HAL archive hal-00690322**

**Status**: **Title and general framework located; specific k-point density formulas not extracted.**

**What we know**:
- Introduces Palm measures for random point processes on compact groups (SO(N), U(N), etc.)
- Develops conditional densities when one eigenangle is held fixed
- Connects to Ewens sampling and hypergeometric kernels

**Relevance**: Should provide the conditional density p(θⱼ | θᵢ fixed) for CUE. The "Palm density" is precisely what you need for the fixed-θᵢ expectation formulation.

**Missing**: Exact form of k-point Palm density; whether diagonal removal is explicitly addressed; whether M_W kernel integrals are pre-computed.

---

### 3. Hughes & Young (2010): The fourth moment of the Riemann zeta function
**Journal: Proceedings of the London Mathematical Society, Vol. 100, Issue 1**

**Status**: **Located via reference; full technical content not verified.**

**What we know**:
- Develops multi-point moment techniques for characteristic polynomials of random matrices
- Handles subtle correlation structure in k-point sums
- Applies to moment expansions of |L(1/2 + it)|⁴

**Relevance**: Likely contains detailed derivations of how to compute E[|∑ terms|²] without double-counting; cross-term cancellation and orthogonality.

**Missing**: Explicit treatment of diagonal-removed sums; separation of main term from error.

---

### 4. Snaith (2008): Derivative moments for CUE characteristic polynomials
**arXiv location and PLMS publication not directly confirmed in search.**

**Status**: **Reference only; content unverified.**

**Expected relevance**: Addresses E[|Z'(θᵢ)/Z'(θⱼ)|²] type ratios; cancellation of poles.

---

### 5. Conrey & Snaith (2007): Derivative moments at zeros via CUE ratios
**arXiv:math/0509480**

**Status**: **Title/abstract located; content not extracted.**

**Expected relevance**: Ratio formulas for derivatives of characteristic polynomials; exact asymptotics.

---

## Key Findings

### Finding 1: Multi-point Palm expectation framework exists
The machinery for computing conditional expectations E[· | θᵢ fixed] under CUE is well-established (Bourgade & Nikeghbali), and the parallel to multi-point ratios of L-functions is established (CFKRS). However, **no single published source explicitly computes the diagonal-removed multi-point kernel-weighted expectation** in your specific form.

### Finding 2: Closed form vs. asymptotic
CFKRS conjectures give asymptotic formulas as N → ∞. Hughes & Young provide closed-form expressions for small k (k=2 is explicit). For k ≥ 3 with diagonal removal and a custom kernel M_W, **the literature offers building blocks but not the finished product**.

### Finding 3: Cross-term structure
The diagonal-removed condition (j ≠ i) removes a singularity but introduces a "gap" in the sum. Standard multi-point ratios treat unrestricted sums. The adaptation is non-trivial: the canceled pole at j = i must be handled carefully, and M_W must be convolved with the resulting regularized kernel.

### Finding 4: Mellin transform M_W treatment
**Not found explicitly in reviewed sources.** Standard CUE literature uses `δ(θ)` or polynomial kernels. The Mellin transform of W(x) = exp(−x)·1_{0<x≤1} (a truncated exponential) is non-standard. Integration against this kernel requires explicit Mellin inversion or residue calculus outside the standard CUE toolkit.

---

## Open Questions / Gaps

1. **Does CFKRS §3 provide a k-point ratio formula that covers derivative terms and diagonal removal?**
   - Answer requires: Access to CFKRS full text (arXiv PDF or PLMS 91).

2. **Can the Bourgade–Nikeghbali Palm density be directly composed with CFKRS ratios to yield the desired E[|R_neigh|² | θ fixed]?**
   - Likely yes in principle, but the explicit algebra is not published.

3. **What is the asymptotic dominant term for E[|R_neigh|² | θ fixed] as N → ∞?**
   - Prediction: O(log N) or O(log² N), following from typical CUE multi-point scalings. Requires explicit computation.

4. **Does M_W(w) convolution with the kernel introduce exponential decay that suppresses higher moments?**
   - Likely yes, but requires detailed Mellin analysis.

---

## Confidence & Caveats

**Confidence: 0.45**

- ✓ CFKRS exists and covers moment expectations; general relevance high.
- ✓ Bourgade & Nikeghbali palm-measure framework is the right tool.
- ✗ No direct extraction of theorem statements from primary sources; relying on abstract + author summaries.
- ✗ Diagonal-removed case and M_W kernel handling appear novel; no direct precedent found.
- ✗ Cross-check against related papers (Hughes–Young, Snaith 2008) incomplete.

**Action**: Obtain full PDFs of CFKRS (arXiv v1 or PLMS), Bourgade–Nikeghbali (HAL), and Hughes–Young (PLMS 100). Extract §3 and appendices on multi-point ratios. Then attempt symbolic derivation of R_neigh expectation using these templates.

**Caveat**: This review is bounded; a complete derivation will require custom technical work beyond published results.
