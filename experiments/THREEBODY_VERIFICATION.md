# Three-Body Gap Verification Results

**Date**: 2026-03-27
**Method**: N-body integration (scipy DOP853, rtol=atol=1e-12)
**Setup**: Equal masses m1=m2=m3=1, planar, zero angular momentum
**Initial positions**: r1=(-1,0), r2=(1,0), r3=(0,0)

## Classification Thresholds

| Category | Position Error | Velocity Error | Meaning |
|---|---|---|---|
| LIKELY PERIODIC | < 0.01 | < 0.01 | High confidence periodic orbit |
| PROMISING | < 0.1 | any | Worth refining with Newton's method |
| MARGINAL | < 1.0 | any | Possible but needs significant refinement |
| NOT PERIODIC | > 1.0 | any | Prediction failed at this precision |

---

## Control Orbits (Known Periodic)

These validate our integrator. Known orbits should return with very small error.

| ID | Word | T_cat | T_used | Mult | Pos Error | Vel Error | E Drift | Status |
|---|---|---|---|---|---|---|---|---|
| I.A-1 | BabA | 6.3259 | 6.3259 | 1x | 2.38e-11 | 2.80e-11 | 1.21e-15 | LIKELY PERIODIC |
| I.A-2 | BAbabaBA | 6.2347 | 6.2347 | 1x | 4.37e-10 | 8.28e-10 | 6.90e-11 | LIKELY PERIODIC |
| I.A-3 | BaBabAbA | 37.3205 | 37.3205 | 1x | 3.98e-07 | 3.47e-07 | 8.95e-15 | LIKELY PERIODIC |
| I.B-1 | BabaBAbabA | 14.8943 | 14.8943 | 1x | 5.67e-09 | 5.45e-09 | 1.82e-11 | LIKELY PERIODIC |
| II.C-2 | BaBAbaBAbaBAbA | 54.7502 | 54.7502 | 1x | 6.52e-07 | 5.90e-07 | 5.24e-11 | LIKELY PERIODIC |

**Integrator validation**: 5/5 controls returned within 0.1

---

## Gap Predictions (Interpolated Initial Conditions)

These are approximate ICs from linear interpolation between neighboring orbits.
Small errors would confirm new periodic orbits; large errors suggest the gap
contains no orbit at the interpolated point (refinement needed).

| Rank | Gap | v1 | v2 | T_pred | T_used | Mult | Pos Error | Vel Error | E Drift | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | II.C-222 / II.C-104 | 0.4018 | 0.3911 | 208.8 | 208.8 | 1x | 6.47e-01 | 7.72e-01 | 2.93e-07 | MARGINAL |
| 2 | II.C-39 / II.C-2 | 0.4959 | 0.4386 | 96.7 | 290.1 | 3x | 2.00e+00 | 7.70e-01 | 6.89e-09 | NOT PERIODIC |
| 3 | II.C-5 / I.A-3 | 0.5832 | 0.5365 | 31.9 | 63.7 | 2x | 2.78e+00 | 1.14e+00 | 2.18e-11 | NOT PERIODIC |
| 4 | I.A-90 / I.A-148 | 0.2713 | 0.4258 | 202.5 | 202.5 | 1x | 5.11e+01 | 2.12e+00 | 3.81e-10 | NOT PERIODIC |
| 5 | I.A-3 / II.C-61 | 0.6424 | 0.5044 | 24.1 | 72.3 | 3x | 2.69e+00 | 1.80e+00 | 4.85e-11 | NOT PERIODIC |
| 6 | II.C-206 / I.B-21 | 0.2553 | 0.3994 | 139.4 | 139.4 | 1x | 1.22e+02 | 1.58e+00 | 1.48e-08 | NOT PERIODIC |
| 7 | II.C-69 / I.A-51 | 0.2612 | 0.2375 | 133.0 | 133.0 | 1x | 4.10e-01 | 9.87e-01 | 5.88e-09 | MARGINAL |
| 8 | II.A-4 / I.A-28 | 0.0376 | 0.6405 | 94.6 | 94.6 | 1x | 1.11e+00 | 2.19e+00 | 6.57e-08 | NOT PERIODIC |
| 9 | II.C-197 / II.C-64 | 0.0919 | 0.1666 | 87.0 | 87.0 | 1x | 3.18e+01 | 1.92e+00 | 2.01e-02 | NOT PERIODIC |
| 10 | II.C-109 / I.A-97 | 0.3240 | 0.5013 | 259.8 | 779.5 | 3x | 1.46e+00 | 1.18e+00 | 5.16e-07 | NOT PERIODIC |

### Summary

- **Likely periodic**: 0/10
- **Promising/Marginal**: 2/10
- **Not periodic**: 8/10

### Candidates for Refinement

- **Gap #1** (II.C-222 <-> II.C-104): v1=0.401768, v2=0.391111, T=208.838, return_error=6.47e-01
- **Gap #7** (II.C-69 <-> I.A-51): v1=0.261194, v2=0.237468, T=132.976, return_error=4.10e-01

---

## Interpretation

The gap predictions use *linear interpolation* of initial conditions between
neighboring known orbits in Stern-Brocot tree position. This is a zeroth-order
approximation; real orbit-finding would use:

1. The interpolated ICs as a **starting point** for Newton's method
2. A **shooting method** that minimizes ||r(T)-r(0)|| + ||v(T)-v(0)||
3. Period T as a free parameter (our T is also interpolated)

Even marginal results (error < 1.0) suggest there may be a nearby periodic
orbit that a proper numerical search would find.

## Orbit Plots

### Control: I.A-1
![I.A-1](threebody_orbit_control_I_A-1.png)

### Control: I.A-2
![I.A-2](threebody_orbit_control_I_A-2.png)

### Control: I.A-3
![I.A-3](threebody_orbit_control_I_A-3.png)

### Control: I.B-1
![I.B-1](threebody_orbit_control_I_B-1.png)

### Control: II.C-2
![II.C-2](threebody_orbit_control_II_C-2.png)

### Gap #1: II.C-222 <-> II.C-104
![Gap 1](threebody_orbit_gap_01.png)

### Gap #2: II.C-39 <-> II.C-2
![Gap 2](threebody_orbit_gap_02.png)

### Gap #3: II.C-5 <-> I.A-3
![Gap 3](threebody_orbit_gap_03.png)

### Gap #4: I.A-90 <-> I.A-148
![Gap 4](threebody_orbit_gap_04.png)

### Gap #5: I.A-3 <-> II.C-61
![Gap 5](threebody_orbit_gap_05.png)

### Gap #6: II.C-206 <-> I.B-21
![Gap 6](threebody_orbit_gap_06.png)

### Gap #7: II.C-69 <-> I.A-51
![Gap 7](threebody_orbit_gap_07.png)

### Gap #8: II.A-4 <-> I.A-28
![Gap 8](threebody_orbit_gap_08.png)

### Gap #9: II.C-197 <-> II.C-64
![Gap 9](threebody_orbit_gap_09.png)

### Gap #10: II.C-109 <-> I.A-97
![Gap 10](threebody_orbit_gap_10.png)

