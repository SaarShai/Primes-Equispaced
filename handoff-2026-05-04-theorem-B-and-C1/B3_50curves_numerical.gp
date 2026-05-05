\\ Bigger numerical: 50+ EC curves at varying N for level-aspect cage testing
\\ Test: as N → ∞, does u_f → 2/(3π) ≈ 0.212 or to lower cage edge c⁻ ≈ 0.132?

default(parisizemax, 16000000000);
default(parisize, 2000000000);
default(realprecision, 30);

\\ Cremona-table EC newforms across N range
\\ Format: (label, conductor)
curves = [
  ["11a1",11], ["14a1",14], ["15a1",15], ["17a1",17], ["19a1",19],
  ["20a1",20], ["21a1",21], ["24a1",24], ["26a1",26], ["27a1",27],
  ["32a1",32], ["33a1",33], ["35a1",35], ["36a1",36], ["37a1",37],
  ["38a1",38], ["39a1",39], ["40a1",40], ["43a1",43], ["44a1",44],
  ["45a1",45], ["46a1",46], ["48a1",48], ["50a1",50], ["50b1",50],
  ["51a1",51], ["53a1",53], ["54a1",54], ["55a1",55], ["56a1",56],
  ["57a1",57], ["58a1",58], ["100a1",100], ["106c1",106], ["121a1",121],
  ["121b1",121], ["121c1",121], ["121d1",121], ["200a1",200], ["221a1",221],
  ["240a1",240], ["258a1",258], ["294a1",294], ["389a1",389], ["432a1",432],
  ["496b1",496], ["510a1",510], ["681a1",681], ["1024a1",1024], ["1225a1",1225],
  ["2048a1",2048], ["5005b1",5005]
];

print("# 50+ curve numerical: u_f at first 100 zeros");
print("# Target: 2/(3π) ≈ 0.212; Lower cage edge c⁻ ≈ 0.132; Upper cage 0.770");
print("");
print("curve,N,T_max,n_zeros,U_f,Y,c_f,u_f");

for(idx=1, #curves,
  cn = curves[idx][1]; N_cond = curves[idx][2];
  E_check = ellinit(cn, 0);
  if(type(E_check) == "t_INT" && E_check == 0,
    printf("# SKIP %s: ellinit failed\n", cn),
    E = ellinit(cn);
    L = lfuncreate(E);
    \\ Compute first 100 zeros
    T_max = 100.0;
    zs = lfunzeros(L, T_max);
    n_zeros = length(zs);
    U = 0.0;
    for(j=1, n_zeros, U = U + abs(lfun(L, 1.0 + I*zs[j], 1))^2);
    \\ c_f via lfunsympow
    L_sym2 = lfunsympow(E, 2);
    cf = lfun(L_sym2, 2)/zeta(2);
    X = sqrt(N_cond) * T_max / (2*Pi);
    Y = log(X);
    u_f = U / (cf * T_max * Y^4);
    printf("%s,%d,%.2f,%d,%.4f,%.4f,%.4f,%.6f\n", cn, N_cond, T_max, n_zeros, U, Y, cf, u_f)
  )
);
quit;
