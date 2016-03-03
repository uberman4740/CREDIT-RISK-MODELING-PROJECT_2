import datetime

import numpy as np

from  MonteCarloSimulators.Vasicek.vasicekMCSim import MC_Vasicek_Sim
from  Products.Rates.IRS.IRS import IRS
from Products.Credit.CDS.CDS import CDS
from Products.Rates.Bond.Bond import bond
from Portfolio.CVA.CVA import CVA

#CashFlow Dates
t_series = np.round(np.arange(0,1.001,0.25/8)*365*8)
base = datetime.datetime.today()
datelist = [base + datetime.timedelta(days=x) for x in t_series]
datelist = [x.date() for x in datelist]

#SDE Calibrated parameter
t_step = 1.0/365
r0 = 0.02534056
sigmaR = 0.00971563
sigmaRef = 0.04994759
muR = 0.05098966
alphaR= 0.13351371
simNumber=1000
muHazardRate = 0.05002043
k = 3.00005858
recovery = 0.4
FixedRate = 0.05098966

#Bond parameters
coupon = 0.08

#Monte Carlo trajectories creation
t1 = datetime.datetime.now()
myVasicek = MC_Vasicek_Sim(datelist, r0,sigmaR, sigmaRef, muR, muHazardRate,alphaR, k, simNumber,t_step)
longLibor = myVasicek.getLibor()
longInterestRate = myVasicek.getInterestRate()
smallInterestRate = myVasicek.getSmallInterestRate()
libor = myVasicek.getSmallLibor()
longsurvival = myVasicek.getSurvival()
survival = myVasicek.getSmallSurvival()

#products
myBond = bond(libor,coupon,datelist,survival, recovery)
myCDS = CDS(libor, datelist, survival, recovery)
myIRS = IRS(smallInterestRate,FixedRate)

print('8 YEARS Risky Bond Price = ', str(myBond.pv().sum()))
print ('8 YEARS Par Spread of CDS for each quarter= ', str(myCDS.parSpread()))
print ('8 YEARS Mark to Market Value of CDS for each quarter = ', myCDS.MTM())
print ('8 YEARS interest rate swap PV = ', myIRS.MTM())
PV = np.zeros((1,3))
PV[:,0]=myBond.pv().sum()
PV[:,1]=myCDS.getPV()
PV[:,2]=myIRS.MTM()
#PV = [myBond.pv().sum(),myCDS.MTM(),myIRS.MTM()]
print ('Portfolio PV = ', PV)

myCVA = CVA(libor,datelist,survival,recovery,PV)
print ('Portfolio CVA = ', myCVA.calCVA())
#myVasicek.saveMeExcel()