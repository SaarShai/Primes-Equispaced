# Practical Applications Deep Scan

Date: 2026-04-07
Status: Assessment complete

## Methodology

Each application scored on three axes:
1. **Buildable in 1-2 weeks?** (Y/N with caveats)
2. **Who uses it?** (concrete audience, not hand-waving)
3. **Prior art that crushes it?** (brutally honest)

Verdict scale: BUILD (genuine value + gap in market), INVESTIGATE (promising but needs prototype to confirm edge), SKIP (prior art dominates or benefit too marginal).

---

## A. Adaptive 1D Grid Generator

**Idea**: Mediant insertion with function-value priority to concentrate grid points near features (discontinuities, peaks, rapid variation).

**Buildable?** Yes. Core algorithm is ~200 lines. Priority queue over Farey gaps, evaluate f at mediant, push children. 1 week.

**Who?** Numerical methods practitioners, ODE/PDE solvers, quadrature users. Students doing adaptive integration.

**Prior art**: Standard adaptive mesh refinement (AMR) has been the workhorse since Berger-Oliger 1984. AMR uses error estimators (Richardson extrapolation, gradient-based) to decide where to refine. The key difference: AMR is error-driven (refine where error is large), Farey is structure-driven (refine where the gap is largest, modulated by function priority). In practice, AMR with a good error estimator will beat blind gap-filling every time for solving PDEs. However, for the simpler problem of "sample a 1D function adaptively for plotting or integration" the Farey approach gives a clean, deterministic, hierarchical scheme with no cascade (zero-cascading property). The mediant guarantee (smallest denominator = simplest fraction in each gap) is genuinely unique.

**Honest edge**: The niche is NOT competing with full AMR solvers. It is: a clean adaptive sampling library for 1D function plotting and tabulation where you want a hierarchical, invertible point set. Think matplotlib's adaptive plotting or Mathematica's adaptive sampling. These currently use ad hoc bisection. Farey mediant is a principled replacement for bisection that gives exact level-of-detail control.

**VERDICT: BUILD** -- Small, clean library. Genuine improvement over bisection-based adaptive sampling. Not an AMR competitor. Ship as a Python/Rust library for adaptive function sampling with LOD control.

---

## B. Hash Table with Perfect Load Balancing

**Idea**: Farey-mediant bucket splitting for hash tables. Each new bucket splits the largest gap.

**Buildable?** Yes, 1 week.

**Who?** Systems programmers building distributed hash tables or load balancers.

**Prior art**: Consistent hashing (Karger et al. 1997) already does ring-based gap splitting. Jump consistent hashing (Lamping & Veach, Google 2014) is O(1) memory, O(ln n) time, and achieves near-perfect balance. Rendezvous hashing (highest random weight) also solves this. The "bounded loads" variant (Mirrokni et al. 2018) guarantees max load within (1+epsilon) of average.

**Honest assessment**: The hashing space is saturated with excellent solutions. Farey mediants give you deterministic splits, but jump consistent hashing is already deterministic, O(1) memory, and battle-tested in production at Google scale. The Farey version adds mathematical elegance but zero practical advantage. The hash function quality matters far more than the bucket boundary placement.

**VERDICT: SKIP** -- Consistent hashing and jump hashing already dominate. No practical gap to fill.

---

## C. Video Streaming Bitrate Ladder

**Idea**: Place quality tiers at Farey-mediant positions in bitrate space. Adding a tier optimally fills the biggest quality gap.

**Buildable?** The Farey part is trivial (~50 lines). But a useful tool needs integration with encoding pipelines. 2 weeks for a standalone recommendation engine.

**Who?** Streaming services, video platform engineers.

**Prior art**: Netflix's per-shot convex hull encoding (2015+) is the industry standard. They exhaustively encode each scene at many bitrate-resolution pairs and pick the Pareto-optimal points. Recent ML-based approaches (2023-2026) predict convex hulls without exhaustive encoding. The ladder construction is content-dependent -- the optimal quality levels depend on scene complexity, not on abstract gap-filling.

**Honest assessment**: The fundamental problem is that bitrate ladders need to be content-adaptive. A scene with lots of motion needs different levels than a static talking head. Farey-based placement is content-blind. The convex hull approach dominates because it is content-aware. Farey could serve as an initial grid for the exhaustive encoding search, but that is a micro-optimization, not a product.

**VERDICT: SKIP** -- Content-dependent optimization dominates. Farey is content-blind. Marginal value as initial grid not worth a product.

