default(realprecision, 30);
mf = mfinit([37, 24], 1);
basis = mfeigenbasis(mf);
print("nb newforms: ", #basis);
print("type basis[1]: ", type(basis[1]));
print("first coefs F1: ", mfcoefs(basis[1], 6));
if (#basis >= 2,
  print("type basis[2]: ", type(basis[2]));
  print("first coefs F2: ", mfcoefs(basis[2], 6));
);
