import MetaTrader5 as mt5
from datetime import datetime
import pandas as pd


login = 67021181
password = "q14d6352C"
server = "RoboForex-ECN"

pd.set_option('display.max_columns', 500) # number of columns to be displayed
pd.set_option('display.width', 1500)      # max table width to display
# display data on the MetaTrader 5 package
print("MetaTrader5 package author: ",mt5.__author__)
print("MetaTrader5 package version: ",mt5.__version__)
print()

# establish connection to the MetaTrader 5 terminal
if not mt5.initialize(login=login, password=password, server=server):
	print("initialize() failed, error code =",mt5.last_error())
	quit()
 
# get the number of deals in history
from_date=datetime(2020,1,1)
to_date=datetime.now()
history_orders=mt5.history_orders_get(from_date, to_date, group="*USD*")
if history_orders==None:
	print("No history orders with group=\"*USD*\", error code={}".format(mt5.last_error()))
elif len(history_orders)>0:
	print("history_orders_get({}, {}, group=\"*USD*\")={}".format(from_date,to_date,len(history_orders)))
print()

# shut down connection to the MetaTrader 5 terminal
mt5.shutdown()