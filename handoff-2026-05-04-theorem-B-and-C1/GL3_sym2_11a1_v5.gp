\\ T8 v5 — sym²(11a1) Δ-machine, CORRECT critical line Re(s)=3/2
\\ Motive of sym²(weight-2 newform) has motivic weight 2 → critical line Re(s)=3/2
\\ Functional equation s ↔ 3-s
\\ PARI lfunzeros gives Im(γ) such that L(3/2 + iγ) = 0
\\
\\ Möbius sum identity (Mellin/Perron):
\\   S(N) = Σ μ_{sym²f}(n) W(n/N)  where W(x)=exp(-x²/2)
\\        = (1/2πi) ∫_{σ=2} N^s · W~(s) · (1/L(s, sym²f)) ds
\\   W~(s) = ∫_0^∞ e^{-x²/2} x^{s-1} dx = 2^(s/2-1) Γ(s/2)
\\
\\ Shift contour σ=2 → σ=1; pick up nontrivial zeros ρ on Re=3/2:
\\   S(N) = Σ_ρ N^ρ · W~(ρ) / L'(ρ, sym²f)  + (residual contour)
\\ Each pair ρ, conj(ρ) contributes 2 Re[ N^ρ W~(ρ)/L'(ρ) ] = N^(3/2)·oscillating

default(realprecision, 30);
default(parisize, 2^30);

print("=== T8 v5: GL(3) Δ-machine via sym²(11a1), critical line Re=3/2 ===");
t0 = getwalltime();

E = ellinit("11a1");
L = lfunsympow(E, 2);
print("Conductor of sym² L-function: 121 = 11²");
print("L(1, sym²f) = ", lfun(L, 1));
print("L(3/2, sym²f) = ", lfun(L, 3/2));   \\ central value

\\ Mellin
Wt(s) = 2^(s/2 - 1) * gamma(s/2);

\\ Build μ_{sym²f}
Nmax_mu = 1000000;
print("\nμ_{sym²f}(n) for n ≤ ", Nmax_mu);
t1 = getwalltime();
av = lfunan(L, Nmax_mu);
mu = vector(Nmax_mu);
mu[1] = 1;
for(n = 2, Nmax_mu, my(s=0); fordiv(n, d, if(d<n, s+=av[n/d]*mu[d])); mu[n] = -s);
print("  μ done in ", (getwalltime()-t1)/1000., " s");
print("  |μ_{sym²f}(n)| sample sizes:");
for(k=1, 6, n=10^k; if(n<=Nmax_mu, printf("    |μ(%d)| = %.2f\n", n, abs(mu[n]*1.))));

\\ Observed S(N)
W(x) = exp(-x*x/2);
Nlist = [1000, 3162, 10000, 31623, 100000];
S_obs = vector(#Nlist);
for(k=1, #Nlist, my(Nv=Nlist[k], nlim=min(Nmax_mu, ceil(8*Nv)), s_acc=sum(n=1, nlim, mu[n]*W(n*1./Nv))); S_obs[k]=s_acc; printf("  S(N=%d) = %.6f, S/N^(3/2) = %.6f\n", Nv, s_acc, s_acc/Nv^1.5));

\\ Compute zeros: PARI lfunzeros uses analytic normalization internally,
\\ so γ_j returned are imaginary parts on the GENUINE critical line.
\\ For our arithmetic L, that line is Re(s)=3/2.
zeros = lfunzeros(L, 50);
print("\n", #zeros, " zeros up to height 50.  First 5: ", zeros[1..min(5,#zeros)]);

\\ Verify: lfun(L, 3/2 + I*zeros[1]) should be ~0
zv = lfun(L, 3/2 + I*zeros[1]);
printf("\nVerify L(3/2 + i·γ_1) = %s, abs=%.3e\n", zv, abs(zv));

\\ Predict S(N) using zeros on Re=3/2
LprimeAt(rho) = my(h=1e-6); (lfun(L, rho+h) - lfun(L, rho-h))/(2*h);

print("\nPrediction S(N) ≈ Σ_ρ N^ρ · W~(ρ) / L'(ρ):");
print("  N        | predicted   | observed    | rel_err     | match digits");
print("  ---------+-------------+-------------+-------------+-------------");
for(k=1, #Nlist,
  my(Nv=Nlist[k], pred=0, Nz_use=min(40,#zeros));
  for(j=1, Nz_use, my(rho=3/2+I*zeros[j], term=2*real(Nv^rho * Wt(rho) / LprimeAt(rho))); pred=pred+term);
  my(rel=(S_obs[k]-pred)/S_obs[k], digits=if(abs(rel)>0, -log(abs(rel))/log(10), 99));
  printf("  %-8d | %11.4f | %11.4f | %11.2e | %.2f\n", Nv, pred, S_obs[k], rel, digits);
);

print("\n=== Total time: ", (getwalltime()-t0)/1000., " s ===");
quit;
