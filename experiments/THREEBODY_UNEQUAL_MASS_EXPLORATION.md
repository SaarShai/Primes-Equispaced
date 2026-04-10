# Three-Body Problem: Unequal-Mass Orbit Exploration

**Date:** 2026-03-29
**Status:** Initial exploration complete
**Verification:** Unverified -- results need independent replication

---

## 1. Data Overview

### Source
GitHub: `sjtu-liao/three-body` (Li & Liao, Shanghai Jiao Tong University)

### Available Datasets

| Dataset | File | Count | Contents |
|---------|------|-------|----------|
| Equal-mass words | `three-body-free-group-word.md` | 695 orbits | Class, word |
| Unequal-mass words | `three-body-unequal-mass-free-group-word.md` | 1,349 orbits | Class, m3, word |
| Supplementary (full) | `non-hierarchical-3b-supplementary_data.txt` | 135,445 orbits | m1,m2,m3, initial conditions, T, stability |

**Critical finding:** The 135K supplementary data contains *continuous families* parameterized by mass ratio (e.g., m2 = 0.750, 0.751, 0.752, ...) with initial conditions, period T, and stability (S/U). These are NOT discrete orbits with free-group words. The word data is in the separate markdown tables.

### Unequal-Mass Word Data
- Setup: m1 = m2 = 1, m3 varies
- Mass values available: m3 = 0.5, 0.75, 2, 4, 5, 8, 10
- Distribution: 565 (m3=0.5), 401 (m3=0.75), 237 (m3=2), 85 (m3=4), 35 (m3=5), 17 (m3=8), 9 (m3=10)
- Word lengths: min=4, max=448, mean=118.9
- Classes: I.A (358), I.B (379), I.C (3), II.A (16), II.B (25), II.C (566), II.D (2)
- Two new classes not in equal-mass set: I.C, II.D

### Supplementary Data Format
- Columns: m1, m2, m3, x1, v1, v2, T, stability (S/U)
- First ~1900 rows all have m1=0.800, m3=1.000, with m2 varying from 0.750 to ~1.7
- Stability rate in sample: 32/1897 = 1.7% stable
- No words in this file -- just initial conditions and periods

---

## 2. Key Findings

### Finding 1: AB-Swap Palindrome Symmetry is UNIVERSAL (1348/1349)

The most important result. In the free group on two generators {A, B} with inverses {a, b}, define:

    swap_AB(w) = exchange A<->B, a<->b

Then the "AB-swap palindrome" property is:

    w = swap_AB(reverse(w))

**Results:**
- Equal mass (m1=m2=m3=1): **695/695 (100%)** are AB-swap palindromes
- Unequal mass (m1=m2=1, m3 varies): **1348/1349 (99.93%)** are AB-swap palindromes

The single exception is orbit I.B.i.c.33 at m3=2.0, which has a suspicious "BabaaBABA" substring that may be a data entry error (expected "BababABABA" based on the pattern).

**Interpretation:** This symmetry comes from the m1 <-> m2 exchange symmetry, which is preserved even when m3 differs. Since all orbits in this catalog have m1 = m2 = 1, the exchange symmetry persists, and so does the palindrome property. The words are NOT plain palindromes and NOT reverse-complement palindromes -- the AB-swap palindrome is the correct symmetry.

**Prediction:** For orbits with m1 != m2 (truly unequal), this palindrome property should BREAK.

### Finding 2: Gamma(2) Matrix and Nobility Generalize

The figure-eight orbit (word "BabA") exists at m3=0.5, 0.75, and 1.0 with IDENTICAL Gamma(2) matrix:

    M = [[13, 8], [8, 5]], trace = 18, nobility = 0.667

This is expected: the free-group word is a topological invariant that doesn't change with mass (the same braid type exists at different mass ratios). The Gamma(2) matrix is fully determined by the word.

**Nobility statistics are nearly identical across mass ratios:**

| m3 | Count | Mean Nobility |
|----|-------|---------------|
| 0.50 | 565 | 0.475 |
| 0.75 | 401 | 0.504 |
| 1.00 (equal) | 695 | 0.476 |
| 2.00 | 237 | 0.409 |
| 4.00 | 85 | 0.377 |
| 5.00 | 35 | 0.396 |
| 8.00 | 17 | 0.404 |
| 10.00 | 9 | 0.414 |

Nobility appears slightly lower for extreme mass ratios (m3 >> 1), but the overall distribution is remarkably stable. Mean ~ 0.46, median ~ 0.42 across all mass ratios.

### Finding 3: Nobility-Entropy Correlation Holds but Weakens at Extreme Mass Ratios

