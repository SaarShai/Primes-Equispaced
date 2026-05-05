\\ Hypothesis from Opus 4.7: (L'/L)_anal(1, sym²f) = (L'/L)_arith(2, sym²f)
\\ because L_arith(s) = L_anal(s − 1) (integer shift from a_p²−p = p(λ_p²−1)).
\\ Evaluate pari L'/L at arith s = 2 for all 16 curves.

default(parisizemax, 8000000000);
default(parisize, 1000000000);
default(realprecision, 30);

curves = ["11a1","14a1","15a1","17a1","19a1","20a1","21a1","24a1","100a1","106c1","200a1","221a1","240a1","496b1","510a1","5005b1"];

print("curve,N,Lp_over_L_sym2_at_s2_arith,method");

for(i=1, #curves, {
  cn = curves[i];
  E = ellinit(cn);
  N = ellglobalred(E)[1];
  L = lfunsympow(E, 2);
  v0 = lfun(L, 2);
  v1 = lfun(L, 2, 1);
  ratio = v1 / v0;
  printf("%s,%d,%.18f,pari_lfun_at_s2\n", cn, N, ratio);
});
quit;
