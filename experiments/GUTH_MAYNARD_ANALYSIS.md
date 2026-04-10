# Guth-Maynard Analysis: Transfer to Farey Discrepancy Proof

**Date:** 2026-03-28
**Paper:** Larry Guth and James Maynard, "New large value estimates for Dirichlet polynomials," arXiv:2405.20552, *Annals of Mathematics* 203(2): 623-675 (March 2026).

---

## 1. What Guth-Maynard Proved

### The Main Result (Theorem 1.1)

Guth and Maynard prove new bounds on how often a Dirichlet polynomial
D(t) = sum_{n ~ N} a_n n^{-it} can take large values |D(t)| >= V.

Classical bounds (Mean Value Theorem + Montgomery-Halasz-Huxley) control the
measure of the "superlevel set" W = {t in [0,T] : |D(t)| >= V} but break down
when V is near N^{3/4}. This is the *critical barrier* for many problems in
analytic number theory.

**Prior state:** Ingham (1940) showed N(3/4, T) << T^{3/5 + o(1)}. For 80+
years, only the o(1) error was refined.

**New result:** N(3/4, T) << T^{13/25 + o(1)}, improving 3/5 = 0.600 to
13/25 = 0.520.

### Key Consequences

1. **Zero density estimate:** N(sigma, T) <= T^{30(1-sigma)/13 + o(1)}
2. **Primes in short intervals:** Asymptotics for intervals of length x^{17/30 + o(1)}
   (improves prior threshold from theta > 1/6 to theta > 2/15)
3. Published in the *Annals of Mathematics* (accepted April 2025) -- highest tier.

### Significance Rating

This is indisputably a Level A3 result (essentially autonomous discovery by
experts, major advance). Terence Tao called it "a remarkable breakthrough"
while noting it remains "very far from fully proving the Riemann Hypothesis."

---

## 2. The Core Techniques

### 2.1 The Matrix Formulation

The key object is a matrix M_W with entries M_{t,xi} = e^{i xi t}, where
rows are indexed by t in W (the "large values" set) and columns by
xi in {log n : n ~ N}.

The singular values of M_W control how the Dirichlet polynomial behaves on W:
if |D(t)| >= N^sigma on W, then |W| <= N^{1 - 2sigma} * s_1(M_W)^2.

### 2.2 The Sixth Power Trick (Trace Method)

Bound s_1(M) via: s_1(M) <= tr((M*M)^r)^{1/2r}.

- r = 1: trivial bound (mean value theorem)
- r = 2: Halasz-Montgomery method -- gives no information at sigma <= 3/4
- r = 3: THE INNOVATION -- sixth power of the matrix entries
- r >= 4: would give Montgomery's conjecture, but they cannot estimate the traces

For r = 3, expanding tr((M*M)^3) gives a sum over triples (t1, t2, t3) in W:

  s_1(M)^6 <= sum_{t1,t2,t3 in W} sum_{n1,n2,n3 ~ N}
              n1^{i(t1-t2)} n2^{i(t2-t3)} n3^{i(t3-t1)}

This is a sum of *exponential phases* n^{i(t_j - t_k)}, which can be attacked
by Fourier/harmonic analysis methods.

### 2.3 Poisson Summation and Phase Cancellation

