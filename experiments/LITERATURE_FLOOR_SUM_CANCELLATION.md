# Literature Survey: Cancellation in Sums of Floor Functions

**Date:** 2026-03-30
**Status:** Initial survey complete
**Verdict:** No known result gives the uniform six-term cancellation bound we need. Several partial tools exist.

---

## 1. Six-Term Floor Sums: No Direct Precedent Found

**Query:** Results on sums of the form Sum_{t=0}^{5} E_{m+t}(n) where E_r(n) = Sum_{n/3 < v <= n/2} (rv mod n - v).

**Finding:** No literature was found addressing cancellation in sums of consecutive-index floor sums of this specific form. The closest structural relatives are:

- **Ramanujan's floor function identities** (JIMS problems): Ramanujan proved identities like floor(n/3) + floor((n+2)/6) + floor((n+4)/6) = floor(n/2) + floor((n+3)/6). These involve *exact* cancellation for small fixed moduli, not asymptotic cancellation for growing parameters.

- **Telescoping sums:** Standard telescoping (a_n - a_{n+1} cancellation) does not apply here because the E_r(n) terms are not differences of a common sequence in r.

- **Steven Brown (arXiv:2507.11666):** Studies S_r(n,m) = Sum_{k=1}^{n-1} floor(km/n)^r, with closed forms for r=2,3 and connections to generalized Dedekind sums. Not directly applicable to our windowed sums, but the techniques (reciprocity, Euclidean algorithm reduction) may be relevant.

**Gap:** The six-term structure with consecutive r-values summed over a window (n/3, n/2] appears to be novel. No literature addresses whether consecutive Dedekind-sum-like objects exhibit systematic cancellation.

---

## 2. Window Sums of Multiplication Maps

**Query:** Bounds for Sum_{v in W} (rv mod n - v) for windows W subset [1,n].

**Finding:** This is closely related to **partial Dedekind sums** (sums of the sawtooth function ((rv/n)) over a subinterval).

### Key references:

- **Dedekind sums** s(r,n) = Sum_{v=1}^{n-1} ((v/n))((rv/n)) sum over the *full* range [1,n-1]. The reciprocity law s(r,n) + s(n,r) = (r/n + 1/(rn) + n/r)/12 - 1/4 (Dedekind, 1880s) gives exact evaluation for the complete sum.

- **Partial Dedekind sums** (sums restricted to a subinterval) are much harder. No clean reciprocity law is known for partial sums. The Fourier expansion of the sawtooth function ((x)) = -Sum_{k=1}^{infty} sin(2 pi k x)/(pi k) can be used to write partial sums as exponential sums, but the resulting bounds are not sharp.

- **Bordelles (arXiv:1901.00170):** Establishes upper bounds for sums of fractional parts of smooth functions using Weyl's bound and Popov's device. The improvement comes from better handling of the main term. Relevant technique but does not address the parameter-dependence issue.

**Key difficulty:** For the multiplication map v -> rv mod n, the discrepancy of {rv/n} in a window depends on gcd(r,n) and the continued fraction expansion of r/n. This makes uniform-in-r bounds fundamentally harder than fixed-r bounds.

---

## 3. Equidistribution of {rv/n} in Windows

**Query:** Explicit error terms for equidistribution of {rv/n} as v ranges over a subinterval, uniform in r.

### What is known:

- **Erdos-Turan inequality:** D_N <= C(1/H + (1/N) Sum_{h=1}^{H} (1/h)|Sum_{v} e(hrv/n)|) for arbitrary H. The exponential sum Sum_{v in [a,b]} e(hrv/n) is a geometric sum that can be evaluated: it equals O(min(b-a, 1/||hr/n||)) where ||x|| is distance to nearest integer.

  For fixed r coprime to n, summing over h gives D = O((log n)/n * (number of "resonant" h)). But the constant depends on the continued fraction of r/n, hence is NOT uniform in r.

  **Best known constants:** Admissible pairs (c_1, c_2) in the inequality include (1, 0.653) and (1.1435, 2/pi). See work by Vaaler on refinements.

