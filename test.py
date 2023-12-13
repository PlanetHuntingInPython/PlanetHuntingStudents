from planetparams import DataHandler
handler = DataHandler("KIC002571238")
print(handler.getFirstMinimum())
handler.plot()