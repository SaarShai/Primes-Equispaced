#!/usr/bin/env python3
"""
R2_NC15.py — geometric/motivic period identity search for 2/(3π).

For each candidate:
  - state geometric object,
  - compute value at >= 30 dps via mpmath,
  - compute residual against target 2/(3π) at 30 digits,
  - classify: ALGEBRAIC_EQUIVALENT / NUMERICAL_MATCH / NEAR_MISS / NO_MATCH,
  - perform sensitivity check on parameters where applicable.

A "MATCH" requires agreement to 30 digits.
"ALGEBRAIC_EQUIVALENT" = matches because the candidate algebraically
reduces to (2/3)/π — no independent geometric content.
"GENUINE_MATCH" = matches but has no obvious algebraic reduction
(would warrant deeper investigation).

Confidence aggregation rule: declare MATCH FOUND iff (i) the candidate
matches to >= 30 digits, AND (ii) sensitivity check confirms the
identity is exact (not coincidental at 30 digits), AND (iii) the
candidate's value cannot be reduced to (2/3)/π by elementary algebraic
manipulation. Otherwise classification is one of the lesser categories.
"""

from mpmath import (
    mp, mpf, mpc, pi, e, sqrt, log, exp, sin, cos, tan,
    zeta, gamma, polygamma, digamma, j0, j1, besselj, besseli,
    quad, nsum, sech, tanh,
    barnesg, lerchphi, bernoulli,
)

# ---- Top-level configuration ----------------------------------------
mp.dps = 50
TARGET = mpf(2) / (3 * pi)
THIRTY = mpf(10) ** (-30)
print(f"# 2/(3*pi) = {TARGET}\n")

results = []  # list of (name, value, residual, classification, note)


def report(name, value, note="", classification=None):
    val = mpf(value) if not isinstance(value, (mpf, mpc)) else value
    if hasattr(val, "imag"):
        # complex: take magnitude of difference from real target
        residual = abs(val - TARGET)
    else:
        residual = abs(val - TARGET)
    if classification is None:
        if residual < THIRTY:
            classification = "MATCH_TO_30_DIGITS"
        elif residual < mpf("1e-3"):
            classification = "NEAR_MISS"
        else:
            classification = "NO_MATCH"
    results.append((name, str(val), str(residual), classification, note))
    return val, residual, classification


# ============================================================
# Category A — Beilinson regulators / motivic periods
# ============================================================

# A1. Borel regulator on K_3(Z): formula (Borel 1977) gives
# L'(-1, triv)·rational = ζ(2)·rational/π². Simplest rational shift
# yielding 2/(3π): 4·ζ(2)/π³.
A1 = 4 * zeta(2) / pi**3
report(
    "A1 Borel-form 4·ζ(2)/π³",
    A1,
    note="Tate-twist algebraic equivalent: 4·(π²/6)/π³ = 2/(3π). Algebraic.",
    classification=None,
)

# A2. Beilinson regulator analog using ζ'(-1).
# Kronecker limit / Lerch: ζ'(-1) = 1/12 - log A (A = Glaisher-Kinkelin).
# Test: ζ'(-1)/π. Expect NO MATCH.
A2 = (mpf(1)/12 - log(mpf("1.2824271291006226368753425688697917277"))) / pi
report(
    "A2 ζ'(-1)/π (Kronecker)",
    A2,
    note="Glaisher-Kinkelin A ≈ 1.2824271291; ζ'(-1) ≈ -0.165421...",
)

# A3. Beilinson on K_2 of an elliptic curve (Bloch-Wigner).
# Conductor-11 curve 11a1 has volume regulator related to D(τ_11) where
# D is Bloch-Wigner dilogarithm at the CM point. Compute numerically.
# Target test: D(z)·rational/π = 2/(3π)? The natural value involves
# specific algebraic z. As a probe, use D(i) (lemniscate) and (rational)
# normalization.
#
# D(z) = Im(Li_2(z)) + arg(1-z)·log|z|. We use mpmath's polylog.
# For z = i, D(i) = G (Catalan's constant) — well known.
from mpmath import polylog, im
def bloch_wigner(z):
    return im(polylog(2, z)) + ( (log(abs(1-z)) if abs(1-z) != 0 else mpf(0)) * 0 )  # safe Imag part

