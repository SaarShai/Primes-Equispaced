\\ PARI B_infty verification at K = 2e6 and K = 10^7 using mpmath-matching
\\ CLOSED-FORM expressions for T_K, T_>=3, and BPC_2 (sums all k via the
\\ analytical per-prime formulas).
\\
\\ Previous PARI scripts (pari_Binfty_K10M_chi5_chi11.gp etc.) used an
\\ explicit k-loop truncated at k = 12, which misses the p = 2 tail at
\\ ~10^-3 for chi_5 and chi_11. This script reproduces the mpmath methodology.

default(realprecision, 50);

G5  = znstar(5,1);  chi5  = lfuncreate([G5,  [1]]);
G11 = znstar(11,1); chi11 = lfuncreate([G11, [1]]);
chi5sq  = lfuncreate([G5,  [2]]);
chi11sq = lfuncreate([G11, [2]]);

t1 = 6.0209489046975966549;     \\ chi_{-4}/z1
t2 = 10.243770304166554552;     \\ chi_{-4}/z2
t3 = 6.1835781954508539144;     \\ chi_5
t4 = 3.5470410917194500767;     \\ chi_11

eval_chim4(n) = kronecker(-4, n);
eval_5(n)  = my(ev = chareval(G5,  [1], n)); if(ev == -1, 0, exp(2*Pi*I*ev));
eval_11(n) = my(ev = chareval(G11, [1], n)); if(ev == -1, 0, exp(2*Pi*I*ev));

\\ T_K(chi, rho) = sum_{p<=K} sum_{k>=2} chi(p)^k / (k p^{k rho})
\\               = sum_{p<=K} [-log(1 - z_p) - z_p]
\\ where z_p = chi(p) / p^rho.
T_K_closed(eval_fn, rho, K) = {
  my(T = 0., c, z, lg);
  forprime(p = 2, K,
    c = eval_fn(p);
    if(c,
      z = c * p^(-rho);
      lg = -log(1 - z) - z;
      T = T + lg;
    );
  );
  T;
};

\\ T_{>=3}(chi, rho) = sum_p [-log(1 - z_p) - z_p - z_p^2/2]
\\ Sums ALL k >= 3 exactly, per prime, via the closed-form Taylor expansion.
T_ge3_closed(eval_fn, rho, pmax) = {
  my(s = 0., c, z);
  forprime(p = 2, pmax,
    c = eval_fn(p);
    if(c,
      z = c * p^(-rho);
      s = s + (-log(1 - z) - z - z*z/2);
    );
  );
  s;
};

\\ BPC_2(chi, rho) = -(1/2) sum_{k>=2}(1/k) sum_p chi(p)^{2k}/p^{2k rho}
\\                 = -(1/2) sum_p [-log(1 - y_p) - y_p]
\\                 = (1/2) sum_p [log(1 - y_p) + y_p]
\\ where y_p = chi(p)^2 / p^{2 rho}.
BPC2_closed(eval_fn, rho, pmax) = {
  my(s = 0., c, y);
  forprime(p = 2, pmax,
    c = eval_fn(p);
    if(c,
      y = c*c * p^(-2*rho);
      s = s + (log(1 - y) + y);
    );
  );
  s / 2;
};

\\ BPC_1: bad-prime correction (imprimitive -> primitive)
\\ chi_{-4}: bad prime p=2, psi=trivial.  BPC_1 = (1/2) log(1 - 2^{-2 rho}).
\\ chi_5, chi_11: no bad primes. BPC_1 = 0.

\\ Run a (chi, rho, character-data) pair at both K = 2e6 and K = 10^7.
run_pair(label, L_chisq, eval_fn, t_seed, K_low, K_high, has_bad_prime_2) = {
  my(rho, halflogL, bpc1, bpc2, tge3, RHS, T_K_low, T_K_high, res_low, res_high);
  print("====== ", label, " ======");
  rho = 1/2 + I*t_seed;
  halflogL = log(lfun(L_chisq, 2*rho)) / 2;

  \\ BPC_1
  if(has_bad_prime_2,
    bpc1 = log(1 - 2^(-2*rho)) / 2,
    bpc1 = 0.
  );

  bpc2 = BPC2_closed(eval_fn, rho, 1000000);   \\ p ≤ 10^6 sufficient (component absolutely conv.)
  tge3 = T_ge3_closed(eval_fn, rho, 1000000);  \\ same
  RHS = halflogL + bpc1 + bpc2 + tge3;
  print("  (1/2) log L(2 rho, psi) = ", halflogL);
  print("  BPC_1                   = ", bpc1);
  print("  BPC_2 (closed-form)     = ", bpc2);
  print("  T_{>=3} (closed-form)   = ", tge3);
  print("  RHS                     = ", RHS);

  T_K_low = T_K_closed(eval_fn, rho, K_low);
  res_low = abs(T_K_low - RHS);
  print("  T_K at K=", K_low, "       = ", T_K_low);
  print("  |T_K - RHS| at K=", K_low, " = ", res_low);

  T_K_high = T_K_closed(eval_fn, rho, K_high);
  res_high = abs(T_K_high - RHS);
  print("  T_K at K=", K_high, "       = ", T_K_high);
  print("  |T_K - RHS| at K=", K_high, " = ", res_high);
  print("  ratio low/high          = ", res_low / res_high, "  (predicted sqrt(K_high/K_low) = ", sqrt(K_high/K_low * 1.0), ")");
  print("");
};

K_low = 2000000;
K_high = 100000000;

print("# PARI B_infty closed-form methodology (matches mpmath)");
print("# realprecision = ", default(realprecision));
print("# K_low = ", K_low, "   K_high = ", K_high);
print("# Component truncation: p ≤ 10^6 (absolutely convergent)");
print("");

run_pair("chi_-4 / z1", lfuncreate(1), (n) -> eval_chim4(n), t1, K_low, K_high, 1);
run_pair("chi_-4 / z2", lfuncreate(1), (n) -> eval_chim4(n), t2, K_low, K_high, 1);
run_pair("chi_5",       chi5sq,        (n) -> eval_5(n),     t3, K_low, K_high, 0);
run_pair("chi_11",      chi11sq,       (n) -> eval_11(n),    t4, K_low, K_high, 0);

print("# done");
quit;
