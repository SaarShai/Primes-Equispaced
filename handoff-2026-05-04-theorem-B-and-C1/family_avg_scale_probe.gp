default(realprecision, 30);
default(parisize, "2G");
E = ellinit("11a1");
L = lfuncreate(E);

gettime();
zs = lfunzeros(L, 2000);
print("T=2000  #zeros=", #zs, "  took ", gettime(), " ms");

gettime();
zs = lfunzeros(L, 5000);
print("T=5000  #zeros=", #zs, "  took ", gettime(), " ms");

gettime();
zs = lfunzeros(L, 10000);
print("T=10000 #zeros=", #zs, "  took ", gettime(), " ms");

quit;
