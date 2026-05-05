default(parisizemax, 16000000000);
default(parisize, 2000000000);
default(realprecision, 30);

\\ weight 24, level 37 newform; small Petersson family case
mf = mfinit([37, 24], 1);
basis = mfeigenbasis(mf);
print("# Number of newforms: ", length(basis));
F = basis[1];
L = lfunmf(mf, F);

T_max = 100;
zs = lfunzeros(L, T_max);
n_zeros = length(zs);
printf("# n_zeros up to T=%d: %d\n", T_max, n_zeros);

\\ Find central by testing
print("# Test centrals:");
for(c=23, 25, val=lfun(L, c/2 + I*zs[1]); printf("# σ=%.1f |L|=%.4e\n", c/2., abs(val)));

\\ For weight-k modular form, central is σ = k/2 = 12 in pari arithmetic
central = 12;

\\ One-line for body to avoid multi-line parse issues
U = 0.0;
for(j=1, n_zeros, U = U + abs(lfun(L, central + I*zs[j], 1))^2);

\\ Compute c_f via L(1, sym²f)/ζ(2)
\\ For weight-k, sym² L can be obtained via lfunsymsqr or lfunsympow
\\ Try lfunsymsqr first, fallback if not available
\\ For weight 24, sym² is degree 3 (just like for weight 2)
sym2 = lfunsymsqr(L);
cf = lfun(sym2, 1) / zeta(2);
printf("# c_f = L(1, sym²)/ζ(2) = %.6f\n", cf);

X = sqrt(37) * 24 * T_max / (2*Pi);
Y = log(X);

printf("# T=%d, X=%.4f, log(NkT)=%.4f, log^4=%.4f\n", T_max, X, Y, Y^4);
printf("# U = Σ |L'(ρ_f)|² = %.6f\n", U);
predicted = 2/(3*Pi) * cf * T_max * Y^4;
printf("# Predicted (2/(3π))·c_f·T·log^4 = %.6f\n", predicted);
printf("# Ratio U / predicted = %.4f  (target: 1.0)\n", U / predicted);
printf("# u_normalized = U/(c_f·T·log^4) = %.6f  (target: 2/(3π) ≈ %.6f)\n", U/(cf*T_max*Y^4), 2/(3*Pi));

quit;
