import unittest
from chapter7.TradingStrategy import TradingStrategy


class TestMarketSimulator(unittest.TestCase):

    def setUp(self):
        self.trading_strategy= TradingStrategy()


    def test_receive_top_of_book(self):
        book_event = {
            "bid_price" : 12,
            "bid_quantity" : 100,
            "offer_price" : 11,
            "offer_quantity" : 150
        }
        self.trading_strategy.handle_book_event(book_event)
        self.assertEqual(len(self.trading_strategy.orders), 2)
        self.assertEqual(self.trading_strategy.orders[0]['side'], 'sell')
        self.assertEqual(self.trading_strategy.orders[1]['side'], 'buy')
        self.assertEqual(self.trading_strategy.orders[0]['price'], 12)
        self.assertEqual(self.trading_strategy.orders[1]['price'], 11)
        self.assertEqual(self.trading_strategy.orders[0]['quantity'], 100)
        self.assertEqual(self.trading_strategy.orders[1]['quantity'], 100)
        self.assertEqual(self.trading_strategy.orders[0]['action'], 'no_action')
        self.assertEqual(self.trading_strategy.orders[1]['action'], 'no_action')


    def test_rejected_order(self):
        self.test_receive_top_of_book()
        order_execution = {
            'id': 1,
            'price': 12,
            'quantity': 100,
            'side': 'sell',
            'status' : 'rejected'
        }
        self.trading_strategy.handle_market_response(order_execution)
        self.assertEqual(self.trading_strategy.orders[0]['side'], 'buy')
        self.assertEqual(self.trading_strategy.orders[0]['price'], 11)
        self.assertEqual(self.trading_strategy.orders[0]['quantity'], 100)
        self.assertEqual(self.trading_strategy.orders[0]['status'], 'new')


    def test_filled_order(self):
        self.test_receive_top_of_book()
        order_execution = {
            'id': 1,
            'price': 11,
            'quantity': 100,
            'side': 'sell',
            'status' : 'filled'
        }
        self.trading_strategy.handle_market_response(order_execution)
        self.assertEqual(len(self.trading_strategy.orders),1)

        order_execution = {
            'id': 2,
            'price': 12,
            'quantity': 100,
            'side': 'buy',
            'status' : 'filled'
        }
        self.trading_strategy.handle_market_response(order_execution)
        self.assertEqual(self.trading_strategy.position, 0)
        self.assertEqual(self.trading_strategy.cash, 10100)
        self.assertEqual(self.trading_strategy.pnl, 100)



