# Three-Body Periodic Orbits x Farey/Stern-Brocot: Concrete Progress Plan

**Date:** 2026-03-27
**Status:** Actionable research plan with verified data sources
**Builds on:** THREE_BODY_FAREY.md (general survey)

---

## THE OPPORTUNITY (Why This Is Novel)

After thorough literature search: **nobody has explicitly mapped three-body periodic orbit free-group words to rational numbers via the Stern-Brocot tree or Farey tessellation, then checked for structure.** This is despite the mathematical infrastructure being completely in place:

1. Three-body orbits are classified by words in F_2 (free group on 2 generators)
2. F_2 is isomorphic to Gamma(2), an index-6 subgroup of PSL(2,Z)
3. PSL(2,Z) generates the Farey tessellation
4. The quotient H/Gamma(2) is a thrice-punctured sphere = the shape sphere

The closest existing work is Kin-Nakamura-Ogawa (2021) on "Lissajous 3-braids" which connects Christoffel words and the Farey tessellation to choreographic 3-body motions, but only for the restricted Lissajous case, not the general catalog.

---

## THE MATHEMATICAL BRIDGE (Precise Statement)

### Chain of isomorphisms:

```
Three-body shape sphere (minus 3 collision pts)
    = thrice-punctured sphere S^2 \ {p1, p2, p3}

pi_1(S^2 \ {3 pts}) = F_2 = free group on generators {a, b}

F_2  ~=  Gamma(2) / {+/- I}  <  PSL(2,Z)  ~=  B_3 / Z(B_3)

PSL(2,Z) acts on H^2, generating the Farey tessellation
Gamma(2) quotient of H^2 = thrice-punctured sphere (same topology!)
```

### The key subgroup relationship:

- PSL(2,Z) = Z/2Z * Z/3Z (free product, NOT free group)
- Gamma(2) = index-6 normal subgroup of PSL(2,Z), IS isomorphic to F_2
- The cosets PSL(2,Z)/Gamma(2) ~= S_3 (symmetric group on 3 elements)
- This S_3 corresponds to the 6 permutations of the 3 bodies

### What this means concretely:

Every free-group word classifying a three-body orbit is an element of Gamma(2), which acts on the hyperbolic plane via Mobius transformations. Every such element has a pair of fixed points on the boundary circle (= real line union infinity), and these fixed points are quadratic surds whose continued fraction expansions encode a path through the Farey tessellation.

---

## DATA SOURCE: VERIFIED AND ACCESSIBLE

### GitHub repository: https://github.com/sjtu-liao/three-body

Contains free-group words for all published catalogs:

| File | Contents | Alphabet |
|------|----------|----------|
| `three-body-free-group-word.md` | 695+ equal-mass orbits | {a, b, A, B} where A=a^-1, B=b^-1 |
| `three-body-unequal-mass-free-group-word.md` | 1,223 unequal-mass orbits | Same |
| `free-fall-3b-free-group-word.md` | Free-fall orbit words | Same |

### Data format (from the MD files):

Columns: Class/number, Free group word

Example entries:
- I.A_1: `BabA` (length 4, the figure-eight orbit)
- I.A_2: `BAbabaBABababABABabaBABababABAbabaBA` (length 34)
- I.B_1: `BabaBAbabA` (length 10)

### Also available on SJTU website:
https://numericaltank.sjtu.edu.cn/three-body/three-body.htm

Additional parameters: periods T, scale-invariant periods T*, initial velocities (v1, v2), word lengths L_f.

---

## THE CONCRETE TEST (Week 1)

### Step 1: Parse the catalog (Day 1-2)

Write a Python script to:
1. Scrape/parse `three-body-free-group-word.md` from the GitHub repo
2. Extract: orbit class, free-group word, word length
3. Cross-reference with period data from the SJTU website or other MD files in the repo

### Step 2: Map words to matrices in Gamma(2) (Day 2-3)

The generators of Gamma(2) acting on H^2 are:

```
a  -->  [[1, 2], [0, 1]]    (translation by 2)
b  -->  [[1, 0], [2, 1]]    (another parabolic element)
```

