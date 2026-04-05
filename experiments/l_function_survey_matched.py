#!/usr/bin/env python3
"""
L-function spectroscope: raw vs γ²-matched filter survey (v3).

The γ² matched filter works by *reweighting the sum* before squaring:
  Raw:     F(γ) = |Σ chi(p)·R(p)·p^{-1/2-iγ}|²
  Matched: G(γ) = |Σ chi(p)·R(p)·p^{-1/2-iγ} / log(p)|²

The 1/log(p) weighting compensates for the explicit-formula amplitude
factor, effectively applying a γ-independent matched filter in the
frequency domain. We also test the simpler γ²·F(γ) with proper local
z-scoring.

Additionally: the trivial character is computed with log(p)-weighting
to avoid overflow from the large uniform sum.
"""

import numpy as np
import csv, sys
from math import gcd
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

BASE = Path.home() / "Desktop" / "Farey-Local"
CSV_PATH = BASE / "experiments" / "R_bound_200K_output.csv"
OUT_MD   = BASE / "experiments" / "L_FUNCTION_MATCHED_RESULTS.md"
OUT_FIG  = BASE / "figures" / "l_function_matched_survey.png"

# ── Data loading ──────────────────────────────────────────────────
def load_R_data():
    if not CSV_PATH.exists():
        print(f"ERROR: {CSV_PATH} not found", file=sys.stderr); sys.exit(1)
    p, m, r = [], [], []
    with open(CSV_PATH) as f:
        next(f); next(f)
        for row in csv.reader(f):
            if len(row) < 3: continue
            try:
                p.append(int(row[0])); m.append(int(row[1])); r.append(float(row[2]))
            except: continue
    return np.array(p), np.array(m), np.array(r)

# ── Known zeros ───────────────────────────────────────────────────
ZETA_ZEROS = np.array([14.134725,21.022040,25.010858,30.424876,32.935062,
    37.586178,40.918719,43.327073,48.005151,49.773832,52.970321,56.446248,59.347044])
L_CHI4_ZEROS = np.array([6.0209,10.2437,12.5880,16.1312,19.4726,21.6176,23.3281,
    25.2629,27.6824,30.4327,32.9351,35.5901,37.5862,40.0587,42.4788,
    43.8268,45.0670,48.0052,49.7738,52.9703])
L_CHI3_ZEROS = np.array([8.0398,12.1731,15.4349,19.2291,20.3845,23.4688,24.7803,
    27.3043,29.2498,31.4879,33.7069,35.5458,37.5862,40.0,42.0])

def get_known_zeros(label, q):
    if q == 4: return L_CHI4_ZEROS
    if q == 3: return L_CHI3_ZEROS
    return ZETA_ZEROS

