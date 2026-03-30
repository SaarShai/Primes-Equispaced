# Higher Moments of Farey Per-Step Discrepancy

**Date:** 2026-03-30
**Status:** Unverified (needs independent replication and novelty check)
**Classification:** C1-C2 (Collaborative, minor-to-publication novelty pending verification)
**Connects to:** N1 (per-step discrepancy), N2 (M(p) connection)

## Setup

For prime p, the **per-step discrepancy** is defined for each fraction a/b in F_{p-1} (with b < p) as:

    delta(a/b) = (pa mod b)/b - a/b

This measures how the fraction a/b is displaced when the Farey sequence transitions from order p-1 to order p. Since p is prime, multiplication by p permutes residues mod b, so pa mod b is a permutation of the coprime residues.

The **L^2 moment** (sum of squared displacements) is known:

    S_2 = sum delta(a/b)^2 ~ p^2 / (2*pi^2)

where the sum runs over all a/b in the interior of F_{p-1}.

## Questions Investigated

1. What are the higher moments S_4, S_6, S_8?
2. Do the ratios S_{2k}/p^2 converge to constants? What are they?
3. Is there a spectral formula for L^4 involving L-function fourth moments?
4. What distribution do the per-step deltas approach?

---

## Finding 1: All Even Moments Scale as p^2

Computed S_{2k}/p^2 for primes up to 997:

| p   | S_2/p^2    | S_4/p^2    | S_6/p^2    | S_8/p^2    |
|-----|-----------|-----------|-----------|-----------|
| 11  | 0.02439   | 0.00545   | 0.00179   | 0.00076   |
| 29  | 0.03774   | 0.01243   | 0.00582   | 0.00333   |
| 53  | 0.04314   | 0.01561   | 0.00764   | 0.00457   |
| 97  | 0.04795   | 0.01823   | 0.00933   | 0.00577   |
| 199 | 0.04785   | 0.01826   | 0.00940   | 0.00586   |
| 503 | 0.04858   | 0.01883   | 0.00980   | 0.00616   |
| 997 | 0.05008   | 0.01984   | 0.01053   | 0.00669   |

All ratios converge as p grows. The constants are:

    S_2/p^2 -> 1/(2*pi^2) = 0.05066  (known)
    S_4/p^2 -> 1/(5*pi^2) = 0.02026  (NEW)
    S_6/p^2 -> 3/(28*pi^2) = 0.01086 (NEW)
    S_8/p^2 -> 1/(15*pi^2) = 0.00675 (NEW)

## Finding 2: Triangular Distribution (Main Discovery)

The standardized per-step deltas (z = delta/sigma) have moments that match the **triangular distribution** on [-1,1] (density f(x) = 1 - |x|) to high precision:

| Moment | Observed (p=997) | Triangular (exact) | Gaussian |
|--------|------------------|--------------------|----------|
| E[z^4] | 2.400            | 12/5 = 2.400       | 3.000    |
| E[z^6] | 7.719            | 54/7 = 7.714       | 15.000   |
| E[z^8] | 28.838           | 144/5 = 28.800     | 105.000  |

The match is remarkable: 4 significant figures for the 4th moment, 3 for the 6th, and 3 for the 8th. The per-step Farey discrepancy converges in distribution to a **triangular random variable**.

All odd moments are zero (by symmetry: the distribution is symmetric around 0).

## Finding 3: General Formula for All Even Moments

The triangular distribution gives a closed-form prediction for ALL even moments:

    S_{2k} / p^2 -> 3 / (pi^2 * (2k+1) * (k+1))

Explicitly:
- S_2/p^2 -> 3/(pi^2 * 3 * 2) = 1/(2*pi^2)  [MATCHES known result]
- S_4/p^2 -> 3/(pi^2 * 5 * 3) = 1/(5*pi^2)
- S_6/p^2 -> 3/(pi^2 * 7 * 4) = 3/(28*pi^2)
- S_8/p^2 -> 3/(pi^2 * 9 * 5) = 1/(15*pi^2)
- S_{2k}/p^2 -> 3/(pi^2 * (2k+1)(k+1))

This is a **single formula that unifies all moments**, with the L^2 case being merely k=1.

## Finding 4: Intuitive Explanation

**Why triangular?** The triangular distribution on [-1,1] arises as the convolution of two independent Uniform[0,1] random variables: U_1 - U_2 ~ Triangular[-1,1].

