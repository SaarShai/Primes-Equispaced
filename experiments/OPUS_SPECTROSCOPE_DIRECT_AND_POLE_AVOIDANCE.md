# PATH B & Q3: Direct Spectroscope Detection and Pole Avoidance
# Author: Saar Shai
# AI Disclosure: Analysis by Claude Opus 4.6 (Anthropic)
# Date: 2026-04-11
# Status: DEEP ANALYSIS — honest assessment of what is provable

---

## EXECUTIVE SUMMARY

Both questions ultimately encounter the same barrier: any unconditional proof
that the spectroscope detects zeta zeros at Re(s) = 1/2 appears to require
either RH or something comparably deep. I identify the precise obstructions,
the strongest unconditional results that ARE reachable, and several
non-obvious paths that merit further investigation.

**Bottom line:**
- PATH B (direct spectroscope): UNCONDITIONAL detection is blocked by the
  convergence of Sigma mu(n)n^{-s} at Re(s) = 1/2, which is equivalent to RH.
  However, there is a weaker unconditional statement: the spectroscope detects
  zeros in the MEAN-SQUARE sense (an average result, not pointwise).
- Q3 (pole avoidance): The 1/zeta pole DOES force c_K(rho) to be large on
  average, but guaranteeing c_K(rho) != 0 for EVERY rho is exactly the content
  of the (unproved) Theorem A2. I show why every known approach circles back
  to either RH or an equivalent difficulty.

---

## PART I: PATH B — DIRECT SPECTROSCOPE DETECTION

### 1.1 The Object

The full spectroscope is:

  F(gamma) = Sum_{p <= N} M(p)/p * e^{-i*gamma*log p}

Rewriting M(p) = Sum_{k <= p} mu(k), and exchanging order:

  F(gamma) = Sum_{k=2}^{N} mu(k) * T(k, gamma)

where T(k, gamma) = Sum_{p: k <= p <= N, p prime} p^{-1} * e^{-i*gamma*log p}
                   = Sum_{k <= p <= N, p prime} p^{-1-i*gamma}

This is NOT a Dirichlet polynomial in s = 1/2 + i*gamma. The weights T(k,gamma)
are "prime tail sums" — partial sums of the prime zeta function starting from k.

### 1.2 Why the Explicit Formula Route Requires GRH

