/* M5_full_polynomial_anchor.gp
   Theorem B empirical anchor closure: include lower-order polynomial corrections.

   Empirical: u_emp = U_f / (c_f · T · Y^4),  Y = log X
   Predicted (full polynomial through order Y^2):
     u_pred = (2/(3*Pi)) * [1 + (a3/a4)/Y + (a2/a4)/Y^2]
   with
     a3/a4 = -4 + 4 B(f)
     a2/a4 = 12 - 12 B(f) + 6 B(f)^2 + 6 kappa_2(f)
     B(f)   = gamma_E + (L'/L)(1, sym^2 f) - 2 (zeta'/zeta)(2) + sum_{p|N} log(p)/(p+1)
     kappa_2(f) = (3/4)*[(L''/L)(1) - ((L'/L)(1))^2] - (1/2) k2_mult - (1/4) k2_add - log(2*Pi)
   where (L'/L)(1) and (L''/L)(1) are at s=1 of sym^2 f.
   k2_mult = sum_{p || N} (log p)^2 [ p/(p+1)^2 + 2 (1/p)/(1+1/p) ]
   k2_add  = sum_{p^2 | N} (log p)^2 [ 1/(1-1/p)^2 + (1/p^2)/(1-1/p^2)^2 ]
*/

default(realprecision, 30);
default(parisize, 2000000000);
default(parisizemax, 16000000000);

GAMMA_E = Euler;
LOG2PI  = log(2*Pi);

/* (zeta'/zeta)(2) numerical */
ZETAP_OVER_ZETA_2 = zeta'(2)/zeta(2);

/* B(f) - arithmetic constant */
compute_Bf(LpL_sym2, N) = {
  my(B, fac);
  B = GAMMA_E + LpL_sym2 - 2*ZETAP_OVER_ZETA_2;
  fac = factor(N);
  for(i=1, matsize(fac)[1],
    my(p = fac[i,1]);
    B = B + log(p)/(p + 1);
  );
  return(B);
};

/* k2_mult: sum over primes p with p || N (p^1 exact) */
compute_k2mult(N) = {
  my(s, fac);
  s = 0.0;
  fac = factor(N);
  for(i=1, matsize(fac)[1],
    my(p = fac[i,1], e = fac[i,2]);
    if (e == 1,
      s = s + log(p)^2 * ( p/(p+1)^2 + 2*(1.0/p)/(1+1.0/p) );
    );
  );
  return(s);
};

/* k2_add: sum over primes p with p^2 | N */
compute_k2add(N) = {
  my(s, fac);
  s = 0.0;
  fac = factor(N);
  for(i=1, matsize(fac)[1],
    my(p = fac[i,1], e = fac[i,2]);
    if (e >= 2,
      s = s + log(p)^2 * ( 1/(1-1.0/p)^2 + (1.0/p^2)/(1-1.0/p^2)^2 );
    );
  );
  return(s);
};

/* kappa_2(f) */
compute_kappa2(LpL, LppL, N) = {
  my(L_cum, k2m, k2a);
  L_cum = LppL - LpL^2;
  k2m   = compute_k2mult(N);
  k2a   = compute_k2add(N);
  return( (3/4)*L_cum - (1/2)*k2m - (1/4)*k2a - LOG2PI );
};

/* Predicted u from full polynomial */
predict_u(B, kappa2, Y) = {
  my(a4, a3_a4, a2_a4);
  a4    = 2/(3*Pi);
  a3_a4 = -4 + 4*B;
  a2_a4 = 12 - 12*B + 6*B^2 + 6*kappa2;
  return( a4 * (1 + a3_a4/Y + a2_a4/Y^2) );
};

/* ---------------- 16-curve k=2 EC ladder ---------------- */
print("=========================================================");
print("M5: Theorem B empirical anchor — full polynomial closure");
print("=========================================================");

curves_k2 = ["11a1","14a1","15a1","17a1","19a1","20a1","21a1","24a1","100a1","106c1","200a1","221a1","240a1","496b1","510a1","5005b1"];
T_per_k2 = [177.16, 172.02, 171.10, 168.91, 166.78, 166.04, 164.70, 162.91, 141.43, 140.91, 132.92, 131.73, 131.01, 123.19, 123.25, 103.35];
u_emp_k2 = [0.345521, 0.239653, 0.275617, 0.321003, 0.279709, 0.365606, 0.238284, 0.228532, 0.340792, 0.183107, 0.185041, 0.156095, 0.150776, 0.212444, 0.131076, 0.214511];

print();
print("### Section 1: 16 EC k=2 curves ###");
print();
printf("%-8s %4s %7s %7s %7s %7s %7s %7s %7s %7s\n", "curve","N","T","Y","B(f)","kap2","u_emp","u_pred","ratio","diff%");

ratios_k2 = List([]);
for(i=1, #curves_k2,
  cn = curves_k2[i];
  E = ellinit(cn);
  N = ellglobalred(E)[1];
  T = T_per_k2[i];
  X = sqrt(N)*T/(2*Pi);
  Y = log(X);

  /* L'/L and L''/L at s=1 of sym^2 f via central-difference */
  Lsym = lfunsympow(E, 2);
  h = 1e-6;
  v0  = lfun(Lsym, 1);
  vph = lfun(Lsym, 1+h);
  vmh = lfun(Lsym, 1-h);
  vp2h = lfun(Lsym, 1+2*h);
  vm2h = lfun(Lsym, 1-2*h);

  /* 5-point stencil */
  L1 = (-vp2h + 8*vph - 8*vmh + vm2h)/(12*h);
  L2 = (-vp2h + 16*vph - 30*v0 + 16*vmh - vm2h)/(12*h^2);

  LpL  = L1 / v0;
  LppL = L2 / v0;

  Bf = compute_Bf(LpL, N);
  k2 = compute_kappa2(LpL, LppL, N);

  u_p = predict_u(Bf, k2, Y);
  u_e = u_emp_k2[i];
  ratio = u_e / u_p;

  printf("%-8s %4d %7.2f %7.3f %+7.3f %+7.2f %7.4f %7.4f %7.3f %+6.1f%%\n",
         cn, N, T, Y, Bf, k2, u_e, u_p, ratio, 100*(ratio-1));
  listput(ratios_k2, ratio);
);

