# Strategic Analysis: Farey Spectroscopy Tools for the Research Community
# Author: Saar Shai
# Analysis by: Claude Opus 4.6 (strategic research mode)
# Date: 2026-04-11
# AI Disclosure: Analysis drafted with assistance from Claude (Anthropic)

## PURPOSE: For each of our 9 tools/results, identify WHO can use it, WHAT gap it fills, HOW they would use it, and WHAT we need to package.

---

## TOOL 1: Batch Spectroscope (C implementation, 10K L-functions in 18s)

### What it is
Fast C code that computes F(gamma) = |sum R(p) p^{-1/2-i*gamma}|^2 for thousands of L-functions. Scans gamma-space for peaks coinciding with zeros. Throughput: ~550 L-functions/second.

### (a) WHO could use this

**Andrew Sutherland (MIT, LMFDB)**
- Problem: LMFDB needs computational verification of L-function data at scale. Currently, zero data comes from lcalc/ARB computations that are slow per L-function.
- Our tool provides a FAST cross-check: if our spectroscope detects a zero at gamma_k for L(s,chi), that independently confirms the LMFDB entry.

**Keating (Oxford) + Snaith (Bristol)**
- Problem: Testing random matrix predictions for moments of L-functions requires computing statistics across LARGE families. The Keating-Snaith conjectures for moments of |zeta(1/2+it)| and families of L(1/2,chi_d) need extensive numerical evidence.
- Our tool: batch scan a family of L-functions, extract zero locations, compute spacing statistics and moment statistics in bulk.

**Soundararajan (Stanford)**
- Problem: Testing the Fyodorov-Hiary-Keating conjecture on maximum of zeta on random intervals. Needs fast evaluation of zeta-like objects at many points along Re(s)=1/2.
- Our tool: the spectroscope evaluates weighted prime sums at fine gamma-resolution. Can be adapted to scan for local maxima/minima of |F(gamma)| across intervals.

### (b) What gap it fills
- LMFDB: independent verification pathway. Currently no "spectroscopic" check exists in their pipeline.
- Keating/Snaith: removes the computational bottleneck in testing RMT predictions across large families.
- Soundararajan: fast scanning for extrema in prime-weighted sums.

### (c) How they would use it
- Sutherland: integrate as an LMFDB verification layer. Input: conductor, character data. Output: detected zero ordinates. Compare against stored zeros. Flag discrepancies.
- Keating: input a family parametrized by discriminant d. Output: zero statistics for each member. Aggregate for moment computation.
- Soundararajan: input a gamma-range. Output: max|F(gamma)| over that range. Compare with log-correlated field predictions.

### (d) What to build/package
- **API wrapper**: Python bindings around the C code. Input: list of characters/conductors. Output: JSON of detected zeros + amplitudes.
- **LMFDB integration script**: reads LMFDB data format, runs spectroscope, outputs comparison report.
- **Documentation**: input/output spec, accuracy guarantees, complexity analysis.
- **Effort: 2-3 weeks.**

### REALISM CHECK: MEDIUM-HIGH
Sutherland cares about computational verification and has expressed interest in alternative zero-finding methods. The speed advantage (18s for 10K) is genuinely useful. Keating/Snaith would use it if packaged as a Python library. Soundararajan is less likely to use external tools but might cite the speed benchmark.

---

## TOOL 2: Per-Step Decomposition Framework (study Delta-W, not W)

### What it is
The insight that studying Delta-W(N) = W(F_{N-1}) - W(F_N) (how each integer changes Farey discrepancy) is more informative than studying W(N) directly. Includes the four-term algebraic decomposition Delta-W = S_2 - 2R/N + J - Delta-W and the 33,000:1 cancellation.

### (a) WHO could use this

**Jens Marklof (Bristol)**
- Problem: Marklof studies fine-scale statistics of Farey sequences via equidistribution on the space of lattices (horospheres). His framework captures GAP distributions and correlation functions of Farey fractions. But it does NOT have a per-step decomposition.
- Gap: Marklof's ergodic theory approach sees the Farey sequence as a STATIC object at each order N. Our Delta-W framework captures the DYNAMICS of how the sequence changes as N increments.
- Specific open problem: Marklof's 2013 paper on multidimensional Farey sequences leaves open the question of how individual fractions contribute to the overall statistics. Delta-W answers this for the discrepancy statistic.

