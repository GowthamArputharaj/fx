# Get and Plot 
# all Trend lines, 
# Support and Resistance Lines, 
# Extreme Points 
# for given point or range of points

# Module Import Area
import pandas as pd 
import numpy as np 

import matplotlib.pyplot as plt 
import mplfinance as mpf

from datetime import datetime

from scipy.signal import argrelextrema

# Constants Area
CANDLE_DATA_FILE_NAME = "../../data/eurusd_col_m1_new.csv"
ROUND_DIGIT = 5
ROUND_CMP = 3
SUPPORT_RESISTANCE_ROUND_CMP = 4
EXTREMES_ORDER = 10
LINE_COLOR = 'blue'
SUPPORT_RESISTANCE_LINE_COLOR = 'lime'
EXTREME_POINTS_COLOR = 'red'
EXTREME_POINTS_INTERSECTION_COLOR = 'green'
LINES_AT_POINT_COLOR = 'purple'
EXTEND_LENGTH = 50
SCAN_LENGTH = 200
READ_TOTAL_CSV_DATA = 500
MIN_MAX_EXTREME = ['extreme']
NUMBER_OF_SUPPORT_RESISTANCE_LINES = 5
TOP_NUMBER_OF_SUPPORT_AND_RESISTANCE_OCCURANCE = 50000000
PITCHFORK_EXTREMES_RANGES = [15]
NUMBER_OF_PITCHFORK_PER_RANGE = 1
PITCHFORK_EXTEND_LENGTH = 40

all_lines = []
all_lines_for_extreme_points = []
all_points = []
all_minimas = []
all_maximas = []
all_extremes = []
all_minimas_pitchfork = []
all_maximas_pitchfork = []
all_extremes_pitchfork = []
all_support_and_resistance_lines = []
all_line_points_at_point = []
all_support_resistance_lines = []
selectPlotCandleStickGraph = []
all_pitchfork_points = []
all_upward_pitchfork_points = []
all_downward_pitchfork_points = []
all_pitchfork_lines = []


data = pd.read_csv(CANDLE_DATA_FILE_NAME)
data = data.iloc[:READ_TOTAL_CSV_DATA]
data.Datetime = pd.to_datetime(data.Datetime)
data = data.set_index('Datetime')

function_initial_data = data.copy(CANDLE_DATA_FILE_NAME)

data_with_Datetime = pd.read_csv(CANDLE_DATA_FILE_NAME)
data_with_Datetime = data_with_Datetime.iloc[:READ_TOTAL_CSV_DATA]
data_with_Datetime.Datetime = pd.to_datetime(data_with_Datetime.Datetime)

def getAllBullishBearishChangingPoints(returnOpenCloseData = False, returnLowHighData = False):
	dtt = function_initial_data.iloc[:]
	points = []
	low_high_data = []
	open_close_data = []

	for i in range(len(dtt)-1):
		i_stat = isPointBullishOrBearish(i)
		i_plus_one_stat = isPointBullishOrBearish(i+1)

		if(i_stat != i_plus_one_stat):
			if((returnOpenCloseData == False) and (returnLowHighData == False)):
				points.append(dtt.iloc[i+1])
		
			if(returnOpenCloseData == True):
				if(i_stat == 'Bullish' and i_plus_one_stat == 'Bearish'):
					open_close_data.append(dtt['close'].iloc[i+1])
				if(i_stat == 'Bearish' and i_plus_one_stat == 'Bullish'):
					open_close_data.append(dtt['open'].iloc[i+1])
			
			if(returnLowHighData == True):
				if(i_stat == 'Bullish' and i_plus_one_stat == 'Bearish'):
					low_high_data.append(dtt['high'].iloc[i+1])
				if(i_stat == 'Bearish' and i_plus_one_stat == 'Bullish'):
					low_high_data.append(dtt['low'].iloc[i+1])
			
	if((returnOpenCloseData == False) and (returnLowHighData == False)):
		return points
	else:
		return open_close_data, low_high_data

def isPointBullishOrBearish(x_point):
	point = function_initial_data.iloc[x_point]
	result = ''
	if(point['close'] < point['open']):
		result = 'Bearish'
	elif(point['open'] < point['close']):
		result = 'Bullish'
	else:
		result = 'Doji'
	
	return result 

