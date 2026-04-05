/Users/saar/Desktop/Farey-Local/experiments/mertens_all_primes_spectroscope.py:86: RuntimeWarning: divide by zero encountered in matmul
  re = np.cos(phases) @ amp
/Users/saar/Desktop/Farey-Local/experiments/mertens_all_primes_spectroscope.py:86: RuntimeWarning: overflow encountered in matmul
  re = np.cos(phases) @ amp
/Users/saar/Desktop/Farey-Local/experiments/mertens_all_primes_spectroscope.py:86: RuntimeWarning: invalid value encountered in matmul
  re = np.cos(phases) @ amp
/Users/saar/Desktop/Farey-Local/experiments/mertens_all_primes_spectroscope.py:87: RuntimeWarning: divide by zero encountered in matmul
  im = np.sin(phases) @ amp
/Users/saar/Desktop/Farey-Local/experiments/mertens_all_primes_spectroscope.py:87: RuntimeWarning: overflow encountered in matmul
  im = np.sin(phases) @ amp
/Users/saar/Desktop/Farey-Local/experiments/mertens_all_primes_spectroscope.py:87: RuntimeWarning: invalid value encountered in matmul
  im = np.sin(phases) @ amp
======================================================================
MERTENS SPECTROSCOPE: ALL PRIMES vs FILTERED
======================================================================

Step 1: Sieve Mobius function to 500000...
  Sieve done in 0.2s
  Total primes <= 500000: 41538
  M(p) range: [-256, 242]
  Primes with M(p)<=-3: 18697 (45.0%)

======================================================================
TEST A: M(p)/sqrt(p) on ALL primes (no filter)
======================================================================
  Computed in 4.7s

  M/sqrt(p), ALL 41538 primes (20 zeros analyzed):
      zero     peak     err%  z-score
    14.135   14.024    0.781     11.6
    21.022   20.908    0.543      3.3
    25.011   24.825    0.744      1.5
    30.425   30.278    0.483      1.2
    32.935   32.752    0.557      0.5
    37.586   37.501    0.228      0.2
    40.919   40.790    0.314      0.1
    43.327   43.808    1.110     -0.1
    48.005   47.971    0.071      0.1
    49.774   49.591    0.368      0.2
    52.970   52.826    0.273     -0.0
    56.446   56.282    0.291      0.1
    59.347   59.127    0.371      0.3
    60.832   61.277    0.733      0.1
    65.112   65.018    0.145      0.0
    67.080   66.954    0.187     -0.1
    69.546   69.371    0.253     -0.1
    72.067   71.828    0.332     -0.0
    75.705   75.544    0.213     -0.1
    77.145   77.691    0.708     -0.1
  Average error: 0.435%
  Average z-score: 0.93
  Zeros with z>2: 2/20

======================================================================
TEST B: M(p)/sqrt(p) on FILTERED primes (M<=-3 only)
======================================================================
  Computed in 2.2s

  M/sqrt(p), FILTERED 18697 primes (20 zeros analyzed):
      zero     peak     err%  z-score
    14.135   14.120    0.101     12.3
    21.022   20.969    0.254      2.9
    25.011   24.991    0.079      1.1
    30.425   30.233    0.631      1.4
    32.935   32.694    0.732      0.4
    37.586   38.784    3.186      0.1
    40.919   39.721    2.926     -0.1
    43.327   44.349    2.358     -0.0
    48.005   48.032    0.056      0.4
    49.774   49.386    0.780      0.2
    52.970   53.645    1.274     -0.1
    56.446   56.196    0.444     -0.2
    59.347   59.095    0.425      0.0
    60.832   62.029    1.969     -0.1
    65.112   64.967    0.223     -0.0
    67.080   66.884    0.292     -0.0
    69.546   69.403    0.207     -0.3
    72.067   73.220    1.600     -0.2
    75.705   76.785    1.427     -0.2
    77.145   78.289    1.484     -0.2
  Average error: 1.022%
  Average z-score: 0.86
  Zeros with z>2: 2/20