- **Vaaler's trigonometric polynomial approximation:** The sawtooth function psi(x) = {x} - 1/2 can be approximated by a trigonometric polynomial psi*(x) of degree M with error bounded by a Fejer-kernel-type expression: |psi*(x) - psi(x)| <= Sum_{|m|<=M} b_M(m) e(mx), where b_M(m) = (1/(2M+2))(1 - |m|/(M+1)). This is fundamental for converting floor-function sums into exponential sums.

- **Denjoy-Koksma inequality:** For irrational rotation by alpha with rational approximation p/q, the ergodic sum deviates from its mean by at most the total variation of the function. This gives O(1) bounds per period but does not help with rational r/n.

- **Koksma-Hlawka inequality:** Error = V(f) * D_N where V is the variation in the sense of Hardy-Krause and D_N is the star-discrepancy. For the sawtooth (variation = 1 per period), the error for N points in a window of size ~n/6 is O(D_{n/6}). The discrepancy D_{n/6} for the sequence {rv/n} depends on r through the Erdos-Turan bound.

### The uniformity problem:

**For r coprime to n:** The sequence {v*r/n} for v = 1,...,n is a permutation of {1/n, 2/n, ..., (n-1)/n, 0}, so the full-range discrepancy is O(1/n). But restricting to a *window* v in (n/3, n/2] breaks this permutation structure.

**For general r:** If gcd(r,n) = d, the sequence {rv/n} takes only n/d distinct values, each repeated d times. The discrepancy over a window is then O(d/n * window_size) = O(d * |W|/n), which can be as large as O(|W|) when d is large.

**Conclusion:** No uniform-in-r bound exists for window discrepancy that avoids dependence on gcd(r,n) or continued fraction data. The best one can hope for is bounds that are uniform over r coprime to n, and these still depend on the quality of rational approximations to r/n.

---

## 4. Mobius-Weighted Sums: Connection to Ramanujan Sums

**Query:** Cancellation in Sum_{d|n} mu(d) * d * E_r(n/d).

### Relevant theory:

- **Ramanujan sums via Kluyver's formula:** c_q(n) = Sum_{d|gcd(n,q)} mu(q/d) * d. This expresses the Ramanujan sum as a Mobius-weighted divisor sum. The key property is that c_q(n) is multiplicative in q (for fixed n) and satisfies |c_q(n)| <= gcd(n,q).

- **Mobius inversion and floor functions:** The generalized Mobius inversion formula states: if g(n) = Sum_{m<=n} f(floor(n/m)), then f(n) = Sum_{m<=n} mu(m) * g(floor(n/m)). This is the "floor function" version of Mobius inversion (distinct from the divisor-sum version).

- **Apostol (Pacific J. Math., 1972):** Studied generalized Ramanujan sums S_{f,g}(m,k) as Dirichlet convolutions. For fixed k, S_{f,g}(m,k) can be expressed as a convolution, and the special case g = mu recovers standard Mobius inversion.

### The critical connection:

The sum Sum_{d|b} mu(d) * Sum_{v in window} (rv mod (b/d)) can potentially be rewritten using the identity:

  Sum_{d|b} mu(d) * e(rv*d/b) = c_b(rv)  (up to normalization)

where c_b is the Ramanujan sum. If b = n and the window sum can be expressed via exponential sums, then:

  Sum_{d|n} mu(d) * Sum_{v in W} {rv/(n/d)} = Sum_{v in W} Sum_{d|n} mu(d) * {rvd/n}

The Fourier expansion of {x} converts this to sums involving c_n(rv*k) for various k, which are Ramanujan sums. Since |c_n(m)| <= gcd(m,n), this gives cancellation when gcd(rv,n) is small for most v.

**However:** The sawtooth {x} is not a character, so the interchange of summation is not clean. The Fourier expansion introduces an infinite series Sum_{k>=1} sin(2 pi k x)/(pi k) which converges only conditionally, making rigorous bounds delicate.

### Barban-Davenport-Halberstam connection:

The BDH theorem bounds the mean square of the error in the prime number theorem for arithmetic progressions: Sum_{q<=Q} Sum_{a mod q} |psi(x;a,q) - x/phi(q)|^2 = O(Qx log x).

