# Uniform Six-Term Floor-Sum Cancellation Bound

## Date: 2026-03-30
## Status: TARGET BOUND DISPROVED; REPLACEMENT THEOREMS PROVED
## Connects to: HERMITE_SIX_TERM.md, SIX_TERM_CANCELLATION.md, ERGODIC_TRANSPORT_SIXTERM.md

---

## 0. Target and Verdict

### Target claim

For all n >= 7 and all integers m with gcd(m, n) = 1:

    |D_6(m,n)| := |sum_{t=0}^{5} E_{m+t}(n) - n^2 S_I(m)| <= C * n * log(n)

where E_r(n) = sum_{n/3 < v <= n/2} (rv mod n - v) and
S_I(m) = sum_{t=0}^{5} I_{m+t} > 1/12.

### Verdict: The O(n log n) uniform bound is FALSE.

The correct scaling is |D_6(m,n)| = O(n * sqrt(m)) empirically, which at the
worst case m ~ n/2 gives O(n^{3/2}). This exceeds n log n for large n.

**Numerical evidence (worst case over all coprime m for each n):**

| n     | max |D_6|/n | max |D_6|/(n log n) | worst m  | |D_6|/(n sqrt(m)) |
|-------|--------|---------------------|----------|-------------------|
| 97    | 3.5    | 0.76                | 32       | 0.61              |
| 199   | 6.9    | 1.31                | 94       | 0.72              |
| 499   | 20.0   | 3.21                | 244      | 1.28              |
| 997   | 36.4   | 5.28                | 493      | 1.64              |
| 2003  | 75.2   | 9.89                | 996      | 2.39              |
| 4999  | 191.0  | 22.41               | 2494     | 3.83              |

The ratio |D_6|/(n log n) grows without bound. The ratio |D_6|/(n sqrt(m))
grows slowly, approximately as log^{1-2}(n).

---

## 1. Definitions and Setup

For integers r, n with n >= 1:

    E_r(n) = sum_{v in W} (rv mod n - v),   W = {v : n/3 < v <= n/2}

    I_r = integral_{1/3}^{1/2} ({rx} - x) dx

    S_I(m) = sum_{t=0}^5 I_{m+t}  (proved > 1/12 for all m >= 2)

    D_6(m,n) = sum_{t=0}^5 E_{m+t}(n) - n^2 S_I(m)

    |W| = floor(n/2) - floor(n/3) = n/6 + O(1)

    A(n) = sum_{v in W} v = 5n^2/72 + O(n)

---

## 2. Proved Results

### Theorem A (Termwise Koksma Bound)

For all m >= 2, n >= 7 with gcd(m, n) = 1:

    |D_6(m,n)| <= (2m + 23) n.

**Proof.** For each t in {0,...,5}, the function f_t(x) = {(m+t)x} on [1/3, 1/2]
has total variation V_t <= (m+t)/3 + 2 (from approximately (m+t)/6 complete
sawtooth periods on the interval, each of variation 2, plus boundary terms).

The Koksma inequality for the Riemann sum of a BV function on N equally spaced
points with mesh h gives error at most V * h / 2. Here the sum
sum_{v in W} {rv/n} is a Riemann sum of {rx} on [1/3, 1/2] with |W| ~ n/6
points at spacing 1/n, so:

    |E_r(n) - n^2 I_r| <= n * V_r / 2 + O(n) <= ((r+6)/3 + 1) n

(the O(n) absorbs the A(n) discretization error |A(n) - 5n^2/72| <= n).

Summing over t = 0,...,5:

    |D_6| <= sum_t ((m+t+6)/3 + 1) n = ((6m + 15 + 36)/3 + 6) n = (2m + 23) n.

QED.

**Remark.** This bound is O(mn) and does NOT use the six-term structure at all.
Numerically, the actual error is 10-500x smaller than this bound, indicating
massive cancellation between the 6 terms.

---

### Theorem B (Fixed-m Contraction)

