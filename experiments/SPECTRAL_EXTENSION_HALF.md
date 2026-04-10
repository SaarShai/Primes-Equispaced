# Extending the Spectral Formula to s = 1/2

## Date: 2026-03-30
## Status: Exploratory (Unverified)
## Connects to: N3 (bridge identity), A2 (Dirichlet L-functions)

---

## 1. The Question

The per-step discrepancy kernel has eigenvalues proportional to |L(1,chi)|^2 for Dirichlet characters chi mod p. Specifically, the L2 discrepancy of the Farey sequence decomposes via Parseval as:

    W(N) = sum_j (f_j - j/n)^2 = (1/n^2) sum_{m >= 1} |S(m,N)|^2 / (2*pi*m)^2

where S(m,N) = sum_{f in F_N} e(m*f) are the Farey exponential sums, and the universal formula gives:

    S(m,N) = 1 + sum_{d|m, d <= N} d * M(floor(N/d))

The 1/(2*pi*m)^2 weight means the kernel is K(x,y) = sum_m e(m(x-y))/m^2, which is the Bernoulli B_2 kernel. The connection to L(1,chi) arises because the character decomposition of S(m,N) involves M_chi(N) = sum_{k<=N} chi(k)*mu(k), and M_chi controls 1/L(s,chi) near s = 1.

**Can we get L(1/2,chi) to appear instead?** This would give a direct geometric connection to the critical line of the Riemann Hypothesis.

---

## 2. Approaches Investigated

### 2.1. Approach 1: Change the kernel exponent (alpha-kernel)

Replace the 1/m^2 weight with 1/m^alpha. Define:

    K_alpha(N) = (1/n^2) sum_{m >= 1} |S(m,N)|^2 / m^alpha

**Hypothesis:** K_alpha relates to sum |L(alpha/2, chi)|^2.

**Numerical results (PART 7 of v1):**

| p  | K_2 * n * p / sum|L(1)|^2 | K_1 * n * p / sum|L(1/2)|^2 |
|----|---------------------------|------------------------------|
| 7  | 0.612                     | 7.398                        |
| 11 | 0.400                     | 3.989                        |
| 17 | 0.292                     | 2.712                        |
| 23 | 0.240                     | 2.197                        |
| 43 | 0.150                     | 1.705                        |
| 97 | (not computed at alpha=1)  | (decreasing)                 |

**Finding:** Neither ratio is constant across p. Both decrease. The alpha=2 ratio decreases as roughly 1/log(p), suggesting a missing log factor in the normalization.

**Analysis:** The reason the alpha=1 case is worse is structural. The Dirichlet series sum |S(m)|^2 / m^{2s} factors (approximately) as:

    D(s,N) ~ sum_{d1,d2} d1 d2 M(N/d1) M(N/d2) / lcm(d1,d2)^{2s} * zeta(2s)

At s = 1/2, the factor zeta(2s) = zeta(1) DIVERGES. This pole contaminates the alpha=1 kernel discrepancy, making it grow logarithmically relative to the L-function values. This is a fundamental obstruction: the naive alpha=1 kernel hits the zeta pole at the critical line.

### 2.2. Approach 2: Character-weighted discrepancy

Compute sum_{a/b in F_N} chi(b) * disc(a/b)^2 and compare to |L(s,chi)|^2.

**Coefficient of variation test (PART 5 of v1):**

| p  | CV at s=1.0 | CV at s=0.75 | CV at s=0.50 |
|----|-------------|--------------|--------------|
| 7  | 0.619       | 0.772        | 0.959        |
| 11 | 0.384       | 0.524        | 0.726        |
| 13 | 0.463       | 0.598        | 0.805        |
| 17 | 0.282       | 0.458        | 0.573        |

**Finding:** s = 1 gives the LOWEST CV (most constant ratio across characters), confirming that the standard formula at s=1 is the natural spectral decomposition. Moving toward s=1/2 makes the ratio LESS constant.

### 2.3. Approach 3: Gauss-sum weighted Farey sums

Define T(s, chi, m) = sum_{a/b in F_N} chi(b)/b^s * e(m*a/b). The b^{-s} weight directly connects to the Euler product of L(s, chi).

**Finding:** The ratios |T(s,chi,1)|^2 / |L(s,chi)|^2 are NOT constant across characters at any s. For s=1, the first character (j=1) gives ratios close to 1 for large p (e.g., 0.947 at p=23), but other characters give wildly different ratios (e.g., 25.5 for j=5 at p=23). So this does not diagonalize cleanly.

### 2.4. Approach 4: Per-character kernel convolution

K(chi, alpha) = sum_m chi(m) * |S(m)|^2 / m^alpha. This twists the kernel by the character.

