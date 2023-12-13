import numpy as np
import matplotlib.pyplot as plt

# Load the data
z, t, flux = np.loadtxt("Data/KIC006922244.tbl", unpack=True, skiprows=3)

plt.plot(t, flux, "k.", markersize=2)
plt.xlabel("time (days)")
plt.ylabel("Flux")
plt.tight_layout()
plt.show()