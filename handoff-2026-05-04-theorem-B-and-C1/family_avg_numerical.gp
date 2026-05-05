/* family_avg_numerical.gp
 * Family-averaged Theorem B numerical test.
 * Conventions match G8 v4 (sigma=k/2, c_f=(1/x)Sum|a_n|^2/n^(k-1) at x=20000,
 * Y=log(sqrt(q*T/(2*Pi))), prediction A4=2/(3*Pi)).
 *
 * Wrapped in main() to avoid gp top-level newline parsing issues.
 */

default(parisizemax, "8G");
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

compute_uf(L, q, k, T_list, label) = {
  print("\n--- ", label, " | q=", q, " k=", k, " sigma=", k/2, " ---");
  my(cf = cf_truncated(L, k, 20000));
  printf("  c_f (x=20000) = %.6f\n", cf);
  my(sigma = k/2);
  my(rows = vector(#T_list));
  for(ti = 1, #T_list,
    my(T = T_list[ti]);
    my(t0 = getwalltime());
    my(zeros = lfunzeros(L, T));
    my(nz = #zeros);
    my(Sf = 0.0);
    for(j = 1, nz, Sf += abs(lfun(L, sigma + I*zeros[j], 1))^2);
    my(Y = log(sqrt(q * T / (2*PI))));
    my(u_f = Sf / (cf * T * Y^4));
    my(elapsed = (getwalltime() - t0)/1000.0);
    my(in_cage = if(u_f >= CAGE_LO && u_f <= CAGE_HI, 1, 0));
    rows[ti] = [T, nz, Sf, cf, Y, u_f, in_cage];
    printf("  T=%5d | N_f=%4d | Sf=%14.4f | cf=%.4f | Y=%.3f | u_f=%.4f | cage=%d | (%.1fs)\n",
           T, nz, Sf, cf, Y, u_f, in_cage, elapsed);
  );
  return(rows);
};

main() = {
  my(T_list_A = [100, 200, 400, 800, 1500]);
  my(T_list_B = [100, 200, 400, 800, 1500]);

  print("\n##############################################################");
  print("FAMILY A: 14 small squarefree-level k=2 elliptic curves");
  print("##############################################################");

  my(family_A_labels = ["11a1","14a1","15a1","17a1","19a1","21a1","26a1","33a1","35a1","37a1","38a1","43a1","53a1","57a1"]);
  my(A_results = vector(#family_A_labels));
  for(i = 1, #family_A_labels,
    my(lbl = family_A_labels[i]);
    print("\n>>> Curve ", i, "/", #family_A_labels, ": ", lbl);
    my(E = ellinit(lbl));
    my(N = ellglobalred(E)[1]);
    my(L = lfuncreate(E));
    A_results[i] = compute_uf(L, N, 2, T_list_A, lbl);
  );

  print("\n##############################################################");
  print("FAMILY B: Delta (k=12 cusp form at level 1)");
  print("##############################################################");

  my(M = mfinit([1, 12], 1));
  my(B_basis = mfeigenbasis(M));
  print("  #orbits at [1,12] = ", #B_basis);
  my(B_results = vector(#B_basis));
  for(orb = 1, #B_basis,
    my(Lvec = lfunmf(M, B_basis[orb]));
    B_results[orb] = compute_uf(Lvec, 1, 12, T_list_B, concat(["Delta_orb", Str(orb)]));
  );

  print("\n##############################################################");
  print("AGGREGATION: family-averaged u_bar(T)");
  print("##############################################################");

  print("\n--- Family A (k=2, |F|=", #family_A_labels, ") ---");
  printf("  T     | mean u  | min u  | max u  | sd     | in_cage | mean_in_cage\n");
  for(ti = 1, #T_list_A,
    my(T = T_list_A[ti]);
    my(uvals = vector(#A_results, i, A_results[i][ti][6]));
    my(mu = sum(i=1, #uvals, uvals[i]) / #uvals);
    my(mn = vecmin(uvals));
    my(mx = vecmax(uvals));
    my(var = sum(i=1, #uvals, (uvals[i]-mu)^2) / #uvals);
    my(sd = sqrt(var));
    my(ncage = sum(i=1, #A_results, A_results[i][ti][7]));
    my(mu_in_cage = if(mu >= CAGE_LO && mu <= CAGE_HI, "Y", "N"));
    printf("  %5d | %.4f | %.4f | %.4f | %.4f | %2d/%d   | %s\n",
           T, mu, mn, mx, sd, ncage, #A_results, mu_in_cage);
  );

  print("\n--- Family B (k=12 Delta) ---");
  printf("  T     | u_f      | in_cage | dev from %.4f\n", A4);
  for(ti = 1, #T_list_B,
    my(T = T_list_B[ti]);
    for(orb = 1, #B_results,
      my(u = B_results[orb][ti][6]);
      my(c = B_results[orb][ti][7]);
      printf("  %5d | %.6f | %d       | %+.4f\n", T, u, c, u - A4);
    );
  );

  print("\n--- Predicted A4 = 2/(3*Pi) = ", A4, " ---");
  print("--- Cage = [", CAGE_LO, ", ", CAGE_HI, "] ---");

  /* Per-curve table dump for the report */
  print("\n##############################################################");
  print("PER-CURVE TABLE (Family A)");
  print("##############################################################");
  for(i = 1, #family_A_labels,
    my(lbl = family_A_labels[i]);
    print("\n  ", lbl, ":");
    for(ti = 1, #T_list_A,
      my(r = A_results[i][ti]);
      printf("    T=%5d  u_f=%.4f  cage=%d\n", r[1], r[6], r[7]);
    );
  );
};

main();
print("\n=== DONE ===");
quit;