**Harper (2025)** proved BDH-type asymptotics for general (possibly very sparse) sets using simple direct methods avoiding exponential sums. This is relevant because:
- Our Mobius-weighted sums average over divisors of n, which is a form of averaging over "moduli"
- BDH shows that on average over moduli, the error is small even if individual errors are large
- The analogy: Sum_{d|n} mu(d)^2 * |E_r(n/d)|^2 might be bounded by a BDH-type result

**Gap:** No one has applied BDH-type averaging specifically to Dedekind-sum-like objects or floor-function sums over windows.

---

## 5. Koksma-Hlawka with Parameter Dependence

**Query:** Koksma-Hlawka bounds where the "variation" term depends on a parameter r.

### What is known:

- **Standard Koksma inequality (1-D):** |Sum f(x_v)/N - integral f| <= V(f) * D_N, where V(f) is the total variation of f.

- For f(v) = rv mod n (or equivalently f(v) = n * {rv/n}), the total variation over v in [1,n] is O(r) (the function has ~r jumps of size ~n, or equivalently the sawtooth {rv/n} has r periods of variation 1 each).

- **Over a window (n/3, n/2]:** The variation of v -> {rv/n} is O(r * |W|/n) = O(r/6) for |W| ~ n/6. Combined with the discrepancy D_{|W|} = O(log n / |W|) for a "generic" r, this gives an error of O(r * log n / n).

- **This is O(n) only when r = O(n/log n).** For r ~ n, the Koksma bound gives O(n), which is trivial.

### Improving the bound:

- **Vaaler's method** replaces the sawtooth by a trigonometric polynomial of degree M, converting the sum to an exponential sum plus an error of O(n/M). The exponential sum can then be bounded by Weyl/van der Corput methods. For the specific sum Sum_{v in W} {rv/n}, this gives O(n/M + M * max_h |S_h|) where S_h = Sum_{v in W} e(hrv/n).

- **Harman's variation on Koksma-Hlawka** (Liverpool, 2010): Uses a different measure of variation that applies to a wider class of functions, potentially giving better bounds for discontinuous functions like the sawtooth.

### The uniformity question:

**A uniform O(n) bound independent of r does NOT follow from standard methods.** The reason is fundamental: when r and n share a large gcd d, the multiplication map v -> rv mod n has only n/d distinct values, creating gaps of size d in the image. The discrepancy of this "sparse" sequence in a window is O(d * |W|/n), not O(|W|/n).

**Possible escape routes:**
1. Average over r: Sum_{r=1}^{n} |E_r(n)|^2 might be O(n^2) by orthogonality, giving E_r = O(n) for "most" r. This is a large-sieve-type argument.
2. Restrict to r coprime to n: Then gcd(r,n) = 1 and the sequence {rv/n} is a permutation of {v/n}. Window discrepancy is then O(log n / n) by Erdos-Turan.
3. Use the six-term structure: If the six consecutive r-values have a special algebraic relationship (e.g., if E_{m+t} can be related to E_m via a shift identity), cancellation might occur for structural reasons rather than analytic ones.

---

## 6. Summary of Available Tools

| Tool | What it gives | Limitation for our problem |
|------|--------------|---------------------------|
| Dedekind reciprocity | Exact evaluation of full-range sawtooth sums | Does not extend to partial/window sums |
| Erdos-Turan inequality | D_N <= O(1/H + exponential sum bound) | Constant depends on r via continued fractions |
| Vaaler approximation | Converts floor sums to exponential sums | Still need to bound the exponential sum |
| Koksma-Hlawka | Error <= Variation * Discrepancy | Variation is O(r), making bound O(r * D_N) |
| Ramanujan sum / Kluyver | Sum_{d|n} mu(d) f(d) = Ramanujan-type expression | Applies to multiplicative structure, not directly to window sums |
| BDH theorem | Mean-square error over moduli is small | Not applied to Dedekind-sum-like objects |
| Large sieve | Sum_r |exponential sum|^2 <= (N + H) * sum |a_n|^2 | Gives average-over-r bounds, not pointwise |
| Vardi (1993) | Dedekind sums have Cauchy limiting distribution | Distribution result, not uniform bound |

