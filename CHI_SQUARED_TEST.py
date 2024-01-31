import numpy as np
import matplotlib.pyplot as plt

# 1/N * summation of (Fi - Fm)^2 / o^2  N times

c, a, b = np.loadtxt("model.tbl", unpack= True)
data_file = "Planet-Hunting-local/KIC006922244.tbl" #data file that will be inputted
z, x, y = np.loadtxt(data_file, unpack = True, skiprows = 3)

N = len(x) 
total_of_squares = 0
total_for_mean = 0
for i in y:
    total_of_squares += i**2
    total_for_mean += i
mean_of_squares = total_of_squares/N
mean = total_for_mean/N

variance = mean_of_squares - mean**2

# N = number of data recordings

sum = 0
for i in range(N):
    sum = ((y[i] - b[i])**2)/variance

X_squared = (1/N)*sum