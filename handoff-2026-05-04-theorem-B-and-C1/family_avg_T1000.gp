/* family_avg_T1000.gp
 * Family-averaged u_f(T) over 14-curve squarefree-level k=2 family.
 *
 * FORMULA (exact task specification, M-N convention):
 *   u_f(T) = sum_{|gamma_f|<=T} |L'(1/2+i*gamma_f, f)|^2 / (c_f * T * log^4(X))
 * where:
 *   X = sqrt(N*T) / (2*pi)     [M-N eq(16)]
 *   c_f = lfun(lfunsympow(E,2), 2) / zeta(2)
 *   sigma = k/2 = 1 for k=2 (PARI arithmetic critical line)
 *   sum over |gamma_f|<=T = 2 * sum_{0<gamma_f<=T} (by symmetry)
 *   L'(1+i*gamma, E) evaluated via lfun(L, 1+I*gamma, 1)
 *
 * FAMILY: 14 squarefree-conductor k=2 newforms
 * {11a1,14a1,15a1,17a1,19a1,21a1,26a1,33a1,35a1,37a1,38a1,43a1,53a1,57a1}
 *
 * TARGETS: T=400 (fast, ~20 min total), T=1000 (full run, ~90 min)
 *
 * PREDICTIONS:
 *   Asymptotic: 2/(3*pi) ~ 0.21221
 *   Cage: [(17-sqrt(145))/(12*pi), (17+sqrt(145))/(12*pi)] ~ [0.1315, 0.7704]
 *   Finite-T inflation for q=11, T=1000: factor ~1.85x -> u_f ~ 0.39 (task prediction)
 *
 * NOTE: lfun(lfunsympow(E,2), 1) = Rankin-Selberg constant c_f^RS ~ 0.5886 (11a1)
 *       lfun(lfunsympow(E,2), 2)/zeta(2) ~ 0.6429 (11a1) -- task formula, ~9% larger
 *       Both conventions tried; task formula used in primary output.
 */

default(realprecision, 30);
default(parisize, "2G");
default(parisizemax, "8G");

const_pred = 2 / (3 * Pi);
cage_lo = (17 - sqrt(145)) / (12 * Pi);
cage_hi = (17 + sqrt(145)) / (12 * Pi);
z2 = zeta(2);

print("=== family_avg_T1000 ===");
print("Formula: u_f(T) = sum_{|gamma|<=T} |L'(1+i*gamma,E)|^2 / (c_f * T * logX^4)");
print("         c_f = lfun(lfunsympow(E,2), 2) / zeta(2)  [task formula]");
print("         X = sqrt(N*T)/(2*pi)");
printf("Predicted asymptotic: 2/(3*pi) = %.8f\n", const_pred);
printf("Cage: [%.8f, %.8f]\n", cage_lo, cage_hi);
printf("zeta(2) = %.8f\n", z2);
print();

/* Family A: 14 squarefree-conductor k=2 elliptic newforms */
labels = ["11a1","14a1","15a1","17a1","19a1","21a1","26a1","33a1","35a1","37a1","38a1","43a1","53a1","57a1"];

/* Process one curve at given T.
 * Returns [N, c_f_task, c_f_rs, S_full, n_pos_zeros, X, logX, u_f_task, u_f_rs, elapsed_s]
 */
process_one(label, height) = {
  my(E, N, L, Lsym2, c_task, c_rs, zs, n_pos, j, v, S, S_full, X, lX, u_task, u_rs, t0);
  t0 = getwalltime();
  E = ellinit(label);
  N = ellglobalred(E)[1];
  L = lfuncreate(E);
  Lsym2 = lfunsympow(E, 2);
  /* c_f: task formula */
  c_task = lfun(Lsym2, 2) / z2;
  /* c_f: Rankin-Selberg (s=1) for cross-check */
  c_rs = lfun(Lsym2, 1);
  /* zeros: positive imaginary parts only (0 < gamma <= T) */
  zs = lfunzeros(L, height);
  n_pos = #zs;
  S = 0;
  for(j = 1, n_pos,
    v = lfun(L, 1 + I*zs[j], 1);
    S += abs(v)^2;
  );
  /* double for |gamma|<=T symmetry */
  S_full = 2 * S;
  X = sqrt(N * height) / (2 * Pi);
  lX = log(X);
  u_task = S_full / (c_task * height * lX^4);
  u_rs   = S_full / (c_rs   * height * lX^4);
  printf("[%s T=%d] N=%d c_task=%.6f c_rs=%.6f #pos_zeros=%d S_full=%.4f X=%.4f logX=%.5f u_task=%.6f u_rs=%.6f (%.1fs)\n",
         label, height, N, c_task, c_rs, n_pos, S_full, X, lX, u_task, u_rs,
         (getwalltime() - t0) / 1000.0);
  return([N, c_task, c_rs, S_full, n_pos, X, lX, u_task, u_rs]);
};

