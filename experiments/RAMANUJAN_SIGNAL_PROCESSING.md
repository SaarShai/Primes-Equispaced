# Ramanujan Sums in Signal Processing: Connection to Our Bridge Identity

Date: 2026-03-29
Status: Research complete, GO/NO-GO assessment at bottom

---

## 1. The Signal Processing Community's Work

### 1.1 Vaidyanathan & Tenneti (Caltech) — The Core Program

P. P. Vaidyanathan and Srikanth Tenneti at Caltech built an entire signal processing
framework on Ramanujan sums over 2014-2023:

**Foundation (2014):**
- "Ramanujan Sums in the Context of Signal Processing" Parts I & II
  (IEEE Trans. Signal Processing, Vol. 62, 2014)
- Established that c_q(n), being periodic with period q and integer-valued,
  is a natural basis for detecting integer periodicities in signals
- Key insight: c_q(n) serves as a "period-q detector" — it responds to
  components of period q while rejecting others

**Farey Dictionary (2014):**
- "The Farey-dictionary for sparse representation of periodic signals" (ICASSP 2014)
- Dictionary matrix A (N x Phi(Q)) with atoms e^{j2pi(k/q)n} for (k,q)=1
- Columns correspond to frequencies k/q from the Farey series
- Period estimation cast as sparse recovery: find sparsest x such that Ax = signal
- The Farey structure ensures orthogonality between different period subspaces

