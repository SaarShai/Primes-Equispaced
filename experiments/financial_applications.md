# Financial Applications of Farey/Prime Scheduling

**Date:** 2026-03-25
**Status:** Feasibility analysis (honest assessment)

---

## Our Mathematical Tools (Recap)

1. **Injection Principle:** When adding fractions with prime denominator p to the Farey sequence F_{p-1}, each existing gap receives at most 1 new point. Proved in Lean 4 (0 sorry).
2. **Modular Inverse Neighbor:** The left neighbor of k/p has denominator k^{-1} mod p. Each actor can compute its own slot independently.
3. **Sub-Gap Formula:** New points create sub-gaps of width 1/(pb) and 1/(pd) where b+d=p. Exact, predictable spacing.
4. **Coordination-Free:** Actors only need to agree on prime p and know their index k. No communication protocol needed.
5. **Collision Guarantee:** Zero collisions when adding p new slots to an existing p-1 slot system (verified computationally for all primes up to 31).

---

## Application 1: Order Scheduling (Algo Trading)

### The Idea

Multiple algorithmic traders need to submit orders without creating congestion. If N traders agree on a prime p > N, trader k submits at time offset k/p within each trading interval. The injection principle guarantees no two traders hit the same time slot.

### How It Would Work

- Trading interval T (e.g., 1 second) is divided into slots
- Trader k gets slot at time t = T * (k/p) for some agreed prime p
- Each trader independently computes their slot using only k and p
- No central coordinator needed
- Adding a new trader (with the next prime) provably does not collide with existing schedules

### Honest Assessment

**Problems that make this impractical:**

1. **Markets already solve this differently.** Exchanges use sequential matching engines with queue priority (price-time priority). The "collision" problem is handled by the exchange's matching engine, not by traders coordinating their submission times.

2. **Latency dominance.** In HFT, the relevant timescale is nanoseconds to microseconds. The advantage comes from being FIRST, not from avoiding collisions. A trader who submits at k/p * T might miss the optimal moment entirely. The whole point of speed is to react to market events as they happen, not on a predetermined schedule.

3. **Market impact is the real problem.** Traders don't just want to avoid simultaneous submission -- they want to minimize price impact. The Almgren-Chriss framework solves this by optimizing the trade-off between market impact (trading too fast) and timing risk (trading too slow). This is a continuous optimization problem, not a scheduling problem.

4. **Adversarial environment.** If your schedule is deterministic and based on a known prime p, other traders can predict exactly when you'll submit orders and front-run you. The predictability that makes Farey scheduling elegant is a WEAKNESS in adversarial markets.

5. **Non-uniform demand.** Trading activity clusters around events: market open, economic releases, earnings announcements. A uniform Farey distribution ignores this reality. You want MORE orders near information events, not equal spacing.

**Verdict: NOT PRACTICAL.** The scheduling problem in trading is not about avoiding collisions -- it's about optimal execution in the presence of market impact, information arrival, and adversarial participants. Farey scheduling solves a problem that markets don't have.

---

## Application 2: Dark Pool Crossing

### The Idea

Dark pools match buyers and sellers without displaying orders publicly. Could Farey scheduling improve the rate at which buy and sell orders "cross" (find matching counterparties)?

### How It Would Work

- Buyers submit at times k_buy/p within each interval
- Sellers submit at times k_sell/q within each interval (different prime)
- The Farey structure guarantees dense coverage of the time interval
- Crossing opportunities arise when a buy and sell are present simultaneously
- The three-distance theorem ensures new submissions are well-distributed

### Honest Assessment

**Problems:**

1. **Dark pools optimize for matching, not timing.** The key challenge in dark pools is finding counterparties with matching size and price, not scheduling when to check for matches. Modern dark pools run continuous matching or periodic auctions (every 100ms or so).

2. **Periodic auctions already exist and are simpler.** IEX's speed bump (350 microseconds) and periodic batch auctions (used in European venues under MiFID II) already batch orders to reduce gaming. These are simpler and better studied than Farey-based scheduling.

3. **Size matching matters more.** A dark pool's value is in matching large institutional orders without information leakage. Whether orders arrive at Farey-spaced times or randomly doesn't affect the fundamental matching problem.

