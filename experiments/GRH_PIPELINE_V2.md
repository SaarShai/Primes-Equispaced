# GRH Pipeline v2: Quadratic Character Spectral Analysis

**Date:** 2026-04-08 07:26
**Sieve limit:** N = 1,000,000
**Primes used:** 78,498
**Gamma range:** [1.0, 50.0], 10000 points
**Peak detection:** scipy prominence + global z > 2.0
**Zero match tolerance:** 0.5

## Methods
- **A (Prime Sum):** F(gamma) = |sum_p chi(p)/sqrt(p) * exp(-i*gamma*log(p))|^2
- **B (Mertens):** F(gamma) = gamma^2 * |sum_p M_chi(p)/p * exp(-i*gamma*log(p))|^2

## Summary Table

| q | A: #Peaks | A: First | B: #Peaks | B: First | Time |
|---|-----------|----------|-----------|----------|------|
|  3 | 13 |   8.00 | 11 |   7.99 | 13.5s |
|  5 | 14 |   6.62 | 12 |  35.73 | 13.3s |
|  7 | 10 |   4.46 |  9 |   4.47 | 13.2s |
| 11 | 12 |   2.55 | 12 |   2.53 | 13.3s |
| 13 | 12 |   7.09 | 12 |  19.42 | 13.2s |
| 17 | 12 |   3.66 |  4 |   5.74 | 13.5s |
| 19 | 10 |   1.60 | 22 |  17.36 | 13.2s |
| 23 | 11 |   2.78 |  8 |  12.38 | 13.4s |
| 29 | 10 |   1.92 | 15 |  10.41 | 13.5s |
| 31 | 11 |   4.72 | 11 |  23.96 | 13.5s |
| 37 | 12 |   2.13 | 13 |   8.06 | 13.4s |
| 41 | 13 |   4.65 |  8 |   5.76 | 13.5s |
| 43 |  9 |  16.19 | 18 |  36.83 | 13.3s |
| 47 | 11 |   2.10 |  8 |   3.78 | 13.3s |
|  4 | 15 |   6.03 | 12 |   6.07 | 13.1s |

## Validation Against Known L-function Zeros

### L(s, chi_3)
Known zeros: 8.04, 13.16

**Method A** (13 peaks):
- Zero 8.04 -> peak 8.00 (delta=0.04) **MATCH**
- Zero 13.16 -> peak 11.32 (delta=1.84) **MISS**

**Method B** (11 peaks):
- Zero 8.04 -> peak 7.99 (delta=0.05) **MATCH**
- Zero 13.16 -> peak 7.99 (delta=5.17) **MISS**

### L(s, chi_4)
Known zeros: 6.02, 10.24, 12.59

**Method A** (15 peaks):
- Zero 6.02 -> peak 6.03 (delta=0.01) **MATCH**
- Zero 10.24 -> peak 10.21 (delta=0.03) **MATCH**
- Zero 12.59 -> peak 13.05 (delta=0.46) **MATCH**

**Method B** (12 peaks):
- Zero 6.02 -> peak 6.07 (delta=0.05) **MATCH**
- Zero 10.24 -> peak 10.11 (delta=0.13) **MATCH**
- Zero 12.59 -> peak 13.02 (delta=0.43) **MATCH**

### L(s, chi_5)
Known zeros: 6.18, 8.72

**Method A** (14 peaks):
- Zero 6.18 -> peak 6.62 (delta=0.44) **MATCH**
- Zero 8.72 -> peak 9.85 (delta=1.13) **MISS**

**Method B** (12 peaks):
- Zero 6.18 -> peak 35.73 (delta=29.55) **MISS**
- Zero 8.72 -> peak 35.73 (delta=27.01) **MISS**


## Verdict

- **Characters tested:** 14 quadratic (q=3..47) + chi_4 = 15 total
- **Known zeros checked:** 7 (chi_3, chi_4, chi_5)
- **Method A matches:** 5/7
- **Method B matches:** 4/7
- **Best method:** A with 71% match rate

