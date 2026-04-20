/* Quick PARI/GP check: compare wrong vs correct μ_f(p²) coefficients for C₁.
   37a1: first complex zero γ_2 ≈ 5.003170
   Δ:    first zero γ_1 ≈ 9.222379
*/
\p 30
default(parisizemax, 2*10^9);

/* ---- 37a1 setup ---- */
E37 = ellinit([0,0,1,-1,0]);
rho37 = 1 + I*5.00317001400665869534627315571;

/* Build mu coefficients two ways for K=5000 */
K = 5000;

/* WRONG version: mu_wrong(p²) = a_p² - p */
c_wrong = 0;
c_correct = 0;
for(n=1, K,
    mu_w = 0; mu_c = 0;
    /* For simplicity: only count squarefree and p²-terms */
    fac = factor(n);
    ok = 1;
    mu_w = 1; mu_c = 1;
    for(j=1, #fac[,1],
        p = fac[j,1]; e = fac[j,2];
        ap = ellap(E37, p);
        if(e==1,
            mu_w *= -ap; mu_c *= -ap
        ,if(e==2,
            mu_w *= ap^2 - p;  /* WRONG */
            mu_c *= p;         /* CORRECT */
        , /* e>=3: both give 0 */
            mu_w = 0; mu_c = 0; ok=0; break
        ))
    );
    c_wrong += mu_w * exp(-n/K) / n^rho37;
    c_correct += mu_c * exp(-n/K) / n^rho37;
    if(n%500==0, print("n=",n));
);

/* L'(rho37) via PARI */
L37 = lfuninit(E37, [1, 10]);
g2 = lfunzeros(L37, [4.9, 5.1])[1];
rho37_exact = 1 + I*g2;
lp37 = lfun(L37, rho37_exact, 1);
lp37_abs = abs(lp37);

C1_wrong = abs(c_wrong) * lp37_abs / (log(K) + Euler);
C1_correct = abs(c_correct) * lp37_abs / (log(K) + Euler);
print("37a1 at K=",K,":");
print("  C₁ (wrong μ p²): ", C1_wrong);
print("  C₁ (correct μ p²): ", C1_correct);
print("  Ratio: ", C1_correct/C1_wrong);

/* ---- Delta setup ---- */
mf = mfinit([1,12],1); f = mfbasis(mf)[1];
rho_delta = 6 + I*9.22237939992110252224376719274;

c_wrong_d = 0;
c_correct_d = 0;
K2 = 1000;  /* smaller K for Delta since p^11 is huge */
for(n=1, K2,
    mu_w = 0; mu_c = 0;
    fac = factor(n);
    mu_w = 1; mu_c = 1;
    for(j=1, #fac[,1],
        p = fac[j,1]; e = fac[j,2];
        tp = mfcoefs(f, p)[p+1];  /* tau(p) */
        if(e==1,
            mu_w *= -tp; mu_c *= -tp
        ,if(e==2,
            mu_w *= tp^2 - p^11;  /* WRONG = tau(p²) */
            mu_c *= p^11;         /* CORRECT */
        ,
            mu_w = 0; mu_c = 0; break
        ))
    );
    c_wrong_d += mu_w * exp(-n/K2) / n^rho_delta;
    c_correct_d += mu_c * exp(-n/K2) / n^rho_delta;
);

/* L'(rho_delta) */
Ld = lfuninit(f, [6, 20]);
g_d = lfunzeros(Ld, [9.1, 9.4])[1];
rho_d_exact = 6 + I*g_d;
lp_d = lfun(Ld, rho_d_exact, 1);
lp_d_abs = abs(lp_d);

C1_wrong_d = abs(c_wrong_d) * lp_d_abs / (log(K2) + Euler);
C1_correct_d = abs(c_correct_d) * lp_d_abs / (log(K2) + Euler);
print("Delta at K=",K2,":");
print("  C₁ (wrong μ p²): ", C1_wrong_d);
print("  C₁ (correct μ p²): ", C1_correct_d);
print("  Ratio: ", C1_correct_d/C1_wrong_d);

print("\nDONE");
quit;
