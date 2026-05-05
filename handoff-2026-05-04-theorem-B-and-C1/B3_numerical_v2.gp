\\ B3 numerical V2 — corrected critical-line convention
\\ pari's lfunzeros returns imaginary parts γ such that L has a zero on the critical line
\\ For elliptic curves in pari's arithmetic norm, central line is σ=1 (NOT σ=1/2)
\\ So zeros are at ρ_f = 1 + iγ_f, and we evaluate L'(1 + iγ_f, f)

default(parisizemax, 16000000000);
default(parisize, 2000000000);
default(realprecision, 30);

curves = ["11a1","14a1","15a1","17a1","19a1","20a1","21a1","24a1","100a1","106c1","200a1","221a1","240a1","496b1","510a1","5005b1"];
T_per = [177.16, 172.02, 171.10, 168.91, 166.78, 166.04, 164.70, 162.91, 141.43, 140.91, 132.92, 131.73, 131.01, 123.19, 123.25, 103.35];

print("# B3 V2 — corrected: ρ_f = 1 + iγ_f (arithmetic norm for EC)");
print("# Target: u_f ∈ M-N cage [0.132, 0.770], conjectural 0.212");
print("");
print("curve,N,T_max,Y,c_f,n_zeros,U_f,u_f,first_few_|L'|²");

for(idx=1, #curves, cn=curves[idx]; E=ellinit(cn); N_cond=ellglobalred(E)[1]; L=lfuncreate(E); T_max=T_per[idx]; X=sqrt(N_cond)*T_max/(2*Pi); Y=log(X); zs=lfunzeros(L, T_max); n_zeros=length(zs); U=0.0; samples=List([]); for(j=1,n_zeros, gamma_j=zs[j]; rho=1.0+I*gamma_j; Lp=lfun(L, rho, 1); Lp2=abs(Lp)^2; U=U+Lp2; if(j<=3, listput(samples, Lp2))); L_sym2=lfunsympow(E,2); cf=lfun(L_sym2, 2)/zeta(2); u_f=U/(cf*T_max*Y^4); printf("%s,%d,%.2f,%.4f,%.4f,%d,%.6f,%.6f,%s\n", cn, N_cond, T_max, Y, cf, n_zeros, U, u_f, Vec(samples)));

quit;