**Finding:** The ratios K(chi,alpha) / |L(alpha/2,chi)|^2 are wildly non-constant and can be negative, meaning this convolution does not decompose into L-function eigenvalues at all. The character twist on the outer sum (over m) does not align with the inner sum structure.

### 2.5. Approach 5: Mellin-type sums

sum_{k=1}^N M(N/k)^2 / k^{2s} at different s values.

**Finding:** At s=1, this is the Franel-Landau sum and relates to W(N). At s=1/2, this gives sum M(N/k)^2 / k, which grows like log(N) * W(N). This again reflects the zeta(1) pole.

---

## 3. The Fundamental Obstruction

All five approaches encounter the same problem: **the zeta pole at s=1**.

The spectral formula at s=1 works because zeta(2) = pi^2/6 is a well-defined constant that can be absorbed into the normalization. When we try to move to s=1/2, the corresponding zeta(1) diverges, and this divergence contaminates every candidate formula.

**Mathematically:** The L2 discrepancy involves the convolution kernel sum |S(m)|^2 / m^{2s}, which factors through zeta(2s). At s=1, zeta(2) is finite. At s=1/2, zeta(1) = infinity.

This is not merely a technical issue --- it reflects a deep fact: the L2 discrepancy naturally lives at s=1, not at s=1/2. To access s=1/2, we need a fundamentally different quantity.

---

## 4. Promising Directions (Not Yet Tested)

Despite the obstruction above, there are several routes that could circumvent it:

### 4.1. The Nyman-Beurling Approach (Most Promising)

The Nyman-Beurling criterion says: **RH holds iff the fractional-part dilations {theta/x} for theta in (0,1) are dense in L^2(0,1).**

This gives a natural L^2 problem whose solution is equivalent to RH. The key objects are:
- The fractional part function rho(theta) = {1/theta} - 1/theta for Farey points theta = a/b
- The Mellin transform of rho, which equals 1/(s(s+1)) * zeta(s+1)/zeta(s)
- At s = 1/2: this involves zeta(3/2)/zeta(1/2), directly touching the critical line

**Connection to our work:** The Farey empirical measure is exactly the set of test points theta = f_j. The Nyman-Beurling distance d_N measures how well {theta/x} spans L^2(0,1) when theta ranges over F_N. By Baez-Duarte's strengthening, one can restrict to integer ratios, and the resulting d_N -> 0 iff RH.

**Why this avoids the zeta(1) pole:** The Nyman-Beurling kernel is NOT a Fourier kernel. It's based on the fractional part function, which has a logarithmic singularity that absorbs the zeta(1) divergence. The resulting L^2 distance involves zeta(s)/zeta(s+1) evaluated at the zeros, not zeta(2s).

**Concrete next step:** Compute the Nyman-Beurling distance d_N for F_N at various N. If d_N * N^{1/2-epsilon} -> 0, this gives the RH convergence rate. The universal formula could provide exact evaluation.

### 4.2. The Karvonen-Zhigljavsky Matern Kernel

Karvonen-Zhigljavsky (2025) proved that for Matern kernels of order >= 1/2, the MMD of F_N converges at polynomial rate iff RH holds. The Matern-1/2 kernel is K(x,y) = exp(-|x-y|/l), whose Fourier transform decays as 1/(1+m^2), not as 1/m^2.

**Key insight:** The Matern-1/2 kernel avoids the zeta(1) pole because its Fourier coefficients decay as 1/(1+m^2) rather than 1/m^2. This means the sum sum |S(m)|^2 / (1+m^2) converges even without the extra m^{-2} factor, bypassing the zeta(1) divergence.

**What this means for L(1/2):** Under RH, the MMD with Matern-1/2 is O(N^{-3/2+epsilon}). The universal formula should give the exact MMD, and its rate of convergence encodes information equivalent to all zeros being on Re(s) = 1/2. The eigenvalues of the Matern-1/2 kernel operator, when restricted to the Farey empirical measure, should involve L(1/2,chi) --- but this requires careful analysis of the operator decomposition.

**Concrete next step:** Compute the Matern-1/2 MMD of F_N exactly using the universal formula. Check if the result factors through |L(1/2,chi)|^2.

### 4.3. Higher-Order Dedekind Sums (Zagier)

Zagier's higher-dimensional Dedekind sums s_m(h,k) use periodized Bernoulli polynomials B_bar_m and connect to L(m,chi) at positive integers m. The generating function approach (Apostol-Zagier sums with complex parameter z) can analytically continue to non-integer m.

