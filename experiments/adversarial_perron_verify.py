#!/usr/bin/env python3
"""
ADVERSARIAL VERIFICATION of Perron integral derivation for T(N).
Independent computation -- no shared code with original script.

Checks:
1. Residue at s=0 (double pole)
2. Residues at zeta zeros c_k = zeta(rho_k+1)/(rho_k * zeta'(rho_k))
3. arg(c_1) and |c_1|
4. d_1 = 1/(rho_1 * zeta'(rho_1)) and its properties
5. Phase prediction: gamma_1*log(2) - arg(d_1) vs 5.208
6. Rubinstein-Sarnak P(T>0) at N=10^7
7. Cross-check: direct brute-force computation of F(N) vs Perron prediction
"""

from mpmath import (mp, mpf, mpc, zeta, zetazero, euler, log, pi, arg,
                     fabs, cos, sin, sqrt, re, im, j0, quad, inf, exp,
                     diff, gamma as mpgamma, power)
import sys

mp.dps = 50  # 50 digits of precision

print("="*70)
print("ADVERSARIAL VERIFICATION OF PERRON INTEGRAL T(N)")
print("="*70)

errors = []
warnings = []

# ============================================================
# CHECK 1: Basic constants
# ============================================================
print("\n--- CHECK 1: Basic constants ---")

gamma_em = euler
zeta_0 = zeta(0)
zetaprime_0 = -log(2*pi)/2  # known value

print(f"  gamma (Euler) = {gamma_em}")
print(f"  zeta(0) = {zeta_0}")
print(f"  zeta'(0) = {zetaprime_0}")
print(f"  zeta'(0) numerical = {diff(zeta, 0)}")

# Verify zeta(0) = -1/2
assert abs(zeta_0 + mpf('0.5')) < 1e-40, "zeta(0) != -1/2"
print("  [OK] zeta(0) = -1/2")

# Verify zeta'(0) = -log(2pi)/2
zetaprime_0_num = diff(zeta, 0)
assert abs(zetaprime_0 - zetaprime_0_num) < 1e-30, f"zeta'(0) mismatch: {zetaprime_0} vs {zetaprime_0_num}"
print(f"  [OK] zeta'(0) = -log(2pi)/2 = {float(zetaprime_0):.10f}")

# ============================================================
# CHECK 2: 1/zeta(s) expansion near s=0
# ============================================================
print("\n--- CHECK 2: 1/zeta(s) expansion near s=0 ---")

# 1/zeta(s) = -2 + c1*s + ...
# c1 = -zeta'(0)/zeta(0)^2 = -(−log(2pi)/2)/(1/4) = 2*log(2pi)
c1_theory = 2*log(2*pi)
print(f"  c1 (theory) = 2*log(2pi) = {float(c1_theory):.10f}")
print(f"  Document claims c1 = 3.6758. We get: {float(c1_theory):.4f}")

# Verify numerically: (1/zeta(h) - (-2))/h for small h
h = mpf('1e-15')
c1_numerical = (1/zeta(h) - (-2)) / h
print(f"  c1 (numerical, h=1e-15) = {float(re(c1_numerical)):.10f}")
assert abs(c1_theory - re(c1_numerical)) < 1e-5, f"c1 mismatch"
print("  [OK] c1 = 2*log(2pi) confirmed")

# IMPORTANT: check the sign. The document says 1/zeta(s) = -2 + 2*log(2pi)*s + ...
# Actually: 1/zeta(s) near s=0. zeta(s) = zeta(0) + zeta'(0)*s + ...
# 1/zeta(s) = 1/(zeta(0)(1 + zeta'(0)/zeta(0) * s + ...))
# = (1/zeta(0)) * (1 - zeta'(0)/zeta(0) * s + ...)
# = -2 * (1 - zeta'(0)/zeta(0) * s + ...)
# = -2 - 2*(-zeta'(0)/zeta(0))*s + ...   wait let me redo
# = -2 * (1 - zeta'(0)/zeta(0) * s)
# = -2 + 2*zeta'(0)/zeta(0) * s  ... NO: -2 * (-zeta'(0)/zeta(0)*s) = +2*zeta'(0)/zeta(0)*s

