



combos =["AA","KK","QQ","JJ","TT","99","88","77","66","55","44","33","22","AK","AQ","AJ","AT","A9","A8","A7","A6","A5","A4","A3","A2","KQ","KJ","KT","K9","K8","K7","K6","K5","K4","K3","K2","QJ","QT","Q9","Q8","Q7","Q6","Q5","Q4","Q3","Q2","JT","J9","J8","J7","J6","J5","J4","J3","J2","T9","T8","T7","T6","T5","T4","T3","T2","98","97","96","95","94","93","92","87","86","85","84","83","82","76","75","74","73","72","65","64","63","62","54","53","52","43","42","32"]


fpath = "./material/bbz-data/mtt-40bb.txt"

final_data_arr = []


with open(fpath) as f:
	data = f.read()
	data_arr = data.split("<\\/i><\\/li><li><i")
	for line in data_arr:

		
		# parse turhat pois
		new_line = line.replace(r"<\/i>", " ")
		new_line = new_line.replace("<li>", " ")
		new_line = new_line.replace("<\\/li>", " ")
		new_line = new_line.replace("<i hp>", " ")
		new_line = new_line.replace(r"<\/b>", " ")
		new_line = new_line.replace("<i><b>", " ")
		new_line = new_line.replace("<i cf dw='100.00' style='width:100.00%'>", " ")
		new_line = new_line.replace("<i hgp dcp='50.76'dfp='43.51'drp='5.72'dap='0.00'>", " ")
		new_line = new_line.replace("<i hp>", " ")
		new_line = new_line.replace("<i hp>", " ")
		# print(new_line + "\n")

		# line->list
		line_arr = new_line.split(" ")
		# tyhjat pois
		line_arr = [i for i in line_arr if i]

		



		# temp print linet missä ei comboa

		# if (line_arr[0][:2] not in combos):
		# 	print(new_line + "\n")


		combo_data = []

		## otetaan data ylös [76s, 0%, 0%, 0%, 100%] formaattiin 
		for i in line_arr:
			# jos vika itemi ht>*combo* formaatissa otetaan ylös combo
			if (i[:3] == "ht>"):
				combo_data.append(i[3:])
			
			if (i[-1] == "%"):
				combo_data.append(float(i[:-1]))




		final_data_arr.append(combo_data)

	temp_arr = []
	# korjataan se että uuten spottiin mennessä '22' ja 'AA' linet samassa
	for combo_data in final_data_arr:
		if len(combo_data) > 5:
			# print(combo_data)
			temp_arr.append(combo_data[:5])
			temp_arr.append(combo_data[5:])
		elif len(combo_data) == 5:
			temp_arr.append(combo_data)

		else:
			print("alert alert" + combo_data)

	final_data_arr = temp_arr
	for i in final_data_arr:
		print(i)



	# TODO: 
	## [0.0, 0.0, 100.0, 0.0, 'AA'] format into pio-format ??
	## vai labelit vaan [stack: 30, pos: BB, situation: rfi/vs-LJ-rfi/vs-BB-3bet/vs-BB-4bet yms]
	## --> ja luon logiikan datan hakemiseen labelien avulla! joo.


























		#print(line_arr)
		# if (line_arr[0][:2] in combos):
		# 	combo = line_arr[0]



		# 	actions_data_arr = [None,None,None,None] #[call, fold, raise, ai]

		# 	if ("Call:" in line_arr):
		# 		call_idx = line_arr.index("Call:") + 1
		# 		#print(call_idx)
		# 		actions_data_arr[0] = line_arr[call_idx]
		# 		#print(actions_data_arr)

# koodissa tärkeitä spotteja: i pos, ht>, 