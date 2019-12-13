from chapter7.LiquidityProvider import LiquidityProvider
from chapter7.TradingStrategy import TradingStrategy
from chapter7.MarketSimulator import MarketSimulator
from chapter7.OrderManager import OrderManager
from chapter7.OrderBook import OrderBook
from collections import deque

def main():
    lp_2_gateway = deque()
    ob_2_ts = deque()
    ts_2_om = deque()
    ms_2_om = deque()
    om_2_ts = deque()
    gw_2_om = deque()
    om_2_gw = deque()

    lp = LiquidityProvider(lp_2_gateway)
    ob = OrderBook(lp_2_gateway, ob_2_ts)
    ts = TradingStrategy(ob_2_ts, ts_2_om, om_2_ts)
    ms = MarketSimulator(om_2_gw, gw_2_om)
    om = OrderManager(ts_2_om, om_2_ts, om_2_gw, gw_2_om)

    lp.read_tick_data_from_data_source()
    while len(lp_2_gateway)>0:
        ob.handle_order_from_gateway()
        ts.handle_input_from_bb()
        om.handle_input_from_ts()
        ms.handle_order_from_gw()
        om.handle_input_from_market()
        ts.handle_response_from_om()
        lp.read_tick_data_from_data_source()




if __name__ == '__main__':
    main()