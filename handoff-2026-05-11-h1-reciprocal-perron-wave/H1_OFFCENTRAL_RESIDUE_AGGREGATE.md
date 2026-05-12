RIGOROUS_REDUCTION

# H1 Offcentral Residue Aggregate

Confidence: 0.80.

No theorem is promoted. The H1 simple-zero aggregate has a clean conditional
closure, but no checked external source currently supplies the needed
reciprocal-derivative bounds for a fixed elliptic curve.

## Scope

Object:

```text
c_E,W(K) = sum_n mu_E(n)/n W(n/K)
         = (1/2 pi i) int_(Re z=sigma)
             K^z W_hat(z) / L(E,1+z) dz.
```

Let `u = log K`. Let `r = ord_{s=1} L(E,s)`. For a simple offcentral zero
`rho = 1+i gamma`, `gamma != 0`, the H1 residue is

```text
a_gamma e^(i gamma u),
a_gamma = W_hat(i gamma) / L'(rho).
```

This file attacks the simple-zero aggregate

```text
Z_W(u) = sum_{gamma != 0} a_gamma e^(i gamma u).
```

Multiple-zero terms are only flagged here; they belong to the sibling
multiple-zero/rank-zero deliverable.

## Verdict

For positive analytic rank `r >= 1`, H1 does not need `Z_W(u) -> 0`. It only
needs

```text
Z_W(u) + contour_tail(u) = o(u^r).
```

Therefore bounded simple-zero residues are enough for the final H1/H2 product
composition.

For rank `r = 0`, boundedness is not enough. A nonzero absolutely convergent
pure-frequency sum is an almost-periodic oscillation, not a decaying error.
Pointwise rank-zero stabilization requires one of:

```text
all a_gamma = 0,
Z_W(u) -> 0 by a stronger non-absolute cancellation theorem,
Z_W(u) retained explicitly as an oscillatory term,
or a declared averaged theorem.
```

Under absolute convergence, the second option collapses to the first: if a
uniformly convergent nonzero-frequency exponential series has a pointwise limit
as `u -> infinity`, all its Fourier coefficients must vanish.

## Sharp Hypotheses

Let `q` denote vertical Mellin decay:

```text
|W_hat(i t)| <= C_W (1+|t|)^(-q).
```

The Agent-3 smoothstep class gives `q = 2`. A `C^infty` compact endpoint kernel
could make `q` arbitrarily large or super-polynomial, but that is a different
kernel class and must be declared.

### H-abs: absolute residue convergence

Assume:

```text
1. all offcentral zeros on Re(s)=1 are simple;
2. no zeros with Re(s)>1 enter the contour shift;
3. sum_{gamma != 0} |W_hat(i gamma)/L'(1+i gamma)| < infinity;
4. the shifted contour and horizontal tails are o(u^r), or O(1) if one only
   wants bounded residue control.
```

Then `Z_W(u)` is bounded and uniformly almost periodic. Hence:

```text
r >= 1:  Z_W(u) = O(1) = o(u^r).
r = 0:   Z_W(u) must be retained unless all coefficients vanish.
```

This is the cleanest pointwise sufficient hypothesis. It is stronger than
needed for positive rank, but it is easy to compose with H2.

### H-lower: simple zeros plus pointwise derivative lower bound

Assume zero counting

```text
N_E(T,2T) := #{gamma: T < |gamma| <= 2T} <= C_E T log T
```

and for every zero in that shell

```text
|L'(1+i gamma)|^(-1) <= C_E T^A.
```

Then on the dyadic shell,

```text
sum_{T<|gamma|<=2T} |a_gamma|
  <= C T^(1 + A - q) log T.
```

Thus `H-abs` follows if

```text
A < q - 1.
```

For the smoothstep `q = 2`, a pointwise lower bound

```text
|L'(1+i gamma)| >= C_E |gamma|^(-A),  A < 1,
```

would suffice. This is sharp at the dyadic-counting level. No checked source
currently gives this for fixed elliptic curves.

### H-ms: mean-square reciprocal derivative

Define the shell second moment

```text
J_E^shell(T) =
  sum_{T<|gamma|<=2T} |L'(1+i gamma)|^(-2).
```

By Cauchy-Schwarz and zero counting,

