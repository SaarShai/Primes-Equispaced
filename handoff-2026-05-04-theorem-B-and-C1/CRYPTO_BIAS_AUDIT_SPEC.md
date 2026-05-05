---
title: "Cryptographic Bias Audit Framework — design spec v0.1"
type: design
domain: crypto-audit
created: 2026-05-03
confidence: 0.7
tags: [koyama, chebyshev-bias, prng-audit, randomness-beacon, lean4, crest-grant]
---

# Bottom line

Build open-source, formally-verified tool that audits cryptographic randomness sources for prime-residue distribution biases. Combines Koyama's "-1 Dominance" theory + cluster-scale computation + Lean 4 certificates. Targets randomness beacons (drand, NIST, RANDAO), VRFs (Algorand, Cardano), PRNGs (system, library), and crypto prime generation.

Pitched for CREST grant under "Mathematical Science for Prediction and Control" theme.

# Problem statement

Existing PRNG / randomness audit tools (NIST SP 800-22, TestU01, dieharder) check for general statistical anomalies. They do NOT include number-theoretic bias tests of the kind predicted by:

- Chebyshev's bias (1853): π(x; q, a) for non-residue a > π(x; q, b) for residue b
- Koyama -1 Dominance (2026): among non-residues, -1 mod q dominates other non-residues
- L(1, χ) modulated bias hierarchies (Koyama Theorem 1.1, Definition 1.2)

For deployed crypto systems that generate or use primes / residues at large scale, these biases:
- Are too small to detect in individual key samples (exponentially suppressed by prime size)
- ARE detectable in aggregate beacon outputs (10^7-10^9 samples, 256-bit values mod small q)
- Could mask backdoored RNGs that pass standard tests but fail bias-hierarchy tests

# Threat model

| Threat | Detectable by framework? | Severity |
|---|---|---|
| Backdoored PRNG (Dual_EC_DRBG style) | YES — bias hierarchy mismatch | CRITICAL |
| Subtly biased VRF implementation | YES — output distribution test | HIGH |
| Validator-coordinated RANDAO bias | YES — bias amplification across blocks | HIGH |
| Threshold signature collusion | partially — depends on bias signature | MEDIUM |
| Algorithmic rounding bias | YES — short modulus tests | MEDIUM |
| Chebyshev-bias in RSA prime sampling | NO at scale 10^617 — exponentially suppressed | LOW (theoretical) |

# Architecture

```
biasaudit/
├── theory/
│   ├── chebyshev_bias.md      # classical theory
│   ├── koyama_dominance.md    # -1 dominance theorem + predictions
│   └── target_specific.md     # bias predictions per target type
├── stats/
│   ├── chi_squared.py         # uniformity test
│   ├── neg_one_dominance.py   # one-sided bias test
│   ├── hierarchy_corr.py      # correlation w/ L(1,χ) predictions
│   └── cross_modulus.py       # consistency across q
├── targets/
│   ├── drand_adapter.py       # historical fetch + parse
│   ├── randao_adapter.py      # ETH archive node
│   ├── nist_beacon_adapter.py
│   ├── prng_adapter.py        # /dev/urandom, OpenSSL, etc.
│   └── prime_gen_adapter.py   # for RSA/ECC key gen audits
├── compute/
│   ├── segmented_sieve.c      # cluster-scale tally pipeline
│   ├── checkpointed_runner.py # restartable
│   └── cluster_dispatcher.py
├── lean/
│   ├── KoyamaDominance.lean   # theorem statements
│   ├── StatTestCorrectness.lean # verified test code
│   └── Certificates.lean      # audit cert format
└── certify/
    ├── report_generator.py
    ├── signed_certificates.py
    └── verifier.py            # third-party verifier
```

# Statistical tests (initial set)

## Test 1: Chi-squared mod q

