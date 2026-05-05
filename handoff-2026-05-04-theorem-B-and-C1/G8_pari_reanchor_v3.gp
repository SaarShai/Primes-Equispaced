/* G8 v3: PARI re-anchor, CORRECTED CRITICAL LINE σ = k/2.
 *
 * KEY FIX vs v1/v2:
 *   PARI's lfunmf(M, F) returns the L-function in ARITHMETIC normalization,
 *   where the critical line is σ = k/2, NOT σ = 1/2.
 *   Equivalently: PARI L_a(s) = L_analytic(s - (k-1)/2).
 *   Derivatives transform by chain rule (shift only): |L_a'(k/2 + iγ)| = |L_an'(1/2 + iγ)|.
 *   So evaluate at σ = k/2 to get M-N's σ=1/2 quantity.
 *
 * c_f: analytic normalization, λ_f(n) = a_f(n) / n^((k-1)/2)
 *      c_f := lim (1/x) Σ_{n≤x} |λ_f(n)|^2  =  L(1, sym²f) / ζ(2)  (level 1)
 *
 * Galois orbits: lfunmf(M, F) returns a t_VEC of L-functions when F is over
 * a number field (orbit dim > 1). Iterate over each embedding L[j].
 *
 * Conjecture (M-N eq 16): Σ_{0<γ_f ≤ T} |L'(ρ_f, f)|^2 ~ a_4 · c_f · T · log^4 X
 *   a_4 = 2/(3π) ≈ 0.21221
 *   X = sqrt(qT/(2π))
 *
 * Cage (G2 unconditional): center 17/(12π) ≈ 0.4509,
 *                          half-width sqrt(145)/(12π) ≈ 0.3193,
 *                          cage = [(17-sqrt(145))/(12π), (17+sqrt(145))/(12π)]
 *                                ≈ [0.1316, 0.7702].
 * a_4 = 2/(3π) ≈ 0.2122 lies inside cage.
 */

default(parisizemax, "4G");
default(realprecision, 30);

PI = Pi;
A4 = 2/(3*PI);
CAGE_LO = (17 - sqrt(145)) / (12 * PI);
CAGE_HI = (17 + sqrt(145)) / (12 * PI);

cf_truncated(L, k, x) = {
  my(an, S);
  an = lfunan(L, x);
  S = sum(n=1, x, an[n]^2 / n^(k-1));
  return(S / x);
};

run_test_one(L, q, k, T_list, label) = {
  my(zeros, nz, T, Y, Sf, ratio, cf_5k, cf_20k, cf, pred, sigma);
  print("\n=== ", label, "  q=", q, "  k=", k, "  σ_crit=k/2=", k/2, " ===");
  cf_5k  = cf_truncated(L, k, 5000);
  cf_20k = cf_truncated(L, k, 20000);
  cf = cf_20k;
  printf("  c_f truncated:  x=5k → %.6f,  x=20k → %.6f  (drift %.3f%%)\n",
         cf_5k, cf_20k, 100*(cf_20k-cf_5k)/cf_20k);
  sigma = k/2;
  printf("  --- evaluating |L'(σ + iγ)|^2 at σ = %s ---\n", Str(sigma));
  printf("    T  | N_f(T) | Σ|L'|^2     | pred        | ratio_a4 | u_f       | Y      | cage in [%.4f, %.4f]\n",
         CAGE_LO, CAGE_HI);
  for(ti = 1, #T_list,
    T = T_list[ti];
    zeros = lfunzeros(L, T);
    nz = #zeros;
    Sf = 0.0;
    for(j = 1, nz, Sf += abs(lfun(L, sigma + I*zeros[j], 1))^2);
    Y = log(sqrt(q * T / (2*PI)));
    pred = A4 * cf * T * Y^4;
    ratio = Sf / pred;
    u_f = Sf / (cf * T * Y^4);
    in_cage = if(u_f >= CAGE_LO && u_f <= CAGE_HI, "Y", "N");
    printf("  %5d | %4d | %10.4f | %10.4f | %.4f   | %.4f    | %.3f  | in_cage=%s\n",
           T, nz, Sf, pred, ratio, u_f, Y, in_cage);
  );
};

run_orbit(M, k, q, T_list, label_prefix) = {
  my(B, Lvec);
  B = mfeigenbasis(M);
  print("\n[", label_prefix, "]: ", #B, " orbit(s)");
  for(orb = 1, #B,
    Lvec = lfunmf(M, B[orb]);
    if(type(Lvec) == "t_VEC" && #Lvec > 0 && type(Lvec[1]) != "t_INT",
      \\ Could be either a vector of L-fns (Galois orbit dim > 1) OR a single Lmisc.
      \\ Heuristic: if Lvec is one of {[N, k, gamma], ...}, it's a single L-fn.
      \\ Use lfunparams to test:
      iferr(
        ( my(p = lfunparams(Lvec));
          \\ If lfunparams works, Lvec IS a single L-function:
          run_test_one(Lvec, q, k, T_list, concat(label_prefix, " orbit#", Str(orb)))
        ),
        E,
        \\ lfunparams failed → Lvec is a t_VEC of L-fns; iterate
        for(emb = 1, #Lvec,
          iferr(
            run_test_one(Lvec[emb], q, k, T_list,
                         concat(label_prefix, " orbit#", Str(orb), " emb#", Str(emb))),
            E2,
            print("    SKIP emb ", emb, ": ", E2)
          )
        )
      ),
      print("  unexpected Lvec type: ", type(Lvec))
    );
  );
};

\\ === Tests ===
{
  print("\n############ k=12 (Delta) ############");
  run_orbit(mfinit([1, 12], 1), 12, 1, [50, 100, 200, 400], "wt12_L1");
}
{
  print("\n############ k=24 ############");
  run_orbit(mfinit([1, 24], 1), 24, 1, [50, 100, 200], "wt24_L1");
}
{
  print("\n############ k=36 ############");
  run_orbit(mfinit([1, 36], 1), 36, 1, [50, 100, 200], "wt36_L1");
}
{
  print("\n############ k=2, level 11 (11a1, sanity check) ############");
  run_orbit(mfinit([11, 2], 1), 2, 11, [50, 100, 200, 400], "wt2_L11");
}

print("\n=== DONE ===");
quit;
