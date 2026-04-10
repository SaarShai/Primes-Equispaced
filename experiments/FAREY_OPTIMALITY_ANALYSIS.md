# Farey Mediant Insertion: Optimality Analysis

**Date:** 2026-03-29
**Status:** Unverified analysis -- needs adversarial review
**Verdict:** Farey mediant insertion is NOT optimal for minimizing maximum gap. Midpoint bisection is strictly better. However, Farey has a different, provable advantage: minimal-denominator gap-filling, which may matter for 3DGS.

---

## 1. Setup

We start with interval [0, 1] (fractions 0/1 and 1/1). We sequentially insert K points. After each insertion, we measure the maximum remaining gap. Two strategies:

- **Midpoint bisection:** always insert the midpoint of the largest gap.
- **Farey mediant:** always insert the mediant (a+c)/(b+d) of the pair a/b, c/d bounding the largest gap.

Both strategies share the greedy property: they always target the largest gap. They differ in WHERE within that gap they place the new point.

## 2. Maximum Gap After K Insertions

### 2.1 Midpoint Bisection

This is well-understood. The strategy always places the new point at the exact center of the largest gap.

After K insertions:
- K=1: insert 1/2, max_gap = 1/2
- K=2: insert 1/4 (or 3/4), max_gap = 1/2 (one half still unsplit)
- K=3: insert 3/4 (or 1/4), max_gap = 1/4
- General: max_gap(K) = 1/2^{floor(log2(K+1))}

This achieves the BEST POSSIBLE max_gap for any sequential insertion strategy targeting the largest gap with a midpoint split, because every split perfectly halves the targeted interval.

### 2.2 Farey Mediant Insertion (Stern-Brocot level order)

The mediant of a/b and c/d is (a+c)/(b+d). For adjacent Farey fractions, the gap is exactly 1/(bd) (since |bc - ad| = 1).

After inserting the mediant (a+c)/(b+d), the gap splits into two sub-gaps:
- Left: (a+c)/(b+d) - a/b = 1/(b(b+d))
- Right: c/d - (a+c)/(b+d) = 1/(d(b+d))

**Critical observation:** The mediant does NOT split the gap in half. It splits it in ratio d:b.

Starting from 0/1 and 1/1:
- K=1: insert mediant 1/2, gap = 1/(1*1) = 1 splits into 1/(1*2) = 1/2 and 1/(1*2) = 1/2. max_gap = 1/2.
  (Same as bisection -- symmetric case.)

- K=2: largest gaps are [0/1, 1/2] and [1/2, 1/1], both size 1/2.
  Insert mediant of 0/1 and 1/2: that's 1/3.
  New gaps: [0/1, 1/3] = 1/3, [1/3, 1/2] = 1/6, [1/2, 1/1] = 1/2.
  max_gap = **1/2**.

  Bisection would insert 1/4. Gaps: [0, 1/4] = 1/4, [1/4, 1/2] = 1/4, [1/2, 1] = 1/2.
  max_gap = **1/2**. (Same.)

  BUT: mediant left a gap of 1/2 AND created an unnecessarily small gap of 1/6. Bisection left gaps more uniform (1/4, 1/4, 1/2).

- K=3: For Farey, largest gap is still [1/2, 1/1] = 1/2. Insert mediant 2/3.
  Gaps: 1/3, 1/6, 1/6, 1/3. max_gap = **1/3**.

  For bisection, largest gap is [1/2, 1] = 1/2. Insert 3/4.
  Gaps: 1/4, 1/4, 1/4, 1/4. max_gap = **1/4**.

  **Farey max_gap = 1/3 > 1/4 = bisection max_gap.**

This gap compounds. At K=3, bisection is already strictly better.

### 2.3 Why Farey Loses: The Asymmetric Split

The mediant (a+c)/(b+d) of a/b and c/d splits the gap 1/(bd) into:
- 1/(b(b+d)) and 1/(d(b+d))

These are equal ONLY when b = d. When b != d, the split is asymmetric, creating one sub-gap larger than half the original and one smaller. This is strictly worse than bisection for the minimax objective.

**Theorem (informal):** For any gap-filling strategy that always targets the largest gap, placing the new point at the midpoint minimizes the maximum gap after each insertion. The mediant placement is suboptimal whenever the bounding denominators differ.

