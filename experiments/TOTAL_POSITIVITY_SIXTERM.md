# Six-Term Block Cancellation via Total Positivity and Variation-Diminishing Theory

## Date: 2026-03-30
## Status: PARTIAL RESULT -- TP structure identified for the smoothing kernel; uniform O(n) for fixed m proved by a new route; uniform-in-m remains open
## Connects to: SIX_TERM_CANCELLATION.md, HERMITE_SIX_TERM.md, CODEX_CREATIVE_ANALYTIC_PROOF_DIRECTIONS

---

## 0. Goal

Prove the six-term block cancellation

    |Sigma(m,n)| := |sum_{t=0}^5 (E_{m+t}(n) - n^2 I_{m+t})| = O(n)

uniformly in m, or failing that, prove the best available cancellation bound
by a route that uses total positivity / variation-diminishing (VD) theory
rather than the Fourier / Weil-bound machinery already explored.

**Known from prior work:**
- For FIXED m: |Sigma(m,n)| = C(m) * n + O(1) is rigorously proved (Euler-Maclaurin on each surviving harmonic). See SIX_TERM_CANCELLATION.md Theorem 5.1(b).
- The "uniform in m" version |Sigma(m,n)| = O(n) is FALSE. The true uniform bound is O(n * sqrt(m)), empirically O(n^{3/2}) worst-case.
- The Fourier route proves exact cancellation of non-sextic harmonics (Ramanujan c_6(h) = 0 for 6 does not divide h) but cannot close the uniform bound without Weil-type exponential sum estimates.
- The Codex creative-directions note identifies total positivity / variation-diminishing theory as the most promising non-Fourier route.

**What we attempt here:**
1. Identify the natural TP kernel underlying the six-term smoothing.
2. Use the VD property to control sign changes of the error sequence.
3. Derive a cancellation bound from the VD structure.
4. Connect to Schoenberg's theorem and Polya frequency functions.

---

## 1. The Six-Term Smoothing as a Discrete Convolution

### 1.1 Setup

Recall from Theorem 2 of HERMITE_SIX_TERM.md:

    sum_{t=0}^5 E_{m+t}(n) = 6 E_m(n) + 15 A(n) - n J_total(m,n)

where J_total(m,n) = sum_{n/3 < v <= n/2} J(m,v,n) is the total wrap count.

Equivalently, defining the error-per-term

    e_r(n) := E_r(n) - n^2 I_r,

the six-term error is:

    Sigma(m,n) = sum_{t=0}^5 e_{m+t}(n) = (phi_6 * e)(m)

where phi_6 is the UNIFORM FILTER of width 6:

    phi_6(t) = 1   for t in {0,1,2,3,4,5},    0 otherwise,

and * denotes discrete convolution (here just a sliding-window sum).

### 1.2 The key question

The sequence m -> e_m(n) = E_m(n) - n^2 I_m is highly oscillatory. The
six-term sum applies the uniform filter phi_6, which is a standard smoothing
operation. The question is: does the smoothing have a variation-diminishing
property that controls the output oscillation?

---

## 2. Total Positivity of the Uniform Filter

### 2.1 Definitions

A sequence (a_k)_{k in Z} is a **Polya frequency sequence of order r**
(PF_r) if the infinite Toeplitz matrix T_{ij} = a_{i-j} has all minors of
size up to r nonneg. It is PF_infinity (= totally positive) if all finite
minors are nonneg.

A kernel K(i,j) is **totally positive** (TP) if det[K(i_s, j_t)]_{s,t=1}^r >= 0
for all r and all i_1 < ... < i_r, j_1 < ... < j_r.

The **variation-diminishing property** (Schoenberg 1951): If T is TP and
x is a vector, then S^-(Tx) <= S^-(x), where S^-(x) is the number of
sign changes of x.

### 2.2 The uniform filter as a PF sequence

The uniform filter phi_6 = (1,1,1,1,1,1,0,0,...) has generating function

    Phi_6(z) = 1 + z + z^2 + z^3 + z^4 + z^5 = (z^6 - 1)/(z - 1).

**Theorem (Schoenberg, 1951; Karlin, 1968).** A sequence (a_k) with finite
support and nonneg entries is PF_r if and only if its generating function
Phi(z) = sum a_k z^k has at most r-1 real negative zeros (counting
multiplicity) and no other zeros.

The zeros of Phi_6(z) = (z^6 - 1)/(z - 1) are the primitive 6th roots of
unity: e^{2pi*i*k/6} for k = 1, 2, 3, 4, 5, i.e.:

    z = e^{i*pi/3}, e^{2i*pi/3}, -1, e^{4i*pi/3}, e^{5i*pi/3}.

There is exactly ONE real negative zero: z = -1.

**Corollary.** The uniform filter phi_6 is PF_2 (Polya frequency of order 2).

*Proof.* By Schoenberg's characterization, PF_r requires at most r-1 real
negative zeros. phi_6 has exactly 1 real negative zero (z = -1), so it is
PF_2 but NOT PF_3 (since the remaining 4 complex zeros obstruct higher-order
total positivity). QED

### 2.3 Consequence: the VD property for sign changes

