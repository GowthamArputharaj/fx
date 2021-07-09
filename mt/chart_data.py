from datetime import datetime
import MetaTrader5 as mt5
import pandas as pd
import pytz


# display data on the MetaTrader 5 package
print("MetaTrader5 package author: ",mt5.__author__)
print("MetaTrader5 package version: ",mt5.__version__)
 
login = 67021181
password = "q14d6352C"
server = "RoboForex-ECN"

# import the 'pandas' module for displaying data obtained in the tabular form
pd.set_option('display.max_columns', 500) # number of columns to be displayed
pd.set_option('display.width', 1500)      # max table width to display
# import pytz module for working with time zone
 
# establish connection to MetaTrader 5 terminal
# if not mt5.initialize():
if not mt5.initialize(login=login, server=server,password=password):
    print("initialize() failed, error code =",mt5.last_error())
    quit()

symbol = "USDJPY"
symbol = "EURUSD"

# set time zone to UTC
timezone = pytz.timezone("Etc/UTC")
# create 'datetime' objects in UTC time zone to avoid the implementation of a local time zone offset
utc_from = datetime(2021, 7, 1, tzinfo=timezone)
utc_to = datetime(2021, 7, 6, hour = 0, tzinfo=timezone)
# utc_to = datetime(2020, 1, 11, hour = 13, tzinfo=timezone)
# get bars from USDJPY M5 within the interval of 2020.01.10 00:00 - 2020.01.11 13:00 in UTC time zone
rates = mt5.copy_rates_range(symbol, mt5.TIMEFRAME_M15, utc_from, utc_to)

# shut down connection to the MetaTrader 5 terminal
mt5.shutdown()

# display each element of obtained data in a new line
print("Display obtained data 'as is'")
counter=0
for rate in rates:
    counter+=1
    if counter<=10:
        print(rate)
 
# create DataFrame out of the obtained data
rates_frame = pd.DataFrame(rates)

print(rates_frame.head(4))

rates_frame['Datetime']=pd.to_datetime(rates_frame['time'], unit='s')

rates_frame = rates_frame[['Datetime', 'open', 'high', 'low', 'close', 'tick_volume']]

rates_frame.columns = ['Datetime', 'open', 'high', 'low', 'close', 'volume']

print(rates_frame.head(3))
exit()


# convert time in seconds into the 'datetime' format
rates_frame['volume']=pd.to_datetime(rates_frame['tick_volume'])

rates_frame = rates_frame[['Datetime', 'open', 'high', 'low', 'close', 'volume']]
# display data
print("\nDisplay dataframe with data")
print(rates_frame.head(10))
print(len(rates_frame))