---

## D. Color Quantization

**Idea**: Farey-based palette hierarchy where each color level is the mediant of neighbors. Progressive rendering with minimal-denominator palette.

**Buildable?** The 1D version is trivial. Extending to 3D color space (RGB) is non-obvious -- mediants of 3D rational vectors need careful definition. 2 weeks.

**Who?** Image processing, progressive web rendering, constrained devices.

**Prior art**: Median cut (Heckbert 1979), octree quantization, k-means clustering, spatial color quantization (Puzicha et al.). These are mature, optimized, and handle perceptual color spaces (CIELAB). The octree method is already hierarchical and supports progressive refinement natively.

**Honest assessment**: Color quantization is a solved problem with perceptually-tuned solutions. Farey mediants operate in a 1D rational number framework and do not naturally extend to 3D perceptual color space. Octree quantization already provides the hierarchical property. The Farey approach would be mathematically interesting but perceptually inferior to existing methods that account for human color perception. No practical edge.

**VERDICT: SKIP** -- Octree already hierarchical. Perceptual color spaces matter more than mathematical gap-filling. Solved problem.

---

## E. Rate Limiter / Token Bucket

**Idea**: N clients get slots at Farey positions k/N. Zero collision, deterministic, O(1) per request.

**Buildable?** Yes, 1 week. Very simple.

**Who?** API gateway developers, microservices architects.

**Prior art**: Token bucket, leaky bucket, sliding window log, sliding window counter, fixed window. All well-understood, widely implemented (nginx, Kong, Envoy, every cloud provider). Redis-based distributed rate limiters are battle-tested.

**Honest assessment**: The Farey approach gives perfectly spaced request slots, which sounds appealing. But rate limiting in practice deals with bursty traffic, not perfectly spaced requests. Token bucket explicitly ALLOWS bursts up to bucket capacity, which is a feature. Leaky bucket smooths traffic. The practical problems in rate limiting are: distributed state, clock skew, burst handling, fairness under contention. Perfectly even spacing is the EASY part -- it is what a simple modular clock already achieves (client i fires at time t if t mod N == i). You don't need Farey sequences for that.

**VERDICT: SKIP** -- Even spacing is trivial (modular arithmetic). Real rate limiting problems are elsewhere (distributed state, bursts). No value-add.

---

## F. Test Case Generation

**Idea**: Generate test inputs at Farey-spaced values to maximize coverage of [0,1] with minimal tests. Each new test fills the largest untested gap.

**Buildable?** Yes, 1 week. Very simple.

**Who?** QA engineers, property-based testing frameworks.

**Prior art**: Quasi-random testing using low-discrepancy sequences (Sobol, Halton, van der Corput) is well-established in the testing literature. Sobol sequences extend naturally to high dimensions and have theoretical guarantees (Koksma-Hlawka inequality). Boundary value analysis and equivalence class partitioning are standard QA techniques. Property-based testing (QuickCheck, Hypothesis) uses shrinking and coverage-guided generation.

**Honest assessment**: Farey sequences ARE low-discrepancy in 1D. But Sobol and Halton sequences are the standard for this and work in arbitrary dimensions. The Farey advantage (smallest-denominator-first = simplest-first testing) is a genuine conceptual selling point for 1D, but 1D is rarely the bottleneck. In high dimensions, Farey has no natural extension. The "simplest first" property maps to a nice story for testing -- test simple rational inputs before complex ones -- but in practice, test effectiveness depends on the failure region structure, not input simplicity.

**Edge case worth noting**: For testing numerical code specifically (roundoff, precision issues), Farey-ordered inputs DO have a unique property: they test all denominators systematically. This catches denominator-specific bugs that random testing misses. This is a genuine niche.

**VERDICT: INVESTIGATE** -- Niche value for numerical precision testing (denominator-systematic). Not competitive with Sobol/Halton for general coverage. Worth a small prototype to test the denominator-bug-finding claim.

---

## G. Audio/Music Polyrhythm Generator

**Idea**: Farey sequences generate rhythmic patterns; each denominator level adds beats at optimal positions.

**Buildable?** Yes, 1 week. Max/MSP patch or Python/JS library.

**Who?** Music producers, electronic musicians, creative coders, Max/MSP/Pure Data users.

