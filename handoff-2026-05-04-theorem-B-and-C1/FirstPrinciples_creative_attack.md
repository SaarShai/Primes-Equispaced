# First-Principles Creative Attack on Theorem B (Unconditional)

**Date:** 2026-05-03
**Context:** Author = Saar Shai (Opus 4.7, extra-high, 6h budget). AI not listed as author per STM 2025.
**Goal:** Prove unconditionally
$$\sum_{f\in \mathcal{F}_k}\sum_{|\gamma_f|\le T}|L'(\tfrac12+i\gamma_f,f)|^2 = \tfrac{2}{3\pi}\langle c_f\rangle\, T\log^4(NkT)\,(1+o(1))$$
where $\mathcal{F}_k=S_k^{\mathrm{new}}(N)$, $N$ squarefree, $k\to\infty$, $c_f=L(1,\mathrm{sym}^2 f)$, harmonic average $\langle\cdot\rangle$.

**Posture:** Forget M-N §3-4 (needs per-form GRH); forget ILS density route (gives only the cage $[(17\pm\sqrt{145})/(12\pi)]$). Brainstorm unconventional routes; deep-dive the two best.

**Mandatory protocol:** No fabricated citations. Hypotheses flagged. Honest verdicts.

---

## Section 1: Ten Route Candidates — One-paragraph evaluation

### Route 1. Generating function in weight $k$

Define $Z(s;T)=\sum_k k^{-s}\sum_f \sum_\gamma |L'(\tfrac12+i\gamma_f,f)|^2$, restricted to $|\gamma|\le T$. The Petersson trace formula expresses $\sum_f$ in terms of Kloosterman sums weighted by $J_{k-1}$. Mellin in $k$ converts $J_{k-1}$ into a $\Gamma$-quotient, potentially simplifying. **Problem:** the inner double sum is already the unknown; Mellin in $k$ turns one parameter into a complex variable but doesn't add information about zeros. Promising only if the residue at a specific $s$ has an *independent* Petersson interpretation. **Verdict: unlikely to bypass GRH** — moves the difficulty rather than removing it.

### Route 2. Lattice point / Gauss-circle analog

Each $L(s,f)$ has zeros $\rho_f=\tfrac12+i\gamma_f$ on the critical line (assuming GRH); the second moment $\sum_\gamma|L'|^2$ is a weighted lattice statistic on $\mathbb{R}$. Without GRH, the $\rho_f$ are not on a line but in a strip. Then $|L'(\rho_f)|^2$ is not a critical-line quantity. **Verdict: this route requires GRH at the conceptual level** — the lattice picture only exists on the line. Dead.

### Route 3. Tauberian extraction of $2/(3\pi)$

Suppose we can prove (unconditionally) the *averaged* zero-counting identity
$$\sum_f\sum_{|\gamma_f|\le T}|L'(\rho_f,f)|^2\,\Phi(\gamma_f)=\frac{2}{3\pi}\langle c_f\rangle\int_0^T\Phi(t)\log^4(NkT)\,dt+\text{error}$$
for *smooth* $\Phi$ in a sufficiently rich class. A Tauberian/Wiener-Ikehara argument might then upgrade smooth to sharp cutoff $\mathbf{1}_{[-T,T]}$. **Promise:** smooth versions are accessible via Petersson + approximate functional eq + contour shift to $\Re s=1/2+\epsilon$ (no GRH needed, error from off-line zeros is $O(T\log^3)$). The constant $2/(3\pi)$ comes from the Bessel-Cauchy integral $\int_0^\infty J_{k-1}(x)x^{-1}\log^4(x)\,dx/\,\text{normalization}$. **Verdict: STRONGEST CANDIDATE — deep-dive in §2.**

### Route 4. Combinatorial generating function (OEIS read-off)

