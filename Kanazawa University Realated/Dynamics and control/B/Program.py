import numpy as np
import matplotlib.pyplot as plt

# Time axis
t = np.linspace(0, 5, 500)

# Parameters
K = 1.0
T = 1.0

# Unit step response
y = K * (1 - np.exp(-t / T))

# Plot
plt.figure()
plt.plot(t, y)
plt.xlabel("Time (s)")
plt.ylabel("Angular velocity y(t)")
plt.title("Step Response of DC Motor (K = 1, T = 1)")
plt.grid()
plt.show()
