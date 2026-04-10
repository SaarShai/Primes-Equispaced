#!/bin/bash
OLLAMA="http://localhost:11434/api/generate"
OUT="$HOME/Desktop/Farey-Local/experiments"
LOG="$OUT/OVERNIGHT_LOCAL_TRACK_LOG.md"

run_model() {
    local model="$1"; local name="$2"; local prompt="$3"; local ctx="${4:-16384}"
    echo "$(date) Starting: $name [$model]" >> "$LOG"
    curl -s "$OLLAMA" -d "{\"model\":\"$model\",\"prompt\":\"$prompt\",\"stream\":false,\"options\":{\"num_ctx\":$ctx}}" 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('response','EMPTY'))" > "$OUT/${name}.md" 2>&1
    sz=$(wc -c < "$OUT/${name}.md")
    echo "$(date) Done: $name (${sz} bytes)" >> "$LOG"
    [ "$sz" -lt 100 ] && echo "$(date) WARNING: $name too small!" >> "$LOG"
}

echo "=== Overnight Local Track $(date) ===" > "$LOG"

# === BATCH 1: deepseek-r1:32b (proofs, ~20 min each) ===

run_model "deepseek-r1:32b" "LOCAL_DS_UNCONDITIONAL_GAMMA1_V3" "Prove unconditionally that the Mertens spectroscope detects gamma_1. Key insight: we don't need GRH. The explicit formula M(x) = sum_rho x^rho/(rho*zeta'(rho)) is an IDENTITY (unconditional). The issue is controlling the ERROR TERM. Use: (1) PNT gives the main term. (2) Zero-free region controls most zeros. (3) The DENSITY of zeros near Re(s)=1 is small (Ingham density estimate). (4) For gamma_1 specifically: it's the zero closest to the real axis, so its contribution is the MOST persistent oscillation in M(x). All other zeros oscillate faster and cancel more. Can we show: the spectroscope peak at gamma_1 grows faster than the cumulative contribution from all other zeros? Think step by step." 32768

run_model "deepseek-r1:32b" "LOCAL_DS_DEDEKIND_INTEGRAL_PROOF" "The Dedekind ergodic argument for B>0: the integral I = integral D(x)*(x-{px}) dx should be positive because mean(D) < 0 implies the dominant term -mu_D/2 > 0. PROVE THIS RIGOROUSLY. Step 1: What is mean(D) for Farey fractions? D(f_j) = j - n*f_j. Sum: sum D(f_j) = sum j - n*sum f_j = n(n-1)/2 - n*sum f_j. Since Farey fractions satisfy sum f_j = (n-1)/2 (by symmetry f <-> 1-f), sum D = n(n-1)/2 - n(n-1)/2 = 0. Wait — mean(D) = 0, not negative! Then the ergodic argument gives integral = 0, not positive. Recheck: is mean(D) really 0? Or does the weighting by delta change things? Resolve this contradiction with the Q6 claim that -mu_D/2 > 0." 32768

# === BATCH 2: phi4 (verification, ~5 min each) ===

run_model "phi4:14b" "LOCAL_PHI4_VERIFY_LIOUVILLE" "Verify: the Liouville spectroscope advantage over Mertens is O(log gamma). The coefficient ratio is |c_L/c_M| = |zeta(2*rho)| where rho = 1/2 + igamma. At 2*rho = 1 + 2igamma: |zeta(1+2igamma)| = O(log(gamma)). Confirm this bound. Also: what is |zeta(1+2i*14.13)|? Use the Euler product approximation: |prod_{p<=100} (1-p^{-1-2i*14.13})|^{-1}. Estimate numerically." 8192

run_model "phi4:14b" "LOCAL_PHI4_VERIFY_GAP_COEFFICIENTS" "Verify: the prime gap spectroscope has coefficients O(1), not 1/rho^2. The gap residual (g_n - log(p_n))/log(p_n) comes from differencing the PNT error. The explicit formula for psi(x) = x - sum_rho x^rho/rho. So psi'(x) = 1 - sum_rho x^{rho-1}. Therefore pi'(x) ~ 1/log(x) * (1 - sum_rho x^{rho-1}). The gap g_n ~ log(p_n) * (1 + sum_rho p_n^{rho-1}). So the gap residual is sum_rho p^{rho-1} = sum_rho p^{-1/2+igamma}. The coefficient at zero rho_k is 1 (not 1/rho_k). Confirm or correct." 8192

