\\ B1.1 — L'/L(1, sym²f) for 16-curve weight-2 EC ladder
\\ Run: gp -q B1_lprime_sym2.gp > B1_lprime_sym2.out 2>&1 &

default(realprecision, 30);

curves = ["11a1","14a1","15a1","17a1","19a1","20a1","21a1","24a1","100a1","106c1","200a1","221a1","240a1","496b1","510a1","5005b1"];

print("curve,N,Lp_over_L_sym2_at_1,abserr_est,method,time_sec");

for(i=1, #curves, {
  cn = curves[i];
  t0 = getwalltime();
  E = ellinit(cn);
  N = ellglobalred(E)[1];
  \\ build sym^2 L-function via lfunsymsqr
  L = lfunsympow(E, 2);
  \\ derivative at s=1: numerical via 5-point stencil
  h = 1e-8;
  v0 = lfun(L, 1);
  vp = lfun(L, 1 + h);
  vm = lfun(L, 1 - h);
  vpp= lfun(L, 1 + 2*h);
  vmm= lfun(L, 1 - 2*h);
  Lprime = (vmm - 8*vm + 8*vp - vpp)/(12*h);
  ratio = Lprime / v0;
  err_est = abs(((vm - 2*v0 + vp)/h^2) * h^2 / 12);  \\ truncation est
  dt = (getwalltime() - t0)/1000.;
  printf("%s,%d,%.18f,%.2e,pari_lfunsymsqr_5pt,%.2f\n", cn, N, ratio, err_est, dt);
});

print("done");
quit;
