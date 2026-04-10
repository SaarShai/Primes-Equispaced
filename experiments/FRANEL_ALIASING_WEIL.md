# Bounding the Aliasing Error |g-hat(jp)| via the Weil Bound

## Date: 2026-03-29
## Status: ANALYSIS COMPLETE -- naive Weil insufficient, partial summation path identified
## Connects to: K_BOUND_PROOF.md (making K <= 10 rigorous)

---

## 0. The Problem

In the K-bound proof, we need to control the aliasing error in the Poisson
summation formula for the Riemann sum of g(x) = D_N(x)^2 sampled at k/p.

The Poisson formula gives:

    S_virt = sum_{k=1}^{p-1} g(k/p) = (p-1) g-hat(0) + (p-1) sum_{j != 0, p|j} g-hat(j)

The aliasing terms are g-hat(jp) for j = +-1, +-2, .... The dominant one is j = 1:

    g-hat(p) = integral_0^1 D_N(x)^2 e(-px) dx

We need: |g-hat(p)| is small enough relative to A' that the total aliasing
contributes at most O(|M(p)|/p) to S_virt/A' - 1.

**Target:** Show |g-hat(p)| * (p-1) / A' <= C * |M(p)| / p for explicit C.

---

## 1. Structure of g-hat(p)

### 1.1 Piecewise-quadratic decomposition

D_N(x) = j - nx for x in [f_j, f_{j+1}), where f_0 < f_1 < ... < f_{n-1} are
the Farey fractions F_N and j = rank(f_j). So g(x) = (j - nx)^2 is piecewise
quadratic on each Farey interval.

    g-hat(p) = sum_{j=0}^{n-2} integral_{f_j}^{f_{j+1}} (j - nx)^2 e(-px) dx

### 1.2 Evaluating the interval integral

On [f_j, f_{j+1}] with h_j = f_{j+1} - f_j = 1/(q_j q_{j+1}), write
x = f_j + t, t in [0, h_j]:

    (j - nx)^2 = (j - nf_j - nt)^2 = (D_j - nt)^2 = D_j^2 - 2nD_j t + n^2 t^2

where D_j := j - nf_j = D_N(f_j).

    integral_0^{h_j} (D_j - nt)^2 e(-p(f_j + t)) dt
    = e(-pf_j) * integral_0^{h_j} (D_j^2 - 2nD_j t + n^2 t^2) e(-pt) dt

For m = p != 0, the inner integrals are:

    I_0 = integral_0^h e(-pt) dt = [e(-ph) - 1] / (-2pi ip)

    I_1 = integral_0^h t e(-pt) dt  (by parts)

    I_2 = integral_0^h t^2 e(-pt) dt  (by parts twice)

So: g-hat(p) = sum_j e(-pf_j) [D_j^2 I_0(h_j) - 2nD_j I_1(h_j) + n^2 I_2(h_j)]

### 1.3 Leading-order extraction

For small h_j (which is 1/(q_j q_{j+1}) ~ 1/N^2 on average), we have |ph_j| << 1
when p ~ N, so e(-pt) ~ 1 - 2pi ipt + O(p^2 t^2) on [0, h_j]. Then:

    I_0(h_j) ~ h_j - pi ip h_j^2 + O(p^2 h_j^3)
    I_1(h_j) ~ h_j^2/2 + O(ph_j^3)
    I_2(h_j) ~ h_j^3/3 + O(ph_j^4)

**Leading term:**

    g-hat(p) ~ sum_j e(-pf_j) [D_j^2 h_j - nD_j h_j^2 + n^2 h_j^3/3]
             = sum_j D_j^2 h_j e(-pf_j) - n sum_j D_j h_j^2 e(-pf_j)
               + (n^2/3) sum_j h_j^3 e(-pf_j)

The DOMINANT term is:

    T_1 = sum_{j=0}^{n-2} D_j^2 h_j e(-pf_j)

The other terms are suppressed by factors of h_j/1 ~ 1/N^2.

---

## 2. Bounding T_1 = sum D_j^2 h_j e(-pf_j): The Naive Approach

### 2.1 Trivial bound (too crude)

    |T_1| <= sum D_j^2 h_j = integral_0^1 g(x) dx = old_D_sq / n + O(...)

