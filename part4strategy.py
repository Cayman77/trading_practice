#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  2 17:11:25 2017

@author: sunkaiman
"""

import pandas as pd
import matplotlib.pyplot as plt


## load data from csv - LUV        
luvdf = pd.read_csv('LUV.csv',index_col='Date',parse_dates = True)

# calc r,ma
data = pd.DataFrame(columns = ['Price','DailyReturn','MA5','MA25'])
data['Price'] = luvdf['Adj Close']
data['DailyReturn'] = data['Price'].pct_change()
data['MA5'] = data['Price'].rolling(window = 5).mean()
data['MA25'] = data['Price'].rolling(window = 25).mean()
temp = pd.DataFrame({'MA5':data['MA5'],'MA25':data['MA25'],'P':data['Price']})
plt.figure(1)
temp.plot(figsize=(10,10))


# signal
Signal = []
for i in range(len(data)):
    if data['MA5'][i]>data['MA25'][i]:
        signal = 1
    elif data['MA5'][i]<data['MA25'][i]:
        signal = -1
    else:
        signal = None
    Signal.append(signal)
data['Signal'] = Signal

# calc pnl..I don't think calculating pnl in this way is right. Shouldn't we consider a security line and a cash line?
## I have some further assumptions in detail, say, can only long and pnl means realized pnl
position = 0
cost = 0
PNL = [0]
for i in range(1,len(data)):
    if data['Signal'][i]==1 and position == 0:
        cost = data['Price'][i]
        pnl = PNL[i-1]
        position = 1
    elif data['Signal'][i]==-1 and position == 1:
        pnl = PNL[i-1]+data['Price'][i]-cost
        position = 0
    else:
        pnl = PNL[i-1]
    PNL.append(pnl)
data['PNL'] = PNL

# improve
## since Luv follows the trend of the industry with a lag. I can use both the cross signal of the industry
## and the cross signal of Luv to set my buy signal of LUV. In this way, I can avoid unfavourable trend。

# call trading strategy
import strategy as st

ts1 = st.trading_strategy()
for price in luvdf['Adj Close'].iteritems():
    ts1.process_tick(price)

ts1.display_pnl() 


