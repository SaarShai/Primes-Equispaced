\\ T8 v2 — proper explicit-formula match for sym²(11a1)
\\ Key insight: L(0, sym²f) = 0 (trivial zero from gamma factors).
\\ So 1/L(s, sym²f) has a POLE at s=0 → main term R_0 from this pole.
\\ Also: μ_{sym²f}(n) is unbounded; the right test sum is the contour integral
\\
\\   S(N) = (1/2πi) ∫ N^s W~(s) / L(s, sym²f) ds
\\
\\ shift contour from Re s = 2 to Re s = -1: pick up
\\   - residue at s=0 from 1/L(s, sym²f) pole  (R_0 term)
\\   - sum over nontrivial zeros ρ:  N^ρ W~(ρ) / L'(ρ, sym²f)
\\   - residues at trivial zeros (gamma poles)
\\
\\ Verify by 5+ digit match.
\\
\\ Run:  gp -q GL3_sym2_11a1_v2.gp > GL3_sym2_11a1_v2.out 2>&1

default(realprecision, 40);
default(parisize, 2^30);

print("=== T8 v2: sym²(11a1) Δ-machine — explicit formula match ===");
t0 = getwalltime();

E = ellinit("11a1");
L = lfunsympow(E, 2);

\\ Verify gamma factors / functional equation parameters
LD = lfundata = L;  \\ keep
print("L data structure inspection:");
print("  L params: ", L);  \\ shows components

\\ Probe L(s) near s=0 to determine pole/zero order of 1/L
print("\nProbing L(s, sym²f) near s=0:");
for(eps_pow = 2, 6, {
  eps = 10.^(-eps_pow);
  v = lfun(L, eps);
  printf("  L(%.0e) = %.20e\n", eps, v);
});

\\ Series expansion: estimate L(s) ≈ c1 s + c2 s² + ...
\\ then 1/L(s) ≈ 1/(c1 s) + ...
h = 1e-6;
Lp0 = (lfun(L, h) - lfun(L, -h))/(2*h);
print("\nL'(0, sym²f) ≈ ", Lp0);
\\ residue of 1/L at s=0 is 1/L'(0)
res0 = 1/Lp0;
print("Residue of 1/L(s) at s=0: ", res0);

\\ Mellin transform of W(x) = exp(-x²/2):  W~(s) = 2^(s/2-1) Γ(s/2)
Wt(s) = 2^(s/2 - 1) * gamma(s/2);

