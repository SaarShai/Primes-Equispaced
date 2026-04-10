# Effective Aliasing Bound via Hurst's Mertens Computation

## Date: 2026-03-29
## Goal: Close GAP 2 in the Sign Theorem proof by making the Poisson aliasing bound effective

---

## 0. The Gap to Close

**What we need:** D'/A' >= 1 - epsilon(p) where epsilon(p) < C'/A'.

Since C'/A' >= pi^2 / (432 log^2 p) (proved), it suffices to show:

    |1 - D'/A'| < pi^2 / (432 log^2 p)

Equivalently, from the sampling ratio rho(p) = sum E(k/p)^2 / [(p-1)/n * sum D^2]:

    |rho(p) - 2| < 2 * pi^2 / (432 log^2 p)

**Key tool:** Hurst (2018, Math. Comp.) verified |M(x)/sqrt(x)| < 0.586 for ALL x <= 10^16.

---

## 1. The Quadratic Form Representation

### 1.1 Setup

Let p be prime, N = p - 1. Define:
- c_m = M(floor(N/m)) for m = 1, ..., N (the Mertens weights)
- E(k/p) = (p-k)/p - (1/p) * S(k) where S(k) = sum_{m=1}^{N} c_m * (mk mod p)

Then (from SAMPLING_RATIO_PROOF.md, Section 2):

    p^2 * sum_{k=1}^{p-1} E(k/p)^2 = sum_{r=1}^{p-1} T(r) * C(r)    ... (QF)

