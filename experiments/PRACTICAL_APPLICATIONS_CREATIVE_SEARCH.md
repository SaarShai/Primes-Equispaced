# Creative Search for Practical Applications — Opus Analysis
# 2026-04-10

## HONEST VERDICT: No general-purpose 2x gain from zero knowledge.
Zeros control ERROR TERMS. Algorithms are designed to be robust to error terms.

## THREE VIABLE CANDIDATES

### 1. NTT Prime Selection for Post-Quantum Crypto (HIGHEST IMPACT)
- CRYSTALS-Kyber uses p=3329 for NTT. Was it optimal? Selection was partly empirical.
- Zero-based analysis could find primes with fewer NTT multiplications
- If 20-50% fewer mults → affects every TLS handshake on the internet
- TEST: For p∈[3000,4000] with p≡1 mod 256, compute NTT costs, correlate with M(p)
- 1 hour, concrete, potentially enormous impact

### 2. Costas Sequence / Radar Waveform Design (10-100x DESIGN speedup)
- Costas sequences from primitive roots mod p
- Zero knowledge predicts which p gives best sidelobes → skip brute search
- 10-100x faster DESIGN, not runtime
- Real defense/radar application

### 3. Musical Inharmonicity Detection (niche 2x)
- Piano overtone deviation from integer ratios
- Farey-filtered residual more sensitive to stiffness coefficient
- Niche but testable

## DEAD ENDS (thoroughly killed)
- Monte Carlo / Halton: <1% gain, primes just need to be coprime
- Hash functions: collision rate independent of prime choice
- Compressed sensing: real signals don't have multiplicative structure
- Network/anomaly detection: IP addresses have no NT significance
- Biological sequences: no multiplicative structure
- Crypto PRNG: possible 10x parameter validation speedup (marginal)
- Portfolio/Erdős-Kac: theoretical connection only

## RECOMMENDATION: Run the NTT prime selection test first.
