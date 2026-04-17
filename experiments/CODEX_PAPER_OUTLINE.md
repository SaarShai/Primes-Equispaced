# Codex: NDC Paper Complete Outline
Date: 2026-04-14
Tokens: 23,123

## CORRECTIONS NOTED UPFRONT
1. L(ρ,χ)=0 at a zero — asymptotics must use L'(ρ,χ), not L(ρ,χ)
2. Turán citation unverified — do NOT use until independently confirmed
3. "double-pole" language for c_K needs care: 1/L has simple pole at ρ, 
   but Perron integrand K^w/(w·L(ρ+w)) has double pole at w=0 via the
   product of Perron's 1/w with 1/L's 1/w. State this precisely.

## JOURNAL TARGET
JNT (Journal of Number Theory) — most realistic.
MRL only if unconditional content is much stronger.
Compositio/Acta: not realistic with conjecture-only main result.

## ABSTRACT STRUCTURE
- [proved] Exact identities: conjugation symmetry + D_K = 1 + R_K
- [conditional] D_K → 1/ζ(2) under GRH + AK asymptotic
- [empirical] Multiple (χ,ρ) pairs cluster near 1/ζ(2); phase ≈ 0
- [significance] 1/ζ(2) links prime-zero duality to squarefree density

## SECTION OUTLINE
1. Introduction — motivation, main conjecture, prior art, paper map
2. Setup & Exact Identities — conjugation proof, D_K=1+R_K (rigorous)
3. Unconditional Non-vanishing — c_K≠0 for all but finitely many K
   (CAUTION: verify Turán attribution or replace with alternative route)
4. Conditional Mechanism — Perron for c_K, AK for E_K, two-line proof
5. Numerical Evidence — tables, plots, D_K·ζ(2) vs logK, phase plots
6. Squarefree Density Connection — arithmetic interpretation of 1/ζ(2)
7. Open Problems — 7 concrete questions

## ANTICIPATED REFEREE OBJECTIONS
1. No theorem: main result is conjectural
2. Turán citation suspect
3. L(ρ) vs L'(ρ) notation inconsistency
4. Statistics too small / correlated
5. Why should 1/ζ(2) appear?
6. Theorem/conjecture/numerics too loosely mixed

## PATH TO UNCONDITIONAL (single key theorem)
"A sharp asymptotic with effective error for E_K^χ(ρ) at a simple zero:
E_K = B_{χ,ρ}/logK + o(1/logK) with B_{χ,ρ} = L'(ρ,χ)/ζ(2) explicit."
This is the missing ingredient. If proved, the paper becomes a theorem.

## STATUS MATRIX (for paper writing)
| Claim | Status | Section |
|---|---|---|
| D_K^χ(ρ)* = D_K^{χ̄}(ρ̄) | PROVED (unconditional) | §2 |
| D_K = 1 + R_K | PROVED (unconditional) | §2 |
| c_K ≠ 0 for all but fin. many K | NEEDS CITATION VERIFY | §3 |
| c_K ~ logK/L'(ρ) | CONDITIONAL (GRH) | §4 |
| E_K ~ L'(ρ)/(ζ(2)logK) | CONJECTURE | §4 |
| D_K → 1/ζ(2) | EMPIRICAL CONJECTURE | §5 |
