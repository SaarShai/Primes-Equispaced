/Users/saar/Desktop/Farey-Local/experiments/spectroscope_deep_analysis.py:58: RuntimeWarning: divide by zero encountered in matmul
  re = np.cos(phases) @ amp
/Users/saar/Desktop/Farey-Local/experiments/spectroscope_deep_analysis.py:58: RuntimeWarning: overflow encountered in matmul
  re = np.cos(phases) @ amp
/Users/saar/Desktop/Farey-Local/experiments/spectroscope_deep_analysis.py:58: RuntimeWarning: invalid value encountered in matmul
  re = np.cos(phases) @ amp
/Users/saar/Desktop/Farey-Local/experiments/spectroscope_deep_analysis.py:59: RuntimeWarning: divide by zero encountered in matmul
  im = np.sin(phases) @ amp
/Users/saar/Desktop/Farey-Local/experiments/spectroscope_deep_analysis.py:59: RuntimeWarning: overflow encountered in matmul
  im = np.sin(phases) @ amp
/Users/saar/Desktop/Farey-Local/experiments/spectroscope_deep_analysis.py:59: RuntimeWarning: invalid value encountered in matmul
  im = np.sin(phases) @ amp
/Users/saar/Desktop/Farey-Local/experiments/spectroscope_deep_analysis.py:176: RuntimeWarning: divide by zero encountered in matmul
  S[s:e] = (np.cos(phases) - 1j * np.sin(phases)) @ amp
/Users/saar/Desktop/Farey-Local/experiments/spectroscope_deep_analysis.py:176: RuntimeWarning: overflow encountered in matmul
  S[s:e] = (np.cos(phases) - 1j * np.sin(phases)) @ amp
/Users/saar/Desktop/Farey-Local/experiments/spectroscope_deep_analysis.py:176: RuntimeWarning: invalid value encountered in matmul
  S[s:e] = (np.cos(phases) - 1j * np.sin(phases)) @ amp
/Users/saar/Desktop/Farey-Local/experiments/spectroscope_deep_analysis.py:221: RuntimeWarning: divide by zero encountered in matmul
  beam[s:e] = (np.cos(phases) - 1j * np.sin(phases)) @ (amp**2)
/Users/saar/Desktop/Farey-Local/experiments/spectroscope_deep_analysis.py:221: RuntimeWarning: overflow encountered in matmul
  beam[s:e] = (np.cos(phases) - 1j * np.sin(phases)) @ (amp**2)
/Users/saar/Desktop/Farey-Local/experiments/spectroscope_deep_analysis.py:221: RuntimeWarning: invalid value encountered in matmul
  beam[s:e] = (np.cos(phases) - 1j * np.sin(phases)) @ (amp**2)
======================================================================
PART 1: WHY WRONG-SIGN PRIMES DETECT GAMMA_1
======================================================================