# zeta'(0)/zeta(0) = (-log(2pi)/2) / (-1/2) = log(2pi)
# So 1/zeta(s) = -2 + 2*zeta'(0)/zeta(0)*s = ... wait

# Let f(s) = 1/zeta(s). f(0) = 1/zeta(0) = -2.
# f'(0) = -zeta'(0)/zeta(0)^2 = -(-log(2pi)/2)/(1/4) = 2*log(2pi)
# So 1/zeta(s) = -2 + 2*log(2pi)*s + O(s^2). Document is CORRECT.

fprime_0 = -zetaprime_0 / zeta_0**2
print(f"  f'(0) = -zeta'(0)/zeta(0)^2 = {float(fprime_0):.10f}")
assert abs(fprime_0 - c1_theory) < 1e-30
print("  [OK] 1/zeta(s) = -2 + 2*log(2pi)*s + ... confirmed")

# ============================================================
# CHECK 3: Residue at s=0
# ============================================================
print("\n--- CHECK 3: Residue at s=0 ---")

# F(s) = N^s * zeta(s+1) / (s * zeta(s))
# Residue = -2*(logN + gamma) + 2*log(2pi)

# Verify numerically by contour integration around s=0
# Res = (1/2pi*i) * oint F(s) ds
# Use a small circle of radius r around s=0

def compute_residue_s0_numerically(N, r=mpf('0.001')):
    """Compute residue at s=0 by numerical contour integration."""
    def integrand(t):
        s = r * exp(mpc(0, 1) * t)
        ds_dt = mpc(0, 1) * r * exp(mpc(0, 1) * t)
        val = power(N, s) * zeta(s + 1) / (s * zeta(s)) * ds_dt
        return val

    result = quad(integrand, [0, 2*pi])
    return result / (2 * pi * mpc(0, 1))

def residue_formula(N):
    return -2*(log(N) + gamma_em) + 2*log(2*pi)

for N_val in [1000, 243798, 10**7]:
    res_formula = residue_formula(N_val)
    res_numerical = compute_residue_s0_numerically(N_val, r=mpf('0.0001'))
    diff_val = abs(res_formula - re(res_numerical))
    status = "[OK]" if diff_val < 0.01 else "[FAIL]"
    print(f"  N={N_val}: formula={float(res_formula):.4f}, numerical={float(re(res_numerical)):.4f}, diff={float(diff_val):.6f} {status}")
    if diff_val >= 0.01:
        errors.append(f"Residue at s=0 for N={N_val}: formula gives {float(res_formula):.4f} but numerical gives {float(re(res_numerical)):.4f}")

# Check document's specific values
res_1000 = residue_formula(1000)
res_243798 = residue_formula(243798)
res_1e7 = residue_formula(10**7)
print(f"\n  Document claims for N=1000: -11.294. We get: {float(res_1000):.3f}")
print(f"  Document claims for N=243798: -22.287. We get: {float(res_243798):.3f}")
print(f"  Document claims for N=10^7: -29.728. We get: {float(res_1e7):.3f}")

# ============================================================
# CHECK 4: Residues at zeta zeros
# ============================================================
print("\n--- CHECK 4: Residues at zeta zeros ---")

# c_k = zeta(rho_k + 1) / (rho_k * zeta'(rho_k))
# where rho_k = 1/2 + i*gamma_k

for k in range(1, 11):
    rho_k = zetazero(k)
    gamma_k = im(rho_k)

    # Compute c_k
    zeta_rho_plus_1 = zeta(rho_k + 1)
    zetaprime_rho = diff(zeta, rho_k)
    c_k = zeta_rho_plus_1 / (rho_k * zetaprime_rho)

    abs_ck = fabs(c_k)
    arg_ck = arg(c_k)

    print(f"  k={k:2d}: gamma={float(gamma_k):.4f}, |c_k|={float(abs_ck):.5f}, arg(c_k)={float(arg_ck):.4f}")