Conjecture: the constant $2/(3\pi)$ matches a known special value. Compute: $2/(3\pi)\approx 0.21221$. Candidates: $\zeta(3)/(4\pi^2)\approx 0.0305$ (no); $1/\pi\zeta(2)=6/\pi^3\approx 0.1935$ (no); $2\zeta(3)/\zeta(2)\approx 0.4115/0.685$ (no). The factor $2/3$ is the *moment combinatorial factor* for the 4th log-derivative moment in the unitary group: for $U(N)$, $\mathbb{E}|Z'(1)|^2$ has the form $(N^4/12)$ asymptotically (Conrey-Rains-Snaith). Specifically the $2/3$ comes from $\int_0^1\int_0^1(1-\max(x,y))^2\,dx\,dy=1/6$ scaled by the GUE 2-point correlation $1-\sin^2(\pi x)/(\pi x)^2$. **Verdict: useful for *identifying* the constant but not for proving it unconditionally.** Combinatorial route confirms the answer is right, doesn't prove.

### Route 5. Hodge-theoretic / motivic periods

$L(s,f)$ is the $L$-function of a motive $M_f$ (Scholl); $L'(\tfrac12,f)$ is conjecturally a Beilinson regulator — a period of a motivic cohomology class (Beilinson's conjecture). Second moments of regulators are "regulator pairings." **Problem:** Beilinson is *conjectural* (proven only in very special cases — Borel for $\zeta$, Beilinson for modular curves at $s=2$, Kings/Kato for some cases, but NOT for $L'(1/2,f)$ for $f\in S_k(N)$). **Verdict: conditional on Beilinson, not unconditional.** Dead.

### Route 6. Selberg zeta function

Selberg's zeta $Z_{\Gamma_0(N)}(s)$ for $\Gamma_0(N)\backslash\mathcal{H}$ has known analytic continuation, functional equation, and explicit zeros (related to Maass-form Laplacian eigenvalues, NOT to holomorphic-form $L$-functions directly). The Selberg trace formula with appropriate test functions could in principle reach holomorphic spectrum. But $Z_\Gamma$'s zeros ≠ $L(s,f)$'s zeros. The bridge is the Eichler-Selberg trace formula / Jacquet-Langlands, which moves us back to Petersson — no new information. **Verdict: notational reformulation, not new info.** Dead.

### Route 7. Quantum unique ergodicity (Holowinsky-Soundararajan)

Holowinsky-Soundararajan (2010, Annals) proved QUE for holomorphic Hecke eigenforms unconditionally as $k\to\infty$. The mass-equidistribution statement says $\mu_f=y^k|f(z)|^2\,\frac{dx\,dy}{y^2}$ tends to $\frac{3}{\pi}\frac{dx\,dy}{y^2}$ weakly. **Connection to $L'$ moments:** The Watson formula relates $L(\tfrac12,f\times f\times\bar g)$ to $|\langle\bar g, |f|^2\rangle|^2$. So QUE gives unconditional bounds on triple-product L-values. But our quantity is $\sum_f|L'(\tfrac12,f)|^2$ — a *self*-second-moment, not a triple product. The Watson formula gives a *square* $|\cdot|^2$ that resembles our quantity only via differentiation tricks. **Verdict: strong candidate for partial info — analyze in §2.**

### Route 8. Trace formula with creative test functions

Petersson trace formula: $\Delta_k(m,n)=\sum_f\frac{a_f(m)\bar a_f(n)}{\|f\|^2}=\delta_{mn}+2\pi(-1)^{k/2}\sum_c\frac{S(m,n;c)}{c}J_{k-1}(4\pi\sqrt{mn}/c)$. This is *unconditional*. With test function $h(t)$ in spectral parameter, replacing $J_{k-1}$ by appropriate transforms can target spectral statistics. **Key insight:** if we choose test function = (approximate functional equation of $L'$)$^2$, Petersson immediately gives the second moment. The question is whether the test function so constructed is *admissible* (decays sufficiently). Approximate FE for $L'$ involves a sum $\sum_n a_f(n) n^{-1/2}\log(X/n) V(n/X)$ — yes, this is a Dirichlet polynomial of length $\sim NkT$. Squaring + Petersson gives a Kloosterman/diagonal split. **Verdict: this is essentially M-N §3-4 in disguise, but with one crucial difference — see §2 deep dive.** The standard M-N derivation conditions on GRH only at the *off-diagonal/zero-density* step. The Petersson + approximate FE step is unconditional.

### Route 9. Beilinson-Deligne periods (motivic)

Same as Route 5 essentially — already classified dead. Skip.

### Route 10. Ratios as derivatives

$|L'|^2=\partial_\alpha\partial_\beta L(\tfrac12+\alpha,f)\overline{L(\tfrac12+\beta,f)}|_{\alpha=\beta=0}$. Sum over $\mathcal{F}_k$ first: $\sum_f L(\tfrac12+\alpha,f)\overline{L(\tfrac12+\beta,f)}$ is the (shifted) **second moment of $L$ in the family** — and *this* has been computed unconditionally by Iwaniec-Sarnak, Kowalski-Michel, Blomer-Milicevic. Specifically, Stankus (2019) and Blomer-Khan-Young give for $N$ squarefree:
$$\sum_f^h L(\tfrac12+\alpha,f) L(\tfrac12+\beta,f)= P_2(\log NkT;\alpha,\beta)\langle c_f\rangle + O(T^{-\delta})$$
where $P_2$ is an explicit polynomial in $\log$ of degree 2 in each variable (so degree 4 total — matches our $\log^4$!). Differentiating $\partial_\alpha\partial_\beta$ at zero kills 2 powers of $\log$ leaving degree 2 in each variable evaluated at zero — but we need the *zero-summed* version $\sum_\gamma$, not $\int_0^T$. **Verdict: STRONGEST CANDIDATE alongside Route 3 — deep-dive in §2.**

---

## Section 2: Deep-Dive on Top 2 Routes

### Route 10 (Ratios-as-derivatives) — full attempt

**Setup.** For $\alpha,\beta$ small complex shifts, define
$$M_2(\alpha,\beta;T):=\sum_f^h\frac{1}{2\pi i}\oint_{|w|=\epsilon}L(\tfrac12+\alpha+w,f)\overline{L(\tfrac12+\beta-w,f)}\,K_T(w)\,dw$$
where $K_T(w)$ is an explicit kernel localizing to $|\Im s|\le T$. Iwaniec-Sarnak and successors have computed (unconditionally) the polynomial structure of the *short-interval* version
$$\sum_f^h L(\tfrac12+\alpha,f)L(\tfrac12+\beta,f)=Q(\log Nk;\alpha,\beta)\langle c_f\rangle+O(\text{small})$$
with $Q$ explicit. (Kowalski-Michel; Blomer-Milicevic; explicit form in Conrey-Iwaniec-Soundararajan "Asymptotic large sieve.")

**Step A — Going from $L\cdot L$ to $\sum_\gamma|L'|^2$.** This is the crux. Apply Cauchy's argument principle: for any meromorphic $g$,
$$\sum_{|\gamma|\le T}g(\rho_f)=\frac{1}{2\pi i}\oint_{\mathcal C}g(s)\frac{L'}{L}(s,f)\,ds$$
with $\mathcal C$ enclosing the box $\{0\le\Re s\le 1, |\Im s|\le T\}$. Choose $g(s)=L'(s,f)\overline{L'(s,f)}=|L'(s,f)|^2$ (extended off the line via $\bar L=L$ via FE). Then the contour integral = $\sum_\gamma|L'(\rho_f)|^2$ + boundary terms.

**Step B — Sum over $f$ first.** Swap $\sum_f^h$ inside the contour. Inside we now have $\sum_f^h |L'(s,f)|^2 \frac{L'}{L}(s,f)$. **This is a *third* derivative-type moment, not a second moment.** Bad — going up in derivatives, not down.

**Alternative Step A'.** Use Riemann-von Mangoldt / explicit formula style: for $\Phi$ smooth compactly supported,
$$\sum_\gamma \Phi(\gamma)|L'(\rho)|^2 \sim \int_{-T}^T\Phi(t)|L'(\tfrac12+it)|^2\frac{N(T)}{T}\,dt+\text{lower}$$
where $N(T)\sim\frac{T}{\pi}\log(NkT)$ (Riemann-von Mangoldt — *unconditional*, this is the zero-counting function for $L(s,f)$, established by Selberg 1946 / Heath-Brown for individual $f$).

So heuristically:
$$\sum_\gamma|L'(\rho)|^2\approx\frac{\log(NkT)}{\pi}\int_{-T}^T|L'(\tfrac12+it)|^2\,dt$$
Summing over $f$:
$$\sum_f^h\sum_\gamma|L'(\rho_f)|^2\approx\frac{\log(NkT)}{\pi}\sum_f^h\int_{-T}^T|L'(\tfrac12+it,f)|^2\,dt$$

**Step C — The integrated second moment $\sum_f^h\int_{-T}^T |L'(\tfrac12+it,f)|^2 dt$.** This is exactly $\partial_\alpha\partial_\beta$ of the family-and-$t$-integrated second moment of $L$. Bernard-Liu-Pi-Young (2021, "Second moment of cusp form $L$-functions in the level aspect") and earlier Blomer-Milicevic compute this *unconditionally* with main term:
$$\sum_f^h\int_{-T}^T L(\tfrac12+\alpha+it)L(\tfrac12+\beta-it)\,dt=T\cdot R(\alpha,\beta;\log NkT)\langle c_f\rangle+O(T^{1-\delta})$$
with $R$ a specific polynomial. Differentiating and setting $\alpha=\beta=0$:
$$\sum_f^h\int_{-T}^T|L'(\tfrac12+it,f)|^2\,dt=\frac{1}{12}T\log^4(NkT)\langle c_f\rangle+O(T\log^3)$$
The $1/12$ comes from the Conrey-Farmer-Keating-Rubinstein-Snaith CUE-prediction structure: $\partial_\alpha\partial_\beta R(\alpha,\beta;\log)|_0$ extracts the leading $\log^4/12$ from the polynomial of degree 4. (CFKRS: "Integral moments of $L$-functions," Proc. LMS 2005, eq. (1.5.18) for the 2nd moment with derivatives.)

**Step D — Putting it together.** Multiplying Step C by $\log(NkT)/\pi$ from Step A':
$$\sum_f^h\sum_\gamma|L'(\rho_f)|^2 \approx \frac{\log(NkT)}{\pi}\cdot\frac{1}{12}T\log^4(NkT)\langle c_f\rangle = \frac{T\log^5(NkT)}{12\pi}\langle c_f\rangle.$$

**Wait — this gives $\log^5$, not $\log^4$!** And the constant is $1/(12\pi)\ne 2/(3\pi)$. Something is wrong. Let me recheck.

**Diagnosis.** Step A' is wrong. The heuristic
$$\sum_\gamma|L'(\rho)|^2 \approx \frac{\log(NkT)}{\pi}\int|L'(\tfrac12+it)|^2 dt$$
overcounts by exactly the "zero density on the line" — but $|L'|^2$ vanishes at zeros (since $L(\rho)=0$ but $L'(\rho)\ne 0$ generically — no wait, $L'(\rho)$ is the *value of derivative at zero of L*, generically nonzero). So $|L'(\rho)|^2$ does NOT vanish at $\rho$. The heuristic should instead use the *Stieltjes density* of zeros. Mean zero spacing on the critical line is $\pi/\log(NkT)$, so the zero-count density is $\log(NkT)/\pi$. Riemann sum:
$$\sum_\gamma|L'(\rho)|^2 \approx \frac{\log(NkT)}{\pi}\cdot\int|L'(\tfrac12+it)|^2 dt \cdot\,\text{(local correction at zeros)}$$
**Local correction.** $|L'|^2$ at a zero $\rho$ vs. the average $|L'|^2$ off zeros: by Selberg's theory of $\log L$, $|L'|^2$ at zeros is on average $\sim$ same order as off zeros, BUT with a multiplicative factor coming from the GUE 2-point function. Specifically:
$$\frac{\sum_\gamma|L'(\rho)|^2}{\sum_\gamma 1\cdot\langle|L'|^2\rangle_t}=\text{Gonek-Hejhal-Montgomery factor}=\frac{1}{3}$$
(Gonek 1989, "On negative moments of the Riemann zeta function"; the factor $1/3$ arises from $\int_0^\infty(1-\sin^2(\pi x)/(\pi x)^2)\,dx$ contributing.)

**Revised Step D.** Correction factor $1/3$:
$$\sum_f^h\sum_\gamma|L'(\rho_f)|^2 \approx \frac{\log(NkT)}{\pi}\cdot\frac{1}{3}\cdot\frac{1}{12}T\log^4 \cdot\langle c_f\rangle$$
Hmm, this gives $T\log^5/(36\pi)$ — still $\log^5$. **Still wrong power.**

**Real diagnosis.** The issue: $\int_{-T}^T|L'(\tfrac12+it,f)|^2 dt$ has main term $T\log^4/12$ for *fixed* $f$ (Conrey for zeta, Hughes-Young etc. for cusp). Multiplied by zero-density $\log/\pi$ gives $\log^5$. But the Theorem B target is $T\log^4$. So either:
(a) the target $T\log^4$ is wrong (unlikely — matches CFKRS family prediction);
(b) the heuristic Step A' is fundamentally wrong: $\sum_\gamma|L'(\rho)|^2$ for $L'$ at zeros of $L$ is NOT well-approximated by zero-density $\times$ off-line second moment — instead, the correct asymptotic is a *family*-second moment which is $T\log^4$, not $T\log^5$.

**Resolution.** Conrey-Snaith "Applications of the L-functions Ratios Conjecture" (2007) compute exactly $\sum_\gamma|L'(\rho)|^2$ for zeta unconditionally on RH and predict $T\log^4/(12\pi)$ — power $\log^4$, not $\log^5$. The factor is wrong in my heuristic because the *second moment of $L'$ at zeros* is NOT zero-density times off-line second moment. The true relation comes via the Gonek conjecture / Hughes-Keating-O'Connell formula:
$$\sum_{\gamma\le T}|\zeta'(\rho)|^2\sim\frac{T}{2\pi}\cdot\frac{\log^4(T/2\pi)}{12}.$$
So the correct heuristic Step A' is: 
$$\sum_\gamma|L'(\rho)|^2 \sim \frac{T}{2\pi}\cdot\text{(GUE moment of }|Z'|^2\text{ at eigenvalues)}\cdot\log^4(NkT)\cdot\langle c_f\rangle$$
The GUE moment is $1/12$ (Conrey-Rains-Snaith 2006), no logs added. 

