# B+C > 0 — Dedekind Sum Proof Attempt (Codex Session, 2026-04-02, updated)

## Task
Prove B + C > 0 for all primes p ≥ 11 via Path 3 (Dedekind sums).

## Key Algebraic Result (PROVED unconditionally)

**Theorem:** For all primes p ≥ 5,

    sum_{a/b in F_{p-1}} f * delta(a/b) = C/2

where C = sum delta^2 and f = a/b.

**Proof sketch:** delta(a/b) = f - {pf}, so:

    sum f*delta = sum f^2 - sum f*{pf}

where S(p,b) = sum_{a coprime to b} a*(pa mod b).

Since p is prime and b < p, multiplication by p is a bijection on (Z/bZ)*.
Via Dedekind reciprocity algebra, S(p,b) simplifies to give:

    sum f*delta = C/2  (exactly)

This is **stronger** than sum f*delta > 0: it is exactly C/2, unconditionally
for all primes p ≥ 5 (not just M(p) ≤ -3).

## Does this prove B+C > 0? NO.

**Critical gap:** sum f*delta = C/2 > 0 settles the f-mediated channel.
But B+C > 0 requires sum D*delta > 0, i.e., the discrepancy-mediated channel.
The step from (sum f*delta > 0) to (sum D*delta > 0) requires that
D and f are positively correlated, which is the original open problem.

Since the Sign Theorem FAILS at p=243,799 while sum f*delta = C/2 > 0 always,
Path 3 alone cannot close the theorem. The formula sum f*delta = C/2 is
an exact identity but does not transfer to the discrepancy channel.

## What was NOT proved
- B+C > 0 for all M(p) ≤ -3 primes
- The connection between positive f-channel and positive D-channel

## Status
- Path 3 is CLOSED with exact identity sum f*delta = C/2
- Remaining open: prove rho(D,delta) > 0 analytically
- The Sign Theorem conjecture remains: B+C > 0 iff M(p) ≤ -3 (verified to p=100,000)

## Codex Detailed Derivation (Session 11 update, 2026-04-02)

### Permutation proof (rigorous)

For fixed b, let π_{p,b}(a) = pa mod b (permutation of U_b = {a: gcd(a,b)=1}).

```
T_b(p) = (1/b²) · sum_{a in U_b} a·(a - π_{p,b}(a))

Since π_{p,b} is a bijection: sum_a π_{p,b}(a)² = sum_a a²

2·T_b(p) = (1/b²) · sum_{a} (a - π_{p,b}(a))² = sum_{(a,b)=1} delta(a/b)²
```

Summing: **X(p) = sum f·delta = C/2**. QED.

Strictness: T_b = 0 iff p ≡ 1 (mod b). For p ≥ 5, T_{p-2} > 0 since p mod (p-2) = 2 ≠ 1.

### Dedekind sum exact formula

```
s^×(p,b) = sum_{(a,b)=1} ((a/b))·((pa/b))   [reduced-units Dedekind sum]

S(p,b) = b²·s^×(p,b) + b²·φ(b)/4
T_b(p) = φ(b)/12 + κ(b)/(6b) - s^×(p,b)
  where κ(b) = prod_{q|b} (1-q)

Full: X(p) = sum_{b=2}^{p-1} (φ(b)/12 + κ(b)/(6b))
           - sum_{c=2}^{p-1} M(floor((p-1)/c)) · s(p,c)
```

Standard bounds on s(·,p) via reciprocity are too weak to force positivity; sign proved via square identity above.

### Critical limitation

The sign theorem FAILS at p=243,799 yet sum f·delta = C/2 > 0 trivially holds there.
Path 3 cannot close B+C > 0 because it doesn't distinguish M(p)≤-3 primes.
The essential open step remains: prove sum D·delta > -C/2 (i.e., rho > -1).
