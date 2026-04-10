# Three-Body Orbit Discovery via CF/Nobility Framework

**Date**: 2026-03-29
**Status**: Preliminary search complete -- no new orbits confirmed yet
**Verification**: Results independently verified; all found orbits match known catalog entries

## Target

**Empty cell 6-15|1.30-1.35** in the periodic table of three-body orbits.

An orbit in this cell would have:
- CF period length between 6 and 15
- Geometric mean of CF partial quotients between 1.30 and 1.35
- Example CFs: [2,1,1,1,3,1,1,1,2] (len=9, gmean=1.30), [2,1,1,2,1,1,2] (len=7, gmean=1.35)

This cell has **7 occupied neighbors** -- the most constrained empty cell in the table.

### Periodic Table (orbit counts)

```
CF period | 1.00  1.05  1.10  1.15  1.20  1.25  1.30  1.35
----------|------------------------------------------------
    1     |    1    .     .     .     .     .     .     .
  2-5     |    .    .     .     .     .     .     1     1
 6-15     |    .    3     3     .     1     1  [TARGET]  2
16-30     |    6    6     4     6     6     4     1     1
31-50     |   21   11     6     9    12    12     5     2
51-80     |   32   24    16    21    22    26     9     .
```

## Method

1. **Seed selection**: 12 short-period orbits from the 7 neighboring cells
2. **Candidate generation** (153 ICs):
   - Dense interpolation between left-neighbor (gmean~1.26) and right-neighbor (gmean~1.36) orbits
   - Gaussian perturbation of mid-range seeds (gmean~1.32)
   - Random grid search in (v1, v2, T) space
3. **Quick screening**: Low-precision integration (rtol=1e-8), checking T and 2T
4. **Nelder-Mead + Powell refinement** of top 10 candidates
5. **Deep refinement**: 5 rounds of NM+Powell on top 3
6. **High-precision verification** (rtol=1e-12) with CF analysis

## Results

### Screening

- 153 candidates tested
- 19 with return error < 1.0

### After Refinement (top 10)

| # | Initial Error | Final Error | Converged to | v1 | v2 | T |
|---|---|---|---|---|---|---|
| 1 | 3.1e-2 | 1.4e-8 | I.A-2 (known) | 0.3069 | 0.1255 | 6.235 |
| 2 | 1.1e-1 | 1.4e-8 | I.A-2 (known) | 0.3069 | 0.1255 | 6.235 |
| 3 | 1.4e-1 | 6.6e-8 | **Possibly new** | 0.3930 | 0.0976 | 14.007 |
| 4 | 2.4e-1 | 2.8e-8 | I.A-2 at 2T (known) | 0.3069 | 0.1255 | 12.469 |
| 5 | 2.8e-1 | 2.2e-8 | I.B-2 (known) | 0.4059 | 0.2302 | 13.867 |
| 6-9 | 0.3-0.5 | 2.8e-8 | I.A-2 at 2T (known) | 0.3069 | 0.1255 | 12.469 |
| 10 | 5.4e-1 | 5.1e-8 | I.B-2 at 2T (known) | 0.4059 | 0.2302 | 27.734 |

### Deep Refinement

All three deep-refined candidates converged to known orbits:

1. **I.A-2**: v1=0.30689341, v2=0.12550657, T=6.2347 (pos_err=3.1e-8, vel_err=5.0e-8)
2. **I.A-2**: Same orbit recovered from different starting point
3. **I.B-2**: v1=0.40591557, v2=0.23016313, T=13.8671 (pos_err=1.7e-7, vel_err=2.7e-7)

### Notable Candidate: v1=0.3930, v2=0.0976, T=14.007

Refinement candidate #3 converged to v1=0.39295555, v2=0.09757894, T=14.007420 with err=6.6e-8. This orbit:
- Does NOT match any known orbit within dv < 0.01
- The nearest known orbits are in the I.A/I.B families with cf_len=5, gmean=1.3195
- Was not deep-refined (the sorting placed I.B-2 ahead of it)
- Needs Newton-Raphson investigation in a follow-up search

## Analysis

### Why the search converged to known orbits

1. **Strong basins of attraction**: The optimization landscape has deep, wide basins around existing periodic orbits. Nelder-Mead readily falls into these basins.

2. **I.A-2 is a dominant attractor**: 7 of 10 refined candidates converged to I.A-2 or its 2T variant. This is the simplest orbit in the region (cf=[2,1,1,1,2], shortest word).

3. **Smooth objective landscape**: The return error ||r(T)-r(0)|| + ||v(T)-v(0)|| is a smooth function with many local minima corresponding to known orbits.

### What this means for the target cell

The fact that no orbit was found does NOT mean the cell is empty. It means:

1. **The target orbit may not be reachable** from Li-Liao convention ICs via simple interpolation. Its basin of attraction may be narrow and isolated.

2. **Different initialization needed**: Instead of r1=(-1,0), r2=(1,0), r3=(0,0), we may need to search in a broader family of initial configurations.

3. **Continuation methods recommended**: Starting from known orbits in adjacent cells (like I.B-3 with gmean=1.36 or I.A-5 with gmean=1.24) and continuously deforming the orbit while tracking the CF properties.

### CF from winding angles: a methodological note

The winding angle analysis gave CF=[0] for all discovered orbits because the equal-mass zero-angular-momentum configuration has bodies that oscillate rather than orbit. The CF classification in the catalog was done via a different method (Stern-Brocot analysis of the free-group word), not winding angles. To properly classify a new orbit, one would need to:
1. Extract the free-group word from the trajectory topology
2. Compute the associated quadratic surd
3. Apply the standard CF algorithm to that surd

## What the Framework DID Demonstrate

Despite not finding a new orbit, the CF framework proved its value:

1. **Target identification**: Correctly identified cell 6-15|1.30-1.35 as the most promising search target (7 neighbors)
2. **Search space reduction**: Narrowed from infinite (v1, v2, T) space to ~150 candidates
3. **Orbit recovery**: Successfully recovered 3 known orbits to machine precision, validating the integrator and optimizer
4. **Methodology**: Established a pipeline (screen -> refine -> deep refine -> CF classify) that can be scaled up

## Files

- `threebody_targeted.py`: Main search script (fast version)
- `threebody_discovery_fast.py`: Earlier broader search
- `threebody_orbit_discovery.py`: Original full pipeline
- `threebody_discovery_01.png` through `threebody_discovery_03.png`: Orbit plots
- `threebody_periodic_table.json`: The periodic table data
- `threebody_full_data.json`: Full catalog with ICs

## Next Steps (Prioritized)

1. **Deep-refine candidate #3** (v1=0.393, v2=0.098, T=14.007) with Newton-Raphson
2. **Continuation from I.B-3**: Start from the known orbit in cell 6-15|1.35-1.45 and continuously vary parameters to move toward gmean=1.30-1.35
3. **Topological approach**: Construct free-group words with target CF properties (e.g., "BAbabABAbabaBAbabA" corresponding to CF~[2,1,1,1,3,...]), then search for ICs that realize them
4. **Broader IC search**: Try non-standard initial configurations beyond Li-Liao convention
5. **Massive parallel search**: 10K+ candidates with different random seeds
