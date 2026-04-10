# GAP 2 Full Closure: Adversarial Verification

## Date: 2026-03-29
## Status: CLOSURE FAILS -- Critical gaps identified in claimed proof chain

---

## 0. Executive Summary (Adversarial)

The claimed closure path via K <= 10 + Dress-El Marraki has **THREE critical
failures**, any one of which is fatal:

1. **K <= 10 is NOT proved.** The "proof" is a sketch with empirical constant
   (K_max = 6.16 for p <= 499). The analytical derivation has internal
   contradictions (Section 3.4 gets S_virt/A' ~ 1/2, then backtracks).
   The decomposition K = 7 + 2 + 1 has no rigorous derivation of the "7".

2. **C/A >= 0.59/log(p) is PURELY EMPIRICAL.** The proved bound is
   C/A >= 1/(65.1 * log^2(p)), which is a factor of ~40x weaker.
   The entire bypass argument 0.13 < 0.59 collapses.

3. **Option B (Dress-El Marraki) ALSO fails** because it needs C/A >= 0.044,
   but the proved bound at p ~ 618K gives C/A >= 1/(65.1 * log^2(618K))
   = 1/(65.1 * 168.6) = 0.000091, which is far below 0.044.

**Bottom line:** The proof has no valid closure path at present. What
follows is a detailed analysis of each component.

---

## 1. Verification of K <= 10 Proof (K_BOUND_PROOF.md)

### 1.1 What IS proved (rigorously)

- The algebraic identity: D'/A' - 1 = (S_virt/A' - 1) + 2X_cross/A' + S_kp/A'
  **STATUS: PROVED** (pure algebra)

- S_kp/A' = O(1/p) with explicit constant
  **STATUS: PROVED** (Section 3.2 of K_BOUND_PROOF.md is correct)

- The Franel exponential sum: sigma_p = sum_{f in F_N} e(pf) = 1 + M(N)
  for prime p > N.
  **STATUS: PROVED** (standard identity, verified computationally for p <= 200)

- The CONNECTION between aliasing error and M(p) via sigma_p.
  **STATUS: PROVED in structure**, but the CONSTANT is not determined.

### 1.2 What is NOT proved

**The dominant term bound |S_virt/A' - 1| <= 7|M(p)|/p is NOT proved.**

The K_BOUND_PROOF.md document itself reveals the failure:

- Section 3.4 (line ~253): The Riemann sum approach gives S_virt/A' ~ 1/2,
  which "contradicts data (S_virt/A' near 1)."

- Section 3.5 attempts a "direct comparison via interpolation identity"
  but only gets to the point of identifying that the floor function error
  sum_j (m_j - p*h_j) * D_j^2 is the source, then says "this is precisely
  the aliasing error, controlled by the Mertens function" without
  establishing the bound.

- Section 4.3 (line ~413): The "proof outline" explicitly says the Erdos-Turan
  bound is "too crude" for this purpose.

- Section 4.5 attempts "direct algebraic proof" via interpolation
  decomposition. This gets partway but then relies on the claim (line ~497):
  "|alpha(p) - 2| * p / |M(p)| <= 12 for all tested primes"
  which is EMPIRICAL, not proved.

- Section 9.5 (the "Mertens function appears" section) has a sketch involving
  Cauchy-Schwarz and Weil bounds but never pins down the constant.

- Section 10.4 claims K = C_alias + C_cross + C_kp = 7 + 2 + 1 but the
  derivation of C_alias = 7 is based on "the amplitude of hat{g}(p)" being
  "bounded by old_D_sq / (n*p) * |sigma_p|" and a "geometric series factor < 2"
  for higher aliasing terms. This is a SKETCH, not a proof.

### 1.3 The real status of K

- **Empirically verified:** K <= 6.16 for all primes p <= 499.
  This is ONLY 93 primes. The verification range is tiny.

- **Analytically:** The structure of the proof (aliasing connects to M(p)
  via Poisson summation) is CORRECT. But the constant is not pinned down.
  The "proof" of K = 10 relies on: sketch + safety margin over empirical max.

- **Risk:** K could grow with p. The worst-case K = 6.16 occurs at p = 359
  with M(359) = -1. For larger primes with |M(p)| = 1, the ratio
  |gap| * p could potentially grow. However, the aliasing framework suggests
  K should be bounded, and the empirical evidence is consistent with this.

### 1.4 Verdict on K <= 10

**NOT PROVED.** The proof document contains a correct structural analysis
and a plausible constant, but the analytical derivation has gaps that are
acknowledged in the document itself. To make this rigorous would require:

(a) A complete explicit Erdos-Turan-Koksma inequality for piecewise-quadratic
    functions with O(n) pieces, sampled at p << n equi-spaced points, or

(b) A direct algebraic proof via the interpolation decomposition (Section 4.5)
    with explicit constant tracking through the Cauchy-Schwarz and Weil bound
    steps, or

(c) Extension of the computational verification to a much larger range
    (p ~ 10^6 or beyond) to build confidence.

---

## 2. Verification of Dress-El Marraki Bound

### 2.1 The claimed bound

|M(x)| <= x/2360 for all x >= 617,973.

### 2.2 Verification

This is a REAL published result:

- **Paper:** F. Dress and M. El Marraki, "Fonction sommatoire de la fonction
  de Mobius. 2. Majorations asymptotiques elementaires," *Experimental
  Mathematics*, Vol. 2, No. 2, pp. 99-112 (1993).

- The bound |M(x)| <= x/2360 for x >= 617,973 is established in this paper.
  It is unconditional.

### 2.3 What this gives for the K bound path

If K <= 10 WERE proved, then for p >= 617,973:

    |1 - D'/A'| <= 10 * |M(p)|/p <= 10/(2360) = 0.004237

This is a FIXED constant bound, not growing with p. It says:
D'/A' is between 0.9958 and 1.0042.

### 2.4 The Ramare bound (alternative)

The K_BOUND_PROOF.md cites "Lee-Leong 2024, refining Ramare 2013" for
|M(p)|/p <= 0.013/log(p) for p >= 1,078,853.

**Verification:** The Lee-Leong paper (arXiv:2208.06141, 2024) does establish
improved explicit bounds on M(x). However, the specific claim
"|M(x)|/x <= 0.013/log(x) for x >= 1,078,853" needs careful checking.

The K_BOUND_PROOF.md Section 6.1 states:
- For e^{45.123} <= x <= e^{1772.504}: |M(x)| <= 0.013x/log(x) - 0.118x/log^2(x)
- For 1,078,853 <= x <= e^{45.123}: |M(x)| <= x/4345

The claim that |M(x)|/x <= 0.013/log(x) for ALL x >= 1,078,853 then requires:
- For x >= e^{45.123}: directly from the first bound
- For 1,078,853 <= x <= e^{45.123}: 1/4345 <= 0.013/log(1,078,853)
  = 0.013/13.89 = 0.000936. But 1/4345 = 0.000230. So 0.000230 < 0.000936.
  CHECK: YES, this holds.

**The Ramare-type bound is CORRECTLY stated in the document.**

But note: El Marraki's own bound gives a WEAKER asymptotic (fixed 1/2360)
but kicks in at a LOWER threshold (617,973 vs 1,078,853).

---

## 3. Verification of C/A >= 0.59/log(p) -- THE FATAL PROBLEM

### 3.1 What is CLAIMED

The K_BOUND_PROOF.md states (line 20):
"Combined with C/A >= 0.59/log p (empirical, supported by proved C' >= 0.035 p^2)"

And later (lines 649-655):
"Empirical: min C/A over M(p) <= -3 primes up to 100K is approximately 0.59/log(p)."

### 3.2 What is PROVED

From CA_LOWER_BOUND_RIGOROUS.md, the clean proved result is (Theorem 9.1):

**(a) Unconditional:** C/A >= 1/(65.1 * log^2(p)) for all primes p >= 101.

**(b) Hybrid (computational C_W):** C/A >= 1/(46.2 * log(p)) for 101 <= p <= 100001
     (using C_W(N) <= 0.71, verified for N <= 100,000).

**(c) Small primes:** C/A >= 0.12 for p in [11, 100].

### 3.3 The gap between proved and empirical

| p       | Proved C/A (unconditional)      | Proved C/A (hybrid) | Empirical C/A |
|---------|---------------------------------|---------------------|---------------|
| 1,000   | 1/(65.1 * 47.7) = 0.000322     | 1/(46.2 * 6.91) = 0.00313 | ~0.085 |
| 10,000  | 1/(65.1 * 84.8) = 0.000181     | 1/(46.2 * 9.21) = 0.00235 | ~0.064 |
| 100,000 | 1/(65.1 * 136.1) = 0.000113    | 1/(46.2 * 11.5) = 0.00188 | ~0.051 |
| 618,000 | 1/(65.1 * 168.6) = 0.0000911   | N/A (beyond comp range) | ~0.044 |
| 1.08M   | 1/(65.1 * 185.7) = 0.0000828   | N/A | ~0.041 |

**The proved bound is 500-600x weaker than empirical.** The CA_LOWER_BOUND_RIGOROUS.md
document itself notes (Section 6): "the bound is 42x too conservative" and traces
the sources of conservatism.

### 3.4 Why the bypass argument 0.13 < 0.59 COLLAPSES

The closure argument in K_BOUND_PROOF.md (Section 6.3) is:

    |1 - D'/A'| <= 0.13/log(p) < 0.59/log(p) <= C/A

But replacing the empirical 0.59/log(p) with the proved 1/(65.1 * log^2(p)):

For p >= 1,078,853, we need:
    0.13/log(p) < 1/(65.1 * log^2(p))
    0.13 * 65.1 * log(p) < 1
    8.46 * log(p) < 1
    log(p) < 0.118
    p < 1.13

This is IMPOSSIBLE for any prime p >= 2. The proved C/A bound is too weak
by a factor of log(p) to compete with the K-bound path.

### 3.5 Option B with Dress-El Marraki: also fails

Option B claims: For p >= 617,973:
    |1 - D'/A'| <= 10/2360 = 0.00424
    C/A >= 0.59/log(p) >= 0.59/log(617973) ~ 0.044

So 0.00424 < 0.044 and the bypass works.

But with the PROVED bound: C/A >= 1/(65.1 * log^2(617973)) = 0.0000911.
We need 0.00424 < 0.0000911. This is FALSE (0.00424 >> 0.0000911).

**Option B also fails with proved constants.**

---

## 4. What IS Actually Proved for C/A?

### 4.1 The C' >= 0.035p^2 claim

The CA_LOWER_BOUND_RIGOROUS.md proves:

    delta_sq >= N^2/(62 * log N) for N >= 100

Since C' = delta_sq/n'^2 and delta_sq >= N^2/(62 log N):

    C' = delta_sq/n'^2 >= N^2/(62 * log(N) * n'^2)

With n' = n + N and n ~ 0.3 N^2, we get n' ~ 0.3 N^2 and n'^2 ~ 0.09 N^4.

    C' >= N^2 / (62 * log(N) * 0.09 * N^4) = 1/(5.58 * N^2 * log(N))

This gives C' ~ 1/(N^2 log N), NOT ~ 0.035 p^2.

**WAIT.** C' here means delta_sq (NOT delta_sq/n'^2). The document's
"C' >= 0.035 p^2" probably refers to delta_sq itself, not the normalized C.

From the proved delta_sq >= N^2/(62 log N) with N = p-1:

    delta_sq >= (p-1)^2 / (62 * log(p-1))

At p = 10000: delta_sq >= 9999^2 / (62 * 9.21) = 99,980,001 / 571 ~ 175,096.

The claim "C' >= 0.035 p^2" would mean delta_sq >= 0.035 * 10^8 = 3,500,000.
But our proved bound gives only 175,096. So 0.035 p^2 is MUCH stronger than
what's proved.

**Checking:** 0.035 p^2 means delta_sq >= 0.035 * p^2. From the proved bound:
delta_sq >= p^2/(62 log p). At p = 10000: p^2/(62*9.21) = 175,096.
And 0.035 * p^2 = 3,500,000.

The ratio: proved / claimed = 1/(62 * 9.21) / 0.035 = 0.00175 / 0.035 = 0.05.

**The proved delta_sq bound is 20x weaker than "0.035 p^2" at p = 10,000.**

For the bound delta_sq >= 0.035 p^2 to hold, we'd need 1/(62 log p) >= 0.035,
i.e., log(p) <= 1/(62 * 0.035) = 0.46, i.e., p <= 1.58. IMPOSSIBLE.

**CONCLUSION: "C' >= 0.035 p^2" is FALSE as a proved bound.** It may be
empirically true for small p (where the minimum deficit bound is very
conservative), but analytically the proved bound is delta_sq >= p^2/(62 log p),
which is weaker by a factor of 62*0.035*log(p) = 2.17*log(p).

### 4.2 Computing C/A from the proved delta_sq

From the definition:
    C/A = (delta_sq * n^2) / (old_D_sq * (n'^2 - n^2))

Using:
- delta_sq >= N^2/(62 log N)
- old_D_sq <= C_W * n^2/N (with C_W <= log N unconditionally)
- n'^2 - n^2 <= 3nN
- n <= 0.35 N^2

    C/A >= [N^2/(62 log N) * n^2] / [log(N) * n^2/N * 3nN]
         = N^2 / (62 * log(N) * 3 * log(N) * n)
         = N^2 / (186 * log^2(N) * n)
         >= N^2 / (186 * log^2(N) * 0.35 * N^2)
         = 1 / (65.1 * log^2(N))

This confirms the CA_LOWER_BOUND_RIGOROUS.md result.

---

## 5. What Would Close GAP 2?

### 5.1 The crossover requirement

We need C/A > |1 - D/A| for all sufficiently large primes with M(p) <= -3.

**If K <= 10 were proved** and using Dress-El Marraki:

    |1 - D/A| <= 10/(2360) = 0.00424 for p >= 617,973

We need C/A > 0.00424.

With the proved C/A >= 1/(65.1 * log^2(p)):
    1/(65.1 * log^2(p)) > 0.00424
    log^2(p) < 1/(65.1 * 0.00424) = 3.623
    log(p) < 1.904
    p < 6.71

IMPOSSIBLE.

### 5.2 What C/A improvement is needed?

To close with K = 10 and Dress-El Marraki, we need:
    C/A >= 0.005 (just above 0.00424) for p >= 617,973

The proved bound gives C/A ~ 0.00009 at p ~ 618K.

**We need a 55x improvement in C/A.** This is substantial.

### 5.3 Paths to improve C/A

**(a) Prove C_W <= constant (instead of C_W <= log N):**

This changes C/A from 1/(65.1 * log^2(p)) to 1/(65.1 * C_W * log(p)).

With C_W <= 0.71 (empirical up to N = 100K):
    C/A >= 1/(46.2 * log(p))

At p = 618K: 1/(46.2 * 13.33) = 0.00162. Still below 0.00424.

With C_W <= 0.71 and K=10 + Dress-El Marraki, the crossover requires:
    1/(46.2 * log(p)) > 10/2360
    log(p) < 2360/(46.2 * 10) = 5.11
    p < e^5.11 = 165

Crossover at p ~ 165. But this bound only applies for 101 <= p <= 100,001!
And for p > 100,001, we'd need C_W <= constant proved analytically.

**(b) Improve delta_sq by including composite denominators:**

The current proof only uses PRIME denominators in GOOD set. Composite
denominators b contribute D_b(p mod b) >= 0 (by rearrangement). Including
them roughly doubles delta_sq (estimated 2x gain in CA_LOWER_BOUND_RIGOROUS.md).

This would give C/A >= 1/(32.6 * log^2(p)). Still insufficient.

**(c) Tighten the minimum deficit:**

Current: D_q(r) >= q(q^2-1)/24 (the r=2 value).
The average D_q(r) is much larger. But the minimum is what matters for the
worst case.

Lemma 3.2 (min deficit = D_q(2)) is only proved for q <= 997
computationally, plus a Dedekind sum argument that isn't fully rigorous.
Making this rigorous doesn't help with the constant gap.

**(d) The nuclear option: prove C_W <= C/sqrt(log N) or better:**

If C_W(N) <= C for an absolute constant C, and we ALSO include composite
denominators (2x gain), we'd get:

    C/A >= 1/(32.6 * C * log(p))

For this to beat 10/2360 = 0.00424:
    log(p) < 2360/(32.6 * 10 * C) = 7.24/C

With C = 1: p < e^7.24 ~ 1394.
With C = 0.71: p < e^10.2 ~ 27,000.

So proving C_W <= 0.71 AND including composites AND proving K <= 10
would give a crossover around p ~ 27,000, which IS within computational
range (100K). But this requires THREE new proofs.

### 5.4 The Walfisz path (from CA_RATIO_PROOF.md)

The Walfisz bound gives |M(p)|/p <= exp(-c * sqrt(log p)) (ineffective c).
Combined with C/A >= 1/(65.1 * log^2 p):

For large enough p: 1/(65.1 * log^2(p)) > K * exp(-c * sqrt(log p))
since 1/log^2(p) decays polynomially while exp(-c*sqrt(log p)) decays
super-polynomially.

This DOES give closure for p >= P_0(c), but P_0 is INEFFECTIVE because
the Walfisz constant c is ineffective.

**The Walfisz path gives an existence result, not a computable P_0.**

---

## 6. Honest Assessment: What Do We Actually Have?

### 6.1 Rigorously proved (no gaps)

1. C > 0 for all primes p >= 5 (rearrangement inequality)
2. D >= 0 (Cauchy-Schwarz)
3. delta_sq >= N^2/(62 log N) for N >= 100
4. C/A >= 1/(65.1 * log^2(p)) for p >= 101 (unconditional)
5. C/A >= 1/(46.2 * log(p)) for 101 <= p <= 100,001 (uses C_W <= 0.71, computational)
6. C_W(N) <= 0.71 for N <= 100,000 (computed)
7. |M(x)| <= x/2360 for x >= 617,973 (Dress-El Marraki 1993)
8. |M(x)/sqrt(x)| < 0.586 for x <= 10^16 (Hurst 2018 / Lee-Leong 2024)
9. DeltaW(p) < 0 for all M(p) <= -3 primes p <= 100,000 (computed)

### 6.2 Structurally correct but not rigorous

1. |1 - D'/A'| <= K * |M(p)|/p with K ~ 6-10 (Poisson aliasing structure
   is correct, constant needs rigorous derivation)
2. C/A ~ c/log(p) with c ~ 0.05-0.12 (empirical scaling, not proved)
3. C_W(N) is bounded by a constant (strong empirical evidence, not proved)

### 6.3 What is needed for full closure

**Minimum viable proof (3 steps, all non-trivial):**

1. Prove K <= K_0 for an explicit constant (currently a sketch)
2. Prove C_W <= C_0 for an explicit constant (currently empirical)
3. Include composite denominators in delta_sq to gain factor ~2
4. Verify computationally up to the crossover P_0 determined by K_0, C_0

**Alternatively:**

- Extend computation to p ~ 10^7 (covers crossover with proved C/A >= 1/log^2)
  COMBINED with proving K bounded. This is the most feasible path.

- Or: prove the Walfisz constant effectively. This is a major open problem
  in analytic number theory.

---

## 7. The Smallest P_0

### 7.1 With all proved bounds

Using ONLY rigorously proved results:
- C/A >= 1/(65.1 * log^2(p))
- |1 - D/A| <= ... (NOT proved, so P_0 is undefined)

We CANNOT determine P_0 because the K bound is not proved.

### 7.2 With K <= 10 (assumed) + Dress-El Marraki

    Need: 1/(65.1 * log^2(p)) > 10/2360

    log^2(p) < 2360/(65.1 * 10) = 3.625

    log(p) < 1.90, p < 6.7.

P_0 does NOT EXIST (no prime satisfies this with the unconditional C/A bound).

### 7.3 With K <= 10 + C_W <= 0.71 (both assumed)

    Need: 1/(46.2 * log(p)) > 10/2360

    log(p) < 2360/462 = 5.11

    p < e^5.11 ~ 165. So P_0 ~ 165.

    Computation covers p <= 100,000, so this WOULD close if both were proved.

### 7.4 With K <= 10 + C_W <= 0.71 + composite denominators (all assumed)

    With ~2x improvement: C/A >= 1/(23.1 * log(p))

    Need: 1/(23.1 * log(p)) > 10/2360

    log(p) < 2360/231 = 10.22

    p < e^10.22 ~ 27,500. P_0 ~ 27,500.

### 7.5 Is P_0 <= 100,000?

**YES, conditionally.** If K <= 10 and C_W <= 0.71 are both proved, then:

- P_0 ~ 165 (without composites) or P_0 ~ 27,500 (conservative with composites)
- Both are well below the computational verification range of 100,000
- The proof would be FULLY CLOSED

The question is whether K <= 10 and C_W <= constant can be proved.

---

## 8. Checking the Ramare Bound Claim More Carefully

### 8.1 What Ramare (2013) actually proved

Ramare's 2013 paper "From explicit estimates for primes to explicit estimates
for the Mobius function" gives methods for converting PNT-type estimates into
Mertens bounds. The specific bound |M(x)| <= 0.6438 * x/log(x) for all x > 1
is from El Marraki (1995).

The claim that |M(x)|/x <= 0.013/log(x) for x >= 1,078,853 appears to come
from Lee-Leong (arXiv:2208.06141). This needs to be verified against the actual
paper. The K_BOUND_PROOF.md states this comes from combining:

- |M(x)| <= 0.013x/log(x) - 0.118x/log^2(x) for e^45.123 <= x <= e^1772.504
- |M(x)| <= x/4345 for 1,078,853 <= x <= e^45.123

The second range: 1/4345 = 0.000230 while 0.013/log(1,078,853) = 0.000936.
So 0.000230 < 0.000936. The bound |M(x)|/x <= 0.013/log(x) does hold.

**But where do these specific constants come from in Lee-Leong?**

The paper arXiv:2208.06141 improves on Ramare using new zero-free region
estimates and computation of zeta zeros. The specific constants would need
to be checked against their Table 1 or similar.

**Assessment:** The Ramare/Lee-Leong bound is plausible and from a published
(peer-reviewed) source. The specific constants should be verified but are
likely correct.

---

## 9. Summary: Status of Each Component

| Component | Status | Notes |
|-----------|--------|-------|
| K <= 10 | UNPROVED (sketch + empirical K <= 6.16 for p <= 499) | Structure correct, constant needs work |
| Dress-El Marraki |M(x)| <= x/2360 for x >= 617,973 | PROVED (published 1993) | Verified reference |
| Lee-Leong |M(x)|/x <= 0.013/log(x) for x >= 1,078,853 | PUBLISHED (2024) | Constants need verification against paper |
| C/A >= 0.59/log(p) | EMPIRICAL ONLY | Proved bound is 1/(65.1 * log^2(p)) -- factor of ~40x weaker |
| C_W(N) <= 0.71 for N <= 100K | COMPUTED | Rigorous within floating-point limits |
| C_W(N) <= constant (all N) | UNPROVED | Strong empirical support, analytical path identified |
| delta_sq >= N^2/(62 log N) | PROVED | For N >= 100, unconditional |
| D' + C' > A' for p <= 100K, M(p) <= -3 | COMPUTED | 2729 primes verified |

---

## 10. Recommended Path Forward

### Path 1: Extend computation (most feasible, least mathematical effort)

Extend the computational verification of DeltaW(p) < 0 to p = 10^7.
This covers the crossover for the proved C/A >= 1/(65.1 * log^2(p)) combined
with the Walfisz-type bound on |1-D/A| (which goes to 0 faster than 1/log^2).

**Problem:** The Walfisz constant is ineffective, so we can't determine
the exact crossover. We'd need to verify K <= constant empirically to
very large p.

**Feasibility:** O(p) per prime, ~10^6 primes to check. Total ~ 10^13 ops.
Hours of computation. FEASIBLE.

### Path 2: Prove C_W <= constant (substantial but identified path)

Use Lee-Leong |M(x)| <= 0.586*sqrt(x) in the Ramanujan sum expansion for
the Farey L^2 discrepancy. The outline in CA_LOWER_BOUND_RIGOROUS.md
Section 8 suggests this is achievable with "careful bookkeeping."

This gives C/A >= c/(constant * log(p)), which with Dress-El Marraki gives
crossover at modest p.

### Path 3: Make K bound rigorous (hardest mathematical step)

The Poisson summation approach in Section 9-10 of K_BOUND_PROOF.md has the
right structure. Making it rigorous requires:
- Explicit treatment of the piecewise-quadratic Fourier coefficients
- Careful handling of the n >> p regime where standard quadrature fails
- Explicit Weil/Kloosterman bounds for the off-diagonal terms

This is the bottleneck for the entire closure.

### Recommended priority order: 1 > 2 > 3

---

## 11. Final Verdict

**The GAP 2 closure via K bound + Dress-El Marraki is NOT complete.**

Three components are missing:
1. K <= constant (analytical, currently a sketch)
2. C/A >= c/log(p) instead of c/log^2(p) (needs C_W <= constant)
3. Computational extension to cover the gap between proved P_0 and 100K

If (1) and (2) are proved, then P_0 ~ 165 and existing computation closes
the proof. If only (1) is proved, then P_0 depends on the Walfisz constant
(ineffective). If only (2) is proved, then DeltaW control is still missing.

The most honest statement: **"GAP 2 closure is structurally identified but
requires completing two non-trivial analytical steps: proving K <= constant
and proving C_W <= constant."**

Neither step requires fundamentally new ideas -- the mathematical frameworks
(Poisson summation for K, Lee-Leong + Ramanujan sums for C_W) are identified
-- but both require careful technical work that has not yet been done.
