from planetparams import DataAnalyser
handler = DataAnalyser("KIC002571238")
print(handler.getOrbitalPeriod())
handler.plot()