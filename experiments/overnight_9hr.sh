#!/bin/bash
OLLAMA="http://localhost:11434/api/generate"
OUT="$HOME/Desktop/Farey-Local/experiments"
LOG="$OUT/OVERNIGHT_9HR_LOG.md"

run35b() {
    local name="$1"; local prompt="$2"
    echo "$(date) Starting: $name [35b]" >> "$LOG"
    curl -s "$OLLAMA" -d "{\"model\":\"qwen3.5:35b\",\"prompt\":\"$prompt\",\"stream\":false,\"options\":{\"num_ctx\":8192}}" 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('response','EMPTY'))" > "$OUT/${name}.md" 2>&1
    echo "$(date) Done: $name ($(wc -c < "$OUT/${name}.md") bytes)" >> "$LOG"
}

rung4() {
    local name="$1"; local prompt="$2"
    echo "$(date) Starting: $name [gemma4]" >> "$LOG"
    curl -s "$OLLAMA" -d "{\"model\":\"gemma4:26b\",\"prompt\":\"$prompt\",\"stream\":false,\"options\":{\"num_ctx\":8192}}" 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('response','EMPTY'))" > "$OUT/${name}.md" 2>&1
    echo "$(date) Done: $name ($(wc -c < "$OUT/${name}.md") bytes)" >> "$LOG"
}

run8b() {
    local name="$1"; local prompt="$2"
    echo "$(date) Starting: $name [8b]" >> "$LOG"
    curl -s "$OLLAMA" -d "{\"model\":\"qwen3:8b\",\"prompt\":\"$prompt\",\"stream\":false,\"options\":{\"num_ctx\":4096}}" 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('response','EMPTY'))" > "$OUT/${name}.md" 2>&1
    echo "$(date) Done: $name ($(wc -c < "$OUT/${name}.md") bytes)" >> "$LOG"
}

run_code() {
    local name="$1"; local prompt="$2"
    echo "$(date) Starting code: $name [35b]" >> "$LOG"
    ~/bin/local_code_agent.sh qwen3.5:35b "$name" "$prompt"
    echo "$(date) Done code: $name" >> "$LOG"
}

echo "=== 9-Hour Overnight Started $(date) ===" > "$LOG"

# ===== PHASE 1: Hours 0-2 (LIGHT only — user using device) =====
# Use qwen3:8b only (5GB, lightweight)

echo "=== PHASE 1: Light tasks (8b only) ===" >> "$LOG"

run8b "PAPER1_SUBMISSION_CHECKLIST" "Create a checklist for submitting a math paper to arXiv. Categories: math.NT primary, math.CO secondary. Items: abstract under 300 words, all refs complete, no compilation errors, endorsement code ready, supplementary materials linked, AI disclosure present, author list correct (single author), MSC codes correct. Check each item yes/no."

run8b "MATHLIB_NAMING_CONVENTIONS" "What are Mathlib4 (Lean 4) naming conventions? List: (1) theorem/lemma naming (snake_case with content description). (2) File naming. (3) Import style. (4) Documentation requirements. (5) What to avoid (native_decide for nontrivial results, sorry, axioms). Give 5 examples of good Mathlib theorem names for Farey sequence results."

run8b "PATENT_PROVISIONAL_TEMPLATE" "What does a US provisional patent application need? List requirements: (1) Description of invention. (2) Drawings if applicable. (3) Cover sheet (name, address). (4) Filing fee ($320 for small entity). (5) No claims needed (provisional). How long does provisional priority last? (12 months). What should the description cover for a mathematical method patent?"

run8b "GRANT_ELIGIBILITY_INDEPENDENT" "Can an independent researcher (no university affiliation) apply for NSF grants? What about Simons Foundation? AMS? What are the requirements? What alternative funding sources exist for independent math researchers? List 5 specific programs with eligibility details."

