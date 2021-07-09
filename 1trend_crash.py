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
START_DATA_LENGTH = 0
END_DATA_LENGTH = START_DATA_LENGTH + DATA_LENGTH

all_lines = []
all_points = []

df = pd.read_csv("../../data/eurusd_col_m1_new.csv")

# dup_df = df.iloc[:500]
# dup_df.Datetime = pd.to_datetime(dup_df.Datetime)
# dup_df = dup_df.set_index('Datetime')

df = pd.read_csv("../../data/eurusd_col_m1_new.csv")

# df = df.iloc[:DATA_LENGTH]
df = df.iloc[START_DATA_LENGTH:END_DATA_LENGTH]

df.Datetime = pd.to_datetime(df.Datetime)
df = df.set_index('Datetime')

data = None

data = df.iloc[:DATA_LENGTH]



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
	# line_length_e = second_min - first_min + LINE_EXTEND_LENGTH

	line_length_e = len(data)

	line = [None] * line_length_e
	ln = line
	
	for i in range(len(ln)):
		# j = i + first_min
		# ln[i] = (m * j) + b
		ln[i] = (m * i) + b
		ln[i] = ln[i]

	ln[0] = data['close'].iloc[first_min]
	ln[second_min-first_min] = data['close'].iloc[second_min]
	all_lines.append(ln)

	return ln

def getPoint(first_pt, second_pt, length):
	pt = [None] * length 

	pt[first_pt] = data['close'].iloc[first_pt]
	pt[second_pt] = data['close'].iloc[second_pt]

	all_points.append(pt)


def getPoints(extremes, length):
	pts = [None] * length
	for i in range(len(extremes)-1):
		pts[extremes[i]] = data['close'].iloc[extremes[i]]
		getPoint(extremes[i], extremes[i+1], length)

	# all_points.append(pts)

	return pts

def getLines(extremes, length):
	# line = [None] * length 
	# print(length)
	line = []

	for i in range(len(extremes)-1):

		first_min = extremes[i]
		second_min = extremes[i+1]

		line_eqn = 0

		x1 = first_min
		y1 = data['close'].iloc[first_min]
		x2 = second_min
		y2 = data['close'].iloc[second_min]

		# print(x1, y1, x2, y2)

		# slope
		m = (y2 - y1) / (x2 - x1)

		# intercept
		b = y1 - (m * x1)

		ln = [None] * length

		for ln_i in range(len(ln)):
			ln[ln_i] = (m * ln_i) + b

		ln[first_min] = data['close'].iloc[first_min]
		ln[second_min] = data['close'].iloc[second_min]
		# print(len(ln))

		line.append(ln)
		all_lines.append(ln)

	return line

def plotTrendLines(start_extreme_pt, end_extreme_pt):
	all_lines = []
	all_points = []
	order = 10
	# min_max_data_len = len(data) - LINE_EXTEND_LENGTH
	# min_max_data = data.iloc[:min_max_data_len]
	min_max_data = data.iloc[start_extreme_pt:end_extreme_pt]
	min_idx, max_idx, idx = findMinMax(min_max_data, order)

	idx.sort()

	# print(min_idx)
	# exit()
	# min_idx = idx
	# min_idx = max_idx

	# plot for minimum ( support ) values

	# plot for maximum ( resistance ) values

	# plot for min max combo 

	# extremes = [min_idx, max_idx, idx]
	extremes = [min_idx, max_idx]
	extremes = [min_idx]
	scatter_colors = ['red', 'blue', 'green']
	line_colors = ['red', 'blue', 'green']

	addplots = []

	for i in range(len(extremes)):
		extreme = extremes[i]
		scatter_color = scatter_colors[i]
		line_color = line_colors[i]

		for i in range(len(extreme)-1):

			first_min = extreme[i]
			second_min = extreme[i+1]

			line_eqn = 0

			x1 = first_min
			y1 = data['close'].iloc[first_min]
			x2 = second_min
			y2 = data['close'].iloc[second_min]

			# print(x1, y1, x2, y2)

			# slope
			m = (y2 - y1) / (x2 - x1)

			# intercept
			b = y1 - (m * x1)

			# ln = getLine(first_min, second_min, m, b)
			# line = ln

			# midpoint
			mid_x = (x1 + x2) / 2
			mid_y = (y1 + y2) / 2


			# pts = [None] * len(data)
			# pts = [None] * (second_min - first_min + LINE_EXTEND_LENGTH)
			# pts = [None] * (second_min + LINE_EXTEND_LENGTH )
			# if(len(pts) > DATA_LENGTH):
			# 	pts = [None] * 	(DATA_LENGTH - second_min)

			# pts = [None] * len(data)

			# for points
			# pts[first_min] = data['close'].iloc[first_min]
			# pts[second_min] = data['close'].iloc[second_min]

			pts = getPoints(extreme, end_extreme_pt-start_extreme_pt)
			# pts = getPoints(extreme, len(data))
			pt = mpf.make_addplot(pd.DataFrame(pts, dtype="float"), type="scatter", color=scatter_color)
			addplots.append(pt)

			# lines = getLines(extreme, len(data))
			lines = getLines(extreme, end_extreme_pt-start_extreme_pt)
			# print(len(lines), len(lines[0]))
			for lines_i in range(len(lines)):
				si = mpf.make_addplot(pd.DataFrame(lines[lines_i], dtype="float"), type='line', width=0.7, alpha=0.5, color=line_color)
				addplots.append(si)


	# getLinePointsAtPoint(1)

	# TO PLOT
	# mpf.plot(data.iloc[:len(data)], addplot=addplots, type='candle', style="yahoo")
		# mpf.plot(data.iloc[first_min:(second_min+LINE_EXTEND_LENGTH)], addplot=addplots, type='candle', style="yahoo")

	plt.show()


