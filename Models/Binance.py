#collects data via Binance Api
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

btc_price = {'error':False}

def btc_trade_history(msg):
    ''' define how to process incoming Websocket messages'''
    if msg['e'] != 'error':
        print(msg['c'])
        btc_price['last'] = msg['c']
        btc_price['bid'] = msg['b']
        btc_price['last'] = msg['a']
    else:
        btc_price['error'] = True


tickers = ['BTCUSDT','ETHUSDT','DOGEUSDT','ADAUSDT','XLMUSDT','XRPUSDT','BNBUSDT','LITUSDT','DOTUSDT',
           'EGLDUSDT','EOSUSDT','LTCUSDT','SXPUSDT','LINKUSDT','BCHUSDT','ATOMUSDT','AAVEUSDT','USDCUSDT',
           'TRXUSDT','UNIUSDT','SUSHIUSDT','EURUSDT','GRTUSDT','1INCHUSDT','AVAXUSDT','ALPHAUSDT','QTUMUSDT',
           'VETUSDT','ZRXUSDT','MANAUSDT','CRVUSDT','ALGOUSDT','LUNAUSDT','XTZUSDT','OMGUSDT','TWTUSDT','ETCUSDT',
           'BTCUPUSDT','ETHUPUSDT','UNFIUSDT','BATUSDT','NEOUSDT','REEFUSDT','XVSUSDT','NEARUSDT','ADAUPUSDT',
           'SNXUSDT','KAVAUSDT','SOLUSDT','FILUSDT','IOSTUSDT','ONTUSDT','IOTAUSDT','HARDUSDT',
           'DASHUSDT','MKRUSDT','CVCUSDT','YFIUSDT','ZECUSDT','MATICUSDT','ICXUSDT','XLMUPUSDT','BTCDOWNUSDT',
           'BALUSDT','THETAUSDT','TOMOUSDT','RENUSDT','DNTUSDT','FTMUSDT','SXPUPUSDT','ZILUSDT','COMPUSDT',
           'YFIIUSDT','XRPUPUSDT','LRCUSDT','BANDUSDT','UMAUSDT','WAVESUSDT','RUNEUSDT','RSRUSDT','EOSUPUSDT','MFTUSDT',
           'ANKRUSDT','TRBUSDT','SRMUSDT','SUNUSDT','OCEANUSDT','XEMUSDT','RIFUSDT','ENJUSDT','AKROUSDT','XMRUSDT','TRUUSDT',
           'HBARUSDT','ETHDOWNUSDT','ADADOWNUSDT','XTZUPUSDT','FLMUSDT','STMXUSDT','SANDUSDT','KNCUSDT',
           'BTTUSDT','CELOUSDT','DOTUPUSDT','BNBDOWNUSDT','TRXUPUSDT','LINKUPUSDT','BELUSDT','FETUSDT',
           'HNTUSDT','SUSHIUPUSDT','RVNUSDT','PNTUSDT','KSMUSDT','INJUSDT','CTKUSDT','AAVEUPUSDT','COTIUSDT',
           'OXTUSDT','SKLUSDT','BZRXUSDT','STXUSDT','CHZUSDT','NANOUSDT','ROSEUSDT','AUDUSDT','FTTUSDT',
           'UNIUPUSDT','FUNUSDT','DIAUSDT','JSTUSDT','NPXSUSDT','ZENUSDT','RLCUSDT','YFIUPUSDT','ANTUSDT',
           'LTCUPUSDT','AXSUSDT','BLZUSDT']


# start the Websocket
bsm = BinanceSocketManager(client)
conn_key = bsm.start_symbol_ticker_socket('BTCUSDT', btc_trade_history)
#bsm.start()

# valid intervals - 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M

# get timestamp of earliest date data is available
#timestamp = client._get_earliest_valid_timestamp('BTCUSDT', '1h')
#print(timestamp)

