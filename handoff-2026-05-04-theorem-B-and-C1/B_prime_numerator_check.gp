/* Check at multiple squarefree levels with multiple newforms.
   Track: LHS = harmonic Petersson <L(0.55,f) L(0.47,f)>_F vs RHS = M_2 prediction. */

a = 0.05;
b = -0.03;

zN(s, N) = zeta(s)*(1 - N^(-s));
gam(al) = (2*Pi)^(2*al) * gamma(1.5-al)/gamma(1.5+al);

run_check(N) = {
  local(mfdat, nfs, total_w, weighted_sum, ll_orbit, weight_orbit,
        sym, pet_mat, Lvec, d, lhs_val, rhs_val, term1, term2);
  print("");
  print("--- N=", N, " ---");
  mfdat = mfinit([N,2,1], 0);
  nfs = mfeigenbasis(mfdat);
  print("# Galois orbits: ", #nfs);
  total_w = 0.0;
  weighted_sum = 0.0;
  for(i=1, #nfs,
    sym = mfsymbol(mfdat, nfs[i]);
    pet_mat = mfpetersson(sym);
    Lvec = lfunmf(mfdat, nfs[i]);
    d = #Lvec;
    \\ For each conjugate embedding, treat as separate newform
    for(j=1, d,
      petj = real(pet_mat[j,j]);
      wj = 1.0/(4*Pi*petj);
      llj = real(lfun(Lvec[j], 0.5+a)*lfun(Lvec[j], 0.5+b));
      total_w = total_w + wj;
      weighted_sum = weighted_sum + wj*llj;
    );
  );
  lhs_val = weighted_sum / total_w;
  term1 = zN(1+a+b, N)/zN(2+2*a+2*b, N);
  term2 = N^(-a-b) * gam(a)*gam(b) * zN(1-a-b, N)/zN(2-2*a-2*b, N);
  rhs_val = real(term1 + term2);
  print("LHS = ", lhs_val);
  print("RHS = ", rhs_val, "  (id=", real(term1), ", swap=", real(term2), ")");
  print("ratio LHS/RHS = ", lhs_val/rhs_val);
  print("rel err = ", abs(lhs_val - rhs_val)/abs(lhs_val));
  return([N, lhs_val, rhs_val]);
};

\\ Squarefree primes / squarefree composites
run_check(23);
run_check(37);
run_check(53);
run_check(67);
run_check(79);
run_check(89);
run_check(97);
run_check(127);
run_check(389);

quit;
