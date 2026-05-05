/* G8: PARI re-anchor at sigma=1/2 (M-N convention from arXiv:1306.0854 eq 16).
 *
 * Conjecture (16): Σ_{0<γ_f ≤ T} |L'(ρ_f, f)|^2 ~ (2/(3π)) · c_f · T · log^4 X
 * where ρ_f = 1/2 + iγ_f, X = sqrt(qT/(2π)),
 *       c_f = lim (1/x) Σ_{n≤x} |λ_f(n)|^2  =  Ress=1 L(s, f x bar f).
 */

default(realprecision, 30);

PI = Pi;
A4 = 2/(3*PI);

\\ Compute c_f via the Rankin-Selberg sum: c_f = lim (1/x) Σ_{n<=x} |λ_f(n)|^2.
\\ Use Dirichlet coeffs of L (which are λ_f(n) since lfunmf returns the analytic normalization).
compute_cf(L, x_lim) = {
  my(an, S);
  an = lfunan(L, x_lim);
  S = sum(n=1, x_lim, abs(an[n])^2);
  return( S / x_lim );
};

run_test(L, q, T_list, label) = {
  my(zeros, nz, T, Y, Sf, ratio, cf, pred);
  print("\n=== ", label, "  q=", q, " ===");
  cf = compute_cf(L, 5000);
  cf2 = compute_cf(L, 20000);
  printf("  c_f (x=5000)  = %.6f\n  c_f (x=20000) = %.6f\n", cf, cf2);
  cf = cf2;
  for(ti = 1, #T_list,
    T = T_list[ti];
    zeros = lfunzeros(L, T);
    nz = #zeros;
    Sf = 0.0;
    for(j = 1, nz,
      Sf += abs( lfun(L, 1/2 + I*zeros[j], 1) )^2;
    );
    Y = log( sqrt(q * T / (2*PI)) );
    pred = A4 * cf * T * Y^4;
    ratio = Sf / pred;
    printf("  T=%5d  N_f(T)=%4d  Σ|L'(ρ,f)|^2 = %.6f   pred = %.6f   ratio = %.4f   Y = %.3f\n",
           T, nz, Sf, pred, ratio, Y);
  );
};

\\ ----- (a) f = Δ, weight 12, level 1 -----
{
  my(M, B, L);
  M = mfinit([1, 12], 1);
  B = mfeigenbasis(M);
  print("\nweight 12 level 1: ", #B, " newform(s) (expect 1: Δ)");
  L = lfunmf(M, B[1]);
  run_test(L, 1, [50, 100, 200, 400], "Δ (k=12, q=1)");
}

\\ ----- (b) weight 24, level 1 -----
{
  my(M, B, L);
  M = mfinit([1, 24], 1);
  B = mfeigenbasis(M);
  print("\nweight 24 level 1: ", #B, " newform(s)");
  for(i = 1, #B,
    L = lfunmf(M, B[i]);
    run_test(L, 1, [50, 100, 200], concat("wt-24 L1 newform #", Str(i)));
  );
}

\\ ----- (c) weight 2, level 11 (squarefree) -----
{
  my(M, B, L);
  M = mfinit([11, 2], 1);
  B = mfeigenbasis(M);
  print("\nweight 2 level 11: ", #B, " newform(s)");
  for(i = 1, #B,
    L = lfunmf(M, B[i]);
    run_test(L, 11, [50, 100, 200, 400], concat("wt-2 L11 newform #", Str(i)));
  );
}

print("\n=== DONE ===");
quit;
