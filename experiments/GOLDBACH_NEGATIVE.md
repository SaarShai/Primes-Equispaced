# Goldbach Spectroscope: NEGATIVE RESULT
# Date: 2026-04-12
# Verified computationally at N=200,000 via FFT convolution

## Both approaches fail:
- Standard r(2n)/r_HL(2n) - 1: z-scores at γ₁..γ₅ all < 1. No detection.
- Möbius-weighted Σμ(p)μ(q): z-scores at γ₁..γ₅ all < 1.1. No detection.

## Why:
Goldbach sum r(2n) is a CONVOLUTION of prime indicators. The double
summation p+q=2n creates interference that smears individual zero peaks.
The Mertens spectroscope works because M(p) is a CUMULATIVE sum evaluated
at PRIMES (insertion points). r(2n) is evaluated at ALL even numbers with
no insertion structure.

## Correction:
M1 qwen report (M1_GOLDBACH_SPECTROSCOPE, 17KB) claimed detection.
That was theoretical analysis, not computation. Computation disproves it.

## Added to killed directions.
