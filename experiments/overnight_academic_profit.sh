#!/bin/bash
OLLAMA="http://localhost:11435/api/generate"
OUT="$HOME/Desktop/Farey-Local/experiments"

run35b() {
    local name="$1"; local prompt="$2"
    echo "$(date) Starting: $name" >> "$OUT/OVERNIGHT_ACADEMIC_PROFIT_LOG.md"
    curl -s "$OLLAMA" -d "{\"model\":\"qwen3.5:35b\",\"prompt\":\"$prompt\",\"stream\":false,\"options\":{\"num_ctx\":8192}}" 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('response','EMPTY'))" > "$OUT/${name}.md" 2>&1
    echo "$(date) Done: $name ($(wc -c < "$OUT/${name}.md") bytes)" >> "$OUT/OVERNIGHT_ACADEMIC_PROFIT_LOG.md"
}

rung4() {
    local name="$1"; local prompt="$2"
    echo "$(date) Starting: $name" >> "$OUT/OVERNIGHT_ACADEMIC_PROFIT_LOG.md"
    curl -s "$OLLAMA" -d "{\"model\":\"gemma4:26b\",\"prompt\":\"$prompt\",\"stream\":false,\"options\":{\"num_ctx\":8192}}" 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('response','EMPTY'))" > "$OUT/${name}.md" 2>&1
    echo "$(date) Done: $name ($(wc -c < "$OUT/${name}.md") bytes)" >> "$OUT/OVERNIGHT_ACADEMIC_PROFIT_LOG.md"
}

# Code agent for computational tasks
run_code() {
    local name="$1"; local prompt="$2"
    echo "$(date) Starting code: $name" >> "$OUT/OVERNIGHT_ACADEMIC_PROFIT_LOG.md"
    ~/bin/local_code_agent.sh qwen3.5:35b "$name" "$prompt"
    echo "$(date) Done code: $name" >> "$OUT/OVERNIGHT_ACADEMIC_PROFIT_LOG.md"
}

echo "=== Overnight Academic+Profit started $(date) ===" > "$OUT/OVERNIGHT_ACADEMIC_PROFIT_LOG.md"

# ===== ACADEMIC: Paper preparation =====

# 1. Paper 1 final review checklist
run35b "PAPER1_FINAL_CHECKLIST" "Create a final checklist for submitting our paper 'The Geometric Signature of Primes in Farey Sequences' to arXiv. The paper introduces per-step Farey discrepancy DeltaW(N), proves exact identities (bridge, injection, four-term decomposition), shows Chebyshev bias correlation R=0.77, and detects 3 zeta zeros via spectroscope. All identities verified in Lean 4 (422 results, 0 sorry). Checklist items: (1) Abstract clear? (2) All terms defined before use? (3) All proofs complete? (4) Figures referenced correctly? (5) Bibliography complete? (6) MSC codes correct? (7) AI disclosure present? (8) Any overclaiming? (9) What arXiv categories? math.NT primary, math.CO secondary? (10) What endorsement is needed?"

# 2. Mathlib PR strategy — which files first
run35b "MATHLIB_PR_STRATEGY" "We have 15 Lean 4 files with 422 results about Farey sequences. Mathlib has NO Farey sequence content. Strategy for contributing: (1) Which file to submit FIRST as the smallest useful PR? Probably the Farey sequence definition + cardinality formula from PrimeCircle.lean. (2) What Mathlib naming conventions must we follow? (3) How to handle native_decide results (Mathlib prefers tactic proofs)? (4) Should we submit one large PR or many small ones? (5) Who reviews number theory PRs in Mathlib? (6) What is the expected review timeline? (7) How to handle our custom definitions that may conflict with existing Mathlib types?"

# 3. Paper 2 detailed structure
run35b "PAPER2_DETAILED_STRUCTURE" "Design the detailed structure for Paper 2: The Compensated Mertens Spectroscope. Key results: (1) gamma^2 matched filter = pre-whitening applied to number-theoretic periodogram (MUST cite classical pre-whitening). (2) 20/20 zero detection with local z-scores. (3) Universality: any 2750 primes suffice. (4) Psi spectroscope edges Mertens for higher zeros. (5) GUE pair correlation RMSE=0.066. (6) L-function extension (108 characters). (7) Siegel zero sensitivity (465M sigma). (8) Amplitude anti-correlates (honest negative). (9) Simple zeros test inconclusive (honest negative). For each result: which section? How long? What figures? What honest caveats?"

# ===== PROFIT EXPLORATION: Where can we take research further =====