where:
- T(r) = sum_{j=1}^{p-1} j * (rj mod p) (multiplicative correlation)
- C(r) = sum_{m: m,mr' in {1,...,N}} c_m * c_{mr'} where r' = r^{-1} mod p
  (more precisely: C(r) = sum over pairs (m,m') with m'm^{-1} = r mod p)

### 1.2 Known values of T(r)

- T(1) = p(p-1)(2p-1)/6
- Average T(r) for r != 1: T_off = p(p-1)(3p-1)/12
- T(r) for r != 1 fluctuates around T_off = (3/4 + O(1/p)) * T(1)

**Key fact:** For r != 1, T(r) = (p^2 - 1)/12 + (correction involving Dedekind sums).
More precisely, T(r) = p(p-1)(3p-1)/12 + O(p^2) for most r.

### 1.3 Splitting the quadratic form

    sum T(r)*C(r) = T(1)*C(1) + sum_{r!=1} T(r)*C(r)

The diagonal: T(1)*C(1) = [p(p-1)(2p-1)/6] * [sum_{m=1}^N c_m^2]

The off-diagonal: sum_{r!=1} T(r)*C(r)

For the sampling ratio rho(p) = 2 + error, we need the off-diagonal to approximately
equal the diagonal. We will instead bound the ERROR directly.

---

## 2. The Mertens Weight Norms

### 2.1 Definition

    C(1) = sum_{m=1}^N c_m^2 = sum_{m=1}^N M(floor(N/m))^2

### 2.2 Bounding C(1) using Hurst

For p <= 10^8 (so N = p-1 <= 10^8 - 1 <= 10^8 < 10^16):

    |c_m| = |M(floor(N/m))| <= 0.586 * sqrt(floor(N/m)) <= 0.586 * sqrt(N/m)

Therefore:

    C(1) = sum_{m=1}^N c_m^2 <= 0.586^2 * sum_{m=1}^N N/m = 0.3434 * N * H_N

where H_N = sum_{m=1}^N 1/m = ln(N) + gamma + O(1/N).

**Bound: C(1) <= 0.3434 * N * (ln N + 1) for all N <= 10^16.**

### 2.3 Lower bound on C(1)

From the Franel-Landau identity:
    sum D(f)^2 = (n/3) * sum_{m=1}^N c_m^2 + lower order

This gives C(1) = sum c_m^2 ~ 3 * sum D^2 / n.

Empirically, C(1) ~ N * C_W where C_W is the Franel-Landau constant (empirically 0.3-0.7).

---

## 3. Bounding the Off-Diagonal: Key Estimate

### 3.1 The sum of C(r) for r != 1

From Proposition 2(b) in SAMPLING_RATIO_PROOF:

    sum_{r=1}^{p-1} C(r) = (sum_{m=1}^N c_m)^2

Now sum_{m=1}^N c_m = sum_{m=1}^N M(floor(N/m)). This is related to N(F_N) - 1 = n - 1.

Actually: sum_{m=1}^N M(floor(N/m)) = sum_{m=1}^N sum_{d | m, d <= N/m} mu(d) ... this is
a well-known identity. We have:

    sum_{m=1}^N M(floor(N/m)) = sum_{m=1}^N sum_{k=1}^{floor(N/m)} mu(k)
                               = sum_{j=1}^N sum_{k | j, k <= N/j} mu(k)

Actually this sum = sum_{j=1}^N 1 = N (no, this is wrong).

Let me reconsider. We have c_m = M(floor(N/m)), and from the Farey sequence identity:

    n - 1 = sum_{m=1}^N phi(m) = sum_{m=1}^N m * sum_{d | m} mu(d)/d

This is NOT the same as sum c_m. In fact:

    sum_{m=1}^N c_m = sum_{m=1}^N M(floor(N/m))

By hyperbola method: = sum_{m=1}^N sum_{k=1}^{floor(N/m)} mu(k) = sum_{j=1}^N d(j)
where the sum counts pairs (m,k) with mk <= N. Wait, no:

    sum_{m=1}^N M(floor(N/m)) = sum_{m=1}^N sum_{k=1}^{floor(N/m)} mu(k)
    = sum_{k=1}^N mu(k) * sum_{m=1}^{floor(N/k)} 1
    = sum_{k=1}^N mu(k) * floor(N/k)

This is EXACTLY n(F_N) - 1 = n - 1 (by the standard identity for Farey cardinality).

So: **(sum c_m)^2 = (n-1)^2 ~ n^2 ~ 9N^4/pi^4.**

Therefore: sum_{r!=1} C(r) = (n-1)^2 - C(1) ~ n^2 - N*C_W.

Average C(r) for r != 1: ~ ((n-1)^2 - C(1)) / (p-2).

### 3.2 The key difficulty

The off-diagonal sum S_off = sum_{r!=1} T(r)*C(r) involves correlations between
T and C that are hard to bound pointwise.

However, we can use a different strategy: bound the ERROR in rho directly.

---

## 4. Direct Approach via the Quadratic Form Error

### 4.1 The exact identity

From the quadratic form:

    p^2 * sum E(k/p)^2 = sum_r T(r) * C(r)

The "target" (for rho = 2) would be:

    2 * p^2 * (p-1)/n * sum D^2 = 2p(p-1) * sum D^2 / n

From the Franel-Landau connection: sum D^2 / n ~ (n/3) * C(1) / n = C(1)/3.
So the target ~ 2p(p-1) * C(1)/3 = 2p(p-1)*C(1)/3.

Meanwhile: T(1)*C(1) = p(p-1)(2p-1)*C(1)/6 ~ p^3*C(1)/3 for large p.

And: sum_r T(r)*C(r) = T(1)*C(1) + S_off.

For rho = 2, we need sum_r T(r)*C(r) ~ 2p^2*(p-1)*C(1)/3.

Since T(1)*C(1) ~ p^3*C(1)/3, we need S_off ~ p^3*C(1)/3 (the off-diagonal
contributes equally to the diagonal, yielding factor 2).

### 4.2 Error analysis via Cauchy-Schwarz

Define the error: epsilon(p) = |rho(p) - 2|.

We want to bound epsilon from ABOVE.

**Approach: Express rho in terms of T and C, and bound the deviation.**

From the exact formula (Section 4.1):

    rho(p) = [sum_r T(r)*C(r)] / [p^2 * (p-1)/n * sum D^2]

**Problem:** This requires knowing sum D^2 in terms of C(1), which introduces
the SAME Franel-Landau identity we're trying to make effective.

### 4.3 Alternative: Direct Poisson approach with explicit error

Instead of the quadratic form, use the Poisson summation directly:

    sum_{k=1}^{p-1} E(k/p)^2 = p * integral_0^1 E(x)^2 dx + p * A(p) - 1

where A(p) = sum_{j != 0} hat_g(jp).

The key claim is |A(p) - integral E^2| = o(integral E^2). We need this EFFECTIVELY.

---

## 5. The Effective Poisson Bound (Main Result)

### 5.1 Fourier coefficients of E(x)

E(x) has Fourier expansion:

    E(x) = sum_{h != 0} hat_E(h) * e(hx)

where for h != 0:

    hat_E(h) = (1/(2*pi*i*h)) * sigma_c(h)

and sigma_c(h) = sum_{m | h, 1 <= m <= N} c_m * m = sum_{m | h, m <= N} m * M(floor(N/m)).

### 5.2 Bounding |sigma_c(h)|

For h with all divisors m of h satisfying m <= N (i.e., h <= N^2, which always holds
for h in our range):

    |sigma_c(h)| <= sum_{m | h, m <= N} m * |M(floor(N/m))|

Using Hurst's bound for N <= 10^8:

    |sigma_c(h)| <= 0.586 * sum_{m | h, m <= N} m * sqrt(N/m)
                  = 0.586 * sqrt(N) * sum_{m | h, m <= N} sqrt(m)
                  <= 0.586 * sqrt(N) * sigma_{1/2}(h)

where sigma_{1/2}(h) = sum_{d | h} d^{1/2}.

### 5.3 Bounding |hat_E(h)|^2

    |hat_E(h)|^2 <= (1/(4*pi^2*h^2)) * |sigma_c(h)|^2
                  <= (0.586^2 * N) / (4*pi^2*h^2) * sigma_{1/2}(h)^2

### 5.4 Bounding integral E^2 = sum_h |hat_E(h)|^2

    integral E^2 = sum_{h != 0} |hat_E(h)|^2

**Lower bound (from Franel-Landau):**

    integral E^2 ~ sum D^2 / n ~ C_W * (p-1) where C_W >= 0.3 empirically

**Upper bound (from Hurst):**

    integral E^2 <= (0.586^2 * N) / (4*pi^2) * sum_{h != 0} sigma_{1/2}(h)^2 / h^2

The sum sum_{h=1}^{infty} sigma_{1/2}(h)^2 / h^2 converges (by comparing with
sum d(h)^2/h^2 via Ramanujan's result). In fact:

    sum_{h=1}^{infty} sigma_{1/2}(h)^2 / h^2 = prod_p (1 + (sqrt(p)/(p^2-1))^2 + ...)

This is a finite Euler product. However, this approach gives a bound on the TOTAL
integral E^2, not on the ERROR of the aliasing.

### 5.5 The aliasing error

The aliasing sum:

    A(p) = sum_{j >= 1} [hat_g(jp) + hat_g(-jp)]

where hat_g(m) = sum_h hat_E(h) * conj(hat_E(h-m)).

The error we want to bound:

    |A(p) - integral E^2| = |sum_{j != 0} hat_g(jp) - hat_g(0)|

---

## 6. A BETTER APPROACH: Quadratic Form with Explicit T(r) Bounds

### 6.1 The T(r) function for general r

For r in {1, ..., p-1}, the multiplicative correlation T(r) has an exact closed form.
Define r* = r^{-1} mod p. Then:

    T(r) = sum_{j=1}^{p-1} j * (rj mod p)

For r = 1: T(1) = p(p-1)(2p-1)/6
For r = p-1 (i.e., r = -1): T(p-1) = sum j*(p - j) = p*p(p-1)/2 - p(p-1)(2p-1)/6
    = p(p-1)(p+1)/6

**For general r != 1:** T(r) = p(p^2-1)/12 + (p/2)*s(r,p) where s(r,p) is the
Dedekind sum. Actually, the precise formula is:

    T(r) = (p^3 - p)/12 + (p/2) * something

Let me compute more carefully. We have:

    T(r) = sum_{j=1}^{p-1} j * (rj mod p) = sum_j j * rj - p * sum_j j * floor(rj/p)

The first sum: sum_j j * rj = r * sum j^2 = r * p(p-1)(2p-1)/6 (mod p, but we're in Z)

Wait, this is not modular. Let me reconsider.

For j in {1,...,p-1} and r in {1,...,p-1}: rj mod p runs through {1,...,p-1} as j does
(since p is prime). So:

    sum_j (rj mod p) = sum_{s=1}^{p-1} s = p(p-1)/2
    sum_j (rj mod p)^2 = sum s^2 = p(p-1)(2p-1)/6

But T(r) = sum_j j * (rj mod p), which DOES depend on the permutation j -> rj mod p.

Using the Kloosterman-type identity:

    T(r) + T(r^{-1}) = p * sum_j j = p^2(p-1)/2
    (since j*(rj mod p) + (rj mod p)*j = ... no, this is wrong)

Actually: substitute j' = rj mod p, then sum_{j'} (r^{-1}j' mod p) * j' = T(r^{-1}).
And j = r^{-1}j' mod p. So T(r) = sum_j j*(rj mod p) and T(r^{-1}) = sum_{j'} j'*(r^{-1}j' mod p).

These are NOT simply related.

### 6.2 Variance of T(r)

What we CAN compute is the variance of T(r) over r:

    sum_{r=1}^{p-1} T(r)^2 = sum_{r,j,k} j*k * (rj mod p) * (rk mod p)

For j = k: sum_r (rj mod p)^2 = sum s^2 = p(p-1)(2p-1)/6 for each j.
    Contribution: sum_j j^2 * p(p-1)(2p-1)/6 = [p(p-1)(2p-1)/6]^2

For j != k: sum_r (rj mod p)(rk mod p). Set s = rj mod p, then rk mod p = (k/j)*s mod p
    = (kj^{-1} mod p)*s mod p. Let q = kj^{-1} mod p (where q != 1 since j != k).

    sum_{s=1}^{p-1} s * (qs mod p) = T(q)

So the j != k contribution is:
    sum_{j!=k} j*k * T(kj^{-1} mod p) = sum_q sum_{j: kj^{-1}=q} j*k * T(q)

For fixed q != 1: the pairs (j,k) with kj^{-1} = q mod p are k = qj, j in {1,...,p-1}.
    sum_j j * (qj) = q * sum j^2 = q * p(p-1)(2p-1)/6.

So: sum_{j!=k} j*k*T(kj^{-1}) = sum_{q!=1} q * p(p-1)(2p-1)/6 * T(q)
    = (p(p-1)(2p-1)/6) * sum_{q!=1} q*T(q)
    = (p(p-1)(2p-1)/6) * [sum_{q=1}^{p-1} q*T(q) - T(1)]

Now sum_q q*T(q) = sum_q sum_j j*q*(rj mod p) where r=q
    = sum_{r,j} r*j*(rj mod p). Substitute s = rj mod p, r = sj^{-1}:
    = sum_{j,s} (sj^{-1} mod p)*j*s = sum_{j,s} s^2 * (j^{-1} mod p) * j

Hmm, this is getting complicated. Let me take a cleaner approach.

---

## 7. CLEAN APPROACH: Direct Riemann Sum Error via Hurst

### 7.1 The key quantity

We need: sum_{k=1}^{p-1} E(k/p)^2 ~ 2(p-1)/n * sum D^2.

The LHS is a Riemann sum of E(x)^2 at the arithmetic points k/p.
The RHS is 2 * (p-1) * integral E^2 (approximately).

So we need: (1/(p-1)) * sum_{k=1}^{p-1} E(k/p)^2 ~ 2 * integral_0^1 E(x)^2 dx.

The Riemann sum approximation: (1/(p-1)) * sum_{k=1}^{p-1} f(k/p) ~ integral_0^1 f(x) dx.

For f = E^2: the EXTRA factor of 2 comes from the aliasing. This is the non-trivial part.

### 7.2 Explicit decomposition

E(x) is a step function with jumps at each Farey fraction. Between consecutive
Farey fractions f_j and f_{j+1}, E(x) is affine: E(x) = (j+1) - n*x.

On the interval (f_j, f_{j+1}), the Farey gap is h_j = 1/(b_j * b_{j+1}).

E(x)^2 = ((j+1) - nx)^2 = D(f_j)^2 - 2n*D(f_j)*(x - f_j) + n^2*(x - f_j)^2
(using E(f_j^+) = j + 1 - n*f_j = D(f_j) + 1, and the linear decrease).

Wait, more carefully: E(x) for x in (f_j, f_{j+1}):
    E(x) = N_{F_N}(x) - n*x = j + 1 - n*x (since N_{F_N}(x) = j+1 for x in (f_j, f_{j+1}))

So E(f_j^+) = j + 1 - n*f_j. And D(f_j) = j - n*f_j (rank is j in 0-based indexing).
Therefore E(f_j^+) = D(f_j) + 1.

At x = f_{j+1}^-: E(f_{j+1}^-) = j + 1 - n*f_{j+1} = D(f_{j+1}).

So E drops from D(f_j) + 1 to D(f_{j+1}) over the interval, linearly.

### 7.3 The p-rational sampling

For k/p with f_j < k/p < f_{j+1}: E(k/p) = j + 1 - n*k/p.

How many k/p points fall in each Farey interval? The interval (f_j, f_{j+1}) has
length h_j = 1/(b_j * b_{j+1}). The number of k/p in this interval is approximately
p * h_j = p/(b_j * b_{j+1}).

For b_j, b_{j+1} <= N = p-1 < p, we have h_j >= 1/N^2, so each interval contains
at least p/N^2 ~ 1/p points -- possibly ZERO points for small intervals!

This is the issue: many Farey intervals contain 0 or 1 sample points.

### 7.4 The correct decomposition for the Sign Theorem

Rather than trying to prove rho(p) = 2 + small, we should work with what the
Sign Theorem actually needs.

**Recall the Sign Theorem condition (from PROOF_CLOSURE.md):**

For primes with M(p) <= -3, we need:

    C' + D' > A' + 1

where:
- A' = old_D_sq * (n'^2 - n^2) / n^2 (the dilution)
- C' = delta_sq = sum delta(a/b)^2 (the shift energy)
- D' = sum_{k=1}^{p-1} D_new(k/p)^2 (the new-fraction discrepancy energy)

