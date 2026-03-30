# Independent Verification of Sign Theorem Proof Claims

**Date:** 2026-03-29
**Method:** Exact Fraction arithmetic (Python), independent computation from scratch
**Verifier:** Adversarial review agent (no access to research agent reasoning)

---

## Summary

| # | Claim | Verdict | Notes |
|---|-------|---------|-------|
| 1 | Cross-term formula: sum D*delta^2 = -(1/2)sum delta^2 - 1/2 | **PASS** | Exact for all 23 primes 5..97 |
| 1b | Fractional parts: sum {pf} = (n-2)/2 | **PASS** | Exact for all 14 primes 5..97 |
| 2 | Cauchy-Schwarz: sum D = -n/2, hence sum D^2 >= n/4 | **PASS** | Exact for N = 5,10,20,50,100,200 |
| 3 | C_W >= N/28 (shift-squared lower bound, raw) | **PASS** | sum delta^2 >= p/28 for all 20 primes 5..97 |
| 4 | sum E(k)^2 >= p^2/28 (endpoint argument) | **PASS** | For all 10 primes 5..37 |
| 5 | D_q(2) = q(q^2-1)/24 (deficit formula) | **PASS** | Exact for all 27 primes 5..109 |
| 6 | D_q(r) >= D_q(2) (deficit minimality) | **PASS** | For all 23 primes 5..97, all r |
| 7 | \|1 - calD/A\| <= K*\|M\|/p with K <= 10 | **PASS** | Max K = 2.54 (at p=41) across 21 primes |
| 8 | B+C > 0 for all M(p) <= -3 primes | **PASS** | All 210 such primes to p=3000, zero violations |
| -- | Four-term decomposition identity | **ISSUE** | Paper formula has boundary term error (see below) |

**Overall: All 8 substantive claims VERIFIED. One minor presentational error found in the decomposition formula.**

---

## Claim 1: Cross-term Formula

**Claim:** For every prime p >= 2,
```
sum_{f in F_{p-1}} D(f) * delta(f)^2 = -(1/2) * sum delta(f)^2 - 1/2
```
where D(f) = rank(f) - n*f (integer-scale) and delta(f) = f - {pf}.

**Method:** Exact Fraction arithmetic. Computed both sides independently for all primes 5 through 97 (23 primes).

**Result:** EXACT equality for all primes. Zero numerical discrepancy (exact rational comparison).

**Verdict: PASS**

---

## Claim 1b: Fractional Parts Sum

**Claim:** sum_{f in F_{p-1}} {pf} = (n-2)/2

**Method:** Exact Fraction. 14 primes tested (5 through 97).

**Result:** EXACT match.

**Verdict: PASS**

---

## Claim 2: Cauchy-Schwarz Bound

**Claim:** sum D(f) = -n/2 (exact), therefore by Cauchy-Schwarz sum D^2 >= n/4.

**Method:** Exact computation for N = 5, 10, 20, 50, 100, 200.

**Results:**
- sum D = -n/2: EXACT for all N tested
- sum D^2 >= n/4: holds with significant margin (ratio sum_D^2/(n/4) ranges from 1.58 to 149)
- C_W = N * sum d^2 ranges from 0.18 (N=5) to 0.61 (N=200), consistent with bounded growth

**Note:** This gives C_W >= N/(4n) ~ pi^2/(12N) -> 0, which is a very weak bound. The Cauchy-Schwarz step is correct but the resulting bound is not tight. The paper's actual C_W bound comes from the Franel-Landau + PNT route, not from this Cauchy-Schwarz step alone.

**Verdict: PASS (identity and bound both verified)**

---

## Claim 3: Shift-Squared Lower Bound

**Claim:** sum delta(f)^2 >= p/28 (equivalently, C_raw >= p/28).

**Method:** Exact computation for 20 primes from 5 to 97.

**Results:**
- p=5: ratio sum/p = 0.244 (above 1/28 = 0.0357) -- PASS
- p=97: ratio = 4.661 -- growing rapidly
- All primes pass with increasing margin

The ratio sum_delta^2 / p grows roughly linearly with p, so the bound p/28 is conservative.

**Verdict: PASS**

---

## Claim 4: Endpoint Argument (sum E(k)^2 >= p^2/28)

**Claim:** sum_{k=1}^{p-1} D_{F_p}(k/p)^2 >= p^2/28

**Method:** Exact computation. For each new fraction k/p, computed its exact rank in F_p and displacement. 10 primes 5 through 37.

**Results:**
- p=5: ratio 2.24x
- p=37: ratio 6.67x
- All primes pass with growing margin

**Verdict: PASS**

---

## Claim 5: Deficit Formula D_q(2) = q(q^2-1)/24

**Claim:** For prime q, the deficit D_q(2) = sum_{gcd(a,q)=1} a^2 - sum_{gcd(a,q)=1} a*(2a mod q) equals q(q^2-1)/24.

**Method:** Brute-force computation for all 27 primes from 5 to 109.

**Result:** EXACT integer match for every prime tested. This is a clean identity.

**Verdict: PASS**

---

## Claim 6: Deficit Minimality D_q(r) >= D_q(2)

**Claim:** Among all multipliers r coprime to q (r = 2, 3, ..., q-1), the multiply-by-2 permutation achieves the minimum deficit.

**Method:** Computed D_q(r) for ALL valid r, for 23 primes from 5 to 97.

**Result:** For every prime tested, D_q(2) is exactly the minimum deficit. Often achieved uniquely at r=2 (and r=q-2 by symmetry).