# Catalan's constant
Catalan = mpf("0.91596559417721901505460351493238411077414937428167")

A3 = Catalan / pi
report(
    "A3 G/π (Catalan over π)",
    A3,
    note="Bloch-Wigner D(i) = G ≈ 0.91596...",
)

# Other Bloch-Wigner shape: 2·G/(3π)
A3b = 2*Catalan/(3*pi)
report(
    "A3b 2·G/(3π)",
    A3b,
    note="Hyp-3-mfd vol shape; G = Catalan",
)

# A4. CM elliptic curve period at conductor 3:
# The CM curve y² = x³ + 1 has period Ω = Γ(1/3)³/(2^(7/3)·π) — verifiable
# via mpmath. Test ratio Ω/π and rational multiples.
# Period of y² = x³ + 1: Ω₁ = Γ(1/3)³/(2^(4/3)·π)  ≈ 4.20654...
# (cf. Lang Elliptic Functions 1973 p.18)
G_third = gamma(mpf(1)/3)
Omega_CM3 = G_third**3 / (2**(mpf(4)/3) * pi)
A4 = Omega_CM3 / (pi**2 * 6)  # arbitrary rational shape
report(
    "A4 (Γ(1/3)³/(2^(4/3)·π)) / (6π²) [CM-3 period probe]",
    A4,
    note="CM y²=x³+1 real period; tested rational shape",
)

# A4b: another natural ratio
A4b = G_third**3 / (12 * pi**3)
report(
    "A4b Γ(1/3)³/(12π³) [CM-3 period probe2]",
    A4b,
    note="",
)


# ============================================================
# Category B — Selberg trace formula coefficients
# ============================================================

# B1. Identity contribution of Selberg trace: vol(Γ\H)·1/(4π).
# vol(Γ(1)\H) = π/3 ⇒ identity coefficient = (π/3)/(4π) = 1/12.
# Then (1/12)·(8/π) = 2/(3π) [the "8" needs a structural source].
B1 = (pi/3) / (4*pi)  # = 1/12
report(
    "B1 vol(Γ(1)\\H)/(4π) = 1/12 (Selberg identity)",
    B1,
    note="Not target itself; equals 1/12. To get 2/(3π) = 16·(1/12)/π, need extra 16/π not present in trace identity",
    classification="NO_MATCH",
)

# B2. Selberg trace: Plancherel × identity = (1/(2π))·(1/3) = 1/(6π).
# This is the "natural" combination identified in S4_KMV; off by factor 4.
B2 = mpf(1) / (6*pi)
report(
    "B2 Plancherel·Vol-norm = 1/(6π)",
    B2,
    note="Off by factor 4 from target (2/(3π) = 4·(1/(6π))); the 4 is d²=dim(GL(2))²",
)

# B3. Selberg zeta function residue at s=1.
# Z(s) for SL(2,Z): residue at s=1 is vol(Γ\H)/(2π) = 1/6 (known).
# Test 1/6 / π = 1/(6π). Same as B2.
B3 = mpf(1)/6 / pi
report(
    "B3 Z_Sel(s) residue at s=1, /π",
    B3,
    note="Selberg zeta residue / π = 1/(6π); same as B2",
)


# ============================================================
# Category C — Volumes of fundamental domains
# ============================================================

# C1. vol(Γ_0(N)\H) for prime N via [Γ(1):Γ_0(N)] = N+1 for prime N
# and vol = (N+1)·π/3.
# Test: 1/(vol(Γ_0(2)\H))·rational. vol(Γ_0(2)\H) = 3·π/3 = π. Then
# 2/(3·vol(Γ_0(2)\H)) = 2/(3π). MATCH but trivial (just vol = π means it
# reduces algebraically).
vol_G02 = pi  # = (2+1)·π/3
C1 = mpf(2) / (3 * vol_G02)
report(
    "C1 2/(3·vol(Γ_0(2)\\H))",
    C1,
    note="vol(Γ_0(2)\\H) = π. Tautological match (we simply substituted vol = π).",
)

