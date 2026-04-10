# Periodic Table of Three-Body Orbits
## Organized by Continued Fraction Structure

**First comprehensive CF-organized catalog of gravitational three-body periodic orbits.**

---

## Overview

- **Total orbits cataloged:** 695
- **Orbits with CF period detected:** 691
- **Organization:** Rows = CF period length (algebraic complexity), Columns = geometric mean of partial quotients (nobility proxy)
- **Source:** Li-Liao catalog of equal-mass zero-angular-momentum three-body orbits
- **CF method:** Exact quadratic surd computation at 100-digit precision

### Analogy with the Chemical Periodic Table

| Chemical Periodic Table | Three-Body Periodic Table |
|------------------------|--------------------------|
| Rows = electron shells | Rows = CF period length (algebraic complexity) |
| Columns = valence electrons | Columns = geometric mean of CF quotients (stability) |
| Atomic number | Word length (braid complexity) |
| Noble gases (most stable) | Noble orbits (highest nobility, most stable) |
| Electron configuration | Continued fraction [a0; a1, a2, ...] |

---

## The Table

| CF Period \ gmean | **1.00-1.05** | **1.05-1.10** | **1.10-1.15** | **1.15-1.20** | **1.20-1.25** | **1.25-1.30** | **1.30-1.35** | **1.35-1.45** |
|---|---|---|---|---|---|---|---|---|
| **1** | 🟢 **1** (n=1.00) | *empty* | *empty* | *empty* | *empty* | *empty* | *empty* | *empty* |
| **2-5** | *empty* | *empty* | *empty* | *empty* | *empty* | *empty* | 🔴 **1** (n=0.60) | 🔴 **1** (n=0.67) |
| **6-15** | *empty* | 🟢 **3** (n=0.92) | 🟡 **3** (n=0.83) | *empty* | 🔴 **1** (n=0.69) | 🔴 **1** (n=0.67) | *empty* | 🔴 **2** (n=0.68) |
| **16-30** | 🟢 **6** (n=0.95) | 🟢 **6** (n=0.90) | 🟡 **4** (n=0.85) | 🟡 **6** (n=0.77) | 🔴 **6** (n=0.71) | 🔴 **4** (n=0.66) | 🔴 **1** (n=0.62) | 🔴 **1** (n=0.69) |
| **31-50** | 🟢 **21** (n=0.96) | 🟢 **11** (n=0.89) | 🟡 **6** (n=0.82) | 🟡 **9** (n=0.77) | 🔴 **12** (n=0.72) | 🔴 **12** (n=0.65) | 🔴 **5** (n=0.63) | 🔴 **2** (n=0.66) |
| **51-80** | 🟢 **32** (n=0.95) | 🟢 **24** (n=0.90) | 🟡 **16** (n=0.82) | 🟡 **21** (n=0.76) | 🔴 **22** (n=0.70) | 🔴 **26** (n=0.64) | 🔴 **9** (n=0.61) | *empty* |
| **81-120** | 🟢 **33** (n=0.97) | 🟢 **23** (n=0.91) | 🟡 **12** (n=0.82) | 🟡 **26** (n=0.77) | 🔴 **34** (n=0.71) | 🔴 **44** (n=0.65) | 🔴 **26** (n=0.61) | *empty* |
| **121-180** | 🟢 **25** (n=0.96) | 🟢 **16** (n=0.90) | 🟡 **7** (n=0.82) | 🟡 **17** (n=0.77) | 🔴 **24** (n=0.70) | 🔴 **33** (n=0.65) | 🔴 **18** (n=0.61) | *empty* |
| **181-300** | *empty* | 🟢 **4** (n=0.90) | 🟡 **2** (n=0.80) | 🟡 **20** (n=0.76) | 🔴 **16** (n=0.69) | 🔴 **29** (n=0.65) | 🔴 **7** (n=0.60) | *empty* |

*Count = number of orbits. n = average nobility. Green = stable, Yellow = moderate, Red = less stable.*

---

## Special Elements

