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
 
symbol = "EURUSD"
# symbol = "AUDUSD"

# create a close request
# position_id=result.order

position_id = 203715369
# position_id = 203715421
lot = 0.01

# mt5.Close(symbol)
# mt5.Close(1)
# mt5.Close(symbol)
# mt5.Close(position_id)
# mt5.Close(symbol, position_id)

# exit()

price=mt5.symbol_info_tick(symbol).bid
deviation=20

request={
    "action": mt5.TRADE_ACTION_DEAL,
    "symbol": symbol,
    "volume": lot,
    "type": mt5.ORDER_TYPE_SELL,
    "position": position_id,
    "price": price,
    "deviation": deviation,
    "magic": 12345678,
    "comment": "python script close",
    "type_time": mt5.ORDER_TIME_GTC,
    "type_filling": mt5.ORDER_FILLING_IOC,
}

# request={
#     "action": mt5.TRADE_ACTION_DEAL,
#     "symbol": symbol,
#     "volume": lot,
#     "type": mt5.ORDER_TYPE_SELL,
#     "position": position_id,
#     "price": price,
#     "deviation": deviation,
#     "magic": magic,
#     "comment": "python script close",
#     "type_time": mt5.ORDER_TIME_GTC,
#     "type_filling": mt5.ORDER_FILLING_IOC,
# }


# send a trading request
result=mt5.order_send(request)

print(result.retcode)

if result.retcode != mt5.TRADE_RETCODE_DONE:
    print("4. order_send failed")
    print("   result",result)

else:
    print("4. position #{} closed, {}".format(position_id,result))
    
    # request the result as a dictionary and display it element by element
    result_dict=result._asdict()
    for field in result_dict.keys():
        print("   {}={}".format(field,result_dict[field]))
        # if this is a trading request structure, display it element by element as well
        if field=="request":
            traderequest_dict=result_dict[field]._asdict()
            for tradereq_filed in traderequest_dict:
                print("       traderequest: {}={}".format(tradereq_filed,traderequest_dict[tradereq_filed]))
    


# shut down connection to the MetaTrader 5 terminal
mt5.shutdown()












