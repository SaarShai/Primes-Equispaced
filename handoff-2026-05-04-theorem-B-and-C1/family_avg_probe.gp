/* Quick probe: check timing for one curve at T=1000 */
default(realprecision, 30);
default(parisize, "1G");

E = ellinit("11a1");
N = ellglobalred(E)[1];
print("N = ", N);
L = lfuncreate(E);

\\ Time c_f via lfunsympow
gettime();
Lsym2 = lfunsympow(E, 2);
csym = lfun(Lsym2, 1);
print("c_f = L(Sym^2 E, 1) = ", csym, "  (took ", gettime(), " ms)");

\\ Zeros up to T=1000
gettime();
zs = lfunzeros(L, 1000);
t1 = gettime();
print("# zeros 0<gamma<=1000: ", #zs, "  (took ", t1, " ms)");

\\ Time one |L'|^2 evaluation
gettime();
v = lfun(L, 1 + I*zs[10], 1);
print("L'(1+i*zs[10]) = ", v, "  |.|^2 = ", abs(v)^2, "  (took ", gettime(), " ms)");

\\ Estimate full sum cost
print("Estimated full sum cost: ", gettime() * #zs / 1000.0, " sec ... but gettime resets - rough estimate");

\\ Do first 10 zeros
gettime();
S = 0;
for(j=1, min(10, #zs), v = lfun(L, 1+I*zs[j], 1); S += abs(v)^2);
t10 = gettime();
print("Sum of first 10 |L'|^2: ", S, "  (took ", t10, " ms => ", t10/10.0, " ms/zero)");
print("Projected for ", #zs, " zeros: ", #zs * t10 / 10.0 / 1000.0, " sec");

quit;
