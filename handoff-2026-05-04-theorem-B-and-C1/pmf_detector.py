"""
PrimeMatchedFilterDetector
==========================

Structure-aware 1D anomaly detector. Combines a matched filter using a
prime-weighted kernel with a local (rolling) z-score.

Design choices (documented per spec):
    * Kernel: γ²(x)[n] = (Σ_k w_k * x[n + k - K//2])²    (squared response)
    * Weights w_k for k in 1..K:
        - 'M_over_sqrt_p':  w_k = M(p_k) / sqrt(p_k)
            where p_k is the k-th prime and M is the Mertens function
            M(n) = Σ_{i<=n} μ(i). This is the program's primary kernel.
        - 'R_p': w_k = 1/sqrt(p_k)               (baseline ablation)
    * Padding: zero-pad outside [0, N).
    * Local mean μ_W and std σ_W computed via uniform rolling window of
      size `window_size` on γ²(x). Centred window. Edges use the available
      partial window (no NaNs).
    * z[n] = (γ²(x)[n] - μ_W[n]) / max(σ_W[n], eps)
    * Prediction: |z| >= threshold
    * 'gamma_squared' is currently the only kernel; the parameter is kept
      for forward compatibility.

Dependencies: numpy, scipy.
"""

from __future__ import annotations

import numpy as np
from typing import Optional, Sequence


# ---------------------------------------------------------------------------
# Number-theoretic helpers (small, no mpmath needed at the scales we use)
# ---------------------------------------------------------------------------

def _sieve_primes(limit: int) -> np.ndarray:
    """Sieve of Eratosthenes; returns primes <= limit."""
    if limit < 2:
        return np.array([], dtype=np.int64)
    is_prime = np.ones(limit + 1, dtype=bool)
    is_prime[:2] = False
    for i in range(2, int(limit**0.5) + 1):
        if is_prime[i]:
            is_prime[i * i :: i] = False
    return np.nonzero(is_prime)[0].astype(np.int64)


def _first_n_primes(n: int) -> np.ndarray:
    """Return the first n primes."""
    if n <= 0:
        return np.array([], dtype=np.int64)
    # Upper bound (Rosser): p_n < n (ln n + ln ln n) for n >= 6
    if n < 6:
        limit = 15
    else:
        limit = int(n * (np.log(n) + np.log(np.log(n)))) + 10
    primes = _sieve_primes(limit)
    while primes.size < n:
        limit *= 2
        primes = _sieve_primes(limit)
    return primes[:n]


def _mobius(limit: int) -> np.ndarray:
    """Möbius function values μ(1..limit) using a linear sieve-ish approach."""
    mu = np.ones(limit + 1, dtype=np.int8)
    mu[0] = 0
    primes = _sieve_primes(limit)
    for p in primes:
        # multiples of p: flip sign
        mu[p :: p] *= -1
        # multiples of p^2: zero
        p2 = p * p
        if p2 <= limit:
            mu[p2 :: p2] = 0
    return mu


def _mertens(limit: int) -> np.ndarray:
    """Mertens function M(0..limit) = cumulative sum of Möbius."""
    mu = _mobius(limit).astype(np.int64)
    return np.cumsum(mu)


# ---------------------------------------------------------------------------
# Rolling window stats
# ---------------------------------------------------------------------------

def _rolling_mean_std(x: np.ndarray, window: int) -> tuple[np.ndarray, np.ndarray]:
    """Centred rolling mean and std with edge truncation (no NaNs)."""
    n = x.size
    if window < 2:
        return x.copy(), np.zeros_like(x)
    # Use cumulative sums for O(N) computation
    cs = np.concatenate(([0.0], np.cumsum(x)))
    cs2 = np.concatenate(([0.0], np.cumsum(x * x)))
    half = window // 2
    starts = np.maximum(0, np.arange(n) - half)
    ends = np.minimum(n, np.arange(n) + (window - half))
    counts = (ends - starts).astype(np.float64)
    sums = cs[ends] - cs[starts]
    sums2 = cs2[ends] - cs2[starts]
    means = sums / counts
    var = sums2 / counts - means * means
    var = np.maximum(var, 0.0)
    return means, np.sqrt(var)


# ---------------------------------------------------------------------------
# Kernel construction
# ---------------------------------------------------------------------------