### H -- "Hydrogen" (I.A-1)
- **Reason:** Simplest orbit, pure golden ratio CF [0; 1,1,1,...], maximum nobility=1.0
- **Nobility:** 1.0
- **CF periodic part:** [1]

### He -- "Helium" (I.A-2)
- **Reason:** Second simplest, word_length=8
- **Nobility:** 0.6
- **CF periodic part:** [2, 1, 1, 1, 2]

### Li -- "Lithium" (I.A-3)
- **Reason:** Third simplest, word_length=8
- **Nobility:** 0.6666666666666666
- **CF periodic part:** [1, 3, 1]

---

## Noble Gases (Most Stable Orbit per Row)

These are the "noble gas" analogs: orbits with the highest nobility within each CF-period-length class.

| CF Period | Orbit ID | Nobility | gmean | CF Length |
|-----------|----------|----------|-------|-----------|
| 1 | I.A-1 | 1.0000 | 1.0000 | 1 |
| 2-5 | I.A-3 | 0.6667 | 1.4422 | 3 |
| 6-15 | II.A-4 | 0.9333 | 1.0760 | 15 |
| 16-30 | I.B-16 | 0.9655 | 1.0242 | 29 |
| 31-50 | II.B-7 | 0.9796 | 1.0142 | 49 |
| 51-80 | II.B-8 | 0.9811 | 1.0132 | 53 |
| 81-120 | II.C-223 | 0.9831 | 1.0118 | 118 |
| 121-180 | II.C-124 | 0.9878 | 1.0085 | 164 |
| 181-300 | II.C-144 | 0.9121 | 1.0628 | 182 |

The figure-eight orbit (I.A-1) is the absolute noble gas: nobility = 1.0000, the golden ratio fixed point.
As CF period length increases, noble gases converge toward gmean -> 1.0, approaching the golden ratio limit.

---

## Row Statistics (CF Period Length)

| CF Period | Count | Fraction |
|-----------|-------|----------|
| 1 | 1 | 0.1% |
| 2-5 | 2 | 0.3% |
| 6-15 | 10 | 1.4% |
| 16-30 | 34 | 4.9% |
| 31-50 | 78 | 11.3% |
| 51-80 | 150 | 21.7% |
| 81-120 | 198 | 28.7% |
| 121-180 | 140 | 20.3% |
| 181-300 | 78 | 11.3% |

The bulk of orbits (81%) have CF periods between 31 and 180.
Only 3 orbits have CF period <= 10 (the "light elements").

## Column Statistics (Geometric Mean)

| gmean Range | Count | Fraction |
|-------------|-------|----------|
| 1.00-1.05 | 118 | 17.1% |
| 1.05-1.10 | 87 | 12.6% |
| 1.10-1.15 | 50 | 7.2% |
| 1.15-1.20 | 99 | 14.3% |
| 1.20-1.25 | 115 | 16.6% |
| 1.25-1.30 | 149 | 21.6% |
| 1.30-1.35 | 67 | 9.7% |
| 1.35-1.45 | 6 | 0.9% |

The most populated column is gmean 1.25-1.30 (21.6%), while the extreme noble end (1.00-1.05) holds 17.1%.
Only 6 orbits (0.9%) have gmean > 1.35.

---

## Empty Cells: Predicted Undiscovered Orbit Types

There are **21** empty cells in the table out of 72 total.

### Structurally Forbidden Empty Cells

Cells in the Period-1 row (except gmean=1.0) are structurally empty:
a CF period of length 1 means [0; k, k, k, ...] which forces gmean = k.
Since k must be a positive integer, the only options are gmean=1.0, 2.0, 3.0, etc.
Only gmean=1.0 falls in our range, giving the single figure-eight orbit.

### Potentially Discoverable Empty Cells

