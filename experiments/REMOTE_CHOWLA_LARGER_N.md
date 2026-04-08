## Summary
Sieving $\mu(n)$ to $10M$ costs negligible time (milliseconds). Spectroscope evaluation requires FFT-based convolution to bypass $O(N \cdot G)$ bottleneck.

## Analysis
| Method | Complexity | Ops | Notes |
| :--- | :--- | :--- | :--- |
| Naive Sum | $O(N \cdot G)$ | $1.5 \cdot 10^{11}$ | Prohibitively slow |
| Prime Subset | $O(\pi(N) \cdot G)$ | $\approx 10^{10}$ | Reduces $N$ by factor 16 |
| FFT Conv | $O(N \log N)$ | $\approx 2 \cdot 10^8$ | Optimal for spectral |
| Chunked | $O(N \cdot G/P)$ | $1.5 \cdot 10^{10}/P$ | Parallelizable |

## Verdict/Next Steps
1. Deploy FFT-based spectroscope.
2. Parallelize chunks across available cores.
3. Validate prime-subset results against full set for $N=1M$ calibration.
4. Target $\epsilon < 0.0005$ at $N=10M$.
