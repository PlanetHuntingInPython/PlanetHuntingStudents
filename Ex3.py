import matplotlib.pyplot as plt
import numpy as np

z, t, flux = np.loadtxt("./Data/KIC006922244.tbl",unpack=True,skiprows=3)
plt.plot(t, flux, '.')
plt.xlabel("Time")
plt.ylabel("Luminosity")
plt.show()
StarRadius = 1.451 * 7 * (10**8)
print(t)
print(t[0])