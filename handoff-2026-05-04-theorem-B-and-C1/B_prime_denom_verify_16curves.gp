/* B' denominator 2-shift identity numerical sanity (16-curve dataset) */
PMAX = 200;
default(realprecision, 30);

A3_local(p, ap, alpha, beta, gamma) = {my(s_ab,s_ag,lp,L_a,L_b,invL_g,zr); s_ab=1+alpha+beta; s_ag=1+alpha+gamma; lp=ap/sqrt(p); L_a=1/(1-lp*p^(-1/2-alpha)+p^(-1-2*alpha)); L_b=1/(1-lp*p^(-1/2-beta)+p^(-1-2*beta)); invL_g=1-lp*p^(-1/2-gamma)+p^(-1-2*gamma); zr=(1-p^(-s_ag))/(1-p^(-s_ab)); L_a*L_b*invL_g*zr};

shift_test(cn, alpha, beta, gamma) = {my(E,N,L,La,Lb,Lg,LHS,zab,zag,Nf,zratio,A3,RHS_lead,p,isbad,i,ap); E=ellinit(cn); N=ellglobalred(E)[1]; L=lfuncreate(E); La=lfun(L,1/2+alpha); Lb=lfun(L,1/2+beta); Lg=lfun(L,1/2+gamma); LHS=La*Lb/Lg; zab=zeta(1+alpha+beta); zag=zeta(1+alpha+gamma); Nf=factor(N); for(i=1,matsize(Nf)[1], p=Nf[i,1]; zab*=(1-p^(-1-alpha-beta)); zag*=(1-p^(-1-alpha-gamma))); zratio=zab/zag; A3=1.0; forprime(p=2,PMAX, isbad=0; for(i=1,matsize(Nf)[1], if(Nf[i,1]==p, isbad=1)); if(!isbad, ap=ellap(E,p); A3*=A3_local(p,ap,alpha,beta,gamma))); RHS_lead=zratio*A3; printf("%s,N=%d,Re_g=%.2f,Im_g=%.2f,|LHS|=%.4f,|RHS|=%.4f,|ratio|=%.4f,arg(LHS/RHS)=%.3f\n", cn, N, real(gamma), imag(gamma), abs(LHS), abs(RHS_lead), abs(LHS/RHS_lead), arg(LHS/RHS_lead))};

curves = ["11a1","14a1","15a1","17a1","19a1","20a1","21a1","24a1","100a1","106c1","200a1","221a1","240a1","496b1","510a1","5005b1"];
alpha = 0.05;
beta = -0.03;

for(gi=1, 3, my(g, gtab); gtab=[0.1+0.5*I, 0.3+0.5*I, 0.5+0.5*I]; g=gtab[gi]; print("=== gamma = ", g, " ==="); for(ci=1, #curves, shift_test(curves[ci], alpha, beta, g)));
quit;
