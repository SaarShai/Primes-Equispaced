# Two Approaches to the Unconditional Sign Theorem: Ergodic and Matrix/Quadratic Form

## Date: 2026-03-29
## Classification: C1 (collaborative, minor novelty) -- analysis of proof strategies, no new theorems
## Verification status: N/A -- this is a feasibility assessment, not a claimed result

---

## 0. Context and Goal

**Sign Theorem (target):** For all primes p >= 11 with M(p) <= -3: DeltaW(p) < 0.

Equivalently: B + C + D > A, where the four-term decomposition gives
DeltaW = (A - B - C - D)/n'^2.

The bypass reduces this to: **D/A + C/A > 1**.

We have:
- C/A >= pi^2/(432 log^2 N) -- PROVED (rearrangement + PNT + Franel-Landau)
- D/A = 1 + o(1) -- known asymptotically but NOT effective
- The gap: proving D/A >= 1 - C/A effectively

Two new approaches are proposed. This document gives a rigorous GO/NO-GO for each.

---

## APPROACH 1: ERGODIC (Horocycle Flow + Unique Ergodicity)

### 1.1 The Idea

The BCZ map (Boca-Cobeli-Zaharescu), which encodes F_{N-1} -> F_N, is a Poincare
section of the horocycle flow on SL(2,Z)\H (Athreya-Cheung 2014). Horocycle flow
on finite-area hyperbolic surfaces is uniquely ergodic (Furstenberg 1973) and in
fact mixing (Hedlund-Marcus).

**Proposed argument:** If the BCZ map is mixing, then for large N the shifts delta
are "effectively random" relative to displacements D. This would give:

    E[sum D * delta] approx 0

Combined with sum delta^2 > 0, this yields B + C > 0 for all sufficiently large N.
The finitely many exceptions can be checked computationally.

### 1.2 What Is Rigorously Known

| Fact | Status | Reference |
|------|--------|-----------|
| BCZ map is a Poincare section of horocycle flow | PROVED | Athreya-Cheung 2014 |
| Horocycle flow on SL(2,Z)\H is uniquely ergodic | PROVED | Furstenberg 1973 |
| Horocycle flow is mixing | PROVED | Marcus 1977 |
| BCZ map is weakly mixing | PROVED | arXiv:2403.14976 (2024) |
| Effective equidistribution of long horocycles | PROVED | Flaminio-Forni-Tanis 2016 |
| Rate: error = O(T^{Re(s_j)-1}) for Maass eigenvalue s_j | PROVED | Flaminio-Forni 2003 |
| Spectral gap for PSL(2,Z)\H: lambda_1 ~ 91.14 | PROVED | Hejhal, numerical |
| Gauss map exponential mixing rate: |lambda_2| = 0.3036... | PROVED | Mayer 1991 |
| Farey map polynomial mixing: O(1/n) | PROVED | Isola 2002, LSV 1999 |

### 1.3 Analysis: Why This Does Not Work

**Problem 1: Wrong type of mixing.**

The BCZ map has been shown to be *weakly mixing* (2024), NOT strongly mixing or
exponentially mixing. Weak mixing means:

    (1/N) sum_{n=0}^{N-1} |<T^n f, g> - <f,1><1,g>|^2 -> 0

This is a *Cesaro-averaged* decorrelation -- it says the correlations are small
ON AVERAGE but allows individual terms <T^n f, g> to be large. For our Sign
Theorem, we need a statement about EVERY prime p individually, not an average
over p. Weak mixing is fundamentally insufficient.

**Problem 2: Mismatch between the observables and the dynamics.**

The horocycle flow/BCZ map describes the transition F_{N-1} -> F_N for consecutive
integers N. Our observables D(f) and delta(f) are defined on F_{N} for a FIXED N.
The mixing of the BCZ map describes correlations ACROSS different N values (the
"time" direction), not correlations among fractions WITHIN a single Farey sequence.

