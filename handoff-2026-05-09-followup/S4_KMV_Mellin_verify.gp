\\ S4_KMV_Mellin_verify.gp
\\
\\ KMV §5 Mellin residue verification — companion PARI/GP source.
\\ NOTE: PARI/GP was not available on the agent's machine.  This file is
\\ written in PARI/GP for compatibility with the prior bundle, and an
\\ equivalent computation is provided in the companion Python+sympy+mpmath
\\ script S4_KMV_Mellin_verify.py (which IS what was actually executed —
\\ see S4_KMV_Mellin_verify.out and the deliverable markdown).
\\
\\ The Python script reproduces the prior PARI bundle's level-aspect
\\ result (handoff-2026-05-04-theorem-B-and-C1/S4_KMV_Mellin_verify.{gp,out})
\\ to >40 digits, namely:  leading L^3 coefficient = 14/3 (exact rational).
\\
\\ The structure of the Mellin residue is identical in level- and weight-
\\ aspect (analytic conductor X = sqrt(N k T)/(2 Pi) replaces qhat = sqrt(q)/(2 Pi));
\\ the diagonal main term polynomial in L = log X is therefore the same
\\ rational polynomial.

default(realprecision, 40);

\\ Stieltjes constants gamma_n via Laurent expansion of zeta:
\\   zeta(1+x) = 1/x + sum_{n>=0} (-1)^n gamma_n x^n / n!
\\
\\ Symbolic computation of the Mellin residue at t=0:
\\   F(t) = (1/t) * Gamma(1+t)^2 * X^{2t} *
\\          [(log X)^2 zeta(1+2t) - 2 (log X) zeta'(1+2t) + zeta''(1+2t)]
\\ Residue at t=0 = coeff of t^0 in (Gamma(1+t)^2 * X^{2t} * B(t)).

t = 'x;
Lvar = 'L;
N = 6;

\\ Gamma(1+t)^2 series at t=0
G2 = exp(2*lngamma(1+t) + O(t^N));

\\ X^{2t} series
qhat2t = exp(2*Lvar*t + O(t^N));

\\ zeta(1+2t):
zser = zeta(1 + t + O(t^N));
Z2t  = subst(zser, t, 2*t) + O(t^N);
Z2tp  = deriv(Z2t, t) / 2;
Z2tpp = deriv(Z2tp, t) / 2;

B = Lvar^2 * Z2t - 2*Lvar*Z2tp + Z2tpp;
H = G2 * qhat2t * B;
res = polcoeff(H, 0, t);

print("Residue (= coeff of t^0):");
print(res);

print("");
print("Q_h^{diag, leading} = 2 * Residue (poly in L = log X):");
print(2*res);

\\ Extract leading L^3 coefficient
leadL3 = polcoeff(2*res, 3, Lvar);
print("");
print("Leading L^3 coefficient:");
print(leadL3);
print("Expected: 14/3 =", 14/3);

\\ Compare to claimed targets
print("");
print("Predicted target c1 = 4/(3*Pi):");
print(4/(3*Pi));
print("Predicted target c1 = 2/(3*Pi):");
print(2/(3*Pi));

print("");
print("Ratio leadL3 / (4/(3*Pi)) =", leadL3 / (4/(3*Pi)));
print("Ratio leadL3 / (2/(3*Pi)) =", leadL3 / (2/(3*Pi)));

\\ Note: 14/3 / (4/(3 Pi)) = 14 Pi / 4 = 7 Pi / 2 ~ 10.9956
\\ Power mismatch: this is L^3, target was L^4.

quit;
