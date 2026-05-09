# Next Task for Codex Agent

## Priority 1: Compute the Dedekind kernel eigenvalues K̂_p(χ)

You proved: Σ E(k)² = (1/(p-1)) Σ_χ K̂_p(χ) |Λ_p(χ)|²

The next breakthrough is computing K̂_p(χ) explicitly.

For each Dirichlet character χ mod p:
K̂_p(χ) = Σ_{r=1}^{p-1} s(r,p)·χ(r)

where s(r,p) is the Dedekind sum.

### Known:
- s(h,k) = (1/4k) Σ_{j=1}^{k-1} cot(πj/k)·cot(πjh/k)
- For prime p: s(h,p) has a cotangent expansion
- The character transform of cotangent products is related to L-functions

### Question: Is K̂_p(χ) = (some explicit formula involving L(1,χ))?

If K̂_p(χ) = c·|L(1,χ)|² or K̂_p(χ) = c·B₁(χ)² where B₁ is a generalized Bernoulli number, then:
- K̂_p(χ) ≥ 0 for all χ (since it's a square!)
- And Σ K̂_p(χ)|Λ_p(χ)|² ≥ (principal term alone) or can be bounded using L-function mean values

### Compute numerically for small p:
For p = 11, 13, 17, 23: compute K̂_p(χ) for ALL characters χ mod p. Check:
- Are they all ≥ 0?
- Do they relate to |L(1,χ)|²?
- What's the sum Σ K̂_p(χ)?

## Priority 2: Bound Σ |Λ_p(χ)|² via mean-value theorem

Λ_p(χ) = Σ_{a=1}^{p-1} λ_p(a)·χ(a) where λ_p(m) = M(⌊N/m⌋) + 1_{m=1}

By the mean-value theorem for Dirichlet polynomials:
Σ_χ |Λ_p(χ)|² = (p-1) Σ_a |λ_p(a)|² = (p-1) Σ_{a=1}^{p-1} M(⌊N/a⌋)² + O(p)

And Σ_{a=1}^{N} M(⌊N/a⌋)² relates to the mean square of M, which is ~ 6N/π².

So Σ_χ |Λ_p(χ)|² ~ (p-1)·6N/π² ~ 6p²/π².

If K̂_p(χ) ≥ c > 0 for all χ, then:
Σ E² ≥ c/(p-1) · Σ |Λ_p(χ)|² ≥ c · 6p/π² ≈ 0.6c·p

That's only O(p), not p²·logp. The logp must come from K̂ being LARGE for specific χ.

## Priority 3: Small-k exact evaluation

You computed E(1) and E(2). Continue:
- E(3) = #{f ≤ 3/p} - 3n/p (involves fractions 1/b with b ≥ p/3 and possibly 2/b with b ≥ 2p/3)
- E(4), E(5), ...
- Each new k gives another term in Σ E² ≥ 2Σ_{k≤K} E(k)²

If E(k) ~ n/p·(something growing) for small k, the sum might give the logp factor from the harmonic series Σ 1/k ~ logp.