```text
sum_{T<|gamma|<=2T} |a_gamma|
 <= (sum_{T<|gamma|<=2T} |W_hat(i gamma)|^2)^(1/2)
    (J_E^shell(T))^(1/2)
 <= C T^((1 - 2q + theta)/2) (log T)^B
```

if

```text
J_E^shell(T) <= C T^theta (log T)^B.
```

Therefore `H-abs` follows if

```text
theta < 2q - 1.
```

For the smoothstep `q = 2`, it is enough to prove

```text
J_E^shell(T) <= C T^(3-delta)
```

for some `delta > 0`. A Gonek-type fixed-curve conjecture

```text
sum_{0<|gamma|<=T} |L'(1+i gamma)|^(-2)
  << T (log T)^B
```

would be far more than enough.

This is the best conditional H1 route. It avoids impossible-looking pointwise
lower bounds and matches the kind of reciprocal-derivative moment studied for
`zeta`. It is still not sourced for EC `L(E,s)`.

### H-pc: pair correlation and square-summable residues

Pair correlation alone does not bound `1/L'(rho)`. It only controls frequency
spacing. It becomes useful only after a magnitude input such as

```text
sum_gamma |a_gamma|^2 < infinity
```

or a truncated version of it.

With square-summable coefficients plus a pair-correlation or Hilbert-inequality
input controlling cross terms, one can aim for

```text
limsup_{U -> infinity} (1/U) int_0^U |Z_W(u)|^2 du
  <= C sum_gamma |a_gamma|^2.
```

This supports averaged or Besicovitch `L^2` formulations. It does not give
pointwise boundedness, and it does not give rank-zero pointwise convergence.

Use `H-pc` only for an explicitly averaged H1 theorem.

## Contour Formulation Avoiding Absolute Convergence

Absolute convergence is sufficient, not necessary. A sharper formulation keeps
the Perron contour as the theorem object.

Let `T_j -> infinity` be heights avoiding zeros. Shift the line from
`Re z = sigma` to `Re z = -eta`, indenting simple poles at `z=i gamma` with
`|gamma| <= T_j`. Write

```text
c_E,W(e^u) = Q_E,W(u) + Z_{T_j}(u) + I_{T_j}(u),
```

where

```text
Q_E,W(u)    = central polynomial, leading term u^r / L^(r)(E,1),
Z_T(u)      = sum_{0<|gamma|<=T} a_gamma e^(i gamma u),
I_T(u)      = shifted-line, horizontal-edge, and indentation remainder.
```

The exact pointwise H1 condition needed for composition is:

```text
there exists an admissible T(u) -> infinity such that
Z_{T(u)}(u) + I_{T(u)}(u) = o(u^r).        (H-cont-r)
```

For rank zero, replace `o(u^r)` by `o(1)`:

```text
Z_{T(u)}(u) + I_{T(u)}(u) = o(1).          (H-cont-0)
```

`H-cont-r` is the sharp reduction. It permits conditional cancellation and
principal-value interpretations that absolute convergence would exclude. But
it is also close to the desired theorem itself: it must be proved by estimates
on `1/L(E,1+z)` near and between zeros, not asserted as a source corollary.

## Known Sources And What They Do Not Give

### EC zero counting

Sheth, `Euler product asymptotics for L-functions of elliptic curves`,
arXiv:2312.05236, was fetched by `curl` and converted by `pdftotext`.

PDF p. 13, Theorem 3.1 gives an EC zero count of size `T log T` for
`N_E(T)`. The page labels it as a statement about the "number of zeros".
PDF p. 13, Corollary 3.2 states that the reciprocal-square zero sum
`sum 1/|gamma|^2` "converges".

Use: this sources the zero-counting input in `H-lower` and `H-ms`.

Limit: it gives no lower bound for `|L'(rho)|`, no mean-square bound for
`1/L'(rho)`, and no control of Laurent coefficients at multiple zeros.

### Zeta reciprocal-derivative analogues

Bui-Florea-Milinovich, `Negative discrete moments of the derivative of the
Riemann zeta-function`, arXiv:2310.03949, was fetched by `curl` and converted
by `pdftotext`.

PDF p. 1 notes that the negative moment `J_{-k}(T)` is "only defined if the
zeros are all simple." PDF p. 2 says: "No upper bounds are known" for the full
negative-moment family when `k > 0`; the paper obtains upper bounds on
subfamilies.

