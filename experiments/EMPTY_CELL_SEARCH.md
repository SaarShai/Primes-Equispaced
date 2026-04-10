# Empty Cell Search: Periodic Table of Three-Body Orbits

## Table Structure

The periodic table organizes **691 equal-mass, zero-angular-momentum three-body periodic orbits** from the Li-Liao catalog into a 9x8 grid based on continued fraction (CF) properties.

### Rows (9): CF Period Length

The CF period length measures **algebraic complexity** -- how many partial quotients repeat in the continued fraction expansion of the orbit's Gamma(2) fixed point.

| Row | Period Length Range | Orbit Count | Fraction |
|-----|-------------------|-------------|----------|
| 1   | exactly 1         | 1 (0.1%)    | Figure-eight only |
| 2-5 | 2 to 5            | 2 (0.3%)    | Simplest non-trivial |
| 6-15 | 6 to 15          | 10 (1.4%)   | |
| 16-30 | 16 to 30        | 34 (4.9%)   | |
| 31-50 | 31 to 50        | 78 (11.3%)  | |
| 51-80 | 51 to 80        | 150 (21.7%) | Peak density |
| 81-120 | 81 to 120      | 198 (28.7%) | Most populated |
| 121-180 | 121 to 180    | 140 (20.3%) | |
| 181-300 | 181 to 300    | 78 (11.3%)  | |

**Why 9 rows?** The bins are chosen to capture the natural distribution of CF period lengths. Most orbits have moderate-to-long CF periods (51-180), reflecting the typical algebraic complexity of three-body choreography fixed points. The bins use logarithmic-ish spacing to give each row meaningful population.

### Columns (8): Geometric Mean of CF Partial Quotients

The geometric mean (gmean) of the CF partial quotients serves as a **nobility proxy** -- lower gmean (closer to 1.0) means the orbit's fixed point is closer to a noble number (all-1s CF like the golden ratio), implying greater dynamical stability.

| Column | Gmean Range | Orbit Count | Fraction |
|--------|------------|-------------|----------|
| 1.00-1.05 | [1.00, 1.05) | 118 (17.1%) | Most noble |
| 1.05-1.10 | [1.05, 1.10) | 87 (12.6%)  | |
| 1.10-1.15 | [1.10, 1.15) | 50 (7.2%)   | |
| 1.15-1.20 | [1.15, 1.20) | 99 (14.3%)  | |
| 1.20-1.25 | [1.20, 1.25) | 115 (16.6%) | |
| 1.25-1.30 | [1.25, 1.30) | 149 (21.6%) | Most populated |
| 1.30-1.35 | [1.30, 1.35) | 67 (9.7%)   | |
| 1.35-1.45 | [1.35, 1.45) | 6 (0.9%)    | Least noble |

**Why 8 columns?** The gmean for physically-realizable orbits concentrates in the range [1.0, 1.45]. Values above ~1.45 are essentially absent (only 6 orbits even reach 1.35-1.45), reflecting a physical constraint: orbits with large partial quotients (high gmean) are unstable and hard to sustain.

### Why 691 orbits in only 51 cells?

Of the 72 possible cells (9 x 8), only 51 are populated and 21 are empty. The orbits cluster because:

1. **Physical constraints** force CF properties into certain ranges. Most orbits land in the "heartland" of rows 31-180 and columns 1.00-1.30.
2. **The top-left corner** (short period, low gmean) is extremely sparse because few orbits have both simple algebraic structure AND near-noble numbers. The figure-eight (I.A-1) is the unique period-1, gmean-1.0 orbit.
3. **The bottom-right corner** (long period, high gmean) is sparse because high gmean implies instability, which is harder to achieve for long-period orbits.
4. **Row 1 and 2-5** are nearly empty because very short CF periods require very special algebraic relationships.

### Extending the catalog

The 695 orbits processed are specifically the **equal-mass (m1=m2=m3=1), zero-angular-momentum** subset. The full Li-Liao catalog contains 10,000+ orbits across all mass ratios. Processing the full catalog would likely populate several currently-empty cells, especially in the high-gmean columns where unequal masses can stabilize otherwise-forbidden orbit types.

