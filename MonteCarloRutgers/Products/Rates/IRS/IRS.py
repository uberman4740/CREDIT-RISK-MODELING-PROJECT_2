import numpy as np
from pandas import DataFrame

class IRS(object):
    def __init__(self, libor,fixedRate):
        self.libor=libor
        self.ntimes = np.shape(self.libor)[0]
        self.fixedRate = fixedRate
        self.MTMValue = []
        return

    def MTM(self):
        self.MTMValue = np.zeros(np.shape(self.libor))
        for i in range(self.ntimes):
            self.MTMValue[i,:] = (self.libor[i,:] - self.fixedRate)*self.libor[i,:]
        return np.average(self.MTMValue,axis=1)[self.ntimes-1]