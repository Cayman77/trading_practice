#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 30 22:09:56 2017

@author: sunkaiman
"""
import pandas as pd
import pandas_datareader.data as pdr
import fix_yahoo_finance as yf
import quandl
import matplotlib.pyplot as plt
import statsmodels.api as sm

# 1.get data
yf.pdr_override()
## fetch data from yahoo - airline industry
start = '2014-06-01'
end = '2016-06-13'
symbol = ['AAL', 'ALK', 'AVH', 'CEA', 'ZNH', 'VLRS', 'CPA', 'DAL', 'GOL', 'LTM',
          'UAL']
all_data = {}
for ticker in symbol:
    all_data[ticker] = pdr.get_data_yahoo(ticker,start,end)
    
## fetch data from quandl - WTI spot price
WTI_spot = quandl.get("EIA/PET_RWTC_D", start_date="2014-06-01", end_date="2016-06-13")
WTI_R = WTI_spot.pct_change()[1:]

## load data from csv - LUV        
luvdf = pd.read_csv('LUV.csv',index_col='Date',parse_dates = True)

# 2.deal with data
## add LUV to all_data
all_data['LUV'] = luvdf['2014-06-02':'2016-06-13']
## create dataframe price
price = pd.DataFrame()
for i in all_data.keys():
   price[i] = all_data[i]['Adj Close']
## create dataframe volume
volume = pd.DataFrame()
for i in all_data.keys():
   volume[i] = all_data[i]['Volume']
## calc daily return
daily_return = price.pct_change()[1:]
daily_return2 = (price/price.shift(1)-1)[1:]

# 3.analysis
## scatter plot between return and volume
plt.figure(1)
plt.scatter(daily_return['AAL'],volume['AAL'][1:])
plt.xlabel('AAL daily return')
plt.ylabel('AAL volumn')
plt.show()

plt.figure(2)
plt.scatter(daily_return['LUV'],volume['LUV'][1:])
plt.xlabel('LUV daily return')
plt.ylabel('LUV volumn')
plt.show()

## print pair-correlation, graphic between correlation of all symbols
print(daily_return.corr(method='pearson'))
plt.figure(3)
pd.plotting.scatter_matrix(daily_return,figsize=(20, 20))
plt.title('correlation of symbols')
plt.show()

## calc MA5
for i in all_data.keys():
    all_data[i]['MovingAverage'] = price[i].rolling(window=5).mean()

## dataframe noluv, onlyluv, tt=aggregation of the two and plot
noluv = daily_return.drop(columns=['LUV']).mean(axis=1)
onlyluv = daily_return['LUV']
tt=pd.DataFrame({'No.LUV':noluv,'LUV':onlyluv})
plt.figure(4)
tt.plot()
plt.show()

## MA return shows a lag of LUV
plt.figure(5)
pd.rolling_mean(tt,10).plot(title = 'window = {} days'.format(10))
plt.show()

## expected return - risk plot
ER = daily_return.mean()
Risk = daily_return.std()
### add labels
temp = {}
temp['ER'] = ER.values
temp['Risk'] = Risk.values
temp['label'] = ER.keys()
plt.figure(6)
plt.scatter(temp['ER'],temp['Risk'])
plt.xlabel('Expected Return')
plt.ylabel('Risk')
for label, x, y in zip(temp['label'],temp['ER'],temp['Risk']):
    plt.annotate(
        label,
        xy=(x,y), xytext=(-20, 20),
        textcoords='offset points', ha='right', va='bottom',
        bbox = dict(boxstyle='round,pad=0.5', fc='blue', alpha=0.5),
        arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0')
            )
plt.show()

## scatter plot
avg_dailyR = daily_return.mean(axis=1)
ll=avg_dailyR.to_frame().join(WTI_spot,how='inner')
ss=avg_dailyR.to_frame().join(WTI_R,how='inner')
plt.figure(7)
plt.scatter(ll[0],ll['Value'])
plt.xlabel('airline industry average daily return')
plt.ylabel('WTI spot price')
plt.show()

plt.figure(8)
plt.scatter(ss[0],ss['Value'])
plt.xlabel('airline industry average daily return')
plt.ylabel('WTI daily return')
plt.show()

## Fit regression model
ss=ss.rename(index=str, columns={0:'airline industry average return','Value':'WTI return'})
Y=ss['airline industry average return']
X=ss['WTI return']
X=sm.add_constant(X)
lm = sm.OLS(Y,X).fit()
print(lm.params)
## plot
y_hat = lm.predict(X)
### plot the regression line, colored in red
plt.figure(9)
plt.plot(X['WTI return'],y_hat, 'r')
### plot the raw data
plt.scatter(X['WTI return'],Y)
plt.ylabel('airline industry average daily return')
plt.xlabel('WTI daily return')
plt.show()
