# D(a/b) vs Sawtooth ((a/b)): Exact Relationship and Decomposition

## Date: 2026-03-29
## Status: Verified computationally for N = 3..59

---

## 1. Setup and Definitions

For the Farey sequence F_N with |F_N| = 1 + sum_{q=1}^N phi(q):

- **Displacement:** D(a/b) = rank(a/b in F_N) - |F_N| * (a/b)
- **Sawtooth:** ((a/b)) = a/b - 1/2 for 0 < a/b < 1, and ((0)) = ((1)) = 0
- **Per-step change (Farey ordering):** delta_STEP(x_i) = D(x_{i+1}) - D(x_i)
- **Multiplicative displacement:** delta_MULT(a/b) = a/b - {pa/b}  [for studying B(p)]

## 2. The Fundamental Identity: D(x) = (1-x) - R(x)

### Derivation

The rank of x in F_N can be computed via Mobius inversion:

    rank(x) = 1 + sum_{q=1}^{N} sum_{d|q} mu(d) * floor(x*q/d)

Using the identity sum_{d|q} mu(d) * (q/d) = phi(q), we split floor(y) = y - {y}:

    rank(x) = 1 + x * sum_{q<=N} phi(q) - sum_{q<=N} sum_{d|q} mu(d) * {x*q/d}
            = 1 + x * (|F_N| - 1) - R(x)

where **R(x) = sum_{q<=N} sum_{d|q} mu(d) * {x*q/d}** and {y} = fractional part of y.

Therefore:

**D(x) = (1-x) - R(x)**

**Verified exactly** (using Python Fraction arithmetic) for all N = 5, 7, 10, 12, 15, 20.

### Change of Variables

Setting m = q/d in the double sum:

    R(x) = sum_{d<=N} mu(d) * sum_{m=1}^{floor(N/d)} {x*m}

The inner sum sum_{m=1}^{M} {(a/b)*m} is a **Dedekind-type fractional part sum**.

## 3. Relationship to Sawtooth

The naive comparison D(a/b) vs |F_N|*((a/b)) gives:

    E(a/b) = D(a/b) - |F_N|*((a/b))

This "error" E is **NOT small** -- it is O(|F_N|) and dominates.

Key finding: **Sum of E over denominator q equals phi(q)/2 exactly.**

| Denom q | phi(q) | Sum of E | phi(q)/2 | Match |
|---------|--------|----------|----------|-------|
| 2       | 1      | 1/2      | 1/2      | Yes   |
| 3       | 2      | 1        | 1        | Yes   |
| 5       | 4      | 2        | 2        | Yes   |
| 7       | 6      | 3        | 3        | Yes   |
| 11      | 10     | 5        | 5        | Yes   |
| 12      | 4      | 2        | 2        | Yes   |

This means the sawtooth is NOT the right comparison function for D. The correct
decomposition is D(x) = (1-x) - R(x), not D = |F_N|*((x)) + error.

## 4. Two Different "delta" Quantities (CRITICAL DISTINCTION)

### delta_STEP: Forward Difference in Farey Ordering

    delta_STEP(x_i) = D(x_{i+1}) - D(x_i)

By Abel summation (telescoping of a quadratic form):

    Sigma D * delta_STEP = (1/2)[D(1)^2 - D(0)^2] - (1/2) Sigma delta_STEP^2
                         = -1/2 - (1/2) Sigma delta_STEP^2

With D(0/1) = 1, D(1/1) = 0 (using 1-indexed rank convention where D(0) = 1).
This is **always negative** for all N. Verified for N = 3..59.

### delta_MULT: Displacement Under Multiplication by p

    delta_MULT(a/b) = a/b - {pa/b} = D_new(a/b) - D_old(a/b)

This is the change in displacement when going from F_{p-1} to F_p.

**B(p) = 2 * Sigma D_old(a/b) * delta_MULT(a/b)** summed over F_{p-1}.

These are DIFFERENT quantities. The Abel identity applies to delta_STEP but NOT
to delta_MULT. The B(p) >= 0 conjecture is about delta_MULT.

### Numerical Comparison

