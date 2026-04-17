**1. Asymptotic for W(N) under RH:**
Under the Riemann Hypothesis, the Farey discrepancy \( W(N) \) is known to satisfy \( W(N) = O(N^{-1 + \epsilon}) \) for any \( \epsilon > 0 \). However, more precise analysis suggests that \( W(N) \) tends to zero as \( N \to \infty \). This is because the discrepancy function \( D(f) \) is bounded by terms like \( O((\log N)/\sqrt{N}) \), leading to squared discrepancies summed over all Farey fractions resulting in a sum that grows slower than any positive power of \( N \). Therefore, the leading term of \( W(N) \) tends to zero.

**2. Bounding A from above:**
Given \( A \approx W(p-1) \cdot \frac{2p - 1}{n^2} \cdot n' \), using the bound \( W(p-1) = O(\log^2 p / p^3) \), we find that \( A \) is bounded above by \( O\left( \frac{\log^2 p}{p^2 n^2} \right) \). This assumes \( n' \) is on the order of \( n \).

**3. Lower bound on Sum delta(f)^2:**
Under RH, establishing a non-trivial lower bound on \( \sum \delta(f)^2 \) is challenging. While each term \( \delta(f)^2 \) contributes non-negatively, without specific control over their distribution or density, it's unclear if such a sum has a guaranteed positive growth rate.

**4. Behavior of C/A:**
Given \( C = \frac{1}{n'^2} \sum \delta(f)^2 \) and the upper bound on \( A \), whether \( C/A \) tends to infinity depends on the asymptotic behavior of both terms. If \( C \) does not decay as fast as \( A \), their ratio could tend to infinity. However, without precise asymptotics for both, this remains speculative.

**5. Additional assumption:**
To ensure \( C/A \to \infty \), an additional assumption might involve a lower bound on \( \sum \delta(f)^2 \) that grows faster than the corresponding upper bound on \( A \).

**6. Explicit asymptotic for DiscrepancyStep lemma:**
Under RH, discrepancy terms often benefit from improved error bounds with exponents like \( O(N^{-1/2 + \epsilon}) \). Thus, the DiscrepancyStep lemma likely has an asymptotic involving such an exponent.

**Final Answers:**

1. The leading term of \( W(N) \) tends to zero under RH.
2. \( A = O\left( \frac{\log^2 p}{p^2 n^2} \right) \).
3. No non-trivial lower bound on \( \sum \delta(f)^2 \) is established with RH alone.
4. Whether \( C/A \to \infty \) is uncertain without precise asymptotics.
5. An additional assumption on discrepancy growth could ensure \( C/A \to \infty \).
6. The DiscrepancyStep lemma under RH has an improved exponent.

\boxed{W(N) = O(N^{-1 + \epsilon}) \text{ and tends to zero; other conclusions as above}}