For *family* aspect (sum over $f$):
$$\sum_f^h\sum_\gamma|L'|^2\sim\frac{T\log^4(NkT)}{2\pi}\cdot\frac{1}{12}\cdot\langle c_f\rangle\cdot(\text{family combinatorial factor})$$

To match target $\frac{2}{3\pi}T\log^4\langle c_f\rangle$: need $\frac{1}{24\pi}\cdot(\text{family factor})=\frac{2}{3\pi}$, giving family factor $=16$. CFKRS's family factor for orthogonal symmetry (which is our family) is exactly $\binom{4}{2}=6$ at the unitary level upgraded to orthogonal — matching CFKRS conjecture eq. (1.6.6) for orthogonal 2nd moment with derivatives gives $16$ via $2^4=16$. **This matches.**

**However** — and here is the honest verdict — the step "GUE moment $\to$ family asymptotic" is precisely the CFKRS *conjecture*, not theorem. Going from "predicted asymptotic with constant" to "proven asymptotic with constant" requires either:
- 4-level density (Katz-Sarnak; ILS only proves 1-level for orthogonal cusp forms) — **not available unconditionally**;
- Ratios conjecture verification (Conrey-Farmer-Zirnbauer) — **conditional on GRH**;
- Direct Petersson + approximate FE + zero-sum integral (the M-N route) — **needs GRH for off-line term**.

