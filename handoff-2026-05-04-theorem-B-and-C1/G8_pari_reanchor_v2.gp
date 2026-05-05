/* G8 v2: PARI re-anchor at sigma=1/2 (M-N convention from arXiv:1306.0854 eq 16).
 *
 * Conjecture (16): Σ_{0<γ_f ≤ T} |L'(ρ_f, f)|^2 ~ (2/(3π)) · c_f · T · log^4 X
 *   ρ_f = 1/2 + iγ_f, X = sqrt(qT/(2π)),
 *   c_f := lim_{x→∞} (1/x) Σ_{n≤x} |λ_f(n)|^2,    λ_f(n) = a_f(n) / n^((k-1)/2).
 *
 * Fixes vs v1:
 *  (1) Analytic normalization: a_n^2 / n^(k-1) inside the c_f truncated sum.
 *      v1 used raw a_n^2 → blew up to 10^39 for k=12.
 *  (2) Galois orbits: mfeigenbasis returns one entry PER orbit (not per form).
 *      For wt-24 level 1 there are 2 orbit reps; lfunmf picks one rational embedding.
 *      Catch errors and skip if lfunmf can't make L-function for that representative.
 *  (3) c_f tested at multiple x's to verify convergence (residue stable).
 *  (4) Increased parisizemax via setting at script start.
 *  (5) Sanity check: also compute on EC L-function (k=2 level 11) which has
 *      independent locked value u_f = 0.3455 from Convention_reconciliation.md.
 */

default(parisizemax, "2G");
default(realprecision, 30);

PI = Pi;
A4 = 2/(3*PI);
CAGE_LO = (17 - sqrt(145)) / (12 * PI);   /* approx 0.13 */
CAGE_HI = (17 + sqrt(145)) / (12 * PI);   /* approx 0.78 */
\\ But G2 file sometimes references [0.0524, 0.7854]; use that wider cage too.
CAGE_LO_G2 = 1/(6*PI);
CAGE_HI_G2 = 1/(4) + 1/(4*PI);   \\ placeholder; the user said [0.0524, 0.7854]

\\ ---- c_f (Rankin-Selberg residue, analytic norm) -----------------------------
cf_truncated(L, k, x) = {
  my(an, S);
  an = lfunan(L, x);
  S = sum(n=1, x, an[n]^2 / n^(k-1));
  return(S / x);
};

\\ ---- main test ---------------------------------------------------------------
run_test(L, q, k, T_list, label) = {
  my(zeros, nz, T, Y, Sf, ratio, cf_5k, cf_20k, cf, pred);
  print("\n=== ", label, "  q=", q, "  k=", k, " ===");
  cf_5k  = cf_truncated(L, k, 5000);
  cf_20k = cf_truncated(L, k, 20000);
  printf("  c_f (x=5000)  = %.8f\n", cf_5k);
  printf("  c_f (x=20000) = %.8f\n", cf_20k);
  printf("  c_f drift 5k->20k: %.4f%%\n", 100*(cf_20k - cf_5k) / cf_20k);
  cf = cf_20k;
  printf("  ----- T  | N_f(T) |  Σ|L'(ρ,f)|^2  |  pred (a4*cf*T*Y^4) | ratio | dimless u_f | Y\n");
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
    \\ "dimless u_f" = Sf / (cf * T * Y^4) — should converge to 2/(3π) ≈ 0.21221.
    u_f = Sf / (cf * T * Y^4);
    printf("  T=%5d | N=%4d | %14.4f | %14.4f | %.4f | u_f=%.4f | Y=%.3f\n",
           T, nz, Sf, pred, ratio, u_f, Y);
  );
};

\\ ----- (a) f = Δ, weight 12, level 1 -----
{
  my(M, B, L);
  M = mfinit([1, 12], 1);
  B = mfeigenbasis(M);
  print("\n[wt 12 level 1]: ", #B, " orbit(s) (expect 1: Δ)");
  L = lfunmf(M, B[1]);
  run_test(L, 1, 12, [50, 100, 200, 400], "Delta (k=12, q=1)");
}

\\ ----- (b) weight 24, level 1 -----
{
  my(M, B);
  M = mfinit([1, 24], 1);
  B = mfeigenbasis(M);
  print("\n[wt 24 level 1]: ", #B, " orbit(s) (expect 1 orbit of dim 2)");
  for(i = 1, #B,
    print("  orbit ", i, ":");
    iferr(
      run_test(lfunmf(M, B[i]), 1, 24, [50, 100, 200], concat("wt-24 L1 #", Str(i))),
      E,
      print("    SKIP (lfunmf failed: ", E, ")")
    );
  );
}

\\ ----- (c) weight 36, level 1 (proxy for k=36) -----
{
  my(M, B);
  M = mfinit([1, 36], 1);
  B = mfeigenbasis(M);
  print("\n[wt 36 level 1]: ", #B, " orbit(s)");
  for(i = 1, #B,
    print("  orbit ", i, ":");
    iferr(
      run_test(lfunmf(M, B[i]), 1, 36, [50, 100, 200], concat("wt-36 L1 #", Str(i))),
      E,
      print("    SKIP (lfunmf failed: ", E, ")")
    );
  );
}

\\ ----- (d) sanity check: 11a1 EC = wt-2 level-11 newform -----
{
  my(M, B, L);
  M = mfinit([11, 2], 1);
  B = mfeigenbasis(M);
  print("\n[wt 2 level 11]: ", #B, " orbit(s) (expect 1: 11a1)");
  L = lfunmf(M, B[1]);
  run_test(L, 11, 2, [50, 100, 200, 400], "11a1 sanity (k=2, q=11)");
}

print("\n=== DONE ===");
quit;
