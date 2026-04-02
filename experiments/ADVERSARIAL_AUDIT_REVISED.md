# Adversarial Audit of main_revised.tex Abstract (Codex, 2026-04-02)

## Overall Verdict
**Abstract is NOT safe as written.** Two claims are WRONG, three are OVERSTATED.
Keep (ii) and (iii); rewrite or delete the rest before submission.

## Per-claim verdicts

| Claim | Verdict | Issue |
|-------|---------|-------|
| Preamble | NEEDS-QUALIFICATION | "Has never been studied" → "to our knowledge" |
| (i) | OVERSTATED | Decomposition doesn't "reduce sign to T(N)"; bridge only works on M(N)=-2 subsequence |
| (ii) | VALID | Regression identity B'/C' = α + ρ proved exactly |
| (iii) | VALID | Computational; counterexample at p=243,799 clearly labeled |
| (iv) | NEEDS-QUALIFICATION | Missing M(N)=-2 restriction; zero-sum needs truncation convention |
| (v) | OVERSTATED | Phase-lock claim uses empirical r=0.95 correlation, not theorem-grade; 0.07 rad is empirical |
| (vi) | **WRONG** | No proof for Dirichlet character decomposition; theory "in progress/unverified"; GRH dependency missing |
| (vii) | OVERSTATED | One alternative ordering experiment ≠ "confirms" ordering-dependence theorem |
| (viii) | **WRONG** | T(N)=Ω_±(√N) for integers doesn't yield prime subsequence without extra sieve argument |

## CRITICAL Issues (must fix before submission)

### (vi) Delete or heavily downgrade
The Dirichlet character decomposition claim has no proof in the paper. Internal
notes mark it "in progress" and "unverified." The GRH dependency is also missing
from the abstract while present in the dependency table. This is a false theorem claim.

### (viii) Delete or add sieve argument
T(N)=Ω_±(√N) is an integer statement. The jump to "infinitely many primes with
each sign" requires a nontrivial sieve argument (e.g., Dirichlet density of
M(p)=-3 primes is positive). The paper uses "vague sieve language" without proof.

## Checklist items

1. **GRH labels:** (iv) and (v) need explicit GRH tags; also (iv) needs M(N)=-2 restriction.
2. **0.07 rad:** Numerically correct (|5.278 - 5.2076| ≈ 0.071) but must be labeled "empirical."
3. **Computational vs analytical:** (iii) is clean; (v) mixes theorem+data; (vi) is presented as theorem despite no proof; (vii) is computation called confirmation.
4. **Missing caveats:** "to our knowledge" for novelty; truncation convention for zero-sums; empirical nature of phase-location; M(p)=-3 sample restriction; unproved (vi); prime-subsequence transfer in (viii).

## Recommended actions

- **Delete** claims (vi) and (viii) from abstract
- **Rewrite** (i): just state the four-term decomposition without claiming sign reduction to T(N)
- **Rewrite** (iv): add M(N)=-2 restriction and truncation convention
- **Rewrite** (v): label phase-lock result as "heuristic" or "empirical observation"
- **Rewrite** (vii): change "confirms" to "suggests" with appropriate qualification
- **Add** "to our knowledge" to preamble novelty claim
