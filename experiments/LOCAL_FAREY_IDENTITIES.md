# New Farey Identities (Session 14, 2026-04-14)
## Identity 1: Sum of new fraction discrepancies
For prime p: Σ_{k=1}^{p-1} D_{F_p}(k/p) = (p-1)/2

PROOF: Farey reflection symmetry. For any Farey sequence F_N with n=|F_N| fractions:
- rank(a/b) + rank((b-a)/b) = n + 1 (symmetry: the k-th and (n+1-k)-th fractions)
- So D_N(a/b) + D_N((b-a)/b) = (n+1) - n*(a/b + (b-a)/b) = (n+1) - n = 1
- The new fractions k/p (k=1..p-1) pair as (k/p, (p-k)/p) for k=1..(p-1)/2
- Each pair sums to 1, giving (p-1)/2 pairs → total = (p-1)/2 □

Verified exactly for p=7,11,13,17,19,23,29,31,37,41,43,47 (all primes tested).

## Identity 2: Sum of shifts is zero
For prime p: Σ_{f∈F_{p-1}} δ(f) = 0
where δ(f) = D_{F_p}(f) - D_{F_{p-1}}(f)

PROOF: 
Σ_{f∈F_N} D_{F_N}(f) = n/2 (exactly) [from pairing: f and 1-f cancel to 1/2 each]
So Σ δ(f) = Σ D_p(f) - Σ D_{p-1}(f)
= n/2 - n/2 = 0 □
(Note: Σ_{f∈F_{p-1}} D_p(f) = n/2 by: n'/2 - Σ_{new} D_p = n'/2 - (p-1)/2 = n/2)

Verified exactly for p=7..47.
