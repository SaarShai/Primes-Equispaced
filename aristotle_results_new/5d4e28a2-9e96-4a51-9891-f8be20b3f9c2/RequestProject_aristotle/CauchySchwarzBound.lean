import Mathlib
import PrimeCircle
import DisplacementShift
import SignTheorem

/-!
# Cauchy-Schwarz Lower Bound on Wobble Numerator

## Main result
wobbleNumerator N ≥ |F_N| / 4

## Proof strategy
1. Sum of displacements: Σ D(f) = -n/2 (from Farey symmetry: Σ f = n/2)
2. Cauchy-Schwarz: (Σ a_i)² ≤ n · Σ a_i²
3. Combine: n²/4 ≤ n · Σ D², so Σ D² ≥ n/4
-/

open Finset BigOperators

/-! ## Step 1: Displacement sum identity -/

/-
PROBLEM
The sum of all displacements in F_N equals -|F_N|/2.
    Proof: Σ D = Σ rank - n·Σ f = n(n-1)/2 - n·(n/2) = -n/2.
    Here n = |F_N| = (fareySet N).card.
    The key fact is Σ_{f ∈ F_N} f = n/2 (Farey symmetry: fractions pair as f ↔ 1-f).

PROVIDED SOLUTION
Σ D(f) = Σ_{ab ∈ fareySet N} (fareyRank N (a/b) - (fareySet N).card * (a/b)). The fareyRank of (a/b) counts all pairs in fareySet N with value ≤ a/b. If we index the n distinct Farey fractions as f_0 < f_1 < ... < f_{n-1}, then fareyRank(f_j) = j+1 (1-indexed, since f_j itself is counted). So Σ fareyRank = 1+2+...+n = n(n+1)/2. Also, Σ_{f ∈ F_N} f = n/2 by Farey symmetry (the involution f ↦ 1-f pairs fractions). So Σ D = n(n+1)/2 - n·(n/2) = n/2. This is a deep result. For a Lean proof, try native_decide for small cases or proceed by establishing the rank-sum and fraction-sum identities separately.
-/
lemma displacement_sum (N : ℕ) (hN : N ≥ 1) :
    ∑ ab ∈ fareySet N, displacement N ((ab.1 : ℚ) / ab.2) =
      ((fareySet N).card : ℚ) / 2 := by
  by_contra h_contra;
  -- Let's calculate the sum of the ranks of the fractions in the Farey sequence.
  have h_rank_sum : ∑ ab ∈ fareySet N, fareyRank N (ab.1 / ab.2) = (∑ i ∈ Finset.range (fareySet N).card, (i + 1 : ℚ)) := by
    -- Let's sort the elements of `fareySet N` in increasing order.
    obtain ⟨seq, hseq⟩ : ∃ seq : Fin (fareySet N).card → ℕ × ℕ, (∀ i, seq i ∈ fareySet N) ∧ StrictMono (fun i => (seq i).1 / (seq i).2 : Fin (fareySet N).card → ℚ) ∧ ∀ x ∈ fareySet N, ∃ i, seq i = x := by
      have h_order : ∃ seq : Fin (fareySet N).card → ℕ × ℕ, (∀ i, seq i ∈ fareySet N) ∧ StrictMono (fun i => (seq i).1 / (seq i).2 : Fin (fareySet N).card → ℚ) := by
        have h_order : ∃ seq : Fin (fareySet N).card → ℚ, StrictMono seq ∧ ∀ i, seq i ∈ Finset.image (fun ab : ℕ × ℕ => (ab.1 : ℚ) / ab.2) (fareySet N) := by
          have h_sorted : Finset.card (Finset.image (fun ab => (ab.1 : ℚ) / ab.2) (fareySet N)) = (fareySet N).card := by
            refine' Finset.card_image_of_injOn _;
            intros a ha b hb hab;
            -- Since $a$ and $b$ are in the Farey set, they are coprime and $a.2 \leq N$, $b.2 \leq N$. If $a.1 / a.2 = b.1 / b.2$, then $a.1 * b.2 = b.1 * a.2$.
            have h_eq : a.1 * b.2 = b.1 * a.2 := by
              rw [ div_eq_div_iff ] at hab <;> norm_cast at * <;> linarith [ Finset.mem_filter.mp ha, Finset.mem_filter.mp hb ];
            -- Since $a$ and $b$ are in the Farey set, they are coprime and $a.2 \leq N$, $b.2 \leq N$. If $a.1 * b.2 = b.1 * a.2$, then $a.1 = b.1$ and $a.2 = b.2$.
            have h_coprime : Nat.Coprime a.1 a.2 ∧ Nat.Coprime b.1 b.2 := by
              unfold fareySet at ha hb; aesop;
            have h_eq : a.1 ∣ b.1 ∧ b.1 ∣ a.1 := by
              exact ⟨ h_coprime.1.dvd_of_dvd_mul_right <| h_eq ▸ dvd_mul_right _ _, h_coprime.2.dvd_of_dvd_mul_right <| h_eq.symm ▸ dvd_mul_right _ _ ⟩;
            have := Nat.dvd_antisymm h_eq.1 h_eq.2; aesop;
          exact ⟨ fun i => Finset.orderEmbOfFin _ ( by aesop ) i, by aesop_cat, fun i => Finset.orderEmbOfFin_mem _ ( by aesop ) _ ⟩;
        obtain ⟨ seq, hseq₁, hseq₂ ⟩ := h_order; choose f hf using fun i => Finset.mem_image.mp ( hseq₂ i ) ; use f; aesop;
      obtain ⟨seq, hseq⟩ := h_order
      have h_surj : Finset.image seq Finset.univ = fareySet N := by
        exact Finset.eq_of_subset_of_card_le ( Finset.image_subset_iff.mpr fun i _ => hseq.1 i ) ( by rw [ Finset.card_image_of_injective _ fun i j hij => hseq.2.injective <| by aesop ] ; simpa );
      exact ⟨ seq, hseq.1, hseq.2, fun x hx => by rw [ ← h_surj ] at hx; exact Finset.mem_image.mp hx |> Exists.imp fun i => And.right ⟩;
    -- By definition of `seq`, we know that `fareyRank N (seq i).1 / (seq i).2 = i + 1` for all `i`.
    have h_rank_eq : ∀ i, fareyRank N ((seq i).1 / (seq i).2 : ℚ) = i + 1 := by
      intro i
      have h_rank_eq : Finset.filter (fun p => (p.1 : ℚ) / p.2 ≤ (seq i).1 / (seq i).2) (fareySet N) = Finset.image (fun j => seq j) (Finset.Iic i) := by
        ext p;
        grind +suggestions;
      convert congr_arg Finset.card h_rank_eq using 1;
      rw [ Finset.card_image_of_injective _ fun x y hxy => hseq.2.1.injective <| by aesop ] ; aesop;
    have h_sum_eq : ∑ ab ∈ fareySet N, fareyRank N (ab.1 / ab.2 : ℚ) = ∑ i ∈ Finset.univ.image seq, fareyRank N (i.1 / i.2 : ℚ) := by
      rw [ Finset.eq_of_subset_of_card_le ( Finset.image_subset_iff.mpr fun i _ => hseq.1 i ) ( by rw [ Finset.card_image_of_injective _ fun i j hij => hseq.2.1.injective <| by aesop ] ; simpa ) ];
    rw [ h_sum_eq, Finset.sum_image ];
    · simp +decide [ Finset.sum_range, h_rank_eq ];
    · exact fun i _ j _ hij => hseq.2.1.injective <| by aesop;
  -- Let's calculate the sum of the fractions in the Farey sequence.
  have h_frac_sum : ∑ ab ∈ fareySet N, (ab.1 / ab.2 : ℚ) = (fareySet N).card / 2 := by
    -- By pairing each fraction with its complement to 1, we can show that the sum of the fractions is equal to the sum of their complements.
    have h_pairing : ∑ ab ∈ fareySet N, (ab.1 / ab.2 : ℚ) = ∑ ab ∈ fareySet N, (1 - ab.1 / ab.2 : ℚ) := by
      apply Finset.sum_bij (fun ab _ => (ab.2 - ab.1, ab.2));
      · simp [fareySet];
        exact fun a b ha hb hb' hab h => ⟨ ⟨ by linarith, hb ⟩, hb', by simpa [ hab ] using h ⟩;
      · simp +contextual [ fareySet ];
        intros; omega;
      · simp +decide [ fareySet ];
        exact fun a b ha hb hb' hab h => ⟨ b - a, ⟨ ⟨ Nat.sub_le_of_le_add <| by linarith, hb ⟩, hb', Nat.sub_le_of_le_add <| by linarith, by simpa [ hab ] using h ⟩, Nat.sub_sub_self hab ⟩;
      · intro ab hab; rw [ Nat.cast_sub ( by linarith [ Finset.mem_filter.mp hab |>.2.1, Finset.mem_filter.mp hab |>.2.2.1 ] ) ] ; ring; norm_num [ show ab.2 ≠ 0 from by linarith [ Finset.mem_filter.mp hab |>.2.1, Finset.mem_filter.mp hab |>.2.2.1 ] ] ;
    norm_num at *; linarith;
  -- Let's simplify the expression for the sum of the displacements.
  have h_displacement_sum_simplified : ∑ ab ∈ fareySet N, displacement N (ab.1 / ab.2) = (∑ i ∈ Finset.range (fareySet N).card, (i + 1 : ℚ)) - (fareySet N).card * ((fareySet N).card / 2 : ℚ) := by
    rw [ ← h_frac_sum, ← h_rank_sum ] ; simp +decide [ displacement ] ; ring;
    simp +decide only [mul_assoc, Finset.mul_sum _ _ _];
  exact h_contra <| h_displacement_sum_simplified.trans <| Nat.recOn ( Finset.card ( fareySet N ) ) ( by norm_num ) fun n ih => by norm_num [ Finset.sum_range_succ ] at * ; linarith;

