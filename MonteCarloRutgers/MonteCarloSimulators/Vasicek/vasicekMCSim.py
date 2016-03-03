__author__ = 'Yule Jin'
from pandas import DataFrame
from pandas import Series
import numpy as np
import pandas as pd

##simulate libor rate and survival  rate
class MC_Vasicek_Sim:
    def __init__(self, datelist,r0,sigmaR, sigmaRef, muR, muHazardRate, alphaR, k, simNumber,t_step):
    #SDE parameters - Vasicek SDE
        self.sigmaR = sigmaR
        self.sigmaRef = sigmaRef
        self.muR = muR
        self.alphaR = alphaR
        self.simNumber = simNumber
        self.t_step = t_step
        self.r0 = r0
        self.muHazardRate = muHazardRate
        self.k = k
    #internal representation of times series - integer multiples of t_step
        self.datelist = pd.DataFrame(datelist)
        self.datelist1 = datelist
    #creation of a fine grid for Monte Carlo integration
        #Create fine date grid for SDE integration
        minDay = min(datelist)
        maxDay = max(datelist)
        self.datelistlong = pd.date_range(minDay, maxDay).tolist()
        self.datelistlong = [x.date() for x in self.datelistlong]
        self.ntimes = len(self.datelistlong)
        self.libor = []
        self.smallLibor = []
        self.survival = []
        self.smallSurvival = []
        self.interestRate = []

    def getLibor(self):
        rd = np.random.standard_normal((self.ntimes,self.simNumber))   # array of numbers for the number of samples
        r = np.zeros(np.shape(rd))
        nrows = np.shape(rd)[0]
        sigmaDT = self.sigmaR* np.sqrt(self.t_step)
    #calculate r(t)
        r[1,:] = self.r0
        for i in np.arange(2,nrows):
            r[i,:] = r[i-1,:]+ self.alphaR*(self.muR-r[i-1,:])*self.t_step + sigmaDT*rd[i,:]
        r[r<0.0] = 0.0
    #calculate integral(r(s)ds)
        integralR = r.cumsum(axis=0)*self.t_step
    #calculate Libor
        self.libor = np.exp(-integralR)
        return self.libor

    def getInterestRate(self):
        rd = np.random.standard_normal((self.ntimes,self.simNumber))   # array of numbers for the number of samples
        r = np.zeros(np.shape(rd))
        nrows = np.shape(rd)[0]
        sigmaDT = self.sigmaR*np.sqrt(self.t_step)# transfer the year sigma into daily sigma
    #calculate r(t)
        r[1,:] = self.r0
        for i in np.arange(2,nrows):
            r[i,:] = r[i-1,:]+ self.alphaR*(self.muR-r[i-1,:])*self.t_step + sigmaDT*rd[i,:]
        r[r<0.0] = 0.0
    #calculate integral(r(s)ds)
        self.interestRate = r
    #calculate Libor
        return self.interestRate

    def getSurvival(self):
        rr = np.random.standard_normal((self.ntimes,self.simNumber))   # array of numbers for the number of samples
        hazardRate = np.zeros(np.shape(rr))
        nrows = np.shape(rr)[0]
        sigmaDD = self.sigmaRef* np.sqrt(self.t_step)
    #calculate hazardRate
        hazardRate[1,:] = 0.07998644
        for i in np.arange(2,nrows):
            hazardRate[i,:] = hazardRate[i-1,:]+ self.k*(self.muHazardRate-hazardRate[i-1,:])*self.t_step + sigmaDD*rr[i,:]
        hazardRate[hazardRate<0.0]=0.0
    #calculate integral(r(s)ds)
        integralSurvival = hazardRate.cumsum(axis=0)*self.t_step
    #calculate Libor
        self.survival = np.exp(-integralSurvival)
        return self.survival
    ##to get libor
    def getSmallLibor(self):
        #calculate indexes
        ind = self.return_indices1_of_a(self.datelistlong, self.datelist1)
        self.smallLibor = np.vstack(self.libor[ind,:])
        return self.smallLibor

    def getSmallInterestRate(self):
        #calculate indexes
        ind = self.return_indices1_of_a(self.datelistlong, self.datelist1)
        self.smallInterestRate = np.vstack(self.interestRate[ind,:])
        return self.smallInterestRate

    def getSmallSurvival(self):
        ind = self.return_indices1_of_a(self.datelistlong, self.datelist1)
        self.smallSurvival = np.vstack(self.survival[ind,:])
        return self.smallSurvival

    def saveMeExcel(self):
        df = DataFrame(self.libor)
        df.to_excel('/Users/Yule/Desktop/LiborVasicek',sheet_name='libor',index=False)


    def return_indices1_of_a(self, a, b):
        b_set = set(b)
        ind = [i for i, v in enumerate(a) if v in b_set]
        return ind

    def return_indices2_of_a(self, a, b):
        index=[]
        for item in a:
            index.append(np.bisect.bisect(b,item))
        return np.unique(index).tolist()