print("\n  Document's values for comparison:")
print("  k=1: |c_1|=0.04853, arg(c_1)=-1.6016")
print("  k=2: |c_2|=0.02778, arg(c_2)=-1.4873")

# Detailed check for k=1
rho_1 = zetazero(1)
gamma_1 = im(rho_1)
print(f"\n  Detailed k=1:")
print(f"    rho_1 = {rho_1}")
print(f"    gamma_1 = {float(gamma_1):.13f}")

zeta_rho1_plus_1 = zeta(rho_1 + 1)
zetaprime_rho1 = diff(zeta, rho_1)

print(f"    zeta(rho_1 + 1) = {zeta_rho1_plus_1}")
print(f"    zeta'(rho_1) = {zetaprime_rho1}")

c_1 = zeta_rho1_plus_1 / (rho_1 * zetaprime_rho1)
print(f"    c_1 = {c_1}")
print(f"    |c_1| = {float(fabs(c_1)):.5f}")
print(f"    arg(c_1) = {float(arg(c_1)):.4f}")
print(f"    Document claims: c_1 = -0.00149 - 0.04851i")
print(f"    We get: c_1 = {float(re(c_1)):.5f} + {float(im(c_1)):.5f}i")

# Check the match
doc_c1 = mpc('-0.00149', '-0.04851')
c1_diff = fabs(c_1 - doc_c1)
if c1_diff < 0.001:
    print(f"  [OK] c_1 matches document (diff = {float(c1_diff):.6f})")
else:
    msg = f"c_1 mismatch: we get {c_1}, document claims {doc_c1}, diff={float(c1_diff):.6f}"
    print(f"  [FAIL] {msg}")
    errors.append(msg)

# ============================================================
# CHECK 5: d_1 = 1/(rho_1 * zeta'(rho_1))
# ============================================================
print("\n--- CHECK 5: d_1 = 1/(rho_1 * zeta'(rho_1)) ---")

d_1 = 1 / (rho_1 * zetaprime_rho1)
print(f"  d_1 = {d_1}")
print(f"  |d_1| = {float(fabs(d_1)):.5f}")
print(f"  arg(d_1) = {float(arg(d_1)):.4f}")
print(f"  Document claims: d_1 = -0.01089 - 0.08847i, |d_1| = 0.08914, arg(d_1) = -1.6933")

doc_d1 = mpc('-0.01089', '-0.08847')
d1_diff = fabs(d_1 - doc_d1)
if d1_diff < 0.001:
    print(f"  [OK] d_1 matches (diff = {float(d1_diff):.6f})")
else:
    msg = f"d_1 mismatch: we get {d_1}, document claims {doc_d1}"
    print(f"  [FAIL/WARN] {msg}")
    if d1_diff < 0.01:
        warnings.append(msg)
    else:
        errors.append(msg)

# ============================================================
# CHECK 6: Phase prediction
# ============================================================
print("\n--- CHECK 6: Phase prediction ---")

gamma1_log2 = gamma_1 * log(2)
gamma1_log2_mod2pi = gamma1_log2 % (2*pi)
print(f"  gamma_1 * log(2) = {float(gamma1_log2):.6f}")
print(f"  gamma_1 * log(2) mod 2pi = {float(gamma1_log2_mod2pi):.4f}")
print(f"  Document claims: 3.5143")

arg_d1 = arg(d_1)
predicted_phase = float(gamma1_log2_mod2pi) - float(arg_d1)
predicted_phase_mod = predicted_phase % (2*float(pi))
print(f"  arg(d_1) = {float(arg_d1):.4f}")
print(f"  Predicted phase = gamma_1*log(2) - arg(d_1) = {predicted_phase:.4f}")
print(f"  Predicted phase mod 2pi = {predicted_phase_mod:.4f}")
print(f"  Document claims: 5.2076")
print(f"  Observed: 5.28")

