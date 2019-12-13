import unittest
from chapter7.LiquidityProvider import LiquidityProvider
from chapter7.TradingStrategy import TradingStrategy
from chapter7.MarketSimulator import MarketSimulator
from chapter7.OrderManager import OrderManager
from chapter7.OrderBook import OrderBook
from collections import deque

class TestTradingSimulation(unittest.TestCase):
    def setUp(self):
        self.lp_2_gateway=deque()
        self.ob_2_ts = deque()
        self.ts_2_om = deque()
        self.ms_2_om = deque()
        self.om_2_ts = deque()
        self.gw_2_om = deque()
        self.om_2_gw = deque()




        self.lp=LiquidityProvider(self.lp_2_gateway)
        self.ob=OrderBook(self.lp_2_gateway, self.ob_2_ts)
        self.ts=TradingStrategy(self.ob_2_ts,self.ts_2_om,self.om_2_ts)
        self.ms=MarketSimulator(self.om_2_gw,self.gw_2_om)
        self.om=OrderManager(self.ts_2_om, self.om_2_ts,self.om_2_gw,self.gw_2_om)



    def test_add_liquidity(self):
        # Order sent from the exchange to the trading system
        order1 = {
            'id': 1,
            'price': 219,
            'quantity': 10,
            'side': 'bid',
            'action': 'new'
        }
        self.lp.insert_manual_order(order1)
        self.assertEqual(len(self.lp_2_gateway),1)
        self.ob.handle_order_from_gateway()
        self.assertEqual(len(self.ob_2_ts), 1)
        self.ts.handle_input_from_bb()
        self.assertEqual(len(self.ts_2_om), 0)
        order2 = {
            'id': 2,
            'price': 218,
            'quantity': 10,
            'side': 'ask',
            'action': 'new'
        }
        self.lp.insert_manual_order(order2.copy())
        self.assertEqual(len(self.lp_2_gateway),1)
        self.ob.handle_order_from_gateway()
        self.assertEqual(len(self.ob_2_ts), 1)
        self.ts.handle_input_from_bb()
        self.assertEqual(len(self.ts_2_om), 2)
        self.om.handle_input_from_ts()
        self.assertEqual(len(self.ts_2_om), 1)
        self.assertEqual(len(self.om_2_gw), 1)
        self.om.handle_input_from_ts()
        self.assertEqual(len(self.ts_2_om), 0)
        self.assertEqual(len(self.om_2_gw), 2)
        self.ms.handle_order_from_gw()
        self.assertEqual(len(self.gw_2_om), 1)
        self.ms.handle_order_from_gw()
        self.assertEqual(len(self.gw_2_om), 2)
        self.om.handle_input_from_market()
        self.om.handle_input_from_market()
        self.assertEqual(len(self.om_2_ts), 2)
        self.ts.handle_response_from_om()
        self.assertEqual(self.ts.get_pnl(),0)
        self.ms.fill_all_orders()
        self.assertEqual(len(self.gw_2_om), 2)
        self.om.handle_input_from_market()
        self.om.handle_input_from_market()
        self.assertEqual(len(self.om_2_ts), 3)
        self.ts.handle_response_from_om()
        self.assertEqual(len(self.om_2_ts), 2)
        self.ts.handle_response_from_om()
        self.assertEqual(len(self.om_2_ts), 1)
        self.ts.handle_response_from_om()
        self.assertEqual(len(self.om_2_ts), 0)
        self.assertEqual(self.ts.get_pnl(),10)