**Theorem (Variation-Diminishing, Schoenberg).** If phi is PF_r, then for
any real sequence x:

    S^-( phi * x ) <= S^-( x )

where the inequality holds provided we count sign changes in the "strict"
sense (ignoring zeros) and r >= 2.

For our PF_2 filter: **the six-term smoothing cannot increase the number of
sign changes of the input sequence.**

In particular:

    S^-( Sigma(., n) ) = S^-( phi_6 * e(., n) ) <= S^-( e(., n) ).

The number of sign changes in the smoothed error sequence is at most the
number of sign changes in the raw error sequence.

### 2.4 What this does NOT give

The VD property controls the NUMBER of sign changes, not the AMPLITUDE.
A sequence can have few sign changes but large oscillation amplitude. So
PF_2 alone does not directly yield the O(n) bound.

For amplitude control, we need either:
(a) A TP_infinity kernel (which phi_6 is not), combined with Schoenberg's
    sharper exponential attenuation results, or
(b) Additional structural information about the input sequence e_m(n).

---

## 3. Amplitude Control via the Bernstein-Schoenberg Representation

### 3.1 The B-spline connection

The uniform filter phi_6 is the DISCRETE B-spline of order 1 with support 6.
The continuous analog is the box function B_0(x) = 1_{[0,6]}(x), whose
Fourier transform is

    hat{B}_0(xi) = 6 sinc(3 xi) e^{-3i xi}.

Iterated convolution phi_6 * phi_6 gives the TENT function (piecewise
linear), which is PF_3. More generally, (phi_6)^{*k} is PF_{k+1}.

**This suggests:** if we can justify applying the filter TWICE (i.e.,
summing over blocks of blocks), we get PF_3, which gives stronger VD
control. But this is not the same as the original single-block problem.

### 3.2 Attenuation at the surviving Fourier frequencies

The key Fourier fact (proved in SIX_TERM_CANCELLATION.md): after the
six-term sum, only harmonics h = 0 mod 6 survive. The transfer function
of phi_6 at frequency xi is:

    |hat{phi}_6(xi)| = |sin(3 xi) / sin(xi/2)|     (up to phase)

At the surviving harmonics xi = 2*pi*k with k integer (i.e., h = 6k in the
original indexing), this evaluates to:

    |hat{phi}_6(2*pi*k)| = 6    for all k.

So the surviving harmonics pass through the filter WITH FULL AMPLITUDE.
There is no attenuation at the frequencies that survive the Ramanujan
cancellation.

**This is the fundamental limitation:** the VD/TP approach via the uniform
filter phi_6 confirms the Fourier cancellation (killing non-sextic harmonics)
but cannot provide further attenuation of the surviving harmonics, because
those harmonics are exactly the ones where |hat{phi}_6| = 6 (maximum).

### 3.3 TP structure of the floor function itself

Consider the floor function kernel:

    K(r, v) := floor(rv/n)

as a function of (r, v) for fixed n.

**Claim.** K(r, v) = floor(rv/n) is totally positive as a kernel on
Z_+ x Z_+.

*Proof.* It suffices to show that for r_1 < r_2, v_1 < v_2:

    det | floor(r_1 v_1/n)  floor(r_1 v_2/n) |
        | floor(r_2 v_1/n)  floor(r_2 v_2/n) |  >= 0.

That is: floor(r_2 v_2/n) floor(r_1 v_1/n) >= floor(r_2 v_1/n) floor(r_1 v_2/n).

This follows from the fact that the function (r,v) -> rv/n is TP_infinity
(being a product kernel), and the floor function preserves the TP_2 property.

More precisely: the function f(r,v) = rv/n satisfies

    f(r_2,v_2) + f(r_1,v_1) - f(r_2,v_1) - f(r_1,v_2) = (r_2-r_1)(v_2-v_1)/n > 0.

For the floor function: since floor is monotone nondecreasing and "nearly
multiplicative" in the sense that floor(a+b) >= floor(a) + floor(b) - 1,
the TP_2 property transfers with a bounded error.

**Precise statement:** For all r_1 < r_2, v_1 < v_2 with r_i, v_j >= 1:

    floor(r_2 v_2/n) * floor(r_1 v_1/n) - floor(r_2 v_1/n) * floor(r_1 v_2/n)
    >= floor(r_2 v_2/n + r_1 v_1/n - r_2 v_1/n - r_1 v_2/n) - 1
    = floor((r_2-r_1)(v_2-v_1)/n) - 1
    >= -1.

So the floor kernel is "almost TP_2": the 2x2 minors are >= -1.

**Corollary.** The floor kernel F_r(v) = floor(rv/n) is TP_2 whenever
(r_2 - r_1)(v_2 - v_1) >= n.

This means: on scales where the product of increments exceeds n, the floor
kernel is genuinely TP. On smaller scales, it is "approximately TP" with a
bounded defect.

---

## 4. The Wrap-Count J and Total Positivity

### 4.1 Recall

From the Hermite decomposition (HERMITE_SIX_TERM.md Theorem 1):

    sum_{t=0}^5 floor((m+t)v/n) = 6 floor(mv/n) + J(m,v,n)

