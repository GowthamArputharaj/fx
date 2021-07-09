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
## File Data Constants
CANDLE_DATA_FILE_NAME = "../../data/eurusd_col_m1_new.csv"
READ_TOTAL_CSV_DATA = 500
EXTEND_LENGTH = 50
SCAN_LENGTH = 200
ROUND_DIGIT = 5
ROUND_CMP = 3
DATA_STARTING_POINT = 200

## Extremes Constants
# EXTREMES_ORDER = 10
EXTREMES_ORDER = 6
EXTREME_POINTS_COLOR = 'red'
EXTREME_POINTS_INTERSECTION_COLOR = 'green'
MIN_MAX_EXTREME = ['extreme']

## Support Resistance Constants
SUPPORT_RESISTANCE_ROUND_CMP = 4
SUPPORT_RESISTANCE_LINE_COLOR = 'lime'
LINE_COLOR = 'blue'
LINES_AT_POINT_COLOR = 'purple'
NUMBER_OF_SUPPORT_RESISTANCE_LINES = 5
TOP_NUMBER_OF_SUPPORT_AND_RESISTANCE_OCCURANCE = 50000000

## Pitchfork Constants
# PITCHFORK_EXTREMES_RANGES = [10]
PITCHFORK_EXTREMES_RANGES = [6]
NUMBER_OF_PITCHFORK_PER_RANGE = 1
PITCHFORK_EXTEND_LENGTH = 40
PITCHFORK_MINIMUM_BC_HEIGHT = 0.00005
#.. first_point to second_point distance can be (PITCHFORK_TAIL_TO_FORK_WIDTH) times distance between second_point to third_point
PITCHFORK_TAIL_TO_FORK_WIDTH = 2 
MAX_EXTREME_POINT_GAP_FOR_ONE_PITCHFORK = 3
# MAX_EXTREMES_FOR_SECOND_PITCHFORK = 2
# MAX_EXTREMES_FOR_THIRD_PITCHFORK = 3
MAX_EXTREMES_FOR_SECOND_PITCHFORK = 2
MAX_EXTREMES_FOR_THIRD_PITCHFORK = 3

# Oscillators
WILLIAM_R_COLOR = 'blue'
RSI_COLOR = 'green'

# 7.500000000004725e-05
# 0.00007500000000004725

# Arrays Area
## Lines Arrays
all_lines = []
all_lines_for_extreme_points = []
all_support_and_resistance_lines = []
all_line_points_at_point = []
all_support_resistance_lines = []

## Extremes Arrays
all_points = []
all_minimas = []
all_maximas = []
all_extremes = []

## Pitchfork Arrays
all_minimas_pitchfork = []
all_maximas_pitchfork = []
all_extremes_pitchfork = []
all_extreme_pitchfork_points = []
all_pitchfork_points = []
all_upward_pitchfork_points = []
all_downward_pitchfork_points = []
all_pitchfork_lines = []

## Graph Arrays
selectPlotCandleStickGraph = []

## Oscillators
william_r_oscillator = []
stochastic_oscillator = []
rsi_oscillator = []
obv_oscillator = []

# Initial something
data = pd.read_csv(CANDLE_DATA_FILE_NAME)
data = data.iloc[:READ_TOTAL_CSV_DATA]
data.Datetime = pd.to_datetime(data.Datetime)
data = data.set_index('Datetime')

function_initial_data = data.copy(CANDLE_DATA_FILE_NAME)

data_with_Datetime = pd.read_csv(CANDLE_DATA_FILE_NAME)
data_with_Datetime = data_with_Datetime.iloc[:READ_TOTAL_CSV_DATA]
data_with_Datetime.Datetime = pd.to_datetime(data_with_Datetime.Datetime)

def getAllBullishBearishChangingPoints(returnOpenCloseData = False, returnLowHighData = False):
	# dtt = function_initial_data.iloc[:]
	dtt = function_initial_data.iloc[DATA_STARTING_POINT:DATA_STARTING_POINT+SCAN_LENGTH]
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

def isPointValueBullishOrBearish(point):
	result = ''
	if(point['close'] < point['open']):
		result = 'Bearish'
	elif(point['open'] < point['close']):
		result = 'Bullish'
	else:
		result = 'Doji'
	
	return result 

