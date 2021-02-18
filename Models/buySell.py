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
import time


#all coins that can be traded, some will need removing

tickers = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'BCCUSDT', 'NEOUSDT', 'LTCUSDT', 'QTUMUSDT', 'ADAUSDT', 'XRPUSDT', 'EOSUSDT',
           'TUSDUSDT', 'IOTAUSDT', 'XLMUSDT', 'ONTUSDT', 'TRXUSDT', 'ETCUSDT', 'ICXUSDT', 'VENUSDT', 'NULSUSDT', 'VETUSDT',
           'PAXUSDT', 'BCHABCUSDT', 'BCHSVUSDT', 'USDCUSDT', 'LINKUSDT', 'WAVESUSDT', 'BTTUSDT', 'USDSUSDT', 'ONGUSDT',
           'HOTUSDT', 'ZILUSDT', 'ZRXUSDT', 'FETUSDT', 'BATUSDT', 'XMRUSDT', 'ZECUSDT', 'IOSTUSDT', 'CELRUSDT', 'DASHUSDT',
           'NANOUSDT', 'OMGUSDT', 'THETAUSDT', 'ENJUSDT', 'MITHUSDT', 'MATICUSDT', 'ATOMUSDT', 'TFUELUSDT', 'ONEUSDT', 'FTMUSDT',
           'ALGOUSDT', 'USDSBUSDT', 'GTOUSDT', 'ERDUSDT', 'DOGEUSDT', 'DUSKUSDT', 'ANKRUSDT', 'WINUSDT', 'COSUSDT', 'NPXSUSDT', 'COCOSUSDT',
           'MTLUSDT', 'TOMOUSDT', 'PERLUSDT', 'DENTUSDT', 'MFTUSDT', 'KEYUSDT', 'STORMUSDT', 'DOCKUSDT', 'WANUSDT', 'FUNUSDT', 'CVCUSDT', 'CHZUSDT',
           'BANDUSDT', 'BUSDUSDT', 'BEAMUSDT', 'XTZUSDT', 'RENUSDT', 'RVNUSDT', 'HCUSDT', 'HBARUSDT', 'NKNUSDT', 'STXUSDT', 'KAVAUSDT', 'ARPAUSDT',
           'IOTXUSDT', 'RLCUSDT', 'MCOUSDT', 'CTXCUSDT', 'BCHUSDT', 'TROYUSDT', 'VITEUSDT', 'FTTUSDT', 'EURUSDT', 'OGNUSDT', 'DREPUSDT', 'BULLUSDT',
           'BEARUSDT', 'ETHBULLUSDT', 'ETHBEARUSDT', 'TCTUSDT', 'WRXUSDT', 'BTSUSDT', 'LSKUSDT', 'BNTUSDT', 'LTOUSDT', 'EOSBULLUSDT', 'EOSBEARUSDT',
           'XRPBULLUSDT', 'XRPBEARUSDT', 'STRATUSDT', 'AIONUSDT', 'MBLUSDT', 'COTIUSDT', 'BNBBULLUSDT', 'BNBBEARUSDT', 'STPTUSDT', 'WTCUSDT', 'DATAUSDT',
           'XZCUSDT', 'SOLUSDT', 'CTSIUSDT', 'HIVEUSDT', 'CHRUSDT', 'BTCUPUSDT', 'BTCDOWNUSDT', 'GXSUSDT', 'ARDRUSDT', 'LENDUSDT', 'MDTUSDT', 'STMXUSDT',
           'KNCUSDT', 'REPUSDT', 'LRCUSDT', 'PNTUSDT', 'COMPUSDT', 'BKRWUSDT', 'SCUSDT', 'ZENUSDT', 'SNXUSDT', 'ETHUPUSDT', 'ETHDOWNUSDT', 'ADAUPUSDT',
           'ADADOWNUSDT', 'LINKUPUSDT', 'LINKDOWNUSDT', 'VTHOUSDT', 'DGBUSDT', 'GBPUSDT', 'SXPUSDT', 'MKRUSDT', 'DAIUSDT', 'DCRUSDT', 'STORJUSDT',
           'BNBUPUSDT', 'BNBDOWNUSDT', 'XTZUPUSDT', 'XTZDOWNUSDT', 'MANAUSDT', 'AUDUSDT', 'YFIUSDT', 'BALUSDT', 'BLZUSDT', 'IRISUSDT', 'KMDUSDT',
           'JSTUSDT', 'SRMUSDT', 'ANTUSDT', 'CRVUSDT', 'SANDUSDT', 'OCEANUSDT', 'NMRUSDT', 'DOTUSDT', 'LUNAUSDT', 'RSRUSDT', 'PAXGUSDT', 'WNXMUSDT',
           'TRBUSDT', 'BZRXUSDT', 'SUSHIUSDT', 'YFIIUSDT', 'KSMUSDT', 'EGLDUSDT', 'DIAUSDT', 'RUNEUSDT', 'FIOUSDT', 'UMAUSDT', 'EOSUPUSDT', 'EOSDOWNUSDT',
           'TRXUPUSDT', 'TRXDOWNUSDT', 'XRPUPUSDT', 'XRPDOWNUSDT', 'DOTUPUSDT', 'DOTDOWNUSDT', 'BELUSDT', 'WINGUSDT', 'LTCUPUSDT', 'LTCDOWNUSDT', 'UNIUSDT',
           'NBSUSDT', 'OXTUSDT', 'SUNUSDT', 'AVAXUSDT', 'HNTUSDT', 'FLMUSDT', 'UNIUPUSDT', 'UNIDOWNUSDT', 'ORNUSDT', 'UTKUSDT', 'XVSUSDT', 'ALPHAUSDT', 'AAVEUSDT',
           'NEARUSDT', 'SXPUPUSDT', 'SXPDOWNUSDT', 'FILUSDT', 'FILUPUSDT', 'FILDOWNUSDT', 'YFIUPUSDT', 'YFIDOWNUSDT', 'INJUSDT', 'AUDIOUSDT', 'CTKUSDT', 'BCHUPUSDT',
           'BCHDOWNUSDT', 'AKROUSDT', 'AXSUSDT', 'HARDUSDT', 'DNTUSDT', 'STRAXUSDT', 'UNFIUSDT', 'ROSEUSDT', 'AVAUSDT', 'XEMUSDT', 'AAVEUPUSDT', 'AAVEDOWNUSDT',
           'SKLUSDT', 'SUSDUSDT', 'SUSHIUPUSDT', 'SUSHIDOWNUSDT', 'XLMUPUSDT', 'XLMDOWNUSDT', 'GRTUSDT', 'JUVUSDT', 'PSGUSDT', '1INCHUSDT', 'REEFUSDT',
           'OGUSDT', 'ATMUSDT', 'ASRUSDT', 'CELOUSDT', 'RIFUSDT', 'BTCSTUSDT', 'TRUUSDT', 'CKBUSDT', 'TWTUSDT', 'FIROUSDT', 'LITUSDT', 'SFPUSDT']




