#!/usr/bin/env python3
"""
EFFECTIVE ALPHA-RHO ANALYSIS - Part 3

NEW APPROACH: Prove B' > C' directly using a LOWER BOUND on B' that
doesn't require bounding rho.

B' = 2*sum(D*delta) = 2*sum_b S_b where S_b = sum_{a coprime b} D(a/b)*delta(a/b)

Split D = D_lin + D_err where D_lin = mean_D + alpha*(f - mean_f).

B' = 2*sum(D_lin*delta) + 2*sum(D_err*delta)
   = alpha * 2*sum((f-mean_f)*delta) + 2*mean_D*sum(delta) + 2*sum(D_err*delta)

For primes: sum(delta) = 0, so:
B' = alpha * 2*sum_fmf_delta + 2*sum_Derr_delta

Now: 2*sum_fmf_delta / C' = alpha_coeff (computed = 1 for primes).

So B'/C' = alpha + rho, and we need alpha + rho > 1.

THE QUESTION: Can we bound the ABSOLUTE SIZE of sum(D_err*delta)
relative to C', without going through norms?

Direct approach: sum(D_err * delta) = sum_b S_b^err

Each S_b^err = sum_{a coprime b} D_err(a/b) * (a - sigma_p(a))/b

Observation: for b = N (largest denominator), phi(N) = phi(p-1) fractions.
sigma_p(a) = pa mod N. Since p mod N = p - N = 1 (because N = p-1),
we have sigma_p(a) = a mod N = a. So delta(a/N) = 0 for all a coprime to N.
This means S_N^err = 0.

Similarly, for b | N: sigma_p(a) = pa mod b. The permutation structure
depends on p mod b.

KEY QUESTION: For the specific case M(p) = -3, can we exploit the
M condition to get a sign constraint on sum(D_err*delta)?

Let me instead look at this: B' > C' iff sum(D*delta) > sum(delta^2)/2.

Since D(f) = rank - n*f and delta(f) = (a - sigma_p(a))/b:

sum(D*delta) = sum(rank * delta) - n * sum(f * delta)

We know: sum(f*delta) = C'/2 (this is the key identity, verified).

So: sum(D*delta) = sum(rank * delta) - n*C'/2

And: B' = 2*sum(D*delta) = 2*sum(rank*delta) - n*C'

B' > C' iff 2*sum(rank*delta) > (n+1)*C'
iff sum(rank*delta) > (n+1)*C'/2

Or: B'/C' = 2*sum(rank*delta)/C' - n
Need: 2*sum(rank*delta)/C' > n + 1

Hmm, this doesn't simplify things.

Let me try yet another angle: the Dirichlet series connection.

From the q-block decomposition:
Term2 = sum_q M(q) * (K[N/q] - K[N/(q+1)])

where K[m] is a cumulative kernel sum. For M(p) = -3:
- q=1: M(1) = 1, contributes positively
- Large q: M(q) varies, weighted by kernel increments

Can we bound Term2 directly from the Dirichlet representation?

Actually, let me reconsider the problem. The audit identified these gaps:
1. B'/C' = alpha + rho identity: NOT PROVED (just verified) - FIXABLE
2. |rho| = O(sqrt(log N)): NOT PROVED unconditionally - HARD
3. Empirical constants: NOT PROVED - HARD

For gap 1, let me provide the algebraic derivation.

For gap 2, the new insight from the user is:
  We don't need |rho| = O(sqrt(log N)).
  We just need |rho| < alpha - 1.
  The unconditional bound gives |corr| = O(sqrt(log p)).

  But |rho| = 2*|corr|*R where R ~ sqrt(N).
  So |rho| = O(sqrt(N * log p)) which is HUGE.

  The unconditional correlation bound is USELESS for this purpose.

So what CAN we do? Let me see if there's a direct approach...

Actually: let's compute the exact |rho| for LARGER primes using
floating-point and see if the scaling |rho| ~ C*sqrt(log p) continues.
If it does up to p = 20000, and alpha - |rho| > 1 for all these primes,
then we have strong evidence. The analytical gap remains.

But WAIT - the user's message suggests something different. Let me re-read:

"if |corr| <= C_0*sqrt(log p) for an EFFECTIVE constant C_0, then:
  |rho| = 2*|corr|*||D_err||*||delta|| / C'"

But this is wrong! |rho| = 2*sum(D_err*delta)/C' = 2*corr*||D_err||*||delta||/C'
                        = 2*corr*||D_err||/||delta||

NOT divided by C' again. Let me verify...

corr = sum(D_err*delta) / (||D_err|| * ||delta||)
So sum(D_err*delta) = corr * ||D_err|| * ||delta||
And rho = 2*sum(D_err*delta)/C' = 2*corr*||D_err||*||delta||/||delta||^2
        = 2*corr*||D_err||/||delta||

Yes, so |rho| = 2*|corr|*||D_err||/||delta|| = 2*|corr|*R

With the unconditional |corr| <= C*sqrt(log p) and R ~ sqrt(N):
  |rho| <= 2*C*sqrt(log p)*sqrt(N) = O(sqrt(N*log p))

This is indeed too big. The unconditional bound does NOT work.

HOWEVER: there is a subtlety. The unconditional bound says
|corr(D_err, delta)| = O(sqrt(log p))

But the CORRELATION is always between -1 and 1! So O(sqrt(log p)) as
an upper bound only makes sense if the implicit constant is < 1/sqrt(log p).

Wait -- re-reading the decorrelation proof line 725:
"|corr| <= N/sqrt(C) ~ N * sqrt(24 log N)/N = O(sqrt(log N))"

So the bound is |corr| <= c * sqrt(log N) for some c.
But since |corr| <= 1 always, we need c * sqrt(log N) < 1 to be nontrivial,
i.e., this bound is only useful for c < 1/sqrt(log N), which means
it's NOT an effective bound at all! It's weaker than the trivial |corr| <= 1.

Actually no -- O(sqrt(log N)) means there exists C such that
|corr| <= C * sqrt(log N). If C ~ 0.3, then for N = 178 (p=179),
C*sqrt(log 178) ~ 0.3 * 2.3 = 0.69 < 1. That's nontrivial.

But for N > e^{1/C^2} ~ e^{11} ~ 60000, the bound exceeds 1 and
becomes vacuous!

So the "unconditional" bound is only useful for SMALL N. For large N,
it's worse than the trivial |corr| <= 1.

CONCLUSION: The unconditional bound is indeed useless. We need a better approach.

Let me instead compute everything at larger primes to extend the data.
"""

