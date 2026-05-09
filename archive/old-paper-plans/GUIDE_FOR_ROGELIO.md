# Guide for Rogelio Tomás García

## What's New Since the Draft You Read

The paper you're reading (paper/main.tex, "The Geometric Signature of Primes") 
is Paper A — the foundational Farey discrepancy paper. Since that draft, 
significant new results have been proved. This guide points to the most relevant 
material for your expertise.

## The Explicit Formula (your question: "how would one get to this?")

The key identity connecting ΔW(p) to zeta zeros:

  ΔW(p) ~ -2 Σ_k Re[p^{iγ_k} / (ρ_k · ζ'(ρ_k))]

**Derivation sketch:**
1. The Bridge Identity (Lean-verified, file `RequestProject/BridgeIdentity.lean`):
   Σ_{f ∈ F_{p-1}} e^{2πipf} = M(p) + 2, via Ramanujan sums c_q(p) = μ(q).

2. The per-step discrepancy ΔW(p) is controlled by M(p) through the 
   four-term decomposition (Section 4-5 in paper/main.tex).

3. The explicit formula for M(x): M(x) ~ Σ_ρ x^ρ / (ρ · ζ'(ρ))
   (standard, see Titchmarsh Ch 14). This was verified to 0.003 rad 
   precision: phase φ₁ = -arg(ρ₁ · ζ'(ρ₁)) = -1.6933 rad matches 
   empirical data.

**Full proof (GRH-conditional):** The resonant term at γ_k grows as 
N^{1/2}/log N while off-resonant terms remain bounded (T₀ = (log N)^A trick).
See: https://github.com/SaarShai/batch-spectroscope/results/ for numerical 
verification data.

## Your C_W Bound Suggestions

You correctly identified that Theorem 6.8 is dominated by 6.9. We will:
- Remove Theorem 6.8
- Apply your analytical rank formulas (Partial Franel sums Theorem 3, 
  Integers y63 Theorem 2, InspireHEP Theorem 1) to improve our C_W ≥ N/28
- Compare to the RH-conditional prediction C_W ~ (1/2π²)N log N
- Cite your papers properly

## Your R(f) / Local Discrepancy Connection

Your Eq. (6) in the 2025 MDPI paper defines a local discrepancy with offset.
Our R(f) = ΣD·δ / Σδ² (correlation ratio) may be related. We have a task 
computing the exact mathematical comparison. The sum limits differ 
(⌊N/d⌋ vs ⌊N/d⌋ mod k) but the structure may connect.

## Most Relevant Files in the Repository

### Lean 4 Formalization (434 results):
- `RequestProject/BridgeIdentity.lean` — the key bridge: Σe^{2πipf} = M(p)+2
- `RequestProject/InjectionPrinciple.lean` — distinct gap insertion
- `RequestProject/PrimeCircle.lean` — core Farey properties, cardinality

### Computational Results:
- https://github.com/SaarShai/batch-spectroscope/results/
  - `DRH_PRECISION_RESULTS.md` — scaling |c_K(ρ)| ~ log(K)/|ζ'(ρ)| at 50 digits
  - `avoidance_ratios.md` — 4-16x zero avoidance phenomenon
  - `interval_certificates_800.md` — 800 rigorous non-vanishing certifications

### Papers in Preparation:
- Paper A (your current read): foundational ΔW, four-term decomposition, sign pattern
- Paper C: "Prime Spectroscopy of Riemann Zeros" — explicit formula proof, 
  avoidance conjecture, batch speedup. Not yet written but outline at 
  batch-spectroscope/results/
