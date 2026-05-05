/* family_avg_finite_T_fix.gp
 * Family-averaged numerical test of Theorem B with finite-T inflation correction.
 *
 * u_f(T) := sum_{|gamma_f| <= T} |L'(1+ i gamma_f, f)|^2
 *           / ( c_f * T * log^4 X(T, N_f) )
 * with X(T,N) = sqrt(N*T)/(2*pi) per Mason-Naples (16),
 * c_f = L(Sym^2 E, 1) via PARI lfunsympow at s=1 (correct normalization for E).
 *
 * Critical line for E in PARI arithmetic conventions: Re(s) = 1.
 * Zeros gamma satisfy L(E, 1 + i*gamma) = 0.
 *
 * Predicted: u_bar(T) -> 2/(3 pi) ~ 0.21221 as T -> infinity.
 * Cage: [(17 -+ sqrt(145))/(12 pi)] = [0.131, 0.770].
 *
 * Compute budget: T=10000 alone takes >>1 hr per curve, infeasible
 * for 14 curves; we restrict to T=1000 and T=5000 family averages
 * plus a single small-N supplement at T=10000.
 */

default(realprecision, 30);
default(parisize, "4G");
default(parisizemax, "8G");

const_pred = 2/(3*Pi);
cage_lo = (17 - sqrt(145))/(12*Pi);
cage_hi = (17 + sqrt(145))/(12*Pi);

print("=== family_avg_finite_T_fix ===");
print("Predicted asymptotic u_bar -> 2/(3 pi) = ", const_pred);
print("Cage [low, high] = [", cage_lo, ", ", cage_hi, "]");

\\ Family A (squarefree-conductor)
labels = ["11a1","14a1","15a1","17a1","19a1","21a1","26a1","33a1","35a1","37a1","38a1","43a1","53a1","57a1"];

