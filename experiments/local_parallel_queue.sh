#!/bin/bash
OLLAMA="http://localhost:11434/api/generate"
OUT="$HOME/Desktop/Farey-Local/experiments"
LOG="$OUT/LOCAL_PARALLEL_LOG.md"

rung4() {
    local name="$1"; local prompt="$2"
    echo "$(date) Starting: $name [gemma4 LOCAL]" >> "$LOG"
    curl -s "$OLLAMA" -d "{\"model\":\"gemma4:26b\",\"prompt\":\"$prompt\",\"stream\":false,\"options\":{\"num_ctx\":8192}}" 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('response','EMPTY'))" > "$OUT/${name}.md" 2>&1
    echo "$(date) Done: $name ($(wc -c < "$OUT/${name}.md") bytes)" >> "$LOG"
}

echo "=== Local Parallel Queue $(date) ===" > "$LOG"

rung4 "LOCAL_SIEGEL_ZERO_LARGER_Q" "Extend Siegel zero analysis. We tested q<=50 and found no anomalies. What is the theoretical maximum q we can test with 78K primes? The sensitivity formula: SNR ~ N/(phi(q)*(1-beta)^2). For N=78000, (1-beta)=0.01: SNR ~ 78000/(phi(q)*0.0001). At q=1000: phi(q)~400, SNR~1.95M. At q=10000: phi(q)~4000, SNR~195K. All enormous. The REAL limitation is: for large q, we need to correctly identify the character (Legendre symbol). And for non-quadratic characters, we need discrete log computation. Assess: what is the practical limit? Can we do q=100? q=500?"

rung4 "LOCAL_PAPER1_ARXIV_CATEGORIES" "What arXiv categories should we submit our two papers to? Paper 1: Per-step Farey discrepancy, exact identities, Chebyshev bias, spectroscope. Paper 2: Compensated Mertens spectroscope, universality, GUE, Chowla test. Three-body paper: CF periodic table. For each paper: primary category, secondary categories, keywords for discoverability. Also: what endorsement categories are needed?"

rung4 "LOCAL_LEAN_MATHLIB_FIRST_PR" "Design the first Mathlib PR from our 422 Lean results. The smallest useful contribution: define FareySequence, prove cardinality formula |F_N| = 1 + sum phi(k). What Mathlib conventions: (1) File name: Mathlib/NumberTheory/FareySequence.lean? (2) Definition style: use Finset or List? (3) Need to connect to existing Nat.totient in Mathlib. (4) What imports needed? (5) Should we include Ramanujan sum evaluation c_q(1)=mu(q)? Draft the PR description."

rung4 "LOCAL_VISUALIZATION_IMPROVEMENTS" "Review our 9 interactive HTML visualizations for a lay audience. For each, suggest ONE specific improvement that would make it clearer to non-mathematicians: (1) viz_sieve.html (2) viz_ulam_spiral.html (3) viz_riemann_zeta.html (4) viz_matched_filter.html (5) viz_holographic_v2.html (6) viz_gue_comparison.html (7) viz_threebody_table.html (8) viz_seeing_invisible.html. Focus on: is the key insight immediately obvious? What metaphor or analogy would help?"

rung4 "LOCAL_ARXIV_ENDORSER_STRATEGY" "Strategy for getting arXiv endorsement for math.NT. We need an endorser who has posted to math.NT. Approach: (1) List 10 active math.NT authors who work on Farey sequences, Mertens function, or computational number theory. (2) For each: their key papers, email (if findable), and why they'd be interested in endorsing. (3) Draft a 3-sentence email requesting endorsement. (4) Backup plan if no endorser found. Key: our endorsement code is 7ULTHZ. We already have a list of 9 candidates in ENDORSER_EMAILS.md."

echo "=== Local queue complete $(date) ===" >> "$LOG"