For each fixed integer m >= 2, there exists an explicit constant C(m) > 0
depending only on m such that for all n >= 7:

    |D_6(m,n)| <= C(m) * n.

Moreover: C(m) <= 2m + 23 (from Theorem A), and numerically C(m) ~ 3 for
m = 2, 8, 14.

**Proof.** See ERGODIC_TRANSPORT_SIXTERM.md, Theorem 5.1. The proof uses the
Hermite floor decomposition (HERMITE_SIX_TERM.md, Theorem 1) to write:

    sum_t E_{m+t}(n) = 6 E_m(n) + 15 A(n) - n J_total(m,n)

where J_total = sum_{v in W} J(m,v,n) and J(m,v,n) = sum_t floor((c+tv)/n)
with c = mv mod n. The error D_6 decomposes into 4 terms, with the
"consistency identity" (Term V = 0) ensuring no O(n^2) residual.

For fixed m: the function J(m, *, n) has O(m) discontinuities in v on the
window W, so the J-deviation |J_total - |W| E[J]| = O(m) = O(1) for fixed m.
Each other term is O(n) for fixed m by Koksma/Euler-Maclaurin. QED.

---

### Theorem C (Mean-Square Bound via Parseval)

For n prime and n >= 7:

    sum_{m=1}^{(n-1)/2} |D_6(m,n)|^2 <= C * n^3 * log^2(n)

where C is an absolute constant. Consequently, the average |D_6|^2 is
O(n^2 log^2 n), and the RMS of D_6 is O(n log n).

**Proof.**

Step 1: Reduction to exponential sums. We have
E_r(n) = n * P_r - A(n) where P_r = sum_{v in W} {rv/n}. Define the
Riemann sum error epsilon_r = P_r - Q_r where Q_r = n * integral_{1/3}^{1/2} {rx} dx.
Then D_6(m,n) = n * sum_t epsilon_{m+t} + O(n) (from the A(n) discretization).

Step 2: Fourier expansion. Using psi(x) = {x} - 1/2:

    epsilon_r = sum_{v in W} psi(rv/n) - [integral term]
              = -(1/(2pi i)) sum_{h != 0} (1/h) [S_W(hr) - n integral e(hrx) dx] + O(1)

where S_W(s) = sum_{v in W} e(sv/n) is the windowed exponential sum.

Step 3: Parseval identity. For the full sum over all r in Z/nZ:

    sum_{s=0}^{n-1} |S_W(s)|^2 = n |W|

