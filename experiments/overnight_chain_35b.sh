#!/bin/bash
# Chain of qwen3.5:35b tasks — runs sequentially for ~3 hours
# Each task gets 8192 context, stream=false

OLLAMA="http://localhost:11435/api/generate"
OUT="$HOME/Desktop/Farey-Local/experiments"

run_task() {
    local name="$1"; local prompt="$2"
    echo "$(date) Starting: $name" >> "$OUT/OVERNIGHT_CHAIN_LOG.md"
    curl -s "$OLLAMA" -d "{\"model\":\"qwen3.5:35b\",\"prompt\":\"$prompt\",\"stream\":false,\"options\":{\"num_ctx\":8192}}" 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('response','EMPTY'))" > "$OUT/${name}.md" 2>&1
    echo "$(date) Finished: $name ($(wc -c < "$OUT/${name}.md") bytes)" >> "$OUT/OVERNIGHT_CHAIN_LOG.md"
}

echo "=== Chain started $(date) ===" > "$OUT/OVERNIGHT_CHAIN_LOG.md"

# Task 1: Why does amplitude anti-correlate?
run_task "WHY_AMPLITUDE_ANTICORRELATES" "The Mertens spectroscope peak heights F(gamma_k) anti-correlate with the explicit formula prediction |c_k|^2 = 1/|rho_k * zeta_prime(rho_k)|^2. Pearson r=-0.44, consecutive ratio r=-0.59. Why? Three hypotheses: (1) Interference between nearby zeros distorts individual peak heights. (2) The periodogram mixes contributions from multiple zero pairs. (3) The effective coefficient in the periodogram is not c_k but involves a sum over zero interactions. Analyze which hypothesis is most likely. Can you derive the correct peak height formula that accounts for cross-zero interference? The peak at gamma_j should be |c_j + sum_{k!=j} c_k * sinc-like(gamma_j - gamma_k)|^2, not just |c_j|^2."

# Task 2: Background growth analysis
run_task "BACKGROUND_GROWTH_ANALYSIS" "The Mertens spectroscope F_comp(gamma) = gamma^2 * |sum M(p)/p * exp(-igamma*log(p))|^2 has local z-scores that decrease at larger N (from z=23.5 at 10M primes to z=12.1 at 50M). The peak heights grow as expected (O(N^2)) but the background grows FASTER than expected. Why? The background at non-zero gamma values is |sum M(p)/p * exp(-igamma*log(p))|^2. Under GRH this should be O(N) from random-walk cancellation. But empirically it grows faster. Hypothesis: the background contains contributions from HIGHER zeta zeros (gamma_21, gamma_22, ...) that become resolved at larger N, filling in the spectrum. If true, the background at gamma=40 (between gamma_7 and gamma_8) should be lower than at gamma=55 (between gamma_11 and gamma_12) where zeros are denser. Can you analyze this?"

# Task 3: Can we detect zeros beyond gamma_20?
run_task "DETECT_BEYOND_20_ZEROS" "The compensated Mertens spectroscope with 1M primes detects all 20 of the first 20 zeta zeros. Can it detect zeros beyond gamma_20=77.14? The next zeros are: gamma_21=79.34, gamma_22=82.91, gamma_23=84.74, gamma_24=87.43. We compute F_comp on gamma in [5,95] with 30000 points. The question: does the local z-score remain above 2 for gamma_21-gamma_24? Predict based on: (a) the c_k coefficient decay, (b) the resolution limit 2pi/log(p_max), (c) the observed local z-score trend from gamma_1 to gamma_20. Give a quantitative prediction."

# Task 4: Optimal gamma exponent (is gamma^2 really optimal?)
run_task "OPTIMAL_GAMMA_EXPONENT" "We multiply the spectroscope by gamma^2 to compensate for |c_k|^2 ~ 1/gamma_k^2 decay. But |c_k|^2 = 1/|rho_k * zeta_prime(rho_k)|^2 where |rho_k| ~ gamma_k and |zeta_prime(rho_k)| varies. Perhaps gamma^2 is not optimal. Consider: (a) gamma^alpha for alpha = 1.5, 1.8, 2.0, 2.2, 2.5 — which gives best average detection? (b) gamma^2 * log(gamma) to account for zeta_prime growth? (c) An adaptive compensation: multiply by the PREDICTED |c_k|^2 envelope (requires knowing approximate zeta_prime values). Derive the optimal exponent theoretically and predict which alpha maximizes the average z-score across 20 zeros."

# Task 5: Twin prime spectroscope
run_task "TWIN_PRIME_SPECTROSCOPE" "Can we build a spectroscope for twin primes? Instead of sum M(p)/p * exp(-igamma*log(p)), consider sum_{p: p and p+2 both prime} w(p) * exp(-igamma*log(p)). What frequencies would this detect? By the Hardy-Littlewood twin prime conjecture, the twin prime counting function Pi_2(x) ~ 2*C_2 * x/log(x)^2 where C_2 is the twin prime constant. Does this have an explicit formula involving zeta zeros? If so, a twin-prime spectroscope should detect zeros with different coefficients. Assess feasibility."

# Task 6: Prove local z-score improves monotonically
run_task "LOCAL_Z_MONOTONIC_PROOF" "We observe that the local z-score of the Mertens spectroscope at gamma_1 improves from 2.6 (100K primes) to 7.9 (5M primes). Under GRH, prove that the local z-score grows as O(sqrt(N)) where N is the number of primes. The local z-score is z = (peak_height - local_mean) / local_std where local statistics are computed in a window around the peak excluding known-zero regions. Peak height ~ |c_1|^2 * N^2. Local mean ~ background ~ O(N). Local std ~ O(sqrt(N)). Therefore z ~ N^2 / (N + sqrt(N)) ~ N. Wait, that gives z~N not sqrt(N). Resolve this."

echo "=== Chain complete $(date) ===" >> "$OUT/OVERNIGHT_CHAIN_LOG.md"