run8b "VIBRATION_ANALYSIS_MARKET_SIZE" "What is the market size for predictive maintenance / vibration analysis in industrial IoT? Key players: SKF, Schaeffler, Emerson, Honeywell, GE Digital. How do they detect bearing faults currently? What algorithms do they use? What do they charge? Is there room for a new spectral method?"

run8b "NETWORK_SECURITY_SPECTRAL_TOOLS" "What spectral analysis tools exist for network security / anomaly detection? How do companies like Darktrace, CrowdStrike, Splunk detect periodic botnet callbacks? Do they use Fourier analysis on packet timestamps? What is the state of the art? Is there a gap for frequency-domain anomaly detection?"

run8b "GRAPH_ML_EIGENVALUE_METHODS" "How are graph eigenvalues currently computed in graph ML? Methods: spectral clustering, GNN, Chebyshev polynomials. Companies: Neo4j, TigerGraph, AWS Neptune. Do any use random-walk-based spectral estimation? What is the state of the art for detecting community structure via eigenvalues? Is there a gap?"

run8b "GENE_EXPRESSION_PERIODICITY" "Do biologists look for periodic patterns in gene expression data? Single-cell RNA-seq produces irregularly sampled developmental timepoints. What methods exist? Is Lomb-Scargle used in genomics? What about circadian rhythm detection from irregular wearable data? Companies in this space?"

# ===== PHASE 2: Hours 2-5 (FULL THROTTLE — 35b) =====

echo "=== PHASE 2: Full throttle (35b) ===" >> "$LOG"

# Academic
run35b "PAPER1_FINAL_CHECKLIST" "Create a detailed final checklist for submitting our paper to arXiv math.NT. The paper: per-step Farey discrepancy DeltaW(N), exact identities (bridge, injection, four-term), Chebyshev bias R=0.77, spectroscope detecting 3 zeros, 422 Lean results. Check: abstract clear and under 300 words? All terms defined before use? All proofs complete? Reviewer feedback addressed? Prior art cited (Csoka 2015, Tomas Garcia 2025)? Figures correct? AI disclosure present?"

run35b "MATHLIB_PR_STRATEGY" "Strategy for contributing our 422 Lean 4 Farey results to Mathlib. Which file first? Probably basic definitions: Farey sequence, cardinality formula, Ramanujan sum evaluation. What naming conventions? How to handle native_decide? Submit one large PR or many small? Expected review timeline?"

run35b "PAPER2_DETAILED_STRUCTURE" "Detailed structure for Paper 2: The Compensated Mertens Spectroscope. For each of 8 sections: title, key results, figures, honest caveats. Must cite pre-whitening as classical technique. Our contribution: application to number-theoretic periodogram, local z-score normalization, universality observation, GUE pair correlation."

# Profit exploration — products and IP
run35b "CRYPTO_APPLICATIONS_DEEP" "Could our spectroscope technique be useful in cryptography? Not as an attack, but as a TOOL. Ideas: (1) Verification tool — check that RSA key generation produces primes with expected spectral properties. If a key generator is biased, the spectroscope would show anomalous peaks. Sell as security audit tool. (2) Hash function testing — verify that hash outputs have no periodic structure. (3) ZK proof circuits — our Lean-verified identities could be compiled into arithmetic circuits for zero-knowledge proofs. Assess each as a PRODUCT (not consulting)."

run35b "QUANTUM_COMPUTING_APPS" "Connections to quantum computing that could be products: (1) Improved classical post-processing for Shor's algorithm using Farey mediant convergents. (2) Optimal parameter initialization for VQE using Farey-spaced angles. (3) Quantum phase estimation circuits optimized by Farey structure. For each: what would the product be? A software library? A hardware design? A SaaS service? Who buys it?"

run35b "RESEARCH_PROFIT_DIRECTIONS" "Our tools: (A) detecting hidden periodicity from irregular samples in colored noise, (B) deterministic optimal gap-filling, (C) 422 verified identities in Lean 4. For each tool: what UNSOLVED problem could it solve where someone would pay? Not consulting — products, IP, services that deliver results. Think: predictive maintenance SaaS, security audit tool, grant-funded research, patent-licensed algorithm."

