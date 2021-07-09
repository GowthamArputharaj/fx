import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 



# data = pd.read_csv('../../data/eurusd_col_m1_500.csv')

# close = data['close']


data = pd.read_csv('../../data/EURUSD_M1_2000.csv')

data['close'] = data.iloc[:, 5]


data['Datetime'] = data.iloc[:,0].str.cat(data.iloc[:,1],sep=" ")

close = data['close']


window_size = 30 

numbers_series = pd.Series(close)
windows = numbers_series.rolling(window_size)
moving_averages = windows.mean()

moving_averages_list = moving_averages.tolist()
# without_nans = moving_averages_list[window_size - 1:]

sma_30 = moving_averages_list



window_size = 200 

numbers_series = pd.Series(close)
windows = numbers_series.rolling(window_size)
moving_averages = windows.mean()

moving_averages_list = moving_averages.tolist()
# without_nans = moving_averages_list[window_size - 1:]

sma_200 = moving_averages_list

plt.plot(data['Datetime'], close, color="black")
plt.plot(data['Datetime'], sma_30, color="blue")
plt.plot(data['Datetime'], sma_200, color="green")
plt.xticks(rotation=45)
plt.xlabel('Datetime')
plt.ylabel('Price')
plt.legend()
plt.show()










