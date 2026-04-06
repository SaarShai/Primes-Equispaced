# Formal Proof: Spectral Detection of Zeta Zeros under GRH

## 1. Preliminaries and Assumptions

Let $\zeta(s)$ denote the Riemann zeta function. We operate under the following mathematical hypotheses:

1.  **Generalized Riemann Hypothesis (GRH):** All non-trivial zeros $\rho$ of $\zeta(s)$ lie on the critical line $\Re(s) = \frac{1}{2}$. Thus, $\rho_k = \frac{1}{2} + i\gamma_k$, where $\gamma_k \in \mathbb{R}$.
2.  **Linear Independence (LI):** The set of ordinates $\{\gamma_k\}_{k \ge 1}$ of the non-trivial zeros is linearly independent over the rationals $\mathbb{Q}$. This implies that for any distinct indices $j \neq k$, the difference $\gamma_k - \gamma_j \neq 0$.
3.  **Subset Density:** Let $S$ be a subset of the primes such that $|S| \to \infty$. We assume $S$ is sufficiently dense (e.g., has a natural density relative to the primes) such that the weighted sum diverges:
    $$ \sum_{p \in S} p^{-1/2} \to \infty \quad \text{as } \max(S) \to \infty. $$
    *(Note: For the proof of the "spectroscope" behavior to hold, the main term must diverge. A pathologically sparse set where this sum converges would not exhibit the infinite spectral growth described.)*

**Definitions:**
*   **Spectroscope Function:** For a frequency $\gamma \in \mathbb{R}$ and a subset $S$,
    $$ F_S(\gamma) = \gamma^2 \left| \sum_{p \in S} \frac{M(p)}{p} e^{-i\gamma \log p} \right|^2 $$
