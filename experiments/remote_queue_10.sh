#!/bin/bash
OUT="$HOME/Desktop/Farey-Local/experiments"
LOG="$OUT/REMOTE_QUEUE_LOG.md"

run_35b() {
    local name="$1"; local prompt="$2"
    echo "$(date) Starting: $name [35b]" >> "$LOG"
    ~/bin/remote_ollama.sh qwen3.5:35b "$name" "$prompt"
    echo "$(date) Done: $name ($(wc -c < "$OUT/${name}.md") bytes)" >> "$LOG"
}

run_deepseek() {
    local name="$1"; local prompt="$2"
    echo "$(date) Starting: $name [deepseek]" >> "$LOG"
    ~/bin/remote_ollama_deep.sh deepseek-r1:32b "$name" "$prompt"
    echo "$(date) Done: $name ($(wc -c < "$OUT/${name}.md") bytes)" >> "$LOG"
}

echo "=== Remote Queue 10 $(date) ===" >> "$LOG"

# DEEPSEEK: retry failed proof tasks
run_deepseek "Q10_UNCONDITIONAL_GAMMA1_DEEPSEEK" "Prove unconditionally that the Mertens spectroscope F(gamma) = |sum M(p)/p * exp(-igamma*log(p))|^2 has a peak near gamma_1 for large X. Available tools: PNT, Ingham (M(x) changes sign infinitely often, |M(x)|>x^{1/2-eps} i.o.), zero-free region, Vinogradov-Korobov. The explicit formula is unconditional as an identity. Key challenge: bounding off-resonance sums without GRH. Zero-density estimates N(sigma,T) << T^{A(1-sigma)} control zeros near sigma=1. But Siegel zeros could dominate. Strategy: prove for gamma_1 only (not all zeros), using that gamma_1 is the CLOSEST zero to the real axis, so its resonance is strongest. Show the peak height grows faster than any off-resonance contribution."

run_deepseek "Q10_COMPOSITE_HEALING_DEEPSEEK" "Prove DeltaW(n)>0 for composite n with phi(n)/n < 1/2. Four-term decomposition: DeltaW = A - B - C - D. For composites: phi(n) new fractions (fewer than n-1). Dilution A ~ phi(n)/n^3 * sum_old D^2. New-fraction damage D ~ phi(n) * avg(D_new^2) / n'^2. Carefully compute the scaling of each term for composites. The key: for composites, phi(n)/n is SMALL, so proportionally few new fractions enter, and the dilution benefit dominates. Make this rigorous."

# 35b: explore the exciting new directions
run_35b "Q10_GAP_SPECTROSCOPE_PREDICTIONS" "The prime gap spectroscope F(gamma) should show zeta zeros PLUS Hardy-Littlewood correlations. The H-L twin prime conjecture predicts a specific correlation structure in g_n = p_{n+1} - p_n. This should manifest as additional spectral peaks beyond the zeta zeros. Where exactly? The singular series S2 for twin primes involves product over primes of (1 - 1/(p-1)^2). Does this product have a spectral signature at specific frequencies? Could the gap spectroscope DISTINGUISH the zeta-zero contribution from the H-L contribution? This would be a new computational tool for studying prime gaps."

run_35b "Q10_TAU_COMPUTE_DESIGN" "Design the computation for the Ramanujan tau spectroscope. (1) Computing tau(n) to N=100000: use q-expansion Delta(z) = q*prod_{n=1}^inf (1-q^n)^24. For N terms: compute prod (1-q^n)^24 truncated to N terms, then multiply by q. This is O(N^2) naive, O(N log N) via FFT convolution. (2) Compute T(p) = sum_{k<=p} tau(k) for primes p. (3) Weight: tau(p)/p^{13/2} per the corrected critical line. (4) Spectroscope: F(gamma) = gamma^alpha * |sum T(p)/p^{13/2} * exp(-igamma*log(p))|^2 on gamma in [5, 30]. (5) Known first zeros of L(s,Delta): gamma ~= 9.22, 13.91, 17.44. Can we detect them? (6) What alpha is optimal for tau? The decay is 1/|rho_tau|^2 where rho_tau = 6 + igamma. So |rho|^2 = 36 + gamma^2. For gamma>6, this is ~gamma^2. So alpha=2 should work."

run_35b "Q10_DEDEKIND_INTEGRAL_COMPUTE" "The Dedekind ergodic argument says B>0 if the integral I = integral_0^1 D(x)*(x - {px}) dx is positive, where D(x) is the continuous approximation to rank discrepancy. Compute I numerically for p=13, 19, 31, 43, 53, 97 using the exact Farey data. For each p: (1) List all fractions in F_{p-1}. (2) For each f=a/b: D(f) = rank - n*f, delta(f) = f - {pf}. (3) Sum D(f)*delta(f) over all f. (4) Normalize: I_p = sum D*delta / (n * n'). (5) Is I_p > 0 for all tested p? If yes, the ergodic argument has strong computational support. (6) How does I_p scale with p?"

run_35b "Q10_SPECTROSCOPE_ZOO" "We now have a zoo of spectroscopes: (1) Mertens M(p)/p. (2) Liouville L(p)/p (advantage: log(gamma) stronger). (3) Psi (psi(p)-p)/p (simpler coefficients 1/rho). (4) Prime gap (g_p - log(p))/log(p) (detects H-L correlations). (5) Tau T(p)/p^{13/2} (detects modular form zeros). Which combinations or comparisons would be most informative? Could we build a MULTI-SPECTROSCOPE that combines them? E.g., jointly analyzing the Mertens and gap spectroscopes to separate zeta-zero from H-L contributions. Design the optimal experimental comparison."

echo "=== Remote Queue 10 complete $(date) ===" >> "$LOG"
