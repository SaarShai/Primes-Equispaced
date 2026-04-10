To determine whether \( S(x) = \sum_{p \leq x} \frac{M(p)^2}{p^2} \) diverges, we start by using partial summation and known results about the Mertens function \( M(p) \).

1. **Partial Summation**: We express \( S(x) \) as an integral involving the prime counting function:
   \[
   S(x) = \int_{2}^{x} \left( \frac{M(t)}{t} \right)^2 d(\pi(t))
   \]
   where \( \pi(t) \) is the prime-counting function.

2. **Prime Number Theorem**: We approximate \( d\pi(t) \sim \frac{dt}{\log t} \), leading to:
   \[
   S(x) \approx \int_{2}^{x} \left( \frac{M(t)}{t} \right)^2 \frac{dt}{\log t}
   \]

3. **Heuristic for \( M(t)^2 \)**: Using the variance heuristic from RH, we consider Var\( (M(x)) \sim \frac{x}{\log x} \). This suggests:
   \[
   \left( \frac{M(t)}{t} \right)^2 \approx \frac{1}{\log t}
   \]
   Thus, the integrand becomes approximately \( \frac{1}{\log t^2} \), leading to a convergent integral.

4. **Unconditional Bounds**: Knowing \( M(x) = O(x^{1/2 + \epsilon}) \) unconditionally, we find:
   \[
   M(p)^2 / p^2 = O(1/p^{1 - 2\epsilon})
   \]
   Summing over primes \( p \leq x \), we note that the series \( \sum_{p} 1/p^{s} \) diverges for \( s \leq 1 \). Hence, without assuming RH, \( S(x) \) diverges.

5. **Conclusion**: Without additional conjectures, the known bounds lead to divergence. Assuming the variance heuristic (related to RH), convergence could be argued, but this is not rigorous under current mathematical knowledge.

Thus, we conclude that:

\[
\boxed{\text{S(x) diverges}}
\]