def pointExtremeInOpenOrClose(x_point):
	result = ''
	isPointBullishOrBearishResult = isPointBullishOrBearish(x_point)
	if(isPointBullishOrBearishResult == 'Doji'):
		result = 'open'

	if(x_point in all_minimas):
		result = 'open' if(isPointBullishOrBearishResult == 'Bullish') else 'close'

	if(x_point in all_maximas):
		result = 'close' if(isPointBullishOrBearishResult == 'Bullish') else 'open'

	return result

def getMinimaPoints(order = EXTREMES_ORDER, set_global_variable = True): 
	global all_minimas
	global all_minimas_pitchfork

	data = ''
	if(set_global_variable == 'pitchfork'):
		data = function_initial_data['close'].iloc[:SCAN_LENGTH]
	else:
		data = function_initial_data['close']

	min_idx = list(argrelextrema(np.array(data), np.less, order=order)[0])
	if(set_global_variable == True):
		all_minimas = min_idx
	elif(set_global_variable == 'pitchfork'):
		all_minimas_pitchfork = min_idx

	return min_idx

def getMaximaPoints(order = EXTREMES_ORDER, set_global_variable = True):
	global all_maximas
	global all_maximas_pitchfork

	data = ''
	if(set_global_variable == 'pitchfork'):
		data = function_initial_data['close'].iloc[:SCAN_LENGTH]
	else:
		data = function_initial_data['close']

	max_idx = list(argrelextrema(np.array(data), np.greater, order=order)[0])
	if(set_global_variable == True):
		all_maximas = max_idx
	elif(set_global_variable == 'pitchfork'):
		all_maximas_pitchfork = max_idx

	return max_idx

def getExtremePoints(sort = False, order = EXTREMES_ORDER, set_global_variable = True):
	global all_extremes
	global all_extremes_pitchfork

	if(set_global_variable == True):
		min_points = getMinimaPoints(order)
		max_points = getMaximaPoints(order)
		extreme_points = min_points + max_points

		if(sort == True):
			extreme_points.sort()

		all_extremes = extreme_points

	elif(set_global_variable == 'pitchfork'):
		min_points = getMinimaPoints(order, 'pitchfork')
		max_points = getMaximaPoints(order, 'pitchfork')
		extreme_points = min_points + max_points

		if(sort == True):
			extreme_points.sort()

		all_extremes_pitchfork = extreme_points
		
	return extreme_points

def getTwoPoints(first_point, second_point, length):
	points = [None] * length 
	points[first_point] = function_initial_data.iloc[first_point]
	points[second_point] = function_initial_data.iloc[second_point]
	return points

def getAllPoints(length = SCAN_LENGTH+EXTEND_LENGTH, extremes = []): # max of extremas < length
	global all_points
	all_points = []
	points = [None] * length 

	if((len(extremes) > 0) and (max(extremas) < length)):
		raise Exception("Hi Gowtham!!! 'Maximum value of Extremas' should be greater then 'length'")

	if(len(extremes) == 0):
		if('min' in MIN_MAX_EXTREME):
			[extremes.append(k) for k in all_minimas]
		if('max' in MIN_MAX_EXTREME ):
			[extremes.append(k) for k in all_maximas]
		if('extreme' in MIN_MAX_EXTREME):
			[extremes.append(k) for k in all_extremes]

	for extreme_point in extremes:
		if(extreme_point < length):
			pointInOpenOrCloseResult = pointExtremeInOpenOrClose(extreme_point)

			if(pointInOpenOrCloseResult == 'close'):
				points[extreme_point] = function_initial_data['close'].iloc[extreme_point]
	
			if(pointInOpenOrCloseResult == 'open'):
				points[extreme_point] = function_initial_data['open'].iloc[extreme_point]

	all_points = points 
	return all_points

def getOneLine(x1, y1, x2, y2, starting_point = 0, ending_point = SCAN_LENGTH + EXTEND_LENGTH):

	# slope
	m = (y2 - y1) / (x2 - x1)

	# intercept
	b = y1 - (m * x1)

	line_length = SCAN_LENGTH + EXTEND_LENGTH
	line = [None] * line_length

	for i in range(line_length):
		if(i >= starting_point and i < ending_point):
			line[i] = (m * i) + b

	return line