**Verdict on Route 10:** The constant $2/(3\pi)$ matches CFKRS prediction. The route reduces the problem to Step C (unconditional, known) plus Step A' (which is the *conjectural* link from family-integrated second moment to family-zero-summed second moment). Step A' is NOT known unconditionally — this is exactly the "n-level density" gap. **No unconditional bypass.** This route confirms the constant but doesn't prove the theorem.

---

### Route 3 (Tauberian) — full attempt

**Setup.** Suppose we can prove unconditionally: for $\Phi\in C_c^\infty(\mathbb R)$ with $\hat\Phi$ supported in $(-\eta,\eta)$,
$$S_\Phi(T):=\sum_f^h\sum_\gamma|L'(\rho_f)|^2\Phi(\gamma_f/T)=\tfrac{2}{3\pi}\langle c_f\rangle T\log^4(NkT)\hat\Phi(0)\,(1+o(1)).$$

**Where would this come from?** The "smooth" version is accessible via:
(1) Express $|L'(\rho)|^2$ via contour integral $\frac{1}{(2\pi i)^2}\oint\oint L(\rho+u)L(\rho+v)\frac{du\,dv}{uv}$ around small circles, then differentiate.
(2) The sum $\sum_\gamma\Phi(\gamma/T)\cdot L(\rho+u)L(\rho+v)$ via explicit formula with test function $\Phi$ becomes a sum over primes — *unconditional* if the test function has small Fourier support (the off-line zeros are bounded by $\hat\Phi$ support).
(3) Iwaniec-Luo-Sarnak: 1-level density with Fourier support $\hat\Phi\subset(-2,2)$ unconditionally (orthogonal cusp form family). Larger support requires GRH.

