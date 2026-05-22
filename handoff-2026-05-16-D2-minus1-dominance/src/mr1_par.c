/* mr1_par.c -- range-split PARALLEL minus-1-dominance dynamic-curve sieve.
 *
 * Same observable as mr1_sieve.c (pi(x;N,a) for N in {7,8,11,19,23}, all
 * coprime a, snapshotted on an external geometric x-grid) but the range
 * [3, Xmax] is partitioned into NCHUNK contiguous value-chunks consumed
 * by T pthreads via an atomic work counter.
 *
 * DETERMINISM: each chunk is sieved independently and produces (a) its
 * per-(N,a) total over the chunk and (b) for every grid point inside the
 * chunk, the LOCAL cumulative per-(N,a) count of primes in [chunk_lo,
 * grid].  The final global value is a fixed-order prefix combine:
 *   pi(grid;N,a) = sum_{chunks fully below grid} chunk_total
 *                + local_cumulative(grid) of the chunk containing it
 *                + [p=2 contribution, chunk 0 only].
 * Output is identical regardless of thread count / scheduling, so a
 * rerun reproduces bit-for-bit and matches the serial mr1_sieve.c.
 *
 * Build:  cc -O3 -std=c99 -Wall -fno-strict-aliasing -pthread -o mr1_par mr1_par.c -lm
 * Run:    ./mr1_par <Xmax> <grid_file> <out_tsv> <nthreads> [nchunks]
 */

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <math.h>
#include <time.h>
#include <pthread.h>

static const int Ns[] = {7, 8, 11, 19, 23};
#define NN 5
#define MAXMOD 23
#define M0 7
#define M1 8
#define M2 11
#define M3 19
#define M4 23

#define SEG_ODDS  (1u << 18)          /* 32 KiB bitset, L1-resident */
#define SEG_BYTES (SEG_ODDS >> 3)

static int       G;
static uint64_t *grid;

/* per-chunk results */
static int       NCHUNK;
static uint64_t  Xmax;
static uint64_t *chunk_lo, *chunk_hi;            /* [lo,hi] inclusive, odd-safe */
static uint64_t (*chunk_tot)[NN][MAXMOD];        /* chunk_tot[c][ni][a]         */
/* local cumulative snapshots: only grid points inside chunk c are valid.
 * stored flat as locsnap[c][g][ni][a]; we only fill g in [g0[c],g1[c]).   */
static uint64_t (*locsnap)[NN][MAXMOD];          /* size NCHUNK*G            */
static int      *g0, *g1;                        /* grid-index span per chunk */

/* shared read-only base primes up to sqrt(Xmax) */
static uint64_t *bp;
static size_t    nbp;

static double now_s(void){ struct timespec t; clock_gettime(CLOCK_MONOTONIC,&t);
    return t.tv_sec + t.tv_nsec*1e-9; }

static void sieve_base(uint64_t lim){
    uint8_t *sv = calloc(lim+1,1);
    if(!sv){ perror("calloc base"); exit(1);}
    for(uint64_t i=2;i*i<=lim;++i) if(!sv[i]) for(uint64_t j=i*i;j<=lim;j+=i) sv[j]=1;
    nbp=0; bp=malloc(sizeof(uint64_t)*(lim/4+64));
    for(uint64_t i=3;i<=lim;i+=2) if(!sv[i]) bp[nbp++]=i;
    free(sv);
}

static int next_chunk;                       /* atomic work counter */
static pthread_mutex_t cmtx = PTHREAD_MUTEX_INITIALIZER;

/* sieve one chunk c over odd values in [chunk_lo[c], chunk_hi[c]].
 * Per-chunk absolute next-composite index (origin = value 3): the
 * `low % p` start is computed ONCE per base prime per chunk, then
 * carried across this chunk's segments with no further division -- the
 * same bookkeeping as serial mr1_sieve.c. */