phase_diff = abs(predicted_phase_mod - 5.2076)
if phase_diff < 0.01:
    print(f"  [OK] Phase prediction matches document (diff = {phase_diff:.4f})")
else:
    msg = f"Phase prediction: we get {predicted_phase_mod:.4f}, document claims 5.2076"
    print(f"  [CHECK] {msg}")
    if phase_diff < 0.1:
        warnings.append(msg)
    else:
        errors.append(msg)

# ============================================================
# CHECK 7: Explicit formula at s=0 -- the constant term
# ============================================================
print("\n--- CHECK 7: Explicit formula constant term ---")

# Document says: T(N) = [-2*log(N) + 2 - 2*gamma + 2*log(2pi)] + oscillatory - M(N) + O(1)
# The constant part of the residue at s=0 is: -2*gamma + 2*log(2pi)
# Plus there's a "+2" that should come from... where?
# The residue gives -2*log(N) - 2*gamma + 2*log(2pi)
# But the document adds "+2" in the explicit formula. Where does the 2 come from?

# Actually, looking more carefully at Section 4.1:
# T(N) = [-2*log(N) + 2 - 2*gamma + 2*log(2pi)] + oscillatory - M(N) + O(1)
# The residue at s=0 gives: -2*log(N) - 2*gamma + 2*log(2pi)
# So the "+2" must come from somewhere else.
#
# F(N) = Res_{s=0} + sum_rho Res_{s=rho} + [trivial zeros] + [error]
# T(N) = F(N) - M(N)
#
# The "+2" is suspicious. Let me check: maybe it's from the definition
# F(N) includes m=1 which is M(N)/1 = M(N). So F(N) = M(N) + T(N).
# But they define T(N) = F(N) - M(N), which is sum from m=2 to N.
#
# The "+2" might be accounting for the m=1 term or residues at trivial zeros.
# Actually wait -- if M(N) = -2 (as stated), then -M(N) = +2.
# So the formula T(N) = [Res at 0] + [osc] - M(N) + O(1)
# with M(N) = -2 gives the "+2" from -M(N). That's just substitution!

# So the "+2" is not a structural constant but "-M(N)" evaluated at M(N)=-2.
# This is a RED FLAG for presentation: they're mixing the general formula with
# a specific M(N) value in Section 4.1.

print("  The '+2' in Section 4.1 formula comes from -M(N) with M(N)=-2.")
print("  This is NOT a universal constant -- it depends on M(N).")
print("  [WARN] Section 4.1 mixes general Perron formula with specific M(N)=-2 case.")
warnings.append("Section 4.1 mixes general formula with M(N)=-2 specific case without clear notation")

# For M(N) = -2:
# T(N) = -2*log(N) - 2*gamma + 2*log(2pi) + 2 + oscillatory + O(1)
# = -2*log(N) + (-2*0.5772 + 2*1.8379 + 2)
# = -2*log(N) + (-1.1544 + 3.6758 + 2)
# = -2*log(N) + 4.5214

constant_for_M_neg2 = -2*float(gamma_em) + 2*float(log(2*pi)) + 2
print(f"  Constant for M(N)=-2: {constant_for_M_neg2:.4f}")
print(f"  Document claims: 6.5213")
print(f"  Discrepancy: {abs(constant_for_M_neg2 - 6.5213):.4f}")

# Hmm, 4.5214 != 6.5213. Something is off. Let me re-read the document.
# The document says: T(N) = -2*log(N) + 6.5213 + 0.0971*sqrt(N)*cos(...) + ...
# But our calculation gives constant = -2*gamma + 2*log(2pi) + 2 = 4.52.
# Where does 6.52 come from?

