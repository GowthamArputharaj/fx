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



df = pd.read_csv("../../data/eurusd_col_m1_new.csv")

df = df.iloc[:500]

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
	line_length_e = line_length + LINE_EXTEND_LENGTH

	line_length_e = second_min + LINE_EXTEND_LENGTH

	line = [0] * line_length_e
	ln = line
	
	ln[0] = data['close'].iloc[first_min]
	ln[line_length-1] = data['close'].iloc[second_min]

	for i in range(len(ln)):
		if(i != first_min and i != second_min):
			ln[i] = (m * i) + b

		if(i == first_min):
			ln[i] = data['close'].iloc[first_min]

		if(i == second_min):
			ln[i] = data['close'].iloc[second_min]

	return ln



def plotTrendLines():
	order = 10
	min_max_data_len = len(data) - LINE_EXTEND_LENGTH + 1
	min_max_data = data.iloc[:min_max_data_len]
	min_idx, max_idx, idx = findMinMax(min_max_data, order)

	# print(min_idx)
	# exit()
	# min_idx = idx
	addplots = []

	for i in range(len(min_idx)-1):

		first_min = min_idx[i]
		second_min = min_idx[i+1]

		# plot one support line
		# print(first_min, second_min)
		# print('_____')
		line_eqn = 0

		x1 = first_min
		y1 = data['close'].iloc[first_min]
		x2 = second_min
		y2 = data['close'].iloc[second_min]

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
		# pts = [None] * (second_min - first_min + LINE_EXTEND_LENGTH)
		pts = [None] * len(ln)
		print(len(pts), len(ln))
		pts[first_min] = data['close'].iloc[first_min]
		pts[second_min] = data['close'].iloc[second_min]

		pt = mpf.make_addplot(pd.DataFrame(pts, dtype="float"), type="scatter", color="red")
		si = mpf.make_addplot(pd.DataFrame(ln, dtype="float"), type='line', width=0.7, alpha=0.5, color="blue")

		print(len(pts), len(ln))
		print('+++++++++++++++++++++++++++++++++++++++++')
		addplots.append(pt)
		addplots.append(si)

		# print(addplots)
		print('________-')
		# exit()
		# mpf.plot(data.iloc[:len(ln)], addplot=addplots, type='candle', style="yahoo")
		mpf.plot(data.iloc[:len(ln)], addplot=addplots, type='candle', style="yahoo")
			
		plt.show()
		print(')))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))');


plotTrendLines()


print('end')