from math import gcd, log, sqrt
import sys

def mobius(n):
    if n == 1: return 1
    temp = n; d = 2; factors = 0
    while d * d <= temp:
        if temp % d == 0:
            factors += 1; temp //= d
            if temp % d == 0: return 0
        d += 1
    if temp > 1: factors += 1
    return (-1) ** factors

def mertens(N):
    return sum(mobius(k) for k in range(1, N+1))

def is_prime(n):
    if n < 2: return False
    if n < 4: return True
    if n % 2 == 0 or n % 3 == 0: return False
    d = 5
    while d * d <= n:
        if n % d == 0 or (n + 2) % d == 0: return False
        d += 6
    return True

def compute_float(p):
    """Compute alpha, rho using floating-point (fast, for larger primes)."""
    N = p - 1

    # Build Farey sequence
    fracs = []
    for b in range(1, N+1):
        for a in range(0, b+1):
            if gcd(a, b) == 1:
                fracs.append((a, b))
    fracs.sort(key=lambda x: x[0]/x[1])
    n = len(fracs)

    # Interior fractions
    interior = [(a, b) for (a, b) in fracs if b >= 2]
    n_int = len(interior)

    # Build rank map
    rank_map = {}
    for j, (a, b) in enumerate(fracs):
        rank_map[(a, b)] = j

    # Compute sums
    sum_f = 0.0; sum_D = 0.0; sum_f2 = 0.0; sum_Df = 0.0; sum_D2 = 0.0
    sum_delta = 0.0; sum_delta2 = 0.0; sum_f_delta = 0.0; sum_D_delta = 0.0

    D_vals = []; f_vals = []; delta_vals = []

    for (a, b) in interior:
        f_val = a / b
        D_val = rank_map[(a, b)] - n * f_val
        sigma = (p * a) % b
        d_val = (a - sigma) / b

        D_vals.append(D_val)
        f_vals.append(f_val)
        delta_vals.append(d_val)

        sum_f += f_val
        sum_D += D_val
        sum_f2 += f_val**2
        sum_Df += D_val * f_val
        sum_D2 += D_val**2
        sum_delta += d_val
        sum_delta2 += d_val**2
        sum_f_delta += f_val * d_val
        sum_D_delta += D_val * d_val

    mean_f = sum_f / n_int
    mean_D = sum_D / n_int
    cov_Df = sum_Df / n_int - mean_D * mean_f
    var_f = sum_f2 / n_int - mean_f**2
    alpha = cov_Df / var_f

    C_prime = sum_delta2
    B_prime = 2 * sum_D_delta

    # Compute D_err and rho
    sum_Derr_delta = 0.0
    sum_Derr2 = 0.0
    for i in range(n_int):
        D_err = D_vals[i] - mean_D - alpha * (f_vals[i] - mean_f)
        sum_Derr_delta += D_err * delta_vals[i]
        sum_Derr2 += D_err**2

    rho = 2 * sum_Derr_delta / C_prime

    R = sqrt(sum_Derr2 / C_prime)
    corr = sum_Derr_delta / (sqrt(sum_Derr2) * sqrt(C_prime))

    return {
        'p': p, 'N': N, 'n': n, 'n_int': n_int,
        'alpha': alpha, 'rho': rho,
        'R': R, 'corr': corr,
        'BoverC': B_prime / C_prime,
    }