# 4. Cryptographic applications deep dive
run35b "CRYPTO_APPLICATIONS_DEEP" "Our spectroscope detects hidden periodic structure in arithmetic sequences. Could this be valuable for cryptography? (1) RSA relies on the difficulty of factoring N=pq. The primes p,q have specific relationships to zeta zeros. Could spectroscopic analysis of RSA moduli reveal information about the factors? (2) Elliptic curve cryptography uses curves over finite fields. Farey sequences connect to modular forms. Is there a spectroscopic attack on ECDLP? (3) Lattice-based crypto (post-quantum) uses structured lattices. Farey mediants are lattice-like (Stern-Brocot tree = lattice basis). Any connection? (4) Hash function design: could Farey-based hash functions have provable distribution properties? (5) Zero-knowledge proofs: our Lean 4 verified identities could serve as ZK circuits. Assess each for feasibility and potential."

# 5. Quantum computing applications
run35b "QUANTUM_COMPUTING_APPS" "Connections between our Farey discoveries and quantum computing: (1) Shor's algorithm uses continued fractions (closely related to Farey sequences) in its classical post-processing. Could our spectroscope improve the classical part of Shor's? (2) Quantum phase estimation produces rational approximations — literally Farey fractions. Could our injection principle optimize quantum phase estimation circuits? (3) VQE (variational quantum eigensolver) needs good parameter initialization. Farey-spaced parameters give optimal gap-filling exploration of parameter space. (4) Quantum error correction codes have connections to number theory. Any link to our identities? (5) The Farey spectroscope detects eigenvalues from data — similar to quantum spectroscopy. Is there a quantum speedup for our spectroscope? Assess each honestly."

# 6. Where to extend research for profit
run35b "RESEARCH_PROFIT_DIRECTIONS" "We have these mathematical tools: (A) Per-step discrepancy tracking — measuring how adding one element changes distribution uniformity. (B) Injection principle — deterministic optimal gap-filling. (C) Spectral compensation (f^alpha pre-whitening) for colored-noise detection. (D) Universality — any subset encodes the full spectral content. (E) 422 Lean-verified Farey identities. For each tool, brainstorm: what UNSOLVED ENGINEERING PROBLEM could this help with? Think beyond number theory. Think: optimization, scheduling, resource allocation, signal processing, machine learning, data structures, compression, networking. For each idea: who would pay for it? How much? What would the product look like? Be creative but honest — mark speculative ideas as such."

# ===== GEMMA4: Literature + market research =====

# 7. Companies working on problems our tools could solve
rung4 "TARGET_COMPANIES_RESEARCH" "Research companies that work on problems where Farey sequence mathematics might help. Categories: (1) Spectral analysis companies (astronomical surveys, medical imaging, vibration analysis). (2) Mesh/geometry companies (Altair, ANSYS, Epic Games, Pixar, Adobe). (3) Optimization companies (Gurobi, CPLEX, Google OR-Tools). (4) Cryptography companies (CertiK, Trail of Bits, NCC Group). (5) Quant finance firms (Two Sigma, Citadel, Jane Street). (6) Semiconductor companies doing computational lithography (ASML, Synopsys). For each category: what specific problems do they face that have any connection to equidistribution, gap-filling, rational approximation, or spectral analysis of arithmetic data?"

# 8. Grant opportunities
rung4 "GRANT_OPPORTUNITIES" "Research grant opportunities for Farey sequence / number theory research with computational applications. Categories: (1) NSF (which programs fund computational number theory?). (2) DARPA (any programs on mathematical foundations for computing?). (3) Simons Foundation (which grants fund independent researchers?). (4) Clay Mathematics Institute. (5) European Research Council (if applicable). (6) Private foundations (Kavli, Sloan). For each: eligibility for an independent researcher (no university affiliation), typical grant size, application process, relevant program areas. Also: are there prizes for computational discoveries in number theory?"

# 9. Monetizable mathematical services
rung4 "MATH_SERVICES_MARKET" "What mathematical consulting services can an independent number theory researcher sell? (1) Formal verification consulting — we have 422 Lean results. Companies like Galois, Certik, Trail of Bits pay for formal verification. Can we sell Lean 4 consulting? (2) Algorithm consulting for quant finance — equidistribution theory is relevant to sampling, Monte Carlo, risk modeling. (3) Cryptographic auditing — Farey/number theory expertise for reviewing crypto implementations. (4) Expert witness — mathematical expert testimony in IP disputes. (5) Technical writing — math textbook chapters, review articles. For each: typical rates, how to find clients, what credentials matter."

# 10. Education and content monetization
rung4 "EDUCATION_MONETIZATION" "How to monetize mathematical education content based on our research: (1) Online course: 'Computational Number Theory with Python' using spectroscope as capstone project. Platforms: Udemy ($10-50/student), Coursera (need university partner), self-hosted ($100-500/student). (2) YouTube channel: 'Math Spectroscope' — visualizations of zeta zeros appearing from prime data. Monetization: ads + Patreon. (3) Textbook chapter contribution to an existing number theory textbook. (4) Workshop at math conferences (ICERM, AIM, BIRS). (5) Interactive web apps for math education (charge schools/universities). Estimate revenue and timeline for each."