Given K outputs interpreted as integers mod q (q ∈ {3, 4, 5, 7, 8, 11, 13, 16, ...}), compute observed counts O_a in each residue class. Expected count under uniform: E_a = K/φ(q) for a coprime to q.

χ² = Σ (O_a − E_a)² / E_a

Compare to χ² distribution with φ(q) − 1 degrees of freedom.

## Test 2: -1 Dominance one-sided

Define D_q = O_{-1} − max_{a ≠ ±1, gcd(a,q)=1} O_a.

Under uniform null: D_q ≈ Normal(0, σ²) with σ² ≈ 2K/φ(q) (approx).

Under Koyama bias (for ACTUAL prime distributions): D_q > 0 with magnitude proportional to L(1, χ) residual.

For pseudorandom outputs (hashes): null is uniform → ANY positive D_q is suspicious.

## Test 3: Bias-hierarchy correlation

Compute D_q for q ∈ Q = {3, 4, 5, 7, 8, 11, 13}. Predict ranking by Koyama Theorem 1.1: D_q proportional to L(1, χ_q^*) for fundamental discriminant.

Spearman rank correlation observed vs predicted. High correlation = bias structurally matches Koyama (suspicious if NOT expected).

## Test 4: Cross-modulus consistency

For q | q': D_q should be derivable from finer-grained data D_{q'}. Inconsistency = manipulation.

# Targets — expected sample sizes

| Target | Historical samples | Output size | Test mode |
|---|---|---|---|
| drand mainnet | ~10^7 (since 2019) | 256-bit | uniform null |
| NIST beacon | ~10^7 (since 2013) | 512-bit | uniform null |
| Ethereum RANDAO | ~10^9 (since merge 2022) | 256-bit | uniform null |
| Algorand VRF | ~10^9 (since 2019) | varies | uniform null |
| Cardano VRF | ~10^8 (since 2020) | varies | uniform null |
| /dev/urandom | unlimited | byte stream | uniform null |
| Bitcoin keypairs (CT logs) | ~10^9 unique | 256-bit | uniform null |
| RSA keys (CT logs) | ~10^9 unique | 2048-bit primes | prime null |

# Lean 4 formalization scope

Phase 1 (paper-ready):
- Koyama Theorem 1.1 statement (no proof needed initially)
- Definition 1.2 (bias strength via L(1, χ))
- Statistical test correctness (chi-squared, normal approximation)

Phase 2 (deployment-ready):
- Verified implementation of segmented residue counter
- Audit certificate format with verification predicate
- End-to-end: input data → certificate → external verifier

Build on existing Saar Lean library (377 named theorems incl. BridgeIdentity, CWMellinShift).

# Compute scaling

Design for checkpointable, clusterable from start.

| Scale | Wall time (1 modern CPU) | Use case |
|---|---|---|
| 10^7 samples | minutes | drand archive |
| 10^9 samples | hours | RANDAO archive |
| 10^14 primes (Koyama target) | days on cluster | -1 dominance verification |

# Deliverables milestone plan

**Month 1-2:** prior art review, methodology lock, prototype on drand sample
**Month 3-4:** RANDAO + NIST beacon adapters, statistical test suite
**Month 5-6:** Lean 4 phase 1, paper draft on methodology
**Month 7-9:** cluster-scale Koyama verification at 10^14
**Month 10-12:** v1.0 release, audit reports on real systems, second paper

# Why this fits CREST

- "Prediction and Control" = predict bias, certify or flag systems
- Concrete social impact: trust certification for crypto/randomness primitives
- Saar's combined skills (compute + Lean + design + entrepreneurship) maps directly
- Real partner pipeline: DeNA already engaged, more crypto/finance natural fits

# Open questions (parallel research dispatched)

1. **Prior art**: what exists in this space? Are there NIST efforts? Academic precedent? (Opus survey running)
2. **Statistical methodology**: precise sample sizes, power analysis, null-hypothesis design (Opus running)
3. **Target deep-dive**: drand and RANDAO architecture, data access, threat models (Opus running)