def pointExtremeInOpenOrClose(x_point, global_variable = []):
	global all_minimas_pitchfork
	
	result = ''
	isPointBullishOrBearishResult = isPointBullishOrBearish(x_point)

	if(len(global_variable) == 0):
		if(isPointBullishOrBearishResult == 'Doji'):
			result = 'open'

		if(x_point in all_minimas):
			result = 'open' if(isPointBullishOrBearishResult == 'Bullish') else 'close'

		if(x_point in all_maximas):
			result = 'close' if(isPointBullishOrBearishResult == 'Bullish') else 'open'

	elif('pitchfork' in global_variable):
		if(isPointBullishOrBearishResult == 'Doji'):
			result = 'open'

		if(x_point in all_minimas_pitchfork):
			result = 'open' if(isPointBullishOrBearishResult == 'Bullish') else 'close'

		if(x_point in all_maximas_pitchfork):
			result = 'close' if(isPointBullishOrBearishResult == 'Bullish') else 'open'

	return result

def getMinimaPoints(order = EXTREMES_ORDER, set_global_variable = True): 
	global all_minimas
	global all_minimas_pitchfork

	data = file_data = []
	if(set_global_variable == 'pitchfork'):
		file_data = function_initial_data.iloc[:SCAN_LENGTH]
	else:
		file_data = function_initial_data.iloc[:SCAN_LENGTH]

	for i in range(len(file_data)):
		point = file_data.iloc[i]

		isPointValueBullishOrBearishResult = isPointValueBullishOrBearish(point)
		if(isPointValueBullishOrBearishResult == 'Bullish'):
			data.append(point['open'])
		elif(isPointValueBullishOrBearishResult == 'Bearish'):
			data.append(point['close'])
		else:
			data.append(point['open'])

	min_idx = list(argrelextrema(np.array(data), np.less, order=order)[0])
	
	if(set_global_variable == True):
		all_minimas = min_idx
	elif(set_global_variable == 'pitchfork'):
		all_minimas_pitchfork = min_idx

	return min_idx

def getMaximaPoints(order = EXTREMES_ORDER, set_global_variable = True):
	global all_maximas
	global all_maximas_pitchfork

	data = file_data = []
	if(set_global_variable == 'pitchfork'):
		file_data = function_initial_data.iloc[:SCAN_LENGTH]
	else:
		file_data = function_initial_data.iloc[:SCAN_LENGTH]

	for i in range(len(file_data)):
		point = file_data.iloc[i]
		
		isPointValueBullishOrBearishResult = isPointValueBullishOrBearish(point)
		if(isPointValueBullishOrBearishResult == 'Bullish'):
			data.append(point['close'])
		elif(isPointValueBullishOrBearishResult == 'Bearish'):
			data.append(point['open'])
		else:
			data.append(point['close'])

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

