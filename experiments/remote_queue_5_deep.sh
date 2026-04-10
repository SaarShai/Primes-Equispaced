#!/bin/bash
OUT="$HOME/Desktop/Farey-Local/experiments"
LOG="$OUT/REMOTE_QUEUE_LOG.md"

run_remote() {
    local name="$1"; local prompt="$2"
    echo "$(date) Starting: $name [DEEP]" >> "$LOG"
    # Use 16K context for deep tasks
    echo "$prompt" | ssh new@192.168.1.218 "python3 -c \"
import sys, json, urllib.request
prompt = sys.stdin.read()
data = json.dumps({'model':'qwen3.5:35b','prompt':prompt,'stream':False,'options':{'num_ctx':16384}}).encode()
req = urllib.request.Request('http://localhost:11434/api/generate', data=data, headers={'Content-Type':'application/json'})
resp = json.loads(urllib.request.urlopen(req, timeout=1200).read())
print(resp.get('response','EMPTY'))
\"" > "$OUT/${name}.md" 2>&1
    echo "$(date) Done: $name ($(wc -c < "$OUT/${name}.md") bytes)" >> "$LOG"
}

echo "=== Remote Queue 5 DEEP THINKING $(date) ===" >> "$LOG"

# 1. DEEP: Full unconditional proof attempt for gamma_1 detection
run_remote "DEEP_UNCONDITIONAL_GAMMA1" "DEEP PROOF ATTEMPT (take your time, be thorough):

Prove WITHOUT GRH that the Mertens spectroscope F(gamma) = |sum_{p<=X} M(p)/p * exp(-igamma*log(p))|^2 has a local maximum within O(1/log(X)) of gamma_1 = 14.1347 for all sufficiently large X.

