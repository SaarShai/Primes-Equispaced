\\ B1.6 v2 — full a_1/a_4 with Opus κ_3 closed form:
\\ κ_3 = (5/8)·L_cum3 − (3/8)·S3_mult − (1/8)·S3_add − γ_E·log(2π)
\\ S^{(3)}_mult = Σ_{p‖N} (log p)³·2u(1+6u²+u⁴)/(1-u²)³
\\ S^{(3)}_add  = Σ_{p²|N} same form

default(parisizemax, 16000000000);
default(parisize, 2000000000);
default(realprecision, 30);

k2m_pp(p) = my(u=1.0/p, lg=log(p)^2); lg*p/(p+1)^2 + 2*lg*u/(1+u);
k2a_pp(p) = my(u=1.0/p, lg=log(p)^2); lg/(1-u)^2 + lg*u^2/(1-u^2)^2;
\\ S^{(3)} per prime: (log p)^3 · 2u(1+6u²+u⁴)/(1-u²)³
s3_pp(p) = my(u=1.0/p, lg3=log(p)^3); lg3 * 2*u*(1+6*u^2+u^4)/(1-u^2)^3;

zL = lfuncreate(1);
zp_z2 = lfun(zL, 2, 1)/lfun(zL, 2);
gE = 0.57721566490153286061;
log2pi = log(2*Pi);

print("curve,N,B,k2,k3,a3_a4,a2_a4,a1_a4,r_a3,r_full");

curves = ["11a1","14a1","15a1","17a1","19a1","20a1","21a1","24a1","100a1","106c1","200a1","221a1","240a1","496b1","510a1","5005b1"];
Y_per = [4.5381, 4.6293, 4.6584, 4.7081, 4.7510, 4.7722, 4.7885, 4.8443, 5.4165, 5.4420, 5.7010, 5.7420, 5.7777, 6.0791, 6.0935, 7.0593];

for(idx=1, #curves, cn=curves[idx]; E=ellinit(cn); Ncond=ellglobalred(E)[1]; Nf=factor(Ncond); L=lfunsympow(E,2); v0=lfun(L,2); v1=lfun(L,2,1); v2=lfun(L,2,2); v3=lfun(L,2,3); LpL=v1/v0; LppL=v2/v0; LpppL=v3/v0; k2m=0.0; k2a=0.0; s3m=0.0; s3a=0.0; sumlp=0.0; Smult=0.0; Sadd=0.0; for(jj=1, matsize(Nf)[1], pj=Nf[jj,1]; ej=Nf[jj,2]; sumlp=sumlp+log(pj)/(pj+1); if(ej==1, k2m=k2m+k2m_pp(pj); s3m=s3m+s3_pp(pj); Smult=Smult+pj*log(pj)/(pj^2-1)); if(ej>=2, k2a=k2a+k2a_pp(pj); s3a=s3a+s3_pp(pj); Sadd=Sadd+log(pj)/(pj-1))); H_unram=LpL-2*zp_z2+sumlp-Smult-Sadd; B_f=gE+H_unram+Smult+Sadd; L_cum=LppL-LpL^2; L_cum3=LpppL - 3*LppL*LpL + 2*LpL^3; kappa2=0.75*L_cum - 0.5*k2m - 0.25*k2a - log2pi; kappa3=(5.0/8)*L_cum3 - (3.0/8)*s3m - (1.0/8)*s3a - gE*log2pi; a3_a4=-4+4*B_f; a2_a4=12-12*B_f+6*B_f^2+6*kappa2; a1_a4=-24+24*B_f-12*B_f^2-12*kappa2+4*B_f^3+12*B_f*kappa2+4*kappa3; Y=Y_per[idx]; r_a3=a3_a4/Y; r_full=r_a3+a2_a4/Y^2+a1_a4/Y^3; printf("%s,%d,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f\n", cn, Ncond, B_f, kappa2, kappa3, a3_a4, a2_a4, a1_a4, r_a3, r_full));

quit;
