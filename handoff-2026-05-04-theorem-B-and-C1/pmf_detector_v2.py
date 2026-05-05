"""
PrimeMatchedFilterDetectorV2
============================

Extends pmf_detector.PrimeMatchedFilterDetector with:
  - Larger n_taps (caller responsibility; class supports any n_taps >= 1)
  - Optional prefilter:
      * None         -> raw signal (default, original behavior)
      * 'ar1_residual' -> x[i] - rho_hat * x[i-1] before matched filter
      * 'highpass'   -> first difference x[i] - x[i-1]
  - Caches prime weights across calls with same (n_taps, weighting).

Salvage attempt for AR(1) + planted-spike benchmark where the original
17-tap PMF lost badly to OneClassSVM. Hypothesis: longer kernels + AR(1)
residualization should help when the noise is colored (low-pass).
"""

from __future__ import annotations

import numpy as np
from typing import Optional, Sequence

from pmf_detector import (
    _build_prime_weights,
    _matched_filter_response,
    _rolling_mean_std,
)


# --- Prefilters --------------------------------------------------------------

def _prefilter(x: np.ndarray, kind: Optional[str]) -> np.ndarray:
    """Apply optional prefilter. Returns same length as input."""
    if kind is None or kind == "none":
        return x
    if kind == "ar1_residual":
        # Estimate AR(1) coefficient by lag-1 OLS (Yule-Walker simplest form)
        if x.size < 3:
            return x
        x0 = x[:-1]
        x1 = x[1:]
        denom = float(np.dot(x0, x0))
        rho = float(np.dot(x0, x1) / denom) if denom > 1e-12 else 0.0
        # clip to stability range
        rho = max(min(rho, 0.999), -0.999)
        out = np.empty_like(x)
        out[0] = x[0]
        out[1:] = x[1:] - rho * x[:-1]
        return out
    if kind == "highpass":
        out = np.empty_like(x)
        out[0] = x[0]
        out[1:] = x[1:] - x[:-1]
        return out
    raise ValueError(f"Unknown prefilter: {kind!r}")


# --- Detector ---------------------------------------------------------------

class PrimeMatchedFilterDetectorV2:
    """PMF detector with prefilter and configurable n_taps.

    Parameters
    ----------
    n_taps : int
        Kernel length.
    window_size : int
        Local z-score window.
    weighting : {'M_over_sqrt_p', 'R_p'}
    prefilter : {None, 'ar1_residual', 'highpass'}
    threshold : float
    """

    def __init__(
        self,
        n_taps: int = 17,
        window_size: int = 100,
        weighting: str = "M_over_sqrt_p",
        prefilter: Optional[str] = None,
        threshold: float = 3.0,
        prime_subset: Optional[Sequence[int]] = None,
    ) -> None:
        self.n_taps = n_taps
        self.window_size = window_size
        self.weighting = weighting
        self.prefilter = prefilter
        self.threshold = threshold
        self.prime_subset = prime_subset

        self._weights: Optional[np.ndarray] = None
        self._gamma2: Optional[np.ndarray] = None
        self._mu: Optional[np.ndarray] = None
        self._sigma: Optional[np.ndarray] = None

    def fit(self, x: np.ndarray) -> "PrimeMatchedFilterDetectorV2":
        x = np.asarray(x, dtype=np.float64).ravel()
        x_pref = _prefilter(x, self.prefilter)
        self._weights = _build_prime_weights(
            self.n_taps, self.weighting, self.prime_subset
        )
        y = _matched_filter_response(x_pref, self._weights)
        self._gamma2 = y * y
        # adapt window if signal is short
        win = min(self.window_size, max(8, x.size // 4))
        self._mu, self._sigma = _rolling_mean_std(self._gamma2, win)
        return self

    def score(self, x: Optional[np.ndarray] = None) -> np.ndarray:
        if x is not None:
            self.fit(x)
        eps = 1e-12
        return (self._gamma2 - self._mu) / np.maximum(self._sigma, eps)


__all__ = ["PrimeMatchedFilterDetectorV2", "_prefilter"]