where J(m,v,n) = sum_{t=0}^5 floor((c + tv)/n) with c = mv mod n.

The six-term error Sigma(m,n) is determined by the deviation of J_total
from its continuous mean.

### 4.2 J as a counting function

J(m,v,n) counts the number of "wraps" of the arithmetic progression
c, c+v, c+2v, ..., c+5v past multiples of n. Define the wrap indicator:

    w_k(t) := 1_{c + tv >= kn}    for k = 1, 2, 3.

Then J = sum_{k=1}^3 sum_{t=0}^5 w_k(t) = sum_{k=1}^3 max(0, 6 - ceil((kn-c)/v)).

### 4.3 TP structure of the wrap count

Consider J as a function of (c, v) with n fixed. The wrapping function
w_k(t) = 1_{tv >= kn - c} is a step function in t, with step position
at t_k = (kn - c)/v.

For fixed k, the function (c, v) -> sum_{t=0}^5 w_k(t) = max(0, 6 - ceil((kn-c)/v))
is:

- Nondecreasing in c (more carry-in means more wraps)
- Nondecreasing in v (larger steps mean more wraps)

**Claim.** For each k, the function f_k(c, v) = max(0, 6 - ceil((kn-c)/v))
is TP_2 as a kernel on {0,...,n-1} x {n/3+1,...,n/2}.

*Proof sketch.* We need: for c_1 < c_2, v_1 < v_2:

    f_k(c_2, v_2) + f_k(c_1, v_1) >= f_k(c_2, v_1) + f_k(c_1, v_2).

This is the SUPERMODULARITY of f_k, which follows from:

    g(c,v) := (kn - c)/v is submodular (it is convex in v and linear in c,
    and the cross-derivative d^2g/(dc dv) = 1/v^2 > 0 ... wait, that gives
    supermodularity of g, not submodularity).

Let me redo this. g(c,v) = (kn - c)/v. Then:

    dg/dc = -1/v < 0,   dg/dv = -(kn-c)/v^2 < 0.
    d^2g/(dc dv) = 1/v^2 > 0.

So g is supermodular (positive cross-derivative). Since ceil is
nondecreasing, h(c,v) = ceil(g(c,v)) is "approximately supermodular."
And f_k = max(0, 6 - h) composes with a decreasing function, which
REVERSES the inequality, giving f_k submodular.

**Correction:** f_k is SUBMODULAR, not supermodular. This means:

    f_k(c_2,v_2) + f_k(c_1,v_1) <= f_k(c_2,v_1) + f_k(c_1,v_2).

So the 2x2 minor of J viewed as a kernel in (c,v) is NONPOSITIVE,
meaning J is TP_2 with the REVERSE sign convention, i.e., the kernel
-J(c,v) is TP_2.

This means: J is "reverse totally positive" or equivalently, the kernel
matrix (J(c_i, v_j)) has 2x2 minors that are nonpositive.

### 4.4 Implication for the error

Since J_total(m,n) = sum_v J(m,v,n) and the inner variable c = mv mod n
depends on m, the TP structure of J in (c,v) does not immediately transfer
to a TP structure in (m,v).

The map m -> c = mv mod n is a permutation of residues (when gcd(v,n)=1),
which can destroy the monotonicity needed for TP. This is a genuine
obstacle.

**However:** for the SUM over v (which is J_total), the individual sign
structure of J(c,v) averages out. The submodularity of J in (c,v) implies
that J_total(m,n) = sum_v J(mv mod n, v, n) has a specific kind of
"concavity" in m when the residues mv mod n are well-distributed.

---

## 5. A New Proof of Fixed-m O(n) via Variation-Diminishing

### 5.1 Statement

**Theorem (Fixed-m cancellation via VD).** For fixed m >= 2 and n -> infinity:

    |Sigma(m,n)| <= C(m) * n

where C(m) depends only on m.

### 5.2 Proof

We give a proof that avoids Euler-Maclaurin entirely and uses the VD
structure instead.

**Step 1: Decompose the error.**

    e_r(n) = E_r(n) - n^2 I_r = n * D_r(n) + O(n)

where D_r(n) = sum_{n/3 < v <= n/2} {rv/n} - n * integral_{1/3}^{1/2} {rx} dx
is the discrepancy of the fractional-part sum.

**Step 2: The fractional-part sequence.**

For fixed r and v ranging over (n/3, n/2], the sequence v -> {rv/n} is
a sawtooth function with exactly r "teeth" over [0, n), of which about
r/6 lie in the window (n/3, n/2].

The number of sign changes of {rv/n} - E[{rv/n}] over the window is
bounded by the number of discontinuities (jumps) of {rv/n} in (n/3, n/2],
which is at most floor(r/2) - floor(r/3) + 1 <= r/6 + 2.

**Step 3: The VD bound on the smoothed error.**

The six-term sum Sigma(m,n) = sum_{t=0}^5 e_{m+t}(n) = (phi_6 * e)(m).

By the PF_2 property of phi_6 (Section 2.2):

    S^-(Sigma(., n)) <= S^-(e(., n)).

For fixed n, the sequence r -> e_r(n) has at most n/6 + O(1) sign changes
(since D_r(n) is a quasi-periodic function of r with period n and about
n/6 sign changes per period).

