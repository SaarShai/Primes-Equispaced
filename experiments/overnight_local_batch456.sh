#!/bin/bash
OLLAMA="http://localhost:11434/api/generate"
OUT="$HOME/Desktop/Farey-Local/experiments"
LOG="$OUT/OVERNIGHT_LOCAL_TRACK_LOG.md"

run_model() {
    local model="$1"; local name="$2"; local prompt="$3"; local ctx="${4:-16384}"
    echo "$(date) Starting: $name [$model]" >> "$LOG"
    curl -s "$OLLAMA" -d "{\"model\":\"$model\",\"prompt\":\"$prompt\",\"stream\":false,\"options\":{\"num_ctx\":$ctx}}" 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('response','EMPTY'))" > "$OUT/${name}.md" 2>&1
    echo "$(date) Done: $name ($(wc -c < "$OUT/${name}.md") bytes)" >> "$LOG"
}

echo "=== Batch 4-6 $(date) ===" >> "$LOG"

# BATCH 4: deepseek — follow up on Codex's Dedekind correlation insight
run_model "deepseek-r1:32b" "LOCAL_DS_DEDEKIND_STRATIFIED" "The B>0 mechanism is denominator-mediated correlation: Cov(D,delta)>0 because both are controlled by denominator q. Small-q fractions have large |D| and structured delta, dominating the sum. PROVE: decompose B = sum_{q<=N} B_q where B_q = sum_{a:gcd(a,q)=1} D(a/q)*delta(a/q). Show B_q > 0 for small q (say q <= sqrt(N)). For small q: D(a/q) ~ n*(a/q - rank/n) has magnitude O(n/q). delta(a/q) = a/q - (pa mod q)/q has magnitude O(1/q). So B_q ~ sum_a O(n/q^2). There are phi(q) terms. B_q ~ phi(q)*n/q^2 ~ n/q. Sum over q<=sqrt(N): sum n/q ~ n*log(sqrt(N)). This should dominate sum over large q. Formalize." 32768

# BATCH 5: phi4 — verify spectroscope zoo ranking
run_model "phi4:14b" "LOCAL_PHI4_VERIFY_ZOO_RANKING" "The spectroscope zoo analysis (18KB) ranked: (1) Tau spectroscope (highest theoretical interest — detects modular form zeros). (2) Liouville (modest O(log gamma) advantage, easy to compute). (3) Gap (O(1) coefficients but SNR~O(1) may be too weak). Verify: is SNR~O(1) for the gap spectroscope really fatal? The gap residual has coefficients O(1) but there are N terms, so signal ~ N. Background from N random phases ~ N. So SNR ~ N/N = O(1). But with gamma^0 compensation: SNR should still be O(1) at each frequency. This means the gap spectroscope CANNOT detect individual zeros. Is this correct? Or does the coherent sum still produce peaks?" 8192

run_model "phi4:14b" "LOCAL_PHI4_VERIFY_DEDEKIND_INTEGRAL" "The Q10 Dedekind integral computation (14KB) should have numerical values. Check: for p=13 (Farey F_12), is sum D(f)*delta(f) positive? The Codex analysis says yes because small-q fractions dominate. For p=13, the small-q fractions are: 0/1, 1/1 (q=1); 1/2 (q=2); 1/3, 2/3 (q=3). These few fractions should have large |D*delta| products. Verify this makes sense." 8192

# BATCH 6: gemma4 — more research
run_model "gemma4:26b" "LOCAL_G4_MODULAR_FORM_SPECTROSCOPY" "Has anyone used spectroscopy (periodogram, Fourier analysis) to study modular forms computationally? We want to build a tau(n) spectroscope. Check: (1) Conrey-Farmer-Keating-Rubinstein-Snaith moments work — do they use spectral methods? (2) Booker's computational L-function methods — any periodogram approaches? (3) The LMFDB modular form pages — how are zeros computed? (4) Any work on detecting Hecke eigenvalues from coefficient data via Fourier methods?" 8192

run_model "gemma4:26b" "LOCAL_G4_DENOMINATOR_STRATIFICATION_LITERATURE" "Has anyone stratified Farey sums by denominator in the number theory literature? We want to decompose B = sum_q B_q and show small-q terms dominate. Check: (1) Boca-Cobeli-Zaharescu denominator-class results. (2) Dress (1999) on Farey statistics by denominator. (3) Kanemitsu-Yoshimoto on Farey discrepancy decomposition. (4) Any work decomposing the Franel-Landau sum sum |f_j - j/n| by denominator class?" 8192

run_model "gemma4:26b" "LOCAL_G4_UNCONDITIONAL_ZERO_DETECTION" "Has anyone proved unconditionally that a spectroscopic method detects zeta zeros? We have conditional proofs (GRH+LI). Check: (1) Does the Selberg class theory give unconditional zero detection? (2) Has anyone shown the explicit formula periodogram has peaks unconditionally? (3) Odlyzko's work on zero computation — is any of it unconditional in the spectral sense? (4) Has anyone used Ingham's theorem on M(x) sign changes to prove spectral peak existence?" 8192

echo "=== Batch 4-6 complete $(date) ===" >> "$LOG"
