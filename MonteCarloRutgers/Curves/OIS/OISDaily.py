__author__ = 'Yule Jin'
from Quandl import Quandl
import pandas as pd
import numpy as np
import pickle
import os
import datetime
from dateutil.relativedelta import relativedelta
from functools import reduce

class OIS(object):
    def __init__(self, trim_start="2005-01-10", trim_end="2010-01-10",WORKING_DIR='.'):
        self.OIS = 0.01*Quandl.get("USTREASURY/YIELD", authtoken="Lqsxas8ieaKqpztgYHxk", trim_start=trim_start, trim_end=trim_end)
        self.OIS.reset_index(level=0, inplace=True)
        self.datesAll = pd.DataFrame(pd.date_range(trim_start,trim_end), columns=['Date'])
        self.datesAll.reset_index(level=0, inplace=True)
        self.OIS = pd.merge(left=self.datesAll, right=self.OIS,how='left')
        self.OIS = self.OIS.fillna(method='ffill').fillna(method='bfill')
        self.OIS = self.OIS.T.fillna(method='ffill').fillna(method='bfill').T # Fill NA forward and backward to eliminate NA
        self.WORKING_DIR = WORKING_DIR
        self.OIS_dict={}
        self.t_step = 1/365.0


    def getOIS(self,datelist=[]):
        if(len(datelist)!=0):
            return self.OIS.iloc[datelist]
        else:
            return self.OIS

    def pickleMe(self,file):
        pickle.dump(self.Data, open(file, "wb"))

    def unPickleMe(self,file):
        if(os.path.exists(file)):
            self.Data = pickle.load(open(file, "rb"))

    def saveMeExcel(self, whichdata, fileName, dir=None):
        df = pd.DataFrame(whichdata)
        if(dir==None):
            fName = os.path.join(self.WORKING_DIR, fileName + '.xlsx')
        else:
            fName = os.path.join(dir, fileName + '.xlsx')
        df.to_excel(fName, sheet_name=fileName, index=False)

    def printois(self):
        print(self.OIS.iloc[0])


    #This interpolationois member function can interpolate 1,3,6,12... months to 30 years' OIS rate so that I can get certain
    #point's value
    def interpolationois(self):
        start=datetime.datetime(2005,1,10)
        start2 = start+datetime.timedelta(days=1)
        end=datetime.datetime(2010,1,10)
        try:
            row_days=(end-start).days+1
        except:
            print("error: may be end day is earlier than start day")
        ndate=[29,89,179,364,729,1094,1824,2554,3649,7329,10949]
        for i in range(0,row_days):
            vdate=pd.DataFrame(self.OIS.iloc[i,2:13]).values.tolist()
            vdate=reduce(lambda x,y: x+y,vdate) # break list of list into one list
            end=start+relativedelta(years=30)
            ndays=(end-start).days
            d_series=np.arange(0,ndays,1)
            self.OIS_dict[start]=np.interp(d_series, ndate, vdate)
            start=start+datetime.timedelta(days=1)
        integralR = self.OIS_dict[start2].cumsum(axis=0)*self.t_step
        return np.exp(-integralR)
    ## get OIS daily rate from OIS class
    def get_OIS_daily(self,current_date,end_date):
        n_days=(end_date-current_date).days
        if n_days<0:
            print("Dear user, the date of OIS you are looking for should be later than the time now ~~ ")
            print("Please check carefully ")
        else:
            return self.OIS_dict[current_date][n_days]

if (__name__=="__main__"):
#CashFlow Dates
    WORKING_DIR = '.'
    myOIS = OIS()
    datelist = np.arange(0,1827)
    ZOIS = myOIS.getOIS(datelist)
    myOIS.saveMeExcel(whichdata=ZOIS, fileName='OIS',dir=WORKING_DIR)
    a=1