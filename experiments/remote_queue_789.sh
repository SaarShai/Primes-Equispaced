#!/bin/bash
OUT="$HOME/Desktop/Farey-Local/experiments"
LOG="$OUT/REMOTE_QUEUE_LOG.md"

run_remote() {
    local name="$1"; local prompt="$2"
    echo "$(date) Starting: $name" >> "$LOG"
    ~/bin/remote_ollama.sh qwen3.5:35b "$name" "$prompt"
    echo "$(date) Done: $name ($(wc -c < "$OUT/${name}.md") bytes)" >> "$LOG"
}

run_deep() {
    local name="$1"; local prompt="$2"
    echo "$(date) Starting: $name [DEEP]" >> "$LOG"
    ~/bin/remote_ollama_deep.sh qwen3.5:35b "$name" "$prompt"
    echo "$(date) Done: $name ($(wc -c < "$OUT/${name}.md") bytes)" >> "$LOG"
}

echo "=== Remote Queue 7-9 $(date) ===" >> "$LOG"

# === Q7: VERIFY + COMPUTE (based on Q6 findings) ===

# Liouville spectroscope is stronger — verify computationally
run_remote "Q7_LIOUVILLE_VS_MERTENS_THEORY" "The Liouville function lambda(n) = (-1)^Omega(n) has summatory function L(x) = sum_{n<=x} lambda(n). The Dirichlet series sum lambda(n)/n^s = zeta(2s)/zeta(s). For the spectroscope: the coefficient at zero rho is zeta(2*rho)/zeta'(rho) vs Mertens' 1/(rho*zeta'(rho)). Since |zeta(2*rho)| = |zeta(1+2igamma)| which is O(log(gamma)), the Liouville coefficient is LARGER by a factor of |rho * zeta(2*rho)| ~ gamma * log(gamma). This means the Liouville spectroscope should have z-scores that are gamma*log(gamma) times higher than Mertens for the same number of terms. Derive this precisely. Is the improvement uniform across all zeros, or does it favor certain zeros?"

# Dedekind ergodic: the integral is positive — formalize
run_deep "Q7_DEDEKIND_ERGODIC_FORMALIZE" "The Q6 result suggests B>0 via ergodic theory because the integral of D(x)*{px} dx involves mean(D) which is negative, giving -mu_D/2 > 0. FORMALIZE THIS COMPLETELY. (1) Define precisely: what is the invariant measure of the map f -> {pf} on Farey fractions? Is it Lebesgue on [0,1]? (2) The Birkhoff ergodic theorem says (1/N)*sum g(f_i) -> integral g d(mu). What is g here? g(f) = D(f)*delta(f) = D(f)*(f - {pf}). (3) Compute integral_0^1 D(x)*(x - {px}) dx where D(x) is treated as the rank discrepancy function (continuous approximation). (4) D(x) ~ n*x - n*x = 0 in the continuous limit? No — D(f_j) = j - n*f_j, so the continuous approximation has D(x) ~ n*F(x) - n*x where F is the Farey CDF. Since F(x) < x (Farey fractions are sparser near 0), D(x) < 0 on average. (5) Compute the integral numerically for p=13,19,31. Is it positive?"

# GUE: fix the Wiener-Khinchin gap
run_deep "Q7_GUE_REGULARIZATION" "The Q6 adversarial check found that Wiener-Khinchin doesn't apply to our signal (it's a distribution, not L^2). Fix this. Approach: REGULARIZE the signal. Instead of f(x) = sum M(p)/p * delta(x - log(p)), use f_epsilon(x) = sum M(p)/p * phi_epsilon(x - log(p)) where phi_epsilon is a Gaussian of width epsilon. Then f_epsilon is in L^2 and Wiener-Khinchin applies. As epsilon -> 0, the periodogram of f_epsilon converges to our spectroscope. Does the pair correlation also converge? Under what conditions? This is a standard regularization argument in spectral theory — formalize it for our specific setting."

# 3BP: the novelty is the CF-nobility link, not the entropy formula
run_remote "Q7_3BP_WHAT_IS_NOVEL" "The entropy formula S = arccosh(tr(M)/2) is known (Thurston 1988). But applying it to 695 three-body orbits via CF nobility is new. What EXACTLY is our novel contribution for the three-body paper? (1) Extending Kin-Nakamura-Ogawa from 13 to 695 orbits with exact arithmetic. (2) The CF periodic table organization (9x8 grid). (3) The nobility-entropy anticorrelation at rho=-0.890. (4) The blind prediction AUC=0.980. (5) The 21 empty-cell predictions. Which of these would a dynamical systems referee find most interesting? Which is the strongest claim? Draft the key theorem statement."

