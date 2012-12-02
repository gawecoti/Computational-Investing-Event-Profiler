# -*- coding: utf-8 -*-
"""
Created on Thu Nov 22 22:07:02 2012

@author: Timothy
"""

import pandas
from qstkutil import DataAccess as da
import numpy as np
import math 
import copy 
import qstkutil.qsdateutil as du
import datetime as dt
import qstkutil.DataAccess as da
import qstkutil.tsutil as tsu
import qstkstudy.EventProfiler as ep

storename = "Yahoo"
closefield = "actual_close"
volumefield = "volume"
window = 10
dataobj = da.DataAccess('Yahoo')

def findEvents(symbols,startday,endday,marketSymbol,verbose = False):
    
    timeofday = dt.timedelta(hours = 16)
    timestamps = du.getNYSEdays(startday,endday,timeofday)
  
    if verbose: 
        print  __name__ + " reading data"
    
    close = dataobj.get_data(timestamps,symbols,closefield)
    close = (close.fillna(method="ffill")).fillna(method="backfill")
    
    np_eventmat = copy.deepcopy(close)
    for sym in symbols:
        for time in timestamps:
            np_eventmat[sym][time] = np.NAN
            
    if verbose:
        print __name__ + " finding events"
    
    price = 7.0     
    for symbol in symbols:
        for i in range(1,len(close[symbol])):
            if close[symbol][i-1] >= price and close[symbol][i] < price:
                np_eventmat[symbol][i] = 1.0
    
    return np_eventmat
            

#################################################
################ MAIN CODE ######################
#################################################

symbols = dataobj.get_symbols_from_list("sp5002012")
symbols.append('SPY')

startday = dt.datetime(2008,1,1)
endday = dt.datetime(2009,12,31)
eventMatrix = findEvents(symbols,startday,endday,marketSymbol='SPY',verbose=True)

eventProfiler = ep.EventProfiler(eventMatrix,startday,endday,lookback_days=20,lookforward_days=20,verbose=True)

eventProfiler.study(filename="EventStudyHomework2.pdf",plotErrorBars=True,plotMarketNeutral=True,plotEvents=False,marketSymbol='SPY')



        
    