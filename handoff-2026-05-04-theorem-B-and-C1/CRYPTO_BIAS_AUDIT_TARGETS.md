# Crypto Bias Audit Targets — drand & Ethereum RANDAO

Date: 2026-05-03 | Scope: feasibility deep-dive for statistical-bias audit prototype, 1–2 wk build.

---

## TARGET 1 — drand (League of Entropy)

### Architecture

**Primitive.** Threshold BLS signature on **BLS12-381**, signatures in G1, hash-to-curve per RFC9380 v7. Production network = `quicknet`, chain hash `52db9ba70e0cc0f6eaf7803dd07447a1f5477735fd3f661792ba94600c84e971` (hex, the canonical "quicknet" hash; `cc9c…a9a5` is `quicknet-t`, a separate testnet variant). Curve params + base points are fixed in spec; compromise of curve choice would equally compromise Ethereum BLS, Filecoin, Zcash Sapling, etc.

**Round flow.**
```
round r → message m_r = SHA256(r as uint64 BE)        (unchained mode, quicknet)
each node i signs:  σ_i = sk_i · H_G1(m_r)
any t-of-n shares → σ_r = ThresholdReconstruct(σ_i)   (Lagrange in G1)
beacon output:     randomness_r = SHA256( σ_r compressed, 48 bytes )
```
- `t = ⌈n/2⌉ + 1` (honest majority threshold). League of Entropy: ~22 nodes, t≈12.
- Genesis timestamp + `period = 3 s` define round number deterministically: `round(t) = (t − genesis)/period + 1`.
- **Unchained**: σ_r depends only on r, not on σ_{r-1}. Stateless verification: `e(σ_r, G2) =? e(H_G1(SHA256(r)), pk)`.

**Where bias could enter.**
1. **Threshold malleability.** With t partials, the t-of-n reconstruction is *unique* (Lagrange is deterministic). A coalition of <t cannot bias. A coalition of ≥t can produce only the unique correct σ_r — they cannot pick from alternatives without breaking BLS. ⟹ Bias-by-grinding is cryptographically impossible under DLOG/co-CDH on BLS12-381.
2. **DKG-time bias.** Distributed Key Generation (Pedersen-style) at network setup is the only window where master pk could be biased. Audited live in 2023 quicknet rollout; fresh DKG required for any reshare.
3. **Hash-to-curve bias.** SHA256 → field → curve. RFC9380 includes a clear-cofactor step. Implementation bugs (early SWU, exception handling) historically caused subgroup confusion in similar systems.
4. **SHA256 of σ.** Output = SHA256(48-byte G1 element). Distinguishable from uniform only if SHA256 is broken or σ has structure leaking through.

### Public data

**HTTP API (LoE relays).** v2:
- `https://api.drand.sh/<chain-hash>/public/<round>`
- `https://api2.drand.sh/...`, `api3.drand.sh/...` (Cloudflare, Protocol Labs, EPFL)
- `https://drand.cloudflare.com/<chain-hash>/public/<round>` (legacy)
- `/info` returns genesis_time, period, public_key, group_hash.

**Format (JSON).**
```json
{ "round": 20986100,
  "randomness": "<64 hex = SHA256 of sig>",
  "signature":  "<96 hex = compressed G1 sig>" }
```
Quicknet chained: 96 hex sig (48-byte G1). Pre-quicknet `default` chain has `previous_signature` field too.

**Volume.** Quicknet genesis ≈ 2023-08-23. As of 2026-05, ~28 M rounds elapsed (≈ 86,400 rounds/day at 3 s). Default chain (30 s period, since 2020-08): ~5.8 M rounds. **Total available ≈ 34 M signatures.** Each ~150 bytes JSON ⟹ ~5 GB raw, ~1.5 GB compressed. Fetch limit: rate-limited by relays; CDN cache hits unlimited. Realistic harvest: 100–500 rps sustained per relay → full quicknet history in 1–3 days.

**Source code.** `github.com/drand/drand` (Go), `drand/kyber` (crypto), `drand/tlock` (timelock).

### Threat models

| Vector | Realism | Detectability via output stats |
|---|---|---|
| Coalition ≥ t generates valid σ but biased | Cryptographically impossible (BLS uniqueness) | N/A — bias would be 0 |
| <t-coalition forges | Requires break of co-CDH on BLS12-381 | Would show as deviation from uniform on SHA256(σ) — testable |
| Skipped rounds (DoS) | Possible; visible as gaps | Not a randomness bias, an availability one |
| Hash-to-curve impl bug | Has happened in similar libs (subgroup attacks) | Subtle bias in σ distribution on G1; SHA256 wrapper masks it |
| Master sk leaked | Catastrophic but bias-free post-leak | Undetectable from output alone (since σ still unique) |
| **Subverted curve params** | Would affect all BLS deployments | Probably untestable given astronomic structure |