Note: There is a choice of generators here. The standard ones for Gamma(2) are:
- T^2 = [[1,2],[0,1]]
- S T^2 S^{-1} = [[1,0],[2,1]]

where S = [[0,-1],[1,0]] and T = [[1,1],[0,1]] are the standard PSL(2,Z) generators.

For each word w = a^{e1} b^{e2} ... in the catalog:
- Compute the matrix M(w) in SL(2,Z)
- This matrix has trace |tr(M)| > 2 (hyperbolic) for non-trivial orbits

### Step 3: Extract the rational/quadratic-surd invariants (Day 3-4)

For each hyperbolic matrix M = [[a,b],[c,d]]:
- Fixed points: x = ((a-d) +/- sqrt((a+d)^2 - 4)) / (2c)
- These are quadratic surds with periodic continued fraction expansions
- The continued fraction period encodes a path through the Farey tessellation
- Extract the purely periodic part [a0; a1, ..., ak, ...]

### Step 4: Check for Farey/Stern-Brocot structure (Day 4-7)

Specific tests:
1. **Convergent ordering**: Do the continued fraction convergents of the fixed points follow Stern-Brocot tree ordering when orbits are sorted by word length?
2. **Trace vs. Stern-Brocot depth**: Does |tr(M(w))| correlate with the depth of related rationals in the Stern-Brocot tree?
3. **Period explanation**: Does the continued fraction structure explain the approximately-linear T* vs L_f relationship better than word length alone?
4. **Progenitor structure**: Do the 10 "progenitor sequences" of Li & Liao correspond to distinct branches of the Stern-Brocot tree?
5. **Dilatation ordering**: For each orbit, the pseudo-Anosov dilatation lambda = (tr + sqrt(tr^2 - 4))/2. Check if log(lambda) correlates with Stern-Brocot depth.

---

## THE DEEPER TEST (Week 2)

### Step 5: Cutting sequences along the Farey tessellation

Following Kin-Nakamura-Ogawa and Series:
1. For each orbit word w, compute the geodesic on H^2 connecting its two fixed points
2. Record the cutting sequence (which triangles of the Farey tessellation the geodesic crosses)
3. This gives a sequence in {L, R} (or the 4-symbol {b,d,p,q} of KNO)
4. The cutting sequence's run-length encoding IS the continued fraction of the fixed point

Check: Does the cutting sequence encode the orbit topology more efficiently than the raw free-group word?

### Step 6: The word-to-rational map

There are several natural maps from F_2 words to rationals:

**Map A (Abelianization):** Count net powers of a and b. The word a^p b^q maps to the rational p/q. This is crude but easy to compute.

**Map B (Matrix trace):** Map w to tr(M(w))/2. This is an integer for elements of SL(2,Z).

**Map C (Fixed point):** Map w to the larger fixed point of M(w). This is a quadratic surd, but its continued fraction convergents are rationals.

**Map D (Stern-Brocot path):** Treat the word as a sequence of L/R moves in the Stern-Brocot tree. This requires a non-trivial translation: the generators {a, b, A, B} of F_2 are not the same as {L, R} of the Stern-Brocot tree. However, since both are encoded by 2x2 integer matrices, there may be a natural dictionary.

Test all four maps and look for structure.

---

## WHAT WE ALREADY KNOW WILL WORK (From KNO 2021)

The Kin-Nakamura-Ogawa paper on Lissajous 3-braids already established:

1. Each Lissajous 3-braid W_{m,n} is a hyperbolic element of PSL(2,Z)
2. These braids are parametrized by (level N, Christoffel slope xi)
3. The slope xi lives in the Stern-Brocot tree
4. Dilatation increases as slope descends in the Stern-Brocot tree
5. Cutting sequences along the Farey tessellation encode these braids as 4-symbol frieze patterns
6. The continued fraction of the quadratic surd fixed point gives the period of the cutting sequence

The question is whether this structure extends from the restricted Lissajous case to the FULL catalog of Li & Liao orbits.

---

## POTENTIAL COLLABORATORS (Ranked by Relevance)

### Tier 1: Direct collaborators with complementary expertise