**The challenge:** L(1/2,chi) is at a half-integer, not an integer. The classical Dedekind sum machinery is algebraic and works cleanly at integers. Analytic continuation to m=1/2 requires moving from Bernoulli polynomials to their generalization via the Hurwitz zeta function: zeta_H(s,x) analytically continues B_m(x) from integer m to complex s.

**Speculative formula:** Replace B_1(x) * B_1(y) in the classical Dedekind sum with zeta_H(-1/2, x) * zeta_H(-1/2, y). The resulting "half-integer Dedekind sum" might have eigenvalues proportional to L(1/2,chi). This is entirely conjectural and needs both analytical and numerical investigation.

### 4.4. The Selberg Trace Formula Approach

The Selberg trace formula for PSL(2,Z) connects spectral data (Laplacian eigenvalues on the modular surface) to geometric data (lengths of closed geodesics). The Farey sequence is intimately connected to PSL(2,Z) via the Farey tessellation.

**Idea:** The Laplacian eigenvalues lambda_j = s_j(1-s_j) on the modular surface include the spectral parameter s_j, and Selberg's zeta function Z(s) has zeros at s_j. If we could express the Farey discrepancy in terms of the Selberg trace formula, the spectral side would naturally involve L-functions at their spectral parameters, including (hypothetically) s = 1/2.

**This is speculative** and would require a deep analysis of how Farey discrepancy projects onto the spectral decomposition of L^2(PSL(2,Z) \ H).

---

## 5. Summary and Assessment

### What we found:
1. **The zeta(1) pole is the fundamental obstruction** to naive extension of the spectral formula from s=1 to s=1/2. Every approach that uses a Fourier kernel sum 1/m^alpha hits this pole at alpha=1 (i.e., s=1/2).

2. **The standard formula at s=1 is optimal** in the sense that it gives the most constant ratio across characters (lowest CV). Moving toward s=1/2 worsens the spectral decomposition.

3. **To access s=1/2, we need non-Fourier kernels** that bypass the zeta(1) pole. The two most promising are:
   - The **Nyman-Beurling fractional-part kernel**, which naturally encodes RH
   - The **Karvonen-Zhigljavsky Matern-1/2 kernel**, which gives RH equivalence

4. **The Gauss-sum weighted approach** (weighting Farey fractions by chi(b)/b^s) does not diagonalize cleanly, ruling out a simple multiplicative modification.

### Classification:
- **Autonomy:** Level A (essentially autonomous exploration)
- **Significance:** Level 1 (useful negative results, promising directions identified, but no new formula yet)

### Recommended next steps (priority order):
1. **[HIGH]** Compute the Matern-1/2 MMD of F_N using the universal formula, for N up to 10000. Check factorization through L(1/2,chi).
2. **[HIGH]** Compute the Nyman-Beurling d_N distance for F_N, check its decay rate and connection to per-step discrepancy.
3. **[MEDIUM]** Investigate the "half-integer Dedekind sum" via Hurwitz zeta analytic continuation. Compute numerically for small primes.
4. **[LOW]** Explore the Selberg trace formula connection (requires substantial theoretical development).

---

## 6. Technical Notes

### Verification of the universal formula
The identity S(m,N) = 1 + sum_{d|m, d<=N} d*M(N/d) was verified numerically. There is a systematic offset of 1 (the "boundary term" from 0/1 in F_N), confirmed for all m=1..6 and N=10,20,50.

### The zeta(2s) factorization
The Dirichlet series D(s,N) = sum_m |S(m)|^2 / m^{2s} was compared to the double sum formula involving lcm(d1,d2). Agreement is approximate (ratio converges to 1 as H -> infinity), confirming the factorization. At s=0.51 (just above the pole), the direct and formula computations agree within 4%.

### Code
- `spectral_extension_half.py` — v1, five approach tests
- `spectral_extension_half_v2.py` — v2, refined analysis with Ramanujan verification

---

## References

- Karvonen, T. and Zhigljavsky, A. "Maximum mean discrepancies of Farey sequences." *Acta Math. Hungar.* (2025).
- Zagier, D. "Higher dimensional Dedekind sums." *Math. Ann.* 202 (1973), 149-172.
- Gunnells, P. and Sczech, R. "Evaluation of Dedekind sums, Eisenstein cocycles, and special values of L-functions." *Duke Math. J.* 118 (2003).
- Baez-Duarte, L. "A strengthening of the Nyman-Beurling criterion for the Riemann hypothesis." *J. London Math. Soc.* 71 (2005), 715-717.
- Nyman, B. "On the one-dimensional translation group..." Uppsala, 1950.
- Beurling, A. "A closure problem related to the Riemann Zeta-function." *PNAS* 41 (1955), 312-314.
- Patkowski, A. "On some Mellin transforms for the Riemann zeta function in the critical strip." arXiv:1705.02256 (2017).