**PARTIAL EVIDENCE:** Some L-function zeros detected. Method shows promise
but may need larger N or finer gamma grid for robust verification.

## Full Peak Lists (Top 10 per character)

### q=3, Method A
  - gamma=7.998, F=1.06e+01, z=4.8
  - gamma=11.316, F=7.29e+00, z=3.0
  - gamma=15.623, F=6.73e+00, z=2.7
  - gamma=18.260, F=7.83e+00, z=3.3
  - gamma=26.522, F=7.58e+00, z=3.2
  - gamma=28.315, F=6.93e+00, z=2.8
  - gamma=33.765, F=6.11e+00, z=2.4
  - gamma=35.612, F=7.91e+00, z=3.3
  - gamma=37.616, F=7.04e+00, z=2.9
  - gamma=42.483, F=5.84e+00, z=2.2
  - ... (3 more)

### q=3, Method B
  - gamma=7.993, F=2.18e+04, z=2.6
  - gamma=28.070, F=2.22e+04, z=2.7
  - gamma=39.944, F=1.99e+04, z=2.3
  - gamma=40.469, F=1.91e+04, z=2.2
  - gamma=43.350, F=2.41e+04, z=3.0
  - gamma=43.884, F=3.58e+04, z=4.9
  - gamma=44.413, F=2.46e+04, z=3.1
  - gamma=46.256, F=2.83e+04, z=3.7
  - gamma=46.785, F=3.90e+04, z=5.4
  - gamma=47.324, F=3.93e+04, z=5.5
  - ... (1 more)

### q=5, Method A
  - gamma=6.616, F=6.48e+00, z=2.3
  - gamma=9.850, F=7.27e+00, z=2.7
  - gamma=12.080, F=6.29e+00, z=2.2
  - gamma=15.902, F=8.53e+00, z=3.4
  - gamma=17.578, F=9.44e+00, z=3.8
  - gamma=19.617, F=6.55e+00, z=2.3
  - gamma=22.151, F=6.12e+00, z=2.1
  - gamma=28.492, F=6.68e+00, z=2.4
  - gamma=29.874, F=7.53e+00, z=2.9
  - gamma=34.676, F=6.21e+00, z=2.2
  - ... (4 more)

### q=5, Method B
  - gamma=35.735, F=3.67e+04, z=2.8
  - gamma=37.857, F=2.92e+04, z=2.0
  - gamma=43.311, F=3.74e+04, z=2.9
  - gamma=43.845, F=5.27e+04, z=4.3
  - gamma=44.369, F=3.67e+04, z=2.8
  - gamma=45.340, F=4.12e+04, z=3.2
  - gamma=45.815, F=4.65e+04, z=3.7
  - gamma=46.334, F=6.55e+04, z=5.6
  - gamma=46.849, F=5.26e+04, z=4.3
  - gamma=47.354, F=4.72e+04, z=3.8
  - ... (2 more)

### q=7, Method A
  - gamma=4.460, F=9.53e+00, z=3.9
  - gamma=6.959, F=7.41e+00, z=2.8
  - gamma=11.017, F=8.87e+00, z=3.5
  - gamma=12.541, F=6.22e+00, z=2.2
  - gamma=21.803, F=8.67e+00, z=3.4
  - gamma=23.194, F=9.20e+00, z=3.7
  - gamma=24.669, F=8.17e+00, z=3.2
  - gamma=38.180, F=7.68e+00, z=2.9
  - gamma=39.405, F=7.72e+00, z=3.0
  - gamma=40.772, F=7.26e+00, z=2.7

