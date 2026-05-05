\\ T8 v3 — sym²(11a1) Δ-machine; correct order-2 zero of L at s=0
\\ L(s, sym²f) ~ c·s² near s=0  (order-2 trivial zero from gamma factors)
\\ Hence 1/L has DOUBLE pole at s=0;  W~(s) = 2^(s/2-1) Γ(s/2) has SIMPLE pole at s=0
\\ → integrand N^s W~(s)/L(s) has TRIPLE pole at s=0; residue depends on N as
\\   R_0(N) = A·log²(N) + B·log(N) + C
\\
\\ This is the GL(3) main term — log² growth is the signature of order-2 zero
\\ (Iwaniec–Kowalski Ch 5 theta-formula style).

default(realprecision, 40);
default(parisize, 2^30);

print("=== T8 v3: sym²(11a1) Δ-machine, fixed for L~s² at 0 ===");
t0 = getwalltime();

E = ellinit("11a1");
L = lfunsympow(E, 2);

\\ Confirm L(s)/s² → constant
print("\nL(s)/s² near 0 (should converge):");
for(k=2, 7, eps=10.^(-k); printf("  L(%.0e)/%e² = %.15e\n", eps, eps, lfun(L, eps)/eps^2));

\\ Get c2 = L''(0)/2
c2 = lfun(L, 1e-3) / (1e-3)^2;
print("\nLeading coefficient: L(s) ≈ c2·s² + ..., c2 ≈ ", c2);

\\ Mellin W~(s) = 2^(s/2-1) Γ(s/2);  near s=0: Γ(s/2) ~ 2/s - γ + ...
\\   2^(s/2-1) ~ (1/2)(1 + (s/2)log2 + ...)
\\ So W~(s) ~ (1/s) - γ/2 + ... (leading = 1/s)
\\
\\ Then  N^s W~(s)/L(s) ~ N^s · (1/s) / (c2 s²) = N^s / (c2 s³)
\\ Residue at s=0 of N^s / (c2 s³) = (1/c2) · (1/2!) · (log N)² = log²(N)/(2 c2)
\\
\\ Plus corrections from higher Taylor terms.

W(x) = exp(-x*x/2);

\\ Compute high-precision residue numerically via small contour
Wt(s) = 2^(s/2 - 1) * gamma(s/2);

residue_at_0(Nv) = {
  my(NPTS=256, r=0.02, total=0, th, s, val);
  for(j=0, NPTS-1,
    th = 2*Pi*j/NPTS;
    s = r * exp(I*th);
    val = Nv^s * Wt(s) / lfun(L, s);
    total = total + val * s;
  );
  real(total / NPTS);
};

print("\nNumerical R_0 = Res_{s=0} N^s W~(s)/L(s, sym²f):");
for(k=1, 6, Nv = 10^k; printf("  N=10^%d:  R_0 = %.6f,  predicted (log²N)/(2c2) = %.6f\n", k, residue_at_0(Nv), log(Nv*1.)^2/(2*c2)));

\\ ---- Now compute observed S(N) ----
Nmax_mu = 800000;
print("\nμ_{sym²f}(n) for n ≤ ", Nmax_mu);
t1 = getwalltime();
av = lfunan(L, Nmax_mu);
mu = vector(Nmax_mu);
mu[1] = 1;
for(n = 2, Nmax_mu, my(s=0); fordiv(n, d, if(d<n, s+=av[n/d]*mu[d])); mu[n] = -s);
print("  μ done in ", (getwalltime()-t1)/1000., " s");

Nlist = [1000, 3000, 10000, 30000, 100000];
S_obs = vector(#Nlist);
for(k=1, #Nlist, Nv=Nlist[k]; nlim=min(Nmax_mu, ceil(8*Nv)); s_acc=sum(n=1, nlim, mu[n]*W(n*1./Nv)); S_obs[k]=s_acc; printf("  S(N=%d) = %.6f\n", Nv, s_acc));

\\ Get nontrivial zeros
zeros = lfunzeros(L, 80);
print("\n", #zeros, " zeros up to height 80");

\\ Predict for each N
print("\nFull explicit-formula prediction:");
print("  N         | R_0          | Σ_zeros (40)  | total_pred   | observed     | rel_err");
print("  ----------+--------------+---------------+--------------+--------------+----------");
for(k=1, #Nlist,
  Nv = Nlist[k];
  R0 = residue_at_0(Nv);
  zsum = 0;
  Nz_use = min(40, #zeros);
  for(j=1, Nz_use,
    rho = 1/2 + I*zeros[j];
    h_d = 1e-6;
    Lprime_at_rho = (lfun(L, rho+h_d) - lfun(L, rho-h_d))/(2*h_d);
    term = 2 * real(Nv^rho * Wt(rho) / Lprime_at_rho);
    zsum = zsum + term;
  );
  total = R0 + zsum;
  rel = (S_obs[k] - total)/abs(S_obs[k]);
  printf("  %-9d | %12.4f | %13.4f | %12.4f | %12.4f | %9.2e\n", Nv, R0, zsum, total, S_obs[k], rel);
);

print("\n=== Total time: ", (getwalltime()-t0)/1000., " s ===");
quit;
