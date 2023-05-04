import numpy as np
from copy import copy


def CI_95(data):  # compute the 95% confidence interval for columns n * m np array
    n, m = data.shape
    a = np.mean(data, axis=0)
    sd = np.std(data, axis=0)
    hw = 1.96 * sd / np.sqrt(n)
    print("Expected gradient is", a.tolist())
    print("Upper bound is", (a + hw).tolist())
    print("Lower bound is", (a - hw).tolist())


np.random.seed(1)

N = 100  # number of gradient descent applied

s1 = [1, 1, 1, 1, 1]  # initial X
S = []
Y = []
X2 = [1,1,1,1,1]
for rep in range(0, N, 1):
    U = np.random.random(5)
    r = 1/(rep+500) # set r that's going to 0 but sum to infinity
    X1 = []
    for i in range(0, 5, 1):
        X1.append(-np.log(1 - U[i]) * s1[i])
    for i in range(5):
        X2 = copy(X1)
        gradX = (-np.log(1 - U[i]))  # compute the gradient of IPA
        s1[i] = max(s1[i]-gradX * r,0.5)
        X2[i] = (-np.log(1 - U[i]) * max(0.5, s1[i] - gradX))
    S.append(s1)
    Y.append(max(X2[0] + X2[3], X2[0] + X2[2] + X2[4], X2[1] + X2[4]))  # Y(X + deltaX)
print("The best optimized SAN is", S[Y.index(min(Y))])
yfinal = []
for rep in range(100):
    U = np.random.random(5)
    Sfinal = S[Y.index(min(Y))]
    X3 = []
    for i in range(0, 5, 1):
        X3.append(-np.log(1 - U[i]) * s1[i])
    yfinal.append(max(X3[0] + X3[3], X3[0] + X3[2] + X3[4], X3[1] + X3[4]))
print('The optimal activity time is', np.mean(yfinal))