**Existing audits.**
- Cloudflare 2019 launch post (Dodis, Syta involvement).
- DEDIS/EPFL papers: Syta et al. *Scalable Bias-Resistant Distributed Randomness*, IEEE S&P 2017 (RandHound/RandHerd, drand precursor).
- Kavousi/Wang/Pirooz/Galbraith *SoK: Public Randomness*, ePrint 2023/1121 — surveys drand security model.
- drand security model doc: `docs.drand.love/docs/security-model/`.
- **No published statistical audit of output distribution.** This is the gap our framework would fill.

### What our framework adds

**Null hypothesis.** Quicknet output `r ∈ {0,1}^256` should be uniform on 2^256, equivalently `int(r)` ~ Uniform[0, 2^256). Tests:

1. **Modular reductions.** For small q (256-bit primes in elliptic-curve apps, q=2 for bit-bias, q=10^9+7 for Farey-relevant scales): test `r mod q ~ U{0,…,q-1}` via χ² with df=q-1. Sample size 28M lets us detect bias of magnitude **ε ≥ √(q/N) ≈ 10^-3** for q=1000, **ε ≥ 10^-4** for q=2.
2. **Chebyshev mod q.** Use the Farey-Chebyshev framework on `n = int(r) mod p` for various primes — direct application of the discrepancy machinery from the active research program.
3. **NIST SP 800-22 suite.** All 15 tests on bit stream `concat(r_1, r_2, …)`. With 28M × 256 bits = 7.2 Gbit, every test reaches its asymptotic regime.
4. **Birthday spacings, OPSO, OQSO** (Marsaglia DIEHARD): on 32-bit windows.
5. **Byte-level entropy.** Min-entropy estimator (NIST SP 800-90B) on per-round 32-byte outputs.
6. **Cross-round correlation.** `corr(r_t, r_{t+k})` for k=1..1000. Should be O(1/√N) ≈ 2·10^-4.
7. **Signature-level** (deeper): decompress σ to G1, project to coordinates, test x-coord uniformity mod field prime p_BLS = 2^381 - …. Catches hash-to-curve bugs that SHA256 wrapper hides.

**Detection thresholds (28M samples).**
- Bias of 1 part in 10^4 in any mod-q test: detected at p<10^-6.
- Bias of 1 part in 10^3 in cross-correlation: trivially detected.
- Below 10^-5: indistinguishable from sampling noise without more data.

### Concrete deliverable spec

```
PHASE 1 — harvest               2 days wall-clock
  for chain in [quicknet, default]:
    parallel-fetch /public/<r> for r in 1..R_max
    verify σ via py_ecc BLS12-381 pairing (sample 1% for sanity)
    write parquet: (round, randomness_hex, sig_hex, verified_bool)

PHASE 2 — basic uniformity      4 hours
  load randomness as uint256
  run NIST SP 800-22 (sts-2.1.2) on bitstream
  χ² mod q for q ∈ {2, 256, 10^3, 10^6, primes 10^4..10^9}
  birthday spacings, monobit, runs, FFT

PHASE 3 — Farey-Chebyshev       1 day
  for prime p in test set:
    project r mod p → [0,1)
    apply Farey-discrepancy estimator
    compare against null Chebyshev distribution
    flag outliers at 4σ

PHASE 4 — signature-level       1 day
  decompress sig → (x,y) in F_p²
  test x mod p_BLS uniformity
  test G1 subgroup membership (should be 100%)
  cross-check: e(σ, G2) =? e(H(round), pk)

PHASE 5 — report                4 hours
```

**Output.** `drand_audit_<date>.pdf`: per-test p-value table, QQ plots vs uniform, bit-correlation heatmap, anomaly flags with redo recommendations. Wall-clock: ~5 days end-to-end on 1 M1 Max.

---

## TARGET 2 — Ethereum RANDAO

### Architecture

**Primitive.** Per-slot proposer signs `epoch_number` with their validator BLS key (BLS12-381, G2 sigs). Reveal hashed → XORed into beacon-state `randao_mix`.

**Round flow (per slot, 12 s).**
```
proposer for slot s, epoch e:
  randao_reveal_s = BLS_sign(sk_validator, ssz_hash(e))
  block.body.randao_reveal = randao_reveal_s
state transition:
  mix' = mix XOR SHA256(randao_reveal_s)
  state.randao_mixes[e mod EPOCHS_PER_HISTORICAL_VECTOR] = mix'
```
- `EPOCHS_PER_HISTORICAL_VECTOR = 65,536`. Past mixes available via API for ~292 days.
- 32 slots/epoch ⟹ 32 reveals XORed per epoch.
- Used for: proposer selection 2 epochs ahead, sync-committee selection every 256 epochs, attestation committees.

