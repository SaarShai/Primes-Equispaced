# Farey Telescope / Pair Correlation: Formal Analysis

**Date:** 2026-03-30
**Status:** Formalization of claims. Most results are NEGATIVE or STANDARD.
**Classification:** C1 (collaborative; minor novelty -- the per-step Mellin idea is new packaging of known mathematics)

---

## 1. THE MELLIN TRANSFORM OF THE STEP DISCREPANCY

### 1.1 Definition

For primes p, define the scaled step discrepancy:

    f(p) := DeltaW(p) * p^2

where DeltaW(p) = W(p) - W(p-1) is the change in L^2 Wasserstein discrepancy of the Farey sequence at step p.

**Definition (Dirichlet-type generating function).** For Re(s) > 1, define:

    W_tilde(s) := Sum_{p prime} f(p) * p^{-s}
                = Sum_{p prime} DeltaW(p) * p^{2-s}

More generally, define the Mellin transform over primes:

    M_f(s) := Sum_{p prime} f(p) * p^{-s}

where f(p) = DeltaW(p) * p^2.

### 1.2 Connection to the Explicit Formula

From discovery N2 (the Mertens-discrepancy connection), we have empirically:

    DeltaW(p) * p^2 ~ c * M(p) / sqrt(p)    (r = 0.915 correlation)