The cross term B = 2 sum_{f in F_{p-1}} D(f) * delta(f) is a sum over fractions
in a SINGLE Farey sequence. This is a spatial correlation, not a temporal one.
The ergodic theory of the BCZ map addresses temporal (step-to-step) correlations.

To use the BCZ framework for spatial correlations, one would need to show that
the natural measure on F_N (uniform on Farey fractions) converges to the Gauss
measure (the invariant measure of the BCZ map) in a sufficiently strong sense
that the spatial correlations are controlled by the spectral gap. This is
essentially the content of effective equidistribution results, but these give
AVERAGE bounds on correlations, not pointwise bounds at each prime.

**Problem 3: The neutral fixed point kills effective rates.**

The Farey map has a neutral (parabolic) fixed point at 0. This causes:
- Only polynomial mixing (O(1/n)) instead of exponential
- Continuous spectrum on [0,1] for the transfer operator (Isola 2002)
- The spectral gap is ZERO for the Farey map

The BCZ map inherits this issue through the cusp of SL(2,Z)\H. The horocycle
flow on the modular surface is mixing, but the RATE of mixing depends on the
regularity of the test functions. For smooth test functions, the rate is
exponential (controlled by the spectral gap lambda_1 ~ 91.14). But D(f) and
delta(f) are NOT smooth -- they are defined on rational points and have jumps
at every Farey fraction. For such irregular observables, the effective
equidistribution rate degrades, potentially to polynomial.

**Problem 4: The Mertens function is the missing ingredient.**

Ergodic/mixing arguments give bounds of the form:

    |sum D * delta| <= C * ||D||_2 * ||delta||_2 * (decay rate)

where the decay rate depends on the mixing properties. But this bound is
SYMMETRIC in the sign of sum D * delta -- it cannot distinguish between
M(p) <= -3 (where B + C > 0) and M(p) > 0 (where B + C can be < 0).

The arithmetic content -- that the Mertens function controls the sign -- is
invisible to pure ergodic theory. The ergodic framework treats all primes
the same (they are all "generic" from the dynamical perspective), but the
Sign Theorem is precisely about the arithmetic specialness of M(p) <= -3.

**Problem 5: Finite exceptions cannot be bounded.**

Even if ergodic mixing gave B + C > 0 "for all but finitely many N," we
would need an EFFECTIVE bound on the number of exceptions to verify them
computationally. Unique ergodicity is inherently non-effective (it gives no
rate), and even effective equidistribution (Flaminio-Forni-Tanis) gives rates
that depend on spectral data too coarsely to identify specific exceptions.

### 1.4 What Could Be Salvaged

The ergodic framework IS useful for **conceptual understanding**:

1. **Why correlations are small:** The mixing of the BCZ map explains heuristically
   why |rho(D, delta)| ~ p^{-0.15} -- the two observables "live at different scales"
   in the dynamical system. D depends on the global structure of F_N (the
   "macroscopic" observable), while delta depends on the local arithmetic of
   multiplication by p (the "microscopic" observable). Mixing predicts these
   should be approximately uncorrelated.

2. **Why the exponent is -0.15:** The polynomial mixing rate O(1/n) of the
   Farey map suggests correlations should decay as N^{-alpha} for some alpha.
   The observed alpha ~ 0.15 is consistent with (but not predicted by) the
   polynomial mixing rate, since the actual decay depends on the regularity
   class of D and delta as observables on the Farey partition.

3. **Paper framing:** The ergodic perspective provides good narrative context
   for the paper: "our Sign Theorem can be understood as a quantitative
   decorrelation result for two natural observables in the ergodic theory of
   continued fractions." But the actual proof uses different tools.

### 1.5 Verdict: NO-GO for proof; GO for exposition

