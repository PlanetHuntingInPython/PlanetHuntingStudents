from abc import ABC, abstractmethod
import numpy as np

class AbstractDataHandler(ABC):
    def __init__(self, dataID):
        pass

    @abstractmethod
    def get_data(self):
        return None
    
class NumpyTableHandler(AbstractDataHandler):
    def __init__(self, dataID):
        self.dataID = dataID
        self.times, self.flux = np.loadtxt(f"./Data/{dataID}.tbl", unpack=True, skiprows=3)[1:]

    def get_data(self):
        return self.times, self.flux