static void do_chunk(int c){
    uint64_t lo = chunk_lo[c], hi = chunk_hi[c];
    uint64_t cnt[NN][MAXMOD]; memset(cnt,0,sizeof cnt);
    int gi = g0[c];

    if (lo < 3) lo = 3;
    if (!(lo & 1ULL)) lo += 1;                 /* lo odd */
    if (lo > hi){                              /* empty chunk */
        while (gi < g1[c]){ memcpy(locsnap[(size_t)c*G+gi],cnt,sizeof cnt);++gi;}
        memcpy(chunk_tot[c], cnt, sizeof cnt); return;
    }

    uint8_t  *seg     = malloc(SEG_BYTES);
    uint64_t *bp_next = malloc(sizeof(uint64_t)*nbp);   /* abs odd-index */
    if(!seg||!bp_next){ perror("malloc chunk"); exit(1);}

    /* first composite to mark in this chunk, per base prime, as the
     * absolute odd-index aidx(v)=(v-3)/2 of max(p*p, first odd multiple
     * of p that is >= lo). */
    for(size_t k=0;k<nbp;++k){
        uint64_t p=bp[k], start=p*p;
        if (start < lo){
            uint64_t r = lo % p;
            start = (r==0)? lo : lo + (p - r);
            if (!(start & 1ULL)) start += p;          /* keep odd */
        }
        bp_next[k] = (start - 3ULL) >> 1;
    }

    uint64_t low = lo;
    while (low <= hi){
        uint64_t high = low + 2ULL*SEG_ODDS - 2;
        if (high > hi) high = hi;
        if (!(high & 1ULL)) high -= 1;
        if (high < low) break;
        uint64_t A     = (low - 3ULL) >> 1;
        uint64_t A_end = A + (((high-low)>>1)+1);
        uint32_t n_odds = (uint32_t)(A_end-A);
        uint32_t n_words = (n_odds+63u)>>6;
        memset(seg,0,(size_t)n_words<<3);

        for(size_t k=0;k<nbp;++k){
            uint64_t p = bp[k];
            if (p*p > high) break;
            uint64_t j = bp_next[k];
            if (j >= A_end) continue;
            for(; j < A_end; j += p){
                uint32_t b=(uint32_t)(j-A);
                seg[b>>3] |= (uint8_t)(1u<<(b&7));
            }
            bp_next[k] = j;
        }

        const uint64_t *segw=(const uint64_t*)seg;
        for(uint32_t w=0; w<n_words; ++w){
            uint64_t bits=~segw[w];
            if (w==n_words-1){ uint32_t rem=n_odds-(w<<6);
                if(rem<64) bits &= ((uint64_t)1<<rem)-1; }
            uint64_t vbase = low + ((uint64_t)(w<<6)<<1);
            while(bits){
                uint32_t t=(uint32_t)__builtin_ctzll(bits);
                uint64_t pv = vbase + ((uint64_t)t<<1);
                while (gi < g1[c] && pv > grid[gi]){
                    memcpy(locsnap[(size_t)c*G+gi], cnt, sizeof cnt);
                    ++gi;
                }
                cnt[0][pv % M0]++; cnt[1][pv % M1]++; cnt[2][pv % M2]++;
                cnt[3][pv % M3]++; cnt[4][pv % M4]++;
                bits &= bits - 1;                 /* clear consumed bit */
            }
        }
        low = high + 2;
    }
    free(seg); free(bp_next);
    while (gi < g1[c]){ memcpy(locsnap[(size_t)c*G+gi], cnt, sizeof cnt); ++gi; }
    memcpy(chunk_tot[c], cnt, sizeof cnt);
}

static void *worker(void *arg){
    (void)arg;
    for(;;){
        int c;
        pthread_mutex_lock(&cmtx);
        c = next_chunk < NCHUNK ? next_chunk++ : -1;
        pthread_mutex_unlock(&cmtx);
        if (c < 0) break;
        double t0 = now_s();
        do_chunk(c);
        fprintf(stderr,"[par] chunk %d/%d [%llu,%llu] done %.1fs\n",
                c+1,NCHUNK,(unsigned long long)chunk_lo[c],
                (unsigned long long)chunk_hi[c], now_s()-t0);
    }
    return NULL;
}