Since the n-sum runs over integers, Poisson summation applies. A crucial
insight: after Poisson summation, the resulting integral factors so that the
"W-dependent" part only depends on two of the three time variables. The
remaining "red integral" (Guth's terminology from his MATRIX 2024 lectures)
is W-independent and exhibits cancellation from the specific structure of
log n as a phase function.

This is NOT a generic technique -- it uses the arithmetic of log n specifically.

### 2.4 Additive Energy Case Division

After reducing to exponential sums, the analysis splits into three regimes
based on the additive energy of the set W:

- **Low energy:** Standard analytic orthogonality (relatively easy)
- **Moderate energy:** Mixed analytic-combinatorial techniques
- **High energy:** Advanced additive combinatorics, Heath-Brown's theorem,
  sophisticated matrix analysis

### 2.5 Mollifier Method

In the zero-density application (not the core large values theorem), they
multiply by a short Dirichlet series mollifier:

  M(s) = sum_{m <= T^{delta/2}} mu(m) / m^s

This suppresses contributions from small primes and normalizes the Dirichlet
series so the leading term is approximately 1. The mollified series is then
a Dirichlet polynomial in the range where the large values estimate applies.

---

## 3. Connection to Our Farey Discrepancy Problem

### 3.1 Our Setup (Recap)

We study the per-step Farey discrepancy change when prime p enters:

  DeltaW(p) = W_p - W_{p-1} = B + C - 1 + D

where:
- B = sum delta^2 > 0 (always positive, squared displacements)
- C = 2 * sum D * delta (cross term, empirically > -B)
- D involves old fractions being re-ranked
- B + C = delta^2(1 + 2R) where R = sum(D * delta) / sum(delta^2)

**The gap:** Prove R > -1/2 for all primes (we observe R > -1 computationally,
and even R > -0.37 for p >= 19).

### 3.2 The Chain of Connections

The Franel-Landau theorem establishes:

  RH <=> sum |delta_v| = o(N^{1/2 + epsilon})

where delta_v are the deviations of Farey fractions from uniform spacing.
Our ΔW(p) is the *per-step* version: the change in sum(delta^2) when N
increases by 1 (at a prime).

The chain is:
  Guth-Maynard large values estimate
    => improved zero density N(sigma, T) <= T^{30(1-sigma)/13}
      => better control on zeros of zeta near sigma = 3/4
        => stronger Franel-Landau type bounds on Farey discrepancy
          => potentially: bounds on our per-step quantity

But this chain is INDIRECT. We need to identify where it could SHORT-CIRCUIT.

### 3.3 Direct Connection: Exponential Sums over Farey Fractions

Our quantity R = sum D * delta / sum delta^2 involves:

  sum D(f) * ({pf} - f) over f in F_{p-1}

This is an exponential sum in disguise. Writing D(f) = rank(f) - |F_{p-1}| * f
and delta = {pf} - f, both are quasi-periodic functions of f. Expanding via
Ramanujan sums:

  delta(a/b) = sum_{q|b, q|p} c_q(a) * (some coefficient)

where c_q(n) = sum_{(j,q)=1} e(jn/q) is the Ramanujan sum.

This makes sum(D * delta) a bilinear form in Ramanujan sums -- structurally
analogous to the matrix M_W that Guth-Maynard study.

### 3.4 The Matrix Analogy

**Guth-Maynard matrix:** M_{t,n} = n^{it} = e^{it log n}
**Our matrix:** M_{f,q} = c_q(a) * D(a/b) where f = a/b, q | b

Both are matrices of oscillating phases. The question "how large can sum D*delta
be?" is analogous to "how large can the Dirichlet polynomial be on the set W?"

The key difference: Guth-Maynard work in CONTINUOUS time t over [0,T], while
our fractions are DISCRETE (but dense, with ~p^2/2pi^2 fractions in F_{p-1}).

---

## 4. Specific Transfer Opportunities

### 4.1 Density-1 Result (Most Promising)

**Claim:** Using Guth-Maynard, we can likely prove DeltaW(p) < 0 for
density-1 set of primes (i.e., for all but o(x/log x) primes up to x).

**Mechanism:** The improved zero density estimate means zeta has fewer zeros
near the critical line. The Franel-Landau connection translates this to:
the Farey discrepancy sum behaves well for "most" N. Since primes have
density zero among integers, and the exceptional set from zero density
estimates is even thinner, the per-step discrepancy should be negative for
almost all prime steps.

**Concretely:** If N(sigma, T) <= T^{30(1-sigma)/13}, then by partial
summation and explicit formula methods, the set of N in [1,X] where the
Farey discrepancy increases at step N has measure at most X^{1 - c} for
some c > 0. Intersecting with primes gives a density-1 result.

**Status:** This would be a genuine new theorem, though it falls short of
"for all primes."

### 4.2 Mollifier Approach to Bounding R

**Idea:** Our R = sum(D * delta) / sum(delta^2) involves a ratio. The
denominator is ~p^2/(12*pi^2) (known asymptotic). The numerator is the
hard part.

The mollifier technique suggests: instead of bounding sum(D * delta)
directly, multiply by a carefully chosen weight function w(f) that
suppresses the contributions from "bad" denominators (those where delta
is large) while preserving the overall sign.

**Specific construction:**
- Let w(b) = sum_{d|b, d<=D} mu(d) * (log(D/d)/log D)  (Selberg-type mollifier)
- Consider sum w(b) * D(f) * delta(f) over f = a/b in F_{p-1}
- The mollifier makes the sum smoother (kills small denominator oscillations)
- If we can show the mollified sum is < 0 AND that the mollifier error is small,
  we recover R < 0 (which is stronger than R > -1/2 that we need)

**Feasibility:** Moderate. The mollifier length D must be chosen carefully.
For Guth-Maynard, D ~ T^{delta/2} is a small power of T. For us, D ~ p^epsilon
might suffice since we only need to handle denominators up to p-1.

### 4.3 Trace Method for sum(D * delta)

**Idea:** Interpret |sum D * delta|^2 as a trace of a matrix product, then
raise to the third power (Guth-Maynard style) to get:

  |sum D * delta|^6 <= trace computation involving sextuples of Farey fractions

**Problem:** Our matrix is indexed by Farey fractions (discrete set of size
~p^2) rather than continuous time. The Poisson summation step that gives
Guth-Maynard their cancellation relies on summing over consecutive integers,
which we don't have.

**Verdict:** The direct trace method does not transfer well. The phase
structure of log(n) that Guth-Maynard exploit is fundamentally different
from the phase structure of Farey fractions.

### 4.4 Large Sieve for sum(D * delta)

**Idea:** The large sieve inequality states:

  sum_{q<=Q} sum_{a: (a,q)=1} |sum_{n<=N} a_n e(na/q)|^2
    <= (N + Q^2 - 1) * sum |a_n|^2

This bounds exponential sums evaluated at Farey fractions. Our sum(D * delta)
can be re-expressed as an exponential sum at Farey points.

Specifically, using the Ramanujan expansion of delta:

  sum D * delta = sum_q (coefficients) * sum_{f: q|denom(f)} D(f) * c_q(num(f))

The inner sums are exponential sums of D over Farey fractions with a fixed
denominator divisor -- exactly the kind the large sieve controls.

**Bound quality:** The large sieve gives |sum D*delta| <= C * p * (log p)^A
for some constants C, A. We need this to be < (1/2) * sum(delta^2) ~ p^2/(24pi^2).
So we need the large sieve to give a bound smaller than p^2, which it does
(it gives ~p * polylog). This is PROMISING.

**Caveat:** The large sieve gives an L^2 average bound over all Farey points,
but we need a bound on a SINGLE sum. However, the Bombieri-Vinogradov
theorem (which is the arithmetic form of the large sieve) gives pointwise
bounds on average over moduli -- this might be enough.

### 4.5 Ramanujan Sum Expansion + Guth-Maynard

**Idea:** Our bridge identity gives sum cos(2*pi*p*f) = M(p) + 2 over
f in F_{p-1}. The Guth-Maynard framework bounds large values of
Dirichlet polynomials sum a_n n^{-it}.

Connection: via Perron's formula, sum cos(2*pi*p*f) over f with denom(f) = q
equals the Ramanujan sum c_q(p) = sum_{(a,q)=1} e(ap/q). These Ramanujan
sums are themselves values of Dirichlet polynomials:

  c_q(p) = sum_{d | gcd(p,q)} d * mu(q/d)

Summing over q <= p-1 with the displacement weight D(f):

  sum D * delta = sum_q sum_{a: (a,q)=1} D(a/q) * ({pa/q} - a/q)

This is a weighted sum of Ramanujan-type exponential sums, where the weights
come from the displacement D. The Guth-Maynard large values theorem could
bound how often the q-th component is large, giving control over the sum.

---

## 5. Recommended Attack Strategy

### Priority 1: Density-1 Theorem (HIGH confidence, publishable)

Use Guth-Maynard zero density estimate + explicit formula + Franel-Landau
to prove: DeltaW(p) < 0 for all primes p except a set of density zero.

This does NOT require proving R > -1/2 for all primes. It uses the
*averaged* control that zero density estimates provide.

**Concrete steps:**
1. Write the per-step discrepancy change via the explicit formula for
   sum mu(n)/n^s over n <= p
2. The exceptional set where this fails is controlled by zeros of zeta
   near sigma = 1
3. Guth-Maynard's improved zero density reduces the exceptional set size
4. Conclude: density-1 set of primes satisfies DeltaW(p) < 0

**Classification:** C2 (collaborative, publication grade). Uses standard
analytic number theory applied to our novel per-step quantity.

### Priority 2: Large Sieve Bound on R (MODERATE confidence)

Apply the large sieve inequality to bound |sum D * delta| directly.

**Concrete steps:**
1. Express sum(D * delta) via Ramanujan expansion
2. Apply large sieve to get |sum D*delta| << p * (log p)^A
3. Use known asymptotic sum(delta^2) ~ p^2 / (12*pi^2) to get R -> 0
4. For EFFECTIVE bound: need explicit constants in the large sieve

**Classification:** C1 (collaborative, minor novelty). Large sieve application
is standard; the novelty is applying it to the per-step quantity.

### Priority 3: Mollifier for Small Primes (LOW-MODERATE confidence)

For the small primes where R is furthest from 0 (the range p = 11 to ~100
where our computational proof stops and the asymptotic regime hasn't kicked
in), construct an explicit mollifier that kills the problematic contributions.

**Concrete steps:**
1. Identify which denominator classes contribute most to |sum D*delta|
2. Construct w(b) to suppress these
3. Verify computationally that the mollified sum has the right sign
4. Bound the mollifier error term

### Priority 4: Trace Method Adaptation (SPECULATIVE)

Adapt the sixth-power trace method to the discrete Farey setting. This would
require replacing Poisson summation with some discrete analogue (perhaps
the Selberg/Beurling extremal function method).

---

## 6. What Does NOT Transfer

### 6.1 The Phase Structure

Guth-Maynard critically exploit that their phases are e^{it log n} where
log n is a SMOOTH function of n. This allows Poisson summation and
stationary phase analysis. Our phases are e^{2*pi*i*a/b} where a/b runs
over Farey fractions -- these are ARITHMETICALLY structured, not smoothly
parameterized. The Poisson summation cancellation that is the heart of
Guth-Maynard does not directly apply.

### 6.2 The Continuous-to-Discrete Gap

Guth-Maynard work with a continuous parameter t in [0,T] and bound the
MEASURE of the superlevel set. We have a single discrete sum. Converting
from "how often is the sum large" to "this particular sum is small" requires
additional arguments (e.g., a zero-free region, not just a zero-density
estimate).

### 6.3 The Critical Exponent

Their breakthrough is at sigma = 3/4, which corresponds to Dirichlet
polynomial values of size N^{3/4}. Our problem concerns sums of size ~N^2
(the Farey discrepancy) where we need cancellation down to N^{1+epsilon}.
This is a DIFFERENT scaling regime from what Guth-Maynard address.

---

## 7. Key References

1. Guth & Maynard, "New large value estimates for Dirichlet polynomials,"
   Annals of Mathematics 203(2), 2026. arXiv:2405.20552.
2. Tao, "A computation-outsourced discussion of zero density theorems,"
   What's New blog, July 7, 2024.
3. Tao, "254A Notes 6: Large values of Dirichlet polynomials," 2015
   (background/course notes).
4. Franel, "Les suites de Farey et le probleme des nombres premiers,"
   Gottinger Nachrichten, 1924.
5. Dress, "Discrépance des suites de Farey," J. Théorie des Nombres de
   Bordeaux 11, 1999. (Exact discrepancy = 1/Q result.)
6. Guth, "New bounds for large values of Dirichlet polynomials,"
   MATRIX 2024 workshop slides.
7. Guth, "Large value estimates in number theory, harmonic analysis,
   and computer science," arXiv:2503.07410 (survey).

---

## 8. Bottom Line

The Guth-Maynard breakthrough is a powerful new tool in analytic number theory,
but it does NOT directly solve our problem. The most promising transfer is
INDIRECT: their improved zero density estimate, fed through the Franel-Landau
framework, could yield a **density-1 theorem** (DeltaW(p) < 0 for almost all
primes). This would be a genuine, publishable result.

For the COMPLETE result (all primes), the large sieve approach is more
promising than direct application of Guth-Maynard. The large sieve gives
bounds of the right ORDER (sum D*delta << p * polylog vs. sum delta^2 ~ p^2)
and does not require the continuous phase structure that Guth-Maynard exploit.

The honest assessment: Guth-Maynard is adjacent to our problem but addresses
a different scaling regime (sigma = 3/4 barrier vs. our need for effective
Franel-Landau bounds). Their techniques inspire new approaches (mollifiers,
trace methods, additive energy case splits) but do not plug in directly.
The density-1 result is the clear actionable target.