def getAllLinesForExtremePoints(extremes = []):
	global all_lines_for_extreme_points
	all_lines_for_extreme_points = []
	lines = []
	if(len(extremes) == 0):
		if('min' in MIN_MAX_EXTREME):
			[extremes.append(k) for k in all_minimas]
		if('max' in MIN_MAX_EXTREME ):
			[extremes.append(k) for k in all_maximas]
		if('extreme' in MIN_MAX_EXTREME):
			[extremes.append(k) for k in all_extremes]

	for i in range(len(extremes)-1):
		x1 = extremes[i]
		y1 = function_initial_data['close'].iloc[x1]
		x2 = extremes[i+1]
		y2 = function_initial_data['close'].iloc[x2]

		line = getOneLine(x1, y1, x2, y2)

		lines.append(line)

	all_lines_for_extreme_points = lines
	return all_lines_for_extreme_points

def getOneParallelLine(x1, y1, x2, y2, xx, yy, starting_point = 0, ending_point = SCAN_LENGTH + EXTEND_LENGTH):
	# find line slope
	m = (y2 - y1) / (x2 - x1)

	# find parallel line equation 
	# y = mx + b 
	b = yy - ( m * xx )

	line_length = SCAN_LENGTH + EXTEND_LENGTH
	line = [None] * line_length

	for i in range(line_length):
		if(i >= starting_point and i < ending_point):
			line[i] = (m * i) + b

	return line




def plotCandleStickGraph(selectGraph):
	addplots = []
	
	if(('lines' in selectGraph) == True):	
		print(all_lines_for_extreme_points)
		for line in all_lines_for_extreme_points:
			line_plot = mpf.make_addplot(pd.DataFrame(line, dtype="float"), type="line", color=LINE_COLOR)
			addplots.append(line_plot)

	if(('points' in selectGraph) == True):
		point_plot = mpf.make_addplot(pd.DataFrame(all_points, dtype="float"), type="scatter", color=EXTREME_POINTS_COLOR)
		addplots.append(point_plot)

	if(('line_points' in selectGraph) == True):
		length = SCAN_LENGTH + EXTEND_LENGTH
		points = []
		for i in all_line_points_at_point:
			pt = [None] * length
			pt[SCAN_LENGTH] = i
			point = mpf.make_addplot(pd.DataFrame(pt, dtype="float"), type="scatter", color=LINES_AT_POINT_COLOR)
			addplots.append(point)
	
	if(('support_resistance' in selectGraph) == True):
		color_i = 0
		for line in all_support_and_resistance_lines:
			line_plot = mpf.make_addplot(pd.DataFrame(line, dtype="float"), type="line", color=SUPPORT_RESISTANCE_LINE_COLOR)
			# line_plot = mpf.make_addplot(pd.DataFrame(line, dtype="float"), type="line", color=(250/1000, (125+color_i)/1000, 0))
			addplots.append(line_plot)
			color_i = color_i + 50

	if(('pitchfork' in selectGraph) == True):
		pitchfork_colors = ['red', 'blue', 'purple', 'orange', 'maroon', 'darkgreen', 'blue']
		for i in range(len(all_pitchfork_lines)):
			color_index = i % len(pitchfork_colors)
			pitchfork_color = pitchfork_colors[color_index]
			if(i > 4):
				for idx, pitchfork_line in enumerate(all_pitchfork_lines[i]):
					print(len(pitchfork_line))
					line_plot = mpf.make_addplot(pd.DataFrame(pitchfork_line, dtype="float"), type="line", color=pitchfork_color)
					addplots.append(line_plot)
			


	# print(len(function_initial_data), len(addplots[1]), addplots[0])
	print(len(addplots), len(all_pitchfork_lines))
	mpf.plot(function_initial_data, addplot=addplots, type='candle', style="yahoo")

def getLinePointsAtPoint(x_value):
	global all_line_points_at_point
	
	points = []
	for line in all_lines_for_extreme_points:
		if(x_value < len(line)):
			pt = line[x_value]
			points.append(pt)
	
	all_line_points_at_point = points
	return points