# === Q8: EXPLORE NEW DIRECTIONS ===

# Tau spectroscope: worth computing?
run_remote "Q8_TAU_FEASIBILITY" "Computing the Ramanujan tau spectroscope requires: (1) tau(n) for n up to 100000. tau(n) can be computed from the q-expansion of Delta(z) = q*prod(1-q^n)^24. This is O(N^2) naive but O(N*log(N)) via FFT. (2) Summatory T(p) = sum_{k<=p} tau(k). (3) Spectroscope F(gamma) = gamma^alpha * |sum T(p)/p^{13/2} * exp(-igamma*log(p))|^2. The zeros of L(s,Delta) start at gamma ~= 9.22. Can we detect them? Key challenge: tau(p) grows as p^{11/2}, so the weight tau(p)/p^{13/2} = tau(p)/p^{13/2} ~ O(1/p). This is the same decay rate as M(p)/p. So the spectroscope should work with similar z-scores. Is this worth computing? What would it demonstrate that Dirichlet L-functions don't?"

# Universality: what about primes in AP?
run_remote "Q8_UNIVERSALITY_PRIMES_IN_AP" "Our universality result says any 2750 primes detect gamma_1. What about primes in a specific arithmetic progression? For primes p = a mod q (Dirichlet's theorem guarantees infinitely many): does the Mertens spectroscope on just these primes detect ZETA zeros, or L-function zeros, or both? Theory: M(p) for p = a mod q involves the explicit formula for M(x), which has contributions from ALL zeros of zeta(s). But the CHARACTER-weighted sum M_chi(p) has contributions from L(s,chi) zeros. If we use p = a mod q without character weighting, we should still get zeta zeros (because the character contributions average out). Verify this reasoning."

# What happens if we spectroscope the GAPS between primes?
run_remote "Q8_PRIME_GAP_SPECTROSCOPE" "New exploration: instead of M(p) at primes, what if we spectroscope the prime GAPS g_n = p_{n+1} - p_n? Define F(gamma) = gamma^2 * |sum (g_n - log(p_n)) / log(p_n) * exp(-igamma*log(p_n))|^2. The weight (g_n - log(p_n))/log(p_n) is the normalized gap residual — how much the gap deviates from the expected log(p). Under the Hardy-Littlewood conjecture, prime gaps have specific correlations controlled by the Siegel-Walfisz theorem. Would the gap spectroscope show peaks at zeta zeros? At OTHER frequencies? This is unexplored territory."

# === Q9: PROOF ATTEMPTS ===

# Retry unconditional gamma_1 with the deep script
run_deep "Q9_UNCONDITIONAL_GAMMA1_V2" "PROOF ATTEMPT (be thorough): Prove unconditionally that the Mertens spectroscope has a peak near gamma_1 for large X. The key insight from Q6: we CANNOT weaken GRH to zero-density because Siegel zeros near sigma=1 would dominate. BUT: we know Siegel zeros don't exist for small conductors (our own Siegel zero test showed this computationally). Can we use the CONDITIONAL nonexistence of Siegel zeros (for q up to some Q_0) to get a PARTIALLY unconditional result? E.g.: 'For all Dirichlet characters of conductor q <= 50, the spectroscope detects gamma_1 unconditionally (since we ruled out Siegel zeros for these characters).' This combines our Siegel zero computation with the universality proof."

# Composite healing: can we prove DeltaW(n)>0 for most composites?
run_deep "Q9_COMPOSITE_HEALING_PROOF" "PROOF: 95.4% of composites have DeltaW(n)>0. Prove for composites n with phi(n)/n < 1/2 (most composites satisfy this). The argument: (1) phi(n) new fractions enter F_n. For composite n, phi(n) << n. (2) Dilution A = sum_old D^2 * (n'^2 - n^2)/(n^2 * n'^2) ~ phi(n)*2n/(n^4) = 2*phi(n)/n^3. (3) New-fraction damage D = (1/n'^2)*sum_new D_p^2. Each new fraction k/n has D(k/n) ~ O(n). There are phi(n) of them. So D ~ phi(n)*n^2/n'^2 ~ phi(n)/n^2 * (n/n')^2 ~ phi(n)/n^2. (4) D/A ~ (phi(n)/n^2) / (2*phi(n)/n^3) = n/2. Wait — this says D/A ~ n/2 which is LARGE, meaning D >> A. That contradicts DeltaW>0. Recheck the scaling. The four-term decomposition for composites needs careful treatment."

echo "=== Remote Queue 7-9 complete $(date) ===" >> "$LOG"
