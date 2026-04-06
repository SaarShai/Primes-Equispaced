#!/bin/bash
OLLAMA="http://localhost:11435/api/generate"
OUT="$HOME/Desktop/Farey-Local/experiments"
CTX="$HOME/Desktop/Farey-Local/model_context/SHARED_CONTEXT.md"

run() {
    local name="$1"; local prompt="$2"
    echo "$(date) Starting: $name" >> "$OUT/SPRINT_LOG.md"
    curl -s "$OLLAMA" -d "{\"model\":\"qwen3.5:35b\",\"prompt\":\"$prompt\",\"stream\":false,\"options\":{\"num_ctx\":8192}}" 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('response','EMPTY'))" > "$OUT/${name}.md" 2>&1
    echo "$(date) Done: $name ($(wc -c < "$OUT/${name}.md") bytes)" >> "$OUT/SPRINT_LOG.md"
}

echo "=== Sprint started $(date) ===" > "$OUT/SPRINT_LOG.md"

# MPR-40: Reconcile phase constant rho vs rho-1
run "PHASE_CONSTANT_RECONCILE" "The explicit formula for M(x) involves coefficients at each zero rho of zeta(s). Two versions exist: (A) c_rho = x^rho/(rho*zeta'(rho)) from direct Perron integral of 1/zeta(s), (B) c_rho = x^rho/((rho-1)*zeta'(rho)) from some other derivations. Which is correct? Derive carefully from the Perron formula: M(x) = (1/2pi*i) * integral_{c-iT}^{c+iT} (1/zeta(s)) * x^s/s ds. The residue at s=rho (simple zero of zeta) is x^rho/(rho*zeta'(rho)). But some sources write the explicit formula for the summatory Mobius as M(x) = sum_rho x^rho/(rho*zeta'(rho)) - 2 + sum_k x^{-2k}/((-2k)*zeta'(-2k)). Verify: is the coefficient 1/(rho*zeta'(rho)) or 1/((rho-1)*zeta'(rho))? The 1/(rho-1) version would come from the Perron formula for sum mu(n)/n, not sum mu(n). Clarify which formula applies to M(x) vs M_1(x)=sum_{n<=x} mu(n)/n."

# MPR-58: Prove R2>0 via Dedekind sum structure
run "R2_DEDEKIND_PROOF" "PROOF ATTEMPT: The damage/response ratio R(p) = sum D(f)*delta(f) / sum delta(f)^2 is positive for all primes with M(p)<=-3 (verified to p=100000). The Permutation Square-Sum Identity gives B+C = delta^2*(1+2R), so R>-1/2 iff B+C>0. We know C>0 always (strict positivity of shift-squared sum, proved in Lean). The cross-term B = (2/n'^2)*sum D*delta decomposes by denominator: B = sum_b B_b where B_b = sum_{a:gcd(a,b)=1} D(a/b)*delta(a/b). For fixed b, delta(a/b) = a/b - {pa/b} involves a Dedekind sum structure. The key identity: T_b(p) - E[T_b] = b^2 * sum_{c|b} mu(b/c)*s(p,c) where s(p,c) is the classical Dedekind sum. Can we bound sum_b B_b from below using the Weil bound |s(p,c)| < c*log(c)/12? The challenge: the Weil bound on individual Dedekind sums doesn't directly give the sign of the aggregate sum over all denominators."

# MPR-47: Gauss-Kuzmin concentration proof
run "GK_CONCENTRATION_RIGOROUS" "PROOF: In the Farey sequence F_p, the top 20% of fractions (by |D*delta|) contribute 94% of the total |sum D*delta|. This concentration follows from the Gauss-Kuzmin law: fractions with small denominators b have |D(a/b)| ~ n*a/b which is O(n/b), and |delta(a/b)| ~ 1/b. So |D*delta| ~ n/b^2 for small b. The total |D*delta| is dominated by fractions with b = O(sqrt(p)) (the top ~sqrt(p)/p ~ 1/sqrt(p) fraction of all fractions). More precisely, by BCZ (Boca-Cobeli-Zaharescu 2001), Farey fractions with denominator b have spacing statistics governed by the density g(b/N). Can we use BCZ to prove the 94% concentration rigorously? The key: sum_{b<=B} phi(b)/b^2 ~ (6/pi^2)*log(B) + C, so the contribution from small b grows logarithmically."

# MPR-27: Verify corrected coefficient numerically
run "COEFFICIENT_NUMERICAL_CHECK" "NUMERICAL TASK: The spectroscope uses weights M(p)/p. The explicit formula gives M(x) ~ sum_rho x^rho/(rho*zeta'(rho)). For the spectroscope, the effective weight at prime p is M(p)/p ~ sum_rho p^{rho-1}/(rho*zeta'(rho)) = sum_rho p^{-1/2+igamma_k}/(rho_k*zeta'(rho_k)). At gamma=gamma_j, the on-resonance term contributes c_j*sum_p p^{-1/2}/p = c_j*sum 1/p^{3/2}. But our spectroscope divides by sqrt(p) again (inside the periodogram), giving effective amplitude M(p)/p / sqrt(p) = M(p)/p^{3/2}. From explicit formula: ~ sum_rho p^{rho-1-1/2}/(rho*zeta'(rho)) = sum_rho p^{igamma_k - 1}/(rho_k*zeta'(rho_k)). So the coefficient IS 1/(rho*zeta'(rho)), not 1/((rho-1)*zeta'(rho)). Confirm this is consistent with our observed spectroscope behavior."

# MPR-24: Composite healing analytical bound
run "COMPOSITE_HEALING_BOUND" "PROOF: 95.4% of composites have DeltaW(n)>0 (they improve Farey uniformity). Prove: for composite n with phi(n)/n < 1/2 (which holds for most composites), DeltaW(n) > 0. Key argument: when n is composite, only phi(n) new fractions enter F_n (vs n-1 for prime n). The dilution term A scales as phi(n)*(1/n^2 - 1/n'^2) ~ phi(n)/n^3. The new-fraction discrepancy D scales as phi(n)^2/n'^2 ~ (phi(n)/n)^2. For phi(n)/n < 1/2, the new-fraction damage is relatively small compared to dilution, so DeltaW > 0. Make this rigorous."

# MPR-44: Quantum ergodicity formalization
run "QUANTUM_ERGODICITY_FORMAL" "The spectroscope F(gamma) = gamma^2*|sum M(p)/p*exp(-igamma*log(p))|^2 detects zeta zeros. This connects to quantum ergodicity via: (1) Farey fractions equidistribute on the modular surface SL2(Z)\\H. (2) The per-step discrepancy DeltaW measures the rate of equidistribution. (3) Zeta zeros control this rate via the explicit formula. (4) The spectroscope extracts the spectral content. This is analogous to the quantum unique ergodicity (QUE) conjecture for Maass forms, where eigenvalues of the Laplacian control equidistribution rates. Formalize: what is the precise mathematical statement connecting our spectroscope to the spectral theory of the modular surface? Is DeltaW related to the Selberg/Eisenstein spectrum?"

echo "=== Sprint 35b complete $(date) ===" >> "$OUT/SPRINT_LOG.md"