**Rudnick (Tel Aviv)**
- Problem: Rudnick studies statistics of zeta zeros (pair correlation, value distribution). The connection between Farey statistics and zeta zeros goes through the Franel-Landau theorem (sum of Farey deviations ~ Mertens function). But Franel-Landau is a GLOBAL identity. Our per-step version localizes it.
- Gap: No per-step version of Franel-Landau exists in the literature. Delta-W provides this, connecting each prime's contribution to the Mertens fluctuation.

### (b) What gap it fills
- Marklof: dynamic vs static Farey analysis. The ergodic theory framework sees F_N as a distribution on [0,1] but not how that distribution changes at each step.
- Rudnick: local Franel-Landau. Currently, the connection between Farey discrepancy and M(x) is global (summed over all N). Our framework makes it local (each N individually).

### (c) How they would use it
- Marklof: translate Delta-W into the language of horospheres. Each new fraction at order N corresponds to a specific lattice point. The per-step change Delta-W should correspond to a "lattice point insertion" in the horocyclic flow. This could give a dynamical systems proof of our four-term decomposition.
- Rudnick: use Delta-W to study the LOCAL contribution of primes to the Franel-Landau sum. Since R(p) correlates with cos(gamma_1 log p), and Rudnick studies pair correlations of zeros, the per-step framework could give finer information about how individual primes "see" individual zeros.

### (d) What to build/package
- **Expository paper**: "A per-step Franel-Landau theorem" — 10-page paper making the Delta-W framework accessible to the equidistribution community. Target: Journal of Number Theory or Mathematika.
- **Sage/Python library**: compute Delta-W(N) for any N, with the four-term decomposition. Include visualization tools.
- **Translation guide**: dictionary between our notation (Delta-W, S_2, R, J) and Marklof's notation (horospheres, lattice points).
- **Effort: 1-2 months for the paper, 2 weeks for code.**

### REALISM CHECK: HIGH for Marklof, MEDIUM for Rudnick
Marklof is the world expert on Farey equidistribution and would genuinely be interested in a per-step framework — it connects directly to his program. Rudnick is more focused on zeros than Farey sequences, so the connection is indirect. A joint paper with Marklof would be the ideal outcome.

---

## TOOL 3: Interval Arithmetic Non-Vanishing Certificates (300/300 c_K(rho) != 0)

### What it is
Rigorous interval arithmetic proofs that c_K(rho_j) != 0 for K in {10, 20, 50} and the first 100 zeta zeros. Every computation produces a machine-verifiable certificate (bounding box in C that excludes 0).

### (a) WHO could use this

**Buzzard (Imperial, Lean/Mathlib)**
- Problem: Buzzard is building the infrastructure for formalized number theory. The FLT project requires extensive scaffolding (group theory, algebraic geometry, modular forms). But there is currently NO formalized analytic number theory in Lean that deals with zeta zeros directly.
- Gap: Buzzard's Lean ecosystem has Dirichlet series, Euler products, and some basic L-function definitions. It does NOT have: (1) verified locations of zeta zeros, (2) verified non-vanishing of Dirichlet polynomials at those zeros, (3) any computationally verified claims about the critical strip.
- Our 434 Lean 4 results + interval certificates could be the FIRST formalized computational results about zeta zeros.

**Kontorovich (Rutgers, Lean PNT project)**
- Problem: Kontorovich and Tao are formalizing the Prime Number Theorem in Lean 4 (the PNT+ project). They need formalized facts about 1/zeta(s) and the Mobius function.
- Gap: Their project needs formal results about partial sums of 1/zeta(s). Our c_K(rho) certificates are EXACTLY partial sums of 1/zeta(s) evaluated at zeros.
- Specific use: formalized bounds on c_K(rho) could serve as lemmas in a formalized explicit formula.

