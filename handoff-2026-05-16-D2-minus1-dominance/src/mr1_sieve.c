/* mr1_sieve.c  --  Minus-1 dominance dynamic-curve sieve (PRIMARY implementation)
 *
 * Standalone experimental-NT study of the Chebyshev-bias hierarchy
 * (Aoki-Koyama, J. Number Theory 245 (2023); Rubinstein-Sarnak 1994):
 * computes pi(x; N, a) for N in a fixed set and ALL coprime residues a,
 * snapshotting at a fine, externally-supplied geometric grid of x values
 * so that  pi(x;N,a) - pi(x;N,1)  can be studied as a CURVE in x.
 *
 * Algorithm: odd-only bit-packed segmented sieve of Eratosthenes.
 * Each base prime's next composite is tracked as an ABSOLUTE odd-index
 * (origin = value 3), so there is no per-segment modulo and no
 * carry/skip bookkeeping that could drift.  Plain C99 + libm, no
 * external dependencies.  Fully deterministic.
 *
 * PRIMARY method.  Cross-checked against (i) the pre-existing,
 * independently-authored koyama_replication_bundle/independent_sieve.c
 * (different code path), (ii) the Dirichlet-orthogonality identity
 * (3.1), and (iii) published pi(x) anchors -- harness in analysis/.
 *
 * Build:  cc -O3 -std=c99 -Wall -o mr1_sieve mr1_sieve.c -lm
 * Run:    ./mr1_sieve <Xmax> <grid_file> <out_tsv> <partial_tsv>
 *   <grid_file> : one ascending uint64 x per line (the snapshot grid)
 *   Output rows : "N\tx\ta\tcount"  and a "TOTAL\tN\tx\tpi_x" line per (N,x).
 *
 * Progress + restart: every 2^30 primes a progress line goes to stderr;
 * every snapshot is appended to <partial_tsv> immediately (kill-safe).
 * The run is deterministic: a clean rerun reproduces bit-for-bit.
 */

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <math.h>
#include <time.h>

/* ----- modulus set under study (matches Phase-1: {7,8,11,19,23}) -----
 * The five moduli are COMPILE-TIME CONSTANTS so the per-prime residue
 * tally (the hot path: ~5*pi(Xmax) operations) strength-reduces to
 * multiply-shift / mask instead of hardware division.  Changing the set
 * requires editing both Ns[] and the hardcoded block in record_prime(). */
static const int Ns[] = {7, 8, 11, 19, 23};
#define NN  ((int)(sizeof(Ns)/sizeof(Ns[0])))
#define MAXMOD 23
#define M0 7
#define M1 8
#define M2 11
#define M3 19
#define M4 23

/* ----- segment geometry -----
 * SEG_ODDS odd integers per segment; bitset = SEG_ODDS/8 bytes.
 * 2^18 odds -> 32 KiB bitset == M1 L1d size: small base primes (which do
 * the bulk of the marking) stay resident in L1.  Covers 2^19 ints/seg. */
#define SEG_ODDS  (1u << 18)
#define SEG_BYTES (SEG_ODDS >> 3)

static uint64_t cur[NN][MAXMOD];          /* running residue counts      */

static int       G;                       /* number of grid points       */
static uint64_t *grid;                     /* ascending snapshot x values  */
static uint64_t (*snap)[NN][MAXMOD];      /* snap[g][ni][a]               */
static int       g_ptr = 0;               /* next grid point to cross     */

static uint64_t  total = 0;               /* primes counted so far        */
static const char *partial_path;

static double now_s(void) {
    struct timespec t; clock_gettime(CLOCK_MONOTONIC, &t);
    return t.tv_sec + t.tv_nsec * 1e-9;
}

static void dump_one_snapshot(int g) {
    FILE *f = fopen(partial_path, "a");
    if (!f) return;
    for (int i = 0; i < NN; ++i) {
        uint64_t tot = 0;
        for (int a = 0; a < Ns[i]; ++a) {
            fprintf(f, "%d\t%llu\t%d\t%llu\n",
                    Ns[i], (unsigned long long)grid[g], a,
                    (unsigned long long)snap[g][i][a]);
            tot += snap[g][i][a];
        }
        fprintf(f, "TOTAL\t%d\t%llu\t%llu\n",
                Ns[i], (unsigned long long)grid[g], (unsigned long long)tot);
    }
    fflush(f);
    fclose(f);
}

