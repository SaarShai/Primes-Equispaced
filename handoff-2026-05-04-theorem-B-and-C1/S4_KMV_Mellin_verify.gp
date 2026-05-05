\\ S4_KMV_Mellin_verify.gp
\\
\\ Goal: verify the leading constant in the KMV second-moment formula
\\ for |Lambda'(f, 1/2)|^2 averaged harmonically over S_2*(q),
\\ then translate to (1/|F_q|) sum |L'(1/2,f)|^2 on the odd subfamily,
\\ and compare to the predicted (log q)^4 leading * 2/(3*Pi).
\\
\\ KMV "Non-vanishing of high derivatives of automorphic L-functions
\\ at the center of the critical strip" (Crelle 526, 2000).
\\
\\ Diagonal main term of harmonic 2nd moment of Lambda'(f,1/2) is
\\   Q_h^{diag} = 2 * qhat * sum_{n>=1} (1/n) * (log(qhat/n))^2 * W(n^2/qhat^2)
\\ where W(y) = (1/(2*Pi*I)) * int_(c) Gamma(1+t)^2 * y^{-t} * dt/t.
\\
\\ Leading order (in log qhat) is (log qhat)^3 with explicit constant
\\ that we will compute below.

default(realprecision, 40);

\\ Step 1: define W(y) by direct numerical integration of its Mellin form
\\ along the line Re(t) = 3.
\\
\\ Equivalently, by closing the contour to the left, W(y) = sum of residues
\\ at t=0 (a simple pole from 1/t) + residues at t = -1, -2, ... from
\\ Gamma(1+t)^2 (double poles at negative integers).
\\
\\ Residue at t = 0:  Gamma(1)^2 = 1.
\\ Residue at t = -m (m >= 1):  double pole, contributes a polynomial in log(y).
\\
\\ For our purposes we only need W(y) for small y, where W(y) ~ 1 + ...
\\
\\ But the actual computation we want is the LEADING CONSTANT
\\ of the (log qhat)^3 piece of Q_h^{diag}.

\\ The cleanest approach: write the diagonal sum as a Mellin integral over t.
\\
\\ sum_{n>=1} n^{-1} (log(qhat/n))^2 (n^2/qhat^2)^{-t}
\\   = qhat^{2t} * sum_n (log(qhat/n))^2 * n^{-1-2t}
\\
\\ Let s = 1 + 2t. Then sum_n (log(qhat/n))^2 / n^s = (d^2/du^2)|_{u=0} qhat^u zeta(s - u)
\\ which gives:
\\   = (log qhat)^2 zeta(s) - 2 (log qhat) zeta'(s) + zeta''(s)
\\
\\ So
\\   Q_h^{diag} = 2 qhat * (1/(2*Pi*I)) int_(c) Gamma(1+t)^2 qhat^{2t}
\\                     * [(log qhat)^2 zeta(1+2t) - 2 log qhat zeta'(1+2t)
\\                        + zeta''(1+2t)] dt/t.

\\ Shift contour to the left, picking up residue at t=0 (where zeta(1+2t) has a simple pole).
\\ Near t = 0:
\\   zeta(1+2t)   = 1/(2t) + gamma + ...
\\   zeta'(1+2t)  = -1/(4t^2) + 2 zeta_1 + ... where zeta_1 is a Stieltjes constant
\\   zeta''(1+2t) = 1/(4t^3)... double check signs.

\\ Use Laurent: zeta(1+x) = 1/x + gamma + sum_{n>=1} (-1)^n gamma_n x^n / n!
\\   gamma_0 = gamma (Euler-Mascheroni)
\\   gamma_1, gamma_2, ... = Stieltjes constants
\\
\\ Setting x = 2t:
\\   zeta(1+2t)   = 1/(2t) + gamma - gamma_1 (2t) + gamma_2 (2t)^2/2 - ...
\\   d/dt: zeta'(1+2t)*2 = -1/(2t^2) + 0 - 2 gamma_1 + 4 gamma_2 t - ...
\\     so zeta'(1+2t) = -1/(4t^2) - gamma_1 + 2 gamma_2 t - ...
\\   d^2/dt^2: zeta''(1+2t)*4 = 1/t^3 + 4 gamma_2 - 24 gamma_3 t/3 + ...
\\     so zeta''(1+2t) = 1/(4 t^3) + gamma_2 - 2 gamma_3 t + ...

