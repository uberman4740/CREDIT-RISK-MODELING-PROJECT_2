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

# a=range(1,5)
# for i in a:
#     print(i)
# print(a)
start=datetime.datetime(2005,1,10)
end=datetime.datetime(2010,1,10)
test_current_day=datetime.datetime(2009,3,5)
test_end_day=datetime.datetime(2037,9,10)
start_temp=start
end_temp=start_temp+relativedelta(years=30)
trim_start="2005-01-10"
trim_end="2010-01-10"
#a=Quandl.get("USTREASURY/YIELD", authtoken="Lqsxas8ieaKqpztgYHxk", trim_start=trim_start, trim_end=trim_end)
#print(a)

testois=OIS()
print('discounted factor',testois.interpolationois())

a=testois.get_OIS_daily(test_current_day,test_end_day)
#print(a)

#test single:24+i to 28+i
# a=testois.interpolationois()
# ndays=(end_temp-start_temp).days
# d_series=np.arange(0,ndays,1)
# plt.plot(d_series,a)
# plt.show()
# a=(end-start).days
# t=[]
# t=np.arange(0,a,1)
# ndate=[29,89,179,364,729,1094,1824,2554,3649,7329,10949]
# print(t)

# start="2005-01-10"
# end="2035-01-10"
#
# d2 = start + relativedelta(years=30)
#
# #datesAll_int = pd.DataFrame(pd.date_range(start,end), columns=['Date'])
# print(start == end)
# a=[1,2,3,4,5]
# b=[3,4]
# c=[4,3,5,9]
# dict={}
# dict[start]=a
# dict[end]=b
# a=(end-start).days
# print(a)

# test coportaterate
# dict={}
# dict1={}
# test=CorporateRates()
# print(test.getCorporates(start,end))
# a=test.interpolation_corporates()
# print(a)
# x = {}
# y = x
# x['key'] = 'value'
# print(y)
#
# x = {}
# print(y)
#
#
# x = {}
# y = x
# y['key'] = 'value'
# print(y)
#
# print(x.clear())
# print(y)



# a=np.transpose([1,2,3])
# b=np.tile(a,4)
# c=np.matrix([[1,2,3],[6,6,6],[5,5,5],[3,3,3]])
# print(c)
# d=np.shape(c)
# print(d)
# e=b.reshape(np.shape(c),order="F")
# print(e)