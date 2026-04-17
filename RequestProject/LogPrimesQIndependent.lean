import Mathlib

/-!
# Q-linear independence of logarithms of distinct primes

Key lemma for the Turán non-vanishing theorem (Theorem A2 in Paper C).
If Σ qⱼ · log pⱼ = 0 for rationals qⱼ and distinct primes pⱼ,
then all qⱼ = 0.

This follows from the Fundamental Theorem of Arithmetic:
if Σ qⱼ log pⱼ = 0, clearing denominators gives Σ mⱼ log pⱼ = 0
with integers mⱼ, hence Π pⱼ^mⱼ = 1, hence mⱼ = 0 for all j
by unique prime factorization.
-/

private abbrev prodPrimePow (ps es : List ℕ) : ℕ :=
  (List.zipWith (fun a b => a ^ b) ps es).prod

/-- log of a prime is positive -/
lemma log_prime_pos {p : ℕ} (hp : Nat.Prime p) : 0 < Real.log (p : ℝ) :=
  Real.log_pos (by exact_mod_cast hp.one_lt)

/-
A prime does not divide a product of powers of other (distinct) primes.
    If p is prime, p ∉ ps (a list of primes), then p does not divide
    the product (p₁^e₁ * p₂^e₂ * ... * pₖ^eₖ).
-/
lemma prime_ndvd_prod_pow_of_nmem (p : ℕ) (ps es : List ℕ)
    (hp : Nat.Prime p) (hprimes : ∀ q ∈ ps, Nat.Prime q) (hnotin : p ∉ ps)
    (hlen : ps.length = es.length) :
    ¬ (p ∣ prodPrimePow ps es) := by
  have hcdp : ∀ q ∈ ps, ∀ e : ℕ, ¬(p ∣ q ^ e) := by
    exact fun q hq e => mt hp.dvd_of_dvd_pow <| fun h => hnotin <| by have := Nat.prime_dvd_prime_iff_eq hp ( hprimes q hq ) ; aesop;
  induction es generalizing ps <;> simp_all +decide [ Prod.fst, Prod.snd, List.zipWith ];
  · exact Nat.Prime.not_dvd_one hp;
  · rcases ps with ( _ | ⟨ q, ps ⟩ ) <;> simp_all +decide [ prodPrimePow ];
    exact Nat.Prime.not_dvd_mul hp ( hcdp.1 _ ) ( by aesop )

/-
The sum Σ eⱼ · log(pⱼ) with natural number coefficients equals log of the product Π pⱼ^eⱼ.
-/
lemma sum_nat_mul_log_eq_log_prod (ps es : List ℕ)
    (hprimes : ∀ p ∈ ps, Nat.Prime p)
    (hlen : ps.length = es.length) :
    (List.zipWith (fun p e => (e : ℝ) * Real.log (p : ℝ)) ps es).sum =
    Real.log ((prodPrimePow ps es : ℕ) : ℝ) := by
  induction ps generalizing es <;> cases es <;> norm_cast;
  · norm_num;
  · simp_all +decide [ mul_comm, List.zipWith ];
    rw [ Real.log_mul, Real.log_pow ] <;> norm_cast <;> simp_all +decide [ Nat.Prime.ne_zero ];
    norm_num [ List.mem_iff_get ];
    exact fun x hx => absurd hx <| Nat.Prime.ne_zero <| hprimes.2 _ <| by simp;

/-
The product of prime powers (with natural exponents) is always positive.
-/
lemma prod_prime_pow_pos (ps es : List ℕ)
    (hprimes : ∀ p ∈ ps, Nat.Prime p)
    (hlen : ps.length = es.length) :
    (0 : ℝ) < ((prodPrimePow ps es : ℕ) : ℝ) := by
  induction ps generalizing es <;> cases es <;> norm_num at *;
  exact mul_pos ( pow_pos ( Nat.cast_pos.mpr hprimes.1.pos ) _ ) ( by rename_i k hk; aesop )

/-
Integer linear independence of logarithms of distinct primes:
    If ps are distinct primes and ms are integers with Σ mⱼ * log(pⱼ) = 0,
    then all mⱼ = 0.