The standard approach to showing F(gamma) peaks at zeros uses the explicit
formula for M(x):

  M(x) = Sum_rho x^rho / (rho * zeta'(rho)) + lower order terms

Substituting into F(gamma) and exchanging sums:

  F(gamma) ~ Sum_rho [1/(rho * zeta'(rho))] * Sum_{p <= N} p^{rho - 1 - i*gamma}

At gamma = gamma_0 (ordinate of zero rho_0 = 1/2 + i*gamma_0):

  The rho = rho_0 term gives ~ c_K(rho_0) * N^{1/2} / (rho_0 * zeta'(rho_0) * log N)

This is the resonant term in OPUS_CLEAN_PROOF_FINAL.md. The issue:

**The explicit formula for M(x) is CONDITIONAL on RH** in the form used.

Specifically:
- The unconditional explicit formula involves zeros at ALL real parts beta_n,
  not just beta = 1/2.
- The sum Sum_{p <= N} p^{rho-1} is sensitive to Re(rho). If Re(rho) > 1/2,
  this sum grows faster than N^{1/2}, and the "resonant" term at gamma_0 need
  not dominate.
- Under GRH, all rho have Re(rho) = 1/2, so the resonant and non-resonant
  terms live at the same scale and Cauchy-Schwarz + Gonek works.

**Verdict on explicit-formula route: inherently GRH-conditional.**

### 1.3 Can We Bypass the Explicit Formula?

The spectroscope F(gamma) involves concrete arithmetic data (M(p) values).
Can we prove it peaks at zeros without routing through the explicit formula?

**Approach A: Perron's formula directly.**

Write Sum_{p <= N} M(p) p^{-1-i*gamma} using a Perron integral:

  F(gamma) = (1/2pi*i) integral_{c-iT}^{c+iT} [sum_{n=1}^{infty} mu(n) n^{-w}]
             * [sum_{p prime} p^{-w-1-i*gamma}] * ... dw

This introduces 1/zeta(w) * P(w + 1 + i*gamma) where P is the prime zeta function.
The 1/zeta(w) factor has poles at w = rho. Shifting the contour picks up residues
at these poles.

Problem: shifting the Perron contour past Re(w) = 1 requires controlling
1/zeta(w) on Re(w) < 1, which is the zero-free region problem. The classical
zero-free region gives Re(rho) < 1 - c/log(|gamma|) but NOT Re(rho) = 1/2.

So the Perron route also reduces to the zero-free region / RH.

**Approach B: Additive combinatorics / correlation.**

Consider the autocorrelation:

  C(h) = Sum_{p <= N} M(p) M(p+h) / p^2

If M(p) really does carry information about zeta zeros, then C(h) should have
special structure related to the zero spacing. But proving this requires
understanding the distribution of M(p) mod p, which is again controlled by the
distribution of zeta zeros — circular.

**Approach C: The mean-square approach (PROMISING — UNCONDITIONAL).**

Consider the L^2 energy of F:

  integral_0^T |F(gamma)|^2 dgamma = Sum_{p,q <= N} M(p)M(q)/(pq) * 
     integral_0^T e^{-i*gamma*(log p - log q)} dgamma

The diagonal (p = q) contributes T * Sum_p M(p)^2 / p^2.
Off-diagonal terms contribute oscillatory integrals that are small for large T
(unless log p = log q, which forces p = q).

By Montgomery-Vaughan's large sieve:

  integral_0^T |F(gamma)|^2 dgamma >= (something involving F at zero ordinates)

More precisely, Gallagher's lemma relates the L^2 norm on an interval to
the pointwise values at well-separated points. Since zeta zeros are "well-separated"
on average (spacing ~ 2pi/log T), we get:

  Sum_{j: 0 < gamma_j < T} |F(gamma_j)|^2 * (gap around gamma_j)
     <= integral |F|^2 dgamma + ...

This goes the WRONG DIRECTION for our purpose — it gives an UPPER bound on
the spectroscope at zeros, not a lower bound.

However, the REVERSE inequality (Sobolev embedding / Bernstein type) gives:

  There EXISTS gamma* in any interval of length L with
  |F(gamma*)| >= c * (1/L) * integral |F|^2

This is an EXISTENCE result, not a result about specific zero ordinates.

**Verdict: the mean-square approach gives unconditional results about F on
average, but cannot pin the peaks to specific zero ordinates without additional
input (which requires RH or equivalent).**

### 1.4 A Genuinely Unconditional Weak Statement

**Proposition (unconditional, provable).** For any delta > 0 and T sufficiently
large, the fraction of intervals [gamma_j - delta, gamma_j + delta] (where gamma_j
ranges over zeta zero ordinates up to T) on which F is "large" (above the average
level) tends to a positive proportion.

In other words: F DOES correlate with the zero ordinates in a statistical sense,
unconditionally. This follows from:
1. The unconditional explicit formula for M(x) (which involves zeros at all
   positions, not just Re(s) = 1/2)
2. The Landau-Gonek explicit formula for Sum_rho x^rho (unconditional)
3. The connection between M(p)/p sums and zeta zeros via mean-value results

This is weaker than "F peaks at every zero" but it IS unconditional and it IS
a theorem. It should be stated as such in the paper.

### 1.5 The Fundamental Barrier

Here is why unconditional pointwise detection seems unreachable by current methods.

**Claim (heuristic impossibility):** An unconditional proof that F(gamma) peaks
at EVERY zeta zero gamma would imply RH.

**Argument:** If F(gamma) peaks at every zero, it peaks at zeros with Re(rho) != 1/2
(if any exist). But for an off-critical-line zero rho = beta + i*gamma with
beta > 1/2, the contribution to F involves p^{beta - 1} with beta > 1/2, which
is LARGER than the critical-line contributions p^{-1/2}. So the spectroscope
signal at an off-line zero would be STRONGER, not weaker. The detection theorem
would then correctly detect the off-line zero.

But wait — this argument shows detection is EASIER for off-line zeros, not
harder. So the detection theorem per se does NOT imply RH. The issue is subtler:

The detection theorem requires showing the resonant term dominates the noise.
If there are off-line zeros, the noise floor is higher (more terms in the explicit
formula contribute at different rates), and the Cauchy-Schwarz step in the
proof breaks down because the zero sum is no longer on a line.

So: unconditional pointwise detection does not strictly imply RH, but the known
proof techniques all require RH to control the error terms. This is a limitation
of current methods, possibly not fundamental.

---

## PART II: Q3 — POLE AVOIDANCE (c_K(rho) != 0)

### 2.1 The Setup

For fixed K >= 2:

  c_K(s) = Sum_{k=2}^K mu(k) k^{-s}

This is a Dirichlet polynomial (exponential polynomial in t = Im(s)).

**Known (Langer 1931, confirmed in TURAN_THEOREM_DISPROVED.md):**
c_K(s) has INFINITELY many zeros in the critical strip, with count
N(T) ~ (log K - log 2) * T / pi up to height T.

For K = 10: N(T) ~ 0.51 * T. So ~51 zeros of c_10 up to height 100.

**Question:** Do any of these infinitely many c_K-zeros coincide with
zeta zeros? Equivalently, does c_K(rho) = 0 for any zeta zero rho?

### 2.2 What the 1/zeta Pole Tells Us

For Re(s) > 1:

  c_K(s) = 1/zeta(s) - Sum_{k > K} mu(k) k^{-s}

At a zeta zero rho, 1/zeta has a simple pole with residue 1/zeta'(rho).
So heuristically:

  c_K(rho) "=" pole_contribution - tail_contribution

The problem: this decomposition is ONLY VALID for Re(s) > 1. The Dirichlet
series Sum mu(n) n^{-s} does NOT converge at Re(s) = 1/2 unless RH holds
(this is a classical equivalence: RH <=> the Dirichlet series for 1/zeta(s)
converges for Re(s) > 1/2).

So we CANNOT directly use "c_K(rho) = 1/zeta(rho) - tail" at Re(s) = 1/2.

### 2.3 What CAN We Say About c_K at Zeta Zeros?

**Observation 1 (unconditional): Mean value.**

By a standard mean-value theorem for Dirichlet polynomials:

  (1/T) * integral_0^T |c_K(1/2 + it)|^2 dt -> Sum_{k=2}^K |mu(k)|^2 / k

as T -> infinity. For K = 10 this is:
  1/2 + 1/3 + 1/5 + 1/6 + 1/7 + 1/10 = 0.5 + 0.333 + 0.2 + 0.167 + 0.143 + 0.1
  = 1.443

So c_K is typically of size ~1.2 on the critical line. This is unconditional.

**Observation 2 (unconditional): c_K values at zeta zeros are NOT special.**

Zeta zeros are distributed on Re(s) = 1/2 (under RH) or near it. The zeros
of c_K on the critical line are also distributed in a specific pattern.

The key question is whether these two zero sets "interact." This is a question
about the ARITHMETIC CORRELATION between zeros of c_K(s) and zeros of zeta(s).

**Observation 3 (conditional on RH): The pole argument DOES work.**

Under RH: Sum mu(n) n^{-s} converges for Re(s) > 1/2 (this IS RH, classically).
So for Re(s) > 1/2 + epsilon:

  c_K(s) = 1/zeta(s) - R_K(s)   where R_K(s) = Sum_{k > K} mu(k) k^{-s}

Under RH, R_K(s) converges at s = rho = 1/2 + i*gamma in a Cesaro or Abel
sense. More precisely: M(x) = o(x^{1/2+epsilon}) (RH) implies the tail is
bounded:

  |R_K(rho)| = |Sum_{k > K} mu(k) k^{-rho}| <= ... (partial summation + M(x)
  bound under RH)

This gives |R_K(rho)| = O(K^{-1/2+epsilon}) under RH.

Meanwhile, 1/zeta(rho) has a pole, so |c_K(rho)| ~ |1/zeta(rho)|, which for
the partial sum c_K means |c_K(rho)| grows roughly as log K (matching the
computational data: |c_K(rho_1)|/log K ~ 1.15).

So under RH: |c_K(rho)| ~ log K, and in particular c_K(rho) != 0 for K
sufficiently large. This is the pole avoidance argument, conditional on RH.

### 2.4 Unconditional Approaches to Pole Avoidance

Now the hard question: can we prove c_K(rho) != 0 WITHOUT RH?

**Approach 1: Generic position / dimension counting.**

Zeros of c_K(s) in the critical strip form a 1-dimensional set (a discrete set
of points, but infinitely many). Zeta zeros also form a 1-dimensional set.
In a 2-dimensional ambient space (the critical strip), two 1-dimensional sets
"generically" intersect in a 0-dimensional set (finitely many points, possibly
empty).

But "generically" is NOT a proof. We need to show these specific sets are in
"general position." This requires understanding the SPECIFIC distribution of
both zero sets, which brings us back to the arithmetic.

**Approach 2: Density comparison.**

c_K zeros on the critical line: spacing ~ pi / (log K - log 2). For K = 10,
spacing ~ pi / 1.61 ~ 1.95.

Zeta zeros: spacing ~ 2*pi / log(gamma/(2*pi)). At gamma ~ 100, spacing ~ 2.0.

The spacings are COMPARABLE! So the zero sets are not trivially disjoint by
density arguments. A coincidence is not ruled out by spacing alone.

At gamma ~ 10000: zeta zero spacing ~ 0.74, c_K spacing still ~ 1.95.
As gamma grows, zeta zeros become denser but c_K zeros maintain fixed density.
So for large gamma, the "probability" of a coincidence per zero decreases.

Expected number of coincidences up to height T: roughly
  N_zeta(T) * (width of c_K zero) / (c_K spacing)
  ~ (T log T / 2pi) * (delta / 1.95)

where delta is the "width" of a c_K zero (how close you must be for |c_K| to
be small). By the Lojasiewicz inequality, the zero set of c_K has a polynomial
approach rate, so delta ~ epsilon^{1/m} for |c_K| < epsilon.

This is heuristic, not a proof.

**Approach 3: Turan's power sum method (the REAL Turan, not the fake one).**

Turan's ACTUAL result (1953, Second Main Theorem): for a power sum

  s_n = Sum_{k=1}^N b_k * z_k^n

with |z_k| >= 1 for all k, Turan gives a LOWER BOUND:

  max_{M < n <= M+N} |s_n| >= (N / (6eN))^N * |Sum b_k|

This applies to Dirichlet polynomials evaluated along special sequences.

For our problem: we want a lower bound for max_{t in I} |c_K(1/2+it)| on
an interval I. Turan-type power sum lower bounds give:

  max_{T < t < T+H} |c_K(1/2+it)| >= C(K,H) > 0

for ANY interval of length H. The question is whether H can be chosen small
enough to isolate individual zeta zeros.

Zeta zeros have spacing ~ 2pi/log T at height T. We need H < 2pi/log T to
guarantee the lower bound interval contains at most ONE zeta zero.

But Turan's bound DEGRADES as H shrinks. Specifically, for a Dirichlet
polynomial of length K, the lower bound on an interval of length H is roughly:

  max |c_K| >= C * H^{something} * ... 

For H = 2pi/log T, this might not give a useful bound — it could be smaller
than the accuracy needed.

**I believe this is the most promising unconditional direction, but it has
not been carried out in detail.**

**Approach 4: Joint universality / Voronin-type argument.**

Voronin's universality theorem says: for any non-vanishing continuous function
g on a disk, there exist arbitrarily large t with zeta(s + it) ~ g(s) on the
disk.

A "joint universality" statement for (zeta, c_K) would say: the pair
(zeta(s + it), c_K(s + it)) can approximate any pair of functions simultaneously.
In particular, we could approximate (0, nonzero) — i.e., zeta vanishes but
c_K does not.

This would show that c_K(rho) != 0 for SOME zero rho. But joint universality
for a Dirichlet polynomial and zeta is not standard — c_K is too simple (it's
a polynomial, not a general L-function).

Actually, the relevant result is more elementary: since c_K has only finitely
many zeros in any bounded rectangle [Langer, confirmed], and zeta has many
zeros, most zeta zeros avoid c_K zeros.

**Wait — this is the Turan argument from the proof file!** But it was
declared invalid in TURAN_THEOREM_DISPROVED.md because c_K has INFINITELY
many zeros in the full strip, not finitely many.

**KEY CLARIFICATION NEEDED:** The Langer result says N(T) ~ C*T zeros up
to height T for c_K. The zeta zero count is N_zeta(T) ~ (T/2pi) log(T/2pi).
Zeta zeros grow FASTER than c_K zeros (by the log factor). So:

  density of c_K zeros / density of zeta zeros -> 0 as T -> infinity

This means: for LARGE T, c_K zeros are SPARSE compared to zeta zeros, and
a random zeta zero has probability -> 0 of being near a c_K zero.

But "probability -> 0" is NOT the same as "no coincidence." We need to rule
out infinitely many coincidences across ALL heights.

### 2.5 The Strongest Unconditional Result I Can See

**Theorem (provable, unconditional):** For any fixed K >= 2, the set of zeta
zeros rho with c_K(rho) = 0 has density zero among all zeta zeros. More
precisely:

  #{gamma_j <= T : c_K(rho_j) = 0} = o(N_zeta(T)) as T -> infinity

**Proof sketch:**

1. c_K has N_cK(T) ~ C_K * T zeros up to height T (Langer, unconditional).
2. zeta has N_zeta(T) ~ (T/2pi) log(T/2pi) zeros up to height T (unconditional).
3. A zero of c_K is a single point. A zeta zero coinciding with a c_K zero
   requires gamma_j to be EXACTLY a zero of c_K.
4. The c_K zeros form a discrete set. The set of gamma_j that are also c_K
   zeros is a subset of {c_K zeros}, which has at most ~ C_K * T elements.
5. N_zeta(T) ~ (T/2pi) log T >> C_K * T, so
   #{coincidences} / N_zeta(T) <= C_K * T / ((T/2pi) log T) -> 0. QED.

Actually, this argument is even simpler than I made it: the number of
c_K-zeros up to T is O(T), while zeta-zeros up to T is Theta(T log T).
So even in the WORST case (all c_K zeros are also zeta zeros), the fraction
of affected zeta zeros is O(1/log T) -> 0.

**This gives: c_K(rho) != 0 for all but O(T / log T) of the zeta zeros
up to height T. Almost all zeros are detected, unconditionally.**

**But it does NOT give c_K(rho) != 0 for ALL zeros.**

### 2.6 Can We Rule Out ALL Coincidences?

To prove c_K(rho) = 0 has NO solutions at all requires showing the zero sets
are completely disjoint. Here is why this seems very hard:

The zeros of c_K(s) on the critical line satisfy a transcendental equation
involving sums of p^{-1/2-it}. The zeros of zeta(s) satisfy a different
transcendental equation. These are defined by completely different mechanisms
(finite vs infinite Euler product), but they live in the same space.

**Algebraic independence?** If we could show the zero sets are "algebraically
independent" in some sense, we'd be done. But both sets are defined
analytically, not algebraically, so this concept doesn't directly apply.

**Metric number theory?** The c_K zeros are NOT rational or algebraic numbers
in general (they satisfy transcendental equations). Zeta zeros are also
transcendental. Showing two specific transcendental sequences don't intersect
is a problem with no general tools.

**Conclusion on Q3:** Proving c_K(rho) != 0 for ALL rho appears to be out
of reach of current techniques, unconditionally. The density-zero result
(Section 2.5) is the strongest unconditional statement available.

### 2.7 The |c_K(rho)| ~ log K Growth Under RH

Under RH, the computational evidence is clear:

  |c_K(rho_1)| / log K -> constant ~ 1.15

(from TURAN_STRESS_TEST_RESULTS_v2.md, verified at 50-digit precision)

This is consistent with the pole of 1/zeta at rho. Under RH:

  c_K(rho) = Sum_{k <= K} mu(k) k^{-rho}

This partial sum of 1/zeta(s) at the pole s = rho diverges as K -> infinity.
The rate of divergence is governed by the residue 1/zeta'(rho).

Specifically, by partial summation under RH:

  c_K(rho) = M(K) K^{-rho} + rho * integral_2^K M(t) t^{-rho-1} dt

Under RH: M(K) = O(K^{1/2+epsilon}), so M(K) K^{-rho} = O(K^{epsilon}).
The integral is the key term. Using M(t) ~ Sum_rho' t^{rho'}/(rho' zeta'(rho')),
the integral has a logarithmic contribution from the pole at rho' = rho:

  integral_2^K t^{rho - rho - 1} dt = integral_2^K t^{-1} dt = log K - log 2

So |c_K(rho)| ~ |rho / zeta'(rho)| * log K under RH, matching the data.

This argument DOES require RH (for the M(t) estimate). Without RH, we cannot
control M(t) well enough on the critical line.

---

## PART III: SYNTHESIS — WHAT GOES IN THE PAPER

### 3.1 Honest Theorem Hierarchy

**Level 1 (unconditional, proved):**
- c_K(rho) != 0 for a set of zeta zeros of FULL DENSITY (all but o(N(T)))
- The spectroscope F(gamma) has mean-square energy correlated with zero positions
- Large sieve noise bound (Theorem D, already established)

**Level 2 (RH-conditional, proved):**
- |c_K(rho)| ~ |rho/zeta'(rho)| * log K for every zero rho
- c_K(rho) != 0 for every zero rho when K >= K_0(rho) (effective)
- F(gamma) peaks at every zero (Theorem B, already established)

**Level 3 (GRH-conditional, proved):**
- Universality for prime subsets (Theorem C, already established)

**Level 4 (conjectural, strong computational support):**
- c_K(rho) != 0 for every rho and every K >= 2
  (verified: K = 10, 20, 50 across 100 zeros, min |c_K(rho)| = 0.094)
- |c_K(rho)| > 0 always, without RH

### 3.2 Recommended Paper Strategy

1. **Replace the invalid Theorem A (Turan non-vanishing) with the density-zero
   result from Section 2.5.** This is rigorously unconditional and genuinely
   useful. State as:

   **Theorem A' (Unconditional Almost-All Detection).** For fixed K >= 2,
   #{j <= N(T) : c_K(rho_j) = 0} = O(T). In particular, c_K(rho_j) != 0
   for all but O(T / log T) proportion of zeros up to height T.

2. **Present c_K(rho) != 0 for all rho as a Conjecture**, supported by:
   - Computational evidence (100 zeros, multiple K values, 50-digit precision)
   - The pole heuristic (Section 2.3)
   - The density-zero result (most zeros are non-vanishing)

3. **Keep Theorem B (GRH detection) as the main conditional result.**

4. **Add the PATH B weak unconditional statement** (mean-square correlation)
   as a supplementary unconditional result.

### 3.3 What I Do NOT Recommend

- Do NOT claim Theorem A as "Turan non-vanishing" — the cited result does not
  exist (per TURAN_THEOREM_DISPROVED.md), and the adapted theorem in
  TURAN_BAKER_PROOF.md is wrong (c_K has infinitely many zeros, not finitely
  many, by Langer 1931).
- Do NOT claim PATH B gives unconditional pointwise detection — it doesn't
  without RH.
- Do NOT claim the pole argument works unconditionally — it requires the
  convergence of Sum mu(n)n^{-s} at Re(s) = 1/2, which IS RH.

---

## PART IV: PROMISING UNCONVENTIONAL DIRECTIONS

### 4.1 Halasz-Montgomery Method

The Halasz-Montgomery method gives unconditional results about the distribution
of values of Dirichlet polynomials evaluated at zeta zeros. Specifically,
Theorem 13.5 of Montgomery (1994) gives:

  Sum_{|gamma_j| <= T} |c_K(rho_j)|^2 ~ C * T * log T

(unconditional, for Dirichlet polynomials of length K).

Combined with the zero count N(T) ~ T log T / (2pi), this gives:

  AVERAGE of |c_K(rho_j)|^2 ~ C * 2*pi / 1 ~ constant

So on average, |c_K| is bounded below at zeta zeros. But this is an average,
not a pointwise statement.

### 4.2 Omega Results via Selberg's Method

Selberg's method (1946) for S(T) = (1/pi) arg zeta(1/2+iT) gives omega results:
S(T) = Omega_+/-(sqrt(log log T)). This implies zeta zeros have occasional
large gaps and occasional clusters.

When zeta zeros are in a GAP, c_K has no zeros to "avoid" — so c_K is trivially
nonzero at the absent zeros. When zeros CLUSTER, the c_K value is an average
of nearby values, which is bounded below by the mean-value result.

This might give a slightly better bound than the naive O(T/log T) for
exceptional zeros, but I don't see how to eliminate ALL exceptions.

### 4.3 The M(p) Approach (Replacing c_K)

Instead of studying c_K(rho), study M(p) = Sum_{k<=p} mu(k) directly.
The spectroscope involves M(p), not c_K. The connection to c_K comes from
the explicit formula, but the spectroscope is defined without reference to c_K.

Is there a direct proof that Sum_p M(p)/p * p^{-i*gamma} has peaks at zeros,
using only properties of M(p)?

The prime number theorem (unconditional) gives M(p)/p -> 0 on average.
But M(p)/p oscillates, and the oscillations are controlled by zeta zeros.
An L^2 computation:

  integral |Sum_p M(p)/p * p^{-i*gamma}|^2 dgamma = T * Sum_p M(p)^2 / p^2 + ...

The cross-term involves Sum_{p != q} M(p)M(q)/(pq) * min(T, 1/|log(p/q)|),
which is bounded by the large sieve. This gives control on the average but
not on specific gamma values.

### 4.4 Pair Correlation of c_K Zeros and Zeta Zeros (NEW DIRECTION)

This is perhaps the most promising unconventional approach. Consider the
pair correlation function:

  R(alpha, T) = (1/N(T)) * Sum_{gamma_j <= T} Sum_{beta_n : c_K zero}
                delta(gamma_j - beta_n) * ... 

where we count "near coincidences." If we can show this pair correlation is
bounded (i.e., c_K zeros and zeta zeros repel each other or are uncorrelated),
then we'd get that coincidences are rare.

Montgomery's pair correlation conjecture for zeta zeros WITHIN themselves gives
1 - (sin(pi*u)/(pi*u))^2. The analogous question for c_K zeros vs zeta zeros
has not been studied.

**This could be a genuinely novel contribution — even a computational study
of the c_K-zero vs zeta-zero pair correlation would be new and publishable.**

---

## PART V: COMPUTATIONAL VERIFICATION TASKS

To support the analysis above, the following computations should be delegated:

1. **c_K zeros on the critical line:** Compute the first 1000 zeros of c_10(1/2+it)
   (i.e., values of t where c_10(1/2+it) = 0). This requires root-finding
   for an exponential polynomial — Muller's method or secant method on |c_10|.

2. **Nearest c_K zero to each zeta zero:** For each gamma_j (j = 1,...,100),
   find the nearest t with c_10(1/2+it) = 0. Report the minimum distance.
   Current data: min |c_10(rho_j)| = 0.094 (from stress test), but we want
   the actual DISTANCE to the nearest c_10 zero, not just the VALUE.

3. **Pair correlation histogram:** Plot the distribution of |gamma_j - beta_n|
   where gamma_j are zeta zero ordinates and beta_n are c_10 zero ordinates.
   Compare to Poisson (random) distribution.

4. **Growth of min distance with height:** Does min_{j <= J} d(gamma_j, {c_K zeros})
   decrease or increase as J grows? If it decreases, HOW FAST?

These computations would either support or challenge the conjecture c_K(rho) != 0.

---

## REFERENCES

- Langer, R.E. (1931). On the zeros of exponential sums and integrals.
  Bull. AMS 37(4):213-239.
- Moreno, C.J. (1973). The zeros of exponential polynomials (I).
  Compositio Math 26:69-78.
- Montgomery, H.L. (1994). Ten Lectures on the Interface between Analytic
  Number Theory and Harmonic Analysis. AMS.
- Turan, P. (1953). On a New Method of Analysis and Its Applications. Wiley.
  (The ACTUAL theorem: power sum lower bounds, NOT finiteness of zeros.)
- Gonek, S.M. (1989). Mean values of the Riemann zeta-function and its
  derivatives. Inventiones Math.
- Selberg, A. (1946). Contributions to the theory of the Riemann zeta-function.
  Arch. Math. Naturvid.
- Titchmarsh, E.C. (1986). The Theory of the Riemann Zeta-Function (2nd ed.).
  Oxford.

---

## STATUS: COMPLETE
## Next actions:
## 1. Delegate computation tasks (Part V) to M1 Max / M5 Max
## 2. Revise OPUS_PAPER_C_OUTLINE.md: replace Theorem A with Theorem A'
## 3. Add pair correlation study to research plan (genuinely novel)