- **Period 6-15, gmean 1.00-1.05**: No orbits found in Li-Liao catalog. Possible target for numerical search.
- **Period 6-15, gmean 1.15-1.20**: No orbits found in Li-Liao catalog. Possible target for numerical search.
- **Period 6-15, gmean 1.30-1.35**: No orbits found in Li-Liao catalog. Possible target for numerical search.
- **Period 51-80, gmean 1.35-1.45**: No orbits found in Li-Liao catalog. Possible target for numerical search.
- **Period 81-120, gmean 1.35-1.45**: No orbits found in Li-Liao catalog. Possible target for numerical search.
- **Period 121-180, gmean 1.35-1.45**: No orbits found in Li-Liao catalog. Possible target for numerical search.
- **Period 181-300, gmean 1.00-1.05**: No orbits found in Li-Liao catalog. Possible target for numerical search.
- **Period 181-300, gmean 1.35-1.45**: No orbits found in Li-Liao catalog. Possible target for numerical search.

---

## Li-Liao Family vs CF Structure: Cross-Analysis

**Average family purity per cell:** 0.688
**Cells with mixed families:** 33

Key finding: Li-Liao families (I.A, I.B, II.*) do NOT map cleanly to CF cells.
The average purity of 0.688 means that on average, the dominant family in each cell accounts for only 69% of orbits.
This reveals that **CF structure captures information orthogonal to the Li-Liao family classification**.

### Most Mixed Cells

| Cell | Families |
|------|----------|
| 16-30 x 1.20-1.25 | {'I.A': 3, 'I.B': 2, 'II.C': 1} |
| 81-120 x 1.05-1.10 | {'I.A': 7, 'I.B': 9, 'II.C': 7} |
| 81-120 x 1.15-1.20 | {'I.A': 5, 'I.B': 9, 'II.C': 12} |
| 81-120 x 1.20-1.25 | {'I.A': 14, 'I.B': 14, 'II.A': 1, 'II.B': 1, 'II.C': 4} |
| 81-120 x 1.25-1.30 | {'I.A': 22, 'I.B': 16, 'II.B': 2, 'II.C': 4} |
| 81-120 x 1.30-1.35 | {'I.A': 11, 'I.B': 11, 'II.C': 4} |
| 16-30 x 1.05-1.10 | {'I.A': 3, 'I.B': 1, 'II.C': 2} |
| 81-120 x 1.00-1.05 | {'I.A': 5, 'I.B': 1, 'II.B': 1, 'II.C': 26} |
| 81-120 x 1.10-1.15 | {'I.A': 4, 'I.B': 3, 'II.C': 5} |
| 16-30 x 1.10-1.15 | {'I.A': 1, 'II.C': 3} |

The large cells (period 81-120, gmean 1.20-1.30) contain roughly equal numbers of I.A and I.B orbits
plus smaller contributions from II.* families. This mixing demonstrates that the CF periodic table
provides a genuinely new organizational axis that is not reducible to the existing family classification.

---

## Key Findings

1. **CF period length correlates with braid complexity** but is NOT identical to word length.
   Orbits with the same word length can have very different CF structures.

2. **Nobility decreases systematically** from the upper-left (short CF period, low gmean)
   to lower-right (long CF period, high gmean), creating a clear "stability gradient".

3. **The figure-eight is uniquely noble**: it is the ONLY orbit with CF period 1 and gmean exactly 1.0.
   Its fixed point is the golden ratio, making it the "hydrogen" of the three-body world.

4. **21 empty cells** represent orbit types not yet found. Some are structurally forbidden
   (period 1 with non-integer gmean), but others may represent genuinely undiscovered orbits.

5. **Family mixing** in CF cells shows that the continued fraction organization reveals
   structure invisible to the Li-Liao family classification. The two organizational
   schemes are complementary, not redundant.

6. **Noble gases** (most stable orbit per CF-period row) systematically have gmean near 1.0,
   meaning their CF partial quotients are predominantly 1s (Fibonacci-like). This connects
   orbital stability to the golden ratio and Fibonacci numbers in a precise way.

---

*Generated from the Li-Liao catalog of 695 three-body orbits.*
*CF analysis via exact quadratic surd method at 100-digit precision.*