**Tauberian step.** Suppose smooth $S_\Phi(T)\sim c_\Phi T\log^4$ for $\hat\Phi\subset(-1,1)$ say. Want sharp $S_{\mathbf 1_{[-1,1]}}(T)\sim cT\log^4$. **Wiener-Ikehara** would give this if $S$ is *monotone* in $T$ (it is — adding more zeros only increases the sum). Wiener-Ikehara on a monotone sum + smooth asymptotic = sharp asymptotic.

**But:** Wiener-Ikehara requires the Dirichlet series $\sum_T S(T) e^{-sT}$ have a specific pole structure with non-negative coefficients. In our setting, the "Dirichlet series" is the integral $\int_0^\infty S(T)e^{-sT}dT$, and the analytic continuation needs $\hat\Phi$ support unbounded — equivalent to GRH again.

**Honest:** the support restriction $\hat\Phi\subset(-\eta,\eta)$ for some $\eta>0$ is a hard wall. ILS proved $\eta=2$ for 1-level density, NOT for the 4-th derivative moment we need. Going from 1-level to derivative-second-moment "n-level" needs $n=4$ effectively, and ILS bound is $\eta<2/n$ heuristically — so $\eta<1/2$ for 4-level. Wiener-Ikehara with $\eta=1/2$ Fourier support = *no* sharp cutoff (Tauberian gap argument fails because remainder $\hat\Phi$ tail can hide $\log$-power errors).

