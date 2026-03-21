import Mathlib

/-!
# Part 10: Farey Sequence Cardinality and Ramanujan Sums

This file proves three theorems:
1. `farey_new_fractions_count`: |F_N| = |F_{N-1}| + φ(N) for N ≥ 2
2. `ramanujan_sum_one`: The Ramanujan sum c_q(1) = μ(q)
3. `prime_ramanujan_neg_one`: For prime p, c_p(1) = -1
-/

open Finset BigOperators Complex

/-! ## Farey Sequence Definitions -/

/-- The Farey set of order N: all pairs (a, q) with 1 ≤ q ≤ N, 0 ≤ a ≤ q, gcd(a,q) = 1.
    These represent fractions a/q in [0,1] in lowest terms with denominator ≤ N. -/
def fareySet (N : ℕ) : Finset (ℕ × ℕ) :=
  ((range (N + 1)) ×ˢ (range (N + 1))).filter
    (fun p => 1 ≤ p.2 ∧ p.1 ≤ p.2 ∧ Nat.Coprime p.1 p.2)

/-- The new fractions added when going from F_{N-1} to F_N:
    pairs (a, N) with 1 ≤ a ≤ N-1 and gcd(a, N) = 1. -/
def fareyNew (N : ℕ) : Finset (ℕ × ℕ) :=
  ((range N).filter (fun a => Nat.Coprime a N)).map
    ⟨fun a => (a, N), fun a b h => by simp [Prod.mk.injEq] at h; exact h⟩

/-- |F_N| = |F_{N-1}| + φ(N) for N ≥ 2. The Farey set of order N contains all fractions from
    F_{N-1} plus the φ(N) new reduced fractions with denominator exactly N. -/
theorem farey_new_fractions_count (N : ℕ) (hN : 2 ≤ N) :
    (fareySet N).card = (fareySet (N - 1)).card + Nat.totient N := by
  rcases N with ⟨ ⟩ <;> norm_num at *;
  rename_i n; erw [ show fareySet ( n + 1 ) = fareySet n ∪ fareyNew ( n + 1 ) from ?_ ] ; erw [ Finset.card_union_of_disjoint ];
  · unfold fareyNew;
    norm_num [ Nat.totient ];
    simp +decide only [Nat.coprime_comm];
  · unfold fareySet fareyNew; norm_num [ Finset.disjoint_left ] ;
    grind;
  · ext ⟨a, b⟩; simp [fareySet, fareyNew];
    grind

/-! ## Ramanujan Sum Definitions and Helper Lemmas -/

/-- The Ramanujan sum c_q(1) = Σ_{a coprime to q, 0 ≤ a < q} exp(2πia/q). -/
noncomputable def ramanujanSum (q : ℕ) : ℂ :=
  ∑ a ∈ (range q).filter (fun a => Nat.Coprime a q),
    exp (2 * ↑Real.pi * I * (↑a : ℂ) / (↑q : ℂ))

/-- The primitive q-th root of unity. -/
noncomputable def rootOfUnity (q : ℕ) : ℂ :=
  exp (2 * ↑Real.pi * I / (↑q : ℂ))

lemma exp_eq_rootOfUnity_pow (q a : ℕ) :
    exp (2 * ↑Real.pi * I * (↑a : ℂ) / (↑q : ℂ)) = rootOfUnity q ^ a := by
  simp only [rootOfUnity]
  rw [div_eq_mul_inv, div_eq_mul_inv, ← Complex.exp_nat_mul]
  ring_nf

lemma ramanujanSum_eq_sum_pow (q : ℕ) :
    ramanujanSum q = ∑ a ∈ (range q).filter (fun a => Nat.Coprime a q),
      rootOfUnity q ^ a := by
  simp only [ramanujanSum, exp_eq_rootOfUnity_pow]

/-
PROBLEM
Sum of all q-th roots of unity equals 0 for q ≥ 2.

PROVIDED SOLUTION
Use the fact that rootOfUnity q is a primitive q-th root of unity (from Complex.isPrimitiveRoot_exp), then apply IsPrimitiveRoot.geom_sum_eq_zero.

