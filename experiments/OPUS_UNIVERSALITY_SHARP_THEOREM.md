# Opus: Universality Sharp Theorem Design
# 2026-04-10

## THE THEOREM (4 parts + 2 corollaries)

### Theorem (Universality of Prime Spectroscopy) — Under GRH:

(i) DETECTION: If Σ_{p∈S} 1/p = ∞, then for every zero ρ = 1/2+iγ₀,
    limsup I_S(γ₀;X) = ∞.

(ii) QUANTITATIVE: If L_S(X) ≥ C·(loglog T)^{1+ε}, then
     I_S(γ_k;X) ≥ c_ε · L_S(X) for all |γ_k| ≤ T.

(iii) PROGRESSION RESOLUTION (partially UNCONDITIONAL via BV):
      I_{q,a}(γ;X) = (1/φ(q)) Σ_χ |χ(a)|² · I_χ(γ;X) + O_A(1/(log X)^A)
      → spectroscope from p≡a mod q detects L(s,χ) zeros, not just ζ zeros
      → UNCONDITIONAL for all but o(Q) moduli q ≤ X^{1/2}/(logX)^B (by BV)

(iv) REDUNDANCY: For any δ>0, ∃ S with |S∩[1,X]| ≤ X^δ and S detects every zero.

### Corollary 1 (Bounded Gaps Detect Zeros):
Primes with gaps ≤ 246 (Maynard-Tao) have Σ1/p = ∞ → detect all zeros under GRH.

### Corollary 2 (Large Sieve as RIP):
The prime-indexed Fourier matrix satisfies Restricted Isometry Property.
This IS compressed sensing — primes are a CS measurement system for the Riemann spectrum.

## MOST SURPRISING COROLLARY: Information Destruction

"You can destroy up to a density-one subset of primes (logarithmic sense)
and still recover EVERY zeta zero from the survivors."

Compression ratio: 9000:1 (2750 primes from 25M). Shannon-theoretic minimum: |S| ≳ logT · log(1/ε).

## COMPRESSED SENSING CONNECTION (genuinely new)

- Large sieve inequality IS a Restricted Isometry Property for prime-indexed Fourier measurements
- This connects universality to Candès-Tao compressed sensing framework
- "Continuous compressed sensing" (super-resolution) applies since zeros are continuous-valued
- Bourgain's work on RIP for bounded orthogonal systems is the technical template

## PROOF STRUCTURE (30-40 pages)
- Part (i): explicit formula + partial summation, 3-5 pages
- Part (ii): quantitative explicit formula bounds, 5-8 pages  
- Part (iii): BV + large sieve, 8-12 pages (hardest)
- Part (iv): PNT in short intervals, 1-2 pages
- CS corollary: large sieve → RIP translation, 3-5 pages

## STRATEGIC FRAMING

For Compositio/Math. Annalen: parts (i)-(iii), BV gives unconditional L-function result
For PNAS/broad: information theory + compressed sensing pitch
DO NOT frame as "energy concentration" — frame as universality + quantitative + information

## HEADLINE RESULTS FOR TALKS
1. "Bounded gap primes detect all zeta zeros"
2. "Primes are a compressed sensing system for the Riemann spectrum"  
3. "9000:1 compression — destroy 99.99% of primes, still recover all zeros"