# 11. AMR 2D shock — honest viability test design
rung4 "AMR_2D_HONEST_TEST_DESIGN" "Design an honest test for Farey AMR in 2D on a shock problem. We know: (1) 1D Farey loses to quadtree (3.8x worse). (2) Farey's advantage is zero cascading, which matters more in 2D/3D. (3) Break-even estimated at 500x500 grid. Test design: (a) 2D Sod shock tube (shock at x=0.5, uniform in y). (b) 2D Kelvin-Helmholtz instability (shear layer with multiple shock-like features). For each: implement quadtree with 2:1 balance vs Farey-mediant insertion targeting same resolution near discontinuity. Measure: total cells, cascade overhead percentage, error vs reference solution. What is the MINIMUM 2D grid size where Farey wins? If break-even is >1000x1000, the market is too narrow."

# 12. Algorithmic trading application
rung4 "ALGO_TRADING_APPLICATION" "Could Farey sequences help in algorithmic trading? (1) Order book analysis: bid/ask prices are rational (tick sizes). Farey-like structure in price levels? (2) Optimal execution: splitting a large order into Farey-spaced sub-orders for minimum market impact? The injection principle says each sub-order fills the largest 'gap' in execution history. (3) Signal detection: we showed f^2 pre-whitening doesn't help for low-freq financial signals. But what about detecting high-frequency microstructure patterns (order flow toxicity, flash crashes)? (4) Portfolio optimization: Farey-spaced portfolio weights as a low-discrepancy exploration of weight space? Assess each. Any that could generate $50K+ consulting revenue?"

echo "=== Overnight complete $(date) ===" >> "$OUT/OVERNIGHT_ACADEMIC_PROFIT_LOG.md"

# ===== NEW TASKS: Product-focused tests =====

# 13. Network Anomaly Detection — test on synthetic botnet traffic
run_code "NETWORK_ANOMALY_TEST" "Test whether f^2 spectral compensation can detect periodic botnet callback patterns in network traffic. Simulate: (1) Background traffic: 10000 packets with Poisson inter-arrival times (mean 0.1s). Timestamps are irregular. (2) Inject botnet C2 callback: 50 periodic packets at exactly every 30 seconds (f=0.033 Hz) hidden in the traffic. Very weak signal (50 out of 10050). (3) Also inject a DDoS pulse: burst of 20 packets every 5 seconds (f=0.2 Hz) for 100 seconds. (4) Compute Lomb-Scargle and f^2 compensated periodogram on packet timestamps. (5) Can either method detect the 0.033 Hz botnet callback? The 0.2 Hz DDoS pulse? (6) Test with increasing noise: add jitter to botnet timing (std=0, 1s, 3s, 5s). At what jitter does detection fail? Report SNR for each method. Save figure. VERDICT: could this be a security product?"

# 14. Vibration Analysis — test on synthetic bearing fault
run_code "VIBRATION_FAULT_TEST" "Test whether f^2 spectral compensation can detect bearing faults from vibration data. Simulate: (1) Normal bearing: vibration signal = sum of harmonics at shaft frequency (30 Hz) and its multiples, plus pink (1/f) noise. Sample at 10kHz but with 5% missing samples (sensor dropouts = irregular sampling). N=50000 points. (2) Inject bearing fault: add weak periodic impulse at ball-pass frequency outer race (BPFO) = 89.2 Hz, amplitude = 5% of main vibration (barely visible). (3) Compute Lomb-Scargle and f^2 compensated periodogram. (4) Can f^2 detect the 89.2 Hz fault signature in pink noise better than LS? The fault is HIGH frequency in COLORED noise — exactly our sweet spot. (5) Test sensitivity: at what fault amplitude does detection fail for each method? Report SNR. Save figure. VERDICT: could this be an industrial IoT product?"

# 15. Graph Spectroscopy — test on Zachary karate club
run_code "GRAPH_SPECTROSCOPE_TEST" "Test whether a spectroscope can detect graph eigenvalues from random walk data. (1) Build Zachary's karate club graph (34 nodes, 78 edges). Use adjacency matrix: A[i][j] = 1 if connected. Compute the Laplacian eigenvalues directly (ground truth). (2) Run 10000-step random walk on the graph. Record: node visited at each step. (3) Build 'graph Mertens function': for each node i, M_G(i) = (visits to i) - (expected visits = degree_i / 2*edges * total_steps). This is the deviation from expected. (4) Compute spectroscope: F(lambda) = lambda^2 * |sum_i M_G(i) * exp(-i*lambda*feature_i)|^2 where feature_i is some node embedding (try: degree, or eigenvector of adjacency). (5) Do peaks in F(lambda) correspond to Laplacian eigenvalues? (6) Also test on stochastic block model (2 communities, 50 nodes each, p_in=0.3, p_out=0.05). VERDICT: does this work at all?"