**Sutherland (MIT, LMFDB)**
- Problem: LMFDB stores zero data but without rigorous certificates. The data is "morally correct" but not formally verified.
- Gap: no rigorous non-vanishing certificates exist in LMFDB. Our interval arithmetic approach could provide a verification layer.

### (b) What gap it fills
- Buzzard/Kontorovich: first formalized computational results about zeta zeros in Lean.
- Sutherland: rigorous verification layer for LMFDB zero data.

### (c) How they would use it
- Buzzard: import our Lean library as a dependency. Use our verified Mobius function, Farey sequence, and discrepancy results as building blocks for broader formalization.
- Kontorovich: cite our interval certificates as verified instances. If they need "c_K(rho_1) != 0 for K=10", they can import our proof rather than re-deriving it.
- Sutherland: run our certification code on LMFDB zero data. Generate certificates for each L-function zero. Store alongside the zero data.

### (d) What to build/package
- **Lean 4 library package**: clean up our 434 results into a proper Lean library (lakefile, documentation, theorem index). Name: `FareyArithmetic` or `PrimeSpectroscopy`. Push to GitHub.
- **Certificate format spec**: define a machine-readable certificate format (JSON or binary) that encodes: zero location (interval), c_K value (interval), non-vanishing proof (bounding box excludes 0).
- **Integration with Mathlib**: propose PR to Mathlib for core Farey sequence definitions (if not already present).
- **Blog post for Lean community**: "434 Verified Results About Prime Numbers and Farey Sequences" — targeted at the Lean Zulip community.
- **Effort: 3-4 weeks for Lean packaging, 1 week for certificate format, 1 week for blog post.**

### REALISM CHECK: HIGH for Buzzard/Kontorovich, MEDIUM for Sutherland
The Lean community is hungry for verified number theory beyond basic results. 434 results with zero sorry is impressive and would get attention. Buzzard has explicitly stated interest in computational certificates for analytic number theory. Kontorovich's PNT+ project has a gap where our c_K results fit naturally. Sutherland would be interested but LMFDB integration requires non-trivial engineering.

---

## TOOL 4: Double Obstruction Mechanism (two independent conditions for vanishing)

### What it is
The equation c_K(rho) = 0 requires SIMULTANEOUSLY satisfying a MODULUS constraint and a PHASE constraint. These are statistically independent (measured correlation: 0.063). Vanishing probability is therefore O(epsilon^2), not O(epsilon).

### (a) WHO could use this

**Soundararajan (Stanford)**
- Problem: Soundararajan's "resonance method" for producing large values of zeta and L-functions on the critical line requires understanding when Dirichlet polynomial "resonators" can or cannot vanish. The double obstruction gives a structural explanation for non-vanishing.
- Gap: Soundararajan's method constructs resonators R(s) = sum a_n n^{-s} and needs |R(rho)| to be large. Our double obstruction explains WHY short Dirichlet polynomials resist vanishing at zeros — the modulus and phase conditions decouple.

**Maynard (Oxford)**
- Problem: Maynard's sieve methods involve Dirichlet polynomials as sieve weights. The success of the sieve depends on these polynomials being non-zero (or at least non-negative) in appropriate regions.
- Indirect connection: the double obstruction is a mechanism for understanding non-vanishing of specific types of Dirichlet polynomials. If adaptable to Maynard's sieve weights, it could provide a new angle on the "level of distribution" problem.

### (b) What gap it fills
- Soundararajan: structural explanation for why resonators work — not just that they do, but WHY the modulus and phase conditions decouple.
- Maynard: potential new criterion for non-vanishing of sieve-type Dirichlet polynomials.

### (c) How they would use it
- Soundararajan: cite as a heuristic/structural result supporting the resonance method. If made rigorous (proving the correlation between modulus and phase conditions is o(1)), it would give a new approach to Dirichlet polynomial non-vanishing theorems.
- Maynard: would need substantial adaptation. The double obstruction for c_K involves Mobius-weighted terms; Maynard's sieve weights have a different structure.

