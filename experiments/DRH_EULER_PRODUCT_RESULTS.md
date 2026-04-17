mp.dps = 30
Computing primes up to 500...
Computing zeta zeros up to 500.0 for generic-point rejection...
Generating 1000 generic points in [0, 500.0] with rejection tolerance 0.1...
Analyzing P = 10...
Analyzing P = 30...
Analyzing P = 100...
Analyzing P = 500...

DRH / partial Euler product summary
Zero sample: first 100 zeta zeros (gamma_j = mpmath.zetazero(j).imag)
Generic sample: 1000 uniform points in [0, 500.0]
Generic points are rejected if they fall within 0.1 of any zeta zero with gamma <= 500.0.

    P #primes    mean|E|_zeros  mean|E|_generic     max|E|_zeros   max|E|_generic    amp ratio  mean|c_P|_zeros  mean|E*c_P-1|_zeros
------------------------------------------------------------------------------------------------------------------------------------
   10       4     0.6543494454      1.508268533      1.631722379      9.084357302 0.4338414751      1.809040912         0.2949795449
   30      10     0.4462471321      1.662418371     0.9624274287      11.89476101 0.2684325076       2.26639068         0.3082679292
  100      25     0.3165983098      1.757212843      0.709072857      9.532126581 0.1801707238      2.806045032         0.3103997813
  500      95     0.2338959105      1.772337105      0.531141973      10.41932463 0.1319703288      3.510870198         0.3093612925

Interpretation:
- Amplification ratio > 1 means |E_P| is larger at zeros than at generic points.
- If the ratio grows with P, that is consistent with the DRH-style pole effect.
- Mean |E_P * c_P - 1| near zero indicates the finite Möbius truncation is
  behaving like an approximate inverse to the partial Euler product.
