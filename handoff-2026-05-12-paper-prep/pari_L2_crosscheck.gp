\\ PARI/GP L2 cross-check for the four Dirichlet (chi, rho) pairs.
\\
\\ L1 reference: handoff-2026-05-09-followup/Koyama_C1.out (mpmath, 50 dps).
\\
\\ Usage:
\\   gp -q pari_L2_crosscheck.gp

default(realprecision, 50);

L_chim4 = lfuncreate(-4);
G5      = znstar(5,1);  chi5  = lfuncreate([G5,  [1]]);
G11     = znstar(11,1); chi11 = lfuncreate([G11, [1]]);

\\ Reference |L'|, |L''|, |C_1| from Koyama_C1.out (50 dps).
ref_absLp_1  = 1.30932; ref_absLp_2  = 1.81292; ref_absLp_3  = 1.20003; ref_absLp_4  = 1.71505;
ref_absLpp_1 = 1.78533; ref_absLpp_2 = 3.40425; ref_absLpp_3 = 1.94171; ref_absLpp_4 = 3.13251;
ref_absC1_1  = 0.52067; ref_absC1_2  = 0.51795; ref_absC1_3  = 0.67423; ref_absC1_4  = 0.53249;
ref_absR_1   = 0.134447; ref_absR_2  = 0.257279; ref_absR_3  = 0.245896; ref_absR_4  = 0.210102;

t1 = 6.0209489046975966549;
t2 = 10.243770304166554552;
t3 = 6.1835781954508539144;
t4 = 3.5470410917194500767;

K_test = 200000;

\\ Newton refinement for the zero starting from imaginary-part seed t0.
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
\\ PARI 2.17: chareval(G, chi, n) returns the fraction a/b s.t. chi(n) = exp(2*Pi*I*a/b),
\\ or -1 if gcd(n, modulus) != 1.  Wrap to recover the complex value.
eval_5(n)  = my(ev = chareval(G5,  [1], n)); if(ev == -1, 0, exp(2*Pi*I*ev));
eval_11(n) = my(ev = chareval(G11, [1], n)); if(ev == -1, 0, exp(2*Pi*I*ev));

\\ c_K = sum_{n<=K} mu(n) * chi(n) * n^{-rho}.
c_K_chim4(rho, K) = my(s = 0., mu_arr); mu_arr = vector(K, n, moebius(n)); for(n = 1, K, if(mu_arr[n], my(c = eval_chim4(n)); if(c, s = s + mu_arr[n] * c * n^(-rho)))); s;
c_K_5(rho, K)     = my(s = 0., mu_arr); mu_arr = vector(K, n, moebius(n)); for(n = 1, K, if(mu_arr[n], my(c = eval_5(n));     if(c, s = s + mu_arr[n] * c * n^(-rho)))); s;
c_K_11(rho, K)    = my(s = 0., mu_arr); mu_arr = vector(K, n, moebius(n)); for(n = 1, K, if(mu_arr[n], my(c = eval_11(n));    if(c, s = s + mu_arr[n] * c * n^(-rho)))); s;

do_pair(label, L, t_seed, ref_absLp, ref_absLpp, ref_absC1, ref_absR, c_K_fn, K) = {
  my(rho, Lp, Lpp, C1, absLp, absLpp, absC1, cK, R, absR);
  print("=== ", label, " ===");
  rho = refine_zero(L, t_seed);
  print("  rho = ", rho);
  print("  |L(rho)| = ", abs(lfun(L, rho)));
  Lp  = lfun(L, rho, 1);
  Lpp = Lpp_findiff(L, rho, 10.^(-15));
  C1  = - Lpp / (2 * Lp^2);
  absLp  = abs(Lp);   absLpp = abs(Lpp);  absC1 = abs(C1);
  print("  L'  = ", Lp);
  print("  |L'|  = ", absLp);
  print("  L'' = ", Lpp);
  print("  |L''| = ", absLpp);
  print("  C_1 = ", C1);
  print("  |C_1| = ", absC1);
  print("  |L1 - L2| on |L'|  = ", abs(absLp  - ref_absLp));
  print("  |L1 - L2| on |L''| = ", abs(absLpp - ref_absLpp));
  print("  |L1 - L2| on |C_1| = ", abs(absC1  - ref_absC1));
  cK   = c_K_fn(rho, K);
  R    = cK - log(K)/Lp - C1;
  absR = abs(R);
  print("  c_K at K=", K, " = ", cK);
  print("  |R(K)| at K=", K, " (L2) = ", absR);
  print("  |R(K)| at K=", K, " (L1 ref) = ", ref_absR);
  print("");
  return(0);
};

print("# PARI/GP L2 cross-check");
print("# PARI version: ", version());
print("# realprecision = ", default(realprecision));
print("# K_test = ", K_test);
print("");

do_pair("chi_-4/z1", L_chim4, t1, ref_absLp_1, ref_absLpp_1, ref_absC1_1, ref_absR_1, c_K_chim4, K_test);
do_pair("chi_-4/z2", L_chim4, t2, ref_absLp_2, ref_absLpp_2, ref_absC1_2, ref_absR_2, c_K_chim4, K_test);
do_pair("chi_5",     chi5,    t3, ref_absLp_3, ref_absLpp_3, ref_absC1_3, ref_absR_3, c_K_5,     K_test);
do_pair("chi_11",    chi11,   t4, ref_absLp_4, ref_absLpp_4, ref_absC1_4, ref_absR_4, c_K_11,    K_test);

print("# done");
quit;