Key steps:
1. Let ω = rootOfUnity q = exp(2πi/q).
2. Show ω is a primitive q-th root of unity: use Complex.isPrimitiveRoot_exp q (by omega from hq).
3. Apply IsPrimitiveRoot.geom_sum_eq_zero to get Σ_{a ∈ range q} ω^a = 0.
-/
lemma sum_rootOfUnity_pow_eq_zero (q : ℕ) (hq : 2 ≤ q) :
    ∑ a ∈ range q, rootOfUnity q ^ a = 0 := by
  convert IsPrimitiveRoot.geom_sum_eq_zero ( Complex.isPrimitiveRoot_exp q ( by positivity ) ) hq

/-
PROBLEM
The Möbius indicator: sum of μ(d) over divisors of n is 1 if n = 1, else 0.

PROVIDED SOLUTION
Use the identity ↑ζ * ↑μ = 1 in the arithmetic function ring (ArithmeticFunction.coe_zeta_mul_coe_moebius). Evaluate both sides at n. The LHS gives Σ_{(d,e) ∈ divisorsAntidiagonal n} ζ(d) * μ(e). The RHS gives [n=1]. Then rewrite the LHS as Σ_{d ∈ n.divisors} μ(d) using Nat.sum_divisorsAntidiagonal or similar.

Actually, a cleaner approach:
- Use ArithmeticFunction.sum_eq_iff_sum_mul_moebius_eq to extract the identity.
- Or directly evaluate (↑ζ * ↑μ)(n) = Σ_{x ∈ n.divisorsAntidiagonal} ↑ζ(x.1) * ↑μ(x.2).
- Since ζ(d) = 1 for d > 0 and ζ(0) = 0, and all d in divisorsAntidiagonal are > 0 (since n > 0), each term is just μ(x.2).
- Reindex: as (d,e) ranges over divisorsAntidiagonal n, e ranges over divisors of n.
- So the sum equals Σ_{e ∈ n.divisors} μ(e) = Σ_{d ∈ n.divisors} μ(d).

Actually, perhaps simplest: use Nat.sum_divisorsAntidiagonal_eq_sum_divisors to convert antidiagonal sum to divisor sum.
-/
lemma sum_moebius_divisors (n : ℕ) (hn : 0 < n) :
    ∑ d ∈ n.divisors, (ArithmeticFunction.moebius d : ℂ) =
    if n = 1 then 1 else 0 := by
  -- Applying the identity for the Möbius function
  have h_moebius : ∑ d ∈ n.divisors, (ArithmeticFunction.moebius d : ℂ) = (ArithmeticFunction.moebius * ArithmeticFunction.zeta) n := by
    simp +decide [ ArithmeticFunction.moebius, ArithmeticFunction.zeta ];
    rw [ Nat.sum_divisorsAntidiagonal fun x y => if y = 0 then 0 else if Squarefree x then ( -1 : ℂ ) ^ ArithmeticFunction.cardFactors x else 0 ];
    exact Finset.sum_congr rfl fun x hx => by rw [ if_neg ( Nat.ne_of_gt ( Nat.div_pos ( Nat.le_of_dvd hn ( Nat.dvd_of_mem_divisors hx ) ) ( Nat.pos_of_mem_divisors hx ) ) ) ] ;
  rw [h_moebius] at *; aesop;

/-
PROBLEM
Partition identity: the sum over divisors of Ramanujan sums equals
    the sum of all roots of unity (= 0 for q ≥ 2, = 1 for q = 1).

PROVIDED SOLUTION
Use Finset.sum_fiberwise_of_maps_to to partition range q by the map a ↦ q / Nat.gcd a q (which maps into q.divisors).

For each divisor d of q, the fiber {a ∈ range q : q / gcd(a,q) = d} consists of elements with gcd(a,q) = q/d, i.e., multiples of q/d in {0,...,q-1}. Write a = (q/d) * b where b ∈ {0,...,d-1} with gcd(b, d) = 1.

Then rootOfUnity q ^ a = rootOfUnity q ^ ((q/d)*b) = (rootOfUnity q ^ (q/d)) ^ b = rootOfUnity d ^ b.

