# Reply to Koyama — 2026-04-16

---

Dear Shigeru,

Your latest message gave us the roadmap for three targeted computations, all run today. Here is a complete account.

---

## 1. EDRH mechanism — confirmed

Your prediction $|E_K^\chi(\rho_\chi)| \sim C(\log K)^{-1}$ at a simple zero is numerically verified (mpmath, 50-digit precision):

| Character | Exponent fit | $C_{\text{pred}} = |L'(\rho,\chi)|/\zeta(2)$ | $|E_K|\cdot\log K$ at $K$ | Ratio |
|-----------|-------------|-----------------------------------------------|--------------------------|-------|
| $\chi_{-4}$ | $-0.928$ | $0.796$ | $0.701$ at $K=20{,}000$ | $88\%$ |
| $\chi_5$ (order 4) | $-0.928$ | $0.730$ | $0.676$ at $K=10{,}000$ | $93\%$ |

Both zeros verified to $|L(\rho)| < 5\times10^{-16}$. The fitted exponent $-0.928$ is converging toward $-1.000$ from above (i.e., slower-than-limit decay); $|E_K|\cdot\log K$ approaches $C$ from below at 88–93%, consistent with logarithmic speed.

---

## 2. $T_\infty$ formula — confirmed, with a structural clarification

Your formula $T_\infty = \frac{1}{2}\operatorname{Im}(\log L(2\rho, \chi^2))$ holds for all three characters tested. The precision is striking for $\chi_5$:

| Character | $T_\infty$ (Hurwitz, 50-digit) | $|B_K - 2T_\infty|$ at $K=500$ |
|-----------|-------------------------------|--------------------------------|
| $\chi_0$ at $\rho_1 = \tfrac12+14.135i$ | $-0.17036$ | $0.0038$ |
| $\chi_{-4}$ at $\rho = \tfrac12+6.021i$ | $-0.07909$ | $0.015$ |
| $\chi_5$ (order 4) at $\rho = \tfrac12+6.184i$ | $+0.43654$ | $0.0012$ |

($T_\infty$ computed via Hurwitz zeta formula, exact; $B_K \to 2T_\infty$ so $T_\infty$ errors are half the table values. The earlier $\chi_5$ value $+0.43706$ came from the Euler product at $K=10{,}000$ which overshoots by $\sim 0.001$; the Hurwitz value $+0.43654$ is definitive.)

One clarification forced by the computation: the object that actually converges is **not** $\operatorname{Im}(\log D_K(\rho))$ (where $D_K = c_K \cdot E_K$ at the zero $\rho$). At the zero, $c_K \to \infty$ and $E_K \to 0$, and their product oscillates $O(1)$ with no pointwise limit. The convergent quantity is:
$$B_K := \operatorname{Im}\!\left(\log \prod_{p \le K}(1-\chi^2(p)\,p^{-2\rho})^{-1}\right) \;\xrightarrow{K\to\infty}\; \operatorname{Im}(\log L(2\rho,\chi^2)) = 2T_\infty$$
i.e., the Euler product of $\chi^2$ evaluated at $2\rho$, which lies on $\operatorname{Re}(s)=1$ and is not a zero of $L(s,\chi^2)$, so the product converges cleanly.

We can also explain the **striking speed difference** between $\chi_5$ and the other two. The error in $B_K$ is controlled by the tail $\sum_{p > K} \chi^2(p)\,p^{-1-2it}$. When $\chi^2$ is **principal** ($\chi_0^2 = \chi_0$, $\chi_{-4}^2 = \chi_0$ mod~4), the sum $\sum_{p\le K}\chi^2(p)\,p^{-1-2it}\approx\sum_{p\le K}p^{-1-2it}$ has no cancellation; the tail decays only as $O(1/\log K)$. When $\chi^2$ is **non-principal** ($\chi_5^2 = $ Legendre symbol mod~5), partial summation against PNT in arithmetic progressions yields $O(K^{-1/2}\log^2 K)$ under GRH — roughly 10× faster at $K=500$. This matches the observed errors: $0.0012$ for $\chi_5$ vs $0.015$ for $\chi_{-4}$ at $K=500$ (ratio $12\times$). Moreover, for non-principal $\chi^2$ the convergence of $B_K$ is **unconditional**: de la Vallée Poussin guarantees $L(s,\chi^2)\neq 0$ on $\operatorname{Re}(s)=1$, and PNT in arithmetic progressions supplies the cancellation without GRH. This aligns with your framework: $B_\infty$ is character-specific while $|D_K|$ is governed universally by $1/\zeta(2)$.