/* Summary printer */
print_summary(T_label, res) = {
  my(n, u_task_vals, u_rs_vals, avg_task, avg_rs, std_task, i);
  n = #res;
  u_task_vals = vector(n, i, res[i][8]);
  u_rs_vals   = vector(n, i, res[i][9]);
  avg_task = sum(i=1, n, u_task_vals[i]) / n;
  avg_rs   = sum(i=1, n, u_rs_vals[i]) / n;
  print("\n=== SUMMARY T=", T_label, " ===");
  print("label       N    c_task    c_rs      S_full         logX    u_task    u_rs      cage_task");
  for(i=1, n,
    my(in_cage = if(u_task_vals[i] >= cage_lo && u_task_vals[i] <= cage_hi, "Y", "N"));
    printf("%-8s %4d  %.6f  %.6f  %12.4f  %.5f  %.6f  %.6f  %s\n",
           labels[i], res[i][1], res[i][2], res[i][3], res[i][4],
           res[i][7], res[i][8], res[i][9], in_cage);
  );
  printf("\nFamily average u_bar_task  = %.8f   ratio/pred = %.5f\n", avg_task, avg_task / const_pred);
  printf("Family average u_bar_rs    = %.8f   ratio/pred = %.5f\n", avg_rs,   avg_rs   / const_pred);
  printf("Cage [%.4f, %.4f]: u_bar_task in cage? %s\n", cage_lo, cage_hi,
         if(avg_task >= cage_lo && avg_task <= cage_hi, "YES", "NO"));
  return([avg_task, avg_rs]);
};

/* ================================================================
 * T = 400  (smaller T for faster check)
 * ================================================================ */
print("\n========== T = 400 ==========");
res400 = vector(#labels);
for(i = 1, #labels, res400[i] = process_one(labels[i], 400));
avg400 = print_summary(400, res400);

/* ================================================================
 * T = 1000  (main target)
 * ================================================================ */
print("\n========== T = 1000 ==========");
res1000 = vector(#labels);
for(i = 1, #labels, res1000[i] = process_one(labels[i], 1000));
avg1000 = print_summary(1000, res1000);

/* ================================================================
 * Inflation analysis
 * ================================================================ */
print("\n========== INFLATION ANALYSIS ==========");
print("Inflation factor per curve: u_f(T) / (2/(3*pi))");
print("Finite-T inflation = u_f_task / const_pred");
print();
printf("%-8s  %6s  %6s  %8s  %8s  %8s  %8s\n",
       "label", "N", "T=400", "infl400", "T=1000", "infl1000", "trend");
for(i=1, #labels,
  u4 = res400[i][8];
  u10 = res1000[i][8];
  infl4 = u4 / const_pred;
  infl10 = u10 / const_pred;
  printf("%-8s  %4d  %8.5f  %8.3f  %8.5f  %8.3f  %+.3f\n",
         labels[i], res400[i][1], u4, infl4, u10, infl10, infl10-infl4);
);

/* Inflation-corrected family average */
print();
printf("u_bar_task(T=400)  = %.6f,  inflation = %.4f\n", avg400[1], avg400[1]/const_pred);
printf("u_bar_task(T=1000) = %.6f,  inflation = %.4f\n", avg1000[1], avg1000[1]/const_pred);
printf("Trend: delta_u_bar = %+.6f\n", avg1000[1] - avg400[1]);

/* Per-curve convergence direction */
print("\nConvergence check (T=400 -> T=1000): positive delta = moving AWAY from pred");
n_up = 0; n_dn = 0;
for(i=1, #labels,
  d = res1000[i][8] - res400[i][8];
  if(d > 0, n_up++, n_dn++);
);
printf("%d curves moving up, %d curves moving down\n", n_up, n_dn);

print("\nDONE.");
quit;