# request historical candle (or klines) data
#bars = client.get_historical_klines('BTCUSDT', '1h',timestamp ,limit=300)

for x in tickers:
    bars = client.get_historical_klines(x, Client.KLINE_INTERVAL_1HOUR, "300 hours ago UTC")
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



    #"""Calculate On-Balance Volume (OBV)"""

#df['obv'] = btalib.obv(df.close,df.Volume)[-1]
    OBV = []
    OBV.append(0)
    for i in range(1, len(df.close)):
        if df.close.iloc[i] > df.close.iloc[i-1]: #If the closing price is above the prior close price
            OBV.append(OBV[-1] + df.Volume.iloc[i]) #then: Current OBV = Previous OBV + Current Volume
        elif df.close.iloc[i] < df.close.iloc[i-1]:
          OBV.append( OBV[-1] - df.Volume.iloc[i])
        else:
          OBV.append(OBV[-1])

    df['OBV'] = OBV
    df['OBV_EMA'] = df['OBV'].ewm(com=20).mean()
    df['OBV_pc'] = df['OBV'].pct_change() * 100
    df['OBV_pc'] = np.round(df['OBV_pc'].fillna(0),2)

#true if EMA12 is above the EMA26
    df['ema12gtema26'] = df['ema12'] > df['ema26']
# true if the current frame is where EMA12 crosses over above
    df['ema12gtema26co'] = df['ema12gtema26'].ne(df['ema12gtema26'].shift())
    df.loc[df['ema12gtema26']== False, 'ema12gtema26co'] = False

#true if ema12 is below the ema26
    df['ema12ltema26'] = df['ema12'] < df['ema26']
#true if the current frame is where ema12 crosses over below
    df['ema12ltema26co'] = df['ema12ltema26'].ne(df['ema12ltema26'].shift())
    df.loc[df['ema12ltema26']== False, 'ema12ltema26co'] = False

#true if MACD is above signal
    df['macdgtsignal'] = df['macd'] > df['signal']

#true if the current frame is where macd crosses over above
    df['macdgtsignalco'] = df['macdgtsignal'].ne(df['macdgtsignal'].shift())
    df.loc[df['macdgtsignal'] == False, 'macdgtsignalco'] = False

#true if the macd is below the signal
    df['macdltsignal'] = df['macd'] < df['signal']

#true if the current frame is where macd crosses over below
    df['macdltsignalco'] = df['macdltsignal'].ne(df['macdltsignal'].shift())
    df.loc[df['macdltsignal'] == False, 'macdltsignalco'] = False

    df_last = df.tail(1)

    ema12gtema26 = bool(df_last['ema12gtema26'].values[0])
    ema12gtema26co = bool(df_last['ema12gtema26co'].values[0])
    macdgtsignal = bool(df_last['macdgtsignal'].values[0])
    macdgtsignalco = bool(df_last['macdgtsignalco'].values[0])
    ema12ltema26 = bool(df_last['ema12ltema26'].values[0])
    ema12ltema26co = bool(df_last['ema12ltema26co'].values[0])
    macdltsignal = bool(df_last['macdltsignal'].values[0])
    macdltsignalco = bool(df_last['macdltsignalco'].values[0])
    obv = float(df_last['OBV'].values[0])
    obv_pc = float(df_last['OBV_pc'].values[0])
    print(x)
    if ((ema12gtema26co == True and macdgtsignal == True and obv_pc > 0.1)):
        action = 'BUY'
# criteria for a sell signal
    elif (ema12ltema26co == True and macdltsignal == True):
        action = 'SELL'
# anything other than a buy or sell, just wait
    else:
        action = 'WAIT'
#print(df)
    print(action)
    if action == 'BUY':
        break
    if action =='Buy':
        buy_order = client.create_test_order(symbol='ETHUSDT', side='BUY', type='MARKET', quantity=100)
        print(buy_order)

#export DataFrome to csf
df.to_csv('btc_bars3.csv')








