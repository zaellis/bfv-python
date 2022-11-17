#!/usr/bin/env python3
from BFV import *
from helper import *

from random import randint
from math import log,ceil

# This implementation follows the description at https://eprint.iacr.org/2012/144.pdf
# Brakerski/Fan-Vercauteren (BFV) somewhat homomorphic encryption scheme
#
# Polynomial arithmetic on ciphertext domain is performed in Z[x]_q/x^n+1
# Polynomial arithmetic on plaintext domain is performed in Z[x]_t/x^n+1
# * n: ring size
# * q: ciphertext coefficient modulus
# * t: plaintext coefficient modulus (if t is equal to 2, no negative values is accepted)
# * psi,psiv,w,wv: polynomial arithmetic parameters
#
# Note that n,q,t parameters together determine the multiplicative depth.

# Parameter generation (pre-defined or generate parameters)
PD = 1 # 0: generate -- 1: pre-defined

if PD == 0:
    # Select one of the parameter sets below
    t = 16;   n, q, psi = 1024 , 132120577         , 73993                # log(q) = 27
    # t = 256;  n, q, psi = 2048 , 137438691329      , 22157790             # log(q) = 37
    # t = 1024; n, q, psi = 4096 , 288230376135196673, 60193018759093       # log(q) = 58

    # other necessary parameters
    psiv= modinv(psi,q)
    w   = pow(psi,2,q)
    wv  = modinv(w,q)
else:
    # Enter proper parameters below
    #t, n, logq = 16, 1024, 27
    t, n, logq = 16, 4, 27
    # t, n, logq = 256, 2048, 37
    # t, n, logq = 1024, 4096, 58

    # other necessary parameters (based on n and log(q) determine other parameter)
    q,psi,psiv,w,wv = ParamGen(n,logq) 

# Determine mu, sigma (for discrete gaussian distribution)
mu    = 0
sigma = 0.5 * 3.2

# Determine T, p (for relinearization and galois keys) based on noise analysis 
T = 256
p = q**2 + 1

# Generate polynomial arithmetic tables
w_table    = [1]*n
wv_table   = [1]*n
psi_table  = [1]*n
psiv_table = [1]*n
for i in range(1,n):
    w_table[i]    = ((w_table[i-1]   *w)    % q)
    wv_table[i]   = ((wv_table[i-1]  *wv)   % q)
    psi_table[i]  = ((psi_table[i-1] *psi)  % q)
    psiv_table[i] = ((psiv_table[i-1]*psiv) % q)

qnp = [w_table,wv_table,psi_table,psiv_table]

print("--- Starting BFV Demo")

# Generate BFV evaluator
Evaluator = BFV(n, q, t, mu, sigma, qnp)

# Generate Keys
Evaluator.SecretKeyGen()
#Evaluator.PublicKeyGen()

# print system parameters
print(Evaluator)

# Generate random message
n1 = randint(-3,3)

print("--- Random integers n1 and n2 are generated.")
print("* n1: {}".format(n1))
print("")

# Encode random messages into plaintext polynomials
print("--- n1 is encoded as polynomial m1(x).")
m1 = Evaluator.IntEncode(n1)

print("* m1(x): {}".format(m1))
print("")

# Encrypt message
ct1 = Evaluator.Encryptionv2(m1)

#generate keyswitch keys and switch self.sk to new key
mt = Evaluator.Decryption(ct1)
print("* -as + dm + e: {}".format(ct1[0]))
print("* a: {}".format(ct1[1]))
print("")
nr = Evaluator.IntDecode(mt)
print(nr)

print("* p: {}".format(p))
print("")

Evaluator.EvalKeyGenV3(p)
ct_new = Evaluator.KeySwitch(ct1)

mt = Evaluator.Decryption(ct_new)
print(mt)

nr = Evaluator.IntDecode(mt)
print(nr)