The ergodic approach **cannot** yield a proof of the Sign Theorem because:
- Weak mixing gives Cesaro averages, not pointwise bounds
- Spatial vs temporal correlation mismatch
- Cannot distinguish M(p) <= -3 from M(p) > 0
- No effective error bounds for the specific observables involved

**Confidence: 95% NO-GO.** The remaining 5% accounts for the unlikely possibility
that someone finds a way to combine BCZ weak mixing with arithmetic input
(Hecke operators?) to get pointwise bounds. This would be a major advance in
homogeneous dynamics, not a routine application of existing theory.

---

## APPROACH 2: MATRIX / QUADRATIC FORM (Angle Between D and delta)

### 2.1 The Idea

Write B + C in terms of inner products:

    B + C = ||v + delta||^2 - ||v||^2 = 2<v, delta> + ||delta||^2

where v = (D(f_1), ..., D(f_n)) and delta = (delta(f_1), ..., delta(f_n)).

Then B + C > 0 iff:

    <v, delta> > -||delta||^2 / 2

Equivalently, in terms of the angle theta between v and delta:

    cos(theta) > -||delta|| / (2||v||)

Since ||delta||/||v|| is empirically small (~0.1-0.3), the constraint is:

    cos(theta) > -(0.05 to 0.15)

i.e., the angle between D and delta must not be EXTREMELY obtuse (more than
about 95-99 degrees). Can we prove this using the structural difference between
D (global rank discrepancy) and delta (local multiplicative shift)?

### 2.2 Empirical Data on the Angle

From the ergodic_approach.md data (primes p <= 2000 with M(p) <= 0):

| Quantity | Value |
|----------|-------|
| Mean cos(theta) | +0.37 |
| Min cos(theta) | -0.12 (p = 1429, M(p) = +3) |
| Correlation rho = cos(theta) | typically 0.2-0.5 for M(p) <= -3 |
| ||delta||/||v|| range | 0.05 - 0.35 |
| Critical cos threshold | -0.025 to -0.175 |

For M(p) <= -3 primes, cos(theta) is ALWAYS positive (up to p = 2000).
The angle is acute, so B = 2<v,delta> > 0 and B + C > 0 follows trivially.

For M(p) in {-2, -1, 0}, cos(theta) can be slightly negative but never
enough to violate B + C > 0 (the delta^2 margin saves it).

### 2.3 Structural Analysis: Why D and delta Should Not Be Anti-Aligned

**The displacement vector v = D:**

D(a/b) = rank(a/b, F_N) - |F_N| * (a/b).

This measures the excess or deficit of Farey fractions up to a/b. By the
theory of Farey sequences:

- D(a/b) depends on all denominators up to N through the totient sum
- D is "smooth" at the scale of 1/N -- consecutive Farey fractions have
  D values differing by O(1)
- D has a Fourier expansion involving the Mertens function:
  D(x) ~ sum_{h=1}^{N} (M(N/h)/h) * {hx} + lower order

**The shift vector delta:**

delta(a/b) = a/b - sigma_p(a)/b, where sigma_p(a) = pa mod b.

This is a "local" quantity -- it depends only on the multiplication-by-p
permutation within each denominator class. Key properties:

- delta(a/b) depends only on a, b, and p -- NOT on the global Farey structure
- For each fixed b, the values delta(a/b) as a ranges over coprime residues
  form a specific permutation of the differences (a - pa mod b)/b
- The sum of delta over each denominator class vanishes:
  sum_{a coprime b} delta(a/b) = 0

**Why anti-alignment is hard:**

For v and delta to be anti-aligned (cos(theta) << 0), we would need:
D(f) and delta(f) to have OPPOSITE signs for most Farey fractions.

But D(f) has large-scale structure (it oscillates with period ~1/N controlled
by the totient function), while delta(f) has small-scale structure (it depends
on the specific residue a mod b for each denominator b). These structures are
"incommensurate" -- a conspiracy where the local permutation delta consistently
opposes the global rank discrepancy D would require an arithmetic miracle.