Milinovich-Ng, `A note on a conjecture of Gonek`, arXiv:1106.1160, was also
fetched and converted. PDF p. 1 describes a "lower bound for a second moment"
of reciprocal zeta derivatives, conditional on RH and simple zeros.

Use: these sources make the H1 reciprocal-derivative hypothesis plausible as a
standard kind of problem and show that a Gonek-type `J_{-1}` bound would close
smoothstep H1.

Limit: they are zeta sources, not fixed elliptic-curve sources. Lower bounds
are the wrong direction for H1 convergence. Subfamily upper bounds do not
control the full offcentral residue aggregate. Pair correlation removes some
close-spacing risk but does not control derivative magnitudes by itself.

## Theorem Candidate

Conditional theorem, simple zeros:

```text
Let E/Q be fixed and let r = ord_{s=1} L(E,s). Let W be an admissible
endpoint kernel with |W_hat(i t)| <= C(1+|t|)^(-q), q > 1.

Assume:
  (A) the relevant offcentral zeros rho=1+i gamma are simple;
  (B) N_E(T,2T) <= C_E T log T;
  (C) either
        sum_{T<|gamma|<=2T} |L'(rho)|^(-2) <= C T^theta (log T)^B
        with theta < 2q-1,
      or
        |L'(rho)|^(-1) <= C |gamma|^A with A < q-1;
  (D) the nonzero shifted-contour tails are o(u^r) after central and
      offcentral residues are removed.

Then
  Z_W(u) = sum_{gamma != 0} W_hat(i gamma)L'(1+i gamma)^(-1)e^(i gamma u)
converges absolutely and is bounded.

Consequently:
  if r >= 1, c_E,W(e^u) = Q_E,W(u) + o(u^r);
  if r = 0, c_E,W(e^u) = 1/L(E,1) + Z_W(u) + o(1), and a pointwise limit
  exists only if the offcentral aggregate is killed, retained, or averaged.
```

This is a valid theorem target, not a closed theorem. The missing source is
`(C)` for fixed EC `L(E,s)` plus the full contour-tail estimate `(D)`.

## No-Go Boundary

Do not claim pointwise rank-zero H1 from absolute convergence. Absolute
convergence gives a bounded oscillatory function. It does not give decay.

Do not claim simple zeros alone are enough. Simplicity makes `1/L'(rho)` finite
one zero at a time, but gives no summability and no uniform lower bound.

Do not claim EC zero counting is enough. With smoothstep `q = 2`, zero counting
would prove

```text
sum |W_hat(i gamma)| < infinity,
```

but H1 needs

```text
sum |W_hat(i gamma)| / |L'(rho)| < infinity.
```

Do not claim pair correlation is enough. It controls spacings, not residue
sizes.

Do not import H2 branch damping. H1 residues have no `1/u` factor.

## Positive Rank Versus Rank Zero

Pointwise positive rank:

```text
r >= 1:
  bounded Z_W(u) is enough;
  more generally Z_W(u) = o(u^r) is exactly what composition needs.
```

Pointwise rank zero:

```text
r = 0:
  bounded Z_W(u) is not enough;
  generic simple offcentral zeros force persistent oscillation;
  final theorem must be oscillatory, averaged, or zero-killed.
```

Averaged rank zero:

```text
If Z_W is absolutely convergent, then
  (1/U) int_0^U Z_W(u) du -> 0.
Thus a logarithmic-average theorem can kill simple nonzero frequencies.
This is an averaged theorem only; it is not pointwise stabilization.
```

## Dependencies

- Exact H1 central polynomial from Agent 1 or equivalent in-repo proof.
- Same `W` and Mellin normalization as H2.
- Analytic rank `r = ord_{s=1} L(E,s)` before any algebraic-rank language.
- Simple-zero assumption for this deliverable; multiple zeros handled
  separately.
- EC zero counting `N_E(T,2T) << T log T`.
- One reciprocal-derivative input: absolute sum, pointwise lower derivative
  bound, mean-square reciprocal derivative, or contour-principal-value
  theorem.
- Shifted-contour tail estimates for `1/L(E,1+z)`.
- Declared theorem mode: pointwise, oscillatory, or averaged.

## Do Not Promote Unless

- The exact offcentral aggregate is proved `o(u^r)` for `r >= 1`, or retained.
- Rank zero is separated; bounded residues are not promoted to pointwise decay.
- Any use of simple zeros is paired with a quantitative derivative hypothesis.
- Any use of pair correlation is paired with a residue-size hypothesis.
- Any use of zeta reciprocal-derivative literature is labelled analogy only,
  unless a fixed-EC theorem is sourced.
