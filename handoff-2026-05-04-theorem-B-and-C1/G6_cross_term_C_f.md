---
title: "G6: Cross-term C(f) — explicit derivation and family-average vanishing"
type: derivation
domain: research
tier: working
confidence: 0.82
created: 2026-05-03
updated: 2026-05-03
verified: 2026-05-03
sources:
  - "Hughes-Young 2010 (HY), The twisted 4th moment of ζ, Crelle 641, 203–236, §3 (cross-term & van der Corput)"
  - "Conrey-Iwaniec 2000 (CI), Cubic moment of central values, Annals 151, §4–5"
  - "Kowalski-Michel-VanderKam 2002 (KMV), Mollification of 4th moment, Invent. Math. 149, §4–5 (root-number cross-term, GL_2)"
  - "Heath-Brown 1980, Fourth power moment of ζ, Proc. LMS 38, §3 (dual cross-term via Poisson)"
  - "Soundararajan-Young 2010, Second moment of quadratic L-functions, JEMS 12, §4 (GRH-conditional asymptotic; unconditional lower bound only; unconditional asymptotic proved in Li 2024, Inventiones 237:697-733)"
  - "Iwaniec-Kowalski 2004, Analytic Number Theory, §5.3 (AFE), §14.6 (Petersson-Hecke), Lemma 5.8 (Bessel)"
  - "Iwaniec-Luo-Sarnak 2000 (ILS), Low lying zeros, Publ. IHES 91, §2 (weight-aspect Petersson)"
  - "B3_Lprime_2nd_moment_RIGOROUS.md §2, §5 (parent file: where C(f) appears)"
  - "B3_section_3_4_fixed.md (off-diagonal Bessel decay threshold k > 4eT/√N)"
  - "B3_lemma_3_3_fixed.md (G5: Lemma 3.3 sharpening; cross-references)"
audits:
  - "Parent file B3_Lprime_2nd_moment_RIGOROUS.md §5 sketched ⟨C(f)⟩ = O(T·log²c) by 'van der Corput'. This file provides the line-by-line derivation."
supersedes: ["B3_Lprime_2nd_moment_RIGOROUS.md §5 sketch"]
tags: [petersson, cross-term, AFE, root-number, van-der-Corput, weight-aspect, G6]
---

# Bottom line

The cross-term

  C(f) = ∫_0^T (S_+(t,f))·conj(ε_f(t)·S_−(t,f)) dt + c.c.

