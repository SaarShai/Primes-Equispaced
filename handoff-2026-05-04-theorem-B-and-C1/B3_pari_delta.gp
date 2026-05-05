default(parisizemax, 16000000000);
default(parisize, 2000000000);
default(realprecision, 30);

\\ Use Δ (Ramanujan tau) — weight 12, level 1, the unique newform
mf = mfinit([1, 12], 1);
basis = mfeigenbasis(mf);
print("# basis size = ", length(basis));
F = basis[1];
L = lfunmf(mf, F);

\\ Verify L is well-formed
print("# L conductor = ", lfuncost(L));
T_max = 50;
zs = lfunzeros(L, T_max);
n_zeros = length(zs);
printf("# zeros up to T=%d: %d\n", T_max, n_zeros);
if(n_zeros > 0, printf("# first 3 zeros γ: %.4f %.4f %.4f\n", zs[1], zs[2], zs[3]));

\\ Test pari's central — for weight-12, central s = 6 in arithmetic
print("# Testing central values:");
for(c=5, 7, x = c + I*zs[1]; val = abs(lfun(L, x)); printf("# at σ=%d: |L| = %.4e\n", c, val));
for(c=11, 13, x = c/2.0 + I*zs[1]; val = abs(lfun(L, x)); printf("# at σ=%.1f: |L| = %.4e\n", c/2.0, val));

\\ Pari for modular forms: lfun normalizes to "analytic" with central at σ=k/2 (arithmetic)
\\ But lfunzeros returns purely imaginary parts γ such that ρ = central + iγ
\\ So central = k/2 = 6 for weight 12

central = 6;
U = 0.0;
for(j=1, n_zeros, U = U + abs(lfun(L, central + I*zs[j], 1))^2);

cf = lfun(lfunsymsqr(L), 1) / zeta(2);
printf("# c_f for Δ = %.6f\n", cf);
X = T_max / (2*Pi);  \\ N=1, k=12 — for level 1, X = T/(2π)
Y = log(X);
\\ Note: weight-12 case has different X normalization; use X = (k/2)·T/(2π) for asymptotic
X_alt = 12 * T_max / (4*Pi);
Y_alt = log(X_alt);

printf("# Standard X = T/2π = %.4f, log = %.4f\n", X, Y);
printf("# Weight-corrected X' = kT/4π = %.4f, log = %.4f\n", X_alt, Y_alt);
printf("# U = %.6f\n", U);
printf("# (2/(3π))·c_f·T·log^4(X')   = %.6f\n", 2/(3*Pi)*cf*T_max*Y_alt^4);
printf("# Ratio U/predicted = %.4f\n", U / (2/(3*Pi)*cf*T_max*Y_alt^4));

quit;
