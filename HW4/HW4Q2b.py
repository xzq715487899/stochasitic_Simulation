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

N = 1000  # number of replications

s1 = [0.5, 1, 0.7, 1, 1]  # initial X

IPA = []

for rep in range(0, N, 1):
    U = np.random.random(5)
    X1 = []
    X2 = []
    for i in range(0, 5, 1):
        X1.append(-np.log(1 - U[i]) * s1[i])

    for i in range(5):
        X2 = copy(X1)
        gradX = (-np.log(1 - U[i]))  # compute the gradient of IPA
        X2[i] = X1[i] + 0.00001
        Y1 = max(X1[0] + X1[3], X1[0] + X1[2] + X1[4], X1[1] + X1[4])  # Y(X)
        Y2 = max(X2[0] + X2[3], X2[0] + X2[2] + X2[4], X2[1] + X2[4])  # Y(X + deltaX)
        if Y1 == Y2:  # X(i) is not on the longest path
            IPA.append(0)
        else:  # X(i) is on the longest path
            IPA.append(gradX)
A = np.array(IPA)  # convert the list to np array to calculate Mean and CI for all FD
A = A.reshape((N, 5))
# print(A)
# print(np.mean(A, axis=0))
# print(np.std(A, axis=0))
CI_95(A)
