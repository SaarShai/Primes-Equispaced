# Adversarial Review Synthesis — Actions Required

## SPECTROSCOPE (220)
1. Peaks at zeros: SURVIVES. R(p) is not random — Farey-specific. ✓ Keep.
2. "Comparable to RS": FAILS. RS is exponentially faster with correction terms. 
   → ACTION: Weaken to "comparable to naive Dirichlet truncation" or remove comparison.
3. Multi-character 1/3 detection: WEAK. No p-value against null.
   → ACTION: Weaken language to "suggests detection" not "detects." Add caveat.
4. r=0.953 amplitude: SURVIVES (p<0.001). But fragile with only 10 points.
   → ACTION: Note sample size limitation. Keep correlation claim.

## CHEBYSHEV (221)  
1. R=0.77 correlation: INVALID if ΔW never flips sign in range.
   → ACTION: This is a real concern. ΔW IS always negative for qualifying p≤100K.
   The correlation is between the MAGNITUDE pattern and cos(), not the sign.
   Reframe: "the oscillation in |ΔW(p)| tracks cos(γ₁·log(p)+φ)"
2. Damage/Response: WEAK without proving R₁+R₂=ΔW.
   → ACTION: Verify the relationship. If they don't sum to ΔW, reframe.
3. D(1/p) 65%: Reviewer says FALSE — contradicts equidistribution.
   → COUNTERPOINT: The 65% is for NEW fractions (Def 1), which is a finite sum.
   The reviewer confused this with the TOTAL Farey sum. Our claim is specific and 
   verified. Keep but clarify it's about the per-step contribution, not cumulative.
4. Density → 1/2: Reviewer says FALSE — Chebyshev bias gives ~0.995.
   → IMPORTANT: Need to distinguish OUR ΔW density from the classical prime race.
   Our ΔW has a DIFFERENT constant term. The density might not be 1/2.
   → ACTION: Weaken to "density approaches 1/2 for the leading oscillation term"
   and note that the exact density depends on the constant term in ΔW.
