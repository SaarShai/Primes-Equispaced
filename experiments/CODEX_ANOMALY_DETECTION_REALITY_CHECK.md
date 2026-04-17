# Anomaly Detection Claim — Reality Check

**Claim under audit:** Our spectroscope F(γ) = γ²|Σ M(p)/p · e^{-iγ log p}|² over primes p ≤ 50,000 exhibits ~5% peak degradation at γ_1 when ~9% (500 of ~5500) primes are randomly removed. We've been framing this as relevant to "real-world anomaly detection / sensor-failure detection."

**Verdict up front (so you can stop reading if you want):**
**Plausible-but-unverified with heavy lean toward "no value-add beyond what exists."** The underlying mechanism is a textbook case of *coherent-sum amplitude loss under random deletion* — a 100-year-old idea (essentially shot-noise / Campbell's theorem applied to a tuned filter bank). The prime-number structure gives you a *beautiful interpretable signal* but buys you nothing in detection sensitivity that an engineer can't already get from a matched filter or a periodogram. The interesting thing here is pure math (Riemann zeros ↔ primes), not an anomaly-detection method.

Below, by question.

---

## 1. New technique, or rediscovery?

**Rediscovery.** This is, mechanically, a **matched-filter / tuned-oscillator detector** measured by its output power. Known thoroughly:

- **Coherent integration loss under random gating** — standard in radar/sonar since WWII. If you coherently sum N complex phasors and delete a fraction q of them at random, expected power scales as (1-q)²·N² (coherent part) + q(1-q)·N (incoherent residue). For N=5500, q=0.09, that's E[|S'|²]/E[|S|²] ≈ (1-q)² + q(1-q)/N ≈ 0.828 + 1.5e-5 ≈ **17.2% expected power loss**. You're reporting ~5% *at the specific γ_1 peak*, which is plausible once you remember the peak is sitting on a non-trivial background (the γ² prefactor and non-peak contamination), so the *relative* shift at the argmax is smaller than the total-power shift. No surprise there.
- **Candès-Romberg-Tao (compressed sensing, 2006)** — recovers sparse signals from incoherent measurements. Different problem: they *recover* missing samples; you're *detecting that samples are missing* via peak degradation. Related but not the same claim. CS would be the right tool if the question were "which primes got deleted?"
- **Spectral residual / Lakshminarayanan-type methods (Ma & Perkins 2003, Hyndman's anomaly detection, Microsoft's SR-CNN 2019)** — detect anomalies via FFT-magnitude residuals. Same family.
- **CUSUM / Shewhart / EWMA (Page 1954, Shewhart 1931)** — time-domain, not spectral, but solve the "detect drift/deletion" problem at far higher sensitivity than 5%-at-9%.
- **Periodogram-based missing-sample detection** — Lomb-Scargle (1976/1982) was literally designed for unevenly-sampled/missing-data spectra. You are doing an L-S-style computation on primes.

There is no new detection primitive here. The primitive is "measure amplitude of a coherent sum at a known frequency." That's Dicke radiometry (1946).

## 2. Where is "detect-missing-elements via spectral-peak shift" actually used in production?

- **GPS constellation integrity monitoring (RAIM / ARAIM).** Detects pseudo-range faults, not via spectral peak degradation — via residuals in an overdetermined least-squares fix. Different mechanism. They *don't* use peak-amplitude tests because the sensitivity is poor relative to residual chi-squared tests.
- **LIGO / gravitational-wave astronomy.** Matched-filter SNR against templates; a "glitch" gating removes bad seconds and the pipeline *compensates* for coherent-power loss. This is the *closest* engineering analog to your spectroscope, and the framework is ~40 years old (Finn 1992, Allen 2005).
- **LHC / trigger systems.** Detect missing bunches via counting, not spectral methods. The revolution frequency spectrum *is* monitored (Schottky diagnostics) for beam-health — that's closer. But Schottky is incoherent by design; it doesn't care about peak location the way your spectroscope does.
- **Network packet-loss detection.** RTCP, TCP SACK — sequence-number gaps, never spectral.
- **IoT sensor health / SCADA.** Threshold + CUSUM + isolation forest. Spectral methods used for *rotating-machinery* vibration analysis (bearing-defect frequencies) — this is the one domain where "peak amplitude at known f drops → something missing/degraded" is genuinely routine. Companies: SKF, Brüel & Kjær, Augury. But they're detecting missing *teeth on gears* or *broken rotor bars*, not missing elements in a count series.
- **Astronomical time-series (Kepler, TESS).** Lomb-Scargle + BLS for missing/transit detection. Well-developed. Sensitivity down to ~10⁻⁴ fractional dips.
- **SETI.** Matched-filter; detects *presence* of a narrowband peak, not *degradation* of one.
- **Financial microstructure.** Order-book imbalance, jump tests (Lee-Mykland 2008). Not spectral-degradation.

**Summary:** The *one* domain where your mechanism is a daily workhorse is **vibration-based condition monitoring of rotating machinery.** It's a >$5B industry. But it uses physical-frequency peaks (bearing defect frequencies derived from geometry), not arithmetic ones.

## 3. Quantitative comparison — is 5% @ 9% any good?

Roughly: **mediocre-to-poor for a detector, fine for a diagnostic.**