Available unconditional tools:
1. PNT: pi(x) ~ x/log(x)
2. Ingham (1942): M(x) changes sign infinitely often, and |M(x)| > x^{1/2-epsilon} infinitely often
3. Zero-free region: zeta(s) != 0 for Re(s) > 1 - c/log(|t|+2)
4. Vinogradov-Korobov: improved zero-free region
5. Explicit formula: M(x) = sum_rho x^rho/(rho*zeta'(rho)) - 2 + ... (valid unconditionally as an asymptotic, though the sum over zeros requires care)

Strategy: The explicit formula IS unconditional — it's an identity, not conditional on GRH. GRH only tells us WHERE the zeros are. But we don't need to know where gamma_1 is — we just need to show the spectroscope has a peak SOMEWHERE near a zero.

Approach: (1) The explicit formula gives M(x) = Re(sum_rho x^rho/(rho*zeta'(rho))) + error. (2) The DOMINANT term is from gamma_1 (the zero with smallest imaginary part). (3) The spectroscope at gamma=gamma_1 computes sum M(p)/p * p^{-igamma_1} which by the explicit formula includes c_1 * sum p^{-1} as the resonant term. (4) The sum p^{-1} diverges (Mertens theorem, unconditional). (5) Off-resonance sums are bounded using the zero-free region.

The key gap: step (5) — bounding off-resonance sums without assuming all zeros are on Re=1/2. With the classical zero-free region, zeros at Re(s) = sigma > 1/2 contribute terms p^{sigma-1} which could dominate p^{-1/2} for sigma close to 1. But the density of such zeros is controlled by zero-density estimates (Ingham, Huxley).

Can this approach work? Write the COMPLETE proof or identify exactly where it breaks."

# 2. DEEP: Derive the complete explicit formula for DeltaW(p)
run_remote "DEEP_DELTAW_EXPLICIT_FORMULA" "DEEP DERIVATION (thorough, all steps):

Derive the complete explicit formula connecting DeltaW(p) to Riemann zeta zeros.

Chain of identities:
1. DeltaW(p) = A - B - C - D (four-term decomposition, PROVED in Lean)
2. A = dilution = sum_old D^2 * (1/n^2 - 1/n'^2). This is O(1/p) and does NOT oscillate with zeros.
3. D = new-fraction discrepancy = (1/n'^2)*sum_new D_p(k/p)^2. By our D(1/p) result, D ~ 3/pi^2 * p. Does NOT oscillate.
4. C = shift-squared = (1/n'^2)*sum delta^2 ~ N^2/(2*pi^2*n'^2) ~ 1/(2*pi^2). Roughly constant.
5. B = cross-term = (2/n'^2)*sum D*delta. THIS is where the oscillation lives.

For B: the Bridge Identity gives sum e^{2pi*i*p*f} = M(p) + 2. The Compact Cross-Term Formula relates B to this sum. Therefore:

B(p) = f(M(p)) for some function f.

Since M(p) = sum_rho p^rho/(rho*zeta'(rho)) - 2, we get:

B(p) = f(sum_rho c_rho * p^{igamma_rho} * p^{1/2} - 2)

Derive f explicitly. What is the EXACT relationship between B and M(p)?

Then: DeltaW(p) = A - B - C - D where only B oscillates.
So: sgn(DeltaW(p)) ~ -sgn(B(p)) ~ -sgn(M(p)) ~ -sgn(cos(gamma_1*log(p) + phi))

This is the complete chain. Derive every step rigorously."

# 3. DEEP: Can we prove the GUE pair correlation result?
run_remote "DEEP_GUE_PROOF" "DEEP PROOF ATTEMPT:

Our spectroscope yields pair correlation RMSE=0.066 vs Wigner surmise from 20 detected zeros. Can this be PROVED to converge to GUE under suitable hypotheses?

The argument:
1. F(gamma) = |sum M(p)/p * exp(-igamma*log(p))|^2 is a periodogram.
2. By Wiener-Khinchin: F = |hat(f)|^2 = hat(f * f*), where f(x) = sum M(p)/p * delta(x - log(p)).
3. The autocorrelation f*f*(tau) = sum_{p,q} (M(p)/p)(M(q)/q) * delta(tau - log(p/q)).
4. Under the explicit formula: M(p)/p ~ sum_rho c_rho * p^{igamma_rho - 1/2}.
5. The autocorrelation becomes: sum_{rho,rho'} c_rho * conj(c_{rho'}) * sum_p p^{i(gamma_rho - gamma_{rho'}) - 1} * delta(tau - ...).
6. The diagonal terms (rho = rho') give the pair correlation.
7. Under Montgomery's conjecture: the pair correlation function is 1 - (sin(pi*x)/(pi*x))^2.

The gap: step 5→6 requires controlling cross terms, which needs pair correlation estimates for the zeros themselves. This is circular unless we can use our COMPUTATIONAL result to bootstrap.

Alternative: can we prove that ANY periodogram of a function satisfying the explicit formula must reproduce the pair correlation of its poles? This would be a general theorem about periodograms of meromorphic functions."

# 4. DEEP: Three-body problem — derive WHY nobility anticorrelates with entropy
run_remote "DEEP_3BP_NOBILITY_ENTROPY" "DEEP DERIVATION:

In our three-body periodic table, CF nobility (fraction of partial quotients = 1) anticorrelates with braid entropy at rho = -0.890 (partial correlation controlling for word length, p < 10^-50).

PROVE this relationship from first principles:

1. A three-body periodic orbit has a braid word w in the free group F_2 = <a,b>.
2. The braid word maps to a matrix M in SL(2,Z) via the standard isomorphism F_2 = Gamma(2).
3. The eigenvalue of M determines the CF via x^2 - tr(M)*x + 1 = 0.
4. Braid entropy = log(spectral radius of M) = log(lambda_max).
5. Nobility = fraction of 1s in the periodic CF of (1+sqrt(tr(M)^2-4))/(2).

The connection: tr(M) determines BOTH the entropy AND the CF.
- High entropy = large tr(M) = large eigenvalue = CF with large partial quotients = low nobility.
- Low entropy = small tr(M) = eigenvalue close to 1 = CF close to golden ratio [1,1,1,...] = high nobility.

This should follow from the monotonic relationship between tr(M) and the geometric mean of CF partial quotients. The golden ratio [1,1,1,...] has tr(M) = 3 (the minimum for hyperbolic elements), which gives the minimum entropy log(phi).

Derive the EXACT functional relationship: entropy = g(nobility) for some function g. Is it linear? Logarithmic?"

# 5. DEEP: Chowla test at larger scale — algorithm design
run_remote "DEEP_CHOWLA_ALGORITHM_10M" "DEEP ALGORITHM DESIGN:

Design an efficient algorithm for the Chowla spectroscopic test at N=10^7 (10 million).

Challenge: the naive spectroscope sum_{n=1}^N mu(n)/n * exp(-igamma*log(n)) requires N*G multiplications where G=15000 gamma grid points. At N=10^7: 1.5*10^11 operations. Too slow for a single sum.

Approaches:
1. SUBSAMPLE: Use only primes (pi(10^7) ~ 620K). Sum over primes only. Reduces to 620K * 15K = 9.3*10^9. Feasible in ~1 hour.
2. NFFT (Non-uniform FFT): The sum is a type-1 NUDFT. Libraries like FINUFFT compute this in O(N*log(N) + G*log(G)) = O(10^8). Feasible in seconds.
3. BLOCK DECOMPOSITION: Split [1,N] into blocks. Compute partial sums per block. Combine.
4. GPU: The sum is embarrassingly parallel. On an M1 Max GPU: ~10^12 FLOPS → 1.5*10^11 in ~0.15 seconds.

For each approach: (a) implementation complexity, (b) accuracy, (c) runtime estimate on M1 Max.

Also design: the normalization. We need |1/zeta(1+igamma)|^2 at higher precision for N=10^7. The Euler product to 1000 primes gives ~6 digits. Need: product to 10000 primes or direct zeta evaluation via mpmath."

echo "=== Remote Queue 5 complete $(date) ===" >> "$LOG"
