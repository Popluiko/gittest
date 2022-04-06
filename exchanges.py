import ccxt
import pandas as pd
import ta
import time
import matplotlib.pyplot as plt

#exchanges_list = ['aax', 'ascendex', 'bequant', 'bibox', 'bigone', 'binance', 'bitbay', 'bitcoincom', 'bitfinex',
#'bitforex', 'bitget', 'bitmart','bitmex', 'bitrue', 'bitso', 'bitstamp','blockchaincom','btcalpha', 'btcturk',
#'bw', 'bybit', 'bytetrade', 'cdax', 'cex','coinbaseprime', 'coinbasepro', 'coinex', 'coinfalcon', 'crex24',
#'cryptocom', 'currencycom','delta', 'exmo', 'fmfwio', 'ftx', 'ftxus', 'gateio', 'hitbtc', 'hitbtc3',
#'huobi', 'huobipro', 'kraken', 'kuna', 'latoken', 'latoken1', 'lbank','liquid', 'lykke', 'mexc', 
#'ndax', 'novadax', 'oceanex', 'okcoin', 'okex', 'okex3', 'okex5', 'phemex', 'poloniex', 'probit', 'qtrade', 
#'stex', 'therock', 'tidex', 'timex', 'upbit', 'wazirx', 'whitebit', 'yobit', 'zb', 'zipmex', 'zonda']
#'hitbtc',

exchanges_list = ['ascendex', 'bibox', 'bigone', 'binance', 'bitbay', 'bitcoincom', 'bitfinex',
'bitforex', 'bitget', 'bitrue', 'bitso', 'bitstamp','blockchaincom', 'btcturk',
'bw', 'bybit', 'cdax', 'cex','coinbaseprime', 'coinbasepro', 'coinfalcon', 'crex24', 'exmo', 'ftx', 
'ftxus','huobi', 'kraken', 'latoken', 'lbank','liquid', 'lykke', 
'ndax', 'novadax', 'okcoin', 'okex', 'phemex', 'poloniex', 'qtrade', 
'stex', 'therock', 'timex', 'upbit', 'whitebit', 'yobit', 'zipmex', 'zonda'] #46

#exchanges_list = ['binance', 'bitfinex', 'currencycom', 'ftx', 'bitstamp', 'bybit', 'huobi', 'kraken', 'okex', 'poloniex', 'yobit']
#exchanges_list = ['binance']

figure_title = "BTC/USDT 30M"
pair = "BTC/USDT"
timeframe = "30m"
exchange_id = 'binance' # <Биржа 
limit  = 8000
limitCandle = 300
depth_quantity = 30
priceK = 4000

fig = plt.figure()
fig.set_figwidth(10)
fig.set_figheight(6)
plt.suptitle(pair, color="black")
plt.title(timeframe, color="black")
plt.suptitle("BTC/USDT 30M")


while True:
	try:
		second = int(time.strftime('%S'))
		minute = int(time.strftime('%M'))
		hour = int(time.strftime('%H'))
		day = int(time.strftime('%d'))
		month = int(time.strftime('%m'))
		year = int(time.strftime('%Y'))
		all_orders = ""
		if second % 10 == 0 and minute % 5 == 0: 
			a = 0
			b = 0
			total_quantity_asks = 0
			total_quantity_bids = 0
			plt.clf()
			exchange_class = getattr(ccxt, exchange_id)
			exchange = exchange_class()
			candles = exchange.fetchOHLCV ("BTC/USDT", timeframe = timeframe, limit = limitCandle, params = {})
			dff = pd.DataFrame(candles, columns=['Date', 'Open', 'High', 'Low', 'Close', 'Volume'])
			date = dff["Date"].astype(int)
			dff["Date"] = pd.to_datetime(dff["Date"] / 1000, unit='s')

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
				print("---------Bids---------------", e)

				priceH = dff['Close'][limitCandle-1] + priceK 
				priceL = dff['Close'][limitCandle-1] - priceK 
				quantity_asks = 0
				quantity_bids = 0

				for i in arr_BIDS:
					if priceL < i[0] < priceH:
						b = b + i[1]
						quantity_bids = quantity_bids + 1
						
					if i[1] >= depth_quantity and priceL < i[0] < priceH:

						if 10<i[1]<30:
							lw = 1
							cl_b = "blue"
						elif 3<i[1]<10:
							lw = 1
							cl_b = "#52DBFF"
						elif 30<i[1]<100:
							lw = 2
							cl_b = "darkblue"
						elif 100<i[1]<400:
							lw = 2
							cl_b = "#2B0F45"
						elif 401<i[1]<10000:
							lw = 2
							cl_b = "#FF00FF"
						else:
							lw = 1
							cl_b = "blue"
						plt.axhline(i[0], color = cl_b, linewidth = lw)
						print("BIDS", i)

						all_orders = all_orders + (f"BIDS {i} -> {e}\n")

				print("---------Asks--------------", e)
				for i in arr_ASKS:
					if priceL < i[0] < priceH:
						a = a + i[1]
						quantity_asks = quantity_asks + 1
					if i[1] >= depth_quantity and priceL < i[0] < priceH:
							
						if 10<i[1]<30:
							lw = 1
							cl_a = "red"
						elif 3<i[1]<10:
							lw = 1
							cl_a = "#E6665D"
						elif 30<i[1]<100:
							lw = 2
							cl_a = "darkred"
						elif 100<i[1]<400:
							lw = 2
							cl_a = "#6C0109"
						elif 401<i[1]<10000:
							lw = 2
							cl_a = "#FFFF00"
						else:
							lw = 1
							cl_a = "red"
						plt.axhline(i[0], color = cl_a, linewidth = lw)

						print("ASKS", i)
						all_orders = all_orders + (f"ASKS {i} -> {e}\n")
					
				total_quantity_asks = total_quantity_asks + quantity_asks
				total_quantity_bids = total_quantity_bids + quantity_bids
			data = open("orders.txt", "w")
			data.write(all_orders)
			data.close()
			print("ASKS", round(a,2))
			print("BIDS", round(b,2))

			k = a / b
			if k == 1:
					grad = 0 * 90
			elif k < 1:
				grad = ((1-k) * 90)
			elif k > 1:
				grad = -(1-(b / a)) * 90

			print("Grad", round(grad,2),"°")
			print("ASKS quantity", round(total_quantity_asks,2))
			print("BIDS quantity", round(total_quantity_bids,2))
			print("ASKS avg order", round(a / total_quantity_asks ,5))
			print("BIDS avg order", round(b / total_quantity_bids,5))
				
			plt.plot(dff["Date"], dff['Close'], color="black", linewidth = 1)	

			file = open("info_orders.txt", "w")
			file.write(f"ASKS all orders {round(a,2)}\nBIDS all orders {round(b,2)}\n")
			file.write(f"Grad { round(grad,2)}°\n")
			file.write(f"ASKS quantity all orders {round(total_quantity_asks,2)}\n")
			file.write(f"BIDS quantity all orders {round(total_quantity_bids,2)}\n")
			file.write(f"ASKS avg order {round(a / total_quantity_asks ,5)}\n")
			file.write(f"BIDS avg order {round(b / total_quantity_bids,5)}\n")
			now_time = (f"{year}-{month}-{day} {hour}:{minute}:{second}")
			file.write(f"Time is last request \n{now_time}\n")
			file.close()

			plt.savefig('orders.png', transparent=False)
			#plt.show()

	except KeyError:
			print(exchange_id, "Server not responding, try again...")
			time.sleep(3)

