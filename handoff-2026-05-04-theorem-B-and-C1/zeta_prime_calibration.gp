/* zeta_prime_calibration.gp  (v4 — final working version)
 * u_zeta(T) = sum_{0<gamma<=T} |zeta'(rho)|^2 / (T log^4 T)
 * Compare to Conrey 1989 constant 1/(24 pi) = 0.013262911924324...
 *
 * CRITICAL PARI syntax note: all for() loop bodies must be on ONE line.
 * Multi-line for/while bodies cause parse errors in file mode.
 *
 * Usage: gp -q zeta_prime_calibration.gp
 */

default(realprecision, 30);
default(parisize,    "1G");
default(parisizemax, "8G");

target = 1/(24*Pi);
print("Target 1/(24*pi) = ", target);
print("T          N(T)       Sum_|zp|^2         u_zeta(T)            rel_dev      time(s)");

\\ Individual T runs (avoids multiline while-loop parsing issue)
Tvals = [100, 500, 1000, 5000, 10000];
for(ti=1, #Tvals, T = Tvals[ti]; Z = lfunzeros(lfunzeta, T); n = #Z; gettime(); S = 0; for(k=1, n, S += abs(lfun(lfunzeta, 1/2 + I*Z[k], 1))^2); t = gettime(); u = S/(T*log(T)^4); rel = abs(u-target)/target; printf("%-10d %-10d %-18.8g  %-22.16g  %-10.6g  [%.1f]\n", T, n, S, u, rel, t/1000.));

quit;