# Test designs for overnight code execution
run35b "NETWORK_ANOMALY_DESIGN" "Design a rigorous test for spectral botnet detection. Simulate realistic network traffic with: (1) Poisson background (mean 0.1s gaps), (2) hidden periodic C2 callback at f=0.033Hz with timing jitter, (3) DDoS pulse at f=0.2Hz. Compute f^2 compensated periodogram vs Lomb-Scargle. The C2 callback is HIGH frequency relative to the Poisson noise spectrum — our sweet spot. Write the test specification (what to measure, what success looks like, what would kill the idea)."

run35b "VIBRATION_FAULT_DESIGN" "Design a rigorous test for bearing fault detection using f^2 spectral compensation. Simulate: (1) shaft vibration at 30Hz + harmonics, (2) pink 1/f noise background, (3) weak bearing fault at BPFO=89.2Hz (5% amplitude). Irregular sampling (10kHz with 5% dropouts). The fault is HIGH frequency in COLORED noise. Measure: detection SNR for f^2 vs LS. What fault amplitude is the detection threshold for each method? What success looks like."

run35b "GRAPH_SPECTROSCOPE_DESIGN" "Design a test for detecting graph Laplacian eigenvalues from random walk data. Graph: Zachary karate club (34 nodes). Run long random walk, collect node visit statistics. Build 'graph Mertens function' M_G(i) = (visits - expected). Compute spectroscope. Do peaks correspond to eigenvalues? Key challenge: what is the 'frequency variable' for graphs? Options: use node features as the exponent base. This is speculative — design the test to find out IF it works at all."

# Universality proof
run35b "UNIVERSALITY_GRH_PROOF" "PROOF under GRH+LI: For any subset S of primes with sum_{p in S} 1/p -> infinity, the spectroscope F_S(gamma) has local maxima near every zeta zero. Key: (1) M(p) = sum_rho p^rho/(rho*zeta'(rho)) by explicit formula. (2) At gamma=gamma_j: sum_{p in S} M(p)/p * p^{-igamma_j} = c_j * sum_{p in S} p^{-1} + sum_{k!=j} c_k * sum_{p in S} p^{i(gamma_k-gamma_j)-1}. (3) On-resonance: c_j * sum p^{-1} diverges. (4) Off-resonance: sum p^{i*alpha-1} = o(sum p^{-1}) under LI by equidistribution of {alpha*log(p)} mod 2pi for irrational alpha. (5) Therefore signal dominates noise for ANY S with divergent sum 1/p. Formalize all steps."

# Phase derivation
run35b "PHASE_PHI_EXACT" "Compute the exact phase phi in the Chebyshev correlation sgn(DeltaW(p)) ~ -sgn(cos(gamma_1*log(p) + phi)). We observe phi=5.28. From the explicit formula: M(p) ~ 2*|c_1|*sqrt(p)*cos(gamma_1*log(p) + alpha_1) where alpha_1 = -arg(rho_1*zeta'(rho_1)). Compute: arg(rho_1) = arctan(2*gamma_1) ~ pi/2. arg(zeta'(rho_1)) requires the actual value of zeta'(1/2+14.1347i). From tables: zeta'(rho_1) ~ -0.174 + 0.413i (approximate). So arg(zeta'(rho_1)) ~ atan2(0.413, -0.174) ~ 1.97. Then alpha_1 = -(pi/2 + 1.97) = -3.54. But phi = 5.28 = 2*pi - 0.95. Does -3.54 + 2*pi = 2.74? Not matching. Where is the error?"

# ===== PHASE 3: Hours 5-7 (gemma4 for breadth) =====

echo "=== PHASE 3: gemma4 breadth ===" >> "$LOG"

