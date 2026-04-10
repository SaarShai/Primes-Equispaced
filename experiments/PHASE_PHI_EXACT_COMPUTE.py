from mpmath import mp, zeta
import cmath

mp.dps = 50

# rho1 = non-trivial zero of zeta function
rho1 = mp.mpc(0.5, 14.134725141734693)

# Compute zeta'(rho1) using numerical derivative (since zetaderiv is not available in mpmath)
h = mp.mpf('1e-10')
zp = (zeta(rho1 + h) - zeta(rho1 - h)) / (2 * h)

# Compute c1 = 1/(rho1 * zeta'(rho1))
c1 = 1 / (rho1 * zp)

# Compute predicted phi = -arg(rho1 * zeta'(rho1))
phi_predicted = -float(mp.arg(rho1 * zp))

# Compute |c1|
c1_magnitude = abs(c1)

print(f"rho1 = {rho1}")
print(f"zeta'(rho1) = {zp}")
print(f"c1 = 1/(rho1 * zeta'(rho1)) = {c1}")
print(f"|c1| = {c1_magnitude}")
print(f"Predicted phi = {phi_predicted}")
print(f"Observed phi ~ 5.28")
print(f"Difference: {abs(phi_predicted - 5.28)}")
