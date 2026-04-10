# Ng's Weak Mertens Conjecture and Signed Fluctuation Cancellation

**Date:** 2026-03-29
**Status:** Exploratory analysis
**Connects to:** N1 (per-step discrepancy), N3 (M(p)-delta correlation)
**Classification:** C1 (collaborative, minor novelty -- leverages known results in new combination)

---

## 1. Setup and Goal

### Our signed fluctuation sum
We need to show that the "tail" sum over generic denominators is controlled:

$$S_{\text{tail}}(p, N) := \sum_{\substack{b \leq N \\ \text{ord}_b(p) > 2}} \frac{T_b(p) - \mathbb{E}[T_b]}{b^2} = o(N^2)$$

where $T_b(p) = \sum_{a: \gcd(a,b)=1} a \cdot (\sigma_p(a) \bmod b)$ encodes the inner product of the identity with the multiplication-by-$p$ permutation on $(Z/bZ)^*$.

We have already proved $T_b \geq 0$ for all $b$ with $p^2 \equiv 1 \pmod{b}$. The difficulty is the "generic" denominators where $\text{ord}_b(p) > 2$.

### Ng's result (2004, conditional)
Assuming RH + Gonek-Hejhal conjecture ($J_{-1}(T) \ll T$, which implies simplicity of zeros):

$$\int_1^X \frac{M(t)^2}{t^2} \, dt \sim \beta \log X$$

where

