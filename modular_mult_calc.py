#!/usr/bin/env python3
n = 4
q = 457 #* 208850

p = 208850

#a = [91, 155, 187, 86]
#b = [51557009, 20688816, 24580469, 90450598]
a = [250, 246, 297, 346]
b = [456, 0, 0, 0]

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
out = [o % q for o in out] 
print("result: {}".format(out))
outn = [(o * -1) % q for o in out]
print("result * -1: {}".format(outn))
print("result / p: {}".format(outp))
