# Python program to get average of a list
from collections import deque

def average(lst):
    return sum(lst) / len(lst)

class TradingStrategyDualMA:
    def __init__(self, ob_2_ts, ts_2_om, om_2_ts):
        self.orders = []
        self.order_id = 0

        self.position = 0
        self.pnl = 0
        self.cash = 10000

        self.paper_position = 0
        self.paper_pnl = 0
        self.paper_cash = 10000

        self.current_bid = 0
        self.current_offer = 0
        self.ob_2_ts = ob_2_ts
        self.ts_2_om = ts_2_om
        self.om_2_ts = om_2_ts
        self.long_signal=False
        self.total=0
        self.holdings=0
        self.small_window=deque()
        self.large_window=deque()
        self.list_position=[]
        self.list_cash=[]
        self.list_holdings = []
        self.list_total=[]

        self.list_paper_position = []
        self.list_paper_cash = []
        self.list_paper_holdings = []
        self.list_paper_total = []


    def create_metrics_out_of_prices(self,price_update):
        self.small_window.append(price_update)
        self.large_window.append(price_update)
        if len(self.small_window)>50:
            self.small_window.popleft()
        if len(self.large_window)>100:
            self.large_window.popleft()
        if len(self.small_window) == 50:
            if average(self.small_window) >\
                average(self.large_window):
                self.long_signal=True
            else:
                self.long_signal = False
            return True
        return False

    def buy_sell_or_hold_something(self, book_event):
        if self.long_signal and self.paper_position<=0:
            self.create_order(book_event,book_event['bid_quantity'],'buy')
            self.paper_position += book_event['bid_quantity']
            self.paper_cash -= book_event['bid_quantity'] * book_event['bid_price']
        elif self.paper_position>0 and not self.long_signal:
            self.create_order(book_event,book_event['bid_quantity'],'sell')
            self.paper_position -= book_event['bid_quantity']
            self.paper_cash -= -book_event['bid_quantity'] * book_event['bid_price']

        self.paper_holdings = self.paper_position * book_event['bid_price']
        self.paper_total = (self.paper_holdings + self.paper_cash)
        # print('total=%d, holding=%d, cash=%d' %
        #       (self.total, self.holdings, self.cash))

        self.list_paper_position.append(self.paper_position)
        self.list_paper_cash.append(self.paper_cash)
        self.list_paper_holdings.append(self.paper_holdings)
        self.list_paper_total.append(self.paper_holdings+self.paper_cash)

        self.list_position.append(self.position)
        self.holdings=self.position*book_event['bid_price']
        self.list_holdings.append(self.holdings)
        self.list_cash.append(self.cash)
        self.list_total.append(self.holdings+self.cash)

    def create_order(self,book_event,quantity,side):
        self.order_id+=1
        ord = {
            'id': self.order_id,
            'price': book_event['bid_price'],
            'quantity': quantity,
            'side': side,
            'action': 'to_be_sent'
        }
        self.orders.append(ord.copy())


    def signal(self, book_event):
        if book_event['bid_quantity'] != -1 and \
                book_event['offer_quantity'] != -1:
            self.create_metrics_out_of_prices(book_event['bid_price'])
            self.buy_sell_or_hold_something(book_event)


    def execution(self):
        orders_to_be_removed=[]
        for index, order in enumerate(self.orders):
            if order['action'] == 'to_be_sent':
                # Send order
                order['status'] = 'new'
                order['action'] = 'no_action'
                if self.ts_2_om is None:
                    print('Simulation mode')
                else:
                    self.ts_2_om.append(order.copy())
            if order['status'] == 'rejected' or order['status']=='cancelled':
                orders_to_be_removed.append(index)
            if order['status'] == 'filled':
                orders_to_be_removed.append(index)
                pos = order['quantity'] if order['side'] == 'buy' else -order['quantity']
                self.position+=pos
                self.holdings = self.position * order['price']
                self.pnl-=pos * order['price']
                self.cash -= pos * order['price']

        for order_index in sorted(orders_to_be_removed,reverse=True):
            del (self.orders[order_index])


    def handle_input_from_bb(self,book_event=None):
        if self.ob_2_ts is None:
            print('simulation mode')
            self.handle_book_event(book_event)
        else:
            if len(self.ob_2_ts)>0:
                be=self.handle_book_event(self.ob_2_ts.popleft())
                self.handle_book_event(be)

    def handle_book_event(self,book_event):
        if book_event is not None:
            self.current_bid = book_event['bid_price']
            self.current_offer = book_event['offer_price']
            self.signal(book_event)
            self.execution()

    def lookup_orders(self,id):
        count=0
        for o in self.orders:
            if o['id'] ==  id:
                return o, count
            count+=1
        return None, None

    def handle_response_from_om(self):
        if self.om_2_ts is not None:
            self.handle_market_response(self.om_2_ts.popleft())
        else:
            print('simulation mode')

    def handle_market_response(self, order_execution):
        print(order_execution)
        order,_=self.lookup_orders(order_execution['id'])
        if order is None:
            print('error not found')
            return
        order['status']=order_execution['status']
        self.execution()

    def get_pnl(self):
        return self.pnl + self.position * (self.current_bid + self.current_offer)/2