### q=7, Method B
  - gamma=4.474, F=2.41e+04, z=5.8
  - gamma=6.905, F=1.40e+04, z=3.0
  - gamma=39.400, F=1.36e+04, z=2.8
  - gamma=46.766, F=1.08e+04, z=2.0
  - gamma=47.300, F=1.61e+04, z=3.6
  - gamma=47.824, F=1.07e+04, z=2.0
  - gamma=48.309, F=1.12e+04, z=2.2
  - gamma=48.858, F=1.46e+04, z=3.1
  - gamma=49.838, F=1.35e+04, z=2.8

### q=11, Method A
  - gamma=2.549, F=7.93e+00, z=2.7
  - gamma=8.963, F=8.89e+00, z=3.2
  - gamma=10.203, F=1.09e+01, z=4.2
  - gamma=16.887, F=6.58e+00, z=2.1
  - gamma=20.190, F=6.88e+00, z=2.2
  - gamma=24.503, F=8.93e+00, z=3.2
  - gamma=25.659, F=9.16e+00, z=3.3
  - gamma=35.362, F=6.77e+00, z=2.2
  - gamma=36.627, F=8.12e+00, z=2.8
  - gamma=37.763, F=8.53e+00, z=3.0
  - ... (2 more)

### q=11, Method B
  - gamma=2.529, F=1.74e+04, z=2.2
  - gamma=8.890, F=1.81e+04, z=2.3
  - gamma=24.513, F=1.90e+04, z=2.5
  - gamma=24.963, F=2.03e+04, z=2.7
  - gamma=25.507, F=3.31e+04, z=5.1
  - gamma=25.978, F=3.04e+04, z=4.6
  - gamma=26.497, F=2.11e+04, z=2.9
  - gamma=36.563, F=2.46e+04, z=3.5
  - gamma=47.368, F=2.44e+04, z=3.5
  - gamma=47.912, F=1.81e+04, z=2.3
  - ... (2 more)

### q=13, Method A
  - gamma=7.091, F=8.31e+00, z=3.1
  - gamma=8.645, F=7.81e+00, z=2.8
  - gamma=18.656, F=7.50e+00, z=2.7
  - gamma=19.607, F=9.03e+00, z=3.4
  - gamma=21.161, F=7.00e+00, z=2.4
  - gamma=25.238, F=9.22e+00, z=3.5
  - gamma=26.399, F=6.53e+00, z=2.2
  - gamma=27.786, F=6.21e+00, z=2.0
  - gamma=34.269, F=6.35e+00, z=2.1
  - gamma=36.793, F=6.98e+00, z=2.4
  - ... (2 more)

### q=13, Method B
  - gamma=19.416, F=2.35e+04, z=4.1
  - gamma=19.916, F=1.43e+04, z=2.1
  - gamma=20.965, F=1.60e+04, z=2.5
  - gamma=25.184, F=1.88e+04, z=3.1
  - gamma=25.694, F=1.82e+04, z=2.9
  - gamma=26.228, F=2.39e+04, z=4.2
  - gamma=26.723, F=1.84e+04, z=3.0
  - gamma=30.060, F=1.49e+04, z=2.2
  - gamma=30.589, F=1.42e+04, z=2.1
  - gamma=47.143, F=1.77e+04, z=2.8
  - ... (2 more)

### q=17, Method A
  - gamma=3.656, F=8.26e+00, z=2.9
  - gamma=5.680, F=7.78e+00, z=2.7
  - gamma=11.948, F=6.42e+00, z=2.0
  - gamma=15.618, F=6.52e+00, z=2.1
  - gamma=16.353, F=8.41e+00, z=3.0
  - gamma=22.106, F=9.49e+00, z=3.5
  - gamma=23.185, F=9.88e+00, z=3.7
  - gamma=24.238, F=1.11e+01, z=4.3
  - gamma=35.784, F=6.77e+00, z=2.2
  - gamma=38.067, F=9.49e+00, z=3.5
  - ... (2 more)

### q=17, Method B
  - gamma=5.744, F=1.81e+04, z=3.0
  - gamma=15.574, F=2.46e+04, z=4.4
  - gamma=16.074, F=2.83e+04, z=5.2
  - gamma=48.084, F=1.44e+04, z=2.2