**Proof sketch:** After splitting the largest gap G into two pieces L and R with L + R = G, the new max_gap is max(L, R, second_largest_gap). To minimize max(L, R), we need L = R = G/2, which is achieved by midpoint bisection. Any asymmetric split gives max(L, R) > G/2.

### 2.4 Quantitative Comparison

| K (insertions) | Bisection max_gap | Farey max_gap | Farey/Bisection ratio |
|---|---|---|---|
| 1 | 1/2 = 0.500 | 1/2 = 0.500 | 1.00 |
| 3 | 1/4 = 0.250 | 1/3 = 0.333 | 1.33 |
| 7 | 1/8 = 0.125 | ~1/5 = 0.200 | ~1.60 |
| 15 | 1/16 = 0.0625 | ~1/8 = 0.125 | ~2.00 |

Asymptotically, after K insertions:
- Bisection: max_gap ~ 1/K (precisely 1/2^{floor(log2(K+1))})
- Farey (SB level order): max_gap ~ C/K for some C > 1

Both are O(1/K), but bisection has a better constant.

## 3. Discrepancy Comparison

### 3.1 Van der Corput Sequence
Star discrepancy: D*_N = O(log N / N). This is optimal among all 1D sequences (matching the Schmidt lower bound up to constants).

### 3.2 Farey Sequence F_Q
The discrepancy of the full Farey sequence F_Q is exactly 1/Q (Dress, 1999). Since |F_Q| ~ 3Q^2/pi^2, this means:
D*_N ~ pi^2/(3N) * 1/sqrt(N * pi^2/3) ... actually, restating:

For the Farey sequence, D_Q = 1/Q with ~3Q^2/pi^2 points, so D*_N ~ pi/(3*sqrt(N/3)) ... No. Let's be precise:

|F_Q| ~ 3Q^2/pi^2, and D_Q (discrepancy of F_Q) = 1/Q exactly. So expressed in terms of N = |F_Q|:
Q ~ sqrt(pi^2 N / 3), so D*_N = 1/Q ~ 1/sqrt(pi^2 N/3) = sqrt(3)/(pi * sqrt(N)) = O(1/sqrt(N)).

This is MUCH WORSE than Van der Corput's O(log N / N).

**However:** this comparison is slightly unfair. F_Q is not a "designed" low-discrepancy sequence -- it's a number-theoretic object containing ALL fractions up to denominator Q. The Stern-Brocot insertion order (level-by-level) produces a different ordering.

### 3.3 Stern-Brocot Level Order Discrepancy
The first K fractions in Stern-Brocot level order are NOT the same as F_Q for any Q. Their discrepancy is not well-studied in the literature. Based on the gap analysis above, since the maximum gap is worse than bisection, the discrepancy is likely worse than Van der Corput.

### 3.4 Verdict on Discrepancy
Farey/Stern-Brocot does NOT beat Van der Corput for discrepancy. The uniformity argument does not hold up.

## 4. What IS Farey Optimal For?

Despite losing on max_gap and discrepancy, Farey mediant insertion has genuine mathematical advantages:

### 4.1 Minimal Denominator Property
**Theorem:** Among all fractions strictly between a/b and c/d (where bc - ad = 1), the mediant (a+c)/(b+d) has the smallest denominator.

*Proof:* Any fraction p/q strictly between a/b and c/d satisfies:
- p/q > a/b implies pb - qa >= 1 (since both are integers), so pb >= qa + 1
- p/q < c/d implies qc - pd >= 1, so qc >= pd + 1
Adding: q(b+d) >= (a+c) + ... wait, let's do this properly.

From pb - qa >= 1 and qc - pd >= 1, adding gives q(c+a)... no. pb - qa >= 1 and qc - pd >= 1. We want to bound q.
Adding: pb + qc - qa - pd >= 2, so q(c-a) + p(b-d)... this doesn't simplify nicely.

Better approach: pb >= qa + 1 and qc >= pd + 1.
Multiply first by d: pbd >= qad + d
Multiply second by b: qbc >= pbd + b
Substituting: qbc >= qad + d + b, so q(bc - ad) >= b + d.
Since bc - ad = 1: **q >= b + d**.