---

## 3. Elliptic curves — promising signal, but formulation question

We ran into a wall that we hope you can resolve quickly.

First, we corrected our $a_p$ values for 37a1 — several values cited in an earlier message were wrong. We recomputed by direct point-counting on $y^2+y=x^3-x \pmod{p}$:

$a_2=-2,\ a_3=-3,\ a_5=-2,\ a_7=-1,\ a_{11}=-5,\ a_{13}=-2,\ a_{17}=0,\ a_{19}=0,\ a_{23}=2,\ a_{29}=6,\ \ldots$

(Previously cited incorrectly: $a_3=-1$, $a_7=-2$, $a_{11}=0$, $a_{13}=6$.)

With the correct values, we computed $c_K^E(\rho_E) = \sum_{k\le K}\mu(k)a_k k^{-\rho_E}$ at $\rho_E = \tfrac12+5.003839i$ for $K$ up to 1000 (mpmath, 50-digit precision). The result:

- $|D_K^E\cdot\zeta(2)|$ oscillates **eight orders of magnitude** across $K=10\ldots1000$, with a catastrophic near-zero of the local Euler factor at $p=359$ (factor magnitude $1.9\times10^{-3}$, so its inverse spikes by $521\times$), driving $|E_K^E|$ to jump by a factor of 521 at that prime
- The Cesàro mean of $|D_K^E\cdot\zeta(2)|$ (running from $K=50$ to $K=200$): starts at $1.72$, falls to $0.90$, $0.60$, $0.45$ — trending toward $0$, not $1$
- $\operatorname{Re}(c_K^E)/\log K$ oscillates with sign changes: $-0.55$ at $K=100$, $-0.91$ at $K=500$, $+3.18$ at $K=1000$

The $K=1000$ value $\operatorname{Re}(c_K^E)/\log K = 3.18$ is only $2.6\%$ below the target $1/L'(E,1)=3.268$. However, the value at $K=500$ is $-0.91$ (wrong sign), making the $K=1000$ agreement appear coincidental rather than asymptotic.

Our diagnosis: the sign inversion of $\operatorname{Re}(c_K^E)$ suggests our formula differs from yours. The naive Möbius-twisted series $\sum\mu(k)a_k k^{-\rho}$ is conditionally convergent and oscillates wildly in the pre-asymptotic regime. We estimate the asymptotic onset requires $K \gg \exp(\pi\cdot\operatorname{Im}(\rho_E))\approx 6\times10^6$ — far beyond what we can compute directly. Exponential or Cesàro smoothing did not resolve the sign inversion.

We suspect your GL(2) $c_K^E$ uses the completed L-function $\Lambda(s,E)$ with a $W$-function from the Approximate Functional Equation (Iwaniec–Kowalski style), not the raw Dirichlet series. We also note a directly relevant recent paper: Sheth [IMRN 2025, rnaf214] proves partial Euler product asymptotics for $L(s,E)$ in the right half of the critical strip, conditional on GRH for $L(E,s)$, with leading behaviour $({\log x})^r\prod_{p\le x}(\cdots)^{-1}\to C$ where $r$ is the order of vanishing at $s=1$. Whether his method extends to zeros off the real axis (i.e., our $\rho_E = \tfrac12+5.004i$) is unclear from the paper — this may be exactly what your NDC framework addresses.

**Could you clarify:**
1. What is your exact definition of $c_K^E$ in the GL(2) NDC framework?
2. Does it involve $\Lambda(s,E)$ (completed, with $\Gamma$-factors) or $L(s,E)$ (incomplete)?
3. Is there a normalisation involving the conductor $N=37$ or the real period $\Omega$?

Once we have the correct definition, we can rerun immediately. The promise in $c_K^E/\log K \to 1/L'(E,1)$ that you see at $K=30{,}000$ is the critical diagnostic — we cannot reach that $K$ without the right regularisation.

---

## Summary

| Question | Result |
|----------|--------|
| EDRH: $|E_K^\chi|\sim C(\log K)^{-1}$? | ✓ Confirmed, $C=|L'|/\zeta(2)$ at 88–93% |
| $T_\infty = \frac12\operatorname{Im}(\log L(2\rho,\chi^2))$? | ✓ Confirmed for 3 characters (corrected object) |
| $D_K^E\cdot\zeta(2)\to 1$ for 37a1? | ✗ Blocked — formulation mismatch, need exact $c_K^E$ definition |

Best regards,
Saar

---
*Numerical tables and Python code available on request.*