-/
lemma int_log_primes_independent (ps : List ℕ) (ms : List ℤ)
    (hprimes : ∀ p ∈ ps, Nat.Prime p)
    (hnodup : ps.Nodup)
    (hlen : ps.length = ms.length)
    (hsum : (List.zipWith (fun p m => (m : ℝ) * Real.log (p : ℝ)) ps ms).sum = 0) :
    ∀ m ∈ ms, m = 0 := by
  induction' ps with p ps ih generalizing ms;
  · cases ms <;> aesop;
  · rcases ms with ( _ | ⟨ m, ms ⟩ ) <;> norm_num at *;
    -- By the properties of logarithms and primes, we can separate the sum into two parts:
    -- one involving $p$ and the other involving the primes in $ps$.
    have h_separated : (Real.log (p ^ m.toNat * (prodPrimePow ps (ms.map Int.toNat)))) = (Real.log (p ^ (-m).toNat * (prodPrimePow ps (ms.map (fun m => (-m).toNat))))) := by
      have h_separated : (List.zipWith (fun p m => m * Real.log p) (List.flatMap (fun a => [↑a]) ps) (List.flatMap (fun a => [↑a]) ms)).sum = (Real.log (prodPrimePow ps (ms.map Int.toNat))) - (Real.log (prodPrimePow ps (ms.map (fun m => (-m).toNat)))) := by
        have h_separated : ∀ (ps : List ℕ) (ms : List ℤ), (∀ p ∈ ps, Nat.Prime p) → List.length ps = List.length ms → (List.zipWith (fun p m => m * Real.log p) (List.flatMap (fun a => [↑a]) ps) (List.flatMap (fun a => [↑a]) ms)).sum = Real.log (prodPrimePow ps (ms.map Int.toNat)) - Real.log (prodPrimePow ps (ms.map (fun m => (-m).toNat))) := by
          intros ps ms hprimes hlen; induction' ps with p ps ih generalizing ms; aesop;
          rcases ms with ( _ | ⟨ m, ms ⟩ ) <;> norm_num at *;
          rw [ ih ms hprimes.2 hlen, Real.log_mul, Real.log_mul ] <;> norm_cast <;> norm_num [ hprimes.1.ne_zero ];
          · cases m <;> norm_num ; ring;
            ring;
          · norm_num [ List.mem_iff_get ];
            exact fun x hx => absurd hx <| Nat.Prime.ne_zero <| hprimes.2 _ <| by simp;
          · norm_num [ List.mem_iff_get ];
            exact fun x hx => absurd hx <| Nat.Prime.ne_zero <| hprimes.2 _ <| by simp;
        exact h_separated ps ms hprimes.2 hlen;
      rcases m with ( _ | m ) <;> norm_num at *;
      · rw [ Real.log_mul ] <;> norm_cast <;> norm_num [ hprimes.1.ne_zero ];
        · linarith;
        · norm_num [ List.mem_iff_get ];
          exact fun x hx => absurd hx <| Nat.Prime.ne_zero <| hprimes.2 _ <| by simp;
      · rw [ Real.log_mul ] <;> norm_cast <;> norm_num [ hprimes.1.ne_zero ];
        · linarith;
        · norm_num [ List.mem_iff_get ];
          exact fun x hx => absurd hx <| Nat.Prime.ne_zero <| hprimes.2 _ <| by simp;
    -- Since the logarithm function is injective, we can equate the arguments:
    have h_eq : (p ^ m.toNat * (prodPrimePow ps (ms.map Int.toNat))) = (p ^ (-m).toNat * (prodPrimePow ps (ms.map (fun m => (-m).toNat)))) := by
      apply_fun Real.exp at h_separated ; rw [ Real.exp_log, Real.exp_log ] at h_separated <;> norm_cast at *;
      · refine' mul_pos ( pow_pos hprimes.1.pos _ ) _;
        convert prod_prime_pow_pos ps ( List.map ( fun m => ( -m |> Int.toNat ) ) ms ) hprimes.2 _;
        · norm_cast;
        · aesop;
      · exact mul_pos ( pow_pos hprimes.1.pos _ ) ( by exact_mod_cast prod_prime_pow_pos ps _ ( by aesop ) ( by aesop ) );
    -- Since $p$ is prime and does not divide any element in $ps$, it must divide the product on the right-hand side.
    by_cases hm : m.toNat > 0;
    · have h_div : p ∣ prodPrimePow ps (ms.map (fun m => (-m).toNat)) := by
        rcases m with ( _ | m ) <;> norm_num at *;
        exact h_eq ▸ dvd_mul_of_dvd_left ( dvd_pow_self _ hm.ne' ) _;
      exact absurd h_div ( prime_ndvd_prod_pow_of_nmem p ps ( List.map ( fun m => ( -m ).toNat ) ms ) hprimes.1 hprimes.2 hnodup.1 ( by simp +decide [ hlen ] ) );
    · cases m <;> norm_num at *;
      · aesop;
      · -- Since $p$ is prime and does not divide any element in $ps$, it must divide the product on the left-hand side.
        have h_div : p ∣ prodPrimePow ps (ms.map Int.toNat) := by
          exact h_eq.symm ▸ dvd_mul_of_dvd_left ( dvd_pow_self _ ( Nat.succ_ne_zero _ ) ) _;
        exact prime_ndvd_prod_pow_of_nmem p ps ( List.map Int.toNat ms ) hprimes.1 hprimes.2 hnodup.1 ( by simpa using hlen ) h_div

/-
The logarithms of distinct primes are Q-linearly independent.
-/
theorem log_primes_Q_independent
    (ps : List ℕ) (qs : List ℚ)
    (hprimes : ∀ p ∈ ps, Nat.Prime p)
    (hnodup : ps.Nodup)
    (hlen : ps.length = qs.length)
    (hsum : (List.zipWith (fun p q => q * Real.log (p : ℝ)) ps qs).sum = 0) :
    ∀ q ∈ qs, q = 0 := by
  -- Multiply the entire sum equation by D := qs.map (fun q => (q.den : ℤ)) |>.prod. This is a positive integer (product of positive natural numbers cast to ℤ).
  set D := qs.map (fun q => (q.den : ℤ)) |>.prod with hD_def;
  -- By multiplying through by D, we get a new equation where all coefficients are integers.
  have hsum_int : List.sum (List.zipWith (fun p m => (m : ℝ) * Real.log (p : ℝ)) ps (qs.map (fun q => D * q))) = 0 := by
    have hsum_int : List.sum (List.zipWith (fun p m => (m : ℝ) * Real.log (p : ℝ)) ps (qs.map (fun q => D * q))) = D * List.sum (List.zipWith (fun p q => (q : ℝ) * Real.log (p : ℝ)) ps qs) := by
      have hsum_int : ∀ (L : List ℕ) (M : List ℚ), List.length L = List.length M → List.sum (List.zipWith (fun p m => (m : ℝ) * Real.log (p : ℝ)) L (List.map (fun q => D * q) M)) = D * List.sum (List.zipWith (fun p q => (q : ℝ) * Real.log (p : ℝ)) L M) := by
        intros L M hlen; induction' L with p L ih generalizing M <;> cases M <;> simp_all +decide [ mul_assoc, mul_comm, mul_left_comm, List.zipWith ] ;
        ring;
      exact hsum_int ps qs hlen;
    aesop;
  -- By definition of $D$, we know that $D * q$ is an integer for all $q \in qs$.
  have h_int : ∀ q ∈ qs, ∃ m : ℤ, D * q = m := by
    intro q hq
    use D * q.num / q.den;
    rw [ Int.cast_div ] <;> norm_num;
    · simp +decide [ mul_div_assoc, Rat.num_div_den ];
    · exact dvd_mul_of_dvd_left ( List.dvd_prod ( List.mem_map.mpr ⟨ q, hq, rfl ⟩ ) ) _;
  -- Apply the integer linear independence result to conclude that each $D * q = 0$.
  have h_zero : ∀ q ∈ qs, D * q = 0 := by
    choose! m hm using h_int;
    convert int_log_primes_independent ps ( List.map m qs ) hprimes hnodup ?_ ?_;
    · aesop;
    · aesop;
    · convert hsum_int using 3;
      norm_num [ List.map_flatMap ];
      rw [ List.flatMap_map ];
      exact List.flatMap_congr fun x hx => by specialize hm x hx; norm_cast at *; aesop;
  aesop