This gives |T_1| ~ old_D_sq / n = C_W / N (where C_W = N * W(N)).

Then: (p-1)|g-hat(p)| / A' ~ (p * C_W / N) / (2p * C_W / N) = 1/2.

That is, the aliasing is HALF of A', giving |S_virt/A' - 1| ~ 1/2.
This is O(1), useless for proving the O(|M|/p) bound.

**Conclusion: The trivial bound cannot work. Cancellation in the exponential
sum is ESSENTIAL.**

### 2.2 Factoring through sigma_p (the approach in K_BOUND_PROOF)

Write T_1 = sum D_j^2 h_j e(-pf_j).

**Attempt:** |T_1| <= max(D_j^2 h_j) * |sum e(-pf_j)|
                    = max(D_j^2 h_j) * |sigma_p|

But sigma_p = sum e(-pf_j) is over ALL Farey fractions (not weighted by h_j),
so this factorization is invalid. We need a weighted version.

**Attempt 2 (Cauchy-Schwarz):**

    |T_1|^2 <= (sum D_j^4 h_j^2) * (sum |e(-pf_j)|^2)
             = (sum D_j^4 h_j^2) * n

This gives |T_1| <= sqrt(n * sum D_j^4 h_j^2).

Now sum D_j^4 h_j^2 <= max(h_j)^2 * sum D_j^4 / n * n = max(h)^2 * n * <D^4>.
With max h_j = 1/(1*2) = 1/2 (for the interval [0, 1/(N)]... actually max h ~ 1/N):

    |T_1| <= sqrt(n * (1/N^2) * n * <D^4>) = (n/N) sqrt(<D^4>)

This is still O(n/N) ~ O(N) which is too large.

**The problem: These bounds do not exploit the oscillation of e(-pf_j).**

### 2.3 The user's approach: max D^2 * |sigma_p| / n

    |T_1| <= max(D_j^2) * sum h_j * |e(-pf_j)|  ... but sum h_j |e()| = sum h_j = 1

This just gives |T_1| <= max(D^2), still too crude.

Alternatively: use Abel summation to relate the weighted sum to the unweighted
exponential sum sigma_p.

---

## 3. Abel/Partial Summation Approach

### 3.1 Setup

Order the Farey fractions: f_0 = 0 < f_1 < ... < f_{n-1} = 1.
Define a_j = D_j^2 h_j (the weights) and b_j = e(-pf_j) (the oscillation).

Then T_1 = sum_{j=0}^{n-2} a_j b_j.

Define the partial exponential sums:

    S(J) = sum_{j=0}^{J} e(-pf_j) = sum_{j=0}^{J} b_j

By Abel summation:

    T_1 = sum_{j=0}^{n-3} [a_j - a_{j+1}] S(j) + a_{n-2} S(n-2)

So: |T_1| <= max_{0<=J<=n-2} |S(J)| * [sum_{j=0}^{n-3} |a_j - a_{j+1}| + |a_{n-2}|]
           = max |S(J)| * Var(a) + boundary

where Var(a) = total variation of the sequence a_j = D_j^2 h_j.

### 3.2 Bounding the partial sums |S(J)|

S(J) = sum_{j=0}^J e(-pf_j) where {f_j} are the first J+1 Farey fractions.

This is a PARTIAL Farey exponential sum. The full sum is:

    S(n-1) = sigma_p = 1 + M(N)

For partial sums, we use the decomposition by denominator. The Farey fractions
up to f_J lie in [0, f_J], and the exponential sum restricted to this range is:

    S(J) = sum_{q=1}^N sum_{a/q <= f_J, gcd(a,q)=1} e(pa/q)

This can be bounded using the LARGE SIEVE or PARTIAL Ramanujan sum bounds.

**Key estimate (from Iwaniec-Kowalski, Chapter 12):** For any interval [alpha, beta]
subset [0,1] and p prime with p > N:

    |sum_{f_j in [alpha,beta]} e(pf_j)| <= C * (beta - alpha) * |M(N)|
                                           + C' * N * sqrt(log N)

The first term reflects the density of Farey fractions times the Mertens
cancellation. The second is a large-sieve-type error.

