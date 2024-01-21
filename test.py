from planetparams import DataAnalyser
#KIC002571238 period = 9.286989632903225
analyser = DataAnalyser("KIC002571238")
print(analyser.getOrbitalPeriod())
analyser.plot()
analyser.getApproxTransitBound()