---

## The 4 Physically Interesting Empty Cells

An empty cell is "physically interesting" if it is surrounded by populated cells -- its neighbors contain known orbits, suggesting the gap might be filled. We count both 4-connected (cardinal: up/down/left/right) and 8-connected (including diagonal) populated neighbors.

### Empty Cell #1: Row=6-15, Col=1.30-1.35 (MOST PROMISING)

**CF properties:** Period length 6-15, gmean 1.30-1.35
**Cardinal neighbors:** 4 (maximum possible for an interior cell)
**Total neighbors:** 7 out of 8

| Direction | Cell | Count | Representative | Nobility |
|-----------|------|-------|---------------|----------|
| Above | 2-5 \| 1.30-1.35 | 1 | I.A-2 (word: BAbabaBA) | 0.600 |
| Below | 16-30 \| 1.30-1.35 | 1 | I.B-17 | 0.621 |
| Left | 6-15 \| 1.25-1.30 | 1 | I.B-2 (word: BAbabABABabaBA) | 0.667 |
| Right | 6-15 \| 1.35-1.45 | 2 | I.B-3 | 0.679 |
| Above-right | 2-5 \| 1.35-1.45 | 1 | I.A-3 | 0.667 |
| Below-left | 16-30 \| 1.25-1.30 | 4 | II.C-190 | 0.663 |
| Below-right | 16-30 \| 1.35-1.45 | 1 | II.C-192 | 0.692 |

**Expected orbit:** An orbit in this cell would have:
- Free-group word of length ~10-20
- CF period of ~10 partial quotients with gmean ~1.325
- Example CF period: [1, 2, 1, 2, 1, 2, 1, 2, 1, 2] (gmean = 2^(5/10) = 1.414, too high)
- Better: [1, 1, 2, 1, 1, 2, 1, 1, 2, 1] (gmean = 2^(3/10) = 1.231, slightly low)
- Best fit: [1, 2, 1, 2, 1, 1, 2, 1] (gmean = 2^(3/8) = 1.297, close but below)
- Or: [2, 1, 2, 2, 1, 2, 1] (gmean = 2^(4/7) = 1.486, too high)
- Likely a period ~8-12 with about 55-65% of partial quotients being 2

### Empty Cell #2: Row=6-15, Col=1.15-1.20

**CF properties:** Period length 6-15, gmean 1.15-1.20
**Cardinal neighbors:** 3
**Total neighbors:** 5

| Direction | Cell | Count | Representative | Nobility |
|-----------|------|-------|---------------|----------|
| Below | 16-30 \| 1.15-1.20 | 6 | II.C-1 | 0.771 |
| Left | 6-15 \| 1.10-1.15 | 3 | I.B-1 | 0.825 |
| Right | 6-15 \| 1.20-1.25 | 1 | I.A-5 | 0.692 |
| Below-left | 16-30 \| 1.10-1.15 | 4 | II.C-61 | 0.847 |
| Below-right | 16-30 \| 1.20-1.25 | 6 | II.C-3 | 0.712 |

**Expected orbit:** CF period ~10-12 with gmean ~1.175. Example: [1,1,1,2,1,2,1,1,1,1,1,2] (gmean = 2^(3/12) = 1.189). Note: no neighbors ABOVE, suggesting short-period orbits with this gmean may be algebraically difficult.

### Empty Cell #3: Row=51-80, Col=1.35-1.45

**CF properties:** Period length 51-80, gmean 1.35-1.45
**Cardinal neighbors:** 2
**Total neighbors:** 4

Neighbors include cells (31-50, 1.35-1.45) with 2 orbits and (51-80, 1.30-1.35) with 9 orbits. This cell sits at the edge of the populated region -- high gmean (low nobility) with moderate complexity. The emptiness may reflect a physical instability threshold.

### Empty Cell #4: Row=2-5, Col=1.25-1.30

**CF properties:** Period length 2-5, gmean 1.25-1.30
**Cardinal neighbors:** 2
**Total neighbors:** 3

