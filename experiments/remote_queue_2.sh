#!/bin/bash
OUT="$HOME/Desktop/Farey-Local/experiments"
LOG="$OUT/REMOTE_QUEUE_LOG.md"

run_remote() {
    local name="$1"; local prompt="$2"
    echo "$(date) Starting: $name" >> "$LOG"
    ~/bin/remote_ollama.sh qwen3.5:35b "$name" "$prompt"
    echo "$(date) Done: $name ($(wc -c < "$OUT/${name}.md") bytes)" >> "$LOG"
}

echo "=== Remote Queue 2 $(date) ===" >> "$LOG"

# Deep math / proof tasks (35b strengths)

run_remote "REMOTE_UNIVERSALITY_GAMMA1_UNCONDITIONAL" "Prove UNCONDITIONALLY that the Mertens spectroscope detects gamma_1 (the first zeta zero). We don't need GRH for this — just PNT. Strategy: (1) By PNT, M(x)/sqrt(x) is unbounded (Ingham 1942). (2) The spectroscope at gamma=gamma_1 computes sum M(p)/p * p^{-igamma_1}. (3) The oscillation of M(x) around zero guarantees nonzero Fourier content. (4) The key: M(x) changes sign infinitely often, and the frequency of oscillation is controlled by gamma_1 (the dominant zero). (5) Can we show the spectroscope peak at gamma_1 exceeds any fixed threshold for sufficiently large N, using only PNT + Ingham? This would be the first unconditional universality result."

run_remote "REMOTE_EXPLICIT_FORMULA_DELTAW_RIGOROUS" "Rigorously derive the connection from DeltaW(p) to zeta zeros. The chain: (1) Four-term decomposition: DeltaW = A-B-C-D. (2) Bridge Identity: sum e^{2pi*i*p*f} = M(p)+2. (3) Cross-term B involves sum D*delta which connects to sum e^{2pi*i*p*f} via Compact Cross-Term Formula. (4) Explicit formula: M(p) = sum_rho p^rho/(rho*zeta'(rho)) - 2. Therefore B oscillates with zeta zeros. (5) Since D/A -> 1 and C>0, the sign of DeltaW is controlled by B, hence by M(p), hence by zeros. Write the COMPLETE derivation connecting DeltaW(p) to sum_rho c_rho * p^{igamma_rho}. This is for Paper 1."

run_remote "REMOTE_GUE_CONDITIONAL_THEOREM" "State and prove a conditional theorem: Under GRH+LI, the pair correlation of zeros detected by the Mertens spectroscope converges to the GUE prediction. Outline: (1) The spectroscope F(gamma) is a periodogram. (2) By Wiener-Khinchin, |hat(f)|^2 = hat(autocorrelation). (3) The autocorrelation of M(p)/p involves sum_{rho,rho'} terms. (4) Under LI, off-diagonal terms (rho != rho') cancel. (5) The diagonal terms give the pair correlation. (6) Montgomery's conjecture: pair correlation -> 1-(sin(pi*x)/(pi*x))^2. (7) Our spectroscope reproduces this because it accesses the pair correlation via the autocorrelation. Formalize."

run_remote "REMOTE_PAPER2_UNIVERSALITY_SECTION" "Write the universality section for Paper 2. Our results: (1) Any 2750+ primes detect all 20 zeros (M(p)/p weight). (2) Works for: random subsets, residue classes, twin primes, positive M, negative M. (3) |M(p)|/sqrt(p) (absolute value) collapses — signed oscillation essential. (4) Interval-restricted subsets [500K,1M] fail — need range spanning small primes. (5) Conditional proof: GRH+LI+VK regularity. (6) Gap 3 is sharp: sum 1/p must diverge. (7) The interpretation: holographic encoding — every prime carries all zero frequencies. Write 1500 words, LaTeX-ready, cite prior art (no prior literature on this)."

run_remote "REMOTE_3BP_EMPTY_CELLS" "The three-body periodic table has 21 empty cells — orbits predicted to exist but not found. 4199 N-body searches found 0 new periodic orbits. Why? Possible reasons: (1) The empty cells correspond to UNSTABLE orbits that exist mathematically but are not numerically findable. (2) The search method (varying initial conditions) doesn't explore the right parameter space. (3) The orbits genuinely don't exist — the periodic table prediction is wrong for those cells. (4) The search tolerance is too tight. Analyze: what CF properties do the empty cells have? Are they in the high-complexity (long period, high geometric mean) region? If so, the orbits would be extremely unstable and near-impossible to find numerically. This would validate the table rather than invalidate it."

run_remote "REMOTE_CHOWLA_LARGER_N" "The Chowla spectroscopic test at N=200K ruled out epsilon>0.004. What would we learn at N=10M? At N=10M: epsilon_min = 1.824/sqrt(10^7) = 0.000577. This is 7x more sensitive. At N=10^8: epsilon_min = 0.000058. Question: is computing mu(n) for n up to 10M feasible? Yes — Mobius sieve to 10M takes seconds. The spectroscope computation is O(N*G) where G=15000 grid points. At N=10M: 10^7 * 15000 = 1.5*10^11 operations — too much for a single sum. But we can subsample: use only n at prime values (pi(10M) ~ 620K primes). Or chunk the computation. Design an efficient algorithm for the Chowla test at N=10M."

run_remote "REMOTE_SPECTROSCOPE_FOR_DIRICHLET" "Extend the spectroscope to detect zeros of general Dirichlet series. Beyond zeta and L-functions, many Dirichlet series have zeros that control arithmetic: (1) Dedekind zeta functions of number fields. (2) Hecke L-functions. (3) Artin L-functions. (4) Automorphic L-functions. For each: what arithmetic data would we need? For Dedekind zeta of Q(sqrt(-d)): use the Kronecker symbol (d/n) as the character. For Hecke: use Hecke eigenvalues at primes. Could our spectroscope framework detect zeros of these more exotic L-functions? What would be the first test case beyond Dirichlet characters?"

run_remote "REMOTE_VISUALIZE_CONCEPTS" "Design 3 more interactive visualizations for lay audience: (1) THE FAREY CIRCLE: show Farey fractions on a circle, animate adding new denominators one at a time. Each new fraction appears at the mediant position (optimally filling the largest gap). Color by denominator level. The pattern becomes increasingly uniform — but when a PRIME denominator is added, many fractions enter at once, creating a burst. Show how DeltaW changes at each step. (2) THE EXPLICIT FORMULA VISUAL: show M(x) as a growing curve. Overlay the individual zero contributions cos(gamma_k*log(x))/gamma_k. As you add more zeros, the approximation to M(x) improves. Interactive: slider for number of zeros used. (3) THE MERTENS FUNCTION WALK: show M(n) as a random walk on integers. Color by prime/composite. The walk is biased negative (Mertens bias). The spectroscope 'listens' to this walk and hears the zero frequencies."

echo "=== Remote Queue 2 complete $(date) ===" >> "$LOG"