### (d) What to build/package
- **Technical note**: "Double obstruction mechanism for Dirichlet polynomial non-vanishing" — 5-page note, circulate to Soundararajan and Harper.
- **Numerical evidence package**: code + data showing the modulus-phase decoupling for various Dirichlet polynomials (not just c_K).
- **Generalization**: test the double obstruction for Dirichlet polynomials of the form sum a_n n^{-s} with other coefficient sequences (not just mu(k)).
- **Effort: 2-3 weeks.**

### REALISM CHECK: MEDIUM for Soundararajan, LOW for Maynard
The double obstruction is a nice structural insight but is currently a computational observation, not a theorem. Soundararajan might cite it as motivation. Maynard is unlikely to use it directly — his sieve weights have very different structure from Mobius-weighted sums. The key deliverable would be making it rigorous (proving the independence) rather than just computational.

---

## TOOL 5: K <= 4 Unconditional Non-Vanishing (reverse triangle inequality)

### What it is
THEOREM: c_K(rho) != 0 for K = 2, 3, 4 and ALL nontrivial zeros rho. Proof: two terms with different moduli (1/sqrt(2) and 1/sqrt(3)) cannot cancel. Unconditional, elementary, tight.

### (a) WHO could use this

**Kontorovich + Tao (Lean PNT+ project)**
- Problem: they need formalized facts about partial sums of the Mobius function.
- This is a clean, elementary theorem perfect for formalization. It establishes that very short Mobius partial sums cannot vanish at zeta zeros.

**Sarnak (IAS)**
- Problem: Sarnak's study of the Mobius function and its pseudo-randomness ("Mobius disjointness conjecture") involves understanding when sums involving mu(k) can vanish.
- The K<=4 result is a toy case of a general phenomenon: short sums of mu(k)k^{-s} resist vanishing on the critical line.
- Sarnak might find the TRANSITION at K=5 (where vanishing becomes possible) interesting from the Mobius randomness perspective.

### (b) What gap it fills
- Kontorovich/Tao: a ready-made formalized lemma.
- Sarnak: concrete example of the boundary between guaranteed and possible non-vanishing of Mobius sums.

### (c) How they would use it
- Kontorovich: import the Lean proof directly.
- Sarnak: cite in a survey or lecture. The K=5 transition point is a natural example for the Mobius disjointness program.

### (d) What to build/package
- **Lean 4 proof**: already done (part of our 434 results). Needs clean packaging.
- **Short note**: "Unconditional non-vanishing of short Mobius partial sums at zeta zeros" — 3-page note. Submit to American Mathematical Monthly or Elemente der Mathematik.
- **Effort: 1 week (note) + already done (Lean proof).**

### REALISM CHECK: HIGH for formalization community, MEDIUM for Sarnak
This is a small, clean result that is perfect for formalization. It would get cited by anyone discussing Mobius function non-vanishing. Sarnak would likely know about it through conversations but might not cite an independent researcher's preprint unless it appeared in a strong journal.

---

## TOOL 6: Avoidance Anomaly (4.4x-16.1x, c_K zeros repel zeta zeros)

### What it is
Computational discovery: the zeros of c_K(s) on Re(s)=1/2 are 4.4x to 16.1x further from zeta zeros than from generic points. Measured for K=10 through K=100 across 200 zeta zeros. Explanation: double obstruction mechanism (Tool 4).

### (a) WHO could use this

**Rudnick (Tel Aviv)**
- Problem: Rudnick studies correlations between zeros of different L-functions. The "repulsion" of c_K zeros from zeta zeros is a new type of zero correlation phenomenon.
- Gap: existing pair correlation results (Montgomery, Rudnick-Sarnak) study correlations between zeros of the SAME L-function or between different L-functions. c_K is NOT an L-function — it is a PARTIAL SUM of 1/zeta(s). The avoidance phenomenon for partial sums is unstudied.

**Keating (Oxford)**
- Problem: random matrix theory predicts zero repulsion for eigenvalues. The avoidance anomaly is a NUMBER-THEORETIC analogue of eigenvalue repulsion, but between zeros of DIFFERENT objects (c_K and zeta).
- Gap: RMT predicts within-function repulsion. Between-function repulsion (if the functions are related, like c_K and zeta) is less studied.