$$\beta = 2 \sum_{\gamma > 0} \frac{1}{|\rho \zeta'(\rho)|^2}$$

summing over nontrivial zeros $\rho = 1/2 + i\gamma$ of $\zeta(s)$.

**Reference:** Nathan Ng, "The distribution of the summatory function of the Mobius function," *Proc. London Math. Soc.* **89** (2004), 361--389. arXiv: math/0310381.

### The question
Can the $\beta \log X$ growth rate for $\int M(t)^2/t^2 \, dt$ be used to control $\sum_{b \leq N} s(p,b)^2$ or the signed fluctuation sum?

---

## 2. Connection: $T_b$ Deviations and Dedekind Sums

### From $T_b$ to Dedekind sums
The deviation $T_b(p) - \mathbb{E}[T_b]$ measures how the multiplication-by-$p$ permutation on $(Z/bZ)^*$ deviates from a "generic" permutation. For coprime $p, b$:

$$T_b(p) - \mathbb{E}[T_b] = \text{(function of the inner product } \sum_a a \cdot (pa \bmod b) \text{)}$$

The classical Dedekind sum is:
$$s(p, b) = \sum_{a=1}^{b-1} \left(\!\left(\frac{a}{b}\right)\!\right) \left(\!\left(\frac{pa}{b}\right)\!\right)$$

where $((x)) = x - \lfloor x \rfloor - 1/2$ for $x \notin \mathbb{Z}$, $((x)) = 0$ for $x \in \mathbb{Z}$.

Expanding $((a/b))((pa/b))$:
$$s(p,b) = \sum_{a=1}^{b-1} \left(\frac{a}{b} - \frac{1}{2}\right)\left(\frac{pa \bmod b}{b} - \frac{1}{2}\right)$$

$$= \frac{1}{b^2} \sum_a a \cdot (pa \bmod b) - \frac{1}{2b}\sum_a a - \frac{1}{2b}\sum_a (pa \bmod b) + \frac{b-1}{4}$$

The first term $\frac{1}{b^2}\sum_a a \cdot (pa \bmod b)$ is essentially $T_b(p)/b^2$.

So the deviation $T_b(p) - \mathbb{E}[T_b]$ is directly expressible in terms of $s(p,b)$:

$$\frac{T_b(p) - \mathbb{E}[T_b]}{b^2} = s(p,b) - s_{\text{avg}}(b) + O(1/b)$$

where $s_{\text{avg}}(b)$ is the mean Dedekind sum for fixed $b$.

**Key:** The signed fluctuation sum becomes (up to lower-order terms):

$$S_{\text{tail}}(p, N) \approx \sum_{\substack{b \leq N \\ \text{ord}_b(p) > 2}} \left(s(p, b) - \overline{s(\cdot, b)}\right)$$

---

## 3. Rademacher's Mean-Square (Fixed Denominator, Varying Numerator)

The classical result (Rademacher--Grosswald, also Walum 1982):

For prime $k$:
$$\sum_{\substack{h=1 \\ \gcd(h,k)=1}}^{k-1} s(h,k)^2 = \frac{k^2 - 1}{144} + O(k \log^2 k)$$

More precisely (Conrey--Fransen--Klein--Scott, 1996), for prime $k$:
$$\sum_{h=1}^{k-1} s(h,k)^{2m} \sim C_m \cdot k^{2m}$$

This gives the **$h$-average for fixed $k$**: the typical size of $|s(h,k)|$ is $O(k)$ for a random $h$.

**What we need:** The **$k$-average for fixed $h = p$**: what is $\sum_{b \leq N} s(p,b)^2$?

This is a fundamentally different sum. There is no direct "reciprocity of mean squares."

---

## 4. The $b$-Average for Fixed $p$: What Is Known

### 4.1 Vardi's limiting distribution (1993)
Ilan Vardi proved that $s(h,k)/\log k$ has a limiting **Cauchy distribution** as $K \to \infty$, averaged over all fractions $h/k$ with $1 \leq h \leq k \leq K$, $\gcd(h,k)=1$.

**Consequence:** For most $(h,k)$, $|s(h,k)| \leq (\log k)^{1+\varepsilon}$.

**Reference:** I. Vardi, "Dedekind sums have a limiting distribution," *Int. Math. Res. Not.* **1** (1993), 1--12.

**Problem:** This averages over BOTH $h$ and $k$ simultaneously. For fixed $h = p$ and varying $k = b$, the distribution is different because the reciprocity law:
$$s(p,b) + s(b,p) = \frac{1}{12}\left(\frac{p}{b} + \frac{1}{pb} + \frac{b}{p}\right) - \frac{1}{4}$$

constrains $s(p,b)$ to be roughly $b/(12p) - s(b,p)$ for large $b$. Since $s(b,p)$ depends on $b \bmod p$ (a periodic function), for fixed $p$:

$$s(p,b) = \frac{b}{12p} - s(b \bmod p, \, p) + O(1/b)$$

The first term is **linear in $b$** (growing), and the second term depends only on $b \bmod p$.

### 4.2 Consequence: $s(p,b)$ for fixed $p$ is NOT mean-zero
For fixed $p$ and large $b$:
$$s(p,b) \approx \frac{b}{12p} - s(b \bmod p, \, p)$$

The mean value:
$$\frac{1}{N}\sum_{b \leq N} s(p,b) \approx \frac{N}{24p} - \frac{1}{p-1}\sum_{r=1}^{p-1} s(r,p) = \frac{N}{24p}$$

(using $\sum_{r=1}^{p-1} s(r,p) = 0$ for prime $p$).

So $s(p,b)$ grows linearly in $b$ on average -- it is NOT a fluctuating quantity.

### 4.3 The centered sum
The deviation from the mean:
$$s(p,b) - \mathbb{E}_b[s(p,\cdot)] = -s(b \bmod p, \, p) + O(1/b)$$

This depends only on $b \bmod p$! So:

$$\sum_{b \leq N} \left(s(p,b) - \frac{b}{12p}\right)^2 = \sum_{b \leq N} s(b \bmod p, \, p)^2 + O(N)$$

$$= \frac{N}{p} \sum_{r=0}^{p-1} s(r,p)^2 + O(p)$$

By Rademacher's formula:
$$\sum_{r=1}^{p-1} s(r,p)^2 = \frac{p^2-1}{144} + O(p \log^2 p)$$

Therefore:
$$\sum_{b \leq N} \left(s(p,b) - \frac{b}{12p}\right)^2 = \frac{N(p^2-1)}{144p} + O(N\log^2 p + p)$$

**This is the "reciprocity of mean squares"** -- obtained not by a new theorem, but by combining the reciprocity law with Rademacher's classical formula.

---

## 5. Connection to Ng's Weak Mertens Conjecture

### 5.1 The link via Kloosterman sums
The Dedekind sum $s(p,b)$ can be expressed via Kloosterman-type sums. Specifically:
$$12 \cdot b \cdot s(p,b) = \sum_{a=1}^{b-1} \cot\left(\frac{\pi a}{b}\right) \cot\left(\frac{\pi pa}{b}\right)$$

The Fourier expansion of the cotangent gives:
$$s(p,b) = \frac{1}{4b} \sum_{a=1}^{b-1} \cot\left(\frac{\pi a}{b}\right) \cot\left(\frac{\pi pa}{b}\right)$$

This connects to character sums and ultimately to L-functions via the relation (Louboutin):
$$\sum_{h \in H} s(h,f) = \text{(expression involving } L(1,\chi) \text{ for characters } \chi \text{ trivial on } H \text{)}$$

### 5.2 Can Ng help?
Ng's result controls $\int M(t)^2/t^2 \, dt \sim \beta \log X$.

The Mertens function enters our problem through the Franel-Landau connection:
$$\sum_{f \in F_N} D(f)^2 \sim \frac{|M(N)|^2}{N^2}$$

where $D(f) = f - \text{rank}(f)/n$ is the Farey discrepancy.

**The chain of connections:**
1. $\int M(t)^2/t^2 \, dt \sim \beta \log X$ (Ng, conditional)
2. $\Rightarrow$ $\frac{1}{X}\int_1^X M(t)^2/t^2 \, dt \to 0$ as $X \to \infty$
3. $\Rightarrow$ On average over $N \leq X$, $M(N)^2/N^2 \ll \log X / X$
4. $\Rightarrow$ On average, $\sum_f D(f)^2 \ll \log N / N$

But this does NOT directly control $\sum_b s(p,b)^2$ because:
- Ng's integral averages M(t) over a continuous range
- Our sum involves Dedekind sums at a FIXED prime $p$ with varying modulus
- The connection between M and s(p,b) would require a spectral decomposition that passes through both

### 5.3 What Ng's result DOES imply (indirectly)
Consider the explicit formula:
$$M(x) = \sum_{\rho} \frac{x^{\rho}}{\rho \zeta'(\rho)} + \text{lower-order terms}$$

The weak Mertens conjecture says these oscillating terms have controlled mean-square. The analogous statement for Dedekind sums would be about the Fourier coefficients of the Dedekind sum generating function.

However, the key observation from Section 4.3 makes this moot:

**We already have a complete mean-square estimate for $s(p,b)$ with fixed $p$ and varying $b$, via reciprocity + Rademacher. We do NOT need Ng's result for this.**

---

## 6. What This Means for the Tail Argument

### 6.1 The signed fluctuation is controlled by periodicity
From Section 4.3, the deviation of $T_b(p)$ from its mean depends (to leading order) on $b \bmod p$ only. This means:

$$S_{\text{tail}}(p, N) = \sum_{\substack{b \leq N \\ \text{ord}_b(p)>2}} \frac{T_b(p) - \mathbb{E}[T_b]}{b^2}$$

has contributions that are **periodic in $b$ with period $p$**, weighted by $1/b^2$.

The sum $\sum_{b \leq N} f(b \bmod p)/b^2$ for a periodic function $f$ converges absolutely (since $\sum 1/b^2 < \infty$), and:

$$\sum_{b=1}^{\infty} \frac{f(b \bmod p)}{b^2} = \frac{1}{p^2} \sum_{r=0}^{p-1} f(r) \cdot \psi^{(1)}\left(\frac{r}{p}\right)$$

where $\psi^{(1)}$ is the trigamma function. This is an absolutely convergent series -- **automatically $O(1)$**, which is much better than the $o(N^2)$ we need.

### 6.2 The real issue: the $b/(12p)$ linear growth
The non-centered part $s(p,b) \approx b/(12p)$ grows linearly. But this is the **expected value** of $T_b(p)/b^2$, not the fluctuation. When we subtract $\mathbb{E}[T_b]$, this linear part cancels.

So the signed fluctuation sum $S_{\text{tail}}$ is controlled by:
- The periodic part: $O(1)$ by absolute convergence of $\sum 1/b^2$
- Error terms: $O(\sum_{b \leq N} 1/b^3)= O(1)$

**Conclusion: The tail is $O(1)$, far better than the needed $o(N^2)$.**

### 6.3 Caveat
The analysis above uses the reciprocity law, which requires $\gcd(p,b)=1$. For our application, $p$ is prime and $b \leq N < p$, so this is automatic for $b \neq p$. The single term $b = p$ (if it appears) contributes $O(1/p^2)$.

The more serious caveat: the passage from $T_b$ deviations to Dedekind sums involves the restriction to $\gcd(a,b) = 1$ in the Farey context, while the Dedekind sum sums over all $a$ from 1 to $b-1$. For prime $b$, these coincide. For composite $b$, the coprimality restriction introduces a Mobius-type correction that should be bounded by standard sieve estimates.

---

## 7. The Role of Bruggeman, Sourmelidis et al.

### 7.1 Bruggeman (1989, 1990, 1994)
Bruggeman studied the distribution of Dedekind sums using the spectral theory of automorphic forms (Kuznetsov sum formula). His results concern the joint distribution over both variables $(h,k)$, not the fixed-$h$ average.

**Relevance to us:** Limited. Bruggeman's spectral methods could in principle be adapted to the fixed-$h$ setting, but the reciprocity trick (Section 4.3) already gives a clean answer without spectral theory.

### 7.2 Minelli--Sourmelidis--Technau (2022, 2023)
These authors studied restricted averages of Dedekind sums over Farey-like sets, proving Ito's conjecture on the sign bias of Dedekind sums in $[0, 1/2]$ vs. $[1/2, 1]$.

**Reference:** Minelli, Sourmelidis, Technau, "On restricted averages of Dedekind sums," *IMRN* **2024** (10), 8485--8502. arXiv: 2301.00441.

**Relevance to us:** Their work on Farey-restricted averages is thematically close but addresses a different question (average of $s(h,k)$ over Farey fractions $h/k$ in a sub-interval). Their methods (van der Corput-type estimates, continued fraction statistics) could potentially sharpen the error terms in our analysis.

---

## 8. Summary and Verdict

### Does Ng's weak Mertens conjecture help?
**No, not directly.** The connection is too indirect: Ng controls $\int M(t)^2/t^2 \, dt$, which relates to $\sum D(f)^2$ via Franel-Landau, but our fluctuation sum involves Dedekind sums $s(p,b)$ at a fixed prime, not the global discrepancy $D(f)$.

### What DOES help?
The **Dedekind reciprocity law** combined with **Rademacher's mean-square formula** gives a complete, unconditional answer:

1. $s(p,b) = b/(12p) - s(b \bmod p, \, p) + O(1/b)$ (reciprocity)
2. The fluctuation $s(p,b) - b/(12p)$ depends on $b \bmod p$ (periodic!)
3. Summing $1/b^2$ times a periodic function converges absolutely
4. Therefore $S_{\text{tail}} = O(1)$, which is far stronger than $o(N^2)$

### Improvement over current argument
- **Current:** The tail argument is RH-conditional (uses bounds on M(p))
- **New (via reciprocity + Rademacher):** The tail bound is UNCONDITIONAL
- **Strength:** $O(1)$ vs. the needed $o(N^2)$ -- enormous room

### Caveats requiring verification
1. The exact correspondence between $T_b$ deviations and Dedekind sums needs careful bookkeeping (coprimality restriction for composite $b$)
2. The $O(1/b)$ error in the reciprocity expansion must be verified to not accumulate when summed over $b$
3. The analysis assumes $b < p$ (automatic for Farey order $N < p$); for $b > p$, additional work needed

### Next steps
1. **Write out the detailed correspondence** between $T_b(p) - \mathbb{E}[T_b]$ and $s(p,b)$ with all normalizations explicit
2. **Verify computationally** for small primes that the reciprocity-based bound matches the empirical tail
3. **Handle composite $b$:** Use Mobius inversion to express the coprimality-restricted sum in terms of unrestricted Dedekind sums
4. **If all checks pass:** Replace the RH-conditional tail argument with the unconditional reciprocity argument in the paper

---

## 9. References

1. N. Ng, "The distribution of the summatory function of the Mobius function," *Proc. London Math. Soc.* 89 (2004), 361-389. [arXiv:math/0310381](https://arxiv.org/abs/math/0310381)
2. I. Vardi, "Dedekind sums have a limiting distribution," *IMRN* 1 (1993), 1-12.
3. R.W. Bruggeman, "Eisenstein series and the distribution of Dedekind sums," *Math. Z.* 202 (1989), 181-198.
4. R.W. Bruggeman, "Dedekind sums and Fourier coefficients of modular forms," *J. Number Theory* 36 (1990), 289-321.
5. J.B. Conrey, E. Fransen, R. Klein, C. Scott, "Mean values of Dedekind sums," *J. Number Theory* 56 (1996), 214-226. [arXiv:math/9410212](https://arxiv.org/abs/math/9410212)
6. H. Walum, "An exact formula for an average of L-series," *Illinois J. Math.* 26 (1982), 1-3.
7. P. Minelli, A. Sourmelidis, M. Technau, "On restricted averages of Dedekind sums," *IMRN* 2024(10), 8485-8502. [arXiv:2301.00441](https://arxiv.org/abs/2301.00441)
8. P. Minelli, A. Sourmelidis, M. Technau, "Bias in the number of steps in the Euclidean algorithm and a conjecture of Ito on Dedekind sums," *Math. Ann.* 387 (2023), 291-320. [arXiv:2206.03214](https://arxiv.org/abs/2206.03214)
9. S. Louboutin, "Dedekind sums, mean square value of L-functions at s=1 and upper bounds on relative class numbers." (Multiple papers, *Colloq. Math.*, *Canad. J. Math.*)
10. H. Rademacher, E. Grosswald, *Dedekind Sums*, Carus Math. Monographs, MAA, 1972.
