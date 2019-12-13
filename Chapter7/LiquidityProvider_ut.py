import unittest
from chapter7.LiquidityProvider import LiquidityProvider


class TestMarketSimulator(unittest.TestCase):
    def setUp(self):
        self.liquidity_provider = LiquidityProvider()

    def test_add_liquidity(self):
        self.liquidity_provider.generate_random_order()
        self.assertEqual(self.liquidity_provider.orders[0]['id'],0)
        self.assertEqual(self.liquidity_provider.orders[0]['side'], 'buy')
        self.assertEqual(self.liquidity_provider.orders[0]['quantity'], 700)
        self.assertEqual(self.liquidity_provider.orders[0]['price'], 11)