So the fiber sum equals Σ_{b coprime to d, b < d} rootOfUnity d ^ b = ramanujanSum d.

Key Lean steps:
1. Use ramanujanSum_eq_sum_pow to express ramanujanSum in terms of rootOfUnity powers.
2. The map a ↦ q / Nat.gcd a q sends range q to q.divisors (since gcd(a,q) | q for any a).
3. For the rootOfUnity identity: rootOfUnity q ^ (q/d) = exp(2πi(q/d)/q) = exp(2πi/d) = rootOfUnity d.
-/
lemma sum_ramanujan_divisors (q : ℕ) (hq : 0 < q) :
    ∑ d ∈ q.divisors, ramanujanSum d =
    ∑ a ∈ range q, rootOfUnity q ^ a := by
  -- For each $d \mid q$, the sum $\sum_{a=0}^{q-1} \omega^{a(q/d)}$ is equal to $\sum_{b=0}^{d-1} \omega^{b}$.
  have h_sum_bound : ∀ d ∈ q.divisors, ∑ a ∈ Finset.filter (fun a => q / Nat.gcd a q = d) (Finset.range q), rootOfUnity q ^ a = ramanujanSum d := by
    intros d hd
    have h_filter : Finset.filter (fun a => Nat.gcd a q = q / d) (Finset.range q) = Finset.image (fun b => b * (q / d)) (Finset.filter (fun b => Nat.Coprime b d) (Finset.range d)) := by
      ext a
      simp [Finset.mem_image, Finset.mem_filter];
      constructor <;> intro h;
      · refine' ⟨ a / ( q / d ), ⟨ _, _ ⟩, _ ⟩;
        · rw [ Nat.div_lt_iff_lt_mul <| Nat.div_pos ( Nat.le_of_dvd hq <| Nat.dvd_of_mem_divisors hd ) <| Nat.pos_of_mem_divisors hd ] ; nlinarith [ Nat.div_mul_cancel <| Nat.dvd_of_mem_divisors hd ] ;
        · -- Since $\gcd(a, q) = q / d$, we have $\gcd(a / (q / d), q / (q / d)) = 1$.
          have h_coprime : Nat.gcd (a / (q / d)) (q / (q / d)) = 1 := by
            rw [ ← h.2, Nat.gcd_div ( Nat.gcd_dvd_left _ _ ) ( Nat.gcd_dvd_right _ _ ), Nat.div_self ( Nat.gcd_pos_of_pos_right _ hq ) ];
          rwa [ Nat.div_div_self ( Nat.dvd_of_mem_divisors hd ) ( by aesop ) ] at h_coprime;
        · rw [ Nat.div_mul_cancel ( h.2 ▸ Nat.gcd_dvd_left _ _ ) ];
      · rcases h with ⟨ b, ⟨ hb₁, hb₂ ⟩, rfl ⟩ ; refine' ⟨ _, _ ⟩ <;> simp_all +decide [ Nat.mul_div_cancel' ( Nat.dvd_of_mem_divisors hd ) ] ;
        · nlinarith [ Nat.div_mul_cancel hd.1 ];
        · cases hd.1 ; simp_all +decide [ Nat.gcd_mul_left, Nat.gcd_mul_right ];
    -- Using the fact that `rootOfUnity q ^ (q / d * b) = rootOfUnity d ^ b`, we can rewrite the sum.
    have h_rewrite : ∑ a ∈ Finset.image (fun b => b * (q / d)) (Finset.filter (fun b => Nat.Coprime b d) (Finset.range d)), rootOfUnity q ^ a = ∑ b ∈ Finset.filter (fun b => Nat.Coprime b d) (Finset.range d), rootOfUnity d ^ b := by
      rw [ Finset.sum_image ];
      · unfold rootOfUnity; norm_num [ pow_mul', ← Complex.exp_nat_mul ] ;
        rw [ Nat.cast_div ( Nat.dvd_of_mem_divisors hd ) ( by aesop ) ] ; ring;
        simp +decide [ mul_assoc, mul_comm, mul_left_comm, hq.ne' ];
      · exact fun x hx y hy hxy => mul_right_cancel₀ ( Nat.ne_of_gt ( Nat.div_pos ( Nat.le_of_dvd hq ( Nat.dvd_of_mem_divisors hd ) ) ( Nat.pos_of_mem_divisors hd ) ) ) hxy;
    convert h_rewrite using 2;
    · convert h_filter using 2;
      ext a; exact ⟨fun h => by
        rw [ ← h, Nat.div_div_self ( Nat.gcd_dvd_right _ _ ) ( by aesop ) ], fun h => by
        rw [ h, Nat.div_div_self ( Nat.dvd_of_mem_divisors hd ) ( by aesop ) ]⟩;
    · exact?;
  rw [ ← Finset.sum_congr rfl h_sum_bound, Finset.sum_fiberwise_of_maps_to ];
  exact fun i hi => Nat.mem_divisors.mpr ⟨ Nat.div_dvd_of_dvd <| Nat.gcd_dvd_right _ _, by aesop ⟩

/-
PROBLEM
The Ramanujan sum c_q(1) equals the Möbius function μ(q), for q ≥ 1.

This follows from Möbius inversion: define g(q) = Σ_{a=1}^{q} exp(2πia/q).
Then g(q) = 0 for q ≥ 2 (sum of roots of unity) and g(1) = 1.
Also g(q) = Σ_{d|q} c_{q/d}(1) by partitioning {1,...,q} according to gcd(a,q).
By Möbius inversion, c_q(1) = Σ_{d|q} μ(q/d) · g(d) = μ(q).

PROVIDED SOLUTION
Use the Möbius inversion formula ArithmeticFunction.sum_eq_iff_sum_smul_moebius_eq.

Define f(n) = ramanujanSum n and g(n) = Σ_{a ∈ range n} (rootOfUnity n)^a = if n ≤ 1 then ↑n else 0.

Step 1: Show the forward direction of Möbius inversion: ∀ n > 0, Σ_{d ∈ n.divisors} f(d) = g(n).
This follows from sum_ramanujan_divisors: Σ_{d ∈ n.divisors} ramanujanSum d = Σ_{a ∈ range n} (rootOfUnity n)^a.
And Σ_{a ∈ range n} (rootOfUnity n)^a = 0 for n ≥ 2 (from sum_rootOfUnity_pow_eq_zero) and = 1 for n = 1.

Step 2: Apply the backward direction of Möbius inversion to get:
∀ n > 0, Σ_{(d,e) ∈ n.divisorsAntidiagonal} μ(d) • g(e) = f(n).

Step 3: Simplify: g(e) = 0 unless e = 1 (for e > 0). When e = 1, g(1) = 1. The only term (d,e) in divisorsAntidiagonal with e = 1 is (n, 1). So the sum = μ(n) • 1 = ↑(μ(n) : ℤ).

Hence ramanujanSum(q) = ↑(μ(q) : ℤ).
-/
theorem ramanujan_sum_one (q : ℕ) (hq : 1 ≤ q) :
    ramanujanSum q = ↑(ArithmeticFunction.moebius q : ℤ) := by
  by_contra h_neq;
  -- By the Möbius inversion formula, we have that $\sum_{d \mid q} \mu(d) g(q/d) = f(q)$.
  have h_mobi : ∑ d ∈ q.divisors, (ArithmeticFunction.moebius d : ℂ) * (∑ a ∈ Finset.range (q / d), (rootOfUnity (q / d)) ^ a) = ramanujanSum q := by
    have := @ArithmeticFunction.sum_eq_iff_sum_smul_moebius_eq ( ℂ ) ( by infer_instance );
    convert @this ( fun n => ramanujanSum n ) ( fun n => ∑ a ∈ Finset.range n, rootOfUnity n ^ a ) |>.1 _ q hq using 1;
    · rw [ Nat.sum_divisorsAntidiagonal fun x y => ArithmeticFunction.moebius x • ∑ a ∈ Finset.range y, rootOfUnity y ^ a ];
      norm_num [ Algebra.smul_def ];
    · intro n hn; rw [ sum_ramanujan_divisors n hn ] ;
  -- Evaluate the inner sum $\sum_{a=0}^{q/d-1} \omega_{q/d}^a$.
  have h_inner : ∀ d ∈ q.divisors, d ≠ q → ∑ a ∈ Finset.range (q / d), (rootOfUnity (q / d)) ^ a = 0 := by
    intros d hd hd_neq
    have h_inner_sum : ∑ a ∈ Finset.range (q / d), (rootOfUnity (q / d)) ^ a = 0 := by
      have h_root : q / d ≥ 2 := by
        nlinarith [ Nat.div_mul_cancel ( Nat.dvd_of_mem_divisors hd ), Nat.lt_of_le_of_ne ( Nat.le_of_dvd hq ( Nat.dvd_of_mem_divisors hd ) ) hd_neq ]
      exact sum_rootOfUnity_pow_eq_zero _ h_root
    exact h_inner_sum;
  rw [ Finset.sum_eq_single q ] at h_mobi;
  · exact h_neq <| h_mobi.symm.trans <| by norm_num [ Nat.div_self hq ] ;
  · aesop;
  · aesop

/-- For prime p, the Ramanujan sum c_p(1) = -1.
    This follows from `ramanujan_sum_one` since μ(p) = -1 for primes. -/
theorem prime_ramanujan_neg_one (p : ℕ) (hp : Nat.Prime p) :
    ramanujanSum p = -1 := by
  rw [ramanujan_sum_one, ArithmeticFunction.moebius_apply_prime hp]
  · norm_num
  · exact hp.pos

/-! ## Part 11: Per-Prime Wobble Decomposition (Stage 1)

The per-prime wobble change ΔW(p) = W(p-1) - W(p) decomposes into three terms:
  ΔW = -ΔS2 + ΔR_term + ΔJ

where:
  ΔS2 = Σ_{k=1}^{p-1} (k/p)²  [sum of squares of new fractions]
  ΔJ = J(|F_{p-1}|) - J(|F_p|) [change in ideal-position sum]
  ΔR_term = 2·R_new/|F_p| - 2·R_old/|F_{p-1}| [rank-weighted sum change]

  J(n) = (n-1)(2n-1)/(6n)  [sum of squared ideal positions]
  R(N) = Σ_{j=0}^{|F_N|-1} j · f_j  [rank-weighted Farey sum]

The following theorems formalize the exact components.
-/

/-- The sum of squares of the new fractions k/p for prime p equals (p-1)(2p-1)/(6p).
This is the ΔS2 component of the wobble decomposition. -/
theorem new_fractions_sum_sq (p : ℕ) (hp : Nat.Prime p) :
    ∑ k ∈ Finset.Ico 1 p, ((k : ℚ) / p) ^ 2 =
    ((p - 1) * (2 * p - 1) : ℚ) / (6 * p) := by
  sorry

/-- The sum of squared ideal positions j²/n² for j=0..n-1 equals (n-1)(2n-1)/(6n).
This is the J(n) function in the decomposition. -/
theorem ideal_position_sum_sq (n : ℕ) (hn : 0 < n) :
    ∑ j ∈ Finset.range n, ((j : ℚ) / n) ^ 2 =
    ((n - 1) * (2 * n - 1) : ℚ) / (6 * n) := by
  sorry

/-- The Farey wobble W(N) decomposes as S2 - (2/n)R + J(n), where
S2 = Σ f_j², R = Σ j·f_j, J(n) = (n-1)(2n-1)/(6n), and n = |F_N|. -/
theorem wobble_decomposition (N : ℕ) (hN : 0 < N) :
    let F := fareySet N
    let n := F.card
    ∑ p ∈ F, ((p.1 : ℚ) / p.2 - (F.indexOf p : ℚ) / n) ^ 2 =
    ∑ p ∈ F, ((p.1 : ℚ) / p.2) ^ 2
    - 2 / n * ∑ p ∈ F, (F.indexOf p : ℚ) * ((p.1 : ℚ) / p.2)
    + ((n - 1) * (2 * n - 1) : ℚ) / (6 * n) := by
  sorry