import ccxt
import pandas as pd
import ta
import time
import matplotlib.pyplot as plt
from function import *

exchanges_list = ['ascendex', 'bibox', 'bigone', 'binance', 'bitbay', 'bitcoincom', 'bitfinex',
'bitforex', 'bitget', 'bitrue', 'bitso', 'bitstamp','blockchaincom', 'btcturk',
'bw', 'bybit', 'cdax', 'cex','coinbaseprime', 'coinbasepro', 'coinfalcon', 'crex24', 'exmo', 'ftx', 
'ftxus','huobi', 'kraken', 'latoken', 'lbank','liquid', 'lykke', 
'ndax', 'novadax', 'okcoin', 'okex', 'phemex', 'poloniex', 'qtrade', 
'stex', 'therock', 'timex', 'upbit', 'whitebit', 'yobit', 'zipmex', 'zonda'] #46

figure_title = "BTC/USDT 30M"
pair = "BTC/USDT"
timeframe = "30m"
exchange_id = 'binance'
limit  = 8000
limitCandle = 300
#--------------------------
depth_quantity_min = 7
priceK_min = 2000

depth_quantity_midl = 15
priceK_midl = 3000

depth_quantity_max = 50
priceK_max = 7000
#--------------------------

while True:
	try:
		second = int(time.strftime('%S'))
		minute = int(time.strftime('%M'))
		hour = int(time.strftime('%H'))
		day = int(time.strftime('%d'))
		month = int(time.strftime('%m'))
		year = int(time.strftime('%Y'))

		if second % 1 == 0 and minute % 1 == 0: 
			exchange_class = getattr(ccxt, exchange_id)
			exchange = exchange_class()
			candles = exchange.fetchOHLCV ("BTC/USDT", timeframe = timeframe, limit = limitCandle, params = {})
			dff = pd.DataFrame(candles, columns=['Date', 'Open', 'High', 'Low', 'Close', 'Volume'])
			date = dff["Date"].astype(int)
			dff["Date"] = pd.to_datetime(dff["Date"] / 1000, unit='s')

			priceH_min = dff['Close'][limitCandle-1] + priceK_min 
			priceL_min = dff['Close'][limitCandle-1] - priceK_min 
			priceH_midl = dff['Close'][limitCandle-1] + priceK_midl 
			priceL_midl = dff['Close'][limitCandle-1] - priceK_midl 
			priceH_max = dff['Close'][limitCandle-1] + priceK_max 
			priceL_max = dff['Close'][limitCandle-1] - priceK_max 
#-----------------------------------------------------------------------------------------------
			fig = plt.figure()
			fig.set_figwidth(10)
			fig.set_figheight(6)
			plt.suptitle(pair, color="black")
			plt.suptitle("BTC/USDT 30M")
#-----------------------------------------------------------------------------------------------
			for e in exchanges_list:
				try:
					exchange_id = e
					exchange_class = getattr(ccxt, exchange_id)
					exchange = exchange_class()
					orderbook= exchange.fetch_l2_order_book(pair, limit)
				except:
					print(exchange_id, "next exchangex")
					next
					
				arr_BIDS = orderbook['bids']
				arr_ASKS = orderbook['asks']
#-----------------------------------------------------------------------------------------------
				for i in arr_BIDS:
					par = paramert_plot("bids", i, depth_quantity_max, priceL_max, priceH_max)
					if len(par) != 0 :
						plt.axhline(i[0], color = par[1], linewidth = par[0])

				for i in arr_ASKS:
					par = paramert_plot("asks", i, depth_quantity_max, priceL_max, priceH_max)
					if len(par) != 0 :
						plt.axhline(i[0], color = par[1], linewidth = par[0])
#-----------------------------------------------------------------------------------------------
			plt.plot(dff["Date"], dff['Close'], color="black", linewidth = 1)
			plt.savefig('ordermax.png', transparent=False)
#-----------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------
			fig = plt.figure()
			fig.set_figwidth(10)
			fig.set_figheight(6)
			plt.suptitle(pair, color="black")
			plt.suptitle(f"BTC/USDT 30M")
#-----------------------------------------------------------------------------------------------
			for e in exchanges_list:
				try:
					exchange_id = e
					exchange_class = getattr(ccxt, exchange_id)
					exchange = exchange_class()
					orderbook= exchange.fetch_l2_order_book(pair, limit)
				except:
					print(exchange_id, "next exchangex")
					next
					
				arr_BIDS = orderbook['bids']
				arr_ASKS = orderbook['asks']
#-----------------------------------------------------------------------------------------------
				for i in arr_BIDS:
					par = paramert_plot("bids", i, depth_quantity_min, priceL_min, priceH_min)
					if len(par) != 0 :
						plt.axhline(i[0], color = par[1], linewidth = par[0])

				for i in arr_ASKS:
					par = paramert_plot("asks", i, depth_quantity_min, priceL_min, priceH_min)
					if len(par) != 0 :
						plt.axhline(i[0], color = par[1], linewidth = par[0])
#-----------------------------------------------------------------------------------------------
			plt.plot(dff["Date"], dff['Close'], color="black", linewidth = 1)
			plt.savefig('ordermin.png', transparent=False)
#-----------------------------------------------------------------------------------------------
	except KeyError:
			print(exchange_id, "Server not responding, try again...")
			time.sleep(3)