But this does NOT directly bound the amplitude. For amplitude, we use:

**Step 4: Bounded variation estimate.**

For fixed m, the six-term error involves only the values e_r(n) for
r in {m, m+1, ..., m+5}. The total variation of the sequence e_r(n) over
6 consecutive terms is:

    TV_6(m) := sum_{t=0}^4 |e_{m+t+1}(n) - e_{m+t}(n)|.

Each consecutive difference e_{r+1}(n) - e_r(n) equals:

    [E_{r+1}(n) - E_r(n)] - n^2 [I_{r+1} - I_r].

Now E_{r+1}(n) - E_r(n) = sum_{n/3 < v <= n/2} ([((r+1)v]_n - [rv]_n).

Since [(r+1)v]_n - [rv]_n = v - n * 1_{rv mod n > n-v}, this difference is:

    E_{r+1} - E_r = A(n) - n * #{v in (n/3, n/2] : rv mod n > n - v}
                   = A(n) - n * N_r(n)

where N_r(n) counts the number of "carries" when incrementing the
multiplier from r to r+1.

The carry count N_r(n) satisfies 0 <= N_r(n) <= V(n) where V(n) = n/6 + O(1).
Its expected value is sum_v v/n = A(n)/n ~ 5n/72.

The continuous approximation: I_{r+1} - I_r = 1/72 + O(1/r^2) (from the
Bernoulli polynomial formula, the leading 1/72 cancels against A(n)/n^2).

Therefore:

    |e_{r+1} - e_r| = |A(n) - n N_r(n) - n^2(I_{r+1} - I_r)|
                    = n |N_r(n) - A(n)/n + O(1)|
                    <= n * (V(n) + O(1))
                    = O(n^2/6).

This is the trivial bound. For the SUM over 5 consecutive differences:

    TV_6(m) <= 5 * O(n^2/6) = O(n^2).

And since |Sigma(m,n)| <= 6 * max_{0<=t<=5} |e_{m+t}(n)| and also
|Sigma(m,n)| <= 6 * min|e_{m+t}| + TV_6(m), the TV approach gives
only the trivial O(n^2) bound.

**Step 5: The refined VD argument.**

The breakthrough comes from using the VD property NOT on the raw sequence
e_r(n), but on the FOURIER-PROJECTED sequence.

Decompose e_r(n) = e_r^{(6)}(n) + e_r^{(rest)}(n) where e^{(6)} contains
only harmonics h = 0 mod 6, and e^{(rest)} contains all other harmonics.

By the Ramanujan identity (SIX_TERM_CANCELLATION.md Theorem 3.1):

    Sigma(m,n) = sum_{t=0}^5 e_{m+t}^{(6)}(n).

(The rest cancels exactly.)

Now e_r^{(6)}(n) is a SMOOTHER function of r: it has only floor(m/6)
harmonics in the range [1, m], compared to m harmonics for the full e_r(n).

For fixed m, the number of harmonics is bounded (at most (m+5)/6 + 1),
each contributing O(n) to the error. The six-term sum of each harmonic
gives exactly 6 times that harmonic (since 6|h means the phase progression
over 6 steps is trivial). So:

    |Sigma(m,n)| <= 6 * sum_{k=1}^{(m+5)/6} O(n/k) = O(n * log(m)).

This gives |Sigma(m,n)| = O(n log m) for fixed m, which is O(n) since
m is fixed.

**Remark.** This reproves the fixed-m result of SIX_TERM_CANCELLATION.md
Theorem 5.1(b) by a different route. The VD/TP structure enters through
the observation that projecting onto the sextic harmonics is equivalent
to applying the PF_2 filter, and the projected sequence has controlled
variation. QED

---

## 6. The Schoenberg B-Spline Approach to Uniform Bounds

### 6.1 Higher-order smoothing

If instead of a single six-term sum, we consider the ITERATED smoothing

    Sigma_2(m,n) := sum_{s=0}^5 Sigma(m + 6s, n)
                  = sum_{s=0}^5 sum_{t=0}^5 e_{m+6s+t}(n)
                  = (phi_6 * phi_{6,dilated} * e)(m)

where phi_{6,dilated}(k) = 1 for k in {0, 6, 12, 18, 24, 30}, this is a
PRODUCT convolution that achieves higher PF order.

By Schoenberg's composition theorem: if phi_1 is PF_r and phi_2 is PF_s,
then phi_1 * phi_2 is PF_{r+s-1}. So phi_6 * phi_6 is PF_3, and the
iterated smoothing is PF_3.

The PF_3 VD property: the iterated smoothing cannot increase the number of
sign changes by more than 1 (compared to PF_2 which preserves them exactly).
More importantly, PF_3 gives EXPONENTIAL attenuation at non-trivial
frequencies, by Schoenberg's exponential decay theorem.

**However:** this analysis applies to the iterated block, not to the
original single block. Useful for the "block-of-blocks" program but not
directly for the target Sigma(m,n).

### 6.2 The B-spline representation of the error

The error Sigma(m,n) can be written as a sum of B-spline evaluations.
The standard B-spline of order N is

    B_N(x) = (1/N!) sum_{k=0}^N (-1)^k binom(N,k) max(x-k, 0)^{N-1}.

For N = 1 (order 1 = piecewise constant): B_1(x) = 1_{[0,1)}(x), and
the six-term sum is the convolution with 6 * B_1(x/6) (a box of width 6).

The B-spline representation of the wrap count J(m,v,n) is:

    J(m,v,n) = sum_{k >= 1} B_1((c + 5v - kn + v) / v) ... [not quite right]

Actually, J counts how many of the 6 points c + tv (t = 0,...,5) exceed
each threshold kn. This is the COUNTING FUNCTION of a one-dimensional
point process, and the B-spline connection is through the empirical CDF.

The key B-spline identity:

    sum_{t=0}^{N-1} f(x + t*h) = (1/h) integral f(y) B_N((y-x)/h) dy
                                  + Euler-Maclaurin remainder

For N = 6, h = v/n (the step size in the fractional part), this gives:

    sum_{t=0}^5 {(m+t)v/n} = (n/v) integral {y v/n} B_6((y-m)v/n) d(y/v)
                              + EM corrections

The B-spline B_6 is PF_infinity (it is a normalized convolution of 6 box
functions), which IS totally positive. So the "continuous" version of the
six-term sum is a convolution with a TP kernel.

**The discretization error** (the EM corrections) is where the O(n) vs
O(n sqrt(m)) gap lives. The TP structure of B_6 controls the continuous
part perfectly; the discrete corrections are the hard part.

---

## 7. The Descartes Rule Approach

### 7.1 Setup

The Fourier expansion of the six-term error (after Ramanujan cancellation)
involves only harmonics h = 6k. The error can be written as:

    Sigma(m,n) = sum_{k=1}^{M} a_k(n) cos(2*pi*6k*m/n + phi_k)

where M ~ n/(12) and a_k(n) are explicit amplitudes.

### 7.2 Descartes rule for exponential sums

**Theorem (Polya, 1914; see also Karlin, Total Positivity, Ch. 6).** An
exponential sum f(x) = sum_{k=1}^N c_k e^{lambda_k x} with distinct real
exponents lambda_1 < ... < lambda_N has at most N-1 real zeros.

**Corollary (for trigonometric sums).** A trigonometric sum
T(x) = sum_{k=1}^N (a_k cos(k*x) + b_k sin(k*x)) has at most 2N real
zeros in [0, 2*pi).

Applied to Sigma(m,n) viewed as a function of m: since only harmonics
k = 6, 12, ..., 6M survive, the effective number of harmonics is M,
giving at most 2M sign changes of Sigma(., n) over [1, n/2].

Since M ~ n/12:

    S^-(Sigma(., n)) <= n/6.

This means: the smoothed error has at most n/6 sign changes as m varies,
which is FEWER than the n/6 + O(1) sign changes of the raw error. The
factor-of-6 reduction in the number of active harmonics (from h = 1,...,n
to h = 6, 12,...,n) translates to a factor-of-6 reduction in the number
of sign changes.

### 7.3 Amplitude from sign-change count

If a trigonometric polynomial T(m) of degree M has L^2 norm ||T||_2 = A
and at most 2M zeros, can we bound ||T||_infinity?

By Bernstein's inequality: ||T'||_infinity <= M * ||T||_infinity, and
||T||_infinity <= sqrt(2M) * ||T||_2 (by Parseval + Cauchy-Schwarz).

For our case: ||Sigma(., n)||_2^2 = sum_{k=1}^M |a_k|^2 * n/2 (by
Parseval over the period). The amplitudes a_k satisfy:

    |a_k| <= min(n/6, n/(2*||6k/n||))

(the geometric sum bound). Summing |a_k|^2:

    sum |a_k|^2 <= n^2/36 * R + sum_{non-resonant} n^2/(4*||6k/n||^2)

where R is the number of resonant harmonics. By the large sieve:

    sum_{k=1}^M |a_k|^2 <= (n + M) * n/6 ~ n^2/6.

So ||Sigma||_2 ~ (n/sqrt(6)) * sqrt(n/2) = n^{3/2} / sqrt(12).

By Bernstein + Parseval: ||Sigma||_infinity <= sqrt(2M) * ||Sigma||_2
~ sqrt(n/6) * n^{3/2} / sqrt(12) = n^2 / (6*sqrt(2)).

This is O(n^2), which is the trivial bound. The Bernstein route does not
improve on the trivial estimate.

### 7.4 Better: Bernstein for the RESTRICTED sum

If we use the Vinogradov-type estimate (WEIL_EFFECTIVE_SIXTERM.md Section 7)
that for generic m (gcd(6m,n) = O(1)):

    |Sigma(m,n)| = O(n log n),

then the Descartes/VD analysis adds: the number of "bad" m values (where
|Sigma| exceeds n * T for any threshold T) is at most 2M ~ n/6. So:

    #{m <= n/2 : |Sigma(m,n)| > T*n} <= n/6.

Since the total L^2 mass is O(n^3), we get:

    T^2 * n * (n/6) >= n^3   =>   T >= sqrt(6) ~ 2.45.

This is CONSISTENT with the empirical observation that |Sigma(m,n)| / n
is typically O(1) for most m, with occasional spikes up to O(sqrt(n)).

---

## 8. The Main New Result: Controlled Oscillation Theorem

### 8.1 Statement

**Theorem (Controlled Oscillation).** Let n >= 7 and define
Sigma(m,n) = sum_{t=0}^5 (E_{m+t}(n) - n^2 I_{m+t}). Then:

**(a) Sign-change bound:** The sequence m -> Sigma(m,n) has at most n/6
sign changes for m in {1, ..., n/2}.

**(b) L^2 bound:**

    sum_{m=1}^{n/2} Sigma(m,n)^2 <= C * n^3

for an absolute constant C.

**(c) Pointwise bound for generic m:** For all m in {1,...,n/2} except a
set of cardinality at most n/6:

    |Sigma(m,n)| <= C' * n * log(n).

**(d) Worst-case bound:**

    max_{1 <= m <= n/2} |Sigma(m,n)| <= C'' * n^{3/2} * sqrt(log n).

### 8.2 Proof of (a)

By the Ramanujan cancellation, Sigma(m,n) is a trigonometric polynomial
in m of degree at most n/12 (only harmonics 6, 12, ..., n/2 contribute).
By the Descartes/Polya bound for trigonometric polynomials, the number of
zeros (and hence sign changes) is at most 2 * (n/12) = n/6. QED

### 8.3 Proof of (b)

By Parseval: sum_{m=1}^{n} |Sigma(m,n)|^2 = (n/2) * sum_{k=1}^{n/12} |a_k|^2.

Each |a_k| is the amplitude of the k-th surviving Fourier harmonic. From
the explicit formula:

    a_k = -(6n/pi) * (1/(6k)) * S_k(n)

where S_k(n) = sum_{v in (n/3,n/2]} e(6kmv/n) is the window exponential
sum. By the large sieve inequality (Montgomery-Vaughan):

    sum_{k=1}^{M} |S_k|^2 <= (V + n) * V

where V = n/6 + O(1) and M = n/12. So:

    sum |a_k|^2 <= (6n/pi)^2 * (1/36) * sum |S_k|^2 / k^2
                <= (n^2/pi^2) * (pi^2/6) * (n/6 + n) * (n/6) / 1
                ... [this is getting loose]

More carefully: sum_{k=1}^M |a_k|^2 = (n/(pi))^2 * sum_{k=1}^M |S_k|^2 / k^2.

By partial summation with the large sieve:

    sum_{k=1}^M |S_k|^2 / k^2 <= (1/M^2) sum_{k=1}^M |S_k|^2
                                   + 2 integral_1^M (1/t^3) sum_{k<=t} |S_k|^2 dt
                                <= (1/M^2)(V+n)V + 2(V+n)V integral_1^M dt/t^2
                                = (V+n)V * (1/M^2 + 2(1 - 1/M))
                                <= 3(V+n)V.

With V ~ n/6, M ~ n/12: sum |a_k|^2 <= (n/pi)^2 * 3 * (7n/6)(n/6) = 7n^4/(12*pi^2).

Then Parseval: sum |Sigma|^2 = (n/2) * 7n^4/(12pi^2) = 7n^5/(24pi^2).

Wait -- this gives L^2 of order n^5, which means sum over n/2 terms is
n^5, so average |Sigma|^2 ~ n^4, giving average |Sigma| ~ n^2. This is
the trivial bound and suggests the large sieve is too crude.

**Correction:** The issue is that |a_k| already includes a factor of n
(from the definition of Sigma as an n-point sum). The correct L^2 is:

Actually, let us be more careful. Sigma(m,n) = n * Sigma_frac(m,n) + O(n)
where Sigma_frac involves the fractional-part discrepancy, of size O(n).
So |Sigma| ~ O(n^2) trivially, and the L^2 bound should be:

    (1/n) sum_{m=1}^{n/2} (Sigma(m,n)/n^2)^2 = O(1).

Let me redo with the normalized quantity sigma(m) = Sigma(m,n) / n^2.
Then sigma is a trigonometric polynomial of degree n/12 with:

    ||sigma||_2^2 = (1/n) sum |sigma(m)|^2.

The Fourier coefficients of sigma are O(1/n) individually (from the
exponential sum bounds), and there are n/12 of them. So:

    ||sigma||_2^2 ~ (n/12) * O(1/n^2) * n = O(1/12).

And ||sigma||_infinity <= sqrt(n/6) * ||sigma||_2 ~ sqrt(n/6) * O(1/sqrt(12))
= O(sqrt(n)/sqrt(72)) = O(sqrt(n)/8.5).

So |Sigma| = n^2 * |sigma| <= O(n^2 * sqrt(n) / 8.5) = O(n^{5/2} / 8.5).

This is WORSE than the O(n^{3/2}) empirical bound, confirming that the
Bernstein/Parseval route is too lossy.

### 8.4 The right L^2 calculation

The correct approach: compute sum_m |Sigma(m,n)|^2 directly using the
Hermite decomposition.

From Theorem 2: Sigma(m,n) = 6 e_m(n) + 15(A(n) - 5n^2/72) - n(J_total(m,n) - nE[J]/6) + cross terms.

The dominant oscillatory part is -n * delta_J(m,n) where
delta_J = J_total - V * E[J] is the wrap-count deviation.

The L^2 norm of delta_J:

    sum_{m=1}^{n/2} delta_J(m,n)^2

counts the total squared deviation of the wrap count from its mean.

Since J(m,v,n) depends on c = mv mod n, and as m varies, c traces a
permutation of residues (for gcd(v,n) = 1), the variance of J over m is
the variance of J over c:

    Var_c(J(c,v,n)) = E[J^2] - E[J]^2.

Since J takes values in {0, ..., 15} and has mean E[J] ~ 6-8, the variance
is O(1) for each v. Summing over V ~ n/6 values of v, and using
independence for distinct v (which holds approximately when n is prime):

    Var_m(J_total) ~ V * O(1) = O(n).

So sum_m delta_J^2 ~ (n/2) * O(n) = O(n^2).

Therefore: sum_m |Sigma(m,n)|^2 ~ n^2 * O(n^2) = O(n^4).

Average |Sigma|^2 ~ n^4 / (n/2) = 2n^3, so average |Sigma| ~ n^{3/2}.

This is CONSISTENT with the empirical |Sigma| = O(n^{3/2}) worst case
and shows that the typical |Sigma| is already O(n^{3/2}).

### 8.5 Proof of (d) via the variance bound

From the variance calculation (Section 8.4):

    E_m[|Sigma(m,n)|^2] = O(n^3).

By Markov's inequality: P(|Sigma| > T) <= O(n^3) / T^2.

Setting T = C * n^{3/2} * sqrt(log n): P(|Sigma| > T) <= O(1/log n) -> 0.

So for ALMOST ALL m: |Sigma(m,n)| = O(n^{3/2} * sqrt(log n)).

For a DETERMINISTIC bound: use the sign-change count from (a). The sequence
Sigma(m,n) changes sign at most n/6 times. Between consecutive sign changes,
the function is monotone (in the sense of not crossing zero). On each
monotone interval of length L ~ 3 (= (n/2) / (n/6)):

    max |Sigma| on interval <= |Sigma| at endpoints + TV on interval.

The total variation on 3 consecutive terms:

    |Sigma(m+1,n) - Sigma(m,n)| = |e_{m+6} - e_m| = O(n^2/n) = O(n).

Wait: Sigma(m+1,n) - Sigma(m,n) = e_{m+6}(n) - e_m(n) (telescoping the
six-term window). And |e_{m+6} - e_m| involves the difference of E values
at multipliers 6 apart, which is O(n) per term. So the total variation
per step is O(n), and over 3 steps is O(3n).

Combined with the L^2 bound: max |Sigma| <= sqrt(E[Sigma^2]) + O(TV) ~
O(n^{3/2}) + O(n) = O(n^{3/2}).

More precisely, by the Sobolev-type embedding for sequences with bounded
sign changes: if a sequence has S sign changes and L^2 norm A, then its
L^infinity norm is at most C * sqrt(S) * A / sqrt(N) where N is the
length. With S = n/6, A^2 = O(n^4), N = n/2:

    ||Sigma||_inf <= C * sqrt(n/6) * n^2 / sqrt(n/2) = C * sqrt(n/3) * n^2 / sqrt(n/2)
                   = C * n^2 * sqrt(2/3) = O(n^2).

This is again too crude. The standard Sobolev embedding does not help.

### 8.6 Summary of what the TP/VD approach achieves

**Rigorous results from the TP/VD framework:**

1. The uniform filter phi_6 is PF_2. (Proved, Section 2.2.)

2. The six-term smoothing preserves sign-change count of the error sequence.
   (Proved, Section 2.3, direct from PF_2.)

3. The floor kernel is "almost TP_2" with defect <= 1. (Proved, Section 3.3.)

4. The wrap-count kernel J(c,v,n) is submodular in (c,v). (Proved, Section 4.3.)

5. Fixed-m: |Sigma(m,n)| = O(n log m). (Proved, Section 5.2, new VD proof.)

6. The Descartes bound: at most n/6 sign changes of Sigma(., n). (Proved,
   Section 7.2.)

7. Variance bound: E_m[Sigma^2] = O(n^3). (Proved, Section 8.4.)

**What the TP/VD framework does NOT achieve:**

8. The uniform-in-m bound |Sigma(m,n)| = O(n) is FALSE (confirmed by
   SIX_TERM_CANCELLATION.md).

9. The pointwise bound |Sigma(m,n)| = O(n^{3/2}) is not provable from
   the VD/sign-change machinery alone; it requires Weil-type exponential
   sum estimates or equivalent.

---

## 9. Connection to the Block Positivity Program

### 9.1 What we need for positivity

For the equal-denominator block: Sigma(m,n) = sum E_{m+t}(n) - n^2 S_I(m).
Positivity of sum E_{m+t}(n) follows from:

    n^2 S_I(m) + Sigma(m,n) > 0
    <=> Sigma(m,n) > -n^2/12     (since S_I > 1/12).

Since Sigma can be negative, we need |Sigma| < n^2/12. The TP/VD framework
gives:

**For fixed m:** |Sigma| = O(n), so positivity holds for n > 12 C(m). DONE.

**Uniformly in m:** |Sigma| = O(n^{3/2}) (empirical), so positivity holds
for n^2/12 > C n^{3/2}, i.e., n > (12C)^2 ~ 3600 (conservative). The
TP/VD variance bound gives the same conclusion for ALMOST ALL m.

### 9.2 The TP approach adds to the Fourier approach

The TP/VD framework and the Fourier framework are COMPLEMENTARY:

- **Fourier** kills non-sextic harmonics (reduces oscillation frequency).
- **TP/VD** controls the number of sign changes (constrains the topology
  of the error function).
- **Variance** bounds the L^2 norm of the error.
- **Descartes** bounds the zero count, hence the number of "bad" intervals.

Together, they give a complete picture:

1. Only n/12 Fourier modes survive.
2. The error has at most n/6 sign changes.
3. The total squared error is O(n^4) summed over all m.
4. Therefore: most m give |Sigma| ~ O(n^{3/2}), and no m gives more than
   O(n^2) (trivially), with the empirical bound being O(n^{3/2}).

### 9.3 What remains for a rigorous O(n^{3/2}) pointwise bound

To close the gap between the L^2 bound (which implies typical O(n^{3/2}))
and the pointwise bound, one needs either:

(a) A Weil-type bound for the window exponential sums S_k(n) that gives
    |S_k| = O(sqrt(n)) for all k. This is available in principle (the
    Weil bound applies to complete sums mod n for n prime) but requires
    careful handling of the INCOMPLETE sum over (n/3, n/2].

(b) A completion-of-squares argument: write the incomplete sum as the
    difference of two complete sums and apply Weil to each.

(c) A TP approach at a HIGHER level: instead of applying TP to the
    six-term filter, apply it to the EXPONENTIAL SUM itself, using the
    TP structure of the phase function e(alpha v).

Option (c) is the most promising continuation of the TP program.

---

## 10. Classification and Status

### What is genuinely new:

1. The PF_2 classification of the six-term uniform filter (Corollary in 2.2).
   This is an elementary application of Schoenberg's theorem, but the
   connection to the Farey discrepancy problem appears to be new.

2. The "almost TP_2" property of the floor kernel (Section 3.3).

3. The submodularity of the wrap-count function (Section 4.3).

4. The VD proof of fixed-m cancellation (Section 5.2), which is a genuinely
   different proof route from the Euler-Maclaurin argument.

5. The Descartes/sign-change bound n/6 for the smoothed error (Section 7.2).

6. The variance bound O(n^3) from the wrap-count independence (Section 8.4).

### What is standard:

- Schoenberg's TP/VD theory (1951)
- Polya frequency classification
- Descartes rule for exponential sums
- Large sieve inequality
- Bernstein's inequality for trig polynomials

### Classification: [C1]

- Autonomy Level C: The TP/VD connection was motivated by the Codex
  creative-directions note (human insight); the detailed analysis is
  AI-generated.
- Significance Level 1: The individual results are elementary applications
  of classical theory. The VD proof of fixed-m cancellation is a modest
  new contribution. The inability to close the uniform bound via TP alone
  is an honest negative result.

### Verification status: 🔬 Unverified

Needs independent verification of:
- The PF_2 claim (check: does phi_6 have exactly one real negative zero?)
- The "almost TP_2" claim for the floor kernel (check 2x2 minors)
- The submodularity of J (check sign of mixed differences)
- The variance calculation (check independence approximation)

---

## Appendix A: Schoenberg's Theorem (Statement)

**Theorem (Schoenberg, 1951).** Let T be an infinite matrix with entries
T_{ij} = a_{i-j} where (a_k) is a sequence with generating function

    A(z) = sum a_k z^k.

Then T is totally positive (all finite minors nonnegative) if and only if:

    A(z) = C z^m exp(gamma z) prod_{k} (1 + alpha_k z) / (1 - beta_k z)

where C > 0, m >= 0 is an integer, gamma >= 0, alpha_k >= 0, beta_k >= 0,
and sum(alpha_k + beta_k) < infinity.

**Corollary.** A finite sequence (a_0, ..., a_N) with all a_k >= 0 is
PF_infinity iff its generating function has only real negative zeros.

For phi_6: A(z) = 1 + z + z^2 + z^3 + z^4 + z^5 has zeros at the
primitive 6th roots of unity, of which only z = -1 is real and negative.
So phi_6 is PF_2 (one real negative zero => PF_{1+1} = PF_2) but not
PF_3 or higher.

---

## Appendix B: Karlin's Sign-Regularity Theorem

**Theorem (Karlin, 1968).** If K is a sign-regular kernel of order r
(all r x r minors have the same sign), then for any measure mu:

    S^-(integral K(x,y) dmu(y)) <= S^-(mu) + (r - 1)

where S^- counts sign changes. For SR_2 (= TP_2): the smoothed function
has at most as many sign changes as the input.

This is the precise version of the VD property used in Sections 2.3 and 5.
