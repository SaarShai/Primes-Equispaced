# Outreach Targets — Prioritized
# 2026-04-10

## TIER 1: DIRECT BENEFICIARIES (our method solves their problem)

### 1. LMFDB Team
- **Who:** John Cremona (Warwick), David Farmer (AIM), John Voight (Dartmouth), Edgar Costa (MIT)
- **What they need:** L-function zeros at high conductor for database expansion
- **Our value:** Batch spectroscope is 20x faster at q=10000. Direct speedup for their pipeline.
- **Contact:** lmfdb.org, or directly via math conferences
- **Priority:** HIGHEST — concrete bottleneck we address

### 2. Computational Zero Verifiers
- **Who:** David Platt (Bristol), Tim Trudgian (UNSW), Jonathan Bober
- **What they need:** Independent verification methods for zero computations
- **Our value:** Completely different algorithm (spectroscope vs Riemann-Siegel). Independent cross-check. Dichotomy theorem naturally detects anomalies.
- **Priority:** HIGH — our method provides redundancy they don't have

### 3. Siegel Zero Searchers
- **Who:** Anyone working on effective bounds for primes in arithmetic progressions
- **What they need:** Computational evidence against Siegel zeros at small conductor
- **Our value:** 465M sigma sensitivity for q≤13. Batch scanning at high q.
- **Key researchers:** Goldfeld (Columbia), Iwaniec (Rutgers)
- **Priority:** HIGH — Siegel zeros are the #1 open problem after RH

## TIER 2: THEORETICAL BENEFICIARIES (our framework extends their work)

### 4. Bounded Gaps Researchers
- **Who:** James Maynard (Oxford), Terence Tao (UCLA), Ben Green (Oxford)
- **What they do:** Prove results about small prime gaps (Maynard-Tao: gap ≤ 246)
- **Our value:** "Bounded gap primes detect all zeta zeros" (corollary of universality). First connection between bounded gaps and zero detection.
- **Priority:** HIGH — novel link between two active frontiers

### 5. Random Matrix / Katz-Sarnak Community
- **Who:** Jon Keating (Oxford), Nina Snaith (Bristol), Peter Sarnak (IAS), Nicholas Katz (Princeton)
- **What they need:** Zero statistics across L-function families to test symmetry predictions
- **Our value:** Batch spectroscope provides family-wide zero data cheaply. GUE RMSE=0.066 from prime data (new pathway).
- **Priority:** MEDIUM-HIGH — our batch method enables their statistical tests at higher conductor

### 6. Quantum Chaos Physicists
- **Who:** Michael Berry (Bristol), Jon Keating (Oxford), Alain Connes (IHÉS/Collège de France)
- **What they study:** Connection between Riemann zeros and eigenvalues of quantum Hamiltonians. Berry-Keating conjecture: zeros = eigenvalues of a specific operator.
- **Our value:** The spectroscope provides a PHYSICAL measurement analogy — prime data as "measurement" of the quantum spectrum. The large sieve = stability of this measurement. The dichotomy = guaranteed detection regardless of the operator's structure.
- **Connes specifically:** His noncommutative geometry approach to RH uses spectral methods. Our spectroscope is a computational realization of spectral zero detection.
- **Priority:** MEDIUM-HIGH — deep conceptual connection, small community

### 7. Analytic Number Theorists (general)
- **Who:** Kannan Soundararajan (Stanford), Andrew Granville (Montréal), Adam Harper (Warwick)
- **What they care about:** Explicit formula applications, zero distribution, multiplicative functions
- **Our value:** Universality theorem, dichotomy as new RH equivalence, quantitative threshold
- **Priority:** MEDIUM — they're the referees, not the users

## TIER 3: INDIRECT BENEFICIARIES (our results inform their field)

### 8. Algebraic Number Theorists / Class Number Researchers
- **Who:** Manjul Bhargava (Princeton), Melanie Wood (Harvard), Jordan Ellenberg (Wisconsin)
- **What they need:** Class numbers of quadratic fields, which require L(1,χ) values
- **Our value:** Batch spectroscope detects anomalously small L(1,χ) (= small class numbers) across all χ mod q simultaneously. Could flag "interesting" fields for further study.
- **Priority:** MEDIUM — indirect value, but connects to Fields Medal-level work