### q=19, Method A
  - gamma=1.603, F=9.54e+00, z=3.3
  - gamma=12.359, F=6.92e+00, z=2.1
  - gamma=16.770, F=1.52e+01, z=5.9
  - gamma=17.417, F=1.21e+01, z=4.5
  - gamma=26.919, F=7.61e+00, z=2.4
  - gamma=30.339, F=8.05e+00, z=2.6
  - gamma=32.726, F=6.98e+00, z=2.1
  - gamma=37.518, F=6.95e+00, z=2.1
  - gamma=45.457, F=7.18e+00, z=2.2
  - gamma=46.506, F=6.86e+00, z=2.1

### q=19, Method B
  - gamma=17.363, F=3.16e+04, z=2.2
  - gamma=17.809, F=3.33e+04, z=2.4
  - gamma=26.355, F=3.40e+04, z=2.4
  - gamma=26.879, F=3.95e+04, z=3.0
  - gamma=27.855, F=3.51e+04, z=2.6
  - gamma=28.320, F=3.21e+04, z=2.2
  - gamma=28.820, F=3.38e+04, z=2.4
  - gamma=29.325, F=4.31e+04, z=3.4
  - gamma=29.820, F=3.36e+04, z=2.4
  - gamma=31.736, F=3.20e+04, z=2.2
  - ... (12 more)

### q=23, Method A
  - gamma=2.779, F=9.21e+00, z=3.2
  - gamma=4.293, F=8.17e+00, z=2.7
  - gamma=12.482, F=7.27e+00, z=2.3
  - gamma=13.589, F=7.52e+00, z=2.4
  - gamma=15.407, F=6.71e+00, z=2.0
  - gamma=16.084, F=1.24e+01, z=4.7
  - gamma=29.923, F=7.12e+00, z=2.2
  - gamma=31.212, F=9.74e+00, z=3.5
  - gamma=31.971, F=9.71e+00, z=3.4
  - gamma=43.360, F=8.04e+00, z=2.7
  - ... (1 more)

### q=23, Method B
  - gamma=12.384, F=1.70e+04, z=3.1
  - gamma=15.290, F=1.43e+04, z=2.5
  - gamma=31.133, F=2.29e+04, z=4.5
  - gamma=31.657, F=2.35e+04, z=4.7
  - gamma=41.596, F=1.62e+04, z=2.9
  - gamma=42.149, F=1.80e+04, z=3.4
  - gamma=48.618, F=1.52e+04, z=2.7
  - gamma=49.716, F=1.27e+04, z=2.1

### q=29, Method A
  - gamma=1.921, F=7.76e+00, z=2.7
  - gamma=11.301, F=7.20e+00, z=2.4
  - gamma=16.691, F=9.00e+00, z=3.3
  - gamma=17.823, F=1.02e+01, z=3.9
  - gamma=18.632, F=9.32e+00, z=3.4
  - gamma=29.526, F=8.48e+00, z=3.0
  - gamma=32.966, F=9.84e+00, z=3.7
  - gamma=44.703, F=6.93e+00, z=2.2
  - gamma=45.467, F=7.14e+00, z=2.4
  - gamma=47.687, F=7.42e+00, z=2.5

### q=29, Method B
  - gamma=10.414, F=2.57e+04, z=2.1
  - gamma=16.721, F=3.74e+04, z=3.4
  - gamma=17.196, F=3.31e+04, z=2.9
  - gamma=17.716, F=4.95e+04, z=4.8
  - gamma=18.186, F=3.30e+04, z=2.9
  - gamma=32.956, F=3.39e+04, z=3.0
  - gamma=33.490, F=3.97e+04, z=3.7
  - gamma=34.005, F=3.18e+04, z=2.8
  - gamma=34.529, F=2.66e+04, z=2.2
  - gamma=45.232, F=4.26e+04, z=4.0
  - ... (5 more)

