#!/bin/bash
OLLAMA="http://localhost:11435/api/generate"
OUT="$HOME/Desktop/Farey-Local/experiments"

run_35b() {
    local name="$1"; local prompt="$2"
    echo "$(date) Starting: $name" >> "$OUT/OVERNIGHT_CHAIN_LOG.md"
    curl -s "$OLLAMA" -d "{\"model\":\"qwen3.5:35b\",\"prompt\":\"$prompt\",\"stream\":false,\"options\":{\"num_ctx\":8192}}" 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('response','EMPTY'))" > "$OUT/${name}.md" 2>&1
    echo "$(date) Finished: $name ($(wc -c < "$OUT/${name}.md") bytes)" >> "$OUT/OVERNIGHT_CHAIN_LOG.md"
}

echo "=== Phase 3 chain started $(date) ===" >> "$OUT/OVERNIGHT_CHAIN_LOG.md"

# 1. Amplitude convergence with N (test cross-zero interference shrinks)
run_35b "AMPLITUDE_CONVERGENCE_PROOF" "PROOF TASK: The Mertens spectroscope peak height at gamma_j is F(gamma_j) = |c_j*W(0) + sum_{k!=j} c_k*W(gamma_j-gamma_k)|^2 where W(delta) = sum_p (1/p)*exp(-i*delta*log(p)) is the window function. As N (number of primes) grows, W(delta) for delta!=0 shrinks relative to W(0) because cross-terms cancel (by PNT, sum p^{i*alpha} / p ~ log(zeta(1+i*alpha)) is bounded). Therefore the interference terms vanish and F(gamma_j) -> |c_j|^2 * |W(0)|^2. Prove: for fixed j, lim_{N->inf} F(gamma_j) / (|c_j|^2 * N^2) = 1. Show the rate of convergence. Is it O(1/log(N))?"

# 2. Background O(N^{3/2}) proof
run_35b "BACKGROUND_GROWTH_PROOF" "PROOF TASK: The Mertens spectroscope background (at non-zero gamma away from all zeros) is B(gamma) = |sum_p M(p)/p * exp(-igamma*log(p))|^2. Claim: B grows as O(N^{3/2}) not O(N), because M(p) ~ sqrt(p) (non-stationary). Prove this. The key: M(p)/p ~ 1/sqrt(p), and sum of 1/sqrt(p) over primes to X diverges as ~2*sqrt(X)/log(X) ~ 2*sqrt(N*log(N)). So the DC component is O(sqrt(N)). For the AC component at nonzero gamma, partial summation gives |sum (M(p)/p)*p^{igamma}| = |sum 1/sqrt(p) * (oscillation) * p^{igamma}|. By Cauchy-Schwarz: |sum|^2 <= (sum 1/p) * (sum M(p)^2/p) ~ log(log(N)) * N. So B = O(N*log(log(N))). Reconcile with the empirical O(N^{3/2}) observation."

# 3. Local z monotonic analytical proof
run_35b "LOCAL_Z_ANALYTICAL_PROOF" "PROOF: The local z-score of the Mertens spectroscope at gamma_1 is z_local = (F(gamma_1) - mu_local) / sigma_local where mu_local and sigma_local are computed from F(gamma) in a window around gamma_1 excluding the peak. Prove z_local grows monotonically with N. Signal: F(gamma_1) ~ |c_1|^2 * N^2 (sum 1 over N primes, squared). Local mean: mu ~ N * C for some constant C (background from cross-terms). Local std: sigma ~ sqrt(N) * D. Therefore z_local ~ (|c_1|^2*N^2 - C*N) / (D*sqrt(N)) ~ |c_1|^2*N^{3/2}/D as N grows. This gives z_local ~ O(N^{3/2}), growing unboundedly. But empirically z grows much slower. The gap is that sigma_local also grows faster than sqrt(N). Resolve."

# 4. Psi vs Mertens analytical comparison
run_35b "PSI_VS_MERTENS_PROOF" "PROOF: The psi spectroscope uses psi(p)-p as weight. The explicit formula gives psi(x)-x ~ -sum_rho x^rho/rho. So the coefficient at zero rho_k is c_k^{psi} = 1/rho_k. For Mertens: M(x) ~ -1 + sum_rho x^rho/(rho*zeta'(rho)), so c_k^{M} = 1/(rho_k*zeta'(rho_k)). The ratio is |c_k^{psi}/c_k^{M}| = |zeta'(rho_k)|. Since |zeta'(rho_k)| varies (not monotone), the psi spectroscope has MORE UNIFORM peak heights across zeros, while Mertens has heights modulated by 1/|zeta'|^2. This explains why psi is better for higher zeros where |zeta'| is larger. Formalize this argument. Is psi provably better in the limit?"

# 5. F(gamma) probes pair correlation — verification
run_35b "PAIR_CORRELATION_VERIFICATION" "VERIFY: The spectroscope F(gamma) = |sum w(p) p^{-igamma}|^2 = sum_{p,q} w(p)*w(q)*(p/q)^{igamma} / (pq). This is a DOUBLE SUM over prime pairs (p,q). The Fourier transform of F(gamma) is the autocorrelation of the prime weight function. By the Wiener-Khinchin theorem, |hat(f)|^2 = hat(f*f_bar). So F encodes the pair structure of primes. Now, the explicit formula says the pair structure is controlled by zero PAIRS (rho_j, rho_k). So F(gamma) has peaks at gamma_j AND oscillations at gamma_j - gamma_k. This is exactly Montgomery's pair correlation. Verify: is F(gamma) literally the Montgomery function, or just analogous? Give the precise mathematical relationship."

echo "=== Phase 3 chain complete $(date) ===" >> "$OUT/OVERNIGHT_CHAIN_LOG.md"