**Prior art**: Euclidean rhythms (Toussaint 2005) are EXACTLY this. E(k,n) distributes k beats as evenly as possible among n positions using the Euclidean algorithm. This is equivalent to Farey-based beat placement. Euclidean rhythm generators are already ubiquitous: hardware modules (Mutable Instruments Grids, WMD Metron), software (Max/MSP externals, VCV Rack modules, Ableton devices, dozens of web apps). The connection between Euclidean rhythms, Stern-Brocot trees, and Farey sequences is well-known in the mathematical music theory literature.

**Honest assessment**: This is thoroughly explored territory. Euclidean rhythms ARE Farey rhythms under a different name. The market is saturated with implementations. Building another one adds nothing.

**What MIGHT be novel**: The LOD hierarchy aspect -- a rhythm generator where you smoothly add/remove complexity by moving up/down Farey levels. Most Euclidean generators set (k,n) statically. A "Farey LOD rhythm" where you sweep denominator depth in real-time to smoothly increase/decrease rhythmic complexity -- that might be a novel interaction paradigm. But it is a feature, not a product.

**VERDICT: SKIP** -- Euclidean rhythms (= Farey rhythms) are well-known and widely implemented. The LOD-sweep interaction is a minor novelty at best.

---

## H. Font Hinting / Subpixel Rendering

**Idea**: Place font grid points at Farey positions for optimal coverage at each resolution level.

**Buildable?** Extremely hard. Font rendering is one of the most complex, platform-specific areas in computing. 2 weeks is laughable.

**Who?** Font rendering engine developers (FreeType, DirectWrite, CoreText teams).

**Prior art**: TrueType hinting uses bytecode instructions to snap outlines to pixel grids. ClearType/FreeType handle subpixel rendering with extensive perceptual tuning. The rendering pipeline involves: outline scaling, grid fitting, rasterization, gamma correction, LCD filtering. Each step has decades of engineering.

**Honest assessment**: Font hinting is not a gap-filling problem. It is a constrained optimization problem: snap glyph control points to grid positions while preserving glyph shape, readability, and consistency across the font. The constraints (stem width consistency, alignment zones, overshoot suppression) are typographic, not mathematical. Farey positions have no relevance to these constraints. Furthermore, with high-DPI displays becoming standard, hinting is decreasingly important.

**VERDICT: SKIP** -- Wrong problem formulation. Font hinting constraints are typographic, not mathematical. Extremely high barrier to entry. Declining relevance with high-DPI displays.

---

## I. Progressive Data Transmission

**Idea**: Send data points in Farey order so each new point maximally reduces the receiver's uncertainty about the underlying signal. Optimal for lossy/interrupted channels.

**Buildable?** Core algorithm (Farey-order serialization) is 1 week. Useful demo with interruption tolerance, 2 weeks.

**Who?** Satellite communications, IoT with unreliable links, constrained bandwidth applications, progressive web loading.

**Prior art**: Progressive JPEG uses frequency-domain ordering (DC coefficients first, then AC). Wavelet-based compression (JPEG 2000, SPIHT, EZW) achieves progressive transmission via bit-plane coding. For 1D signals, these are well-established. For SPATIAL point data, the GIS community uses multi-resolution progressive transmission (Douglas-Peucker hierarchy, quadtree-based). Low-discrepancy sequences (van der Corput) already provide the "each new point fills the biggest gap" property -- and van der Corput IS essentially Farey order restricted to powers of 2.

**Honest assessment**: For 1D spatial data, Farey order is genuinely optimal in a specific sense: it minimizes the maximum gap after each insertion (this is the Farey injection principle). Van der Corput does this for base-2 subdivisions; Farey does it for ALL denominators, giving finer granularity. The practical question is: does this finer granularity matter compared to van der Corput or simple bisection?

**Where it genuinely helps**: Sensor networks transmitting non-uniformly-sampled 1D data (e.g., temperature along a pipeline, signal strength along a path). If transmission is interrupted, the receiver has the best possible approximation of the full signal. This is a real use case with a genuine Farey advantage over bisection (you get intermediate denominators like thirds, fifths, etc., not just powers-of-2 bisection).

**VERDICT: BUILD** -- Genuine theoretical advantage over bisection-based progressive transmission for 1D signals. Clean, small library. Real use case in sensor networks and progressive web data loading. The key selling point: interruption-tolerant data transmission where any prefix of the stream gives the best possible spatial coverage.

---

## J. Database Index Page Splits

**Idea**: Use Farey mediant instead of median key for B-tree page splits.

**Buildable?** Modifying a B-tree implementation is doable in 2 weeks.

**Who?** Database engine developers.