def getAllPoints(set_global_variable=[], length = SCAN_LENGTH+EXTEND_LENGTH, extremes = []): # max of extremas < length
	global all_points
	global all_extremes_pitchfork
	global all_extreme_pitchfork_points

	all_points = []
	points = [None] * length 

	# if(len(extremes) > 0):
	# 	if(max(extremes) < length):
	# 		raise Exception("Hi Gowtham!!! 'Maximum value of Extremas' should be greater then 'length'")

	if(len(extremes) == 0):
		if(len(set_global_variable) == 0):
			if('min' in MIN_MAX_EXTREME):
				[extremes.append(k) for k in all_minimas]
			if('max' in MIN_MAX_EXTREME ):
				[extremes.append(k) for k in all_maximas]
			if('extreme' in MIN_MAX_EXTREME):
				[extremes.append(k) for k in all_extremes]
		if('pitchfork' in set_global_variable):
			extremes = all_extremes_pitchfork
		

	for extreme_point in extremes:
		if(extreme_point < length):
			pointInOpenOrCloseResult = pointExtremeInOpenOrClose(extreme_point)

			if(pointInOpenOrCloseResult == 'close'):
				points[extreme_point] = function_initial_data['close'].iloc[extreme_point]
	
			if(pointInOpenOrCloseResult == 'open'):
				points[extreme_point] = function_initial_data['open'].iloc[extreme_point]

	if(len(set_global_variable) == 0):
		all_points = points 
	if('pitchfork' in set_global_variable):
		all_extreme_pitchfork_points = points 

	return points

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
		stat = pointExtremeInOpenOrClose(x1)
		y1 = function_initial_data[stat].iloc[x1]
		x2 = extremes[i+1]
		stat = pointExtremeInOpenOrClose(x2)
		y2 = function_initial_data[stat].iloc[x2]

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
		pitchfork_colors = ['red', 'blue', 'darkorange', 'purple', 'darkslategrey', 'darkgreen', 'darkviolet', 'orange', 'steelblue']
		for i in range(len(all_pitchfork_lines)):
			if(i > 0):
				color_index = i % len(pitchfork_colors)
				pitchfork_color = pitchfork_colors[color_index]

				for idx, pitchfork_line in enumerate(all_pitchfork_lines[i]):
					line_plot = mpf.make_addplot(pd.DataFrame(pitchfork_line, dtype="float"), type="line", color=pitchfork_color)
					addplots.append(line_plot)
			
	if(('william_r' in selectGraph) == True):
		# for point in william_r_oscillator:
		line_plot = mpf.make_addplot(pd.DataFrame(william_r_oscillator, dtype="float"),panel=1, color=WILLIAM_R_COLOR)
		addplots.append(line_plot)
			
	if(('stochastic' in selectGraph) == True):
		# for point in william_r_oscillator:
		line_plot = mpf.make_addplot(pd.DataFrame(stochastic_oscillator, dtype="float"),panel=1, color=WILLIAM_R_COLOR)
		addplots.append(line_plot)
			
	if(('rsi' in selectGraph) == True):
		# for point in william_r_oscillator:
		line_plot = mpf.make_addplot(pd.DataFrame(rsi_oscillator, dtype="float"),panel=1, color=RSI_COLOR)
		addplots.append(line_plot)
			
	if(('obv' in selectGraph) == True):
		# for point in obv_oscillator:
		line_plot = mpf.make_addplot(pd.DataFrame(obv_oscillator, dtype="float"),panel=1, color=RSI_COLOR)
		addplots.append(line_plot)
			
	if(('rsi' in selectGraph) or ('william_r' in selectGraph) or ('stochastic' in selectGraph) or ('obv' in selectGraph)):
		oscillator_line_eight = [None] * (SCAN_LENGTH+EXTEND_LENGTH)
		oscillator_line_seven = [None] * (SCAN_LENGTH+EXTEND_LENGTH)
		oscillator_line_three = [None] * (SCAN_LENGTH+EXTEND_LENGTH)
		oscillator_line_two = [None] * (SCAN_LENGTH+EXTEND_LENGTH)

		for i in range(SCAN_LENGTH+EXTEND_LENGTH):
			ones_digit = i % 10
			if(ones_digit in [1, 2, 3, 4, 5]):
				oscillator_line_eight[i] = 0.8	
				oscillator_line_seven[i] = 0.7
				oscillator_line_three[i] = 0.3
				oscillator_line_two[i] = 0.2

		line_plot = mpf.make_addplot(pd.DataFrame(oscillator_line_eight, dtype="float"),panel=1, color='red')
		addplots.append(line_plot)
		line_plot = mpf.make_addplot(pd.DataFrame(oscillator_line_seven, dtype="float"),panel=1, color='red')
		addplots.append(line_plot)
		line_plot = mpf.make_addplot(pd.DataFrame(oscillator_line_three, dtype="float"),panel=1, color='red')
		addplots.append(line_plot)
		line_plot = mpf.make_addplot(pd.DataFrame(oscillator_line_two, dtype="float"),panel=1, color='red')
		addplots.append(line_plot)

	# print(len(addplots), len(all_pitchfork_lines))
	mpf.plot(function_initial_data, addplot=addplots, type='candle', style="yahoo",figscale=1.2, volume=True)

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

	merged_all_extremes_pitchfork = []

	for range_i in ranges:
		getMinimaPoints(range_i, set_global_variable = 'pitchfork')
		getMaximaPoints(range_i, set_global_variable = 'pitchfork')
		getExtremePoints(sort = True, order = range_i, set_global_variable = 'pitchfork')
		merged_all_extremes_pitchfork.extend(all_extremes_pitchfork)

	merged_all_extremes_pitchfork = list(np.unique(merged_all_extremes_pitchfork))

	ranges = list(np.unique(ranges))

	for range_i in ranges:
		desc_all_extremes_pitchfork = merged_all_extremes_pitchfork
		desc_all_extremes_pitchfork.reverse()

		no_of_pitchforks_found_per_range = 0
		check_upward_pitchfork = True 
		check_downward_pitchfork = True

		if(no_of_pitchforks_found_per_range < NUMBER_OF_PITCHFORK_PER_RANGE):
			for i in range(len(desc_all_extremes_pitchfork)):
				# Upward Pitchfork min-max-min point
				if(check_upward_pitchfork == True): 
					if(desc_all_extremes_pitchfork[i] in all_minimas_pitchfork): # if point is minima
						temp_extremes = desc_all_extremes_pitchfork[i:]
						jj = 1
						for j in range(i, len(desc_all_extremes_pitchfork)):
							jj = jj + 1
							if(desc_all_extremes_pitchfork[j] in all_maximas_pitchfork): # if point is maxima
								temp_extremes = desc_all_extremes_pitchfork[j:]
								kk = 1
								for k in range(j, len(desc_all_extremes_pitchfork)):
									kk = kk + 1
									if(desc_all_extremes_pitchfork[k] in all_minimas_pitchfork): # if point is minima
										first_point = desc_all_extremes_pitchfork[k]
										second_point = desc_all_extremes_pitchfork[j]
										third_point = desc_all_extremes_pitchfork[i]
										
										stat = pointExtremeInOpenOrClose(second_point, 'pitchfork')
										second_point_y = function_initial_data[stat].iloc[second_point]
										stat = pointExtremeInOpenOrClose(third_point, 'pitchfork')
										third_point_y = function_initial_data[stat].iloc[third_point]

										if(second_point_y > third_point_y):
											temp = [first_point, second_point, third_point]
											temp = np.unique(temp)
											if(len(temp) == 3):
												temp = list(temp)
												temp.append('UPWARD')
												all_pitchfork_points.append(temp)
												all_upward_pitchfork_points.append(temp)

									if(kk > MAX_EXTREMES_FOR_SECOND_PITCHFORK):
										break
										print('')
										print(desc_all_extremes_pitchfork[k], desc_all_extremes_pitchfork[j], desc_all_extremes_pitchfork[i])

							if(jj > MAX_EXTREMES_FOR_THIRD_PITCHFORK):
								break
								print('')


				# Downward Pitchfork min-max-min point
				if(check_downward_pitchfork == True):
					if(desc_all_extremes_pitchfork[i] in all_maximas_pitchfork): # if point is maxima
						temp_extremes = desc_all_extremes_pitchfork[i:]
						jj = 1
						for j in range(i, len(desc_all_extremes_pitchfork)):
							jj = jj + 1
							if(desc_all_extremes_pitchfork[j] in all_minimas_pitchfork): # if point is minima
								temp_extremes = desc_all_extremes_pitchfork[j:]
								kk = 1
								for k in range(j, len(desc_all_extremes_pitchfork)): 
									kk = kk + 1
									if(desc_all_extremes_pitchfork[k] in all_maximas_pitchfork): # if point is maxima
										first_point = desc_all_extremes_pitchfork[k]
										second_point = desc_all_extremes_pitchfork[j]
										third_point = desc_all_extremes_pitchfork[i]
										
										stat = pointExtremeInOpenOrClose(second_point, 'pitchfork')
										second_point_y = function_initial_data[stat].iloc[second_point]
										stat = pointExtremeInOpenOrClose(third_point, 'pitchfork')
										third_point_y = function_initial_data[stat].iloc[third_point]

										if(second_point_y < third_point_y):
											temp = [first_point, second_point, third_point]
											temp = np.unique(temp)
											if(len(temp) == 3):
												temp = list(temp)
												temp.append('DOWNWARD')
												all_pitchfork_points.append(temp)
												all_downward_pitchfork_points.append(temp)
				
									if(kk > MAX_EXTREMES_FOR_SECOND_PITCHFORK):
										break
										print('')
										print(desc_all_extremes_pitchfork[k], desc_all_extremes_pitchfork[j], desc_all_extremes_pitchfork[i])

		
							if(jj > MAX_EXTREMES_FOR_THIRD_PITCHFORK):
								break
								print('')

		else:
			# continue
			# break
			print('No of Pitchfork has reached to Maximum ')


	temp = all_pitchfork_points
	temp.sort()
	temp = np.unique(temp, axis=0)
	all_pitchfork_points = temp
	# all_pitchfork_points.append(temp)
	# temp = np.unique(all_pitchfork_points, axis=0)
	# all_pitchfork_points = temp

