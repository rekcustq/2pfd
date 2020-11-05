import random
from datetime import datetime

debug = 1
random.seed(datetime.now())
n = 3
q = 17 # prime
g = 3 # alpha
# x = random.randint(1, q-1) # 765 # random
# h = (g**x) % q # = (2**765) % q = 949 # beta

# U = [0, 0, 1, 1, 0]
# V = [1, 1, 0, 0, 1]
U = []
V = []
for i in range(n):
    U.append(1)
    V.append(1)
if debug: print(U, '\n', V)

kx = []
ky = []
kz = []
kX = []
kY = []
kZ = []
for i, u in enumerate(U):
    kx.append(random.randint(1, q-1))
    kX.append(g**kx[i] % q)
    ky.append(random.randint(1, q-1))
    kY.append(g**ky[i] % q)
    kz.append(random.randint(1, q-1))
    kZ.append(g**kz[i] % q)

kp = []
kq = []
ks = []
kP = []
kQ = []
kS = []
for i, v in enumerate(V):
    kp.append(random.randint(1, q-1))
    kP.append(g**kp[i] % q)
    kq.append(random.randint(1, q-1))
    kQ.append(g**kq[i] % q)
    ks.append(random.randint(1, q-1))
    kS.append(g**ks[i] % q)

# x = 0
# y = 0
# for i in range(n):
#     x += kx[i] + kp[i]
#     y += ky[i] + kq[i]
# if debug: print(g**x % q, g**y % q)

X = 1
Y = 1
for i in range(n):
    X = (X * ((kX[i] * kP[i]) % q)) % q
    Y = (Y * ((kY[i] * kQ[i]) % q)) % q
# if debug: print(X, Y)

# def gcd(a, b):
#     if a == 0:
#         return b
    
#     return gcd(b % a, a)

# def modInv(x, q):
#     g = gcd(x, q)
#     if g != 1:
#         return -1
#     return x**(q-2) % q

#------------------------------------------------
print('Phase 1')
c = []
C1 = []
C2 = []
for i, u in enumerate(U):
    c.append(random.randint(0, q-1))
    C1.append(((g**u % q) * (kZ[i]**c[i] % q)) % q)
    C2.append(g**c[i] % q)
    # Gửi C1[i] và C2[i] đến Miner
    if debug: print(C1[i], C2[i])
print()

#------------------------------------------------
print('Phase 2')
r = []
R1 = []
R2 = []
R3 = []
for i, v in enumerate(V):
    # Lấy C1[i] và C2[i] từ Miner
    r.append(random.randint(0, q-1))
    if v == 0:
        R1.append(X**kq[i] % q)
        R2.append(((C2[i]**(ks[i] * r[i]) % q) * Y**kp[i]) % q)
        R3.append(kS[i]**r[i] % q)
    if v == 1:
        R1.append(((C1[i]**v % q) * X**kq[i]) % q)
        R2.append(((C2[i]**(ks[i] * r[i]) % q) * Y**kp[i]) % q)
        R3.append((pow(kZ[i], q-2, q) * (kS[i]**r[i] % q)) % q)
    # Gửi R1[i], R2[i] và R3[i] đến Miner
    if debug: print(R1[i], R2[i], R3[i])
print()

#------------------------------------------------
print('Phase 3')
K1 = []
K2 = []
for i, u in enumerate(U):
    # Lấy R1[i], R2[i] và R3[i] từ Miner
    K1.append((R1[i] * (R3[i]**c[i] % q) * (X**ky[i] % q)) % q)
    K2.append((R2[i] * (Y**kx[i] % q)) % q)
    # Gửi K1[i] và K2[i] đến Miner
    if debug: print(K1[i], K2[i])
print()

#------------------------------------------------
print('Phase 4')
d = 1
for i in range(n):
    d = (d * (K1[i] * pow(K2[i], q-2, q))) % q
print(d)

for f in range(q):
    tmp = g**f % q
    if tmp == d:
        print(f)
        break