---

## 7. Key Papers to Obtain and Read in Full

1. **Bordelles, "Sums of certain fractional parts" (arXiv:1901.00170)** -- Explicit bounds using Weyl + Popov for sums of fractional parts. Most relevant for our window sums.

2. **Conrey-Franson-Klein-Scott, "Mean Values of Dedekind Sums" (J. Number Theory 56, 1996)** -- Average of Dedekind sums over r coprime to k. Shows s(r,k) = O(log^{1+eps} k) for almost all r. Directly relevant to bounding E_r.

3. **Harper, "Simple BDH-type asymptotics for general sequences" (Warwick, 2025)** -- Modern BDH for sparse sets. Could potentially be applied to our setting.

4. **Lemke Oliver-Soundararajan, "Distribution of consecutive prime biases"** -- Uses Fejer-kernel windowing of sawtooth sums with explicit bounds. Technique directly applicable to our windowed sums.

5. **Vaaler, "Refinements of the Erdos-Turan inequality"** -- The extremal function method for sawtooth approximation.

6. **Brown, "Floor function powers and generalized Dedekind sums" (arXiv:2507.11666)** -- Recent work connecting floor sums to Dedekind sums with closed forms.

7. **Apostol, "Arithmetical properties of generalized Ramanujan sums" (Pacific J. Math. 41, 1972)** -- Convolution identities for generalized Ramanujan sums.

---

## 8. Assessment for Our Problem

### What we need:
A bound showing that Sum_{t=0}^5 E_{m+t}(n) = O(n) with the implied constant INDEPENDENT of m and n.

### What exists:
- For *fixed* r, each E_r(n) = O(n) with constant depending on r (via Koksma). The constant grows as O(r).
- For r coprime to n, each E_r(n) = O(n * log n / n) = O(log n) by Erdos-Turan. The six-term sum is O(log n).
- For *average* over r, the mean-square of E_r(n) is O(n) by large-sieve / orthogonality.
- For the Mobius-weighted version, Ramanujan sum identities reduce the problem to bounding c_n(rv) which is bounded by gcd(rv,n).

### What does NOT exist (to our knowledge):
- A uniform-in-r bound for six-term partial Dedekind sums.
- A proof that consecutive r-values produce cancellation in the six-term sum.
- Any application of BDH-type averaging to Dedekind sums over windows.

### Recommended approach:
1. **Prove it for r coprime to n first** -- this should follow from Erdos-Turan + Vaaler and give O(log n).
2. **Handle gcd(r,n) > 1 separately** -- use the factorization E_r(n) = d * E_{r/d}(n/d) when d = gcd(r,n), reducing to the coprime case.
3. **For the six-term sum** -- investigate whether the specific algebraic structure of six consecutive indices creates additional cancellation beyond what individual bounds give.
4. **For the Mobius-weighted version** -- use Kluyver's formula to express the sum in terms of Ramanujan sums and exploit |c_n(m)| <= gcd(m,n).

---

## 9. Novel Aspects of Our Setting

The following features of our problem appear to be *absent* from the existing literature:

1. **Six consecutive indices:** Summing E_{m+t} for t=0,...,5 with the specific window (n/3, n/2] is not studied anywhere.

2. **Window (n/3, n/2]:** This specific choice of window has number-theoretic significance (it is where the Farey mediant condition applies) but is not standard in the Dedekind sum literature.

3. **Combined Mobius + window + consecutive index structure:** The full expression Sum_{d|n} mu(d) * d * Sum_{t=0}^5 Sum_{n/(3d) < v <= n/(2d)} ((m+t)v/(n/d)) has no analog in the literature.

4. **Connection to Farey discrepancy:** The E_r(n) sums arise from per-step Farey discrepancy analysis, which is itself novel (see INSIGHTS.md, N1-N3).

This suggests that proving the six-term cancellation bound will require a new argument, likely combining:
- Vaaler/Erdos-Turan for the exponential sum bounds
- Ramanujan sum identities for the Mobius structure
- Some new algebraic identity for the six-term consecutive sum
