from math import floor
from data_handler import AbstractDataHandler, LocalDataHandler
import matplotlib.pyplot as plt
import numpy as np
from numpy.polynomial.polynomial import Polynomial, polyval

SAMPLES = 200

def plot(time, flux):
    plt.figure()
    plt.xlabel("Time")
    plt.ylabel("Flux")
    plt.plot(time, flux, '.', markersize=2)
    plt.show()

class TransitDetector():
    def __init__(self, times, flux, averageTime=False):
        self.times, self.flux = times, flux
        self.transitBound = None

        self.size = len(self.times)
        self.transitBound = None
        self.dt = min(self.times[1]-self.times[0], self.times[2]-self.times[1]) if averageTime else (self.times[-1] - self.times[0])/self.size
        self.standardStep = 1
        
        self.end = self.times[-1]
        self.start = self.times[0]

    def setStandardStep(self, time):
        self.standardStep = abs(floor(time/self.dt)) or 1

    def __findTime(self, time):
        return (self.times.searchsorted(time) or 1) - 1
    
    def __normaliseStep(self, step):
        return self.standardStep if step is None else floor(step*self.standardStep) or (self.standardStep if step >= 0 else -self.standardStep)

    def findTransitPeak(self, time=0, step=None):
        return self.times[self.__findTransitPeak(self.__findTime(time), self.__normaliseStep(step))]

    def __findTransitPeak(self, start=0, step=1):
        return self.__findTransitBounds(start, step)[1]
    
    def findTransitBounds(self, time=0, step=None):
        return tuple((self.times[x] for x in self.__findTransitBounds(self.__findTime(time), self.__normaliseStep(step))))

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
        end = self.size - 2 if step >= 0 else 0
        for i in range(start, end, step):
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
        end = self.size - 2 if step >= 0 else 0
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
    
    def __getitem__(self, key):
        if isinstance(key, slice):
            start = self.__findTime(key.start)
            stop = self.__findTime(key.stop)
            return self.times[start:stop:key.step], self.flux[start:stop:key.step]
        else:
            i = self.__findTime(key)
            return self.times[i], self.flux[i]

class DataAnalyser():
    def __init__(self, dataID, dataHandler:AbstractDataHandler=LocalDataHandler):
        dataHandler = dataHandler(dataID)
        #Flux against Time data
        self.times, self.flux = dataHandler.getData()
        self.phaseFoldedTimes, self.phaseFoldedFlux = None, None
        self.transits = TransitDetector(self.times, self.flux)
        self.model = None
        #Stellar radius and mass
        self.radius, self.mass = dataHandler.getRadius(), dataHandler.getMass()


        self.size = len(self.times)
        self.period = None
        self.transitBound = None
        self.transitLenth = None
        self.phase = None
        self.dt = min(self.times[1]-self.times[0], self.times[2]-self.times[1])

    def plot(self, plotType=""):
        match plotType:
            case "normal" | "standard" | "n" | "s":
                plot(self.times, self.flux)
            case "phase" | "phase folded" | "p":
                plot(*self.getPhaseFoldedData())
            case "model" | "m":
                self.getModel().plot()
            case "phase model" | "pm" | "p+":
                plot(*self.getPhaseFoldedData())
                plot(self.getModel().plot())

    def getData(self):
        return self.times, self.flux

    def getPhaseFoldedData(self):
        if self.phaseFoldedTimes is None:
            self.getOrbitalPeriod()
            self.phaseFoldedTimes = ((self.times - self.phase + self.period/2) % self.period) - self.period/2
            sort = np.argsort(self.phaseFoldedTimes)
            self.phaseFoldedTimes, self.phaseFoldedFlux = self.phaseFoldedTimes[sort], self.flux[sort]
        return self.phaseFoldedTimes, self.phaseFoldedFlux
    
    def getModel(self):
        if self.model is None:
            self.model = TransitModel(*self.getPhaseFoldedData())
        return self.model

    def getOrbitalPeriod(self):
        return self.period if self.period is not None else self.__calculateOrbitalPeriod()

    def getTransitLength(self):
        if self.transitLength is None:
            self.getPhase()
        return self.transitLength

    def getPhase(self):
        if self.phase is None:
            firstTransitStart, self.phase, firstTransitEnd = self.transits.findTransitBounds()
            self.transitLenth = firstTransitEnd - firstTransitStart
        return self.phase
    
    def __calculateOrbitalPeriod(self):
        self.getPhase()
        self.period = self.phase - self.times[0]
        nextTransitTimePredicted = self.phase + self.period
        self.transits.setStandardStep(self.transitLenth/2)
        lastTransit = self.transits.findTransitPeak(self.transits.end,-1)
        nTransitsStep, nTransits, skippedTransits = 1, 1, 0
        while nextTransitTimePredicted < lastTransit:
            nextTransitTimeFound = self.transits.findTransitPeak(nextTransitTimePredicted)
            if nTransits > 1:
                skippedTransits = round((nextTransitTimeFound-nextTransitTimePredicted)/self.period)
            self.period = (nextTransitTimeFound - self.phase)/(nTransits + skippedTransits)
            nTransitsStep *= 2
            nTransits += nTransitsStep + skippedTransits
            nextTransitTimePredicted = nextTransitTimeFound + self.period*(nTransitsStep-0.05)
        return (lastTransit-self.phase)/round((lastTransit-self.phase)/self.period)

class TransitModel():
    def __init__(self, phaseFoldedTimes, phaseFoldedFlux):
        self.phaseFoldedTimes, self.phaseFoldedFlux = phaseFoldedTimes, phaseFoldedFlux
        self.transitDetector = TransitDetector(phaseFoldedTimes, phaseFoldedFlux, True)
        self.min, self.max = self.transitDetector.findTransitBounds(0,-1)[2], self.transitDetector.findTransitBounds(0)[2]
        self.model = Polynomial.fit(*self.transitDetector[self.min:self.max], 6)
        self.coeffs = self.model.convert().coef

    def plot(self):
        plot(self.phaseFoldedTimes, np.fromiter(self, float))

    def __iter__(self):
        for i in self.phaseFoldedTimes:
            yield self[i]

    def __getitem__(self, time):
        return polyval(time, self.coeffs) if self.min < time < self.max else .0