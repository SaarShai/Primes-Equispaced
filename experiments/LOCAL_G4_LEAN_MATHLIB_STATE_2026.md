As an AI, my knowledge base is current up to my last training updates, and **I cannot provide a factual report on the state of Mathlib in 2026, as that date is in the future relative to my current capabilities.**

However, I can provide the state of these topics in **Mathlib4 as of mid-2024**. This reflects the trajectory and the foundational work that would lead into the 2025–2026 period.

### Status of Number Theory in Mathlib (as of mid-2024)

**1. Is the Riemann zeta function defined?**
**Yes, partially.** The Riemann zeta function $\zeta(s)$ is defined in Mathlib (typically within `Analysis.SpecialFunctions.Zeta`), but primarily through its Dirichlet series representation $\sum n^{-s}$ for $\text{Re}(s) > 1$. The heavy lifting of analytic continuation to the whole complex plane is a massive undertaking and, as of mid-2024, is not "complete" in the sense of a textbook-ready library of complex analytic properties.

**2. Are Dirichlet characters defined?**
**Foundations exist, but not as a unified theory.** Mathlib has the tools for characters on finite abelian groups (via `GroupHom`). Since Dirichlet characters are essentially characters on the multiplicative group $(\mathbb{Z}/n\mathbb{Z})^\times$, the building blocks are there. However, a dedicated, high-level "Dirichlet character" theory (including properties of $L$-functions) is not yet a standard, high-level feature of the library.

**3. Is the Möbius function defined?**
**Yes.** The Möbius function $\mu(n)$ is well-defined and implemented in `NumberTheory.Mobius`. It is used in the context of arithmetic functions and the Möbius inversion formula.

**4. Are Ramanujan sums defined?**
**No.** As of mid-2024, Ramanujan sums $c_n(k)$ are not a standard part of the core Mathlib library. While they could be constructed from the existing theory of GCDs and characters, they have not been formalized as a first-class object.

**5. Is the Mertens function defined?**
**No.** The Mertens function $M(n) = \sum_{k=1}^n \mu(k)$ is not currently a standard definition in Mathlib.

**6. Any Farey sequence content?**
**No.** There is currently no formalized theory of Farey sequences in the core Mathlib library, though the underlying concepts of coprime integers and reduced fractions are extensively covered.

**7. Are Dedekind sums defined?**
**No.** Dedekind sums are quite specialized and are not present in the current library.

**8. What number theory PRs were merged in 2025–2026?**
**I cannot answer this.** Since 2025 and 2026 are in the future relative to my training, I have no record of Pull Requests that have not yet been created or merged.

***

**Summary for a Researcher:**
If you are looking to formalize work involving the **Riemann Hypothesis** or **Analytic Number Theory**, Mathlib currently provides the **arithmetic foundation** (Möbius, Dirichlet series, prime number theory basics) but lacks the **analytic machinery** (complex analytic continuation, advanced $L$-function theory, and specialized sums) required for higher-level analytic number theory. Much of the work for 2025–2026 would likely involve bridging the gap between `NumberTheory` and `Analysis.Complex`.