# valid intervals - 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M

# get timestamp of earliest date data is available
#timestamp = client._get_earliest_valid_timestamp('BTCUSDT', '1h')
#print(timestamp)


def buysell():
    for symbol in tickers:
        bars = client.get_historical_klines(symbol, Client.KLINE_INTERVAL_1HOUR, "300 hours ago UTC")
        for line in bars:
            del line[6:]
# each symbol is
        df = pd.DataFrame(bars, columns=['date', 'open', 'high', 'low', 'close', 'Volume'])
        df['date'] = pd.to_datetime(df['date'],unit='ms')
        df['close'] = df['close'].astype('float64')
        df['Volume'] = df['Volume'].astype('float64')

        df.set_index('date', inplace=True)

        sma12 = btalib.sma(df.close,period=12)
        sma26 = btalib.sma(df.close,period=26)
        df['ema12'] = df['close'].ewm(span=12).mean()
        df['ema26'] = df['close'].ewm(span=26).mean()
        df['macd'] = df['ema12'] - df['ema26']
        df['signal'] = df['macd'].ewm(span=9, adjust=False).mean()



    #"""Calculate On-Balance Volume (OBV)"""
#not sure if the below lib method was calculating OBV correctly. Done it manually below.
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
        #print(symbol)
        if ((ema12gtema26co == True and macdgtsignal == True and obv_pc > 0.1)):
            action = 'BUY'
    # criteria for a sell signal
        elif (ema12ltema26co == True and macdltsignal == True):
            action = 'SELL'
    # anything other than a buy or sell, just wait
        else:
            action = 'WAIT'
    #print(df)
        if action == 'BUY' or action == 'SELL':
            print(action)
            print(symbol)

while True:
    localtime = time.localtime()
    result = time.strftime("%I:%M:%S %p", localtime)
    print(result)
    print(buysell())
    time.sleep(3463)