/* G8 v4: PARI re-anchor with σ = k/2 (PARI arithmetic crit line).
 * Cleaner orbit handling: run_test_one expects a single Lmisc.
 * run_orbit dispatches: try direct, if fails iterate.
 */

default(parisizemax, "4G");
default(realprecision, 30);

PI = Pi;
A4 = 2/(3*PI);
CAGE_LO = (17 - sqrt(145)) / (12 * PI);
CAGE_HI = (17 + sqrt(145)) / (12 * PI);

cf_truncated(L, k, x) = {
  my(an = lfunan(L, x));
  my(S = sum(n=1, x, an[n]^2 / n^(k-1)));
  return(S / x);
};

run_test_one(L, q, k, T_list, label) = {
  print("\n--- ", label, " | q=", q, " k=", k, " σ=k/2=", k/2, " ---");
  my(cf_5k = cf_truncated(L, k, 5000));
  my(cf_20k = cf_truncated(L, k, 20000));
  printf("  c_f truncated: x=5k → %.6f,  x=20k → %.6f  (drift %.3f%%)\n",
         cf_5k, cf_20k, 100*(cf_20k-cf_5k)/cf_20k);
  my(cf = cf_20k);
  my(sigma = k/2);
  printf("    T  | N_f(T) | Σ|L'|^2          | pred             | u_f      | Y     | in_cage[%.4f, %.4f]\n",
         CAGE_LO, CAGE_HI);
  for(ti = 1, #T_list,
    my(T = T_list[ti]);
    my(zeros = lfunzeros(L, T));
    my(nz = #zeros);
    my(Sf = 0.0);
    for(j = 1, nz, Sf += abs(lfun(L, sigma + I*zeros[j], 1))^2);
    my(Y = log(sqrt(q * T / (2*PI))));
    my(pred = A4 * cf * T * Y^4);
    my(u_f = Sf / (cf * T * Y^4));
    my(in_cage = if(u_f >= CAGE_LO && u_f <= CAGE_HI, "Y", "N"));
    printf("  %5d | %4d | %16.6f | %16.6f | %.4f   | %.3f | %s\n",
           T, nz, Sf, pred, u_f, Y, in_cage);
  );
};

run_orbit(M, k, q, T_list, label_prefix) = {
  my(B = mfeigenbasis(M));
  print("\n[", label_prefix, "]: ", #B, " orbit(s)");
  for(orb = 1, #B,
    my(Lvec = lfunmf(M, B[orb]));
    my(direct_ok = 0);
    iferr(lfunparams(Lvec); direct_ok = 1, E, direct_ok = 0);
    if(direct_ok,
      run_test_one(Lvec, q, k, T_list, concat([label_prefix, " orb#", Str(orb)])),
      print("  orbit ", orb, " has ", #Lvec, " embeddings");
      for(emb = 1, #Lvec,
        iferr(
          run_test_one(Lvec[emb], q, k, T_list,
                       concat([label_prefix, " orb#", Str(orb), " emb#", Str(emb)])),
          E2,
          print("    SKIP emb ", emb, ": ", E2)
        )
      )
    );
  );
};

print("\n############ k=12 (Delta) ############");
run_orbit(mfinit([1, 12], 1), 12, 1, [50, 100, 200, 400], "wt12_L1");

print("\n############ k=24 ############");
run_orbit(mfinit([1, 24], 1), 24, 1, [50, 100, 200], "wt24_L1");

print("\n############ k=36 ############");
run_orbit(mfinit([1, 36], 1), 36, 1, [50, 100, 200], "wt36_L1");

print("\n############ k=2 level 11 (11a1 sanity) ############");
run_orbit(mfinit([11, 2], 1), 2, 11, [50, 100, 200, 400], "wt2_L11");

print("\n=== DONE ===");
quit;
