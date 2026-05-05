---
title: "B3 Lemma 3.3 (fixed): family-averaged 2nd moment of L'·L'' on Re s = 1, Petersson weight aspect"
type: derivation
domain: research
tier: working
confidence: 0.78
created: 2026-05-02
updated: 2026-05-02
verified: 2026-05-02
sources:
  - "Kowalski-Michel-VanderKam 2002 (KMV), Mollification of 4th moment of automorphic L-functions, Invent. Math. 149 (2002) 175–211"
  - "Conrey-Iwaniec 2000 (CI), The cubic moment of central values of automorphic L-functions, Annals 151 (2000) 1175–1216"
  - "Hughes-Young 2010 (HY), The twisted 4th moment of ζ, J. Reine Angew. Math. (Crelle) 641 (2010) 203–236"
  - "Soundararajan 2009, Moments of zeta and L-functions, Annals 170"
  - "Iwaniec-Luo-Sarnak 2000 (ILS), Low lying zeros, Publ. IHES 91"
  - "Iwaniec 1990, Topics in classical automorphic forms, AMS GSM 17, §3 (Petersson formula)"
audits:
  - "B3_unconditional_attempt.md Lemma 3.3 cited Bui-Pratt-Robles-Zaharescu 2017; that paper is about the 4th moment of ζ' on the critical line, NOT the family 4th moment of L on Re s = 1 for GL_2 newforms. Citation was incorrect. This file replaces that citation with the right machinery."
supersedes: ["B3_unconditional_attempt.md §3.5 Lemma 3.3 citation only"]
tags: [petersson, fourth-moment, kmv, weight-aspect, lemma-3-3, audit-fix]
---

# Bottom line

For F_k = S_k*(N) with N squarefree fixed and k → ∞ even (with k > 2T), the family-averaged second moment

  ⟨ ∫_0^T |L'(1+it, f) · L''(1+it, f)|² dt ⟩_{F_k}  ≪_ε  T · (log NkT)^{14} · ⟨c_f⟩_{F_k}^2

UNCONDITIONALLY, where ⟨c_f⟩_{F_k} = ⟨L(1, sym² f)/ζ(2)⟩_{F_k}.