**Note on proof:** The paper attributes this to Dedekind reciprocity. The numerical evidence is overwhelming but this is NOT a proof. The claim should be treated as verified computationally but requiring an analytical proof for publication.

**Verdict: PASS (computational verification)**

---

## Claim 7: K <= 10 in |1 - calD/A| <= K * |M(p)|/p

**Claim:** The ratio calD/A satisfies |1 - calD/A| <= K * |M(p)|/p with K <= 10 (equivalently, K is a moderate constant).

**Method:** Exact computation of A (dilution) and calD (new-fraction discrepancy) for 21 primes 11 through 97.

**Results:**
- Maximum K observed: 2.54 at p=41 (M(41) = -1)
- For M(p) <= -3 primes, K is typically below 1.5
- calD/A ranges from 1.001 (p=73) to 1.18 (p=19), always > 1 in this range

**Note:** calD/A > 1 means the new-fraction discrepancy EXCEEDS the dilution. This is consistent with the paper's observation that calD/A = 1 + O(1/p).

**Verdict: PASS (K <= 2.55, well within the claimed K <= 10)**

---

## Claim 8: B + C > 0 for All M(p) <= -3 Primes

**Claim:** For every prime p with M(p) <= -3, the sum B + C > 0 (where B is the cross term and C is the shift-squared term, both excluding f=1 from the sum).

**Method:**
- Exact Fraction arithmetic for p <= 200 (21 primes)
- Float64 arithmetic for 200 < p <= 3000 (189 primes)
- Total: 210 primes with M(p) <= -3 tested

**Results:**
- Zero violations
- Minimum B+C = 6.44e-7 at p=2543 (M=-3)
- B+C decreases roughly as O(1/p^2) but remains strictly positive
- B itself is always positive (when B excludes f=1 from the sum)

**Note on B sign:** The paper (Remark after Thm 5.1) states "The cross term B is negative at p = 13." This is **inconsistent with the paper's own definition** of B (which excludes f=1). With f=1 excluded, B is POSITIVE for ALL M(p) <= -3 primes including p=13. The negative B at p=13 occurs only when f=1 is INCLUDED in the sum:
- B_excl(13) = +2.02e-4 (positive, using paper's definition)
- B_all(13) = -3.72e-4 (negative, including f=1)

This is a **minor inconsistency** in the paper's boundary treatment.

**Verdict: PASS**

---

## ISSUE: Four-Term Decomposition Formula

### Paper's claim (Equation 4.2):
```
DeltaW(p) = A - B - C - calD - 1/n'^2
```
where DeltaW(p) = W(p-1) - W(p), and B, C are summed over old fractions EXCLUDING f=1.

### What is actually true:

**Two correct forms:**
1. `DeltaW = A - B_excl - C_excl - calD` (B,C exclude f=1, NO boundary term)
2. `DeltaW = A - B_all - C_all - calD - 1/n'^2` (B,C include ALL f, WITH boundary term)

The paper uses B,C excluding f=1 BUT includes the 1/n'^2 boundary correction. This double-counts the boundary. The correct formula with their definition of B,C (excluding f=1) should have NO 1/n'^2 term.

### Proof of the discrepancy:
For f=1: D_old(1) = -1, delta(1) = 1.
- Including f=1 adds -2/n'^2 to B (from 2*D*delta = 2*(-1)*1) and +1/n'^2 to C
- Net: including f=1 shifts -(B+C) by -(-2/n'^2 + 1/n'^2) = +1/n'^2
- So A - B_all - C_all = A - B_excl - C_excl + 1/n'^2
- Therefore A - B_all - C_all - 1/n'^2 = A - B_excl - C_excl

Both give the same result, but the paper mixes conventions.

### Impact on the proof:
**NONE.** The 1/n'^2 term is negligible (of order 1/N^4) and does not affect any bound or conclusion. The sign theorem is correct regardless. The DeltaW < 0 condition correctly requires A < B + C + calD (for the f=1-excluded version), which is exactly what the computational and analytical arguments establish.

### Verified:
The corrected formula `DeltaW = A - B_excl - C_excl - calD` matches EXACTLY (Fraction arithmetic) for all 23 primes from p=5 to p=97.

---

## Additional Observations

### DeltaW sign convention
The paper defines DeltaW(N) = W(N-1) - W(N), so DeltaW > 0 means uniformity IMPROVES. This is the reverse of the standard convention DeltaW = W(N) - W(N-1). Verified by direct computation:
- p=5: DeltaW = +0.013 (wobble decreases, improvement)
- p=13: DeltaW = -0.0027 (wobble increases, worsening)
This is consistent with the paper's claim that M(13)=-3 primes have DeltaW < 0.

### Deficit minimality (Claim 6)
For all 23 primes tested, r=2 achieves the EXACT minimum deficit. This is a remarkably clean result. For the proof to be complete, an analytical argument (via Dedekind reciprocity or otherwise) is needed. The computational evidence is compelling but does not constitute a proof.

### Growth of B relative to C
As p increases, B dominates C (B/C grows roughly as p). This means the cross-term, not the shift-squared term, provides the dominant margin. The proof's strategy of bounding C alone (ignoring B) leaves significant margin on the table.

---

## Methodology Notes

1. **Farey generation:** Used the mediant algorithm (O(n) time, no sorting) for exact generation
2. **Arithmetic:** Python `fractions.Fraction` for all small-prime computations (p <= 200). Float64 for p > 200 in Claim 8 only, where margins are 4+ orders of magnitude above float64 precision
3. **Independence:** No code or results from the research agent were used. All quantities computed from definitions
4. **Adversarial posture:** Specifically checked for off-by-one errors, boundary mishandling, sign conventions, and formula consistency