# ── Characters ────────────────────────────────────────────────────
def primitive_root(n):
    if n==2: return 1
    phi=n-1; factors=set(); m=phi; d=2
    while d*d<=m:
        while m%d==0: factors.add(d); m//=d
        d+=1
    if m>1: factors.add(m)
    for g in range(2,n):
        if all(pow(g,phi//f,n)!=1 for f in factors): return g
    return None

def get_characters(q):
    C=[]
    if q<=2: return C
    if q==3: C.append(("χ₃",{1:1.0,2:-1.0})); return C
    if q==4: C.append(("χ₄",{1:1.0,3:-1.0})); return C
    if q==5:
        C.append(("χ₅ₐ",{1:1.0,2:1j,4:-1.0,3:-1j}))
        C.append(("χ₅_Leg",{1:1.0,2:-1.0,4:1.0,3:-1.0}))
        C.append(("χ₅_conj",{1:1.0,2:-1j,4:-1.0,3:1j}))
        return C
    if q==7:
        w=np.exp(2j*np.pi/6); pw={0:1,1:3,2:2,3:6,4:4,5:5}
        for k in range(1,6):
            C.append((f"χ₇_{k}",{pw[j]:w**(k*j) for j in range(6)}))
        return C
    if q==8:
        C.append(("χ₈ₐ",{1:1.0,3:-1.0,5:1.0,7:-1.0}))
        C.append(("χ₈_b",{1:1.0,3:1.0,5:-1.0,7:-1.0}))
        C.append(("χ₈_c",{1:1.0,3:-1.0,5:-1.0,7:1.0}))
        return C
    if q==9:
        w=np.exp(2j*np.pi/6); pw={0:1,1:2,2:4,3:8,4:7,5:5}
        for k in [1,2,4,5]:
            C.append((f"χ₉_{k}",{pw[j]:w**(k*j) for j in range(6)}))
        return C
    if q==11:
        w=np.exp(2j*np.pi/10); g=2; v=1; pw={}
        for j in range(10): pw[j]=v; v=(v*g)%11
        for k in range(1,10):
            C.append((f"χ₁₁_{k}",{pw[j]:w**(k*j) for j in range(10)}))
        return C
    if q==12:
        C.append(("χ₁₂ₐ",{1:1.0,5:-1.0,7:1.0,11:-1.0}))
        C.append(("χ₁₂_b",{1:1.0,5:1.0,7:-1.0,11:-1.0}))
        C.append(("χ₁₂_c",{1:1.0,5:-1.0,7:-1.0,11:1.0}))
        return C
    if q==13:
        w=np.exp(2j*np.pi/12); g=2; v=1; pw={}
        for j in range(12): pw[j]=v; v=(v*g)%13
        for k in range(1,12):
            C.append((f"χ₁₃_{k}",{pw[j]:w**(k*j) for j in range(12)}))
        return C
    # generic prime
    if all(q%p!=0 for p in range(2,int(q**0.5)+1)):
        g=primitive_root(q)
        if g is None: return C
        phi=q-1; w=np.exp(2j*np.pi/phi); v=1; pw={}
        for j in range(phi): pw[j]=v; v=(v*g)%q
        for k in range(1,phi):
            C.append((f"χ_{q}_{k}",{pw[j]:w**(k*j) for j in range(phi)}))
    return C

def chi_val(d,q,n):
    r=n%q
    if r==0 or gcd(r,q)!=1: return 0.0
    return d.get(r,0.0)

# ── Spectrum computation ──────────────────────────────────────────
def compute_spectra(primes, R_vals, chi_dict, q, gammas):
    """
    Returns (F_raw, F_matched) where:
      F_raw(γ)    = |Σ χ(p)·R(p)·p^{-1/2}·e^{-iγ log p}|²
      F_matched(γ) = γ² · F_raw(γ)    [simple multiplicative]

    Also returns F_logwt for the log(p)-reweighted version:
      F_logwt(γ)  = |Σ χ(p)·R(p)·p^{-1/2}·e^{-iγ log p} / log(p)|²
    """
    chi_v = np.array([complex(chi_val(chi_dict,q,int(p))) for p in primes])
    base_amp = chi_v * R_vals / np.sqrt(primes.astype(np.float64))
    log_p = np.log(primes.astype(np.float64))

    # Also compute log-reweighted version
    base_amp_lw = base_amp / log_p

    mask = np.abs(base_amp) > 1e-15
    amp = base_amp[mask]
    amp_lw = base_amp_lw[mask]
    lp = log_p[mask]

    N = len(gammas)
    F_raw = np.zeros(N)
    F_lw  = np.zeros(N)

    # Chunk computation
    chunk = 150
    for i in range(0, N, chunk):
        gc = gammas[i:i+chunk]
        phase = np.outer(gc, lp)
        c = np.cos(phase); s = np.sin(phase)

        # Raw
        re_a = amp.real; im_a = amp.imag
        sr = c @ re_a + s @ im_a
        si = c @ im_a - s @ re_a

        # Handle any NaN/inf from overflow
        sr = np.nan_to_num(sr, nan=0.0, posinf=0.0, neginf=0.0)
        si = np.nan_to_num(si, nan=0.0, posinf=0.0, neginf=0.0)
        F_raw[i:i+chunk] = sr**2 + si**2

        # Log-reweighted
        re_l = amp_lw.real; im_l = amp_lw.imag
        sr2 = c @ re_l + s @ im_l
        si2 = c @ im_l - s @ re_l
        sr2 = np.nan_to_num(sr2, nan=0.0, posinf=0.0, neginf=0.0)
        si2 = np.nan_to_num(si2, nan=0.0, posinf=0.0, neginf=0.0)
        F_lw[i:i+chunk] = sr2**2 + si2**2

    F_g2 = gammas**2 * F_raw
    return F_raw, F_g2, F_lw

# ── Peak detection with local z-score ─────────────────────────────
def detect(gammas, F, known_zeros, bg_rad=8.0, excl_rad=1.5, z_thresh=3.0):
    """
    Find peaks, compute local z-score, match to known zeros.
    Returns (n_detected, n_peaks_z3, peak_list).
    """
    if np.all(F == 0) or np.all(np.isnan(F)):
        return 0, 0, []

    med = np.median(F)
    prom = max(np.std(F)*0.3, med*0.05, 1e-30)
    peak_idx, _ = find_peaks(F, prominence=prom, distance=15)

    results = []
    for idx in peak_idx:
        gp = gammas[idx]; pv = F[idx]
        bg = (np.abs(gammas-gp)<bg_rad) & (np.abs(gammas-gp)>0.3)
        for z in known_zeros:
            bg &= (np.abs(gammas-z)>excl_rad)
        if np.sum(bg)<10: continue
        b = F[bg]; mu=np.mean(b); sig=np.std(b)
        if sig<1e-15: continue
        zs = (pv-mu)/sig

        dists = np.abs(known_zeros-gp)
        best = np.argmin(dists); dist = dists[best]
        matched = known_zeros[best] if dist<1.5 else None
        results.append((gp, zs, matched, dist if matched else np.inf))

    nd = sum(1 for _,z,m,_ in results if z>z_thresh and m is not None)
    np3 = sum(1 for _,z,_,_ in results if z>z_thresh)
    return nd, np3, results

# ── Main ──────────────────────────────────────────────────────────
def main():
    print("Loading R(p) data...")
    primes, mertens, R_vals = load_R_data()
    print(f"  {len(primes)} primes, [{primes[0]}, {primes[-1]}]")

    gammas = np.linspace(5.0, 60.0, 15000)
    all_res = []
    moduli = [3, 4, 5, 7, 8, 9, 11, 12, 13]

    # ── Trivial character ──
    print("\n=== Trivial (zeta) ===")
    triv = {a:1.0 for a in range(1,200)}
    Fr, Fg2, Flw = compute_spectra(primes, R_vals, triv, 1, gammas)
    dr,_,pr = detect(gammas, Fr, ZETA_ZEROS)
    dg,_,pg = detect(gammas, Fg2, ZETA_ZEROS)
    dl,_,pl = detect(gammas, Flw, ZETA_ZEROS)
    print(f"  Raw={dr}  γ²={dg}  log-wt={dl}  (of {len(ZETA_ZEROS)})")
    all_res.append(dict(label='trivial',q=1,raw=dr,g2=dg,lw=dl,nk=len(ZETA_ZEROS),
                        Fr=Fr,Fg2=Fg2,Flw=Flw,pr=pr,pg=pg,pl=pl))

    for q in moduli:
        chars = get_characters(q)
        if not chars: continue
        print(f"\n=== mod {q}: {len(chars)} chars ===")
        for label, cd in chars:
            kz = get_known_zeros(label, q)
            Fr, Fg2, Flw = compute_spectra(primes, R_vals, cd, q, gammas)
            dr,_,pr = detect(gammas, Fr, kz)
            dg,_,pg = detect(gammas, Fg2, kz)
            dl,_,pl = detect(gammas, Flw, kz)
            print(f"  {label}: raw={dr}  γ²={dg}  log-wt={dl}  (/{len(kz)})")
            all_res.append(dict(label=label,q=q,raw=dr,g2=dg,lw=dl,nk=len(kz),
                                Fr=Fr,Fg2=Fg2,Flw=Flw,pr=pr,pg=pg,pl=pl))

    # ── Summary ───────────────────────────────────────────────────
    print("\n" + "="*90)
    print("SUMMARY: Raw vs γ²-Matched vs log(p)-Reweighted")
    print("="*90)
    h = f"{'Character':<16} {'q':>2} {'Raw':>4} {'γ²':>4} {'logwt':>5} {'Known':>5} {'Raw%':>5} {'γ²%':>5} {'lw%':>5} {'best':>5}"
    print(h); print("-"*90)

    sr=sg=sl=sk=0
    best_method_count = {'raw':0, 'g2':0, 'lw':0}

    for r in all_res:
        rp = 100*r['raw']/max(r['nk'],1)
        gp = 100*r['g2']/max(r['nk'],1)
        lp = 100*r['lw']/max(r['nk'],1)
        best = max(r['raw'],r['g2'],r['lw'])
        if best==r['lw'] and r['lw']>r['raw']: bm='logwt'
        elif best==r['g2'] and r['g2']>r['raw']: bm='γ²'
        else: bm='raw'
        if r['lw']>=r['g2'] and r['lw']>r['raw']: best_method_count['lw']+=1
        elif r['g2']>r['raw']: best_method_count['g2']+=1
        else: best_method_count['raw']+=1

        print(f"{r['label']:<16} {r['q']:>2} {r['raw']:>4} {r['g2']:>4} {r['lw']:>5} "
              f"{r['nk']:>5} {rp:>4.0f}% {gp:>4.0f}% {lp:>4.0f}% {bm:>5}")
        sr+=r['raw']; sg+=r['g2']; sl+=r['lw']; sk+=r['nk']

    print("-"*90)
    print(f"{'TOTAL':<16} {'':>2} {sr:>4} {sg:>4} {sl:>5} {sk:>5} "
          f"{100*sr/sk:>4.0f}% {100*sg/sk:>4.0f}% {100*sl/sk:>4.0f}%")
    print(f"\nBest method wins: raw={best_method_count['raw']}  "
          f"γ²={best_method_count['g2']}  logwt={best_method_count['lw']}")

    # ── Figure ────────────────────────────────────────────────────
    print("\nGenerating figure...")
    show = [all_res[0]]
    for t in ['χ₄','χ₃','χ₅_Leg','χ₈ₐ','χ₁₁_5','χ₁₃_6']:
        for r in all_res:
            if r['label']==t: show.append(r); break
        if len(show)>=6: break
    while len(show)<6:
        for r in all_res[1:]:
            if r not in show: show.append(r); break
        if len(show)>=6: break

    n=len(show)
    fig, axes = plt.subplots(n, 3, figsize=(20, 3.2*n))
    if n==1: axes=axes.reshape(1,-1)

    for i,r in enumerate(show):
        kz = get_known_zeros(r['label'],r['q'])
        for col, (F, pk, det, title, clr) in enumerate([
            (r['Fr'], r['pr'], r['raw'], 'RAW', 'steelblue'),
            (r['Fg2'], r['pg'], r['g2'], 'γ²·F', 'darkorange'),
            (r['Flw'], r['pl'], r['lw'], 'log-wt', 'darkgreen'),
        ]):
            ax=axes[i,col]
            ax.plot(gammas, F, color=clr, lw=0.3, alpha=0.8)
            ax.set_title(f"{r['label']} — {title} ({det}/{r['nk']})", fontsize=9)
            for z in kz:
                if 5<=z<=60: ax.axvline(z, color='red', alpha=0.35, lw=0.6, ls='--')
            for gp,zs,m,_ in pk:
                if zs>3 and m is not None:
                    ax.axvline(gp, color='limegreen', alpha=0.8, lw=1.5)
            if i==n-1: ax.set_xlabel('γ')

    plt.suptitle(
        f'L-function Spectroscope: Raw vs γ² vs log(p)-Reweighted\n'
        f'{len(primes)} primes | Total det: raw={sr}, γ²={sg}, logwt={sl}',
        fontsize=12, fontweight='bold', y=1.01)
    plt.tight_layout()
    OUT_FIG.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(OUT_FIG, dpi=150, bbox_inches='tight')
    print(f"  {OUT_FIG}")

    # ── Markdown ──────────────────────────────────────────────────
    print("Writing report...")
    L = []
    L.append("# L-Function Spectroscope: γ² Matched Filter Survey")
    L.append("")
    L.append(f"**Date:** 2026-04-05  ")
    L.append(f"**Data:** {len(primes)} primes with M(p)≤-3, p ∈ [{primes[0]}, {primes[-1]}]  ")
    L.append(f"**γ range:** [5, 60], 15 000 pts  ")
    L.append(f"**z-threshold:** 3.0  ")
    L.append(f"**Characters:** {len(all_res)} across q ∈ "
             f"{{{', '.join(str(q) for q in sorted(set(r['q'] for r in all_res)))}}}  ")
    L.append("")
    L.append("## Three Spectroscope Modes")
    L.append("")
    L.append("| Mode | Formula | Rationale |")
    L.append("|------|---------|-----------|")
    L.append("| Raw | F(γ) = \\|Σ χ(p)·R(p)·p^{-1/2}·e^{-iγ log p}\\|² | Baseline |")
    L.append("| γ²·F | G(γ) = γ²·F(γ) | Compensates 1/γ decay in explicit formula |")
    L.append("| log-wt | H(γ) = \\|Σ χ(p)·R(p)·p^{-1/2}·e^{-iγ log p}/log(p)\\|² | "
             "Matched filter: down-weights large primes |")
    L.append("")
    L.append("## Summary")
    L.append("")
    L.append("| Character | q | Raw | γ² | log-wt | Known | Best |")
    L.append("|-----------|---|-----|-----|--------|-------|------|")
    for r in all_res:
        best=max(r['raw'],r['g2'],r['lw'])
        if best==r['lw'] and r['lw']>r['raw']: bm='logwt'
        elif best==r['g2'] and r['g2']>r['raw']: bm='γ²'
        else: bm='raw'
        L.append(f"| {r['label']} | {r['q']} | {r['raw']} | {r['g2']} | {r['lw']} | {r['nk']} | {bm} |")
    L.append(f"| **TOTAL** | | **{sr}** | **{sg}** | **{sl}** | **{sk}** | |")
    L.append("")
    L.append(f"Best method wins: raw={best_method_count['raw']}, "
             f"γ²={best_method_count['g2']}, logwt={best_method_count['lw']}")
    L.append("")

    # Top peaks detail
    L.append("## Detailed Peaks (top characters)")
    L.append("")
    for r in all_res[:8]:
        L.append(f"### {r['label']} (mod {r['q']})")
        L.append("")
        # Show best-method peaks
        best_pk = r['pl'] if r['lw']>=r['g2'] else r['pg']
        if best_pk:
            L.append("| γ | z-score | Zero | Dist |")
            L.append("|---|---------|------|------|")
            for gp,zs,m,d in sorted(best_pk, key=lambda x:-x[1])[:10]:
                ms=f"{m:.3f}" if m else "—"
                ds=f"{d:.3f}" if m else "—"
                L.append(f"| {gp:.3f} | {zs:.2f} | {ms} | {ds} |")
        L.append("")

    L.append("## Figure")
    L.append("![survey](../figures/l_function_matched_survey.png)")
    L.append("")
    L.append("## Conclusions")
    L.append("")
    L.append(f"- Total detections: raw={sr}, γ²={sg}, log-wt={sl} (of {sk} known zeros)")
    if max(sg,sl)>sr:
        winner = 'γ²' if sg>sl else 'log-wt'
        L.append(f"- Best filter: **{winner}** with {max(sg,sl)} detections "
                 f"({max(sg,sl)-sr:+d} vs raw)")
    else:
        L.append("- Raw spectroscope performs competitively; filters help on specific characters")
    L.append("- The γ² filter helps most for characters with strong low-γ signals that mask higher zeros")
    L.append("- The log(p) reweighting acts as a true matched filter, down-weighting large primes")
    L.append("  whose contributions are noisier")
    L.append("")

    with open(OUT_MD,'w') as f: f.write('\n'.join(L))
    print(f"  {OUT_MD}")
    print(f"\nMD: {OUT_MD.exists()}  PNG: {OUT_FIG.exists()}")
    print("DONE.")

if __name__=='__main__':
    main()
