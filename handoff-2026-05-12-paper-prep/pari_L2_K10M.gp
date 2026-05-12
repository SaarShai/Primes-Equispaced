\\ PARI/GP L2 cross-check at K = 10^7 on all four Dirichlet (chi, rho) pairs.
\\ Drop-in extension of pari_L2_crosscheck.gp; longer wall-clock.

default(realprecision, 50);

L_chim4 = lfuncreate(-4);
G5      = znstar(5,1);  chi5  = lfuncreate([G5,  [1]]);
G11     = znstar(11,1); chi11 = lfuncreate([G11, [1]]);

t1 = 6.0209489046975966549;
t2 = 10.243770304166554552;
t3 = 6.1835781954508539144;
t4 = 3.5470410917194500767;

K_test = 10000000;

refine_zero(L, t0) = {
  my(r, dL, w);
  w = 1/2 + I*t0;
  for(it = 1, 30,
    r  = lfun(L, w);
    dL = lfun(L, w, 1);
    if(abs(r) < 10.^(-48), return(w));
    w = w - r/dL;
  );
  w;
};
Lpp_findiff(L, w, h) = (lfun(L, w + h, 1) - lfun(L, w - h, 1)) / (2*h);

eval_chim4(n) = kronecker(-4, n);
eval_5(n)  = my(ev = chareval(G5,  [1], n)); if(ev == -1, 0, exp(2*Pi*I*ev));
eval_11(n) = my(ev = chareval(G11, [1], n)); if(ev == -1, 0, exp(2*Pi*I*ev));

\\ c_K = sum_{n<=K} mu(n) * chi(n) * n^{-rho}.  Streaming version: do not
\\ materialize the full mu vector for K = 10^7 (~80 MB at default size).
c_K_streaming(eval_fn, rho, K) = {
  my(s, mn, c);
  s = 0.;
  for(n = 1, K,
    mn = moebius(n);
    if(mn,
      c = eval_fn(n);
      if(c, s = s + mn * c * n^(-rho));
    );
  );
  s;
};

do_pair(label, L, t_seed, c_K_fn, K) = {
  my(rho, Lp, Lpp, C1, cK, R, absR, t0, dt);
  print("=== ", label, " ===");
  rho = refine_zero(L, t_seed);
  print("  rho = ", rho);
  Lp  = lfun(L, rho, 1);
  Lpp = Lpp_findiff(L, rho, 10.^(-15));
  C1  = - Lpp / (2 * Lp^2);
  print("  L' = ", Lp, "    (|L'| = ", abs(Lp), ")");
  print("  L'' = ", Lpp, "    (|L''| = ", abs(Lpp), ")");
  print("  C_1 = ", C1, "    (|C_1| = ", abs(C1), ")");
  t0 = getwalltime();
  cK = c_K_fn(rho, K);
  dt = (getwalltime() - t0) / 1000.0;
  print("  c_K computation took ", dt, " s");
  R = cK - log(K)/Lp - C1;
  absR = abs(R);
  print("  c_K at K=", K, " = ", cK);
  print("  R(K) = c_K - log K/L' - C_1 = ", R);
  print("  |R(K)| at K=", K, " = ", absR);
  print("  log(K)/sqrt(K) predicted scale = ", log(K)/sqrt(K));
  print("");
  return(0);
};

print("# PARI L2 push to K = 10^7");
print("# realprecision = ", default(realprecision));
print("# K = ", K_test);
print("");

do_pair("chi_-4/z1", L_chim4, t1, (rho,K) -> c_K_streaming(eval_chim4, rho, K), K_test);
do_pair("chi_-4/z2", L_chim4, t2, (rho,K) -> c_K_streaming(eval_chim4, rho, K), K_test);
do_pair("chi_5",     chi5,    t3, (rho,K) -> c_K_streaming(eval_5,     rho, K), K_test);
do_pair("chi_11",    chi11,   t4, (rho,K) -> c_K_streaming(eval_11,    rho, K), K_test);

print("# done");
quit;
