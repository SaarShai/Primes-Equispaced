#!/bin/bash
OUT="$HOME/Desktop/Farey-Local/experiments"
LOG="$OUT/REMOTE_QUEUE_LOG.md"

echo "=== Remote Queue 10 FIXED $(date) ===" >> "$LOG"

# Deepseek tasks — use streaming script
echo "$(date) Starting: Q10_COMPOSITE_HEALING_DEEPSEEK [deepseek-stream]" >> "$LOG"
~/bin/remote_ollama_deepseek.sh "Q10_COMPOSITE_HEALING_DEEPSEEK" "Prove DeltaW(n)>0 for composite n with phi(n)/n < 1/2. Four-term decomposition: DeltaW = A - B - C - D. For composites: phi(n) new fractions. Dilution A benefits from fewer new points. New-fraction damage D proportional to phi(n). Show D/A < 1 when phi(n)/n is small. Be thorough."
echo "$(date) Done: Q10_COMPOSITE_HEALING_DEEPSEEK ($(wc -c < "$OUT/Q10_COMPOSITE_HEALING_DEEPSEEK.md") bytes)" >> "$LOG"

# Regular 35b tasks
for task_info in \
    "Q10_GAP_SPECTROSCOPE_PREDICTIONS|The prime gap spectroscope has coefficients O(1) not 1/rho^2 (Codex corrected). With alpha=0 (no compensation), predict what the gap spectroscope should look like. Peaks at zeta zeros with uniform heights? Or decaying? The explicit formula gives gap residual ~ sum p^{rho-1}. At gamma=gamma_k the resonant term is p^{igamma_k - 1/2}. The squared sum gives peaks of height ~ (sum p^{-1/2})^2 = O(N). Background also O(N). So SNR ~ O(1)? That would mean NO detection. Analyze carefully." \
    "Q10_TAU_COMPUTE_DESIGN|Design the Ramanujan tau computation. tau(n) from q-expansion of Delta(z) = q*prod(1-q^n)^24. For N=100000: (1) Compute prod(1-q^n)^24 as power series truncated to N terms. O(N^2) naive, O(N log N) via FFT. (2) The first few tau values: tau(1)=1, tau(2)=-24, tau(3)=252, tau(4)=-1472. (3) Sum T(p) for primes p. (4) Weight tau(p)/p^{13/2}. (5) Spectroscope on gamma in [5,30]. First zeros of L(s,Delta): 9.22, 13.91, 17.44. Estimate: will we detect them with 9592 primes (to 100K)?" \
    "Q10_DEDEKIND_INTEGRAL_COMPUTE|Compute the Dedekind ergodic integral numerically. For p=13,19,31,43,53,97: list all fractions in F_{p-1}, compute D(f)=rank-n*f and delta(f)=f-{pf}, sum D*delta, normalize. Is the sum positive for all tested p? Report the values." \
    "Q10_SPECTROSCOPE_ZOO|We have a zoo of spectroscopes: Mertens, Liouville (log gamma stronger), Psi (simpler coefficients), Gap (no zeta prime, O(1) coefficients), Tau (modular form zeros). Which should we compute first? Rank by: (1) theoretical interest, (2) computational feasibility, (3) likelihood of new discovery. The gap spectroscope may have SNR~O(1) (too weak). Liouville is a modest improvement. Tau detects different zeros. Recommend the TOP 2 to compute next."
do
    IFS='|' read -r name prompt <<< "$task_info"
    echo "$(date) Starting: $name [35b]" >> "$LOG"
    ~/bin/remote_ollama.sh qwen3.5:35b "$name" "$prompt"
    echo "$(date) Done: $name ($(wc -c < "$OUT/${name}.md") bytes)" >> "$LOG"
done

echo "=== Remote Queue 10 FIXED complete $(date) ===" >> "$LOG"
