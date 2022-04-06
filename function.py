min_order = 0
def paramert_plot(name_order, i, depth_quantity, priceL, priceH):
	arr = []
	global min_order
	if i[1] >= depth_quantity and priceL < i[0] < priceH:
							
		if name_order == "bids":
			color = ["blue", "#52DBFF", "darkblue", "#2B0F45", "#FF00FF"]
		elif name_order == "asks":
			color = ["red", "#E6665D", "darkred", "#6C0109", "#aeeb07"]#"#FFFF00"]
		else:
			color = ["dark", "dark", "dark", "dark", "dark"]

		if depth_quantity == 1000:
			min_order = 5
		elif depth_quantity == 3000:
			min_order = 10
		elif depth_quantity == 6000:
			min_order = 30

		if 10<i[1]<30:
			lw = 1
			cl = color[0]
		elif min_order<i[1]<10:
			lw = 1
			cl = color[1]
		elif 30<i[1]<100:
			lw = 2
			cl = color[2]
		elif 100<i[1]<400:
			lw = 2
			cl = color[3]
		elif 400<i[1]<10000:
			lw = 2
			cl = color[4]
		else:
			lw = 1
			cl= color[0]
		arr.append(lw)
		arr.append(cl)
	return (arr)


def grad(a, b):
	k = a / b
	if k == 1:
		grad = 0 * 90
	elif k < 1:
		grad = ((1-k) * 90)
	elif k > 1:
		grad = -(1-(b / a)) * 90
	return (grad)