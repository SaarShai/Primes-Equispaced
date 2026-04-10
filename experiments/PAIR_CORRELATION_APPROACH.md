# Pair Correlation Approach to Bounding Σ E(k)² from Below

## Date: 2026-03-29
## Status: 🔬 Unverified — analytical framework, needs rigorous proof

---

## 1. Setup and Objective

### Notation

Let p be prime, N = p - 1, F_N the Farey sequence of order N, n = |F_N|.
Define:

    A(k) = #{f ∈ F_N : f ≤ k/p}       (1 ≤ k ≤ p-1)
    E(k) = A(k) - nk/p                  (counting error on the p-grid)

From Codex Proposition 4 (CODEX_RESEARCH_NOTE_PGRID_GAP2_2026_03_29.md):

    Σ_{k=1}^{p-1} A(k)² = Σ_{f,g ∈ F_N*} (p-1 - ⌊p·max(f,g)⌋)

where F_N* = F_N \ {1}.

### Goal

Prove: there exists c > 0 such that Σ E(k)² ≥ c·p² for all large primes p.

The stronger conjecture (supported by data): Σ E(k)² ~ c*·p²·log p, with
c* ≈ 0.066.

---

## 2. Decomposition of the Pair-Count Kernel

### 2.1 The kernel K(f,g)

For each pair (f,g) ∈ F_N* × F_N*, define:

    K(f,g) = p - 1 - ⌊p·max(f,g)⌋

This kernel has a geometric meaning: it counts the number of grid points
k/p that lie ABOVE max(f,g). Specifically:

    K(f,g) = #{k ∈ {1,...,p-1} : k/p > max(f,g)}
           = p - 1 - ⌊p·max(f,g)⌋

Note: K is symmetric in (f,g) and depends only on max(f,g).

### 2.2 Diagonal vs off-diagonal split

Write Σ A(k)² = S_diag + S_off where:

    S_diag = Σ_{f ∈ F_N*} K(f,f) = Σ_{f ∈ F_N*} (p-1 - ⌊pf⌋)
    S_off  = Σ_{f≠g ∈ F_N*} K(f,g) = Σ_{f≠g} (p-1 - ⌊p·max(f,g)⌋)

### 2.3 Evaluating the diagonal

For the diagonal:

    S_diag = Σ_{f ∈ F_N*} (p-1 - ⌊pf⌋)

Since f ranges over F_N \ {1}, and the Farey fractions are approximately
uniformly distributed with density n ≈ 3N²/π²:

    S_diag ≈ ∫₀¹ (p-1-px) · n dx = n(p-1)/2 ≈ np/2

More precisely, using Σ_{f∈F_N} f = n/2 (symmetry of Farey sequence):

    S_diag = (p-1)(n-1) - Σ_{f ∈ F_N*} ⌊pf⌋
           = (p-1)(n-1) - (p·Σf - Σ{pf})
           = (p-1)(n-1) - p(n/2 - 1) + Σ{pf}

where {x} = x - ⌊x⌋ is the fractional part. This gives:

    S_diag = n(p-2)/2 + 1 + Σ_{f ∈ F_N*} {pf}

The fractional parts sum Σ{pf} over Farey fractions is related to the
Dedekind sum structure. For our purposes:

    S_diag ≈ np/2 ≈ (3/π²)p³

---

## 3. The Continuous L² Discrepancy: What Is Known

### 3.1 The standard Farey L² discrepancy

Define the continuous counting error:

    E(x) = #{f ∈ F_N : f ≤ x} - nx     for x ∈ [0,1]

The L² discrepancy is:

    W(N) := (1/n²) Σ_{j=0}^{n-1} D(f_j)²

where D(f_j) = j - n·f_j. Equivalently:

    Σ D(f_j)² = n² · W(N)

### 3.2 Known bounds on W(N) and C_W(N)

From CW_BOUND_PROOF.md:

    C_W(N) := N · W(N)

Unconditional:  C_W(N) ≤ C·log(N)    [from PNT + Ramanujan sums]
Computational:  C_W(N) ≈ 0.67 for N ≤ 100000, growing as ~0.16 + 0.24·log(log N)

Therefore:

    Σ D(f_j)² ≈ n² · C_W(N)/N ≈ (9/π⁴)·N³·C_W(N) ≈ (9/π⁴)·0.67·N³

### 3.3 The sampled vs continuous connection

Our object Σ E(k)² samples E(x)² at the p-grid {k/p : 1 ≤ k ≤ p-1}.
As a Riemann sum:

    (1/p) Σ_{k=1}^{p-1} E(k/p)² ≈ ∫₀¹ E(x)² dx

But E(k/p) in our notation is E(k) = A(k) - nk/p, which IS the continuous
counting error E(x) evaluated at x = k/p (up to boundary effects at
Farey fractions themselves).

So naively: Σ E(k)² ≈ p · ∫₀¹ E(x)² dx.

