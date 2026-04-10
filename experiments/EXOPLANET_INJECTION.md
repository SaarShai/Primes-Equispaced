# Exoplanet Resonance Chains and the Farey Injection Principle

**Date:** 2026-03-27
**Status:** Exploratory research note
**Honesty level:** Explicitly marked [RIGOROUS], [PLAUSIBLE], or [SPECULATIVE] throughout

---

## 1. Background: What Are Resonance Chains?

### The Phenomenon

When planets form in a protoplanetary disk, they interact gravitationally with
the gas and migrate inward. If outer planets migrate faster than inner ones,
they can become locked into mean-motion resonances (MMRs) -- orbital period
ratios close to small integer ratios like 3:2, 4:3, 2:1. When multiple
sequential planet pairs are each in MMR, the result is a **resonance chain**.

[RIGOROUS] This is standard planetary dynamics. The theoretical framework
(type I migration, convergent migration, resonance capture) has been
established since the 2000s.

### Known Resonance Chain Systems

| System      | Planets | Adjacent Period Ratios              | Discovery | Notes                          |
|-------------|---------|-------------------------------------|-----------|--------------------------------|
| TRAPPIST-1  | 7       | 8:5, 5:3, 3:2, 3:2, 4:3, 3:2      | 2017      | All 7 in chain; Laplace angles |
| HD 110067   | 6       | 3:2, 3:2, 3:2, 4:3, 4:3           | 2023      | Pristine; unchanged since birth|
| TOI-178     | 6       | 5:3, 2:1, 3:2, 3:2, 4:3           | 2021      | 5 of 6 in Laplace chain       |
| Kepler-223  | 4       | 4:3, 3:2, 4:3                      | 2016      | Period ratio 3:4:6:8           |
| Kepler-80   | 5       | ~3:2, ~3:2, ~4:3, ~3:2            | 2014      | Orbit ratio ~9:6:4:3:2         |
| GJ 876      | 3       | 2:1, 2:1                           | 2010      | Laplace resonance (4:2:1)      |

### How Chains Form

1. **Convergent migration:** Planets embedded in a gas disk migrate inward at
   rates depending on their mass and local disk conditions. When an outer planet
   catches up to an inner one, capture into MMR can occur.
2. **Sequential capture:** Each newly arriving planet locks into resonance with
   the chain's outermost member, extending the chain.
3. **Disk inner edge:** The innermost planet stalls near the disk's magnetic
   truncation radius. Others pile up behind it.

Wong & Lee (2024, AJ) derived analytic criteria for convergent migration,
showing it depends on disk surface density and temperature gradients (alpha, beta).

### How Chains Break

The puzzle: migration simulations consistently produce resonant chains, but
only ~1-5% of observed Kepler systems are resonant.

**"Breaking the Chains" model** (Izidoro, Raymond, Morbidelli et al. 2017):
- After disk dispersal, resonant chains lose damping forces
- ~90-95% go dynamically unstable on ~100 Myr timescales
- Giant impacts scramble the chain into non-resonant orbits
- The ~5% that survive are the TRAPPIST-1-like systems we observe

[RIGOROUS] The breaking-the-chains model is the current leading explanation,
supported by N-body simulations matching the observed period ratio distribution.

### The TRAPPIST-1 Two-Step Formation (Pichierri et al. 2024)

A 2024 Nature Astronomy paper showed TRAPPIST-1's inner planets (b,c,d,e)
initially formed a 3:2 chain, then got "stretched" to higher-order resonances
(8:5, 5:3) as the disk inner edge receded. The outer planets (f,g,h) joined
later, establishing their own first-order resonances. This explains why the
inner pairs show higher-order (more complex) resonances than the outer pairs.

---

## 2. The Existing Farey-Resonance Connection

### Already Known (Not Our Contribution)

[RIGOROUS] The connection between Farey sequences and resonance diagrams is
already established in physics, though not in the exoplanet context specifically:

1. **Tomas (2014), Phys. Rev. ST Accel. Beams 17, 014001:** Proved that
   resonance lines in accelerator tune diagrams are fully described by Farey
   sequences. The resonance lines cut the horizontal axis at Farey fractions.
   The largest resonance-free gaps occur next to low-order resonances -- a
   property of Farey sequences.

2. **Arnold tongues / mode-locking:** In nonlinear dynamics, when two
   frequencies compete, the system locks into resonances ordered by the
   Stern-Brocot tree (which contains the Farey tree). The strongest resonances
   are the simplest fractions (1:1, 2:1, 3:2), with capture probability
   decreasing for higher-order fractions deeper in the tree.

3. **Celestial mechanics:** Malhotra's work on Neptune-Pluto resonance and
   the structure of the Kuiper belt uses resonance overlap and capture theory
   where rational period ratios play the central role.

