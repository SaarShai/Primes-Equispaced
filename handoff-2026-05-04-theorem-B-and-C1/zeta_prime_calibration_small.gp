/* Fallback: smaller T cap, faster. */
default(realprecision, 32);
default(parisize,    "1G");
default(parisizemax, "8G");

target = 1/(24*Pi);
print("Target 1/(24 pi) = ", target);

Tmax = 10000;
print("lfuninit h=", Tmax, " der=1 ...");
gettime();
L = lfuninit(1, [Tmax], 1);
print("  lfuninit ", gettime(), " ms");

print("zeros up to ", Tmax);
gettime();
Z = lfunzeros(L, Tmax);
print("  ", #Z, " zeros in ", gettime(), " ms");

gettime();
V = vector(#Z);
for(k=1, #Z, V[k] = abs(lfun(L, 1/2 + I*Z[k], 1))^2;
  if(k % 1000 == 0, print("  ", k, "/", #Z, " t=", gettime()/1000., "s")));
print("done");

Ts = [100, 500, 1000, 5000, 10000];
print("=== RESULTS_SMALL ===");
print("T       N(T)   sum                u_zeta(T)            rel_err");
S = 0.; idx = 1; ti = 1;
while(ti <= #Ts,
  T = Ts[ti];
  while(idx <= #Z && Z[idx] <= T, S += V[idx]; idx += 1);
  u = S / (T * log(T)^4);
  printf("%-7d %-6d %-18.10g %-22.16g %-10.5g\n", T, idx-1, S, u, abs(u-target)/target);
  ti += 1);
quit;
