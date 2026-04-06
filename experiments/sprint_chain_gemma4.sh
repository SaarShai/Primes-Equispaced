#!/bin/bash
OLLAMA="http://localhost:11435/api/generate"
OUT="$HOME/Desktop/Farey-Local/experiments"

run() {
    local name="$1"; local prompt="$2"
    echo "$(date) Starting: $name" >> "$OUT/SPRINT_LOG.md"
    curl -s "$OLLAMA" -d "{\"model\":\"gemma4:26b\",\"prompt\":\"$prompt\",\"stream\":false,\"options\":{\"num_ctx\":8192}}" 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('response','EMPTY'))" > "$OUT/${name}.md" 2>&1
    echo "$(date) Done: $name ($(wc -c < "$OUT/${name}.md") bytes)" >> "$OUT/SPRINT_LOG.md"
}

# Literature: BCZ 2001 results for GK concentration
run "BCZ_LITERATURE_REVIEW" "Review the Boca-Cobeli-Zaharescu (BCZ) 2001 paper on Farey sequence statistics. What do they prove about the distribution of Farey fractions by denominator? What bounds do they give on spacing statistics? Can their results be used to prove that the top 20% of fractions (by denominator size) contribute 94% of the cross-term sum D*delta? Key paper: Boca, Cobeli, Zaharescu, Distribution of lattice points visible from the origin, Communications in Mathematical Physics (2000/2001). What are the main theorems?"

# Literature: horocycle equidistribution and Farey
run "HOROCYCLE_FAREY_LITERATURE" "Survey the connection between Farey sequences and horocycle equidistribution on the modular surface. Key authors: Marklof, Strombergsson, Boca, Zaharescu. What is known about: (1) Farey fractions as horocycle orbits on SL2(Z)\\H, (2) equidistribution rate and its connection to spectral theory, (3) any existing connection to the Riemann zeta zeros via this route. Does anyone connect per-step Farey discrepancy to horocycle dynamics?"

# Paper 2 detailed section drafts
run "PAPER2_SECTION2_DRAFT" "Draft Section 2 of Paper 2: 'Mathematical Construction and the gamma-squared Matched Filter.' Key content: (1) Define the Mertens spectroscope F(gamma) = |sum M(p)/p * exp(-igamma*log(p))|^2. (2) Explain why peaks appear at zeta zeros (explicit formula). (3) Derive the gamma^2 compensation: |c_k|^2 ~ 1/gamma_k^2, so multiplying by gamma^2 flattens peaks. (4) Prove the compensation ratio gamma^2/(1/4+gamma^2) is in [4/5,1) for gamma>=1. (5) Cite prior art: Fourier duality is classical (Csoka 2015, Van der Pol 1947). Our contribution: the gamma^2 matched filter. Write in LaTeX-ready style."

# Goldbach spectroscope feasibility
run "GOLDBACH_SPECTROSCOPE_TEST" "Can a spectroscope approach work for Goldbach representations? Define r(2n) = number of ways to write 2n as sum of two primes. The singular series predicts r(2n) ~ 2*C_2 * prod_{p|n, p>2} (p-1)/(p-2) * n/log(n)^2. If we compute F(gamma) = |sum (r(2n) - predicted) * exp(-igamma*log(n))|^2, would peaks appear at zeta zeros? The error term in Goldbach counts is controlled by zeros of zeta via the circle method. Assess feasibility. What data would we need? Is r(2n) efficiently computable to 10^6?"

echo "=== Sprint gemma4 complete $(date) ===" >> "$OUT/SPRINT_LOG.md"
