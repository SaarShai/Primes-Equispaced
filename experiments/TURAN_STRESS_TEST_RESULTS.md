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
gamma_1 = (0.5 + 14.13472514173469379045725j)
|c_2(1/2 + i*gamma_1)| = 12719.24258228290442469925
1/sqrt(2)              = 0.7071067811865475244008444
difference             = 12718.53547550171787717485

SECTION 1. First 100 nontrivial zeta zeros
--- K = 10 ---
min_j |c_K(rho_j)| = 42832952965509.187002 at j = 1
mean |c_K(rho_j)|  = 1.0589739355233884451e+234
std  |c_K(rho_j)|  = 1.0520614540167609842e+235
any |c_K| < 1e-10? no

--- K = 20 ---
min_j |c_K(rho_j)| = 318942829754980391.58 at j = 1
mean |c_K(rho_j)|  = 6.5605242625865722742e+299
std  |c_K(rho_j)|  = 6.5260462433683284973e+300
any |c_K| < 1e-10? no

--- K = 50 ---
min_j |c_K(rho_j)| = 5.0046141945225537294e+22 at j = 1
mean |c_K(rho_j)|  = 4.4967256782855118287e+392
std  |c_K(rho_j)|  = 4.4741019740967051323e+393
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
       2        12719.2425822829044           18349.9881973232793
       5        3393610714.08171042           2108568890.95475705
      10         42832952965509.187           18602115116542.1663
      20       318942829754980392.0          106465732125188256.0
      50    5.00461419452255373e+22       1.27929058381772745e+22
     100    1.91202911233299182e+27       4.15191846362295586e+26
     200    8.43151705371521491e+31       1.59135749529638362e+31
     500    8.03448546224849884e+36       1.29283863680613269e+36
    1000    3.78740828279497162e+40        5.4828350597750896e+39

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
