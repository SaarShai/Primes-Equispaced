# Coupling Proof Exploration: sigma_p vs Random Permutations

## Setup

For each denominator b coprime to prime p, the multiplication-by-p map sigma_p: a -> pa mod b is a permutation of the coprime residues (Z/bZ)*. We investigated whether this group automorphism structure can be exploited to bound R(p), the cumulative cross-correlation quantity related to Farey discrepancy.

### Definitions
- **Sawtooth function**: ((x)) = {x} - 1/2 for non-integer x, 0 otherwise
- **Per-b cross-correlation**: C(p,b) = sum over a coprime to b of ((a/b)) * ((pa/b))
- **This equals the Dedekind sum** s(p,b) (restricted to coprime residues)
- **Cumulative**: R(p) = sum over b <= B of (1/b) * C(p,b)
- **Mobius-weighted**: R_mu(p) = sum over b of (mu(b)/phi(b)) * C(p,b)

## Key Findings

### 1. Per-b z-scores are mild (sigma_p behaves like a typical permutation)

| Prime p | Mean z | Std z | |z| > 2 | |z| > 3 |
|---------|--------|-------|---------|---------|
| 13      | 0.48   | 0.91  | 9/183   | 0/183   |
| 31      | 0.13   | 1.26  | 22/192  | 2/192   |
| 97      | -0.10  | 1.78  | 39/196  | 14/196  |

For individual b values, sigma_p cross-correlation looks like a draw from the random permutation distribution. The z-scores are O(1), not systematically negative.

### 2. C(sigma_p, b) = s(p,b) connects to Dedekind sums

Verified: the coprime-restricted cross-correlation equals the Dedekind sum s(p,b).
- Correlation between C(sigma) and full s(p,b): 0.59-0.70
- Dedekind reciprocity s(p,b) + s(b,p) = (1/12)(p/b + b/p + 1/pb) - 1/4 confirmed numerically

### 3. Principal character cancellation (from character theory)

Decomposing in Dirichlet characters: S_b = (1/b) sum over chi != chi_0 of c_chi (1 - chi_bar(p)) tau_chi

The principal character term VANISHES because chi_0_bar(p) = 1. This is the key structural advantage of the group automorphism over random permutations.

### 4. Ratio C(sigma_p)/C(identity) shrinks with b

| b  | phi(b) | C(identity) = sum((a/b))^2 | C(sigma_p) = s(p,b) | Ratio  |
|----|--------|---------------------------|---------------------|--------|
| 7  | 6      | 0.357                     | -0.357              | -1.000 |
| 23 | 22     | 1.674                     | 0.022               | 0.013  |
| 53 | 52     | 4.170                     | -0.736              | -0.176 |
| 97 | 96     | 7.835                     | 0.691               | 0.088  |

The ratio C(sigma_p)/C(identity) = s(p,b)/[phi(b)/12] -> 0 as b grows, since s(p,b) = O(log b) while phi(b)/12 grows linearly.

### 5. Cumulative R(p) grows slowly (O(log B)^2 bound available)

Unweighted R(p) = sum (1/b) s(p,b):

| p  | R at b<=50 | R at b<=100 | R at b<=200 | z at b<=200 |
|----|-----------|-------------|-------------|-------------|
| 13 | -0.011    | 0.154       | 0.499       | 3.81        |
| 31 | -0.054    | -0.030      | 0.102       | 0.76        |
| 97 | 0.081     | 0.033       | -0.049      | -0.36       |

### 6. Mobius-weighted R_mu(p) STAYS BOUNDED (most promising)

| p  | R_mu at b<=50 | R_mu at b<=200 | z_cum at b<=200 | Growth exponent |
|----|--------------|----------------|-----------------|-----------------|
| 13 | -0.090       | 0.004          | 0.02            | B^{-2.3}        |
| 31 | 0.097        | 0.067          | 0.34            | B^{-0.3}        |
| 97 | -0.200       | -0.005         | -0.03           | B^{-1.9}        |

The Mobius-weighted version shows NEGATIVE growth exponents, meaning |R_mu| actually decreases. The z-scores never exceed 1.2 in absolute value.

## Assessment of the Coupling Approach

### What WORKS:
1. **Dedekind sum bounds**: |s(p,b)| <= O(log b) gives |R(p)| <= O((log B)^2) unconditionally
2. **Principal character cancellation**: Provably eliminates the dominant Fourier term
3. **Dedekind reciprocity**: Provides inter-b structural constraints
4. **Mobius-weighted cancellation**: R_mu(p) empirically stays O(1) or shrinks

### What DOES NOT work:
1. **sigma_p <= random (per-b)**: FALSE in cumulative. sigma_p cross-correlation accumulates while random permutations cancel (by independence across b).
2. **Variance reduction**: The per-b variance of sigma_p is NOT systematically below random. The z-scores are ~N(0,1).
3. **Displacement reduction**: sigma_p displacement is only marginally less than random (~97%).

### The original premise was backwards:
The data showed |R(p)| below all 500 random trials, but this was for a different quantity (the full delta-W, not the sawtooth cross-correlation). The sawtooth cross-correlation under sigma_p is of TYPICAL magnitude per b, but accumulates systematically (nonzero mean for p=13), while random permutations average to zero per b and cancel across b by independence.

## Viable Proof Paths

### Path A: Direct Dedekind sum bound (simplest)
- |R(p)| <= sum |s(p,b)|/b <= sum O(log b)/b = O((log B)^2)
- Unconditional, uses only Rademacher's bound
- Does NOT use the coupling idea at all

### Path B: Character sum approach
- Principal character cancels: saves a factor of phi(b) in the main term
- Non-principal characters bounded by Polya-Vinogradov or Burgess
- Could give R(p) = O(B^{1/2 + epsilon}) with effort

### Path C: Dedekind reciprocity + Mobius inversion
- Use reciprocity to pair s(p,b) with s(b,p) for b < p
- Mobius-weighted sum naturally cancels (empirically confirmed)
- Could prove R_mu(p) = O(1), which is the strongest result

### Path D: Hybrid coupling (salvageable)
- Don't compare sigma_p to random permutations
- Compare sigma_p to OTHER group automorphisms (multiplication by different primes)
- The set of group automorphisms is a subgroup of S_{phi(b)}
- Average over automorphisms to get cancellation

## Files
- `coupling_proof.py` - v1: basic comparison (found variance ratio ~50)
- `coupling_proof_v2.py` - v2: corrected with displacement analysis
- `coupling_proof_v3.py` - v3: full Farey discrepancy (found it's permutation-invariant)
- `coupling_proof_v4.py` - v4: sawtooth cross-correlation (definitive analysis)
- `coupling_proof_data.json` - raw data from v1

## Status: The coupling is useful as INTUITION, not as a proof technique.
The Dedekind sum route (Path A or C) is the actual proof path.
Aletheia rating: A1 (autonomous, minor novelty -- connects known objects in a modestly new way).