# Confidence + caveats

Confidence 0.7. Core idea is sound. Risks:
- Bias signal in pseudorandom outputs may be too small even at 10^9 samples
- Existing PRNG tests may already catch what we'd catch (unlikely but verify)
- Lean 4 formalization scope creep
- Patent landscape for "bias-aware crypto" needs scan (Saar's patent background helps)

# v0.2 update — synthesized from 3 parallel research dispatches

## Prior art (CRYPTO_BIAS_AUDIT_PRIOR_ART.md)
- Gap confirmed: no PRNG battery, no beacon audit, no verified crypto library tests prime-residue / Chebyshev bias
- 6 novel application areas (G1-G6)
- 8+ historical bias-failures cataloged — Chebyshev framework = complementary canary, not replacement

## Statistical methodology (CRYPTO_BIAS_AUDIT_STATS.md)
- Two-mode framing: prime-source (test FOR Koyama bias) vs pseudorandom-source (test against uniform)
- Test 2 redesigned: subtract second-best non-trivial competitor (n_{-1} − max{n_a : a ≠ ±1})
- Variance: 2Kp from multinomial covariance
- Sample-size headlines: drand K=10^7 → 0.28% detection floor; RANDAO K=10^9 → 10^{-4}
- Validation gates: must reproduce Chebyshev on raw primes ≤ 10^{10} + show null on /dev/urandom 10^{10} BEFORE deployment
- Multiple-comparisons: Bonferroni α=10^{-3} family-wise

## Target deep-dive (CRYPTO_BIAS_AUDIT_TARGETS.md)
- **drand Quicknet**: BLS12-381 G1, 3s period, ~34M sigs since 2020. Bias-by-grinding crypto-impossible. Detection floor 10^{-4} at N=28M. **No published statistical audit exists.**
- **Ethereum RANDAO**: ~290k epoch mixes / 9.4M reveals since 2022-09. Alpturer-Weinberg AFT 2024 predicts bias for top stakers. **Lido (~28%) and Coinbase (~9%) bias is ABOVE √N noise floor at boundary epochs — first empirical confirmation possible.**
- EIP-7998 (Aug 2025) would replace randao_reveal with VRF, killing attack — not adopted yet
- Forking-RANDAO ePrint 2025/037 searched empirically, no traces on mainnet

## STRATEGIC DECISION: RANDAO first

Higher leverage than drand because:
- Theoretical bias prediction exists (Alpturer-Weinberg)
- Predicted bias above noise floor for top stakers
- Empirical confirmation/refutation = novel publishable result
- 7 days wall-clock with beacon archive node

drand follows as week-3 deliverable: clean baseline, expected null result, demonstrates framework operational.

## Updated milestone plan

**Week 1-2:** RANDAO empirical test of Alpturer-Weinberg bound
**Week 3:** drand statistical audit
**Week 4:** Lean 4 phase 1 (Koyama theorem statement + test correctness)
**Week 5-6:** methodology paper draft + open-source tool release + CREST grant section
**Week 7-12:** scale to 10^14 Koyama -1 Dominance computation (Koyama's main ask)

## Validation gates (per Saar Computational Verification Gates rule)

Before any "bias detected" claim:
1. Reproduce Chebyshev bias on raw primes ≤ 10^{10} (positive control)
2. Null on /dev/urandom 10^{10} samples (negative control)
3. mpmath verification at 30 digits of all L(1, χ_q) values used
4. Cross-check Koyama theorem statement: GRH-conditional vs unconditional, effect-size constants

## Critical confidence note

"No obscure paper anticipates this" = medium confidence only. 30-min sweeps insufficient. Recommend Google Scholar + IACR ePrint deep search + direct queries to Bernstein, Heninger, Sarnak before committing to publication path.

## Updated overall confidence

0.7 → 0.78 after synthesis. Direction is sound. Specific RANDAO target has highest publishability. Remaining unknowns: (1) thorough prior-art sweep, (2) actual Lido/Coinbase epoch boundary data confirms or refutes Alpturer-Weinberg.

# v0.3 update — methodology lessons from prototype runs

## Lesson 1: single-x deviation test doesn't detect Chebyshev bias

Prototype v1 (chi-squared + D_q) on primes ≤ 10^7:
- All q ∈ {4, 5, 7, 8, 11}: NULL results (p > 0.7)
- Reason: Chebyshev bias signal at x=10^7 is ~200, CLT noise σ≈408 → SUB-CLT
- Even at x=10^14, the bias signal vs CLT noise ratio is bounded — single-x test of this kind cannot detect

**Implication:** chi-sq test as defined fails for Chebyshev / Koyama bias. Must use race / lead-fraction / quantile statistics.

## Lesson 2: lead-fraction is arcsine-distributed under uniform null

Prototype v2 (race methodology):
- Positive control (primes ≤ 10^7): fraction(3 leads mod 4) = **0.9995** vs Rubinstein-Sarnak prediction 0.9959 ✓
- **Negative control (urandom 10^6 samples): fraction(3 leads mod 4) = 0.985 — ALSO ABOVE 0.99**

**Why the failed negative control:** lead-fraction for a SINGLE random walk is arcsine-distributed (not uniform). Single-realization lead-fraction CANNOT distinguish biased from unbiased.

**Real implication:**
- For PRIMES: Rubinstein-Sarnak / Koyama logarithmic density is well-defined deterministic property. Koyama's 10^14 verification is well-posed.
- For PRNG/beacon audit: need MULTI-realization framework — split N samples into K chunks, distribution of per-chunk fractions distinguishes arcsine (null) from concentrated-near-1 (bias).

## Updated test suite

**Test 1 (deprecated):** Single-sample chi-squared / D_q — not useful for Chebyshev-style bias.

**Test 2 (NEW):** Multi-realization lead-fraction distribution
- Split N samples into K chunks of size N/K
- For each chunk: compute lead fraction (race -1 vs other non-residues mod q)
- Test distribution: 
  - Null (uniform random): arcsine distribution
  - Bias (Chebyshev/Koyama): distribution concentrated near specific value > 0.5
- KS test against arcsine

**Test 3 (NEW):** Max |S_n| scaling
- Compute max_n |n_{-1}(n) - n_a(n)| for n up to N
- Null: max scales as √(N log log N) (law of iterated logarithm)
- Bias: max scales as N · |L(1,χ)|/log N (Koyama prediction)
- Distinguishable for N ≥ ~10^9

**Test 4 (preserved):** Logarithmic density of leads (Saar/Koyama 10^14 main project)
- For primes: well-defined per Rubinstein-Sarnak
- Koyama's main computational target

## Honest re-pitch for CREST

Two-track value proposition:

**Track A (mathematics):** Koyama -1 dominance at 10^14 — well-posed verification of analytic number theory prediction. Mathematical rigor + cluster-scale compute. Saar's role: clean.

**Track B (cryptographic application):** Multi-realization bias detector for randomness sources. NOVEL test methodology (no PRNG suite has this). Distinguishes arcsine-null random walks from concentrated-bias walks. Less easy than pitched, but still publishable + practically useful.

Track A is the mathematical centerpiece. Track B is the applied translation that justifies the "predict + control" framing.

## Updated confidence

0.78 → 0.65 after methodology lessons. Direction still sound but more nuanced than initially pitched. The "easy detection in 10^7 beacon samples" framing was naïve — real test needs multi-realization or specific scaling statistics.

## Next steps

1. **Validate v3 prototype** (multi-realization arcsine vs concentrated): split samples into chunks, KS test against arcsine
2. **Verify Koyama logarithmic density on primes ≤ 10^9** (positive control for Track A)
3. **Update CREST proposal section** with two-track structure
4. **Patent scan** still pending
