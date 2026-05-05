default(parisizemax, 16000000000);
default(parisize, 2000000000);
default(realprecision, 30);

\\ kappa_2^good per prime: (h_p''/h_p)(1) - ((h_p'/h_p)(1))^2
\\ = (log p)^2 [ sum_{j in {2,0,-2}} beta^j u/(1-beta^j u)^2 - u/(1-u)^2 - 2 u^2(1+u^2)/(1-u^2)^2 ]
kappa2_good_per_prime(p, ap) = my(u=1.0/p, lg=log(p)^2, disc=ap^2-4*p, b2, bn2, sd, theta, ss=0); if(disc>=0, sd=sqrt(disc); b2=((ap+sd)/(2*sqrt(p)))^2; bn2=1/b2, theta=acos(ap/(2*sqrt(p))); b2=exp(I*2*theta); bn2=exp(-I*2*theta)); ss = b2*u/(1-b2*u)^2 + u/(1-u)^2 + bn2*u/(1-bn2*u)^2 - u/(1-u)^2 - 2*u^2*(1+u^2)/(1-u^2)^2; real(lg*ss);

kappa2_mult_per_prime(p) = my(u=1.0/p, lg=log(p)^2); lg*p/(p+1)^2 + 2*lg*u/(1+u);

kappa2_add_per_prime(p) = my(u=1.0/p, lg=log(p)^2); lg/(1-u)^2 + lg*u^2/(1-u^2)^2;

zL = lfuncreate(1);
z2val = lfun(zL, 2);
zp_z2 = lfun(zL, 2, 1)/z2val;
zpp_z2 = lfun(zL, 2, 2)/z2val;
\\ ζ-cumulant: (ζ''/ζ)(2) - (ζ'/ζ)(2)^2  (corrected sign per v2)
G_zeta_cumulant = zpp_z2 - zp_z2^2;
gE = 0.57721566490153286061;
print("# zeta-cumulant (zpp/z - (zp/z)^2) at s=2 = ", G_zeta_cumulant);
print("");
print("curve,Ncond,LpL,LppL,L_cumulant,k2_good,k2_mult,k2_add,kappa2_total,B_f,a2_over_a4,delta_2");

PMAX = 10000;
curves = ["11a1","14a1","15a1","17a1","19a1","20a1","21a1","24a1","100a1","106c1","200a1","221a1","240a1","496b1","510a1","5005b1"];

for(idx=1, #curves, cn=curves[idx]; E=ellinit(cn); Ncond=ellglobalred(E)[1]; Nf=factor(Ncond); L=lfunsympow(E,2); v0=lfun(L,2); v1=lfun(L,2,1); v2=lfun(L,2,2); LpL=v1/v0; LppL=v2/v0; bad=vector(matsize(Nf)[1], j, Nf[j,1]); k2g=0.0; pp=2; while(pp<=PMAX, isbad=0; for(j=1, length(bad), if(bad[j]==pp, isbad=1)); if(!isbad, k2g=k2g+kappa2_good_per_prime(pp, ellap(E,pp))); pp=nextprime(pp+1)); k2m=0.0; k2a=0.0; sumlp=0.0; for(jj=1, matsize(Nf)[1], pj=Nf[jj,1]; ej=Nf[jj,2]; if(ej==1, k2m=k2m+kappa2_mult_per_prime(pj)); if(ej>=2, k2a=k2a+kappa2_add_per_prime(pj)); sumlp=sumlp+log(pj)/(pj+1)); L_cumul=LppL - LpL^2; kappa2_total=k2g+k2m+k2a+L_cumul+G_zeta_cumulant; B_f=gE+LpL-2*zp_z2+sumlp; a2_a4=12 - 12*B_f + 6*B_f^2 + 6*kappa2_total; delta2=a2_a4-12; printf("%s,%d,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f\n", cn, Ncond, LpL, LppL, L_cumul, k2g, k2m, k2a, kappa2_total, B_f, a2_a4, delta2));

quit;
