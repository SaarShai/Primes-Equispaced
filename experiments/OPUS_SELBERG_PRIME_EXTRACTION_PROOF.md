# UNCONDITIONAL PROOF: Σ_{p≤x} M(p)²/p² = (6/π²)·log log x + O(1)
# Opus 4.6 analysis, 2026-04-09
# STATUS: Claimed complete — needs adversarial verification

## Theorem (Unconditional)
Σ_{p≤x} M(p)²/p² = (6/π²) · log log x + O(1).

## Proof

### Input: Selberg (1946)
Σ_{n≤x} M(n)²/n² = (6/π²) log x + O(1). Call this F(x).

### Step 1: Stieltjes decomposition
Σ_{p≤x} M(p)²/p² = ∫₂⁻ˣ (M(⌊t⌋)²/t²) dπ(t)
                    = ∫₂ˣ (M(⌊t⌋)²/t²) d(li(t)) + ∫₂ˣ (M(⌊t⌋)²/t²) dE(t)
where E(t) = π(t) - li(t) = O(t·exp(-c√log t)).

### Step 2: Main term
∫₂ˣ M(⌊t⌋)²/(t² log t) dt = Σ_{n≤x} M(n)²/(n² log n) + O(1)
(MVT: ∫_n^{n+1} dt/(t² log t) = 1/(n² log n) + O(1/(n² log²n)), error sum converges)

### Step 3: Partial summation on discrete sum
Σ_{n≤x} M(n)²/(n² log n) = Σ_{n≤x} (M(n)²/n²) · (1/log n)

Using F(x) = Σ_{n≤x} M(n)²/n² = (6/π²) log x + O(1) and weight g(n) = 1/log n:

= F(x)/log x + ∫₂ˣ F(t)/(t log²t) dt

= [(6/π²) log x + O(1)]/log x + ∫₂ˣ [(6/π²) log t + O(1)]/(t log²t) dt

= (6/π²) + O(1/log x) + (6/π²) ∫₂ˣ dt/(t log t) + O(∫ dt/(t log²t))

= (6/π²) + (6/π²)·log log x - (6/π²)·log log 2 + O(1)

= **(6/π²)·log log x + O(1)**

### Step 4: Error term = O(1)
∫₂ˣ f(t) dE(t) where f(t) = M(⌊t⌋)²/t².
Integration by parts: boundary term f(x)E(x) = O(exp(-c√log x)) → 0.
Smooth part: O(∫ exp(-c√log t)/t dt) converges.
Jump part: each Δf(n) = O(|M(n)|/n²), times E(n) = O(n·exp(-c√log n)),
gives O(|M(n)|/n · exp(-c√log n)). With M(n) = O(n), sum is O(Σ exp(-c√log n)) < ∞. ∎

## Key Observations (Opus)
- This is "folklore" — anyone who knows Selberg + partial summation could derive it
- NOT explicitly stated in the literature (checked: Ng, Soundararajan, Harper, Granville)
- The smoothness concern was a non-issue: Stieltjes integral handles step functions natively
- No hypothesis beyond PNT + Selberg needed — fully unconditional
- The constant 6/π² = 1/ζ(2) is elegant and connects to squarefree density

# ADDENDUM: This proof is INVALID — the Selberg input was wrong.
# See SELBERG_INPUT_DISPROVED.md for details.
# The (6/π²) constant was for μ(n)² (squarefree), not M(n)² (Mertens).