def getAndrewPitchforkLines(withTypes = ['andrew']): # regular_schiff, modified_schiff, andrew,
	global all_pitchfork_points, all_pitchfork_lines

	# sets all_minimas, all_maximas
	getExtremePoints()
	
	for pitchfork_points in all_pitchfork_points:

		pitchfork_line = []

		first_point = int(pitchfork_points[0])
		second_point = int(pitchfork_points[1])
		third_point = int(pitchfork_points[2])

		# line BC
		x1 = second_point
		stat_y1 = pointExtremeInOpenOrClose(x1, 'pitchfork')
		
		if(stat_y1 == None):
			raise Exception("Hi Gowtham!!! Pitchfork: Point is not within Extreme Point getAndrewPitchforkLines() ")
			
		y1 = function_initial_data[stat_y1].iloc[x1]

		x2 = third_point
		stat_y2 = pointExtremeInOpenOrClose(x2, 'pitchfork')
		y2 = function_initial_data[stat_y2].iloc[x2]

		line_BC = getOneLine(x1, y1, x2, y2, starting_point = x1, ending_point = x2+1)

		# midpoint of line BC ( D )
		mid_x = (x1 + x2) / 2
		mid_x = int(mid_x)
		mid_y = (y1 + y2) / 2

		# line AD
		x1 = first_point
		stat_y1 = pointExtremeInOpenOrClose(x1, 'pitchfork')
		
		if(stat_y1 == ''):
			raise Exception("Hi Gowtham!!! Pitchfork: Point is not within Extreme Point getAndrewPitchforkLines() ")

		y1 = function_initial_data[stat_y1].iloc[x1]

		x2 = mid_x
		y2 = mid_y

		pitchfork_starting_point = x1

		if((x2 + PITCHFORK_EXTEND_LENGTH) < (SCAN_LENGTH + EXTEND_LENGTH)):
			pitchfork_ending_point = x2 + PITCHFORK_EXTEND_LENGTH
		else: 
			pitchfork_ending_point = SCAN_LENGTH + EXTEND_LENGTH

		if(abs(y1 - y2) < PITCHFORK_MINIMUM_BC_HEIGHT):
			# helow there
			continue

		# line_AD = getOneLine(x1, y1, x2, y2, starting_point = pitchfork_starting_point, ending_point = pitchfork_ending_point)
		line_AD = getOneLine(x1, y1, x2, y2, starting_point = pitchfork_starting_point)

		# check BC to AD(to midpoint) ratio

		a_mid = abs(first_point - second_point)
		b_c = abs(second_point - third_point)

		if((a_mid/PITCHFORK_TAIL_TO_FORK_WIDTH) > b_c):
			continue


		# Parallel lines 
		# x1, y1, x2, y2 are from AD point ( since it is parallel line )

		# Parallel line from second point 
		xx = second_point 
		stat_y1 = pointExtremeInOpenOrClose(xx, 'pitchfork')
		yy = function_initial_data[stat_y1].iloc[xx]

		starting_point = xx

		# second_parallel_line = getOneParallelLine(x1, y1, x2, y2, xx, yy, starting_point = starting_point, ending_point = pitchfork_ending_point)
		second_parallel_line = getOneParallelLine(x1, y1, x2, y2, xx, yy, starting_point = starting_point)
		
		# parallel line from third point
		xx = third_point 
		stat_y1 = pointExtremeInOpenOrClose(xx, 'pitchfork')
		yy = function_initial_data[stat_y1].iloc[xx]

		starting_point = xx

		# third_parallel_line = getOneParallelLine(x1, y1, x2, y2, xx, yy, starting_point = starting_point, ending_point = pitchfork_ending_point)
		third_parallel_line = getOneParallelLine(x1, y1, x2, y2, xx, yy, starting_point = starting_point)

		# plt.plot(range(len(line_BC)), line_BC)
		# plt.plot(range(len(line_AD)), line_AD)
		# plt.plot(range(len(second_parallel_line)), second_parallel_line)
		# plt.plot(range(len(third_parallel_line)), third_parallel_line)

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

