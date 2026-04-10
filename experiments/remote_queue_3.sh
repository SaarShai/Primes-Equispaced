#!/bin/bash
OUT="$HOME/Desktop/Farey-Local/experiments"
LOG="$OUT/REMOTE_QUEUE_LOG.md"

run_remote() {
    local name="$1"; local prompt="$2"
    echo "$(date) Starting: $name" >> "$LOG"
    ~/bin/remote_ollama.sh qwen3.5:35b "$name" "$prompt"
    echo "$(date) Done: $name ($(wc -c < "$OUT/${name}.md") bytes)" >> "$LOG"
}

echo "=== Remote Queue 3 $(date) ===" >> "$LOG"

# Research: what have others done recently?
run_remote "REMOTE_RECENT_FAREY_PAPERS_2024_2025" "Survey recent papers (2024-2025) on Farey sequences, Mertens function, and computational zeta zero detection. What new results exist? Key questions: (1) Has anyone else built a spectroscope-like tool since Csoka 2015? (2) Any new Farey discrepancy results beyond the MMD paper (2407.10214)? (3) Any new Lean/formal verification of number theory results? (4) Any new connections between Farey and RMT? (5) Has Tomas Garcia (2025) published follow-ups? (6) Any new results on Chowla conjecture computations? List papers with authors, dates, key results."

# Research: what theorems could we prove next?
run_remote "REMOTE_NEXT_PROVABLE_THEOREMS" "Given our tools (spectroscope, universality, 422 Lean results, four-term decomposition), what NEW THEOREMS could we realistically prove? Not conjectures — actual provable statements. Candidates: (1) The universality theorem (conditional on GRH+LI+VK — we have the proof). (2) The phase phi derivation (exact computation, not a theorem per se). (3) D(1/p) = 1 - |F_p|/p (already proved). (4) Composite healing for phi(n)/n < 1/2 (proof sketch exists). (5) Spectral positivity sum c_b(p)^2 * phi(b)/b^2 >= c*log(p) (computable). (6) Chowla detection threshold epsilon_min = 1.824/sqrt(N) (derivation complete). Which are closest to publishable proofs? Which would have the most impact?"

# Research: connections to other fields
run_remote "REMOTE_CROSS_FIELD_CONNECTIONS" "What connections exist between our discoveries and other mathematical fields? (1) Dynamical systems: the map f->{pf} is studied in ergodic theory. Our DeltaW is a Birkhoff observable. Connection to mixing rates? (2) Algebraic geometry: Farey tessellation = fundamental domain of SL2(Z). Our spectroscope operates on this tessellation. Connection to modular forms? (3) Probability: M(p)/sqrt(p) is a martingale-like object. Our universality says any subsequence preserves the 'information'. Connection to martingale convergence? (4) Information theory: universality implies redundancy — the zero information is distributed holographically. Connection to erasure codes? (5) Category theory: the Farey sequence has a natural categorical structure (Stern-Brocot as a free monoid). Any categorical interpretation of our results?"

# 3BP deeper analysis
run_remote "REMOTE_3BP_CF_STABILITY_PROOF" "In our three-body periodic table, nobility (fraction of CF partial quotients = 1) anticorrelates with braid entropy at rho=-0.890. Can this be PROVED? The argument: (1) High nobility means the CF is close to the golden ratio [1,1,1,...]. (2) The golden ratio is the 'most irrational' number (hardest to approximate). (3) In dynamical systems, 'most irrational' rotation numbers correspond to the most stable orbits (KAM theory). (4) Braid entropy measures topological complexity. (5) Therefore: high nobility -> most irrational -> most stable -> low entropy. Can this chain be made rigorous? What would the theorem statement look like?"

# Research: what would make our work more impactful?
run_remote "REMOTE_IMPACT_MAXIMIZATION" "Our work has: (1) two paper drafts, (2) 422 Lean results, (3) interactive demos, (4) a spectroscope tool, (5) Chowla test methodology, (6) three-body periodic table. What would make the MAXIMUM IMPACT in the math community? Options: (A) Submit both papers to high-profile journals (Experimental Math, Math Comp). (B) Give talks at conferences (JMM, ICERM workshops). (C) Contribute Lean library to Mathlib (permanent infrastructure). (D) Create a website with interactive demos + papers. (E) Collaborate with established researchers (Rubinstein, Booker, Soundararajan). (F) Write a survey/expository article for a wider audience (Notices of the AMS, Math Intelligencer). Rank by impact-per-effort. What would get us cited?"