4. **Information leakage risk.** If the crossing schedule is known (deterministic Farey times), informed traders can time their orders to coincide with expected dark pool crossings, defeating the purpose of darkness.

**One narrow possibility:** In a periodic auction where multiple dark pools coordinate crossing times, Farey spacing could ensure that different venues' auction times don't overlap. But this is a trivial scheduling problem that doesn't need Farey theory -- any set of non-overlapping times works.

**Verdict: NOT PRACTICAL.** Dark pool design is about information protection and matching quality, not time-slot coordination.

---

## Application 3: Market Making Quote Rotation

### The Idea

Market makers continuously quote bid and ask prices. Multiple market makers could use Farey-based rotation to ensure their quote updates don't all arrive simultaneously, reducing message congestion and potentially reducing adverse selection.

### How It Would Work

- N market makers agree on prime p > N
- Market maker k updates quotes at time offsets k/p within each quoting cycle
- The injection principle ensures no two makers update simultaneously
- When a new market maker enters, their update times provably don't collide with existing makers

### Honest Assessment

**This is the most plausible of the four applications, but still has problems:**

**In favor:**
- Quote congestion IS a real problem. Exchanges experience message bursts that can cause delays.
- Coordinated quote rotation could reduce peak message rates.
- The coordination-free property is genuinely valuable: each maker only needs to know p and k.
- Reducing simultaneous updates could slightly reduce the "stale quote" problem (where multiple makers have outdated quotes simultaneously after a price move).

**Against:**
1. **Market makers quote reactively.** A market maker's optimal quote depends on the current state of the order book, recent trades, and inventory. Forcing quotes onto a Farey schedule means sometimes quoting at suboptimal moments (right after a trade when you should widen) and missing optimal moments (when you have information advantage).

2. **Exchanges already have throttling.** Most exchanges limit message rates per participant (e.g., 1000 messages/second on NYSE). This serves the same congestion-reduction purpose without requiring inter-maker coordination.

3. **Regulatory concerns.** Coordinating quote timing between competing market makers could raise antitrust/collusion concerns under Reg NMS (US) or MiFID II (EU). Even if the coordination is purely mechanical (just agreeing on a prime p), regulators might view it as an agreement that affects market quality.

4. **Adverse selection is about information, not timing.** A market maker gets adversely selected when an informed trader picks off their stale quote. Whether quotes are updated on a Farey schedule or randomly doesn't change the fundamental information asymmetry.

**Verdict: THEORETICALLY INTERESTING, PRACTICALLY MARGINAL.** The coordination-free property is genuinely nice, but the benefits don't outweigh the cost of forcing quotes onto a rigid schedule.

---

## Application 4: Connection to Optimal Execution (Almgren-Chriss)

### The Idea

The Almgren-Chriss model (2000) is the standard framework for optimal trade execution. It minimizes a cost function balancing market impact against timing risk. Could Farey scheduling improve on the standard solution?

### The Almgren-Chriss Framework

- You need to sell X shares over time horizon T
- Trading faster causes more market impact (price moves against you)
- Trading slower exposes you to price volatility (timing risk)
- The optimal solution is a deterministic schedule: trade at rate x(t) that minimizes expected cost + risk penalty
- For linear impact and constant volatility, the optimal schedule is a smooth curve (often close to TWAP -- time-weighted average price)

### Where Farey Might Connect

The Almgren-Chriss optimal trajectory is continuous. To implement it, you must discretize: break T into N time slots and trade x_i shares at each slot. The question is how to choose the N time points.

- **Standard approach:** Equal spacing (TWAP) or volume-weighted spacing (VWAP)
- **Farey approach:** Space the N trade times at Farey fractions k/p

### Honest Assessment

**The connection is superficial.** Here's why:

1. **Discretization isn't the bottleneck.** The error from discretizing the optimal trajectory into N equal steps scales as O(1/N), and N is typically large (hundreds to thousands of intervals per day). Switching from equal spacing to Farey spacing changes this error by a negligible amount.

