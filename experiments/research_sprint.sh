#!/bin/bash
OLLAMA="http://localhost:11434/api/generate"
OUT="$HOME/Desktop/Farey-Local/experiments"
LOG="$OUT/RESEARCH_SPRINT_LOG.md"

run35b() {
    local name="$1"; local prompt="$2"
    echo "$(date) Starting: $name" >> "$LOG"
    curl -s "$OLLAMA" -d "{\"model\":\"qwen3.5:35b\",\"prompt\":\"$prompt\",\"stream\":false,\"options\":{\"num_ctx\":8192}}" 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('response','EMPTY'))" > "$OUT/${name}.md" 2>&1
    echo "$(date) Done: $name ($(wc -c < "$OUT/${name}.md") bytes)" >> "$LOG"
}

run_code() {
    local name="$1"; local prompt="$2"
    echo "$(date) Starting code: $name" >> "$LOG"
    ~/bin/local_code_agent.sh qwen3.5:35b "$name" "$prompt"
    echo "$(date) Done code: $name" >> "$LOG"
}

echo "=== Research Sprint $(date) ===" > "$LOG"

# 1. UNIVERSALITY: creative approaches to remove GRH
run35b "UNIVERSALITY_UNCONDITIONAL_V1" "The universality theorem currently requires GRH+LI+regularity. Can we prove ANY version unconditionally? Creative approaches: (1) Instead of the explicit formula (needs GRH), use Selberg's unconditional result that a positive proportion of zeros lie on the critical line. This gives weaker but unconditional signal. (2) Use the prime number theorem in arithmetic progressions (unconditional) instead of the explicit formula. (3) Use Bombieri-Vinogradov theorem (unconditional on average over characters). (4) Prove a WEAKER statement: not that ALL zeros are detected, but that AT LEAST ONE zero is detected (gamma_1). This might be provable from just PNT. (5) Use Ingham's theorem: M(x) changes sign infinitely often. This forces the spectroscope to have a peak SOMEWHERE near gamma_1. Formalize the most promising approach."

# 2. GUE PAIR CORRELATION: analytical proof attempt
run35b "GUE_PAIR_CORRELATION_PROOF" "Can we prove that the Farey spectroscope pair correlation matches GUE? The spectroscope F(gamma) = |sum M(p)/p * exp(-igamma*log(p))|^2 is a periodogram. By Wiener-Khinchin, |hat(f)|^2 = hat(f * f_bar), so F encodes the autocorrelation of M(p)/p at primes. Under GRH: M(p)/p ~ sum_rho p^{rho-1}/(rho*zeta'(rho)). The autocorrelation involves sum_{rho,rho'} terms, which are exactly the zero pair statistics. Montgomery's conjecture: the pair correlation function R_2(alpha) ~ 1 - (sin(pi*alpha)/(pi*alpha))^2. If our spectroscope's autocorrelation reproduces this, it's because the explicit formula transmits the zero pair statistics into the M(p) data. Can we derive this connection rigorously? Even a conditional (GRH+LI) proof connecting F's autocorrelation to R_2 would be significant."

# 3. CHOWLA/SARNAK: top priority
run35b "CHOWLA_SARNAK_ATTACK" "TOP PRIORITY: The Chowla conjecture states that mu(n) has no correlations: sum_{n<=N} mu(n)*mu(n+h) = o(N) for all h>=1. Sarnak's conjecture: mu(n) is disjoint from all deterministic sequences. Our pre-whitening spectroscope detects structure in mu(n) partial sums (the Mertens function). Could we use the spectroscope to test Chowla/Sarnak computationally? Approach: (1) Compute the spectroscope of mu(n) directly (not M(p) at primes, but mu(n) for all n). (2) Under Chowla, the spectroscope should show peaks ONLY at zeta zeros (the deterministic component) and NO other structure. (3) If we see additional peaks, that would be computational evidence AGAINST Chowla. (4) The pre-whitening removes the zeta-zero contribution. What remains should be 'random' under Chowla. Test: is the pre-whitened mu(n) spectroscope flat? Or does it have structure? Design the computation."

# 4. CHOWLA: computational test
run_code "CHOWLA_SARNAK_COMPUTATIONAL" "Test the Chowla conjecture computationally using our spectroscope. (1) Compute mu(n) for n=1 to 100000 using a sieve. (2) Compute the spectroscope F(gamma) = |sum_{n=1}^N mu(n)/n * exp(-igamma*log(n))|^2 on gamma in [5, 80], 20000 points. This sums over ALL integers, not just primes. (3) Apply gamma^2 compensation. (4) Find peaks. They should be at zeta zeros (the deterministic part of mu). (5) Now PRE-WHITEN: divide F by the expected peak envelope (gamma^{-2} from explicit formula). The residual should be FLAT under Chowla. (6) Is the residual flat? Or does it have additional structure? Compute the chi-squared statistic of the residual against a flat spectrum. Print results."

