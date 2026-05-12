default(realprecision, 50);
G5  = znstar(5,1);  chi5  = lfuncreate([G5,  [1]]);
G11 = znstar(11,1); chi11 = lfuncreate([G11, [1]]);
chi5sq  = lfuncreate([G5,  [2]]);
chi11sq = lfuncreate([G11, [2]]);

t3 = 6.1835781954508539144;
t4 = 3.5470410917194500767;

eval_5(n)  = my(ev = chareval(G5,  [1], n)); if(ev == -1, 0, exp(2*Pi*I*ev));
eval_11(n) = my(ev = chareval(G11, [1], n)); if(ev == -1, 0, exp(2*Pi*I*ev));

T_K_stream(eval_fn, rho, K) = my(T = 0., c, z, lg); forprime(p = 2, K, c = eval_fn(p); if(c, z = c*p^(-rho); lg = -log(1-z) - z; T = T + lg)); T;

BPC2(eval_fn, rho, pmax) = my(s = 0., c, ksum); for(k = 2, 12, ksum = 0.; forprime(p = 2, pmax, c = eval_fn(p); if(c, ksum = ksum + c^(2*k) * p^(-2*k*rho))); s = s + ksum / k); -s/2;

Tge3(eval_fn, rho, pmax) = my(s = 0., c, ksum); for(k = 3, 12, ksum = 0.; forprime(p = 2, pmax, c = eval_fn(p); if(c, ksum = ksum + c^k * p^(-k*rho))); s = s + ksum / k); s;

K2 = 2000000;

print("=== chi_5 at K = ", K2, " (components also at p <= ", K2, ") ===");
rho_5 = 1/2 + I*t3;
halflogL_5 = log(lfun(chi5sq, 2*rho_5))/2;
bpc2_5 = BPC2((n)->eval_5(n), rho_5, K2);
tge3_5 = Tge3((n)->eval_5(n), rho_5, K2);
RHS_5 = halflogL_5 + bpc2_5 + tge3_5;
T_K_5 = T_K_stream((n)->eval_5(n), rho_5, K2);
print("  RHS = ", RHS_5);
print("  T_K = ", T_K_5);
print("  T_K - RHS = ", T_K_5 - RHS_5);
print("  |T_K - RHS| = ", abs(T_K_5 - RHS_5));
print("");

print("=== chi_11 at K = ", K2, " ===");
rho_11 = 1/2 + I*t4;
halflogL_11 = log(lfun(chi11sq, 2*rho_11))/2;
bpc2_11 = BPC2((n)->eval_11(n), rho_11, K2);
tge3_11 = Tge3((n)->eval_11(n), rho_11, K2);
RHS_11 = halflogL_11 + bpc2_11 + tge3_11;
T_K_11 = T_K_stream((n)->eval_11(n), rho_11, K2);
print("  RHS = ", RHS_11);
print("  T_K = ", T_K_11);
print("  T_K - RHS = ", T_K_11 - RHS_11);
print("  |T_K - RHS| = ", abs(T_K_11 - RHS_11));
quit;