**Where bias enters.**
1. **Proposer manipulation (canonical).** Last proposer of an epoch sees `mix'` if they include their block, vs. `mix` if they skip. ⟹ 1-bit choice per epoch → 1 bit of bias on next-but-one epoch's proposer assignments. Generalizes to k-bit bias if attacker controls last k slots.
2. **Forking-based grinding.** Attacker controlling slots near epoch boundary can fork: include vs. orphan their own block. Costs missed attestation reward (~ 0.0001 ETH).
3. **`randao_reveal` predictability.** Since the message is `epoch_number`, BLS signature is deterministic for a given key — proposer knows their reveal weeks in advance. Cannot grind on the reveal itself, only on inclusion.
4. **Algorithmic bias.** SHA256 wrapper + XOR is information-theoretically optimal *given non-adversarial inputs*. Adversarial inputs ⟹ bias bounded by Σ(adversary's controlled slots in last k of epoch) per Alpturer–Weinberg.

### Public data

**Beacon API.**
- `GET /eth/v1/beacon/states/{state_id}/randao?epoch={e}` → `randao_mix` for specified epoch.
- `GET /eth/v2/beacon/blocks/{block_id}` → contains `body.randao_reveal` (BLS sig, 96 bytes).
- Public endpoints: Ankr, QuickNode, Infura beacon, BeaconCha.in API, plus local Lighthouse/Prysm/Teku archive nodes.

**Format.**
- `randao_reveal`: hex 96 bytes (G2 BLS sig).
- `randao_mix`: hex 32 bytes (SHA256-derived).

**Volume (2026-05).** PoS launched 2022-09-15. ~3.5 yr × 32 slots/epoch × 7,200 slots/day = **~9.4 M slots, ~9.4 M reveals**. ~290k epochs ⟹ ~290k mix values (only ~65k visible in any single state due to ring-buffer; deeper history requires reconstruction from blocks).

**Reconstructing full history.** Walk all blocks 0..head, extract `randao_reveal`, replay XOR. ~100 GB of beacon block data. Tools: `ethdo`, `lighthouse db`, BeaconCha.in's archived dumps.

### Threat models

| Vector | Realism | Already shown |
|---|---|---|
| 1-slot last-revealer | Always available to the assigned proposer | Buterin 2018 |
| k-last-slot manipulation | Requires controlling k consecutive last-of-epoch slots | Edgington/Shapiro |
| Optimal grinding strategy (Alpturer–Weinberg, AFT 2024) | 5% stake → 5.05% slots; 20% → 20.68% | Yes, quantified |
| Forking-based RANDAO manipulation (ePrint 2025/037) | Empirically searched on mainnet; **no significant traces detected** | Yes |
| BLS reveal forgery | Requires breaking BLS12-381 | No |
| Validator set deanon via reveal patterns | Possible side-channel | Unstudied |

**Mitigations under discussion.** EIP-7998 (Aug 2025): replace `randao_reveal` with a VRF whose output is unpredictable even to the revealer, eliminating last-revealer attacks. Not adopted as of 2026-05.

**Existing audits.**
- Buterin, *Validator selection*, ethresear.ch 2017–2018.
- Edgington, *Eth2Book §2.9 Randomness* (annotated spec).
- Hu et al. *RANDAO-based RNG: Last Revealer Attacks*, arXiv 2403.09541 (2024) — proposes SSS variant.
- Alpturer & Weinberg, *Optimal RANDAO Manipulation*, AFT 2024 (LIPIcs vol 316).
- *Forking the RANDAO*, ePrint 2025/037 — empirical mainnet measurement, no traces of forking attacks found.

**Output-distribution audits.** None published at scale. Edgington notes "outputs *appear* uniform"; no χ² / NIST suite report exists.

### What our framework adds

**Null hypothesis.** RANDAO mix per epoch should be a uniform 256-bit value *in the absence of grinding*. Two-pronged test:

1. **Macro test on mixes.** Treat sequence of 290k mixes as iid uniform; run full NIST suite + Farey-Chebyshev mod q.
2. **Micro test on residuals.** For each epoch, compute the *observed* shift in next-epoch proposer assignment vs. expected under fair shuffle. Under null (no grinding), observed-expected is mean-zero. Under k-stake attacker, mean shift = k · ε_optimal (Alpturer–Weinberg gives ε_optimal for each k). Estimate stake-weighted ε from data.
3. **Concentration test.** Group reveals by validator pubkey. Per-validator empirical distribution of `SHA256(reveal)` should be ~uniform. Detects single-validator reveal-grinding (impossible by construction, but tests integrity of data pipeline).
4. **Boundary-slot test (the new one).** Compare distribution of mixes at epoch boundaries where last 1, 2, 3, 4 slots are controlled by *the same staking pool* (Lido, Coinbase, Kraken, etc., stake>5%). Under null, no difference vs. random-slot epochs. Under grinding, large pools' boundary epochs should show measurable bias toward selecting their own validators in next-epoch proposer slots. **This is the headline test.**

**Detection thresholds.**
- 290k epochs of mix data ⟹ √N ≈ 540 ⟹ baseline noise ε ≈ 2·10^-3.
- Alpturer–Weinberg predicts 0.05% deviation for 5% stake, 0.68% for 20% stake.
- ⟹ For top stakers (Lido ~28%, Coinbase ~9%) the predicted bias is **above** noise floor. Detectable. For minor stakers, requires N → 10⁶+ epochs (years away).

### Concrete deliverable spec

```
PHASE 1 — beacon archive sync       3 days
  spin up Lighthouse archive node (or rent QuickNode)
  pull all blocks slot 0..head (~9.4M)
  extract (slot, proposer_index, randao_reveal, parent_root)
  pull validator registry snapshots → (pool_label per pubkey)

PHASE 2 — reconstruct mixes         8 hours
  iterate epochs, replay XOR
  cross-check vs. /states/{id}/randao at 100 sampled epochs

PHASE 3 — macro tests               6 hours
  NIST SP 800-22 on concat(mixes)
  χ² mod q same as drand
  Farey-Chebyshev test set

PHASE 4 — boundary test (★)         2 days
  for pool in {Lido, Coinbase, Kraken, Binance, ...}:
    epochs_pool = {e : last 1+ slot of e proposed by pool}
    epochs_other = complement
    compare next-epoch proposer-share for pool: empirical vs. expected stake share
    Welch t-test, multiple-correction Bonferroni
  expected: top stakers show small but statistically significant excess
            consistent with Alpturer–Weinberg quantitative bound

PHASE 5 — micro test                4 hours
  per-validator reveal entropy

PHASE 6 — report                    4 hours
```

**Output.** `randao_audit_<date>.pdf`: same skeleton as drand report PLUS pool-level boundary table — first published empirical confirmation/refutation of optimal-grinding theoretical bounds. Wall-clock: ~7 days, gated on archive sync.

---

## Comparative summary

| | drand | RANDAO |
|---|---|---|
| Bias-by-grinding cryptographically possible? | **No** (BLS uniqueness) | **Yes**, bounded |
| Sample size available | ~34M | ~290k epoch mixes (~9.4M reveals) |
| Best-case detection threshold | 10^-4 deviation | 10^-3 deviation |
| Novelty of audit | First output-distribution test | First empirical pool-attribution test |
| Build effort | 5 days, 1 machine | 7 days, archive node needed |
| Headline result if clean | "drand passes 28M-sample uniformity" | "Lido boundary epochs show X bias, matches Alpturer 2024 prediction" |

**Recommendation.** Build RANDAO first — the headline result (empirical confirmation of the AFT 2024 theoretical bound on real-pool data) is more interesting than another clean PRG audit. drand is a 1-week follow-on.

## Sources

- drand HTTP API: https://docs.drand.love/dev-guide/API%20Documentation%20v2/drand-http-api/
- drand quicknet announcement: https://docs.drand.love/blog/2023/10/16/quicknet-is-live/
- drand Ethereum verification (2025): https://docs.drand.love/blog/2025/08/26/verifying-bls12-on-ethereum/
- drand security model: https://docs.drand.love/docs/security-model/
- drand cryptography: https://docs.drand.love/docs/cryptography/
- drand GitHub: https://github.com/drand/drand
- Cloudflare LoE: https://www.cloudflare.com/leagueofentropy/
- SoK Public Randomness, Kavousi et al. 2023: https://eprint.iacr.org/2023/1121.pdf
- Syta et al. RandHound/RandHerd 2017 (drand precursor): https://www.researchgate.net/publication/317919572_Scalable_Bias-Resistant_Distributed_Randomness
- Hu et al. Last Revealer Attacks: https://arxiv.org/abs/2403.09541
- Alpturer & Weinberg, Optimal RANDAO Manipulation, AFT 2024: https://drops.dagstuhl.de/storage/00lipics/lipics-vol316-aft2024/LIPIcs.AFT.2024.10/LIPIcs.AFT.2024.10.pdf
- Forking the RANDAO, ePrint 2025/037: https://eprint.iacr.org/2025/037.pdf
- EIP-7998 (VRF for randao_reveal): https://eips.ethereum.org/EIPS/eip-7998
- Beacon API spec: https://ethereum.github.io/beacon-APIs/
- Eth2Book §2.9 Randomness (Edgington): https://eth2book.info/latest/part2/building_blocks/randomness/
- Paradigm SNARK-RNG analysis: https://www.paradigm.xyz/2023/01/eth-rng