\\ At s=0: W~(s) has a pole from Γ(s/2) ~ 2/s
\\ So  W~(s)/L(s) near s=0 has DOUBLE POLE: (2/s)·(1/(L'(0) s)) · (1/2) = 1/(L'(0) s²)
\\ Hmm — need to be careful. Let me compute residue numerically by contour.

\\ Better: numerical residue via small circle around 0
print("\nNumerical residue of W~(s)/L(s) at s=0 via circle contour:");
Nv_test = 10000;
res_total = 0;
NPTS = 64;
r_circ = 0.05;
for(k=0, NPTS-1, {
  th = 2*Pi*k/NPTS;
  s = r_circ * (cos(th) + I*sin(th));
  if(abs(s) > 1e-10,
    val = Nv_test^s * Wt(s) / lfun(L, s);
    res_total += val;
  );
});
res_total = res_total * r_circ * (2*Pi*I) / NPTS;
\\ Actually:  (1/2πi) ∫ f(s) ds  on circle of radius r:
\\   ds = i r e^{iθ} dθ;  so integrand becomes (1/2π) ∫ f(s) r e^{iθ} dθ
res_total_v2 = 0;
for(k=0, NPTS-1, {
  th = 2*Pi*k/NPTS;
  s = r_circ * exp(I*th);
  val = Nv_test^s * Wt(s) / lfun(L, s);
  res_total_v2 += val * I * s;   \\ ds/dθ = i s
});
res_total_v2 = res_total_v2 / NPTS;   \\ (1/2π)·(2π/N) sum
\\ (1/2πi) ∫ f ds = (1/2πi) Σ f(s_k) · (i s_k)·(2π/N)
\\                = (1/N) Σ f(s_k) · s_k
res_main = 0;
for(k=0, NPTS-1, {
  th = 2*Pi*k/NPTS;
  s = r_circ * exp(I*th);
  val = Nv_test^s * Wt(s) / lfun(L, s);
  res_main += val * s;
});
res_main = real(res_main / NPTS);
printf("  R_0 (residue at s=0) at N=%d: %.10f\n", Nv_test, res_main);

\\ Compare to weighted Möbius sum.
\\ For S(N) = Σ μ_{sym²f}(n) W(n/N), there's a normalization:
\\ S(N) = (1/2πi) ∫_{Re=σ}  N^s · W~(s) · (1/L(s, sym²f)) ds   for σ large enough
\\ where W~ is Mellin of W on (0,∞).  Verify normalization on simple test.

\\ Simple test: ζ(s) (Möbius classical):
\\ Σ μ(n) exp(-n²/(2 N²))  for ζ.  Should match (1/2πi)∫ N^s W~(s) / ζ(s) ds.
print("\n--- Sanity check: classical Möbius vs ζ ---");
Nz = 1000;
mu_class = vector(8000, k, moebius(k));
S_class = sum(n=1, 8000, mu_class[n] * exp(-(n*1./Nz)^2/2));
printf("Σ μ(n) exp(-n²/(2·1000²)) for n≤8000 = %.10f\n", S_class);
\\ Predict: zeros of zeta dominate;  pole of 1/ζ at s=1: residue = N · W~(1)
\\ W~(1) = 2^(1/2 - 1) Γ(1/2) = sqrt(π/2)
\\ So main term = N·sqrt(π/2)·Res_{s=1}(1/ζ(s)) = N·sqrt(π/2)·(1/ζ'... no, 1/ζ has no pole at 1; ζ has pole).
\\ For 1/ζ(s):  ζ(s) ~ 1/(s-1) + γ, so 1/ζ(s) ~ (s-1) - γ(s-1)² + ...; analytic at s=1.
\\ At s=0: ζ(0) = -1/2, so 1/ζ(0) = -2.
\\ Main term from s=0 pole of W~(s): W~(s) = 2^(s/2-1) Γ(s/2) ~ 2^(s/2-1) · 2/s
\\ Residue at s=0 of N^s · W~(s) · (1/ζ(s)):
\\   = lim_{s→0} s · N^s · 2^(s/2-1) · 2/s · (-2) = -2  (ignoring N^s → 1)
\\ So predicted main term = -2 ?  Let's check.
print("Classical predicted main: ~ -2 (from s=0 pole of Γ(s/2))");
\\ Hmm S_class = ?  if matches -2 we're good.

\\ ---- Now build μ_{sym²f}, S(N), and full prediction ----
Nmax_mu = 100000;
print("\nμ_{sym²f}(n) for n ≤ ", Nmax_mu);
av = lfunan(L, Nmax_mu);
mu = vector(Nmax_mu);
mu[1] = 1;
for(n = 2, Nmax_mu, {
  s = 0;
  fordiv(n, d, if(d < n, s += av[n/d] * mu[d]));
  mu[n] = -s;
});

W(x) = exp(-x*x/2);
Nlist = [500, 1000, 5000, 10000];
print("\nWeighted Möbius sums S(N) = Σ μ_{sym²f}(n) W(n/N):");
S_obs = vector(#Nlist);
for(k=1, #Nlist, {
  Nv = Nlist[k];
  nlim = min(Nmax_mu, ceil(8*Nv));
  s_acc = sum(n=1, nlim, mu[n] * W(n*1./Nv));
  S_obs[k] = s_acc;
  printf("  S(N=%d) = %.6f\n", Nv, s_acc);
});

\\ Predict via residue at s=0 + nontrivial zeros
zeros = lfunzeros(L, 60);
print("\n", #zeros, " nontrivial zeros up to height 60");

print("\nExplicit-formula prediction (residue at 0 + first ", min(20, #zeros), " zeros):");
for(k=1, #Nlist, {
  Nv = Nlist[k];
  \\ Residue at s=0 numerically
  r_circ = 0.03;
  NPTS = 128;
  res_main = 0;
  for(j=0, NPTS-1, {
    th = 2*Pi*j/NPTS;
    s = r_circ * exp(I*th);
    val = Nv^s * Wt(s) / lfun(L, s);
    res_main += val * s;
  });
  res_main = real(res_main / NPTS);
  \\ Zeros contribution
  zsum = 0;
  for(j=1, min(20, #zeros), {
    rho = 1/2 + I*zeros[j];
    h_d = 1e-6;
    Lprime_at_rho = (lfun(L, rho+h_d) - lfun(L, rho-h_d))/(2*h_d);
    term = 2 * real( Nv^rho * Wt(rho) / Lprime_at_rho );
    zsum += term;
  });
  total_pred = res_main + zsum;
  printf("  N=%d: R_0=%.6f, Σ_zeros=%.6f, total=%.6f, observed=%.6f, diff=%.6f\n",
         Nv, res_main, zsum, total_pred, S_obs[k], S_obs[k]-total_pred);
});

print("\n=== Total time: ", (getwalltime()-t0)/1000., " s ===");
quit;
