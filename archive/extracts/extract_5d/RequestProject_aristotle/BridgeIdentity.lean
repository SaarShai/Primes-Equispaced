import Mathlib
import PrimeCircle

/-!
# The Bridge Identity

For every prime p >= 2,
  Sigma_{f in F_{p-1}} e^{2 pi i p f} = M(p) + 2

where F_{p-1} is the Farey sequence of order p-1 and M(p) is the Mertens function.

## Proof strategy

1. The Farey exponential sum decomposes by denominator q:
   Sigma_{(a,q) in fareySet(p-1)} e^{2 pi i p a/q} = Sigma_{q=1}^{p-1} c_q(p)
   where c_q(p) is the Ramanujan sum.

2. For q >= 2 with gcd(q,p) = 1 (which holds since p is prime and q < p):
   c_q(p) = mu(q).
   This follows because multiplication by p permutes the coprime residues mod q.

3. The q=1 term contributes 2 (from a=0 and a=1).

4. Summing: 2 + Sigma_{q=2}^{p-1} mu(q) = 2 + M(p-1) - mu(1) = M(p-1) + 1.

5. Since mu(p) = -1 for primes: M(p) = M(p-1) + mu(p) = M(p-1) - 1,
   so M(p-1) = M(p) + 1, giving the result M(p) + 2.
-/

open Finset BigOperators Complex

/-! ## The Mertens function -/

/-- The Mertens function M(n) = Sigma_{k=1}^{n} mu(k). -/
def mertens (n : ℕ) : ℤ :=
  ∑ k ∈ Finset.Icc 1 n, ArithmeticFunction.moebius k

/-! ## Generalized Ramanujan sum -/

/-- The generalized Ramanujan sum c_q(m) = Sigma_{a coprime to q, 0 <= a < q} exp(2 pi i a m / q). -/
noncomputable def ramanujanSumGen (q m : ℕ) : ℂ :=
  ∑ a ∈ (Finset.range q).filter (fun a => Nat.Coprime a q),
    exp (2 * ↑Real.pi * I * (↑a : ℂ) * (↑m : ℂ) / (↑q : ℂ))

/-- The standard Ramanujan sum c_q(1) agrees with ramanujanSum from PrimeCircle. -/
lemma ramanujanSumGen_one (q : ℕ) : ramanujanSumGen q 1 = ramanujanSum q := by
  simp only [ramanujanSumGen, ramanujanSum, Nat.cast_one]
  congr 1
  ext a
  ring

/-! ## Key permutation lemma -/

/-
PROBLEM
Multiplication by a coprime integer permutes the coprime residue classes mod b.
    This is the fundamental fact that {a*p mod b : gcd(a,b)=1} = {a : gcd(a,b)=1}
    when gcd(p,b) = 1.