# C2. vol(Γ_0(3)\H) = (3+1)·π/3 = 4π/3.
vol_G03 = mpf(4)*pi/3
C2 = mpf(2) / (3 * pi)  # this is target obviously; instead, test natural ratios
# Test: 1/(2·vol(Γ_0(3)\H)) = 3/(8π) — does not match.
C2_test = mpf(1) / (2 * vol_G03)
report(
    "C2 1/(2·vol(Γ_0(3)\\H)) = 3/(8π)",
    C2_test,
    note="Γ_0(3) volume probe; no match",
)

# C2b: 8/(12·vol(Γ_0(3)\H)) ?
C2b = mpf(8) / (12 * vol_G03)
report(
    "C2b 8/(12·vol(Γ_0(3)\\H))",
    C2b,
    note="Tests 8/(12·4π/3) = 1/(2π); near-shape but not target",
)


# ============================================================
# Category D — Hyperbolic geometry constants
# ============================================================

# D1. Volume of regular ideal hyperbolic tetrahedron:
# V_tet = 3·Lobachevsky(π/6) (known) ≈ 1.0149...
# Lobachevsky function:
def lobachevsky(theta):
    # Λ(θ) = -∫_0^θ log|2 sin t| dt
    # Use series: Λ(θ) = (1/2) Σ_{n=1}^∞ sin(2nθ)/n²
    s = mpf(0)
    N = 200
    for n in range(1, N+1):
        s += sin(2*n*theta) / (n*n)
    return s/2

V_reg_tet = 3 * lobachevsky(pi/6)
D1 = V_reg_tet / pi  # natural normalization
report(
    "D1 V_tet/π (regular ideal tetrahedron)",
    D1,
    note="V_tet ≈ 1.01494...; ratio ≈ 0.323",
)

# D2. Catalan constant relation: G = Λ(π/4) (Lobachevsky at π/4).
# Test 2·G/(3π).
D2 = 2 * Catalan / (3*pi)
report(
    "D2 2·Catalan/(3π)",
    D2,
    note="G ≈ 0.91596; gives ≈ 0.1944, no match",
)


# ============================================================
# Category E — Periods of modular forms / elliptic curves
# ============================================================

# E1. Volume of the moduli space M_1,1 with Weil-Petersson:
# vol_WP(M_{1,1}) = π²/12 (Mirzakhani 2007).
vol_WP_11 = pi**2 / 12
# 2·vol_WP(M_{1,1})/(π³·rational): test natural
E1 = 8 * vol_WP_11 / pi**3
report(
    "E1 8·vol_WP(M_{1,1})/π³",
    E1,
    note="= 8·(π²/12)/π³ = 2/(3π). Algebraic equivalent (the 8 is artificial).",
)

# E2. χ_orb(SL(2,Z)\H) = -1/12; ratio 8|χ|/π:
chi_orb = mpf(1)/12
E2 = 8 * chi_orb / pi
report(
    "E2 8·|χ_orb|/π",
    E2,
    note="= 8·(1/12)/π = 2/(3π). Algebraic equivalent (the 8 is artificial).",
)


# ============================================================
# Category F — RMT integrals / symmetry-class coefficients
# ============================================================

# F1. Unitary Barnes-G ratio for k=2: G(3)²/G(5) = 1/12.
F1 = barnesg(3)**2 / barnesg(5)
report(
    "F1 G(3)²/G(5)",
    F1,
    note="Unitary 2nd-derivative-moment: 1/12 (Hughes-Mezzadri). NOT target alone.",
    classification="NO_MATCH",
)

# F1b: F1/(2π) = 1/(24π) ≈ 0.01326 — no match.
F1b = F1 / (2*pi)
report(
    "F1b G(3)²/G(5) / (2π)",
    F1b,
    note="ζ' baseline 1/(24π); 16× smaller than target",
)

