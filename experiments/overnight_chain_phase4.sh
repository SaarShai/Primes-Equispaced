#!/bin/bash
OLLAMA="http://localhost:11435/api/generate"
OUT="$HOME/Desktop/Farey-Local/experiments"

run_35b() {
    local name="$1"; local prompt="$2"
    echo "$(date) Starting: $name" >> "$OUT/OVERNIGHT_CHAIN_LOG.md"
    curl -s "$OLLAMA" -d "{\"model\":\"qwen3.5:35b\",\"prompt\":\"$prompt\",\"stream\":false,\"options\":{\"num_ctx\":8192}}" 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('response','EMPTY'))" > "$OUT/${name}.md" 2>&1
    echo "$(date) Finished: $name ($(wc -c < "$OUT/${name}.md") bytes)" >> "$OUT/OVERNIGHT_CHAIN_LOG.md"
}

echo "=== Phase 4 chain started $(date) ===" >> "$OUT/OVERNIGHT_CHAIN_LOG.md"

# 1. Universality proof under GRH
run_35b "UNIVERSALITY_ANALYTICAL_PROOF" "PROVE under GRH: ANY subset S of primes with |S|->infinity detects zeta zeros via the spectroscope F_S(gamma) = gamma^2 * |sum_{p in S} M(p)/p * exp(-igamma*log(p))|^2. The key: M(p) = -1 + sum_rho p^rho/(rho*zeta_prime(rho)). Each p^rho = p^{1/2+igamma_k} contributes oscillation cos(gamma_k*log(p)) to M(p). For the spectroscope sum at gamma=gamma_j: sum_{p in S} M(p)/p * p^{-igamma_j} = sum_{p in S} sum_k c_k * p^{igamma_k - igamma_j - 1/2}. The k=j term: c_j * sum_{p in S} p^{-1/2} ~ c_j * 2*sqrt(max(S))/log(max(S)) -> infinity. Cross terms k!=j: sum_{p in S} p^{i(gamma_k-gamma_j)-1/2} = o(sum p^{-1/2}) by equidistribution of {(gamma_k-gamma_j)*log(p)} mod 2pi (under LI). Therefore F_S(gamma_j) ~ |c_j|^2 * (sum p^{-1/2})^2 regardless of which primes are in S. Formalize this."

# 2. Simple zeros: prove peak shape is Lorentzian under simple zeros hypothesis
run_35b "SIMPLE_ZEROS_PEAK_SHAPE_PROOF" "PROVE: Under GRH with simple zeros, the spectroscope peak at gamma_j has Lorentzian shape. The peak profile is F(gamma_j+delta) = |sum_p M(p)/p * exp(-i*(gamma_j+delta)*log(p))|^2 = |W(delta)|^2 where W(delta) = sum_p (M(p)/p) * exp(-idelta*log(p)) * p^{-igamma_j}. Near delta=0, W(delta) ~ c_j * N + sum_{k!=j} c_k * W_k(delta). The main peak shape comes from |W_0(delta)|^2 where W_0(delta) = sum_p p^{-1/2} * exp(-idelta*log(p)). By partial summation against pi(x): W_0(delta) ~ integral_2^X x^{-1/2-idelta}/log(x) dx. For small delta: |W_0(delta)|^2 ~ |W_0(0)|^2 * 1/(1 + (delta*T)^2) where T ~ log(X)/2. This is a Lorentzian with width 1/T ~ 2/log(X). For a DOUBLE zero: the coefficient involves c_j*log(p), changing W_0 to W_1(delta) = sum p^{-1/2}*log(p)*exp(-idelta*log(p)). This gives |W_1|^2 ~ (log(X))^2 / (1+(delta*T)^2)^2 — a SQUARED Lorentzian. Prove this rigorously."

# 3. Siegel zero: prove spectroscope sensitivity formula
run_35b "SIEGEL_SENSITIVITY_PROOF" "PROVE: If L(beta,chi)=0 with beta real and close to 1, then the twisted spectroscope F_chi(gamma) at gamma~0 satisfies F_chi(0) >= C * N^2 / (1-beta)^2 where N is the number of primes used. The argument: from the explicit formula, the contribution of the Siegel zero to M(x,chi) = sum_{n<=x} mu(n)*chi(n) is approximately x^beta / (beta*L_prime(beta,chi)). At gamma=0, the spectroscope sum becomes sum_p chi(p)*M(p)/p * 1 ~ sum_p chi(p)/p * (contribution from Siegel zero) ~ (1/(beta*L_prime(beta,chi))) * sum_p chi(p) * p^{beta-1}. Since beta~1, p^{beta-1} ~ 1, so the sum ~ N/phi(q). The peak height ~ N^2 / (beta*(1-beta)*L_prime)^2. Since (1-beta) is tiny, this is huge. Formalize."

echo "=== Phase 4 chain complete $(date) ===" >> "$OUT/OVERNIGHT_CHAIN_LOG.md"