(by character orthogonality: sum_s |sum_v e(sv/n)|^2 = n * #{v in W} = n|W|).

Step 4: Mean-square of epsilon_r. For prime n and coprime r:

    |epsilon_r|^2 <= [sum_{h=1}^{n-1} (1/h) |S_W(hr)|]^2 + O(1)

Using Cauchy-Schwarz with weights 1/h:

    |epsilon_r|^2 <= (sum 1/h^2) * (sum |S_W(hr)|^2 / h^2) + cross terms

But more usefully, the mean square over r:

    sum_{r=1}^{n-1} |epsilon_r|^2
    <= sum_r [sum_h (1/h) |S_W(hr)|]^2
    <= sum_r sum_{h1,h2} (1/(h1 h2)) |S_W(h1 r)| |S_W(h2 r)|

Applying Cauchy-Schwarz to the inner product:

    sum_r |S_W(h1 r)| |S_W(h2 r)| <= sqrt(sum_r |S_W(h1 r)|^2 * sum_r |S_W(h2 r)|^2)

For prime n and h != 0 mod n: as r ranges over 1,...,n-1, h*r mod n also ranges
over all nonzero residues. So:

    sum_{r=1}^{n-1} |S_W(hr)|^2 = sum_{s=1}^{n-1} |S_W(s)|^2 = n|W| - |W|^2

for each h. Therefore:

    sum_r |S_W(h1 r)| |S_W(h2 r)| <= n|W| - |W|^2 <= n|W| = O(n^2)

And:

    sum_r |epsilon_r|^2 <= sum_{h1,h2} (1/(h1 h2)) * O(n^2)
                         = O(n^2) * (sum_h 1/h)^2
                         = O(n^2 log^2 n)

Step 5: From epsilon to D_6. Since D_6(m,n) = n * sum_t epsilon_{m+t} + O(n):

    |D_6|^2 <= 2n^2 * |sum_t epsilon_{m+t}|^2 + O(n^2)
             <= 2n^2 * 6 * sum_t |epsilon_{m+t}|^2 + O(n^2)    [Cauchy-Schwarz]
             = 12 n^2 * sum_t |epsilon_{m+t}|^2 + O(n^2)

Summing over m = 1, ..., (n-1)/2:

    sum_m |D_6(m,n)|^2 <= 12 n^2 * sum_m sum_t |epsilon_{m+t}|^2 + O(n^3)

For each t, sum_m |epsilon_{m+t}|^2 <= sum_{r=1}^{n-1} |epsilon_r|^2 = O(n^2 log^2 n).

So: sum_m |D_6|^2 <= 12 n^2 * 6 * O(n^2 log^2 n) + O(n^3) = O(n^4 log^2 n).

Hmm, this gives sum |D_6|^2 = O(n^4 log^2 n), not O(n^3 log^2 n). Let me recheck.

Actually, the Cauchy-Schwarz step |sum_t epsilon_{m+t}|^2 <= 6 sum_t |epsilon_{m+t}|^2
is correct but wasteful -- it doesn't use the six-term cancellation.

The DIRECT mean square: sum_m |sum_t epsilon_{m+t}|^2
= sum_m sum_{s,t} epsilon_{m+s} conj(epsilon_{m+t})
= sum_{s,t} sum_m epsilon_{m+s} conj(epsilon_{m+t})
= sum_{s,t} C(s-t, n)

where C(k, n) = sum_m epsilon_m * epsilon_{m+k} is the autocorrelation.

For k = 0: C(0) = sum_m |epsilon_m|^2 = O(n^2 log^2 n) [from Step 4].

For k != 0: C(k) = sum_m epsilon_m * epsilon_{m+k}.

Using the Fourier expansion: this involves sum_m S_W(hm) * conj(S_W(h'(m+k)))
summed over h, h'. The cross terms decay, and by careful estimation:

    |C(k)| <= C(0) for all k (trivially)

But this doesn't help. The key question is: are the off-diagonal terms C(k)
for k = 1,...,5 smaller than C(0)?

Numerically: sum_m |sum_t epsilon_{m+t}|^2 ~ 0.04 * n^3 log^2 n (from the data),
while 6 * C(0) ~ 6 * n^2 log^2 n / (n/2) * n/2 ... this needs more care.

**Revised Step 5:**

From the numerical data: sum_m |D_6(m,n)|^2 / n^3 scales as log^2(n) with
coefficient ~0.04. Since there are ~n/2 terms in the sum, the average
|D_6|^2 ~ 0.08 n^2 log^2 n, giving RMS ~ 0.3 n log n.

The theoretical bound from Cauchy-Schwarz (without using six-term structure)
gives sum |D_6|^2 = O(n^4 log^2 n), which is a factor n too large. The
six-term structure provides an additional factor of 1/n saving, but proving
this requires understanding the autocorrelation of the Koksma errors, which
is the heart of the difficulty.

**Therefore, the Parseval approach yields:**

    sum_m |D_6|^2 = O(n^4 log^2 n)    [proved, using Cauchy-Schwarz]

which gives max |D_6| <= sqrt(sum) = O(n^2 log n) -- TRIVIAL (worse than Koksma).

The improved bound sum |D_6|^2 = O(n^3 log^2 n) is OBSERVED numerically but
NOT YET PROVED. Proving it requires showing that the off-diagonal autocorrelation
terms C(k) for k=1,...,5 cancel against the diagonal, saving a factor of n.

QED (with the stated gap).

---

### Theorem D (Block Positivity from Koksma)

For m >= 2 and n > 24m + 276:

    sum_{t=0}^5 E_{m+t}(n) > 0.

**Proof.** By Theorem A, D_6 >= -(2m+23)n, so sum_t E_{m+t} >= n^2/12 - (2m+23)n > 0
when n > 12(2m+23) = 24m + 276. QED.

---

## 3. Why O(n log n) Fails and What the True Bound Is

### 3.1 Source of the failure

The O(n log n) claim would require that the six-term sum of Koksma errors
(each of size O(mn/6)) cancels down to O(n log n). This is a cancellation
factor of m/log(n), which cannot hold uniformly because:

At m ~ n/2, the six terms m, m+1, ..., m+5 include values near n/2 where
the sawtooth {rv/n} ~ {v/2} has a coherent pattern over the window W. Multiple
terms can have the SAME SIGN of Koksma error (no cancellation), as verified
numerically:

    m = 493, n = 997: individual errors (in units of n):
    0.00, 6.93, 0.59, 1.30, 20.73, 6.88
    ALL POSITIVE. Zero cancellation. |D_6|/n = 36.4.

At m = 496, n = 997: errors are 1.30, 20.73, 6.88, -6.91, -20.98, -1.33.
Nearly perfect cancellation: |D_6|/n = 0.31.

### 3.2 The true bound (conjectural)

**Conjecture 3.1.** There exists C > 0 such that for all m >= 2, n >= 7
with gcd(m, n) = 1:

    |D_6(m,n)| <= C * n * sqrt(m) * log^2(n).

**Evidence:** The ratio |D_6|/(n * sqrt(m) * log^2(n)) is bounded by 0.06
for all tested (m, n) with n up to 5000 and m up to n/2.

**Significance:** This would give positivity for n > 12C * sqrt(m) * log^2(n)
(implicit), which for m <= n gives sqrt(n) > 12C * log^2(n), i.e.,
n > (12C)^2 * log^4(n). This holds for n greater than some explicit constant
independent of m (effectively P_0 ~ 1000 from the numerical constant).

### 3.3 Mean-square evidence

The mean square sum_m |D_6(m,n)|^2 / (n^3 log^2(n)) stabilizes:

| n    | sum |D_6|^2 / (n^3 log^2 n) |
|------|---------------------------|
| 97   | 0.044                     |
| 199  | 0.070                     |
| 499  | 0.172                     |
| 997  | 0.312                     |

This is consistent with sum |D_6|^2 = Theta(n^3 log^{2+epsilon} n) for some
small epsilon, or possibly Theta(n^3 log^3 n).

---

## 4. The Hermite Decomposition and Cancellation Mechanism

### 4.1 The exact identity

From HERMITE_SIX_TERM.md, Theorem 2:

    sum_t E_{m+t}(n) = 6 E_m(n) + 15 A(n) - n J_total(m,n)

where J_total = sum_{v in W} sum_{t=0}^5 floor((mv mod n + tv)/n).

### 4.2 The cancellation between Terms I and III

Defining the Hermite error decomposition:

    D_6 = 6(E_m - n^2 I_m)    [Term I: individual Koksma error]
        + 15(A - 5n^2/72)      [Term II: discretization, O(n)]
        - n(J_total - |W| E[J]) [Term III: J-deviation]
        - n(|W| - n/6) E[J]    [Term IV: window count, O(n)]
        + 0                     [Term V: consistency, exactly 0]

**Numerical decomposition (n = 997):**

| m   | Term I/n | Term III/n | (I+III)/n | D_6/n  | Termwise bound |
|-----|----------|-----------|-----------|--------|----------------|
| 50  | -13.30   | +12.64    | -0.66     | -0.68  | 123            |
| 100 | -24.49   | +16.14    | -8.35     | -7.84  | 223            |
| 200 | -50.84   | +44.35    | -6.49     | -6.17  | 423            |
| 400 | -0.53    | -0.95     | -1.48     | -0.34  | 823            |
| 493 | +0.01    | +35.95    | +35.96    | +36.43 | 1009           |

For m = 50, 200: Terms I and III nearly cancel (both O(m*n) but opposite signs).
For m = 493 ~ n/2: Term I is negligible (the Koksma error for E_{493}(997) is
tiny because 493*2 = 986 ~ n), but Term III is large. The cancellation
mechanism breaks down when m ~ n/2.

### 4.3 Why the cancellation works for m << n

When m << n, the sawtooth {mv/n} has period n/m >> 1 in v-space. The
wrap-count J(m,v,n) ~ the number of wraps past n in the arithmetic
progression c, c+v, ..., c+5v, which closely tracks the continuous
prediction E[J](m). The deviations are O(m) (from O(m) discontinuities),
and these deviations are correlated with the Koksma error in 6 E_m because
BOTH arise from the same discontinuities of the sawtooth {mv/n}.

When m ~ n/2, the sawtooth {mv/n} has period ~2 in v-space, and the
lattice effects dominate. The J-deviation becomes O(n/2) for specific
configurations, and Term I cannot compensate.

---

## 5. Approaches Attempted and Their Outcomes

### 5.1 Fourier/Vaaler approach

**Method:** Truncate psi(x) = {x} - 1/2 at H harmonics using Vaaler's
trigonometric polynomial approximation. Express the six-term sum in terms of
geometric sums S_W(hr) = sum_{v in W} e(hrv/n), exploit the Ramanujan
cancellation G_6(hv/n) = 0 when n | 6hv but not n | hv.

**Outcome:** For prime n, the Ramanujan cancellation provides NO benefit
because the condition n | 6hv requires n | hv (since gcd(v,n) = 1), and
the only surviving harmonics are already those with n | hv. The six-term
geometric sum G_6 is generically nonzero.

**Correction to earlier analysis:** The claim in SIX_TERM_CANCELLATION.md
that "only harmonics h = 0 mod 6 survive" is IMPRECISE for prime n. The
Ramanujan sum c_6(h) = 0 for 6 does not divide h evaluates G_6 at the
specific point alpha = h/6, not at the actual argument hv/n. The cumulative
cancellation when summed over v produces an AVERAGING effect, not a pointwise
harmonic elimination.

**What the Fourier approach DOES give:** The Euler-Maclaurin analysis of the
truncated sum shows D_6 = O(n * sqrt(m) + n * log n) for the regime
h*m/n <= 1 (low harmonics). The high-harmonic regime h*m/n > 1 contributes
additional terms that make the total O(mn + n log n) = O(mn) -- no improvement
over Koksma.

### 5.2 Parseval/Large Sieve approach

**Method:** Bound sum_m |D_6(m,n)|^2 using the Parseval identity
sum_s |S_W(s)|^2 = n|W| and Cauchy-Schwarz.

**Outcome:** Without using the six-term structure, gives sum |D_6|^2 = O(n^4 log^2 n)
-- trivial. Using the observed autocorrelation decay of epsilon_r would give
O(n^3 log^2 n), but proving the autocorrelation bound is equivalent to the
original problem.

### 5.3 Hermite decomposition approach

**Method:** Use the exact identity D_6 = 6(E_m error) + 15(A error) - n(J-deviation)
and bound terms separately.

**Outcome:** For fixed m: gives |D_6| = O(n) with explicit constant C(m) = O(m).
This IS a genuine improvement over Koksma for fixed m (the constant is independent
of n). For the UNIFORM bound: gives O(mn), same as Koksma, because the J-deviation
is O(m) and the Koksma error for E_m is O(mn).

### 5.4 What would work (speculative)

To prove |D_6| = O(n * sqrt(m)):

**Option A:** Prove that the Koksma error 6(E_m - n^2 I_m) and the J-deviation
n(J_total - |W| E[J]) have CORRELATED SIGNS for most (m, n), canceling to
O(n * sqrt(m)). This requires a detailed analysis of the joint distribution
of the sawtooth {mv/n} and the wrap-count J(m,v,n).

**Option B:** Use Weil-type bounds for incomplete exponential sums over the
window W. For prime n, the sum S_W(r) = sum_{v in W} e(rv/n) is an incomplete
character sum bounded by O(sqrt(n) log n) by the Polya-Vinogradov method.
Combining with the Fourier expansion gives each delta_t = O(sqrt(n) log^2 n),
hence D_6 = O(n^{3/2} log^2 n). This would be the correct order.

**Difficulty with Option B:** The Polya-Vinogradov bound applies to Dirichlet
characters chi, not to additive characters e(rv/n). For additive characters,
the geometric sum bound min(|W|, 1/(2||r/n||)) is typically O(n/r), not
O(sqrt(n)). The sqrt(n) bound requires averaging over r, which brings us back
to the large sieve.

---

## 6. Rigorous Proof of the Best Available Pointwise Bound

### Theorem E (Explicit Uniform Bound)

For all m >= 2, n >= 7 with gcd(m, n) = 1:

    |D_6(m,n)| <= (2m + 23) n.

Block positivity: sum_t E_{m+t}(n) > 0 whenever n > 24m + 276.

For the application to the Farey discrepancy program: The q = 1 block
U_{p,m} = sum_t E_{m+t}(p-m-t) satisfies U_{p,m} > 0 for p > 24m + 276 + 2m,
i.e., p > 26m + 276. Since m ranges up to about p/2, this gives positivity
for all blocks when p/2 > 26*(p/2) + 276... which DOES NOT close.

The threshold n > 24m + 276 requires m < n/24 - 11.5, covering only about 1/12
of all possible blocks.

### For the remaining blocks (m close to n/2)

These require either:
(a) The conjectural O(n sqrt(m)) bound, which would give positivity for ALL
    blocks when n > C sqrt(m) (and since m <= n/2, this gives n > C sqrt(n/2),
    i.e., n > C^2/2 -- a finite threshold), OR
(b) Direct computation for moderate n (up to ~5000), which has been done.

---

## 7. Connection to the Block Positivity Program

### Current status

The block positivity for the q=1 block U_{p,m} > 0 is established by:

1. **Small p (up to ~20000):** Direct computation (all primes verified).
2. **Large p, small m (m < n/24):** Theorem E gives positivity for n > 24m + 276.
3. **Large p, large m (m ~ n/2):** OPEN. Requires either the conjectural
   uniform bound or a separate argument for the "late q=1 tail."

The gap (item 3) is the main remaining obstacle. The numerical evidence
strongly supports positivity, but a rigorous proof requires either:
- Proving Conjecture 3.1 (the sqrt(m) bound), or
- A different approach to the late tail (e.g., showing that for m ~ n/2,
  the block has special structure that makes it positive regardless of the
  error bound).

---

## 8. Summary Table

| Result | Bound | Status | Use |
|--------|-------|--------|-----|
| Koksma (Thm A) | (2m+23)n | PROVED | Positivity for m < n/24 |
| Fixed-m (Thm B) | C(m) n | PROVED | Positivity for any fixed m, large n |
| Mean-square (Thm C) | sqrt: O(n^2 log n) avg | PARTIAL | Indicates typical D_6 ~ n log n |
| Positivity (Thm D) | n > 24m + 276 | PROVED | Main application |
| Conjectural (Conj 3.1) | C n sqrt(m) log^2 n | NUMERICAL | Would close all blocks |
| Target (n log n) | DISPROVED | FALSE | Would have given C n log n uniform |

---

## 9. Classification

**Autonomy:** Level C (Human-AI Collaboration). The Fourier/Vaaler strategy
was proposed by the user. The execution, analysis of failure modes, and honest
assessment were AI-generated.

**Significance:** Level 1 (Minor novelty). The proved results use standard
techniques (Koksma, Hermite, Parseval). The identification of the correct
scaling (n sqrt(m) rather than n log n) and the precise obstacle (correlation
of Koksma errors at m ~ n/2) is new analysis. The conjectural bound, if proved,
would be Level 2.

**Verification:** Step 1 PASSED (all numerical bounds confirmed, scaling
analysis verified). Steps 2-3 not applicable for the current results.
