#!/bin/bash
OLLAMA="http://localhost:11435/api/generate"
OUT="$HOME/Desktop/Farey-Local/experiments"

run_task() {
    local name="$1"; local prompt="$2"
    echo "$(date) Starting: $name" >> "$OUT/OVERNIGHT_CHAIN_LOG.md"
    curl -s "$OLLAMA" -d "{\"model\":\"gemma4:26b\",\"prompt\":\"$prompt\",\"stream\":false,\"options\":{\"num_ctx\":8192}}" 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('response','EMPTY'))" > "$OUT/${name}.md" 2>&1
    echo "$(date) Finished: $name ($(wc -c < "$OUT/${name}.md") bytes)" >> "$OUT/OVERNIGHT_CHAIN_LOG.md"
}

# Task 7: Open problems that our spectroscope addresses
run_task "OPEN_PROBLEMS_SURVEY" "Survey open problems in analytic number theory that the Mertens spectroscope might address. The spectroscope detects zeta zeros from M(p) values at primes using F(gamma)=gamma^2*|sum M(p)/p*exp(-igamma*log(p))|^2. Consider: (1) de Bruijn-Newman constant Lambda — can spectroscope data constrain it? (2) Simple zeros hypothesis — can peak shapes distinguish simple from double zeros? (3) GRH for specific L-functions — systematic verification via twisted spectroscope. (4) Lehmer phenomenon — detecting unusually close zero pairs. (5) Selberg eigenvalue conjecture — connection via automorphic forms. (6) Density hypothesis — can spectroscope data test N(sigma,T) bounds? List 10 open problems with assessment."

# Task 8: Semiclassical trace formula connection
run_task "TRACE_FORMULA_CONNECTION" "The Mertens spectroscope F(gamma)=|sum M(p)/p*exp(-igamma*log(p))|^2 resembles a trace formula: primes play the role of periodic orbits, log(p) plays the role of orbit length, and zeta zeros play the role of eigenvalues. In the Selberg trace formula for hyperbolic surfaces, the spectral side sums over eigenvalues lambda_k and the geometric side sums over closed geodesics of length l_n. Our spectroscope: spectral side = zeta zeros gamma_k, geometric side = primes with weight M(p)/p. Is this a rigorous analogy? Can we formalize it? What would the Weyl law look like? The density of zeta zeros is N(T) ~ T/(2pi)*log(T/(2pi*e)), which is the analogue of the Weyl law."

# Task 9: Practical test — detecting anomalous prime gaps
run_task "ANOMALOUS_GAP_DETECTION" "Can the spectroscope detect anomalous prime gaps? Large prime gaps correspond to regions where M(p) changes slowly (few new primes contribute). If we remove primes in a gap region and recompute the spectroscope, the peaks should shift. This could be used to test whether a specific set of primes has the expected spectral properties — a kind of spectral audit. Describe how to implement this test. What would a tampered prime list look like in the spectroscope?"

# Task 10: Connection to Selberg's central limit theorem
run_task "SELBERG_CLT_CONNECTION" "Selberg proved that log|zeta(1/2+it)| is approximately Gaussian with variance (1/2)*log(log(T)). Our spectroscope detects individual zeros from arithmetic data. Is there a connection between the spectroscope peak heights and Selberg's CLT? The peak height at gamma_k depends on |zeta_prime(rho_k)|. Selberg's result constrains the distribution of |zeta| on the critical line. Does it also constrain |zeta_prime| at zeros? If so, this would predict the distribution of spectroscope peak heights."

# Task 11: Prime race spectroscope  
run_task "PRIME_RACE_SPECTROSCOPE" "The Chebyshev bias (prime race pi(x;4,3) > pi(x;4,1)) is controlled by zeros of L(s,chi_4). Our spectroscope detects L-function zeros via twisting. Can we build a spectroscope that directly measures the prime race bias? Instead of M(p), use the race function R(x) = pi(x;q,a) - pi(x;q,b). The spectroscope F_race(gamma) = |sum R(p)/sqrt(p) * exp(-igamma*log(p))|^2 should detect zeros of L(s,chi) where chi distinguishes residue classes a and b. Assess feasibility."

# Task 12: Error term in prime counting function
run_task "PRIME_COUNTING_SPECTROSCOPE" "Instead of M(p), use the prime counting error: psi(x) - x where psi is the Chebyshev function. The explicit formula psi(x) = x - sum_rho x^rho/rho + ... means a spectroscope built from psi(p) - p should also detect zeros. Compare: (a) M(p) spectroscope vs (b) psi(p)-p spectroscope. Which has better SNR? The psi function has a simpler explicit formula (no zeta_prime in denominator), so the coefficients are 1/rho instead of 1/(rho*zeta_prime(rho)). This means peaks decay as 1/gamma instead of 1/(gamma*|zeta_prime|). Analyze which is better."

echo "=== Gemma4 chain complete $(date) ===" >> "$OUT/OVERNIGHT_CHAIN_LOG.md"
