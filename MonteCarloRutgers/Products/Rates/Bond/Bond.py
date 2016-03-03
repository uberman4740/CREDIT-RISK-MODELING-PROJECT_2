__author__ = 'Yule Jin'
import numpy as np
from pandas import DataFrame

class bond(object):
    def __init__(self, libor, coupon, t_series,survival, recovery):
        self.libor=libor
        self.coupon=coupon
        self.t_series = t_series
        self.ntimes=len(self.t_series)
        self.pvAvg=0.0
        self.pvAvgRiskless=0.0
        self.ntimes = np.shape(self.libor)[0]
        self.ntrajectories = np.shape(self.libor)[1]
        self.cashFlows = DataFrame()
        self.survival = survival
        self.recovery = recovery
        return
    ## present value of risky bond
    def pv(self):
        deltaT= np.zeros(self.ntrajectories)
        ones = np.ones(shape=[self.ntrajectories])
        for i in range(1,self.ntimes):
            deltaTrow = ((self.t_series[i]-self.t_series[i-1]).days/365)*ones
            deltaT = np.vstack ((deltaT,deltaTrow))
        self.cashFlows= self.coupon*deltaT
        principal = ones
        self.cashFlows[self.ntimes-1,:] += principal
        pv = self.cashFlows*self.libor*self.survival
        defaultPayment = np.zeros(np.shape(self.libor))
        defaultPayment[1,:] = (self.survival[0] - self.survival[1])*self.libor[1,:]*self.recovery
        pv[1,:] = pv[1,:] + defaultPayment [1,:]
        for i in range(2, np.shape(self.survival)[0]):
            pv[i,:] = pv[i,:]+(self.survival[i-1]-self.survival[i])*self.libor[i,:]*self.recovery
        self.pvAvg = np.average(pv,axis=1)
        return self.pvAvg
    # the present value of riskless bond
    def riskless(self):
        deltaT= np.zeros(self.ntrajectories)
        ones = np.ones(shape=[self.ntrajectories])
        for i in range(1,self.ntimes):
            deltaTrow = ((self.t_series[i]-self.t_series[i-1]).days/365)*ones
            deltaT = np.vstack ((deltaT,deltaTrow))
        self.cashFlows= self.coupon*deltaT
        principal = ones
        self.cashFlows[self.ntimes-1,:] += principal
        pvRiskless = self.cashFlows*self.libor
        self.pvAvgRiskless=np.average(pvRiskless,axis=1)
        return self.pvAvgRiskless