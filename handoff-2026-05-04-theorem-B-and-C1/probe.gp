default(realprecision, 30);
default(parisize, "2G");
{
  for(k = 12, 26, if(k%2==0,
    mf = mfinit([1, k], 1);
    b = mfeigenbasis(mf);
    print("weight ", k, " level 1: nb_newforms = ", #b);
  ));
}
{
  print();
  print("--- level 2, weights 12-24 ---");
  for(k = 12, 24, if(k%2==0,
    mf = mfinit([2, k], 1);
    b = mfeigenbasis(mf);
    print("weight ", k, " level 2: nb_newforms = ", #b);
  ));
}
{
  print();
  print("--- weight 24 various small levels ---");
  for(N = 1, 11,
    mf = mfinit([N, 24], 1);
    b = mfeigenbasis(mf);
    print("weight 24 level ", N, ": nb_newforms = ", #b);
  );
}
