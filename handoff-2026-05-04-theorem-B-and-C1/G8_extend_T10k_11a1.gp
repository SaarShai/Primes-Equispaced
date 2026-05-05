/* Extend G8 v4 to T=10000 on 11a1 to test possibility (a): slow convergence to 2/(3π) */

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

run_extended(L, q, k, T_list, label) = {
  print("\n--- ", label, " | q=", q, " k=", k, " σ=k/2=", k/2, " ---");
  printf("  Target 2/(3π) = %.6f, cage = [%.4f, %.4f]\n", A4, CAGE_LO, CAGE_HI);
  my(cf_20k = cf_truncated(L, k, 20000));
  printf("  c_f (x=20k) = %.6f\n", cf_20k);
  my(cf = cf_20k);
  my(sigma = k/2);
  printf("\n    T   |  N_f  | Σ|L'|^2            | u_f      | Y      | %% off 2/(3π) | in_cage\n");
  printf("  ------+-------+---------------------+----------+--------+--------------+--------\n");
  for(ti = 1, #T_list,
    my(T = T_list[ti]);
    my(t0 = getwalltime());
    my(zeros = lfunzeros(L, T));
    my(nz = #zeros);
    my(Sf = 0.0);
    for(j = 1, nz, Sf += abs(lfun(L, sigma + I*zeros[j], 1))^2);
    my(Y = log(sqrt(q * T / (2*PI))));
    my(u_f = Sf / (cf * T * Y^4));
    my(pct_off = 100 * (u_f - A4) / A4);
    my(in_cage = if(u_f >= CAGE_LO && u_f <= CAGE_HI, "Y", "N"));
    my(elapsed = (getwalltime() - t0) / 1000.0);
    printf("  %5d | %5d | %19.6f | %.4f   | %.3f  | %+8.1f%%    | %s   (%.1fs)\n",
           T, nz, Sf, u_f, Y, pct_off, in_cage, elapsed);
  );
};

print("\n############ 11a1 EXTENDED to T=10000 ############");
run_extended(lfuncreate(ellinit("11a1")), 11, 2, [400, 800, 1500, 3000, 5000, 10000], "11a1_extended");

print("\n=== DONE ===");
quit;
