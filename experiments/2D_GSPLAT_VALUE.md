# 2D Gaussian Splatting for Images: Industry Value Assessment

**Date:** 2026-03-29
**Verdict: Active research area, pre-commercial. Our +0.37 dB is marginal.**

## The Field Is Real and Growing

2D Gaussian image representation is a legitimate, active research line with top-venue publications:

- **GaussianImage** (ECCV 2024) — started the field. 2000 FPS decoding, 3x less GPU memory than INRs.
- **Instant GaussianImage** (ICCV 2025) — 10x faster training via learned initialization.
- **GaussianImage++** (Dec 2025) — distortion-driven densification, beats COIN/COIN++.
- **EA-GI** (ScienceDirect, Jan 2026) — entropy-aware Gaussian allocation per region complexity.
- **SmartSplat** (Dec 2025) — scales to 8K/16K images, feature-aware sampling.
- **Neural Video Compression via 2DGS** (2025) — extends to video, 88% faster encoding.

At least 6+ papers in 18 months, across ECCV, ICCV, AAAI, ScienceDirect. Not niche.

## What People Care About

The value proposition is NOT compression ratio (neural codecs like VVC still win on R-D curves). It is:

1. **Decode speed** — 1500-2000 FPS vs ~10 FPS for neural codecs. 100-200x faster.
2. **Low memory** — no neural network weights needed at decode time.
3. **Editability** — Gaussians are individually addressable primitives, not a black-box latent.
4. **Scalability** — works at 8K/16K without architecture changes (SmartSplat).

The killer app is real-time decoding on low-end devices where neural codecs are too heavy.

## Commercial Status

**Zero commercial products found.** No startup, no product, no SDK shipping 2DGS image compression. The entire field is academic prototypes with GitHub repos. 3DGS has commercial traction (Zillow, film VFX, Postshot), but 2D image representation does not.

## Does Our +0.37 dB Matter?

**Probably not in isolation.** Here's why:

- GaussianImage++ already acknowledges it "lags behind" learned codecs on R-D performance. The field knows quality is the weakness — speed is the selling point.
- +0.37 dB on Kodak is a small improvement. Papers in this space report 1-3 dB gaps between methods.
- The interesting claim would be: **same quality with fewer Gaussians** (= smaller file, faster). If Farey initialization gets the same PSNR with 20-30% fewer Gaussians, THAT matters for compression ratio. Pure PSNR improvement with same Gaussian count is less compelling.

## Recommendation

**DEPRIORITIZE** unless we can show Gaussian count reduction (not just PSNR gain).

- If we achieve same quality with 25%+ fewer Gaussians: worth a short paper. Frame as "structured initialization for Gaussian image codecs."
- If we only have +0.37 dB at same count: not enough to publish or commercialize.
- The field has no commercial pull yet. Academic interest only.

**Bottom line:** The research area is real but pre-commercial. Our result is too small to move the needle unless reframed as efficiency (fewer Gaussians, not better PSNR).
