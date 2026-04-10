# Practical Algorithms — Which Benefit From Zero Knowledge?
# 2026-04-10 — Opus analysis + our prime counting test

## DEAD ENDS (no gain)
- AKS, Pollard rho, Reed-Solomon, LDPC, RSA keygen, EC-DLP, ECPP, Lenstra ECM
- Prime counting with explicit formula: TESTED, makes π(x) WORSE at moderate x (oscillation)

## TESTABLE WITH MEASURABLE GAIN

### 1. Dirichlet L-function zero computation (THE KILLER APP)
- Classical: O(q) per evaluation for L(s,χ) mod q
- Spectroscope: batch all χ mod q simultaneously 
- Already verified: 12x at q=10K, 141x at q=1M
- TEST: wall-clock timing comparison at q=101, 1009, 10007
- This is our EXISTING batch speedup result — just needs timing verification

### 2. QS smoothness bound optimization (~5-15% improvement)
- Dickman function correction from zeta zeros changes optimal B by ~5-10%
- Measurable: count relations per sieve unit with standard vs corrected B
- 45 min test

### 3. Unconditional error bounds from verified L-function zeros
- Verify GRH for L(s,χ) to height T → unconditional bounds
- Specific: least quadratic nonresidue unconditional bound
- Publishable story: "arithmetic data gives unconditional bounds"
- 45 min test

## KEY INSIGHT FROM OPUS
"The genuine breakthrough application is Dirichlet L-function zero computation
from arithmetic data. If the spectroscope scales better than O(q) per zero,
that is a genuine algorithmic contribution to computational number theory,
independent of all application-layer stuff."

This IS our batch L-function result. We already have it.
The test needed: actual wall-clock timing, not just operation counts.
