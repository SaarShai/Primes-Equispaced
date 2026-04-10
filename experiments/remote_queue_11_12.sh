#!/bin/bash
OUT="$HOME/Desktop/Farey-Local/experiments"
LOG="$OUT/REMOTE_QUEUE_LOG.md"

run_35b() {
    local name="$1"; local prompt="$2"
    echo "$(date) Starting: $name [35b]" >> "$LOG"
    ~/bin/remote_ollama.sh qwen3.5:35b "$name" "$prompt"
    echo "$(date) Done: $name ($(wc -c < "$OUT/${name}.md") bytes)" >> "$LOG"
}

run_ds() {
    local name="$1"; local prompt="$2"
    echo "$(date) Starting: $name [deepseek-stream]" >> "$LOG"
    ~/bin/remote_ollama_deepseek.sh "$name" "$prompt"
    echo "$(date) Done: $name ($(wc -c < "$OUT/${name}.md") bytes)" >> "$LOG"
}

echo "=== Remote Q11-12 $(date) ===" >> "$LOG"

# Q11: proofs + exploration (deepseek for proofs, 35b for research)
run_ds "Q11_UNIVERSALITY_PARTIAL_UNCONDITIONAL" "We want to prove SOMETHING unconditional about the spectroscope. Even if we can't prove peak detection unconditionally, can we prove: (1) The spectroscope power at gamma_1 tends to infinity as X->infinity? This is weaker than peak detection but still meaningful. By Ingham: |M(x)| > x^{1/2-eps} infinitely often. So |sum M(p)/p * p^{-igamma_1}| should grow. But we need to show the growth is at gamma_1 specifically, not at some other frequency. (2) Alternative: prove the spectroscope is NOT flat — it has at least one peak above the mean. This follows from the variance being larger than expected for white noise. Derive the variance of F(gamma) under independence assumption vs under the explicit formula."

run_35b "Q11_LIOUVILLE_COMPUTATION_PLAN" "Plan the Liouville spectroscope computation. We need lambda(n) for n to 500K. lambda(n) = (-1)^Omega(n) where Omega counts prime factors with multiplicity. Sieve: for each prime p, for each multiple mp: Omega(mp) += 1. Then lambda(n) = (-1)^Omega(n). L(n) = cumulative sum. Spectroscope: F(gamma) = gamma^2 * |sum L(p)/p * exp(-igamma*log(p))|^2. Advantage over Mertens: coefficient is zeta(2*rho)/(rho*zeta'(rho)) with |zeta(2*rho)| = O(log(gamma)). Predict: what z-scores should we expect compared to our Mertens results? If Mertens gives z=65 at gamma_1, Liouville should give z ~ 65 * log(14.13) ~ 65 * 2.6 ~ 170. Is this right?"

run_ds "Q11_DEDEKIND_INTEGRAL_NUMERICAL" "Compute the Dedekind ergodic integral numerically. For p=13: (1) Build F_12 (Farey sequence of order 12). List all fractions a/b with 0<=a<=b<=12, gcd(a,b)=1, sorted. (2) n = |F_12|. (3) For each fraction f_j = a/b in F_12: D(f_j) = j - n*f_j (rank discrepancy, zero-based). delta(f_j) = a/b - frac(13*a/b) where frac is fractional part. (4) Compute B_raw = sum_{j} D(f_j) * delta(f_j). (5) Is B_raw positive? (6) Repeat for p=19 (build F_18), p=31 (build F_30). Report the values. This is the key test: if B_raw > 0 for all tested p, the ergodic argument has strong support."

run_35b "Q11_3BP_PREDICTION_STRATEGY" "Our three-body periodic table has 21 empty cells where orbits are predicted but not found. 4199 random N-body searches failed. What TARGETED search strategy would work better? (1) The empty cells have specific CF properties — use these to compute the expected matrix M, then the expected eigenvalue, then the expected period. Search near that period. (2) Use variational methods instead of random initial conditions — find orbits as minimizers of the action functional. (3) Use Lin-Zhu symmetry classification to reduce the search space. (4) Use our Lean-verified injection principle to constrain possible orbit topologies. Design the optimal search strategy."

run_35b "Q11_SPECTROSCOPE_SENSITIVITY_LIMITS" "What are the fundamental limits of the Mertens spectroscope? (1) Resolution: 2pi/log(X). At X=10^6: 0.46. At X=10^9: 0.33. At X=10^12: 0.25. (2) Detection limit: how WEAK can a zero be and still be detected? The z-score scales as |c_k|^2 * N^2 / background. The weakest zeros have |c_k|^2 ~ 1/(gamma_k^2 * |zeta'(rho_k)|^2). For gamma_k ~ 100: |c_k|^2 ~ 10^{-6}. With N=78K: z ~ 10^{-6} * 6*10^9 / 10^4 ~ 600. Still huge! So the spectroscope should detect zeros well beyond gamma_100. Why then do we only detect 20? Because the BACKGROUND at high gamma is not flat — it has structure from many overlapping zero contributions."

run_ds "Q11_GUE_REGULARIZATION_PROOF" "Fix the Wiener-Khinchin gap in the GUE proof. Our signal is f(x) = sum M(p)/p * delta(x - log(p)) which is a distribution, not L^2. REGULARIZE: replace delta by Gaussian phi_eps of width eps. Then f_eps is in L^2 and W-K applies. The periodogram |hat(f_eps)|^2 = hat(autocorrelation of f_eps). As eps->0: hat(f_eps)(gamma) -> sum M(p)/p * exp(-igamma*log(p)) * exp(-eps^2*gamma^2/2). The Gaussian damping factor exp(-eps^2*gamma^2/2) -> 1 pointwise. So the periodogram converges. The autocorrelation of f_eps involves sum_{p,q} M(p)M(q)/(pq) * phi_{sqrt(2)*eps}(log(p/q)). For p=q (diagonal): this gives sum M(p)^2/p^2 * phi_0(0). For p!=q: phi_{sqrt(2)*eps}(log(p/q)) selects pairs with p/q close to 1. These encode the pair correlation. DERIVE the limit as eps->0 and connect to Montgomery."

echo "=== Remote Q11-12 complete $(date) ===" >> "$LOG"