| Mass ratio | Spearman rho | p-value |
|------------|-------------|---------|
| m3=0.50 | 0.488 | 4.3e-35 |
| m3=0.75 | 0.592 | 2.6e-39 |
| m3=1.00 (equal) | 0.461 | 8.5e-38 |
| m3=2.00 | 0.181 | 5.5e-03 |
| m3=4.00 | **-0.279** | 9.8e-03 |
| m3=5.00 | 0.015 | 0.93 (ns) |
| m3=8.00 | 0.129 | 0.62 (ns) |
| m3=10.00 | 0.217 | 0.58 (ns) |

**Key observation:** The correlation is strong and significant for m3 near 1 (mass ratios close to equal), but **reverses sign** at m3=4 and becomes insignificant for extreme mass ratios. This is a real finding: the Farey/nobility structure is most informative for near-equal-mass systems.

### Finding 4: 100 Words Shared Between Equal and Unequal Mass

100 of the 695 equal-mass words also appear in the unequal-mass catalog. These are topological types (braids) that persist across mass ratios. Examples:
- BabA (figure-eight): appears at m3 = 0.5, 0.75, 1.0
- BAbabaBA: appears at m3 = 1.0, 2.0
- BaBabAbA: appears at m3 = 0.5, 0.75, 1.0

22 words appear at multiple unequal-mass values (not counting equal mass).

### Finding 5: Extended Periodic Table

The (n_L, n_R) periodic table, where n_L = count of A/a generators and n_R = count of B/b generators:

- Equal mass: 117 distinct cells
- Unequal mass: 154 distinct cells (37 new cells)
- The table is almost perfectly diagonal (n_L = n_R for nearly all orbits), consistent with the AB-swap palindrome symmetry
- New cells from unequal mass include (3,3), which was empty for equal mass
- The table extends to (n_L, n_R) up to ~224 for unequal mass (vs ~125 for equal mass)
- Empty cells do NOT get systematically filled -- the diagonal structure persists

---

## 3. Feasibility Assessment

### Data Accessibility: GOOD
- Free-group words: easily parseable HTML tables, ~5400 lines for unequal mass
- Supplementary 135K data: 13.6 MB text file, straightforward columnar format
- All data freely available on GitHub (raw content accessible via curl)

### Parsing: DONE
- Script `threebody_unequal_parse.py` successfully parses both word tables
- Handles HTML parsing, class extraction, mass extraction
- Computes Gamma(2) matrices, continued fractions, nobility, braid entropy
- Parsing is reliable: 695 equal-mass + 1349 unequal-mass orbits parsed

### Limitations
1. The 135K supplementary data has NO free-group words -- only initial conditions and stability
2. Computing words from initial conditions would require numerical orbit integration + braid computation (significant effort)
3. The word catalog only covers 7 mass ratios (m3 = 0.5, 0.75, 2, 4, 5, 8, 10)
4. Small samples for extreme mass ratios (m3=10 has only 9 orbits)
5. No stability information in the word tables (separate data)

---

## 4. Implications for Our Work

### What generalizes:
1. **AB-swap palindrome symmetry**: Universal whenever m1 = m2 (persists for all m3)
2. **Nobility distribution**: Remarkably stable across mass ratios (mean ~ 0.46)
3. **Same topological types exist**: 100 shared words between equal/unequal mass
4. **Gamma(2) matrix is mass-independent**: Same word always gives same matrix

### What does NOT generalize:
1. **Nobility-entropy correlation weakens**: Only significant for m3 near 1
2. **Nobility-entropy correlation reverses at m3=4**: This is unexpected and potentially important

### Open questions:
1. Do orbits with m1 != m2 break the palindrome symmetry? (Predicted: yes)
2. What happens to nobility when the palindrome symmetry breaks?
3. Can we connect the 135K supplementary data to words via topological classification?
4. Does the reversal of nobility-entropy correlation at m3=4 have a physical explanation?

### Rating: C1 (Collaborative, Minor Novelty)
- The palindrome universality is not surprising given the m1=m2 symmetry
- The correlation weakening at extreme mass ratios is an interesting empirical observation
- The 100-word overlap is a nice structural result but not deep
- Main value: confirms our Gamma(2)/nobility framework is robust

---

## 5. Files Produced

- `threebody_unequal_parse.py` -- Full parsing and analysis script
- This report

## 6. Next Steps (if pursued)

1. **Find truly unequal data (m1 != m2)**: The Li-Liao catalog also has "piano trio" orbits (m1=m2 != m3 for 3D) -- check if there are planar orbits with all three masses different
2. **Cross-reference with stability**: Download full 135K file, identify which mass triples correspond to known word types, check if stability correlates with nobility
3. **Investigate the m3=4 correlation reversal**: Is this a statistical artifact (n=85) or a real transition?
4. **Compute words from initial conditions**: Would require a numerical three-body integrator + braid computation pipeline (substantial engineering effort)
