/* ============================================================
   Smoothed_Dwf_numerical.gp
   Numerical verification of the Smoothed Delta_w_e (Mobius) explicit
   formula with R0 = -2.

   Identity tested (canonical case f = e_1, W(x) = exp(-x^2)):

     M_W(N) := sum_{n>=1} mu(n) * exp(-(n/N)^2)
            = R0 + Zsum(N) + tail(N)

   where R0 = 1/zeta(0) = -2 (residue of M_W(s) = (1/2) Gamma(s/2)
   at s=0 against 1/zeta(s); res of M_W = 1, value 1/zeta(0) = -2).

   Zsum(N) = 2 * Re sum_{rho zeta-zero, Im rho > 0}
                       N^rho * M_W(rho) / zeta'(rho).

   Author: Saar Shai, 2026-05-03
   ============================================================ */

default(realprecision, 50);
default(parisize, "256M");

print("Computing zeta zeros up to T=250...");
gammas = lfunzeros(1, [0, 250]);
NUM_ZEROS = length(gammas);
print("  obtained ", NUM_ZEROS, " zeros, gamma_1=", gammas[1]);
print("  gamma_{end}=", gammas[NUM_ZEROS]);

print("Computing zeta'(rho_k) at each zero...");
zetapr = vector(NUM_ZEROS);
{
for(k=1, NUM_ZEROS,
  rho = 1/2 + I*gammas[k];
  zetapr[k] = lfun(1, rho, 1)
);
}

print("Computing M_W(rho_k) = (1/2)*Gamma(rho_k/2) at each zero...");
MWrho = vector(NUM_ZEROS);
{
for(k=1, NUM_ZEROS,
  rho = 1/2 + I*gammas[k];
  MWrho[k] = (1/2) * gamma(rho/2)
);
}

LHS(N) = {
  my(s = 0.0, ncut, nN);
  ncut = ceil(12*N);
  nN = 1.0/N;
  s = 0.0;
  for(n = 1, ncut,
    s = s + moebius(n) * exp(-(n*nN)^2)
  );
  return(s);
};

Zsum(N, K = NUM_ZEROS) = {
  my(s = 0.0, rho, Nf);
  Nf = 1.0 * N;
  for(k = 1, K,
    rho = 1/2 + I*gammas[k];
    s = s + Nf^rho * MWrho[k] / zetapr[k]
  );
  return(2 * real(s));
};

R0 = -2;

print("");
print("=== Smoothed Mobius identity verification ===");
print("Identity: LHS(N) = R0 + Zsum(N) + tail(N), R0 = -2");
print("Using ", NUM_ZEROS, " zeros");
print("");
print("    N |       LHS(N)          |     LHS(N)-R0         |     Zsum(N)           |  |residual|");
print("------|-----------------------|-----------------------|-----------------------|------------");

test_Ns = [11, 14, 17, 19, 21, 50, 100, 300, 1000, 3000, 10000];
{
for(i = 1, length(test_Ns),
  N = test_Ns[i];
  L = LHS(N);
  Z = Zsum(N);
  r = L - R0 - Z;
  printf("%5d | %21.14f | %21.14f | %21.14f | %.4e\n", N, L, L-R0, Z, abs(r))
);
}

print("");
print("=== Squarefree-only counter-check at N=11 ===");
{
my(N=11, sf, ssf);
sf = 0.0; ssf = 0.0;
for(n=1, 12*N,
  if(moebius(n) != 0,
    sf = sf + moebius(n) * exp(-(n*1.0/N)^2);
    if(issquarefree(n),
      ssf = ssf + moebius(n) * exp(-(n*1.0/N)^2)
    )
  )
);
printf("  full=%.14f, squarefree-only=%.14f, diff=%.2e\n", sf, ssf, abs(sf-ssf));
}

print("");
print("=== Zero-count sensitivity at N=10000 ===");
{
my(N=10000, L, Z, K);
L = LHS(N);
printf("  LHS(N=10000) - R0 = %.14f\n", L - R0);
foreach([10, 25, 50, 100, 250, NUM_ZEROS], K,
  if(K <= NUM_ZEROS,
    Z = Zsum(N, K);
    printf("  K=%4d zeros: Zsum=%.14f, residual=%.4e\n", K, Z, abs(L - R0 - Z))
  )
);
}

print("");
print("=== Tail-decay check at K=NUM_ZEROS ===");
{
my(L, Z, r);
foreach([100, 1000, 10000, 100000], N,
  L = LHS(N);
  Z = Zsum(N);
  r = L - R0 - Z;
  printf("  N=%6d: LHS-R0=%.10f, Zsum=%.10f, residual=%.4e\n", N, L-R0, Z, abs(r))
);
}

print("");
print("=== Done ===");

quit;
