__author__ = 'Yule Jin'
import numpy as np
from pandas import DataFrame

class CVA(object):
    def __init__(self, libor, t_series,survival, recovery, PV):
        self.libor=libor
        self.t_series = t_series
        self.ntimes=len(self.t_series)
        self.ntimes = np.shape(self.libor)[0]
        self.survival = survival
        self.recovery = recovery
        self.MTMavg = 0.0
        self.parspread = 0.0
        self.pv = PV
        self.EPE = 0.0
        self.CVA = 0.0
        return

    def calEPE(self):
        self.pv[self.pv<0]=0
        self.EPE = np.sum(self.pv)
        return self.EPE

    def calCVA(self):
        self.CVA = (1-self.recovery)*(1- np.average(self.survival[self.ntimes-1]))*self.calEPE()
        return self.CVA
