\\ T8 v7 — clean
default(realprecision, 30);
default(parisize, 2^30);

E = ellinit("11a1");
L = lfunsympow(E, 2);

Wt(s) = 2^(s/2 - 1) * gamma(s/2);
W(x) = exp(-x*x/2);

Nmax_mu = 1000000;
av = lfunan(L, Nmax_mu);
mu = vector(Nmax_mu);
mu[1] = 1;
for(n = 2, Nmax_mu, my(s=0); fordiv(n, d, if(d<n, s+=av[n/d]*mu[d])); mu[n] = -s);
print("μ done");

zeros = lfunzeros(L, 80);
print(#zeros, " zeros up to height 80");

LprimeAt(rho) = my(h=1e-6); (lfun(L, rho+h) - lfun(L, rho-h))/(2*h);

\\ Precompute zero contributions per zero, separate from N
\\ For each zero ρ_j, store W~(ρ_j)/L'(ρ_j) and the imaginary part
NZ = #zeros;
zcoef = vector(NZ);
for(j = 1, NZ, my(rho = 3/2 + I*zeros[j]); zcoef[j] = Wt(rho)/LprimeAt(rho));
print("zcoef precomputed");

\\ Function: predict S(N) using first K zeros
predictNK(Nv, K) = my(p=0., j); for(j=1, K, my(rho=3/2+I*zeros[j]); p += 2*real(Nv^rho * zcoef[j])); p;

\\ Observed S(N)
Sobs(Nv) = my(nlim = min(Nmax_mu, ceil(8*Nv))); sum(n=1, nlim, mu[n]*W(n*1./Nv));

\\ Run for various N
NL = [1000, 3162, 10000, 31623, 100000];

print("\nN, S_obs, pred_K10, pred_K20, pred_K40, pred_K60");
for(k = 1, #NL, my(Nv=NL[k], so=Sobs(Nv), p10=predictNK(Nv,10), p20=predictNK(Nv,20), p40=predictNK(Nv,40), p60=predictNK(Nv,60)); printf("%d, %.6f, %.6f, %.6f, %.6f, %.6f\n", Nv, so, p10, p20, p40, p60));

print("\nMatch table:");
print("N          observed       pred(K=60)     abs_diff       rel_err        digits");
for(k = 1, #NL, my(Nv=NL[k], so=Sobs(Nv), pr=predictNK(Nv,60), df=so-pr, re=if(so!=0,df/so,0.), dg=if(abs(re)>1e-30,-log(abs(re))/log(10),30.)); printf("%-9d  %13.4f  %13.4f  %13.4f  %.4e  %.2f\n", Nv, so, pr, df, re, dg));

quit;
