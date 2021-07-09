import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 
import mplfinance as mpf

import plotly.graph_objects as go 
from datetime import datetime

import matplotlib.pyplot as plt 
from scipy.signal import argrelextrema

# constant area
LINE_EXTEND_LENGTH = 60

DATA_LENGTH = 500

df = pd.read_csv("../../data/eurusd_col_m1_new.csv")

df = df.iloc[:DATA_LENGTH]

df.Datetime = pd.to_datetime(df.Datetime)
df = df.set_index('Datetime')


data = df.iloc[:500]


def findMinMax(data, order):
	max_idx = list(argrelextrema(np.array(data['close']), np.greater, order=order)[0])
	min_idx = list(argrelextrema(np.array(data['close']), np.less, order=order)[0])

	idx = max_idx + min_idx

	idx.sort()

	return min_idx, max_idx, idx 


def getLine(first_min, second_min, m, b):
	line_length = second_min - first_min

	# line_length_e = line_length + LINE_EXTEND_LENGTH
	# line_length_e = second_min + LINE_EXTEND_LENGTH

	line_length_e = second_min - first_min + LINE_EXTEND_LENGTH

	line = [0] * line_length_e
	ln = line
	
	for i in range(len(ln)):
		j = i + first_min
		ln[i] = (m * j) + b
		ln[i] = ln[i]

	ln[0] = data['close'].iloc[first_min]
	ln[second_min-first_min] = data['close'].iloc[second_min]

	return ln



def plotTrendLines():
	order = 10
	min_max_data_len = len(data) - LINE_EXTEND_LENGTH
	min_max_data = data.iloc[:min_max_data_len]
	min_idx, max_idx, idx = findMinMax(min_max_data, order)

	# print(min_idx)
	# exit()
	# min_idx = idx
	# min_idx = max_idx
	addplots = []

	for i in range(len(min_idx)-1):

		first_min = min_idx[i]
		second_min = min_idx[i+1]

		line_eqn = 0

		x1 = first_min
		y1 = data['close'].iloc[first_min]
		x2 = second_min
		y2 = data['close'].iloc[second_min]

		print(x1, y1, x2, y2)

		# slope
		m = (y2 - y1) / (x2 - x1)

		# intercept
		b = y1 - (m * x1)

		ln = getLine(first_min, second_min, m, b)
		line = ln

		# midpoint
		mid_x = (x1 + x2) / 2
		mid_y = (y1 + y2) / 2

		addplots = []


		# pts = [None] * len(data)
		pts = [None] * (second_min - first_min + LINE_EXTEND_LENGTH)
		# pts = [None] * (second_min + LINE_EXTEND_LENGTH )
		# if(len(pts) > DATA_LENGTH):
		# 	pts = [None] * 	(DATA_LENGTH - second_min)

		pts[0] = data['close'].iloc[first_min]
		pts[second_min-first_min] = data['close'].iloc[second_min]

		pt = mpf.make_addplot(pd.DataFrame(pts, dtype="float"), type="scatter", color="red")
		si = mpf.make_addplot(pd.DataFrame(ln, dtype="float"), type='line', width=0.7, alpha=0.5, color="blue")

		addplots.append(pt)
		addplots.append(si)

		# mpf.plot(data.iloc[:len(ln)], addplot=addplots, type='candle', style="yahoo")
		mpf.plot(data.iloc[first_min:(second_min+LINE_EXTEND_LENGTH)], addplot=addplots, type='candle', style="yahoo")

		plt.show()


plotTrendLines()


print('end')