def getWilliamRAtPointOscillator(x_point):
	william_data = function_initial_data['close'].iloc[x_point-14:x_point]
	william_list = list(william_data)

	highest_high = max(william_list)
	lowest_low = min(william_list)
	last_x = x_point - 1
	last_close = function_initial_data['close'].iloc[last_x]

	william_percent_range = (highest_high - last_close) / (highest_high - lowest_low)

	return william_percent_range

def getWilliamROscillator():
	global william_r_oscillator
	william_data = function_initial_data['close'].iloc[14:SCAN_LENGTH]
	william_r_oscillator = [None] * (SCAN_LENGTH+EXTEND_LENGTH)
	# william_r_oscillator = [0] * 14
	for i in range(14, len(william_data)+14):
		william_percent_range = getWilliamRAtPointOscillator(i)
		# william_r_oscillator.append(william_percent_range)
		william_r_oscillator[i] = william_percent_range
		# print(william_percent_range)

	# print(len(william_r_oscillator))
	# print(max(william_r_oscillator))
	# print(min(william_r_oscillator))
	return william_r_oscillator

def sumOfIndividualForNCandles(rsi_range, x_point):
	sum_data = function_initial_data['close'].iloc[x_point-rsi_range:x_point]
	sum_data = list(sum_data)
	totalUps = totalDowns = float(0.00)

	for i in range(1, len(sum_data)):
		last_close = sum_data[i-1]
		current_close = sum_data[i]
		if(current_close > last_close):
			totalUps = totalUps + ( current_close - last_close )
		elif(last_close > current_close):
			totalDowns = totalDowns + ( last_close - current_close )
	
	return totalUps, totalDowns

