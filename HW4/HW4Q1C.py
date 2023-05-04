import scipy.stats
import numpy as np

q = 0.95 ** (1 / 5)
print(q)
# find T critical value
#t = scipy.stats.t.ppf(q=q, df=99)
t = scipy.stats.t.ppf(q=q, df=499)
print(t)

# X = [14563.12, 14120.54, 14183.89, 14193.99, 14392.32, 15070.28]
# S = [540718.99, 249321.93, 248723.14, 270852.59, 195064.12, 123330.97]
# Y = []
X500 = [14609.78, 14181.33, 14194.31, 14234.95, 14412.74, 15081.34]
S500 = [609189.88, 384984.86, 291411.53, 297170.89, 170901.57, 138963.18]
Y500 = []
for i in range(6):
    threshold = X500[1] + np.sqrt(t * t * S500[i] / 100 + t * t * S500[1] / 100)
    Y500.append(threshold)
print('Subset selection threshold for X1 - X6', Y500)
