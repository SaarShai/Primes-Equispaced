To justify the interchange of summations in the explicit prime sum formula, we analyze the truncation error introduced by restricting the sum over zeros γ to those with |γ| ≤ T. The key steps are as follows:

1. **Understanding R(p,T):**  
   Define \( R(p,T) = M(p) - \left(-1 + \sum_{|\gamma| \leq T} \frac{p^\rho}{\rho \zeta'(\rho)}\right) \). This represents the difference between the Möbius function at prime p and a truncated version of an infinite series over zeros γ.

2. **Bounding R(p,T):**  
   Utilize the standard bound \( |R(x,T)| \leq C \cdot x \cdot (\log^2 x)/T \). For each prime \( p \), this gives:
   \[
   |R(p,T)| \leq C \cdot p \cdot (\log^2 p) / T
   \]

3. **Summing Over Primes:**  
   We consider the sum \( \sum_p |R(p,T)| / p \). Substituting the bound:
   \[
   \sum_p \frac{|R(p,T)|}{p} \leq C \cdot \sum_p \frac{\log^2 p}{T}
   \]
   Since \( \sum_p 1 = \pi(N) \sim N / (\log N) \), and each term involves \( \log^2 p \):
   \[
   \sum_p \frac{\log^2 p}{T} \leq C \cdot \frac{N \log^2 N}{\log N \cdot T} = C \cdot \frac{N \log N}{T}
   \]

4. **Choosing T Appropriately:**  
   Set \( T = N^A \) for some \( A > 1 \). Substituting into the bound:
   \[
   \sum_p \frac{|R(p,T)|}{p} \leq C \cdot \frac{N \log N}{N^A}
   \]
   Simplifying:
   \[
   C \cdot N^{1 - A} \log N
   \]

5. **Asymptotic Behavior:**  
   For \( A > 1 \), \( N^{1 - A} \) decays polynomially to zero as \( N \to \infty \). Thus, the remainder term becomes negligible:
   \[
   C \cdot N^{1 - A} \log N = o\left(\frac{\sqrt{N}}{\log N}\right)
   \]

6. **Conclusion:**  
   By choosing \( T = N^A \) with \( A > 1 \), the truncation error introduced by interchanging the sums is asymptotically insignificant compared to the main term of interest.

Therefore, the interchange \( \sum_{|\gamma| \leq T} \sum_p \leftrightarrow \sum_p \sum_{|\gamma| \leq T} \) in the explicit prime sum formula is justified as \( T \to \infty \), within an error term that vanishes relative to the resonant term. QED.

\boxed{\text{Interchange is justified as } T \to \infty \text{ with truncation error being negligible.}}
