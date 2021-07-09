
from datetime import datetime
import MetaTrader5 as mt5
import pandas as pd
# import pytz module for working with time zone
import pytz


login = 67021181
password = "q14d6352C"
server = "RoboForex-ECN"


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

symbol = "EURUSD"
symbol = "AUDCAD"

# display data on active orders on GBPUSD
orders = mt5.orders_get(symbol=symbol)

# print(orders)
# exit()

if orders is None:
    print("No orders on EURUSD, error code={}".format(mt5.last_error()))
else:
    print("Total orders on EURUSD:",len(orders))
    # display all active orders
    for order in orders:
        print(order)
print()

# get the list of orders on symbols whose names contain "*GBP*"
eur_orders=mt5.orders_get(group="*EUR*")
if eur_orders is None:
    print("No orders with group=\"*EUR*\", error code={}".format(mt5.last_error()))
else:
    print("orders_get(group=\"*EUR*\")={}".format(len(eur_orders)))
    # display these orders as a table using pandas.DataFrame
    df=pd.DataFrame(list(eur_orders),columns=eur_orders[0]._asdict().keys())
    df.drop(['time_done', 'time_done_msc', 'position_id', 'position_by_id', 'reason', 'volume_initial', 'price_stoplimit'], axis=1, inplace=True)
    df['time_setup'] = pd.to_datetime(df['time_setup'], unit='s')
    print(df)


# shut down connection to the MetaTrader 5 terminal
mt5.shutdown()