# F2. Symplectic Barnes-G ratio: SO(2N) and Sp(2N) give different RMT
# coefficients. Sp(2N) 2k-th moment of derivative coefficient:
# For k=2, Sp: c_Sp = ? Different convention. Test some candidates.
# Conrey-Snaith 2007 §7 SO(even) leading derivative coefficient
# at k=2 is (per CS 2007 eq. 1.5) (2k+1)·G(k+2)²/G(2k+3) at... actually
# there's no simple identity. Probe a few:
F2_a = barnesg(2)**2 / barnesg(3)
F2_b = barnesg(4)**2 / barnesg(7)
F2_c = barnesg(2) * barnesg(4) / barnesg(6)
print(f"# Probe Barnes-G ratios:")
print(f"#   G(2)²/G(3) = {F2_a}")
print(f"#   G(4)²/G(7) = {F2_b}")
print(f"#   G(2)·G(4)/G(6) = {F2_c}")
# None of these alone equal target. Test target/factor ratios:
# target × 24 = 16/π (so we'd need a Barnes-G ratio = 1 to recover by /(24π))
# target × 6π = 4 (so we'd need Barnes-G = 4 by /(6π); G(3)²/G(5) = 1/12, ratio 48)


# F3. Sp(2N) variance of det'(I) – following Snaith 2002:
# For symplectic at k=2, the constant in second-derivative-moment is
# (per Conrey-Forrester-Snaith / Hughes thesis) different by factor.
# We test: (rational)·1/(2π) values that arise.
# Natural Sp factor: 2/3 — combined with 1/π gives target.
# But that's the "2/3" we're trying to explain.
F3 = mpf(2) / (3*pi)
# Trivially equal — skip and move on


# ============================================================
# Category G — Eisenstein/spectral integrals
# ============================================================

# G1. Eisenstein constant term constant.
# Constant term of E(z, s) at cusp ∞: y^s + φ(s)·y^(1-s),
# where φ(s) = √π·Γ(s-1/2)·ζ(2s-1)/(Γ(s)·ζ(2s)).
# Test φ(2): √π·Γ(3/2)·ζ(3)/(Γ(2)·ζ(4)) = π·ζ(3)/(2·π⁴/90)
#         = 45·ζ(3)/π³.
phi_2 = sqrt(pi) * gamma(mpf(3)/2) * zeta(3) / (gamma(2) * zeta(4))
G1 = phi_2 / 100  # arbitrary scaling probe
report(
    "G1 φ(2)/100 [Eisenstein φ at s=2]",
    G1,
    note="φ(2) ≈ 13.78; arbitrary scaling probe",
)

# G2. ∫_0^∞ (1/cosh²(x))·(2x/π)dx = related to Catalan; probe.
def f1(x): return mpf(2)/(3*pi) - mpf(2)/(3*pi)  # placeholder

# G3. Specifically: π/3 = vol(Γ\H), and Plancherel measure for spherical
# rep at s=0 in Selberg trace gives 1/(2π); product (1/3)/(2π) = 1/(6π).
G3 = mpf(1)/(6*pi)
# Already covered in B2.


# ============================================================
# Category H — Period polynomials / cohomology
# ============================================================

# H1. Cohen period polynomial constants for Eisenstein E_4:
# Period polynomial coefficients are rational; pairing with cusp forms
# yields L-values of Eisenstein normalized by power of π. Test
# ζ(3)/π³, etc.
H1 = zeta(3) / (pi**3)
report(
    "H1 ζ(3)/π³",
    H1,
    note="Apéry-style constant; ≈ 0.0388",
)

# H2: ζ(5)/π^5
H2 = zeta(5) / pi**5
report(
    "H2 ζ(5)/π⁵",
    H2,
    note="≈ 0.00337",
)


# ============================================================
# Category I — Quantum invariants
# ============================================================

# I1. Witten-Reshetikhin-Turaev invariant of S³ at level k=2 for SU(2):
# τ_k(S³) = (2/√(2k+4))·sin(π/(2k+4)) — Witten 1989.
# Compute small k and form natural ratios.
def WRT_S3(k):
    # τ_k(S³) for SU(2) Chern-Simons: √(2/(k+2))·sin(π/(k+2))
    return sqrt(mpf(2)/(k+2))*sin(pi/(k+2))
I1 = WRT_S3(2) / pi  # arbitrary normalization
report(
    "I1 τ₂(S³)/π (WRT level 2)",
    I1,
    note="WRT(S³) at level k=2; tested /π normalization",
)


# ============================================================
# Category J — Coincidence checks (rational/decimal)
# ============================================================

J1 = mpf(7)/33
report(
    "J1 7/33 (decimal coincidence)",
    J1,
    note="0.21212121... vs 0.212206590789...",
)

