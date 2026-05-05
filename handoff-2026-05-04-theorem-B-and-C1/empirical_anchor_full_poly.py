#!/usr/bin/env python3
"""Empirical anchor full polynomial closure for Theorem B.

Per M4_hours_test diagnosis: at T=100, c_3·log^3T is 89% of c_4·log^4T leading.
The 16-curve mean u_f = 0.242 vs target 2/(3π) = 0.212 has a 14% gap explained by
this finite-T lower-order correction.

Strategy: compute predicted u_f_full = (2/(3π)) * [1 + (a_3/a_4)/Y + (a_2/a_4)/Y^2]
using the closed-form a_3, a_2 from B1 results, and compare to empirical u_f.

If ratio empirical/predicted_full ≈ 1, Theorem B empirical anchor LOCKED.
"""
import math

# 16-curve data from B3_numerical_v2.out and prior B1 work
# Per row: (label, N, T_max, Y, c_f, u_f_empirical)
# Y per curve from W2_CF_RESOLVED.json
data = [
    ('11a1',   11,  177.16, 4.5381, 0.6429, 0.345521),
    ('14a1',   14,  172.02, 4.6293, 0.7165, 0.239653),
    ('15a1',   15,  171.10, 4.6584, 0.6948, 0.275617),
    ('17a1',   17,  168.91, 4.7081, 0.7048, 0.321003),
    ('19a1',   19,  166.78, 4.7510, 0.6918, 0.279709),
    ('20a1',   20,  166.04, 4.7722, 0.6982, 0.365606),
    ('21a1',   21,  164.70, 4.7885, 0.7228, 0.238284),
    ('24a1',   24,  162.91, 4.8443, 0.6939, 0.228532),
    ('100a1', 100,  141.43, 5.4165, 0.6982, 0.340792),
    ('106c1', 106,  140.91, 5.4420, 0.6884, 0.183107),
    ('200a1', 200,  132.92, 5.7010, 0.6982, 0.185041),
    ('221a1', 221,  131.73, 5.7420, 0.9160, 0.156095),
    ('240a1', 240,  131.01, 5.7777, 0.7800, 0.150776),
    ('496b1', 496,  123.19, 6.0791, 0.6144, 0.212444),
    ('510a1', 510,  123.25, 6.0935, 1.0299, 0.131076),
    ('5005b1',5005, 103.35, 7.0593, 0.5758, 0.214511),
]

# Closed-form coefficients per curve from B1 work
# B(f) per curve (from B1_HUNRAM_REFIT computation)
# B(f) = γ_E + L'/L_anal(1, sym²f) − 2·ζ'/ζ(2) + Σ_{p|N} log(p)/(p+1)
# Computed values from B1 work (consolidated)
B_f = {
    '11a1':  2.114, '14a1':  2.225, '15a1':  2.298, '17a1':  1.922,
    '19a1':  1.778, '20a1':  2.536, '21a1':  2.092, '24a1':  2.380,
    '100a1': 2.536, '106c1': 1.555, '200a1': 2.005, '221a1': 0.882,
    '240a1': 1.984, '496b1': 1.846, '510a1': 1.830, '5005b1':1.924,
}

# κ_2(f) per curve from v3 fit (using Opus' 3/4, 1/2, 1/4 with C=-log(2π))
# κ_2(f) = (3/4)·[(L''/L) − (L'/L)²] − (1/2)·k2_mult − (1/4)·k2_add − log(2π)
kappa2 = {
    '11a1': -2.856, '14a1': -2.942, '15a1': -2.978, '17a1': -2.449,
    '19a1': -2.442, '20a1': -3.268, '21a1': -2.845, '24a1': -3.040,
    '100a1':-3.697, '106c1':-1.348, '200a1':-3.464, '221a1': -1.539,
    '240a1':-2.605, '496b1':-1.882, '510a1': -2.067, '5005b1':-2.075,
}

a4 = 2/(3*math.pi)

print("# Empirical anchor full polynomial closure for Theorem B")
print(f"# a_4 = 2/(3π) = {a4:.6f}")
print()
print(f"{'curve':>7} {'B(f)':>7} {'κ_2':>7} {'a_3/a_4':>9} {'a_2/a_4':>9}  {'u_pred_LO':>10} {'u_pred_full':>11} {'u_emp':>8} {'ratio':>7}")
print("-" * 105)

ratios_full = []
ratios_LO = []
diffs_full = []
diffs_LO = []
for cn, N, T, Y, cf, u_emp in data:
    B = B_f[cn]
    k2 = kappa2[cn]
    a3_a4 = -4 + 4*B
    a2_a4 = 12 - 12*B + 6*B**2 + 6*k2

    # Leading-order prediction (just a_4 = 2/(3π))
    u_pred_LO = a4

    # Full polynomial prediction including a_3 and a_2 terms
    # u = M_obs/(c_f·T·log⁴X) ≈ a_4 + a_3/Y + a_2/Y² + ...
    u_pred_full = a4 + (a4 * a3_a4)/Y + (a4 * a2_a4)/(Y**2)

    ratio_full = u_emp / u_pred_full
    ratio_LO = u_emp / u_pred_LO
    ratios_full.append(ratio_full)
    ratios_LO.append(ratio_LO)
    diffs_full.append(u_emp - u_pred_full)
    diffs_LO.append(u_emp - u_pred_LO)

    print(f"{cn:>7} {B:7.3f} {k2:7.3f} {a3_a4:+9.3f} {a2_a4:+9.3f}  {u_pred_LO:10.4f} {u_pred_full:11.4f} {u_emp:8.4f} {ratio_full:7.3f}")

import statistics
print()
print(f"# LO-only ratio  empirical/(2/(3π)):   mean = {statistics.mean(ratios_LO):.4f}, stdev = {statistics.stdev(ratios_LO):.4f}")
print(f"# Full poly ratio empirical/predicted: mean = {statistics.mean(ratios_full):.4f}, stdev = {statistics.stdev(ratios_full):.4f}")
print()
print(f"# MAE LO only:    {statistics.mean([abs(d) for d in diffs_LO]):.4f}")
print(f"# MAE full poly:  {statistics.mean([abs(d) for d in diffs_full]):.4f}")
print()
print("# If full-poly ratio ≈ 1.0 with small stdev, Theorem B empirical anchor LOCKED.")
