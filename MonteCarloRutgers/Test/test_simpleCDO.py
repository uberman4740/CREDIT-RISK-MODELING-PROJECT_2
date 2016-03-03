__author__ = 'Yule Jin'
from pandas import DataFrame
from pandas import Series
from Quandl import Quandl
import numpy as np
import datetime
from dateutil.relativedelta import relativedelta
from Curves.Corporates.CorporateDaily import CorporateRates
import pandas as pd
from Curves.OIS.OISDaily import OIS
import matplotlib.pyplot as plt
from Products.Credit.CDO.SimpleCDO import SimpleCDO
from scipy.stats import norm
from  MonteCarloSimulators.Vasicek.vasicekMCSim import MC_Vasicek_Sim

rho = 0.9
simNumber = 1000
numNames = 100
probability = 0.04
tranches = [0,0.03,0.07,0.5,1.0]
R = 0.4
r = 0.04

QP = pd.DataFrame(np.ones([100, 1]))
QP.loc[:,0] = 0.90
#QP = np.zeros((100,1))
#QP[:,0]=0.95
Beta = 0.2

myCDO = SimpleCDO(probability=probability, rho=rho, simNumber=simNumber, numNames=numNames, Q=QP, beta=Beta)
variate = myCDO.getVariate()
trancheFraction = myCDO.getFractionOfTranchesDefaulted(Tranches=tranches,R=R,r=r)
#SurvivalProb = myCDO.getQTranche(0.07,0.5)
#print("Q= ", SurvivalProb)
print("trancheFraction = ", trancheFraction)
#yy = SimpleCDO.getVariate()
# start=datetime.datetime(2005,1,10)
# end=datetime.datetime(2010,1,10)
# test_current_day=datetime.datetime(2009,3,5)
# test_end_day=datetime.datetime(2037,9,10)
# start_temp=start
# end_temp=start_temp+relativedelta(years=30)
# trim_start="2005-01-10"
# trim_end="2010-01-10"