# Wait -- maybe there are contributions from trivial zeros or the double pole
# has a different coefficient than I computed. Let me check...
#
# Actually the issue might be: the residue formula gives -2(logN + gamma) + 2log(2pi) = -2logN + 2.52
# For M(N) = -2: T(N) = (-2logN + 2.52) + osc + (-(-2)) = -2logN + 2.52 + 2 = -2logN + 4.52
#
# But document says 6.52. So there's a discrepancy of 2.0.
# This could come from contributions of trivial zeros at s = -2, -4, ...
# Or from an error in the document.

# Let me check if the document includes something extra...
# From Section 4.1: T(N) = [-2*log(N) + 2 - 2*gamma + 2*log(2*pi)] + sum + O(1)
# = -2*log(N) + 2 + (-2*0.5772) + 2*1.8379 = -2logN + 2 - 1.1544 + 3.6758
# = -2logN + 4.5214

# But then with M(N) = -2, the "- M(N)" adds 2 more, giving:
# Hmm wait, is the formula in 4.1 already T(N) (i.e., already subtracted M(N))?
# Re-reading: "For M(N) = -2:" then formula with 6.5213.
# 6.5213 = 4.5214 + 2 = if M(N) is subtracted twice?

# OR: 6.5213 ≈ 2 - 2*gamma + 2*log(2pi) + some_correction
# 2 - 1.1544 + 3.6758 = 4.5214. Still not 6.52.
#
# Let me try: is it perhaps -2*log(N) + 2*(-M(N)) - 2*gamma + 2*log(2pi)?
# With M(N)=-2: -2logN + 4 - 1.1544 + 3.6758 = -2logN + 6.5214. YES!
# So the "2" in Section 4.1 might actually be 2*(-M(N)/M(N))... no.
#
# Actually I think the issue is: the constant is -2logN + 2.52 for the Perron residue,
# and then -M(N) = +2, giving T(N) = -2logN + 4.52 + osc.
# Document says 6.52. So there's an EXTRA +2.0 unaccounted for.
#
# This MIGHT be the contribution from trivial zeros. Let me compute it.

print("\n  INVESTIGATING: constant 6.52 vs our 4.52 -- difference = 2.0")
print("  Checking if trivial zeros contribute +2.0...")

# Trivial zero at s = -2: zeta(-2) = 0
# Residue at s = -2: N^(-2) * zeta(-1) / ((-2) * zeta'(-2))
# zeta(-1) = -1/12
# zeta'(-2) can be computed
rho_triv = mpf(-2)
zeta_neg1 = zeta(-1)
zetaprime_neg2 = diff(zeta, mpf(-2))
res_neg2 = zeta(rho_triv + 1) / (rho_triv * zetaprime_neg2)  # without N^s factor
print(f"  zeta(-1) = {zeta_neg1}")
print(f"  zeta'(-2) = {zetaprime_neg2}")
print(f"  c(-2) = zeta(-1)/((-2)*zeta'(-2)) = {float(res_neg2):.6f}")
print(f"  For N=1000: contribution = N^(-2)*c(-2) = {float(res_neg2)/1000**2:.10f}")
print("  Trivial zeros contribute negligibly for large N.")

# So the +2 discrepancy is NOT from trivial zeros.
# Let me reconsider. Maybe I'm wrong about the formula.

# Going back to basics: F(N) = sum_{m=1}^N M(floor(N/m))/m
# F(N) has the Perron representation.
# T(N) = F(N) - M(N) = F(N) - M(N)/1 (removing the m=1 term)
#
# So T(N) = Res_{s=0}[F(s)] + sum_rho Res_{rho}[F(s)] + error - M(N)
#
# For the Res_{s=0}: -2logN - 2gamma + 2log(2pi)
# oscillatory: sum 2Re[c_k N^{rho_k}]
# -M(N) with M(N)=-2: +2
# T(N) = -2logN + 2.52 + osc + 2 = -2logN + 4.52 + osc
#
# Document claims 6.52. There's a definite discrepancy of 2.0.
#
# UNLESS: the constant "+2" in Section 4.1 is not "-M(N)" but something else,
# and -M(N) = +2 is added SEPARATELY. Then:
# -2logN + 2 - 2gamma + 2log(2pi) = -2logN + 2 - 1.15 + 3.68 = -2logN + 4.52
# Then with -M(N)=+2: -2logN + 6.52. That matches!
#
# But WHERE does the "+2" come from in the Perron formula itself?
# The Perron residue at s=0 gives: -2logN - 2gamma + 2log(2pi) = -2logN + 2.52
# NOT -2logN + 2 - 2gamma + 2log(2pi).
#
# So either:
# (a) There's an additional +2 contribution I'm missing (from O(1) terms, or from the
#     double pole's principal part), or
# (b) The document has an error of +2.

