#!/bin/bash
OUT="$HOME/Desktop/Farey-Local/experiments"
LOG="$OUT/REMOTE_QUEUE_LOG.md"

run_remote() {
    local name="$1"; local prompt="$2"
    echo "$(date) Starting: $name" >> "$LOG"
    ~/bin/remote_ollama.sh qwen3.5:35b "$name" "$prompt"
    echo "$(date) Done: $name ($(wc -c < "$OUT/${name}.md") bytes)" >> "$LOG"
}

echo "=== Remote Queue 6 $(date) ===" >> "$LOG"

# VERIFY: 3BP entropy = arccosh(tr(M)/2) — is this actually new?
run_remote "VERIFY_3BP_ENTROPY_FORMULA" "We derived: for three-body orbits, braid entropy S = arccosh(tr(M)/2) where M is the SL(2,Z) matrix. This links CF nobility to entropy monotonically via trace. VERIFY: (1) Is this formula KNOWN in the dynamical systems literature? Check: Thurston, Bestvina-Handel, Bowen for connections between braid entropy and matrix trace. (2) Is the specific application to the Li-Liao catalog (695 orbits) new? (3) Does arccosh(tr/2) match our computational rho=-0.890? Compute: if nobility n correlates with 1/geometric_mean of CF, and geometric_mean relates to trace via the CF period, then S = arccosh(tr/2) should give rho close to -0.89. Check."

# EXPLORE: Liouville function spectroscope
run_remote "EXPLORE_LIOUVILLE_SPECTROSCOPE" "The Liouville function lambda(n) = (-1)^Omega(n) where Omega counts prime factors with multiplicity. Its Dirichlet series: sum lambda(n)/n^s = zeta(2s)/zeta(s). Our spectroscope applied to lambda: F(gamma) = gamma^2 * |sum L(n)/n * exp(-igamma*log(n))|^2 where L(n) = sum_{k<=n} lambda(k) (summatory Liouville). Peaks should appear at zeta zeros (same as Mertens). BUT: lambda has different autocorrelation properties than mu. The Chowla conjecture for lambda: sum lambda(n)*lambda(n+h) = o(N). Does the Liouville spectroscope give DIFFERENT z-scores than the Mertens spectroscope? If so, which is stronger? Analyze theoretically."

# VERIFY: GUE conditional proof (from DEEP_GUE_PROOF)
run_remote "VERIFY_GUE_PROOF" "We have a 6.4KB GUE conditional proof claiming: under GRH+LI, the pair correlation from the Mertens spectroscope converges to Montgomery's prediction. The proof uses Wiener-Khinchin to connect F(gamma) autocorrelation to zero pair statistics. ADVERSARIAL CHECK: (1) Does Wiener-Khinchin apply here? Our 'signal' is sum M(p)/p * delta(x-log(p)) which is a distribution, not L^2. (2) The diagonal/off-diagonal separation in step 5-6: does LI really guarantee off-diagonal cancellation for the PAIR sum, not just the single sum? (3) Is the convergence uniform in the test function, or just pointwise? Identify any gaps."

# EXPLORE: Ramanujan tau spectroscope — does it detect modular form zeros?
run_remote "EXPLORE_TAU_SPECTROSCOPE" "The Ramanujan tau function tau(n) is the n-th Fourier coefficient of the modular discriminant Delta(z). Its L-function L(s,Delta) has zeros on Re(s)=11/2 (by Deligne). Could a spectroscope F(gamma) = gamma^2 * |sum T(p)/p * exp(-igamma*log(p))|^2 where T(p) = sum_{k<=p} tau(k) detect these zeros? Key differences from Mertens: (1) tau(p) = p^{11/2} * (alpha_p + beta_p) with |alpha_p|=|beta_p|=1 (Ramanujan-Petersson). (2) The natural weight is tau(p)/p^{11/2+1} = tau(p)/p^{13/2}. (3) Zeros are at s = 11/2 + igamma_k. Would this work? What would the detection look like?"

# RETRY failed tasks with 16K context
run_remote "RETRY_UNIVERSALITY_WEAKEN_GRH" "Can we weaken GRH in the universality theorem to just a zero-free region? Our proof needs: off-resonance sums bounded by on-resonance. With GRH (all zeros at Re=1/2): off-resonance = O(sum p^{-1/2}) vs on-resonance = O(sum p^{-1}). Without GRH: zeros at Re(s)=sigma>1/2 give terms p^{sigma-1} which could be O(p^{-0.1}) >> O(p^{-1/2}). The zero-density estimate N(sigma,T) << T^{A(1-sigma)} (Ingham) means FEW zeros are far from Re=1/2. Can we show: the TOTAL contribution from off-line zeros is still o(sum p^{-1}) using zero-density + the few-ness of exceptional zeros? This would give universality conditional on zero-density, not GRH."

run_remote "RETRY_DEDEKIND_ERGODIC" "Fresh approach to B>0 via ergodic theory. The sum B = (2/n'^2)*sum D(f)*delta(f) where delta(f)=f-{pf}. The map T_p: f -> {pf} is measure-preserving on [0,1] with Lebesgue measure. The Birkhoff average (1/N)*sum g(f_i) should converge to integral g(x)*dx. For our observable g(x) = D(x)*(x-{px}): compute the integral. D(x) ~ n*(x - rank(x)/n) and {px} is equidistributed. So integral D(x)*(x-{px}) dx = integral D(x)*x dx - integral D(x)*{px} dx. The first integral = sum D(f)*f/n ~ constant. The second involves the correlation between D and {p*}. If D and {pf} are asymptotically independent, the integral is (mean D)*(mean {pf}) = negative * 1/2. Is the integral positive?"

echo "=== Remote Queue 6 complete $(date) ===" >> "$LOG"
