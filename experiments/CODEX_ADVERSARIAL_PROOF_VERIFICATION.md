# Codex: Adversarial Verification of Three Theorems
# 2026-04-10 — FINAL CHECK

## RESULTS: 5 genuine gaps found

| Attack | Target | Verdict | Issue |
|--------|--------|---------|-------|
| A. Finite maximum | Thm 1 | PASS (not an issue) | Finite set, max achieved |
| B. Tied maximizers | Thm 1 | PASS (not an issue) | Ties don't invalidate |
| C. Off-line pollution | Thm 1 | **GENUINE HOLE** | No uniform gap β*-β_j ≥ ε. Nearby zeros approach β* |
| D. Too many zeros | Thm 1 | **GENUINE HOLE** | T=N² gives N² log N zeros. Error sum convergence not proved for this many |
| E. Sign of c | Thm 1 | **GENUINE HOLE** | c > 0 asserted but not proved. F_N can oscillate |
| F. Undefined residues | Thm 1+2 | **HARD FAILURE** | Need lower bounds on |ζ'(ρ)|. None cited unconditionally |
| G. M(p) majorant | Thm 2 | UNCLEAR | M(p) = O(p·exp(-c√logp)) needs exact citation |
| H. Σ p^{-1/2} | Thm 2 | PASS (correct) | p^{-1/2} ≥ p^{-1}, Lean verified |
| I. Large sieve swap | Thm 3 | **GENUINE HOLE** | Swapping roles of test points and coefficients not symmetric. Bound can blow up by factor P |

## MOST DANGEROUS: Attack F
The coefficients c_j = 1/(ρ_j·ζ'(ρ_j)) require |ζ'(ρ_j)| to be bounded below.
No unconditional lower bound on |ζ'(ρ)| is known.
If some ζ'(ρ_j) is very small, the error sum DIVERGES.

## SECOND MOST DANGEROUS: Attack I  
Theorem 3 (Upper RIP) may have the large sieve applied with wrong roles.
Need to re-derive directly with correct δ-spacing and normalization.

## RECOMMENDED FIXES
1. For Theorems 1+2: Write exact explicit formula identity for F_N term-by-term.
   Replace every zero term by correct residue. Prove uniform weighted zero-sum bound
   from a NAMED theorem (zero-density or mollifier).
2. For Theorem 3: Re-derive from additive large sieve with correct orientation.
   The prime logs are the "sequence", test frequencies are the "well-spaced points."
   This should give the correct bound without the swap issue.
3. For Attack E: F_N is defined as |...|² — it's NONNEG by definition. 
   But c > 0 in the lower bound needs the resonant term to not cancel.
   This requires the explicit formula evaluation to give a definite sign.
4. For Attack G: Cite Ivić (2003) or Titchmarsh Ch. 12 for the precise 
   unconditional bound on M(x).