/-! ## Step 2: Cauchy-Schwarz application -/

/-
PROBLEM
**Cauchy-Schwarz lower bound on wobble numerator.**
    Since wobbleNumerator N = Σ D(f)² and Σ D(f) = -n/2,
    by Cauchy-Schwarz: (Σ D)² ≤ n · Σ D² implies n²/4 ≤ n · Σ D²,
    so Σ D² ≥ n/4.

PROVIDED SOLUTION
By Cauchy-Schwarz (sum_sq_ge_quarter_of_sum_eq_pos_half from CWBound.lean, or the neg version from AbstractCauchySchwarz.lean applied to -D): We have displacement_sum giving Σ D = n/2. Apply sum_sq_ge_quarter_of_sum_eq_pos_half with s = fareySet N, a = displacement N, to get Σ D² ≥ n/4. This is exactly wobbleNumerator N ≥ (fareySet N).card / 4. Note: wobbleNumerator N = Σ_{ab ∈ fareySet N} (displacement N (ab.1/ab.2))², so unfold wobbleNumerator and apply the abstract result. Or use sum_sq_ge_quarter_of_sum_eq_neg_half from AbstractCauchySchwarz applied to (-displacement), since Σ(-D) = -n/2 and Σ(-D)² = Σ D².
-/
theorem wobbleNumerator_ge_card_div_four (N : ℕ) (hN : N ≥ 1) :
    wobbleNumerator N ≥ ((fareySet N).card : ℚ) / 4 := by
  -- Apply the Cauchy-Schwarz inequality with $a = -displacement N$ and use the fact that $card(fareySet N) > 0$.
  have h_card_pos : 0 < (fareySet N).card := by
    exact Finset.card_pos.mpr ⟨ ( 0, 1 ), by unfold fareySet; aesop ⟩;
  have h_sum_sq : (∑ ab ∈ fareySet N, (displacement N ((ab.1 : ℚ) / ab.2))) ^ 2 ≤ (fareySet N).card * (∑ ab ∈ fareySet N, (displacement N ((ab.1 : ℚ) / ab.2)) ^ 2) := by
    exact?
  generalize_proofs at *; (
  unfold wobbleNumerator; nlinarith [ show ( 0 : ℚ ) < ( fareySet N |> Finset.card ) by positivity, displacement_sum N hN ] ;)