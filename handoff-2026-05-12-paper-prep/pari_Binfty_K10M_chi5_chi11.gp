\\ PARI/GP push of the B_infty identity residual to K = 10^7 for the two
\\ clean-character pairs (chi_5 and chi_11; no bad primes -> pure
\\ conditional-tail K^{-1/2}/log K regime).
\\
\\ Compares T_K(chi, rho) = sum_{p<=K} sum_{k>=2} chi(p)^k / (k * p^{k rho})
\\ against the prediction
\\   RHS = (1/2) log L(2 rho, chi^2) + BPC_1 + BPC_2 + T_{>=3}
\\ from Theorem X.4.1 / Appendix A of the section draft.

default(realprecision, 50);

G5      = znstar(5,1);  chi5  = lfuncreate([G5,  [1]]);
G11     = znstar(11,1); chi11 = lfuncreate([G11, [1]]);
\\ Squared characters: chi_5^2 is the Legendre character mod 5 (primitive);
\\ chi_11^2 is the order-5 character mod 11 (primitive). For both, BPC_1 = 0.
chi5sq  = lfuncreate([G5,  [2]]);   \\ chi_5^2 has Conrey "2" (twice the order-4 generator)
chi11sq = lfuncreate([G11, [2]]);

t3 = 6.1835781954508539144;
t4 = 3.5470410917194500767;

K_test = 10000000;

eval_5(n)  = my(ev = chareval(G5,  [1], n)); if(ev == -1, 0, exp(2*Pi*I*ev));
eval_11(n) = my(ev = chareval(G11, [1], n)); if(ev == -1, 0, exp(2*Pi*I*ev));

\\ Streaming T_K computation: T_K = sum_{p <= K} log_taylor where
\\ log_taylor = -log(1 - chi(p) p^{-rho}) - chi(p) p^{-rho}.
T_K_streaming(eval_fn, rho, K) = {
  my(T, c, z, lg);
  T = 0.;
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

\\ BPC_2 absolutely convergent: -(1/2) sum_{k>=2} (1/k) sum_p chi(p)^{2k}/p^{2k rho}.
\\ Restrict to k <= 12 and prime sum to p <= 10^6 (this gives full machine precision).
BPC_2(eval_fn, rho) = {
  my(s, c, ksum, pmax);
  pmax = 1000000;
  s = 0.;
  for(k = 2, 12,
    ksum = 0.;
    forprime(p = 2, pmax,
      c = eval_fn(p);
      if(c, ksum = ksum + c^(2*k) * p^(-2*k*rho));
    );
    s = s + ksum / k;
  );
  - s / 2;
};

\\ T_{>=3} absolutely convergent: sum_{k>=3} (1/k) sum_p chi(p)^k/p^{k rho}.
T_ge3(eval_fn, rho) = {
  my(s, c, ksum, pmax);
  pmax = 1000000;
  s = 0.;
  for(k = 3, 12,
    ksum = 0.;
    forprime(p = 2, pmax,
      c = eval_fn(p);
      if(c, ksum = ksum + c^k * p^(-k*rho));
    );
    s = s + ksum / k;
  );
  s;
};

do_pair(label, L_chi, L_chisq, eval_fn, t_seed, K) = {
  my(rho, halflogLpsi, bpc1, bpc2, t_ge_3, RHS, T_K, residual, dt, t0);
  print("=== ", label, " ===");
  rho = 1/2 + I*t_seed;
  halflogLpsi = log(lfun(L_chisq, 2*rho)) / 2;
  bpc1 = 0.;  \\ no bad primes for chi_5 or chi_11
  bpc2 = BPC_2(eval_fn, rho);
  t_ge_3 = T_ge3(eval_fn, rho);
  RHS = halflogLpsi + bpc1 + bpc2 + t_ge_3;
  print("  rho = ", rho);
  print("  (1/2) log L(2 rho, psi) = ", halflogLpsi);
  print("  BPC_1 (no bad primes)   = ", bpc1);
  print("  BPC_2                   = ", bpc2);
  print("  T_{>=3}                 = ", t_ge_3);
  print("  RHS                     = ", RHS);
  t0 = getwalltime();
  T_K = T_K_streaming(eval_fn, rho, K);
  dt = (getwalltime() - t0) / 1000.0;
  print("  T_K at K=", K, "        = ", T_K);
  print("  T_K computation time    = ", dt, " s");
  residual = T_K - RHS;
  print("  T_K - RHS               = ", residual);
  print("  |T_K - RHS|             = ", abs(residual));
  print("  predicted O(K^{-1/2} / log K) = ", 1.0 / (sqrt(K) * log(K)));
  print("");
  return(0);
};

print("# PARI L2 push: B_infty identity residual at K = 10^7 for chi_5 and chi_11");
print("# realprecision = ", default(realprecision));
print("# K = ", K_test);
print("");

do_pair("chi_5",  chi5,  chi5sq,  (n) -> eval_5(n),  t3, K_test);
do_pair("chi_11", chi11, chi11sq, (n) -> eval_11(n), t4, K_test);

print("# done");
quit;