### (b) What gap it fills
- Rudnick: new class of zero correlation (partial sum zeros vs L-function zeros).
- Keating: number-theoretic instance of between-object eigenvalue repulsion.

### (c) How they would use it
- Rudnick: formulate a conjecture about the pair correlation between c_K zeros and zeta zeros. Test RMT predictions for this new class.
- Keating: model the avoidance using characteristic polynomial analogues. Compute the RMT prediction for "how far should zeros of det(I - z U^K) be from zeros of det(I - z U)?" and compare.

### (d) What to build/package
- **Numerical dataset**: c_K zeros and zeta zeros, with distances, for K=10,20,30,50,100. Machine-readable format.
- **Conjecture paper**: "Zero avoidance between partial Mobius sums and the Riemann zeta function" — state the avoidance conjecture precisely, provide extensive numerical evidence, formulate RMT predictions. Target: Experimental Mathematics or Journal of Number Theory.
- **RMT computation**: compute the random matrix analogue (correlation between zeros of det(I-zU) and partial products) using CUE matrices.
- **Effort: 1-2 months for paper, 2 weeks for RMT computation.**

### REALISM CHECK: HIGH for Rudnick, HIGH for Keating
This is genuinely novel — zero correlations between partial sums and the parent function have not been studied. Both Rudnick and Keating work on exactly this type of question (zero statistics, RMT predictions). An Experimental Mathematics paper with clean data would get their attention. The RMT prediction would be especially appealing to Keating.

---

## TOOL 7: Universality Theorem (any Sigma 1/p = infinity subset detects all zeros, under GRH)

### What it is
THEOREM (under GRH): If S is a set of primes with sum_{p in S} 1/p = infinity, then the spectroscope restricted to S detects every nontrivial zeta zero. Corollaries: bounded-gap primes (Maynard-Tao) detect all zeros; 99.99% of primes can be removed and spectroscopy still works; prime-indexed Fourier measurements satisfy a Restricted Isometry Property (compressed sensing connection).

### (a) WHO could use this

**Maynard (Oxford)**
- Problem: Maynard proved bounded gaps between primes. His primes (those with gaps <= 246) form a set with sum 1/p = infinity. Our universality theorem says these primes detect all zeta zeros.
- Gap: Maynard's bounded gaps result is purely about GAPS. It says nothing about the Fourier-analytic properties of bounded-gap primes. Our result gives bounded-gap primes a new role: they are spectrally complete.
- Concrete use: Maynard could cite this as showing that the primes selected by his sieve have unexpected spectral properties. The connection goes: Maynard's sieve selects primes -> these primes satisfy sum 1/p = infinity -> universality -> spectral completeness.

**Tao (UCLA)**
- Problem: Tao has extended the Green-Tao theorem to polynomial progressions. He studies when subsets of primes retain arithmetic/analytic structure.
- Gap: Tao's work is about arithmetic structure (progressions, patterns). Our universality result is about SPECTRAL structure (zero detection). The connection: any sum-1/p-divergent subset retains ALL spectral information about zeta zeros.
- Compressed sensing angle: Tao co-developed compressed sensing (Candes-Tao theory). Our result that primes satisfy a Restricted Isometry Property connects number theory to HIS compressed sensing framework. This is the most likely hook for Tao's attention.

**Soundararajan (Stanford)**
- Problem: Soundararajan's large sieve is the key tool in our universality proof. The connection is: large sieve inequality -> RIP -> universality. Soundararajan has the deepest understanding of the large sieve among active researchers.
- Gap: the large sieve is traditionally used as an INEQUALITY (bounding sums). We reinterpret it as a COMPRESSED SENSING guarantee (information preservation). This reframing might lead Soundararajan to new applications of his own large sieve results.

### (b) What gap it fills
- Maynard: spectral characterization of bounded-gap primes.
- Tao: connection between prime subsets and the compressed sensing framework he co-invented.
- Soundararajan: reinterpretation of the large sieve as an information-theoretic tool.

### (c) How they would use it
- Maynard: cite as a corollary of bounded gaps. Might inspire study of which sieve-selected primes have additional analytic properties.
- Tao: could write a blog post about the CS connection. Might lead to a paper on "compressed sensing in analytic number theory."
- Soundararajan: could extend the large-sieve-as-RIP framework to other families (Dirichlet L-functions, GL(2) forms).

