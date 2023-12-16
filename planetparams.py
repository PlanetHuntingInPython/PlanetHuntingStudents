from statistics import stdev 
from math import floor
from datahandler import AbstractDataHandler, NumpyTableHandler
import matplotlib.pyplot as plt
import numpy as np

APPROX_SAMPLES = 200
OUTLIER_DEVS = 5

class DataAnalyser():
    def __init__(self, dataID, handler:AbstractDataHandler=NumpyTableHandler):
        self.handler = handler(dataID)
        self.times, self.flux = self.handler.get_data()
        self.size = len(self.times)

        self.period = None
        self.stdev = None
        self.transitBound = None
        self.transitLenth = None

    def plot(self):
        plt.figure()
        plt.plot(self.times, self.flux, '.', markersize=2)
        plt.show()


    def getOrbitalPeriod(self):
        return self.period or self.__calculateOrbitalPeriod()
           
    def __calculateOrbitalPeriod(self):
        transit1 = self.__findNextTransit()
        peak = self.__findPeak(transit1)
        self.transitLenth = self.times[peak - transit1] - self.times[0]

        transit1 = self.times[transit1]
        self.period = transit1 - self.times[0]
        nextTransitT = transit1 + self.period
        p = 1
        nTransits = 1
        tLast = self.times[-1]
        while nextTransitT < tLast:
            nextTransitT = self.findNextTransitPeak(nextTransitT) 
            self.period = (nextTransitT - transit1)/nTransits
            p *= 2
            nTransits += p
            nextTransitT += self.period*(p-0.5)
        return self.period

    def getStdev(self):
        return

    def __findTime(self, time):
        return self.times.searchsorted(time) - 1

    def findNextTransitPeak(self, time):
        return self.times[self.__findNextTransitPeak(self.__findTime(time))]

    def __findNextTransitPeak(self, start=0):
        return self.__findPeak(self.__findNextTransit(start))

    def findNextTransit(self, time=0):
        return self.times[self.__findNextTransit(self.__findTime(time))]
    
    def __findNextTransit(self, start=0):
        lb = self.getApproxTransitBound()
        for i in range(start, self.size):
            if self.flux[i] < lb and self.flux[i + 1] < lb and self.flux[i + 2] < lb:
                return i
                
    def findPeak(self, start):
        return self.times[self.__findPeak(self.__findTime(start))]

    def __findPeak(self, start):
        lb = self.getApproxTransitBound()
        iLow = start
        fluxLow = self.flux[start]
        start = self.__findNextTransit(start)
        for i in range(start, self.size):
            if self.flux[i] < fluxLow:
                fluxLow, iLow = self.flux[i], i
            elif self.flux[i] > lb and self.flux[i + 1] > lb and self.flux[i + 2] > lb:
                return iLow
            
    def getApproxTransitBound(self):
        if self.transitBound is None:
            step = floor(APPROX_SAMPLES/3)
            self.transitBound = -OUTLIER_DEVS*min([stdev(self.flux[step*i:step*(i+1)]) for i in range(3)])
        return self.transitBound    