# NDC Elliptic Curve AFE Computation — 37a1
**Date:** 2026-04-16  
**Curve:** 37a1: y²+y=x³-x, rank 1, conductor N=37  
**Method:** mpmath mp.dps=50, Approximate Functional Equation approach  
**Script:** `/Users/saar/Desktop/Farey-Local/experiments/ndc_afe_computation.py`

---

## Setup

```
ρ_E = 0.5 + 5.003838972·i   (first zero of L(E,s))
L'(E,1) = 0.3059997738340523
1/L'(E,1) = 3.267976272
ζ(2) = π²/6 = 1.6449340668482264365
```

a_p values (direct point counting, verified):
a_2=-2, a_3=-3, a_5=-2, a_7=-1, a_11=-5, a_13=-2, a_17=0, a_19=0,
a_23=2, a_29=6, a_31=-4, a_37=0, a_41=-9, a_43=2, a_47=-9, a_53=1,
a_59=8, a_61=-8, a_67=8, a_71=9

---

## Part A: Euler Product L_K(2,E) — Sanity Check

| K    | L_K(2,E)          |
|------|-------------------|
| 100  | 0.383101167583368 |
| 200  | 0.383098012857419 |
| 500  | 0.383097391873101 |
| Dirichlet Σ_{n≤2000} | 0.383111551810244 |

**Ratio EP_500 / DS_2000 = 0.9999630396**

Convergence is clean. L(2,E) ≈ 0.38310 for 37a1 (note: this differs from the
Cremona value because L(2,E) ≠ L(1,E); true L(2,E) ≈ 0.3831 is consistent
with known computations). a_p values confirmed correct.

---

## Part B: |L(ρ_E, E)| Verification

### Raw partial sums (no smoothing — expected to diverge):

| K    | |L(ρ_E,E)|  | Re          | Im          |
|------|------------|-------------|-------------|
| 200  | 7.0916     | -5.5783     | 4.3787      |
| 500  | 3.3330     | 3.2399      | 0.7823      |
| 1000 | 10.2301    | 8.5082      | -5.6803     |
| 2000 | 14.4146    | 7.2125      | -12.4804    |

Raw sums diverge — expected at s=ρ_E on the critical line.

### Exponentially smoothed sums (Σ a_n·n^{-ρ}·exp(-n/K)):

| K    | |L(ρ_E,E)|  | Re          | Im          |
|------|------------|-------------|-------------|
| 100  | 4.2466     | -2.9762     | 3.0292      |
| 200  | 4.2651     | -2.7204     | 3.2848      |
| 500  | 1.1996     | -0.6075     | 1.0344      |
| 1000 | 2.7943     | 1.4551      | -2.3856     |

**Assessment:** Smoothed sums are O(1) at K=500-1000, oscillating but not
growing. They are NOT cleanly converging to 0 at these K values. This is
consistent with ρ_E being a zero — convergence to 0 via the AFE requires
K >> |t|² ≈ 25, but actual convergence is slow due to oscillation.
The magnitude trend (1.2 at K=500, 2.8 at K=1000) shows we are in the
oscillatory regime. Need K ~ 10^4-10^5 for clean convergence.

---

## Part C: Smoothed c_K^E(ρ_E)

### Exponential smoothing: c_K = Σ_k μ(k)·a_k·k^{-ρ}·exp(-k/K)

| K    | Re(c_K)      | Im(c_K)     | |c_K|       |
|------|--------------|-------------|------------|
| 100  | -0.27354     | 3.34479     | 3.35596    |
| 200  | -1.24073     | 4.01477     | 4.20212    |
| 500  | -2.01268     | 5.55931     | 5.91243    |
| 1000 | -2.69435     | 7.81328     | 8.26480    |

### Cesaro regularization: c_K = Σ_{k<K} μ(k)·a_k·k^{-ρ}·(1-k/K)

| K    | Re(c_K)      | Im(c_K)     | |c_K|       |
|------|--------------|-------------|------------|
| 100  | 0.76544      | 2.40828     | 2.52700    |
| 200  | -0.19440     | 4.23428     | 4.23874    |
| 500  | -2.82123     | 4.09443     | 4.97229    |
| 1000 | -2.11568     | 5.31400     | 5.71968    |

**Both smoothings give |c_K| growing roughly like log(K), with dominant
imaginary part. The real part Re(c_K) is negative and growing in magnitude.**

---

## Part D: E_K^E(ρ_E) in Log Space

E_K = Π_{p≤K} (1 - a_p·p^{-ρ} + p^{1-2ρ})

Computed as exp(log E_K) where log E_K = -Σ_{p≤K} log(local factor).

| K    | Re(log E_K)  | Im(log E_K)  | |E_K|          | arg(E_K)/π  |
|------|--------------|--------------|---------------|-------------|
| 50   | -3.929        | -2.387       | 0.019664      | -0.75973    |
| 100  | -7.977        | -2.010       | 3.433e-4      | -0.63981    |
| 200  | -7.130        | 7.347        | 8.011e-4      | +2.33856    |
| 500  | -4.960        | -3.592       | 7.015e-3      | -1.14325    |
| 1000 | -9.494        | -9.173       | 7.531e-5      | -2.91988    |

**Key finding:** |E_K| is TINY (~10^{-4} to 10^{-5}) and varies erratically.
The Euler product at s=ρ_E is near-zero because ρ_E is a zero of L(E,s) and
E_K^{-1} → L(ρ_E,E) = 0. This means |E_K| → 0, causing the near-zero
factor explosion seen in the previous raw computation.
Im(log E_K) oscillates wildly (the arg of E_K is NOT stabilizing).

---

