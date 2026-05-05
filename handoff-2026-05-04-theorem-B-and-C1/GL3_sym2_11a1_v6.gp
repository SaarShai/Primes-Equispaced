\\ T8 v6 — clean parser, predict S(N) from zeros on Re=3/2
default(realprecision, 30);
default(parisize, 2^30);

print("=== T8 v6: GL(3) Δ-machine sym²(11a1), critical Re=3/2 ===");
t0 = getwalltime();

E = ellinit("11a1");
L = lfunsympow(E, 2);

Wt(s) = 2^(s/2 - 1) * gamma(s/2);
W(x) = exp(-x*x/2);

\\ Build μ_{sym²f}
Nmax_mu = 1000000;
print("Computing μ_{sym²f}(n) for n ≤ ", Nmax_mu);
av = lfunan(L, Nmax_mu);
mu = vector(Nmax_mu);
mu[1] = 1;
for(n = 2, Nmax_mu, my(s=0); fordiv(n, d, if(d<n, s+=av[n/d]*mu[d])); mu[n] = -s);

\\ Observed sums
Nlist = [1000, 3162, 10000, 31623, 100000];
nN = #Nlist;
S_obs = vector(nN);
for(k = 1, nN, my(Nv=Nlist[k], nlim=min(Nmax_mu, ceil(8*Nv))); S_obs[k] = sum(n=1, nlim, mu[n]*W(n*1./Nv)));

\\ Zeros
zeros = lfunzeros(L, 80);
print(#zeros, " zeros up to height 80");

\\ Function to predict using K zeros
LprimeAt(rho) = my(h=1e-6); (lfun(L, rho+h) - lfun(L, rho-h))/(2*h);

predictN(Nv, K) = {
  my(p=0., Nu=min(K, #zeros), j, rho, lp);
  for(j=1, Nu,
    rho = 3/2 + I*zeros[j];
    lp = LprimeAt(rho);
    p = p + 2*real(Nv^rho * Wt(rho) / lp);
  );
  p;
};

print("\nPrediction S(N) ≈ Σ N^ρ W~(ρ)/L'(ρ) over first K zero pairs:");
print("N         K=10        K=20        K=40        K=60        Observed");
for(k=1, nN,
  my(Nv=Nlist[k], p10, p20, p40, p60);
  p10 = predictN(Nv, 10);
  p20 = predictN(Nv, 20);
  p40 = predictN(Nv, 40);
  p60 = predictN(Nv, 60);
  printf("%-8d  %10.3f  %10.3f  %10.3f  %10.3f  %10.3f\n", Nv, p10, p20, p40, p60, S_obs[k]);
);

\\ Match-digits diagnostic at largest K
print("\nMatch table (K=60 zeros):");
print("N          predicted     observed      diff           rel_err     digits_match");
for(k=1, nN,
  my(Nv=Nlist[k], p, d, r, dg);
  p = predictN(Nv, 60);
  d = S_obs[k] - p;
  r = if(S_obs[k]!=0, d/S_obs[k], 0);
  dg = if(abs(r)>1e-30, -log(abs(r))/log(10), 30);
  printf("%-9d  %12.4f  %12.4f  %12.4f  %10.2e  %.2f\n", Nv, p, S_obs[k], d, r, dg);
);

print("\n=== Time: ", (getwalltime()-t0)/1000., " s ===");
quit;