And D_new(k/p) = rank_{F_p}(k/p) - n'*(k/p).

**The ratio D'/A'** is what we need close to 1.

D' = sum_{k=1}^{p-1} D_new(k/p)^2.

Now D_new(k/p) relates to E(k/p) via:
    D_new(k/p) = rank_{F_p}(k/p) - n'*(k/p)

where rank_{F_p}(k/p) = (number of f in F_N with f <= k/p) + (number of j/p <= k/p, j != 0)
    = N_{F_N}(k/p) + k
    = E(k/p) + n*(k/p) + k

So D_new(k/p) = E(k/p) + n*(k/p) + k - n'*(k/p)
              = E(k/p) + (n - n')*(k/p) + k
              = E(k/p) - (p-1)*(k/p) + k      (since n' = n + p - 1)
              = E(k/p) + k - k*(p-1)/p
              = E(k/p) + k/p

Therefore:

    D' = sum_{k=1}^{p-1} (E(k/p) + k/p)^2
       = sum E(k/p)^2 + 2 sum (k/p)*E(k/p) + sum (k/p)^2

The last sum: sum_{k=1}^{p-1} (k/p)^2 = (p-1)(2p-1)/(6p^2) ~ p/3.

The cross term: 2 sum (k/p)*E(k/p). Using E(k/p) = (p-k)/p - S(k)/p:
    sum (k/p)*E(k/p) = sum (k/p)*(p-k)/p - sum (k/p)*S(k)/p

The first part: sum k(p-k)/p^2 = (1/p^2) * [p*p(p-1)/2 - p(p-1)(2p-1)/6]
    = (p-1)/2 - (p-1)(2p-1)/(6p) = (p-1)(p+1)/(6p) ~ p/6.

So D' involves sum E(k/p)^2 plus correction terms of order p.

### 7.5 The dilution A'

A' = old_D_sq * (n'^2 - n^2) / n^2

With n' = n + (p-1): n'^2 - n^2 = (2n + p - 1)(p - 1) ~ 2n(p-1).

So A' ~ 2(p-1) * old_D_sq / n.

And old_D_sq / n = (n/3) * C(1) / n = C(1)/3 (approximately, from Franel-Landau).

So A' ~ 2(p-1) * C(1)/3.

---

## 8. The Effective Bound Strategy (REVISED)

### 8.1 What we actually need

The condition C' + D' > A' + 1 can be rewritten as:

    D' > A' + 1 - C'

Since C' >= 0.035 * p^2 (from PROOF_CLOSURE Step 3) and A' ~ 2(p-1)*old_D_sq/n,
with old_D_sq ~ n * C_W * (p-1) and n ~ 3(p-1)^2/pi^2:

    A' ~ 2(p-1)^2 * C_W * 3(p-1)/(pi^2 * 3) ~ ...

Let me be more concrete. We need D' > A'(1 - C'/A') + 1, i.e.,
D'/A' > 1 - C'/A' + 1/A'.

Since C'/A' ~ pi^2/(432*C_W*log(p)) >= 0.023/log^2(p) (proved) and 1/A' is tiny
(A' grows as p^2), we need:

    **D'/A' > 1 - c/log^2(p) for an effective constant c.**

### 8.2 The relationship between D'/A' and the sampling ratio

From Section 7.4:

    D' = sum E(k/p)^2 + 2*sum(k/p)*E(k/p) + (p-1)(2p-1)/(6p^2)

Let:
- R_1 = sum E(k/p)^2
- R_2 = 2*sum(k/p)*E(k/p)
- R_3 = (p-1)(2p-1)/(6p^2)

And A' = old_D_sq * (n'^2 - n^2)/n^2.

The sampling ratio rho = R_1 / [(p-1)/n * old_D_sq].

So R_1 = rho * (p-1) * old_D_sq / n.

And A' = old_D_sq * (n'^2 - n^2)/n^2 ~ 2(p-1) * old_D_sq / n.

Therefore: **R_1/A' = rho/2**.

We also need bounds on R_2/A' and R_3/A'.

R_3/A' ~ [(p-1)(2p-1)/(6p^2)] / [2(p-1)*old_D_sq/n]
        = n*(2p-1)/(12p^2*old_D_sq)
        ~ [3p^2/pi^2] * 2p / (12p^2 * n*C_W*p/3)
        This is tiny: O(1/(p*C_W)).

R_2/A': From the computation, sum(k/p)*E(k/p) ~ (p-1)(p+1)/(6p) + (cross with S(k)).
The S(k) cross term can be bounded:

    |sum (k/p)*S(k)/p| = |(1/p^2) * sum_m c_m * sum_k k*(mk mod p)|
    = |(1/p^2) * sum_m c_m * T(m)|

Using T(m) ~ p^3/4 and sum |c_m| <= 0.586 * sum sqrt(N/m) ~ 0.586 * 2*sqrt(N) * sqrt(N) = 1.172*N:

    |R_2 cross|/A' is bounded but this needs care.

### 8.3 The critical simplification

Actually, the key insight from the existing proof framework is simpler:

**From the exact D/A computation (ANALYTICAL_PROOF_PATH_C.md Section 5):**

    |1 - D'/A'| <= K * |M(p)| / p

with empirical K ~ 6.37. This is NOT proved analytically yet.

**THIS is what we want to make effective using Hurst.**

If we can PROVE K <= K_0 (some explicit constant), then for p <= 10^8:

    |1 - D'/A'| <= K_0 * 0.586 * sqrt(p) / p = K_0 * 0.586 / sqrt(p)

And we need this < C'/A' >= pi^2/(432*log^2(p)):

    K_0 * 0.586 / sqrt(p) < pi^2 / (432 * log^2(p))
    sqrt(p) / log^2(p) > K_0 * 0.586 * 432 / pi^2 = K_0 * 25.64

For K_0 = 6.37: sqrt(p)/log^2(p) > 163.3.

| p | sqrt(p)/log^2(p) |
|---|-------------------|
| 10^6 | 5.24 |
| 10^8 | 29.5 |
| 10^10 | 186.6 |
| 10^11 | 491.3 |

**Crossover: p ~ 9 * 10^9 with K_0 = 6.37.**

---

## 9. Proving the Constant K: The Bridge Identity Approach

### 9.1 The bridge identity

The key connection between D'/A' and M(p) comes from the Franel representation:

    E(k/p) = 1 + sum_{m=1}^N c_m * floor(mk/p) - n*k/p

For the sum of E(k/p)^2 at k/p points, the dominant dependence on M(p) enters through
the Mertens weight c_1 = M(N) = M(p-1).

### 9.2 Deriving K analytically

The deviation |rho - 2| can be expressed as:

    |rho - 2| = |sum_r T(r)*C(r)/(p^2*(p-1)*old_D_sq/n) - 2|

Expanding: this involves the autocorrelation C(r) of the Mertens weights.

The key bound: using C(1) = sum c_m^2 and the constraint sum_r C(r) = (n-1)^2:

    |sum_{r!=1} T(r)*C(r) - T_off * sum_{r!=1} C(r)|
    <= max_{r!=1} |T(r) - T_off| * sum_{r!=1} |C(r)|

Now: max_{r!=1} |T(r) - T_off| <= p^2 * max|s(r,p)|/2 where s(r,p) is the Dedekind sum.
The Dedekind sum satisfies |s(r,p)| <= (1/8)*(p/3 + 1/p), so max|T(r) - T_off| = O(p^3).

And: sum_{r!=1} |C(r)| <= sqrt((p-2) * sum_{r!=1} C(r)^2) by Cauchy-Schwarz.

The sum sum_{r!=1} C(r)^2 is bounded by... the 4th moment of the c_m weights.

**This approach gets very technical. Let me instead try a more computational path.**

---

## 10. Computational Verification Path

### 10.1 Strategy

Given the difficulty of proving K analytically, the most practical path is:

1. **For p <= P_comp (computational range):** Verify D' + C' > A' + 1 directly.
   Already done for all M(p) <= -3 primes to p = 100,000.

2. **For P_comp < p <= 10^8:** Use Hurst's bound to get an effective rho bound.

3. **For p > 10^8:** Use El Marraki (effective) or Ramare (stronger for large p).

### 10.2 What Hurst gives for the quadratic form

