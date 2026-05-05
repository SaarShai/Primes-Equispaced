default(realprecision, 30);

\\ Probe pari's lfunsympow normalization
\\ Question: does lfun(L,s) return L(s) (Dirichlet) or Lambda(s) (completed)?

curves = ["11a1", "14a1", "221a1", "20a1"];
for(i=1, #curves, {
  cn = curves[i];
  E = ellinit(cn);
  L = lfunsympow(E, 2);
  N_sym2 = lfunan(L, 1)[1];  \\ first Dirichlet coefficient (should be 1)
  v0 = lfun(L, 1);
  \\ pari's lfuncreate stores all params; access via getlocal
  Lan_first = lfunan(L, 5);  \\ first 5 Dirichlet coefficients
  printf("%s: L(1,sym2)=%.10f, first 5 a_n: %s\n", cn, v0, Lan_first);
});

\\ Now: predicted L(1, sym^2(E)) = ratio of completed Lambda evaluated.
\\ For sym^2 of weight-2 EC, the gamma factor is Gamma_R(s+1) * Gamma_C(s)
\\ = pi^{-(s+1)/2} Gamma((s+1)/2) * (2pi)^{-s} Gamma(s)
\\ At s=1: Gamma_R(2)*Gamma_C(1) = pi^{-1} * 1 * (2pi)^{-1} * 1 = 1/(2 pi^2)

\\ Critical: compare lfun(L,s)*lfungammafactor with what we expect
\\ Better: just check L'/L at s=1 directly via pari's lfun derivative
print("--- direct derivative via lfun ---");
for(i=1, #curves, {
  cn = curves[i];
  E = ellinit(cn);
  L = lfunsympow(E, 2);
  \\ pari has lfun(L, s, der) where der is derivative order
  v0 = lfun(L, 1);
  v1 = lfun(L, 1, 1);  \\ first derivative
  ratio = v1 / v0;
  printf("%s: L(1)=%.10f, L'(1)=%.10f, L'/L(1)=%.10f\n", cn, v0, v1, ratio);
});

\\ Compare to my 5-point stencil values
print("--- expected from earlier 5-pt stencil ---");
print("11a1: 1.252077865588207488");
print("14a1: 0.933994930191732195");
print("221a1: -3.374855409201785821");
print("20a1: 1.320362233623441846");
quit;