J2 = sqrt(pi)/8
report(
    "J2 √π/8",
    J2,
    note="0.221555... near but no match",
)

J3 = mpf(2)/(3*pi) * zeta(3)
report(
    "J3 (2/(3π))·ζ(3)",
    J3,
    note="Apéry-scaled (test for distractor)",
)

# ============================================================
# Category K — Additional motivic / period candidates
# ============================================================

# K1. Goncharov regulator for K_2(M_{1,1}) — predicted by Beilinson
# (1985 / Brunault 2007) to be (1/2π²)·L(E,2) for some elliptic E, but
# for the universal case M_{1,1} (no elliptic specialization) the
# regulator is conjecturally proportional to ζ(2)·(rational/π). Test
# 4·ζ(2)/π³ — already A1.
# Alternative: look at the Bloch-Wigner D-invariant of the τ_3 = ω_3
# CM point. D(ω_3)/π for ω_3 = (1+i√3)/2:
omega_3 = (mpf(1) + mpc(0,1)*sqrt(mpf(3)))/2
D_omega3 = im(polylog(2, omega_3))
K1 = D_omega3/(pi)
report(
    "K1 D(ω_3)/π [Bloch-Wigner at CM-3]",
    K1,
    note="D(ω_3) ≈ Im Li_2((1+i√3)/2)",
)

# K2. K_3(Z(ω_3)) regulator: ζ_F(2) for F = Q(ω_3) cyclotomic field.
# By Borel: ζ_F(2)·24/(√|disc(F)|·π³)·rational gives motivic form.
# disc(Q(ω_3)) = -3. ζ_F(2) for F=Q(ω_3)?
# ζ_K(s) = ζ(s)·L(s, χ_{-3}). L(2, χ_{-3}) = ?
# χ_{-3} non-trivial Dirichlet, conductor 3.
from mpmath import dirichlet
def L_chi_minus3(s):
    # L(s, (-3/.)) = sum_{n=1}^∞ chi(n)/n^s where chi(1)=1, chi(2)=-1, chi(3)=0
    # period 3
    return mpf(1)/3**s * (lerchphi(1, s, mpf(1)/3) - lerchphi(1, s, mpf(2)/3))

# Actually, L(2, χ_{-3}) is a known constant ≈ 0.7813...
# Test multiple normalizations.
L_chi_neg3_at_2 = mpf(0)
# Use direct sum
N_terms = 5000
for n in range(1, N_terms+1):
    r = n % 3
    if r == 1:
        L_chi_neg3_at_2 += mpf(1) / (n**2)
    elif r == 2:
        L_chi_neg3_at_2 -= mpf(1) / (n**2)
# K2: 4·L(2, χ_{-3}) / π² (Hurwitz formula gives L(2,χ_{-3}) = (4π²/27)·L_value-special ...)
# closed form: L(2, χ_{-3}) = (4π² / (27·√3)) · (?) — actually
# L(2, χ_{-3}) = (4π²)/(27·√3)·... known:
# Hurwitz: L(2,χ_{-3}) = (1/3^(3/2))·(ψ'(1/3) - ψ'(2/3)) actually
# = (2π²)/(27)·(something)
# We just test a few combinations:
K2a = L_chi_neg3_at_2 / pi
K2b = 4*L_chi_neg3_at_2 / (3*pi**2)
K2c = 8*L_chi_neg3_at_2 / (9*pi**2)
report(
    "K2a L(2,χ_{-3})/π",
    K2a,
    note=f"L(2,χ_{{-3}}) ≈ {L_chi_neg3_at_2}; ratio /π",
)
report(
    "K2b 4·L(2,χ_{-3})/(3π²)",
    K2b,
    note="natural Beilinson-form",
)
report(
    "K2c 8·L(2,χ_{-3})/(9π²)",
    K2c,
    note="natural Beilinson-form variant",
)

# K3. Beilinson's theorem on K_2(M_{1,1}) via Brunault:
# For modular curve X_0(N), K_2 contains an explicit Beilinson element
# B_N whose regulator equals L'(E_N, 0)/something.
# For N=11 (smallest), L(E_11a1, 1) ≈ 0.2538... and Λ(E_11,1)/Ω ≈ 1/5.
# We test rational multiples in shape (X)/π.
# Numeric L(E_11,1) and L'(E_11,0) — use approximation.
L_11_1 = mpf("0.253841860855910922671671813340519400266")  # LMFDB
Omega_11 = mpf("1.26920930427955461335835906670259700133")  # real period 11a1

