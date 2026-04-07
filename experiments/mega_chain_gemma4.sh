#!/bin/bash
OLLAMA="http://localhost:11435/api/generate"
OUT="$HOME/Desktop/Farey-Local/experiments"

run() {
    local name="$1"; local prompt="$2"
    echo "$(date) Starting: $name" >> "$OUT/MEGA_CHAIN_LOG.md"
    curl -s "$OLLAMA" -d "{\"model\":\"gemma4:26b\",\"prompt\":\"$prompt\",\"stream\":false,\"options\":{\"num_ctx\":8192}}" 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('response','EMPTY'))" > "$OUT/${name}.md" 2>&1
    sz=$(wc -c < "$OUT/${name}.md")
    echo "$(date) Done: $name (${sz} bytes)" >> "$OUT/MEGA_CHAIN_LOG.md"
}

# 1. Horocycle equidistribution + Farey (retry — was empty)
run "HOROCYCLE_FAREY_RETRY" "Survey the connection between Farey sequences and horocycle equidistribution on the modular surface SL2(Z)\H. Key authors: Marklof, Strombergsson, Boca, Zaharescu. What is known about: (1) Farey fractions as orbits of horocycle flow, (2) equidistribution rate controlled by spectral gap of the Laplacian, (3) connection to Selberg eigenvalue conjecture, (4) any per-step analysis of equidistribution. References and key theorems."

# 2. Quantum ergodicity retry
run "QUANTUM_ERGODICITY_RETRY" "The Mertens spectroscope F(gamma)=gamma^2*|sum M(p)/p*exp(-igamma*log(p))|^2 detects zeta zeros. This connects to quantum chaos: (1) Berry-Keating conjecture says zeros are eigenvalues of operator H=xp. (2) The spectroscope computes spectral density from 'matrix elements' at primes. (3) Selberg trace formula relates eigenvalues to geodesics; our spectroscope relates zeros to primes. Formalize these connections. What would constitute a rigorous mathematical framework?"

# 3. Triangular distribution of delta (MPR-33)
run "TRIANGULAR_DELTA_PROOF" "The insertion shift delta(f) = f - {pf} for Farey fractions has an approximately triangular distribution. For f=a/b with gcd(a,b)=1, delta(a/b) = a/b - (pa mod b)/b. As p varies over primes, pa mod b is equidistributed mod b (by Dirichlet). So delta(a/b) = (a - pa mod b)/b takes values in [-1+1/b, 1-1/b] with a specific distribution. Prove: the distribution of delta over all fractions in F_{p-1} converges to the triangular distribution on [-1,1] as p->infinity. The key: for fixed b, the values {pa mod b : a coprime to b} are a permutation of {a : gcd(a,b)=1}."

# 4. Goldbach spectroscope implementation plan
run "GOLDBACH_IMPLEMENTATION_PLAN" "Design a computational test for a Goldbach spectroscope. r(2n) = number of representations of 2n as sum of two primes. The Hardy-Littlewood prediction gives r_pred(2n). Define error(n) = r(2n) - r_pred(2n). Compute F_G(gamma) = gamma^2 * |sum error(n)/n * exp(-igamma*log(n))|^2 for n=2,3,...,N. If the circle method is correct, peaks should appear at zeta zeros. Specify: what is the maximum N needed? How to compute r(2n) efficiently? What is the expected SNR? Feasibility for N=10^5, 10^6?"

# 5. Paper 2 introduction draft
run "PAPER2_INTRO_DRAFT" "Draft the introduction (Section 1) for Paper 2: The Compensated Mertens Spectroscope. Key points: (1) The classical Fourier duality between primes and zeta zeros (cite Csoka 2015, Van der Pol 1947, Planat). (2) What is new: the gamma^2 matched filter, local z-score, connection from Farey geometry, universality. (3) Main results: 20/20 zeros detected, GUE pair correlation RMSE=0.066, L-function extension (108 characters), Siegel zero sensitivity. (4) The paper is computational/experimental — we don't prove the spectroscope works, we demonstrate it. Write 500 words in LaTeX style."