PROVIDED SOLUTION
Show the image equals the original set by proving it's a subset and has the same cardinality (via injectivity). For subset: if a is coprime to b and a < b, then a*p % b < b and a*p % b is coprime to b (coprimality preserved under multiplication by coprime p and mod). For injectivity: if a₁*p ≡ a₂*p (mod b) and gcd(p,b)=1, cancel p to get a₁ ≡ a₂ (mod b), and since both are < b, a₁ = a₂. Use Nat.ModEq for modular arithmetic and ZMod or Nat.Coprime cancellation lemmas.
-/
lemma coprime_mul_perm (b p : ℕ) (hb : 0 < b) (hcop : Nat.Coprime p b) :
    (Finset.filter (fun a => Nat.Coprime a b) (Finset.range b)).image (fun a => a * p % b) =
    Finset.filter (fun a => Nat.Coprime a b) (Finset.range b) := by
  -- To prove the equality of sets, we show mutual inclusion.
  apply Finset.ext
  intro a
  simp [Finset.mem_image];
  constructor;
  · rintro ⟨ a, ⟨ ha₁, ha₂ ⟩, rfl ⟩;
    exact ⟨ Nat.mod_lt _ hb, by rw [ Nat.coprime_iff_gcd_eq_one ] at *; rw [ ← Nat.gcd_rec, Nat.gcd_comm ] ; exact Nat.Coprime.mul_left ha₂ hcop ⟩;
  · intro ha
    obtain ⟨a', ha'⟩ : ∃ a', a' * p ≡ a [MOD b] ∧ a' < b ∧ Nat.Coprime a' b := by
      -- Since $p$ is coprime to $b$, there exists an $a'$ such that $a' * p ≡ a \pmod{b}$.
      obtain ⟨a', ha'⟩ : ∃ a', a' * p ≡ a [MOD b] := by
        -- Since $p$ is coprime to $b$, there exists an $a'$ such that $a' * p ≡ 1 \pmod{b}$.
        obtain ⟨a', ha'⟩ : ∃ a', a' * p ≡ 1 [MOD b] := by
          have := Nat.exists_mul_mod_eq_one_of_coprime hcop;
          rcases b with ( _ | _ | b ) <;> simp_all +decide [ mul_comm, Nat.ModEq ];
          · exact ⟨ 0, by norm_num ⟩;
          · exact ⟨ this.choose, this.choose_spec.2 ⟩;
        exact ⟨ a * a', by simpa [ mul_assoc, mul_comm, mul_left_comm ] using ha'.mul_left a ⟩;
      refine' ⟨ a' % b, _, _, _ ⟩;
      · simpa [ Nat.ModEq, Nat.mul_mod ] using ha';
      · exact Nat.mod_lt _ hb;
      · -- Since $a' * p \equiv a \pmod{b}$ and $\gcd(a, b) = 1$, it follows that $\gcd(a', b) = 1$.
        have h_coprime : Nat.Coprime (a' * p) b := by
          exact ha'.gcd_eq.trans ha.2;
        rw [ Nat.coprime_mul_iff_left ] at h_coprime ; aesop;
    exact ⟨ a', ⟨ ha'.2.1, ha'.2.2 ⟩, ha'.1.symm ▸ Nat.mod_eq_of_lt ha.1 ⟩

/-! ## Ramanujan sum at coprime argument -/

/-
PROBLEM
The Ramanujan sum at a coprime argument equals the Ramanujan sum at 1.
    c_q(m) = c_q(1) when gcd(m, q) = 1.
    This is because multiplication by m permutes the coprime residues mod q,
    so Sigma_{gcd(a,q)=1} exp(2pi i am/q) = Sigma_{gcd(a,q)=1} exp(2pi i a/q).

PROVIDED SOLUTION
Use the permutation lemma coprime_mul_perm to show that the map a ↦ a*m % q is a bijection on the coprime residues mod q. Then use Finset.sum_bij or Finset.sum_nbij to rewrite the sum. Each term exp(2πi (a*m) / q) needs to equal exp(2πi (a*m % q) / q) * exp(2πi k) for some integer k, which equals exp(2πi (a*m % q) / q) since exp(2πi k) = 1. The key identity is: a*m/q = (a*m % q)/q + (a*m / q), so exp(2πi a*m/q) = exp(2πi (a*m%q)/q) * exp(2πi ⌊a*m/q⌋). Then the sum over a of exp(2πi a*m/q) = sum over a of exp(2πi (a*m%q)/q) = sum over b in coprime_residues of exp(2πi b/q) = ramanujanSum q, where b = a*m % q ranges over the same set by coprime_mul_perm.
-/
theorem ramanujanSumGen_coprime (q m : ℕ) (hq : 0 < q) (hcop : Nat.Coprime m q) :
    ramanujanSumGen q m = ramanujanSum q := by
  -- The sum over a coprime to q of exp(2pi i am / q) equals
  -- the sum over a coprime to q of exp(2pi i a / q)
  -- because a -> a*m mod q is a bijection on the coprime residues.
  -- The exponentials match because a*m ≡ a*m mod q (mod q),
  -- so exp(2pi i (am) / q) = exp(2pi i (am mod q) / q) * exp(2pi i k) for integer k.
  convert Finset.sum_bij ( fun a _ => a * m % q ) _ _ _ _ using 2;
  · simp +contextual [ Nat.mod_lt _ hq ];
    exact fun a ha ha' => ha'.mul_left hcop;
  · intro a₁ ha₁ a₂ ha₂ h_eq
    have h_cong : a₁ * m ≡ a₂ * m [MOD q] := by
      exact h_eq;
    have h_cancel : a₁ ≡ a₂ [MOD q] := by
      rw [ Nat.modEq_iff_dvd ] at *;
      simp_all +decide [ ← sub_mul ];
      exact Int.dvd_of_dvd_mul_left_of_gcd_one h_cong hcop.symm;
    exact Nat.mod_eq_of_lt ( Finset.mem_range.mp ( Finset.mem_filter.mp ha₁ |>.1 ) ) ▸ Nat.mod_eq_of_lt ( Finset.mem_range.mp ( Finset.mem_filter.mp ha₂ |>.1 ) ) ▸ h_cancel;
  · intro b hb; have := coprime_mul_perm q m hq hcop; rw [ Finset.ext_iff ] at this; specialize this b; aesop;
  · intro a ha; rw [ Complex.exp_eq_exp_iff_exists_int ] ; use ( a * m ) / q; push_cast; ring;
    rw [ Nat.mod_def ] ; ring;
    rw [ Nat.cast_sub ( Nat.mul_div_le _ _ ) ] ; push_cast ; ring;
    norm_num [ hq.ne' ];
    norm_cast ; ring

/-- Combining with ramanujan_sum_one: c_q(m) = mu(q) when gcd(m,q)=1 and q >= 1. -/
theorem ramanujanSumGen_coprime_eq_moebius (q m : ℕ) (hq : 1 ≤ q) (hcop : Nat.Coprime m q) :
    ramanujanSumGen q m = ↑(ArithmeticFunction.moebius q : ℤ) := by
  rw [ramanujanSumGen_coprime q m (by omega) hcop, ramanujan_sum_one q hq]

/-! ## Farey exponential sum -/

/-- The Farey exponential sum over F_N evaluated at frequency p. -/
noncomputable def fareyExpSumBridge (N p : ℕ) : ℂ :=
  ∑ ab ∈ fareySet N, exp (2 * ↑Real.pi * I * (↑p : ℂ) * (↑ab.1 : ℂ) / (↑ab.2 : ℂ))

/-! ## Auxiliary lemmas -/

/-- For 1 <= q < p with p prime, we have gcd(q, p) = 1. -/
lemma coprime_of_lt_prime (q p : ℕ) (hq : 1 ≤ q) (hqp : q < p) (hp : Nat.Prime p) :
    Nat.Coprime q p := by
  exact (hp.coprime_iff_not_dvd.mpr (fun h => absurd (Nat.le_of_dvd (by omega) h) (not_le.mpr hqp))).symm

/-- exp(2 pi i n) = 1 for any integer n. -/
lemma exp_two_pi_int_mul_I (n : ℤ) :
    exp (2 * ↑Real.pi * I * (↑n : ℂ)) = 1 := by
  rw [show 2 * ↑Real.pi * I * (↑n : ℂ) = ↑n * (2 * ↑Real.pi * I) from by ring]
  rw [Complex.exp_int_mul]
  simp [Complex.exp_two_pi_mul_I]

/-- The Mertens function satisfies M(n) = M(n-1) + mu(n) for n >= 2. -/
lemma mertens_succ (n : ℕ) (hn : 2 ≤ n) :
    mertens n = mertens (n - 1) + ArithmeticFunction.moebius n := by
  unfold mertens
  have h1 : Finset.Icc 1 n = Finset.Icc 1 (n - 1) ∪ {n} := by
    ext x; simp only [Finset.mem_Icc, Finset.mem_union, Finset.mem_singleton]; omega
  rw [h1, Finset.sum_union]
  · simp
  · simp only [Finset.disjoint_singleton_right, Finset.mem_Icc, not_and, not_le]
    intro _; omega

/-- mu(p) = -1 for prime p. -/
lemma moebius_prime (p : ℕ) (hp : Nat.Prime p) :
    (ArithmeticFunction.moebius p : ℤ) = -1 :=
  ArithmeticFunction.moebius_apply_prime hp

/-- M(p-1) = M(p) + 1 for prime p. -/
lemma mertens_pred_prime (p : ℕ) (hp : Nat.Prime p) :
    mertens (p - 1) = mertens p + 1 := by
  have h2 := mertens_succ p hp.two_le
  rw [moebius_prime p hp] at h2
  omega

/-- mu(1) = 1. -/
lemma moebius_one : (ArithmeticFunction.moebius 1 : ℤ) = 1 :=
  ArithmeticFunction.moebius_apply_one

/-- M(1) = 1. -/
lemma mertens_one : mertens 1 = 1 := by
  unfold mertens
  simp [moebius_one]

/-! ## Decomposition lemmas for bridge identity -/

/-
PROBLEM
fareyExpSumBridge decomposes as a sum over denominators q ∈ [1,N].

PROVIDED SOLUTION
Unfold fareyExpSumBridge and fareySet. The fareySet is a filtered product set. Rewrite the sum over the filtered product as an iterated sum: first sum over q (second coordinate), then sum over a (first coordinate). Use Finset.sum_sigma' or Finset.sum_biUnion or Finset.sum_product to decompose. The key is that fareySet N = {(a,q) : q ∈ Icc 1 N, a ∈ range(q+1), Coprime a q} since a ≤ q ≤ N implies a ∈ range(N+1) automatically. So the sum over fareySet equals the iterated sum ∑_q ∑_{a coprime to q, a ≤ q} f(a,q).
-/
lemma fareyExpSum_eq_sum_by_denom (N p : ℕ) :
    fareyExpSumBridge N p =
    ∑ q ∈ Finset.Icc 1 N,
      ∑ a ∈ (Finset.range (q + 1)).filter (fun a => Nat.Coprime a q),
        exp (2 * ↑Real.pi * I * (↑p : ℂ) * (↑a : ℂ) / (↑q : ℂ)) := by
  -- Let's unfold the definition of `fareyExpSumBridge` using the definition of `fareySet`.
  have h_fareySet : fareySet N = Finset.biUnion (Finset.Icc 1 N) (fun q => Finset.image (fun a => (a, q)) (Finset.filter (fun a => Nat.Coprime a q) (Finset.range (q + 1)))) := by
    ext ⟨a, q⟩; simp [fareySet];
    grind;
  unfold fareyExpSumBridge; rw [ h_fareySet, Finset.sum_biUnion ] ; aesop;
  exact fun a ha b hb hab => Finset.disjoint_left.mpr fun x hx₁ hx₂ => hab <| by aesop;

/-
PROBLEM
For q ≥ 2, the coprime residues in {0,...,q} equal those in {0,...,q-1}
    since gcd(q,q) = q ≥ 2 ≠ 1.

PROVIDED SOLUTION
Show the two sets are equal by ext. An element a is in (range(q+1)).filter(coprime · q) iff a < q+1 and coprime a q, i.e., a ≤ q and coprime a q. An element a is in (range q).filter(coprime · q) iff a < q and coprime a q. The only difference is a = q, but coprime q q = (q = 1), which is false since q ≥ 2. So both sets are {a : a < q, coprime a q}.
-/
lemma coprime_filter_range_succ (q : ℕ) (hq : 2 ≤ q) :
    (Finset.range (q + 1)).filter (fun a => Nat.Coprime a q) =
    (Finset.range q).filter (fun a => Nat.Coprime a q) := by
  grind

/-
PROBLEM
The q=1 contribution to the Farey exponential sum is 2.

PROVIDED SOLUTION
Evaluate the finite sum. range 2 = {0, 1}. Both 0 and 1 are coprime to 1. So the filter gives {0, 1}. The sum is exp(2πi·p·0/1) + exp(2πi·p·1/1) = exp(0) + exp(2πi·p) = 1 + 1 = 2. For exp(0) = 1, use Complex.exp_zero after showing the argument is 0 (since a=0). For exp(2πi·p) = 1, use exp_two_pi_int_mul_I or Complex.exp_int_mul_two_pi_mul_I. Then 1 + 1 = 2.
-/
lemma farey_denom_one_sum (p : ℕ) :
    ∑ a ∈ (Finset.range 2).filter (fun a => Nat.Coprime a 1),
      exp (2 * ↑Real.pi * I * (↑p : ℂ) * (↑a : ℂ) / (↑(1 : ℕ) : ℂ)) = 2 := by
  norm_num [ Finset.sum_filter, Finset.sum_range_succ ];
  rw [ Complex.exp_eq_one_iff.mpr ⟨ p, by push_cast; ring ⟩ ] ; ring

/-
PROBLEM
For q ≥ 2, the inner sum over the Farey set equals ramanujanSumGen q p.

PROVIDED SOLUTION
Use coprime_filter_range_succ to rewrite (range(q+1)).filter(coprime · q) as (range q).filter(coprime · q). Then the sum becomes exactly ramanujanSumGen q p by definition, after noting that the summand exp(2πi·p·a/q) can be rewritten as exp(2πi·a·p/q) by commutativity of multiplication (the order of p and a in the product).
-/
lemma farey_denom_ge2_eq_ramanujan (q p : ℕ) (hq : 2 ≤ q) :
    ∑ a ∈ (Finset.range (q + 1)).filter (fun a => Nat.Coprime a q),
      exp (2 * ↑Real.pi * I * (↑p : ℂ) * (↑a : ℂ) / (↑q : ℂ)) =
    ramanujanSumGen q p := by
  rw [ coprime_filter_range_succ q hq ];
  exact Finset.sum_congr rfl fun x hx => by ring;

/-
PROBLEM
Sum of μ over Icc 2 N equals mertens N - 1, for N ≥ 1.

PROVIDED SOLUTION
Unfold mertens as Σ_{k ∈ Icc 1 N} μ(k). Split Icc 1 N = {1} ∪ Icc 2 N (for N ≥ 1). Then mertens N = μ(1) + Σ_{q ∈ Icc 2 N} μ(q) = 1 + Σ_{q ∈ Icc 2 N} μ(q). So Σ_{q ∈ Icc 2 N} μ(q) = mertens N - 1.
-/
lemma sum_moebius_Icc_2 (N : ℕ) (hN : 1 ≤ N) :
    ∑ q ∈ Finset.Icc 2 N, (ArithmeticFunction.moebius q : ℤ) = mertens N - 1 := by
  unfold mertens;
  erw [ Finset.sum_Ico_eq_sub _ _, Finset.sum_Ico_eq_sub _ _ ] <;> norm_num [ hN ];
  · native_decide +revert;
  · linarith

/-! ## The Bridge Identity -/

/-
PROBLEM
**The Bridge Identity** (formal statement):
    For every prime p >= 2,
      Sigma_{(a,b) in fareySet(p-1)} exp(2 pi i p a/b) = mertens(p) + 2

    This is the key identity connecting Farey sequences to the Mertens function.

    Proof outline:
    1. Decompose fareySet(p-1) by denominator q into q=1 and q in [2, p-1].
    2. The q=1 contribution is 2 (from exp(0) + exp(2pi*i*p) = 1 + 1).
    3. For 2 <= q <= p-1, each denominator contributes c_q(p) = mu(q).
    4. Total = 2 + Sigma_{q=2}^{p-1} mu(q) = 2 + M(p-1) - 1 = M(p-1) + 1 = M(p) + 2.

PROVIDED SOLUTION
Step 1: Rewrite using fareyExpSum_eq_sum_by_denom to get ∑ q ∈ Icc 1 (p-1), (inner sum).
Step 2: Split Icc 1 (p-1) = {1} ∪ Icc 2 (p-1) using Finset.Icc_insert_left (since p ≥ 2 so p-1 ≥ 1). Use Finset.sum_union or Finset.sum_insert.
Step 3: For q=1: the inner sum with q=1 has range(1+1) = range 2. Use farey_denom_one_sum to get 2.
Step 4: For q ∈ Icc 2 (p-1): use farey_denom_ge2_eq_ramanujan to rewrite each inner sum as ramanujanSumGen q p. Then use ramanujanSumGen_coprime_eq_moebius (with coprime_of_lt_prime to get coprimality) to rewrite as μ(q). The coprimality follows from coprime_of_lt_prime since 2 ≤ q ≤ p-1 < p.
Step 5: Use sum_moebius_Icc_2 to get ∑_{q ∈ Icc 2 (p-1)} μ(q) = mertens(p-1) - 1.
Step 6: Use mertens_pred_prime to replace mertens(p-1) with mertens(p) + 1.
Step 7: Algebra: 2 + (mertens(p) + 1 - 1) = mertens(p) + 2.
Key: the cast from ℤ to ℂ needs care. The sum ∑ μ(q) is in ℤ but the exponential sum is in ℂ. Cast the ℤ result to ℂ at the end.
-/
theorem bridge_identity (p : ℕ) (hp : Nat.Prime p) :
    fareyExpSumBridge (p - 1) p = ↑(mertens p) + 2 := by
  -- Apply the decomposition lemma to split the sum into the q=1 term and the sum over q ≥ 2.
  have h_split : fareyExpSumBridge (p - 1) p = 2 + ∑ q ∈ Finset.Icc 2 (p - 1), ramanujanSumGen q p := by
    rw [fareyExpSum_eq_sum_by_denom];
    rw [ Finset.Icc_eq_cons_Ioc, Finset.sum_cons ] <;> norm_num;
    · refine' congrArg₂ ( · + · ) _ ( Finset.sum_congr rfl fun q hq => _ ) <;> norm_num [ ramanujanSumGen ];
      · norm_num [ Finset.sum_range_succ ];
        norm_num [ mul_comm ( 2 * Real.pi * Complex.I ) ];
      · rw [ coprime_filter_range_succ q ( by linarith [ Finset.mem_Icc.mp hq ] ) ] ; ac_rfl;
    · exact Nat.sub_pos_of_lt hp.one_lt;
  -- For each q ≥ 2, since gcd(q,p)=1 (because p is prime and q < p), we have ramanujanSumGen q p = μ(q).
  have h_ramanujan : ∀ q ∈ Finset.Icc 2 (p - 1), ramanujanSumGen q p = (ArithmeticFunction.moebius q : ℂ) := by
    intros q hq
    apply ramanujanSumGen_coprime_eq_moebius;
    · linarith [ Finset.mem_Icc.mp hq ];
    · exact hp.coprime_iff_not_dvd.mpr fun h => by have := Nat.le_of_dvd ( by linarith [ Finset.mem_Icc.mp hq ] ) h; linarith [ Finset.mem_Icc.mp hq, Nat.sub_add_cancel hp.pos ] ;
  -- Substitute h_ramanujan into h_split to get the sum of μ(q) over q in [2, p-1].
  have h_sum_moebius : ∑ q ∈ Finset.Icc 2 (p - 1), ramanujanSumGen q p = ∑ q ∈ Finset.Icc 2 (p - 1), (ArithmeticFunction.moebius q : ℂ) := by
    exact Finset.sum_congr rfl h_ramanujan;
  -- Use sum_moebius_Icc_2 to get ∑_{q ∈ Icc 2 (p-1)} μ(q) = mertens(p-1) - 1.
  have h_sum_moebius_Icc_2 : ∑ q ∈ Finset.Icc 2 (p - 1), (ArithmeticFunction.moebius q : ℂ) = (mertens (p - 1) - 1 : ℂ) := by
    have h_sum_moebius_Icc_2 : ∑ q ∈ Finset.Icc 2 (p - 1), (ArithmeticFunction.moebius q : ℤ) = mertens (p - 1) - 1 := by
      convert sum_moebius_Icc_2 ( p - 1 ) ( Nat.sub_pos_of_lt hp.one_lt ) using 1;
    norm_cast;
  -- Use mertens_pred_prime to replace mertens(p-1) with mertens(p) + 1.
  have h_mertens_pred : mertens (p - 1) = mertens p + 1 := by
    exact mertens_pred_prime p hp
  rw [ h_split, h_sum_moebius, h_sum_moebius_Icc_2, h_mertens_pred ] ; push_cast ; ring

/-! ## Computational verification for small primes

We verify M(p) + 2 for small primes, confirming the right-hand side
of the bridge identity. -/

/-- M(2) + 2 = 2. (mu(1) + mu(2) = 1 - 1 = 0, so M(2) = 0.) -/
theorem bridge_rhs_p2 : mertens 2 + 2 = (2 : ℤ) := by native_decide

/-- M(3) + 2 = 1. -/
theorem bridge_rhs_p3 : mertens 3 + 2 = (1 : ℤ) := by native_decide

/-- M(5) + 2 = 0. -/
theorem bridge_rhs_p5 : mertens 5 + 2 = (0 : ℤ) := by native_decide

/-- M(7) + 2 = 0. -/
theorem bridge_rhs_p7 : mertens 7 + 2 = (0 : ℤ) := by native_decide

/-- M(11) + 2 = 0. -/
theorem bridge_rhs_p11 : mertens 11 + 2 = (0 : ℤ) := by native_decide

/-- M(13) + 2 = -1. -/
theorem bridge_rhs_p13 : mertens 13 + 2 = (-1 : ℤ) := by native_decide

/-! ## Proof outline (structured sorry proof)

The full proof of the bridge identity proceeds as follows:

**Step 1.** Decompose fareySet(p-1) by denominator q:
  fareyExpSumBridge(p-1, p) = Sigma_{q=1}^{p-1} (Sigma_{a coprime q, a<=q} exp(2pi i p a/q))

**Step 2.** The inner sum for q >= 2 equals c_q(p) (the Ramanujan sum at argument p),
  after handling the boundary terms a=0 (only for q=1) and a=q.
  For q >= 2, the only a with gcd(a,q)=1 are in {1, ..., q-1} (excluding 0 and q).

**Step 3.** Since p is prime and 2 <= q <= p-1 < p, we have gcd(p,q) = 1.
  By the permutation lemma, c_q(p) = c_q(1) = mu(q).

**Step 4.** The q=1 contribution: fareySet has (0,1) and (1,1), contributing
  exp(0) + exp(2pi i p) = 1 + 1 = 2.

**Step 5.** Total = 2 + Sigma_{q=2}^{p-1} mu(q)
             = 2 + (M(p-1) - mu(1))
             = 2 + (M(p-1) - 1)
             = M(p-1) + 1
             = (M(p) + 1) + 1    [since M(p-1) = M(p) + 1 for prime p]
             = M(p) + 2. QED
-/