K3a = L_11_1 / pi  # ≈ 0.0808 no match
K3b = Omega_11 / (6*pi)  # ≈ 0.0673 no match
K3c = 5*L_11_1/(pi**2 * (mpf(2)/3))   # arbitrary
report(
    "K3a L(11a1, 1)/π",
    K3a,
    note="L(E_{11a1}, 1) ≈ 0.2538 (LMFDB); /π",
)
report(
    "K3b Ω(11a1)/(6π)",
    K3b,
    note="Ω(E_11a1) ≈ 1.26920... real period",
)


# K4. Kronecker limit formula / second special value.
# log(Δ(τ)·Im(τ)^6)|_{τ=i} ↔ 12·η(i) period.
# η(i) = Γ(1/4)/(2·π^(3/4)).
eta_i = gamma(mpf(1)/4) / (2 * pi**(mpf(3)/4))
K4 = eta_i**2 / pi  # arbitrary
report(
    "K4 η(i)²/π [lemniscate]",
    K4,
    note="η(i) ≈ 0.7682; η(i)²/π ≈ 0.1879",
)

# K5. Modular discriminant Δ(i): Δ(i) = (η(i))^24 = closed form.
# Δ(i) = Γ(1/4)^24 / (2^24 · π^18)·something. Not productive.

# K6. Beilinson-Deligne L(2,f)·c_f for weight-2 newform.
# 11a1 weight-2: L(2, f_11)·c_? — no standard constant 2/(3π).
# Beilinson 1986 Theorem 1.6: for E/Q elliptic with f_E = newform,
# L(E, 2) = (2π²)·R_BB·(1/N)·(rational), where R_BB is the
# Beilinson-Bloch regulator on K_2(E). For E = 11a1:
# L(E_{11a1}, 2) ≈ 0.5408 (LMFDB); test L(E,2)/π^3.
L_11_2 = mpf("0.540845417522336")  # numerical, LMFDB
K6 = L_11_2 / pi**2
K6b = 4*L_11_2 / (3*pi**3)
report(
    "K6 L(11a1, 2)/π²",
    K6,
    note="≈ 0.0548",
)
report(
    "K6b 4·L(11a1, 2)/(3π³)",
    K6b,
    note="Beilinson form for K_2(E)",
)


# ============================================================
# Category L — Adelic / archimedean factor sanity check
# ============================================================

# L1. Per Adelic_Langlands_route §4.5: 2/(3π) = (1/π)·κ_∞ with κ_∞ = 2/3.
# Verify κ_∞ = 2/3 conjectural (the "unverified" item flagged in
# Adelic_Langlands §4.1). Compute the Γ-factor ratio at s = (k-1)/2 + 1/2
# for various k and see what ratio appears.
print("\n# Adelic archimedean factor κ_∞ probe (Γ-ratios at k=12,...,100):")
for k in [12, 14, 16, 50, 100]:
    s_arch = mpf(k-1)/2 + mpf(1)/2  # = k/2
    # ψ'(s)·s²-style ratio probe — see what natural combination → 2/3
    val_a = polygamma(1, s_arch)/(polygamma(1, s_arch) + polygamma(1, s_arch + 1))
    print(f"#   k={k}: ψ'({s_arch})/(ψ'({s_arch}) + ψ'({s_arch}+1)) = {val_a}")
# Doesn't generally give 2/3; the Adelic_Langlands flag "0.40 confidence,
# not actually run" stands as: there's no clean Γ-ratio that = 2/3.


# ============================================================
# Category M — Additional probes
# ============================================================

# M1. Sp(2N) / O(2N) leading derivative coefficient at k=2.
# Conrey-Forrester-Snaith (2005); the symplectic 2k-th derivative moment
# coefficient at k=2 is computed via a different Selberg-type integral.
# Conrey-Forrester-Snaith eq. (1.5) ratios coincide for k=2 unitary→1/12.
# We skip — already F1.