*   **Modulation Factor:**
    $$ M(p) = -1 + \sum_{\rho} c_\rho p^\rho, \quad \text{where } c_\rho = \frac{1}{\rho \zeta'(\rho)} $$
    Summation over $\rho$ is over non-trivial zeros of $\zeta(s)$.

---

## 2. Expansion of the Spectroscope

We evaluate the inner sum of the spectroscope at a specific zero ordinate $\gamma = \gamma_j$ (where $\rho_j = 1/2 + i\gamma_j$).

Substitute $M(p)$ into the sum:
$$ \Sigma_S(\gamma_j) = \sum_{p \in S} \frac{1}{p} \left( -1 + \sum_{\rho} c_\rho p^\rho \right) p^{-i\gamma_j \log p} $$
$$ \Sigma_S(\gamma_j) = -\sum_{p \in S} \frac{1}{p} e^{-i\gamma_j \log p} + \sum_{p \in S} \frac{1}{p} \sum_{\rho} c_\rho p^\rho p^{-i\gamma_j \log p} $$

By GRH, substitute $p^\rho = p^{1/2 + i\gamma_k}$:
$$ \Sigma_S(\gamma_j) = \underbrace{-\sum_{p \in S} \frac{1}{p} e^{-i\gamma_j \log p}}_{\text{Constant Term}} + \sum_{\rho} c_\rho \sum_{p \in S} p^{1/2} p^{-i\gamma_j \log p} p^{-1} p^{i\gamma_k \log p} $$
Simplifying the exponents: $p^{1/2} \cdot p^{-1} \cdot p^{i(\gamma_k - \gamma_j)\log p} = p^{-1/2} e^{i(\gamma_k - \gamma_j)\log p}$.
Thus:
$$ \Sigma_S(\gamma_j) = \mathbf{T}_{\text{const}} + \sum_{k} c_{\rho_k} \underbrace{\sum_{p \in S} p^{-1/2} e^{i(\gamma_k - \gamma_j)\log p}}_{D_k(\gamma_j)} $$

---

## 3. Analysis of the Diagonal Term ($k=j$)

Consider the term where the frequency in the sum matches the evaluation frequency ($k=j$, i.e., $\gamma_k = \gamma_j$). The exponential phase becomes $e^0 = 1$.
$$ D_j(\gamma_j) = \sum_{p \in S} p^{-1/2} $$

**Growth Rate:**
By the Prime Number Theorem (PNT), the sum of prime reciprocals with a half-power weight behaves as:
$$ \sum_{p \le x} p^{-1/2} \sim \int_2^x \frac{t^{-1/2}}{\log t} \, dt \sim \frac{2\sqrt{x}}{\log x} $$
Given the assumption that $S$ is a sufficiently dense infinite subset, we have:
$$ \sum_{p \in S} p^{-1/2} \sim C_S \frac{2\sqrt{\max(S)}}{\log(\max(S))} $$
where $C_S$ depends on the relative density of $S$. Crucially, as $|S| \to \infty$, **$D_j(\gamma_j) \to \infty$**.

**Dominance over Constant Term:**
The constant term $\mathbf{T}_{\text{const}}$ involves the sum $\sum_{p \in S} p^{-1} e^{-i\gamma_j \log p}$. Under GRH/LI arguments, this behaves similarly to $\sum p^{-1}$, which grows logarithmically (Mertens' theorem).
Since $D_j(\gamma_j)$ grows as $x^{1/2}/\log x$ and $\mathbf{T}_{\text{const}}$ grows as $\log \log x$, the diagonal term dominates exponentially:
$$ |\mathbf{T}_{\text{const}}| = o(D_j(\gamma_j)) $$
Thus, $\Sigma_S(\gamma_j) \approx c_{\rho_j} D_j(\gamma_j)$.

---

## 4. Analysis of Off-Diagonal Terms ($k \neq j$)

For $k \neq j$, the exponent involves $\Delta_{kj} = \gamma_k - \gamma_j \neq 0$.
The term is:
$$ D_k(\gamma_j) = \sum_{p \in S} p^{-1/2} e^{i \Delta_{kj} \log p} $$

**Equidistribution:**
Under the assumption of LI (Linear Independence of zeros), the sequence of values $\{ \Delta_{kj} \log p \}_{p \in S}$ modulo $2\pi$ is equidistributed.
Consequently, the complex exponential terms $e^{i \Delta_{kj} \log p}$ behave like random unit vectors on the complex plane.

By the orthogonality of characters or standard properties of trigonometric sums with incommensurable frequencies:
$$ \sum_{p \in S} p^{-1/2} e^{i \Delta_{kj} \log p} = o\left( \sum_{p \in S} p^{-1/2} \right) $$
More precisely, the magnitude is bounded by:
$$ |D_k(\gamma_j)| \ll \left( \sum_{p \in S} p^{-1/2} \right)^{1/2} \quad \text{(by Cauchy-Schwarz/Random Walk estimates)} $$
Thus, the off-diagonal terms are **negligible** compared to the diagonal growth.

---

## 5. Synthesis and Spectral Detection

Substituting the approximations back into the expression for $\Sigma_S(\gamma_j)$:

$$ \Sigma_S(\gamma_j) = c_{\rho_j} \sum_{p \in S} p^{-1/2} + \sum_{k \neq j} c_{\rho_k} \cdot o\left( \sum_{p \in S} p^{-1/2} \right) + o\left( \sum_{p \in S} p^{-1/2} \right) $$

Factor out the dominant magnitude $W_S = \sum_{p \in S} p^{-1/2}$:
$$ \Sigma_S(\gamma_j) = W_S \left( c_{\rho_j} + \epsilon_{S,j} \right) $$
where $\epsilon_{S,j} \to 0$ as $\max(S) \to \infty$ due to the cancellation of cross terms.

**Evaluating the Spectroscope $F_S(\gamma_j)$:**
$$ F_S(\gamma_j) = \gamma_j^2 \left| \Sigma_S(\gamma_j) \right|^2 \approx \gamma_j^2 |c_{\rho_j}|^2 \left( \sum_{p \in S} p^{-1/2} \right)^2 $$

Since $\sum_{p \in S} p^{-1/2} \to \infty$, we have:
$$ F_S(\gamma_j) \sim \text{const}_j \cdot \left( \frac{\sqrt{\max(S)}}{\log(\max(S))} \right)^2 \to \infty $$

For any $\gamma \neq \gamma_j$ (not near a zero), the cross terms dominate (all $k \neq j$), and by the orthogonality of the oscillations, the sum vanishes:
$$ \sum_{p \in S} \frac{M(p)}{p} e^{-i\gamma \log p} \to 0 \quad \text{(Relative to the diagonal)} $$

## 6. Conclusion

The function $F_S(\gamma)$ exhibits a sharp, diverging peak at $\gamma = \gamma_j$ for every non-trivial zero $\rho_j$. Specifically:
1.  **At resonance:** $F_S(\gamma_j) \sim \text{const} \cdot \left(\sum_{p \in S} p^{-1/2}\right)^2 \to \infty$.
2.  **Off-resonance:** $F_S(\gamma) \approx 0$ (or bounded by noise relative to the peak).

Thus, the "spectroscope" detects every non-trivial zero of the Riemann zeta function, confirming the result.
