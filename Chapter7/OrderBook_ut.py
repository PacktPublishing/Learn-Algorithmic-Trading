import unittest
from chapter7.OrderBook import OrderBook


class TestOrderBook(unittest.TestCase):

    def setUp(self):
        self.reforderbook = OrderBook()

    def test_handlenew(self):
        order1 = {
            'id': 1,
            'price': 219,
            'quantity': 10,
            'side': 'bid',
            'action': 'new'
        }

        ob_for_aapl = self.reforderbook
        ob_for_aapl.handle_order(order1)
        order2 = order1.copy()
        order2['id'] = 2
        order2['price'] = 220
        ob_for_aapl.handle_order(order2)
        order3 = order1.copy()
        order3['price'] = 223
        order3['id'] = 3
        ob_for_aapl.handle_order(order3)
        order4 = order1.copy()
        order4['side'] = 'ask'
        order4['price'] = 220
        order4['id'] = 4
        ob_for_aapl.handle_order(order4)
        order5 = order4.copy()
        order5['price'] = 223
        order5['id'] = 5
        ob_for_aapl.handle_order(order5)
        order6 = order4.copy()
        order6['price'] = 221
        order6['id'] = 6
        ob_for_aapl.handle_order(order6)

        self.assertEqual(ob_for_aapl.list_bids[0]['id'],3)
        self.assertEqual(ob_for_aapl.list_bids[1]['id'], 2)
        self.assertEqual(ob_for_aapl.list_bids[2]['id'], 1)
        self.assertEqual(ob_for_aapl.list_asks[0]['id'],4)
        self.assertEqual(ob_for_aapl.list_asks[1]['id'], 6)
        self.assertEqual(ob_for_aapl.list_asks[2]['id'], 5)


    def test_handleamend(self):
        self.test_handlenew()
        order1 = {
            'id': 1,
            'quantity': 5,
            'action': 'modify'
        }
        self.reforderbook.handle_order(order1)

        self.assertEqual(self.reforderbook.list_bids[2]['id'], 1)
        self.assertEqual(self.reforderbook.list_bids[2]['quantity'], 5)


    def test_handledelete(self):
        self.test_handlenew()
        order1 = {
            'id': 1,
            'action': 'delete'
        }
        self.assertEqual(len(self.reforderbook.list_bids), 3)
        self.reforderbook.handle_order(order1)
        self.assertEqual(len(self.reforderbook.list_bids), 2)

    def test_generate_book_event(self):
        order1 = {
            'id': 1,
            'price': 219,
            'quantity': 10,
            'side': 'bid',
            'action': 'new'
        }

        ob_for_aapl = self.reforderbook
        self.assertEqual(ob_for_aapl.handle_order(order1),
                         {'bid_price': 219, 'bid_quantity': 10,
                          'offer_price': -1, 'offer_quantity': -1})
        order2 = order1.copy()
        order2['id'] = 2
        order2['price'] = 220
        order2['side'] = 'ask'
        self.assertEqual(ob_for_aapl.handle_order(order2),
        {'bid_price': 219, 'bid_quantity': 10,
         'offer_price': 220, 'offer_quantity': 10})



if __name__ == '__main__':
    unittest.main()