def _build_prime_weights(
    n_taps: int,
    weighting: str,
    prime_subset: Optional[Sequence[int]] = None,
) -> np.ndarray:
    """Return a length-`n_taps` weight vector.

    If `prime_subset` is given it overrides `n_taps` (uses len(prime_subset)).
    """
    if prime_subset is not None:
        primes = np.asarray(prime_subset, dtype=np.int64)
    else:
        primes = _first_n_primes(n_taps)

    if weighting == "M_over_sqrt_p":
        max_p = int(primes.max())
        M = _mertens(max_p)
        w = M[primes].astype(np.float64) / np.sqrt(primes.astype(np.float64))
    elif weighting == "R_p":
        # baseline: 1 / sqrt(p)
        w = 1.0 / np.sqrt(primes.astype(np.float64))
    else:
        raise ValueError(f"Unknown weighting: {weighting!r}")

    # Normalise so kernel has unit L2 (scale-invariance for thresholding)
    norm = np.linalg.norm(w)
    if norm > 0:
        w = w / norm
    return w


def _matched_filter_response(x: np.ndarray, w: np.ndarray) -> np.ndarray:
    """Linear matched filter response, centred. Output length == x length.
    Uses scipy.signal.fftconvolve when beneficial.
    """
    from scipy.signal import fftconvolve

    # Zero-pad equivalent: 'same' mode of convolution with reversed kernel
    # gives a correlation. We want correlation (matched filter), so flip.
    kernel = w[::-1]
    y = fftconvolve(x, kernel, mode="same")
    return y


# ---------------------------------------------------------------------------
# Detector
# ---------------------------------------------------------------------------

class PrimeMatchedFilterDetector:
    """Anomaly detector using a prime-weighted matched filter + local z-score.

    Parameters
    ----------
    prime_subset : sequence of ints, optional
        If supplied, use these primes for the kernel. Otherwise the first
        `n_taps` primes are used.
    n_taps : int
        Kernel length (number of primes). Default 17.
    window_size : int
        Local z-score window (samples). Default 100.
    threshold : float
        |z|-score threshold for predict(). Default 3.0.
    weighting : {'M_over_sqrt_p', 'R_p'}
        Weight scheme. 'M_over_sqrt_p' is the program's primary kernel.
    kernel : {'gamma_squared'}
        Detector statistic. Currently only 'gamma_squared' (γ² = filter
        response squared, i.e. an energy detector after matched filtering).
    """

    def __init__(
        self,
        prime_subset: Optional[Sequence[int]] = None,
        n_taps: int = 17,
        window_size: int = 100,
        threshold: float = 3.0,
        weighting: str = "M_over_sqrt_p",
        kernel: str = "gamma_squared",
    ) -> None:
        if kernel != "gamma_squared":
            raise ValueError("Only 'gamma_squared' kernel is implemented.")
        self.prime_subset = prime_subset
        self.n_taps = n_taps
        self.window_size = window_size
        self.threshold = threshold
        self.weighting = weighting
        self.kernel = kernel

        self._weights: Optional[np.ndarray] = None
        self._gamma2: Optional[np.ndarray] = None
        self._mu: Optional[np.ndarray] = None
        self._sigma: Optional[np.ndarray] = None

    # ---- API ------------------------------------------------------------
    def fit(self, x: np.ndarray) -> "PrimeMatchedFilterDetector":
        x = np.asarray(x, dtype=np.float64).ravel()
        self._weights = _build_prime_weights(
            self.n_taps, self.weighting, self.prime_subset
        )
        # Matched filter response, then square (energy / "γ²")
        y = _matched_filter_response(x, self._weights)
        self._gamma2 = y * y
        self._mu, self._sigma = _rolling_mean_std(self._gamma2, self.window_size)
        return self

    def score(self, x: Optional[np.ndarray] = None) -> np.ndarray:
        """Return local |z|-scores. If x is None, returns scores from fit."""
        if x is not None:
            self.fit(x)
        eps = 1e-12
        z = (self._gamma2 - self._mu) / np.maximum(self._sigma, eps)
        return z  # signed; callers usually want abs

    def predict(
        self,
        x: Optional[np.ndarray] = None,
        threshold: Optional[float] = None,
    ) -> np.ndarray:
        """Binary anomaly labels (1 = anomaly, 0 = normal)."""
        z = self.score(x)
        thr = self.threshold if threshold is None else threshold
        return (np.abs(z) >= thr).astype(np.int8)

    def fit_predict(
        self, x: np.ndarray, threshold: Optional[float] = None
    ) -> np.ndarray:
        return self.fit(x).predict(threshold=threshold)


__all__ = ["PrimeMatchedFilterDetector"]
