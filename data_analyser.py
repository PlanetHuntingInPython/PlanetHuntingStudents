from statistics import stdev
from math import floor, ceil
from data_handler import AbstractDataHandler, LocalDataHandler
import matplotlib.pyplot as plt
import numpy as np
from pwlf import PiecewiseLinFit

SAMPLES = 200

class DataAnalyser():
    def __init__(self, dataID, handler:AbstractDataHandler=LocalDataHandler):
        self.handler = handler(dataID)
        #Flux against Time data
        self.times, self.flux = self.handler.getData()
        self.phaseFoldedTime = None
        #Stellar radius and mass
        self.radius, self.mass = self.handler.getRadius(), self.handler.getMass()

        self.size = len(self.times)
        self.period = None
        self.transitBound = None
        self.transitLength = None
        self.phase = None
        self.dt = min(self.times[1]-self.times[0], self.times[2]-self.times[1])

    def plot(self, plotType=""):
        plt.figure()
        plt.xlabel("Time")
        plt.ylabel("Flux")
        match plotType:
            case "normal" | "standard" | "n" | "s":
                plt.plot(self.times, self.flux, '.', markersize=2)
            case "phase" | "phase folded" | "p":
                plt.plot(self.__getPhaseFoldedTime(), self.flux, '.', markersize=2)
        plt.show()

    def __getPhaseFoldedTime(self):
        if self.phaseFoldedTime is None:
            self.getOrbitalPeriod()
            self.phaseFoldedTime = ((self.times - self.phase + self.period/2) % self.period) - self.period/2
        return self.phaseFoldedTime

    def getOrbitalPeriod(self):
        return self.period if self.period is not None else self.__calculateOrbitalPeriod()

    def getTransitLength(self):
        if self.transitLength is None:
            self.getPhase()
        return self.transitLength

    def getPhase(self):
        if self.phase is None:
            firstTransitStart, firstTransitPeak = self.__findTransitBounds()[:2]
            self.phase = self.times[firstTransitPeak]
            self.transitLength = 2*(self.phase - self.times[firstTransitStart])
        return self.phase
    
    def __calculateOrbitalPeriod(self):
        self.getPhase()
        self.period = self.phase - self.times[0]
        nextTransitTimePredicted = self.phase + self.period
        searchStep = self.__timeToIndex(self.transitLength/2)
        lastTransit = self.times[self.__findTransitPeak(-1,-searchStep)]
        nTransitsStep, nTransits, skippedTransits = 1, 1, 0
        while nextTransitTimePredicted < lastTransit:
            nextTransitTimeFound = self.times[self.__findTransitPeak(self.__findTime(nextTransitTimePredicted), searchStep)]
            if nTransits > 1:
                skippedTransits = round((nextTransitTimeFound-nextTransitTimePredicted)/self.period)
            self.period = (nextTransitTimeFound - self.phase)/(nTransits + skippedTransits)
            nTransitsStep *= 2
            nTransits += nTransitsStep + skippedTransits
            nextTransitTimePredicted = nextTransitTimeFound + self.period*(nTransitsStep-0.05)
        return (lastTransit-self.phase)/round((lastTransit-self.phase)/self.period)

    def __findTime(self, time):
        return self.times.searchsorted(time) - 1
    
    def __timeToIndex(self, time):
        return 1 if time is None else floor(time/self.dt) or (1 if time >= 0 else -1)

    def findTransitPeak(self, time=0, step=None):
        return self.times[self.__findTransitPeak(self.__findTime(time), self.__timeToIndex(step))]

    def __findTransitPeak(self, start=0, step=1):
        return self.__findTransitBounds(start, step)[1]
    
    def __findTransitBounds(self, start=0, step=1):
        """
        Returns the time index of a transit's start, peak and end.

        ----------
        Parameters:
            start (int) - The time index the searching of a transit begins from.

            step (int) - The distance between samples for detecting a transit. When searching for a transit of a given length, the step 
            should be half the transit length.

        ----------
        Returns:
            tuple (start, peak, end):
                start (int) - The time index at which the transit is detected (flux is inside the transit bound consistently).
                peak (int) - The time index at which the transit reaches its maximum flux.
                end (int) - The time index at which the transit ends (flux is outside the transit bound consistently). 
        """
        lb = self.getApproxTransitBound()
        start = self.__findTransit(start, step)
        iLow = start
        fluxLow = self.flux[start]
        for i in range(start, self.size - 2):
            if self.flux[i] < fluxLow:
                fluxLow, iLow = self.flux[i], i
            elif self.flux[i] > lb and self.flux[i + 1] > lb and self.flux[i + 2] > lb:
                return start, iLow, i

    def __findTransit(self, start=0, step=1):
        """
        Searches for the start of a transit. For a transit to be detected, the flux value must be inside the transit bound consistently.
        
        ----------
        Parameters:
            start (int) - The time index the searching of a transit begins from.

            step (int) - The distance between samples for detecting a transit. When searching for a transit of a given length, the step 
            should be half the transit length.

        ----------
        Returns:
            tuple (start, peak, end):
                start (int) - The time index at which the transit is detected (flux is inside the transit bound consistently).

                peak (int) - The time index at which the transit reaches its maximum flux.

                end (int) - The time index at which the transit ends (flux is outside the transit bound consistently). 
        """
        lb = self.getApproxTransitBound()
        end = self.size - 2 if step >= 0 else start
        start = start if step >= 0 else self.size - 2
        for i in range(start, end, step):
            if self.flux[i] < lb and self.flux[i + 1] < lb and self.flux[i + 2] < lb:
                return i
        raise Exception("Transit not found.")
            
    def getApproxTransitBound(self):
        """
        Returns an approximate flux value below which transits should occur:

        ----------
        Returns:
            float (Flux Value) -- Approx Transit Bound = Q1 - 3*IR, where Q1 is the lower quartile, IR the inequartile range.
        """
        if self.transitBound is None:
            sortedSamples = sorted(self.flux[:SAMPLES])
            self.transitBound = 4*sortedSamples[floor(0.25*SAMPLES)] - 3*sortedSamples[floor(0.75*SAMPLES)]
        return self.transitBound