# Research: extend Lean formalization
run_remote "REMOTE_LEAN_NEXT_FORMALIZATIONS" "We have 422 Lean 4 results about Farey sequences. What should we formalize NEXT? Candidates ordered by value to Mathlib: (1) The universality theorem (conditional — Lean can handle conditional proofs). (2) The Chowla detection threshold formula. (3) The compensation bound gamma^2/(1/4+gamma^2) in [4/5,1). (4) The phase phi = -arg(rho_1*zeta'(rho_1)) (this requires complex analysis in Lean). (5) The GUE pair correlation connection (too vague for Lean). (6) Additional Ramanujan sum identities. Which are feasible in Lean 4 with current Mathlib? Which would be most impressive as a contribution?"

# Research: Selberg trace formula connection
run_remote "REMOTE_SELBERG_TRACE_DEEP" "Deep analysis: is our spectroscope a disguised Selberg trace formula? The Selberg trace formula for the modular surface Gamma\H relates: SPECTRAL SIDE: sum over eigenvalues lambda_k of the Laplacian. GEOMETRIC SIDE: sum over closed geodesics (which correspond to hyperbolic conjugacy classes in SL2(Z)). Our spectroscope: SPECTRAL SIDE: peaks at zeta zeros gamma_k. DATA SIDE: sum over primes (with Mertens weights). The prime p corresponds to the hyperbolic element [[p,0],[0,1]] in GL2. Is there a RIGOROUS mapping from our spectroscope to the Selberg trace formula? If so, our computational results would have immediate spectral-theoretic significance."

# Research: what do established experts think?
run_remote "REMOTE_EXPERT_PREDICTIONS" "Predict how established experts would react to our work. (1) Andrew Odlyzko (zeta zero computation): would likely say our spectroscope is 'a nice illustration of the explicit formula' but computationally inferior to Riemann-Siegel. What would change his mind? (2) Peter Sarnak (Mobius disjointness): would be interested in our Chowla test methodology. What would he want to see? (3) Michael Rubinstein (L-function computation): would care about the GRH verification pipeline. What precision would impress him? (4) Terence Tao (Chowla/Sarnak): would want the detection threshold formalized. Is our epsilon_min derivation rigorous enough? (5) Brian Karis (Nanite): would want 3D mesh demo, not theory. We showed 0 cracks on icosphere — enough? For each: what would make them take notice?"

# Research: three-body paper improvements
run_remote "REMOTE_3BP_PAPER_IMPROVEMENTS" "Our three-body paper needs strengthening before submission. Current weaknesses: (1) 0/4199 empty-cell predictions validated. (2) Hristov test showed CF-nobility fails for free-fall orbits. (3) Nobility has rho=0.994 with geometric mean (nearly redundant). (4) The 'periodic table' organization is novel visualization but unclear if it provides PREDICTIVE power. What improvements would make the paper stronger? Ideas: (A) Test on Li-Liao extended catalog (if newer data exists). (B) Use different CF invariants (e.g., Lyapunov exponent of the CF map). (C) Machine learning: can CF features predict stability better than nobility alone? (D) Test on figure-eight family perturbations (where we have exact golden ratio)."

# Research: can we connect spectroscope to quantum computing?
run_remote "REMOTE_QUANTUM_SPECTROSCOPE" "Shor's algorithm uses continued fractions (= Farey structure) in its classical post-processing. Our spectroscope detects eigenvalues from data. Quantum phase estimation (QPE) also detects eigenvalues from data (quantum data). Question: is there a FORMAL connection between our classical spectroscope and QPE? Both: (1) take a function evaluated at specific points (primes / quantum states), (2) compute a Fourier transform, (3) peaks correspond to eigenvalues. If we could show our spectroscope is the 'classical limit' of QPE applied to the Riemann zeta operator (Berry-Keating), that would bridge our work to quantum computing. Is this feasible or fantasy?"

echo "=== Remote Queue 3 complete $(date) ===" >> "$LOG"
