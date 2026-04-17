============================================================
Turán non-vanishing theorem numerical verification
mp.dps = 50
============================================================

SECTION 0. Möbius sanity check via trial factorization
mu( 2) = -1
mu( 3) = -1
mu( 4) = 0
mu( 5) = -1
mu( 6) = 1
mu( 7) = -1
mu( 8) = 0
mu( 9) = 0
mu(10) = 1
mu(11) = -1
mu(12) = 0
mu(13) = -1
mu(14) = 1
mu(15) = 1

SECTION 0b. Cross-check: c_2(s) = -2^{-s}
gamma_1 = 14.13472514173469379045725
|c_2(1/2 + i*gamma_1)| = 0.7071067811865475244008444
1/sqrt(2)              = 0.7071067811865475244008444
difference             = 1.336382355046097823070268e-51

SECTION 1. First 100 nontrivial zeta zeros
--- K = 10 ---
min_j |c_K(rho_j)| = 0.094330481690331190794 at j = 59
mean |c_K(rho_j)|  = 1.2149562172589745588
std  |c_K(rho_j)|  = 0.63883163407313795503
any |c_K| < 1e-10? no

--- K = 20 ---
min_j |c_K(rho_j)| = 0.12031385484859735185 at j = 84
mean |c_K(rho_j)|  = 1.395898765416091726
std  |c_K(rho_j)|  = 0.83055887976479741287
any |c_K| < 1e-10? no

--- K = 50 ---
min_j |c_K(rho_j)| = 0.13266437085543239312 at j = 38
mean |c_K(rho_j)|  = 1.7883984528503651641
std  |c_K(rho_j)|  = 1.0381899692564549314
any |c_K| < 1e-10? no

SECTION 2. 500 evenly spaced t in [0, 5000]
--- K = 10 ---
global min over 500 sampled t values: 0.058172417978233472184
attained at t = 2625.250501002004008

--- K = 20 ---
global min over 500 sampled t values: 0.053222904325032819528
attained at t = 1122.2444889779559118

--- K = 50 ---
global min over 500 sampled t values: 0.034581831644527435016
attained at t = 2244.4889779559118236

SECTION 3. |c_K(rho_1)| for increasing K
       K               |c_K(rho_1)|         |c_K(rho_1)| / log(K)
------------------------------------------------------------------
       2       0.707106781186547524           1.02013944659678948
       5        1.61876474242846884           1.00579508530419955
      10        2.42476297930315367           1.05306118183464846
      20        3.42488884504124127           1.14325598294473752
      50        4.49238101842850159           1.14835240288594342
     100         5.2941568645928427           1.14961155631144638
     200        5.85929771474803635           1.10587896295942158
     500        7.13805337633125281           1.14859268087130254
    1000        8.02225928459715592           1.16134097989922449

SECTION 4. Summary
1. Möbius values were computed from scratch by trial factorization.
2. The cross-check c_2(s) = -2^{-s} matches |c_2(1/2 + i*gamma_1)| = 1/sqrt(2).
3. For K = 10, 20, 50 the script reports the first-100-zero statistics, including
   the minimum, mean, standard deviation, and whether any values fall below 1e-10.
4. For K = 10, 20, 50 the script also reports the minimum over 500 sampled points on
   the line Re(s) = 1/2 for t in [0, 5000].
5. The K-table for |c_K(rho_1)| is printed with the normalization by log(K).
6. All computations use mpmath at 50-digit precision.
============================================================
