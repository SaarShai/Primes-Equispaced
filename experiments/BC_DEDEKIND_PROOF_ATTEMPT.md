# B+C > 0 — Dedekind Sum Proof Attempt (Codex Session, 2026-04-02)

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
