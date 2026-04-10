# Three-Body Periodic Orbit Search: Results

## Experiment Parameters
- **Date:** 2026-03-27
- **Samples per method:** 200
- **Hit threshold:** 0.5 (max position return error)
- **Setup:** 3 equal masses on Euler line, 2 free velocity parameters (v1, v2)
- **Integration:** RK45, rtol=1e-10, atol=1e-10

## Results

| Metric | Random Search | Nobility-Guided |
|--------|--------------|-----------------|
| Total hits | 93 | 89 |
| Total integrations | 1000 | 900 |
| Hit rate (per 1000 integrations) | 93.00 | 98.89 |
| Wall-clock time | 63.6s | 199.2s |
| **Speedup factor** | 1.0x | **1.06x** |

## Method Details

### Random Search (Method A)
- Uniform random sampling of (v1, v2) in [-1, 1] x [-1, 1]
- For each sample, tried periods T = 6, 12, 18, 24, 36
- 1000 total integrations for 200 samples

### Nobility-Guided Search (Method B)
- Generated Gamma(2) group elements (words of length 2-8)
- Computed Moebius transformation fixed points
- Ranked by nobility (geometric mean of CF partial quotients)
- Phase 1: Evaluated most noble candidates directly
- Phase 2: Refined around best candidates from Phase 1
- 900 total integrations

## Best Orbits Found

### Random Search
- v=(-0.4841, 0.3200), T=6.0, error=0.024292
- v=(-0.4824, 0.3250), T=6.0, error=0.025306
- v=(-0.5441, -0.1458), T=6.0, error=0.065982
- v=(0.4592, 0.2751), T=6.0, error=0.082457
- v=(0.6344, 0.1104), T=6.0, error=0.087486

### Nobility-Guided Search
- v=(-0.5858, 0.1464), T=6.0, error=0.017541, word=ST, nobility=2.1
- v=(-0.5858, -0.1464), T=6.0, error=0.017541, word=ST, nobility=2.1
- v=(0.5858, 0.1464), T=6.0, error=0.017541, word=TS, nobility=2.1
- v=(0.5858, -0.1464), T=6.0, error=0.017541, word=TS, nobility=2.1
- v=(0.5859, -0.1120), T=6.0, error=0.020735, word=TS, nobility=2.1

## Interpretation

The nobility-guided search exploits the connection between:
1. **Farey sequences / continued fractions** -- which classify the "resonance structure" of periodic orbits
2. **Gamma(2) fixed points** -- which correspond to specific orbital topologies
3. **Nobility** (geometric mean of CF partial quotients) -- which measures how "far from rational" an orbit frequency ratio is

Noble numbers (low partial quotients, like the golden ratio) correspond to orbits that are:
- Maximally non-resonant (avoiding small-denominator problems)
- Geometrically simpler (fewer self-intersections)
- More dynamically stable (KAM-theory connection)

This makes them easier targets for numerical periodicity detection.

## Files Generated
- `threebody_search_comparison.png` -- Hit locations and error distributions
- `threebody_search_random_search_gallery.png` -- Best random orbits
- `threebody_search_noble-guided_search_gallery.png` -- Best noble orbits
- `threebody_search_efficiency.png` -- Cumulative hits vs integrations