1. **Hiroaki Nakamura** (Osaka University) -- proved the Farey tessellation / Christoffel word connection for Lissajous 3-braids. Has the exact mathematical toolkit needed.
   - Contact: nakamura@math.sci.osaka-u.ac.jp (from paper affiliations)
   - Approach: "We want to extend your Lissajous 3-braid / Farey tessellation results to the full Li-Liao catalog of 695+ orbits"

2. **Xiaoming Li and Shijun Liao** (Shanghai Jiao Tong University) -- created the orbit catalogs, maintain the GitHub repo and SJTU database.
   - Contact: sjliao@sjtu.edu.cn (from publications)
   - Approach: "We have a number-theoretic framework that may explain the quasi-Kepler third law and progenitor sequence structure"

3. **Veljko Dmitrasinovic** (Belgrade) -- established the period-topology linear law, co-discovered the original 13 orbits.
   - Approach: "Your T* ~ L_f law may have a number-theoretic explanation via the Stern-Brocot tree structure of Gamma(2)"

### Tier 2: Mathematicians with relevant expertise

4. **Richard Montgomery** (UC Santa Cruz) -- invented the shape sphere classification framework
5. **Caroline Series** (Warwick, emerita) -- foundational work on cutting sequences and the Farey tessellation
6. **Eiko Kin** (Osaka) -- co-author on the Lissajous 3-braids paper

### Tier 3: For later stages

7. **Alessandro Trani** (Niels Bohr Institute) -- "islands of regularity" in three-body chaos
8. **Jacques Fejoz** (Paris-Dauphine) -- rigorous KAM / Chirikov for three-body

---

## SPECIFIC PREDICTIONS TO TEST

If the Farey/SB structure is real, we should find:

1. **Progenitor orbits sit at low depth in the Stern-Brocot tree.** The 6 progenitor orbits that generate the 10 algebraic sequences should map to simple rationals (small numerator/denominator) or to fixed points with short continued fraction periods.

2. **Satellite orbits (w^k) correspond to deeper tree positions.** Taking k-th powers of a word should move deeper in the SB tree, analogous to how repeating a continued fraction period multiplies the quadratic surd.

3. **The 10 algebraic sequences correspond to 10 branches of the SB tree.** Each sequence has a slightly different slope in the T* vs L_f plot; this should correspond to a different branch of the tree.

4. **The linear T* ~ L_f law becomes EXACT under the right SB-based normalization.** Instead of normalizing by word length alone, normalizing by some SB-depth-related quantity should reduce the scatter in the period data.

5. **Orbits related by the S_3 symmetry (body permutation) should be related by PSL(2,Z)/Gamma(2) coset action.** The 6 cosets correspond to the 6 permutations of 3 bodies.

---

## MINIMUM VIABLE RESULT

Even a negative result is publishable: "We mapped the Li-Liao catalog of 695 three-body periodic orbit words to matrices in Gamma(2) < PSL(2,Z), computed their fixed points and cutting sequences along the Farey tessellation, and found [structure / no additional structure beyond word length]."

A positive result -- showing that the SB tree organizes the catalog in a way that explains the quasi-Kepler law or the progenitor sequence structure -- would be a genuine contribution bridging number theory and celestial mechanics.

---

## IMPLEMENTATION SKETCH (Python)

