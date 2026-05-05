#!/usr/bin/env python3
"""Fit Opus v3 regression form for κ_2 using full 16-curve data.

Form: κ_2 = c_L·L_cum + c_M·k2_mult + c_A·k2_add + c_z·ζ_cum + C_0
Determine coefficients from data; check structural integers (1/4, etc.)
"""
import csv, json
import numpy as np
import math

mp_data = """curve,Ncond,LpL,LppL,L_cumulant,k2_good,k2_mult,k2_add,kappa2_total,B_f,a2_over_a4,delta_2
11a1,11,0.197410,-0.386487,-0.425457,-43.851120,1.397546,0.000000,-41.994550,2.114372,-238.516349,-250.516349
14a1,14,0.033169,-0.279136,-0.280236,-42.427784,1.787867,0.000000,-40.035671,2.224594,-225.216244,-237.216244
15a1,15,0.037742,-0.150165,-0.151590,-42.402385,2.052970,0.000000,-39.616523,2.297773,-221.593852,-233.593852
17a1,17,0.047251,0.062881,0.060649,-43.527357,1.313075,0.000000,-41.269152,1.921790,-236.516735,-248.516735
19a1,19,-0.086462,0.054767,0.047291,-43.671820,1.278784,0.000000,-41.461263,1.777898,-239.136831,-251.136831
20a1,20,0.319746,-0.277644,-0.379881,-41.950677,1.223193,2.135347,-38.087537,2.536172,-208.366273,-220.366273
21a1,21,-0.142836,0.137751,0.117349,-42.184880,2.190575,0.000000,-38.992475,2.092194,-220.797526,-232.797526
24a1,24,0.157581,-0.313166,-0.337998,-41.918638,0.829777,2.135347,-38.407030,2.380421,-213.008805,-225.008805
100a1,100,0.319746,-0.277644,-0.379881,-41.950677,0.000000,6.295101,-35.150975,2.536172,-190.746902,-202.746902
106c1,106,-0.466557,1.735706,1.518031,-41.136758,1.297398,0.000000,-37.436847,1.555154,-216.771905,-228.771905
200a1,200,-0.211639,-0.025458,-0.070249,-41.367828,0.000000,6.295101,-34.258494,2.004788,-193.493373,-205.493373
221a1,221,-1.176192,3.574868,2.191440,-40.435835,2.689287,0.000000,-34.670626,0.881557,-201.939582,-213.939582
240a1,240,-0.507130,1.314459,1.057279,-39.386194,2.052970,2.135347,-33.256116,1.983950,-187.727757,-199.727757
496b1,496,-0.209916,1.426075,1.382011,-40.783983,1.094009,2.135347,-35.288135,1.845583,-201.438749,-213.438749
510a1,510,-0.818148,2.892303,2.222936,-37.893059,3.793114,0.000000,-30.992526,1.830332,-175.818449,-187.818449
5005b1,5005,-0.687186,3.727958,3.255733,-37.783216,5.357748,0.000000,-28.285253,1.924465,-158.583699,-170.583699
"""

# Y per curve from W2_CF_RESOLVED.json
Y_per = {
    '11a1': 4.5381, '14a1': 4.6293, '15a1': 4.6584, '17a1': 4.7081, '19a1': 4.7510,
    '20a1': 4.7722, '21a1': 4.7885, '24a1': 4.8443, '100a1': 5.4165, '106c1': 5.4420,
    '200a1': 5.7010, '221a1': 5.7420, '240a1': 5.7777, '496b1': 6.0791, '510a1': 6.0935,
    '5005b1': 7.0593,
}

R_OBS = {
    '11a1': 0.7825, '14a1': 0.9296, '15a1': 1.0850, '17a1': 0.6168, '19a1': 0.3847,
    '20a1': 1.0612, '21a1': 0.7052, '24a1': 1.1921, '100a1': 1.0013, '106c1': 0.3166,
    '200a1': 0.3065, '221a1': -0.1615, '240a1': 0.7112, '496b1': 0.5377,
    '510a1': 0.5679, '5005b1': 0.6251,
}

ZETA_CUM = 0.884481833963523885  # (ζ''/ζ)(2) − (ζ'/ζ)(2)²