### q=31, Method A
  - gamma=4.719, F=9.17e+00, z=3.2
  - gamma=5.793, F=9.95e+00, z=3.6
  - gamma=18.323, F=7.44e+00, z=2.4
  - gamma=20.332, F=6.67e+00, z=2.0
  - gamma=22.449, F=6.63e+00, z=2.0
  - gamma=24.723, F=9.48e+00, z=3.4
  - gamma=33.137, F=7.43e+00, z=2.4
  - gamma=33.809, F=8.18e+00, z=2.8
  - gamma=39.371, F=1.08e+01, z=4.0
  - gamma=40.037, F=7.70e+00, z=2.5
  - ... (1 more)

### q=31, Method B
  - gamma=23.959, F=1.41e+04, z=3.9
  - gamma=24.459, F=1.39e+04, z=3.8
  - gamma=24.988, F=1.23e+04, z=3.3
  - gamma=32.388, F=1.17e+04, z=3.1
  - gamma=32.946, F=1.56e+04, z=4.4
  - gamma=33.515, F=1.07e+04, z=2.7
  - gamma=34.020, F=9.99e+03, z=2.5
  - gamma=39.332, F=1.10e+04, z=2.8
  - gamma=39.939, F=1.47e+04, z=4.1
  - gamma=40.522, F=1.05e+04, z=2.6
  - ... (1 more)

### q=37, Method A
  - gamma=2.132, F=6.66e+00, z=2.1
  - gamma=6.944, F=8.33e+00, z=2.9
  - gamma=8.106, F=9.77e+00, z=3.6
  - gamma=9.257, F=7.26e+00, z=2.4
  - gamma=19.661, F=8.57e+00, z=3.0
  - gamma=20.313, F=1.17e+01, z=4.6
  - gamma=27.223, F=7.75e+00, z=2.6
  - gamma=27.913, F=1.04e+01, z=3.9
  - gamma=36.744, F=6.85e+00, z=2.2
  - gamma=41.699, F=6.78e+00, z=2.1
  - ... (2 more)

### q=37, Method B
  - gamma=8.062, F=2.65e+04, z=4.0
  - gamma=9.042, F=1.75e+04, z=2.3
  - gamma=25.997, F=2.00e+04, z=2.7
  - gamma=27.036, F=2.35e+04, z=3.4
  - gamma=27.570, F=2.21e+04, z=3.1
  - gamma=28.124, F=1.68e+04, z=2.1
  - gamma=42.791, F=2.07e+04, z=2.9
  - gamma=43.321, F=2.37e+04, z=3.4
  - gamma=43.825, F=1.78e+04, z=2.3
  - gamma=45.786, F=1.62e+04, z=2.0
  - ... (3 more)

### q=41, Method A
  - gamma=4.646, F=6.94e+00, z=2.1
  - gamma=5.979, F=8.07e+00, z=2.7
  - gamma=7.150, F=8.80e+00, z=3.0
  - gamma=12.644, F=8.99e+00, z=3.1
  - gamma=13.286, F=9.29e+00, z=3.3
  - gamma=20.724, F=7.95e+00, z=2.6
  - gamma=21.891, F=7.93e+00, z=2.6
  - gamma=28.374, F=9.72e+00, z=3.5
  - gamma=38.768, F=1.09e+01, z=4.0
  - gamma=41.507, F=6.80e+00, z=2.1
  - ... (3 more)

### q=41, Method B
  - gamma=5.758, F=1.52e+04, z=2.9
  - gamma=21.871, F=1.38e+04, z=2.6
  - gamma=41.321, F=1.31e+04, z=2.4
  - gamma=43.477, F=1.53e+04, z=3.0
  - gamma=47.422, F=1.27e+04, z=2.3
  - gamma=47.956, F=1.35e+04, z=2.5
  - gamma=48.530, F=1.92e+04, z=4.0
  - gamma=49.069, F=1.99e+04, z=4.2