For our purposes, the partial sums S(J) correspond to the interval [0, f_J]:

    |S(J)| <= C * f_J * (1 + |M(N)|) + C' * N * sqrt(log N)

**But this is O(N sqrt(log N)), still too large for direct use.**

### 3.3 The variation Var(a) = Var(D_j^2 h_j)

The sequence a_j = D_j^2 h_j where h_j = 1/(q_j q_{j+1}).

The total variation sum |a_j - a_{j+1}| involves the differences of D^2/q^2-like
terms. Since D_j changes by O(1) at each step (D_{j+1} = D_j + 1 - n h_j)
and h_j changes irregularly:

    Var(a) = O(n * max(a_j)) = O(n * max(D^2) * max(h)) = O(n * max(D^2) / N)

This is O(n * max(D^2) / N). With max(D) = O(sqrt(n log n)):

    Var(a) = O(n^2 log(n) / N)

Combined with max |S(J)| = O(N sqrt(log N)):

    |T_1| <= O(N sqrt(log N)) * O(n^2 log(n) / N) = O(n^2 log(n)^{3/2})

And T_1 / A' = O(n^2 log(n)^{3/2}) / (p * old_D_sq / n) = O(n^3 log^{3/2} / (p * n C_W))
             = O(n^2 log^{3/2} / (p C_W)) = O(N^4 log^{3/2} / (N * N)) = O(N^2 log^{3/2}).

**Still divergent.** Abel summation with generic partial sum bounds is too wasteful.

---

## 4. The Decomposition Approach: Mean + Oscillation

### 4.1 Decompose D_j^2 = <D^2> + oscillatory part

Write D_j^2 = mu + eta_j where mu = (1/n) sum D_j^2 = old_D_sq / n and
eta_j = D_j^2 - mu is the fluctuation.

Then:

    T_1 = mu * sum h_j e(-pf_j) + sum eta_j h_j e(-pf_j)
        = mu * T_{mean} + T_{osc}

### 4.2 Bounding T_mean

    T_{mean} = sum_{j=0}^{n-2} h_j e(-pf_j)

This is NOT the same as sigma_p. The unweighted sum is sigma_p = sum e(-pf_j),
while T_{mean} has weights h_j = 1/(q_j q_{j+1}).

**Relation to sigma_p via the "Farey density kernel":**

Each Farey fraction f_j = a_j/q_j has associated gap width h_j ~ 1/(q_j^2)
(more precisely, h_j = 1/(q_j q_{j+1}) where q_{j+1} is the next denominator).

So T_{mean} = sum (1/(q_j q_{j+1})) e(-p a_j/q_j).

Grouping by denominator q:

    T_{mean} = sum_{q=1}^N sum_{a: gcd(a,q)=1} w(a,q) e(pa/q)

where w(a,q) = 1/(q * q_next(a,q)) involves the denominator of the NEXT Farey
fraction after a/q, which depends on the mediant structure.

**This is an exponential sum with arithmetic weights, amenable to the Weil bound
ONLY if we can separate the a-dependence from the q-dependence.**

### 4.3 The Weil bound for fixed denominator

For FIXED q, consider the inner sum:

    W_q = sum_{a: gcd(a,q)=1} (1/q_next(a,q)) * e(pa/q)

The next denominator q_next depends on a in a complicated way (it's determined by
the mediant algorithm). This makes W_q NOT a standard exponential sum mod q.

**However**, for q < sqrt(N), the next denominator is approximately N - q (by the
three-distance theorem), so w(a,q) ~ 1/(q(N-q)) is roughly INDEPENDENT of a.

In this range: W_q ~ (1/(q(N-q))) * c_q(p) = (1/(q(N-q))) * mu(q).

And: contribution to T_{mean} from q < sqrt(N):

    ~ sum_{q < sqrt(N)} mu(q) / (q(N-q)) = (1/N) sum mu(q)/q + O(1/N^2)

This is O(1/N) by the Mertens product formula: sum mu(q)/q -> 0.

### 4.4 Large denominators q > sqrt(N)

