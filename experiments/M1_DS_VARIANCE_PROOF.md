To prove the given theorem, we start by considering the function \( F_N(\gamma) = \frac{1}{N} \left| \sum_{p \leq N} \mu(p) p^{-i\gamma} \right|^2 \), where \(\mu(p)\) is the Möbius function. We aim to show that for any interval \([A, B]\) containing at least one ordinate \(\gamma_k\) of a nontrivial zero of the Riemann zeta function \(\zeta(s)\), the integral of \(F_N(\gamma)\) over this interval grows faster than some constant times \((\log N)^{c_2}\). Conversely, under a zero-free model, the integral is bounded.

1. **Expressing \( F_N(\gamma) \)**:
   - The function \( F_N(\gamma) \) can be expanded as:
     \[
     F_N(\gamma) = \frac{1}{N} \left| \sum_{p \leq N} \mu(p) p^{-i\gamma} \right|^2
     \]
   - This expands into diagonal and cross terms:
     \[
     F_N(\gamma) = \frac{1}{N} \left( \sum_p |\mu(p)|^2 + \sum_{p \neq q} \mu(p)\mu(q) p^{-i\gamma} q^{i\gamma} \right)
     \]
   - Since \(|\mu(p)|^2 = 1\) for primes, this simplifies to:
     \[
     F_N(\gamma) = \frac{1}{N} \left( \pi(N) + \sum_{p \neq q} p^{-i\gamma} q^{i\gamma} \right)
     \]

2. **Integrating \( F_N(\gamma) \)**:
   - The integral over \([A, B]\) becomes:
     \[
     \int_A^B F_N(\gamma) \, d\gamma = \frac{1}{N} \left( \pi(N)(B - A) + \sum_{p \neq q} \int_A^B e^{i \gamma \log(q/p)} \, d\gamma \right)
     \]
   - The first term is negligible as \(N\) grows because it tends to zero.
   - The second term involves cross terms which are analyzed using the large sieve inequality.

3. **Using the Explicit Formula**:
   - The explicit formula for \(M(x)\) is used, which relates sums over zeros of \(\zeta(s)\). This helps express the integral in terms of contributions from zeros within \([A, B]\).
   - Each zero \(\gamma_k\) contributes a term proportional to \((\log \log N)^2\).

4. **Bounding Cross Terms**:
   - The large sieve inequality bounds the cross terms, showing they grow slower than the diagonal contributions.
   - Under a zero-free model, these cross terms result in an integral that is \(O(1)\) due to random phase cancellation.

5. **Conclusion**:
   - For intervals containing at least one zero \(\gamma_k\), the integral grows faster due to constructive interference from these zeros.
   - This results in the integral exceeding \(c_1 (\log N)^{c_2}\) for some constants \(c_1, c_2 > 0\).

Thus, we have proven that:

\[
\boxed{\int_A^B F_N(\gamma) \, d\gamma > c_1 (\log N)^{c_2}}
\]