So the denominator of ANY fraction between a/b and c/d is at least b+d, and the mediant achieves this minimum. QED.

### 4.2 Implications for 3DGS

In 3DGS, a "fraction" p/q parameterizes a Gaussian splat. The denominator q controls:
- The "complexity" or "cost" of the representation
- In a hierarchical scheme, lower-denominator fractions are more "fundamental"

The mediant insertion therefore gives the CHEAPEST possible new point in each gap. This is a real advantage if:
1. There is a cost associated with denominator size
2. You want a hierarchy where coarser levels use simpler fractions
3. You're building a level-of-detail structure

### 4.3 Best Rational Approximation Property
The Stern-Brocot tree has the property that for any real number x, the path from the root to x gives the sequence of best rational approximations (convergents of the continued fraction). This means Stern-Brocot insertion is optimal for APPROXIMATION of a target, not for COVERAGE of an interval.

## 5. Honest Assessment for the Paper

### What we CANNOT claim:
- Farey mediant insertion minimizes maximum gap (FALSE -- bisection is better)
- Farey gives better coverage/discrepancy than standard sequences (FALSE -- Van der Corput is better)
- Farey is the optimal sequential insertion strategy (FALSE in the minimax sense)

### What we CAN claim:
1. **Minimal denominator gap-filling (Theorem):** The mediant has the smallest possible denominator among all fractions in a given gap. This is a clean, provable result (proved above).

2. **Hierarchical efficiency:** Stern-Brocot insertion produces a natural tree structure where each level approximately doubles the point count, with each new point being the "simplest" possible in its gap.

3. **Both strategies are O(1/K):** While bisection has a better constant, both Farey and bisection achieve max_gap = O(1/K), so the asymptotic rate is the same.

4. **Rational structure:** Farey points have exact rational coordinates with controlled denominators, which may matter for fixed-point arithmetic or hierarchical data structures.

5. **Adaptive potential:** In practice, 3DGS doesn't need uniform coverage -- it needs to fill gaps where error is high. Both Farey and bisection target the largest gap. The question is whether the minimal-denominator property of Farey leads to better convergence in practice -- this is an empirical question, not a theorem.

## 6. Candidate Lean Theorem

The minimal denominator result (Section 4.1) is clean enough to formalize:

**Theorem (Mediant Minimality):** Let a/b and c/d be Farey neighbors (bc - ad = 1). For any fraction p/q with a/b < p/q < c/d and gcd(p,q) = 1, we have q >= b + d. Equality holds iff p/q = (a+c)/(b+d).

This is a known result in the theory of continued fractions (essentially the "children property" of the Stern-Brocot tree), but formalizing it in Lean would be valuable for our framework.

## 7. Summary

| Criterion | Farey Mediant | Midpoint Bisection | Winner |
|---|---|---|---|
| Max gap after K insertions | ~C/K (C > 1) | 1/2^{floor(log2(K+1))} | Bisection |
| Discrepancy | Worse than O(log N/N) | O(log N/N) equivalent | Bisection |
| Minimal denominator | YES (provably optimal) | No (irrational points) | Farey |
| Hierarchical structure | Natural tree, each level 2x | Binary tree, each level 2x | Tie |
| Best approximation | Convergents are optimal | No approximation guarantee | Farey |
| Rational arithmetic | All points rational | Points are k/2^n (dyadic) | Tie |

**Bottom line:** Farey is not optimal for coverage. It IS optimal for minimal-denominator gap-filling. The paper should emphasize the denominator minimality theorem, not claim coverage optimality.

## References

- Stern-Brocot tree: https://en.wikipedia.org/wiki/Stern%E2%80%93Brocot_tree
- Farey sequence gap properties: https://en.wikipedia.org/wiki/Farey_sequence
- Van der Corput discrepancy: https://en.wikipedia.org/wiki/Van_der_Corput_sequence
- Dress (1999) on Farey discrepancy: https://link.springer.com/article/10.1007/s10474-018-0868-x
- Online dispersion problem: https://arxiv.org/abs/1704.06823
- Farey gap distribution (BCZ map): https://arxiv.org/abs/2407.04380