- The contour formulation specifies the height sequence, indentation rule, and
  tail bound.
- No cross-curve universality, BSD evidence, H2 package promotion, or rank substitution
  is made.

## Changed Files

- `handoff-2026-05-11-h1-reciprocal-perron-wave/H1_OFFCENTRAL_RESIDUE_AGGREGATE.md`

## Commands Run

```bash
sed -n '1,220p' ../start.md
./te doctor
sed -n '1,220p' token-economy.yaml
test -f L0_rules.md && sed -n '1,220p' L0_rules.md || true
test -f L1_index.md && sed -n '1,260p' L1_index.md || true
pwd
ls -la
ls -la ..
find .. -maxdepth 2 -name te -type f -o -name token-economy.yaml -type f
../te doctor
sed -n '1,220p' ../token-economy.yaml
wc -l HANDOFF.md L2_facts/farey-claim-ledger.md handoff-2026-05-11-ec-theorem-closure-wave/THEOREM_CLOSURE_SYNTHESIS_2026-05-11.md H1_H2_COMPOSITION_AUDIT.md SOURCE_PACKET.md handoff-2026-05-11-h1-reciprocal-perron-wave/H1_OFFCENTRAL_RESIDUE_AGGREGATE.md 2>/dev/null || true
sed -n '1,260p' HANDOFF.md
sed -n '1,260p' L2_facts/farey-claim-ledger.md
sed -n '1,260p' handoff-2026-05-11-ec-theorem-closure-wave/THEOREM_CLOSURE_SYNTHESIS_2026-05-11.md
sed -n '1,320p' handoff-2026-05-11-ec-theorem-closure-wave/H1_H2_COMPOSITION_AUDIT.md
sed -n '1,360p' handoff-2026-05-11-ec-theorem-closure-wave/SOURCE_PACKET.md
find handoff-2026-05-11-h1-reciprocal-perron-wave -maxdepth 2 -type f -print -exec wc -l {} \;
rg -n "reciprocal|Perron|offcentral|L'|1/L|rank zero|zero" handoff-2026-05-11-ec-theorem-closure-wave handoff-2026-05-11-ec-smoothing-blockers handoff-2026-05-11-ec-s1-explicit-formula-sprint handoff-2026-05-11-ec-h2-mertens-sprint -g '*.md'
command -v pdftotext || true; command -v curl || true
sed -n '1,220p' handoff-2026-05-11-h1-reciprocal-perron-wave/DISPATCH_MANIFEST_2026-05-11.md
git status --short
ls -la /tmp/agent6-source-packet-20260511 2>/dev/null | sed -n '1,120p'
find /tmp -maxdepth 4 \( -name pdftotext -o -name '*pdftotext*' \) 2>/dev/null | head -20
python3 - <<'PY'
try:
 import PyPDF2
 print('PyPDF2 ok')
except Exception as e:
 print('PyPDF2 no', e)
try:
 import pdfminer
 print('pdfminer ok')
except Exception as e:
 print('pdfminer no', e)
PY
find /tmp/agent6-source-packet-20260511/xpdf-tools-mac-4.06 -maxdepth 3 -type f | sed -n '1,120p'
mkdir -p /tmp/agent2-h1-offcentral-20260511 && cd /tmp/agent2-h1-offcentral-20260511 && curl -L --fail -o milinovich_ng_1106.1160.pdf https://arxiv.org/pdf/1106.1160 && /tmp/agent6-source-packet-20260511/xpdf-tools-mac-4.06/bin64/pdftotext -layout milinovich_ng_1106.1160.pdf milinovich_ng_1106.1160.txt && wc -l milinovich_ng_1106.1160.txt && sed -n '1,120p' milinovich_ng_1106.1160.txt
cd /tmp/agent2-h1-offcentral-20260511 && curl -L --fail -o sheth_ec_arxiv_2312.05236.pdf https://arxiv.org/pdf/2312.05236 && /tmp/agent6-source-packet-20260511/xpdf-tools-mac-4.06/bin64/pdftotext -layout sheth_ec_arxiv_2312.05236.pdf sheth_ec_arxiv_2312.05236.txt && rg -n "Theorem 3.1|Corollary 3.2|number of zeros|converges|zeros" sheth_ec_arxiv_2312.05236.txt | sed -n '1,80p' && /tmp/agent6-source-packet-20260511/xpdf-tools-mac-4.06/bin64/pdftotext -layout -f 13 -l 13 sheth_ec_arxiv_2312.05236.pdf - | sed -n '1,180p'
cd /tmp/agent2-h1-offcentral-20260511 && curl -L --fail -o heap_milinovich_2310.03949.pdf https://arxiv.org/pdf/2310.03949 && /tmp/agent6-source-packet-20260511/xpdf-tools-mac-4.06/bin64/pdftotext -layout heap_milinovich_2310.03949.pdf heap_milinovich_2310.03949.txt && sed -n '1,120p' heap_milinovich_2310.03949.txt && rg -n "subfamily|Assuming|Theorem|J|simple|negative" heap_milinovich_2310.03949.txt | sed -n '1,80p'
cd /tmp/agent2-h1-offcentral-20260511 && shasum -a 256 sheth_ec_arxiv_2312.05236.pdf heap_milinovich_2310.03949.pdf milinovich_ng_1106.1160.pdf
cd /tmp/agent2-h1-offcentral-20260511 && /tmp/agent6-source-packet-20260511/xpdf-tools-mac-4.06/bin64/pdftotext -layout -f 1 -l 2 heap_milinovich_2310.03949.pdf - | sed -n '1,180p'
cd /tmp/agent2-h1-offcentral-20260511 && /tmp/agent6-source-packet-20260511/xpdf-tools-mac-4.06/bin64/pdftotext -layout -f 1 -l 2 milinovich_ng_1106.1160.pdf - | sed -n '1,160p'
sed -n '1,180p' handoff-2026-05-11-ec-smoothing-blockers/T1_SMOOTHED_PERRON_THEOREM.md 2>/dev/null || true; sed -n '1,120p' handoff-2026-05-11-ec-theorem-closure-wave/S1_ZERO_SUMMABILITY.md
find '/Users/za/Documents/Farey NOW' -path '*H1_OFFCENTRAL_RESIDUE_AGGREGATE.md' -print
ls -la '/Users/za/Documents/Farey NOW/handoff-2026-05-11-h1-reciprocal-perron-wave' 2>/dev/null || true; ls -la '/Users/za/Documents/Farey NOW/primes-equispaced/handoff-2026-05-11-h1-reciprocal-perron-wave'
mv '/Users/za/Documents/Farey NOW/handoff-2026-05-11-h1-reciprocal-perron-wave/H1_OFFCENTRAL_RESIDUE_AGGREGATE.md' '/Users/za/Documents/Farey NOW/primes-equispaced/handoff-2026-05-11-h1-reciprocal-perron-wave/H1_OFFCENTRAL_RESIDUE_AGGREGATE.md' && rmdir '/Users/za/Documents/Farey NOW/handoff-2026-05-11-h1-reciprocal-perron-wave'
sed -n '1,300p' handoff-2026-05-11-h1-reciprocal-perron-wave/H1_OFFCENTRAL_RESIDUE_AGGREGATE.md
rg -n "^RIGOROUS_REDUCTION|^Confidence:|^## Dependencies|^## Do Not Promote Unless|^## Changed Files|^## Commands Run|curl|pdftotext|rank zero|H-ms|H-cont" handoff-2026-05-11-h1-reciprocal-perron-wave/H1_OFFCENTRAL_RESIDUE_AGGREGATE.md
perl -ne 'print $. . ":" . $_ if /[^\x00-\x7F]/' handoff-2026-05-11-h1-reciprocal-perron-wave/H1_OFFCENTRAL_RESIDUE_AGGREGATE.md
find '/Users/za/Documents/Farey NOW' -path '*H1_OFFCENTRAL_RESIDUE_AGGREGATE.md' -print; git status --short -- handoff-2026-05-11-h1-reciprocal-perron-wave/H1_OFFCENTRAL_RESIDUE_AGGREGATE.md HANDOFF.md L2_facts/farey-claim-ledger.md log.md
```

Bootstrap note: `./te doctor` and `token-economy.yaml` were absent from the
specified workspace; the parent `../te doctor` also reported missing project
config/start files for this workspace. The required `../start.md` and local
handoff files were read directly. Existing dirty files in the repository were
observed and not edited.
