from Models.Account import client
import os
import pandas as pd
import re
import btalib
import numpy as np
from binance.client import Client
from binance.websockets import BinanceSocketManager
import matplotlib.pyplot as plt
from twisted.internet import reactor


bars = client.get_historical_klines('BTCUSDT', Client.KLINE_INTERVAL_1HOUR, "300 hours ago UTC")
for line in bars:
        del line[6:]
#print(bars)
df = pd.DataFrame(bars, columns=['date', 'open', 'high', 'low', 'close', 'Volume'])
df['date'] = pd.to_datetime(df['date'],unit='ms')
df['close'] = df['close'].astype('float64')
df['Volume'] = df['Volume'].astype('float64')

df.set_index('date', inplace=True)
#print(btc_df.head())
#df = pd.read_csv('btc_bars3.csv',parse_dates=True,index_col='date')

#btc_df[]
sma12 = btalib.sma(df.close,period=12)
sma26 = btalib.sma(df.close,period=26)
df['ema12'] = df['close'].ewm(span=12).mean()
df['ema26'] = df['close'].ewm(span=26).mean()
df['macd'] = df['ema12'] - df['ema26']
df['signal'] = df['macd'].ewm(span=9, adjust=False).mean()

OBV = []
OBV.append(0)
for i in range(1, len(df.close)):
    if df.close.iloc[i] > df.close.iloc[i - 1]:  # If the closing price is above the prior close price
        OBV.append(OBV[-1] + df.Volume.iloc[i])  # then: Current OBV = Previous OBV + Current Volume
    elif df.close.iloc[i] < df.close.iloc[i - 1]:
        OBV.append(OBV[-1] - df.Volume.iloc[i])
    else:
        OBV.append(OBV[-1])

df['OBV'] = OBV
df['OBV_EMA'] = df['OBV'].ewm(com=20).mean()
df['OBV_pc'] = df['OBV'].pct_change() * 100
df['OBV_pc'] = np.round(df['OBV_pc'].fillna(0), 2)

# Visually show close, ema12 and ema26
#Create and plot the graph
plt.figure(figsize=(12.2,4.5)) #width = 12.2in, height = 4.5
plt.plot( df['close'],  label='close')#plt.plot( X-Axis , Y-Axis, line_width, alpha_for_blending,  label)
plt.plot( df['ema12'], label='ema12')
plt.plot( df['ema26'], label='ema26')
plt.xticks(rotation=45)
plt.title('close Price History')
plt.xlabel('Date',fontsize=18)
plt.ylabel('Price USD ($)',fontsize=18)
plt.show()


# shows macd and signal
plt.figure(figsize=(12.2,4.5)) #width = 12.2in, height = 4.5
plt.plot( df['macd'],  label='macd')#plt.plot( X-Axis , Y-Axis, line_width, alpha_for_blending,  label)
plt.plot( df['signal'], label='signal')
plt.xticks(rotation=45)
plt.title('close Price History')
plt.xlabel('Date',fontsize=18)
plt.ylabel('Price USD ($)',fontsize=18)
plt.show()


#Create and plot the graph
plt.figure(figsize=(12.2,4.5)) #width = 12.2in, height = 4.5
#plt.plot( df['Close'],  label='Close')#plt.plot( X-Axis , Y-Axis, line_width, alpha_for_blending,  label)
plt.plot( df['OBV'],  label='OBV', color= 'orange')
plt.plot( df['OBV_EMA'],  label='OBV_EMA', color= 'purple')
plt.plot( df['close'],  label='close', color='black')
plt.xticks(rotation=45)
plt.title('OBV/OBV_EMA')
plt.xlabel('Date',fontsize=18)
plt.ylabel('Price USD ($)',fontsize=18)
plt.show()