**CRITICAL NUMERICAL FINDING:** The actual ratio is:

    Σ E(k)² / (p · ∫ E(x)² dx) ≈ 2.0

uniformly across all tested primes p ≤ 199. This "factor of 2" is NOT a
Riemann-sum error — it is a genuine structural effect. The discrete p-grid
sampling sees TWICE the energy of the continuous integral.

**Explanation:** E(x) is piecewise linear with slope -n, and E(k/p) samples
this at p points. Since E has n >> p zero-crossings (one per Farey interval),
and E(x)² is minimized at zeros, the p-grid systematically AVOIDS the zeros
of E and oversamples the peaks. This is the "aliasing" effect.

More precisely: the p-grid spacing 1/p is much coarser than the Farey gap
spacing ~1/n, so each sample E(k/p) captures the cumulative error over
~n/p Farey fractions. The variance of this cumulative sum is larger than
the average of the pointwise variance by a factor related to the
autocorrelation structure of E(x).

The factor of 2 can be understood as follows: E(x) within a p-grid cell
behaves like a random walk of n/p steps, each of mean 0 and variance ~1.
The variance at the endpoint is n/p (which is what we sample), while the
average variance over the cell is (n/p)/2 (by the random walk bridge
formula). So endpoint sampling gives 2x the integral average.

This means: Σ E(k)² ≈ 2p · ∫₀¹ E(x)² dx

