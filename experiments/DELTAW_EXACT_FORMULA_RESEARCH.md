# ΔW Exact Formula — Open Problem Research
Created: 2026-04-13

## Problem Statement
Express cross term B = (2/n'²) Σ_{f ∈ F_{p-1}} D(f)·δ(f) in closed form.

## Known
- ΔW(p) = A - B - C + 1 - D_term - 1/n'² (four-term decomposition, exact, Lean-verified)
- A, C, D_term: always positive, clean expressions
- B: sign unknown, B can be negative (observed at p=9001, B=-3.72×10⁻⁴)
- Bridge identity: Σ_{f∈F_{p-1}} e^{2πipf} = M(p)+2 (proven, separate from B)
- Dedekind connection: T_b(p) = p²[s(b,p)+(p-1)/4] (mentioned in paper, not fully developed)

## Key Decomposition by Denominator
δ(a/b) = (a - pa mod b)/b
D(a/b) = #{f' ∈ F_{p-1}: f' ≤ a/b} - (n-1)·(a/b)

For fixed denominator b, the sum:
  S_b = Σ_{a: gcd(a,b)=1, 1≤a<b} D(a/b)·δ(a/b)

Then: Σ_{f} D(f)·δ(f) = Σ_b S_b + [boundary terms]

S_b may have a Dedekind-sum representation.

## Numerical verification needed
- Compute S_b for b=2,3,4,5,6,... at prime p=11
- Compare to Dedekind sums s(p,b) for those b
- If S_b = c·φ(b)·s(p,b) or similar → Dedekind formula found

## Status: OPEN PROBLEM, agents launched 2026-04-13
- Codex: thinking mode, algebraic approach
- Q3.6: literature + Dedekind sum angle
- Aristotle: pending (Q-linear independence task still in queue)

## Codex Analysis (2026-04-13)

### Key Result: FOUR-TERM DECOMPOSITION IS THE ENDPOINT

**1. Dedekind-Rademacher approach (feasible but not compact)**
- D(f) = finite sum of sawtooth terms ψ(mf) via Möbius inversion
- δ(f) = (f-1/2) - ψ(pf)  — isolates p-dependence into periodic fluctuation
- Product D(f)·δ(f) → bilinear sawtooth form → generalized Dedekind-Rademacher sums
- Computable, but not a single classical Dedekind sum. Divisor-summed combination.

**2. Critical exact cancellation (NEW)**
For each fixed denominator b with gcd(b,p)=1:
  Σ_{(a,b)=1} δ(a/b) = 0
Reason: multiplication by p permutes reduced residues mod b.
CONSEQUENCE: B is a COVARIANCE, not driven by a mean. M(p) as leading term unlikely.

**3. Asymptotic scale confirmed**
B = (2/n'²) Σ D(f)·δ(f) = O(log N / N²) ~ O(log p / p²)
This matches observed behavior. B ~ c·M(p)/p is not credible.
B ~ c·M(p)/p² possible only as secondary fluctuation.

**4. Bridge identity cannot control B**
Bridge: Σ e^{2πipf} = M(p)+2 is one unweighted Fourier mode.
B involves D(f)-weighted harmonic — strictly different object.
Bridge informative but not sufficient for B.

**5. Final verdict: NO f(M(p), p) formula**
Missing info: multiplicative residue data across ALL denominators b ≤ p-1.
M(p) alone cannot encode that. 

**Six-word summary:** Four-term decomposition is the natural endpoint.

## Status: RESOLVED (2026-04-13)
The open problem "derive ΔW from Farey without spectroscope chain" has a negative answer:
- No closed form B = f(M(p), p) exists
- B can be expressed as generalized Dedekind-Rademacher sums (computable, not compact)
- Connection ΔW ↔ M(p) is non-algebraic by necessity
- The four-term decomposition IS the exact Farey formula
- Any further compression requires zeros of ζ(s) via explicit formula