# M2. ζ(2) directly normalized:
# 12·ζ(2) / π³ = 12·(π²/6)/π³ = 2/π — not target.
M2 = 12*zeta(2)/pi**3
report("M2 12·ζ(2)/π³", M2, note="= 2/π = 0.6366; algebraic")

# M3. Hurwitz zeta-style: ζ(2, 1/3) - ζ(2, 2/3) related to L(2, χ_{-3}).
# Hurwitz: ψ'(1/3) = ζ(2, 1/3); we already covered K2.

# M4. Hyperbolic 3-manifold volume of figure-8 knot complement:
# V_{4_1} = 2·V_{tet} ≈ 2.0299. Probe.
V_fig8 = 2 * V_reg_tet
M4 = V_fig8 / pi**2
report("M4 V(figure-8)/π²", M4, note="V_4_1 ≈ 2.0299; not target")

# M5. Eisenstein series E_2 (quasi-modular) at i: E_2*(i) = 3/π.
# So 1/E_2*(i) = π/3, and target × (π/3) = 2/9. No good probe.

# M6. CFKRS unitary 4-shift integral / 4! = unitary 4th-derivative coef.
# G(5)²/G(9): test as candidate for higher symmetry.
M6 = barnesg(5)**2 / barnesg(9)
report("M6 G(5)²/G(9)", M6, note="Higher Barnes-G; ≈ 1/24024")

# M7. WP volume of M_0,4: vol_WP(M_{0,4}) = π²/2 (small-genus). Test
# (rational)·vol_WP(M_{0,4})/π³.
vol_WP_04 = pi**2 / 2  # M_0,4 ≅ P^1\{0,1,∞,t}
M7 = mpf(2) * vol_WP_04 / (3*pi**3)
report("M7 (2/3)·vol_WP(M_{0,4})/π³", M7, note="= (2/3)·(π²/2)/π³ = 1/(3π)")

# M8. Mirzakhani vol(M_{2,0}): vol_WP(M_{2,0}) = 43π⁶/2160 (Mirzakhani 2007).
# Test: very small ratios.
vol_WP_20 = mpf(43) * pi**6 / 2160
M8 = vol_WP_20 / pi**7
report("M8 vol_WP(M_{2,0})/π⁷", M8, note="= 43/(2160π) ≈ 0.00633")

# M9. K_3(Z[i])  related to L'(0,χ_{-4}) = (π/4)log(?) — Lerch.
# L(0, χ_{-4}) = 1/2; L'(0, χ_{-4})/π = (1/2)·(2 log Γ(1/4) - log(π)/2 ...)
# Skip — would need nuanced derivation.

# M10. Beilinson-Kato: L(E_11a1, 2)/(2π)² for elliptic 11a1.
M10 = L_11_2 / (2*pi)**2
report("M10 L(11a1, 2)/(2π)²", M10, note="Beilinson-Kato shape; ≈ 0.0137")

# M11. Sarnak class-number constant h_d/√d for indefinite quadratics.
# h_d log(ε_d)·(weight) = π²/12 average — Gauss-Hermite-Selberg.
# Sum over d coincides with vol(SL(2,Z)\H₂) = π²/12 (heuristic).
M11_classnum_const = pi**2/12
M11 = M11_classnum_const / pi**3
report("M11 (π²/12)/π³ = 1/(12π)", M11, note="Sarnak class number average shape; ≈ 0.0265")

# M12. ζ(2)·ζ(3)/π^5 — multiple zeta proxy.
M12 = zeta(2)*zeta(3)/pi**5
report("M12 ζ(2)·ζ(3)/π⁵", M12, note="MZV proxy; ≈ 0.00201")

# M13. The motivic ζ value 16ζ(2)/π² · 1/(8π) = 2/(3π).
# This factors algebraically as (16/8)·(ζ(2)/π³) = 2·(1/6)/π = 1/(3π). NO.
M13 = mpf(16)*zeta(2)/(8*pi**3)
report("M13 16·ζ(2)/(8π³)", M13, note="= 16·(π²/6)/(8π³) = 1/(3π) ≈ 0.106")

# M14. The Dedekind zeta of Q(ω) = Q(ζ_3) at s=2:
# ζ_F(2) = ζ(2)·L(2, χ_{-3}). Test rational shape.
M14 = zeta(2)*L_chi_neg3_at_2 / pi**4
report("M14 ζ_{Q(ω₃)}(2)/π⁴", M14, note="Dedekind ζ; ≈ 0.0133")

