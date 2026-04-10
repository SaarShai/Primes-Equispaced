#!/bin/bash
OUT="$HOME/Desktop/Farey-Local/experiments"
LOG="$OUT/REMOTE_QUEUE_LOG.md"

run_remote() {
    local name="$1"; local prompt="$2"
    echo "$(date) Starting: $name" >> "$LOG"
    ~/bin/remote_ollama.sh qwen3.5:35b "$name" "$prompt"
    echo "$(date) Done: $name ($(wc -c < "$OUT/${name}.md") bytes)" >> "$LOG"
}

echo "=== Remote Queue 4 $(date) ===" >> "$LOG"

run_remote "REMOTE_SPECTROSCOPE_OPTIMAL_WEIGHTS" "What is the OPTIMAL weight function w(p) for the spectroscope F(gamma) = gamma^2 * |sum w(p) * exp(-igamma*log(p))|^2? We tested: M(p)/p (standard), M(p)/sqrt(p) (1.7x better z-score), psi(p)-p (edges out Mertens for high zeros), unit weight (surprisingly good). Derive the theoretically optimal w(p) that maximizes SNR at a target zero gamma_j. Under the explicit formula, the optimal matched filter should be w(p) = conjugate of the expected signal. The expected signal at gamma_j is c_j * p^{igamma_j - 1/2}. So optimal w(p) = p^{-igamma_j + 1/2} / |c_j|. But this requires knowing gamma_j in advance. For a BLIND search (unknown gamma), what is optimal?"

run_remote "REMOTE_MERTENS_FUNCTION_DEEP" "Deep analysis of the Mertens function M(x). We use M(p) at primes as our spectroscope input. Key facts: (1) M(x) = O(x^{1/2+epsilon}) under RH. (2) M(x)/sqrt(x) is unbounded (Ingham). (3) The Mertens conjecture |M(x)| < sqrt(x) is FALSE (Odlyzko-te Riele 1985). (4) The first sign change of M(x)/sqrt(x) - 1 is unknown. Questions for our research: (a) What is the distribution of M(p)/sqrt(p) over primes? Is it Gaussian? (b) How does the autocorrelation of M(p) decay? (c) Can we detect the Odlyzko-te Riele counterexample computationally via our spectroscope?"

run_remote "REMOTE_FAREY_MEDIANT_APPLICATIONS" "The Farey mediant (a+c)/(b+d) is the simplest fraction between a/b and c/d. After adversarial review, most 'applications' were killed (IoT=TDMA, adaptive sampling=standard quadrature, Nanite=geometry-blind). What applications GENUINELY use the mediant property specifically? (1) Stern-Brocot tree for exact rational arithmetic. (2) Continued fraction computation. (3) Best rational approximation (convergents). (4) Clock synchronization in distributed systems (Ford circles). (5) Musical tuning theory (just intonation ratios). For each: is there an UNMET NEED where the mediant property provides genuine value over existing solutions?"

run_remote "REMOTE_PAPER1_STRENGTHEN" "Our Paper 1 reviewer wanted a rigorous proof connecting DeltaW to zeros. We added a GRH-conditional section. What ELSE can we strengthen? (1) The four-term decomposition proof is Lean-verified but could the PAPER proof be clearer? (2) The spectroscope section claims 3 zeros detected — should we update to 20 zeros (with the gamma^2 filter from Paper 2)? Or keep Paper 1 conservative? (3) The Chebyshev bias correlation R=0.77 — should we add the phase phi=5.28 derivation? (4) Should we cite the Chowla result? (5) How to handle the 422 vs 258 Lean result count? Recommend specific improvements."

run_remote "REMOTE_ARITHMETIC_QUANTUM_GRAVITY" "Speculative: connections between our Farey research and physics. (1) The Farey tessellation tiles the hyperbolic plane. This is the same geometry as AdS space in string theory. (2) Zeta zeros ↔ energy levels of a quantum system (Berry-Keating). Our spectroscope detects these 'energy levels' from 'scattering data' (primes). (3) The modular group SL2(Z) is the mapping class group of the torus — relevant to topological quantum field theory. (4) Our GUE result connects to random matrix theory, which also describes quantum chaos. Are these connections deep or superficial? Could our computational results contribute to quantum gravity research?"

run_remote "REMOTE_WHAT_WOULD_RAMANUJAN_DO" "Ramanujan discovered deep patterns in number theory through numerical experimentation — exactly our approach. Our spectroscope is a computational tool for discovering number-theoretic patterns. What patterns have we NOT looked for? (1) Partition function p(n) — does its spectroscope show modular form zeros? (2) Divisor function sigma(n) — does its spectroscope show Eisenstein series zeros? (3) Prime gaps g_n = p_{n+1} - p_n — does the gap spectroscope show structure? (4) Euler phi function — does its spectroscope connect to Dirichlet L-functions differently than mu(n)? Suggest 5 arithmetic functions whose spectroscope we should compute."

run_remote "REMOTE_COMPUTATIONAL_CHALLENGES" "What are the current OPEN COMPUTATIONAL CHALLENGES in number theory that our tools might address? (1) LMFDB has gaps in its L-function database — can our spectroscope fill them? (2) Verify zeros of degree-2 L-functions (more exotic than Dirichlet). (3) Test the ratio conjecture computationally. (4) Compute pair correlation statistics for L-function families. (5) Verify the Katz-Sarnak symmetry type predictions for specific families. For each: what data do we need, what computation, and would a contribution be valued?"

run_remote "REMOTE_GRANT_NSF_DMS" "Draft a 2-page NSF DMS (Computational Mathematics) proposal. Title: Spectroscopic Methods for L-Function Zero Detection and Verification. Emphasis: computational methodology, not pure theory. Key innovations: (1) Compensated periodogram with alpha-tunable pre-whitening. (2) Local z-score normalization. (3) Universality theorem (conditional). (4) Chowla spectroscopic test with detection thresholds. (5) 422 Lean-verified identities. (6) GRH verification pipeline for 17 characters. Proposed: extend to degree-2 L-functions, formalize Lean library for Mathlib, scale to N=10^8. Budget: $150K/2yr. Target: DMS-2400000 series."

echo "=== Remote Queue 4 complete $(date) ===" >> "$LOG"