def getSupportAndResistanceLines():
	global all_support_and_resistance_lines
	lines = []
	points = []

	points_open_close_data, points_low_close_data = getAllBullishBearishChangingPoints(returnOpenCloseData = True, returnLowHighData = True)
	[points.append(round(point, SUPPORT_RESISTANCE_ROUND_CMP)) for point in points_open_close_data]
	[points.append(round(point, SUPPORT_RESISTANCE_ROUND_CMP)) for point in points_low_close_data]
	
	unique_points, points_count = np.unique(points, return_counts = True)

	points_count = np.unique(points_count)
	points_count.sort()
	points_count = points_count[-TOP_NUMBER_OF_SUPPORT_AND_RESISTANCE_OCCURANCE:] # gets last 5 i.e top 5 biggest nos
	points_count = list(points_count) # [5, 3, 9, 7]
	points_count.reverse() # [9, 7, 5, 3] giving more priority to more occured point
	
	# NUMBER_OF_SUPPORT_RESISTANCE_LINES = 3
	no_of_sup_res_lines_found = 0
	for point_count in points_count:
		if((no_of_sup_res_lines_found < NUMBER_OF_SUPPORT_RESISTANCE_LINES) and (point_count > 5)):
			for unique_pt in unique_points:
				unique_point_count = points.count(unique_pt)
				if(unique_point_count == point_count):
					line = [unique_pt] * (SCAN_LENGTH + EXTEND_LENGTH)
					lines.append(line)
					no_of_sup_res_lines_found = no_of_sup_res_lines_found + 1
					if(no_of_sup_res_lines_found == NUMBER_OF_SUPPORT_RESISTANCE_LINES):
						break
		else:
			break
	
	all_support_and_resistance_lines = lines
	return all_support_and_resistance_lines

def getAndrewPitchforkPoints(): 
	global all_pitchfork_points
	ranges = PITCHFORK_EXTREMES_RANGES
	drawing_length = len(function_initial_data) - EXTEND_LENGTH

	for range_i in ranges:
		getMinimaPoints(range_i, set_global_variable = 'pitchfork')
		getMaximaPoints(range_i, set_global_variable = 'pitchfork')
		getExtremePoints(sort = True, order = range_i, set_global_variable = 'pitchfork')

		# print(all_minimas_pitchfork)
		# print(all_maximas_pitchfork)
		# print(all_extremes_pitchfork)

		desc_all_extremes_pitchfork = all_extremes_pitchfork
		desc_all_extremes_pitchfork.reverse()

		# print(desc_all_extremes_pitchfork)

		no_of_pitchforks_found_per_range = 0
		check_upward_pitchfork = True 
		check_downward_pitchfork = True

		if(no_of_pitchforks_found_per_range < NUMBER_OF_PITCHFORK_PER_RANGE):
			for i in range(len(desc_all_extremes_pitchfork)):
				# Upward Pitchfork min-max-min point
				if(check_upward_pitchfork == True):
					# if point is minima
					if(desc_all_extremes_pitchfork[i] in all_minimas_pitchfork):
						temp_extremes = desc_all_extremes_pitchfork[i:]
						for j in range(len(temp_extremes)):
							# if point is maxima
							if(desc_all_extremes_pitchfork[j] in all_maximas_pitchfork):
								temp_extremes = desc_all_extremes_pitchfork[j:]
								for k in range(len(temp_extremes)):
									# if point is minima
									if(desc_all_extremes_pitchfork[k] in all_minimas_pitchfork):
										temp = [desc_all_extremes_pitchfork[k], desc_all_extremes_pitchfork[j], desc_all_extremes_pitchfork[i]]
										temp = np.unique(temp)
										if(len(temp) == 3):
											temp = list(temp)
											temp.append('UPWARD')
											all_pitchfork_points.append(temp)
											all_upward_pitchfork_points.append(temp)

							
				# Downward Pitchfork min-max-min point
				if(check_downward_pitchfork == True):
					# if point is maxima
					if(desc_all_extremes_pitchfork[i] in all_maximas_pitchfork):
						temp_extremes = desc_all_extremes_pitchfork[i:]
						for j in range(len(temp_extremes)):
							# if point is minima
							if(desc_all_extremes_pitchfork[j] in all_minimas_pitchfork):
								temp_extremes = desc_all_extremes_pitchfork[j:]
								for k in range(len(temp_extremes)):
									# if point is maxima
									if(desc_all_extremes_pitchfork[k] in all_maximas_pitchfork):
										temp = [desc_all_extremes_pitchfork[k], desc_all_extremes_pitchfork[j], desc_all_extremes_pitchfork[i]]
										temp = np.unique(temp)
										if(len(temp) == 3):
											temp = list(temp)
											temp.append('DOWNWARD')
											all_pitchfork_points.append(temp)
											all_downward_pitchfork_points.append(temp)
				


		else:
			# continue
			# break
			print('No of Pitchfork has reached to Maximum ')

		temp = all_pitchfork_points
		temp.sort()
		temp = np.unique(temp, axis=0)
		all_pitchfork_points = temp

