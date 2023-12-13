import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import make_interp_spline 

z, t, flux = np.loadtxt("./Data/KIC006922244.tbl",unpack=True,skiprows=3)

xnew = np.linspace(t.min(), t.max(), 300) 
  
gfg = make_interp_spline(t, flux, k=3) 
  
y_new = gfg(xnew) 
  
plt.plot(xnew, y_new, '.') 
  
plt.show() 