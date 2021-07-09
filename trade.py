import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 

# from matplotlib.finance import candlestick_ohlc
import plotly.graph_objects as go 
from datetime import datetime

# from mplfinance import candlestick_ohlc


# data = pd.read_csv('../../data/eurusd_col_m1_500.csv')

# close = data['close']

import mplfinance as mpf

# constant area
ROUND_DIGITS = 5
IGNORE_CANDLE_STATUS = False
MIN_SHAVEN_BODY = 1 * ROUND_DIGITS
MAX_STAR_BODY = 10 * (10 ** -ROUND_DIGITS)

# print(MAX_STAR_BODY)
# exit()

def findTrend(data):
	if(data[0] < data[len(data)-1]):
		return 'uptrend'
	else:
		return 'downtrend'

def findSingleCandleStructure(data):
	open, high, low, close, volume = [round(data[i], ROUND_DIGITS) for i in range(len(data))]

	patterns = []
	MIN_SHADOW = 10

	MIN_SHADOW_VALUE = MIN_SHADOW * ROUND_DIGITS

	candle_status = 'bullish' if(close > open) else 'bearish'

	candle_body = round(abs(open - close), ROUND_DIGITS)
	if(candle_status == 'bearish'):
		upper_shadow = round(abs(open - high), ROUND_DIGITS)
		lower_shadow = round(abs(close - low), ROUND_DIGITS)
	elif(candle_status == 'bullish'):
		upper_shadow = round(abs(close - high), ROUND_DIGITS)
		lower_shadow = round(abs(open - low), ROUND_DIGITS)

	if(open == close):
		patterns.append('doji')

	if(not('doji' in patterns)):
		if((candle_body < 2*lower_shadow) and (upper_shadow < lower_shadow) and (upper_shadow < MIN_SHADOW_VALUE) and (lower_shadow > candle_body) and (candle_status == 'bullish' or IGNORE_CANDLE_STATUS)):
			patterns.append('hammer')

		if((candle_body < 2*lower_shadow) and (upper_shadow < lower_shadow) and (upper_shadow < MIN_SHADOW_VALUE) and (lower_shadow > candle_body) and (candle_status == 'bearish' or IGNORE_CANDLE_STATUS)):
			patterns.append('hanging_man')

		if((candle_body < 2*upper_shadow) and (upper_shadow > lower_shadow) and (lower_shadow < MIN_SHADOW_VALUE) and (upper_shadow > candle_body) and (candle_status == 'bullish' or IGNORE_CANDLE_STATUS)):
			patterns.append('inverted_hammer')

		if((candle_body < 2*upper_shadow) and (upper_shadow > lower_shadow) and (lower_shadow < MIN_SHADOW_VALUE) and (upper_shadow > candle_body) and (candle_status == 'bearish' or IGNORE_CANDLE_STATUS)):
			patterns.append('shooting_star')

		if((candle_body > upper_shadow) and (candle_body > lower_shadow) and (lower_shadow < MIN_SHADOW_VALUE) and (upper_shadow < MIN_SHADOW_VALUE) and (candle_body > 0.0001)):
			patterns.append('shaven_shadows')

		max_star_body = 5 * (10 ** -ROUND_DIGITS)
		if((candle_body < max_star_body)):
			if((upper_shadow < candle_body) and (lower_shadow < candle_body) and (not 'hammer' in patterns) and (not 'hanging_man' in patterns) and (not 'inverted_hammer' in patterns) and (not 'shooting_star' in patterns)):
				patterns.append('ideal_star')
			else:
				patterns.append('star')


	# print(candle_body, upper_shadow, lower_shadow, patterns, candle_status)
	return patterns, candle_status, upper_shadow, candle_body, lower_shadow



def plotSingleCandlePerChart(signal, padding_data, predictions, patterns):
	no_of_bullish = predictions.count('bullish')
	no_of_bearish = predictions.count('bearish')

	if(no_of_bullish == no_of_bearish):
		return False 

	if(no_of_bullish > no_of_bearish):
		marker = '^'
		color = 'green'
		pred = 'buy'
	else:
		marker = 'v'
		color = 'red'
		pred = 'sell'

	title = ' | '.join(map(str, patterns))

	# si = mpf.make_addplot(pd.DataFrame(signal, dtype="float"), type='scatter',markersize=200,marker='^')
	si = mpf.make_addplot(pd.DataFrame(signal, dtype="float"), type='scatter',markersize=200,marker=marker, color=color)

	# mpf.plot(padding_data, addplot=si, type='candle', style="yahoo", title=title)
	mpf.plot(padding_data, addplot=si, type='candle', title=title)