======================================================================
TEST C: Unit weight on ALL primes
======================================================================
  Computed in 4.6s

  Unit weight, ALL 41538 primes (20 zeros analyzed):
      zero     peak     err%  z-score
    14.135   14.264    0.917      2.8
    21.022   20.917    0.497      1.5
    25.011   25.318    1.226      0.4
    30.425   30.476    0.169      0.6
    32.935   32.960    0.074      0.8
    37.586   37.731    0.385      0.2
    40.919   41.062    0.351      0.3
    43.327   43.517    0.438      0.5
    48.005   47.677    0.684      0.2
    49.774   49.706    0.137      0.3
    52.970   53.044    0.138      0.0
    56.446   56.314    0.234      0.2
    59.347   59.236    0.187      0.3
    60.832   60.794    0.062      0.1
    65.112   64.935    0.272      0.1
    67.080   66.932    0.220     -0.1
    69.546   69.835    0.414     -0.2
    72.067   72.193    0.175      0.1
    75.705   75.473    0.306      0.3
    77.145   77.016    0.167     -0.0
  Average error: 0.353%
  Average z-score: 0.41
  Zeros with z>2: 1/20

======================================================================
TEST D: Unit weight on FILTERED primes
======================================================================
  Computed in 2.1s

  Unit weight, FILTERED 18697 primes (20 zeros analyzed):
      zero     peak     err%  z-score
    14.135   14.114    0.147     11.0
    21.022   20.975    0.223      1.9
    25.011   25.014    0.011      1.2
    30.425   30.252    0.568      0.4
    32.935   32.732    0.616     -0.0
    37.586   37.488    0.262      0.1
    40.919   40.918    0.001     -0.1
    43.327   42.598    1.682     -0.2
    48.005   48.823    1.703      0.1
    49.774   48.823    1.911      0.1
    52.970   53.024    0.102     -0.1
    56.446   57.104    1.166     -0.2
    59.347   60.429    1.824     -0.0
    60.832   61.882    1.727     -0.0
    65.112   65.015    0.149     -0.1
    67.080   68.167    1.621      0.1
    69.546   68.347    1.725      0.0
    72.067   71.883    0.256     -0.1
    75.705   74.552    1.523     -0.3
    77.145   78.149    1.301     -0.2
  Average error: 0.926%
  Average z-score: 0.68
  Zeros with z>2: 1/20

======================================================================
TEST E: M(p)/sqrt(p) on WRONG-SIGN primes (M(p) > 0)
======================================================================
  Primes with M(p)>0: 21704
  Computed in 2.4s

  M/sqrt(p), WRONG-SIGN 21704 primes (20 zeros analyzed):
      zero     peak     err%  z-score
    14.135   14.108    0.192      9.4
    21.022   20.930    0.437      2.4
    25.011   25.116    0.420      0.8
    30.425   30.377    0.157      0.2
    32.935   33.129    0.589      0.4
    37.586   38.784    3.186     -0.1
    40.919   41.053    0.327      0.3
    43.327   44.259    2.151      0.4
    48.005   46.938    2.224     -0.1
    49.774   49.603    0.342      0.1
    52.970   53.236    0.501     -0.3
    56.446   55.248    2.122      0.0
    59.347   58.385    1.622     -0.2
    60.832   60.951    0.196     -0.1
    65.112   63.914    1.840     -0.0
    67.080   68.279    1.788     -0.3
    69.546   69.252    0.423     -0.2
    72.067   73.249    1.640     -0.4
    75.705   75.624    0.107     -0.3
    77.145   77.544    0.517     -0.3
  Average error: 1.039%
  Average z-score: 0.59
  Zeros with z>2: 2/20

======================================================================
SUMMARY: Filter vs Weight comparison (first 5 zeros)
======================================================================

  First 5 zeros:
  Config                                Avg err%    Avg z
  M/sqrt(p), ALL primes                    0.622     3.61
  M/sqrt(p), filtered M<=-3                0.359     3.60
  Unit, ALL primes                         0.577     1.20
  Unit, filtered M<=-3                     0.313     2.89

  First 10 zeros:
  Config                                Avg err%    Avg z
  M/sqrt(p), ALL primes                    0.520     1.87
  M/sqrt(p), filtered M<=-3                1.110     1.86
  Unit, ALL primes                         0.488     0.75
  Unit, filtered M<=-3                     0.712     1.45

  All 20 zeros:
  Config                                Avg err%    Avg z
  M/sqrt(p), ALL primes                    0.435     0.93
  M/sqrt(p), filtered M<=-3                1.022     0.86
  Unit, ALL primes                         0.353     0.41
  Unit, filtered M<=-3                     0.926     0.68

Done!
