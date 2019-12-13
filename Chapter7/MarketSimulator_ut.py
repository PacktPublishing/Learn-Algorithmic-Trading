import unittest
from chapter7.MarketSimulator import MarketSimulator


class TestMarketSimulator(unittest.TestCase):

    def setUp(self):
        self.market_simulator = MarketSimulator()

    def test_accept_order(self):
        self.market_simulator
        order1 = {
            'id': 10,
            'price': 219,
            'quantity': 10,
            'side': 'bid',
            'action' : 'New'
        }
        self.market_simulator.handle_order(order1)
        self.assertEqual(len(self.market_simulator.orders),1)
        self.assertEqual(self.market_simulator.orders[0]['status'], 'accepted')

    def test_accept_order(self):
        self.market_simulator
        order1 = {
            'id': 10,
            'price': 219,
            'quantity': 10,
            'side': 'bid',
            'action' : 'Amend'
        }
        self.market_simulator.handle_order(order1)
        self.assertEqual(len(self.market_simulator.orders),0)