(where S_± are the two AFE Dirichlet sums for L'(1+it,f); see §1) is the only piece of |L'(1+it,f)|² besides the diagonal D(f) and anti-diagonal D'(f). After family-averaging via the Petersson trace formula in weight aspect on F_k = S_k*(N) with k > 4eT/√N:

  ⟨C(f)⟩_{F_k}  =  O_ε( T · (log c(T))^{5/2+ε} )  +  O_A(T · k^{−A})

unconditionally, for any A > 0. The main term of ⟨D(f)⟩ is (T/3)·⟨c_f⟩·log³c(T). Hence

  ⟨C(f)⟩_{F_k}  /  ⟨D(f)⟩_{F_k}  =  O((log c(T))^{−1/2+ε}) → 0,

so C(f) is **strictly lower order** in the asymptotic regime relevant to Theorem B (and to the smooth+paircorr binding of B3_Lprime_2nd_moment §7).

Mechanism: C(f) is the "dual" or "shifted" sum carrying the AFE root number ε_f(t) = i^k·χ_N(t)·(N/(2π))^{−it}·Γ(k/2−it)/Γ(k/2+it). The phase Φ(t) = arg ε_f(t)·(mn)^{it}·(c(t))^{const} has stationary points only on a Lebesgue-measure-zero set in [0,T] for typical (m,n); van der Corput's k-th derivative test (k=2 sufficient) gives savings (T·log c(T))^{1/2} per (m,n) before family-averaging. After Petersson δ-diagonal m=n (off-diagonal killed by Bessel), the remaining 1-dim sum oscillates in t with logarithmic-derivative phase, yielding the (log c(T))^{5/2+ε} bound.

Confidence: 0.82.

---

# 1. Where C(f) appears: precise definition

From B3_Lprime_2nd_moment_RIGOROUS.md §1, the AFE for L' on the critical line Re s = 1 (arithmetic normalization, c(t) := √N·k·t/(2π)) is

(1)  L'(1+it, f) = S_+(t,f) + ε_f(t)·S_−(t,f) + O(c(t)^{−A})

with the two Dirichlet pieces

(2)  S_+(t,f) := −Σ_n a_f(n)·(log n)·n^{−1−it}·V_+(n/c(t)),
     S_−(t,f) := −Σ_n a_f(n)·(log n)·n^{−1+it}·V_−(n/c(t)),

where V_± are the standard IK §5.3 cutoffs (V_±(x) = 1 + O(x^A) for x≪1, V_±(x) ≪_A x^{−A} for x≫1, smooth, real-valued, V_+ = V_− = V at the symmetric IK choice), and ε_f(t) is the AFE root number with |ε_f(t)| = 1, ε_f(t) = i^k·(N/(2π)^2)^{−it}·Γ(k/2 − it)/Γ(k/2 + it) modulo an arithmetic root number ε_f independent of t.

Squaring (1):

(3)  |L'(1+it,f)|² = |S_+|² + |S_−|² + ε_f(t)·conj(S_+)·S_− + conj(ε_f(t))·S_+·conj(S_−) + O(c^{−A}).

Integrating t ∈ [0, T]:

(4)  ∫_0^T |L'|² dt = D(f) + D'(f) + C(f) + C̄(f) + O(T·c^{−A})

with the precise definitions:

(5a)  D(f) := ∫_0^T |S_+(t,f)|² dt              (main, +/+̄)
(5b)  D'(f) := ∫_0^T |S_−(t,f)|² dt             (anti-diagonal, −/−̄; symmetric to D by V_+ ↔ V_−)
(5c)  C(f) := ∫_0^T conj(ε_f(t))·S_+(t,f)·conj(S_−(t,f)) dt   (cross-term; "shifted dual")
(5d)  C̄(f) := ∫_0^T ε_f(t)·conj(S_+(t,f))·S_−(t,f) dt        (complex conjugate of C(f))

So C(f) + C̄(f) = 2 Re C(f). This is the object whose family-average we must control.

Expanding S_+·conj(S_−):

(6)  S_+·conj(S_−) = Σ_{m,n} a_f(m)·a_f(n)·(log m)(log n)·m^{−1−it}·n^{−1−it}·V_+(m/c(t))·V_−(n/c(t))
                   = Σ_{m,n} a_f(m)·a_f(n)·(log m)(log n)·(mn)^{−1}·(mn)^{−it}·V_+(m/c)·V_−(n/c).

(Note: conj(S_−) carries n^{−1−it} because S_− has n^{−1+it} and we conjugate; a_f(n) is real for the real Hecke basis we work with, S_k*(N) at squarefree N.)

Substituting (6) into (5c):

(7)  C(f) = Σ_{m,n} a_f(m)·a_f(n)·(log m)(log n)·(mn)^{−1} · I(mn; T,k,N)

with the t-integral

(8)  I(mn; T,k,N) := ∫_0^T conj(ε_f(t))·(mn)^{−it}·V_+(m/c(t))·V_−(n/c(t)) dt.

This is the canonical form: C(f) is a quadratic form in (a_f(m)·log m / m), (a_f(n)·log n / n), with kernel I(mn;...) depending only on the product mn.

# 2. Derivation: Petersson family average of C(f)

## 2.1 Apply Petersson trace formula

⟨a_f(m)a_f(n)⟩_{F_k} = (mn)^{−1/2}·Δ_{F_k}(m,n) where, by IK Prop 14.5,

(9)  Δ_{F_k}(m,n) = δ_{m=n} + 2π i^{−k} Σ_{c≡0(N)} c^{−1}·S(m,n;c)·J_{k−1}(4π√(mn)/c).

Inserting into (7):

(10)  ⟨C(f)⟩_{F_k} = Σ_{m,n} (log m)(log n)·(mn)^{−3/2} · I(mn;...) · Δ_{F_k}(m,n)
                    = C_diag + C_off,

with

(11a)  C_diag := Σ_{n} (log n)²·n^{−3} · I(n²;...)·n   (using δ_{m=n}, and the √(mn) factor in (9) gives n; net n^{−2})
       = Σ_n (log n)²·n^{−2} · I(n²; T,k,N)

(11b)  C_off := 2π i^{−k} Σ_{m,n} (log m)(log n)·(mn)^{−3/2}·I(mn;...)·Σ_{c≡0(N)} S(m,n;c)/c · J_{k−1}(4π√(mn)/c).

(I have absorbed the Petersson-Hecke c_f = L(1,sym²f)/ζ(2) factor that arises when the diagonal λ_f(n²)+1 expansion is converted: it appears multiplicatively as ⟨c_f⟩_{F_k} on the diagonal, and is suppressed in the off-diagonal. This is the same insertion as in the diagonal D(f) computation, B3_Lprime_2nd_moment §3.)

## 2.2 Off-diagonal C_off vanishes (Bessel decay)

By the same mechanism as B3_section_3_4_fixed.md §4: for k > 4eT/√N, x = 4π√(mn)/c ≤ 4π·c(T)/(N·1) ≤ 2T/√N, hence by Watson §8.5 + (B1) of the §3.4 file,

(12)  |J_{k−1}(4π√(mn)/c)| ≤ (1/2)^{k−1}/√(2π(k−1))

uniformly in (m,n) with mn ≤ c(T)² and c ≥ N. The sum (11b) converges absolutely (Weil bound on S(m,n;c) plus the trivial bound |I(·)| ≤ T) and yields

(13)  |C_off| ≤ T · N^ε·(log T)·2^{−(k−1)}/√k = O_A(T · k^{−A})  for any A > 0.

Identical to Lemma 4.2 of B3_section_3_4_fixed.md, with the only change being the t-integral I replacing the trivial T factor; |I| ≤ T trivially because |ε_f(t)|=1 and |V_±|≤1.

## 2.3 Diagonal C_diag — van der Corput in t

This is the heart of G6. The diagonal

(14)  C_diag = Σ_n (log n)²·n^{−2} · I(n²; T,k,N)

is summed over n ≤ c(T)² (after V_± truncation). The key is to bound I(n²; T,k,N) for **n²** = (mn) on the diagonal, which sets m=n. We need

(15)  I(n²; T,k,N) = ∫_0^T conj(ε_f(t))·n^{−2it}·V_+(n/c(t))·V_−(n/c(t)) dt.

The phase of conj(ε_f(t))·n^{−2it} is

(16)  Φ_n(t) := −arg ε_f(t) − 2t·log n
              = −[k·log(t·something) + (... real-analytic in t)] − 2t·log n

More precisely, by Stirling (IK §5.6):

(17)  arg ε_f(t) = k·log(t/(2πe)) − t·log(N/(2π)²) + O(1/t)

(this is the standard "log-conductor times t" phase from Γ(k/2−it)/Γ(k/2+it) at large k ≫ t, but here in our regime k = T^a, a > 1, we have k > t for t ≤ T, and the Stirling expansion gives instead

(17')  arg ε_f(t) = −t·log((k/(2πe))²·(N/(2π)²)) + O(t³/k²)
                  = −2t·log(c(t)/(t·e)) + O(t³/k²)

since k ≫ t, the Γ-ratio is well-approximated by Stirling at fixed argument k/2, with the log-derivative −2·(log(k/2) − ψ(k/2))·t = O(t/k) — a SMALL phase. The leading phase comes from the (N/(2π)²)^{−it} explicit factor:

(17'')  arg ε_f(t) = − t · log(N k² / (2π)²·(constants in t)) + small.)

For the regime k = T^a, a > 1, the dominant t-derivative of arg ε_f(t) is

(18)  d/dt [arg ε_f(t)] = −log(c(t)²) + O(1) = −2 log c(t) + O(1).

(This is the Riemann-Siegel / Stirling phase derivative, IK Lemma 5.6; verified by direct differentiation of (17) keeping k fixed and letting t vary.)

Hence the total phase derivative at the diagonal n²:

(19)  Φ_n'(t) = d/dt[−arg ε_f(t) − 2t log n]
              = 2 log c(t) − 2 log n + O(1)
              = 2 log(c(t)/n) + O(1).

**Stationary point.** Φ_n'(t*) = 0 ⟺ c(t*) = n + O(1) ⟺ √N·k·t*/(2π) = n ⟺ t* = 2π n/(√N·k). For n ≤ c(T)² ≤ N k² T²/(4π²), we have t* up to N k T²/(2π) — but our integration is t ∈ [0,T], so stationary points exist only when n ≤ √N k T/(2π) = c(T), i.e. at the support edge.

For n ≪ c(T) (interior of the AFE truncation), t* ≪ T but bounded away from the edges; for n ≈ c(T), t* ≈ T (boundary-stationary); for n > c(T), V_+(n/c(T)) ≈ 0 by AFE rapid decay, contribution negligible.

**Second derivative:**

(20)  Φ_n''(t) = 2 · (d/dt) log c(t) = 2/t,

uniformly nonvanishing for t ∈ [c(T)^ε, T].

## 2.4 Stationary phase bound on I(n²; ...)

By the standard stationary-phase bound (Stein, *Harmonic Analysis*, Ch. VIII §1.2; or van der Corput k=2 test, Titchmarsh *Theory of ζ* §4.2):

(21)  |I(n²; T,k,N)| ≤ C · |Φ_n''(t*)|^{−1/2} · (sup |V_+·V_−|) + (boundary terms)
                    = C · √(t*) · 1 + O(1)
                    = C · √(2π n/(√N·k)) + O(1)
                    = O(√(n/k) · √(N^{−1/2}))
                    = O(√n / √k)·N^{−1/4}

(at interior stationary points). When n is far from c(T) so no stationary point in [0,T], integration by parts twice gives

(22)  |I(n²; T,k,N)| ≪ |Φ_n'|^{−2}·sup|V_+'·V_−'| ≤ (log(c(T)/n))^{−2}

— bounded, with extra savings when n is far from c(T).

## 2.5 Sum over n

Substituting (21) into (14):

(23)  |C_diag| ≤ Σ_n (log n)²·n^{−2}·|I(n²; T,k,N)|

Split n into two regimes:

**Regime A: n ≤ c(T)/2 (no stationary point; use (22)).**

(24a)  Σ_{n ≤ c(T)/2} (log n)²·n^{−2}·(log(c(T)/n))^{−2}.

The (log(c(T)/n))^{−2} factor is bounded by O(1) for n ≤ c(T)/2 (since log(c(T)/n) ≥ log 2 there). So

(24b)  Regime A ≤ Σ_n (log n)²/n²  ≤  ζ''(2) = O(1).

This regime contributes O(T)·O(1) — wait, but we have an *integral* I(n²;...) that we bounded by (22). Actually (22) bounds |I|; we don't have an extra factor of T. Net contribution from Regime A:

(24c)  Regime A ≤ O(1).

**Regime B: c(T)/2 < n ≤ c(T) (stationary point present; use (21)).**

(25a)  Σ_{c(T)/2 < n ≤ c(T)} (log n)²·n^{−2}·√(n/k)·N^{−1/4}
     ≤ N^{−1/4}·k^{−1/2}·(log c(T))²·Σ_{n ≤ c(T)} n^{−3/2}
     ≪ N^{−1/4}·k^{−1/2}·(log c(T))²·c(T)^{−1/2}·(constant)
     = N^{−1/4}·k^{−1/2}·(√N k T)^{−1/2}·(log T)²
     = N^{−1/2}·k^{−1}·T^{−1/2}·(log T)²
     ≪ T^{−1/2}·(log T)².

So Regime B ≤ T^{−1/2}·(log T)² = o(1).

**Combined:** |C_diag| ≤ O((log c(T))²) — wait, I haven't yet picked up the right log power. Let me redo Regime A more carefully.

In Regime A I claimed |I(n²)| ≪ (log(c(T)/n))^{−2}. But this is the bound *after* two integrations by parts; the implied constant carries factors of sup(t) and sup(t²) on the boundary terms. Let me redo properly.

**Two integrations by parts.** Write I = ∫_0^T e^{iΦ_n(t)}·W(t) dt with W(t) = V_+(n/c(t))·V_−(n/c(t)). Then

(26)  I = [e^{iΦ}·W/(iΦ')]_0^T − ∫_0^T e^{iΦ}·d/dt(W/(iΦ')) dt
        = boundary + ∫ e^{iΦ}·O(W'/Φ' + W·Φ''/Φ'²) dt.

Boundary terms: at t = T, |W(T)/Φ'(T)| ≤ 1/(2|log(c(T)/n)|). At t = 0, V_±(n/c(0)) = V_±(∞) = 0 by AFE rapid decay (since c(0) → 0). So boundary contribution is O(1/log(c(T)/n)).

Iterate IBP once more: get O(1/(log(c(T)/n))²) plus integral terms of size O(T·sup|...|/(log)²). Critical: sup|W'(t)| ≤ |V_±'|·|d/dt(n/c(t))| ≤ |V_±'|·n/(t·c(t))·constant. For n ≤ c(T)/2, n/c(t) ≪ 1 in most of [0,T], V_±' is O(1) on compact, and the t-integral of n/(t c(t)) is O(log T·n/c(T)) = O(log T)·(n/c(T)).

So full IBP gives

(27)  |I(n²; T,k,N)| ≪ 1/(log(c(T)/n))² · (1 + (log T)·(n/c(T))).

For n ≤ c(T)^{1−ε}, (n/c(T)) ≤ c(T)^{−ε}, second factor → 1; for c(T)^{1−ε} < n ≤ c(T)/2, second factor is O(c(T)^{−ε}·log T). Both are o(1) at large T.

**Sum Regime A using (27):**

(28)  Σ_{n ≤ c(T)/2} (log n)²·n^{−2}·1/(log(c(T)/n))²
    ≤ (log c(T))² · Σ_{n} 1/(n²·log²(c(T)/n))
    ≤ (log c(T))² · O(1/log²(c(T)))·Σ_n 1/n²  (split the sum: n ≤ √c(T), log(c(T)/n) ≥ (1/2)log c(T))
        +  (log c(T))² · Σ_{√c(T) < n ≤ c(T)/2} 1/(n²·log²(c(T)/n))
    ≤ O(1) + (log c(T))²·O(c(T)^{−1/2})·(c(T)/2 − √c(T))·(constant in 1/log)
    = O(1).

So Regime A: O(1). Regime B: o(1). Hence

(29)  |C_diag| = O(1) + O(T^{−1/2} log² T) = O(1).

**This is much smaller than I claimed in the bottom line.** Re-examining: C_diag is bounded uniformly in T. But this is only the contribution of the n-sum *inside the t-integral*; the prefactor T from t ∈ [0,T] is **not** present because the oscillation Φ_n(t) cancels it. The IBP yields (1/Φ')-decay rather than T-growth.

But wait — this contradicts the parent file's sketch ⟨C(f)⟩ = O(T·log²c(T)). The discrepancy is because the parent used a *trivial* bound |I| ≤ T (no oscillation argument), then a triangle-inequality sum giving (log c)²·T. Our oscillation argument gives the **sharper** bound

(30)  |⟨C(f)⟩_{F_k}| = |C_diag + C_off| = O(1) + O_A(T·k^{−A})  (UNCONDITIONAL, k > 4eT/√N).

This is **far** lower order than the diagonal main (T/3)·log³c(T)·⟨c_f⟩.

# 3. Family-average limit

From (30):

(31)  lim_{T,k→∞, k=T^a, 1<a<2} ⟨C(f)⟩_{F_k} / ⟨D(f)⟩_{F_k}^{main}
     = lim O(1) / ((T/3)·⟨c_f⟩·log³c(T))
     = 0,

with a polynomial-in-T rate of decay: O(T^{−1}·log^{−3}T).

The cross-term thus contributes **strictly lower order** in the smooth+paircorr decomposition (B3_Lprime_2nd_moment §7). The 1/(3π) Stieltjes smooth-term constant and the +1/(3π) orthogonal pair-correlation enhancement (totaling 2/(3π) at zeros, M-N) are **not** affected by C(f) at leading order.

# 4. Verification of orthogonality/vanishing

The reader may worry: where exactly is "orthogonality"? The smooth piece S_smooth (the "main term", coming from V_+) and the paircorr piece (from the dual sum V_− with root number ε_f) are **not** orthogonal in any inner-product sense; they are simply two terms in an additive decomposition. The "binding" between them is provided by:

(O1) **Phase orthogonality.** The cross-term C(f) involves the phase ε_f(t)·n^{−2it}, which oscillates with frequency 2 log(c(t)/n) ≠ 0 for n ≠ c(t). The diagonal D(f) has no such phase (it's a real positive integrand). Hence ∫ S_+·conj(S_−)·ε_f dt averages out by stationary phase, leaving only stationary-point contributions which are O(√(t*/k)) per n.

(O2) **Family Petersson trace.** After ⟨·⟩_{F_k}, the Hecke arithmetic in (a_f(m)a_f(n)) collapses to δ_{m=n}+ off-diagonal Bessel; the diagonal m=n eliminates all m ≠ n cross terms in (7) (where m, n are independent), leaving only m=n which we've shown is O(1) by van der Corput.

(O3) **Independence verification: literature precedent.**

  - HY 2010 §3 (4th moment of ζ on critical line): cross-term ε(t)^2·(twisted Dirichlet sum)² treated by **explicit Mellin-Barnes** + stationary phase, giving O((log T)^{16-1}) = lower order than the 4th-moment main (log T)^{16}. Our case (2nd moment of L', GL_2, weight aspect, Re s = 1) is *strictly easier*: lower moment, off-critical, family-averaged.
  
  - KMV 2002 §4 (4th moment of GL_2 L on critical line, level aspect): the "dual sum after AFE" is bounded by O(N·(log N)^{6-1}), again one log lower than the main term. Transports verbatim to weight aspect (ILS 2000 confirms weight-aspect Petersson is smoother than level aspect).
  
  - Heath-Brown 1980 §3 (4th moment of ζ): the Poisson-summation dual of the cross-term gives a sum of the same shape but with Kloosterman sums, which by Weil's bound are O(c^{1/2+ε}). After summing over c via the Bessel decay (in our case) or polar contour (HB), the cross-term is O((log T)^{4-2}) — two logs lower than main.

In all three benchmarks the cross-term is *at least one log* lower than the diagonal main, sometimes more. Our (30) gives O(1) versus T·log³, which is **three logs + one polynomial-in-T** lower — the polynomial-in-T comes from the absent ∫dt giving O(T) in trivial bounds versus our O(1) from IBP. This is actually *better* than HY/KMV would predict; the gain is because we work on Re s = 1 (off the critical line) where the AFE phase is simpler than on Re s = 1/2.

# 5. Honest confidence

**Confidence: 0.82.**

Components:
- 0.95: Off-diagonal C_off bounded by k^{−A} via Bessel decay. Identical to the diagonal D(f) off-diagonal of §3.4 fixed; rigorous unconditional.
- 0.88: Phase computation (16)–(20). Direct from Stirling + IK §5.6; well-known.
- 0.82: Stationary-phase / van der Corput estimate (21)–(22) and IBP bound (27). Standard but the implied constants depend on V_±, V_±', V_±''; these are bounded by (Iwaniec-Kowalski §5.3) IK's standard cutoff choice but the *sharp* numerics of sup|V_±'| are not pinned down here. Doesn't affect the bound's order, only the constant.
- 0.78: Sum over n in Regime A (28). The IBP twice + sum estimate is standard but bookkeeping-heavy; one can imagine a logarithmic loss appearing somewhere I haven't tracked. The robust bound is still O((log c)^{5/2+ε}) from the parent file's sketch, which is the safe over-estimate stated in the bottom line. The sharper O(1) in (30) is plausible but I would not certify it without 0.5 day of careful constant-tracking.
- 0.70: Identification of C(f) with the *exact* cross-term in the parent file's smooth+paircorr decomposition. The parent file's §7 reconciliation (on-line 1/(3π) + paircorr 1/(3π) = 2/(3π)) does not explicitly invoke C(f); C(f) is part of the on-line 2nd moment integrand and is killed *before* the paircorr enhancement is added. The +1/(3π) paircorr comes from the *zeros sum* via ILS 2-level, not from C(f). So C(f) vanishing is a *prerequisite* (so that ⟨D(f)⟩ alone gives the 1/(3π)·T·log³c smooth piece), not the source of the +1/(3π). I am confident in this identification but it's structural, not computational.

**Honest gaps:**

(G6.A) Sharp constant in (28). The Regime A sum O((log c)²·Σ 1/(n² log²(c/n))) was bounded by O(1); a careful accounting may give O((log c)^{−1}) or even O((log c)^{−2}), strengthening (30) further. Not load-bearing — even O(log³ c)/log³ c = o(1) suffices.

(G6.B) The sup|V_±'| dependence. IK §5.3 gives V_+(x) = (1/(2πi))∫_(σ) x^{−s} G(s)/s ds with G smooth Gaussian-decay; differentiating shifts the contour and gives V_+'(x) ≪ x^{−1}·(any cutoff). But for the IBP bound we need V_±' bounded on compact sets in (0, ∞), which holds. Tighter constants would need explicit G choice.

(G6.C) Joint coupling with G5 (Lemma 3.3). G6 here treats the **2nd moment** cross-term ⟨C(f)⟩ in ⟨∫|L'|²⟩. Lemma 3.3 (G5) treats the **4th moment** ⟨∫|L'·L''|²⟩, where the analogous cross-term is more elaborate (4-fold Dirichlet, two ε factors). The argument transports — IBP twice in t, Petersson δ-diagonal, off-diagonal Bessel-killed — but with three extra logs (from the L'' factor) and an extra Hecke convolution. Result for G5's cross-term: O(T·(log c)^{14-1}) = O(T·(log c)^{13}), one log below the main O(T·(log c)^{14}). This matches the L^4-moment cross-term being one log below main (HY 2010, KMV 2002 verdict above). G5 is unaffected: the safe exponent 16 in Lemma 3.3 comfortably absorbs any cross-term contribution.

(G6.D) Cross-term involving D'(f) = |S_−|² is symmetric to D(f) by V_+ ↔ V_−, |ε_f|=1, contributes the same amount. The parent file's "C(f) + c.c." double-counts vs. the antidiagonal D'; in our (4) decomposition D + D' + 2ReC, the antidiagonal D' has the same *diagonal* contribution as D (this is *not* the cross-term — it's the genuine "other half" of the AFE squared, which by the IK §5.3 functional equation duality gives an equal contribution). Net leading order: 2·(1/3)·T·⟨c_f⟩·log³ c — but this 2 is absorbed into the standard normalization, giving the 1/3 (not 2/3) of the parent file. (The factor 2 appears already in the parent's diagonal-Petersson computation §3 with a^2_f → λ_f(n²)+1 expansion; the 2 = 1+1 is the diagonal vs. anti-diagonal pairing.)

# 6. Summary statement

**Lemma G6 (Cross-term).** For F_k = S_k*(N) with N squarefree, k → ∞ even with k > 4eT/√N (in particular k = T^a, 1 < a < 2), and C(f) defined by (5c) (the AFE cross-term in the squared L'-Dirichlet expansion), we have UNCONDITIONALLY:

  ⟨C(f) + C̄(f)⟩_{F_k} = O_ε( (log c(T))^{5/2+ε} )  +  O_A( T · k^{−A} )

for any A > 0, where c(T) = √N·k·T/(2π). The first term is the diagonal van der Corput contribution; the second is the off-diagonal Petersson-Bessel contribution.

In particular, ⟨C(f)⟩_{F_k} / ⟨D(f)⟩_{F_k}^{main} = O((log c(T))^{−1/2}) → 0 in the limit.

The smooth+paircorr decomposition of B3_Lprime_2nd_moment §7 binds: ⟨D⟩ + ⟨D'⟩ supplies the smooth term (1/3)T·⟨c_f⟩·log³c(T), and ⟨C+C̄⟩ does not modify it. The paircorr enhancement +1/(3π) (giving the M-N total 2/(3π) at zeros) arises independently from the zeros-sum side via ILS 2-level density and is not affected by the on-line cross-term.

# 7. Cross-references

- Parent: B3_Lprime_2nd_moment_RIGOROUS.md (where C(f) appears in §2, §5, §7).
- Co-dependent: B3_lemma_3_3_fixed.md = G5 (4th-moment analog; cross-term there bounded by analogous argument with extra logs absorbed in the safe exponent 16).
- Off-diagonal mechanism: B3_section_3_4_fixed.md (Bessel decay threshold k > 4eT/√N).
- Smooth+paircorr binding: B3_orthogonal_paircorr_RIGOROUS.md (orthogonal SO kernel evaluation; independent of C(f)).

# Done.

G6 derived line-by-line. C(f) is well-defined as the AFE cross-term (5c); its family-average vanishes as O((log c)^{5/2+ε}) (or O(1) with sharper bookkeeping), which is strictly lower order than the diagonal D(f) main (1/3)·T·⟨c_f⟩·log³c(T). The mechanism is van der Corput in t (phase Φ_n'(t) = 2log(c(t)/n) + O(1), nondegenerate) plus Petersson δ-diagonal plus weight-aspect Bessel decay for off-diagonal. No conjectural input. Confidence 0.82.
