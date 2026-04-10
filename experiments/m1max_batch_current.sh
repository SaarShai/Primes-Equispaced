#!/bin/bash
OUT="$HOME/Desktop/Farey-Local/experiments"
LOG="$OUT/M1MAX_CONTINUOUS_LOG.md"

run() {
    local model="$1"; local name="$2"; local prompt="$3"
    echo "$(date) Starting: $name [$model]" >> "$LOG"
    if [ "$model" = "deepseek-r1:32b" ]; then
        ~/bin/remote_ollama_deepseek.sh "$name" "$prompt"
    else
        ~/bin/remote_ollama.sh "$model" "$name" "$prompt"
    fi
    echo "$(date) Done: $name ($(wc -c < "$OUT/${name}.md") bytes)" >> "$LOG"
}

echo "=== M1 Max Batch $(date) ===" >> "$LOG"

run "qwen3.5:35b" "M1_LIOUVILLE_COMPUTE_SPEC" "Design exact computation spec for Liouville spectroscope. Sieve lambda(n) to 500K. Compute L(p) = sum lambda(k) for k<=p at each prime. Weight: L(p)/p. Spectroscope F(gamma) = gamma^2 * |sum L(p)/p * exp(-igamma*log(p))|^2. Compare z-scores to Mertens at gamma_1..gamma_20. Predict advantage."

run "qwen3.5:35b" "M1_DEDEKIND_STRATIFIED_NUMERICAL" "Compute B stratified by denominator for p=13,19,31. For each q from 1 to p-1: B_q = sum_{a:gcd(a,q)=1} D(a/q)*delta(a/q). Report B_q for each q. Verify: are B_q positive for small q and dominant?"

run "deepseek-r1:32b" "M1_DS_UNIVERSALITY_MINIMUM" "We detect gamma_1 with only 2750 primes but theory says sum 1/p must diverge (requires astronomically many). Why the discrepancy? The theoretical bound is WORST-CASE over all subsets. Random/structured subsets are much better. Derive the EXPECTED detection threshold for random subsets of N primes from [2,X]. The key: random subsets have sum 1/p ~ N*mean(1/p) ~ N/(X/2) which diverges as N grows even for fixed X. So 2750 primes from [2,100K] gives sum 1/p ~ 2750*2/100000 ~ 0.055. This is tiny! Yet detection works. Something else must explain it. Think deeper."

run "qwen3.5:35b" "M1_PHASE_PHI_HIGHER_ZEROS" "Derive phases phi_k = -arg(rho_k*zeta'(rho_k)) for k=1..5. These control the multi-zero sign pattern of DeltaW(p). If we use a 5-term explicit formula: DeltaW(p) ~ sum_{k=1}^5 A_k*cos(gamma_k*log(p) + phi_k), how much does R improve from 0.77?"

run "qwen3.5:35b" "M1_3BP_TARGETED_SEARCH" "Design targeted search for 21 empty periodic table cells. For each cell: expected trace tr(M) from CF structure, expected period, initial condition constraints. Use variational methods vs random shooting."

run "qwen3.5:35b" "M1_SPECTROSCOPE_ERROR_ANALYSIS" "Rigorous error analysis: position error O(1/log X), systematic bias check, confidence intervals for detected zeros, false positive rate at z=3 with 20000 grid points."

echo "=== Batch complete $(date) ===" >> "$LOG"