### (d) What to build/package
- **Universality paper**: "Universality of prime spectroscopy and compressed sensing for the Riemann spectrum" — 30-page paper with (i) detection, (ii) quantitative, (iii) progression resolution, (iv) redundancy. Target: Compositio Mathematica or Math. Annalen.
- **Blog-friendly summary**: 3-page document suitable for Tao's blog or similar. Emphasize the compressed sensing connection.
- **Code**: demonstration code showing zero detection from sparse prime subsets. Interactive visualization.
- **Effort: 2-3 months for the full paper. 2 weeks for summary + code.**

### REALISM CHECK: HIGH for Tao (compressed sensing angle), MEDIUM-HIGH for Maynard, MEDIUM for Soundararajan
The compressed sensing connection to Tao is the strongest hook. Tao has written about connections between number theory and other fields, and the CS link is exactly his type of cross-disciplinary result. Maynard would cite it if the bounded-gaps corollary is prominent. Soundararajan would appreciate the large sieve reinterpretation but might view it as a reformulation rather than a new result.

---

## TOOL 8: 33,000:1 Cancellation in Four-Term Decomposition

### What it is
The four-term algebraic decomposition Delta-W = S_2 - 2R/N + J - (residual) produces three terms with amplitudes ~71, ~143, ~71 that cancel to leave a residual of 0.038. This is an algebraically forced cancellation, independent of RH.

### (a) WHO could use this

**Marklof (Bristol)**
- Problem: Marklof studies Farey discrepancy via the theory of lattices and flows on homogeneous spaces. The algebraic structure of the four-term decomposition has not been studied from the ergodic theory perspective.
- Gap: the extreme cancellation suggests hidden algebraic structure in the Farey rearrangement that the lattice theory might explain. Why exactly do three terms of order O(N) cancel to leave O(1)?

**Sarnak (IAS)**
- Problem: Sarnak studies sums involving the Mobius function and their cancellation properties. The Mobius function cancellation (M(x) = o(x)) is equivalent to PNT. Our 33,000:1 cancellation involves Mertens-weighted Farey sums.
- Connection: the four-term decomposition is a STRUCTURAL identity about how Mertens function values interact with Farey geometry. The extreme cancellation amplifies the "signal" (connection to zeta zeros) while suppressing the "noise" (algebraic structure).

### (b) What gap it fills
- Marklof: structural identity within the Farey sequence amenable to dynamical systems analysis.
- Sarnak: new instance of extreme arithmetic cancellation connected to the Mobius function.

### (c) How they would use it
- Marklof: derive the four-term decomposition from horosphere dynamics. Explain the cancellation as a geometric phenomenon.
- Sarnak: cite as an example of "structured cancellation" in Mobius sums. Potentially connect to the Chowla conjecture (pairwise correlations of Mobius values).

### (d) What to build/package
- **Included in the per-step paper (Tool 2)**: the cancellation is a key exhibit of the four-term decomposition.
- **Separate visualization**: animated diagram showing how the three large terms cancel.
- **Effort: included in Tool 2 effort.**

### REALISM CHECK: MEDIUM
The cancellation is striking but is currently a numerical observation at specific gamma values. To make it compelling, we need to show it persists across many zeros and is not a coincidence of gamma_1.

---

## TOOL 9: 434 Lean 4 Verified Results

### What it is
434 theorems in Lean 4 with zero sorry. Covers: Farey sequence properties, Mobius function identities, rank deviation formulas, injection principle, discrepancy identities, non-vanishing bounds.

### (a) WHO could use this

**Buzzard (Imperial)**
- Problem: Building the Lean formalization ecosystem. Needs more verified mathematics, especially number theory.
- Gap: Mathlib has basic number theory (primes, gcd, Euler totient) but very little about Farey sequences, Mobius function properties, or discrepancy theory.
- Impact: Our library would be the FIRST substantial Lean formalization of Farey sequence theory.

