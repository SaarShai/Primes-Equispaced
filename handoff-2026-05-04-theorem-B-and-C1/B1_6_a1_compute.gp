\\ B1.6 a_1(f)/a_4 numerical test on 16-curve ladder using Opus closed form:
\\ a_1/a_4 = -24 + 24·B - 12·B² - 12·κ_2 + 4·B³ + 12·B·κ_2 + 4·κ_3
\\ where κ_3(f) = (1/8)·[L'''/L − 3·L''/L·L'/L + 2·(L'/L)³] + bad-prime S^(3) + small universal const C_3
\\ Initially compute *without* the C_3 constant (as TBD); fit C_3 from empirical data afterwards.

default(parisizemax, 16000000000);
default(parisize, 2000000000);
default(realprecision, 30);

\\ k2 helpers (from B1_5_a2_v2_compute.gp)
k2m_pp(p) = my(u=1.0/p, lg=log(p)^2); lg*p/(p+1)^2 + 2*lg*u/(1+u);
k2a_pp(p) = my(u=1.0/p, lg=log(p)^2); lg/(1-u)^2 + lg*u^2/(1-u^2)^2;
\\ k3 helpers (analogous third-cumulant of bad-prime local factor — TBD form
\\ For multiplicative bad: cube of Euler factor logarithmic derivative...
\\ Use simple cubic (log p)^3 weighted by bad-prime structure as a placeholder.
\\ Without rigorous bad-prime k3 formula (TBD for v3), set them to 0 and absorb in C_3.
k3m_pp(p) = 0.0;
k3a_pp(p) = 0.0;

zL = lfuncreate(1);
z2val = lfun(zL, 2);
zp_z2 = lfun(zL, 2, 1)/z2val;
gE = 0.57721566490153286061;

print("curve,Ncond,LpL,LppL,LpppL,k2m,k2a,L_cum,L_cum3,B_f,kappa2,kappa3_no_C,a1_a4_no_C,a2_a4,r_pred_a3,r_pred_full_no_C");

curves = ["11a1","14a1","15a1","17a1","19a1","20a1","21a1","24a1","100a1","106c1","200a1","221a1","240a1","496b1","510a1","5005b1"];

\\ Y per curve
Y_per = [4.5381, 4.6293, 4.6584, 4.7081, 4.7510, 4.7722, 4.7885, 4.8443, 5.4165, 5.4420, 5.7010, 5.7420, 5.7777, 6.0791, 6.0935, 7.0593];

for(idx=1, #curves, cn=curves[idx]; E=ellinit(cn); Ncond=ellglobalred(E)[1]; Nf=factor(Ncond); L=lfunsympow(E,2); v0=lfun(L,2); v1=lfun(L,2,1); v2=lfun(L,2,2); v3=lfun(L,2,3); LpL=v1/v0; LppL=v2/v0; LpppL=v3/v0; k2m=0.0; k2a=0.0; sumlp=0.0; Smult=0.0; Sadd=0.0; for(jj=1, matsize(Nf)[1], pj=Nf[jj,1]; ej=Nf[jj,2]; sumlp=sumlp+log(pj)/(pj+1); if(ej==1, k2m=k2m+k2m_pp(pj); Smult=Smult+pj*log(pj)/(pj^2-1)); if(ej>=2, k2a=k2a+k2a_pp(pj); Sadd=Sadd+log(pj)/(pj-1))); H_unram=LpL-2*zp_z2+sumlp-Smult-Sadd; B_f=gE+H_unram+Smult+Sadd; L_cum=LppL-LpL^2; kappa2=0.75*L_cum - 0.5*k2m - 0.25*k2a - log(2*Pi); L_cum3=LpppL - 3*LppL*LpL + 2*LpL^3; kappa3_no_C=0.125*L_cum3; a2_a4=12 - 12*B_f + 6*B_f^2 + 6*kappa2; a1_a4_no_C=-24 + 24*B_f - 12*B_f^2 - 12*kappa2 + 4*B_f^3 + 12*B_f*kappa2 + 4*kappa3_no_C; Y=Y_per[idx]; r_a3=(-4+4*B_f)/Y; r_full=r_a3 + a2_a4/Y^2 + a1_a4_no_C/Y^3; printf("%s,%d,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f\n", cn, Ncond, LpL, LppL, LpppL, k2m, k2a, L_cum, L_cum3, B_f, kappa2, kappa3_no_C, a1_a4_no_C, a2_a4, r_a3, r_full));

quit;