# Let me re-examine the Laurent expansion more carefully.
# F(s) = N^s * zeta(s+1) / (s * zeta(s))
# = [1 + s*L + s^2*L^2/2 + ...] * [1/s + gamma + gamma1*s + ...] * (1/s) * [-2 + c1*s + c2*s^2 + ...]
#
# where L = logN, c1 = 2*log(2pi), gamma = Euler's constant.
#
# Let me expand step by step.
# Product of zeta(s+1) and 1/s:
# P(s) = zeta(s+1)/s = 1/s^2 + gamma/s + gamma1 + ...
#
# Product with 1/zeta(s):
# Q(s) = P(s) * (1/zeta(s)) = [1/s^2 + gamma/s + gamma1 + ...] * [-2 + c1*s + c2*s^2 + ...]
# = -2/s^2 + (-2*gamma + c1)/s + (-2*gamma1 + c1*gamma + c2) + ...  (*)
#
# wait, let me be careful about the s^0 term:
#   from 1/s^2 * c2*s^2 = c2
#   from gamma/s * c1*s = c1*gamma
#   from gamma1 * (-2) = -2*gamma1
# So coefficient of s^0 in Q(s) = c2 + c1*gamma - 2*gamma1
#
# Now Q(s) * N^s = Q(s) * [1 + s*L + ...]
# The coefficient of 1/s in this product:
#   from -2/s^2 * s*L = -2L/s  (contributes -2L to 1/s coefficient)
#   from (-2*gamma + c1)/s * 1 = (-2*gamma + c1)/s  (contributes (-2*gamma+c1))
#
# So Res_{s=0} = -2L + (-2*gamma + c1) = -2*logN - 2*gamma + c1
# = -2*logN - 2*gamma + 2*log(2pi)
#
# This is what I had before. The "+2" is NOT in the Perron residue.

# CONCLUSION: Document's constant 6.5213 = -2*gamma + 2*log(2pi) + 4
# = 2.5214 + 4 = 6.5214.
# This means the formula in Section 4.1 has an EXTRA +4 (or equivalently,
# it double-counts -M(N)).
#
# Actually wait. Let me re-read Section 4.1 one more time:
# "T(N) = [-2*log(N) + 2 - 2*gamma + 2*log(2*pi)] + sum_{rho} 2*Re[c_rho * N^rho] - M(N) + O(1)"
#
# For M(N) = -2:
# "T(N) = -2*log(N) + 6.5213 + 0.0971 * sqrt(N) * cos(...)"
#
# So: -2logN + 2 - 2gamma + 2log(2pi) - M(N) = -2logN + 2 + 2.52 - (-2) = -2logN + 6.52
# AH! So the formula ALREADY has "+2" as a separate constant PLUS "-M(N)" which adds another +2.
# The question is: where does the FIRST "+2" come from?
#
# The Perron residue at s=0 is -2logN - 2gamma + 2log(2pi) = -2logN + 2.52.
# So the general formula should be:
# F(N) = (-2logN + 2.52) + sum 2Re[c_k N^rho_k] + O(1)
# T(N) = F(N) - M(N) = (-2logN + 2.52) + osc - M(N) + O(1)
#
# The document says:
# T(N) = [-2logN + 2 - 2gamma + 2log(2pi)] + osc - M(N) + O(1)
# = [-2logN + 4.52] + osc - M(N) + O(1)
#
# So it has an EXTRA +2. Where?
#
# FOUND IT: Maybe it's the m=1 term in F(N). F(N) = M(N)/1 + sum_{m>=2} M(floor(N/m))/m.
# Wait no, that doesn't help -- the Perron integral already computes F(N) including m=1.
#
# OR: Maybe the "+2" comes from the F(N) = sum_{n<=N} h(n) where h(1) = sum_{d|1} mu(1)/1 = 1,
# and there's an off-by-one in Perron: the integral computes sum_{n<=N} h(n) but the
# hyperbolic sum might differ at the boundary...
#
# Actually I think this "+2" might be an ERROR in the document. Let me flag it.

