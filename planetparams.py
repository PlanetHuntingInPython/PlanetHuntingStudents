from statistics import stdev
from math import floor
from datahandler import AbstractDataHandler, LocalDataHandler
import matplotlib.pyplot as plt
import numpy as np

SAMPLES = 300
OUTLIER_DEVS = 5

class DataAnalyser():
    def __init__(self, dataID, handler:AbstractDataHandler=LocalDataHandler):
        self.handler = handler(dataID)
        self.times, self.flux = self.handler.getData()
        self.size = len(self.times)

        self.period = None
        self.transitBound = None
        self.transitLenth = None
        self.timeDelta = min(self.times[1]-self.times[0], self.times[2]-self.times[1])

    def plot(self):
        plt.figure()
        plt.xlabel("Time")
        plt.ylabel("Flux")
        plt.plot(self.times, self.flux, '.', markersize=2)
        plt.show()

    def getOrbitalPeriod(self):
        return self.period or self.__calculateOrbitalPeriod()
           
    def __calculateOrbitalPeriod(self):
        transit1Start = self.__findTransit()
        transit1 = self.__findPeak(transit1Start)
        self.transitLenth = 2*(self.times[transit1] - self.times[transit1Start])

        transit1 = self.times[transit1]
        self.period = transit1 - self.times[0]
        nextTransitTimePredicted = transit1 + self.period
        p = 1
        nTransits = 1
        skippedTransits = 0
        endTime = self.times[-1]
        step = self.__timeToIndex(self.transitLenth/2)
        try:
            while nextTransitTimePredicted < endTime:
                nextTransitTimeFound = self.times[self.__findTransitPeak(self.__findTime(nextTransitTimePredicted), step)]
                if nTransits > 1:
                    skippedTransits = round((nextTransitTimeFound-nextTransitTimePredicted)/self.period)
                self.period = (nextTransitTimeFound - transit1)/(nTransits + skippedTransits)
                p *= 2
                nTransits += p + skippedTransits
                nextTransitTimePredicted = nextTransitTimeFound + self.period*(p-0.01)
        except Exception:
            pass
        transitLast = self.times[self.__findTransitPeak(-1,-1)]
        return (transitLast-transit1)/round((transitLast-transit1)/self.period)

    def __findTime(self, time):
        return self.times.searchsorted(time) - 1
    
    def __timeToIndex(self, time):
        return 1 if time is None else floor(time/self.timeDelta) or (1 if time >= 0 else -1)

    def findTransitPeak(self, time=0, step=None):
        return self.times[self.__findTransitPeak(self.__findTime(time), self.__timeToIndex(step))]

    def __findTransitPeak(self, start=0, step=1):
        return self.__findPeak(self.__findTransit(start, step))

    def findTransit(self, time=0, step=None):
        return self.times[self.__findTransit(self.__findTime(time), self.__timeToIndex(step))]
    
    def __findTransit(self, start=0, step=1):
        lb = self.getApproxTransitBound()
        end = self.size - 2 if step >= 0 else start
        start = start if step >= 0 else self.size - 2
        for i in range(start, end, step):
            if self.flux[i] < lb and self.flux[i + 1] < lb and self.flux[i + 2] < lb:
                return i
        raise Exception("Transit not found.")
                
    def findPeak(self, time=0, step=None):
        return self.times[self.__findPeak(self.__findTime(time), self.toI(step))]

    def __findPeak(self, start=0):
        lb = self.getApproxTransitBound()
        iLow = start
        fluxLow = self.flux[start]
        for i in range(start, self.size - 2):
            if self.flux[i] < fluxLow:
                fluxLow, iLow = self.flux[i], i
            elif self.flux[i] > lb and self.flux[i + 1] > lb and self.flux[i + 2] > lb:
                return iLow
            
    def getApproxTransitBound(self):
        """
        Returns an approximate flux value below which transits should occur:

        Returns:
            float (Flux Value) -- Approx Transit Bound = Q1 - 3*IR, where Q1 is the lower quartile, IR the inequartile range.
        """
        if self.transitBound is None:
            sortedSamples = sorted(self.flux[:SAMPLES])
            self.transitBound = 4*sortedSamples[floor(0.25*SAMPLES)] - 3*sortedSamples[floor(0.75*SAMPLES)]
        return self.transitBound