int main(int argc,char**argv){
    if(argc<5){ fprintf(stderr,
        "usage: %s <Xmax> <grid> <out_tsv> <nthreads> [nchunks]\n",argv[0]);
        return 2; }
    Xmax = strtoull(argv[1],NULL,10);
    const char *grid_path=argv[2], *out_path=argv[3];
    int T = atoi(argv[4]);
    NCHUNK = (argc>5)? atoi(argv[5]) : T*32;
    if (T<1) T=1; if (NCHUNK<1) NCHUNK=1;

    FILE *gf=fopen(grid_path,"r"); if(!gf){perror("grid");return 1;}
    int cap=4096; grid=malloc(sizeof(uint64_t)*cap); G=0; char ln[64];
    while(fgets(ln,sizeof ln,gf)){
        if(ln[0]=='#'||ln[0]=='\n'||ln[0]=='\r') continue;
        if(G==cap){cap*=2; grid=realloc(grid,sizeof(uint64_t)*cap);}
        grid[G++]=strtoull(ln,NULL,10);
    }
    fclose(gf);
    for(int i=1;i<G;++i) if(grid[i]<=grid[i-1]){
        fprintf(stderr,"[par] FATAL grid not ascending @%d\n",i); return 1; }
    if(G&&grid[G-1]>Xmax){ fprintf(stderr,"[par] FATAL grid>Xmax\n"); return 1; }

    uint64_t sq=(uint64_t)floor(sqrt((double)Xmax))+2;
    sieve_base(sq);
    fprintf(stderr,"[par] Xmax=%llu grid=%d base_primes=%zu T=%d NCHUNK=%d\n",
            (unsigned long long)Xmax,G,nbp,T,NCHUNK);

    /* contiguous equal-width chunks over [3,Xmax]; boundaries made odd */
    chunk_lo=malloc(sizeof(uint64_t)*NCHUNK);
    chunk_hi=malloc(sizeof(uint64_t)*NCHUNK);
    chunk_tot=calloc(NCHUNK,sizeof(*chunk_tot));
    g0=malloc(sizeof(int)*NCHUNK); g1=malloc(sizeof(int)*NCHUNK);
    locsnap=calloc((size_t)NCHUNK*G,sizeof(*locsnap));
    if(!locsnap){ perror("calloc locsnap"); return 1; }

    uint64_t span = (Xmax-3)/NCHUNK;
    for(int c=0;c<NCHUNK;++c){
        uint64_t lo = 3 + (uint64_t)c*span;
        uint64_t hi = (c==NCHUNK-1)? Xmax : (3 + (uint64_t)(c+1)*span - 1);
        chunk_lo[c]=lo; chunk_hi[c]=hi;
    }
    /* assign each grid point to the chunk whose [lo,hi] contains it */
    {
        int gi=0;
        for(int c=0;c<NCHUNK;++c){
            g0[c]=gi;
            while(gi<G && grid[gi]>=chunk_lo[c] && grid[gi]<=chunk_hi[c]) ++gi;
            g1[c]=gi;
        }
        /* grid points below chunk 0 lo (none, since grid>=1e6>3) or above
         * last hi (none, grid<=Xmax) -> all assigned. sanity: */
        if (gi!=G){ fprintf(stderr,"[par] FATAL grid assign %d/%d\n",gi,G);
            return 1; }
    }

    next_chunk=0;
    pthread_t *th=malloc(sizeof(pthread_t)*T);
    double t0=now_s();
    for(int i=0;i<T;++i) pthread_create(&th[i],NULL,worker,NULL);
    for(int i=0;i<T;++i) pthread_join(th[i],NULL);
    fprintf(stderr,"[par] all chunks done %.1fs, combining\n",now_s()-t0);

    /* deterministic prefix combine.
     * running[ni][a] = sum of chunk_tot for all chunks strictly before the
     * chunk that owns the current grid point. Grid points are ascending and
     * chunk spans are contiguous & ascending, so we can sweep chunks. */
    FILE *out=fopen(out_path,"w"); if(!out){perror("out");return 1;}
    fprintf(out,"# mr1_par Xmax=%llu grid=%d T=%d NCHUNK=%d\n",
            (unsigned long long)Xmax,G,T,NCHUNK);
    fprintf(out,"# schema: N<TAB>x<TAB>a<TAB>count  and  TOTAL<TAB>N<TAB>x<TAB>pi_x\n");

    uint64_t running[NN][MAXMOD]; memset(running,0,sizeof running);
    for(int c=0;c<NCHUNK;++c){
        for(int gi=g0[c]; gi<g1[c]; ++gi){
            uint64_t (*ls)[MAXMOD] = locsnap[(size_t)c*G+gi];
            for(int i=0;i<NN;++i){
                uint64_t tot=0;
                /* p=2 is never in any chunk (chunks start at value 3) but
                 * every grid x >= 1e6 > 2, so inject it into class 2%N. */
                int two_cls = 2 % Ns[i];
                for(int a=0;a<Ns[i];++a){
                    uint64_t v = running[i][a] + ls[i][a]
                               + ((a==two_cls)?1ULL:0ULL);
                    fprintf(out,"%d\t%llu\t%d\t%llu\n",
                        Ns[i],(unsigned long long)grid[gi],a,
                        (unsigned long long)v);
                    tot += v;
                }
                fprintf(out,"TOTAL\t%d\t%llu\t%llu\n",
                    Ns[i],(unsigned long long)grid[gi],(unsigned long long)tot);
            }
        }
        for(int i=0;i<NN;++i) for(int a=0;a<Ns[i];++a)
            running[i][a]+=chunk_tot[c][i][a];
    }
    fclose(out);
    fprintf(stderr,"[par] DONE\n");
    return 0;
}
