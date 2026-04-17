Under the Generalized Riemann Hypothesis (GRH), the sum \( S_K = \sum_{p \leq K} p^{-\rho_1} \) with \( \rho_1 = 0.5 + 14.1347i \) is analyzed using partial summation and approximations from analytic number theory.

**Step-by-Step Analysis:**

1. **Partial Summation Application:**
   - Express \( S_K \) as:
     \[
     S_K = \pi(K) K^{-\rho_1} + \rho_1 \int_{2}^{K} \pi(t) t^{-\rho_1 - 1} dt
     \]
   - Using the prime number theorem, approximate \( \pi(t) \approx \text{Li}(t) = \frac{t}{\log t} + o\left(\frac{t}{\log t}\right) \).

2. **Leading Term Evaluation:**
   - The leading term becomes:
     \[
     \pi(K) K^{-\rho_1} \approx \frac{K}{\log K} \cdot K^{-0.5 - i\tau} = \frac{\sqrt{K}}{\log K} e^{-i\tau \log K}
     \]
   - The magnitude is approximately \( \frac{\sqrt{K}}{\log K} \).

3. **Integral Term Approximation:**
   - The integral term:
     \[
     \int_{2}^{K} \frac{t}{\log t} \cdot t^{-1.5 - i\tau} dt
     \]
     transforms to an exponential integral which is negligible compared to the leading term for large \( K \).

4. **Asymptotic Behavior of |S_K|:**
   - The dominant term gives:
     \[
     |S_K| \approx \frac{\sqrt{K}}{\log K}
     \]
   - Therefore, the ratio \( A = \frac{|S_K|}{\sqrt{K / \log K}} \) simplifies to:
     \[
     A \approx \frac{\sqrt{K} / \log K}{\sqrt{K / \log K}} = \frac{1}{\sqrt{\log K}}
     \]
   - As \( K \to \infty \), \( A \to 0 \).

5. **Conclusion:**
   - The ratio decreases to zero, supporting the random walk model prediction (GUE).
   - The discrepancy in Result 2 is likely due to incorrect assumptions or numerical inaccuracies.

**Final Answer:**

Under GRH, \( |S_K| \) grows asymptotically as \( O\left(\frac{\sqrt{K}}{\log K}\right) \), making the ratio \( A \) tend to zero. This confirms the random walk prediction and contradicts Result 2's stabilization claim.

**Answer:**

Under GRH, the correct asymptotic for \( |S_K| \) is \( O\left(\frac{\sqrt{K}}{\log K}\right) \), leading to the ratio \( A = \frac{|S_K|}{\sqrt{K / \log K}} \) tending to zero as \( K \to \infty \). Thus, Result 1 is correct.

$\boxed{|S_K| = O\left(\dfrac{\sqrt{K}}{\log K}\right)}$
