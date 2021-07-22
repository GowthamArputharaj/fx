import MetaTrader5 as mt5
import pandas as pd
pd.set_option('display.max_columns', 500) # number of columns to be displayed
pd.set_option('display.width', 1500)      # max table width to display


login = 67021181
password = "q14d6352C"
server = "RoboForex-ECN"

# establish connection to the MetaTrader 5 terminal
if not mt5.initialize():
    print("initialize() failed, error code =",mt5.last_error())
    quit()
 
symbol = "AUDCAD"
# symbol = "EURUSD"
# get open positions on USDCHF
positions=mt5.positions_get(symbol=symbol)
if positions==None:
    print("No positions on AUDUSD, error code={}".format(mt5.last_error()))
elif len(positions)>0:
    print("Total positions on AUDUSD =",len(positions))
    # display all open positions
    for position in positions:
        print(position)
 
# get the list of positions on symbols whose names contain "*USD*"
# symbol_positions=mt5.positions_get(group="*USD*")
# symbol_positions=mt5.positions_get(group="*AUD*")
symbol_positions=mt5.positions_get(symbol)
if symbol_positions==None:
	print("No positions with group=\"*AUD*\", error code={}".format(mt5.last_error()))
elif len(symbol_positions)>0:
	print("positions_get(group=\"*AUD*\")={}".format(len(symbol_positions)))
	# display these positions as a table using pandas.DataFrame
	df=pd.DataFrame(list(symbol_positions),columns=symbol_positions[0]._asdict().keys())
	df['time'] = pd.to_datetime(df['time'], unit='s')
	df.drop(['time_update', 'time_msc', 'time_update_msc', 'external_id'], axis=1, inplace=True)
	print(df)
	print('Profit is : ' + str(df['profit']), (df['profit'] > 0))

 
# shut down connection to the MetaTrader 5 terminal
mt5.shutdown()