# 5. PHASE PHI: compute exact
run_code "PHASE_PHI_EXACT_COMPUTE" "Compute the exact phase constant phi in the Chebyshev sign pattern. We observe sgn(DeltaW(p)) ~ -sgn(cos(gamma_1*log(p) + phi)) with phi~5.28. From the explicit formula: phi = -arg(rho_1 * zeta'(rho_1)). Compute using mpmath at 50 digits precision: (1) from mpmath import mp, zetaderiv; mp.dps=50. (2) rho1 = 0.5 + 14.134725141734693j. (3) zp = zetaderiv(1, rho1) — this is zeta'(rho_1). (4) c1 = 1/(rho1 * zp). (5) phi_predicted = -float(mp.arg(rho1 * zp)). (6) Print: phi_predicted, and compare to observed phi=5.28. (7) Also compute |c1| and the predicted leading oscillation amplitude. If mpmath zetaderiv not available, try: from mpmath import zeta; zp = (zeta(rho1+1e-10) - zeta(rho1-1e-10)) / 2e-10."

# 6. 30+ ZEROS: extend spectroscope
run_code "EXTEND_30_ZEROS_10M" "Extend the compensated Mertens spectroscope to detect 30 zeros using 10M primes. (1) Sieve Mobius to 10000000 (~664K primes). (2) Compute F_comp(gamma) = gamma^2 * |sum M(p)/p * exp(-igamma*log(p))|^2 on [5, 120], 30000 points. Use chunked computation (chunk primes into blocks of 100000). (3) Known zeros gamma_1..gamma_30: [14.1347, 21.0220, 25.0109, 30.4249, 32.9351, 37.5862, 40.9187, 43.3271, 48.0052, 49.7738, 52.9703, 56.4462, 59.3470, 60.8318, 65.1125, 67.0798, 69.5464, 72.0672, 75.7047, 77.1448, 79.3374, 82.9104, 84.7355, 87.4253, 88.8091, 92.4919, 94.6514, 95.8706, 98.8312, 101.318]. (4) For each: compute local z-score. (5) Report: how many of 30 detected at z>3? Print table."

# 7. MONTGOMERY: more zeros for stronger test
run_code "MONTGOMERY_30_ZEROS" "Compute pair correlation from 30 detected zeros. (1) Use the 30-zero spectroscope data (if EXTEND_30_ZEROS_10M ran, use those results; otherwise sieve to 5M and compute). (2) From detected zero positions: compute all C(30,2)=435 pairwise differences. (3) Normalize: alpha = (gamma_j - gamma_k) * log(gamma_mean) / (2*pi). (4) Histogram of alpha vs Montgomery's 1 - (sin(pi*alpha)/(pi*alpha))^2. (5) Compute RMSE in range alpha in [0,4]. (6) Also compute nearest-neighbor spacing and compare to Wigner surmise. (7) Compare: RMSE with 20 zeros (190 pairs) vs 30 zeros (435 pairs). Does more data improve the Montgomery match?"

# 8. THREE-BODY: spectroscope for orbit periods
run_code "THREEBODY_SPECTROSCOPE" "Test whether the Farey spectroscope can detect three-body orbit periods. (1) Load orbit data from ~/Desktop/Farey-Local/experiments/threebody_full_data.json. This contains 695 orbits with periods, braid words, and CF invariants. (2) Extract the periods T_k for all orbits. (3) Compute a 'period spectroscope': F(omega) = |sum_{k=1}^{695} w_k * exp(-i*omega*log(T_k))|^2 where w_k = 1/T_k (or try nobility as weight). (4) Does this show peaks at any meaningful frequencies? (5) The three-body problem has no explicit formula analogue, so this is speculative. But the STRUCTURE of the period distribution might have hidden frequencies from the underlying symmetry group. (6) Also try: spectroscope of the CF partial quotients. Do they cluster in Farey-like patterns?"

# 9. THREE-BODY: verify periodic table
run_code "THREEBODY_VERIFY_TABLE" "Verify the three-body periodic table structure. (1) Load ~/Desktop/Farey-Local/experiments/threebody_periodic_table.json. (2) Recreate the 9x8 grid: x-axis = CF period length, y-axis = geometric mean of partial quotients. (3) Count: populated cells, empty cells, orbits per cell. (4) For each populated cell: what percentage of orbits belong to the same topological family? (reported as 69% in the paper). (5) Verify: are the 21 empty cells genuine predictions or artifacts of binning? (6) Sanity check: do nearby cells in the table have similar physical properties (period, energy, stability)?"

# 10. DEDEKIND: fresh approach
run35b "DEDEKIND_FRESH_APPROACH" "The Dedekind sum gap: prove B = (2/n'^2)*sum D(f)*delta(f) > 0 for primes with M(p)<=-3. All previous approaches failed: (A) Per-denominator bounds (Weil) — individual R_b can be < -1/2. (B) Cauchy-Schwarz — too loose by 16x. (C) Kernel decomposition — K_2..K_9 positive but doesn't close. FRESH IDEAS: (1) Probabilistic: show B>0 holds for 'most' primes unconditionally. Even proving B>0 for a positive density of primes would be new. (2) Ergodic: the map f -> {pf} is ergodic on [0,1]. The sum D*delta is a Birkhoff average. Ergodic theorem says it converges to the integral of D*delta over the invariant measure. Compute: is this integral positive? (3) Large sieve: the large sieve inequality bounds sum of |sum a_n e^{2pi*i*n*alpha}|^2 over many alpha. Can we use this to bound sum D*delta? (4) Pretentious number theory: use the theory of multiplicative functions (Granville-Soundararajan) to analyze the oscillation pattern of delta(f)."

echo "=== Sprint complete $(date) ===" >> "$LOG"
