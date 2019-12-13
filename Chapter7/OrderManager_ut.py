import unittest
from chapter7.OrderManager import OrderManager


class TestOrderBook(unittest.TestCase):

    def setUp(self):
        self.order_manager = OrderManager()

    def test_receive_order_from_trading_strategy(self):
        order1 = {
            'id': 10,
            'price': 219,
            'quantity': 10,
            'side': 'bid',
        }
        self.order_manager.handle_order_from_trading_strategy(order1)
        self.assertEqual(len(self.order_manager.orders),1)
        self.order_manager.handle_order_from_trading_strategy(order1)
        self.assertEqual(len(self.order_manager.orders),2)
        self.assertEqual(self.order_manager.orders[0]['id'],1)
        self.assertEqual(self.order_manager.orders[1]['id'],2)

    def test_receive_order_from_trading_strategy_error(self):
        order1 = {
            'id': 10,
            'price': -219,
            'quantity': 10,
            'side': 'bid',
        }
        self.order_manager.handle_order_from_trading_strategy(order1)
        self.assertEqual(len(self.order_manager.orders),0)

    def display_orders(self):
        for o in self.order_manager.orders:
            print(o)

    def test_receive_from_gateway_filled(self):
        self.test_receive_order_from_trading_strategy()
        orderexecution1 = {
            'id': 2,
            'price': 13,
            'quantity': 10,
            'side': 'bid',
            'status' : 'filled'
        }
        # self.display_orders()
        self.order_manager.handle_order_from_gateway(orderexecution1)
        self.assertEqual(len(self.order_manager.orders), 1)

    def test_receive_from_gateway_acked(self):
        self.test_receive_order_from_trading_strategy()
        orderexecution1 = {
            'id': 2,
            'price': 13,
            'quantity': 10,
            'side': 'bid',
            'status' : 'acked'
        }
        # self.display_orders()
        self.order_manager.handle_order_from_gateway(orderexecution1)
        self.assertEqual(len(self.order_manager.orders), 2)
        self.assertEqual(self.order_manager.orders[1]['status'], 'acked')
