### Mathlib4 (Lean 4) Naming Conventions

1. **Theorem/Lemma Naming**  
   - Use **snake_case** with a descriptive name.  
   - Example: `additive_monoid_hom_eq`, `continuous_map_eq`.  
   - Avoid generic names like `lemma1` or `theorem_x`.  

2. **File Naming**  
   - Use **snake_case** for filenames.  
   - Example: `nat.lean`, `algebra_group.lean`, `farey_sequence.lean`.  
   - Files are typically named after the main topic (e.g., `farey_sequence.lean` for Farey sequence-related results).  

3. **Import Style**  
   - Use full paths with `import` statements.  
   - Example: `import data.nat`, `import algebra.group`.  
   - Avoid relative imports (e.g., `import .foo` unless explicitly needed).  

4. **Documentation Requirements**  
   - Include **docstrings** (using triple backticks or `--doc`) to explain the theorem's purpose.  
   - Example:  
     ```lean
     --doc: States that the mediant of two consecutive Farey terms is the next term.
     theorem mediant_property (a b c d : ℕ) : ... 
     ```

5. **What to Avoid**  
   - **`native_decide`** for nontrivial results (use `decidable` or `by_cases` instead).  
   - **`sorry`** for proofs (replace with actual proofs or mark as `noncomputable`).  
   - **Axioms** unless explicitly required (prefer constructive proofs).  

---

### Examples of Good Mathlib Theorem Names for Farey Sequence Results

1. **`mediant_property`**  
   - *Description*: The mediant of two consecutive terms in a Farey sequence is the next term in the sequence.  
   - Example: `mediant_property a b c d : (a + c) / (b + d) ∈ F_{n+1}`.

2. **`farey_sequence_length_formula`**  
   - *Description*: The length of the Farey sequence of order `n` is `1 + ∑_{k=1}^n φ(k)`.  
   - Example: `farey_sequence_length_formula n : #F_n = 1 + ∑_{k=1}^n φ k`.

3. **`consecutive_terms_mediant`**  
   - *Description*: The mediant of two consecutive terms in a Farey sequence lies between them.  
   - Example: `consecutive_terms_mediant a b c d : a/b < (a+c)/(b+d) < c/d`.

4. **`farey_sequence_continued_fraction_connection`**  
   - *Description*: A Farey sequence of order `n` contains all fractions with denominators ≤ `n` that are in reduced form.  
   - Example: `farey_sequence_continued_fraction_connection n : ∀ a b, a/b ∈ F_n → b ≤ n`.

5. **`farey_sequence_order_n_property`**  
   - *Description*: The Farey sequence of order `n` is closed under the mediant operation for terms in `F_n`.  
   - Example: `farey_sequence_order_n_property n : ∀ a b c d, a/b ∈ F_n ∧ c/d ∈ F_n → (a+c)/(b+d) ∈ F_{n+1}`.  

--- 

These names follow Mathlib4 conventions by being descriptive, using snake_case, and avoiding reserved keywords or non-constructive tactics.
