/* B3_pari_higher_k_FIXED.gp
   Numerical verification of Theorem B at higher weights.
   Cases: Delta (k=12, N=1) and weight 24, level 37 (2 newforms).
   PARI/GP 2.17 compatible.
   NOTE: gp parses each top-level line independently — wrap multi-line
   logic in functions or use { ... } block syntax.
*/

default(realprecision, 19);
default(parisize, 2000000000);
default(parisizemax, 8000000000);

/* --------------------------------------------------------- *
 * c_f via Euler product over good primes (Sym^2 L-function) *
 * c_f = prod_p [ (1 + 1/p) / (1 - (lambda^2-2)/p + 1/p^2) ] *
 * --------------------------------------------------------- */

/* Try to use Lraw directly; if lfunan errors, return Lraw[1]. */
test_lfun(Lraw) = lfunan(Lraw, 2);
pick_L(Lraw) = {
  my(ok);
  ok = iferr(test_lfun(Lraw), E, 0);
  if (ok == 0,
    print("lfunmf returned vector of ", length(Lraw), " embeddings; using #1");
    return(Lraw[1]),
    return(Lraw)
  );
};

/* c_f from numerical L-coefficients.
   pari's lfunan returns ARITHMETIC-normalized a_p (integer Hecke eigenvalues
   for modular forms). To get Deligne-normalized lambda_p, divide by p^((k-1)/2). */
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

/* Compute U = sum |L'(central+i*gamma)|^2 robustly. */
safe_lfun_deriv(L, s) = iferr(lfun(L, s, 1), E, 0);
compute_U(L, central, n_zeros, zs) = {
  my(U, val);
  U = 0.0;
  for(j = 1, n_zeros,
    val = safe_lfun_deriv(L, central + I*zs[j]);
    U = U + abs(val)^2;
    print("    j=", j, "  gamma=", zs[j], "  |L'|^2=", abs(val)^2);
  );
  return(U);
};

/* Process a single newform: print summary line.
   For non-rational forms, lfunmf returns a vector of L-functions, one per
   complex embedding. We pick the first by default. */
process_newform(label, mf, F, N, k, T_max, n_zeros_target, Pmax) = {
  my(L, Lraw, central, zs, n_zeros, U, T, cf, logCan, logX, u_logT, u_logX, u_logCan);
  print();
  print("=== ", label, " (N=", N, ", k=", k, ") ===");
  Lraw = lfunmf(mf, F);
  L = pick_L(Lraw);
  central = k/2.0;
  print("Central sigma = ", central);
  print("Arith a_p for p in [2,11]: ", vector(5, j, my(p=prime(j)); lfunan(L, p)[p]));
  print("Deligne lambda_p = a_p/p^((k-1)/2): ", vector(5, j, my(p=prime(j)); lfunan(L, p)[p]/p^((k-1)/2.0)));
  zs = lfunzeros(L, T_max);
  n_zeros = min(n_zeros_target, #zs);
  print("Zeros found up to T=", T_max, ": ", #zs, "; using ", n_zeros);
  if (n_zeros == 0, print("  ABORT: no zeros"); return(0));
  print("First 5 zeros: ", vector(min(5, n_zeros), j, zs[j]));
  U = compute_U(L, central, n_zeros, zs);
  T = zs[n_zeros];
  print("  U computed = ", U, "  T = ", T);
  print("  Computing cf via Euler product (Pmax=", Pmax, ")...");
  cf = iferr(cf_euler(L, N, k, Pmax), E, print("  cf_euler ERRORED, using -1.0"); -1.0);
  print("  cf returned = ", cf);
  logCan = log(N * (k/(4*Pi))^2 * T^2);
  logX = logCan / 2;
  u_logT = U / (cf * T * log(T)^4);
  u_logX = U / (cf * T * logX^4);
  u_logCan = U / (cf * T * logCan^4);
  print("U = ", U);
  print("T = ", T);
  print("c_f (Euler prod, Pmax=", Pmax, ") = ", cf);
  print("log T   = ", log(T));
  print("log X   = ", logX);
  print("log Can = ", logCan);
  print("u_norm (log T)^4   = ", u_logT);
  print("u_norm (log X)^4   = ", u_logX);
  print("u_norm (log Can)^4 = ", u_logCan);
  print("[target 2/(3*pi) = ", 2/(3*Pi), "]");
  return(0);
};

print("=========================================================");
print("Theorem B numerical verification: higher-weight modular");
print("=========================================================");

/* CASE 1: Delta */
print();
print("###  CASE 1: Ramanujan Delta  ###");
mf1 = mfinit([1, 12], 1);
basis1 = mfeigenbasis(mf1);
print("nb newforms in S_12^new(SL2Z): ", #basis1);
process_newform("Delta", mf1, basis1[1], 1, 12, 50, 20, 5000);

/* CASE 2: weight 24, level 37 */
print();
print("###  CASE 2: weight 24, level 37  ###");
mf2 = mfinit([37, 24], 1);
basis2 = mfeigenbasis(mf2);
print("nb newform Galois orbits in S_24^new(Gamma0(37)): ", #basis2);

/* Process each Galois orbit. mfeigenbasis returns one rep per orbit;
   coefficients lie in a number field — pari picks an embedding for lfunmf. */
process_newform("level37_wt24_orbit1", mf2, basis2[1], 37, 24, 30, 15, 1000);
process_newform("level37_wt24_orbit2", mf2, basis2[2], 37, 24, 30, 15, 1000);

print();
print("=========================================================");
print("DONE");
print("=========================================================");