# 16. Universality theorem — proof attempt under GRH
run35b "UNIVERSALITY_GRH_PROOF" "PROOF ATTEMPT under GRH: For any subset S of primes with |S|->infinity and S spanning [2,X] with X->infinity, the compensated spectroscope F_S(gamma) = gamma^2 * |sum_{p in S} M(p)/p * exp(-igamma*log(p))|^2 has local maxima within O(1/log(X)) of each nontrivial zeta zero gamma_k. Key steps: (1) M(p) = sum_rho p^rho/(rho*zeta'(rho)) - 2 (explicit formula under GRH). (2) The spectroscope sum at gamma_j: sum_{p in S} M(p)/p * p^{-igamma_j} = sum_rho c_rho * sum_{p in S} p^{i(gamma_rho - gamma_j) - 1}. (3) On-resonance term (rho=rho_j): c_j * sum_{p in S} p^{-1} ~ c_j * log(log(max(S))). (4) Off-resonance terms: sum_{p in S} p^{i*alpha - 1} for alpha = gamma_k - gamma_j != 0. Under GRH+LI, these sums are o(sum p^{-1}) by equidistribution of {alpha*log(p)} mod 2pi. (5) Therefore the on-resonance term dominates regardless of which subset S is chosen, as long as sum_{p in S} p^{-1} -> infinity. (6) The condition sum p^{-1} -> infinity is equivalent to S being unbounded and sufficiently dense. Formalize. Identify exactly what assumptions are needed beyond GRH."

# 17. Patent landscape — what's patentable
rung4 "PATENT_LANDSCAPE_ANALYSIS" "Analyze what from our research could be patented (US utility patent). We have: (1) A method for detecting periodic structure in arithmetic data using frequency-compensated periodogram. (2) A method for progressive data ordering using Farey denominator complexity. (3) A method for detecting anomalies in network traffic using spectral analysis of packet timestamps. (4) A method for detecting mechanical faults from irregularly-sampled vibration data using f^alpha spectral compensation. For each: (a) Is it patent-eligible under US law (35 USC 101 — abstract idea exclusion for math)? (b) Is there prior art that would block it? (c) What would the claims look like? (d) Estimated cost to file (provisional + utility)? Key issue: the Alice/Mayo test — mathematical methods are generally not patentable, but APPLICATIONS of math to specific technical problems ARE. Which of our ideas cross the line into patentable territory?"

# 18. NSF/Simons grant outline
rung4 "GRANT_PROPOSAL_OUTLINE" "Draft a 2-page grant proposal outline for NSF DMS (Division of Mathematical Sciences) or Simons Foundation Collaboration Grants. Title: Spectral Detection of L-Function Zeros from Arithmetic Data. PI: Saar Shai (independent researcher). Key results to highlight: (1) Per-step Farey discrepancy (new mathematical object). (2) 20/20 zeta zero detection via compensated spectroscope. (3) Universality theorem (any 2750 primes suffice). (4) GUE pair correlation from arithmetic data (RMSE=0.066). (5) 422 Lean 4 verified results. (6) Extension to 108 L-function characters. Proposed work: (a) Prove universality under GRH. (b) Extend to automorphic L-functions. (c) Investigate connections to quantum chaos via horocycle equidistribution. (d) Develop GRH verification pipeline for systematic L-function checking. Budget: $50K-200K over 2 years. Note: Simons Collaboration Grants for Mathematicians are $8400/year — small but prestigious."

# 19. What NEW capability exists that didn't before?
run35b "NEW_CAPABILITY_ANALYSIS" "Think creatively: our spectroscope detects eigenvalues (zeta zeros) from a function evaluated at primes (Mertens function). This is a general technique: given ANY function f evaluated at irregular sample points, compute F(lambda) = lambda^alpha * |sum f(x_i) * exp(-i*lambda*g(x_i))|^2 where g(x) is some transform of the sample points. Peaks in F reveal hidden periodicities. The novelty: the lambda^alpha compensation + local z-score normalization. What NEW problems could this general framework solve? Think: (1) Detecting periodic gene expression from single-cell RNA-seq (cells sampled at irregular developmental times). (2) Detecting orbital resonances from asteroid position data (irregularly sampled). (3) Detecting circadian rhythms from wearable sensor data (irregular sampling due to wear patterns). (4) Detecting hidden periodicity in earthquake catalogs. For each: who would pay for this? What would the product look like? Is it a SaaS API, a library, or a one-time analysis service?"

