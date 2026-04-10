#!/bin/bash
OUT="$HOME/Desktop/Farey-Local/experiments"
LOG="$OUT/REMOTE_QUEUE_LOG.md"

run_remote() {
    local name="$1"; local prompt="$2"
    echo "$(date) Starting: $name" >> "$LOG"
    ~/bin/remote_ollama.sh qwen3.5:35b "$name" "$prompt"
    echo "$(date) Done: $name ($(wc -c < "$OUT/${name}.md") bytes)" >> "$LOG"
}

echo "=== Remote M1 Max Queue $(date) ===" > "$LOG"

# 1. Fix 30-zero extension (crashed on local)
run_remote "REMOTE_30_ZEROS_ANALYSIS" "We tried to detect 30 zeta zeros using the compensated Mertens spectroscope at 10M primes. The code crashed. Analyze theoretically: with 664K primes to 10M, resolution is 2pi/log(10^7) = 0.39. Zero spacings gamma_21-gamma_30 range from 1.6 to 3.5. All resolvable. But the local z-score test found 0/30 detected. Why? Possible reasons: (1) Code bug (most likely). (2) Background growth overwhelming at 10M. (3) The gamma^2 compensation insufficient for zeros above gamma_20. (4) Need stronger compensation (higher alpha). Analyze which is most likely and propose the fix."

# 2. Three-body spectroscope theory
run_remote "REMOTE_3BP_SPECTROSCOPE_THEORY" "Can a spectroscope detect three-body orbit periods? The Li-Liao catalog has 695 orbits with periods T_k. If we compute F(omega) = |sum w_k * exp(-i*omega*log(T_k))|^2, would peaks appear at meaningful frequencies? Unlike the Mertens spectroscope where the explicit formula guarantees peaks at zeros, there is NO explicit formula for three-body orbits. However: (1) The braid group structure might impose algebraic constraints on period ratios. (2) KAM theory predicts resonances at rational frequency ratios. (3) The CF structure we found organizes orbits by algebraic complexity. Could peaks in the period spectroscope correspond to resonance frequencies? Analyze."

# 3. Universality — can we weaken GRH?
run_remote "REMOTE_UNIVERSALITY_WEAKEN_GRH" "Our universality proof requires GRH+LI+regularity. The Vinogradov-Korobov bound closes gaps 1-2. Can we weaken GRH to something less? Options: (1) Replace GRH with density hypothesis (weaker). (2) Use Selberg's unconditional result (positive proportion on critical line). (3) Use zero-free region (classical, unconditional) instead of all-zeros-on-line. (4) Prove for gamma_1 only (just the first zero) — this might need only PNT. Which weakening is feasible? Derive the weakest hypothesis that still gives universality for gamma_1."

# 4. Chowla — formalize for paper
run_remote "REMOTE_CHOWLA_PAPER_SECTION" "Write a paper section (1500 words) on our Chowla spectroscopic test. Title: Spectroscopic Test for the Chowla Conjecture with Detection Thresholds. Content: (1) Define the test: compute mu(n) periodogram, normalize by |1/zeta(1+igamma)|^2, check residual flatness. (2) Result: CV=1.47%, 78x flatter than null, consistent with Chowla at N=200K. (3) Detection threshold: epsilon_min = 1.824/sqrt(N). At N=200K rules out epsilon>0.004. (4) The false alarm: unnormalized residual showed structure from |1/zeta| envelope. (5) Unweighted test with sigma=0.1 smoothing also consistent. (6) Direct lag-h test: sqrt(N) cancellation confirmed. Write in LaTeX-ready mathematical prose."

# 5. Network security — deeper analysis
run_remote "REMOTE_NETWORK_SECURITY_DEEPER" "Our per-IP spectral anomaly detector works (z>4 for botnet C2, z>4 for exfil beacon). But f^2 compensation adds only marginal value over standard LS. Question: what IS the unique value proposition? (1) The per-IP spectroscope approach itself (regardless of f^2) — is this novel in network security? (2) The local z-score normalization — does any SIEM use this? (3) Timing-based detection (not payload-based) — what is the state of the art? (4) Could we patent the PER-IP SPECTRAL FINGERPRINTING method specifically? Not the f^2 part (that's pre-whitening) but the architecture: decompose traffic by source IP, compute periodogram per IP, flag periodic anomalies. Is this novel?"

# 6. Paper 2 — integrate phase phi result
run_remote "REMOTE_PAPER2_PHASE_PHI" "Write the phase phi section for Paper 2. Our discovery: the phase constant phi=5.28 in sgn(DeltaW(p)) ~ -sgn(cos(gamma_1*log(p)+phi)) is derived from first principles. phi = -arg(rho_1 * zeta'(rho_1)) = -1.69 (mod 2pi = 5.28). Computed via mpmath: zeta'(rho_1) = 0.783+0.125i. This means the explicit formula predicts BOTH frequency AND phase of the Chebyshev bias oscillation. Significance: the last free parameter in our model is now derived. Write as a subsection of the Chebyshev bias section. Include the computation, the mod-2pi resolution, and the significance."

# 7. Dedekind — ergodic approach
run_remote "REMOTE_DEDEKIND_ERGODIC" "Fresh approach to proving B>0 using ergodic theory. The map f -> {pf} on [0,1] is ergodic (equidistributed mod 1 for p prime, by Weyl). The sum B = (2/n'^2)*sum D(f)*delta(f) where delta(f)=f-{pf}. This is a Birkhoff sum of the observable g(f,{pf}) = D(f)*(f-{pf}) along the orbit of the map T:f->{pf}. By the ergodic theorem, (1/N)*sum g(f_i, T(f_i)) -> integral g(x,y) d(mu) where mu is the invariant measure. Compute: what is the integral? If it's positive, then B>0 for almost all primes (density 1). The invariant measure of f->{pf} on Farey fractions is related to the hyperbolic measure on the modular surface. Derive."

# 8. Grant proposal draft
run_remote "REMOTE_GRANT_PROPOSAL" "Draft a 3-page grant proposal for Simons Collaboration Grant for Mathematicians. Title: Spectral Detection of L-Function Zeros from Arithmetic Data. PI: Saar Shai (independent researcher). Results: (1) 20/20 zero detection via compensated spectroscope (novel). (2) Universality (any 2750 primes, novel). (3) GUE RMSE=0.066 from arithmetic data (novel). (4) Phase phi derived exactly (novel). (5) Chowla spectroscopic test with thresholds (novel methodology). (6) 422 Lean-verified results (novel formalization). (7) Three-body periodic table (695 orbits). Proposed: extend universality proof, Chowla at larger N, automorphic L-functions, GRH verification pipeline. Budget: $8,400/year. Note: Simons allows independent researchers."

echo "=== Remote queue complete $(date) ===" >> "$LOG"