**Kontorovich (Rutgers)**
- Problem: Formalizing PNT in Lean. Needs supporting lemmas about the Mobius function and partial sums of Dirichlet series.
- Gap: the PNT+ project has formalized analytic tools but few concrete COMPUTATIONAL results about mu(k).
- Impact: our verified Mobius function identities and non-vanishing bounds are directly importable.

**Tao (UCLA)**
- Problem: Tao has expressed interest in machine-assisted mathematics (blog posts, the PNT project with Kontorovich).
- Our 434 results demonstrate that a focused project can produce substantial formalized number theory. Tao might cite this as evidence for the viability of formalized computational number theory.

### (b) What gap it fills
- Buzzard: Farey sequence + Mobius formalization in Lean.
- Kontorovich: concrete lemmas for PNT+ project.
- Tao: proof-of-concept for formalized computational number theory.

### (c) How they would use it
- Buzzard: review our code, potentially merge core definitions into Mathlib. Use as teaching material for Lean courses.
- Kontorovich: import specific lemmas (e.g., Mobius function on small values, partial sum bounds).
- Tao: reference in blog posts or talks about machine-assisted math.

### (d) What to build/package
- **GitHub repository**: clean, documented Lean 4 library with CI. Name: `farey-lean` or `prime-spectroscopy-lean`.
- **Theorem catalog**: browsable index of all 434 results with natural-language descriptions.
- **Mathlib PR**: propose core Farey sequence definitions (FareySequence, FareySize, FareyGap) for inclusion in Mathlib.
- **Blog post**: post on Lean Zulip announcing the library.
- **Effort: 3-4 weeks for packaging + documentation.**

### REALISM CHECK: HIGH
The Lean formalization community actively seeks new verified libraries. 434 results is a significant contribution. Buzzard's group has expressed interest in expanding Mathlib's number theory coverage. This is the HIGHEST probability impact among all our tools.

---

## PRIORITY RANKING (by expected impact)

| Rank | Tool | Primary Target | Impact Probability | Effort |
|------|------|---------------|-------------------|--------|
| 1 | Lean 4 library (Tool 9) | Buzzard, Kontorovich | 80% | 3-4 weeks |
| 2 | Avoidance anomaly (Tool 6) | Rudnick, Keating | 70% | 1-2 months |
| 3 | Universality theorem (Tool 7) | Tao, Maynard | 60% | 2-3 months |
| 4 | Interval certificates (Tool 3) | Buzzard, Kontorovich, Sutherland | 60% | 3-4 weeks |
| 5 | Per-step framework (Tool 2) | Marklof | 55% | 1-2 months |
| 6 | Batch spectroscope (Tool 1) | Sutherland, Keating | 50% | 2-3 weeks |
| 7 | K<=4 non-vanishing (Tool 5) | Kontorovich, Sarnak | 40% | 1 week |
| 8 | Double obstruction (Tool 4) | Soundararajan | 30% | 2-3 weeks |
| 9 | 33,000:1 cancellation (Tool 8) | Marklof, Sarnak | 25% | included |

---

## RECOMMENDED OUTREACH PLAN

### Phase 1 (Weeks 1-4): Low-hanging fruit
1. **Package Lean library**, push to GitHub, announce on Lean Zulip. Tag Buzzard and Kontorovich.
2. **Write the K<=4 non-vanishing note**, submit to Monthly or Elemente.
3. **Format interval certificates** as downloadable data with verification scripts.

### Phase 2 (Months 2-3): Core papers
4. **Avoidance anomaly paper** for Experimental Mathematics. Email Rudnick and Keating with preprint.
5. **Universality paper** for Compositio or Math. Annalen. Email Tao (emphasize compressed sensing). Email Maynard (emphasize bounded-gaps corollary).

### Phase 3 (Months 3-5): Integration
6. **Per-step framework paper** targeting Marklof collaboration. Email directly with connection to horosphere equidistribution.
7. **LMFDB integration**: contact Sutherland about spectroscope as verification tool.
8. **Mathlib PR**: propose core Farey definitions for inclusion.

