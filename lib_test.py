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
from ta import add_all_ta_features
from ta.utils import dropna
import pandas_ta as ta 


# constant area

import matplotlib.pyplot as plt 

# print(MAX_STAR_BODY)
# exit()
df = pd.read_csv("../../data/eurusd_col_m1_new.csv")

# df = df.iloc[50]

df = pd.DataFrame(df) 

data = pd.DataFrame()
data['Open'] = df['open']
data['High'] = df['high']
data['Low'] = df['low']
data['Close'] = df['close']

from stolgo.candlestick import CandleStick

# help(df.ta)
# help(df.ta.hl2)

# df.ta.indicators()
# df.ta.cdl_pattern(name="all")
# help(df.ta.bbands)
# exit()
# df = df.iloc[0:600]
# df = df.iloc[0:50]
df.Datetime = pd.to_datetime(df.Datetime)
df = df.set_index('Datetime')

cdl = CandleStick()

is_bullish_engulfing = cdl.is_bullish_engulfing(data)
print(is_bullish_engulfing)
exit()

for j in range(len(data)-50):
	i = j + 50
	print(i)
	candle = CandleStick()
	# print(data.iloc[i])
	# print(data.iloc[i]['Close'])
	# exit()

	is_bullish_engulfing = candle.is_bullish_engulfing(data.iloc[i])

	print(is_bullish_engulfing)
	si_val = np.full([60], False)

	si_val[30] = round(df.iloc[i,3] * 0.99, round_digits)

	ok = df.iloc[i-30:i+30,:]

	signal = si_val


exit()
# sma10 = ta.sma(df["close"], length=10)

# print(sma10)

# si = mpf.make_addplot(pd.DataFrame(sma10, dtype="float"), type='line',markersize=2, color="black")

# mpf.plot(df, addplot=si, type='candle', style="yahoo")


# https://github.com/stockalgo/stolgo
# https://github.com/SpiralDevelopment/candlestick-patterns
# print(df.head())
