rows = []
for line in mp_data.strip().split('\n')[1:]:
    fields = line.split(',')
    cn = fields[0]
    LpL = float(fields[2])
    LppL = float(fields[3])
    L_cum = float(fields[4])
    k2g = float(fields[5])
    k2m = float(fields[6])
    k2a = float(fields[7])
    B_f = float(fields[9])
    Y = Y_per[cn]
    r_obs = R_OBS[cn]
    r_pred_a3 = (-4 + 4*B_f)/Y
    residual = r_obs - r_pred_a3  # = (a_2/a_4)/Y + ...
    a2_a4_emp = residual * Y      # empirical a_2/a_4
    delta_2_emp = a2_a4_emp - 12  # empirical δ_2
    # κ_2 implied: δ_2 = -12B + 6B² + 6κ_2  →  κ_2 = (δ_2 + 12B - 6B²)/6
    kappa2_emp = (delta_2_emp + 12*B_f - 6*B_f**2)/6
    rows.append({
        'curve': cn, 'B': B_f, 'L_cum': L_cum, 'k2m': k2m, 'k2a': k2a,
        'a2_a4_emp': a2_a4_emp, 'delta_2_emp': delta_2_emp, 'kappa2_emp': kappa2_emp
    })

print("curve, B, L_cum, k2m, k2a, a2/a4_emp, δ_2_emp, κ_2_emp")
for r in rows:
    print(f"{r['curve']:>7} {r['B']:7.3f} {r['L_cum']:+8.3f} {r['k2m']:7.3f} {r['k2a']:7.3f} {r['a2_a4_emp']:+7.3f} {r['delta_2_emp']:+7.3f} {r['kappa2_emp']:+7.3f}")

# Fit κ_2_emp = c_L·L_cum + c_M·k2m + c_A·k2a + C_0
# (universal ζ_cum = 0.884 is constant; absorb in C_0)
A = np.array([[r['L_cum'], r['k2m'], r['k2a'], 1.0] for r in rows])
b = np.array([r['kappa2_emp'] for r in rows])
coeffs, residuals, rank, sv = np.linalg.lstsq(A, b, rcond=None)
print(f"\nLeast-squares fit: κ_2 = {coeffs[0]:+.4f}·L_cum + {coeffs[1]:+.4f}·k2m + {coeffs[2]:+.4f}·k2a + {coeffs[3]:+.4f}")
pred = A @ coeffs
fit_residuals = b - pred
print(f"residual max abs: {max(abs(fit_residuals)):.4f}, MAE: {np.mean(abs(fit_residuals)):.4f}, R²: {1 - sum(fit_residuals**2)/sum((b-b.mean())**2):.4f}")
print("\nResiduals per curve:")
for r, fr in zip(rows, fit_residuals):
    print(f"  {r['curve']:>7}: {fr:+.4f}")

# Try clean fractional ansatzes
print("\n--- structural ansatz tests ---")
ansatzes = [
    ("κ_2 = ¼·L_cum − ¼·k2m − ⅛·k2a − ζ_cum + 0", lambda r: 0.25*r['L_cum'] - 0.25*r['k2m'] - 0.125*r['k2a'] - ZETA_CUM),
    ("κ_2 = ½·L_cum − ½·k2m − ¼·k2a − ζ_cum", lambda r: 0.5*r['L_cum'] - 0.5*r['k2m'] - 0.25*r['k2a'] - ZETA_CUM),
    ("κ_2 = (L_cum − k2m − ½·k2a)/4 − ζ_cum + (-0.33)", lambda r: (r['L_cum']-r['k2m']-0.5*r['k2a'])/4 - ZETA_CUM - 0.33),
    ("κ_2 = ¼(L_cum − k2m) − ζ_cum − 0.33", lambda r: 0.25*(r['L_cum']-r['k2m']) - ZETA_CUM - 0.33),
    ("κ_2 = LSQ best", None),
]
for name, fn in ansatzes:
    if fn is None: continue
    diffs = [fn(r) - r['kappa2_emp'] for r in rows]
    print(f"  {name:<55} MAE={np.mean(np.abs(diffs)):.3f} max={max(abs(d) for d in diffs):.3f}")
