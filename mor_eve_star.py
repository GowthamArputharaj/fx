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

df = pd.read_csv("../../data/eurusd_col_m1_500.csv")
# df = df.iloc[:50, :]

df.Datetime = pd.to_datetime(df.Datetime)

df = df.set_index('Datetime')
data = df

round_digits = 5

signal = []
max_of_min_tail_length = 0.0002
no_of_patters = 0
no_of_win = 0
no_of_loss = 0
ratio = 2

for j in range(len(df)-50):
	i = j+50
	# body of candle
	diff_open_close = round(abs(data['open'][i] - data['close'][i]), round_digits)

	# tail of candle possibilities
	diff_close_low = round(abs(data['close'][i] - data['low'][i]), round_digits)
	diff_close_high = round(abs(data['close'][i] - data['high'][i]), round_digits)
	diff_open_low = round(abs(data['open'][i] - data['low'][i]), round_digits)
	diff_open_high = round(abs(data['open'][i] - data['high'][i]), round_digits)

	# candle body height
	diff_open_close = round(abs(data['open'][i] - data['close'][i]), round_digits)

	max_of_min_tail_length = diff_open_close

	vol = round(abs(data['close'][i-1] - data['open'][i]), round_digits)


	# if(((diff_close_high > 2*diff_open_close) or (diff_close_low > 2*diff_open_close) or (diff_open_high > 2*diff_open_close) or (diff_open_low > 2*diff_open_close)) and ((diff_open_high < max_of_min_tail_length) or (diff_open_low < max_of_min_tail_length) or (diff_close_high < max_of_min_tail_length) or (diff_close_low < max_of_min_tail_length))):
	if(((diff_close_high > ratio*diff_open_close) or (diff_close_low > ratio*diff_open_close) or (diff_open_high > ratio*diff_open_close) or (diff_open_low > ratio*diff_open_close)) and ((diff_open_high < max_of_min_tail_length) or (diff_open_low < max_of_min_tail_length) or (diff_close_high < max_of_min_tail_length) or (diff_close_low < max_of_min_tail_length))):
		
		si_val = np.full([60], False)
		# si_val = df.iloc[i-30:i+30,[0,3]]
		# si_val[i-30:i+30,3] = np.full([60], False)

		si_val[30] = round(df.iloc[i,3] * 0.99, round_digits)

		ok = df.iloc[i-30:i+30,:]

		signal = si_val

		marker = 'v'
		color = 'red'
		pred = 'sell'

		diff_last_five = round(abs(data['close'][i-5] - data['close'][i]), round_digits)
		diff_last_five = data['close'][i-5] < data['close'][i]
		# last_candle_high_or_low = data['open'][i-1] > data['close'][i-1]

		# if(data['open'][i-1] > data['close'][i-1]):
		 # can check trend of two candles instead of last candle black or white
		 # like if yesterday open is higher than today open is downtrend and viseversa
		 # if yesterday open is lower than today open is uptrend

		# if((data['open'][i-1] > data['close'][i-1]) and (diff_last_five)):
		if((data['open'][i-1] > data['close'][i-1])):
			marker = '^'
			color = 'green'
			pred = 'buy'

		# si = mpf.make_addplot(pd.DataFrame(signal, dtype="float"), type='scatter',markersize=200,marker='^')
		si = mpf.make_addplot(pd.DataFrame(signal, dtype="float"), type='scatter',markersize=200,marker=marker, color=color)

		truth = 'sell'
		if(data['close'][i] < data['close'][i+1]):
			truth = 'buy'

		if(truth == pred):
			no_of_win = no_of_win + 1
		else:
			no_of_loss = no_of_loss + 1

		no_of_patters = no_of_patters + 1
		print(str(i) + '   ' + str(no_of_patters) + pred + ' ' + truth + ' ' + str(no_of_win) + ' ' + str(no_of_loss))

		# if(truth != pred):
		mpf.plot(ok, addplot=si, type='candle', style="yahoo")



print('done')



