# Literature: Cancellation in Floor-Function Sums over Arithmetic Progressions

**Date:** 2026-03-30
**Context:** Our problem reduces to Sigma_{t=0}^{5} E_{m+t}(n) where E_r(n) involves floor sums floor(rv/n). We need cancellation results for six consecutive terms.

---

## 1. Hermite's Identity (the foundational tool)

**Statement:** For x in R, n in Z+:
```
sum_{k=0}^{n-1} floor(x + k/n) = floor(nx)
```

**With n=6:** The six-term identity becomes:
```
floor(x) + floor(x+1/6) + floor(x+2/6) + floor(x+3/6) + floor(x+4/6) + floor(x+5/6) = floor(6x)
```

**Key mechanism:** Each term floor(x + k/n) takes only the values floor(x) or floor(x)+1. The number of terms that "jump up" is exactly floor(n{x}) where {x} is the fractional part. This is the fundamental cancellation: n floor-function evaluations collapse to a single floor(nx).

**Relevance to our problem:** If we can write our six-term sum Sigma_{t=0}^5 E_{m+t}(n) in the form of Hermite's LHS (with x = rv/n and n=6, or a variant), then the sum collapses to a single floor evaluation plus a bounded error. The question is whether the E_r terms have the right structure.

**Sources:**
- Hermite (1884), original identity
- [Brilliant Wiki](https://brilliant.org/wiki/hermites-identity/)
- [Wikipedia](https://en.wikipedia.org/wiki/Hermite's_identity)
- Graham, Knuth, Patashnik, *Concrete Mathematics* (2nd ed., 1994), Section 3.5

---

## 2. Pongsriiam's Generalization (sums over residue systems)

**Paper:** S. Aursukaree, T. Khemaratchatakumthorn, P. Pongsriiam, "Generalizations of Hermite's Identity and Applications," *Fibonacci Quarterly* 57(2), 126-133 (2019).

**Key results:**
- **Theorem (partial sums):** Considers sum_{k=a}^{b} floor(x + k/n) for integers a < b. Gives explicit formula.
- **Theorem 3.6 (complete residue system):** When k ranges over a COMPLETE residue system mod n (i.e., {ka mod n : k=0,...,n-1} for gcd(a,n)=1), the sum equals floor(nx). This is because permuting residues doesn't change the Hermite sum.
- **Application to Tverberg's result:** Provides alternative proof of bounds on Jacobsthal-type floor sums.

**Relevance:** If our six-term E_{m+t} sum can be reindexed as k ranging over a complete residue system mod 6, Pongsriiam's theorem applies directly. The consecutive indices m, m+1, ..., m+5 DO form a complete residue system mod 6, so this is promising.

**Source:** [Full PDF](https://www.fq.math.ca/Papers/57-2/pongsriiam02072019.pdf)

---

## 3. Dedekind Sums and Reciprocity

**Definition:** For coprime integers p, q:
```
s(p,q) = sum_{i=1}^{q} ((i/q))((pi/q))
```
where ((x)) = x - floor(x) - 1/2 for non-integer x, and 0 for integer x (the sawtooth function).

**Key properties:**
- **Periodicity:** s(a,b) is periodic in a with period b. If h1 = h2 mod k, then s(h1,k) = s(h2,k).
- **Antisymmetry:** s(-h,k) = -s(h,k).
- **Dedekind reciprocity:** For coprime b,c > 0: s(b,c) + s(c,b) = (b/c + 1/(bc) + c/b)/12 - 1/4.
- **Mod reduction:** Dedekind sums depend only on a mod b.

**Connection to floor sums:** Since ((x)) = {x} - 1/2 (for non-integers), Dedekind sums are built from fractional parts, and floor(x) = x - {x}. Every sum of floor(rv/n) can be rewritten in terms of Dedekind-type sums plus explicit main terms.

**Block cancellation in Dedekind sums:** Newform Dedekind sums exhibit square-root cancellation on average. For our mod 6 block sum, the periodicity s(a,b) = s(a + kb, b) means that summing over six consecutive values of the first argument may produce cancellation if those six values span a structured set of residues.

**Sources:**
- [Wikipedia: Dedekind sum](https://en.wikipedia.org/wiki/Dedekind_sum)
- [Wolfram MathWorld](https://mathworld.wolfram.com/DedekindSum.html)
- Zagier, "Higher dimensional Dedekind sums," *Math. Ann.* 202, 149-172 (1973). [PDF](https://people.mpim-bonn.mpg.de/zagier/files/doi/10.1007/BF01351173/HigherDedekindSums.pdf)
- Rademacher & Grosswald, *Dedekind Sums* (Carus Math. Monographs, 1972)

---

## 4. Zagier's Reciprocity and Higher-Dimensional Sums

**Zagier (1973):** Defined higher-dimensional Dedekind sums d(p; a1, ..., an) and proved:
- d depends only on a_i mod p
- Symmetric in arguments
- d(p; -a1, ..., an) = -d(p; a1, ..., an)
- Reciprocity law generalizing Dedekind and Rademacher

**Hall-Wilson-Zagier:** For each integer N >= 0, there is a reciprocity law for Dedekind-Rademacher sums. When one parameter equals 1, only two of three terms are nontrivial.

**Relevance:** Our six-term sum may be expressible as a higher-dimensional Dedekind sum with specific parameters. Zagier's reciprocity could then give the cancellation we need.

**Source:** [Zagier PDF](https://people.mpim-bonn.mpg.de/zagier/files/doi/10.1007/BF01351173/HigherDedekindSums.pdf)

---

## 5. Beck & Robins: Lattice Point Enumeration

**Book:** Matthias Beck & Sinai Robins, *Computing the Continuous Discretely: Integer-Point Enumeration in Polyhedra* (Springer, 2nd ed. 2015).

**Key content:**
- Dedekind sums computed via Euclidean-algorithm-style reciprocity in O(log b) steps
- Floor sums arise naturally as lattice-point counts in polytopes
- Ehrhart theory connects floor-function sums to polynomial expressions
- Chapter on Dedekind sums with explicit reciprocity formulas

**Relevance:** Our floor sum sum_v floor(rv/n) counts lattice points in a triangle with slope r/n. Summing over r = m, m+1, ..., m+5 counts lattice points in six such triangles. Beck-Robins framework may give the right language for proving cancellation.

**Source:** [Author's website](https://matthbeck.github.io/ccd.html), [Springer](https://link.springer.com/book/10.1007/978-1-4939-2969-6)

---

## 6. Carlitz and Jacobsthal-type Sums

**Carlitz (1960):** "Some arithmetic sums connected with the greatest integer function," studied sums of the form sum_{k} floor(f(k)) for various arithmetic functions f.

**Jacobsthal sums:** Sums of floor functions of the form sum_{k=1}^{n-1} floor(mk/n), studied by Jacobsthal, then Carlitz, Grimson, and Tverberg. These are closely related to Dedekind sums.

**Tverberg's bounds:** Sharp upper and lower bounds for Jacobsthal-type floor sums, proved by Onphaeng-Pongsriiam (2017).

**Relevance:** The individual E_r(n) terms in our sum are essentially Jacobsthal sums. The question is whether summing six consecutive ones (r, r+1, ..., r+5) produces additional cancellation beyond what each term exhibits individually.

**Sources:**
- L. Carlitz, *Archiv der Mathematik* (1960)
- Tverberg's conjecture, proved in Onphaeng-Pongsriiam (2017)

---

## 7. Weyl Sums and Equidistribution

**Weyl's criterion:** The sequence {n*alpha} is equidistributed mod 1 iff for all nonzero integers h, (1/N) sum_{n=1}^N e(hn*alpha) -> 0.

**Quantitative form (Erdos-Turan):** Gives explicit bounds on discrepancy in terms of exponential sums.

**For rational alpha = r/n:** The fractional parts {rv/n} for v=1,...,n-1 are NOT equidistributed in the Weyl sense (they hit only n-1 distinct values), but they ARE uniformly distributed over those values. The exponential sum is sum_{v=1}^{n-1} e(hrv/n), which vanishes unless n | hr.

**Relevance:** When we sum E_r(n) = sum_v (rv/n - floor(rv/n) - 1/2)-type terms, the cancellation is governed by exponential sums. For six consecutive r values, the relevant exponential sum is sum_{t=0}^5 sum_v e(h(m+t)v/n). The inner sum over t gives geometric-series cancellation: sum_{t=0}^5 e(htv/n) = e(6hv/n)-1)/(e(hv/n)-1) when hv is not divisible by n.

**This is the most promising approach:** The six-term block sum introduces a factor of (e(6hv/n)-1)/(e(hv/n)-1) into the Fourier analysis, which has known cancellation properties.

**Sources:**
- [Wikipedia: Equidistribution](https://en.wikipedia.org/wiki/Equidistributed_sequence)
- [Tao's blog on equidistribution](https://terrytao.wordpress.com/tag/weyls-equidistribution-theorem/)
- [Elkies, Harvard notes](https://people.math.harvard.edu/~elkies/M259.02/weyl.pdf)

---

## 8. Merca: Periodic Sequences and Floor-Sum Identities

**Paper:** Mircea Merca, "Inequalities and Identities Involving Sums of Integer Functions," *Journal of Integer Sequences* 14 (2011), Article 11.9.5.

**Key method:** Given a sequence {a_n} that is periodic mod m, derives identities and inequalities for sums involving floor(a_n * k/m), ceil(a_n * k/m). The periodicity allows the sum to be decomposed into complete blocks plus a remainder.

**Relevance:** If our E_r(n) has periodic structure in r (period dividing 6), Merca's framework directly applies. The six-term block would then be a "complete period" and the sum would simplify.

**Source:** [Full PDF](https://cs.uwaterloo.ca/journals/JIS/VOL14/Merca/merca3.pdf)

---

## 9. Bordelles-Dai-Heyman-Pan-Shparlinski Framework

**Key result (2019+):** For S_f(x) = sum_{n <= x} f(floor(x/n)):
- When f is "small" (f(n) << n^epsilon), the error is O(x^{1/2+epsilon})
- Wu (2020) improved to O(x^{1/3} log x) for many cases
- Stucky (2022) generalized further

**Relevance:** Our floor sums sum_v floor(rv/n) are exactly of this type with f related to the indicator function. The Bordelles et al. framework gives asymptotic expansions. Summing six such terms may improve the error if there is additional cancellation from the arithmetic progression structure.

**Sources:**
- Bordelles, Dai, Heyman, Pan, Shparlinski, *J. Number Theory* 202, 278-297 (2019)
- Wu, *Period. Math. Hungar.* 80(1), 95-102 (2020)

---

## 10. Grinberg: Floor Functions and Arithmetic Functions

**Notes:** Darij Grinberg, "Floor and Arithmetic Functions," MIT 18.781 lecture notes (2016).

**Content:** Comprehensive treatment of floor function properties, GCD connections, arithmetic functions (phi, Mobius, divisor sums), Dirichlet convolution, and multiplicativity. Provides useful toolkit for manipulating floor sums.

**Source:** [PDF](https://www.cip.ifi.lmu.de/~grinberg/floor.pdf)

---

## 11. Lemke Oliver-Soundararajan: Distribution of Sawtooth Sums

**Paper:** Studies the discrete Fourier transform of the Dedekind sum s_q(a) over residue classes.

**Key insight:** The Fourier transform s-hat_q(t) = (1/q) sum_{a mod q} s_q(a) e(at/q) reveals how Dedekind sums distribute across residue classes. This is directly relevant to understanding how our sum over six consecutive r-values behaves.

**Source:** [PDF](https://rlemke01.math.tufts.edu/papers/18-DistributionSawtooth.pdf)

---

## Assessment: Most Promising Approaches for Our Problem

### Direct application of Hermite (n=6):
If E_r(n) = sum_{v} floor((r+t/6)*v/n) for some parametrization, then summing t=0,...,5 gives floor(6*something) by Hermite. **Check if this parametrization is valid.**

### Fourier/Weyl approach (Section 7):
Write E_r(n) in terms of exponential sums. The six-term sum introduces the geometric factor sum_{t=0}^5 e(tv*h/n). This factor equals 6 when 6|hv/n and exhibits cancellation otherwise. **This is the cleanest path to proving O(small error).**

### Dedekind sum decomposition (Section 3):
Write each E_r(n) as a Dedekind sum s(r,n) plus explicit terms. Sum six consecutive ones. Use periodicity s(r,n) = s(r mod n, n) and reciprocity. **Works if the Dedekind-sum remainder after summing six terms is smaller than individual terms.**

### Beck-Robins lattice-point view (Section 5):
Count lattice points in six triangles with slopes r/n, (r+1)/n, ..., (r+5)/n. The union or alternating sum of these triangles may have a simpler lattice-point count. **More geometric, possibly gives intuition.**

### Priority ranking:
1. **Fourier/Weyl** -- most likely to give quantitative bounds
2. **Hermite direct** -- cleanest if the parametrization works
3. **Dedekind reciprocity** -- good for exact identities
4. **Lattice-point geometry** -- good for intuition and visualization
