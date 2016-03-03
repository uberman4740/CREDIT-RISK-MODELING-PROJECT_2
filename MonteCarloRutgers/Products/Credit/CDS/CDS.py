__author__ = 'Yule Jin'
import numpy as np
from pandas import DataFrame

class CDS(object):
    def __init__(self, libor, t_series,survival, recovery):
        self.libor=libor
        self.t_series = t_series
        self.ntimes=len(self.t_series)
        self.ntimes = np.shape(self.libor)[0]
        self.ntrajectories = np.shape(self.libor)[1]
        self.cashFlows = DataFrame()
        self.survival = survival
        self.recovery = recovery
        self.MTMavg = 0.0
        self.parspread = 0.0
        self.CDSPV = []
        return
    ##calculate par spread of CDS
    def parSpread(self):
        deltaT= np.zeros(self.ntrajectories)
        ones = np.ones(shape=[self.ntrajectories])
        for i in range(1,self.ntimes):
            deltaTrow = ((self.t_series[i]-self.t_series[i-1]).days/365)*ones
            deltaT = np.vstack ((deltaT,deltaTrow))
        #self.cashFlows= self.coupon*deltaT
        #principal = ones
        #self.cashFlows[self.ntimes-1,:] += principal
        #protectionLeg = np.zeros(np.shape(self.libor))
        #riskAnnuity = np.zeros(np.shape(self.libor))
        parspread = np.zeros(np.shape(self.libor))
        a = np.shape(self.libor)[1]
        for i in range(np.shape(self.survival)[0],1,-1):
            protectionLeg = np.zeros((i,a))
            riskAnnuity = np.zeros((i,a))
            #parspread= np.zeros((i,a))
            for h in range(1, i):
                riskAnnuity[h,:] = riskAnnuity[h-1,:] + deltaT[h,:]*self.libor[h,:]*self.survival[h,:]
            #for j in range(2, i):
            #    riskAnnuity[j,:] = riskAnnuity[j,:]+riskAnnuity[j-1,:]
            for k in range(1, i):
                protectionLeg[k,:] = protectionLeg[k-1,:]+(self.survival[k-1]-self.survival[k])*self.libor[k,:]*(1-self.recovery)
            #for l in range(2, i):
            #    protectionLeg[l,:] = protectionLeg[l,:]+protectionLeg[l-1,:]
            parspread[(np.shape(self.survival)[0]-i+1),:]=protectionLeg[i-1,:]/riskAnnuity[i-1:]
        #self.par_spread = np.average(parspread,axis=1)
        self.parspread=parspread
        return np.average(parspread,axis=1)
    ##calculate mark to market value of CDS
    def MTM(self):
        MTMvalue = np.zeros(np.shape(self.libor))
        MTMvalue[1,:]=0
        iniSpread = np.zeros(self.ntrajectories)
        iniSpread[:]= self.parspread[1,:]
        deltaT= np.zeros(self.ntrajectories)
        ones = np.ones(shape=[self.ntrajectories])
        for i in range(1,self.ntimes):
            deltaTrow = ((self.t_series[i]-self.t_series[i-1]).days/365)*ones
            deltaT = np.vstack ((deltaT,deltaTrow))
        for i in range(2,np.shape(self.survival)[0]):
            MTMvalue[i,:] = MTMvalue[i-1,:]+(iniSpread-self.parspread[i,:])*deltaT[i,:]*self.libor[i,:]*self.survival[i,:]
        self.MTMavg = np.average(MTMvalue,axis=1)
        self.CDSPV = self.MTMavg[self.ntimes-1]
        return self.MTMavg

    def getPV(self):
        return self.CDSPV