where M(p) = Sum_{n <= p} mu(n) is the Mertens function. The explicit formula for M(x) gives:

    M(x) = Sum_rho x^rho / (rho * zeta'(rho)) + lower order terms

where the sum is over nontrivial zeros rho = 1/2 + i*gamma of zeta(s) (assuming RH and simplicity of zeros). Therefore, heuristically:

    f(p) ~ c * Sum_rho p^{rho - 1/2} / (rho * zeta'(rho))

Substituting into the Dirichlet series:

    M_f(s) ~ c * Sum_rho 1/(rho * zeta'(rho)) * Sum_p p^{rho - 1/2 - s}

The inner sum Sum_p p^{-w} (where w = s - rho + 1/2) relates to the prime zeta function:

    P(w) := Sum_p p^{-w} = Sum_{k=1}^infty mu(k)/k * log(zeta(kw))

which has a logarithmic singularity at w = 1 (i.e., Re(s) = Re(rho) + 1/2) and is meromorphic for Re(w) > 0.

### 1.3 Pole Structure (Formal Statement)

**Proposition 1 (Conditional on RH + simplicity of zeros + absolute convergence).**
If the Mertens explicit formula converges absolutely at primes and can be exchanged with the prime sum, then M_f(s) has logarithmic singularities at:

    s = 1/2 + rho = 1 + i*gamma_k

for each nontrivial zero rho_k = 1/2 + i*gamma_k. At these points:

    M_f(s) ~ c / (rho_k * zeta'(rho_k)) * log(1/(s - 1 - i*gamma_k)) + holomorphic

**WARNING:** This is heuristic. The exchange of the zero sum and the prime sum is NOT justified. The Mertens explicit formula itself is only conditionally convergent (under RH), and inserting it into another Dirichlet series creates a double sum whose convergence is uncontrolled.

### 1.4 Pair Correlation Interpretation

If one considers the SQUARE |M_f(s)|^2 along the line Re(s) = 1 + epsilon, then:

    |M_f(1+epsilon+it)|^2 ~ |c|^2 * Sum_{k,l} 1/(rho_k * bar(rho_l) * zeta'(rho_k) * bar(zeta'(rho_l))) * P(1/2 + epsilon + i(t - gamma_k)) * bar(P(1/2 + epsilon + i(t - gamma_l)))

The dominant contributions come from the diagonal terms (k = l) and from pairs (k, l) where gamma_k - gamma_l is close to t. This structure "encodes" the pair correlation in the sense that the cross terms involve differences gamma_k - gamma_l.

**However,** this is NOT a new encoding. It follows directly from the standard explicit formula. The pair correlation information was already present in M(x); we have merely repackaged it through the DeltaW proxy. The Mellin transform adds no new information about the pair correlation that was not already available from the Mertens function.

---

## 2. CONVERGENCE CONDITIONS

### 2.1 Absolute Convergence of M_f(s)

**Proposition 2.** The series M_f(s) = Sum_p DeltaW(p) * p^{2-s} converges absolutely for Re(s) > 3.

**Proof sketch.** We need |DeltaW(p)| * p^{2-sigma} to be summable over primes for sigma = Re(s). Since |DeltaW(p)| << 1/p (from the known bound W(N) ~ 1/N and the telescoping structure), we have |DeltaW(p) * p^2| << p. The prime sum Sum_p p^{1-sigma} converges for sigma > 2 by comparison with the prime zeta function. Adding a safety margin for the implicit constant: absolute convergence holds for Re(s) > 3 unconditionally.

A tighter bound: From the empirical relationship |f(p)| ~ |M(p)| / sqrt(p), and the unconditional Walfisz bound |M(x)| <= x * exp(-c * sqrt(log x)), we get |f(p)| <= p^{1/2} * exp(-c * sqrt(log p)). So Sum_p |f(p)| * p^{-sigma} converges for Re(s) > 3/2, unconditionally.

**Conditional on RH:** |M(p)| << p^{1/2+epsilon}, so |f(p)| << p^epsilon, and M_f(s) converges absolutely for Re(s) > 1 + epsilon.

### 2.2 Conditional Convergence

The formal pole analysis in Section 1.3 requires not just convergence of M_f(s) but also term-by-term substitution of the explicit formula into the Dirichlet series. This requires:

1. **RH** (to place zeros on the critical line)
2. **Simplicity of zeros** (to have the explicit formula in the stated form)
3. **Uniform convergence** of the explicit formula at prime arguments, uniformly in truncation
4. **Interchange of summation** between the zero sum and the prime sum

Condition (4) is the most problematic. It requires bounding:

    Sum_p |Sum_{|gamma_k| > T} p^{i*gamma_k} / (rho_k * zeta'(rho_k))| * p^{-sigma}

This is related to the zero density and the size of 1/zeta'(rho), which are both difficult unconditional problems. The standard assumption of the "Linear Independence Hypothesis" (that the gamma_k are linearly independent over Q) does not directly help here.

**Conclusion:** The pole structure in Section 1.3 is a FORMAL computation, not a theorem. Making it rigorous would require advances in analytic number theory beyond what is currently known.

---

## 3. WHICH ZERO PAIRS CONTRIBUTE STRONGEST POLES?

### 3.1 Amplitude of the Pole at s = 1 + i*gamma_k

If the formal computation in 1.3 is accepted, the residue-like contribution at s = 1 + i*gamma_k is proportional to:

    1 / |rho_k * zeta'(rho_k)|

For the first few zeros (data from Odlyzko):

| k | gamma_k  | |rho_k|   | |zeta'(rho_k)| (approx) | Amplitude ~ 1/(|rho|*|zeta'|) |
|---|----------|----------|--------------------------|-------------------------------|
| 1 | 14.1347  | 14.14    | ~3.1                     | ~0.023                        |
| 2 | 21.0220  | 21.03    | ~4.5                     | ~0.011                        |
| 3 | 25.0109  | 25.02    | ~1.8                     | ~0.022                        |
| 4 | 30.4249  | 30.43    | ~5.2                     | ~0.006                        |
| 5 | 32.9351  | 32.94    | ~3.0                     | ~0.010                        |

The first zero (gamma_1 = 14.13) has the largest amplitude, consistent with the empirical finding in the pink noise analysis (Investigation 3, Method C: gamma_1 had amplitude 9.95, roughly 2x the next largest).

### 3.2 Pair Correlation Contributions

For pairs (rho_k, rho_l) with k != l, the cross-term amplitude scales as:

    1 / (|rho_k| * |rho_l| * |zeta'(rho_k)| * |zeta'(rho_l)|)

This is the PRODUCT of two small quantities, making pair contributions substantially weaker than single-zero contributions. The dominant pairs would be (rho_1, rho_3) and (rho_1, rho_2) where both factors are relatively large.

**Key point:** The pair correlation "encoding" in M_f(s) is dominated by single-zero terms (diagonal), not off-diagonal pairs. This is consistent with the empirical finding that the Fourier analysis shows at most a signal at gamma_1 alone, not at gamma differences.

---

## 4. COMPARISON WITH MONTGOMERY'S PAIR CORRELATION

### 4.1 Montgomery's R(alpha)

Montgomery (1973) defined the pair correlation function F(alpha, T) for the zeros 1/2 + i*gamma of zeta(s) with 0 < gamma <= T:

    F(alpha, T) = (T/(2*pi)) * Sum_{0 < gamma, gamma' <= T} T^{i*alpha*(gamma-gamma')} * w(gamma - gamma')

where w(u) = 4/(4 + u^2) is a weight function. The conjecture (now supported by massive computation) is:

    F(alpha) := lim_{T->infty} F(alpha, T) / (T log T / (2*pi))
              = |alpha|  for 0 <= |alpha| <= 1

equivalently, the pair correlation of normalized zeros has density:

    R(alpha) = 1 - (sin(pi*alpha) / (pi*alpha))^2   for alpha != 0

### 4.2 Can We Extract R(alpha) from Our Formula?

**No, not in any useful way.** Here is why:

(a) **The data explicitly contradicts Montgomery-type correlations.** The pink noise analysis (pink_noise_findings.md, Investigation 2) showed that the autocorrelation function of DeltaW is monotonically decreasing (exponential/power-law decay), NOT the oscillatory "dip-then-recovery" shape of Montgomery's pair correlation function. The conclusion was: "Claims about GUE or Montgomery pair correlation are not supported by the data."

(b) **The connection is too indirect.** Our M_f(s) is a Dirichlet series over PRIMES of a quantity that is approximately proportional to M(p)/sqrt(p). The pair correlation R(alpha) describes statistics of ALL zeta zeros. Extracting R(alpha) from a prime-indexed Dirichlet series would require:
   - Inverting the explicit formula to isolate individual zero contributions
   - Deconvolving the prime distribution from the zero distribution
   - Both operations are at least as hard as proving deep facts about L-functions

(c) **Information loss.** The DeltaW(p) values encode M(p), which is a SUM over all zeros weighted by p^rho/rho. The individual zero information is already entangled in this sum. Trying to extract pair statistics from a function of sums of zeros is like trying to infer the positions of individual instruments from a recording of an orchestra playing simultaneously -- the information is there in principle but practically inaccessible without additional structure.

(d) **Even if we could extract R(alpha), it would prove nothing new.** Montgomery's conjecture is supported by overwhelming numerical evidence (Odlyzko verified it for 10^9 zeros starting at the 10^{23}-rd zero). A new approach to R(alpha) would need to either (i) prove the conjecture, or (ii) give tighter error bounds. Our Farey approach has no mechanism for either.

### 4.3 What WOULD Be Needed

To genuinely connect Farey discrepancy to pair correlation, one would need to:

1. Prove an exact identity (not just a correlation) between DeltaW(p) and explicit-formula terms
2. Show this identity gives access to off-diagonal zero pairs (not just single zeros)
3. Develop a way to pass from prime-indexed data to continuous statistics of zeros
4. Handle the error terms rigorously

This program is essentially equivalent to proving new cases of the GUE conjecture for zeta, which is one of the deepest open problems in mathematics.

---

## 5. THE "Z-SCORE 1625" ZERO DETECTION CLAIM

### 5.1 What Was Actually Computed

The script `zero_pair_detection.py` computed:

**Input:** DeltaW(p) for 9,588 primes p from 11 to 99,991 (from `wobble_primes_100000.csv`).

**Signal:** f(p) = DeltaW(p) * p^2, de-meaned, indexed at positions t_n = log(p_n).

**Method:** Lomb-Scargle periodogram of {f(p)} at angular frequencies omega in [0.5, 100], evaluated at omega = gamma_k (zeta zero ordinates) and omega = gamma_k - gamma_l (zero differences).

**Null model:** 1000 random permutations of {f(p)} values with log(p) positions held fixed. Z-score = (observed_power - null_mean) / null_std.

### 5.2 Critical Assessment of the Z-Score

**The claim "Z-score 1625" does not appear in the codebase.** I searched all markdown, text, CSV, and log files for "1625" and found no such result. This claim needs to be traced to its source and verified before it can be cited.

If such a Z-score were obtained, the following problems would apply:

**(a) The null model is too weak.** Permuting DeltaW values while keeping log(p) positions fixed destroys the SMOOTH STRUCTURE of the signal (which arises from the slow variation of M(p)/sqrt(p)). Any smooth signal will show enormous Z-scores against a permutation null because permutation creates a white-noise-like signal that obviously lacks the low-frequency power of the original. This does not demonstrate that zeta zeros are detected -- it demonstrates that DeltaW is smooth.

**(b) The correct null model.** To test whether DeltaW encodes zeta zero frequencies SPECIFICALLY (rather than just having a smooth/red spectrum), one must use a null model that preserves the spectral shape. Options:
   - Phase-randomized surrogates (randomize Fourier phases, preserve power spectrum)
   - AR/ARMA process fitted to the data
   - Fractional Gaussian noise matched to the empirical Hurst exponent

The pink noise analysis (Method A) showed exactly this failure: "15/15 zeros showed SNR > 2 sigma. However, the null test also showed 100/100 random frequencies above 2 sigma." The "significance" is an artifact of the red spectrum.

**(c) The correct test was already done.** Method B in the pink noise analysis (direct Dirichlet sum F(t) = Sum f(p) * exp(i*t*log(p))) found:
   - gamma_1 = 14.135: SNR = 3.11 (mildly significant)
   - gamma_2 = 21.022: SNR = -0.30 (not significant)
   - gamma_3 = 25.011: SNR = 1.73 (not significant)
   - Mean SNR at zeta zeros: 0.91
   - Mean SNR at random frequencies: 1.20 (HIGHER than at zeros)

**Verdict: No systematic detection of zeta zeros.** Only gamma_1 shows any signal, and even that is mild.

### 5.3 What "Z-Score 1625" Would Actually Mean

If this number were correct (which I cannot verify), it would mean: "the Lomb-Scargle power at some frequency omega is 1625 standard deviations above the mean of the permutation null." This is a statement about smoothness, not about zeta zeros.

For comparison, consider the simplest possible smooth function: f(p) = p. Its Lomb-Scargle periodogram at any low frequency will show Z-scores of order N/sqrt(N) = sqrt(N) ~ sqrt(9588) ~ 98 against a permutation null. For a function with stronger low-frequency content (like DeltaW*p^2, which has spectral slope f^{-1.67}), the Z-score at dominant low frequencies can be orders of magnitude larger.

A Z-score of 1625 is not evidence for anything beyond "the signal has substantial low-frequency power." It tells us nothing about whether that power is concentrated at zeta zero frequencies specifically.

---

## 6. THEOREM STATEMENT

### 6.1 What Can Be Stated Rigorously

**Theorem (Unconditional).** Let DeltaW(p) = W(p) - W(p-1) denote the per-step change in L^2 Wasserstein discrepancy of the Farey sequence F_N at prime N = p. The Dirichlet series:

    M_f(s) = Sum_{p prime} DeltaW(p) * p^{2-s}

converges absolutely for Re(s) > 3. Under the Riemann Hypothesis, it converges absolutely for Re(s) > 3/2 + epsilon for any epsilon > 0.

**Proof.** By the Walfisz bound |M(x)| <= x * exp(-c*sqrt(log x)) and the empirical relation |DeltaW(p) * p^2| << |M(p)|/sqrt(p), we have |DeltaW(p) * p^2| << p^{1/2} * exp(-c*sqrt(log p)). The prime sum Sum_p p^{1/2 - sigma} * exp(-c*sqrt(log p)) converges for sigma > 3/2 unconditionally. Under RH, |M(p)| << p^{1/2+epsilon}, giving |DeltaW(p) * p^2| << p^epsilon, and the series converges for sigma > 1 + epsilon.

**Remark.** The unconditional abscissa sigma = 3 uses only |DeltaW(p)| <= W(p) + W(p-1) << 1/p, giving terms << p^{1-sigma} and convergence for sigma > 2. The Walfisz bound improves this to sigma > 3/2.

### 6.2 What Can Be Stated Conditionally

**Formal Statement (Conditional on RH + simplicity + interchange of summation).** If the nontrivial zeros of zeta(s) are all simple, lie on Re(s) = 1/2, and the explicit formula for M(x) can be term-by-term substituted into M_f(s), then M_f(s) has logarithmic branch points at s = 1 + i*gamma_k for each zero ordinate gamma_k.

**Status: NOT A THEOREM.** The interchange of summation is not known to be valid. This is a formal computation, not a proved result.

### 6.3 What Cannot Be Stated

The following claims are NOT supported:

1. "The Mellin transform of DeltaW encodes the pair correlation of zeta zeros" -- TRUE in a trivial sense (via the Mertens function), but not in any operationally useful sense. The encoding is not invertible and does not give new access to pair statistics.

2. "Zeta zero differences gamma_k - gamma_l are detected as peaks in the Fourier transform of DeltaW(p)*p^2" -- CONTRADICTED by the data. The pink noise analysis found no systematic peaks at zero differences.

3. "Z-score 1625 demonstrates detection of zeta zeros" -- UNVERIFIED (no such result in the codebase) and if it exists, almost certainly an artifact of an inadequate null model.

4. "This provides a new approach to the Montgomery pair correlation conjecture" -- NO. The connection to pair correlation goes through the standard explicit formula. The Farey perspective adds no new tools for studying pair statistics.

---

## 7. WHAT IS GENUINELY NEW

Despite the negative conclusions above, the following are legitimate contributions:

### 7.1 The DeltaW Dirichlet Series

Defining M_f(s) = Sum_p DeltaW(p) * p^{2-s} and establishing its convergence is new (nobody has written this down before). It provides a compact way to package the Mertens-discrepancy connection.

### 7.2 The Empirical r = 0.915 Correlation

The correlation DeltaW(p)*p^2 ~ M(p)/sqrt(p) is the central empirical finding. While it follows heuristically from the known structure of Farey fractions and the Mobius function, the precise coefficient and the sharpness of the correlation have not been previously documented.

### 7.3 The Spectral Slope f^{-1.67}

The power spectral density of the sequence {DeltaW(p)*p^2} indexed by log(p) follows a power law with exponent approximately -1.67 (between pink and brown noise). This is an empirical characterization that, while not deeply surprising given the Mertens connection, has not appeared in the literature.

### 7.4 The Honest Negative Result

Demonstrating that the Farey step discrepancy does NOT show discrete peaks at zeta zero frequencies, and that the pair correlation structure is NOT Montgomery-like, is itself a useful result. It closes a speculative direction and clarifies the limits of what DeltaW can tell us about individual zeros.

---

## 8. RECOMMENDATIONS

1. **Do not claim pair correlation detection.** The data does not support it.

2. **Do not cite "Z-score 1625" without rerunning the computation with a proper null model** (phase-randomized surrogates, not permutation).

3. **The Mellin transform section, if included in the paper, should be framed as "formal computation"** with explicit caveats about unjustified interchange of limits.

4. **Focus the paper on what IS novel:** the DeltaW framework (N1), the Mertens connection (N2), the sign theorem, and the four-term decomposition. These stand on their own without needing to invoke pair correlation.

5. **If spectral properties are discussed,** report the f^{-1.67} slope and the r=0.915 Mertens correlation as empirical findings, with the honest assessment that they follow from the known explicit formula rather than revealing new structure.

---

## APPENDIX: NOTATION AND DEFINITIONS

- **F_N:** The Farey sequence of order N (all fractions a/b with 0 <= a/b <= 1 and 1 <= b <= N)
- **W(N):** L^2 Wasserstein discrepancy of F_N from the uniform distribution
- **DeltaW(N):** W(N) - W(N-1), the per-step change
- **M(x):** Mertens function, Sum_{n <= x} mu(n)
- **rho = 1/2 + i*gamma:** Nontrivial zero of the Riemann zeta function
- **P(s):** Prime zeta function, Sum_p p^{-s}
- **R(alpha):** Montgomery pair correlation function of zeta zeros
- **Lomb-Scargle:** Periodogram method for unevenly sampled data
- **GUE:** Gaussian Unitary Ensemble (random matrix theory)