/* snapshot every grid point strictly below the just-emitted prime p
 * (so the snapshot counts reflect exactly the primes < p, i.e. <= grid[g]). */
static void maybe_snapshot(uint64_t p) {
    while (g_ptr < G && p > grid[g_ptr]) {
        for (int i = 0; i < NN; ++i)
            for (int a = 0; a < Ns[i]; ++a)
                snap[g_ptr][i][a] = cur[i][a];
        dump_one_snapshot(g_ptr);
        fprintf(stderr, "[mr1] snapshot x=%llu  pi=%llu  (grid %d/%d)\n",
                (unsigned long long)grid[g_ptr],
                (unsigned long long)total, g_ptr + 1, G);
        ++g_ptr;
    }
}

/* hot path: hardcoded constant moduli -> strength-reduced, no hw divide.
 * snapshot fast-check is inlined; the (rare) crossing calls maybe_snapshot. */
static inline void record_prime(uint64_t p) {
    if (__builtin_expect(g_ptr < G && p > grid[g_ptr], 0))
        maybe_snapshot(p);
    cur[0][p % M0] += 1;
    cur[1][p % M1] += 1;
    cur[2][p % M2] += 1;
    cur[3][p % M3] += 1;
    cur[4][p % M4] += 1;
    ++total;
}

/* ---- base primes up to sqrt(Xmax) ---- */
static uint64_t *bp;        /* odd base prime values (>=3)                 */
static uint64_t *bp_next;   /* ABSOLUTE odd-index of next composite to mark */
static size_t    nbp;

/* odd-index <-> value:  aidx(v) = (v-3)/2 ;  value(j) = 3 + 2*j           */
static void sieve_base(uint64_t lim) {
    uint8_t *sv = calloc(lim + 1, 1);
    if (!sv) { perror("calloc base"); exit(1); }
    for (uint64_t i = 2; i * i <= lim; ++i)
        if (!sv[i]) for (uint64_t j = i * i; j <= lim; j += i) sv[j] = 1;
    nbp = 0;
    bp = malloc(sizeof(uint64_t) * (lim / 4 + 64));
    for (uint64_t i = 3; i <= lim; i += 2) if (!sv[i]) bp[nbp++] = i;
    bp_next = malloc(sizeof(uint64_t) * (nbp + 1));
    for (size_t k = 0; k < nbp; ++k) {
        uint64_t p = bp[k];
        bp_next[k] = (p * p - 3ULL) >> 1;     /* first composite = p*p (odd) */
    }
    free(sv);
}

