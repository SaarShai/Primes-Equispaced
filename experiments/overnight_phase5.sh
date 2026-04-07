#!/bin/bash
OLLAMA="http://localhost:11434/api/generate"
OUT="$HOME/Desktop/Farey-Local/experiments"
LOG="$OUT/OVERNIGHT_PHASE5_LOG.md"

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

echo "=== Phase 5: Full throttle $(date) ===" > "$LOG"

# ===== PAPER 2 HIGHEST PRIORITY =====

run35b "PAPER2_SECTION1_INTRODUCTION" "Write Section 1 (Introduction) for Paper 2: The Compensated Mertens Spectroscope. 800-1000 words. Structure: (1) The classical Fourier duality between primes and zeta zeros (cite Csoka 2015, Van der Pol 1947, Planat). (2) What is new: the specific application of frequency compensation (pre-whitening) to the Mertens periodogram, the local z-score normalization, the universality observation, and the connection from Farey per-step discrepancy. (3) Main results summary: 20/20 zeros with local z-scores, GUE RMSE=0.066, 108 L-function characters, Siegel zero sensitivity 465M sigma, universality with 2750 primes. (4) Paper organization. Write in LaTeX-ready mathematical prose. Be honest: pre-whitening is classical, our contribution is the specific application and the quantitative analysis."

run35b "PAPER2_SECTION2_CONSTRUCTION" "Write Section 2 (Mathematical Construction) for Paper 2. Define: (1) Mertens spectroscope F(gamma) = |sum M(p)/p * exp(-igamma*log(p))|^2. (2) The compensated version F_comp = gamma^alpha * F. (3) Local z-score: z_local = (peak - local_mean) / local_std. (4) Explain why peaks appear at zeta zeros via the explicit formula M(x) = sum_rho x^rho/(rho*zeta'(rho)). (5) Derive the compensation: |c_k|^2 ~ 1/gamma_k^2, so gamma^2 flattens. (6) Note: this is pre-whitening applied to the specific noise structure of Mertens data. Give all formulas in LaTeX."

run35b "PAPER2_SECTION3_DETECTION" "Write Section 3 (Zero Detection Performance) for Paper 2. Present: (1) Global z-score results at 100K, 500K, 1M primes. (2) The 'peaking at 1M' artifact from global normalization. (3) Local z-score resolves the artifact: 20/20 at all scales. (4) Table: per-zero detection with local z at 1M (gamma_1 z=65.4 down to gamma_20 z=4.8). (5) Comparison: raw (2/20) vs compensated (20/20). (6) Scaling to 10M, 25M, 50M. (7) Optimal exponent: alpha=0.3 minimax, alpha=1.8 average. (8) The null battery: 5/6 tests pass, z=117.6."

run35b "PAPER2_SECTION4_GUE" "Write Section 4 (Spectral Statistics and GUE) for Paper 2. Present: (1) 20 detected zeros give 190 pairwise differences. (2) Nearest-neighbor spacing distribution: RMSE=0.066 vs Wigner surmise. (3) Level repulsion clearly visible. (4) Montgomery pair correlation comparison. (5) Autocorrelation detects zero-difference lags. (6) Connection: F(gamma) is a periodogram, which probes pair correlation via Wiener-Khinchin. (7) This is random matrix statistics derived from arithmetic data."

run35b "PAPER2_SECTION5_UNIVERSALITY" "Write Section 5 (Universality) for Paper 2. Present: (1) Any subset of 2750+ primes detects all zeros. (2) Tested: random subsets, residue classes, twin primes, positive M(p), negative M(p). (3) |M(p)|/sqrt(p) collapses: signed oscillation carries the signal. (4) Interval-restricted subsets (only large primes) fail: need range spanning small primes. (5) Connection to explicit formula: each prime carries all zero frequencies. (6) Twin prime spectroscope: same zeros, 2-6% amplitude (Hardy-Littlewood). (7) Literature check: this observation appears novel."

run35b "PAPER2_SECTION6_LFUNCTIONS" "Write Section 6 (Extension to L-Functions) for Paper 2. Present: (1) Twisted spectroscope F_chi for Dirichlet characters. (2) 108 characters mod q<=20 all show peaks. (3) log(p) reweighting beats gamma^2 for L-functions (+11%). (4) Siegel zero sensitivity: 465M sigma at beta=0.99. (5) No Siegel zeros detected for q<=50. (6) GRH verification pipeline: 3/5 direct matches at 500K primes. (7) Combined spectroscope detects Dedekind zeta zeros of Q(i)."

