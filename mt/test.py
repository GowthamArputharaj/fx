
from datetime import datetime
import MetaTrader5 as mt5
import pandas as pd
# import pytz module for working with time zone
import pytz
 

login = 48410080
password = "yhyji5kh"
server = "MetaQuotes-Demo"


login = 67021181
password = "q14d6352C"
server = "RoboForex-ECN"

metatrader_file_path = 'C:\Program Files\MetaTrader 5'

pd.set_option('display.max_columns', 500) # number of columns to be displayed
pd.set_option('display.width', 1500)      # max table width to display
 
# establish MetaTrader 5 connection to a specified trading account
if not mt5.initialize(login=login, server=server,password=password):
    print("initialize() failed, error code =",mt5.last_error())
    quit()
 
# set time zone to UTC
timezone = pytz.timezone("Etc/UTC")

# create 'datetime' objects in UTC time zone to avoid the implementation of a local time zone offset
utc_from = datetime(2020, 1, 10, tzinfo=timezone)
utc_to = datetime(2020, 1, 11, hour = 13, tzinfo=timezone)
# get bars from EURUSD M5 within the interval of 2020.01.10 00:00 - 2020.01.11 13:00 in UTC time zone
# rates = mt5.copy_rates_range("EURUSD", mt5.TIMEFRAME_M5, utc_from, utc_to)
rates = mt5.copy_rates_range("EURUSD", mt5.TIMEFRAME_M1, utc_from, utc_to)

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
# convert time in seconds into the 'datetime' format
rates_frame['time']=pd.to_datetime(rates_frame['time'], unit='s')
 
# display data
print("\nDisplay dataframe with data")
print(rates_frame.head(10))
print(len(rates))





