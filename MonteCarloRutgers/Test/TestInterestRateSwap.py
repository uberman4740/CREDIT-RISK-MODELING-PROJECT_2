import datetime

import numpy as np

from  MonteCarloSimulators.Vasicek.vasicekMCSim import MC_Vasicek_Sim
from  Products.Rates.IRS.IRS import IRS
from Products.Credit.CDS.CDS import CDS
from Products.Rates.Bond.Bond import bond

#CashFlow Dates
t_series = np.round(np.arange(0,1.001,0.25)*365)
base = datetime.datetime.today()
datelist = [base + datetime.timedelta(days=x) for x in t_series]
datelist = [x.date() for x in datelist]
#SDE parameter
t_step = 1.0/365
r0 = 0.08
sigmaR = 0.09
sigmaRef = 0.03
muR = 0.05
alphaR=3.0
simNumber=1000
muHazardRate = 0.005
k = 0.1
recovery = 0.4
FixedRate = 0.055

#Bond parameters
coupon = 0.08

#Monte Carlo trajectories creation
t1 = datetime.datetime.now()
myVasicek = MC_Vasicek_Sim(datelist, r0,sigmaR, sigmaRef, muR, muHazardRate,alphaR, k, simNumber,t_step)
longLibor = myVasicek.getLibor()
longInterestRate = myVasicek.getInterestRate()
smallInterestRate = myVasicek.getSmallInterestRate()
longsurvival = myVasicek.getSurvival()
survival = myVasicek.getSmallSurvival()
#myVasicek.saveMeExcel()

#Bond Pricing

myIRS = IRS(smallInterestRate,FixedRate)

print('Interest Rate Swap = ', myIRS.MTM())
