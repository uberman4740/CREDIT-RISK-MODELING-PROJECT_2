__author__ = 'Yule Jin'
import numpy as np
import pandas as pd
from scipy.stats import norm
from statsmodels.sandbox.distributions.extras import mvstdnormcdf
import matplotlib.pyplot as plt

class SimpleCDO(object):
    def __init__(self, probability, rho, simNumber, numNames, Q, beta):
        self.rho = rho
        self.simNumber = simNumber
        self.probability = probability
        self.numNames = numNames
        self.results = []
        self.getVariate()
        self.Q = Q
        self.beta = beta
        self.QTranche = []

    def getVariate(self):
        rd = np.random.standard_normal((self.numNames,self.simNumber))
        systemicVar = np.tile(np.random.standard_normal([self.numNames,1]),[1,self.simNumber])
        self.rndSpace = self.rho * systemicVar + np.sqrt(1-self.rho*self.rho)*rd
        defaultBarrier = norm.ppf(self.probability)
        self.rndSpace = self.rndSpace > defaultBarrier

    def getFractionOfTranchesDefaulted(self,Tranches, R, r):
        self.R = R
        self.r = r
        self.Tranches = pd.DataFrame(Tranches)*100
        self.results = (self.numNames - self.rndSpace.sum(axis=0))*(1.0-self.R)
        lower = self.Tranches.values[0]
        trancheFranction = {}
        for i in self.Tranches.values[1:]:
            trancheFranction[i[0]] = self.gettrancheFraction(lower,i)
        return trancheFranction

    def gettrancheFraction(self,lower,upper):
        discount = np.exp(-self.r * 1)
        trancheFractionInBetween=[]
        [trancheFractionInBetween.append(x) for x in self.results if (x > lower and x < upper)]
        a = (pd.DataFrame(trancheFractionInBetween)-lower)/(upper - lower)
        b = pd.DataFrame([x for x in self.results if x > upper])
        tranchefraction = (len(a)*np.mean(a)+len(b))/self.simNumber*discount
        return tranchefraction[0]

    def getQTranche(self, K1, K2):
        self.K1 = K1
        self.K2 = K2
        #CT = norm.ppf((1.0 - self.Q))
        CT = (1.0 - self.Q).apply(norm.ppf)
        # K1 Calculation
        AA = lambda x: (CT - np.sqrt(1 - self.beta ** 2) * norm.ppf(x/(1-self.R))) / self.beta
        # MVN Calculation
        mvn1 = pd.DataFrame(index=CT.index, columns=CT.columns)
        mvn2 = pd.DataFrame(index=CT.index, columns=CT.columns)
        AAK1 = AA(K1)
        AAK2 = AA(K2)
        for t in CT.index:
            for sim in CT.columns:
                mvn1.loc[t, sim] = mvstdnormcdf(lower=[-np.inf, -np.inf], upper=[CT.loc[t, sim], -AAK1.loc[t, sim]],
                                            corrcoef=-self.beta)
                mvn2.loc[t, sim] = mvstdnormcdf(lower=[-np.inf, -np.inf], upper=[CT.loc[t, sim], -AAK2.loc[t, sim]],
                                            corrcoef=-self.beta)
        EminK1 = pd.DataFrame(K1*norm.cdf(AAK1), index=self.Q.index, columns=self.Q.columns) + (1-self.R)*mvn1
        EminK1.fillna(value=0, inplace=True)
        EminK2 = pd.DataFrame(K2*norm.cdf(AAK2), index=self.Q.index, columns=self.Q.columns) + (1-self.R)*mvn2
        self.QTranche = 1.0 - (EminK2 - EminK1) / (K2 - K1)
        self.QTranche.fillna(1, inplace=True)
        self.QTranche[self.QTranche>1.0]=1.0
        return self.QTranche