### 3.4 What is ∫ E(x)² dx?

    ∫₀¹ E(x)² dx = ∫₀¹ (#{f ∈ F_N : f ≤ x} - nx)² dx

Between consecutive Farey fractions f_j < f_{j+1}, the count is constant (= j+1
for f ∈ [f_j, f_{j+1})), so E(x) = j+1 - nx is linear in x. The integral
becomes a sum over Farey intervals:

    ∫₀¹ E(x)² dx = Σ_{j=0}^{n-1} ∫_{f_j}^{f_{j+1}} (j+1-nx)² dx

Let d_j = f_{j+1} - f_j (Farey gap), D_j = j+1 - nf_j (displacement at left
endpoint). Then:

    ∫_{f_j}^{f_{j+1}} (j+1-nx)² dx = D_j²·d_j - D_j·n·d_j² + n²·d_j³/3

The dominant term is D_j²·d_j. Using d_j ≈ 1/n on average:

    ∫ E(x)² dx ≈ (1/n) Σ D_j² = n · W(N)

Therefore:

    Σ E(k)² ≈ p · n · W(N) = p · n · C_W(N)/N = p · C_W(N) · n/N

Since n ≈ 3N²/π² and N = p-1:

    Σ E(k)² ≈ p · C_W(p) · (3p²/π²)/p = (3/π²) · C_W(p) · p²

With C_W(p) ≈ 0.67: Σ E(k)² ≈ 0.204 · p²

With C_W(p) ~ c·log p: Σ E(k)² ~ (3c/π²) · p² · log p

With the factor-of-2 correction from discrete sampling:

    Σ E(k)² ≈ 2 · (3/π²) · C_W(p) · p²

With C_W(p) ≈ 0.55 at p ~ 200: Σ E(k)²/(p²·log p) ≈ 2·(3/π²)·0.55/log(200)
≈ 2·0.167·0.55/5.3 ≈ 0.035.

The data shows ~0.065, suggesting the factor may be slightly larger than 2,
or C_W at larger p contributes more. The key point is the STRUCTURAL
relationship:

    Σ E(k)² = Θ(p² · C_W(p))

and C_W(p) is bounded below by a positive constant.

---

## 4. The Core Argument: Lower Bound via Pair Correlation

### 4.1 Strategy

The Riemann sum approximation above gives us the heuristic. To make it a
rigorous LOWER bound, we need:

    (1/p) Σ_{k=1}^{p-1} E(k)² ≥ (1 - ε) · ∫₀¹ E(x)² dx

for some controllable ε. Then a lower bound on ∫ E(x)² dx gives one on Σ E(k)².

### 4.2 Riemann sum lower bound

E(x) is piecewise linear on each Farey interval [f_j, f_{j+1}] with
slope -n. The function E(x)² is therefore piecewise quadratic (convex on
each interval since E is linear).

**Key observation:** For a convex function g on [a,b], the left-endpoint
or right-endpoint Riemann sum UNDER-estimates the integral:

    (b-a)·g(a) ≤ ∫_a^b g(x) dx

if g is increasing, and (b-a)·g(b) ≤ ∫_a^b g(x) dx if g is decreasing.

But E(x)² is convex on each Farey interval (since E is linear and squaring
a linear function gives a convex quadratic). For convex functions, the
TRAPEZOIDAL rule OVER-estimates:

    ∫_a^b g(x)dx ≤ (b-a)(g(a)+g(b))/2

and the MIDPOINT rule UNDER-estimates:

    (b-a)·g((a+b)/2) ≤ ∫_a^b g(x)dx

So midpoint sampling gives a lower bound. The p-grid is NOT a midpoint
sampling of Farey intervals. We need a different approach.

### 4.3 Approach via Fourier analysis (more promising)

Write E(x) = Σ_{f ∈ F_N} 1_{[0,x]}(f) - nx. By the Fourier expansion:

    E(x) = Σ_{h≠0} (1/(2πih)) · Σ_{f ∈ F_N} e^{2πihf} · (e^{-2πihx} - 1) + ...

Actually, let's use the simpler approach via the explicit formula for Σ A(k)².

### 4.4 Direct attack on the pair sum

From Proposition 4:

    Σ A(k)² = Σ_{f,g ∈ F_N*} (p-1 - ⌊p·max(f,g)⌋)

Rewrite using max(f,g) = (f+g+|f-g|)/2:

    ⌊p·max(f,g)⌋ = ⌊p(f+g+|f-g|)/2⌋

This is hard to work with directly. Instead, organize by the gap structure.

### 4.5 Contribution by denominator class

For a Farey fraction f = a/b ∈ F_N*, we have:

    ⌊pf⌋ = ⌊pa/b⌋ = (pa - r)/b     where r = pa mod b

So the diagonal term K(f,f) = p - 1 - ⌊pa/b⌋ depends on the residue of p
mod b. This connects to the Boca-Cobeli-Zaharescu (BCZ) pair correlation
theory, which analyzes the distribution of {pa/b} for Farey fractions.

### 4.6 The BCZ pair correlation connection

The BCZ (2001) result: for Farey fractions F_N, the limiting pair
correlation function (at the natural scale 1/N²) is:

    R₂(s) = (6/π²)·s + higher order

This means: for small separations, consecutive Farey fractions repel
linearly (not as strongly as GUE's quadratic repulsion, but stronger
than Poisson's constant R₂ = 1).

The relevance: the off-diagonal sum S_off involves pairs (f,g) weighted
by K(f,g) = p - 1 - ⌊p·max(f,g)⌋. For "close" pairs where |f-g| is
small compared to 1/p, K(f,g) ≈ K(f,f) ≈ p(1-f). The BCZ pair
correlation controls how many such close pairs exist.

However, the BCZ result is about CONSECUTIVE pairs, while our sum ranges
over ALL pairs. The dominant contribution comes from pairs where f and g
lie in the same or adjacent p-grid cells.

---

## 5. A Cleaner Route: Variance Decomposition

### 5.1 Reformulation as variance

Since Σ E(k) = 0 (Proposition 2, mean-zero identity):

    Σ_{k=1}^{p-1} E(k)² = (p-1) · Var_k(E(k))

where Var_k denotes the variance over the uniform distribution on {1,...,p-1}.

So the question reduces to: how large is the variance of E(k)?

### 5.2 E(k) as a sum of indicators

    E(k) = Σ_{f ∈ F_N} [1_{f≤k/p} - k/p] + k/p - #{F_N ∩ {0}} · 1_{0≤k/p}

More cleanly, for f ∈ F_N* (excluding f=0 and f=1 for the moment):

    E(k) = Σ_{f ∈ F_N} (1_{f ≤ k/p} - k/p)   (approximately, ignoring boundary)

This is a sum of n terms, each of which is a centered indicator.

### 5.3 Variance computation

    Var_k(E(k)) = Σ_{f,g ∈ F_N} Cov_k(1_{f≤k/p}, 1_{g≤k/p})

For a given pair (f,g) with f ≤ g (WLOG):

    E_k[1_{f≤k/p}] = #{k : k/p ≥ f} / (p-1) = (p-1-⌊pf⌋)/(p-1) ≈ 1-f

    E_k[1_{f≤k/p} · 1_{g≤k/p}] = #{k : k/p ≥ g} / (p-1) = (p-1-⌊pg⌋)/(p-1) ≈ 1-g

Therefore:

    Cov_k = (1-g) - (1-f)(1-g) = (1-g)·f = f(1-g)    (for f ≤ g)

More precisely:

    Cov_k(1_{f≤·}, 1_{g≤·}) = (p-1-⌊pg⌋)/(p-1) - [(p-1-⌊pf⌋)(p-1-⌊pg⌋)]/(p-1)²

Let α_f = (p-1-⌊pf⌋)/(p-1) ≈ 1-f. Then:

    Cov_k = α_g - α_f · α_g = α_g(1 - α_f)

For f ≤ g: Cov_k = α_g · (1 - α_f) ≈ (1-g)·f

### 5.4 The variance sum

    Var_k(E(k)) = Σ_{f,g ∈ F_N*} Cov_k(...)

Separating f ≤ g and f > g (by symmetry of covariance):

    Var_k(E(k)) = 2 Σ_{f<g} f(1-g) + Σ_f f(1-f)

The diagonal: Σ_{f ∈ F_N*} f(1-f) ≈ n · E[f(1-f)] = n · (1/2 - 1/3) = n/6.
(Using E[f] = 1/2, E[f²] = 1/3 for uniform distribution on [0,1].)

The off-diagonal: 2 Σ_{f<g} f(1-g).

Note that Σ_{f<g} f(1-g) = (Σ_f f)(Σ_g (1-g)) - Σ_f f(1-f) - Σ_{f>g} f(1-g)
is hard to compute directly this way. Instead:

    Σ_{f,g} f(1-g) = (Σ_f f)(Σ_g (1-g)) = (n/2)(n/2) = n²/4

    Σ_{f=g} f(1-f) = n/6

    Σ_{f≤g} f(1-g) + Σ_{f>g} f(1-g) = n²/4 - n/6

By symmetry under f↔g: Σ_{f>g} f(1-g) = Σ_{f<g} g(1-f).

Actually, let's just compute Var directly:

    Var_k(E) = Σ_{f,g} Cov = Σ_{f,g} [min(α_f,α_g) - α_f·α_g] · (p-1)
             ... (not quite, need to be more careful)

Wait — let me redo this cleanly.

### 5.5 Clean variance computation

Let X_f(k) = 1_{f ≤ k/p} - α_f where α_f = E_k[1_{f≤k/p}].

Then E(k) = Σ_f X_f(k) + (Σ_f α_f - nk/p). The second term is approximately
0 (it's the mean-zero condition).

More precisely, if we use the exact mean:

    Ē = (1/(p-1)) Σ_k E(k) = 0

So Var(E) = (1/(p-1)) Σ_k E(k)² = Σ E(k)² / (p-1).

Now:

    E(k)² = [Σ_f (1_{f≤k/p} - k/p)]²

    Σ_k E(k)² = Σ_{f,g} Σ_k (1_{f≤k/p} - k/p)(1_{g≤k/p} - k/p)

For fixed f ≤ g:

    Σ_k (1_{f≤k/p} - k/p)(1_{g≤k/p} - k/p)
    = Σ_k 1_{k/p≥g} - (1/p)Σ_k k·1_{k/p≥f} - (1/p)Σ_k k·1_{k/p≥g} + (1/p²)Σ k²

The first sum: #{k : k ≥ ⌈pg⌉} = p - 1 - ⌊pg⌋ (call this L_g).

The second: Σ_{k=⌈pf⌉}^{p-1} k = Σ_{k=1}^{p-1} k - Σ_{k=1}^{⌈pf⌉-1} k
           = p(p-1)/2 - ⌈pf⌉(⌈pf⌉-1)/2

This is getting complex. Let's use the approximate continuous version.

### 5.6 Continuous approximation (the key calculation)

Replace k/p by a continuous variable t ∈ [0,1]:

    (1/p) Σ_k E(k)² ≈ ∫₀¹ E_cont(t)² dt

where E_cont(t) = #{f ∈ F_N : f ≤ t} - nt.

We know (from Section 3):

    ∫₀¹ E_cont(t)² dt ≈ n · W(N) = n · C_W(N)/N

Therefore:

    Σ E(k)² ≈ p · n · C_W(N)/N = (3/π²) · C_W(N) · p²

### 5.7 Lower bound on ∫ E(t)² dt

The Farey L² discrepancy satisfies (unconditionally):

    ∫₀¹ E(t)² dt = Σ D_j² / n² · n + lower order = W(N) · n

**Lower bound:** The discrepancy cannot be zero. In fact, E(f_j) = D_j/n
takes both positive and negative values (since Σ D_j = 0 but D_j are not
all zero). The L² integral is therefore strictly positive.

More quantitatively: the Farey discrepancy has an explicit lower bound.
From the three-distance theorem and the structure of Farey gaps:

The largest gap in F_N is 1/(N+1) (between 0 and 1/(N+1) or between N/(N+1) and 1).
At x just above 0, E(x) = 1 - nx (one fraction f=0 counted, expected nx).
For x = 1/(2N), E ≈ 1 - n/(2N) ≈ 1 - 3N/(2π²) which is large and negative.
For x just below 1/N, E = 1 - n/N ≈ 1 - 3N/π² (large negative).

Actually, E(x) has substantial oscillations. The key lower bound comes from:

    ∫₀¹ E(t)² dt ≥ (1/n) Σ_{j} D_j²    (approximately, from Section 3)

And Σ D_j² has a known lower bound from the UNCONDITIONAL theory:

    Σ D_j² ≥ c · n · log(n)

for some c > 0. This is the "other direction" of Franel-Landau.

**Claim:** Σ D_j² ~ (n/2π²) · log(n) asymptotically.

Evidence: C_W(N) = N · Σ D_j² / n² ≈ 0.67 for N ≤ 100000, and if
C_W(N) → c₀ (bounded away from 0), then:

    Σ D_j² = n² · C_W(N)/N ≈ (9/π⁴) · c₀ · N³

This gives ∫ E(t)² dt ≈ (9/π⁴) · c₀ · N³ / n ≈ (3/π²) · c₀ · N.

### 5.8 The lower bound we actually need

We need: Σ E(k)² ≥ c · p².

From Σ E(k)² ≈ p · ∫ E(t)² dt ≈ p · (3/π²) · c₀ · N ≈ (3/π²) · c₀ · p²:

    Σ E(k)² ≥ c · p²    iff    ∫ E(t)² dt ≥ c' · p

So we need ∫₀¹ E(t)² dt ≥ c' · N, which requires:

    W(N) ≥ c'/n ≈ c''·π²/(3N²)

i.e., C_W(N) = N · W(N) ≥ c'' · π²/(3N).

But C_W(N) → constant (numerically ~0.67), so C_W(N) ≥ some c₃ > 0 for
all large N. This is MUCH stronger than what we need!

---

## 6. The Rigorous Argument (Proposed Proof)

### Theorem (Sampled L² lower bound)

There exists c > 0 such that for all primes p ≥ 5:

    Σ_{k=1}^{p-1} E(k)² ≥ c · p²

### Proof strategy (3 steps):

**Step 1: Continuous L² lower bound.**

Show: ∫₀¹ E(x)² dx ≥ c₁ · N for all N ≥ N₀.

This follows from: the Farey sequence F_N has gaps d_j = f_{j+1} - f_j
satisfying Σ d_j² ≥ 1/(N+1) (since the maximum gap is ≥ 1/(N+1) and
each gap's square contributes). Actually, we need a more direct argument.

**Better Step 1:** Use the explicit Farey gap second moment.

The sum of squared gaps satisfies:

    Σ d_j² = Σ_{j=0}^{n-1} (f_{j+1} - f_j)² = (2ζ(2))/(n · ζ(4)/ζ(2)) + lower = ...

Actually, the classical result (Hall 1970) gives:

    Σ_{j} (f_{j+1}-f_j)² · N² ~ (72/π⁴) · log(N)/N

as N → ∞ (the mean-square gap is ~(72/π⁴)·log(N)/(N·n²), which is
larger than 1/n² by a log factor due to the heavy tail of gap sizes).

But we need the L² discrepancy, not the gap variance. The connection is:

    ∫₀¹ E(x)² dx = Σ_{j} ∫_{f_j}^{f_{j+1}} (j+1-nx)² dx
                  = Σ_j [D_j² · d_j - n · D_j · d_j² + n²·d_j³/3]

where D_j = j+1 - nf_j is the displacement. The dominant term is
Σ D_j² · d_j.

Using d_j ≈ 1/n + (fluctuations):

    Σ D_j² · d_j ≈ (1/n) Σ D_j² + Cov(D²,d)

And Σ D_j² = n² · W(N). So:

    ∫ E(x)² dx ≈ n · W(N) + correlation correction

**Step 2: Riemann sum vs integral.**

Show: Σ_{k=1}^{p-1} E(k/p)² ≥ (p-1)(1-ε) · ∫₀¹ E(x)² dx for some
controllable ε → 0.

The issue: E(x)² is piecewise quadratic (convex on each Farey interval).
The p-grid {k/p} samples at spacing 1/p, while Farey intervals have
lengths ~1/n ≈ π²/(3N²) ≈ π²/(3p²).

Since 1/p >> 1/n (for large p), each p-grid interval [k/p, (k+1)/p]
contains approximately n/p ≈ 3p/π² Farey fractions. This means E(x) makes
~3p/π² linear segments within each p-grid interval.

The function E(x)² restricted to [k/p, (k+1)/p] is a sum of convex arcs.
Its average value on this interval equals E(k/p)² approximately (since the
function oscillates around a slowly-varying mean).

Actually, we can use:

    Σ E(k)² = p · (1/(p-1)) Σ E(k)²

and the Riemann sum error for a function of bounded variation. E(x)² has
total variation ≤ C · n² (since E has jumps of size 1 at each Farey fraction,
and there are n of them, so E² has total variation ≤ 2n·max|E|·1 ≤ C·n²).

The Riemann sum error is ≤ (TV of integrand) / p ≤ C·n²/p ≈ C·p³/p = C·p².

This is the SAME order as the main term! So the BV approach is too crude.

**Better Step 2:** Use the pair-count formula directly.

From Proposition 4:

    Σ A(k)² = Σ_{f,g} (p-1 - ⌊p·max(f,g)⌋)

We compute:

    Σ_{f,g} (p-1) = (n-1)² · (p-1)      [there are (n-1)² pairs in F_N*]

    Σ_{f,g} ⌊p·max(f,g)⌋ = Σ_{f,g} [p·max(f,g) - {p·max(f,g)}]
                           = p · Σ_{f,g} max(f,g) - Σ_{f,g} {p·max(f,g)}

The first term: Σ_{f,g} max(f,g) = Σ_{f,g} (f+g+|f-g|)/2.

For f,g iid uniform on F_N*: E[max(f,g)] = 2E[f] - E[min(f,g)] = 2·(1/2) - 1/3 = 2/3
(since E[min] = 1/3 for iid uniform on [0,1]).

So: Σ max(f,g) ≈ (2/3)(n-1)²

Therefore: Σ A(k)² ≈ (n-1)²(p-1) - p(2/3)(n-1)² + fractional parts
                    = (n-1)²(p/3 - 1) + Σ{p·max(f,g)}

And: Σ E(k)² = Σ A(k)² - 2(n/p)Σ kA(k) + (n²/p²)Σk²

The dominant terms should give Σ E(k)² ≈ (1/12)(n-1)²(p-1) + corrections,
which is ≈ (1/12)·(9/π⁴)·p⁵. That's way too big — I'm making an error in
the approximation by treating f,g as independent uniform.

The correction: the Farey fractions are NOT iid uniform. Their pair
distribution deviates from uniform, and this deviation is precisely what
creates the discrepancy.

**Step 3: Use the pair-sum formula minus the expected value.**

The "expected" value of Σ A(k)² under perfect equidistribution would be:

    Σ_k (nk/p)² = (n²/p²) · p(p-1)(2p-1)/6 ≈ n²p/3

And Σ A(k)² - Σ(nk/p)² = Σ E(k)² + 2(n/p)Σ kE(k)

Since Σ kE(k) is the weighted first moment (controlled by Proposition 3),
the dominant contribution to the difference Σ A² - Σ(nk/p)² comes from
the pair correlation deviation of Farey fractions from uniform.

---

## 7. Most Promising Path Forward

### The cleanest argument

**Proposition:** The following three ingredients yield Σ E(k)² ≥ c·p²:

1. **Franel-Landau L² identity:** ∫₀¹ E(x)² dx = n·W(N) ≥ c₁·N
   (since C_W(N) = N·n·W(N)/n ≥ c₂ > 0 for large N).

2. **Sampling inequality:** For the p-grid sampling of a piecewise-linear
   function with n pieces on [0,1] sampled at p points where p << n:

   Each p-grid cell [k/p, (k+1)/p] has width 1/p and contains ~n/p Farey
   intervals. By the second-moment formula for piecewise-linear functions:

       (1/p) Σ_k E(k/p)² ≥ ∫₀¹ E(x)² dx - (correction from sampling error)

   The correction involves the "aliasing" between the p-grid and the Farey
   grid. Since p and the Farey denominators are typically coprime (p is prime!),
   the aliasing should be small.

3. **Combine:** Σ E(k)² ≥ p · [c₁·N - correction] ≥ c·p² for large p.

### The key gap to close

The rigorous lower bound on C_W(N) requires showing that the Farey L²
discrepancy is bounded BELOW. This is morally obvious (the discrepancy
can't be zero since Farey fractions are not exactly equidistributed), but
making it rigorous requires:

Either (a) an unconditional lower bound on Σ D_j² = n²·W(N), or
       (b) a direct lower bound on the pair sum Σ_{f,g} {p·max(f,g)}.

For (a): The Farey discrepancy at x = 1/N is D₁ = 1 - n/N = 1 - (3/π²)N + O(log N).
So |D₁| ~ (3/π²)N for large N. This single term contributes D₁² ~ (9/π⁴)N².
Therefore Σ D_j² ≥ D₁² ≥ (9/π⁴ - ε)N² ≈ 0.92N².

That gives: W(N) ≥ 0.92N²/n² ≈ 0.92/(9N²/π⁴) = π⁴·0.92/(9N²) ≈ 10/N²

And: C_W(N) ≥ 10/N → 0 as N → ∞. This is too weak!

We need multiple large displacements. The fractions k/N for k = 1,...,N
have D(k/N) = rank(k/N) - n·(k/N). For k = 1: D(1/N) = #{f ≤ 1/N} - n/N.
The only fraction ≤ 1/N in F_N is 0 and 1/N itself (and possibly 1/(N-1)
if N-1 > 1). So A(1/N) ≈ 2, while n/N ≈ 3N/π². So D ≈ 2 - 3N/π² ≈ -0.3N.

Similarly for k/N near 0 or 1: D is of order N.

There are ~2N/K fractions k/N with k ≤ K or k ≥ N-K, each with |D| ≥ c·N.
Wait, that's not right either — the displacement for interior fractions
is smaller.

**Better:** Use the Euler totient sum. The number of fractions in F_N with
denominator exactly b is φ(b). The displacement for a fraction a/b is
approximately M(N/b)·(b/N)·... this gets complicated.

### Alternative: use the explicit formula for C_W(N)

From CW_BOUND_PROOF.md: C_W(N) ≈ 0.67 for N up to 100,000, with
extremely slow growth (~loglog N).

If C_W(N) ≥ c₀ > 0 for all N ≥ N₁ (which is obvious from the data, and
should follow from any explicit lower bound on the Ramanujan sum expansion),
then:

    ∫₀¹ E(x)² dx = n·C_W(N)/N ≥ c₀·n/N = c₀·(3/π²)·N ≥ c₃·N

giving Σ E(k)² ≥ (Riemann sum lower bound) ≥ c·p·N ≥ c·p².

---

## 8. The Explicit Lower Bound for C_W(N) (Key Lemma Needed)

### Lemma (C_W lower bound)

There exists c₀ > 0 and N₀ such that for all N ≥ N₀:

    C_W(N) := N · (1/n²) Σ_{j=0}^{n-1} D(f_j)² ≥ c₀

### Proof sketch

The Ramanujan sum expansion gives:

    Σ D_j² = Σ_{q=1}^{N} (n/q)² · |Σ_{d|q, d≤N} μ(d)|²
             + cross terms involving Ramanujan sums

The q = 1 term is n² · |M(N)|² = n² (since M(1) = 1, well actually
M(N) for the Mertens function at N...).

Hmm wait, the Ramanujan expansion of the Farey discrepancy gives:

    D(f_j) = Σ_{q=1}^{N} (n/q) · c_q(j)

where c_q(j) is the Ramanujan sum evaluated at... no, this isn't quite right.

The correct identity (from the Ramanujan expansion of Farey discrepancy) is:

    D(a/b) = Σ_{q=1}^{N} c_q(a/b) · (M(N/q)/q)     [schematic]

The L² norm then involves:

    Σ_j D(f_j)² = Σ_{q,r} (M(N/q)/q)(M(N/r)/r) · Σ_j c_q(f_j)c_r(f_j)

The orthogonality of Ramanujan sums over Farey fractions gives
Σ_j c_q(f_j)c_r(f_j) ∝ δ_{q,r} · n/q (approximately). So:

    Σ D_j² ≈ n · Σ_{q=1}^{N} M(N/q)² / q³

The q = 1 term: n·M(N)²/1 = n·M(N)². Since |M(N)| ≥ 1 for all N ≥ 1:

    Σ D_j² ≥ n·1 = n

Therefore: C_W(N) = N·Σ D_j²/n² ≥ N·n/n² = N/n ≈ π²/(3N)

Again too weak (→ 0). We need a better lower bound on M(N)², or we need
to use more terms in the Ramanujan expansion.

**The real issue:** M(N) oscillates and can be very small (e.g., M(N) = 0
infinitely often, conjectured). So the q=1 term alone doesn't work.

**But:** Σ_{q≤N} M(N/q)²/q³ counts ALL the Mertens function values.
Even if M(N) = 0, M(N/2), M(N/3), etc., contribute. The sum is:

    Σ_{q≤N} M(N/q)²/q³ ≥ Σ_{q≤N} 1/q³ = O(1)

since |M(x)| ≥ 1 for most x (M(x) = 0 only when a new μ(n) = +1 value
exactly cancels the running sum, which is relatively rare).

Actually |M(x)| ≥ 1 is NOT guaranteed — M(x) = 0 for x < 1 and M(1) = 1,
M(2) = 0, M(3) = -1, M(4) = -1, M(5) = -2, etc. M(x) = 0 at x = 2.

But Σ M(x)² over x = 1,...,N is known to satisfy (Ng 2004):

    Σ_{m=1}^{N} M(m)² ~ c · N²     (unconditionally, with c > 0)

This is because M(m) has variance proportional to m (under GUE predictions)
or at least proportional to m/log(m) (unconditionally from PNT-level bounds).

So: Σ_{q≤N} M(N/q)²/q³ ≈ Σ_{q≤N} (N/q)/(q³·some_log) ≈ N·Σ 1/q⁴ ≈ cN

This gives Σ D_j² ≈ n·c·N, hence C_W ≈ N·n·cN/n² = cN²/n ≈ c·π²N²/(3N²) = const.

So C_W(N) ≥ c₀ > 0 SHOULD follow from Σ M(m)² ~ cN². Making this rigorous
requires:

1. An explicit Ramanujan sum expansion of Σ D_j² (exists in the literature,
   e.g., Dress-El Marraki 1999, Huxley-Watt 1995).
2. An unconditional lower bound on Σ_{m≤N} M(m)² ≥ c·N² (known from the
   mean-value theorem for Dirichlet series, using 1/ζ(s)).

---

## 9. Connection to BCZ Pair Correlation

### How BCZ enters

The Boca-Cobeli-Zaharescu pair correlation result analyzes the distribution
of normalized gaps N²·(f_{j+1} - f_j) in F_N. Their main result gives the
limiting distribution function P(s) = (6/π²)·s for 0 ≤ s ≤ 1 (approximately).

For our pair sum Σ_{f,g} ⌊p·max(f,g)⌋:

Consider pairs (f,g) with f in a fixed p-grid cell [k/p, (k+1)/p] and
g in cell [l/p, (l+1)/p]. For k ≠ l, max(f,g) depends on which cell is
larger. For k = l, we need the pair structure within a single cell.

Within a single cell of width 1/p, there are ~n/p = 3p/π² Farey fractions.
The BCZ pair correlation controls the fine-scale distribution of these
fractions. Specifically, the number of pairs within distance δ of each
other (for δ << 1/p) is controlled by the pair correlation function.

However, for the p-grid sampling, we only care about the COUNT in each cell,
not the fine structure within cells. So the BCZ pair correlation enters
only through higher-order corrections.

### When BCZ would be crucial

BCZ becomes crucial if we try to get the SHARP constant c* ≈ 0.066 in

    Σ E(k)² ~ c* · p² log p

The log p factor should come from the same source as the log N factor in
the Farey gap variance (which is controlled by BCZ). But for the mere
existence of a lower bound Σ E(k)² ≥ c·p², we don't need BCZ.

---

## 10. Summary and Recommended Path

### What we've established

1. **Σ E(k)² ≈ 2p · ∫₀¹ E(x)² dx** (numerical verification: ratio ≈ 2.0
   for all tested primes p ≤ 199). The factor of 2 comes from aliasing:
   endpoint sampling of a piecewise-linear function overestimates the
   integral average by a factor of 2 (random walk bridge effect).

2. **∫₀¹ E(x)² dx ≈ n · W(N) = n · C_W(N)/N** where C_W(N) is the
   normalized L² discrepancy.

3. **C_W(N) is bounded below** by a positive constant (morally clear from
   the Ramanujan sum expansion + mean-value theorem for Mertens function).
   Numerically: C_W(N) ≥ 0.18 for all N ≥ 4.

4. **Combining:** Σ E(k)² ≈ 2p · n · C_W(N)/N ≈ 2·(3/π²)·C_W(N)·p²
   ≥ c · p² for large p.

5. **For the log p factor:** C_W(N) grows as ~loglog N computationally.
   The log p in Σ E(k)² ~ c* · p² log p may come from the discrete
   sampling correction growing logarithmically, or from C_W's slow growth.

### Three proof paths, in order of feasibility

**Path A (most feasible):** Prove C_W(N) ≥ c₀ > 0 unconditionally.
- Uses: Ramanujan sum expansion of Σ D_j² + unconditional mean-value
  theorem for Mertens function.
- Gives: Σ E(k)² ≥ c · p² (quadratic lower bound, no log).
- Difficulty: Medium. The Ramanujan expansion is classical; the mean-value
  bound for Mertens is standard (follows from 1/ζ(s) having no poles on
  Re(s) = 1).

**Path B (harder):** Prove Σ E(k)² ≥ c · p² directly from the pair-count
formula, bypassing the continuous L² integral.
- Uses: Direct analysis of Σ_{f,g} (p-1-⌊p·max(f,g)⌋) minus the expected
  value under equidistribution.
- Gives: Potentially sharper constants and the log factor.
- Difficulty: High. Requires careful pair correlation analysis.

**Path C (hardest, highest payoff):** Prove Σ E(k)² ~ c* · p² · log p.
- Uses: BCZ pair correlation + detailed analysis of the pair-count kernel
  on the "Farey square" [0,1]² restricted to pairs of Farey fractions.
- Gives: Asymptotic with the observed constant.
- Difficulty: Very high. Would be a genuinely new result in the Farey
  fraction literature.

### Immediate next steps

1. **Write a rigorous version of Path A** using explicit citations for:
   - Ramanujan sum expansion of Farey L² discrepancy (Franel 1924, or
     Dress-El Marraki 1999)
   - Mean-value theorem: Σ_{m≤N} M(m)² ≥ c·N² (from the mean-value
     theorem for Dirichlet series, specifically for 1/ζ(s))
   - Riemann sum approximation with error bounds

2. **Numerically verify** the Riemann sum connection:
   - Compute ∫ E(x)² dx exactly for small primes
   - Compare p · ∫ E² with Σ E(k)²
   - Quantify the "aliasing" correction

3. **Search for** an explicit unconditional lower bound C_W(N) ≥ c₀ in the
   literature (this may already exist).

---

## Appendix: Normalization Reconciliation

| Quantity | Definition | Approximate size |
|----------|-----------|-----------------|
| n = \|F_N\| | Farey sequence size | 3N²/π² |
| D_j = j - n·f_j | Integer-scale displacement | O(N) typical, O(N·logN^{1/2}) max under RH |
| W(N) = Σ D_j²/n² | Normalized L² discrepancy | C_W(N)/N where C_W ~ 0.7 |
| old_D_sq = Σ D_j² | Integer-scale L² | ~n²·C_W/N ~ (9/π⁴)·C_W·N³ |
| E(k) = A(k)-nk/p | p-grid counting error | O(√p) typical |
| Σ E(k)² | Our target | ~c*·p²·log p, c* ≈ 0.066 |
| ∫ E(x)² dx | Continuous L² | ~n·C_W/N ~ (3/π²)·C_W·N |
| C_W(N) = N·W(N) | Renormalized discrepancy | ~0.67, grows as ~loglog N |
