import numpy as np

N = 10**7  # number of samples

X = 2.0*(np.random.rand(2, N)-0.5)
r = np.sqrt(np.power(X[0, :], 2)+np.power(X[1, :], 2))
Y = np.zeros(N)

Y[r < 1.0] = 4.0
print('%.3f' % np.mean(Y))
