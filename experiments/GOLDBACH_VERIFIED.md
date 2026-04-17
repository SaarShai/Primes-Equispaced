# Goldbach Spectroscope — Computational Verification
# Date: 2026-04-12

Sieving primes up to 200000...
  17984 primes
Computing r(2n) via FFT convolution...
  Done in  Done in 506.3s
  r(10)=3, r(100)=12, r(1000)=56

Computing Hardy-Littlewood predictions...
  Mean residual: 0.8173
  Std residual: 0.7056

Building spectroscope...
  Done in 1.2s

=== TOP 10 PEAKS ===
Background: mean=56.2, std=72.7
   gamma |      score |  z-score | note
--------------------------------------------------
    41.4 |      323.1 |     3.67 | 
    43.7 |      318.7 |     3.61 | 
    43.6 |      315.3 |     3.57 | 
    41.5 |      308.9 |     3.48 | 
    41.3 |      304.6 |     3.42 | 
    43.8 |      290.8 |     3.23 | 
    40.9 |      290.1 |     3.22 | 
    43.5 |      282.3 |     3.11 | 
    41.0 |      281.2 |     3.10 | 
    41.2 |      278.2 |     3.06 | 

=== DETECTION AT KNOWN ZEROS ===
      zero |    gamma |      score |  z-score | detected?
------------------------------------------------------------
   gamma_1 |     14.1 |        1.7 |    -0.75 | no
   gamma_2 |     21.0 |       62.4 |     0.09 | no
   gamma_3 |     25.0 |       22.6 |    -0.46 | no
   gamma_4 |     30.4 |       51.2 |    -0.07 | no
   gamma_5 |     32.9 |       51.5 |    -0.06 | no

=== ENHANCEMENT: Möbius-weighted Goldbach ===
Computing Möbius-weighted Goldbach sums...

Möbius-weighted peaks:
      zero |    gamma |  z-score | detected?
---------------------------------------------
   gamma_1 |     14.1 |    -0.25 | no
   gamma_2 |     21.0 |     0.80 | no
   gamma_3 |     25.0 |     0.27 | no
   gamma_4 |     30.4 |    -0.18 | no
   gamma_5 |     32.9 |     0.32 | no

Möbius-weighted top 5:
  gamma=46.2, z=1.06 
  gamma=46.8, z=1.00 
  gamma=45.6, z=0.97 
  gamma=21.1, z=0.96 <-- zeta gamma_2
  gamma=33.2, z=0.91 

Done.
