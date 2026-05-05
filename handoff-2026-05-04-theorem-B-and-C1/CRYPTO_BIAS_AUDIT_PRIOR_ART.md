# Prior Art Survey: Cryptographic Bias Audit Framework

Scope: tooling that audits cryptographic randomness sources (RNGs, VRFs, beacons) for the prime-residue / Chebyshev-Koyama-style asymptotic biases predicted by analytic number theory. Survey window: ≤30 min, focused on what exists vs gaps.

Date: 2026-05-03. Author: Saar Shai. Confidence levels per section noted.

---

## 1. PRNG / RNG test suite landscape (what exists)

The dominant batteries in widespread use:

- **NIST SP 800-22 Rev 1a** (Rukhin et al., 2010; current rev finalised pre-2020). 15 tests: frequency, block frequency, runs, longest-run, binary matrix rank, DFT (spectral), non-overlapping/overlapping template matching, Maurer's universal, linear complexity, serial, approximate entropy, cumulative sums, random excursions, random excursions variant. Outputs p-values; pass/fail at α=0.01.
- **NIST SP 800-90B** (Turan et al., final 2018). Entropy-source assessment standard, not a randomness test per se. Provides 10 min-entropy estimators (most-common-value, collision, Markov, compression, t-tuple, LRS, multi-MCW, lag, MultiMMC, LZ78Y) plus IID permutation tests. Used for FIPS 140-3 entropy validation.
- **TestU01** (L'Ecuyer & Simard, 2007, ACM TOMS). The strongest battery. Predefined suites: SmallCrush (10 tests), Crush (96 tests), BigCrush (160 tests). Includes birthday spacings, collision, gap, poker, coupon collector, permutation, sample autocorrelation, run, matrix rank, Hamming weight, random walk, linear complexity, etc.
- **Diehard / Dieharder** (Marsaglia 1995; Brown's Dieharder ~2003-2018). Birthday spacings, OPSO/OQSO/DNA, parking lot, minimum distance, 3D spheres, squeeze, sums, runs, craps. Now considered weaker than TestU01 BigCrush.
- **PractRand** (Doty-Humphrey, ~2010-present, unmaintained but widely used). Adaptive sample-size testing, very strong at finding low-bit biases in modern PRNGs.
- **ENT** (Walker), **gjrand**. Smaller batteries.

**What none of these test for:** prime-residue distribution biases. The closest are:
- Spectral / DFT tests (look at Fourier structure, not multiplicative structure mod q).
- Serial / approximate entropy (look at k-gram frequencies, agnostic to arithmetic structure).
- Linear complexity (Berlekamp-Massey; algebraic but over GF(2), not mod q for odd q).

No test in any standard battery measures π(N; q, a) - π(N; q, b) -style residue counts on output streams, nor checks for the log-log Chebyshev oscillation. **This is a real gap.** Confidence: high.

## 2. Randomness beacon audit landscape

Deployed public beacons:
- **NIST Randomness Beacon** (random.nist.gov, since 2013; rebooted 2018 as v2.0 with NIST SP 800-90B-validated entropy sources). 512-bit pulse every 60s, signed.
- **drand / League of Entropy** (since 2019). t-of-n threshold BLS signatures over BLS12-381; current epoch 30s pulse. Members: Cloudflare, EPFL, Kudelski, Protocol Labs, U. Chile, etc. Used by Filecoin leader election.
- **Ethereum 2.0 RANDAO** (post-Merge, 2022-). Per-slot BLS signature of epoch counter from block proposer, XORed into running mix.
- **Algorand sortition VRF** (Gilad et al., SOSP 2017). ECVRF-EDWARDS25519-SHA512.
- **Cardano Ouroboros Praos** (Eurocrypt 2018) and **Genesis** (CCS 2018) VRF-based slot leader election.

Published attacks / audits:
- **RANDAO Last-Revealer Attack**: Hwang et al., arXiv:2403.09541 (2024). 2^k bias for k consecutive tail proposers. Alpturer, AFT 2024 (LIPIcs vol. 316), "Optimal RANDAO Manipulation in Ethereum". Forking the RANDAO, ePrint 2025/037.
- **EIP-7998** (2025): proposal to replace RANDAO with proper VRF-based reveal.
- **ECVRF security analysis**: Peikert & Shiehian via Esgin et al., "Classical and Quantum Security of Elliptic Curve VRF", PKC 2023 / ePrint 2023/223. Indifferentiability argument.
- **Breaking X-VRF**: FC 2024, post-quantum VRF used in Algorand-style sortition shown to fail uniqueness (deterministic algorithm produces two valid outputs for same input).
- **Cardano grinding**: CIP-0161 "Ouroboros Phalanx" (2024-25), CPS-0021 "Ouroboros Randomness Manipulation". Acknowledges grinding cost ~10^10× for honest vs adversary.
- **drand** has internal cryptographic security proofs (Syta et al., S&P 2017 on RandHerd/RandHound; Cachin et al. on threshold BLS) but no public third-party formal audit specifically on output bias.

**What auditors check for:** unbiasability under adversarial proposer models, unpredictability, liveness, threshold security. **What no one checks:** distributional biases of the bit-stream output (mod-q residue class counts, Chebyshev-style log-log skew). Confidence: high.

## 3. Historical bias-related crypto failures (8 incidents)

1. **Dual_EC_DRBG backdoor** — Shumow & Ferguson, CRYPTO 2007 rump session. NIST-standardised PRNG with NSA-controllable backdoor via P/Q point relationship. Withdrawn 2014. RSA BSAFE shipped it as default. Snowden 2013 confirmed NSA influence. (Bernstein et al., ePrint 2015/767 "Dual EC: A Standardized Back Door".)
2. **Debian OpenSSL PRNG bug (CVE-2008-0166)**, May 2008. Removal of an "uninitialised memory" line reduced entropy to PID space (~32k seeds) for 20 months. Massive key reissuance.
3. **Sony PS3 ECDSA static-k**, fail0verflow CCC 2010. Same nonce in every signature → trivial private key recovery from two signatures.
4. **Mining your Ps and Qs** — Heninger, Durumeric, Wustrow, Halderman, USENIX Security 2012 (Best Paper). 0.75% of TLS certs and 0.50% of TLS host RSA keys factorable via batch GCD due to shared primes; 1.03% of SSH DSA hosts had recoverable keys due to nonce reuse. All traced to weak boot-time entropy in embedded devices.
5. **Bernstein et al. "Factoring RSA keys from certified smart cards: Coppersmith in the wild"**, ASIACRYPT 2013. Taiwan Citizen Digital Certificate cards: shared primes in supposedly-certified hardware RNGs.
6. **ROCA / Infineon RSALib (CVE-2017-15361)** — Nemec, Sys, Svenda et al., CCS 2017. Structured prime generation makes 1024/2048-bit keys factorable in practical time. Affected millions of TPMs, Estonian eID.
7. **Bitcoin Android wallet ECDSA nonce bug**, August 2013. SecureRandom seeded poorly on Android < 4.2; multiple wallets reused nonces, lost funds.
8. **Juniper ScreenOS Dual_EC backdoor swap**, December 2015. Attacker-replaced Q-point in Dual_EC inside NetScreen firewalls, allowing VPN traffic decryption. (Checkoway et al., USENIX Security 2016.)

Common thread: every failure was a **uniformity / independence** failure, not an asymptotic-bias failure. Standard tests would have caught most (Debian PID-bounded seeds, PS3 static k, ROCA structured form) — but they were not run, or not run on production output. Confidence: high.

## 4. Number-theoretic bias literature (very thin, as expected)

- **Chebyshev's bias** (1853 letter to Fuss): π(x; 4, 3) > π(x; 4, 1) "almost always". Rubinstein-Sarnak, *Experimental Mathematics* 1994 — the canonical analytic treatment, conditional on GRH + Grand Simplicity Hypothesis. Density δ(q;a,b) defined.
- **Granville-Martin, AMM 2006**, "Prime number races" — survey.
- **Ford-Sneed 2010**, "Chebyshev's bias for products of two primes" — extends to semiprimes (relevant to RSA modulus distribution).
- **Fiorilli-Martin** various, on secondary terms.
- **Koyama 2026** (draft): "Dominance of −1" — among quadratic non-residues mod q, the class containing −1 dominates. The user's specific framework.

**Cryptographic uptake:** essentially zero. The Number Analytics blog post and a Wolfram MathWorld entry vaguely mention "implications for RSA prime selection", but no concrete cryptographic test, no audit tool, no paper that proposes "given a bit stream from a beacon, partition its 256-bit chunks by residue class mod q, test for Chebyshev-style log-log oscillation."

Closest hits to genuine crypto-relevant number-theoretic auditing:
- **Google's `paranoid_crypto`** library (open source 2022): checks for ROCA, Mersenne-form, shared factors, Coppersmith-attackable structure. **Does not** test residue distributions mod small primes on signature outputs or beacon output.
- **Cohen-Lenstra-style heuristics** are used in elliptic curve security analysis but not in deployed audit tools.

Confidence: high that this gap exists; medium that no obscure paper has anticipated it (a thorough literature search would take longer than 30 min).

## 5. Formal verification of crypto primitives

- **HACL\*** (Bhargavan et al., CCS 2017; ePrint 2017/536). F\*-verified C library. Curve25519, Ed25519, ChaCha20-Poly1305, AES-GCM, SHA-2/3, HMAC, HKDF. Verifies memory safety, functional correctness, secret-independence (timing). **Does not verify randomness quality** — its `Lib_RandomBuffer` is unverified glue around `/dev/urandom` / `BCryptGenRandom`.
- **EverCrypt** (Protzenko et al., CSF 2020). Cross-platform provider combining HACL\* + Vale (verified assembly). Same randomness caveat.
- **fiat-crypto** (Erbsen et al., S&P 2019). Coq-verified field arithmetic for curve operations. Used in BoringSSL, Firefox NSS. No randomness verification.
- **Jasmin / Cryptol / SAW**: verified-assembly toolchains; crypto correctness, not statistical bias.
- **CertiCrypt / EasyCrypt**: game-based proofs of cryptographic protocols; no statistical-distribution verification on real outputs.

**Gap:** no formal-verification project currently states or proves quantitative bounds of the form "the output distribution lies within ε of uniform mod q for q ≤ Q" for production RNGs / VRFs. This is a verification gap **and** a measurement gap. Confidence: high.

## 6. Identified gaps where Koyama-style bias audit would be NOVEL

**G1. No PRNG battery tests for prime-residue / Chebyshev structure.** A Koyama-aware test would partition the output stream into n-bit chunks, treat each as an integer, count residue class membership mod each prime q in a small set (3, 5, 7, 11, ..., Q), and apply a log-log-oscillation test calibrated against Rubinstein-Sarnak densities. **Genuinely novel** as a battery addition.

**G2. No randomness beacon audit looks at output distribution mod q.** drand, NIST Beacon, RANDAO, Algorand VRF, Cardano VRF — all are audited for unbiasability under adversarial-proposer models, none for asymptotic distributional biases. Running a Koyama-bias detector against the full drand history (~5 years × 2 pulses/min ≈ 5M pulses × 64 bytes) is a tractable, novel audit.

**G3. Detection of biased PRNGs in deployed embedded devices.** Heninger-Halderman 2012 used GCD on RSA moduli to find shared primes. Koyama-bias detection on the *output stream* of an embedded RNG (e.g., a TPM's `getrandom` output before key generation) is a complementary technique that could detect biased entropy sources before they generate weak keys, not after. **Novel angle**: bias-detection as RNG quality canary, not just key-recovery.

**G4. RSA prime distribution audit.** Ford-Sneed bias for products-of-two-primes predicts non-uniform density of N = pq across residue classes mod small q. Auditing the distribution of deployed RSA-2048 moduli (e.g., from Censys / certificate transparency) for Chebyshev-Koyama deviation from the predicted bias is a plausible novel measurement. (Could either detect anomalies or confirm the theorem on a 10^9-modulus dataset.)

**G5. VRF output Chebyshev test.** ECVRF (Algorand, Cardano) outputs are claimed indistinguishable from uniform under DDH-style assumptions. A Koyama-style residue test gives a *concrete numerical* falsifiability criterion: predict an effect size, measure on production data, contradict the indistinguishability claim if found. No published work does this.

**G6. Formal-verification target.** Stating "HACL\* / EverCrypt RNG output has Koyama-bias bounded by f(N, q)" is a new specification target. Currently nobody specifies, let alone verifies, the bias profile of verified-crypto RNG output.

Highest-leverage opportunities, in priority order:
1. G2 — drand + Beacon audit. Public data, reproducible, immediate.
2. G4 — TLS modulus dataset (Censys has these) audit. Tests theorem on real data.
3. G1 — battery contribution. Long-term standards influence.
4. G5 — falsifiability claim against ECVRF.

## 7. Confidence and caveats

**High confidence:**
- Standard batteries (NIST 800-22, TestU01, PractRand, Dieharder) do not include prime-residue Chebyshev-style tests. Verified by reviewing each suite's published test list.
- No deployed beacon audit checks for asymptotic distributional bias mod q.
- HACL\* / EverCrypt do not verify randomness quality.

**Medium confidence:**
- No obscure paper has proposed exactly this audit framework. A 30-min survey cannot exclude this; recommend a follow-up dedicated literature search on Google Scholar + IACR ePrint with queries like "Chebyshev bias cryptographic test", "prime race randomness", "Koyama bias", "residue class statistical test cryptography". My search returned zero direct hits, but absence of evidence ≠ evidence of absence.

**Low confidence / open:**
- Whether the predicted effect size (Koyama dominance of −1 mod q) is large enough at N = 2^256 sample sizes to be statistically detectable above sampling noise. **Computational verification gate applies** (per global rules): before claiming this is a useful audit, must compute Σ over real beacon data the predicted Chebyshev difference and confirm it exceeds 3σ at realistic sample sizes. This is the critical sanity check before publishing.
- Whether "secondary to Dirichlet equidistribution" means the effect is too small to be useful in cryptographic detection. Needs numerical estimation against the convergence rate predicted by Koyama's theorem.

**Caveats / red flags to verify before claims (per common.md gates):**
- Verify Koyama's "Dominance of −1" theorem is correctly stated with explicit conditions (GRH? unconditional?) and effect-size constants.
- Verify Rubinstein-Sarnak densities δ(q; a, b) by direct mpmath computation before citing.
- Cross-check on an independent residue-class enumeration (e.g., π(10^9; 8, 1), π(10^9; 8, 3), π(10^9; 8, 5), π(10^9; 8, 7)) before any "novel detection" claim.

**Key citations (single SOT for next phase):**
- Rubinstein & Sarnak, *Exper. Math.* 3 (1994) 173-197.
- Heninger et al., USENIX Security 2012.
- L'Ecuyer & Simard, ACM TOMS 33 (2007) 22.
- Hwang et al., arXiv:2403.09541 (2024).
- Esgin et al., PKC 2023 / ePrint 2023/223.
- Bhargavan et al., CCS 2017 (HACL\*).
- Nemec et al., CCS 2017 (ROCA).
- Bernstein et al., ePrint 2015/767 (Dual EC).
- Checkoway et al., USENIX Security 2016 (Juniper).

---

End of survey. Word count ≈ 1850.