For the per-step discrepancy:
- delta(a/b) = {pa/b} - a/b  (fractional part minus the fraction)
- For fixed b, {pa/b} is a permutation of coprime residues mod b
- When we average over ALL denominators b < p, the pair (a/b, {pa/b}) becomes approximately equidistributed in [0,1]^2
- In the limit, delta behaves like U_1 - U_2 with independent uniforms
- The convolution Uniform * Uniform = Triangular

The key step (asymptotic independence of a/b and {pa/b} when averaged over b) is the non-trivial claim that would need proof.

## Finding 5: Farey Sequence Discrepancy (Non-Per-Step) is NOT Gaussian

For the full Farey sequence F_N discrepancy delta_j = f_j - j/|F_N|, the standardized kurtosis GROWS with N:

| p   | n = |F_p| | E[z^4]   |
|-----|-----------|----------|
| 53  | 883       | 11.9     |
| 199 | 12153     | 31.2     |
| 503 | 77201     | 80.6     |
| 997 | 302647    | 154.2    |

The kurtosis grows roughly as p/6 (proportional to sqrt(n)). This means the Farey discrepancy has **extremely heavy tails**: most discrepancies are small, but a few fractions have disproportionately large discrepancy. This is consistent with the fact that discrepancy is concentrated near "badly approximable" fractions (those with small denominators).

The Farey sequence discrepancy does NOT converge to any fixed distribution -- it has a limiting shape that scales with N.

## Finding 6: Spectral Connection to L-Functions

The L^2 spectral identity is:

    W(N) = (N/pi^2) * sum_{chi} |L(1,chi)|^2 * |weights|^2

For L^4, if a parallel identity exists, it would involve the **fourth moment of L-functions**:

    sum_{chi mod q} |L(1,chi)|^4

The fourth moment of L-functions at the critical line is deeply studied (connected to the Iwaniec-Kowalski program). Our triangular distribution result suggests that the spectral decomposition of M_4 should factor cleanly, with the constant 1/(5*pi^2) encoding the same pi^2 factor from the Ramanujan sum spectral identity.

This connection warrants further investigation but is not yet established.

---

## Summary of Constants

| Moment | Constant c_{2k}     | Exact form             | Numerical value |
|--------|---------------------|------------------------|-----------------|
| S_2    | c_2 = 1/(2pi^2)     | 3/(pi^2 * 6)          | 0.050661        |
| S_4    | c_4 = 1/(5pi^2)     | 3/(pi^2 * 15)         | 0.020264        |
| S_6    | c_6 = 3/(28pi^2)    | 3/(pi^2 * 28)         | 0.010856        |
| S_8    | c_8 = 1/(15pi^2)    | 3/(pi^2 * 45)         | 0.006755        |
| S_{2k} | c_{2k}              | 3/(pi^2(2k+1)(k+1))   | decreasing      |

---

## Verification Status

- [x] Computed for primes 11, 29, 53, 97, 199, 503, 997
- [x] Exact arithmetic verification for p = 11, 29, 53
- [x] Standardized moments match triangular to 3-4 significant figures
- [x] Known L^2 result recovered as k=1 special case
- [ ] Independent replication by separate agent (Step 1)
- [ ] Novelty check for triangular distribution claim (Step 2)
- [ ] Adversarial audit (Step 3)
- [ ] Analytical proof of triangular convergence

## Next Steps

1. **Prove the triangular convergence**: Show that the pair (a/b, {pa/b}) is equidistributed in [0,1]^2 when averaged over b < p with appropriate Euler totient weights. This likely uses large sieve or Kloosterman sum estimates.

2. **Spectral decomposition of M_4**: Express S_4 in terms of L-function fourth moments using the Ramanujan sum framework from the L^2 case.

3. **Rate of convergence**: The convergence to 1/(5*pi^2) is slower than for 1/(2*pi^2). Quantify the error terms.

4. **Connection to RH**: If the spectral formula for S_4 involves |L(1/2,chi)|^4, this creates a new route to RH through moment bounds. The fourth moment of L-functions is better understood than individual L-function values.

5. **Lean formalization**: The triangular distribution result, once proved, is a clean theorem suitable for Lean 4 formalization.

## Scripts

- `experiments/higher_moments.py` -- initial computation (v1)
- `experiments/higher_moments_v2.py` -- refined computation with distribution analysis