run_model "phi4:14b" "LOCAL_PHI4_VERIFY_CHOWLA_THRESHOLD" "Verify: the Chowla detection threshold epsilon_min = 18/(pi^2*sqrt(N)) = 1.824/sqrt(N). Derivation: Var[T_h] = (1/N)*(6/pi^2)^2 under null. sigma = 0.6079/sqrt(N). 3-sigma detection: epsilon > 3*sigma = 1.824/sqrt(N). At N=200K: epsilon > 0.004. Check: is the independence assumption valid? mu(n) and mu(n+h) are NOT independent for small h (they share prime factors). Does this affect the variance calculation?" 8192

run_model "phi4:14b" "LOCAL_PHI4_VERIFY_PHASE_PHI" "Verify: phase phi = -arg(rho_1 * zeta'(rho_1)) = -1.69, which equals 5.28 mod 2pi. rho_1 = 0.5 + 14.1347i. arg(rho_1) = arctan(14.1347/0.5) = arctan(28.27) = 1.535 (close to pi/2). zeta'(rho_1) was computed as 0.783 + 0.125i. arg(zeta'(rho_1)) = arctan(0.125/0.783) = 0.159. So arg(rho_1*zeta'(rho_1)) = 1.535 + 0.159 = 1.694. phi = -1.694. And -1.694 + 2*pi = 4.589. But observed is 5.28. Gap = 0.69. Is this within numerical error? Or is there an error in the zeta' computation?" 8192

# === BATCH 3: gemma4 (research, ~1 min each) ===

run_model "gemma4:26b" "LOCAL_G4_RECENT_CHOWLA_COMPUTATIONAL" "Survey computational results on the Chowla conjecture as of 2025. Who has tested it computationally? What N values? What methods? Key papers: Tao (2016) proved Chowla on average. Matomaki-Radziwill (2016) proved short interval results. Helfgott? Fried-Soundararajan? Any computational papers testing sum mu(n)*mu(n+h) directly? What is the largest N anyone has tested to?" 8192

run_model "gemma4:26b" "LOCAL_G4_LEAN_MATHLIB_STATE_2026" "What is the current state of number theory in Mathlib (Lean 4) as of 2026? Specifically: (1) Is the Riemann zeta function defined? (2) Are Dirichlet characters defined? (3) Is the Mobius function defined? (4) Are Ramanujan sums defined? (5) Is the Mertens function defined? (6) Any Farey sequence content? (7) Are Dedekind sums defined? (8) What number theory PRs were merged in 2025-2026?" 8192

run_model "gemma4:26b" "LOCAL_G4_SPECTROSCOPE_PRIOR_ART_DEEP" "Deep prior art search for spectroscopic zero detection. Beyond Csoka 2015: (1) Mazur-Stein 'Visualizing the Riemann zeta function' — do they compute periodograms? (2) Du Sautoy's work on music of the primes — any computational spectroscopy? (3) Berry's semiclassical approach — does it produce a practical spectroscope? (4) The LMFDB spectral data — how are zeros currently computed and verified? (5) Booker-Platt-Rubinstein computational methods — do any use periodogram-type approaches? Be thorough. We need to know if ANYONE has done what we're doing." 8192

run_model "gemma4:26b" "LOCAL_G4_TAU_SPECTROSCOPE_PRIOR_ART" "Has anyone built a spectroscope for the Ramanujan tau function or other modular form L-functions? Search: (1) Computational methods for zeros of L(s,Delta). (2) Has anyone used Fourier analysis of tau(p) values to detect zeros? (3) The Sato-Tate distribution of tau(p)/p^{11/2} — does it have spectral implications? (4) Ghitza-McAndrew computational data on modular form zeros. Any periodogram approaches?" 8192

run_model "gemma4:26b" "LOCAL_G4_3BP_ORBIT_DATABASES" "What three-body orbit databases exist beyond Li-Liao (695 orbits)? (1) Suvakov-Dmitrasinovic (2013) — how many orbits? (2) Li-Liao extended catalogs? (3) Hristov et al. (4) Montgomery (figure-eight family). (5) Any database with >1000 orbits? (6) Any with unequal masses? We need larger catalogs to test our periodic table on." 8192

echo "=== Batch 1-3 complete $(date) ===" >> "$LOG"
echo "=== CHECKPOINT: Review results, decide on Batch 4-6 ===" >> "$LOG"
