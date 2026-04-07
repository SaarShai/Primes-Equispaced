#!/bin/bash
OLLAMA="http://localhost:11435/api/generate"
OUT="$HOME/Desktop/Farey-Local/experiments"

run() {
    local name="$1"; local model="$2"; local prompt="$3"
    echo "$(date) Starting: $name ($model)" >> "$OUT/APP_TASKS_LOG.md"
    curl -s "$OLLAMA" -d "{\"model\":\"$model\",\"prompt\":\"$prompt\",\"stream\":false,\"options\":{\"num_ctx\":8192}}" 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('response','EMPTY'))" > "$OUT/${name}.md" 2>&1
    echo "$(date) Done: $name ($(wc -c < "$OUT/${name}.md") bytes)" >> "$OUT/APP_TASKS_LOG.md"
}

echo "=== App tasks started $(date) ===" > "$OUT/APP_TASKS_LOG.md"

# 1. Siegel zero — extend sensitivity analysis to q<=200
run "SIEGEL_SENSITIVITY_SCALING" "qwen3.5:35b" "The Mertens spectroscope detects Siegel zeros with 465M sigma sensitivity for q<=13 using 78K primes. How does sensitivity scale with modulus q? For character chi mod q, the number of primes contributing per residue class is ~N/phi(q). The signal from a Siegel zero at beta scales as (N/phi(q))^2 * 1/(1-beta)^2. The noise scales as N/phi(q). So SNR ~ N/(phi(q)*(1-beta)^2). For N=78000 and (1-beta)=0.01: SNR ~ 78000/(phi(q)*0.0001). For q=100: phi(q)=40, SNR~19.5M. For q=1000: phi(q)~400, SNR~1.95M. For q=10000: phi(q)~4000, SNR~195K. All still enormous. What is the maximum q for which we can rule out |1-beta|>0.01? Derive the formula."

# 2. AMR — design the hybrid prototype
run "AMR_HYBRID_PROTOTYPE_DESIGN" "qwen3.5:35b" "Design a hybrid AMR prototype that uses Farey refinement near discontinuities and standard quadtree refinement in smooth regions. Requirements: (1) Detect discontinuities via gradient threshold. (2) In cells adjacent to discontinuity: use Farey mediant insertion (zero cascading). (3) In smooth cells: use standard 2:1 balanced quadtree. (4) Transition region: ensure conforming mesh at Farey/quadtree boundary. Specify: data structures, algorithm pseudocode, expected cell count savings vs pure quadtree on a Sod shock tube problem. Target: OpenFOAM-compatible output format."

# 3. GRH verification — design systematic pipeline
run "GRH_VERIFICATION_PIPELINE" "gemma4:26b" "Design a systematic GRH verification pipeline using the compensated Mertens spectroscope. For each primitive Dirichlet character chi mod q (q up to 1000): (1) Compute twisted Mertens M_chi(p) = sum mu(n)*chi(n). (2) Compute F_chi(gamma) = gamma^2 * |sum M_chi(p)/p * exp(-igamma*log(p))|^2. (3) Compare peaks against known zeros of L(s,chi). (4) Flag any character where peaks DON'T match known zeros (potential GRH violation). What computational resources needed? How many characters total? What precision required? How to handle unknown L-function zeros for large q?"

# 4. AMR market entry strategy
run "AMR_MARKET_ENTRY" "gemma4:26b" "Market entry strategy for Farey AMR technology. The technology eliminates 20-40% wasted cells in shock-dominated CFD via zero-cascading mesh refinement. Best in 1D/2D shock problems (7-15x improvement). Weak in 3D and smooth problems. Options: (A) Open-source OpenFOAM plugin — builds community, no direct revenue. (B) License to ANSYS/Fluent/COMSOL — high revenue but hard to get meetings. (C) SaaS mesh generation API — medium complexity. (D) Consulting for specific industries (hypersonics, fusion). (E) Patent + license. For each: estimate revenue, timeline, effort. What is the minimum viable product? Who are the first customers?"

# 5. Quasi-random sampling comparison
run "FAREY_VS_SOBOL_HALTON" "qwen3.5:35b" "Compare Farey sequences as low-discrepancy sequences for quasi-Monte Carlo integration against Sobol and Halton sequences. The Farey sequence F_N has discrepancy D_N ~ O(N^{-1/2+eps}) (conditional on RH). Sobol has D_N ~ O(log(N)^d / N) in d dimensions. Halton has D_N ~ O(log(N)^d / N). In 1D: Farey discrepancy is WORSE than Sobol/Halton (their O(log(N)/N) beats O(N^{-1/2+eps})). But Farey has a structural advantage: the injection principle gives an ADAPTIVE refinement strategy — you can add points one at a time, each optimally placed. Sobol/Halton require generating the full sequence. Assess: is there a niche where Farey's adaptive property beats Sobol's lower discrepancy?"

# 6. Scheduling/load balancing application
run "FAREY_SCHEDULING_APPLICATION" "gemma4:26b" "The Farey Injection Principle states: when adding denominators one at a time, each new fraction enters a distinct gap, and each is the mediant (geometrically optimal midpoint) of its neighbors. Can this be applied to job scheduling or load balancing? Model: N servers with current loads [0,1]. New job arrives — place it at the 'mediant' of the two most underloaded adjacent servers. Compare to: (A) random placement, (B) least-loaded, (C) round-robin. Does the Farey approach minimize max load imbalance? Design a simulation test."

echo "=== App tasks complete $(date) ===" >> "$OUT/APP_TASKS_LOG.md"
