#!/bin/bash
OLLAMA="http://localhost:11435/api/generate"
OUT="$HOME/Desktop/Farey-Local/experiments"

run() {
    local name="$1"; local prompt="$2"
    echo "$(date) Starting: $name" >> "$OUT/MEGA_CHAIN_LOG.md"
    curl -s "$OLLAMA" -d "{\"model\":\"qwen3.5:35b\",\"prompt\":\"$prompt\",\"stream\":false,\"options\":{\"num_ctx\":8192}}" 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('response','EMPTY'))" > "$OUT/${name}.md" 2>&1
    sz=$(wc -c < "$OUT/${name}.md")
    echo "$(date) Done: $name (${sz} bytes)" >> "$OUT/MEGA_CHAIN_LOG.md"
    [ "$sz" -lt 100 ] && echo "$(date) WARNING: $name appears empty!" >> "$OUT/MEGA_CHAIN_LOG.md"
}

echo "=== Mega chain 35b started $(date) ===" > "$OUT/MEGA_CHAIN_LOG.md"

# --- PROOFS (highest priority) ---

# 1. Prove B>0 for large primes (the Dedekind gap — POST-8 HIGHEST)
run "PROVE_B_POSITIVE_LARGE_P" "PROOF: The cross-term B = (2/n'^2)*sum_{f in F_{p-1}} D(f)*delta(f) where D is rank discrepancy and delta is insertion shift. For primes with M(p)<=-3, B>0 computationally for all p<=100000. Prove B>0 for all sufficiently large p with M(p)<=-3. Strategy: B = (2/n'^2)*sum_b sum_{a:gcd(a,b)=1} D(a/b)*delta(a/b). For large p, D(a/b) ~ n*(a/b - rank/n) and delta(a/b) = a/b - {pa/b}. The product D*delta has a Dedekind sum structure within each denominator b. The key: sum_b C_b where C_b = sum_a D(a/b)*delta(a/b). For the dominant denominators b ~ p/2 to p, we have D(a/b) ~ O(p) and delta(a/b) ~ O(1/b), so C_b ~ O(p/b)*phi(b). Summing: B ~ sum_{b~p/2}^p p*phi(b)/b ~ p^2. This exceeds A-D ~ O(p). Formalize."

# 2. Prove the four-term decomposition rigorously (reviewer asked)
run "FOUR_TERM_RIGOROUS_PROOF" "PROVE rigorously: DeltaW(p) = A - B - C - D where A = sum_old D_{p-1}^2 * (1/n^2 - 1/n'^2) is dilution, B = (2/n'^2)*sum_old D_{p-1}*delta is cross-term, C = (1/n'^2)*sum_old delta^2 is shift-squared, D = (1/n'^2)*sum_new D_p^2 is new-fraction discrepancy. Start from W(p) = (1/n'^2)*sum_{f in F_p} D_p(f)^2 and W(p-1) = (1/n^2)*sum_{f in F_{p-1}} D_{p-1}(f)^2. Use D_p(f) = D_{p-1}(f) + delta(f) for old fractions. Expand (D+delta)^2 = D^2 + 2D*delta + delta^2. Collect terms. Show that the boundary f=1 contributes a correction term. This is Lean-verified but the paper proof needs expansion for the reviewer."

# 3. Prove D(1/p) dominance rigorously
run "D1P_DOMINANCE_PROOF" "PROVE: D(1/p) = 1 - |F_p|/p ~ -3p/pi^2 as p->inf. Then show |D(1/p)*delta(1/p)| / |sum_new D*delta| >= 0.65 for large p. D(1/p) has rank j=1 in F_p (only 0/1 precedes it since 1/(p-1) > 1/p for p>=3). So D(1/p) = 1 - n/p where n=|F_p|. By n = 1 + sum_{k=1}^p phi(k) ~ 3p^2/pi^2, we get D(1/p) = 1 - (3p^2/pi^2 + O(p*log(p)))/p = 1 - 3p/pi^2 - O(log(p)). For the dominance: delta(1/p) = 1/p - {p/p} = 1/p - 0 = 1/p (since p*1/p = 1 is integer). So D(1/p)*delta(1/p) = (1-n/p)/p. The sum over all new fractions: sum_{k=1}^{p-1} D(k/p)*delta(k/p). Show the k=1 term dominates."