print("\n  *** POTENTIAL ERROR: Document's constant 6.52 vs our derivation 4.52 ***")
print("  The Perron residue at s=0 gives: -2*logN - 2*gamma + 2*log(2pi)")
print("  Adding -M(N) = +2 gives: -2*logN + 4.52 (for M(N)=-2)")
print("  Document claims: -2*logN + 6.52")
print("  UNEXPLAINED +2.0 DISCREPANCY")

# Could this be from the s^0 term of the Laurent expansion that I'm omitting?
# The full residue at s=0 of a double pole includes the coefficient of 1/s,
# which is what I computed. The s^0 term would be the "regular part" which
# doesn't contribute to the residue.
#
# Unless the document is also including contributions from the integral's
# truncation error or something non-standard.

errors.append("Constant term discrepancy: document claims 6.52 but derivation gives 4.52 for M(N)=-2. Unexplained +2.0 difference. Possible double-counting of -M(N) or missing contribution.")

# ============================================================
# CHECK 8: Amplitude of first zero contribution
# ============================================================
print("\n--- CHECK 8: Amplitude of first zero oscillation ---")

# The oscillatory contribution from rho_1 pair is:
# 2 * Re[c_1 * N^{rho_1}] = 2 * |c_1| * N^{1/2} * cos(gamma_1*logN + arg(c_1))
# So amplitude = 2 * |c_1| * sqrt(N)
# Document claims 0.0971 * sqrt(N), so 2*|c_1| should be 0.0971

two_c1 = 2 * float(fabs(c_1))
print(f"  2*|c_1| = {two_c1:.5f}")
print(f"  Document claims: 0.0971")
print(f"  Match: {'YES' if abs(two_c1 - 0.0971) < 0.001 else 'NO (diff=' + str(abs(two_c1-0.0971)) + ')'}")

# ============================================================
# CHECK 9: Variance from first 20 zeros
# ============================================================
print("\n--- CHECK 9: Variance sigma^2 from 20 zeros ---")

sigma_sq = mpf(0)
for k in range(1, 21):
    rho_k = zetazero(k)
    zeta_rho_plus_1 = zeta(rho_k + 1)
    zetaprime_rho = diff(zeta, rho_k)
    c_k = zeta_rho_plus_1 / (rho_k * zetaprime_rho)
    sigma_sq += 2 * fabs(c_k)**2

sigma_val = sqrt(sigma_sq)
print(f"  sigma^2 = {float(sigma_sq):.6f}")
print(f"  sigma = {float(sigma_val):.4f}")
print(f"  Document claims: sigma^2 = 0.01018, sigma = 0.1009")

# ============================================================
# CHECK 10: Rubinstein-Sarnak P(T>0) approximation
# ============================================================
print("\n--- CHECK 10: Rubinstein-Sarnak P(T>0) at N=10^7 ---")

# The effective threshold is delta(N) = (2*logN - C) / sqrt(N)
# where C = -2*gamma + 2*log(2pi) + 2 (the constant part) ... or +4?
# Using our derivation: C = 2.52 (without the mysterious +2)
# Using document's: C = 4.52 or 6.52