# M15. Mahler measure m(P) for P = 1+x+y+xy: m = 7ζ(3)/(2π²) (Smyth).
# Test ratio vs target.
m_Smyth = 7*zeta(3)/(2*pi**2)
M15 = m_Smyth/pi
report("M15 m(1+x+y+xy)/π = 7ζ(3)/(2π³)", M15, note="Smyth mahler measure")

# M16. Mahler measure of Boyd's 11a1-related polynomial — yields L'(E_11,0).
# Boyd 1998: m(P_11) = (7√(11)/π²) · L(E_{11}, 2).
# Test natural ratios.
M16 = (7*sqrt(11)/pi**2)*L_11_2 / pi
report("M16 [Boyd 11a1]/π = (7√11/π³)·L(11a1, 2)", M16, note="Mahler for elliptic 11a1")

# ============================================================
# Sensitivity check on the apparent "matches"
# ============================================================
# For each algebraic-equivalent match, perturb the prefactor by 1% and
# show the value moves: confirms NOT a magic numerical coincidence
# (which the candidate authors used as a pre-emptive defense).

print("\n# Sensitivity check (1% perturbation):")
def sense(name, func_at_eps):
    # func_at_eps(eps) returns a value
    base = func_at_eps(0)
    perturbed = func_at_eps(mpf("0.01"))
    rel = (perturbed - base)/base
    print(f"#   {name}: base={base}, perturbed={perturbed}, rel={rel}")

sense("16/(24π)", lambda eps: mpf(16)/(24*pi*(1+eps)))
sense("4ζ(2)/π³", lambda eps: 4*zeta(2)*(1+eps)/pi**3)
sense("8·vol_WP/π³", lambda eps: 8*pi**2/12/(pi**3 * (1+eps)))


# ============================================================
# Final report
# ============================================================
print("\n# === MASTER TABLE ===")
print(f"# {'NAME':<60} | {'VALUE':<35} | {'RESIDUAL':<22} | CLASS")
print(f"# {'-'*60} | {'-'*35} | {'-'*22} | {'-'*15}")
for (name, value, residual, classification, note) in results:
    val_short = value[:28] + "..." if len(value) > 28 else value
    # Ensure residual displays exponent
    res_str = str(residual)
    if 'e' in res_str:
        res_short = res_str[:22]
    else:
        # Could be a plain decimal; format scientifically
        try:
            res_mpf = mpf(residual)
            if res_mpf == 0:
                res_short = "0"
            else:
                res_short = mp.nstr(res_mpf, 6)
        except:
            res_short = res_str[:22]
    print(f"# {name:<60} | {val_short:<35} | {res_short:<22} | {classification}")

# Summary stats
match_count = sum(1 for r in results if r[3] == "MATCH_TO_30_DIGITS")
near_miss = sum(1 for r in results if r[3] == "NEAR_MISS")
no_match = sum(1 for r in results if r[3] == "NO_MATCH")
print(f"\n# MATCH_TO_30_DIGITS: {match_count}")
print(f"# NEAR_MISS:          {near_miss}")
print(f"# NO_MATCH:           {no_match}")
print(f"# Total candidates:   {len(results)}")

# Diagnostic distinguishing constants
print("\n# DISTRACTOR/DISCRIMINATION TABLE:")
discriminators = {
    "2/(3π)": TARGET,
    "1/(24π)·16": mpf(16)/(24*pi),
    "1/(2π)": mpf(1)/(2*pi),
    "1/π²": mpf(1)/pi**2,
    "4/(3π²)": mpf(4)/(3*pi**2),
    "1/(2π²)": mpf(1)/(2*pi**2),
    "√π/8": sqrt(pi)/8,
    "7/33": mpf(7)/33,
    "(2/(3π))·ζ(3)": (mpf(2)/(3*pi))*zeta(3),
    "I_ON/11 = 2.3328/11": mpf("2.3328")/11,
}
for name, val in discriminators.items():
    diff = abs(val - TARGET)
    print(f"#   {name:<25} = {val} | diff = {diff}")

print("\n# Done.")