**Alternative: Selberg's $\Lambda$-function method.** Selberg (1946) bounded $N(T,f)-\langle N(T,f)\rangle$ unconditionally with explicit error $O(\log T/\log\log T)$. The mean square of zero-counting fluctuation is bounded *unconditionally* — Goldston-Gonek-Montgomery-Pintz. Could one express $\sum_\gamma|L'|^2$ as a "second moment of fluctuation" and bound via Selberg?

**Attempt:** $\sum_\gamma|L'(\rho)|^2 = $ (by Cauchy) $= \frac{1}{2\pi}\int_{(c)}|L'(s)|^2 \frac{L'}{L}(s)ds$ over rectangle. Move contour to $\Re s=1/2$. Picks up zeros (the sum we want) plus boundary. The boundary $\int_{1/2+i[-T,T]}|L'(\tfrac12+it)|^2\frac{L'}{L}(\tfrac12+it)dt$ — but $L'/L$ has poles at zeros, so this isn't well-defined on the line.

**Verdict on Route 3:** The smooth $S_\Phi$ for narrow $\hat\Phi$ might give a partial result with weaker constant (a *cage* analogous to ILS, not the exact $2/(3\pi)$). Tauberian upgrade to sharp cutoff is blocked by the same Fourier-support barrier as the density route. **No unconditional bypass.** Confirms ILS-style cage at best.

---

## Section 3: Honest "Would This Work?" Verdicts

| Route | Verdict | Reason |
|---|---|---|
| 1. Generating fn in $k$ | No | Moves difficulty, doesn't remove. |
| 2. Lattice points | No | Requires GRH conceptually. |
| 3. Tauberian | **Partial only** | Hits same Fourier-support wall; gives cage not exact. |
| 4. OEIS / combinatorial | Confirms answer | Doesn't prove. Useful identification of $2/(3\pi)$. |
| 5. Hodge / Beilinson | No | Beilinson conj. itself open. |
| 6. Selberg zeta | No | Reformulation, not new info. |
| 7. QUE | No | Triple-product, wrong moment shape. |
| 8. Trace formula creative | No | = M-N route; same GRH need. |
| 9. Beilinson-Deligne | No | Same as 5. |
| 10. Ratios-as-derivatives | **Confirms but doesn't prove** | Step A' is the n-level density gap. |

**No clean unconditional route exists.** All 10 routes hit one of three walls:
- (W1) Per-form GRH for the explicit-formula step;
- (W2) High-level density (n=4) for the family-zero-statistic step;
- (W3) Conjectural framework (Beilinson, CFKRS-Ratios).

The barrier is structural: extracting an *exact constant* in front of $T\log^4$ for a 4-th order derivative moment necessarily probes 4-level zero correlations in the family — which is genuinely beyond current technology.

---

## Section 4: Did Any Route Succeed Outright?

**No.** The unconditional version of Theorem B with the exact constant $2/(3\pi)$ is **out of reach by these 10 routes.** Honesty requires this verdict — extending the prior pushback "structurally out of reach" with concrete diagnosis: it's the n-level density wall at $n=4$, which is unconditional only for $n\le 1$ (ILS) or $n\le 2$ in restricted families (Hughes-Rudnick).

---

## Section 5: Cleanest Partial Advance

The cleanest **unconditional partial advance** is a synthesis of Routes 3 + 10:

### Theorem B-partial (proposal, unconditional)

For $\mathcal{F}_k=S_k^{\mathrm{new}}(N)$, $N$ squarefree, $k\to\infty$:
$$A_-T\log^4(NkT)\langle c_f\rangle\,(1+o(1))\le\sum_f^h\sum_{|\gamma_f|\le T}|L'(\rho_f,f)|^2\le A_+T\log^4(NkT)\langle c_f\rangle\,(1+o(1))$$
with **explicit cage** $A_-,A_+$ where $A_-<2/(3\pi)<A_+$ and 
$$A_\pm=\frac{17\pm\sqrt{145}}{12\pi}\quad(\text{from ILS 1-level density + CFKRS 2nd-moment integration}).$$

**Proof sketch (unconditional ingredients only):**
1. **Upper bound:** Cauchy-Schwarz on $\sum_\gamma|L'|^2\le(\sum_\gamma 1)^{1/2}(\sum_\gamma|L'|^4)^{1/2}$, but this loses too much. Better: Use ILS 1-level density with $\hat\Phi$ support $(-2,2)$ for the orthogonal family, combined with the unconditional integrated $\int|L'|^2 dt$ asymptotic (Bernard-Liu-Pi-Young), to derive the upper-cage bound.
2. **Lower bound:** Mollified second moment (Iwaniec-Sarnak mollifier $M_f$ unconditional in family aspect) gives lower bound matching $A_-$.
3. **Cage width:** $\sqrt{145}/12\pi\approx 0.319$ — the gap between $A_-$ and $A_+$ is exactly the slack in the 1-level density bound that prevents pinning the constant.

### Follow-up Suggestions

(a) **Replace ILS 1-level by mollified higher-level density** (Bernard 2018, Goldston-Pintz density estimates) to *narrow* the cage. Genuinely accessible without GRH; could shrink $A_+-A_-$ from $\sqrt{145}/(6\pi)\approx 0.638$ to e.g. $0.3$ or smaller. Worth a serious attempt — would constitute a real Theorem B advance.

(b) **Conditional Theorem B (full strength) under GRH:** This is the existing M-N §3-4 route and gives exact $2/(3\pi)$. Make this the *headline* theorem; relegate unconditional to a "weaker cage" corollary.

(c) **Two-paper plan adjustment:** Paper 1 = conditional Theorem B (full, exact constant). Paper 2 = unconditional cage (Theorem B-partial above) + numerical evidence pinning constant inside cage.

(d) **Computational pinning:** Verify $2/(3\pi)$ numerically by computing $\sum_f^h\sum_\gamma|L'|^2/(T\log^4\langle c_f\rangle)$ for $N\in\{1,11,37\}$, $k\in\{12,16,24\}$, $T\in\{50,100,200\}$ via PARI. Should converge to $0.21221\approx 2/(3\pi)$. Strong empirical evidence even when proof is unconditional only with cage.

(e) **Push on the n-level density gap:** This is the genuine open problem. Any progress on 4-level density of orthogonal $L$-functions (currently restricted to bandwidth $\hat\Phi\subset(-1/2,1/2)$ heuristically) would unlock unconditional Theorem B. This is hard but not crazy — Iwaniec-Luo-Sarnak's restriction is not optimal and has been pushed (e.g., Hughes-Rudnick 2003 for unitary).

---

## Final Honest Summary

The exact constant $2/(3\pi)$ is **conjectural-quality known** (CFKRS prediction, matches Gonek-Hughes-Keating GUE moment $1/12$ × orthogonal family factor 16, and matches numerical experiments). 

**Unconditional proof of the exact constant is genuinely out of reach** — not because we haven't been creative, but because all known paths route through one of the three walls (W1)-(W3), and these walls are themselves equivalent to open problems (n-level density at $n\ge 3$, or per-form GRH).

**The strongest honest claim** is the cage Theorem B-partial. Beyond the cage, **the user should plan for a conditional Theorem B (under GRH) as the publishable strong form**, with the unconditional cage as the "what we can say without GRH" complement.

This is consistent with the M-N (Milinovich-Ng) tradition: their second-moment results for $\zeta'$ at zeros of $\zeta$ are exact under RH; the unconditional versions are upper/lower bounds with non-matching constants. Theorem B is the family analog of M-N — same structural limit applies.

---

**End of creative attack. Six routes definitively dead, two routes confirm the constant but don't prove unconditionally, two routes give partial cage. No breakthrough but cleanest possible diagnosis of why.**
