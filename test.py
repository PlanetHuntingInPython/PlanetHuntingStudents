from data_analyser import DataAnalyser
from time import perf_counter

class Timing():
    def __init__(self, sinceLastOut=True, ms=True):
        self.s = perf_counter()
        self.last = self.s
        self.sinceLastOut = sinceLastOut
        self.unit = 1000 if ms else 1
        self.unitPrefix = 'm'*ms + 's'

    def out(self,label):
        print(f"{label}: {((e := perf_counter()) - self.last)*self.unit} {self.unitPrefix}")
        if self.sinceLastOut:
            self.last = e

    def totalOut(self, label=""):
        if not self.sinceLastOut:
            self.out(label)
        print(f"Total: {(perf_counter() - self.s)*self.unit} {self.unitPrefix}")

def timedTest(dataID, plotType=""):
    print(f"{dataID} results:")
    t = Timing(True, True)
    analyser = DataAnalyser(dataID)
    t.out("Initialisation")
    period = analyser.getOrbitalPeriod()
    t.out("Period")
    m = analyser.getModel()
    print(m.min, m.max)
    t.out("Model")
    print(m.chiSquaredFunc())
    t.out("Model Error")
    print(period)
    t.totalOut()
    analyser.plot(plotType)

#KIC002571238 period = 9.286989632903225
timedTest("KIC002571238", "pm")