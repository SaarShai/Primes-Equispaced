======================================================================
LMFDB BENCHMARK: Batch Spectroscope vs Individual Computation
======================================================================


============================================================
  CONDUCTOR q = 97 (prime), phi(q) = 96
============================================================

Method A: Batch spectroscope (96 characters, 290 gamma values)...
  Time: 159.46s
  Top 10 detected zeros:
    chi_13: gamma = 29.9000, score = 7242.07
    chi_10: gamma = 29.4000, score = 5335.40
    chi_2: gamma = 25.6000, score = 3691.70
    chi_7: gamma = 28.8000, score = 3573.66
    chi_5: gamma = 29.9000, score = 3563.21
    chi_18: gamma = 28.4000, score = 3124.19
    chi_16: gamma = 29.8000, score = 2890.20
    chi_1: gamma = 29.3000, score = 2716.03
    chi_9: gamma = 20.7000, score = 1955.24
    chi_4: gamma = 28.5000, score = 1586.27

Method B: Individual zero search (first 20 characters)...
  Time: 40.63s
  First 10 detected zeros:
    chi_1: gamma ~ 2.5000
    chi_2: gamma ~ 17.1000
    chi_3: gamma ~ 24.9000
    chi_4: gamma ~ 25.7000
    chi_5: gamma ~ 21.6000
    chi_6: gamma ~ 13.2000
    chi_7: gamma ~ 11.0000
    chi_8: gamma ~ 25.7000
    chi_9: gamma ~ 5.4000
    chi_10: gamma ~ 27.9000

  COMPARISON (q=97):
    Batch (96 chars): 159.46s
    Individual (20 chars): 40.63s
    Projected individual (all 96 chars): 195.0s
    SPEEDUP: 1.2x

============================================================
  CONDUCTOR q = 251 (prime), phi(q) = 250
============================================================

Method A: Batch spectroscope (250 characters, 290 gamma values)...
  Time: 420.85s
  Top 10 detected zeros:
    chi_9: gamma = 21.3000, score = 8043.75
    chi_7: gamma = 25.6000, score = 4873.74
    chi_11: gamma = 29.9000, score = 4815.72
    chi_10: gamma = 29.8000, score = 4769.89
    chi_6: gamma = 29.2000, score = 4177.50
    chi_8: gamma = 29.3000, score = 3599.97
    chi_5: gamma = 29.9000, score = 3478.36
    chi_12: gamma = 28.9000, score = 1465.28
    chi_4: gamma = 25.2000, score = 1426.31
    chi_13: gamma = 21.3000, score = 1123.22