### 9. Chebotarev / Langlands Program
- **Who:** Peter Scholze (Bonn), Laurent Fargues, Ana Caraiani, broad community (~200+)
- **What they study:** How primes split in number field extensions (Artin L-functions)
- **Our value:** Progression decomposition shows spectroscope detects Artin L-function zeros from prime splitting data. Computational test of Chebotarev predictions.
- **Priority:** LOW-MEDIUM — very indirect, large community but distant connection

### 10. Compressed Sensing / Signal Processing
- **Who:** Emmanuel Candès (Stanford), Terence Tao (UCLA), Jean Bourgain's school
- **What they need:** Deterministic RIP constructions
- **Our value:** Conceptual connection (large sieve = upper RIP). NOT competitive practically (δ⁺ ~ 250). But the observation "RH barrier = lower RIP barrier" is novel framing.
- **Priority:** LOW — conceptual interest only, not practical

### 11. Formal Verification / Lean Community
- **Who:** Kevin Buzzard (Imperial), Patrick Massot (Paris-Saclay), Johan Commelin
- **What they need:** Formalized number theory results for Mathlib
- **Our value:** 434 Lean results, Farey cardinality, prime power sum divergence. Mathlib PR candidates.
- **Priority:** LOW — infrastructure contribution, not research impact

## OUTREACH PLAN
1. Contact LMFDB team with batch spectroscope benchmark data
2. Write to Platt/Trudgian about independent verification pipeline
3. Present at a number theory seminar (any university with NT group)
4. Post preprint on arXiv (need endorser — SAAR ACTION ITEM)
5. Submit to IMRN or J. Number Theory
6. Announce Lean results on Lean Zulip

## ADDITIONAL METHODS AND TOOLS (added 2026-04-10)

### Not strictly spectroscope:
- **Predictive M(p) model:** 20-term explicit formula predicts M(p)/√p with R=0.952 out-of-sample
  → Useful for: explicit formula researchers, computational NT
- **Detection pattern characterization:** Only 1/ζ and -ζ'/ζ type functions detect zeros
  → Useful for: analytic NT theory, sparse recovery theory
- **General spectroscope principle:** ANY summatory function with explicit formula → detection
  → Useful for: broad analytic NT
- **Four-term decomposition:** ΔW = A-B-C-D reveals mechanistic structure
  → Useful for: Farey sequence researchers

### New discoveries:
- **Prime gap spectroscope (3.8x):** Gaps carry zero information — NOVEL
  → Useful for: prime gap researchers, Cramér model
- **Smooth number spectroscope (2.9x):** Connects to Dickman function
  → Useful for: factoring algorithm researchers
- **Fourth moment (96x):** Connects to Montgomery pair correlation
  → Useful for: RMT community, Keating/Snaith

### Applications:
- **Class number bounds (5-14x):** Via Siegel zero exclusion
  → Useful for: Bhargava/Wood/Ellenberg
- **"Previously impractical → now feasible" framing:**
  - Batch L-function at q>400: faster than individual computation
  - GRH verification for 9592+ characters simultaneously
  - Class numbers unconditional where Goldfeld gives ~1
  - Primes in progressions for large q where Siegel-Walfisz fails
  → Useful for: computational NT broadly

### RH connection (speculative):
- **Low-rank structure → density estimates:** Guth-Maynard 2024 pipeline
  → Useful for: zero-density theorem researchers
  → 10-20% chance of publishable partial result (Codex assessment)

## SPARSE RECOVERY / CS THEORY RESEARCHERS

| Researcher | Affiliation | Why they'd care |
|-----------|-------------|----------------|
| Emmanuel Candès | Stanford | Founder of CS/RIP theory. Our detection characterization (1/ζ vs ζ products) is a new algebraic criterion for which structures support sparse recovery |
| Holger Rauhut | RWTH Aachen | Structured random matrices + RIP. Our prime matrix is a natural structured matrix |
| Simon Foucart | Texas A&M | Compressive sensing theory. Our upper RIP from large sieve is a new example |
| Jean Bourgain's school | Various | Deterministic RIP constructions. Our prime matrix contributes to this program |
| Jelani Nelson | UC Berkeley | Dimensionality reduction. The "detection pattern" (1/L vs L products) is relevant to which sketching structures preserve sparse information |

Our relevant findings for this community:
- Upper RIP from large sieve (proved, unconditional)
- Detection pattern: only 1/L(s) and -L'/L(s) types support sparse recovery of zeros
- Products like ζ(s-1)/ζ(s) interfere — the numerator's oscillations destroy recovery
- This is a new ALGEBRAIC CRITERION for RIP-like properties
