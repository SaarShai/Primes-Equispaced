# Gauss Circle Per-Step Spectroscope — COMPUTATIONAL VERIFICATION
# Date: 2026-04-11
# Precision: 25 digits

Computing r_2(n) for n=1..100000...
  Done in 0.0s. Total representations: 314196, nonzero n: 24028
  r_2(1)=4, r_2(2)=4, r_2(5)=8, r_2(25)=12
  Mean r_2 = 3.1420 (should be ~pi = 3.1416)

Building spectroscope...
  Done in 700.7s (490 gamma values)

=== TOP 15 PEAKS ===
   gamma |        score |                           note
-------------------------------------------------------
    46.4 |      42719.7 |                               
    46.3 |      42275.5 |                               
    46.5 |      41363.7 |                               
    46.2 |      40171.0 |                               
    46.6 |      38293.1 |                               
    46.1 |      36738.6 |                               
    46.7 |      33807.0 |                               
    46.0 |      32435.2 |                               
    46.8 |      28367.3 |                               
    45.9 |      27757.2 |                               
    44.1 |      26028.4 |                               
    44.0 |      25585.8 |                               
    44.2 |      25509.8 |                               
    27.3 |      24869.9 |                               
    27.2 |      24840.1 |                               

=== DETECTION AT KNOWN ZEROS ===
Background: mean=4212.7, std=7354.0

                        target |    gamma |      score |  z-score
-----------------------------------------------------------------
           L(s,chi_-4) gamma_1 |      6.0 |       46.5 |    -0.57 no
           L(s,chi_-4) gamma_2 |     10.2 |      170.2 |    -0.55 no
                  zeta gamma_1 |     14.1 |      197.3 |    -0.55 no
                  zeta gamma_2 |     21.0 |      369.6 |    -0.52 no
                  zeta gamma_3 |     25.0 |      551.4 |    -0.50 no

=== VERDICT ===
If z-score > 3 at L(s,chi_-4) zeros: FRAMEWORK GENERALIZES
If z-score > 3 at zeta zeros: DOUBLE DETECTION (both L-functions)
