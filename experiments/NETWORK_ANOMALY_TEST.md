# Network Anomaly Detection: f^2 Spectral Compensation vs Lomb-Scargle

**Date:** 2026-04-07 21:23:02

**Simulation Parameters:**
- Background packets: 10000 (Poisson, mean 0.1s inter-arrival)
- Botnet C2: 50 packets every 30s (f = 0.033 Hz)
- DDoS pulses: 20 packets every 5s for 100s (f = 0.2 Hz)

## Results Table

| Jitter (s) | Method | Botnet SNR (dB) | DDoS SNR (dB) |
|-----------|--------|----------------|---------------|
| 0          | LS     | inf                | inf                |
| 0          | f^2 Comp| -6.79              | 18.64              |
| 1          | LS     | inf                | inf                |
| 1          | f^2 Comp| -12.13             | 17.75              |
| 3          | LS     | inf                | inf                |
| 3          | f^2 Comp| -16.15             | 16.80              |
| 5          | LS     | inf                | inf                |
| 5          | f^2 Comp| -12.93             | 15.72              |

## Conclusion

**Jitter = 0s:** Lomb-Scargle performs better for botnet detection. SNR improvement: inf dB

**Jitter = 1s:** Lomb-Scargle performs better for botnet detection. SNR improvement: inf dB

**Jitter = 3s:** Lomb-Scargle performs better for botnet detection. SNR improvement: inf dB

**Jitter = 5s:** Lomb-Scargle performs better for botnet detection. SNR improvement: inf dB