def getAndrewPitchforkLines(withTypes = ['andrew']): # regular_schiff, modified_schiff, andrew,
	global all_pitchfork_points, all_pitchfork_lines

	# sets all_minimas, all_maximas
	getExtremePoints()
	
	for pitchfork_points in all_pitchfork_points:
		# print(pitchfork_points)
		pitchfork_line = []

		first_point = int(pitchfork_points[0])
		second_point = int(pitchfork_points[1])
		third_point = int(pitchfork_points[2])

		# line BC
		x1 = second_point
		stat_y1 = pointExtremeInOpenOrClose(x1)
		y1 = function_initial_data[stat_y1].iloc[x1]

		x2 = third_point
		stat_y2 = pointExtremeInOpenOrClose(x2)
		y2 = function_initial_data[stat_y2].iloc[x2]

		line_BC = getOneLine(x1, y1, x2, y2, starting_point = x1, ending_point = x2+1)

		# midpoint of line BC ( D )
		mid_x = (x1 + x2) / 2
		mid_x = int(mid_x)
		mid_y = (y1 + y2) / 2

		# line AD
		x1 = first_point
		stat_y1 = pointExtremeInOpenOrClose(x1)
		y1 = function_initial_data[stat_y1].iloc[x1]

		x2 = mid_x
		y2 = mid_y

		pitchfork_starting_point = x1

		if((x2 + PITCHFORK_EXTEND_LENGTH) < (SCAN_LENGTH + EXTEND_LENGTH)):
			pitchfork_ending_point = x2 + PITCHFORK_EXTEND_LENGTH
		else: 
			pitchfork_ending_point = SCAN_LENGTH + EXTEND_LENGTH

		line_AD = getOneLine(x1, y1, x2, y2, starting_point = pitchfork_starting_point, ending_point = pitchfork_ending_point)

		
		# Parallel lines 
		# x1, y1, x2, y2 are from AD point ( since it is parallel line )

		# Parallel line from second point 
		xx = second_point 
		stat_y1 = pointExtremeInOpenOrClose(xx)
		yy = function_initial_data[stat_y1].iloc[xx]

		starting_point = xx

		second_parallel_line = getOneParallelLine(x1, y1, x2, y2, xx, yy, starting_point = starting_point, ending_point = pitchfork_ending_point)
		
		# parallel line from third point
		xx = third_point 
		stat_y1 = pointExtremeInOpenOrClose(xx)
		yy = function_initial_data[stat_y1].iloc[xx]

		starting_point = xx

		third_parallel_line = getOneParallelLine(x1, y1, x2, y2, xx, yy, starting_point = starting_point, ending_point = pitchfork_ending_point)

		# print(second_parallel_line)
		# exit()


		"""
		## Parallel lines
		stat_y1 = pointExtremeInOpenOrClose(second_point)
		y1 = function_initial_data[stat_y1].iloc[second_point]
		height_between_midpoint_to_BC = abs(mid_y - y1)
		
		# Parallel lines from second pitchfork point
		x1 = second_point
		stat_y1 = pointExtremeInOpenOrClose(x1)
		y1 = function_initial_data[stat_y1].iloc[x1]

		x2 = pitchfork_ending_point
		
		if(pitchfork_points[3] == 'DOWNWARD'):
			y2 = abs(line_AD[pitchfork_ending_point-1] - height_between_midpoint_to_BC)	
		if(pitchfork_points[3] == 'UPWARD'):
			y2 = line_AD[pitchfork_ending_point-1] + height_between_midpoint_to_BC

		parallel_line_from_second_pitchfork = getOneLine(x1, y1, x2, y2, starting_point = x1, ending_point = pitchfork_ending_point)	

		# Parallel line from third pitchfork point
		x1 = third_point
		stat_y1 = pointExtremeInOpenOrClose(x1)
		y1 = function_initial_data[stat_y1].iloc[x1]
		
		x2 = pitchfork_ending_point
		if(pitchfork_points[3] == 'UPWARD'):
			y2 = abs(line_AD[pitchfork_ending_point-1] - height_between_midpoint_to_BC)	
		if(pitchfork_points[3] == 'DOWNWARD'):
			y2 = line_AD[pitchfork_ending_point-1] + height_between_midpoint_to_BC

		parallel_line_from_third_pitchfork = getOneLine(x1, y1, x2, y2, starting_point = x1, ending_point = pitchfork_ending_point)

		# print(parallel_line_from_second_pitchfork, parallel_line_from_third_pitchfork)
		# exit()
		"""


		# plt.plot(range(len(line_BC)), line_BC)
		# plt.plot(range(len(line_AD)), line_AD)
		# plt.plot(range(len(parallel_line_from_second_pitchfork)), parallel_line_from_second_pitchfork)
		# plt.plot(range(len(parallel_line_from_third_pitchfork)), parallel_line_from_third_pitchfork)

		# plt.show()
		# exit()

		line_AD_none_count = line_AD.count(None)
		line_BC_none_count = line_BC.count(None)
		second_parallel_none_count = second_parallel_line.count(None)
		third_parallel_none_count = third_parallel_line.count(None)

		if((line_AD_none_count < len(line_AD)) and 
		(line_BC_none_count < len(line_BC)) and 
		(second_parallel_none_count < len(second_parallel_line)) and 
		(third_parallel_none_count < len(third_parallel_line))):
	
			pitchfork_lines = [line_AD, line_BC, second_parallel_line, third_parallel_line]

			all_pitchfork_lines.append(pitchfork_lines)
	

	print(len(all_pitchfork_lines))