Only two orbits exist with CF period 2-5 at all (I.A-2 and I.A-3), making this row inherently sparse. A third orbit with gmean 1.25-1.30 would need a very specific CF structure, e.g., [2, 1, 1, 2] (gmean = 2^(2/4) = 1.414, too high) or [1, 1, 2] (gmean = 2^(1/3) = 1.260, in range!). So CF period [1, 1, 2] with gmean = 1.26 would fall here.

---

## Orbit Search Results

### Target: Cell (6-15, 1.30-1.35)

**Method:** Numerical shooting with scipy integration
- Equal masses m1=m2=m3=1, G=1
- Li-Liao IC convention: r1=(-1,0), r2=(1,0), r3=(0,0), v1=v2=(vx,vy), v3=-2(vx,vy)
- Integration: DOP853, rtol=1e-10, atol=1e-10
- Close-encounter and escape detection (abort if bodies approach within 0.001 or exceed distance 10)
- Return error = Euclidean distance between final state and initial state

**Search strategies tried:**
1. Direct evaluation of all 7 neighbor orbits at their known ICs
2. Period harmonics: each neighbor orbit at T multiples (0.5, 0.75, 1.0, 1.25, 1.5, 2.0, 2.5, 3.0)
3. Random perturbations: 40 samples at 5 scales (0.005 to 0.1) around each of 4 focus orbits, at multiple T values
4. Pairwise interpolation: alpha = 0.25, 0.5, 0.75 between all pairs of 4 focus orbits, plus perturbations
5. Nelder-Mead and Powell refinement of the best candidate

**Total evaluations:** 4,199

**Result:** The search converged to the **known orbit I.A-2** (vx=0.306893, vy=0.125507, T=6.2347) with return error 8.95e-9. This orbit lives in cell (2-5, 1.30-1.35), adjacent to but NOT in the target cell. No genuinely new orbit was discovered.

### Verification of Known Orbits

The integrator was verified against known orbits:
- I.A-2: return error = 5.7e-8 (period T=6.23)
- I.B-2: return error = 3.9e-7 (period T=13.87)
- I.B-17: return error > 1e10 (period T=41.79 -- too long for reliable integration at this tolerance)

### Interpretation

The failure to find a new orbit in cell (6-15, 1.30-1.35) has several possible explanations:

1. **Genuine physical gap:** The combination of moderate CF period (6-15) and high gmean (1.30-1.35) may simply not be achievable for equal-mass, zero-angular-momentum orbits. The free-group word structure needed may not be compatible with the dynamical constraints.

2. **Basin of attraction problem:** Even with 4,199 evaluations, the initial condition space (vx, vy, T) is 3-dimensional and the basins of attraction for periodic orbits are narrow. A more exhaustive search (e.g., 100,000 evaluations with GPU-accelerated integration) might find something.

3. **Requires different mass ratios:** The full Li-Liao catalog includes orbits for m3 != 1. Some CF structures may only be realizable at specific mass ratios.

4. **Higher-order harmonics:** The orbit might exist at T values far from what we searched (we covered T in [5, 60]). Very specific T values corresponding to unusual word structures might be needed.

### Recommendations for Further Search

1. **GPU-accelerated integration** (e.g., via diffrax/JAX) could evaluate 100x more candidates in the same time.
2. **Continuation methods:** Start from a known orbit (e.g., I.B-2 in the neighboring cell) and continuously deform a parameter, tracking the orbit family. If the family extends into the target cell, it would reveal the orbit.
3. **Symbolic search:** Instead of random ICs, enumerate free-group words with the right CF properties and search for ICs realizing each word.
4. **Unequal masses:** Extend the CF analysis to the full 10,000+ orbit catalog. Many cells empty at equal mass may be populated at other mass ratios.

---

## Files

- `threebody_periodic_table.json` -- Full periodic table data (691 orbits, 72 cells)
- `threebody_periodic_table.png` -- Visualization
- `threebody_new_orbit.json` -- Orbit search results (converged to known orbit)
- `threebody_exact_data.json` -- Source data with CF analysis of all 695 orbits
- `build_periodic_table.py` -- Script that builds the periodic table
- `orbit_search_v3.py` -- Orbit search script (v3, with close-encounter detection)
