\\ B3 numerical verification on 16-curve weight-2 EC ladder
\\ Compute u_f = U_f(T) / (c_f · T · log⁴X) for each of 16 curves
\\ where U_f(T) = Σ_{0 < γ_f ≤ T} |L'(1+iγ_f, f)|²
\\ M-N cage (unconditional): u_f ∈ [(17-√145)/(12π), (17+√145)/(12π)] = [0.132, 0.770]
\\ Opus tighter cage (unconditional, weight aspect): u_f ∈ [1/(6π), 2/(3π)] = [0.053, 0.212]
\\ Conjectural value (M-N predicted, GRH+ratios): u_f = 2/(3π) ≈ 0.212
\\ For weight-2 EC, the data may not match Opus's weight-aspect cage exactly (k=2 fixed),
\\ but should validate whether u_f cluster near 0.212 (conjectural) or scatter inside cage.

default(parisizemax, 16000000000);
default(parisize, 2000000000);
default(realprecision, 30);

curves = ["11a1","14a1","15a1","17a1","19a1","20a1","21a1","24a1","100a1","106c1","200a1","221a1","240a1","496b1","510a1","5005b1"];

\\ T_200 from W2_CF_RESOLVED.json
T_per = [177.16, 172.02, 171.10, 168.91, 166.78, 166.04, 164.70, 162.91, 141.43, 140.91, 132.92, 131.73, 131.01, 123.19, 123.25, 103.35];

print("# B3 NUMERICAL VERIFICATION");
print("# u_f = U_f(T_200) / (c_f * T_200 * log^4 X), X = sqrt(N)*T_200/2pi");
print("# Cages: M-N [0.132, 0.770]; Opus [0.053, 0.212]; conjectural 0.212");
print("");
print("curve,N,T_200,Y,c_f,zero_count,U_f,u_f,in_MN_cage,in_Opus_cage,delta_to_target");

for(idx=1, #curves, cn=curves[idx]; E=ellinit(cn); N_cond=ellglobalred(E)[1]; L=lfuncreate(E); T_max=T_per[idx]; X=sqrt(N_cond)*T_max/(2*Pi); Y=log(X); zs=lfunzeros(L, T_max); n_zeros=length(zs); U=0.0; for(j=1,n_zeros, gamma_j=zs[j]; rho=1.0/2 + I*gamma_j; Lp=lfun(L, rho, 1); U=U+abs(Lp)^2); L_sym2=lfunsympow(E,2); cf=lfun(L_sym2, 2)/zeta(2); u_f=U/(cf*T_max*Y^4); in_mn = (u_f >= 0.132 && u_f <= 0.770); in_opus = (u_f >= 0.053 && u_f <= 0.212); delta=u_f - 2/(3*Pi); printf("%s,%d,%.2f,%.4f,%.4f,%d,%.4f,%.6f,%d,%d,%+.4f\n", cn, N_cond, T_max, Y, cf, n_zeros, U, u_f, in_mn, in_opus, delta));

quit;
