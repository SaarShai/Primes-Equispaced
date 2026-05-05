# Family-Averaged Theorem B Numerical Test

**Date:** 2026-05-03
**Hypothesis tested:** family-averaging accelerates convergence of the
Montgomery–Nakamura ratio
$$
u_f(T) = \frac{\sum_{|\gamma_f|\le T}|L'(\tfrac12+i\gamma_f,f)|^2}{c_f \cdot T \cdot \log^4(N_f T/(2\pi))}
$$
to the predicted constant $A_4 = 2/(3\pi) \approx 0.21221$, where the slow
single-curve drift $u_{11a1}(T) \approx 2.6$ (T=800) is suspected to be a
finite-T fluctuation that the family average cancels.

## Conventions (G8 v4)

- $\sigma = k/2$ (PARI arithmetic critical line)
- $c_f = (1/x)\sum_{n\le x} |a_n|^2 / n^{k-1}$ at $x = 20{,}000$
- $Y = \log\sqrt{q T / (2\pi)}$  (matches G8 v4; no $k$ factor)
- $u_f(T) = S_f / (c_f \cdot T \cdot Y^4)$
- Family average: $\bar u(T) = |F|^{-1}\sum_{f\in F} u_f(T)$
- Cage: $[(17-\sqrt{145})/(12\pi),\, (17+\sqrt{145})/(12\pi)] \approx [0.1315, 0.7704]$

## Families

- **Family A:** 14 small squarefree-level $k=2$ elliptic newforms
  {11a1, 14a1, 15a1, 17a1, 19a1, 21a1, 26a1, 33a1, 35a1, 37a1, 38a1, 43a1, 53a1, 57a1}
  at $T \in \{100, 200, 400, 800, 1500\}$.
- **Family B:** $\Delta$ (level 1, $k=12$) — single orbit at $T \in \{100, 200, 400, 800, 1500\}$.

## Section 1: Per-curve $u_f$ at each $T$ (Family A)

[populated from PARI output]

## Section 2: Family-averaged $\bar u(T)$ vs $0.21221$

[populated from PARI output]

## Section 3: Variance across family

[populated from PARI output]

## Section 4: Cage check on family average

[populated from PARI output]

## Section 5: Verdict — possibility (a) vs possibility (c)

[populated after data]