2. **The optimal schedule is non-uniform.** Almgren-Chriss gives a trajectory that typically front-loads or back-loads trading depending on the risk-aversion parameter. Farey points are uniformly distributed (by the equidistribution theorem). Using uniform Farey points to approximate a non-uniform trajectory is worse than using non-uniform points chosen to match the trajectory shape.

3. **The discrepancy connection is real but irrelevant.** Our Farey points have low discrepancy (related to the Mertens function). Low-discrepancy sequences are used in Quasi-Monte Carlo methods for EVALUATING expected execution costs (numerical integration). But that's computing the cost, not choosing the execution schedule. You could use Farey-QMC to EVALUATE the cost of any schedule, but the schedule itself should come from the optimization.

4. **One genuine (tiny) connection:** If you're doing Monte Carlo simulation of execution costs under different market scenarios, Farey-based QMC point sets with M(N) as a quality metric (from our Application A4) could give faster convergence than pseudorandom sampling. But this is a standard QMC application, not specific to Almgren-Chriss.

**Verdict: NO MEANINGFUL CONNECTION.** The optimal execution problem is a continuous optimization problem. Farey scheduling addresses a discrete collision-avoidance problem. These are fundamentally different.

---

## Summary: Would a Quant Actually Implement This?

**No, with one caveat.**

### Why Not

| Reason | Explanation |
|--------|-------------|
| Wrong problem | Markets solve congestion through matching engines, throttling, and auctions -- not coordination-free scheduling |
| Adversarial environment | Deterministic schedules are exploitable. Randomness is a feature, not a bug |
| Reactive nature of trading | Optimal actions depend on current market state, not predetermined time slots |
| Marginal benefit | Even where applicable (quote rotation), the improvement over simple alternatives is negligible |
| Regulatory risk | Coordinated scheduling between competitors raises antitrust concerns |

### The Caveat

There is ONE scenario where Farey scheduling could be genuinely useful in finance, though it's not the high-frequency trading context:

**Internal order routing across multiple execution venues.** A large broker-dealer routes client orders to 5-15 different exchanges and dark pools. The internal scheduling of when to send child orders to each venue is a real coordination problem where:
- You control all the actors (no adversarial concern)
- Avoiding simultaneous submissions to multiple venues reduces information leakage
- The number of venues is small (works well with small primes)
- Coordination-free is valuable because different routing algorithms handle different order types

Even here, the benefit is incremental -- randomized jitter achieves similar results with less mathematical machinery.

---

## Comparison: Where Our Tools ARE Useful vs Finance

| Feature | Finance Needs | Our Tools Provide | Match? |
|---------|---------------|-------------------|--------|
| Collision avoidance | Not primary concern | Perfect guarantee | Misaligned |
| Deterministic schedule | Actively harmful (exploitable) | Core feature | Misaligned |
| Coordination-free | Nice-to-have for internal systems | Strong | Partial |
| Optimal timing | Depends on market state | Fixed rational times | Misaligned |
| Congestion reduction | Solved by exchanges | Solved by prime spacing | Redundant |
| Low discrepancy | Useful for Monte Carlo | Available via M(N) metric | Partial (QMC only) |

### Where Our Tools Genuinely Shine (Non-Finance)

For comparison, these are the domains where the injection principle and Farey scheduling solve REAL problems:

1. **TDMA / wireless networks** (Application A2): Collision avoidance IS the primary concern, deterministic schedules are GOOD, coordination-free is essential. Rating: STRONG
2. **Mesh generation** (Application A1): Quality guarantees during refinement. Rating: STRONG
3. **Frequency hopping** (Application A3): Bounded collision count per pair. Rating: GENUINE

---

## Bottom Line

The Farey injection principle is a beautiful mathematical result with genuine applications in distributed systems, mesh generation, and signal processing. Finance is not one of them. The financial markets are an adversarial, information-driven environment where the problems are about optimal response to changing conditions, not about deterministic scheduling. Trying to apply Farey scheduling to finance is like using a perfectly tuned piano to hammer nails -- the instrument is excellent, but the application is wrong.

The honest answer: a quant who read this would appreciate the math but would not implement it. The closest practical connection is using Farey-QMC for Monte Carlo pricing/risk simulations, which is a standard QMC application dressed up in Farey clothing.
