import os
import sys
from pathlib import Path
from box import Box

sys.path
os.getcwd()
sys.path.append(str(Path("/home/bzrq/data/zr/Learn-Algorithmic-Trading")))


from Chapter7.LiquidityProvider import LiquidityProvider
from Chapter9.TradingStrategyDualMA import TradingStrategyDualMA
from Chapter7.MarketSimulator import MarketSimulator
from Chapter7.OrderManager import OrderManager
from Chapter7.OrderBook import OrderBook
from collections import deque


import pandas as pd
from pandas_datareader import data
import matplotlib.pyplot as plt


def call_if_not_empty(deq, fun):
    while (len(deq) > 0):
        fun()

EBT__self = Box({})


def EBT____init__():
    EBT__self.lp_2_gateway = deque()
    EBT__self.ob_2_ts = deque()
    EBT__self.ts_2_om = deque()
    EBT__self.ms_2_om = deque()
    EBT__self.om_2_ts = deque()
    EBT__self.gw_2_om = deque()
    EBT__self.om_2_gw = deque()


    EBT__self.lp = LiquidityProvider(EBT__self.lp_2_gateway)
    EBT__self.ob = OrderBook(EBT__self.lp_2_gateway, EBT__self.ob_2_ts)
    EBT__self.ts = TradingStrategyDualMA(EBT__self.ob_2_ts, EBT__self.ts_2_om, EBT__self.om_2_ts)
    EBT__self.ms = MarketSimulator(EBT__self.om_2_gw, EBT__self.gw_2_om)
    EBT__self.om = OrderManager(EBT__self.ts_2_om, EBT__self.om_2_ts, EBT__self.om_2_gw, EBT__self.gw_2_om)


def EBT__process_data_from_yahoo(price):

    order_bid = {
        'id': 1,
        'price': price,
        'quantity': 1000,
        'side': 'bid',
        'action': 'new'
    }
    order_ask = {
        'id': 1,
        'price': price,
        'quantity': 1000,
        'side': 'ask',
        'action': 'new'
    }
    EBT__self.lp_2_gateway.append(order_ask)
    EBT__self.lp_2_gateway.append(order_bid)
    EBT__self.process_events()

    order_ask['action']='delete'
    order_bid['action'] = 'delete'

    EBT__self.lp_2_gateway.append(order_ask)
    EBT__self.lp_2_gateway.append(order_bid)

def EBT__process_events():
    while len(EBT__self.lp_2_gateway) > 0:
        call_if_not_empty(EBT__self.lp_2_gateway, EBT__self.ob.handle_order_from_gateway)
        call_if_not_empty(EBT__self.ob_2_ts, EBT__self.ts.handle_input_from_bb)
        call_if_not_empty(EBT__self.ts_2_om, EBT__self.om.handle_input_from_ts)
        call_if_not_empty(EBT__self.om_2_gw, EBT__self.ms.handle_order_from_gw)
        call_if_not_empty(EBT__self.gw_2_om, EBT__self.om.handle_input_from_market)
        call_if_not_empty(EBT__self.om_2_ts, EBT__self.ts.handle_response_from_om)





def load_financial_data(start_date, end_date, output_file):
    try:
        df = pd.read_pickle(output_file)
        print("File data found...reading GOOG data")
    except FileNotFoundError:
        print("File not found...downloading the GOOG data")
        # df = data.DataReader('GOOG', 'yahoo', start_date, end_date)
        df = yf.download("GOOG", start_date, end_date)
        df.to_pickle(output_file)

    return df


goog_data = load_financial_data(start_date="2001-01-01", end_date="2018-01-01", output_file="goog_data.pkl")



EBT____init__()
for line in zip(goog_data.index,goog_data['Adj Close']):
    date=line[0]
    price=line[1]
    price_information={'date' : date,
                      'price' : float(price)}
    EBT__process_data_from_yahoo(price_information['price'])
    EBT__process_events()


plt.plot(eb.ts.list_paper_total,label="Paper Trading using Event-Based BackTester")
plt.plot(eb.ts.list_total,label="Trading using Event-Based BackTester")
plt.legend()
plt.show()

