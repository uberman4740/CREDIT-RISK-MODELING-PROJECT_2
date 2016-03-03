__author__ = 'Yule Jin'
import datetime

import numpy as np

from MonteCarloSimulators.Vasicek.VasicekAffine import VasicekAffine
from Products.Credit.CDS.CDS import CDS
from Products.Rates.Bond.Bond import bond

#CashFlow Dates
x = [0.1,0.005,0.03,0.03]
y = [3,0.05,0.09,0.08]
#t_series = np.round(np.arange(0,1.001,0.25)*365)
t_series = np.round(np.arange(0,365.001*30+6.001,1))
start=datetime.datetime(2005,1,10)
base = datetime.datetime.today()
datelist = [start + datetime.timedelta(days=x) for x in t_series]
datelist = [x.date() for x in datelist]

Affine = VasicekAffine(x, y, datelist)
#print("Q is ", Affine.calQ())
print("r is ", Affine.calR())
QQ=Affine.calQ().values

VBond = bond(Affine.calR().values,0.08,datelist,Affine.calQ().values, 0.4)
VCDS = CDS(Affine.calR().values, datelist, Affine.calQ().values, 0.4)
print('Risky Bond Price = ', str(1000*VBond.pv().sum()))
print('Riskless Bond Price = ', str(1000*VBond.riskless().sum() ))
print ('5 years Par Spread for each quarter= ', str(VCDS.parSpread()))
print ('5 years Mark to Market Value for each quarter = ', VCDS.MTM())
