__author__ = 'Yule Jin'
from Quandl import Quandl
import pandas as pd
from Curves.OIS.OISDaily import OIS
import numpy as np
import pickle
import datetime
from functools import reduce
from dateutil.relativedelta import relativedelta

class CorporateRates(object):
    def __init__(self):
        self.dates = []
        self.OIS = OIS()
        self.corporates = []
        self.ratings = ['AAA', 'AA']
        self.corpSpreads = {}
        self.corporates = pd.DataFrame()
        self.corporates_full={}

    def getCorporates(self, trim_start, trim_end, WORKING_DIR='.'):
        self.OIS = OIS(trim_start=trim_start, trim_end=trim_end,WORKING_DIR=WORKING_DIR)
        self.datesAll = self.OIS.datesAll
        self.OISData = self.OIS.getOIS()
        self.WORKING_DIR = WORKING_DIR
        for rating in self.ratings:
            index = 'ML/' + rating + 'TRI'
            try:
                corpSpreads =1e-4* ( Quandl.get(index, authtoken="Lqsxas8ieaKqpztgYHxk", trim_start=trim_start, trim_end=trim_end) )
                corpSpreads.reset_index(level=0, inplace=True)
                corpSpreads = pd.merge(left=self.datesAll, right= corpSpreads,how='left')
                corpSpreads = corpSpreads.fillna(method='ffill').fillna(method='bfill')
                self.corpSpreads[rating] = corpSpreads.T.fillna(method='ffill').fillna(method='bfill').T
            except:
                print(index, " not found")
        self.corpSpreads = pd.Panel.from_dict(self.corpSpreads)
        self.corporates = {}
        self.OISData.drop('Date', axis=1, inplace=True)
        ntenors = np.shape(self.OISData)[1]
        for rating in self.ratings:
            try:
                tiledCorps = np.tile(self.corpSpreads[rating]['Value'],ntenors)
                tiledCorps=tiledCorps.reshape(np.shape(self.OISData),order="F")
                self.corporates[rating] = pd.DataFrame(data = (tiledCorps + self.OISData.values))
                self.corporates[rating].drop(self.corporates[rating].columns[[0]], axis=1, inplace=True)
            except:
                print("Error in addition of Corp Spreads")
        self.corporates = pd.Panel(self.corporates)
        return self.corporates

    def interpolation_corporates(self):
        start=datetime.datetime(2005,1,10)
        end=datetime.datetime(2010,1,10)
        try:
            row_days=(end-start).days+1
        except:
            print("error: may be end day is earlier than start day")
        ndate=[29,89,179,364,729,1094,1824,2554,3649,7329,10949]
        for rating in self.ratings:
            temp_dict={}
            start=datetime.datetime(2005,1,10)
            for i in range(0,row_days):
                vdate=pd.DataFrame(self.corporates[rating].iloc[i,0:11]).values.tolist()
                vdate=reduce(lambda x,y: x+y,vdate)
                end=start+relativedelta(years=30)
                ndays=(end-start).days
                d_series=np.arange(0,ndays,1)
                temp_dict[start]=np.interp(d_series, ndate, vdate)
                start=start+datetime.timedelta(days=1)
            self.corporates_full[rating]=temp_dict
        h = self.corporates_full['AAA']
        end_temp=datetime.datetime(2008,1,10)
        g = h[end_temp][7]
        # self.corporates_full=pd.Panel.from_dict(self.corporates_full)
        return self.corporates_full


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

if (__name__=="__main__"):
#CashFlow Dates
    WORKING_DIR = '.'
    trim_start="2005-01-10"
    trim_end="2005-02-10"
    WORKING_DIR='.'
    myCorp = CorporateRates()
    myCorpRates = myCorp.getCorporates(trim_start=trim_start, trim_end=trim_end, WORKING_DIR=WORKING_DIR)
    myCorp.pickleMe('./myCorp')
    a=1