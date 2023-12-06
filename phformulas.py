import matplotlib.pyplot as plt
import numpy as np

class FileParser():
    def __init__(self, dataID):
        self.file = dataID
        self.times, self.flux = np.loadtxt("./Data/" + dataID + ".tbl")[1:]
        self.size = len(self.times)

    def getOrbitalPeriod(self):
        pass