int main(int argc, char **argv) {
    if (argc < 5) {
        fprintf(stderr,
          "usage: %s <Xmax> <grid_file> <out_tsv> <partial_tsv>\n", argv[0]);
        return 2;
    }
    uint64_t Xmax = strtoull(argv[1], NULL, 10);
    const char *grid_path = argv[2];
    const char *out_path  = argv[3];
    partial_path          = argv[4];

    FILE *gf = fopen(grid_path, "r");
    if (!gf) { perror("open grid"); return 1; }
    int cap = 4096; grid = malloc(sizeof(uint64_t) * cap); G = 0;
    char line[64];
    while (fgets(line, sizeof line, gf)) {
        if (line[0] == '#' || line[0] == '\n' || line[0] == '\r') continue;
        if (G == cap) { cap *= 2; grid = realloc(grid, sizeof(uint64_t)*cap); }
        grid[G++] = strtoull(line, NULL, 10);
    }
    fclose(gf);
    for (int i = 1; i < G; ++i)
        if (grid[i] <= grid[i-1]) {
            fprintf(stderr, "[mr1] FATAL grid not strictly ascending at %d\n", i);
            return 1;
        }
    if (G && grid[G-1] > Xmax) {
        fprintf(stderr, "[mr1] FATAL last grid point %llu > Xmax %llu\n",
                (unsigned long long)grid[G-1], (unsigned long long)Xmax);
        return 1;
    }
    snap = calloc(G, sizeof(*snap));

    fprintf(stderr, "[mr1] Xmax=%llu  grid=%d pts  seg=%u odds (%u B bitset)\n",
            (unsigned long long)Xmax, G, SEG_ODDS, SEG_BYTES);

    uint64_t sq = (uint64_t)floor(sqrt((double)Xmax)) + 2;
    sieve_base(sq);
    fprintf(stderr, "[mr1] base primes <=%llu : %zu\n",
            (unsigned long long)sq, nbp);

    record_prime(2);                          /* the only even prime */

    if (Xmax >= 3) {
        uint8_t *seg = malloc(SEG_BYTES);
        if (!seg) { perror("malloc seg"); return 1; }
        double t0 = now_s();
        uint64_t next_prog = (1ULL << 30);

        uint64_t low = 3;                     /* low is always odd          */
        while (low <= Xmax) {
            uint64_t high = low + 2ULL * SEG_ODDS - 2;   /* last odd in seg */
            if (high > Xmax) high = Xmax;
            if (!(high & 1ULL)) high -= 1;               /* keep high odd   */
            if (high < low) break;

            uint64_t A      = (low - 3ULL) >> 1;         /* base odd-index  */
            uint64_t A_end  = A + (((high - low) >> 1) + 1); /* exclusive    */
            uint32_t n_odds = (uint32_t)(A_end - A);
            uint32_t n_words = (n_odds + 63u) >> 6;

            memset(seg, 0, (size_t)n_words << 3);         /* clear full words */

            for (size_t k = 0; k < nbp; ++k) {
                uint64_t p = bp[k];
                if (p * p > high) break;          /* no composite in/before */
                uint64_t j = bp_next[k];
                if (j >= A_end) continue;         /* first composite later  */
                for (; j < A_end; j += p) {
                    uint32_t b = (uint32_t)(j - A);
                    seg[b >> 3] |= (uint8_t)(1u << (b & 7));
                }
                bp_next[k] = j;                   /* absolute: no carry bug */
            }

            /* word-at-a-time extraction: 1-bit (after complement) = prime */
            const uint64_t *segw = (const uint64_t *)seg;
            for (uint32_t w = 0; w < n_words; ++w) {
                uint64_t bits = ~segw[w];
                if (w == n_words - 1) {
                    uint32_t rem = n_odds - (w << 6);     /* 1..64 valid    */
                    if (rem < 64) bits &= ((uint64_t)1 << rem) - 1;
                }
                uint64_t vbase = low + ((uint64_t)(w << 6) << 1);
                while (bits) {
                    uint32_t t  = (uint32_t)__builtin_ctzll(bits);
                    record_prime(vbase + ((uint64_t)t << 1));
                    bits &= bits - 1;
                }
            }
            if (total >= next_prog) {
                double s = now_s() - t0;
                fprintf(stderr,
                  "[mr1] primes=%llu p~=%llu elapsed=%.1fs rate=%.3e p/s\n",
                  (unsigned long long)total, (unsigned long long)high,
                  s, total / (s > 0 ? s : 1));
                next_prog += (1ULL << 30);
            }
            low = high + 2;                       /* stays odd */
        }
        free(seg);
    }

    /* flush remaining grid points (x in [last crossed, Xmax]) */
    while (g_ptr < G) {
        for (int i = 0; i < NN; ++i)
            for (int a = 0; a < Ns[i]; ++a)
                snap[g_ptr][i][a] = cur[i][a];
        dump_one_snapshot(g_ptr);
        ++g_ptr;
    }

    FILE *out = fopen(out_path, "w");
    if (!out) { perror("open out"); return 1; }
    fprintf(out, "# mr1_sieve  Xmax=%llu  total_pi=%llu  grid=%d\n",
            (unsigned long long)Xmax, (unsigned long long)total, G);
    fprintf(out, "# schema: N<TAB>x<TAB>a<TAB>count  and  TOTAL<TAB>N<TAB>x<TAB>pi_x\n");
    for (int g = 0; g < G; ++g)
        for (int i = 0; i < NN; ++i) {
            uint64_t tot = 0;
            for (int a = 0; a < Ns[i]; ++a) {
                fprintf(out, "%d\t%llu\t%d\t%llu\n",
                        Ns[i], (unsigned long long)grid[g], a,
                        (unsigned long long)snap[g][i][a]);
                tot += snap[g][i][a];
            }
            fprintf(out, "TOTAL\t%d\t%llu\t%llu\n",
                    Ns[i], (unsigned long long)grid[g], (unsigned long long)tot);
        }
    fclose(out);
    fprintf(stderr, "[mr1] DONE total_pi(%llu)=%llu\n",
            (unsigned long long)Xmax, (unsigned long long)total);
    return 0;
}
