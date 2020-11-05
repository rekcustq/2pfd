import random
import numpy as np

A = ['ID', 'Tuổi', 'Thu nhập', 'Sinh viên', 'Đánh giá tín dụng']
U = [['youth', 'high', 'no', 'fair'], 
     ['youth', 'high', 'no', 'excellent'],
     ['middle', 'high', 'no', 'fair'],
     ['senior', 'medium', 'no', 'fair'],
     ['senior', 'low', 'yes', 'fair'],
     ['senior', 'low', 'yes', 'excellent'], 
     ['middle', 'low', 'yes', 'excellent'], 
     ['youth', 'medium', 'no', 'fair'], 
     ['youth', 'low', 'yes', 'fair'], 
     ['senior', 'medium', 'yes', 'fair'], 
     ['youth', 'medium', 'yes', 'excellent'], 
     ['middle', 'medium', 'no', 'excellent'], 
     ['middle', 'high', 'yes', 'fair'], 
     ['senior', 'medium', 'no', 'excellent']]
V = ['no', 'no', 'yes', 'yes', 'yes', 'no', 'yes', 'yes', 'yes', 'yes', 'yes', 'yes', 'yes', 'no']
a = U
m = 4
t = n = 14
u = []
k = []
s = []

kx = np.zeros((n))
kX = np.zeros((n))
ky = np.zeros((n))
kY = np.zeros((n))
kp = np.zeros((n))
kP = np.zeros((n))
kq = np.zeros((n))
kQ = np.zeros((n))
r = np.zeros((n))
c = np.zeros((n))
v = np.zeros((n))

X = np.zeros((m, t))
Y = np.zeros((m, t))
d = np.zeros((m, t))

q = 2579 # p
g = 2 # alpha
x = 765 # a
h = (g**x) % q # = (2**765) % q = 949 # beta
C = np.zeros((m, t, n, 4))
R = np.zeros((m, t, n, 4))
K = np.zeros((m, t, n, 4))

def gen_key():
    x = random.randint(1, q-1)
    X = g**x % q
    return x, X

# Phase 1
for l in enumerate(U):
    # U[l]
    kx[l], kX[l] = gen_key()
    ky[l], kY[l] = gen_key()
    kp[l], kP[l] = gen_key()
    kq[l], kQ[l] = gen_key()
    
    for i in range(m):
        for j in range(t):
            u[l] = int(a[l][j] == T[i][j].a)
            k[l] = random.randint(1, q-1)
            s[l] = random.randint(1, q-1)
            # To Miner
            C[i][j][l][1] = g**u[l] * kX[l]**s[l]
            C[i][j][l][2] = g**s[l]
            C[i][j][l][3] = kX[l]**k[l] * kP[l]
            C[i][j][l][4] = kY[l]**k[l] * kQ[l]

for i in range(m):
    for j in range(t):
        X[i][j] = 1
        Y[i][j] = 1
        for l in range(n):
            X[i][j] *= C[i][j][l][3]
            Y[i][j] *= C[i][j][l][4]

# Phase 2
for l in enumerate(V):
    for i in range(m):
        for j in range(t):
            # Get from Miner
            r[l] = random.randint(1, q-1)
            # To Miner
            if c[l] != T[i][j].c:
                v[l] = 0
                R[i][j][l][1] = kX[l]**r[l] * X[i][j]**kq[l]
                R[i][j][l][2] = g**r[l]
                R[i][j][l][3] = Y[i][j]**kp[l]
            else:
                v[l] = 1
                R[i][j][l][1] = kX[l](r[l] + s[l]) * X[i][j]**kq[l]
                R[i][j][l][2] = g**(r[l] + s[l])
                R[i][j][l][3] = Y[i][j]**kp[l]

# Phase 3
for l in enumerate(U):
    for i in range(m):
        for j in range(t):
            # Get from Miner
            # To Miner
            K[i][j][l][1] = R[i][j][l][1] * R[i][j][l][2]**(-kx[l]) * X[i][j]**(k[l] * ky[l])
            K[i][j][l][1] = R[i][j][l][3] * Y[i][j]**(k[l] * kx[l])

# Phase 4
for i in range(m):
    for j in range(t):
        d[i][j] = 1
        for l in range(n):
            d[i][j] *= K[i][j][l][1] / K[i][j][l][2]
        f = 0
        for fT in range(n):
            if d[i][j] == (g**fT) % q:
                f = fT
                break
        
        for l in range(p):
            f[c[l]] # ?