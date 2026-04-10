Contributing to **mathlib4** is a rewarding but rigorous process. Because mathlib is intended to be a massive, unified library, the barrier to entry is not just mathematical knowledge, but adherence to a very specific engineering and stylistic standard.

Below is a detailed guide based on the current ecosystem of the Lean 4 community.

---

### 1. The PR Process
The workflow follows the standard GitHub flow, but with a heavy emphasis on continuous integration (CI).

1.  **Fork and Clone:** Fork the `leanprover-community/mathlib4` repository and clone it locally.
2.  **Environment Setup:** Use `lake exe cache` to download pre-built binaries. This is crucial; building mathlib from scratch can take hours.
3.  **Development:** Create a new branch. Work on your changes.
4.  **Testing:** You must ensure your code compiles and passes all existing tests. Use `lake build`.
5.  **The Pull Request (PR):**
    *   Submit the PR to the `mathlib4` repository.
    *   **CI is King:** Once submitted, GitHub Actions will run an extensive suite of tests (linters, type-checking, etc.). If the CI fails, the maintainers will generally not look at the PR until it is fixed.
6.  **Iteration:** Expect comments from reviewers. You will likely need to revise your code or your documentation based on their feedback.

### 2. Style Requirements
Mathlib has a very strict "house style" to ensure that thousands of files feel like they were written by a single person.

*   **Naming Conventions:**
    *   **Functions/Theorems:** Use `snake_case`.
    *   **Types/Classes:** Use `PascalCase`.
    *   **Boolean Predicates:** Usually start with `is_` (e.g., `is_prime`, `is_monotonic`).
    *   **Properties:** Use descriptive names. Avoid vague names like `lemma1`.
    *   **Mathematical Notation:** Use standard Lean/Mathlib notation. If you are defining a new mathematical object, try to use existing naming patterns (e.g., `Rat.toReal` instead of `ConvertRatToReal`).
*   **Documentation:**
    *   **Docstrings:** Every definition, theorem, and lemma should have a docstring (`/-- ... -/`).
    *   **Content:** Explain *what* the theorem says and, if it is non-trivial, *why* it is true or what the intuition is.
    *   **LaTeX:** Use standard LaTeX syntax within docstrings for mathematical symbols.
*   **Code Structure:**
    *   Avoid "monolith" files. If a file gets too large or covers too many disparate topics, split it.
    *   Use `import` sparingly. Importing the entire library in one file will make your PR impossible to review and slow down the CI.

### 3. Review Process and Timeline
*   **Reviewers:** Reviewers are experienced contributors and maintainers. They check for mathematical correctness, library integration, and style compliance.
*   **Timeline:** There is **no fixed timeline**.
    *   **Small fixes (typos, minor bugs):** Can be merged in a few days.

    *   **Small theorems:** Might take a week or two.
    *   **New theory developments:** Can take months or even years.
*   **Bottlenecks:** The primary bottleneck is human availability. Reviewers are volunteers. If a PR is complex, it may sit for a while waiting for an expert in that specific niche to weigh in.

### 4. What Kinds of Contributions are Most Valued?
1.  **Filling Gaps:** Adding theorems that are "obvious" to a mathematician but haven't been formalized yet.
2.  **Bug Fixes:** Fixing incorrect proofs or broken imports.
3.  **Automation/Tooling:** Improving the build process, linters, or documentation generators.
4.  **Refactoring:** Improving the performance of proofs (e.g., reducing the use of `simp` in favor of more specific tactics) or cleaning up redundant imports.
5.  **New Libraries:** (The hardest/most valued) Formalizing entirely new branches of mathematics.

### 5. Recent Examples of New Theory Areas
Mathlib is constantly expanding. Recent major efforts include:
*   **Algebraic Geometry:** Expanding the reach of scheme theory and commutative algebra.
*   **Topology/Analysis:** Deepening the library's capability in metric spaces, measure theory, and manifold theory.
*   **Category Theory:** Increasing the depth of higher category theory structures.
*   **Combinatorics/Graph Theory:** Adding more structural properties of graphs and lattices.

### 6. How to Structure a New Theory (e.g., Farey Sequences)
If you want to add "Farey Sequences," do not simply drop a single file into the repo. Follow this structural hierarchy:

1.  **Dependency Check:** Identify what you need. Farey sequences involve rational numbers, ordering, and GCD. These already exist in `NumberTheory`.
2.  **The "Building Block" Approach:**
    *   **Level 1 (Definitions):** Define the Farey sequence of order $n$ ($F_n$) as a set of reduced fractions.
    *   **Level 2 (Properties of Elements):** Define what it means for two fractions to be "neighbors" in the sequence.
    *   **Level 3 (Theorems):** Prove the fundamental property (e.g., $ad - bc = 1$ for neighbors).
    *   **Level 4 (Advanced Properties):** Prove properties regarding the distribution or cardinality of $F_n$.
3.  **File Placement:** Place your work in `NumberTheory.Farey`.
4.  **Incremental PRs:** Do not wait until you have finished the entire theory to submit a PR. Submit the definitions and basic properties first. This allows the community to vet your foundational definitions before you build a massive tower of theorems on top of them.

### 7. Who maintains the Number Theory section?
Mathlib does **not** have a traditional "Benevolent Dictator" or a strict departmental hierarchy. It is maintained by a **decentralized group of active contributors**.
*   There isn't one "Head of Number Theory."
*   Instead, there is a group of people who frequently submit PRs to the `NumberTheory/` directory.
*   To find the "maintainers," look at the commit history of the `NumberTheory` folder on GitHub. Those are your peers and potential reviewers.

### 8. Is there an RFC Process for New Theories?
There is no formal, written "RFC (Request for Comments) Document" system like there is in the Rust programming language. However, **the Zulip Chat is the de facto RFC platform.**

*   **The Workflow:** Before writing any code, go to the **mathlib Zulip chat**.
*   **The Proposal:** Post in the `#mathlib-dev` or `#number-theory` channels. Say: *"I am planning to formalize Farey Sequences. I intend to start with definitions of $F_n$ and move toward properties of neighbors. Does this sound like a good direction, or is there existing work I should build upon?"*
*   **The Benefit:** This prevents you from wasting weeks on a project that someone else is already working on, or on a project that the community thinks is structurally incompatible with the current library.

**Summary Tip:** If you want to contribute, **talk on Zulip first.** The community is incredibly helpful, but they value coordination over isolated, massive code dumps.