**Ramanujan Subspaces:**
- S_q = span of {e^{j2pi(k/q)n} : 1 <= k <= q, gcd(k,q)=1}
- dim(S_q) = phi(q) (Euler's totient)
- Key property: S_q contains ONLY signals of period exactly q (not divisors of q)
- Different S_q are mutually orthogonal

**Ramanujan Filter Banks (2015):**
- "Ramanujan filter banks for estimation and tracking of periodicities" (ICASSP 2015)
- "Properties of Ramanujan filter banks" (EUSIPCO 2015)
- Filter bank indexed by q = 1, 2, ..., Q_max
- q-th filter passes period-q components, rejects all others
- Produces a "time-period plane" analogous to the time-frequency plane
- Unlike wavelets: specifically tuned for integer periods via number theory
- Unlike comb filters: non-adaptive comb filters CANNOT separate periods unless
  they are Ramanujan filters (proved by Tenneti)

**Efficient Implementation (2017):**
- Multiplier-less structures using Mobius function (ICASSP 2017)
- The Mobius function mu(q) enables efficient filter construction
- Pei & Chang: 2D extensions for image processing

**Unified Theory (2016-2019):**
- Unified union-of-subspaces theory (IEEE Trans. SP, 2016)
- Critical data length: min samples = max(P_i + P_j - gcd(P_i, P_j))
- iMUSIC: MUSIC-like algorithms for integer periods (IEEE Trans. SP, 2019)

**Overview (2020):**
- "Srinivasa Ramanujan and signal-processing problems"
  (Philosophical Transactions of the Royal Society A, Vol. 378, 2020)
- Comprehensive review tying Ramanujan subspaces, Farey dictionaries,
  and filter banks into a unified framework

### 1.2 Planat et al. — The Number Theory Connection

Michel Planat (CNRS) established the deeper number-theoretic connections:

**Ramanujan-Fourier Transform (2002):**
- "Ramanujan sums for signal processing of low-frequency noise"
  (Phys. Rev. E 66, 056128, 2002)
- Introduced the RFT as alternative to DFT for arithmetical sequences
- Key observation: Mobius and Mangoldt functions are "coding sequences for primes"
- The Mertens function M(n) = sum mu(k) appears as the cumulative spectral density
- Connected 1/f noise in electronics to the Riemann Hypothesis via Ramanujan sums
- Farey spin chains and SL(2,Z) modular group invoked

**Long-Period Analysis (2008-2009):**
- "Ramanujan sums analysis of long-period sequences and 1/f noise" (EPL, 2009)
- Applied RFT to Dow Jones index (13 years) and solar coronal index (69 years)
- Showed RFT can discriminate long periods that Fourier sees as 1/f^alpha

### 1.3 Recent Work (2023-2025)

**Capon-Optimized RFBs (2023):**
- Kulkarni & Vaidyanathan: "Periodicity-Aware Signal Denoising Using
  Capon-Optimized Ramanujan Filter Banks" (IEEE Trans. SP, 2023)
- Hybrid analysis-synthesis framework with pruned Ramanujan dictionaries
- Addresses the false-period problem in standard RFBs

**Signal Recovery (2025):**
- Kalra & Shukla: "Ramanujan sums in signal recovery and uncertainty principle
  inequalities" (arXiv:2512.16190, Dec 2025)
- Perfect reconstruction property of Ramanujan filter banks
- Uncertainty principle via tight frame of Ramanujan sum shifts
- Non-uniform Ramanujan filter banks for handling large periods efficiently

**Biomedical Applications (2022-2025):**
- ECG QRS-complex detection via RFB periodicity estimation (2022)
- Myocardial infarction detection using Ramanujan sums wavelet transform (2025)
- Absence seizure detection in EEG via period tracking

**Geophysics (2024-2025):**
- Microseismic denoising via Ramanujan subspace + DTW (2024)
- Adaptive periodic mode decomposition for bearing fault diagnosis

---

## 2. Precise Mathematical Connection to Our Work

### 2.1 What They Use

The signal processing community uses Ramanujan sums as:

**Period detector:** For a signal x(n) with hidden period P, project onto S_q:
  x_q(n) = projection of x(n) onto span{c_q(n-k)}

If ||x_q|| is large, period q is present. The actual period is P = lcm of all
active q values.

**Filter construction:** The q-th Ramanujan filter has impulse response:
  h_q(n) = c_q(n) / phi(q)

This passes period-q components and annihilates others because c_q(n) is
orthogonal to c_r(n) for q != r (when evaluated over a full period).

**Dictionary atoms:** The Farey dictionary uses frequencies k/q for (k,q)=1,
which are exactly the Farey fractions! The dictionary is literally indexed
by the Farey sequence F_Q.

### 2.2 What We Proved

Our bridge identity:

  sum_{a/b in F_{p-1}} e^{2pi i p (a/b)} = M(p) + 2

Equivalently:

  sum_{q=1}^{p-1} c_q(p) = M(p)

Because for (q,p)=1 (which holds for all q < p when p is prime): c_q(p) = mu(q).
So the sum becomes sum mu(q) = M(p-1) = M(p) (since mu(p) adjusts by -1 but the
upper limit compensates).

More generally:

  sum_{a/b in F_N} e^{2pi i (a/b)} = 1 + M(N)

### 2.3 The Overlap — Honest Assessment

**What they already know:**
1. c_q(n) = mu(q) when gcd(q,n)=1 — THIS IS STANDARD (Ramanujan 1918)
2. sum of mu(q) = M(N) — THIS IS THE DEFINITION of Mertens function
3. Farey fractions index the Ramanujan subspaces — KNOWN since Vaidyanathan 2014
4. The Mobius function enables efficient filter construction — KNOWN since 2017
5. The RFT connects to the Mertens function — KNOWN since Planat 2002

**What they do NOT know (our contributions):**
1. The per-step analysis: How does adding the p-th Farey level change things?
   - Nobody studies Delta_W(p) = W(p) - W(p-1)
   - The signal processing community treats the Farey dictionary as STATIC
   - We treat it as DYNAMIC — a growing sequence of nested dictionaries

2. The Sign Theorem: sign(Delta_W(p)) is controlled by M(p)
   - This has NO analogue in their work
   - They use Ramanujan sums for period detection, not for understanding
     how the detection capability CHANGES as you increase the dictionary order

3. The Four-Term Decomposition (A + B + C + D):
   - They decompose signals into periodic components
   - We decompose the DISCREPANCY CHANGE into four algebraic terms
   - Completely different decomposition target

4. The Injection Principle: each Farey level adds at most 1 fraction per gap
   - This is about the GEOMETRY of Farey refinement
   - Relevant to adaptive dictionary design (see Section 3)

5. The Sigmoid Law: P(Delta_W < 0) follows a sigmoid in M(p)/sqrt(p)
   - A sharp empirical law with no analogue in signal processing

---

## 3. Potential New Contributions

### 3.1 Adaptive Ramanujan Dictionary Ordering (MOST PROMISING)

**The problem they face:** When estimating an unknown period P in a noisy signal,
the standard approach tests ALL periods q = 1, 2, ..., Q_max. For large Q_max,
this is computationally expensive (the dictionary has Phi(Q_max) ~ 3Q_max^2/pi^2
columns).

**What we offer:** Our per-step analysis tells you WHICH dictionary levels to add
first and when to stop.

Specifically:
- The Mediant Minimality theorem says new Farey fractions are always mediants
  of existing neighbors. This means adding level q to the dictionary inserts
  atoms that are "midway" between existing atoms in a precise sense.
- The Injection Principle guarantees at most 1 new atom per existing gap.
- Our discrepancy analysis tells you: if M(q) is large and negative, adding
  level q IMPROVES equidistribution (and thus dictionary coverage). If M(q)
  is positive, it may not help.

**Concrete proposal:** ADAPTIVE RAMANUJAN FILTER BANK
- Instead of testing q = 1, 2, 3, ..., Q_max sequentially:
  1. Start with small primes (they add the most new atoms per level)
  2. Prioritize levels q where mu(q) = -1 (squarefree with odd prime factors)
  3. Skip levels where mu(q) = 0 (non-squarefree: they add ZERO new subspace
     dimension to the Ramanujan decomposition anyway!)
  4. Use cumulative M(q) as a "coverage quality" metric

This is NOT obvious from the existing literature. They order filters by q = 1,2,3,...
which is natural but not optimal.

### 3.2 Sign Theorem as Detection Threshold

**The problem they face:** When is a detected period "real" vs. noise artifact?
The standard approach uses energy thresholds or statistical tests.

**What we offer:** The Sign Theorem says that when M(p) <= -3, the Farey sequence
at level p is strictly MORE equidistributed than at level p-1. In signal processing
terms: the Ramanujan dictionary at order p has strictly better "coverage" than at
order p-1.

This gives a NUMBER-THEORETIC detection criterion:
- If the signal's dominant period is q, and M(q) <= -3, then the Ramanujan
  filter at order q is in a "favorable regime" — the dictionary is well-conditioned.
- If M(q) > 0, the dictionary at that level may be poorly conditioned.

### 3.3 Compression for Farey-Sampled Signals

**Already partially explored in our compression_applications_findings.md:**
- The bridge identity gives O(1) spectral computation at prime frequencies
- 35,000x speedup at N=300 for Farey-sampled signals
- Prime frequencies carry disproportionate energy in polynomial signals

**New angle for signal processing:**
- For signals with rational frequency structure (music, communications),
  the Farey sampling + bridge identity gives a compressed spectral representation
- The "lossy compression" aspect (3000:1 at p=97) means the Ramanujan decomposition
  is inherently a DIMENSIONALITY REDUCTION technique
- Our quantification of the compression ratio is new

### 3.4 Non-Squarefree Filter Pruning (EASY WIN)

**Direct consequence of our analysis:**
- For non-squarefree q (like q=4, 8, 9, 12, ...), mu(q) = 0
- This means c_q(n) = 0 for gcd(q,n) = 1
- In the Ramanujan filter bank, these filters contribute NOTHING to coprime-argument
  signals
- About 30% of all integers up to Q are non-squarefree

**Impact:** You can prune ~30% of filters from the bank with NO loss for detecting
periods coprime to the signal's fundamental frequency. This is mentioned tangentially
in some papers but never connected to the Mertens function perspective.

---

## 4. Is This Publishable?

### 4.1 Target Venues

| Venue | Fit | Required Contribution |
|-------|-----|-----------------------|
| IEEE Trans. Signal Processing | Good | Need concrete algorithm + simulations showing improvement |
| ICASSP | Good | Shorter paper, proof-of-concept sufficient |
| IEEE Signal Processing Letters | OK | Short result, e.g., adaptive ordering theorem |
| Phil. Trans. Royal Society A | Stretch | Need deep mathematical content |

### 4.2 What Would Be Needed

For a publishable contribution, we would need:

1. **Algorithm:** Formally specify the Adaptive Ramanujan Filter Bank (ARFB)
   that uses M(q) to order filter application

2. **Theory:** Prove that the ARFB ordering reduces the expected number of
   filters needed to detect a period P, compared to sequential ordering

3. **Simulations:** Show on standard benchmarks (synthetic periodic signals
   in noise, ECG, DNA tandem repeats) that:
   - ARFB detects periods with fewer filters than standard RFB
   - The M(q)-based quality metric predicts detection accuracy
   - Non-squarefree pruning maintains accuracy while reducing computation

4. **Comparison:** Benchmark against Kulkarni & Vaidyanathan's Capon-optimized
   RFB (2023), which is the current state of the art

### 4.3 Realistic Assessment

**Strengths:**
- The adaptive ordering idea is genuinely new and practically useful
- The non-squarefree pruning is easy to implement and verify
- Connects two communities (analytic number theory, signal processing)
  that rarely talk to each other
- Vaidyanathan himself would likely find this interesting

**Weaknesses:**
- The improvement may be modest (constant factor, not asymptotic)
- Signal processing reviewers may not care about the number theory
- Number theory reviewers may not care about the signal processing
- We need ACTUAL SIMULATIONS to make this convincing, not just theory

**Estimated effort:** 2-3 weeks for a solid ICASSP-quality paper
                      2-3 months for IEEE Trans. Signal Processing

---

## 5. GO/NO-GO Assessment

### CONDITIONAL GO

**The honest truth:**

1. The bridge identity ITSELF is largely a restatement of what Planat (2002) and
   Vaidyanathan (2014) already know, viewed from a slightly different angle. The
   identity sum c_q(p) = M(p) for prime p follows immediately from c_q(p) = mu(q)
   when gcd(q,p)=1, which is Ramanujan's own result from 1918. If we write a paper
   claiming "we discovered that Ramanujan sums connect to Mertens," the signal
   processing community will not be impressed.

2. HOWEVER, our PER-STEP ANALYSIS is genuinely new. Nobody in signal processing
   studies how the Ramanujan dictionary changes INCREMENTALLY as you raise the
   order. The Sign Theorem, the Sigmoid Law, and the Four-Term Decomposition have
   no analogues in their literature.

3. The ADAPTIVE ORDERING idea is the most publishable contribution. It translates
   our per-step insights into a concrete algorithmic improvement.

### Recommended Path

**Phase 1 (1 week):** Build a proof-of-concept
- Implement standard Ramanujan Filter Bank in Python
- Implement M(q)-ordered variant
- Test on synthetic signals with known periods
- Measure: detection accuracy vs. number of filters used

**Phase 2 (decision point):** If Phase 1 shows >10% improvement in filter count
for same accuracy, proceed. If <10%, this is a NO-GO for signal processing venues
(but may still be worth noting in our math paper as a connection).

**Phase 3 (2 weeks):** Full paper
- Formal algorithm specification
- Theoretical analysis (expected filter count reduction)
- Comprehensive benchmarks
- Target: ICASSP 2027 submission

### What to NOT pursue:
- Do NOT try to publish the bridge identity as a signal processing contribution
  (it is already known in equivalent form)
- Do NOT try to improve period estimation accuracy (Vaidyanathan's theory is
  already optimal in certain senses)
- Do NOT try to connect the Riemann Hypothesis to signal processing (Planat
  already did this in 2002, and it led nowhere practical)

### What IS worth mentioning in our math paper:
- The bridge identity has a natural signal processing interpretation as the
  "total Ramanujan response" at a prime argument
- Per-step Farey discrepancy = per-level change in Ramanujan dictionary quality
- This connects our work to a well-established engineering community
- Cross-reference Vaidyanathan 2014, 2020 and Planat 2002

---

## 6. Key References

### Vaidyanathan & Tenneti (Caltech)
1. Vaidyanathan PP. "Ramanujan Sums in the Context of Signal Processing — Part I:
   Fundamentals." IEEE Trans. SP, 62(16):4145-4157, 2014.
2. Vaidyanathan PP. "Ramanujan Sums in the Context of Signal Processing — Part II:
   FIR Representations and Applications." IEEE Trans. SP, 62(16):4158-4172, 2014.
3. Vaidyanathan PP, Pal P. "The Farey-dictionary for sparse representation of
   periodic signals." ICASSP 2014, pp. 360-364.
4. Tenneti S, Vaidyanathan PP. "Ramanujan filter banks for estimation and tracking
   of periodicities." ICASSP 2015, pp. 3851-3855.
5. Tenneti S, Vaidyanathan PP. "Properties of Ramanujan filter banks." EUSIPCO 2015.
6. Tenneti S, Vaidyanathan PP. "A unified theory of union of subspaces representations
   for period estimation." IEEE Trans. SP, 64:5217-5231, 2016.
7. Tenneti S, Vaidyanathan PP. "Efficient multiplier-less structures for Ramanujan
   filter banks." ICASSP 2017, pp. 6458-6462.
8. Tenneti S, Vaidyanathan PP. "iMUSIC: a family of MUSIC-like algorithms for
   integer period estimation." IEEE Trans. SP, 67:367-382, 2019.
9. Vaidyanathan PP, Tenneti S. "Srinivasa Ramanujan and signal-processing problems."
   Phil. Trans. R. Soc. A 378:20180446, 2020.

### Planat et al.
10. Planat M, Rosu HC, Perrine S. "Ramanujan sums for signal processing of
    low-frequency noise." Phys. Rev. E 66:056128, 2002.
11. Planat M, Minarovjech M, Saniga M. "Ramanujan sums analysis of long-period
    sequences and 1/f noise." EPL 85:40005, 2009.

### Recent (2023-2025)
12. Kulkarni P, Vaidyanathan PP. "Periodicity-Aware Signal Denoising Using
    Capon-Optimized Ramanujan Filter Banks." IEEE Trans. SP 71:494-511, 2023.
13. Kalra S, Shukla NK. "Ramanujan sums in signal recovery and uncertainty
    principle inequalities." arXiv:2512.16190, Dec 2025.
14. Gupta A, Chandra Ray K. "Myocardial Infarction Detection Using Ramanujan Sums
    Wavelet Transform." IEEE Trans. Instr. Meas. 74:1-10, 2025.

### Our Work
15. Bridge identity: sum_{a/b in F_N} e^{2pi i (a/b)} = 1 + M(N)
    Formally verified in Lean 4 via Aristotle theorem prover.
16. Sign Theorem: For M(p) <= -3, Delta_W(p) < 0 (proved)
17. Per-step decomposition: Delta_W = A + B + C + D

---

## 7. Aletheia Classification

**Bridge identity as signal processing contribution:** C0 (collaborative, negligible novelty)
— The identity is already known in equivalent form. Repackaging it does not add value.

**Adaptive Ramanujan Filter Bank (if Phase 1 succeeds):** C1-C2
— Minor to publication-grade novelty depending on the magnitude of improvement.
— Autonomy level C because it requires human domain insight (connecting two fields)
  plus AI computational exploration.

**Per-step analysis as noted in math paper:** Part of the main paper's contribution,
not a separate signal processing claim.
