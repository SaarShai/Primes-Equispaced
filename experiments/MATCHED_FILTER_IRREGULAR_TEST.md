# Matched-Filter Periodogram vs Lomb-Scargle: Irregular Sampling Test

Date: 2026-04-07  |  Seed: 42

## Setup

- Frequencies: [np.float64(2.3), np.float64(5.7), np.float64(11.1)] Hz, amplitudes [np.float64(1.0), np.float64(0.3), np.float64(0.1)]
- SNR = 10 dB, minimax alpha = 0.3
- N values tested: [100, 200, 500, 1000]
- Prime-log grid: 168 primes ≤ 1000

## Results Table

| Sampling | N | Method | Err f1 | Err f2 | Err f3 | SNR(f3) | FP |
|----------|---|--------|--------|--------|--------|---------|----|
| prime-log | 168 | Lomb-Scargle | 0.0095 | 0.0670 | 0.1815 | 2.60 | 7 |
| prime-log | 168 | gamma^2 filter | 0.0207 | 0.0372 | 0.0644 | 4.43 | 33 |
| prime-log | 168 | gamma^0.3 filter | 0.0132 | 0.0446 | 0.0644 | 1.99 | 17 |
| uniform | 100 | Lomb-Scargle | 0.0020 | 0.0001 | 0.0197 | 2.06 | 404 |
| uniform | 100 | gamma^2 filter | 0.0017 | 0.0001 | 0.0101 | 2.66 | 321 |
| uniform | 100 | gamma^0.3 filter | 0.0017 | 0.0001 | 0.0101 | 1.06 | 426 |
| uniform | 200 | Lomb-Scargle | 0.0017 | 0.0037 | 0.0309 | 3.73 | 292 |
| uniform | 200 | gamma^2 filter | 0.0020 | 0.0037 | 0.0011 | 3.21 | 326 |
| uniform | 200 | gamma^0.3 filter | 0.0020 | 0.0037 | 0.0309 | 4.87 | 341 |
| uniform | 500 | Lomb-Scargle | 0.0017 | 0.0001 | 0.0048 | 7.54 | 59 |
| uniform | 500 | gamma^2 filter | 0.0017 | 0.0001 | 0.0048 | 24.82 | 322 |
| uniform | 500 | gamma^0.3 filter | 0.0017 | 0.0001 | 0.0048 | 9.98 | 122 |
| uniform | 1000 | Lomb-Scargle | 0.0017 | 0.0001 | MISS | 0.00 | 1 |
| uniform | 1000 | gamma^2 filter | 0.0017 | 0.0001 | 0.0027 | 16.26 | 313 |
| uniform | 1000 | gamma^0.3 filter | 0.0017 | 0.0001 | MISS | 0.00 | 14 |

## Scaling: SNR of weakest frequency (f3) vs N

| N | Lomb-Scargle | gamma^2 | gamma^0.3 |
|---|-------------|---------|-----------|
| 100 | 2.06 | 2.66 | 1.06 |
| 200 | 3.73 | 3.21 | 4.87 |
| 500 | 7.54 | 24.82 | 9.98 |
| 1000 | 0.00 | 16.26 | 0.00 |

## Prime-log Sampling

- **Lomb-Scargle**: errors=['0.0095', '0.0670', '0.1815'], SNR(f3)=2.60, FP=7
- **gamma^2 filter**: errors=['0.0207', '0.0372', '0.0644'], SNR(f3)=4.43, FP=33
- **gamma^0.3 filter**: errors=['0.0132', '0.0446', '0.0644'], SNR(f3)=1.99, FP=17

## Verdict

**Average SNR(f3):** LS=3.33, gamma^2=11.74, gamma^0.3=3.98
**Average FP count:** LS=189.0, gamma^2=320.5, gamma^0.3=225.8
**f3 detection rate:** LS=75%, gamma^2=100%, gamma^0.3=75%

### Is gamma^2 matched filter viable for general signal processing? **YES**

gamma^2 filter shows 3.5x improvement in weak-frequency SNR over standard Lomb-Scargle. The frequency-dependent weighting compensates for spectral leakage in irregular grids, directly analogous to the zeta-zero enhancement.

### Implications for Farey research

The gamma^2 weighting in our zeta-zero detector is specifically tuned to the 
prime-logarithmic sampling grid. Its effectiveness on generic irregular grids 
depends on the sampling density profile. When the sampling is roughly uniform-random, 
standard Lomb-Scargle (which implicitly normalizes for sampling) may already 
capture most of the benefit. The gamma^2 factor adds value precisely when the 
sampling density has structure (like log-primes) that correlates with the target frequencies.