# 6. Literature: Selberg's CLT and peak height distribution
run "SELBERG_CLT_DETAILED" "Selberg proved log|zeta(1/2+it)| is approximately normally distributed with mean 0 and variance (1/2)*log(log(T)). Does this constrain |zeta'(rho_k)| at the zeros? If zeta'(rho_k) = lim_{s->rho_k} (s-rho_k)/zeta(s), then |zeta'(rho_k)| is related to the local behavior of zeta near the zero. Selberg's CLT governs |zeta| ON the critical line between zeros, not AT zeros. But Farmer (1993) and Hughes-Keating (2000) study moments of |zeta'(rho)|. What do they find? Give the key results and how they might constrain our spectroscope peak heights."

# 7. Dressing up negative results for Paper 2
run "NEGATIVE_RESULTS_FRAMING" "Our spectroscope research produced several negative results that should be reported honestly: (1) Amplitude anti-correlates r=-0.44 with exact zeta'(rho_k). (2) Simple zeros test inconclusive at 10M (4/20, p=0.76). (3) Multi-taper destroys signal. (4) PRNG auditing infeasible (r=0.996 real vs fake). (5) Background z-scores decline at 50M primes. How should these be framed in a paper? Each negative result is informative — explain why. The amplitude failure reveals cross-zero interference. The simple zeros failure sets a lower bound on data needed. Multi-taper failure reveals coherent phase structure. Give suggested paragraph framings for each."

# 8. Lehmer phenomenon deep analysis
run "LEHMER_DEEP_ANALYSIS" "The Lehmer phenomenon: unusually close pairs of zeta zeros. The closest known pair around height T~7000 has spacing ~0.0001. Can our spectroscope detect Lehmer pairs? The spectroscope resolution at N primes to X is ~2pi/log(X). For X=10^6: resolution~0.46. For X=10^9: resolution~0.30. A Lehmer pair with spacing 0.01 would require resolution < 0.01, meaning log(X) > 628, or X > e^628 — impossible. So the spectroscope CANNOT resolve Lehmer pairs directly. However: Lehmer pairs should produce a characteristic BROADENED peak (two unresolved peaks merge). Can we detect this broadening? How does the kurtosis of a merged peak differ from a single peak?"

# 9. Mersenne prime phase prediction (MPR-43)
run "MERSENNE_PHASE_PREDICTION" "The Chebyshev bias sign pattern predicts sgn(DeltaW(p)) ~ -sgn(cos(gamma_1*log(p)+phi)) with phi=5.28, R=0.77. For Mersenne primes p = 2^n - 1, log(p) ~ n*log(2). The phase is gamma_1*n*log(2) + phi. Since gamma_1 = 14.1347 and log(2) = 0.6931: gamma_1*log(2) = 9.796. So the phase advances by ~9.8 radians per doubling of the exponent. For known Mersenne primes: M31 (p=2^31-1), M61, M89, M107, M127, M521, M607, M1279, M2203, M2281... Predict sgn(DeltaW) for each. Does the prediction match computation for small Mersenne primes?"

# 10. Explicit Ramanujan sum identities we use
run "RAMANUJAN_SUM_IDENTITIES" "List and prove all Ramanujan sum identities used in our paper. The Ramanujan sum c_b(m) = sum_{a=1,gcd(a,b)=1}^b e^{2*pi*i*m*a/b} satisfies: (1) c_b(m) = mu(b/gcd(b,m)) * phi(b)/phi(b/gcd(b,m)) for squarefree b. (2) For prime p and b<p: c_b(p) = mu(b). (3) sum_{b=1}^N c_b(m) = Ramanujan-type sum related to M(N). (4) The multiplicativity: c_{b1*b2}(m) = c_{b1}(m)*c_{b2}(m) when gcd(b1,b2)=1. Our Bridge Identity sum_{f in F_{p-1}} e^{2*pi*i*p*f} uses (2) and (3). Prove each identity from scratch."

echo "=== Mega chain gemma4 complete $(date) ===" >> "$OUT/MEGA_CHAIN_LOG.md"