def getLinePointsAtPoint(x_axis_value):
	# print('___________________________________________________________________________')
	# print(len(all_lines))
	points = []
	for i in range(len(all_lines)):
		line = all_lines[i]
		# if(i <= len(line)):
		if(x_axis_value < len(line)):
			pt = line[x_axis_value]
			points.append(pt)

	# print(points)

	return points

SCAN_LENGTH = 200
PRED_LENGTH = 50

start_pt = 210
end_pt = 350

ROUND_CMP = 5
ROUND_CMP = 4
ROUND_CMP = 3


dup_df = pd.read_csv("../../data/eurusd_col_m1_new.csv")

dup_df = dup_df.iloc[:500]
dup_df.Datetime = pd.to_datetime(dup_df.Datetime)
# dup_df = dup_df.set_index('Datetime')

dt = dup_df.iloc[:]

pt_iter = dt.iloc[start_pt:end_pt]

# iterate over each point
for i in range(len(pt_iter)):
	all_lines = []
	all_points = []
	print(i)
	print('-------------')
	# draw line before 200 from starting point ( data length is SCAN_LENGTH + PRED_LENGTH )
	# ln_data = dt.iloc[start_pt+i-SCAN_LENGTH:start_pt+i+PRED_LENGTH]
	ln_data = dt.iloc[start_pt-SCAN_LENGTH:start_pt+PRED_LENGTH]

	# plot trendlines 
	# plotTrendLines(start_pt+i-SCAN_LENGTH, start_pt+i+PRED_LENGTH)
	plotTrendLines(start_pt+i-SCAN_LENGTH, start_pt+i+PRED_LENGTH)

	# get all points of x = target point 
	# remember all_lines range is 200 previous value + 50 predict value
	print(len(all_lines), len(all_points))
	# exit()
	for line_i in range(len(all_lines)):
		# print('Line no: ' + str(line_i) + ' / ' + str(len(all_lines)))
		# target_point_x = start_pt+line_i
		target_point_x = start_pt+i
		line_point_x = SCAN_LENGTH+i

		target_point_y = data['close'].iloc[target_point_x]
		line_point_y = all_lines[line_i][line_point_x]
		# print(line_i, len(all_lines[line_i]), line_point_x)
		# print(line_i)

		# print(target_point_x, target_point_y)
		# print(line_point_x, line_point_y)

		round_target_point_y = round(target_point_y, ROUND_CMP)
		round_line_point_y = round(line_point_y, ROUND_CMP)
		# print(round_target_point_y, round_line_point_y)

		# if(round_target_point_y > 0):
		if(round_target_point_y == round_line_point_y):
			addplots = []
			print('target_point_y ' + str(target_point_y) + ' is same as line_point_y ' + str(line_point_y) + ' ======= ' + str(dup_df['Datetime'].iloc[start_pt+i]))
			pts = [None] * len(all_lines[line_i])
			pts[SCAN_LENGTH] = target_point_y

			# pt = mpf.make_addplot(pd.DataFrame(pts, dtype="float"), type="scatter", color="red")

			for ln_iter in range(len(all_lines)):
				color = "green"
				if(ln_iter == line_i):
					color = "black"

				si = mpf.make_addplot(pd.DataFrame(all_lines[ln_iter], dtype="float"), type='line', width=0.7, alpha=0.5, color=color)
				# addplots.append(si)

				points = mpf.make_addplot(pd.DataFrame(all_points[ln_iter], dtype="float"), type="scatter", color="blue")
				addplots.append(points)

			# addplots.append(pt)
			# print(start_pt+i)

			# mpf.plot(data.iloc[start_pt+i-SCAN_LENGTH:start_pt+i+PRED_LENGTH], addplot=addplots, type='candle', style="yahoo")
			dtt = dup_df.set_index('Datetime')

			mpf.plot(dtt.iloc[start_pt+i-SCAN_LENGTH:start_pt+i+PRED_LENGTH], addplot=addplots, type='candle', style="yahoo")
			# mpf.plot(data.iloc[:len(data)], addplot=addplots, type='candle', style="yahoo")
			plt.show()
			break

	# print(len(all_lines), len(all_lines[2]))
	# print(start_pt+i-SCAN_LENGTH, start_pt+i+PRED_LENGTH)


	# exit()











dup_df = dup_df.set_index('Datetime')

# mpf.plot(dup_df.iloc[start_pt-200:end_pt], type='candle', style="yahoo")
# plt.show()

# end_extreme_pt = len(data) - LINE_EXTEND_LENGTH
# start_extreme_pt = 0
# plotTrendLines(start_extreme_pt, end_extreme_pt)


# getLinePointsAtPoint(4)


print('end')