Prime counts: negative M(p)=19451, positive=21704, zero=383
  All primes          : gamma_1 peak=14.024 err=0.781% z=11.6 | gamma_2 peak=20.908 err=0.543% z=3.3
  M(p)<0 only         : gamma_1 peak=14.021 err=0.803% z=12.6 | gamma_2 peak=20.921 err=0.482% z=3.7
  M(p)>0 only         : gamma_1 peak=14.108 err=0.192% z=9.4 | gamma_2 peak=20.930 err=0.437% z=2.4
  |M(p)|/sqrt(p)      : gamma_1 peak=14.108 err=0.192% z=1.6 | gamma_2 peak=21.055 err=0.157% z=1.1

  Random 50% subsets (10 trials), M/sqrt(p) weight:
    gamma_1 z-scores: ['10.3', '11.5', '11.7', '12.1', '12.2', '10.7', '12.3', '11.5', '11.7', '12.1']
    mean=11.6, min=10.3, max=12.3
  p≡1 mod 4            (N=20731): gamma_1 z=11.8
  p≡3 mod 4            (N=20806): gamma_1 z=11.5

  CONCLUSION: gamma_1 detection is UNIVERSAL — it works for ANY
  subset of primes weighted by M(p)/sqrt(p), because the explicit
  formula M(x) ~ sum_rho x^rho/(rho*zeta'(rho)) applies to ALL primes.

======================================================================
PART 2: COMPENSATING FOR HIGHER-ZERO DECAY
        (CLEAN algorithm: subtract known zeros)
======================================================================

  Complex sum at gamma_1: -0.0345-11.6640j
  |S|^2 = 136.0500

  Iterative CLEAN (subtract detected zeros one at a time):
  Iter 1: peak=14.024, nearest gamma_1=14.135, err=0.78%, z=11.0
  Iter 2: peak=14.341, nearest gamma_1=14.135, err=1.46%, z=11.1
  Iter 3: peak=13.989, nearest gamma_1=14.135, err=1.03%, z=10.8
  Iter 4: peak=14.312, nearest gamma_1=14.135, err=1.26%, z=10.8
  Iter 5: peak=13.970, nearest gamma_1=14.135, err=1.17%, z=10.5
  Iter 6: peak=14.293, nearest gamma_1=14.135, err=1.12%, z=10.3
  Iter 7: peak=13.960, nearest gamma_1=14.135, err=1.23%, z=10.0
  Iter 8: peak=14.284, nearest gamma_1=14.135, err=1.05%, z=9.8
  Iter 9: peak=13.954, nearest gamma_1=14.135, err=1.28%, z=9.4
  Iter 10: peak=14.271, nearest gamma_1=14.135, err=0.96%, z=9.2

  CLEAN detected 10 zeros before z<1.0:
    Detected     True   Error%      z
      14.024   14.135     0.78   11.0
      14.341   14.135     1.46   11.1
      13.989   14.135     1.03   10.8
      14.312   14.135     1.26   10.8
      13.970   14.135     1.17   10.5
      14.293   14.135     1.12   10.3
      13.960   14.135     1.23   10.0
      14.284   14.135     1.05    9.8
      13.954   14.135     1.28    9.4
      14.271   14.135     0.96    9.2

  Without CLEAN: gamma_1 z=11.6, gamma_2 z=3.3, gamma_3 z=1.5
  With CLEAN: see above — does iterative subtraction reveal more zeros?

======================================================================
PART 3: WINDOWING / TAPERING to reduce sidelobes
======================================================================

  Hanning-windowed spectroscope:
  gamma_ 1 (14.135): Hanning z=11.2 vs original z=11.6 (0.96x)
  gamma_ 2 (21.022): Hanning z=2.7 vs original z=3.3 (0.83x)
  gamma_ 3 (25.011): Hanning z=1.0 vs original z=1.5 (0.69x)
  gamma_ 4 (30.425): Hanning z=1.0 vs original z=1.2 (0.84x)
  gamma_ 5 (32.935): Hanning z=0.6 vs original z=0.5 (1.05x)
  gamma_ 6 (37.586): Hanning z=0.2 vs original z=0.2 (1.05x)
  gamma_ 7 (40.919): Hanning z=0.3 vs original z=0.1 (2.33x)
  gamma_ 8 (43.327): Hanning z=0.1 vs original z=-0.1 (infx)
  gamma_ 9 (48.005): Hanning z=0.2 vs original z=0.1 (1.92x)
  gamma_10 (49.774): Hanning z=0.1 vs original z=0.2 (0.31x)

  Blackman-Harris windowed spectroscope:
  gamma_ 1 (14.135): BH z=10.1 vs original z=11.6 (0.87x)
  gamma_ 2 (21.022): BH z=2.3 vs original z=3.3 (0.71x)
  gamma_ 3 (25.011): BH z=0.9 vs original z=1.5 (0.59x)
  gamma_ 4 (30.425): BH z=0.8 vs original z=1.2 (0.67x)
  gamma_ 5 (32.935): BH z=0.4 vs original z=0.5 (0.84x)
  gamma_ 6 (37.586): BH z=0.1 vs original z=0.2 (0.45x)
  gamma_ 7 (40.919): BH z=0.2 vs original z=0.1 (1.20x)
  gamma_ 8 (43.327): BH z=-0.0 vs original z=-0.1 (infx)
  gamma_ 9 (48.005): BH z=0.1 vs original z=0.1 (0.69x)
  gamma_10 (49.774): BH z=-0.0 vs original z=0.2 (-0.09x)

Done!