# 4. Expand Theorem 3.5 proof (reviewer asked for more detail)
run "THEOREM_35_EXPANDED" "The Universal Farey Exponential Sum theorem states: for all integers m and N>=1, sum_{f in F_N} e^{2*pi*i*m*f} = sum_{d|gcd(m,N)} mu(N/d)*d + [m=0]*|F_N|. The current proof in the paper is brief. Expand it with all intermediate steps: (1) Write |F_N| as sum_{b=1}^N phi(b). (2) The exponential sum splits by denominator: sum_{f in F_N} e^{2*pi*i*m*f} = sum_{b=1}^N sum_{a=1,gcd(a,b)=1}^{b} e^{2*pi*i*m*a/b}. (3) The inner sum is the Ramanujan sum c_b(m) = sum_{a,gcd(a,b)=1} e^{2*pi*i*m*a/b}. (4) By Ramanujan's formula: c_b(m) = sum_{d|gcd(b,m)} mu(b/d)*d. (5) Interchange sums. (6) The m=0 case gives sum phi(b) = |F_N| - 1 (exclude f=0). Give every step."

# 5. Expand Theorem 3.9 proof (Cross-Term Formula)
run "THEOREM_39_EXPANDED" "Expand the proof of the Cross-Term Formula. The theorem states a compact formula for B = (2/n'^2)*sum D*delta in terms of Ramanujan sums. The proof uses the Bridge Identity and Displacement-Shift identity. Key steps: (1) Start from B = (2/n'^2)*sum_{f in F_{p-1}, f!=1} D_{F_{p-1}}(f)*delta(f). (2) Substitute delta(f) = f - {pf} from Definition 2.2. (3) Use the Permutation Square-Sum identity to relate sum D*delta to sum D*(f-{pf}). (4) Split: sum D*f - sum D*{pf}. (5) The first sum is computable from sum D(f)*f = sum (j-nf)*f = sum jf - n*sum f^2. (6) For the second sum, use the connection to Ramanujan sums via the Bridge Identity. Give all intermediate algebraic steps."

# 6. Bridge Identity novelty clarification
run "BRIDGE_IDENTITY_NOVELTY" "Assess the novelty of the Bridge Identity: sum_{f in F_{p-1}} e^{2*pi*i*p*f} = M(p) + 2. Is this identity known in the literature? The left side is a Ramanujan sum: sum_{f in F_N} e^{2*pi*i*m*f} = sum_{b=1}^N c_b(m). For m=p (prime) and N=p-1: this becomes sum_{b=1}^{p-1} c_b(p). Since p is prime: c_b(p) = mu(b) when gcd(b,p)=1 (which is always since b<p). So the sum is sum_{b=1}^{p-1} mu(b) = M(p-1). But M(p-1) = M(p) - mu(p) = M(p) + 1 (since mu(p) = -1). Adding the f=0 and f=1 boundary terms (both e^0 = 1): total = M(p) + 1 + 2 = M(p) + 3? Check this carefully. Is the +2 from boundaries correct? Is this identity truly new or is it a special case of the Ramanujan sum formula?"

# 7. Prove the Injection Principle with full detail
run "INJECTION_PRINCIPLE_EXPANDED" "Expand the proof of the Injection Principle: when prime p enters the Farey sequence, each new fraction k/p lands in a DISTINCT gap of F_{p-1}. The key: the gap containing k/p is determined by the neighbors of k/p in F_{p-1}. By the mediant property, k/p is the mediant of its Farey neighbors a/b and c/d where bc-ad=1 and b+d=p. The map k -> (a/b, c/d) is injective because different k give different mediants. Prove: (1) Every k in {1,...,p-1} maps to a unique gap. (2) The map is via modular inversion: k determines a unique b via k*b_inv = a mod b. (3) No two k share a gap. (4) The length of each gap is 1/(bd) <= 1/p. Give the full proof with all steps."

# 8. Spectral positivity proof attempt
run "SPECTRAL_POSITIVITY_PROOF" "PROVE: For prime p and denominator b with 1<=b<=p-1, the Dedekind kernel K_b(p) = |sum_{a=1,gcd(a,b)=1}^b e^{2*pi*i*pa/b}|^2 = c_b(p)^2 is non-negative (which is trivially true since it's a squared modulus). The more interesting claim: sum_b K_b(p)*w_b >= 0 for suitable weights w_b. Specifically, with w_b = phi(b)/b^2, can we show sum_b c_b(p)^2 * phi(b)/b^2 >= c * p for some constant c > 0? This would give a lower bound on C in the four-term decomposition. Use: c_b(p) = mu(b) for gcd(b,p)=1 (all b<p), so c_b(p)^2 = 1. Then sum_{b=1}^{p-1} phi(b)/b^2 ~ 6/pi^2 * log(p). This gives C >= (6/pi^2)*log(p)/p which is too weak. Can we do better?"