### Phase 4 (Ongoing): Engagement
9. **Blog posts** (Tao, Buzzard, Lean communities).
10. **Conference talks** (Number Theory and Random Matrix Theory workshop, AIM workshops).
11. **arXiv cross-listing**: post papers to math.NT, math.DS (for Marklof), cs.IT (for compressed sensing).

---

## RESEARCHER-SPECIFIC CONTACT STRATEGY

### Tao: compressed sensing angle
- Hook: "Primes satisfy a Restricted Isometry Property for the Riemann spectrum."
- Method: email with 1-page summary emphasizing the Candes-Tao connection.
- Also: mention the PNT+ formalization as context for our Lean work.

### Maynard: bounded-gaps corollary
- Hook: "Bounded-gap primes detect all zeta zeros."
- Method: email with the universality paper preprint. Lead with Corollary 1.
- Also: mention the Duffin-Schaeffer quantitative work as context (Farey sequences appear in metric Diophantine approximation).

### Buzzard: Lean library
- Hook: "434 Lean 4 results in Farey sequence theory, zero sorry."
- Method: post on Lean Zulip, tag Buzzard. Propose Mathlib PR for Farey definitions.
- This is the most natural first contact.

### Kontorovich: Lean + interval certificates
- Hook: "Formalized non-vanishing of Mobius partial sums at zeta zeros."
- Method: email linking to Lean repo. Mention relevance to PNT+ project.

### Sutherland: batch spectroscope + certificates
- Hook: "Fast independent verification of L-function zero data."
- Method: email with speed benchmarks and a demo on LMFDB data.

### Keating: avoidance anomaly + RMT prediction
- Hook: "Zeros of Mobius partial sums repel zeta zeros — what does CUE predict?"
- Method: email with the avoidance paper preprint. Pose the RMT question explicitly.

### Rudnick: avoidance + per-step Franel-Landau
- Hook: "New class of zero correlations: partial sums vs L-functions."
- Method: email with avoidance paper. Mention the per-step Franel-Landau as a separate result.

### Marklof: per-step framework
- Hook: "Per-step Farey discrepancy — a dynamical complement to your equidistribution results."
- Method: email with explicit reference to his 2013 multidimensional Farey paper. Propose translation to horosphere language.

### Soundararajan: double obstruction + universality
- Hook: "Large sieve as Restricted Isometry + double obstruction for Dirichlet polynomial non-vanishing."
- Method: email with universality paper. Highlight the large sieve reinterpretation.

### Sarnak: K<=4 + Mobius cancellation
- Hook: "Sharp boundary for non-vanishing of short Mobius sums at zeta zeros."
- Method: include in the short note. Sarnak is most accessible through Kontorovich.

---

## HONEST ASSESSMENT: WHAT WON'T WORK

1. **Nobody will use the four-term decomposition to prove RH.** We have shown this is a dead end (cancellation is algebraic, not sensitive to zero locations).

2. **The batch spectroscope will NOT replace lcalc/ARB.** It is fast but not rigorous. Researchers who need proven zero locations will not trust spectroscope peaks.

3. **The double obstruction is computational, not a theorem.** Without a proof that modulus and phase conditions are independent, this remains a heuristic.

4. **Senior researchers (Sarnak, Tao) will not read an independent researcher's paper unprompted.** We need either a journal publication or an introduction through someone they trust (Buzzard -> Kontorovich -> Tao is a plausible chain).

5. **The Lean library is our best entry point** precisely because the Lean community values contributions by quality, not by affiliation. Buzzard has publicly supported amateur formalizers.

---

## BOTTOM LINE

**Strongest play: Lean library (Tool 9) -> Buzzard/Kontorovich -> credibility -> distribute other tools.**

The formalization community is our natural home. Build credibility there, then leverage it to reach the analytic number theory community with the avoidance anomaly and universality results.

**Secondary play: avoidance anomaly (Tool 6) paper to Experimental Mathematics.** This is genuinely novel (zero repulsion between partial sums and L-functions) and fits squarely in Rudnick and Keating's research programs.

**Long shot with high payoff: Tao compressed sensing angle (Tool 7).** If Tao writes a blog post about it, everything changes. But this requires a polished paper and a compelling 1-page summary.