def getRSIAtPointOscillator(x_point):
	# find RS
	## find total upward, downward price movement in last 14 candles
	totalUps, totalDowns = sumOfIndividualForNCandles(14, x_point)

	RS = totalUps / totalDowns

	# find RSI
	RSI = 100 - (100 / (1 + RS))

	return RSI

def getRSIOscillator():
	global rsi_oscillator
	rsi_data = function_initial_data['close'].iloc[14:SCAN_LENGTH]
	rsi_oscillator = [None] * (SCAN_LENGTH+EXTEND_LENGTH)
	# rsi_oscillator = [0] * 14
	for i in range(14, len(rsi_data)+14):
		rsi = getRSIAtPointOscillator(i)
		rsi = rsi * 0.01
		# rsi_oscillator.append(rsi)
		rsi_oscillator[i] = rsi
		# print(william_percent_range)

	# print(len(rsi_oscillator))
	# print(max(rsi_oscillator))
	# print(min(rsi_oscillator))
	return rsi_oscillator

def getStochasticAtPointOscillator(x_point):
	stochastic_data = function_initial_data['close'].iloc[x_point-14:x_point]
	stochastic_list = list(stochastic_data)

	highest_high = max(stochastic_list)
	lowest_low = min(stochastic_list)
	last_x = x_point - 1
	last_close = function_initial_data['close'].iloc[last_x]

	# stochastic_range = (highest_high - last_close) / (highest_high - lowest_low)
	stochastic_range = (last_close - lowest_low) / (highest_high - lowest_low)

	return stochastic_range

def getStochasticOscillator():
	global stochastic_oscillator
	william_data = function_initial_data['close'].iloc[14:SCAN_LENGTH]
	stochastic_oscillator = [None] * (SCAN_LENGTH+EXTEND_LENGTH)
	# stochastic_oscillator = [0] * 14
	for i in range(14, len(william_data)+14):
		stochastic = getWilliamRAtPointOscillator(i)
		# stochastic_oscillator.append(stochastic)
		stochastic_oscillator[i] = stochastic
		# print(william_percent_range)

	# print(len(stochastic_oscillator))
	# print(max(stochastic_oscillator))
	# print(min(stochastic_oscillator))
	return stochastic_oscillator

def getOBVAtPointOscillator(x_point):
	global obv_oscillator
	len_obv_oscillator = len(obv_oscillator)
	if(len_obv_oscillator <= 0):
		getOBVOscillator()

	if(len_obv_oscillator > 0):
		if(len_obv_oscillator > x_point):
			return len_obv_oscillator[x_point]
		
	return False

