\\ T8 v8 — full Δ-machine: R_0 + zeros sum
\\ R_0 = Res_{s=0} N^s W~(s) / L(s, sym²f)
\\ L has order-2 zero at s=0; W~(s) has simple pole; → triple pole at s=0
default(realprecision, 30);
default(parisize, 2^30);

E = ellinit("11a1");
L = lfunsympow(E, 2);

Wt(s) = 2^(s/2 - 1) * gamma(s/2);
W(x) = exp(-x*x/2);

\\ R_0 via small-circle contour
R0_at(Nv) = {
  my(NPTS=512, r=0.04, total=0., j, th, s);
  for(j=0, NPTS-1,
    th = 2*Pi*j/NPTS;
    s = r * exp(I*th);
    total = total + (Nv^s * Wt(s) / lfun(L, s)) * s;
  );
  real(total / NPTS);
};

print("R_0 (residue at s=0) for various N:");
for(k=1, 6, my(Nv=10^k); printf("  N=10^%d:  R_0 = %.6f\n", k, R0_at(Nv)));

\\ μ
Nmax_mu = 1000000;
av = lfunan(L, Nmax_mu);
mu = vector(Nmax_mu);
mu[1] = 1;
for(n = 2, Nmax_mu, my(s=0); fordiv(n, d, if(d<n, s+=av[n/d]*mu[d])); mu[n] = -s);

zeros = lfunzeros(L, 100);
NZ = #zeros;
print(NZ, " zeros up to height 100");

LprimeAt(rho) = my(h=1e-6); (lfun(L, rho+h) - lfun(L, rho-h))/(2*h);
zcoef = vector(NZ); for(j=1, NZ, my(rho=3/2+I*zeros[j]); zcoef[j] = Wt(rho)/LprimeAt(rho));

predictNK(Nv, K) = my(p=0., j); for(j=1, K, my(rho=3/2+I*zeros[j]); p += 2*real(Nv^rho * zcoef[j])); p;
Sobs(Nv) = my(nlim = min(Nmax_mu, ceil(8*Nv))); sum(n=1, nlim, mu[n]*W(n*1./Nv));

NL = [1000, 3162, 10000, 31623, 100000];

print("\nFull match: S(N) vs R_0 + Σ_zeros");
print("N          observed       R_0           Σ_zeros(K=80)  total          diff           digits");
for(k = 1, #NL, my(Nv=NL[k], so=Sobs(Nv), R0=R0_at(Nv), zsum=predictNK(Nv,min(80,NZ)), tot=R0+zsum, df=so-tot, re=if(so!=0,df/so,0.), dg=if(abs(re)>1e-30,-log(abs(re))/log(10),30.)); printf("%-9d  %13.4f  %12.4f  %13.4f  %13.4f  %12.4e  %.2f\n", Nv, so, R0, zsum, tot, df, dg));

quit;
