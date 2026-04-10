#!/bin/bash
OUT="$HOME/Desktop/Farey-Local/experiments"
LOG="$OUT/M1MAX_CONTINUOUS_LOG.md"

echo "=== PRIORITY: Variance Proof Batch $(date) ===" >> "$LOG"

# TOP PRIORITY: deepseek on the unconditional variance proof
echo "$(date) Starting: M1_DS_VARIANCE_PROOF [deepseek-stream]" >> "$LOG"
~/bin/remote_ollama_deepseek.sh "M1_DS_VARIANCE_PROOF" "PROVE THE FOLLOWING THEOREM UNCONDITIONALLY:

For any interval [A,B] with 0 < A < B containing at least one ordinate gamma_k of a nontrivial zero of zeta(s), there exist effective constants c_1, c_2 > 0 such that for all sufficiently large N:

integral_A^B F_N(gamma) dgamma > c_1 * (log N)^{c_2}

where F_N(gamma) = (1/N) * |sum_{p<=N} mu(p) * p^{-igamma}|^2, whereas under a zero-free model (no nontrivial zeros), integral_A^B F_N(gamma) dgamma = O(1).

PROOF STRATEGY:
1. The explicit formula M(x) = sum_rho x^rho/(rho*zeta'(rho)) - 2 + ... is an UNCONDITIONAL identity.
2. Substitute into F_N and expand the square. Get diagonal terms (rho=rho') and cross terms (rho != rho').
3. The diagonal contribution at zero rho_k is |c_k|^2 * |sum_{p<=N} p^{-1}|^2 ~ |c_k|^2 * (log log N)^2.
4. Integrate over [A,B]: the diagonal contributes sum_{gamma_k in [A,B]} |c_k|^2 * (log log N)^2.
5. The cross terms: use the LARGE SIEVE inequality (Montgomery-Vaughan) to bound sum_{rho != rho'} cross-products. The large sieve gives: sum |sum a_p p^{-irho}|^2 << (N + T^2) * sum |a_p|^2. This bounds the total power, and the cross terms are the difference between total and diagonal.
6. Show diagonal grows faster than cross terms as N -> infinity.
7. Under zero-free model: F_N is just noise, integral is O(1) from random phase cancellation.

Be thorough. Show ALL steps. Identify exactly where each unconditional tool is used. If a gap remains, state precisely what additional hypothesis would close it."
echo "$(date) Done: M1_DS_VARIANCE_PROOF ($(wc -c < "$OUT/M1_DS_VARIANCE_PROOF.md") bytes)" >> "$LOG"

# Also: tau spectroscope exploration
echo "$(date) Starting: M1_TAU_SPECTROSCOPE_EXPLORE [qwen3.5:35b]" >> "$LOG"
~/bin/remote_ollama.sh qwen3.5:35b "M1_TAU_SPECTROSCOPE_EXPLORE" "Design and analyze the Ramanujan tau spectroscope in detail. tau(n) from Delta(z) = q*prod(1-q^n)^24. First zeros of L(s,Delta) at gamma = 9.22, 13.91, 17.44, 19.65, 22.33. Weight: T(p)/p^{13/2} where T(p) = sum_{k<=p} tau(k). The tau spectroscope detects DIFFERENT zeros than Mertens. Significance: first spectroscopic detection of modular form zeros. Connection to Sato-Tate distribution. What alpha compensation? Since critical line is Re(s)=6 (unnormalized) or Re(s)=1/2 (normalized), the coefficient decay is similar to Mertens. Predict z-scores."
echo "$(date) Done: M1_TAU_SPECTROSCOPE_EXPLORE ($(wc -c < "$OUT/M1_TAU_SPECTROSCOPE_EXPLORE.md") bytes)" >> "$LOG"

# Elliptic curve spectroscope — new direction
echo "$(date) Starting: M1_ELLIPTIC_CURVE_SPECTROSCOPE [qwen3.5:35b]" >> "$LOG"
~/bin/remote_ollama.sh qwen3.5:35b "M1_ELLIPTIC_CURVE_SPECTROSCOPE" "Design a spectroscope for an elliptic curve L-function. Take the simplest curve: E: y^2 = x^3 - x (conductor 32). Its a_p values are available from LMFDB. The L-function L(s,E) has zeros on Re(s)=1 (by modularity). First zeros at gamma = 6.87, 9.72, 12.27. Build: F_E(gamma) = gamma^2 * |sum A_E(p)/p * exp(-igamma*log(p))|^2 where A_E(p) = sum_{k<=p} a_k(E). If this detects L(s,E) zeros, it connects our spectroscope to the Birch-Swinnerton-Dyer conjecture. What would detection mean? How many primes needed?"
echo "$(date) Done: M1_ELLIPTIC_CURVE_SPECTROSCOPE ($(wc -c < "$OUT/M1_ELLIPTIC_CURVE_SPECTROSCOPE.md") bytes)" >> "$LOG"

# GUE regularization retry with deepseek streaming
echo "$(date) Starting: M1_DS_GUE_REGULARIZATION [deepseek-stream]" >> "$LOG"
~/bin/remote_ollama_deepseek.sh "M1_DS_GUE_REGULARIZATION" "Fix the Wiener-Khinchin gap in the GUE proof. Our signal f(x) = sum M(p)/p * delta(x-log(p)) is a distribution, not L^2. REGULARIZE with Gaussian phi_eps of width eps. f_eps is in L^2, W-K applies. Key steps: (1) |hat(f_eps)|^2 converges to our spectroscope as eps->0. (2) The autocorrelation of f_eps involves pairs (p,q) with log(p/q) small. (3) For p=q (diagonal): contributes to the pair correlation at spacing 0. (4) For p close to q: contributes to pair correlation at small spacings (level repulsion). (5) Connect to Montgomery via the explicit formula for the pair sum. Derive the limit."
echo "$(date) Done: M1_DS_GUE_REGULARIZATION ($(wc -c < "$OUT/M1_DS_GUE_REGULARIZATION.md") bytes)" >> "$LOG"

echo "=== Batch complete $(date) ===" >> "$LOG"