# 9. Prove composite healing for most composites
run "COMPOSITE_HEALING_RIGOROUS" "PROVE: For composite n with phi(n)/n < 1/2, DeltaW(n) > 0 (the Farey sequence becomes more uniform). 95.4% of composites satisfy this. Key argument: the number of new fractions is phi(n), which for composites is strictly less than n-1. The dilution term A = old_D_sq * (n'^2-n^2)/n^2 benefits from the addition of new points. The damage term D = (1/n'^2)*sum_new D_p^2 is proportional to phi(n)^2. For phi(n)/n < 1/2: D/A = phi(n)^2 / (n*phi(n)*(2n+phi(n))) ~ phi(n)/(2n^2) < 1/(4n) which goes to 0. So D << A for composites with small phi(n)/n. The cross-term B is typically small for composites. Therefore DeltaW = A - B - C - D > 0."

# 10. Explicit formula connection to DeltaW
run "EXPLICIT_FORMULA_DELTAW" "DERIVE: How does the explicit formula M(x) = sum_rho x^rho/(rho*zeta'(rho)) - 2 + ... lead to a formula for DeltaW(p)? The four-term decomposition gives DeltaW(p) = A - B - C - D. The cross-term B involves sum D*delta which is related to M(p) via the Bridge Identity. Specifically: the Bridge Identity sum e^{2*pi*i*p*f} = M(p) + 2 connects the Farey exponential sum to M(p). And B can be written in terms of this exponential sum (via the Compact Cross-Term Formula). So B(p) ~ f(M(p)) for some function f. Since M(p) = sum_rho p^rho/(rho*zeta'(rho)) - 2, we get B(p) ~ sum_rho g(rho)*p^rho for some coefficients g(rho). This means DeltaW(p) oscillates with the zeta zeros through B. Derive the precise formula."

# 11. Prove GK concentration bound
run "GK_CONCENTRATION_BOUND" "PROVE: In F_p, the fractions with denominator b <= sqrt(p) (roughly the top 1/sqrt(p) fraction by denominator rank) contribute at least 90% of |sum D*delta|. The argument: |D(a/b)| ~ n/b for small b (large D). |delta(a/b)| ~ 1/b for small b. So |D*delta| ~ n/b^2 for denominator b. The total |D*delta| from denominator b is ~ phi(b)*n/b^2. Summing over b<=B: ~ n*sum_{b<=B} phi(b)/b^2 ~ n*(6/pi^2)*log(B). Total over all b<=p: ~ n*(6/pi^2)*log(p). Ratio: log(B)/log(p). For B=sqrt(p): log(sqrt(p))/log(p) = 1/2, giving 50% not 90%. Where does the 94% come from? The missing factor: |D*delta| is not uniform in a — the terms with a=1 (i.e., f=1/b) dominate within each denominator class."

# 12. Phase phi=5.28 derivation
run "PHASE_DERIVATION" "DERIVE the phase constant phi=5.28 in the sign pattern sgn(DeltaW(p)) ~ -sgn(cos(gamma_1*log(p) + phi)). From the explicit formula: M(p) ~ 2*Re(p^{rho_1}/(rho_1*zeta'(rho_1))). Write rho_1 = 1/2 + i*gamma_1. Then p^{rho_1} = sqrt(p)*e^{i*gamma_1*log(p)}. And 1/(rho_1*zeta'(rho_1)) = |c_1|*e^{i*alpha_1} where alpha_1 = -arg(rho_1) - arg(zeta'(rho_1)). So M(p) ~ 2*|c_1|*sqrt(p)*cos(gamma_1*log(p) + alpha_1). The observed phi=5.28 should equal alpha_1 = -arg(rho_1*zeta'(rho_1)). Compute: arg(rho_1) = arctan(gamma_1/(1/2)) = arctan(28.27) ~ pi/2 - 0.035. arg(zeta'(rho_1)) requires computing zeta'(rho_1). Does phi=5.28 match -arg(rho_1) - arg(zeta'(rho_1))?"

echo "=== Mega chain 35b complete $(date) ===" >> "$OUT/MEGA_CHAIN_LOG.md"