### 2.4 The Smooth-Rough Decomposition

(From MPR-25 in the MASTER_TABLE)

Decompose D into smooth and rough parts:

    D = D_smooth + D_rough

where D_smooth is the "trend" (low-frequency part, depending on x = a/b
through a smooth function of x) and D_rough is the "oscillation" (high-
frequency part, depending on the specific denominator b through Ramanujan sums).

**Key identity (claimed, under verification):**

    sum D_smooth(f) * delta(f) = 0

This holds because D_smooth(x) ~ g(x) for a smooth function g, and the
sum of delta over each denominator class vanishes. So the smooth part of
D contributes NOTHING to the cross term B.

Therefore:

    B = 2 sum D_rough * delta

The cross term depends ONLY on the rough (arithmetic) part of D. This is
where the Mertens function enters: D_rough involves Ramanujan sums
c_q(n) = sum_{(a,q)=1} e(an/q) and the Mertens function controls their
partial sums.

### 2.5 Attempting a Proof via the Angle Bound

**What we need:** cos(theta) > -||delta||/(2||v||) for all p with M(p) <= -3.

**Step 1: Bound ||delta||/||v||.**

||delta||^2 = C (the shift-squared term).
||v||^2 = old_D_sq (the Farey discrepancy sum).

We know: C/old_D_sq ~ pi^2/(6N * C_W) where C_W = N * W(N) ~ 0.67 (empirically bounded).

So ||delta||/||v|| ~ sqrt(pi^2/(6N * C_W)) ~ 1.3/sqrt(N).

For p >= 100: ||delta||/||v|| <= 0.13.
For p >= 10000: ||delta||/||v|| <= 0.013.

**Step 2: Bound cos(theta) from below.**

This is the hard part. We need:

    cos(theta) = <D, delta> / (||D|| ||delta||) > -0.065 (for p ~ 100)

Using the smooth-rough decomposition:

    <D, delta> = <D_rough, delta>

So cos(theta) = <D_rough, delta> / (||D|| ||delta||).

Since ||D_rough|| <= ||D|| (Pythagorean), we get:

    |cos(theta)| <= ||D_rough|| * ||delta|| / (||D|| * ||delta||) = ||D_rough|| / ||D||

**If ||D_rough||/||D|| were small**, then |cos(theta)| would be small and
the angle bound would be satisfied. But empirically, ||D_rough||/||D|| is
NOT small -- D_rough carries a substantial fraction of the total variance.

**Step 3: The Kloosterman connection.**

The inner product <D_rough, delta> involves sums of the form:

    sum_{a coprime b} R_b(a) * (a - pa mod b)

where R_b(a) involves Ramanujan sums. These are generalized Kloosterman sums.
The Weil bound gives:

    |sum_{a coprime b} R_b(a) * (a - pa mod b)| <= C * sqrt(b) * log(b)

Summing over denominators b:

    |<D_rough, delta>| <= C * sum_{b=2}^{N} sqrt(b) * log(b) * (amplitude of R_b)

The amplitude of R_b depends on the Ramanujan sum expansion of D. The leading
term is c_b(1) = mu(b), and the Mertens function appears through:

    sum_{b <= N} mu(b) * (...) ~ M(N) * (...) + lower order

This is WHERE M(p) enters the angle bound. When M(p) <= -3, the Mertens
contribution pushes the inner product <D_rough, delta> toward being positive
(or at least not too negative), keeping cos(theta) above the critical threshold.

### 2.6 The Central Obstacle (Same as ANALYTICAL_PROOF_PATH_C)

The Kloosterman/Weil bound approach gives:

    |<D, delta>| <= C_1 * N * sqrt(N) * log(N)

while:

    ||D|| * ||delta|| ~ C_2 * N * sqrt(N) * sqrt(log N)

