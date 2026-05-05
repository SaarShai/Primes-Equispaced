/* zeta_prime_calibration_v2.gp
 * u_zeta(T) = sum_{0<gamma<=T} |zeta'(rho)|^2 / (T log^4 T)
 * Compare to Conrey 1989 constant 1/(24 pi) = 0.013262911924324...
 * Strategy: T_max=5000 first (feasible ~10 min), then push to 10000 if fast enough.
 */

default(realprecision, 30);
default(parisize,    "1G");
default(parisizemax, "8G");

target = 1/(24*Pi);
print("Target 1/(24*pi) = ", target);
print("Run started: ", Str(1));

/* --- Phase 1: zeros up to Tmax --- */
Tmax = 5000;
print("\n[1/3] Computing zeros up to T=", Tmax, " ...");
gettime();
Z = lfunzeros(lfunzeta, Tmax);
t1 = gettime();
nZ = #Z;
print("  Found ", nZ, " zeros in ", t1/1000., " s");

/* --- Phase 2: |zeta'(rho)|^2 at each zero --- */
print("\n[2/3] Computing |zeta'(rho)|^2 at all ", nZ, " zeros ...");
gettime();
V = vector(nZ);
for(k=1, nZ, V[k] = abs(lfun(lfunzeta, 1/2 + I*Z[k], 1))^2; if(k%1000==0, print("  k=",k," t=",gettime()/1000.,"s")));
t2 = gettime();
print("  Done in ", t2/1000., " s");

/* --- Phase 3: accumulate and print table --- */
Ts = [100, 500, 1000, 5000];
print("\n=== RESULTS (T_max=5000) ===");
print("T          N(T)       Sum|zp|^2       u_zeta(T)            rel_dev");
S = 0; idx = 1; ti = 1;
while(ti <= #Ts,
  T = Ts[ti];
  while(idx <= nZ && Z[idx] <= T, S += V[idx]; idx += 1);
  N = idx - 1;
  u = S / (T * log(T)^4);
  rel = abs(u - target)/target;
  printf("%-10d %-10d %-15.8g  %-22.16g  %-10.6g\n", T, N, S, u, rel);
  ti += 1);

quit;