def getOBVOscillator():
	global obv_oscillator
	obv_data = function_initial_data.iloc[:SCAN_LENGTH]
	obv = [None] * (SCAN_LENGTH+EXTEND_LENGTH)
	obv[0] = 0
	for i in range(1, SCAN_LENGTH-1):
		last_close = obv_data['close'].iloc[i-1]
		current_close = obv_data['close'].iloc[i]
		current_volume = obv_data['volume'].iloc[i]

		if(last_close > current_close):
			current_obv = obv[i-1] - current_volume
		elif(last_close < current_close):
			current_obv = obv[i-1] + current_volume
		else:
			current_obv = obv[i-1]
		
		obv[i] = current_obv

	obv = np.array(obv)
	obv = np.linalg.norm(obv)
	obv_oscillator = obv
	print(obv_oscillator)

	return obv_oscillator

def getAllAtPointValue():
	# Trend Line
	# Support Resistance
	# Pitchfork
	# Oscillators
	# Candle Pattern


if __name__ == "__main__":
	DATA_STARTING_POINT = 200
	function_initial_data = function_initial_data.iloc[DATA_STARTING_POINT:DATA_STARTING_POINT+SCAN_LENGTH+EXTEND_LENGTH]
	# function_initial_data = function_initial_data.iloc[200:200+SCAN_LENGTH+EXTEND_LENGTH]
	# function_initial_data = function_initial_data.iloc[150:150+SCAN_LENGTH+EXTEND_LENGTH]
	# function_initial_data = function_initial_data.iloc[250:250+SCAN_LENGTH+EXTEND_LENGTH]
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

	# getWilliamROscillator()
	# selectPlotCandleStickGraph = ['william_r']
	# plotCandleStickGraph(selectPlotCandleStickGraph)

	# getRSIOscillator()
	# selectPlotCandleStickGraph = ['rsi']
	# plotCandleStickGraph(selectPlotCandleStickGraph)
	
	# getStochasticOscillator()
	# selectPlotCandleStickGraph = ['stochastic']
	# plotCandleStickGraph(selectPlotCandleStickGraph)
	
	getOBVOscillator()
	selectPlotCandleStickGraph = ['obv']
	plotCandleStickGraph(selectPlotCandleStickGraph)
	exit()


	getMinimaPoints()
	getMaximaPoints()
	getExtremePoints()
	getAllPoints()
	# getAllLinesForExtremePoints()
	getSupportAndResistanceLines()

	MIN_MAX_EXTREME = ['min', 'max']
	getAllLinesForExtremePoints()

	getMinimaPoints(set_global_variable = 'pitchfork')
	getMaximaPoints(set_global_variable = 'pitchfork')
	getExtremePoints(set_global_variable = 'pitchfork')
	getAllPoints()
	# getAllPoints(set_global_variable = ['pitchfork'])

	getAndrewPitchforkPoints()	
	# print(pt)
	# exit()
	getAndrewPitchforkLines(withTypes = ['andrew'])

	# selectPlotCandleStickGraph = ['points', 'pitchfork']
	# selectPlotCandleStickGraph = ['points', 'lines', 'pitchfork']
	# selectPlotCandleStickGraph = ['points', 'support_resistance', 'pitchfork', 'lines']
	# selectPlotCandleStickGraph = ['points', 'support_resistance', 'lines']
	# selectPlotCandleStickGraph = ['points', 'lines']
	selectPlotCandleStickGraph = ['william_r']
	

	# print(all_points)
	# print(all_extremes)
	# print(all_pitchfork_points)
	# print(all_extremes_pitchfork)

	plotCandleStickGraph(selectPlotCandleStickGraph)

	# a = [[242, 212, 242], [173, 212, 242], [110, 212, 242], [77, 212, 242], [242, 194, 242], [173, 194, 242], [110, 194, 242], [242, 131, 242], [173, 131, 242], [242, 94, 242], [242, 44, 242], [242, 212, 173], [173, 212, 173], [110, 212, 173], [77, 212, 173], [242, 194, 173], [173, 194, 173], [110, 194, 173], [242, 131, 173], [173, 131, 173], [242, 212, 110], [173, 212, 110], [110, 212, 110], [77, 212, 110], [242, 194, 110], [173, 194, 110], [110, 194, 110], [242, 212, 77], [173, 212, 77], [110, 212, 77], [77, 212, 77]]

	# a = np.array(a)
	# print(len(a))
	# b = np.unique(a, axis=0)
	# print(len(b))






