**Prior art**: B-tree splits at the median key, which gives optimal balance BY DEFINITION -- it minimizes the max size of the two resulting pages. B*-trees defer splits by redistributing to siblings. B+ trees, LSM trees, and other variants address different aspects of the split problem.

**Honest assessment**: The median key split is ALREADY OPTIMAL for what it optimizes (balanced page sizes). The Farey mediant is the simplest fraction between two fractions -- but B-tree keys are not fractions, they are arbitrary comparable values. Even if keys were rational, the mediant minimizes DENOMINATOR, not PAGE SIZE. These are different objectives. Splitting at the mediant would give WORSE balance than splitting at the median. This idea is based on a category error: confusing "simplest fraction in a gap" with "best split point for a data structure."

**VERDICT: SKIP** -- Median split is already optimal for page balance. Farey mediant optimizes the wrong objective. Category error.

---

## Summary Table

| App | Verdict | Timeframe | Key Reason |
|-----|---------|-----------|------------|
| A. Adaptive 1D grid | **BUILD** | 1 week | Principled replacement for bisection in adaptive sampling. LOD control. |
| B. Hash table | SKIP | -- | Jump consistent hashing dominates. |
| C. Video bitrate ladder | SKIP | -- | Must be content-dependent. Farey is content-blind. |
| D. Color quantization | SKIP | -- | Octree already hierarchical. Perceptual spaces matter more. |
| E. Rate limiter | SKIP | -- | Even spacing is trivial. Real problems are elsewhere. |
| F. Test case generation | INVESTIGATE | 1 week | Niche for denominator-systematic numerical testing. |
| G. Audio polyrhythm | SKIP | -- | = Euclidean rhythms (Toussaint 2005). Saturated market. |
| H. Font hinting | SKIP | -- | Wrong problem formulation. Extreme barrier. |
| I. Progressive transmission | **BUILD** | 2 weeks | Genuine optimality for interruption-tolerant 1D data. |
| J. B-tree page splits | SKIP | -- | Category error. Median already optimal for balance. |

## Recommended Build Order

### Week 1: Adaptive 1D Sampler (Application A)
- Python library: `farey_sampler`
- API: `sample(f, a, b, max_points=100, priority='gap_weighted')` returns hierarchical point set
- Priority modes: uniform (pure Farey), gradient-weighted, curvature-weighted
- Key feature: any prefix of the returned points is the best N-point approximation
- Output: points with their Farey level (denominator), enabling LOD filtering
- Demo: adaptive plotting that beats matplotlib's default sampler

### Week 2: Progressive 1D Transmission (Application I)
- Rust/Python library: `farey_stream`
- API: `FareyEncoder.encode(data_points)` produces Farey-ordered stream; `FareyDecoder.decode_partial(stream_prefix)` reconstructs best approximation from any prefix
- Key feature: graceful degradation under packet loss / bandwidth interruption
- Demo: streaming sensor data over lossy channel, compare reconstruction quality vs bisection order and random order
- Theoretical backing: Farey injection principle (Lean-proved) guarantees each new point goes into the largest gap

### Week 3 (if time): Numerical Test Generator (Application F)
- Prototype to validate the denominator-systematic testing claim
- Generate Farey-ordered test inputs for known numerical edge cases (catastrophic cancellation, precision loss at specific denominators)
- Compare bug-finding rate against random, Sobol, and boundary-value testing
- Only proceed to full library if prototype shows genuine advantage

## What We Are NOT Building

To be explicit about what we rejected and why:

- **Anything in the hashing/load-balancing space**: saturated, no gap
- **Anything requiring perceptual tuning** (color, audio, fonts): the math does not map to human perception
- **Anything where content-dependence dominates** (video encoding): Farey is content-blind
- **Anything where the problem is misframed** (B-tree splits): optimizing the wrong objective

## Novel Contributions We CAN Claim

For the BUILD items:
1. **Farey adaptive sampling**: Not "adaptive mesh refinement." Specifically: a deterministic, hierarchical, LOD-controlled sampling scheme for 1D functions based on the mediant property. The closest prior art is bisection-based adaptive sampling, which lacks the LOD hierarchy and the smallest-denominator optimality.

2. **Farey progressive transmission**: Not "progressive encoding." Specifically: an ordering of spatial samples that minimizes the maximum gap at every prefix length, with a Lean-verified proof of the injection principle. The closest prior art is van der Corput sequences (restricted to base-2). Farey gives finer granularity by using all denominators.

Both of these are genuine, if modest, contributions with clear practical value and defensible novelty.
