from abc import ABC, abstractmethod
from PyPDF2 import PdfReader
import numpy as np

class AbstractDataHandler(ABC):
    def __init__(self, dataID):
        pass

    @abstractmethod
    def getData(self):
        return None

class LocalDataHandler(AbstractDataHandler):
    stellarMassRadiusDict = None

    def __init__(self, dataID):
        self.dataID = dataID
        self.times, self.flux = np.loadtxt(f"Data/{dataID}.tbl", unpack=True, skiprows=3)[1:]
        if self.stellarMassRadiusDict is None:
            self.__initialiseStellarMassRadiusDict()
        self.radius, self.mass = self.stellarMassRadiusDict[dataID] if dataID in self.stellarMassRadiusDict else None, None

    def getData(self):
        return self.times, self.flux
    
    def __initialiseStellarMassRadiusDict(self):
        f = PdfReader(open("Data/Stellar_Mass_Radius.pdf", 'rb'))
        tableData = f.pages[0].extract_text().split()[9:]
        self.stellarMassRadiusDict = {tableData[i]:(float(tableData[i+1]),float(tableData[i+2]))  for i in range(0,len(tableData),3)}

    def getRadius(self):
        return self.radius

    def getMass(self):
        return self.mass