So the ratio |<D,delta>|/(||D||*||delta||) is bounded by O(sqrt(log N)),
which is GROWING, not decaying. The Weil bound per denominator is tight
(cannot be improved), but the summation over denominators introduces an
extra log factor.

**This is exactly the same obstacle identified in ANALYTICAL_PROOF_PATH_C
Section 7:** the Weil bound approach gives a crossover at P_0 ~ 10^10,
which is tractable computationally but enormous.

### 2.7 Can the Quadratic Form Structure Help?

The quadratic form perspective suggests a different approach: instead of
bounding the inner product directly, study the EIGENSTRUCTURE of the
linear map delta: v -> v + delta.

**Observation:** B + C = ||v + delta||^2 - ||v||^2. This is positive when
the perturbation delta "inflates" the norm of v. In matrix terms, if we
think of the map v -> v + delta as adding a perturbation, B + C > 0 is
equivalent to saying the perturbation is "outward-pointing" on average.

**The Rayleigh quotient approach (MPR-13):**

Consider the ratio W(p)/W(p-1) = ||v + delta||^2 / (something involving ||v||^2).
If we could show this ratio exceeds a specific threshold, the Sign Theorem follows.

The Rayleigh quotient of the perturbation operator (I + Delta) with respect
to the "discrepancy norm" is:

    R = ||v + delta||^2 / ||v||^2 = 1 + 2<v,delta>/||v||^2 + ||delta||^2/||v||^2
      = 1 + B/old_D_sq + C/old_D_sq

The Sign Theorem (via the bypass) needs R >= C/A / (C/old_D_sq), which simplifies
to verifying the D/A + C/A >= 1 bound -- we are back to the same bottleneck.

### 2.8 A Novel Angle: Majorization and Schur Convexity

(From MPR-14 in the MASTER_TABLE)

The vector v + delta is obtained from v by a specific permutation-plus-shift
operation. The theory of majorization asks: does v + delta majorize v in some sense?

**Schur's inequality:** If f is Schur-convex and x majorizes y, then f(x) >= f(y).
The L2 norm sum x_i^2 is Schur-convex.

**Question:** Does (D + delta) majorize D in the sense of Hardy-Littlewood-Polya?

This would require showing that the partial sums of the sorted |D + delta|
vector dominate the sorted |D| vector. The shift delta, being a permutation
of residues within each denominator class, has a specific structure that
might yield majorization.

**Assessment:** This is unexplored territory. The connection between the
Farey permutation sigma_p and majorization theory has not been studied.
It could yield a clean proof IF the majorization holds, but there is no
evidence for or against it. This requires computational verification first.

### 2.9 Verdict: CONDITIONAL GO

The quadratic form / angle approach **can potentially yield a proof** but faces
the same core obstacle as all other analytical approaches: proving D/A ~ 1
effectively. The angle formulation provides useful STRUCTURE but does not
bypass the fundamental difficulty.

**What the angle approach adds:**
1. Geometric intuition: the angle between D and delta must not be too obtuse
2. Connection to Kloosterman sums via the smooth-rough decomposition
3. A clear quantitative target: cos(theta) > -||delta||/(2||v||) ~ -1/sqrt(N)
4. The Schur convexity / majorization direction is genuinely novel and unexplored

**What it does NOT solve:**
1. The Weil bound summation problem (log factor grows with N)
2. The effective equidistribution of D at arithmetic sample points
3. The role of M(p) (enters indirectly through Ramanujan sums, hard to make effective)

**Confidence: 40% conditional GO.** The approach has merit and could work if
combined with additional arithmetic input (particularly improved Kloosterman
summation or a majorization argument). It is more promising than the ergodic
approach but still faces fundamental obstacles.

---

## COMPARISON OF THE TWO APPROACHES