**What is NOT established:** No one has explicitly applied the Farey injection
principle (at most one new fraction per gap per level) to constrain how
resonance chains assemble.

---

## 3. The Injection Principle Connection

### Our Result (Formally Verified)

The injection principle (proven in Lean 4, file `InjectionPrinciple.lean`):

> For any prime p >= 3, each gap between adjacent fractions in the Farey
> sequence F_{p-1} contains at most one fraction k/p.

More generally (`GeneralInjection.lean`): for any N, each gap in F_{N-1}
receives at most one new fraction from F_N.

### The Proposed Analogy

[SPECULATIVE] Here is the analogy we could explore:

**Farey sequence levels <-> stages of planetary migration**

| Farey Concept               | Exoplanet Analog                                 |
|-----------------------------|--------------------------------------------------|
| Farey level F_N             | System with N bodies in resonance                |
| Gap between adjacent a/b, c/d | Frequency range between two existing resonances|
| New fraction at level N+1   | New planet migrating into the chain              |
| Mediant (a+c)/(b+d)        | Predicted resonance ratio of the new planet      |
| Injection principle (<=1 per gap) | At most one planet can stably join per gap  |

### What the Principle Would Predict

**Prediction 1 (Ordering):** [PLAUSIBLE] When a new planet migrates into an
existing resonance chain, its period ratio relative to neighbors should
approximate a Farey mediant of the existing resonances.

Test: In TRAPPIST-1, if the 8:5 resonance between b-c "splits" the gap
between 3:2 and 2:1, is 8:5 the mediant? mediant(3/2, 2/1) = 5/3 (not 8/5).
But 5:3 IS the c-d resonance! And mediant(5/3, 2/1) = 7/4, while
mediant(3/2, 5/3) = 8/5 -- which IS the b-c resonance.

This is tantalizing: the TRAPPIST-1 inner resonances 3:2, 5:3, 8:5 form a
sequence of Farey mediants. But this needs careful verification and could be
coincidence given the small number of simple fractions available.

**Prediction 2 (Capacity):** [SPECULATIVE] The injection principle says each
gap receives at most one new fraction per level. In the exoplanet context, this
would mean: at each stage of migration, at most one new planet can stably
insert into each gap between existing resonances.

This is qualitatively consistent with the sequential capture picture (planets
arrive one at a time and lock in). But it goes further by predicting WHERE
(at the mediant) and HOW MANY (at most one per gap per stage).

**Prediction 3 (Missing planets):** [SPECULATIVE] If a system's observed
resonances skip a Farey level, there might be an undetected planet at the
mediant ratio. For example, if a system has planets in 3:2 and 2:1 resonance
but nothing in between, the injection principle predicts a potential planet at
5:3 (the mediant).

### Honest Assessment of the Analogy

**Strengths:**
- The Farey ordering of resonances is already established physics (Arnold
  tongues, Tomas 2014)
- Sequential planet capture does build chains one planet at a time
- The mediant property is at least suggestive in TRAPPIST-1
- Our injection principle adds a rigorous bound (at most 1 per gap) that goes
  beyond existing work

**Weaknesses:**
- [CRITICAL] Farey sequences organize ALL rationals, but planetary resonances
  only occur at specific ratios where resonance is strong enough for capture.
  Not all Farey fractions correspond to viable resonances.
- [CRITICAL] The injection principle is about fractions with prime denominator.
  There is no physical reason why planetary system "levels" would correspond
  to prime numbers specifically.
- [CRITICAL] Resonance capture depends on migration rate, planet mass, disk
  properties, and eccentricity -- not just the number-theoretic structure of
  the period ratio. Two planets with period ratio 7:5 might never lock into
  resonance because the resonance is too weak, even though 7/5 is a perfectly
  good Farey fraction.
