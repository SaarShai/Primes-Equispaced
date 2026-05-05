\\ T8 v4 — verify normalization & contour identity
default(realprecision, 30);
default(parisize, 2^30);

E = ellinit("11a1");
L = lfunsympow(E, 2);

print("=== Normalization probe ===");
print("L(1) = ", lfun(L, 1));    \\ 0.589 — this is the special value
print("L(2) = ", lfun(L, 2));    \\ should be reasonable
print("L(3) = ", lfun(L, 3));    \\ Σ a(n)/n^3

\\ Direct sum at s=2 with first 10000 coefficients
av = lfunan(L, 100000);
direct_at_2 = sum(n=1, 100000, av[n]/n^2.);
print("Direct Σ a(n)/n² (n≤10^5) = ", direct_at_2);
direct_at_3 = sum(n=1, 100000, av[n]/n^3.);
print("Direct Σ a(n)/n³ (n≤10^5) = ", direct_at_3);

\\ a(p) for small primes; compare to expected α_p² + α_p β_p + β_p²
\\ For E=11a1: a_p of E gives α_p + β_p = a_p, α_p β_p = p
\\ sym² Frobenius eigenvalues: α_p², α_p β_p = p, β_p² → trace = α² + p + β²= a_p² - p
\\ Expected a_{sym²f}(p) = a_E(p)² - p
print("\nFrobenius check:");
print("  a_E(2) = ", ellap(E, 2), "  a_E(2)²-2 = ", ellap(E,2)^2 - 2, "  PARI lfun: ", av[2]);
print("  a_E(3) = ", ellap(E, 3), "  a_E(3)²-3 = ", ellap(E,3)^2 - 3, "  PARI lfun: ", av[3]);
print("  a_E(5) = ", ellap(E, 5), "  a_E(5)²-5 = ", ellap(E,5)^2 - 5, "  PARI lfun: ", av[5]);
print("  a_E(7) = ", ellap(E, 7), "  a_E(7)²-7 = ", ellap(E,7)^2 - 7, "  PARI lfun: ", av[7]);
print("  a_E(13)= ", ellap(E,13), "  a_E(13)²-13 = ", ellap(E,13)^2 - 13, "  PARI lfun: ", av[13]);

\\ With analytic normalization (Hecke eigenvalues normalized so |α_p|=1):
\\   a_E^norm(p) = a_E(p)/sqrt(p)
\\   a_{sym²f}^norm(p) = a_E^norm(p)² - 1
\\ critical line at 1/2.
\\ With arithmetic normalization (PARI default for elliptic curves):
\\   a_{sym²f}(p) = a_E(p)² - p, growing like p
\\   critical line at s=1, functional eq s ↔ 2-s, special values L(1), zeros at 1+iγ
\\
\\ PARI lfunzeros gives γ where L(1/2+iγ)=0 in analytic norm OR L(1+iγ)=0 in arithmetic.
\\ Check: lfun(L, 1+I*3.8992814948)
gv = lfun(L, 1 + I*3.8992814948);
print("\nL(1 + i·3.8993) = ", gv, "    abs = ", abs(gv));
gv2 = lfun(L, 1/2 + I*3.8992814948);
print("L(1/2 + i·3.8993) = ", gv2, "    abs = ", abs(gv2));

\\ Functional equation symmetry point: s -> k - s where k from Lcomplex
\\ Print central character info
print("\nGamma factors: ", L[1][1][3]);  \\ the [k_1, k_2, ...] degrees
quit;