For p <= 10^8 (N <= 10^8 < 10^16, well within Hurst's range):

**All Mertens values involved are bounded:** |c_m| = |M(floor(N/m))| <= 0.586 * sqrt(N/m).

The quadratic form sum E(k/p)^2 = (1/p^2) * sum_r T(r)*C(r) involves:

C(r) = sum_{m: 1<=m,mr'<=N} c_m * c_{m*r' mod p}

For the diagonal: C(1) = sum c_m^2 <= 0.586^2 * N * H_N ~ 0.343 * N * ln(N).

For the total: sum_r |C(r)| <= (p-1)*C(1) (trivially, since |C(r)| <= C(1)).

But this gives a trivial bound. We need the CANCELLATION in sum_r T(r)*C(r).

### 10.3 The correct split

Write:

    sum_r T(r)*C(r) = T_off * sum_r C(r) + sum_r (T(r) - T_off)*C(r) + (T(1)-T_off)*C(1)

Wait, let me split differently:

    sum_r T(r)*C(r) = T_off * (n-1)^2 + (T(1) - T_off)*C(1) + sum_{r!=1} (T(r) - T_off)*C(r)

The first term: T_off * (n-1)^2 = [p(p-1)(3p-1)/12] * (n-1)^2 / (p-2)
    Wait, T_off = average of T(r) for r!=1, not T(r) for all r.

Let me define T_avg = [sum_r T(r)] / (p-1) = [p(p-1)/2]^2 / (p-1) = p^2(p-1)/4.

Then:

    sum_r T(r)*C(r) = T_avg * sum_r C(r) + sum_r (T(r) - T_avg)*C(r)
                    = T_avg * (n-1)^2 + sum_r (T(r) - T_avg)*C(r)

The "fluctuation" term: sum_r (T(r) - T_avg)*C(r).

If C(r) were constant (= (n-1)^2/(p-1) for all r), the fluctuation would vanish.
The fluctuation measures the correlation between T and C.

### 10.4 Bounding the fluctuation

By Cauchy-Schwarz:

    |sum_r (T(r) - T_avg)*C(r)| <= sqrt(sum_r (T(r) - T_avg)^2) * sqrt(sum_r C(r)^2)

**Variance of T:**

    Var(T) = (1/(p-1)) sum_r T(r)^2 - T_avg^2

The sum sum_r T(r)^2 can be computed:

    sum_r T(r)^2 = sum_r [sum_j j*(rj mod p)]^2
    = sum_r sum_{j,k} jk*(rj mod p)*(rk mod p)
    = sum_{j,k} jk * sum_r (rj mod p)(rk mod p)

For j = k: sum_r (rj mod p)^2 = sum_{s=1}^{p-1} s^2 = p(p-1)(2p-1)/6.
    Contribution: sum_j j^2 * p(p-1)(2p-1)/6 = [p(p-1)(2p-1)/6]^2

For j != k: sum_r (rj mod p)*(rk mod p) = T(kj^{-1} mod p).
    Contribution: sum_{j!=k} jk*T(kj^{-1} mod p)

Substituting q = kj^{-1} mod p: for fixed q != 1, the pairs are (j, qj mod p) for
j = 1,...,p-1. So k = qj mod p and jk = j*(qj mod p).
    sum_{j=1}^{p-1} j*(qj mod p) = T(q).

So sum_{j!=k} jk*T(kj^{-1}) = sum_{q!=1} T(q)^2.

Therefore:

    sum_r T(r)^2 = T(1)^2 + sum_{q!=1} T(q)^2

Hmm, this is circular. Let me instead note:

    sum_r T(r)^2 = T(1)^2 + sum_{q=2}^{p-1} T(q)^2

So: (p-1) Var(T) = sum T(r)^2 - (p-1)*T_avg^2 = sum (T(r) - T_avg)^2.

We know T(1) ~ p^3/3 and T_avg ~ p^3/4, so T(1) - T_avg ~ p^3/12.
For most r != 1, T(r) fluctuates around T_avg with std dev ~ p^2
(from Dedekind sum fluctuations).

**Key bound:** std(T) = O(p^2). This is because:

    T(r) - T_avg = (correction from rearrangement of {1,...,p-1} by multiplication by r)

The fluctuation is bounded by the largest Dedekind sum: O(p*log(p)) per term, giving
O(p^2*sqrt(p*log(p))) total... this is getting imprecise.

### 10.5 An explicit bound on Var(T)

Actually, we can compute Var(T) exactly:

    sum_{r=1}^{p-1} T(r)^2 = sum_{j,k} jk * [j=k ? p(p-1)(2p-1)/6 : T(kj^{-1})]

For j=k: [p(p-1)(2p-1)/6] * sum j^2 = [p(p-1)(2p-1)/6]^2.

For j!=k: sum_{j!=k} jk T(kj^{-1}). For each fixed q = kj^{-1} (with q != 1):
    the pairs (j,k) with k = qj give contribution sum_j j*(qj mod p) * T(q) = ...

    Actually wait. sum_{j!=k} jk * T(kj^{-1}) = sum_{q!=1} [sum_j j*(qj mod p)] * [sum_l l*(ql mod p)]

No. For fixed q != 1: the contribution is sum_{j=1}^{p-1} j*(qj mod p) = T(q).
    And the sum over pairs is sum_{q!=1} T(q) * T(q) = sum_{q!=1} T(q)^2.

Hmm wait, for j != k with k/j = q: the j,k contribution is jk * T(q). But jk = j*(qj mod p).
    So the q-contribution is T(q) * T(q)? No.

    For fixed q: sum_{j=1}^{p-1} j * (qj mod p) = T(q), and the (j,k) sum for this q is:
    sum_j j*(qj mod p) * T(q)? No, the T(kj^{-1}) in the original sum is already evaluated
    at kj^{-1} = q. So:

    sum_{j: k=qj} jk * T(q) = sum_j j*(qj mod p) * T(q) = T(q)^2.

    Wait, that's not right either. Let me restart this computation.

For j != k:
    sum_{r} (rj mod p)(rk mod p) = ?
    Set s = rj mod p. Then rk mod p = (k/j)s mod p = (kj^{-1} mod p)*s mod p.
    Let q = kj^{-1} mod p. Then sum_r = sum_{s=1}^{p-1} s*(qs mod p) = T(q).

So: sum_r T(r)^2 = sum_{j,k} jk * [delta_{jk} * (p(p-1)(2p-1)/6 - T(1)) + T(kj^{-1})]
    ... this is getting confused. Let me just use the result.

**The variance of T is O(p^5).** [Since T ~ p^3 and there are p-1 terms, Var = O(p^5).]

The standard deviation of T is O(p^{5/2}).

### 10.6 Bounding the C(r) fluctuation

sum_r C(r)^2 = sum_r [sum_{m} c_m * c_{mr' mod p}]^2

This is the 4th-moment object. Using Hurst:

    sum_r C(r)^2 <= (p-1) * C(1)^2

(since |C(r)| <= C(1) always).

So sqrt(sum_r C(r)^2) <= sqrt(p) * C(1).

### 10.7 Putting it together

    |sum_r (T(r) - T_avg)*C(r)| <= sqrt(p * Var(T)) * sqrt(p) * C(1)
                                 = p * sqrt(Var(T)) * C(1)

We need: this error << T_avg * (n-1)^2.

T_avg * (n-1)^2 ~ (p^3/4) * (3p^2/pi^2)^2 = (p^3/4) * 9p^4/pi^4 ~ 9p^7/(4*pi^4).

The error: p * O(p^{5/2}) * C(1) = O(p^{7/2}) * 0.343 * N * ln(N) ~ O(p^{9/2} * ln(p)).

Ratio: O(p^{9/2} * ln(p)) / O(p^7) = O(ln(p) / p^{5/2}).

**This goes to 0!** But does it give an effective bound?

|error| / (T_avg * (n-1)^2) <= C_explicit * ln(p) / p^{5/2}

For this to be < pi^2/(432*log^2(p)) (= C'/A'), we need:

    C_explicit * ln(p) / p^{5/2} < pi^2/(432*log^2(p))
    C_explicit * log^3(p) / p^{5/2} < pi^2/432

This is satisfied for all p >= small constant (since p^{5/2} >> log^3(p)).

**BUT: the bound |C(r)| <= C(1) is too crude.** The actual C(r) for r != 1 is MUCH
smaller than C(1) due to cancellation in the Mertens weights.

---

## 11. REFINED BOUND ON sum C(r)^2

### 11.1 The 4th moment of Mertens autocorrelation

    sum_{r=1}^{p-1} C(r)^2 = sum_{r} [sum_m c_m c_{mr'}]^2
    = sum_r sum_{m,m'} c_m c_{mr'} c_{m'} c_{m'r'}
    = sum_{m,m'} c_m c_{m'} sum_r c_{mr'} c_{m'r'}

For the inner sum: sum_r c_{mr'} c_{m'r'}.

Let a = mr' mod p, b = m'r' mod p. As r ranges over 1,...,p-1, so does r' = r^{-1}.
So (a,b) = (m*r', m'*r') ranges over pairs (m*s, m'*s) for s = 1,...,p-1.

    sum_s c_{ms mod p} c_{m's mod p} = C_2(m, m')

where C_2 is a "two-point correlation" of the Mertens weight vector as shifted.

If m, m' are both <= N: the indices ms mod p and m's mod p range over all of {1,...,p-1}.
But c_j is only defined for j in {1,...,N} (it's 0 for j > N+1, approximately).

Actually wait: c_m = M(floor(N/m)) is defined for m = 1,...,N. For m > N, c_m = 0.

So: C(r) = sum_{m=1}^N c_m * c_{mr' mod p} where we need mr' mod p in {1,...,N}.

Since p > N+1, the values mr' mod p are in {1,...,p-1}, and c_j = M(floor(N/j)) for
j <= N, c_j = 0 for j > N.

So C(r) = sum_{m: m<=N AND mr' mod p <= N} c_m * c_{mr' mod p}.

For a RANDOM r, the fraction of m values in {1,...,N} whose image mr' mod p also
falls in {1,...,N} is approximately N/(p-1) ~ 1 (since N = p-1). So almost ALL
terms contribute -- the constraint mr' mod p <= N is almost always satisfied.

Actually, since N = p-1 and mr' mod p ranges in {1,...,p-1}, the constraint
mr' mod p <= N = p-1 is ALWAYS satisfied. So C(r) = sum_{m=1}^N c_m * c_{mr' mod p}
where all indices are valid (since mr' mod p is in {1,...,p-1} = {1,...,N}).

Great, so C(r) = sum_{m=1}^N c_m * c_{mr^{-1} mod p} for all r.

### 11.2 Parseval on C(r)

    sum_{r=1}^{p-1} C(r)^2 = sum_r |sum_m c_m c_{mr'}|^2

Let hat_c(chi) = sum_{m=1}^{p-1} c_m * chi(m) be the character transform of c.
(Where c_m = M(floor(N/m)) for m = 1,...,N and c_m = 0 for m = N+1,...,p-1.)

Then: C(r) = sum_m c_m * c_{mr'} = (1/(p-1)) sum_{chi} |hat_c(chi)|^2 * chi(r)

(This is the standard convolution identity for multiplicative characters.)

And: sum_r C(r)^2 = sum_r |(1/(p-1)) sum_chi |hat_c(chi)|^2 chi(r)|^2
    = (1/(p-1)) sum_chi |hat_c(chi)|^4

by Parseval.

**Key estimate:** sum_chi |hat_c(chi)|^4 <= (max_chi |hat_c(chi)|^2) * sum_chi |hat_c(chi)|^2
    = (max_chi |hat_c(chi)|^2) * (p-1) * C(1)

So: sum_r C(r)^2 <= C(1) * max_chi |hat_c(chi)|^2.

### 11.3 Bounding max_chi |hat_c(chi)|^2

For the trivial character chi_0: hat_c(chi_0) = sum c_m = n - 1 ~ 3p^2/pi^2.
So |hat_c(chi_0)|^2 ~ 9p^4/pi^4.

For non-trivial chi: hat_c(chi) = sum_{m=1}^N M(floor(N/m)) * chi(m).

This is a character sum weighted by Mertens values. By partial summation:

    hat_c(chi) = sum_{m=1}^N c_m * chi(m) = sum_{j=1}^N M(j) * [chi(floor(N/j)) terms]

More carefully, define the Dirichlet series:
    sum_{m=1}^N c_m * chi(m) = sum_{m=1}^N M(floor(N/m)) * chi(m)

Using the substitution j = floor(N/m): this decomposes into blocks where j is constant.
For j fixed, m ranges over (N/(j+1), N/j], and c_m = M(j) for all such m.

    hat_c(chi) = sum_{j=1}^N M(j) * sum_{m: floor(N/m)=j} chi(m)
               = sum_{j=1}^N M(j) * [sum_{m=floor(N/(j+1))+1}^{floor(N/j)} chi(m)]

The inner sum is a short character sum over an interval of length ~ N/j^2.

**Using the Polya-Vinogradov inequality:** |sum_{a<m<=b} chi(m)| <= sqrt(p) * log(p)/2.

Since each block has length O(N/j^2) = O(p/j^2) and there are O(sqrt(N)) distinct
values of j (by the hyperbola method), and |M(j)| <= 0.586*sqrt(j):

    |hat_c(chi)| <= sum_j |M(j)| * min(N/j^2, sqrt(p)*log(p)/2)

For j <= J (small): use the trivial bound N/j^2 for the character sum.
    sum_{j<=J} 0.586*sqrt(j) * N/j^2 ~ 0.586*N * sum 1/j^{3/2} ~ 0.586*N*zeta(3/2)
    ~ 0.586*N*2.612 ~ 1.53*N

For j > J (large): use Polya-Vinogradov.
    sum_{j>J} 0.586*sqrt(j) * sqrt(p)*log(p)/2 ~ 0.293*sqrt(p)*log(p) * sum_{j>J} sqrt(j)

The sum sum_{j>J} sqrt(j) diverges, so we need to be more careful.

Actually, for j > sqrt(N), each block has at most 1 element, so the character sum is
either 0 or chi(m) for a single m, giving |sum| <= 1.

    sum_{j>sqrt(N)} |M(j)| * 1 <= sum_{j=1}^N |M(j)| * 1_{j>sqrt(N)}

But the sum over j goes up to N, and for j > sqrt(N): |M(j)| <= 0.586*sqrt(j) <= 0.586*sqrt(N).
Number of such j: N - sqrt(N).

    Contribution: <= 0.586*sqrt(N) * N = 0.586*N^{3/2}

For j <= sqrt(N): block length ~ N/j^2 >= sqrt(N). Use:
    |sum chi(m)| <= min(N/j^2, sqrt(p)*log(p)/2)

The crossover: N/j^2 = sqrt(p)*log(p)/2 => j ~ sqrt(2N/(sqrt(p)*log(p))) ~ sqrt(2*sqrt(p)/log(p)).

For j <= j_0 = sqrt(2*sqrt(p)/log(p)): use N/j^2 bound.
    sum_{j<=j_0} 0.586*sqrt(j) * N/j^2 <= 0.586*N * sum_{j=1}^{j_0} j^{-3/2}
    ~ 0.586*N*2 = 1.172*N

For j_0 < j <= sqrt(N): use Polya-Vinogradov.
    sum 0.586*sqrt(j) * sqrt(p)*log(p)/2 <= 0.293*sqrt(p)*log(p) * sum_{j=j_0}^{sqrt(N)} sqrt(j)
    ~ 0.293*sqrt(p)*log(p) * (2/3)*N^{3/4}
    ~ 0.195*sqrt(p)*log(p)*N^{3/4}
    = 0.195*p^{1/2}*log(p)*p^{3/4} = 0.195*p^{5/4}*log(p)

Combining all three ranges:

    |hat_c(chi)| <= 1.172*N + 0.195*p^{5/4}*log(p) + 0.586*N^{3/2}

For large p, the N^{3/2} = p^{3/2} term dominates. So:

    max_chi |hat_c(chi)|^2 <= O(p^3)     (for non-trivial chi)

But for chi_0: |hat_c(chi_0)|^2 = (n-1)^2 ~ 9p^4/pi^4.

So the trivial character DOMINATES and:

    sum_r C(r)^2 <= C(1) * max(9p^4/pi^4, O(p^3)) = C(1) * 9p^4/pi^4

Therefore: sqrt(sum_r C(r)^2) <= sqrt(C(1)) * 3p^2/pi^2 ~ sqrt(0.343*N*ln(N)) * 3p^2/pi^2.

This is dominated by the trivial character contribution, which corresponds to
the MEAN of C(r) being large: average C(r) ~ (n-1)^2/(p-1) ~ 9p^3/pi^4.

**The problem:** The fluctuation of C(r) is dominated by its mean, which is large.
We already accounted for the mean in the T_avg * sum C(r) term.

### 11.4 Separating mean from fluctuation

Define: C'(r) = C(r) - bar_C where bar_C = (n-1)^2/(p-1).

Then: sum_r C'(r) = 0 and:

    sum_r T(r)*C(r) = T_avg*(n-1)^2 + sum_r (T(r) - T_avg)*C'(r) + bar_C*sum_r (T(r)-T_avg)

The last term: bar_C * 0 = 0 (since T(r) averages to T_avg).

So: sum_r T(r)*C(r) = T_avg*(n-1)^2 + sum_r (T(r)-T_avg)*C'(r)

Now: |sum_r (T(r)-T_avg)*C'(r)| <= sqrt(sum_r (T(r)-T_avg)^2) * sqrt(sum_r C'(r)^2)

**Variance of T:** We need this explicitly. From the structure of T(r):

    Var(T) = (1/(p-1))*sum(T(r) - T_avg)^2

Since T(1) ~ p^3/3 and T_avg ~ p^3/4, the contribution from r=1 alone gives:

    (T(1) - T_avg)^2 ~ (p^3/12)^2 = p^6/144

So sum(T-T_avg)^2 >= p^6/144, giving std(T) >= p^3/(12*sqrt(p)) = p^{5/2}/12.

The overall Var(T) ~ p^5 (from the p^6 contribution divided by p).

**Variance of C':**

    sum_r C'(r)^2 = sum_r C(r)^2 - (p-1)*bar_C^2
    = sum_r C(r)^2 - (n-1)^4/(p-1)

Using the character-sum bound from 11.2:

    sum_r C(r)^2 = (1/(p-1)) sum_chi |hat_c(chi)|^4

The chi_0 term: |hat_c(chi_0)|^4/(p-1) = (n-1)^4/(p-1) = (p-1)*bar_C^2.

So: sum_r C'(r)^2 = (1/(p-1)) sum_{chi != chi_0} |hat_c(chi)|^4.

For non-trivial chi, |hat_c(chi)| <= O(p^{3/2}) (from the analysis above).

And: sum_{chi != chi_0} |hat_c(chi)|^2 = (p-1)*C(1) - (n-1)^2
    ~ p*(0.343*p*ln(p)) - 9p^4/pi^4

For large p: (n-1)^2 ~ 9p^4/pi^4 dominates, so this is NEGATIVE.

Wait, that can't be right. Let me recheck.

Parseval: sum_chi |hat_c(chi)|^2 = (p-1) * sum_m c_m^2 = (p-1)*C(1).

And |hat_c(chi_0)|^2 = (sum c_m)^2 = (n-1)^2.

So: sum_{chi != chi_0} |hat_c(chi)|^2 = (p-1)*C(1) - (n-1)^2.

Now C(1) = sum c_m^2. And (n-1)^2 = (sum c_m)^2. By Cauchy-Schwarz,
(sum c_m)^2 <= N * sum c_m^2 = N*C(1). So (n-1)^2 <= N*C(1), hence:

    sum_{chi!=chi_0} |hat_c(chi)|^2 = (p-1)*C(1) - (n-1)^2 >= 0

(since p - 1 = N). Actually p - 1 = N, so (p-1)*C(1) = N*C(1) >= (n-1)^2.

In fact, (n-1)^2 ~ 9N^4/pi^4 while N*C(1) ~ N * 0.343*N*ln(N) = 0.343*N^2*ln(N).
So (n-1)^2 >> N*C(1) for N >= small constant.

**CONTRADICTION:** This means (p-1)*C(1) < (n-1)^2, which contradicts Parseval!

**Error found:** The Parseval identity is:

    sum_chi |hat_c(chi)|^2 = (p-1) * sum_{m=1}^{p-1} c_m^2

where the SUM IS OVER m = 1,...,p-1, not just 1,...,N.

Since c_m = 0 for m > N = p-1, and N = p-1, the sum is over m = 1,...,p-1.
So sum_{m=1}^{p-1} c_m^2 = sum_{m=1}^N c_m^2 = C(1). OK so Parseval gives
(p-1)*C(1).

And (n-1)^2 ~ (3N^2/pi^2)^2 = 9N^4/pi^4, while (p-1)*C(1) ~ N * N*log(N) = N^2*log(N).

So indeed 9N^4/pi^4 >> N^2*log(N), meaning (n-1)^2 >> (p-1)*C(1).

**But Cauchy-Schwarz says (sum c_m)^2 <= N * sum c_m^2!**

Let's check: sum c_m = n - 1 ~ 3N^2/pi^2. And sum c_m^2 = C(1) ~ 0.343*N*log(N).
Then N*C(1) ~ 0.343*N^2*log(N), while (sum c_m)^2 ~ 9N^4/pi^4.

For N = 100: N*C(1) ~ 0.343*10000*4.6 ~ 15778, while (sum c_m)^2 ~ 9*10^8/97 ~ 9.3*10^6.

So (sum c_m)^2 >> N*C(1). This VIOLATES Cauchy-Schwarz!

**The resolution:** The claim C(1) ~ 0.343*N*log(N) from Hurst's bound is an UPPER bound,
not the actual value. The actual C(1) might be much larger.

Let me reconsider. C(1) = sum_{m=1}^N M(floor(N/m))^2.

For m = 1: c_1 = M(N) = M(p-1). Using Hurst: |c_1| <= 0.586*sqrt(N).
For m = 2: c_2 = M(floor(N/2)). |c_2| <= 0.586*sqrt(N/2).
...
For m = k: c_k = M(floor(N/k)). Note floor(N/k) takes only O(sqrt(N)) distinct values.

By the hyperbola decomposition:

    C(1) = sum_{m=1}^N M(floor(N/m))^2 = sum_{j=1}^N M(j)^2 * |{m : floor(N/m) = j}|

The count |{m : floor(N/m) = j}| = floor(N/j) - floor(N/(j+1)).

    C(1) = sum_{j=1}^N M(j)^2 * (floor(N/j) - floor(N/(j+1)))

Using Hurst: M(j)^2 <= 0.586^2 * j = 0.3434 * j.

    C(1) <= 0.3434 * sum_j j * (floor(N/j) - floor(N/(j+1)))

By Abel summation: sum_j j*(N/j - N/(j+1)) = N*sum_j (1 - j/(j+1)) = N*sum 1/(j+1) ~ N*log(N).

So C(1) <= 0.3434 * N * log(N). This IS an upper bound.

But what is the ACTUAL size? The sum sum c_m = n - 1 ~ 3N^2/pi^2 implies:

    (sum c_m)^2 / N = (3N^2/pi^2)^2/N = 9N^3/pi^4

This must be <= C(1) by Cauchy-Schwarz. So C(1) >= 9N^3/pi^4.

But 9N^3/pi^4 >> 0.3434*N*log(N), which contradicts the Hurst bound!

**CRITICAL ERROR IDENTIFIED:** The Hurst bound gives |M(j)| <= 0.586*sqrt(j) for j <= 10^16.
But sum c_m = n - 1 requires large positive and negative cancellations. Let me recheck
whether sum c_m = n - 1 is correct.

Actually: sum_{m=1}^N c_m = sum_{m=1}^N M(floor(N/m)) = sum_{m=1}^N sum_{k=1}^{floor(N/m)} mu(k)
= sum_{j=1}^N sum_{k | j} mu(k) * ...

Wait: sum_m M(floor(N/m)) = sum_m sum_{k<=N/m} mu(k) = sum_k mu(k) * floor(N/k) = n(F_N) - 1.

Hmm, actually: n(F_N) = sum_{b=1}^N phi(b) = sum_{b=1}^N sum_{d|b} mu(d) * b/d... no.

Let me just use the basic fact: sum_{k=1}^N mu(k)*floor(N/k) = 1 (a standard identity,
since it counts the number of n <= N with n = 1, which is 1).

Wait, that's different. sum_{k=1}^N mu(k)*floor(N/k) = sum_{n=1}^N sum_{k|n} mu(k) = sum_{n=1}^N [n=1] = 1.

So sum_{m=1}^N c_m = sum_m M(floor(N/m)) which is NOT the same as sum mu(k)*floor(N/k).

Let me recompute: sum_m M(floor(N/m)) = sum_m sum_{k=1}^{floor(N/m)} mu(k).

Change order: this counts pairs (m,k) with k <= floor(N/m), i.e., km <= N (approximately).
More precisely, k <= floor(N/m) iff k*m <= N (not quite, but close for the leading term).

    = sum_{j=1}^N d(j) (approximately, where d(j) is the number of divisors of j... no)

Actually, sum_m sum_{k<=floor(N/m)} 1 = sum_{m=1}^N floor(N/m) = sum_{j=1}^N d(j) (hyperbola).

No wait: sum_{k<=floor(N/m)} mu(k) = M(floor(N/m)), and sum_m M(floor(N/m)) is just
what we're computing. Using the Mobius function, NOT the constant 1.

OK let me just accept: sum c_m = sum_m M(floor(N/m)). Numerically, for N=10:
    m=1: M(10) = -1 (mu: 1,-1,-1,0,-1,1,-1,0,0,1 => M = 1,0,-1,-1,-2,-1,-2,-2,-2,-1)
    m=2: M(5) = -2
    m=3: M(3) = -1
    m=4: M(2) = 0
    m=5: M(2) = 0
    m=6: M(1) = 1
    m=7: M(1) = 1
    m=8: M(1) = 1
    m=9: M(1) = 1
    m=10: M(1) = 1
    Sum = -1 -2 -1 +0+0+1+1+1+1+1 = 1.

And n(F_10) = 1 + phi(1)+...+phi(10) = 1+1+1+2+2+4+2+6+4+6+4 = 33. So n-1 = 32 != 1.

**So sum c_m = 1, NOT n-1!**

I was confusing two different identities. The correct identity is:

    sum_{m=1}^N M(floor(N/m)) = 1

(which is the Mobius inversion of sum_{m=1}^N 1 = N, giving M*1 = identity).

Actually: sum_{m=1}^N M(floor(N/m)) = sum_{k=1}^N mu(k)*floor(N/k) = 1 (standard identity).

Wait, that's not right either. Let me verify: sum_{k=1}^{10} mu(k)*floor(10/k):
    k=1: 1*10 = 10
    k=2: -1*5 = -5
    k=3: -1*3 = -3
    k=4: 0*2 = 0
    k=5: -1*2 = -2
    k=6: 1*1 = 1
    k=7: -1*1 = -1
    k=8: 0*1 = 0
    k=9: 0*1 = 0
    k=10: 1*1 = 1
    Sum = 10-5-3+0-2+1-1+0+0+1 = 1. Yes!

And I showed sum_m M(floor(N/m)) = sum_m sum_{k<=floor(N/m)} mu(k) which counts pairs
(m,k) with k <= floor(N/m). But this is NOT the same as mu(k)*floor(N/k).

Let me recompute: sum_{m=1}^N sum_{k=1}^{floor(N/m)} mu(k) = sum_{m=1}^N M(floor(N/m)).
For N=10: this is 1 (computed above).

And sum_{k=1}^N mu(k) * |{m : floor(N/m) >= k}| = sum_k mu(k) * floor(N/k).
These are the SAME since {m : floor(N/m) >= k} = {m : m <= N/k} has floor(N/k) elements.

So indeed sum_m M(floor(N/m)) = sum_k mu(k)*floor(N/k) = 1.

**CORRECTED:** (sum c_m)^2 = 1. NOT (n-1)^2.

This resolves the Cauchy-Schwarz contradiction!

And from Proposition 2(b) in SAMPLING_RATIO_PROOF: sum_r C(r) = (sum c_m)^2 = 1.

So: bar_C = 1/(p-1), which is TINY. The mean of C(r) for r != 1 is approximately
    (1 - C(1))/(p-2).

### 11.5 Revised Parseval

    sum_{chi} |hat_c(chi)|^2 = (p-1)*C(1)
    |hat_c(chi_0)|^2 = (sum c_m)^2 = 1

    sum_{chi!=chi_0} |hat_c(chi)|^2 = (p-1)*C(1) - 1

Now C(1) ~ 0.3434*N*log(N) (upper bound from Hurst). Actually, C(1) = sum M(floor(N/m))^2.

Empirically, C(1) grows roughly as N (not N*log(N)), with C(1)/N ~ 0.3-0.6
(consistent with C_W from the Franel-Landau connection).

### 11.6 The corrected fluctuation bound

    sum_r C'(r)^2 = sum_r (C(r) - 1/(p-1))^2 ~ sum_r C(r)^2 - 1/(p-1)

Using character sums: sum_r C(r)^2 = (1/(p-1)) sum_chi |hat_c(chi)|^4.

The chi_0 contribution: 1/(p-1).
The non-trivial: (1/(p-1)) sum_{chi!=chi_0} |hat_c(chi)|^4.

For non-trivial chi, using the bound |hat_c(chi)| <= O(N^{3/2}):

    sum_{chi!=chi_0} |hat_c(chi)|^4 <= max_{chi!=chi_0} |hat_c(chi)|^2 * sum_{chi!=chi_0} |hat_c(chi)|^2
    <= O(N^3) * (p-1)*C(1) = O(N^3) * N * O(N*logN) = O(N^5*logN)

So: sum_r C(r)^2 <= O(N^5*logN)/(p-1) + 1/(p-1) ~ O(N^4*logN).

And: sqrt(sum_r C(r)^2) ~ O(N^2*sqrt(logN)).

### 11.7 The final fluctuation estimate

    |sum_r (T(r)-T_avg)*C'(r)| <= sqrt((p-1)*Var(T)) * sqrt(sum_r C'(r)^2)

With Var(T) ~ p^5 and sum C'^2 ~ N^4*logN = p^4*logp:

    fluctuation <= sqrt(p*p^5) * sqrt(p^4*logp) = p^3 * p^2 * sqrt(logp) = p^5*sqrt(logp)

The main term: T_avg * (sum C(r)) = T_avg * 1 = p^2(p-1)/4 ~ p^3/4.

**PROBLEM:** fluctuation ~ p^5 >> main term ~ p^3. The bound is useless!

### 11.8 Why the bound fails and what to do

The Cauchy-Schwarz bound on the fluctuation is too loose because:
1. T(r) - T_avg has large contributions from specific r values (especially r=1 and r=p-1)
2. C(r) is large for r=1 (= C(1) ~ N*logN) but small for most other r

The actual mechanism is that the quadratic form sum T(r)*C(r) is dominated by:
- r = 1: T(1)*C(1) = p^3*C(1)/3
- r = p-1: T(p-1)*C(p-1) (also large because C(p-1) is large)
- A small number of other r values where C(r) is significant

The Cauchy-Schwarz bound spreads the variance over ALL r values, missing this sparsity.

---

## 12. THE CORRECT EFFECTIVE APPROACH

### 12.1 Separating the dominant terms

Instead of bounding the full fluctuation, isolate the dominant contributions:

    sum_r T(r)*C(r) = T(1)*C(1) + T(p-1)*C(p-1) + sum_{r != 1, p-1} T(r)*C(r)

**r = 1:** T(1)*C(1) = p(p-1)(2p-1)/6 * sum c_m^2.

**r = p-1:** T(p-1) = p(p-1)(p+1)/6.
    C(p-1) = sum_m c_m * c_{(-m) mod p} = sum_m c_m * c_{p-m}.
    Since c_j = M(floor(N/j)) and for m + (p-m) = p, c_{p-m} = M(floor(N/(p-m))).
    For m < p/2: floor(N/(p-m)) = floor((p-1)/(p-m)).
    For m = 1: floor((p-1)/(p-1)) = 1, so c_{p-1} = M(1) = 1.
    For m = 2: floor((p-1)/(p-2)) = 1, so c_{p-2} = M(1) = 1.
    For m < p/2: floor((p-1)/(p-m)) ~ 1 + (m-1)/(p-m) ~ 1 for m << p.

    So for most m: c_{p-m} = M(1) = 1.

    C(p-1) ~ sum_{m=1}^{N/2} c_m * 1 + sum_{m=N/2+1}^{N} c_m * c_{p-m}

    The first sum: ~ sum_{m=1}^{N/2} M(floor(N/m)) which is close to sum_{m=1}^N M(floor(N/m)) = 1
    (since the large-m terms are small).

    So C(p-1) ~ 1 (a constant, NOT growing with p).

Actually, C(p-1) = sum_m c_m * c_{p-m}. For m close to p/2, both c_m and c_{p-m}
can be large. But for m << p/2: c_{p-m} = M(1) = 1.

Numerically (from SAMPLING_RATIO_PROOF): C(p-1) is large and negative.
For p=89: C(88) = -86 vs C(1) = 117.

So C(p-1) is significant but SMALLER than C(1).

### 12.2 The remaining sum

For r not in {1, p-1}: how large is C(r)?

C(r) = sum_m c_m * c_{mr^{-1} mod p}. For "generic" r, the values mr^{-1} mod p
scramble the indices, creating cancellation in the sum (since the c_m have varying signs).

By the large sieve inequality or character sum bounds, for MOST r:

    |C(r)| <= O(sqrt(N * C(1))) = O(sqrt(N^2 * logN)) = O(N*sqrt(logN))

compared to C(1) ~ N*logN.

### 12.3 The effective ratio

The target: rho(p) * p^2 * (p-1)/n * old_D_sq = sum_r T(r)*C(r).

The "prediction" for rho = 2:
    2 * p^2 * (p-1)/n * old_D_sq ~ 2p^2 * (p-1) * C(1)/(3)
    (using old_D_sq ~ n*C(1)/3)
    = 2p^2(p-1)*C(1)/3

The actual: sum_r T(r)*C(r) = T(1)*C(1) + rest.

T(1)*C(1) = p(p-1)(2p-1)*C(1)/6 ~ p^3*C(1)/3.

For rho = 2: we need sum_r T(r)*C(r) = 2p^2(p-1)*C(1)/3 = p^3*C(1)/3 * 2(p-1)/p ~ 2p^3*C(1)/3.

So we need T(1)*C(1) + rest = 2p^3*C(1)/3, i.e., rest = 2p^3*C(1)/3 - p^3*C(1)/3 = p^3*C(1)/3.

The rest must contribute equally to the diagonal. This IS the aliasing identity.

---

## 13. CONCLUSION AND ASSESSMENT

### 13.1 Status of the Hurst effective bound approach

The attempt to use Hurst's |M(x)/sqrt(x)| < 0.586 to make the aliasing bound
effective encounters a FUNDAMENTAL OBSTACLE:

**The quadratic form sum_r T(r)*C(r) requires the off-diagonal to contribute equally
to the diagonal (both ~ p^3*C(1)/3). Bounding the off-diagonal from ABOVE using
Cauchy-Schwarz or character sum bounds gives estimates of order p^5, far exceeding
the target p^3. The bound fails by a factor of p^2.**

The reason: the off-diagonal sum is NOT small -- it equals the diagonal. A bound
must capture the EXACT cancellation pattern, not just the upper bound.

### 13.2 What WOULD work

**Option A: Extend computation to p ~ 10^7.**
The crossover condition (Section 8.3) requires sqrt(p)/log^2(p) > 163.
This is satisfied for p > 8 * 10^9. But if we can tighten K from 6.37 to ~3
(plausible from the data), then p > 4 * 10^8 suffices.
With C_W <= 0.71 (verified to 100K) and the tighter C/A bound:
P_0 could drop to 5 * 10^6.

Extending computation to p = 10^7 is FEASIBLE (estimated 2-3 hours on C code).

**Option B: Prove the effective aliasing via Ramanujan-sum expansion.**
Instead of bounding the full quadratic form, expand C(r) using Ramanujan sums:
    C(r) = sum_{q | p-1} c_q * r_q(r) (Ramanujan expansion)
where r_q(r) is the Ramanujan sum. The T(r) function has a known expansion.
The convolution then becomes a sum over q with explicit coefficients.
This is a MORE PROMISING analytical route.

**Option C: Use the Franel identity DIRECTLY.**
The Franel identity states: sum D^2 = (n/3) * sum_{m=1}^N M(floor(N/m))^2 + ...
Use this to express BOTH the numerator and denominator of D'/A' in terms of
the SAME Mertens values, then bound the ratio directly.

### 13.3 Honest assessment

The Hurst bound alone is INSUFFICIENT to close GAP 2. The bound |M(x)| < 0.586*sqrt(x)
provides pointwise control on the Mertens weights, but the aliasing identity
requires CORRELATION control (how the weights interact under multiplicative shifts),
which is a fundamentally different and harder problem.

**GAP 2 remains open.** The most practical closure path is:

1. Extend B+C computation to p = 10^7 (feasible, ~2-3 hours)
2. Prove K <= 10 analytically (the empirical bound |1-D/A| <= K*|M(p)|/p)
3. Use Hurst for the finite range p <= 10^8 with the proved K
4. Use El Marraki / Ramare for p > 10^8

Step 2 (proving K) is the actual analytical challenge.

### 13.4 Error in the original strategy

The original strategy assumed that bounding |M(j)| pointwise would suffice to
bound sum E(k/p)^2. This is WRONG because:

1. E(k/p) = linear combination of Mertens values with coefficient depending on k
2. sum E(k/p)^2 involves ALL pairwise products of Mertens values
3. The pairwise products create a quadratic form whose off-diagonal requires
   CORRELATION bounds, not just pointwise bounds
4. The correlation C(r) = sum c_m * c_{mr'} depends on the multiplicative structure
   of the indices, which Hurst's pointwise bound cannot capture

This is similar to why |M(x)| < sqrt(x) does not immediately imply bounds on
quadratic forms in M values -- the cross terms require separate analysis.

---

## 14. WHAT CAN BE SALVAGED

### 14.1 The empirical model |1 - D/A| ~ K*|M(p)|/p

From computational data (210 M(p)<=-3 primes to p=3000):
- Empirical max K = 6.37
- The model predicts |1-D/A| well across all tested primes
- K appears to be DECREASING for larger primes

If we accept K = 6.37 as a conjecture (supported by computation to 100K), then:

**For p <= 10^8:** Using Hurst, |M(p)| < 0.586*sqrt(p):
    |1 - D/A| < 6.37 * 0.586 / sqrt(p) = 3.733 / sqrt(p)

**For p <= 10^16:** Same bound applies (Hurst covers this range).

**For p > 10^16:** Using El Marraki, |M(p)| < 0.644*p/log(p):
    |1 - D/A| < 6.37 * 0.644 / log(p) = 4.102 / log(p)

Now C/A >= pi^2/(432*log^2(p)). The condition |1-D/A| < C/A requires:

**Hurst regime (p <= 10^16):**
    3.733/sqrt(p) < pi^2/(432*log^2(p))
    sqrt(p)/log^2(p) > 3.733*432/pi^2 = 163.4
    Holds for p > 8*10^9.

**El Marraki regime (p > 10^16):**
    4.102/log(p) < pi^2/(432*log^2(p))
    log(p) > 4.102*432/pi^2 = 179.6
    Holds for p > e^{179.6} ~ 10^{78}. **DOES NOT CLOSE!**

**Problem:** The El Marraki bound is too weak for the large-p regime.
We need a bound of the form |M(p)| < p/log^{1+delta}(p) to match the 1/log^2(p) of C/A.

### 14.2 Using Ramare (2013) for large p

Ramare: |M(p)| < 0.013*p/log(p) for p >= 1,078,853.
Then: |1-D/A| < 6.37*0.013/log(p) = 0.0828/log(p).

    0.0828/log(p) < pi^2/(432*log^2(p))
    log(p) > 0.0828*432/pi^2 = 3.624
    Holds for p > e^{3.624} = 37.5.

**This CLOSES for all p >= 1,078,853!** (Where Ramare applies.)

### 14.3 The combined argument (CONJECTURAL on K = 6.37)

Assuming K = 6.37:

**For p in [11, 100,000]:** Verified computationally (B+C > 0 for all M(p)<=-3).

**For p in [100,000, 1,078,853]:** Use Hurst + K = 6.37:
    |1-D/A| < 3.733/sqrt(100,000) = 0.0118
    C/A >= pi^2/(432*log^2(1,078,853)) = 0.000138

    0.0118 > 0.000138. **DOES NOT CLOSE in this range!**

The issue: C/A ~ 1/log^2(p) is too small relative to 1/sqrt(p) for moderate p.

### 14.4 Tightening C/A

Using the TIGHTER bound C/A >= pi^2/(162*log^2(p)) (from improved constants):

**For p in [100,000, 1,078,853]:**
    C/A >= pi^2/(162*log^2(1,078,853)) = 0.000368

Still 0.0118 > 0.000368. Gap is 32x.

### 14.5 Using the ACTUAL empirical C/A

Empirically, C/A ~ 0.126 at p = 10,000, and C/A ~ 0.05 at p = 100,000.

So at p = 100,000: C/A ~ 0.05 vs |1-D/A| ~ 0.0118.
**C/A > |1-D/A|. THE GAP CLOSES EMPIRICALLY!**

The problem is the analytical C/A bound is 360x too conservative.

### 14.6 The real bottleneck

The bottleneck is NOT the Hurst bound on M. It is:

1. **The analytical C/A lower bound is 100-1000x too conservative.**
2. **The constant K in |1-D/A| <= K*|M|/p is not proved.**

If either (1) is tightened to within 10x of the truth, or (2) is proved with
a reasonable K, then the proof closes.

---

## 15. ACTIONABLE CONCLUSIONS

### 15.1 The Hurst bound is necessary but not sufficient

Hurst gives |M(x)| < 0.586*sqrt(x) for x <= 10^16. This is MUCH stronger than
El Marraki's |M(x)| < 0.644*x/logx. But the effective closure requires:

(a) An analytical proof of K (the proportionality constant in |1-D/A| ~ K*|M|/p)
(b) A tighter analytical lower bound on C/A

Neither (a) nor (b) follows from Hurst alone.

### 15.2 Recommended path forward

**Path 1 (Computational, most reliable):**
Extend the computation of B+C > 0 to p = 10^7, which with the Ramare bound
and conjectural K, covers up to p = 10^{78} (i.e., everything).

Cost: ~2-3 hours of C code computation.

**Path 2 (Analytical, harder but more satisfying):**
Prove K <= 10 by analyzing the Franel identity. The key step is showing that
sum_{k=1}^{p-1} D_old(k/p)^2 approximates (p-1)*old_D_sq/(2n) with error
at most K*|M(p)|*old_D_sq/p.

This is a statement about the equidistribution of D_old^2 at arithmetic points,
which should follow from the Ramanujan-sum expansion of D_old and the
explicit prime-counting bounds.

**Path 3 (Hybrid, most practical):**
- Compute B+C > 0 to p = 10^6 (~ 10 minutes)
- Prove C/A >= c/log(p) (instead of 1/log^2(p)) by using the Ramare coprimality bounds
- Then with K=6.37 and Ramare, the crossover is at p ~ 37, well below 10^6

The key to Path 3 is improving C/A from 1/log^2(p) to 1/log(p).

### 15.3 Immediate action items

1. **Verify B+C > 0 for M(p)<=-3 primes in [100K, 1M]** using the existing C code
   (certify_fast or bc_extend_fast2). This is a 10-minute computation.

2. **Investigate whether C/A >= c/log(p) can be proved.** The current 1/log^2 comes from
   using C_W <= log(N) in the denominator. If C_W can be bounded by a constant
   (conjectured C_W <= 0.71, verified to N=100K), then C/A >= c/log(p) follows.

3. **Analyze the model |1-D/A| <= K*|M(p)|/p more carefully.** Can K be related
   to the Franel-Landau constant? Is there a theoretical reason K < 10?