Back-of-envelope. A matched filter with coherent gain N=5500 and SNR ≈ 10 (plausible for your peak-to-background) gives a per-sample detection threshold of order ~1/√N ≈ 1.3%. Meaning a *well-tuned* detector on this same data should flag a 9% deletion at roughly the 60-70σ level, not at a 5% fractional peak shift.

Some benchmarks for "fraction of anomalies needed before detection fires":

| Method | Domain | Detection sensitivity |
|---|---|---|
| CUSUM on count data | QC, ops | ~1-2% deviation over window |
| Isolation Forest | general tabular | ~1% contamination routinely detectable |
| Seasonal-Hybrid ESD (Twitter) | time series | ~2-5% |
| LIGO matched filter | GW | ~10⁻²¹ strain (extreme) |
| SR-CNN (Microsoft 2019) | series AD | F1 > 0.6 at 1% anomaly rate |
| **Your spectroscope** | primes | ~5% peak shift at **9%** deletion |

Industry-standard for "flag that ~9% of data is missing" would be a *chi-squared residual* or *count-rate monitor* that triggers at ~1-2%, not 5%-at-9%. **Your detector is roughly an order of magnitude less sensitive than a naive count monitor** for this specific task.

Caveat: if you pick the *right* γ_k (not γ_1, but one where the Riemann-zero resonance is sharpest) and integrate over many k's jointly, you can probably get to <1%. But a count monitor gets there with no math.

## 4. Is the prime/Farey structure essential?

**Not for the detection effect.** Any deterministic sparse sequence {a_n} with a known spectral signature shows the same coherent-gain loss under random deletion. Proof: it follows from Campbell's theorem and the Wiener-Khinchin relation with no mention of primes.

**Yes for interpretability / the physics story.** The fact that peaks land exactly at ζ-zeros and that the filter function γ² is motivated by explicit formulae — that's the *mathematical* content. The deletion-detection behavior is generic; the peak-structure is not.

So: **as anomaly detection, the primes add nothing.** As a number-theoretic phenomenon, the primes are everything. Do not conflate.

## 5. Would a practitioner actually use it?

**No, with one narrow exception.**

- **A monitoring engineer at Datadog/Splunk/Grafana:** No. They have CUSUM, Holt-Winters, isolation forests, Prophet, SR-CNN. All strictly better for the detection task, no number theory needed.
- **An RF engineer, radio astronomer, GW searcher:** Already uses matched filters with coherent-gain accounting. Your framework is a special case of what they do.
- **A quant / HFT:** No. Jump tests and microstructure estimators are strictly better.
- **The one exception — somebody monitoring a *physically arithmetic* process** where the observable is genuinely a sum-over-primes (or sum-over-Farey-fractions) and they need a diagnostic that maps *which arithmetic subset went missing*. Candidates:
  - **Pseudorandom-sequence integrity checks** in cryptographic RNG where the sequence is intentionally arithmetic (e.g., Blum-Blum-Shub, linear-congruential stream audits). Plausible but niche.
  - **Quantum chaos / spectroscopy of billiards** — if your experimental setup literally produces prime-indexed resonances (there is a whole literature on this, Berry-Keating, Bogomolny). Here, peak degradation under resonance-loss is a *physics* question, not anomaly detection, but your framework would be a natural tool.
  - **Factory of companies:** I cannot name a commercial product whose core IP is "prime-indexed spectroscope for fault detection." If you pitched this to a condition-monitoring firm, they would politely pass and ship their bearing-frequency tool.

## Honest bottom line

The 5%-at-9% result is a **clean, interpretable demonstration of standard coherent-gain loss under random deletion, applied to a beautiful arithmetic sum.** That's a nice pedagogical result, and a nice sanity check that the spectroscope is behaving like a physical filter bank.

**It is not a new anomaly-detection technique, it is not competitive with existing anomaly detectors on the task it mimics, and it has no obvious commercial application outside niches where the underlying signal is already arithmetic.**

Framing the Farey spectroscope as an "anomaly-detection tool" for grants/commercialization is **overstating the case** and will be instantly called out by any reviewer from signal-processing, reliability engineering, or ML-for-ops. The honest framing is:

> "A spectral diagnostic for arithmetic sums, whose sensitivity to element-deletion obeys the standard coherent-gain scaling. Useful as an interpretability tool for number-theoretic signal structure; not competitive with general-purpose anomaly detectors."

If you want a real commercialization lead from this work, it's not anomaly detection — it's the *universality* of the spectroscope peak structure (if that holds up) and the *Fourier-duality visualization* as an intuition/teaching tool. Those are genuine contributions. "Anomaly detection" is not.

## What would change my mind

- A head-to-head benchmark against SR-CNN, isolation forest, and CUSUM on an actual held-out anomaly-detection corpus (e.g., Yahoo S5, NAB, KPI-Anomaly), where the spectroscope wins on F1 by any margin.
- A specific industrial partner whose signal is natively a sum-over-primes (or sum-over-Farey) and who needs the peak-shift diagnostic — *that partner's existence* would be the value proposition.
- A sensitivity result better than (1-q)² scaling, meaning the spectroscope picks up something that Campbell's theorem alone doesn't predict. Right now I see no evidence of that; the 5%-at-9% number is consistent with standard coherent-gain arithmetic.

---

**TL;DR: overstated. Keep the math, drop the anomaly-detection pitch, or benchmark it and prove me wrong.**