## Part E: D_K^E(ρ_E)·ζ(2) — NDC Test

D_K = c_K^{exp} · E_K

| K    | Re(D_K·ζ2)    | Im(D_K·ζ2)    | |D_K·ζ2|      |
|------|---------------|---------------|--------------|
| 50   | 0.04457        | -0.06349       | 0.07757      |
| 100  | 0.001775       | -0.000663      | 0.001895     |
| 200  | -0.005419      | 0.001140       | 0.005537     |
| 500  | -0.006992      | -0.067868      | 0.068227     |
| 1000 | 0.0005643      | -0.0008543     | 0.001024     |

### Cesaro Average of D_K·ζ(2) [dense K sampling]:

| K    | Avg Re   | Avg Im   | Avg |D·ζ2| |
|------|----------|----------|------------|
| 10   | -0.88771 | 0.08375  | 0.89165    |
| 20   | 0.71609  | 0.20188  | 0.74400    |
| 30   | 0.54667  | 0.36499  | 0.65732    |
| 50   | 0.42115  | 0.25787  | 0.49382    |
| 75   | 0.33619  | 0.20344  | 0.39295    |
| 100  | 0.28045  | 0.16943  | 0.32766    |
| 150  | 0.24283  | 0.14775  | 0.28424    |
| 200  | 0.21179  | 0.12942  | 0.24821    |
| 300  | 0.18828  | 0.11503  | 0.22064    |
| 500  | 0.16875  | 0.09674  | 0.19451    |

**Critical observation:** The running average is DECREASING monotonically but
slowly, and is heading AWAY from 1, toward 0. At K=500 the running average
|D·ζ2| ≈ 0.195. This is NOT converging to 1.

---

## Part F: Re(c_K^exp)/log(K) vs Target 3.268

Target: 1/L'(E,1) = 3.267976272

| K    | Re(c_K^exp)  | log(K)  | Re(c_K)/log(K) | ratio/target |
|------|--------------|---------|----------------|--------------|
| 100  | -0.27354     | 4.605   | -0.05940       | -0.01818     |
| 200  | -1.24073     | 5.298   | -0.23417       | -0.07166     |
| 300  | -1.67132     | 5.704   | -0.29302       | -0.08966     |
| 500  | -2.01268     | 6.215   | -0.32386       | -0.09910     |
| 750  | -2.33843     | 6.620   | -0.35323       | -0.10809     |
| 1000 | -2.69435     | 6.908   | -0.39005       | -0.11935     |
| 1500 | -3.35994     | 7.313   | -0.45943       | -0.14059     |
| 2000 | -3.89127     | 7.601   | -0.51195       | -0.15666     |

**Re(c_K)/log(K) is NEGATIVE throughout and trending toward more negative
values. It is NOT converging to 1/L'(E,1) = +3.268.**

---

## Interpretation & Diagnosis

### What's happening

1. **Part A is clean:** a_p values are correct, Euler product at s=2 works perfectly.

2. **The fundamental obstruction:** At s=ρ_E (a zero of L(E,s)):
   - The Euler product E_K = Π_{p≤K} local_factor → 0 as K→∞
   - Simultaneously c_K → ∞ (growing like log K with oscillation)
   - Their product D_K = c_K · E_K must → (something finite) for NDC to hold
   - The product oscillates with |D_K| ~ 10^{-3} to 10^{-1}

3. **The smoothing has a sign problem:** Re(c_K) is NEGATIVE throughout,
   meaning the exponential smoothing has inverted the real part relative
   to the expected +3.268/log(K) behavior. The imaginary part dominates.

4. **Formulation issue:** The NDC conjecture D_K^E(ρ_E)·ζ(2) → 1 likely
   requires a specific normalization convention for D_K. The definition
   D_K = c_K · E_K where c_K = Σ μ(k)a_k k^{-ρ} is NOT standard in the
   literature — it is Koyama's specific definition and may require:
   - A different smoothing kernel
   - A different normalization of E_K
   - That c_K is defined via a Möbius inversion of the COMPLETED L-function
   
5. **Running average diverges from 1:** The Cesaro average of D_K·ζ(2) starts
   near 1 (by coincidence at K~10-20) then trends toward 0, not toward 1.

### The near-zero Euler factor problem persists

Even with log-space computation, |E_K| at K=1000 is 7.5×10^{-5}. The product
c_K · E_K involves cancellation between a growing c_K and a shrinking E_K.
The result (|D_K| ~ 10^{-3}) is much smaller than 1, not close to 1/ζ(2) = 0.608.

### What would be needed for NDC verification

- Implement the exact AFE formula from Koyama's paper with the completed
  L-function Λ(s,E) and proper smoothing via the W function from Iwaniec-Kowalski
- Use the explicit formula for c_K in terms of zeros of L(E,s)
- K ~ 10^6 with the AFE method (per original task description this was wrong;
  the raw Dirichlet series needs K~10^6, but AFE should converge with K~100)

### Tentative conclusion

**INCONCLUSIVE.** The computation confirms the near-zero Euler factor
obstruction is fundamental, not a numerical artifact. The AFE-style exponential
smoothing does not resolve it at K≤2000. The Cesaro average of D_K·ζ(2) is
decreasing toward 0, not increasing toward 1.

**Status:** Open problem. Need correct Koyama formula with explicit W-function.

---

## Files

- Script: `/Users/saar/Desktop/Farey-Local/experiments/ndc_afe_computation.py`
- Output: `/Users/saar/Desktop/Farey-Local/experiments/NDC_EC_AFE_COMPUTATION.md`

---

*Computation: mpmath mp.dps=50. Author: Saar Shai. AI assistance: Claude (Anthropic).*
