\\ Sanity check: independently derive the residue using a cleaner approach.
\\ Use the integral representation
\\   Q_h^{diag}/q̂ = 2 * (1/(2*Pi*I)) ∫ Gamma(1+t)^2 * q̂^{2t} *
\\                  [L^2 ζ(1+2t) - 2 L ζ'(1+2t) + ζ''(1+2t)] / t dt
\\ where L = log(qhat).
\\
\\ As an alternative check: the integrand is the second derivative
\\ d^2/du^2 [Gamma(1+t)^2 q̂^{2t} ζ(1+2t-u) q̂^u] / t at u=0.
\\
\\ This equals d^2/du^2 [Gamma(1+t)^2 ζ(1+2t-u) (q̂^2)^t * q̂^u] / t
\\
\\ At u=0, evaluating residue at t=0:
\\ Set s = 1 + 2t, then t = (s-1)/2, dt = ds/2.
\\
\\ Integrand becomes Gamma((s+1)/2)^2 q̂^{s-1} ζ(s-u) q̂^u dt/t = Gamma((s+1)/2)^2
\\  ... wait Gamma(1+t) = Gamma(1 + (s-1)/2) = Gamma((s+1)/2).
\\
\\ Actually a much simpler check: the leading log-cubic coefficient of
\\ the harmonic 2nd moment of zeta'(1/2 + i*T) over T smoothed should be related.
\\
\\ For us, just verify 14/3 is the correct closed form.

default(realprecision, 50);

\\ Direct: compute residue at t=0 of
\\   F(t) = Gamma(1+t)^2 * exp(2*L*t) * [L^2 ζ(1+2t) - 2 L ζ'(1+2t) + ζ''(1+2t)] / t
\\
\\ Use polynomial L symbolically again, but with 50 digits.

t = 'x; Lvar = 'L; N = 8;
G2 = exp(2*lngamma(1+t) + O(t^N));
qhat2t = exp(2*Lvar*t + O(t^N));
zser = zeta(1 + 2*t + O(t^N));
zserp = deriv(zser, t)/2;
zserpp = deriv(zserp, t)/2;
B = Lvar^2 * zser - 2*Lvar*zserp + zserpp;
H = G2 * qhat2t * B;
res = polcoeff(H, 0, t);
print("L^3 coefficient: ", polcoeff(res, 3, Lvar));
print("Should equal 7/3 (since Q_h diag = 2*qhat * res, leading L^3 of Q_h/qhat = 2 * 7/3 = 14/3):");
print(7/3);
print("");
print("Coeff of L^3 in res (before *2):");
print(polcoeff(res, 3, Lvar));
print("Confirmed = 7/3? ", polcoeff(res, 3, Lvar) == 7/3);

\\ Independent derivation via Cauchy: Cubic pole at t=0.
\\ Near t=0:
\\   1/t * (1 + 2(L-gamma_E)*t + ...) * [zeta''(1+2t) leading 1/(4t^3) + ...]
\\
\\ The pure cubic-pole piece of B at t=0:
\\ zeta''(1+2t) ~ 1/(4 t^3) + lower
\\ This combines with 1/t prefactor and Gamma(1+t)^2 q̂^{2t} ~ 1 at t=0:
\\ Coefficient of t^0 (residue) from 1/t * 1/(4 t^3) requires cubing in q̂^{2t}.
\\
\\ q̂^{2t} = 1 + 2L t + 2 L^2 t^2 + (4 L^3/3) t^3 + ...
\\ So contribution: (1/t) * 1 * (4 L^3/3) t^3 * (1/(4 t^3))? No: total
\\
\\ Multiply (1/t) * Gamma(1+t)^2 * q̂^{2t} * (1/(4 t^3)) and look for t^{-1} residue
\\   = (1/(4 t^4)) * Gamma(1+t)^2 * q̂^{2t}
\\   = (1/(4 t^4)) * (1 + a1 t + a2 t^2 + a3 t^3 + a4 t^4 + ...)
\\   residue (coeff of t^{-1} in this expression after dividing by 4t^4? No, this is part of F = 1/t * G2 * q̂^{2t} * B
\\ Be careful: F(t) = (1/t)*(stuff). Residue at t=0 is coefficient of t^0 in (stuff).
\\
\\ stuff = G2 * q̂^{2t} * B
\\
\\ B has piece 1/(4 t^3) from zeta''. So we need coeff of t^3 in G2 * q̂^{2t}, divided by 4.
\\ coefficient of t^3 in (1 + a1 t + a2 t^2 + a3 t^3 + ...) = a3.
\\ a3 from G2 * q̂^{2t}:
gprod = G2 * qhat2t;
print("");
print("Coeff of t^3 in Gamma(1+t)^2 q̂^{2t}: ");
print(polcoeff(gprod, 3, t));
print("(expected (4/3) L^3 + lower = 4 L^3/3 + ...)");

\\ contribution to L^3 from B = ζ''(1+2t)'s 1/(4t^3) piece:
\\   (1/4) * coeff of t^3 in G2 * q̂^{2t}, restrict to L^3 part:
c_zetapp_L3 = polcoeff(polcoeff(gprod, 3, t), 3, Lvar) / 4;
print("Contribution to L^3 residue from 1/(4t^3) piece of zeta''(1+2t): ", c_zetapp_L3);
print("Expected (4/3)/4 = 1/3");

\\ Other ζ pieces:
\\ -2L * zeta'(1+2t):
\\ Near t=0: zeta'(1+2t) = -1/(4t^2) + Stieltjes... so -2L * (-1/(4t^2)) = L/(2 t^2).
\\ Contribution to res: coeff of t^2 in G2*q̂^{2t} * (L/2):
c_zetap = (Lvar/2) * polcoeff(gprod, 2, t);
\\ Take L^3 part:
c_zetap_L3 = polcoeff(c_zetap, 3, Lvar);
print("Contribution to L^3 residue from -1/(4t^2) piece of -2L*zeta'(1+2t): ", c_zetap_L3);

\\ L^2 * zeta(1+2t) ~ L^2 * (1/(2t) + ...) -> contribution L^2/(2t).
\\ Coeff of t^1 in G2*q̂^{2t} * L^2/2:
c_zeta = (Lvar^2/2) * polcoeff(gprod, 1, t);
c_zeta_L3 = polcoeff(c_zeta, 3, Lvar);
print("Contribution to L^3 residue from 1/(2t) piece of L^2*zeta(1+2t): ", c_zeta_L3);

\\ Sum:
total = c_zetapp_L3 + c_zetap_L3 + c_zeta_L3;
print("");
print("Total L^3 contribution to residue: ", total);
print("= 1/3 + 1/2 (from 2*L^2*L/2) + ... ");
print("Expected = 7/3 (per residue earlier)");

quit;
