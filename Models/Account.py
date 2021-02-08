import os
from binance.websockets import BinanceSocketManager
from binance.client import Client
# init
api_key = os.environ.get('binance_api')
api_secret = os.environ.get('binance_secret')
client = Client(api_key ='slxV98HxyHJJDrXraDnTDOS3gBbfj7WICoRLxPO8sf8Fx9OFHQv6DqR3lmSwOqat', api_secret='8TzPuuLS6kMuMBh9MuFkhHMlelAlFBsjCc53YkBh1lVv6t29g06OWZR67o925kci')

#client.API_URL = 'https://api.binance.com'
# currently facing test Endpoint
#client.API_URL = 'https://testnet.binance.vision/api'

# Get all account details
#print(client.get_account())

# Get balance for specific coin
#print(client.get_asset_balance(asset='XLM'))

# get balances for futures account
#print(client.futures_account_balance())

# get balances for margin account
#print(client.get_margin_account())

# get latest price from Binance API
btc_price = client.get_symbol_ticker(symbol="BTCUSDT")
# print full output (dictionary)
#print(btc_price)
prices = client.get_all_tickers()
#print(prices)

#buy_order = client.create_order(symbol='BTCUSDT' , side='SELL', type='MARKET', quantity=0.001)