run35b "PAPER2_SECTION7_HONEST_NEGATIVES" "Write Section 7 (Limitations and Open Problems) for Paper 2. Honestly present: (1) Amplitude anti-correlates (r=-0.44) — cross-zero interference explains this. (2) Simple zeros test inconclusive at 10M (4/20, p=0.76). (3) Background z-scores decline at 50M — non-stationary M(p). (4) Multi-taper destroys signal. (5) The technique is pre-whitening, not a novel signal processing method. (6) Open: prove universality under GRH. (7) Open: derive convergence rate rigorously. (8) Open: understand background growth."

# ===== PRODUCT TESTS (code agent) =====

# Fix and rerun vibration test
run_code "VIBRATION_FAULT_TEST_V2" "Test bearing fault detection. Generate: (1) shaft vibration sin(2*pi*30*t) + 0.5*sin(2*pi*60*t). (2) Pink noise: generate white noise, FFT, multiply by 1/sqrt(f), IFFT. (3) Irregular sampling: 50000 points at 10kHz with 5% random dropout. (4) Add fault: amplitude*sin(2*pi*89.2*t). Test amplitudes: 0.01, 0.02, 0.05, 0.1, 0.2. (5) For each amplitude: compute Lomb-Scargle power at 89.2Hz and f^2 compensated power at 89.2Hz. Use scipy.signal.lombscargle. For f^2: power = (2*pi*89.2)^2 * abs(sum(signal * exp(-2j*pi*89.2*times)))**2 / len(times)**2. (6) Compare SNR: peak_at_89.2 / median_nearby. Print table of amplitude vs SNR for each method."

# Test steganography idea (from creative brainstorm)
run_code "ARITHMETIC_STEGANOGRAPHY_TEST" "Test if we can hide information in the spectral properties of a number sequence. (1) Generate a 'carrier' sequence: the first 1000 primes. (2) 'Encode' a message by slightly perturbing M(p) values at specific primes to inject a spectral peak at a SECRET frequency f_secret=7.77. Perturbation: add epsilon*cos(2*pi*f_secret*log(p)) to M(p)/p for selected primes. (3) Compute spectroscope of original vs perturbed. (4) Can the secret frequency be detected by someone who knows to look for it? (5) Can it be detected by someone who DOESN'T know (blind scan)? (6) What is the minimum epsilon that makes f_secret detectable at z>3? This tests if arithmetic steganography is feasible."

# Test data integrity / fake data detection
run_code "FAKE_DATA_DETECTION_TEST" "Test if the spectroscope can detect fake mathematical data. (1) Generate REAL Mertens function M(p) for primes to 100000. Compute spectroscope — should show zeta zero peaks. (2) Generate FAKE 'Mertens' by: random walk with same mean and variance as real M(p). Compute spectroscope — should NOT show zeta zero peaks. (3) Generate SOPHISTICATED FAKE: real M(p) + perturbation that shifts zero locations by 1%. Compute spectroscope — peaks should be at WRONG locations. (4) Can we build a classifier: given M(p) data, is it real or fake? Measure: at what perturbation level can we distinguish real from fake?"

# Universality computational proof
run_code "UNIVERSALITY_COMPUTATIONAL_PROOF" "Comprehensive computational verification of universality. (1) Sieve Mobius to 1M. (2) For 20 different subset types (random 50%, random 25%, random 10%, p mod 3=1, p mod 3=2, p mod 4=1, p mod 4=3, p mod 5=1,2,3,4, twin primes, primes in [2,500K], primes in [500K,1M], every 3rd prime, every 5th prime, primes with even M(p), primes with odd M(p)), compute compensated spectroscope and count zeros detected with local z>3. (3) Report: detection rate for each subset. (4) Find: minimum subset size for 100% detection across ALL subset types."

# ===== MORE PAPER 2 =====

run35b "PAPER2_SECTION8_CONCLUSION" "Write Section 8 (Conclusion) for Paper 2. Summarize: (1) The compensated Mertens spectroscope detects all 20 first zeta zeros. (2) The technique is pre-whitening applied to number-theoretic data. (3) Universality shows any 2750+ primes suffice. (4) GUE statistics emerge from arithmetic data. (5) Extensions to L-functions and Dedekind zeta. (6) Honest: amplitude matching remains open, background growth unexplained, no rigorous convergence proof. (7) The contribution: not a novel signal processing technique, but a novel APPLICATION that reveals the quantitative structure of the explicit formula at the level of individual primes."

run35b "PAPER2_ABSTRACT" "Write the abstract for Paper 2 (200-250 words). The paper: applies spectral compensation (pre-whitening) to a periodogram of the Mertens function at primes. Detects all 20 first zeta zeros. Key innovation: gamma^alpha compensation + local z-score normalization. Results: universality (2750 primes), GUE pair correlation RMSE=0.066, 108 L-function characters, Siegel zero 465M sigma. Honest: technique is classical pre-whitening, contribution is the application. Cite: Csoka 2015, Van der Pol 1947 as prior art."

echo "=== Phase 5 complete $(date) ===" >> "$LOG"