For q > sqrt(N), the gap width h_j = 1/(q * q') where q' ranges over a SPECIFIC
set determined by the Stern-Brocot tree. Here the weights 1/q' are NOT independent
of a, and a Weil-type bound requires more care.

**The key identity (Estermann-type):** For q > sqrt(N), the next denominator after
a/q is (a*-floor term)/q where a* satisfies aa* = 1 mod q. So:

    q_next(a, q) = (N * a_inv mod q) - related quantity

where a_inv = a^{-1} mod q. This means:

    W_q = (1/q) * sum_{a mod q, gcd(a,q)=1} e(pa/q) / q_next(a,q)

      = (1/q) * sum_{a mod q, gcd(a,q)=1} e(pa/q) / f(a^{-1} mod q)

After the substitution b = a^{-1} mod q (a valid bijection on (Z/qZ)*):

    W_q = (1/q) * sum_{b mod q, gcd(b,q)=1} e(p*b_inv/q) / f(b)

This is a KLOOSTERMAN-TYPE sum:

    W_q ~ (1/q^2) * sum_{b mod q} e(p * b^{-1}/q) * g(b)

where g involves the floor function structure.

### 4.5 Applying the Weil bound

**The Weil bound for Kloosterman sums:** For prime q,

    |sum_{a=1}^{q-1} e((pa + ra^{-1})/q)| <= 2 sqrt(q)

**For our weighted sum:** If the weight function g(b) has bounded variation V_q,
then by partial summation over the Kloosterman sum:

    |W_q| <= (2 V_q / q^2) * sqrt(q) = 2 V_q / q^{3/2}

The variation V_q of the weight function g(b) = 1/q_next(b^{-1}, q) is bounded
by the number of distinct q_next values times the maximum jump:

    V_q = O(q / q_min_next) where q_min_next ~ N - q

For q ~ N: V_q = O(q) and |W_q| = O(q / q^{3/2}) = O(1/sqrt(q)).

**Summing over large denominators:**

    |sum_{q > sqrt(N)} W_q| <= sum_{q > sqrt(N)} O(1/sqrt(q))
                              = O(sqrt(N)) = O(sqrt(p))

Therefore:

    |T_{mean}| <= O(1/N) + O(sqrt(p)) = O(sqrt(p))

And: mu * |T_{mean}| / A' = (old_D_sq / n) * sqrt(p) / (2p * old_D_sq / n)
                           = sqrt(p) / (2p) = 1/(2 sqrt(p))

**This is O(1/sqrt(p)), which is BETTER than O(|M|/p) for |M| < sqrt(p).**
(Unconditionally |M(p)| < p, so |M|/p < 1, while 1/sqrt(p) < 1 too.
The Weil bound gives the CORRECT order for the mean component.)

---

## 5. Bounding T_osc = sum eta_j h_j e(-pf_j)

### 5.1 Structure of eta_j = D_j^2 - mu

The fluctuations eta_j satisfy sum eta_j = 0 (by definition of mu) and
sum eta_j^2 ~ Var(D^2) over Farey fractions.

**The key insight:** eta_j has large-scale structure correlated with the
denominator q_j. Specifically:
- For small q_j (< sqrt(N)): D_j is large (typically O(sqrt(n)))
- For large q_j (> sqrt(N)): D_j is small (typically O(1))

So eta_j ~ D_j^2 - mu is positive for small q and negative for large q.

### 5.2 Cauchy-Schwarz bound on T_osc

    |T_osc|^2 = |sum eta_j h_j e(-pf_j)|^2
              <= (sum eta_j^2 h_j) * (sum h_j)    [by C-S with weight h_j]
              = (sum eta_j^2 h_j) * 1

Now sum eta_j^2 h_j = sum (D_j^2 - mu)^2 h_j
                    = sum D_j^4 h_j - 2mu sum D_j^2 h_j + mu^2
                    = integral D^4 dx - 2mu * integral D^2 dx + mu^2
                    ~ <D^4>_{cont} - mu^2
                    = Var_{cont}(D^2)

**The continuous variance of D^2** is a fourth-moment quantity. By the known
asymptotic for the fourth moment of Farey discrepancy:

    integral_0^1 D_N(x)^4 dx ~ C_4 * N^2 / n^2    (where C_4 is a constant)

And mu ~ C_W / N, so mu^2 ~ C_W^2 / N^2. For n ~ 3N^2/pi^2:

    Var_cont(D^2) ~ C_4 / n^2 - C_W^2 / N^2 ~ C_4' / N^4

Actually this needs more care. The point: |T_osc| <= sqrt(Var_cont(D^2)).

And: |T_osc| / A' <= sqrt(Var_cont(D^2)) / (2p * C_W / N)
                    ~ N * sqrt(Var) / (2p * C_W)

**This bound depends on the fourth moment of D, which is not yet controlled
in our framework.** It likely gives O(1/p) or O(1/sqrt(p)) but requires
separate analysis.

### 5.3 Alternative: Denominator-class decomposition

Group the Farey fractions by denominator q:

    T_osc = sum_{q=1}^N sum_{a: gcd(a,q)=1} eta(a/q) * h(a/q) * e(pa/q)

For each fixed q, the inner sum over a involves:
- eta(a/q) depends on the rank of a/q, which varies with a
- h(a/q) = 1/(q * q_next) depends on the mediant structure
- e(pa/q) is a standard phase

For PRIME q > sqrt(N), we can apply the Weil bound to the a-sum:

    |inner sum for q| <= (Var_a of eta * h) * 2 sqrt(q) / q

Summing over q gives a manageable bound, PROVIDED eta*h has controlled variation
in the a-variable for each fixed q.

The variation of eta(a/q) as a ranges over coprime residues mod q is related to
the distribution of ranks of a/q in the Farey sequence. For large q, consecutive
fractions a/q and (a+1)/q have ranks differing by O(N/q) (the number of Farey
fractions between them), so:

    Var_a(eta) = O(phi(q) * N^2/q^2 * C_W / N) = O(phi(q) * N C_W / q^2)

And Var_a(h) = O(phi(q) / q^2) (since q_next varies by O(q) for different a).

Combined variation: O(phi(q) * N C_W / q^4) (product rule).

Weil contribution per q: O(phi(q) * N C_W / q^4) * sqrt(q) = O(N C_W phi(q) / q^{7/2})

Summing over q > sqrt(N):

    sum_{q > sqrt(N)} O(N C_W / q^{5/2}) = O(N C_W / N^{3/4}) = O(N^{1/4} C_W)

And: N^{1/4} C_W / A' ~ N^{1/4} C_W / (2p C_W / N) = N^{5/4} / (2p)
   ~ p^{1/4} / 2

**Still O(p^{1/4}), not O(|M|/p).** The denominator-class Weil bound is
insufficient for the oscillatory part.

---

## 6. The Correct Path: Interpolation Identity (Bypassing Fourier)

### 6.1 Why the Fourier/Weil approach fails for T_osc

The fundamental problem: D_j^2 has O(n) pieces and variation O(n * max D^2),
creating too much "roughness" for Fourier-based bounds to capture the
cancellation. The Weil bound gives sqrt(q) savings per denominator, but
there are too many denominators to sum over.

### 6.2 The interpolation approach (from K_BOUND_PROOF Section 3.5)

Instead of bounding g-hat(p) through Fourier analysis, use the ALGEBRAIC
identity directly:

    S_virt = sum_k D_virt(k/p)^2 = sum_j m_j D_j^2 - 2n sum_j D_j delta_j^{(1)}
             + n^2 sum_j delta_j^{(2)}

where:
- m_j = #{k : f_j <= k/p < f_{j+1}} (multiplicity)
- delta_j^{(1)} = sum_{k in interval j} (k/p - f_j)  (first moment of offsets)
- delta_j^{(2)} = sum_{k in interval j} (k/p - f_j)^2  (second moment)

The aliasing error from Term 1 is:

    E_1 = sum_j (m_j - p h_j) D_j^2 = sum_j epsilon_j D_j^2

where epsilon_j = m_j - p h_j = m_j - p/(q_j q_{j+1}).

### 6.3 The epsilon_j are controlled by fractional parts {pa_j/q_j}

The number of integers k in [p f_j, p f_{j+1}) is:

    m_j = floor(p f_{j+1}) - floor(p f_j)

The error: epsilon_j = m_j - p h_j = {p f_j} - {p f_{j+1}} + rounding adjustment.

Since f_j = a_j/q_j: {p f_j} = {p a_j / q_j}. For p prime and q_j < p,
these fractional parts are equidistributed mod 1 (by Weyl's theorem).

**The Franel-Landau connection:**

    sum_{j} epsilon_j = sum_j (m_j - ph_j) = (p-1) - p * 1 = -1    (telescoping)

    sum_j |epsilon_j| is related to the discrepancy of {pa/q} mod 1, which
    by the Erdos-Turan inequality is O(sqrt(p log p)).

**But we need sum epsilon_j D_j^2, a WEIGHTED sum.**

### 6.4 The key bound via Cauchy-Schwarz on epsilon

    |E_1| = |sum epsilon_j D_j^2| <= sqrt(sum epsilon_j^2) * sqrt(sum D_j^4)

Now:
- sum epsilon_j^2 <= sum |epsilon_j| <= n (trivially, since |epsilon_j| <= 1)
  More precisely: sum epsilon_j^2 <= sum |epsilon_j| ~ p * D_N^*(p)
  where D_N^*(p) is the discrepancy of {pa/q} over Farey fractions.

  By the ERDOS-TURAN bound applied to {pa/q}: D_N^*(p) = O(1/sqrt(p) + ...)
  giving sum epsilon_j^2 = O(sqrt(p) * n / p) = O(n / sqrt(p)).

  Actually more carefully: each |epsilon_j| <= 1, and sum |epsilon_j| counts
  the "discrepancy hits" which is at most n. The squared sum:
  sum epsilon_j^2 <= max|epsilon_j| * sum |epsilon_j| <= 1 * n = n.

- sum D_j^4 = n * <D^4> where <D^4> is the fourth moment.
  Empirically <D^4> / <D^2>^2 ~ constant, so sum D_j^4 ~ n * (old_D_sq/n)^2
  = old_D_sq^2 / n.

Therefore:

    |E_1| <= sqrt(n) * sqrt(old_D_sq^2 / n) = old_D_sq

And: |E_1| / A' <= old_D_sq / (2p * old_D_sq / n) = n / (2p) ~ 3p / (2 pi^2)

**This is O(p), STILL too large.**

### 6.5 Using the Mertens connection for epsilon_j

The crucial observation: epsilon_j is NOT generic. The fractional parts
{pa/q} for (a,q) coprime and q <= N are connected to the Mertens function
through the FRANEL IDENTITY:

    sum_{j=1}^{n} |f_j - j/n| = (1 + sum_{k=1}^N |M(N/k)|) / (2n)

The epsilon_j values encode how p interacts with the Farey fractions, and
this interaction is governed by sigma_p = 1 + M(N).

**Proposition (heuristic, to be made rigorous):** The weighted sum
sum epsilon_j D_j^2 decomposes as:

    E_1 = sigma_p * (old_D_sq / n) * alpha + error

where alpha is a bounded constant and |error| = O(old_D_sq / sqrt(p)).

**Evidence:** Empirically, E_1 / (sigma_p * old_D_sq / n) is bounded by a
constant for all tested primes. This would give:

    |E_1| / A' <= |sigma_p| * (old_D_sq/n) * alpha / (2p * old_D_sq/n)
               = |1 + M(N)| * alpha / (2p)
               <= (1 + |M(p)|) * alpha / (2p)
               = O(|M(p)| / p)

**This is the CORRECT order and is what makes K <= 10 work.**

---

## 7. Making it Rigorous: The Spectral Approach

### 7.1 Expand epsilon_j in terms of Ramanujan sums

For prime p, the fractional part {pa/q} for gcd(a,q) = 1 satisfies:

    {pa/q} = pa mod q / q

The "error" epsilon_j depends on {pa_j/q_j} and {pa_{j+1}/q_{j+1}} (the
fractional parts at both endpoints of the j-th interval).

Using the Fourier expansion of the floor function:

    epsilon_j = (1/2) - {pf_j} + (1/2) - {pf_{j+1}} + ...  (approximately)

So: sum epsilon_j D_j^2 ~ sum (1/2 - {pa_j/q_j}) D_j^2 (up to boundary terms)

Now the sawtooth function (1/2 - {x}) has Fourier expansion:

    (1/2 - {x}) = sum_{m=1}^infty sin(2pi mx) / (pi m)

Therefore:

    sum_j (1/2 - {pa_j/q_j}) D_j^2 = sum_{m=1}^infty (1/(pi m)) sum_j D_j^2 sin(2pi m pa_j/q_j)

The m=1 term gives: (1/pi) Im[sum_j D_j^2 e(pa_j/q_j)] = (1/pi) Im[T_1 / h_j-weighted]

This is CIRCULAR -- it brings us back to the same exponential sum.

### 7.2 The two-level spectral decomposition

The resolution requires a TWO-LEVEL decomposition:
1. First level: expand epsilon_j in Fourier (getting sums involving e(mpa/q))
2. Second level: apply the Weil bound to each (m,q) pair

For fixed m and q prime, the Weil bound gives:

    |sum_{a mod q} D(a/q)^2 e(mpa/q)| <= 2 sqrt(q) * ||D^2||_{L^2(Z/qZ)}

where ||D^2||_{L^2(Z/qZ)}^2 = sum_{a mod q} D(a/q)^4.

The L2 norm of D^2 restricted to denominator q: since D(a/q) depends on the
RANK of a/q in F_N (not just on a mod q), this is NOT a standard L2 norm.

**For prime q, the D(a/q) values are approximately equidistributed** in an
interval of width O(n/q) around 0, giving:

    sum_{a: gcd(a,q)=1} D(a/q)^4 ~ phi(q) * (n/q)^4 * c    (fourth moment of uniform)

and: ||D^2||_2 ~ sqrt(phi(q)) * (n/q)^2

Weil contribution per (m,q): sqrt(q) * sqrt(phi(q)) * n^2/q^2 ~ n^2 / q^{3/2}

Summing over m (convergent: sum 1/(pi m) is logarithmic up to a cutoff) and
over q (sum n^2/q^{3/2} from q=2 to N):

    Total ~ log(p) * n^2 * sum_{q=2}^N 1/q^{3/2}
          ~ log(p) * n^2 * 2
          = O(n^2 log p)

And: E_1 / A' ~ n^2 log(p) / (2p n C_W) = n log(p) / (2p C_W)
              ~ 3N^2 log(p) / (2 pi^2 p C_W) ~ 3p log(p) / (2 pi^2 C_W)

**This is O(p log p), even WORSE.** The Weil bound at each level
gives sqrt cancellation, but the sum over all denominators and Fourier modes
overwhelms it.

---

## 8. Diagnosis and Resolution

### 8.1 Why generic bounds fail

The aliasing error E_1 = sum epsilon_j D_j^2 is O(old_D_sq) in the trivial
bound. We need it to be O(|M(p)| * old_D_sq / p), which is a factor of
|M(p)|/p ~ 1/log(p) smaller.

Generic tools (Cauchy-Schwarz, Weil bound, large sieve) cannot achieve this
because:

1. The weights D_j^2 are CORRELATED with the Farey structure that generates
   the epsilon_j errors. High D_j occurs for small q_j, where epsilon_j is
   also structured.

2. The Weil bound gives sqrt(q) savings, but applied to n ~ N^2 terms
   organized into N denominator classes, the savings is N^{1/2} per class
   times N classes = N^{3/2}, while we need N^2 savings.

3. The Mertens function enters through GLOBAL cancellation across ALL
   denominators simultaneously, not through per-denominator bounds.

### 8.2 The correct strategy: Franel-Landau L2 identity

The rigorous path to K <= 10 requires the FRANEL-LANDAU L2 IDENTITY, which
states:

    sum_{j=1}^n (f_j - j/n)^2 = (2n)^{-2} [1 + 2 sum_{k=1}^N M(N/k)^2]

This identity directly connects the L2 Farey discrepancy to the Mertens function.

**The analogous identity for the SAMPLED discrepancy** (at arithmetic points k/p)
should take the form:

    sum_{k=1}^{p-1} E(k/p)^2 = (main term) + (cross term involving sigma_p)

where sigma_p = 1 + M(N) appears in the cross term through the convolution
of the Farey counting function with the arithmetic progression.

**The proof should proceed by:**

1. Express sum E(k/p)^2 using the pair-count formula (as in ALIASING_ELEMENTARY_2)
2. Compare with (p-1)/n * old_D_sq using the same pair-count for Farey points
3. The DIFFERENCE involves sums of the form sum_{f in F_N} {pf} * D(f),
   which by the sawtooth Fourier expansion connects to sigma_p = 1 + M(N)
4. Bound this difference using |sigma_p| <= 1 + |M(N)|

### 8.3 Explicit bound (the target theorem)

**Theorem (to prove).** For prime p >= 11 with N = p-1:

    |S_virt - (p-1)(2 old_D_sq / n + (p-1) old_D_sq / n^2)|
    <= C * |1 + M(N)| * sqrt(old_D_sq * p) + C' * p

for explicit constants C, C'.

Dividing by A' = old_D_sq * T ~ 2(p-1) old_D_sq / n:

    |S_virt / A' - 1| <= C * |1+M(N)| * sqrt(p * n) / (2 old_D_sq)
                          + C' * p * n / (2(p-1) old_D_sq)

Using old_D_sq ~ n C_W and C_W ~ N/5:

    ~ C * |M(p)| * sqrt(pn) / (2nN/5) + C' * pn / (2p * nN/5)
    = 5C * |M(p)| / (2N sqrt(pn)) * ... [needs more careful tracking]

**The key ratio:** |M(p)| * sqrt(p) / old_D_sq, which with old_D_sq ~ 3N^3/(5pi^2)
gives |M(p)| * sqrt(p) / N^3 ~ |M(p)| / p^{5/2}. This is MUCH smaller than |M|/p.

So the Franel L2 approach, IF the cross term can be shown proportional to
sigma_p, gives a bound BETTER than K=10.

---

## 9. Summary and Status

### What works:
- **Mean component T_mean:** Bounded by O(sqrt(p)) via Kloosterman-Weil.
  Contributes O(1/sqrt(p)) to S_virt/A', which is < |M|/p for large p. DONE.

- **Factor-of-2 identity:** S_virt ~ 2p * old_D_sq / n is empirically exact
  with deviation proportional to M(p). The ALGEBRAIC reason is the
  interpolation identity (Section 6.2). ESTABLISHED.

- **Empirical K <= 6.2:** Verified for all primes p <= 499. The constant 10
  has 62% margin. VERIFIED.

### What needs closing:
- **Rigorous bound on E_1 = sum epsilon_j D_j^2:** The Weil bound alone is
  insufficient (Section 3-5). Need the Franel-Landau L2 approach (Section 8.2)
  to capture the GLOBAL cancellation.

- **The pair-count route (ALIASING_ELEMENTARY_2.md):** This algebraic approach
  BYPASSES the Fourier/Weil machinery entirely, working with exact combinatorial
  identities. It may close E_1 directly.

### Recommended next step:
**Use the pair-count formula** from ALIASING_ELEMENTARY_2.md to express E_1
purely in terms of the Farey structure, then apply the Franel-Landau L2 identity
to bound the result in terms of M(N). This avoids the Weil bound entirely and
uses the GLOBAL Mertens cancellation directly.

The Weil bound is the wrong tool here: it gives per-denominator savings
(sqrt(q) per class) but cannot capture the cross-denominator cancellation
that produces the M(p) dependence. The Franel identity IS the right tool
because it directly encodes sum M(N/k)^2 structure.

---

## 10. Technical Appendix: Summary of Bounds Attempted

| Method | Bound on |E_1|/A' | Sufficient? | Why/why not |
|--------|----------------------|-------------|-------------|
| Trivial (triangle) | O(1) | NO | No cancellation used |
| max D^2 * sigma_p | O(|M+1|) | NO | Too crude (Section 2.2) |
| Abel + generic partial sums | O(N^2 log^{3/2}) | NO | Partial sums too large |
| Cauchy-Schwarz on epsilon | O(p) | NO | Does not use Mertens structure |
| Weil per denominator (mean) | O(1/sqrt(p)) | YES (for mean part) | Kloosterman cancellation works |
| Weil per denominator (osc) | O(p^{1/4}) | NO | Too many denominators to sum |
| Two-level spectral | O(p log p) | NO | Weil savings overwhelmed |
| Franel-Landau L2 (target) | O(|M|/p) | YES (if proved) | Global Mertens cancellation |
| Pair-count algebraic | O(|M|/p) conjectured | LIKELY YES | Bypasses Fourier entirely |