# Find all M=-3 primes up to 500 (float computation is fast enough)
print("Finding M=-3 primes...", file=sys.stderr)
m3_primes = []
for p in range(2, 501):
    if is_prime(p) and mertens(p) == -3:
        m3_primes.append(p)

print(f"Found {len(m3_primes)} M=-3 primes up to 500: {m3_primes}")
print()

print(f"{'p':>5} {'alpha':>8} {'rho':>8} {'a+r':>8} {'|rho|':>8} "
      f"{'a-1':>8} {'|r|/(a-1)':>10} {'R':>8} {'|corr|':>10} "
      f"{'|r|/slp':>8}")
print("-" * 120)

for p in m3_primes:
    print(f"  Computing p={p}...", file=sys.stderr)
    r = compute_float(p)
    a = r['alpha']
    rho = r['rho']
    rho_abs = abs(rho)
    a_m1 = a - 1
    ratio = rho_abs / a_m1 if a_m1 > 0 else float('inf')
    lp = log(p)
    slp = sqrt(lp)

    print(f"{p:5d} {a:8.4f} {rho:8.4f} {a+rho:8.4f} {rho_abs:8.4f} "
          f"{a_m1:8.4f} {ratio:10.4f} {r['R']:8.4f} {abs(r['corr']):10.6f} "
          f"{rho_abs/slp:8.4f}")

print()
print("=== SCALING CHECK ===")
print(f"{'p':>5} {'|rho|/sqrt(log p)':>18} {'|corr|*sqrt(p)':>16} {'R/sqrt(N)':>12}")
for p in m3_primes:
    r = compute_float(p)
    lp = log(p)
    print(f"{p:5d} {abs(r['rho'])/sqrt(lp):18.4f} {abs(r['corr'])*sqrt(p):16.4f} {r['R']/sqrt(p-1):12.4f}")
