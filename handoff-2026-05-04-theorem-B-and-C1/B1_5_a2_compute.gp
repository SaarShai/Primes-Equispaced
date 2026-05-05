default(parisizemax, 16000000000);
default(parisize, 2000000000);
default(realprecision, 30);

K2_good_per_prime(p, ap) = my(u=1.0/p, lg=log(p)^2, disc=ap^2-4*p, beta_sq, beta_neg_sq, sd, theta, ss=0); if(disc>=0, sd=sqrt(disc); beta_sq=((ap+sd)/(2*sqrt(p)))^2; beta_neg_sq=1/beta_sq, theta=acos(ap/(2*sqrt(p))); beta_sq=exp(I*2*theta); beta_neg_sq=exp(-I*2*theta)); ss = beta_sq*u/(1-beta_sq*u)^2 + u/(1-u)^2 + beta_neg_sq*u/(1-beta_neg_sq*u)^2 - u/(1-u)^2 - 2*u^2*(1+u^2)/(1-u^2)^2; real(lg*ss);

K2_mult_per_prime(p) = my(u=1.0/p, lg=log(p)^2); lg*p/(p+1)^2 + 2*lg*u/(1+u);

K2_add_per_prime(p) = my(u=1.0/p, lg=log(p)^2); lg/(1-u)^2 + lg*u^2/(1-u^2)^2;

zL = lfuncreate(1);
z2val = lfun(zL, 2);
zp_z2 = lfun(zL, 2, 1)/z2val;
zpp_z2 = lfun(zL, 2, 2)/z2val;
G_univ = zp_z2^2 - zpp_z2;
gE = 0.57721566490153286061;
print("# zp_z2=", zp_z2, "  zpp_z2=", zpp_z2, "  G_univ=", G_univ);
print("");
print("curve,Ncond,LpL,LppL,K2_good,K2_mult,K2_add,G_curve,B_f,a2_over_a4");

PMAX = 5000;
curves = ["11a1","14a1","15a1","17a1","19a1","20a1","21a1","24a1","100a1","106c1","200a1","221a1","240a1","496b1","510a1","5005b1"];

\\ wrap entire loop body inside one-shot expression with comma-separated statements
for(idx=1, #curves, cn=curves[idx]; E=ellinit(cn); Ncond=ellglobalred(E)[1]; Nf=factor(Ncond); L=lfunsympow(E,2); v0=lfun(L,2); v1=lfun(L,2,1); v2=lfun(L,2,2); LpL=v1/v0; LppL=v2/v0; bad=vector(matsize(Nf)[1], j, Nf[j,1]); K2g=0.0; pp=2; while(pp<=PMAX, isbad=0; for(j=1, length(bad), if(bad[j]==pp, isbad=1)); if(!isbad, K2g=K2g+K2_good_per_prime(pp, ellap(E,pp))); pp=nextprime(pp+1)); K2m=0.0; K2a=0.0; sumlp=0.0; for(jj=1, matsize(Nf)[1], pj=Nf[jj,1]; ej=Nf[jj,2]; if(ej==1, K2m=K2m+K2_mult_per_prime(pj)); if(ej>=2, K2a=K2a+K2_add_per_prime(pj)); sumlp=sumlp+log(pj)/(pj+1)); G_curve=G_univ + 2*gE*LpL + LppL - LpL^2; K2_arith=K2g+K2m+K2a; B_f=gE+LpL-2*zp_z2+sumlp; a2_over_a4=12+24*B_f^2-32*B_f+2*K2_arith+2*G_curve; printf("%s,%d,%.8f,%.8f,%.8f,%.8f,%.8f,%.8f,%.8f,%.8f\n", cn, Ncond, LpL, LppL, K2g, K2m, K2a, G_curve, B_f, a2_over_a4));

quit;
