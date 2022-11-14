#!/usr/bin/env python3
n = 4
q = 134217689# * 18014388040500722

p = 18014388040500722

a = [107473724, 548062, 50708536, 95944201]
b = [2394511973064212855166608, 1323821576830572365394598, 1277806234317375373317768, 1037370199752092571066329] 

temp = [0] * (len(a) + len(b))
out = [0] * n

for i in range(len(a)):
    for j in range(len(b)):
        temp[i + j] += a[i] * b[j]

print(temp)

for i in range(len(temp)):
    if(i >= n):
        out[i - n] -= temp[i]
    else:
        out[i] += temp[i]
outp = [(o // p) % (q/p) for o in out]
out_mod = [o % q for o in out] 
print("no mod: {}".format(out))
print("result: {}".format(out_mod))
outn = [(o * -1) % q for o in out_mod]
print("result * -1: {}".format(outn))
print("result / p: {}".format(outp))