### q=43, Method A
  - gamma=16.192, F=6.76e+00, z=2.0
  - gamma=19.460, F=8.85e+00, z=3.0
  - gamma=27.585, F=9.07e+00, z=3.1
  - gamma=28.173, F=8.77e+00, z=3.0
  - gamma=34.715, F=9.35e+00, z=3.3
  - gamma=35.348, F=8.60e+00, z=2.9
  - gamma=44.835, F=1.19e+01, z=4.5
  - gamma=45.457, F=9.01e+00, z=3.1
  - gamma=47.515, F=7.00e+00, z=2.1

### q=43, Method B
  - gamma=36.827, F=6.56e+04, z=2.5
  - gamma=37.367, F=5.89e+04, z=2.1
  - gamma=37.906, F=6.93e+04, z=2.7
  - gamma=38.469, F=1.03e+05, z=4.6
  - gamma=39.008, F=6.98e+04, z=2.7
  - gamma=39.528, F=6.49e+04, z=2.4
  - gamma=40.037, F=7.65e+04, z=3.1
  - gamma=40.562, F=5.81e+04, z=2.1
  - gamma=44.364, F=6.72e+04, z=2.6
  - gamma=44.859, F=6.89e+04, z=2.7
  - ... (8 more)

### q=47, Method A
  - gamma=2.103, F=7.39e+00, z=2.2
  - gamma=3.744, F=7.30e+00, z=2.1
  - gamma=14.560, F=9.26e+00, z=3.0
  - gamma=15.167, F=1.17e+01, z=4.1
  - gamma=29.565, F=7.96e+00, z=2.4
  - gamma=30.535, F=7.64e+00, z=2.3
  - gamma=31.623, F=9.55e+00, z=3.2
  - gamma=32.187, F=1.31e+01, z=4.8
  - gamma=44.394, F=7.87e+00, z=2.4
  - gamma=46.442, F=9.74e+00, z=3.2
  - ... (1 more)

### q=47, Method B
  - gamma=3.783, F=1.13e+04, z=3.5
  - gamma=7.782, F=1.16e+04, z=3.7
  - gamma=30.864, F=8.78e+03, z=2.5
  - gamma=31.506, F=1.07e+04, z=3.3
  - gamma=42.365, F=1.08e+04, z=3.3
  - gamma=42.899, F=7.90e+03, z=2.2
  - gamma=43.355, F=7.98e+03, z=2.2
  - gamma=43.845, F=9.35e+03, z=2.8

### q=4, Method A
  - gamma=6.028, F=9.58e+00, z=4.5
  - gamma=10.208, F=6.33e+00, z=2.7
  - gamma=13.045, F=5.66e+00, z=2.3
  - gamma=16.290, F=6.27e+00, z=2.6
  - gamma=18.358, F=6.12e+00, z=2.5
  - gamma=21.366, F=5.27e+00, z=2.1
  - gamma=23.332, F=7.05e+00, z=3.1
  - gamma=25.738, F=5.76e+00, z=2.3
  - gamma=28.281, F=6.12e+00, z=2.5
  - gamma=29.771, F=6.59e+00, z=2.8
  - ... (5 more)

### q=4, Method B
  - gamma=6.072, F=1.88e+04, z=3.8
  - gamma=10.115, F=1.56e+04, z=3.0
  - gamma=13.021, F=1.32e+04, z=2.3
  - gamma=25.404, F=1.24e+04, z=2.1
  - gamma=28.315, F=1.35e+04, z=2.4
  - gamma=36.097, F=1.53e+04, z=2.9
  - gamma=36.597, F=1.28e+04, z=2.2
  - gamma=38.244, F=1.36e+04, z=2.4
  - gamma=40.356, F=1.59e+04, z=3.0
  - gamma=44.462, F=1.41e+04, z=2.5
  - ... (2 more)