if __name__ == "__main__":
	function_initial_data = function_initial_data.iloc[200:200+SCAN_LENGTH+EXTEND_LENGTH]
	"""
	getMinimaPoints()
	getMaximaPoints()
	getExtremePoints()
	# MIN_MAX_EXTREME = ['min']
	MIN_MAX_EXTREME = ['min', 'max']
	getAllLinesForExtremePoints()
	getAllPoints()
	getLinePointsAtPoint(SCAN_LENGTH)
	# plotCandleStickGraph(True, True, True, False)
	"""
	# getBullishBearishChangingPoints()

	# getSupportAndResistanceLines()
	# # # selectPlotCandleStickGraph = ['lines', 'points', 'line_points', 'support_resistance']
	# selectPlotCandleStickGraph = ['support_resistance']
	# plotCandleStickGraph(selectPlotCandleStickGraph)
	# exit()
	getAndrewPitchforkPoints()	
	getAndrewPitchforkLines(withTypes = ['andrew'])

	selectPlotCandleStickGraph = ['pitchfork']

	plotCandleStickGraph(selectPlotCandleStickGraph)

	# a = [[242, 212, 242], [173, 212, 242], [110, 212, 242], [77, 212, 242], [242, 194, 242], [173, 194, 242], [110, 194, 242], [242, 131, 242], [173, 131, 242], [242, 94, 242], [242, 44, 242], [242, 212, 173], [173, 212, 173], [110, 212, 173], [77, 212, 173], [242, 194, 173], [173, 194, 173], [110, 194, 173], [242, 131, 173], [173, 131, 173], [242, 212, 110], [173, 212, 110], [110, 212, 110], [77, 212, 110], [242, 194, 110], [173, 194, 110], [110, 194, 110], [242, 212, 77], [173, 212, 77], [110, 212, 77], [77, 212, 77]]

	# a = np.array(a)
	# print(len(a))
	# b = np.unique(a, axis=0)
	# print(len(b))






