print();
ratios_v = Vec(ratios_k2);
mean_r = vecsum(ratios_v)/#ratios_v;
var_r = vecsum(apply(x -> (x-mean_r)^2, ratios_v))/#ratios_v;
print("k=2 EC ladder ratio mean = ", mean_r);
print("k=2 EC ladder ratio std  = ", sqrt(var_r));
print("Target: ratio -> 1 within 5% means 0.95 < ratio < 1.05");

/* ---------------- Level 1, weights k=16,18,20,22,26 ---------------- */
print();
print("### Section 2: 5 level-1 newforms, weights k = 16,18,20,22,26 ###");
print();

/* Empirical data from M4_pari_level1_kladder.gp output, repeated in M4 .md:
     k=16: T=99.31, U=1277.5, c_f=0.615, u(logT)^4=0.0468  (u using log T not log X)
     k=18: T=98.47, U=1244.4, c_f=0.755, u(logT)^4=0.0377
     k=20: T=98.82, U=1057.8, c_f=0.627, u(logT)^4=0.0384
     k=22: T=97.10, U=975.4,  c_f=0.573, u(logT)^4=0.0400
     k=26: T=96.15, U=894.0,  c_f=0.480, u(logT)^4=0.0446

   For weight-k level-1, X = sqrt(N) * k * T / (4*Pi) = k*T/(4*Pi) (N=1).
   Recompute u_emp using Y = log X here (the proper M-N analytic conductor log).
*/
weights = [16, 18, 20, 22, 26];
T_per_lvl1 = [99.31, 98.47, 98.82, 97.10, 96.15];
U_per_lvl1 = [1277.5, 1244.4, 1057.8, 975.4, 894.0];
cf_per_lvl1 = [0.615, 0.755, 0.627, 0.573, 0.480];

printf("%-3s %7s %7s %7s %7s %7s %7s %7s %7s %7s\n", "k","T","Y_X","B(f)","kap2","u_emp","u_pred","ratio","diff%","note");
ratios_lvl1 = List([]);

for(i=1, #weights,
  k = weights[i];
  T = T_per_lvl1[i];
  N = 1;
  /* Analytic conductor: X = k*T/(4*Pi) for level 1 weight k */
  X = k*T/(4*Pi);
  Y = log(X);
  U = U_per_lvl1[i];
  cf = cf_per_lvl1[i];
  /* u_emp with Y=log(X) */
  u_emp = U / (cf * T * Y^4);

  /* B(f), kappa_2: need (L'/L)(1, sym^2 f) and (L''/L)(1, sym^2 f) for the
     newform of weight k. For weight k newforms, sym^2 lift exists via Gelbart-Jacquet.
     Compute via mfinit + lfunmf + sympow lift. */
  mf = mfinit([1, k], 1);
  basis = mfeigenbasis(mf);
  F = basis[1];
  /* Use mfsymsq if available, else fall back to direct Euler product attempt */
  Lsym = lfunsympow(F, 2);
  h = 1e-6;
  v0 = lfun(Lsym, 1);
  vph = lfun(Lsym, 1+h);
  vmh = lfun(Lsym, 1-h);
  vp2h = lfun(Lsym, 1+2*h);
  vm2h = lfun(Lsym, 1-2*h);

  L1 = (-vp2h + 8*vph - 8*vmh + vm2h)/(12*h);
  L2 = (-vp2h + 16*vph - 30*v0 + 16*vmh - vm2h)/(12*h^2);

  LpL  = L1/v0;
  LppL = L2/v0;

  /* B(f), kappa_2 with N=1 (no bad-prime sums) */
  Bf = compute_Bf(LpL, N);
  k2 = compute_kappa2(LpL, LppL, N);

  u_p = predict_u(Bf, k2, Y);
  ratio = u_emp / u_p;

  printf("%-3d %7.2f %7.3f %+7.3f %+7.2f %7.4f %7.4f %7.3f %+6.1f%% %s\n",
         k, T, Y, Bf, k2, u_emp, u_p, ratio, 100*(ratio-1), "");
  listput(ratios_lvl1, ratio);
);

print();
ratios_v2 = Vec(ratios_lvl1);
mean_r2 = vecsum(ratios_v2)/#ratios_v2;
var_r2 = vecsum(apply(x -> (x-mean_r2)^2, ratios_v2))/#ratios_v2;
print("Level-1 ladder ratio mean = ", mean_r2);
print("Level-1 ladder ratio std  = ", sqrt(var_r2));

/* ---------------- Combined ---------------- */
print();
print("### Combined statistics ###");
all_r = concat(ratios_v, ratios_v2);
mean_all = vecsum(all_r)/#all_r;
var_all = vecsum(apply(x -> (x-mean_all)^2, all_r))/#all_r;
print("Combined N=", #all_r, " ratio mean = ", mean_all, "  std = ", sqrt(var_all));
print();
print("Verdict:");
if(abs(mean_all - 1) < 0.05 && sqrt(var_all) < 0.10,
  print("  THEOREM B EMPIRICAL ANCHOR LOCKED to within 5%."),
  print("  Gap remains. mean=", mean_all, "; need diagnosis on which a_j coefficient.")
);

print();
print("=========================================================");
print("DONE");
print("=========================================================");
quit;
