__author__ = 'Yule Jin'
from pandas import DataFrame
from pandas import Series
import numpy as np
import pandas as pd


## calculate libor rate and suvival rate's vascicek models
class VasicekAffine:
     def __init__(self, x = None, y= None, datelist = None):
        if x==None and y==None and datelist == None:
            return
        self.datelist = datelist
        self.y = y
        self.x = x
        self.Q = []
        self.r = []
        self.h=0
     ##function used to calculate the survival rate based on Vasicek model
     def calQ(self):
         tenors = self.datelist
         a = self.x[0]
         theta = self.x[1]
         sigma = self.x[2]
         lambda0 = self.x[3]
         time0 = self.datelist[0]
         self.Q = pd.DataFrame(np.ones([1, 1]))
         for k in np.arange(len(tenors)):
             i = (tenors[k]-time0).days/365.0
             B = 1/a * (1-np.exp(-a*i))
             A = (theta-sigma*sigma/(2*a*a))*(i-B)+ sigma*sigma/(4*a)*B*B
             self.Q.loc[k,:] = np.exp(-A-B*lambda0)
         self.Q.index = tenors
         return self.Q
     ## function used to calculate the interest rate based on Vasicek model
     def calR(self):
         tenors = self.datelist
         kappa = self.y[0]
         mu = self.y[1]
         sigmaR = self.y[2]
         lambdaR0 = self.y[3]
         time0 = self.datelist[0]
         length = len(tenors)
         #self.r = pd.DataFrame(np.ones([1,1]))
         self.r=np.zeros(np.shape(tenors))
         for self.h in range(0,length-1):
             j = (tenors[self.h]-time0).days/365.0
             B_r = 1/kappa * (1-np.exp(-kappa*j))
             A_r = (mu - sigmaR*sigmaR/(2*kappa*kappa))*(j-B_r) + sigmaR*sigmaR/(4*kappa)*B_r*B_r
             #self.r.loc[h,:] = np.exp(-A_r-B_r*lambdaR0)
             self.r[self.h]=(np.exp(-A_r-B_r*lambdaR0))
         #self.r.index = tenors
         return self.r
