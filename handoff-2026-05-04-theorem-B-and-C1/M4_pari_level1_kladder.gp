/* M4 hours-test: level-1 weights k = 16, 18, 20, 22, 26 (rational newforms,
   one each in S_k(SL2Z)). Numerical Theorem B sanity at increasing weight.
   PARI/GP 2.17 compatible. Adapted from B3_pari_higher_k_FIXED.gp. */

default(realprecision, 19);
default(parisize, 2000000000);
default(parisizemax, 8000000000);

test_lfun(Lraw) = lfunan(Lraw, 2);
pick_L(Lraw) = {
  my(ok);
  ok = iferr(test_lfun(Lraw), E, 0);
  if (ok == 0,
    print("lfunmf returned vector; using #1");
    return(Lraw[1]),
    return(Lraw)
  );
};

cf_euler(L, N, k, Pmax) = {
  my(an, prod_val, lam_p, ap, local_factor);
  an = lfunan(L, Pmax);
  prod_val = 1.0;
  forprime(p = 2, Pmax,
    if (N % p != 0,
      ap = an[p];
      lam_p = ap / p^((k-1)/2.0);
      local_factor = (1 + 1.0/p) / (1 - (lam_p^2 - 2)/p + 1.0/p^2);
      prod_val = prod_val * local_factor;
    );
  );
  return(prod_val);
};

safe_lfun_deriv(L, s) = iferr(lfun(L, s, 1), E, 0);
compute_U(L, central, n_zeros, zs) = {
  my(U, val);
  U = 0.0;
  for(j = 1, n_zeros,
    val = safe_lfun_deriv(L, central + I*zs[j]);
    U = U + abs(val)^2;
  );
  return(U);
};

process_level1(k, T_max, n_zeros_target, Pmax) = {
  my(mf, basis, F, L, Lraw, central, zs, n_zeros, U, T, cf, logCan, logX, u_logT, u_logX, u_logCan);
  print();
  print("=== level=1, k=", k, "  T_max=", T_max, " ===");
  mf = mfinit([1, k], 1);
  basis = mfeigenbasis(mf);
  print("  #newforms in S_", k, "^new(SL2Z): ", #basis);
  F = basis[1];
  Lraw = lfunmf(mf, F);
  L = pick_L(Lraw);
  central = k/2.0;
  zs = lfunzeros(L, T_max);
  n_zeros = min(n_zeros_target, #zs);
  print("  Zeros found up to T=", T_max, ": ", #zs, "; using ", n_zeros);
  if (n_zeros == 0, print("  ABORT: no zeros"); return(0));
  U = compute_U(L, central, n_zeros, zs);
  T = zs[n_zeros];
  cf = iferr(cf_euler(L, 1, k, Pmax), E, print("  cf_euler ERRORED"); -1.0);
  logCan = log(1 * (k/(4*Pi))^2 * T^2);
  logX = logCan / 2;
  u_logT = U / (cf * T * log(T)^4);
  u_logX = U / (cf * T * logX^4);
  u_logCan = U / (cf * T * logCan^4);
  print("  U                  = ", U);
  print("  T                  = ", T);
  print("  c_f (Euler, P=", Pmax, ")= ", cf);
  print("  log T              = ", log(T));
  print("  log X              = ", logX);
  print("  log Can            = ", logCan);
  print("  u_norm (log T)^4   = ", u_logT);
  print("  u_norm (log X)^4   = ", u_logX);
  print("  u_norm * zeta(2)   = ", u_logT * Pi^2/6);
  print("  [target 2/(3*pi)   = ", 2/(3*Pi), "]");
  return(0);
};

print("=========================================================");
print("M4: Level-1 k=16,18,20,22,26 numerical Theorem B test");
print("=========================================================");

process_level1(16, 200, 60, 3000);
process_level1(18, 200, 60, 3000);
process_level1(20, 200, 60, 3000);
process_level1(22, 200, 60, 3000);
process_level1(26, 200, 60, 3000);

print();
print("DONE");