def trade():
	# df = pd.read_csv("../../data/eurusd_col_m1_500.csv")
	# df = pd.read_csv("../../data/eur_usd_m1_2000.csv")
	# df = pd.read_csv("../../data/eurusd_m1_7000.csv")
	# df = pd.read_csv("../../data/eurusd_col_y1.csv")
	df = pd.read_csv("../../data/eurusd_col_m1_new.csv")
	# df = df.iloc[:50, :]


	df.Datetime = pd.to_datetime(df.Datetime)

	df = df.set_index('Datetime')
	data = df

	round_digits = 5

	signal = []
	max_of_min_tail_length = 0.0002
	no_of_patterns = 0
	no_of_win = 0
	no_of_loss = 0
	ratio = 2

	for j in range(len(df)-51):
		i = j+50
		# body of candle
		diff_open_close = round(abs(data['open'][i] - data['close'][i]), round_digits)
		# print(i)
		# tail of candle possibilities
		diff_close_low = round(abs(data['close'][i] - data['low'][i]), round_digits)
		diff_close_high = round(abs(data['close'][i] - data['high'][i]), round_digits)
		diff_open_low = round(abs(data['open'][i] - data['low'][i]), round_digits)
		diff_open_high = round(abs(data['open'][i] - data['high'][i]), round_digits)

		# candle body height
		diff_open_close = round(abs(data['open'][i] - data['close'][i]), round_digits)

		max_of_min_tail_length = diff_open_close

		vol = round(abs(data['close'][i-1] - data['open'][i]), round_digits)

		trend = findTrend(data['close'][i-5:i])

		n_structure, n_status, n_upper_shadow, n_candle_body, n_lower_shadow = findSingleCandleStructure(data.iloc[i])
		n_minus_one_structure, n_minus_one_status, n_minus_one_upper_shadow, n_minus_one_candle_body, n_minus_one_lower_shadow = findSingleCandleStructure(data.iloc[i-1])
		n_minus_two_structure, n_minus_two_status, n_minus_two_upper_shadow, n_minus_two_candle_body, n_minus_two_lower_shadow = findSingleCandleStructure(data.iloc[i-2])
		n_minus_three_structure, n_minus_three_status, n_minus_three_upper_shadow, n_minus_three_candle_body, n_minus_three_lower_shadow = findSingleCandleStructure(data.iloc[i-3])

		last_I = 0
		considerTweezer = True
		considerCounterBearishAttack = True
		considerCounterBullishAttack = True

		# print(str(i) + '/' + str(len(df)-50))
		if(len(n_structure) > 0):
			# print('No of Patterns for this candle: ' + str(len(n_structure)))
			# print(n_structure, last_candle_structure)
			for index in range(len(n_structure)):
				plot = False
				predictions = []
				patterns = []

				"""
				# Predict Patterns
				# Hammer
				if((n_structure[index] == 'hammer') and (trend == 'downtrend') and (not(('shaven_shadows' in n_minus_one_structure) and (n_minus_one_status == 'bearish')))):
					plot = True
					predictions.append('bullish')
					patterns.append('bullish_hammer')

				# Inverted Hammer
				if((n_structure[index] == 'inverted_hammer') and (trend == 'downtrend') and (not(('shaven_shadows' in n_minus_one_structure) and (n_minus_one_status == 'bearish')))):
					plot = True
					predictions.append('bullish')
					patterns.append('bullish_inverted_hammer')

				# Hanging Man
				if((n_structure[index] == 'hanging_man') and (trend == 'uptrend') and (not(('shaven_shadows' in n_minus_one_structure) and (n_minus_one_status == 'bullish')))):
					plot = True
					predictions.append('bearish')
					patterns.append('bearish_hanging_man')

				# Shooting Star
				if((n_structure[index] == 'shooting_star') and (trend == 'uptrend') and (not(('shaven_shadows' in n_minus_one_structure) and (n_minus_one_status == 'bullish')))):
					plot = True
					predictions.append('bearish')
					patterns.append('bearish_shooting_star')
				
				# Engulfing
				if((n_structure[index] == 'shaven_shadows') and ('shaven_shadows' in n_minus_one_structure)):
					# Bullish Engulfing
					if((trend == 'downtrend') and (n_minus_one_status == 'bearish') and (n_status == 'bullish') and (data['open'][i-1] < data['close'][i]) and (data['close'][i-1] > data['open'][i])):
						plot = True 
						predictions.append('bullish')
						patterns.append('bullish_engulfing')

					# Bearish Engulfing
					if((trend == 'uptrend') and (n_minus_one_status == 'bullish') and (n_status == 'bearish') and (data['open'][i-1] > data['close'][i]) and (data['close'][i-1] < data['open'][i])):
						plot = True 
						predictions.append('bearish')
						patterns.append('bearish_engulfing')


				# Dark Cloud
				if((n_structure[index] == 'shaven_shadows') and ('shaven_shadows' in n_minus_one_structure) and (trend == 'uptrend') and (n_minus_one_status == 'bullish') and (n_status == 'bearish')):
					n_minus_one_half_point = (data['close'][i-1] + data['open'][i-1]) / 3
					if((data['open'][i-1] < data['close'][i]) and (data['close'][i-1] < data['open'][i]) and (data['close'][i] < n_minus_one_half_point)):
						plot = True 
						predictions.append('bearish')
						patterns.append('dark_cloud')
				

				# Piercing
				if((n_structure[index] == 'shaven_shadows') and ('shaven_shadows' in n_minus_one_structure) and (trend == 'downtrend') and (n_minus_one_status == 'bearish') and (n_status == 'bullish')):
					n_minus_one_half_point = (data['close'][i-1] + data['open'][i-1]) / 2
					if((data['open'][i-1] > data['close'][i]) and (data['close'][i-1] > data['open'][i]) and (data['close'][i] > n_minus_one_half_point)):
						plot = True 
						predictions.append('bullish')
						patterns.append('Piercing')
				

				# Morning Star
				if((trend == 'downtrend') and (n_minus_two_status == 'bearish') and (n_minus_one_status == 'bearish') and (n_status == 'bullish')):
					if(('shaven_shadows' in n_minus_two_structure) and (n_minus_one_candle_body < MAX_STAR_BODY)  and (n_minus_one_candle_body != 0) and (n_structure[index] == 'shaven_shadows')):
						if((data['open'][i-1]) < (data['close'][i]) and (data['open'][i-1] < data['close'][i-2])  and (data['close'][i] < data['open'][i-2])):
							plot = True 
							predictions.append('bullish')
							patterns.append('morning_star')

				# Evening Star
				if((trend == 'uptrend') and (n_minus_two_status == 'bullish') and (n_minus_one_status == 'bullish') and (n_status == 'bearish')):
					if(('shaven_shadows' in n_minus_two_structure) and (n_minus_one_candle_body < MAX_STAR_BODY)  and (n_minus_one_candle_body != 0) and (n_structure[index] == 'shaven_shadows')):
						if((data['close'][i-1]) > (data['open'][i]) and (data['open'][i-1] > data['close'][i-2])  and (data['close'][i] > data['open'][i-2])):
							plot = True
							predictions.append('bearish')
							patterns.append('evening_star')
				
				# Morning doji
				if((trend == 'downtrend') and ('doji' in n_minus_one_structure) and (n_minus_two_status == 'bearish') and (n_minus_one_status == 'bearish') and (n_status == 'bullish')):
					if(('shaven_shadows' in n_minus_two_structure) and (n_structure[index] == 'shaven_shadows')):
						if((data['open'][i-1]) < (data['close'][i]) and (data['open'][i-1] < data['close'][i-2])  and (data['close'][i] < data['open'][i-2])):
							plot = True 
							predictions.append('bullish')
							patterns.append('morning_doji')
				
				# Evening doji
				if((trend == 'uptrend') and ('doji' in n_minus_one_structure) and (n_minus_two_status == 'bullish') and (n_minus_one_status == 'bullish') and (n_status == 'bearish')):
					if(('shaven_shadows' in n_minus_two_structure) and (n_structure[index] == 'shaven_shadows')):
						if((data['close'][i-1]) > (data['open'][i]) and (data['open'][i-1] > data['close'][i-2])  and (data['close'][i] > data['open'][i-2])):
							plot = True
							predictions.append('bearish')
							patterns.append('evening_doji')
				

				# Harami 
				if(('shaven_shadows' in n_minus_one_structure) and ((n_structure[index] == 'star') or (n_structure[index] == 'ideal_star'))):
					# Bearish Harami
					if((trend == 'uptrend') and (n_minus_one_status == 'bullish') and (n_status == 'bearish')):
						if((data['open'][i-1] < data['high'][i]) and (data['open'][i-1] < data['low'][i]) and (data['close'][i-1] > data['high'][i]) and (data['close'][i-1] > data['low'][i])):
							plot = True 
							predictions.append('bearish')
							patterns.append('bearish_harami')

					# Bullish Harami
					if((trend == 'downtrend') and (n_minus_one_status == 'bearish') and (n_status == 'bullish')):
						if((data['open'][i-1] > data['high'][i]) and (data['open'][i-1] > data['low'][i]) and (data['close'][i-1] < data['high'][i]) and (data['close'][i-1] < data['low'][i])):
							plot = True 
							predictions.append('bullish')
							patterns.append('bullish_harami')
				

				# Harami Cross
				if(('shaven_shadows' in n_minus_one_structure) and (n_structure[index] == 'doji')):
					# Bearish Harami Cross
					if((trend == 'uptrend') and (n_minus_one_status == 'bullish')):
						if((data['open'][i-1] < data['high'][i]) and (data['open'][i-1] < data['low'][i]) and (data['close'][i-1] > data['high'][i]) and (data['close'][i-1] > data['low'][i])):
							plot = True 
							predictions.append('bearish')
							patterns.append('bearish_harami_cross')

					# Bullish Harami Cross
					if((trend == 'downtrend') and (n_minus_one_status == 'bearish')):
						if((data['open'][i-1] > data['high'][i]) and (data['open'][i-1] > data['low'][i]) and (data['close'][i-1] < data['high'][i]) and (data['close'][i-1] < data['low'][i])):
							plot = True 
							predictions.append('bullish')
							patterns.append('bullish_harami_cross')

				

				# Tweezers
				if((considerTweezer == True) and ('shaven_shadows' in n_minus_one_structure)):
					# Bearish Tweezer Top
					if((n_minus_one_status == 'bullish') and (n_status == 'bearish')):
						if((data['high'][i-1] == data['high'][i]) and (trend == 'uptrend')):
							plot = True 
							predictions.append('bearish')
							patterns.append('bearish_tweezer_top')
							considerTweezer = False

					# Bullish Tweezer Bottom
					if((n_minus_one_status == 'bearish') and (n_status == 'bullish')):
						if((data['low'][i-1] == data['low'][i]) and (trend == 'downtrend')):
							plot = True 
							predictions.append('bullish')
							patterns.append('bullish_tweezer_bottom')
							considerTweezer = False

				

				# Three Black Crows
				if((trend == 'uptrend') and (n_status == 'bearish') and (n_minus_one_status == 'bearish') and (n_minus_two_status == 'bearish') and (n_minus_three_status == 'bullish')):
					if((n_structure[index] == 'shaven_shadows') and ('shaven_shadows' in n_minus_one_structure) and ('shaven_shadows' in n_minus_two_structure)):
						plot = True 
						predictions.append('bearish')
						patterns.append('three_black_crows')


				# Three White Soldiers
				if((trend == 'downtrend') and (n_status == 'bullish') and (n_minus_one_status == 'bullish') and (n_minus_two_status == 'bullish') and (n_minus_three_status == 'bearish')):
					if((n_structure[index] == 'shaven_shadows') and ('shaven_shadows' in n_minus_one_structure) and ('shaven_shadows' in n_minus_two_structure)):
						plot = True 
						predictions.append('bullish')
						patterns.append('three_white_soldiers')

				

				# # Bearish CounterAttack Line
				# # # # # if((n_structure[index] == 'shaven_shadows') and ('shaven_shadows' in n_minus_one_structure)):
				# if((considerCounterBearishAttack == True) and (n_status == 'bearish') and (n_minus_one_status == 'bullish') and (not 'doji' in n_structure[index])):
				# 	if((data['close'][i-1] == (data['close'][i]))):
				# 		plot = True 
				# 		predictions.append('bearish')
				# 		patterns.append('bearish_counter_attack')
				# 		considerCounterBearishAttack = False

				

				# # Bullish CounterAttack Line
				# # # # # if((n_structure[index] == 'shaven_shadows') and ('shaven_shadows' in n_minus_one_structure)):
				# if((considerCounterBullishAttack == True) and (n_status == 'bullish') and (n_minus_one_status == 'bearish') and (not 'doji' in n_minus_one_structure)):
				# 	if((data['close'][i-1] == (data['close'][i]))):
				# 		plot = True 
				# 		predictions.append('bullish')
				# 		patterns.append('bullish_counter_attack')
				# 		considerCounterBullishAttack = False

				"""


				if(plot):
					real = 'bullish' if(data['open'][i+1] < data['close'][i+1]) else 'bearish'
	
					no_of_patterns = no_of_patterns + 1

					# if(predictions == real):
					if(real in predictions):
						no_of_win = no_of_win + 1
					else:
						no_of_loss = no_of_loss + 1

					# if(len(predictions) > 1):
					print(str(i) + '. No of Trades: ' + str(no_of_patterns) + '| No of Win: ' + str(no_of_win) + '| No of Loss: ' + str(no_of_loss) + ' | Win Percentage: ' + str((no_of_win/no_of_patterns)*100))
					# print(predictions)
					# print('/n')

					si_val = np.full([60], False)

					si_val[30] = round(df.iloc[i,3] * 0.99, round_digits)

					padding_data = df.iloc[i-30:i+30,:]

					signal = si_val

					# if(not real in predictions):
					# plotSingleCandlePerChart(signal, padding_data, predictions, patterns)


				last_I = i

trade()

print('done')