- [IMPORTANT] The "at most one per gap" bound might be trivially true for
  physical reasons (planets can't be arbitrarily close) rather than providing
  new information.
- [IMPORTANT] Sample size is tiny. Only ~6 well-characterized resonant chains
  exist. Statistical claims would be extremely weak.

---

## 4. What Would We Need to Test This

### 4.1 Data Sources

**NASA Exoplanet Archive** (https://exoplanetarchive.ipac.caltech.edu/)
- Free, public access via web interface and API (TAP service)
- Key table: `PSCompPars` (Planetary Systems Composite Parameters)
- Relevant columns: `hostname`, `pl_orbper` (orbital period), `sy_pnum`
  (number of planets)
- As of March 2026: 6,150+ confirmed exoplanets
- API base: `https://exoplanetarchive.ipac.caltech.edu/cgi-bin/nstedAPI/nph-nstedAPI?`

**Specific query to get multi-planet system periods:**
```
SELECT hostname, pl_name, pl_orbper, pl_orbpererr1, pl_orbpererr2, sy_pnum
FROM pscomppars
WHERE sy_pnum >= 3
ORDER BY hostname, pl_orbper
```

**Other sources:**
- Exoplanet.eu catalog
- Individual system papers (TRAPPIST-1, HD 110067, etc.)

### 4.2 The Mapping Problem

[PLAUSIBLE] The mapping from period ratios to Farey fractions is
straightforward in principle:

1. For each multi-planet system, compute pairwise period ratios P_outer/P_inner
2. Find the closest rational p/q with small denominator (best rational
   approximation, which is exactly a continued fraction / Stern-Brocot
   tree operation)
3. Identify the Farey level at which each ratio appears
4. Check whether the ordering of planets by their entry into the chain
   follows the Farey level ordering

**The problem:** We don't observe the historical ORDER in which planets joined
the chain. We only see the final configuration. This makes it very hard to
test Prediction 2 directly.

**Workaround:** We could check whether the SET of observed period ratios forms
a valid Farey subsequence -- i.e., whether they are consistent with having been
built up one level at a time.

### 4.3 A Concrete Test

**Test: Do observed resonance chains respect Farey ordering?**

For each known resonant chain:
1. List all adjacent period ratios as reduced fractions
2. Compute the Farey level (= max denominator) of each ratio
3. Check: is it possible to order the ratios such that each one is a mediant
   of two already-present ratios?
4. Compare against random fractions with similar denominators (null hypothesis)

**TRAPPIST-1 test case:**
- Ratios: 8/5, 5/3, 3/2, 3/2, 4/3, 3/2
- Unique ratios: 3/2, 4/3, 5/3, 8/5
- Farey levels: 3/2 at F_2, 4/3 at F_3, 5/3 at F_3, 8/5 at F_5
- Can we build this up? Start with 1/1, 2/1 (trivial boundaries)
  - F_2: add 3/2 = mediant(1/1, 2/1). YES.
  - F_3: add 4/3 = mediant(1/1, 3/2). YES. Add 5/3 = mediant(3/2, 2/1). YES.
  - F_5: add 8/5 = mediant(3/2, 5/3). YES.
- Result: All TRAPPIST-1 resonances are Farey mediants! But this is a very
  small sample and simple fractions are constrained to be mediants anyway.

**HD 110067 test case:**
- Ratios: 3/2, 3/2, 3/2, 4/3, 4/3
- Unique ratios: 3/2, 4/3
- These are the simplest first-order resonances. Not much structure to test.

### 4.4 A More Ambitious Test

[SPECULATIVE] Rather than testing individual chains, test the POPULATION:

1. Get all multi-planet systems from the Archive (~900 systems with 2+ planets)
2. Compute all adjacent period ratios
3. Histogram these ratios on a Stern-Brocot tree
4. Check: do period ratios cluster at low Farey levels more than expected?
5. Is there a deficit of planets at non-Farey ratios?

This would be a population-level test of whether the Farey structure constrains
planetary architecture globally, not just in resonant chains.

---

## 5. Potential Collaborators

### Tier 1: Most Relevant

**Renu Malhotra** (University of Arizona)
- Regents Professor, NAS member, expert on orbital resonances
- Literally wrote the textbook chapter on orbital resonances in planetary systems
- 2024 work on compact planetary system architectures (Volk & Malhotra, AJ)
- Connection: Her work on resonance capture theory is the closest to the
  mathematical structure we're proposing. She would immediately see whether
  the Farey structure adds anything beyond what's already known from
  resonance capture theory.
- Risk: She may say "this is already implicit in Arnold tongue theory."

**Daniel Fabrycky** (University of Chicago)
- Full professor, 20,000+ citations, expert on multi-planet dynamics
- Led the Kepler-223 resonance chain analysis
- Co-authored TRAPPIST-1 resonance chain paper
- Connection: Has the most hands-on experience with real resonance chain data
  and the dynamics of chain formation.

**Sean Raymond** (Laboratoire d'Astrophysique de Bordeaux)
- CNRS researcher, 23,500+ citations
- Lead author of "Breaking the Chains" framework
- Connection: His work on how resonant chains form AND break is exactly where
  the injection principle's "at most one per gap" constraint would matter most.
  If the injection principle constrains chain assembly, it might also constrain
  what kinds of instabilities can break them.

### Tier 2: Valuable

**Andre Izidoro** (Rice University) -- co-architect of "Breaking the Chains"
**Gabriele Pichierri** (MPIA Heidelberg) -- TRAPPIST-1 two-step formation
**Rafael Luque** (University of Chicago) -- HD 110067 discovery team

### Approach Strategy

[PLAUSIBLE] The most productive approach would be:
1. Write a short (2-3 page) note showing the TRAPPIST-1 mediant analysis
   concretely, with honest caveats
2. Include a computational test on all known resonant chains
3. Send to Fabrycky or Raymond with a clear question: "Does the Farey injection
   principle add predictive power beyond what resonance capture theory already
   provides?"
4. If the answer is "maybe," propose a joint study

---

## 6. Practical Applications

### 6.1 Predicting Undiscovered Planets

[SPECULATIVE] If a resonant chain has a "gap" where the Farey structure
predicts a mediant resonance, this could flag systems for targeted follow-up.

Example: If a system has confirmed planets at 3:2 and 2:1 resonance with no
planet in between, the mediant predicts a potential planet at 5:3 resonance.

**Honest caveat:** This is weak as a standalone prediction. Resonance capture
theory already predicts which resonances are most likely. The injection
principle would only add value if it provides tighter constraints than existing
dynamical analysis.

### 6.2 Constraining Formation Histories

[PLAUSIBLE] Different migration histories would produce different orderings of
resonance assembly. The injection principle constrains which orderings are
"Farey-compatible" (i.e., can be built up by sequential mediant insertion).

This could potentially rule out certain migration scenarios. For instance, if
a system's resonances can only be built in a specific Farey order, this implies
a specific sequence of planet arrivals.

### 6.3 Stability Boundaries

[SPECULATIVE] The injection principle's "at most one per gap" constraint might
relate to the stability boundary for resonant chains. If you try to insert
two planets into the same gap (violating the injection principle), the system
is over-packed and goes unstable.

This connects to Petit et al. (2020) on stability criteria for resonant chains,
and to the Hill stability criterion for planet spacing.

---

## 7. Honest Bottom Line

### What is real:
- Resonance chains ARE organized by rational period ratios
- Farey sequences DO provide the natural ordering of such ratios
- The Tomas (2014) paper proves the connection for accelerator resonance diagrams
- Our injection principle IS a rigorous result about Farey sequence structure

### What is suggestive but unproven:
- The TRAPPIST-1 resonances do form a Farey mediant sequence
- Sequential planet capture is qualitatively similar to Farey level construction
- The "at most one per gap" constraint is qualitatively consistent with
  observed chain assembly

### What is speculative:
- Whether the injection principle adds predictive power beyond existing
  resonance capture theory
- Whether "Farey level" maps to any physical quantity in planet formation
- Whether the prime-denominator version of the injection principle has
  physical meaning
- Whether the sample size of ~6 resonant chains can support any statistical claim

### The key question to answer:
**Does the Farey injection principle tell us anything that resonance capture
theory (Arnold tongues, adiabatic resonance sweeping, Hill stability) does not
already tell us?**

If yes, this is a genuinely new application connecting number theory to
planetary science. If no, it is a beautiful mathematical reformulation of
known physics -- which might still have pedagogical or computational value,
but would not constitute a new scientific prediction.

### Recommended next step:
Write a Python script that:
1. Downloads all multi-planet system data from the NASA Exoplanet Archive
2. Computes period ratios and maps them to Stern-Brocot tree locations
3. Tests whether resonant chains are Farey-ordered more often than chance
4. Visualizes the result on a Stern-Brocot tree diagram

This would take ~1 day of work and would answer whether there's enough
signal to justify reaching out to Fabrycky or Raymond.

---

## References

- Tomas, R. (2014). "From Farey sequences to resonance diagrams."
  Phys. Rev. ST Accel. Beams 17, 014001.
- Izidoro, A., Raymond, S.N., et al. (2017). "Breaking the chains: Hot
  super-Earth systems from migration and disruption of compact resonant
  chains." MNRAS 470, 1750.
- Pichierri, G. et al. (2024). "Forming the Trappist-1 system in two
  steps during the recession of the disc inner edge." Nature Astronomy.
- Luque, R. et al. (2023). "A resonant sextuplet of sub-Neptunes transiting
  the bright star HD 110067." Nature 623, 932.
- Mills, S.M., Fabrycky, D.C. et al. (2016). "A resonant chain of four
  transiting, sub-Neptune planets." Nature 533, 509.
- Wong, M. & Lee, M.H. (2024). "Resonant Chains and the Convergent Migration
  of Planets in Protoplanetary Disks." AJ 167, 112.
- Volk, K. & Malhotra, R. (2024). "Differences between Stable and Unstable
  Architectures of Compact Planetary Systems." AJ 167, 271.
- Leleu, A. et al. (2021). "Six transiting planets and a chain of Laplace
  resonances in TOI-178." A&A 649, A26.
- Luger, R. et al. (2017). "A seven-planet resonant chain in TRAPPIST-1."
  Nature Astronomy 1, 0129.
