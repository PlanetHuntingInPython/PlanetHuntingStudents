import statistics
import os
import matplotlib.pyplot as plt
import numpy as np

OUTLIER_FACTOR = 5

class DataHandler():
    def __init__(self, dataID):
        self.file = dataID
        self.times, self.flux = np.loadtxt(f"./Data/{dataID}.tbl", unpack=True, skiprows=3)[1:]
        self.size = len(self.times)

    def plot(self):
        plt.figure()
        plt.plot(self.times, self.flux, '.', markersize=2)
        plt.show()

    def getOrbitalPeriod(self):
        pass

    def getEquilibriumState(self):
        fluxMean = statistics.mean(self.flux[:100])
        fluxValidRange = statistics.stdev(self.flux[:100]) * OUTLIER_FACTOR
        return fluxMean, fluxValidRange

    def getFirstMinimum(self, start=0):
        mean, validRange = self.getEquilibriumState()
        for i in range(start, len(self.times)):
            if self.flux[i] < mean - validRange:
                break
        return self.times[i]