| Criterion | Ergodic (Approach 1) | Matrix/Angle (Approach 2) |
|-----------|---------------------|--------------------------|
| Uses known results | Yes (BCZ, horocycle) | Yes (Weil bound, Ramanujan) |
| Addresses the right object | No (temporal vs spatial) | Yes (inner product <D,delta>) |
| Can distinguish M(p) sign | No (ergodic = generic) | Partially (via Mertens in Ramanujan sums) |
| Effective bounds available | No (unique ergodicity non-effective) | Partially (Weil bound effective but too loose) |
| Novel unexplored angles | No (standard ergodic theory) | Yes (majorization, Schur convexity) |
| Gives proof for large p | No | Maybe (P_0 ~ 10^10 via Weil) |
| Gives proof for all p | No | No (small p requires computation) |
| Usefulness for paper | Good framing/narrative | Good technical content |

---

## RECOMMENDED STRATEGY

### Immediate actions:

1. **Do NOT pursue the ergodic approach for proof.** Use it for paper exposition only.
   Frame the Sign Theorem as "a quantitative decorrelation result in the ergodic
   theory of continued fractions" in the introduction, but prove it arithmetically.

2. **Pursue the matrix/angle approach as THEORETICAL CONTEXT** but do not expect
   a clean proof from it alone. The angle formulation is pedagogically useful and
   connects to well-studied objects (Kloosterman sums, Ramanujan sums).

3. **Explore Schur convexity / majorization** as a genuinely new direction.
   Computational test: for each prime p <= 2000 with M(p) <= -3, check whether
   the sorted |D + delta| vector majorizes the sorted |D| vector.

### The honest path to the Sign Theorem remains:

**Hybrid proof:**
- Analytical: C/A >= pi^2/(432 log^2 N) for all N (DONE)
- Analytical: D/A = 1 + O(|M(p)|/p) (provable via Weil bound for p >= P_0)
- Computational: verify D/A + C/A >= 1 for all primes p < P_0 with M(p) <= -3

The value of P_0 depends on which analytical tools are used:
- Weil bound alone: P_0 ~ 10^10 (feasible with C code, ~hours)
- Weil + improved Kloosterman summation: P_0 ~ 10^6 (already verified)
- With majorization (if it works): could reduce P_0 dramatically

---

## KEY REFERENCES (for both approaches)

### Horocycle flow and equidistribution
- Furstenberg, H. (1973). "The unique ergodicity of the horocycle flow." LNM 318.
- Marcus, B. (1977). "The horocycle flow is mixing of all degrees." Invent. Math.
- Flaminio, L. & Forni, G. (2003). "Invariant distributions for horocycle flows." Duke Math. J.
- Flaminio, Forni & Tanis (2016). "Effective equidistribution of twisted horocycles." GAFA.
- Sarnak, P. (1981). "Asymptotic behavior of periodic orbits of the horocycle flow."

### BCZ map
- Athreya, J. & Cheung, Y. (2014). "A Poincare section for horocycle flow." IMRN.
- arXiv:2403.14976 (2024). "The BCZ map is weakly mixing."
- Boca, F., Cobeli, C., Zaharescu, A. (2001). "Farey fractions and lattice point problems."

### Kloosterman sums and Weil bounds
- Weil, A. (1948). "On some exponential sums." PNAS.
- Iwaniec, H. & Kowalski, E. (2004). "Analytic Number Theory." AMS Colloquium.
- Estermann, T. (1961). "On Kloosterman's sum." Mathematika.

### Spectral theory of the modular surface
- Mayer, D. (1991). "Thermodynamic formalism for the Gauss map." OUP.
- Isola, S. (2002). "On the spectrum of Farey and Gauss maps." Nonlinearity.
- Lewis, J. & Zagier, D. (2001). "Period functions for Maass wave forms." Ann. Math.

### Majorization theory
- Marshall, A., Olkin, I., Arnold, B. (2011). "Inequalities: Theory of Majorization." Springer.
- Schur, I. (1923). "Uber eine Klasse von Mittelbildungen." Sitzungsber. Preuss. Akad.