rung4 "TARGET_COMPANIES_RESEARCH" "Companies that might buy products based on detecting hidden periodicity in irregular data: (1) Predictive maintenance: SKF, Schaeffler, Emerson Automation, Augury, Senseye, Uptake. (2) Network security: Darktrace, Vectra AI, ExtraHop. (3) Astronomy: STScI (Hubble/JWST pipeline), Vera Rubin Observatory (LSST). (4) Genomics: 10x Genomics, Illumina, Flatiron Health. (5) Industrial IoT: Siemens MindSphere, PTC ThingWorx, GE Predix. For each: what they currently use, what gap exists, what product we could offer, estimated deal size."

rung4 "PATENT_LANDSCAPE_ANALYSIS" "What from our research is patentable under US law? Alice/Mayo test: pure math is NOT patentable, but specific technical applications ARE. Assess: (1) Method for detecting mechanical faults from irregularly-sampled vibration data using frequency-compensated periodogram. (2) Method for detecting network intrusion patterns via spectral analysis of packet timestamps with colored-noise compensation. (3) System for progressive data transmission using number-theoretic ordering. (4) Method for verifying L-function zeros using arithmetic spectroscopy. For each: prior art, claim structure, estimated filing cost."

rung4 "GRANT_PROPOSAL_OUTLINE" "Draft NSF DMS / Simons grant outline. Title: Spectral Detection of L-Function Zeros from Arithmetic Data. Key results: 20/20 zero detection, universality (2750 primes), GUE pair correlation, 422 Lean results, 108 L-function characters. Proposed: prove universality under GRH, extend to automorphic L-functions, GRH verification pipeline. Budget $50-200K. Can independent researcher apply?"

rung4 "EDUCATION_MONETIZATION" "Products (not consulting) for math education: (1) Interactive web app 'Spectroscope Explorer' — SaaS subscription for universities ($500-2K/year/institution). (2) Python library farey-tools on PyPI — free but with premium features (GPU acceleration, batch L-function scanning). (3) Textbook chapter or monograph on computational Farey sequence theory. (4) Online course platform (not Udemy — own platform with higher margins). For each: revenue estimate, timeline, effort."

rung4 "PREDICTIVE_MAINTENANCE_PRODUCT" "Design a predictive maintenance product using our spectral compensation technique. Product: SaaS API that takes irregularly-sampled vibration sensor data and returns detected fault frequencies with confidence scores. USP: handles irregular sampling natively (no resampling needed) + colored noise compensation. Pricing: $0.01/analysis or $500/month/sensor. Target: factories with 100-1000 sensors. Revenue at 10 customers: $50K-500K/month. Technical requirements: cloud API, data pipeline, ML post-processing. What would an MVP look like?"

rung4 "NETWORK_SECURITY_PRODUCT" "Design a network security product using spectral anomaly detection. Product: plugin for SIEM platforms (Splunk, Elastic) that analyzes packet timestamp patterns and flags periodic anomalies (botnet C2, data exfiltration beacons). USP: detects timing-based anomalies that payload-based detection misses. Pricing: $1K-10K/month per deployment. Target: SOC teams at enterprises. What would an MVP look like? What existing SIEM APIs could we integrate with?"

rung4 "BIOTECH_PERIODICITY_PRODUCT" "Design a bioinformatics product for detecting periodic gene expression patterns. Product: Python/R library or web tool that takes single-cell RNA-seq time-course data and identifies genes with periodic expression (cell cycle, circadian, ultradian). USP: handles irregular developmental pseudotime natively. Target: computational biology labs, pharma R&D. Pricing: free library + paid cloud processing ($100/analysis for large datasets). What datasets could we benchmark on?"

rung4 "WHAT_QUESTIONS_NOT_ASKING" "Think creatively about our Farey research. We have: spectroscope detecting eigenvalues from arithmetic data, universality across subsets, formal verification library, pre-whitening for colored noise. What questions are we NOT asking? What perspectives have we not considered? Think: (1) Could our technique work BACKWARDS — given eigenvalues, reconstruct the arithmetic data? (2) Could universality mean we can COMPRESS prime-related data? (3) Could the Lean library be used for AUTOMATED CONJECTURE GENERATION? (4) Is there a connection to machine learning interpretability (detecting hidden features in neural network weights)? (5) Could the spectroscope detect FAKE data (synthetic primes, fraudulent sequences)? Generate 10 unconventional ideas."

