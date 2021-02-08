import os

from binance.client import Client
# init
api_key = os.environ.get('binance_api')
api_secret = os.environ.get('binance_secret')
client = Client(api_key ='x6Xi3JQcpmtYzgupmqQ7b3zztRdTeKom7jpQVp4D9V6YVnsK9DHUQHwUU5D8a6N9', api_secret='JVbBnE9oQkB3YOa9Oz6WGpAt7com37lhfaIHlHEcPkmV2p4sY4hrmJ8RjGRqIWHl')

#client.API_URL = 'https://api.binance.com'

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

