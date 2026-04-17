# Checklist: Before Proposing Joint Paper with Koyama
*Updated: 2026-04-16 (after email exchange + Session 11 verification)*

## Numerical Evidence (MUST HAVE)
- [x] D_K for χ_{-4} at K ≤ 50,000: oscillates ~0.60 ± 0.03 ✓
- [x] D_K for χ_3 at K ≤ 10,000: oscillates ~0.61 ✓ (from KOYAMA_REPLY_DRAFT)
- [x] P_K for ζ: converges to -e^{-γ} ✓ (M1_DS_DUALITY_PRODUCT)
- [x] Sign contrast: P_K < 0 (ζ), D_K > 0 (L) ✓
- [x] **EDRH rate confirmed** (2026-04-16): |E_K^χ|·log K → C=|L'(ρ,χ)|/ζ(2) ✓ for χ_{-4} (88% at K=20K, exponent -0.928→-1) and χ_5 (93% at K=10K) — SENT TO KOYAMA
- [x] **T_∞ formula confirmed** (2026-04-16): T_∞=(1/2)Im(log L(2ρ,χ²)) for 3 characters; B_K object correctly identified as Im(log E_K^{χ²}(2ρ)) NOT Im(log D_K) ✓ — SENT TO KOYAMA
- [x] **Rate dichotomy B_K** (2026-04-16): principal χ² → O(1/log K); nonprincipal χ² → O(K^{-1/2}log²K) ✓
- [ ] D_K for χ_{-4} at K = 10^5 — in M1 queue
- [ ] D_K for ≥3 MORE characters (different moduli) — need to verify universality
- [ ] D_K at SECOND zero of L(s,χ_{-4}) — does it differ?
- [ ] Higher-order sum R(ρ_χ) = Σ_p Σ_{k≥2} 1/(kp^{kρ_χ}) — Koyama's explanation
- [ ] **GL(2) NDC for 37a1**: BLOCKED — need Koyama's c_K^E definition; raw Dirichlet series gives Cesàro mean 0.45 at K=200 (trending toward 0); asymptotic onset K~6×10^6

## Theoretical Understanding (SHOULD HAVE)
- [x] Koyama's explanation: k≥2 higher-order terms after k=1 cancellation ✓
- [x] **B_∞ mechanism explained**: rate dichotomy from principal/nonprincipal χ² cancellation ✓
- [ ] Rigorous proof that D_K converges (or at least conditional on GRH)
- [ ] Proof that limit = 1/ζ(2) specifically (not just "some constant")
- [ ] Connection to Aoki-Koyama (2023) convergence rate O((log K)^{-m})
- [ ] Why universal across χ? (Must explain independence from character)
- [ ] Relationship between e^{-γ} (ζ case) and 1/ζ(2) (L case) — coincidence or connected?
- [ ] **GL(2) c_K^E formula**: awaiting Koyama's response to 3 questions (Apr 16 email)

## Literature Check (MUST HAVE)
- [x] **Akatsuka (2017)** (NOT 2013): "On the Euler products for the Riemann zeta-function" Kodai Math J 40:79-101 ✓
- [x] **Sheth (2025a)** IMRN rnaf214: Euler products for elliptic curves — DIRECTLY RELEVANT to GL(2) ✓
- [x] **Sheth (2025b)** Math Proc Cambridge Phil Soc 179:2 pp.331-349: central Euler products ✓
- [x] **Kaneko (2022)** Bull Australian Math Soc 106:48-56: Dirichlet L-function Euler products ✓
- [ ] Verify Aoki-Koyama (2023) paper: exact title, journal, theorem numbers
- [ ] Check if D_K → constant at L-function zeros appears ANYWHERE in literature
- [ ] Check if c_K^χ × Euler product formula appears in Montgomery-Vaughan, Iwaniec-Kowalski

## Paper Drafting (NICE TO HAVE before proposing)
- [ ] 1-page summary of results + conjectures
- [ ] Clean Python code producing all tables (reproducible)
- [ ] Error analysis: distinguish 1/ζ(2) from e^{-γ} to needed precision

## Risk Assessment
- Convergence is O(1/log K) — VERY slow
- At K=50000, |D_K - 6/π²| ≈ 0.015 — that's 2.5% error
- Need K ~ 10^8 to get 1% — infeasible with mpmath
- BUT: averaging over multiple characters/zeros may reduce variance
- Alternative: numpy complex128 for large K (loses precision but gains speed)