# ===== PHASE 4: Hours 7-9 (35b code agents for testing) =====

echo "=== PHASE 4: Code agent tests ===" >> "$LOG"

# These use local_code_agent.sh — 35b writes AND runs Python
run_code "NETWORK_ANOMALY_TEST" "Test whether f^2 spectral compensation can detect periodic botnet callback patterns in network traffic. Simulate: (1) Background: 10000 packets with Poisson inter-arrival times (mean 0.1s). (2) Inject botnet C2: 50 periodic packets every 30 seconds (f=0.033 Hz). (3) Inject DDoS pulse: burst of 20 packets every 5 seconds (f=0.2 Hz) for 100 seconds. (4) Compute Lomb-Scargle vs f^2 compensated periodogram on packet timestamps. Use scipy.signal.lombscargle for LS. For f^2: power = (2*pi*f)^2 * |sum exp(-2*pi*i*f*t)|^2. (5) Measure detection SNR for each signal with each method. (6) Test jitter: add Gaussian jitter std=0,1,3,5 seconds to botnet timing. Print results table. Save to ~/Desktop/Farey-Local/experiments/NETWORK_ANOMALY_TEST.md"

run_code "VIBRATION_FAULT_TEST" "Test bearing fault detection with f^2 compensation. Simulate: (1) Normal: vibration = sin(2*pi*30*t) + 0.5*sin(2*pi*60*t) + pink noise (1/f spectrum). Sample at 10kHz with 5% random dropouts (irregular). N=50000. (2) Inject fault: add 0.05*sin(2*pi*89.2*t) (BPFO). (3) Compute LS and f^2 periodogram near 89.2 Hz. (4) Measure SNR of fault peak for each. (5) Vary fault amplitude: 0.01, 0.02, 0.05, 0.1, 0.2. Find detection threshold for each method. Print results. Save to ~/Desktop/Farey-Local/experiments/VIBRATION_FAULT_TEST.md"

run_code "GRAPH_SPECTROSCOPE_TEST" "Test graph spectroscopy. (1) Build Zachary karate club graph: 34 nodes, edges from standard adjacency. Compute Laplacian eigenvalues (ground truth). (2) Run 50000-step random walk. Record node sequence. (3) For each node i: M_G(i) = (visit_count/total - degree_i/(2*num_edges)). (4) Try spectroscope: F(lambda) = lambda^2 * |sum_i M_G(i) * exp(-i*lambda*i)|^2 for lambda in [0, 5], 5000 points. (5) Do peaks match eigenvalues? (6) Also try with node degree as feature: F(lambda) = lambda^2 * |sum_i M_G(i) * exp(-i*lambda*degree_i)|^2. Print eigenvalues, peak positions, matches. Save to ~/Desktop/Farey-Local/experiments/GRAPH_SPECTROSCOPE_TEST.md"

run_code "GENE_PERIODICITY_TEST" "Test periodicity detection in simulated gene expression data. (1) Simulate 200 cells at irregular developmental times t ~ sorted(Uniform(0, 24 hours)). (2) Gene A: expression = 2 + sin(2*pi*t/6) + noise(std=0.5) — 6-hour periodic (cell cycle). (3) Gene B: expression = 3 + 0.2*sin(2*pi*t/24) + noise(std=0.5) — weak circadian. (4) Gene C: no periodicity, just noise. (5) Apply LS and f^2 periodogram to each gene. (6) Can we detect the 6-hour period for gene A? The weak 24-hour period for gene B? Does f^2 help? Print results. Save to ~/Desktop/Farey-Local/experiments/GENE_PERIODICITY_TEST.md"

echo "=== Overnight 9HR complete $(date) ===" >> "$LOG"
