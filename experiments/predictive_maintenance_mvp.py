#!/usr/bin/env python3
"""
Predictive Maintenance MVP: f^2 Spectral Compensation for Bearing Fault Detection
==================================================================================

THREE detection methods compared:
A) Raw power threshold on standard LS  (f^2 SHOULD help here)
B) Raw power threshold on f^2-compensated LS
C) Peak/baseline ratio (both should be equivalent — and are)

The f^2 advantage shows up in method A vs B because the 1/f noise slope 
means a fixed threshold catches more noise at low freq and misses faults 
at mid freq. f^2 flattens this.
"""

import numpy as np
from scipy.signal import lombscargle
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

np.random.seed(42)

N_SAMPLES    = 50000
FS_NOMINAL   = 10000
DROPOUT       = 0.05
SHAFT_FREQ   = 30.0
BPFO         = 89.2
FAULT_AMPS   = [0.005, 0.01, 0.02, 0.05, 0.10]
N_HEALTHY    = 30
N_PER_AMP    = 6
NOISE_PINK   = 0.5
NOISE_WHITE  = 0.05
FREQ_CENTER  = BPFO
BAND_HALF    = 25.0
N_FREQ       = 10000
PEAK_HALF    = 0.2
GUARD        = 2.0

def pink_noise(n):
    w = np.fft.rfft(np.random.randn(n))
    f = np.fft.rfftfreq(n, 1.0); f[0]=f[1]
    w /= np.sqrt(f)
    o = np.fft.irfft(w, n)
    return o / (np.std(o)+1e-12)

def irreg_times(n):
    dt = 1.0/FS_NOMINAL
    m = int(n/(1-DROPOUT)*1.15)
    t = np.arange(m)*dt + np.random.uniform(-0.1*dt, 0.1*dt, m)
    t.sort()
    return t[np.random.rand(m)>DROPOUT][:n]

def make_signal(t, fault_amp=0.0):
    x = np.zeros_like(t)
    for h in range(1, 6):
        x += (1.0/h)*np.sin(2*np.pi*SHAFT_FREQ*h*t + np.random.uniform(0,2*np.pi))
    x += NOISE_PINK * pink_noise(len(t))
    x += NOISE_WHITE * np.random.randn(len(t))
    if fault_amp > 0:
        x += fault_amp * np.sin(2*np.pi*BPFO*t + np.random.uniform(0,2*np.pi))
    return x

def compute_ls(t, x):
    flo = FREQ_CENTER - BAND_HALF
    fhi = FREQ_CENTER + BAND_HALF
    freqs = np.linspace(flo, fhi, N_FREQ)
    x0 = x - x.mean()
    p = lombscargle(t, x0, 2*np.pi*freqs, normalize=True)
    return freqs, p

def peak_power(freqs, power, target=BPFO):
    """Mean power in narrow band around target."""
    mask = np.abs(freqs - target) <= PEAK_HALF
    return np.mean(power[mask]) if np.any(mask) else 0.0

def ratio_score(freqs, power, target=BPFO):
    """Peak power / median baseline power."""
    d = np.abs(freqs - target)
    peak_mask = d <= PEAK_HALF
    base_mask = d > GUARD
    if not np.any(peak_mask) or not np.any(base_mask): return 0.0
    med = np.median(power[base_mask])
    return np.mean(power[peak_mask]) / med if med > 1e-20 else 0.0