\\ In the integrand:
\\   F(t) = (1/t) Gamma(1+t)^2 qhat^{2t} *
\\          [(log qhat)^2 zeta(1+2t) - 2 log qhat * zeta'(1+2t) + zeta''(1+2t)]
\\
\\ The bracket near t=0:
\\   (log qhat)^2 [1/(2t) + gamma + ...]
\\   - 2 log qhat [-1/(4t^2) - gamma_1 + ...]
\\   + [1/(4t^3) + gamma_2 + ...]
\\
\\   = 1/(4 t^3)
\\     + (1/(2t)) (log qhat)^2 + (1/(2 t^2)) log qhat
\\     + gamma (log qhat)^2 + 2 gamma_1 log qhat + gamma_2 + O(t).

\\ With prefactor 1/t and Gamma(1+t)^2 qhat^{2t} = 1 + 2 t (log qhat - gamma_E) + ..., we get
\\ a quartic pole at t = 0:
\\   F(t) = (1/t) [1 + 2 t (log qhat) + 2 t^2 ((log qhat)^2 - 2 gamma_E log qhat + ...) + ...]
\\          * [1/(4t^3) + (1/(2 t^2)) log qhat + (1/(2t)) (log qhat)^2 + gamma (log qhat)^2 + ...]
\\
\\ Residue at t=0 = coefficient of t^{-1} in F(t) before integration.

\\ Let L = log qhat for brevity.
\\ Gamma(1+t)^2 = exp(2 log Gamma(1+t)) = 1 - 2 gamma_E t + (gamma_E^2 + Pi^2/6) t^2 + ...
\\ qhat^{2t} = exp(2 t L) = 1 + 2 L t + 2 L^2 t^2 + (4 L^3/3) t^3 + ...
\\ Product: 1 + (2L - 2 gamma_E) t + ((2L - 2 gamma_E)^2/2 + (gamma_E^2 + Pi^2/6) - 2 gamma_E (2L) ) t^2 ...

\\ Bracket B(t) := (1/4) t^{-3} + (L/2) t^{-2} + (L^2/2) t^{-1} + (gamma_0 L^2 + 2 gamma_1 L + gamma_2) + O(t)

\\ F(t) = (1/t) * Gamma(1+t)^2 * qhat^{2t} * B(t)
\\      = (1/t) * [1 + a1 t + a2 t^2 + a3 t^3 + ...] * B(t)
\\ where a1 = 2(L - gamma_E),
\\       a2 = 2(L - gamma_E)^2 + (Pi^2/6 - gamma_E^2),  (verify below)
\\       a3 = computed similarly.

\\ Multiply (1/t) * (1 + a1 t + a2 t^2 + a3 t^3) * ((1/4) t^{-3} + (L/2) t^{-2} + (L^2/2) t^{-1} + C_L)
\\ where C_L = gamma * L^2 + 2 gamma_1 L + gamma_2.

\\ Expand and collect t^{-1} coefficient (which is the residue):
\\
\\   (1/t) * (1/4) t^{-3} -> t^{-4}: irrelevant for residue
\\   (1/t) * (L/2) t^{-2} -> t^{-3}: irrelevant
\\   (1/t) * (L^2/2) t^{-1} -> t^{-2}: irrelevant
\\   (1/t) * C_L -> t^{-1}: contributes C_L
\\
\\   (a1) * (1/4) t^{-3} -> t^{-3}: irrelevant
\\   (a1 t / t) * (L/2) t^{-2} = a1 (L/2) t^{-2} -> irrelevant
\\   (a1 / t) wait, careful: (1/t)*(a1 * t) = a1, multiply by (L^2/2) t^{-1} -> a1 (L^2/2) t^{-1}. CONTRIBUTES.
\\   (1/t)*(a1 t)*C_L -> a1 C_L which is t^0, irrelevant.
\\
\\   (a2 t^2 / t)*(1/4 t^{-3}) = (a2/4) t^{-2}. Irrelevant.
\\   (a2 t^2 / t)*(L/2 t^{-2}) = (a2 L/2) t^{-1}. CONTRIBUTES.
\\
\\   (a3 t^3/t)*(1/4 t^{-3}) = (a3/4) t^{-1}. CONTRIBUTES.
\\
\\ Therefore residue = C_L + a1 (L^2/2) + (a2 L/2) + (a3/4).
\\
\\ Q_h^{diag, leading} = 2 qhat * Residue.
\\
\\ Plug in:
\\ a1 = 2(L - gamma_E)
\\ a3 = 1/3 (a1)^3? No, more careful series.

\\ Compute via formal Taylor series in PARI:

t = 'x;
Lvar = 'L;  \\ formal log qhat
N = 6;

\\ Gamma(1+t)^2 series at t=0:
G2 = exp(2*lngamma(1+t) + O(t^N));

\\ qhat^{2t} = exp(2 L t)
qhat2t = exp(2*Lvar*t + O(t^N));

\\ Need Stieltjes constants gamma_0, gamma_1, gamma_2:
\\ zeta(1+x) = 1/x + sum_{n=0}^\infty (-1)^n gamma_n x^n / n!
\\ Use PARI: zeta(s) Taylor at s=1: zeta(1+x) is a Laurent series
zser = zeta(1 + t + O(t^N));

\\ zeta(1+2t):
Z2t = subst(zser, t, 2*t) + O(t^N);
\\ derivative zeta'(1+2t) = (1/2) d/dt zeta(1+2t):
Z2tp = deriv(Z2t, t) / 2;
\\ zeta''(1+2t) = (1/4) d^2/dt^2 zeta(1+2t):
Z2tpp = deriv(Z2tp, t) / 2;

\\ Bracket:
B = Lvar^2 * Z2t - 2*Lvar*Z2tp + Z2tpp;

\\ Integrand minus the 1/t prefactor:
H = G2 * qhat2t * B;

\\ F(t) = H/t. The residue at t=0 is coefficient of t^0 in H.
res = polcoeff(H, 0, t);

print("Residue (= coeff of t^0 in Gamma(1+t)^2 * qhat^{2t} * B):");
print(res);

print("");
print("Q_h^{diag, leading} = 2*qhat * Residue. Coefficients in L = log qhat:");
print(2 * res);

\\ Extract leading L^3 coefficient:
print("");
print("Leading (log qhat)^3 coefficient of Q_h^{diag} / qhat:");
leadL3 = polcoeff(2*res, 3, Lvar);
print(leadL3);

print("");
print("Leading (log qhat)^2 coefficient:");
print(polcoeff(2*res, 2, Lvar));
print("Leading (log qhat)^1 coefficient:");
print(polcoeff(2*res, 1, Lvar));
print("Leading (log qhat)^0 coefficient:");
print(polcoeff(2*res, 0, Lvar));

\\ Now translate to (1/|F_q|) sum |L'(1/2,f)|^2 on the odd subfamily.
\\ Lambda'(1/2, f) = qhat^{1/2} * L'(1/2, f) for f odd.
\\ For f even, Lambda'(1/2,f) = qhat^{1/2} * (log(qhat) * L(1/2,f) + L'(1/2,f) + Gamma'(1)*L(1/2,f))
\\                            = qhat^{1/2} * (log(qhat) * L(1/2,f) - gamma_E * L(1/2,f) + L'(1/2,f))
\\
\\ |Lambda'(1/2, f)|^2 / qhat:
\\   odd:  |L'(1/2, f)|^2
\\   even: |log qhat * L(1/2,f) - gamma_E*L(1/2,f) + L'(1/2,f)|^2
\\         ~ (log qhat)^2 |L(1/2,f)|^2 + cross terms + |L'(1/2,f)|^2
\\
\\ Sum^h |Lambda'(1/2,f)|^2 = qhat * [Sum^h_{odd} |L'|^2 + Sum^h_{even} (above)]
\\
\\ The harmonic average is over ALL f in S_2*(q). The "diagonal" main term we computed
\\ comes from BOTH even and odd subfamilies via the explicit-formula expansion.
\\
\\ KMV eq. (5): Q_h ~ c'_k (log qhat)^{2k+1} for k=1 means c'_1 (log qhat)^3.
\\ Our computation gives c'_1 = leadL3 above (numerical value).

\\ For comparison, the predicted constant for the odd-subfamily natural-average
\\ second moment of L'(1/2,f) is (4-th moment of zeta on critical line analog):
\\ Hughes-Young / CFKRS predict constant 2/(3*Pi) * (log q)^4
\\ ON THE ODD SUBFAMILY for (1/|F_q^-|) sum |L'(1/2,f)|^2,
\\ provided the leading power is (log q)^4.

\\ KMV eq. (5) shows the leading power for unmollified Q_h (over ALL f) is (log qhat)^3.
\\ This is one power LOWER than the predicted (log q)^4 in the note.

print("");
print("=== Translation to L'(1/2,f) on odd subfamily ===");
print("");
print("Note: KMV eq. (5) gives unmollified harmonic 2nd moment of");
print("Lambda^(k)(f,1/2) over ALL of S_2*(q) as ~ c'_k (log qhat)^{2k+1}.");
print("For k=1: power is (log qhat)^3.");
print("");
print("On odd subfamily, |Lambda'(1/2,f)|^2 = qhat * |L'(1/2,f)|^2.");
print("On even subfamily, |Lambda'(1/2,f)|^2 = qhat * |log(qhat)*L(1/2,f) + ...|^2,");
print("which is (log qhat)^2 * |L(1/2,f)|^2 to leading order, contributing");
print("(log qhat)^2 * (log qhat)  = (log qhat)^3 from the L^2 average ~ log qhat.");
print("");
print("Hence the (log qhat)^3 leading total in eq. (5) comes from BOTH subfamilies.");
print("");
print("On odd subfamily ALONE, sum^h |L'(1/2,f)|^2 has leading order");
print("at most (log qhat)^3, NOT (log qhat)^4 as the S4 chain claims.");
print("");
print("Numerical leading L^3 coefficient:");
print(leadL3);
print("");
print("Predicted target (per the note): 4/(3*Pi) ~");
print(4/(3*Pi));
print("Or 2/(3*Pi) ~");
print(2/(3*Pi));

\\ Sanity check: ratio
print("");
print("Ratio leadL3 / (4/(3*Pi)):");
print(leadL3 / (4/(3*Pi)));
print("Ratio leadL3 / (2/(3*Pi)):");
print(leadL3 / (2/(3*Pi)));

quit;