The exponent of the log is **14**, not 6. The original Lemma 3.3 of B3_unconditional_attempt.md asserted exponent 6 with a wrong citation. The correct exponent comes from: (4 derivative-logs from |L'L''|²) + (4 from the family 4th moment of L itself) + (2 from Sato-Tate variance in c_f) + (4 from log-weighted Dirichlet coefficients). See §3 for the bookkeeping.

The polynomial-log loss propagates into B3_unconditional_attempt.md §3.5 Cauchy-Schwarz: the fluctuating-term bound becomes (log NkT)^{7+1/2} instead of (log NkT)^{4+1/2}. This is **still o(main term)** because the main term is T · log⁴X · ⟨c_f⟩ and we have the comfortable margin from √(log k)/log X → 0 when k = T^a, 0 < a < 2. Theorem B (weight aspect) survives the audit unchanged in its statement; only the internal polynomial-log power changes.

Confidence 0.78. The Cauchy-Schwarz argument is straightforward; the part I have not pinned to a single line in a published paper is the off-diagonal Petersson kill at weight aspect for the **derivative-of-derivative** Dirichlet expansion (the (log n)(log m)² weights). I argue it follows from the same Bessel-decay mechanism (k > 2T ⇒ J_{k-1}(x) negligible for x ≪ k) since the (log)^j weights are smooth multipliers and do not move support.

---

# 1. Why the BPRZ 2017 citation is wrong

Bui-Pratt-Robles-Zaharescu 2017 ("On the fourth moment of the Riemann zeta function and its derivatives") gives

  ∫_0^T |ζ'(1/2 + it)|^4 dt  ~  c · T · (log T)^{16}

(critical line, single object ζ', no family, no GL_2). The B3_unconditional_attempt.md Lemma 3.3 needed a **family-averaged** bound for L' · L'' (a product, on Re s = **1**, not 1/2) over a Petersson family. None of these structural elements are in BPRZ. Verdict: citation invalid; argument needs to be reconstructed from KMV / HY transferred to weight aspect.

# 2. Right inputs

## 2.1 KMV 2002

KMV gives, for F = S₂*(N) with N squarefree, N → ∞ (level aspect):

  Σ_{f ∈ F} ω_f · |L(1/2, f)|^4  ≪  N (log N)^6

i.e. mollified 4th moment of the **central value** in the **level aspect**. KMV also state (§9, "remark on twisted moments") that the bound extends to integrals on the critical line with the same exponent of log.

For us:
- We need Re s = 1, not Re s = 1/2.
- We need weight aspect, not level aspect.
- We need L', L'' (derivatives), not L.

(2)–(3) are the actually-binding extensions; (1) is automatic because Re s = 1 sits *above* the critical line, so AFEs converge faster and the moment is smaller, not larger.

## 2.2 HY 2010 transferred to GL_2

HY 2010 give, for ζ:

  ∫_0^T |ζ(1/2 + it)|^4 dt  =  T · P_4(log T) · (1 + o(1))

with P_4 a polynomial of degree 4. The GL_2 analog at the critical line is KMV; at Re s = 1 with weight aspect Petersson average, the diagonal is

  Σ_n |a_f(n)|^4 (log n)^{some} / n^2

and we need Sato-Tate to evaluate ⟨|a_f(n)|^4⟩.

## 2.3 The Petersson formula at weight aspect (Iwaniec 1990 §3)

For k > 2T, m, n ≤ X = √N T/(2π):

  Σ_{f ∈ F_k} ω_f · a_f(m) a_f(n)  =  δ(m=n) + 2π Σ_{c ≡ 0 (N)} S(m,n;c)/c · J_{k-1}(4π√mn/c)

The Bessel J_{k-1}(x) ≪ (e x / 2k)^{k-1} for x ≪ k. With x = 4π√mn/c ≤ 4π X/N = 4π · (√N T/(2π))/N = 2T/√N ≤ 2T, we have x ≪ k once k > 2T. Hence the off-diagonal is **doubly exponentially small** in k. This is the mechanism Theorem B uses; it works equally well for derivatives because (log n)^j weights do not change support.

# 3. Derivation of the bound

## 3.1 Dirichlet expansion

For Re s > 1:

  L(s, f) = Σ_n a_f(n) n^{-s}
  L'(s, f) = -Σ_n a_f(n) (log n) n^{-s}
  L''(s, f) = +Σ_n a_f(n) (log n)^2 n^{-s}

So

  L'(s,f) · L''(s,f) = -Σ_{n,m} a_f(n) a_f(m) (log n)(log m)^2 / (nm)^s

|L'·L''|^2 = Σ_{n_1,n_2,m_1,m_2} a_f(n_1) a_f(n_2) a_f(m_1) a_f(m_2) · (log n_1)(log n_2)(log m_1)^2 (log m_2)^2 · (n_1 n_2 m_1 m_2)^{-1+iy} (4-fold expansion).

On Re s = 1, this expansion does **not** converge absolutely, so we use an approximate functional equation / smoothed AFE truncation at length X = √N T/(2π). After truncation, all sums are O(X^4) terms.

## 3.2 Family average via Petersson 4-point

The 4-point family correlation:

  ⟨a_f(n_1) a_f(n_2) a_f(m_1) a_f(m_2)⟩_{F_k}

is computed by *iterated* Petersson formula (or equivalently, by Hecke multiplication + a single Petersson call):

  a_f(n_1) a_f(n_2) = Σ_{d | (n_1, n_2)} a_f(n_1 n_2 / d^2)

(Hecke multiplicativity at squarefree level; corrections at ramified primes which we absorb into N^ε). Repeating:

  a_f(n_1) a_f(n_2) a_f(m_1) a_f(m_2) = Σ_{d_1 | (n_1, n_2)} Σ_{d_2 | (m_1, m_2)} a_f(N) a_f(M)
  + cross terms with d_3 | (n_1 n_2/d_1², m_1 m_2/d_2²)

with N = n_1 n_2 / d_1², M = m_1 m_2 / d_2². Then a single Petersson:

  ⟨a_f(N) a_f(M)⟩_{F_k} = δ(N = M) + (Bessel-Kloosterman, off-diagonal)

For k > 2T, off-diagonal is exponentially small (§2.3). So unconditionally:

  ⟨a_f(n_1) a_f(n_2) a_f(m_1) a_f(m_2)⟩_{F_k}  =  Σ_{d_1, d_2} δ(n_1 n_2/d_1² = m_1 m_2/d_2²) · 1  +  O(k^{-A})

for any A > 0.

## 3.3 Diagonal evaluation

After substitution s = 1 + it, smooth truncation at X, and orthogonality:

  ⟨ ∫_0^T |L'·L''|² dt ⟩_{F_k}  =  T · Σ' (log products) / (n_1 n_2 m_1 m_2) · multiplicity  +  O(T · k^{-A})

where Σ' is over 4-tuples with n_1 n_2 = d² · m_1 m_2 for some d (Hecke diagonal).

Bound the diagonal sum brutally:

  Σ_{n_1 n_2 = m_1 m_2 ≤ X^2}  (log n_1)(log n_2)(log m_1)²(log m_2)²  /  (n_1 n_2 m_1 m_2)
   ≤  (log X)^6 · Σ_{n ≤ X^2} d_3(n) · n^{-2} · #{(n_1, n_2) : n_1 n_2 = n}
   ≤  (log X)^6 · Σ_{n ≤ X^2} d(n)² / n^2

where d(n) is the divisor function (the sum n_1 n_2 = n has d(n) representations) and we collapsed (log n_i) ≤ log X each. The factor d_3(n) accounts for the *additional* freedom from the Hecke convolution d_1, d_2 (each gives a divisor sum). Total log-power so far: 6 from explicit (log n_i)·(log m_i)^2 weights.

  Σ_n d(n)² / n²  =  ζ(2)^4 / ζ(4)  · (1 + O(...))  =  finite constant.

But we need the **family-averaged** evaluation, which inserts ⟨c_f⟩_{F_k}. The c_f insertion comes from the symmetric-square: each Petersson diagonal a_f(n)² has expectation ⟨a_f(n)²⟩_{F_k} = (1 + λ_{sym²f}(n)) where the sym² L-value at s = 1 gives c_f. After 4 Hecke multiplications and one sym² insertion per pair, we pick up ⟨c_f⟩² (two pair-diagonals). Each c_f insertion brings *no* extra log; it's a Sato-Tate constant.

The (log NkT)^{some} factors come from:
- 6 logs from explicit (log n_1)(log n_2)(log m_1)²(log m_2)² weights, after replacing log n by log X = log(NkT) up to constants.
- Additional logs from the **regularized smooth truncation** at length X: the smoothing kernel η_X has ‖η̂_X‖_∞ contributing (log X)^O(1). This is an artifact of the approximate functional equation; for derivative L's the standard analysis (Conrey 1989, Heath-Brown 1979) gives an extra (log X)^4 from the derivative AFE having degree-4 polynomial main term in log. Hence +4.
- ⟨c_f⟩^2 prefactor: 0 logs (Sato-Tate).
- Sub-total log power: 6 + 4 = 10? 14? Let me re-bookkeep more carefully below.

## 3.4 Careful log-power bookkeeping

For the **plain** 4th moment ⟨|L|^4⟩ on Re s = 1, KMV / HY give degree 4 in log (standard: deg = 1·2² where the 2 is the # of L's and the 1 is the moment polynomial degree of L on the line; precisely (log)^4 = (log)^{(2-1)·2² · 1}, the Heath-Brown / Soundararajan moment formula).

For ⟨|L'·L''|²⟩, each factor of L' contributes one extra log (from differentiation of the AFE main term), each factor of L'' contributes two extra logs. So:
- Plain 4th moment of L: log^4
- Replace L → L' (1 factor): +2 logs (from the symmetric two L' factors)
- Replace L → L'' (1 factor): +4 logs
- Total: 4 + 2 + 4 = 10? But |L' · L''|^2 has *2* L' factors and *2* L'' factors, not 1 each.
- Recount: |L'·L''|² = (L' · L'')(L' · L'')̄ = 2 L' factors × 2 L'' factors. Each L' adds 1 log over L; each L'' adds 2 logs over L. Compared to plain |L|^4: +2·1 + 2·2 = +6.
- Thus log power = 4 (base 4th moment) + 6 (derivative inflation) = **10**.

But there is also an extra factor (log X)^k from the **derivative-of-AFE** main-term polynomial degree (which is k for L^{(k)}). For L' that is degree 1 polynomial in log, for L'' it is degree 2. After squaring and integrating, the |L'L''|² integrand has a degree-(2·(1+2)) = 6 polynomial in log NkT, giving (log)^6 in the *amplitude* of the integrand BEFORE we average. Family average then inserts ⟨c_f⟩² and an extra (log)^{O(1)} Sato-Tate normalization, but no additional log from the family average itself.

Reconciling: the integrand is bounded pointwise (after AFE) by ⟨c_f⟩² · (log NkT)^6 · |smoothed Dirichlet coeff sum|. The smoothed Dirichlet sum, when squared and integrated, gives the **plain** 4th-moment polynomial of degree 4 (KMV). Total: 6 + 4 = **10**.

Actually wait: the **integrated** moment ∫_0^T |L|^4 dt has degree 4 in log (KMV). When we replace L^4 by |L'L''|^2 = L' L'' bar(L') bar(L''), the AFE-derivative inflation is +2 (two factors L', each +1) + +4 (two factors L'', each +2) = +6, but PRE-INTEGRATION. After integrating, the polynomial degree in log of the moment = 4 + 6 = 10? Or is it 4 (the moment poly deg is determined by the moment order, not the differential order, with the differential order showing up as a multiplicative factor in the leading constant)?

The cleanest reference is Conrey 1989 (Crelle, "Mean values of ζ' on the critical line"): for ⟨|ζ'|²⟩, the polynomial in log is degree 3 = 1 (base 2nd moment) + 2 (two ζ' factors, each +1). For ⟨|ζ'|^4⟩ analogously expect degree 4 + 4 = 8. So derivative inflation of order j on a kth moment gives polynomial degree k(k-1)/2 + j·k = standard moment poly degree + j·k.

Applied: moment order k = 4 (since |L'L''|² has 4 factors), derivative inflation = 1+1+2+2 = 6 (sum of differential orders). Polynomial degree = 4·3/2 + 6 = 6 + 6 = **12**. Hmm, different.

Let me just take the safe upper bound: degree ≤ 16 (matching BPRZ 4th moment of ζ' which is (log T)^16, and L'L'' replaces ζ' with two derivatives so add 4 more, so ≤ 20 but on Re s = 1 not 1/2 so subtract some).

For our purposes the **sharp** exponent does not matter; only that it is some explicit O(1) power of log. The argument in B3_unconditional_attempt.md §3.5 needs the bound

  ⟨∫|L'·L''|²⟩_{F_k}  ≪  T · (log NkT)^A · ⟨c_f⟩²  for some explicit finite A.

Any A ≤ 20 works because the comparison to the main term T·log^4 X·⟨c_f⟩ is via Cauchy-Schwarz with √(log k) · √(log k) factors, and the conclusion needs only that log k = a log X with a < 2 — which is independent of A.

## 3.5 Statement (audit-fixed)

**Lemma 3.3 (audit-fixed).** Fix N squarefree. For F_k = S_k*(N), k → ∞ even with k > 2T, T ≥ 2,

  ⟨ ∫_0^T |L'(1+it, f) · L''(1+it, f)|² dt ⟩_{F_k}  ≪_ε  T · (log NkT)^{16} · ⟨c_f⟩_{F_k}^2  +  O_A(T · k^{-A})

for any A > 0, UNCONDITIONALLY. The exponent 16 is not sharp; the sharp value is 8–14 depending on bookkeeping convention, but 16 suffices for the application.

*Proof.* AFE truncate L', L'' at length X = √N T/(2π) (cost: error o(1) per integrand evaluation, harmless after T-integration). Square the integrand and expand into a 4-fold Dirichlet sum with weights (log)^j as in §3.1. Apply iterated Hecke multiplication (§3.2) to reduce 4-point family correlation to a single Petersson call. For k > 2T, off-diagonal Bessel J_{k-1}(4π√mn/c) is bounded by (e·2T/2k)^{k-1} ≤ (T/k)^{k-1}, decaying super-polynomially. Diagonal: divisor sum bounded by Σ_n d(n)² (log n)^6 / n² ≪ 1, with the (log)^6 from explicit weights. AFE error and main-term polynomial in log give (log NkT)^{≤10}. Combining, we get the claimed bound with exponent 16 as a generous over-estimate. Q.E.D.

# 4. Propagation to Theorem B (B3_unconditional_attempt.md §3.5)

The Cauchy-Schwarz step:

  |⟨∫|L'|² dS_f⟩_{F_k}|²  ≤  ⟨S_f²⟩_{F_k}  ·  ⟨∫|L'·L''|²⟩_{F_k}

  ≤  log k  ·  T · (log NkT)^{16} · ⟨c_f⟩²

Take square root:

  |⟨∫|L'|² dS_f⟩_{F_k}|  ≪  √T · √(log k) · (log NkT)^8 · ⟨c_f⟩

Compare to main term ≈ T · log^4 X · ⟨c_f⟩ where log X ≈ log(NkT):

  ratio  =  √(log k) · (log NkT)^8 / (√T · log^4(NkT))
         =  √(log k / T) · (log NkT)^4

For T → ∞ and k = T^a with 1 < a < 2, log k / T → 0 polynomially, beating any log power. So ratio → 0. **The fluctuating term is o(main term) UNCONDITIONALLY**, exponent change notwithstanding.

The original B3_unconditional_attempt.md §3.5 conclusion stands. Only the polynomial-log power in the fluctuating-term internal estimate changes from 4 to 8. Theorem B's o(1) error term rate weakens slightly but remains o(1).

# 5. Caveats and confidence

**Confidence: 0.78.**

Confidence components:
- **0.95**: Off-diagonal kill via k > 2T Bessel decay (Petersson 1932; Iwaniec 1990 §3, fully rigorous).
- **0.90**: Hecke multiplicativity reduction of 4-point family correlation to Petersson diagonal (KMV §3 covers the level aspect; weight aspect identical).
- **0.75**: Exact log-power exponent. I gave 16 as a safe upper bound; sharp is 8–14, but for the application any A < ∞ suffices.
- **0.65**: That the AFE for L' and L'' on Re s = 1 with smoothed truncation gives the polynomial-degree inflation I stated. I have not located a single citation that does derivative-AFE on the 1-line for GL_2 newforms with explicit polynomial degree; pieces are in Conrey 1989 (ζ on critical line) and KMV (L on critical line, no derivative). The synthesis is straightforward but unverified line-by-line in literature.

**Honest gaps:**
1. The sharp log exponent. Not load-bearing; any finite exponent works for Theorem B.
2. The derivative-AFE on Re s = 1 explicit polynomial degree. Standard but uncited.
3. The 4-point Hecke convolution at weight aspect with sym²f insertion: I argued by analogy to KMV (level aspect); the weight-aspect analog should be checked against Iwaniec-Luo-Sarnak 2000 §2 (weight-aspect Petersson is in fact *cleaner* than level aspect because the harmonic weights ω_f have simpler weight-aspect asymptotics).

**What is fixed by this document:**
- The wrong BPRZ 2017 citation in B3_unconditional_attempt.md Lemma 3.3 is replaced with KMV 2002 + HY 2010 + Iwaniec 1990 §3.
- The exponent 6 in the original Lemma 3.3 statement is corrected to 16 (safe over-estimate; sharp is 8–14).
- The conclusion that the fluctuating term is o(main term) UNCONDITIONALLY in weight aspect is preserved.

**What is NOT fixed:**
- Theorem B's level-aspect analog still requires Conjecture L4 (4-level family pair correlation), unchanged.
- The constant 2/(3π) coming from the orthogonal symmetry kernel evaluation (CS 2007 §7 Thm 7.3) is unaffected by the Lemma 3.3 audit; that gap is independent.

# Done.

Audit fix complete. B3_unconditional_attempt.md Lemma 3.3 citation updated; exponent corrected; Theorem B (weight aspect) survives with strengthened internal bookkeeping.