\\ Process one (label, height); returns [N, c_f, S_full, n_zeros_pos, X, log_X, u_f]
process_one(label, height) = {
  my(E, N, L, Lsym2, c, zs, S, S_full, j, v, X, lX, denom, u, t0);
  t0 = getwalltime();
  E = ellinit(label);
  N = ellglobalred(E)[1];
  L = lfuncreate(E);
  Lsym2 = lfunsympow(E, 2);
  c = lfun(Lsym2, 1);
  zs = lfunzeros(L, height);
  S = 0.0;
  for(j=1, #zs,
    v = lfun(L, 1 + I*zs[j], 1);
    S += abs(v)^2;
  );
  S_full = 2*S;
  X = sqrt(N*height)/(2*Pi);
  lX = log(X);
  denom = c * height * lX^4;
  u = S_full / denom;
  printf("[%s T=%d] N=%d c_f=%.6f #zeros+=%d S_full=%.4f X=%.3f logX=%.4f u_f=%.6f (%.1fs)\n",
        label, height, N, c, #zs, S_full, X, lX, u, (getwalltime()-t0)/1000.0);
  return([N, c, S_full, #zs, X, lX, u]);
};

\\ T=1000 full family
print("\n========== T = 1000 ==========");
res1k = vector(#labels);
for(i=1, #labels, res1k[i] = process_one(labels[i], 1000));

\\ T=5000 full family
print("\n========== T = 5000 ==========");
res5k = vector(#labels);
for(i=1, #labels, res5k[i] = process_one(labels[i], 5000));

\\ T=10000 — small subset to demonstrate direction
print("\n========== T = 10000 (smallest 3 conductors only) ==========");
small_idx = [1, 2, 3];   \\ 11a1 (N=11), 14a1 (N=14), 15a1 (N=15)
res10k = vector(#small_idx);
for(j=1, #small_idx, res10k[j] = process_one(labels[small_idx[j]], 10000));

\\ ====== Summary ======
print("\n\n========== SUMMARY: per-curve u_f ==========");
print("label   N     c_f          u_f(T=1k)    u_f(T=5k)    u_f(T=10k)");
for(i=1, #labels,
  s10k = "  -  ";
  pos = 0;
  for(j=1, #small_idx, if(small_idx[j]==i, pos=j));
  if(pos > 0, s10k = Str(res10k[pos][7]));
  printf("%s  %4d  %10.6f  %10.6f  %10.6f  %s\n",
        labels[i], res1k[i][1], res1k[i][2],
        res1k[i][7], res5k[i][7], s10k);
);

avg1k = sum(i=1, #labels, res1k[i][7]) / #labels;
avg5k = sum(i=1, #labels, res5k[i][7]) / #labels;

avg1k_sub = sum(j=1, #small_idx, res1k[small_idx[j]][7]) / #small_idx;
avg5k_sub = sum(j=1, #small_idx, res5k[small_idx[j]][7]) / #small_idx;
avg10k_sub = sum(j=1, #small_idx, res10k[j][7]) / #small_idx;

print("\n========== FAMILY AVERAGES ==========");
printf("u_bar(T=1k) full14   = %.6f   ratio to 2/(3pi) = %.4f\n", avg1k, avg1k/const_pred);
printf("u_bar(T=5k) full14   = %.6f   ratio to 2/(3pi) = %.4f\n", avg5k, avg5k/const_pred);
print();
printf("u_bar(T=1k) sub3     = %.6f   ratio to 2/(3pi) = %.4f\n", avg1k_sub, avg1k_sub/const_pred);
printf("u_bar(T=5k) sub3     = %.6f   ratio to 2/(3pi) = %.4f\n", avg5k_sub, avg5k_sub/const_pred);
printf("u_bar(T=10k) sub3    = %.6f   ratio to 2/(3pi) = %.4f\n", avg10k_sub, avg10k_sub/const_pred);

print("\n========== CAGE CHECK ==========");
inside(x) = (x >= cage_lo) && (x <= cage_hi);
printf("Cage = [%.4f, %.4f]\n", cage_lo, cage_hi);
print("u_bar(1k,full)   in cage? ", inside(avg1k));
print("u_bar(5k,full)   in cage? ", inside(avg5k));
print("u_bar(10k,sub3)  in cage? ", inside(avg10k_sub));

print("\n========== INFLATION ANALYSIS ==========");
print("Per the inflation hypothesis, u_f(T) ~ const_pred * (logN + 2 logT - 2 log(2pi))^4 / (logT - log(2pi))^4");
print("Try corrected u_f := u_f * (logT)^4 / (logX)^4  -- this replaces logX denominator with logT");
print("\nAt T=5000:");
for(i=1, #labels,
  N = res5k[i][1]; lX = res5k[i][6];
  inflation = (lX / log(5000))^4;
  u_corr = res5k[i][7] * inflation;   \\ moves to log T denominator
  printf("  %s  N=%d  inflation=(logX/logT)^4=%.4f  u_logT=%.6f\n",
        labels[i], N, inflation, u_corr);
);
avg5k_logT = sum(i=1, #labels, res5k[i][7] * (res5k[i][6]/log(5000))^4) / #labels;
printf("u_bar(T=5k) with logT denom = %.6f  ratio to 2/(3pi) = %.4f\n", avg5k_logT, avg5k_logT/const_pred);

avg1k_logT = sum(i=1, #labels, res1k[i][7] * (res1k[i][6]/log(1000))^4) / #labels;
printf("u_bar(T=1k) with logT denom = %.6f  ratio to 2/(3pi) = %.4f\n", avg1k_logT, avg1k_logT/const_pred);

print("\n========== CONVERGENCE TREND ==========");
printf("Full 14: u_bar(1k)=%.6f -> u_bar(5k)=%.6f  drift = %+.4f\n", avg1k, avg5k, avg5k-avg1k);
printf("Sub  3:  %.6f -> %.6f -> %.6f  drifts = %+.4f, %+.4f\n",
      avg1k_sub, avg5k_sub, avg10k_sub, avg5k_sub-avg1k_sub, avg10k_sub-avg5k_sub);

print("\nDONE.");
quit;