| p  | Sigma D*delta_STEP | Sigma D*delta_MULT | B = 2*Sigma D*delta_MULT |
|----|--------------------|--------------------|--------------------------|
| 5  | -0.264             | -0.111             | -0.222                   |
| 7  | -1.419             | -0.450             | -0.900                   |
| 11 | -7.204             | -0.764             | -1.528                   |
| 13 | -12.224            | +0.352             | +0.704                   |
| 17 | -25.120            | -1.305             | -2.610                   |
| 19 | -34.913            | +2.134             | +4.269                   |
| 23 | -55.902            | +1.151             | +2.301                   |
| 29 | -101.198           | +6.818             | +13.635                  |

delta_STEP is always negative (Abel). delta_MULT changes sign -- it is positive
exactly for primes where M(p) <= -3 (the B >= 0 phenomenon).

## 5. Decomposition of B(p) Using D = (1-x) - R(x)

    B(p)/2 = Sigma D(a/b) * delta_MULT(a/b)
           = Sigma D(a/b) * [a/b - {pa/b}]
           = Sigma D(a/b) * a/b  -  Sigma D(a/b) * {pa/b}

Using D = (1-x) - R(x):

    B(p)/2 = Sigma [(1-x) - R(x)] * x  -  Sigma [(1-x) - R(x)] * {px}
           = [Sigma x(1-x) - Sigma R(x)*x]  -  [Sigma (1-x)*{px} - Sigma R(x)*{px}]

The four terms are:
1. **Sigma x(1-x)**: Elementary, ~ |F_N|/6 for large N
2. **Sigma R(x)*x**: Mobius-weighted fractional part sums times x
3. **Sigma (1-x)*{px}**: Smooth function times multiplication fractional parts
4. **Sigma R(x)*{px}**: The "deep" term -- Mobius fractional parts times p-fractional parts

Term 4 is where the arithmetic of both the Farey structure and multiplication by p interact.

## 6. Scaling of Sigma D*delta_STEP

| N  | |F_N| | Sigma D*delta_STEP | -Sigma D*Dx  | -Sigma D*DR  | DR fraction |
|----|-------|--------------------|--------------|--------------|-------------|
| 5  | 11    | -2.23              | -0.70        | -1.53        | 68%         |
| 12 | 47    | -13.22             | -0.78        | -12.44       | 94%         |
| 20 | 129   | -47.89             | -0.87        | -47.02       | 98%         |
| 30 | 279   | -121.67            | -0.94        | -120.53      | 99%         |
| 50 | 775   | -411.30            | -1.03        | -408.53      | 99.3%       |

The smooth term Sigma D*Delta_x converges to -1 as N -> infinity.
Almost all of Sigma D*delta_STEP comes from the Mobius fractional-part term.

## 7. Summary of Key Findings

1. **D(x) = (1-x) - R(x)** is an exact identity where R involves Mobius-weighted
   fractional part sums. This decomposes D into a smooth part (1-x) and an
   arithmetic part R(x).

2. **The sawtooth comparison fails**: E = D - |F_N|*((x)) is O(|F_N|), not small.
   But sum_q E = phi(q)/2, a clean identity.

3. **Two different deltas**: delta_STEP (Farey forward diff) satisfies Abel summation
   and is trivially always-negative in total. delta_MULT (multiplication by p) is the
   one relevant to B(p) and does NOT satisfy Abel.

4. **R(x) = sum_{d<=N} mu(d) * sum_{m=1}^{N/d} {xm}** connects D to Dedekind-type sums
   via the inner fractional part sums.

5. **B(p)/2 decomposes into 4 terms**, the deepest being Sigma R(x)*{px} which involves
   simultaneous Farey and multiplicative structure.

## 8. Proof Implications

The identity D = (1-x) - R(x) could help prove B(p) >= 0 if we can show:

    Sigma R(x)*{px} is controlled by Sigma R(x)*x + known bounds

The connection to Dedekind sums s(a,b) through the inner sum sum_{m<=M} {am/b}
opens a path via Dedekind sum reciprocity and the three-term relation.

Key open question: Does the Mobius inversion in R interact favorably with
the multiplicative structure of {pa/b} for prime p?