```python
import numpy as np
from fractions import Fraction

# Generators of Gamma(2) in SL(2,Z)
# a = T^2 = translation by 2
# b = S T^2 S^{-1}
# A = a^{-1}, B = b^{-1}

gen = {
    'a': np.array([[1, 2], [0, 1]]),
    'b': np.array([[1, 0], [2, 1]]),
    'A': np.array([[1, -2], [0, 1]]),
    'B': np.array([[1, 0], [-2, 1]]),
}

def word_to_matrix(word):
    """Convert free-group word to SL(2,Z) matrix."""
    M = np.eye(2, dtype=int)
    for letter in word:
        M = M @ gen[letter]
    return M

def matrix_fixed_points(M):
    """Compute fixed points of Mobius transformation [a,b;c,d]."""
    a, b, c, d = M[0,0], M[0,1], M[1,0], M[1,1]
    if c == 0:
        return None  # parabolic or identity
    disc = (a + d)**2 - 4
    if disc <= 0:
        return None  # elliptic
    sqrt_disc = np.sqrt(disc)
    x_plus = ((a - d) + sqrt_disc) / (2 * c)
    x_minus = ((a - d) - sqrt_disc) / (2 * c)
    return x_plus, x_minus

def continued_fraction(x, max_terms=20):
    """Compute continued fraction expansion of x."""
    cf = []
    for _ in range(max_terms):
        a_n = int(np.floor(x))
        cf.append(a_n)
        frac = x - a_n
        if abs(frac) < 1e-10:
            break
        x = 1.0 / frac
    return cf

# Example: figure-eight orbit word "BabA"
w = "BabA"
M = word_to_matrix(w)
print(f"Word: {w}")
print(f"Matrix:\n{M}")
print(f"Trace: {np.trace(M)}")
fps = matrix_fixed_points(M)
if fps:
    print(f"Fixed points: {fps[0]:.6f}, {fps[1]:.6f}")
    print(f"CF of x+: {continued_fraction(fps[0])}")
    print(f"CF of x-: {continued_fraction(abs(fps[1]))}")
```

---

## TIMELINE

| Day | Task | Deliverable |
|-----|------|-------------|
| 1-2 | Parse GitHub catalog, extract all words + metadata | CSV: word, class, length |
| 2-3 | Implement word-to-matrix, compute traces and fixed points | CSV: word, matrix, trace, fixed_pts |
| 3-4 | Compute continued fractions and SB-tree positions | CSV: word, CF, SB_depth |
| 4-5 | Correlate with period data (T*, L_f) | Scatter plots, correlation coefficients |
| 5-7 | Test predictions 1-5 above | Draft findings document |
| 8-10 | Extend to unequal-mass catalog (1,223 orbits) | Extended results |
| 10-14 | Write up results, contact collaborators | Draft paper section or letter |

---

## KEY REFERENCES

### The orbit catalogs:
- Suvakov & Dmitrasinovic (2013), Phys. Rev. Lett. 110, 114301. [arXiv:1303.0181](https://arxiv.org/abs/1303.0181)
- Li & Liao (2017), Science China Phys. 60, 129511. [arXiv:1705.00527](https://arxiv.org/abs/1705.00527)
- Li, Jing & Liao (2018), PASJ 70(4), 64. [arXiv:1709.04775](https://arxiv.org/abs/1709.04775)
- Hristov et al. (2023), Celest. Mech. Dyn. Astron. [Springer](https://link.springer.com/article/10.1007/s10569-023-10177-w)
- Li & Liao (2025), 10,059 3D orbits. [SJTU website](https://numericaltank.sjtu.edu.cn/three-body/three-body.htm)
- **GitHub data repo:** https://github.com/sjtu-liao/three-body

### The mathematical bridge:
- Kin, Nakamura & Ogawa (2021), "Lissajous 3-braids", J. Math. Soc. Japan 75(1). [arXiv:2008.00585](https://arxiv.org/abs/2008.00585)
- Montgomery (2015), "The Three-Body Problem and the Shape Sphere", Amer. Math. Monthly 122(4). [arXiv:1402.0841](https://arxiv.org/abs/1402.0841)
- Series, "Continued Fractions and Hyperbolic Geometry". [PDF](https://warwick.ac.uk/fac/sci/maths/people/staff/caroline_series/hypgeomandcntdfractions.pdf)
- Moeckel, "Symbolic Dynamics in the Planar Three-Body Problem". [PDF](https://www-users.cse.umn.edu/~rmoeckel/research/SymDyn5.pdf)

### The period-topology law:
- Dmitrasinovic et al. (2015), Phys. Lett. A 379, 1939-1945.
- Dmitrasinovic et al. (2018), J. Phys. A 51, 315101. [arXiv:1705.03728](https://arxiv.org/abs/1705.03728)

### Background on PSL(2,Z) and Farey:
- Modular group: [Wikipedia](https://en.wikipedia.org/wiki/Modular_group)
- Congruence subgroups: [Wikipedia](https://en.wikipedia.org/wiki/Congruence_subgroup)
- Stern-Brocot tree: [Wikipedia](https://en.wikipedia.org/wiki/Stern%E2%80%93Brocot_tree)
