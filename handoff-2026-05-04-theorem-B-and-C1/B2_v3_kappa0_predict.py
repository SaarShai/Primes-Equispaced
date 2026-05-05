#!/usr/bin/env python3
"""Compute Soshnikov-Palm prediction at κ=0, compare to MC."""
import numpy as np
from scipy.integrate import quad, dblquad

def MW(y):
    w = 1j*y
    return (1 - np.exp(-1 - w))/(1 + w)

def sinc(x):
    return np.sinc(x)  # sin(πx)/(πx)

# Test function at κ=0 is f(y) = M_W(iy)
# Palm-conditioned variance for sine-kernel det. process at the eigenvalue at 0:
#  Var_Palm( Σ_{j≠0} f(y_j) )
#  = ∫|f|²(1-sinc²(πy))dy
#    - ∫∫ f(y)f̄(y') sinc²(π(y-y')) dy dy'
#    + |∫ f(y) sinc(πy) dy|²
#
# (The +|∫f·sinc|² is the Palm correction from y'=0 in the conditional kernel.)
#
# At high κ, the off-diagonal double integral and the |∫f·sinc|² both vanish
# by destructive oscillation, leaving I_ON.
# At κ=0, all three terms survive.

# Fourier-side: parseval for sine-kernel projection.
# Var(Σf) (unconditional) = ∫ |f̂(ξ)|² · K_*(ξ) dξ   where K_* is the
# eigenvalue-process Fourier kernel. For determinantal sine-kernel:
#   Var(Σf) = ∫|f̂|²(ξ) · min(|ξ|,1) dξ      (Soshnikov 2000 Eq. (1.5)/Thm 1)
# (sine-kernel is a projection, so Var = ⟨f,(K-K²)f⟩ = ⟨f̂,(|ξ|·𝟙_|ξ|≤1)f̂⟩ ext.)

# Precompute integrals.
I_naive, _ = quad(lambda y: abs(MW(y))**2,                       -500, 500, limit=800)
I_ON,    _ = quad(lambda y: abs(MW(y))**2*(1-sinc(y)**2),         -500, 500, limit=800)

# ∫ M_W(iy) sinc(πy) dy   (used for Palm correction term)
J_re, _ = quad(lambda y: MW(y).real * np.sinc(y), -500, 500, limit=800)
J_im, _ = quad(lambda y: MW(y).imag * np.sinc(y), -500, 500, limit=800)
J = complex(J_re, J_im)
print(f"∫|M_W|²       = {I_naive:.4f}")
print(f"∫|M_W|²(1-s²) = {I_ON:.4f}")
print(f"∫M_W·sinc dy  = {J}    |J|² = {abs(J)**2:.4f}")
print()

# Soshnikov full Palm variance at κ=0:
# Two equivalent forms:
#  (A) "off-diagonal" form
#      Var_Palm = ∫|f|²(1-s²) - ∫∫f f̄' s² + |∫f·s|²
#  (B) Fourier form (Soshnikov 2000 Thm 1 + Palm shift)
#      Var_Palm = ∫|f̂|² · g(ξ) dξ
# We'll use (A) directly via numerical 2D integration.

# Bourgade-Nikeghbali Palm formula for sine-kernel:
#   K_Palm(y,y') = sinc(π(y-y')) - sinc(πy)·sinc(πy')   [reduced kernel after Palm at 0]
# Then Var_Palm(Σ_{j≠0} f) = ∫|f|² K_P(y,y) dy − ∫∫ f f̄' |K_P(y,y')|² dy dy' + |∫f·K_P(0,·)|²
# K_P(y,y) = 1 − sinc²(πy) ✓
# But the unconditional-style formula simplifies further:
#   Var_Palm = ∫|f|²(1−sinc²) − ∫∫ f f̄' [sinc(π(y-y')) − sinc(πy)sinc(πy')]² dy dy'

def integrand_re(y, yp):
    fy = MW(y); fp = MW(yp)
    KP = sinc(y - yp) - sinc(y)*sinc(yp)
    return (fy * np.conj(fp) * KP**2).real

LIM = 25.0
D_re, _ = dblquad(integrand_re, -LIM, LIM, lambda y: -LIM, lambda y: LIM,
                   epsabs=1e-4, epsrel=1e-4)
print(f"∫∫ f·f̄'·K_Palm² dy dy' = {D_re:+.4f}")
print()

Var_pred = I_ON - D_re
print(f"Predicted Var_Palm(S; κ=0) = ∫|f|²(1−sinc²) − ∫∫f·f̄'·K_Palm²")
print(f"                          = {I_ON:.4f} − {D_re:.4f}")
print(f"                          = {Var_pred:.4f}")
print()

# Compare to MC:
print(f"MC at κ=0, N=250: Var(S) = 0.1397   (from B2_v3_kappa0.out)")
print(f"Predicted:               = {Var_pred:.4f}")
print(f"Ratio MC/pred           = {0.1397/Var_pred:.4f}")