# The P(T>0) is P(Y > delta) where Y has the Rubinstein-Sarnak distribution.
# For a rough Gaussian approximation: P = Phi(-delta/sigma)

from mpmath import erfc

# Let's compute for both our C and document's C
for label, C_val in [("Our derivation (C=2.52)", 2.52),
                     ("Document (C=4.52, +2 from Res only)", 4.52),
                     ("Document (C=6.52, as written)", 6.52)]:
    N = 10**7
    delta_N = (2*log(N) - C_val) / sqrt(N)
    # Gaussian approx: P(Y > delta) = 0.5 * erfc(delta/(sigma*sqrt(2)))
    sigma_f = float(sigma_val)
    delta_f = float(delta_N)
    P_gauss = float(0.5 * erfc(delta_f / (sigma_f * sqrt(2))))
    print(f"  {label}: delta={delta_f:.5f}, P(T>0)_Gauss={P_gauss:.3f}")

print(f"  Document claims P(T>0) = 0.47 at N=10^7")
print(f"  Observed: 0.462")

# ============================================================
# CHECK 11: Direct brute-force verification of F(N) for small N
# ============================================================
print("\n--- CHECK 11: Brute-force F(N) for small N ---")

def mertens(n):
    """Compute M(n) = sum_{k=1}^n mu(k) directly."""
    if n <= 0:
        return 0
    mu = [0] * (n + 1)
    mu[1] = 1
    for i in range(1, n + 1):
        for j in range(2*i, n + 1, i):
            mu[j] -= mu[i]
    M = [0] * (n + 1)
    M[1] = 1
    for i in range(2, n + 1):
        M[i] = M[i-1] + mu[i]
    return M

def compute_F_brute(N):
    """Compute F(N) = sum_{m=1}^{N} M(floor(N/m))/m."""
    M = mertens(N)
    F = mpf(0)
    for m in range(1, N + 1):
        F += mpf(M[N // m]) / m
    return F

def compute_T_brute(N):
    """Compute T(N) = F(N) - M(N)."""
    M = mertens(N)
    F = mpf(0)
    for m in range(1, N + 1):
        F += mpf(M[N // m]) / m
    return F - M[N]

# Compute Perron prediction for small N
def perron_predict_F(N, num_zeros=20):
    """Predict F(N) using Perron formula: residue at 0 + first num_zeros zero pairs."""
    # Residue at s=0
    pred = -2*(log(N) + gamma_em) + 2*log(2*pi)

    # Add contributions from zeta zeros
    for k in range(1, num_zeros + 1):
        rho_k = zetazero(k)
        zeta_rho_plus_1 = zeta(rho_k + 1)
        zetaprime_rho = diff(zeta, rho_k)
        c_k = zeta_rho_plus_1 / (rho_k * zetaprime_rho)
        contrib = 2 * re(c_k * power(N, rho_k))
        pred += contrib

    return float(pred)

for N_test in [100, 500, 1000, 2000]:
    F_actual = float(compute_F_brute(N_test))
    F_perron = perron_predict_F(N_test, num_zeros=50)
    T_actual = float(compute_T_brute(N_test))
    M_list = mertens(N_test)
    M_N = M_list[N_test]
    T_predicted_from_F = F_perron - M_N

    print(f"  N={N_test}: F_actual={F_actual:.4f}, F_perron(50 zeros)={F_perron:.4f}, "
          f"diff={abs(F_actual - F_perron):.4f}, M(N)={M_N}, "
          f"T_actual={T_actual:.4f}, T_from_perron={T_predicted_from_F:.4f}")

# ============================================================
# SUMMARY
# ============================================================
print("\n" + "="*70)
print("SUMMARY")
print("="*70)

print(f"\nERRORS ({len(errors)}):")
for i, e in enumerate(errors):
    print(f"  {i+1}. {e}")

print(f"\nWARNINGS ({len(warnings)}):")
for i, w in enumerate(warnings):
    print(f"  {i+1}. {w}")

print("\nDone.")