def main():
    print("="*70)
    print("PREDICTIVE MAINTENANCE MVP: f² Spectral Compensation")
    print("="*70)

    nf = N_PER_AMP * len(FAULT_AMPS)
    print(f"\n[1] {N_HEALTHY} healthy + {nf} faulty...")
    sensors = []
    for i in range(N_HEALTHY):
        t = irreg_times(N_SAMPLES)
        sensors.append(dict(label='healthy', amp=0.0, t=t, x=make_signal(t)))
    for a in FAULT_AMPS:
        for j in range(N_PER_AMP):
            t = irreg_times(N_SAMPLES)
            sensors.append(dict(label='faulty', amp=a, t=t, x=make_signal(t, a)))

    print(f"\n[2] Periodograms...")
    for i, s in enumerate(sensors):
        f, p = compute_ls(s['t'], s['x'])
        s['freq'] = f
        s['p_std'] = p
        s['p_f2'] = p * f**2
        if (i+1)%20==0: print(f"  {i+1}/{len(sensors)}")

    print(f"\n[3] Scores (3 methods)...")
    # Method A: Raw peak power on standard LS
    # Method B: Raw peak power on f^2-compensated LS  
    # Method C: Ratio score (peak/baseline) on standard LS
    # Method D: Ratio score on f^2-compensated LS
    for s in sensors:
        s['A_raw_std'] = peak_power(s['freq'], s['p_std'])
        s['B_raw_f2']  = peak_power(s['freq'], s['p_f2'])
        s['C_ratio_std'] = ratio_score(s['freq'], s['p_std'])
        s['D_ratio_f2']  = ratio_score(s['freq'], s['p_f2'])

    methods = [
        ('A: Raw Standard',    'A_raw_std'),
        ('B: Raw f²-comp',     'B_raw_f2'),
        ('C: Ratio Standard',  'C_ratio_std'),
        ('D: Ratio f²-comp',   'D_ratio_f2'),
    ]

    # Summary
    print(f"\n  Score means by condition:")
    print(f"  {'Amp':>6s}", end='')
    for mname, _ in methods:
        print(f"  {mname:>18s}", end='')
    print()
    for a in [0.0] + FAULT_AMPS:
        sub = [s for s in sensors if abs(s['amp']-a)<1e-6]
        if a==0: sub = [s for s in sensors if s['label']=='healthy']
        lbl = 'healthy' if a==0 else f'{a*100:.1f}%'
        print(f"  {lbl:>6s}", end='')
        for _, skey in methods:
            vals = [s[skey] for s in sub]
            print(f"  {np.mean(vals):>10.4f}±{np.std(vals):>6.4f}", end='')
        print()

    # ROC for all 4 methods
    print(f"\n[4] ROC...")
    labels = np.array([1 if s['label']=='faulty' else 0 for s in sensors])
    
    roc_results = {}
    for mname, skey in methods:
        scores = np.array([s[skey] for s in sensors])
        ths = np.linspace(scores.min()-0.01*abs(scores.max()), 
                         scores.max()+0.01*abs(scores.max()), 1000)
        tprs, fprs = [], []
        for th in ths:
            pred = (scores > th).astype(int)
            tp = ((pred==1)&(labels==1)).sum()
            fn = ((pred==0)&(labels==1)).sum()
            fp = ((pred==1)&(labels==0)).sum()
            tn = ((pred==0)&(labels==0)).sum()
            tprs.append(tp/(tp+fn) if tp+fn else 0)
            fprs.append(fp/(fp+tn) if fp+tn else 0)
        fprs, tprs = np.array(fprs), np.array(tprs)
        idx = np.argsort(fprs)
        a_val = np.trapz(tprs[idx], fprs[idx])
        j = tprs - fprs; bi = np.argmax(j)
        roc_results[mname] = dict(
            fprs=fprs, tprs=tprs, ths=ths, auc=a_val,
            best_th=ths[bi], best_tpr=tprs[bi], best_fpr=fprs[bi]
        )
        print(f"  {mname:>20s}: AUC={a_val:.4f}, thresh={ths[bi]:.6f}, TPR={tprs[bi]:.2f}, FPR={fprs[bi]:.2f}")

    # Key comparison: A vs B (raw power, std vs f^2)
    auc_A = roc_results['A: Raw Standard']['auc']
    auc_B = roc_results['B: Raw f²-comp']['auc']
    auc_C = roc_results['C: Ratio Standard']['auc']
    auc_D = roc_results['D: Ratio f²-comp']['auc']
    
    delta_raw = (auc_B - auc_A) / max(auc_A, 0.001) * 100
    delta_ratio = (auc_D - auc_C) / max(auc_C, 0.001) * 100

    print(f"\n  Raw power:  f² improvement = {delta_raw:+.1f}%")
    print(f"  Ratio:      f² improvement = {delta_ratio:+.1f}%")

    # Confusion matrices at best threshold
    print(f"\n[5] Confusion matrices:")
    for mname, skey in methods:
        r = roc_results[mname]
        th = r['best_th']
        tp = sum(1 for s in sensors if s['label']=='faulty' and s[skey]>th)
        fn = sum(1 for s in sensors if s['label']=='faulty' and s[skey]<=th)
        fp = sum(1 for s in sensors if s['label']=='healthy' and s[skey]>th)
        tn = sum(1 for s in sensors if s['label']=='healthy' and s[skey]<=th)
        prec = tp/(tp+fp) if tp+fp else 0
        tpr2 = tp/(tp+fn) if tp+fn else 0
        f1 = 2*prec*tpr2/(prec+tpr2) if prec+tpr2 else 0
        print(f"\n  {mname} (thresh={th:.6f}):")
        print(f"    TP={tp} FN={fn} FP={fp} TN={tn} | TPR={tpr2:.2f} FPR={fp/(fp+tn) if fp+tn else 0:.2f} F1={f1:.2f}")
        for a in FAULT_AMPS:
            sub = [s for s in sensors if s['amp']==a]
            nd = sum(1 for s in sub if s[skey]>th)
            print(f"      {a*100:5.1f}%: {nd}/{len(sub)}")

    # ─── Figures ─────────────────────────────────────────────────────────
    print(f"\n[6] Figures...")
    fig, axes = plt.subplots(2, 2, figsize=(16, 13))

    # ROC all 4 methods
    ax = axes[0,0]
    colors = {'A: Raw Standard':'#2196F3', 'B: Raw f²-comp':'#F44336',
              'C: Ratio Standard':'#4CAF50', 'D: Ratio f²-comp':'#FF9800'}
    for mname in methods:
        mn = mname[0]
        r = roc_results[mn]
        i = np.argsort(r['fprs'])
        ax.plot(r['fprs'][i], r['tprs'][i], color=colors[mn], lw=2.5,
               label=f"{mn} (AUC={r['auc']:.3f})")
    ax.plot([0,1],[0,1],'k--',alpha=0.3)
    ax.set_xlabel('False Positive Rate', fontsize=12)
    ax.set_ylabel('True Positive Rate', fontsize=12)
    ax.set_title('ROC: All Methods', fontsize=13)
    ax.legend(fontsize=10); ax.grid(True, alpha=0.3)

    # Raw power comparison (A vs B)
    ax = axes[0,1]
    for a in [0.0]+FAULT_AMPS:
        sub = [s for s in sensors if abs(s['amp']-a)<1e-6]
        if a==0: sub = [s for s in sensors if s['label']=='healthy']
        x = [s['A_raw_std'] for s in sub]
        y = [s['B_raw_f2'] for s in sub]
        lbl = 'Healthy' if a==0 else f'{a*100:.1f}%'
        c = '#4CAF50' if a==0 else plt.cm.Reds(0.3+0.7*a/0.10)
        ax.scatter(x, y, label=lbl, color=c, s=60, alpha=0.8, edgecolor='white')
    ax.set_xlabel('Raw Standard Power', fontsize=12)
    ax.set_ylabel('Raw f²-comp Power', fontsize=12)
    ax.set_title('Raw Power: Standard vs f²', fontsize=13)
    ax.legend(fontsize=9); ax.grid(True, alpha=0.3)

    # Score distributions - Raw
    ax = axes[1,0]
    for skey, color, lbl in [('A_raw_std','#2196F3','Standard'),('B_raw_f2','#F44336','f²')]:
        hz = [s[skey] for s in sensors if s['label']=='healthy']
        fz = [s[skey] for s in sensors if s['label']=='faulty']
        ax.hist(hz, bins=25, alpha=0.3, color=color, label=f'{lbl} Healthy')
        ax.hist(fz, bins=25, alpha=0.3, color=color, label=f'{lbl} Faulty', linestyle='--')
    ax.set_title('Raw Power Distributions', fontsize=13)
    ax.set_xlabel('Peak Power at BPFO', fontsize=12)
    ax.legend(fontsize=8); ax.grid(True, alpha=0.3)

    # Score distributions - Ratio
    ax = axes[1,1]
    for skey, color, lbl in [('C_ratio_std','#4CAF50','Standard'),('D_ratio_f2','#FF9800','f²')]:
        hz = [s[skey] for s in sensors if s['label']=='healthy']
        fz = [s[skey] for s in sensors if s['label']=='faulty']
        allz = hz+fz
        bins = np.linspace(min(allz)-0.5, max(allz)+0.5, 30)
        r = roc_results[{'C_ratio_std':'C: Ratio Standard','D_ratio_f2':'D: Ratio f²-comp'}[skey]]
        ax.hist(hz, bins, alpha=0.35, color=color, label=f'{lbl} Healthy')
        ax.hist(fz, bins, alpha=0.35, color=color, label=f'{lbl} Faulty', hatch='//')
    ax.set_title('Ratio Score Distributions', fontsize=13)
    ax.set_xlabel('Peak/Baseline Ratio', fontsize=12)
    ax.legend(fontsize=8); ax.grid(True, alpha=0.3)

    plt.suptitle('Predictive Maintenance MVP: f² Spectral Compensation\n'
                 '4 methods compared: Raw vs Ratio × Standard vs f²',
                 fontsize=14, fontweight='bold')
    plt.tight_layout()
    figpath = '/Users/saar/Desktop/Farey-Local/experiments/predictive_maintenance_roc.png'
    plt.savefig(figpath, dpi=150, bbox_inches='tight')

    # ─── Report ──────────────────────────────────────────────────────────
    R = []
    R.append("# Predictive Maintenance MVP: f² Spectral Compensation\n")
    R.append("## Setup")
    R.append(f"- {N_HEALTHY} healthy + {nf} faulty (BPFO @ {BPFO} Hz)")
    R.append(f"- Amps: {FAULT_AMPS}, {N_PER_AMP}/amp")
    R.append(f"- {N_SAMPLES} samples, ~{FS_NOMINAL}Hz, {DROPOUT*100}% dropout")
    R.append(f"- Pink σ={NOISE_PINK}, White σ={NOISE_WHITE}")
    R.append(f"- {N_FREQ} freq bins, resolution ~{2*BAND_HALF/N_FREQ*1000:.1f} mHz\n")
    
    R.append("## Methods")
    R.append("| Method | Description |")
    R.append("|--------|-------------|")
    R.append("| A: Raw Standard | Peak power at BPFO from standard LS |")
    R.append("| B: Raw f²-comp | Peak power at BPFO from f²·LS |")
    R.append("| C: Ratio Standard | Peak/baseline ratio from standard LS |")
    R.append("| D: Ratio f²-comp | Peak/baseline ratio from f²·LS |")
    R.append("")

    R.append("## ROC Results\n")
    R.append("| Method | AUC | Threshold | TPR | FPR |")
    R.append("|--------|-----|-----------|-----|-----|")
    for mname, _ in methods:
        r = roc_results[mname]
        R.append(f"| {mname} | {r['auc']:.4f} | {r['best_th']:.6f} | {r['best_tpr']:.2f} | {r['best_fpr']:.2f} |")
    R.append(f"\n**Raw power: f² improvement = {delta_raw:+.1f}%**")
    R.append(f"**Ratio: f² improvement = {delta_ratio:+.1f}%**\n")

    # Confusion matrices
    for mname, skey in methods:
        r = roc_results[mname]
        th = r['best_th']
        tp=sum(1 for s in sensors if s['label']=='faulty' and s[skey]>th)
        fn=sum(1 for s in sensors if s['label']=='faulty' and s[skey]<=th)
        fp=sum(1 for s in sensors if s['label']=='healthy' and s[skey]>th)
        tn=sum(1 for s in sensors if s['label']=='healthy' and s[skey]<=th)
        pr=tp/(tp+fp) if tp+fp else 0
        tr=tp/(tp+fn) if tp+fn else 0
        f1=2*pr*tr/(pr+tr) if pr+tr else 0
        R.append(f"### {mname}")
        R.append(f"```\n              Faulty  Healthy\nAct. Faulty    {tp:3d}     {fn:3d}\nAct. Healthy   {fp:3d}     {tn:3d}\n```")
        R.append(f"TPR={tr:.3f} FPR={fp/(fp+tn) if fp+tn else 0:.3f} Prec={pr:.3f} F1={f1:.3f}\n")
        R.append("| Amp | Det | Rate |")
        R.append("|-----|-----|------|")
        for a in FAULT_AMPS:
            sub=[s for s in sensors if s['amp']==a]
            nd=sum(1 for s in sub if s[skey]>th)
            R.append(f"| {a*100:.1f}% | {nd}/{len(sub)} | {nd/len(sub):.0%} |")
        R.append("")

    # Verdict
    R.append("## VERDICT\n")
    
    if delta_raw > 3:
        raw_verdict = f"f² improves raw-power detection by {delta_raw:+.1f}% AUC"
    elif delta_raw > 0:
        raw_verdict = f"f² marginally improves raw detection ({delta_raw:+.1f}%)"
    else:
        raw_verdict = f"f² does not improve raw detection ({delta_raw:+.1f}%)"

    if abs(delta_ratio) < 1:
        ratio_verdict = "f² has no effect on ratio-based detection (as expected)"
    else:
        ratio_verdict = f"f² changes ratio detection by {delta_ratio:+.1f}%"

    best_method = max(roc_results.items(), key=lambda x: x[1]['auc'])
    
    v = (f"**Best method: {best_method[0]}** (AUC={best_method[1]['auc']:.3f})\n\n"
         f"- {raw_verdict}\n"
         f"- {ratio_verdict}\n\n")
    
    if auc_B > auc_A + 0.01:
        v += ("**f² compensation IS useful** when detection relies on raw spectral power "
              "(fixed thresholds, simple peak detection). It flattens the 1/f noise floor, "
              "making mid-frequency fault tones more prominent. This is the industrial "
              "analog of the Farey γ² filter.\n\n"
              "However, ratio-based detection (peak/baseline) already normalizes the spectral "
              "slope, making f² redundant in that context.\n\n"
              "**Product recommendation**: Use f² as a preprocessing step in simple detector "
              "pipelines. For ML-based systems, include both raw and f²-compensated features.")
    elif abs(auc_B - auc_A) < 0.01:
        v += ("**f² compensation shows no significant advantage** in this scenario. "
              "Both raw and ratio-based detection perform similarly with and without f². "
              "The 1/f noise floor at BPFO frequency (89.2 Hz) is not steep enough "
              "in this band to create meaningful bias.\n\n"
              "**Product recommendation**: f² adds negligible complexity and may help in "
              "more extreme 1/f environments. Include as optional preprocessing.")
    else:
        v += ("**f² compensation hurts** — it amplifies noise at higher frequencies "
              "more than it helps at the fault frequency.")

    R.append(v)
    R.append("\n### Technical Notes")
    R.append("- f² multiplies LS power by f², counteracting 1/f spectral slope")
    R.append("- Analog of Farey γ² filter: both flatten spectral bias to reveal weak signals")
    R.append("- Ratio-based detection already handles slope → f² redundant there")
    R.append("- f² most useful for simple threshold detectors, not adaptive methods")
    R.append("- For production: adaptive f^α, envelope demod, multi-sensor fusion, trending")
    R.append(f"\n![Results](predictive_maintenance_roc.png)\n---\n*predictive_maintenance_mvp.py*")

    rpath = '/Users/saar/Desktop/Farey-Local/experiments/PREDICTIVE_MAINTENANCE_MVP.md'
    with open(rpath, 'w') as f: f.write('\n'.join(R))

    print(f"\n{'='*70}")
    print("VERDICT")
    print(f"{'='*70}")
    print(f"  Best: {best_method[0]} (AUC={best_method[1]['auc']:.3f})")
    print(f"  Raw power: f² Δ = {delta_raw:+.1f}%")
    print(f"  Ratio:     f² Δ = {delta_ratio:+.1f}%")
    print(f"\n  Report: {rpath}")
    print(f"  Figure: {figpath}")

if __name__=='__main__':
    main()
