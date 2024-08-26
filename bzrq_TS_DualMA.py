from box import Box

def average(lst):
    return sum(lst) / len(lst)


TS_DualMA__self = Box({})

def TS_DualMA____init__(ob_2_ts, ts_2_om, om_2_ts):
    TS_DualMA__self.orders = []
    TS_DualMA__self.order_id = 0

    TS_DualMA__self.position = 0
    TS_DualMA__self.pnl = 0
    TS_DualMA__self.cash = 10000

    TS_DualMA__self.paper_position = 0
    TS_DualMA__self.paper_pnl = 0
    TS_DualMA__self.paper_cash = 10000

    TS_DualMA__self.current_bid = 0
    TS_DualMA__self.current_offer = 0
    TS_DualMA__self.ob_2_ts = ob_2_ts
    TS_DualMA__self.ts_2_om = ts_2_om
    TS_DualMA__self.om_2_ts = om_2_ts
    TS_DualMA__self.long_signal = False
    TS_DualMA__self.total = 0
    TS_DualMA__self.holdings = 0
    TS_DualMA__self.small_window = deque()
    TS_DualMA__self.large_window = deque()
    TS_DualMA__self.list_position = []
    TS_DualMA__self.list_cash = []
    TS_DualMA__self.list_holdings = []
    TS_DualMA__self.list_total = []

    TS_DualMA__self.list_paper_position = []
    TS_DualMA__self.list_paper_cash = []
    TS_DualMA__self.list_paper_holdings = []
    TS_DualMA__self.list_paper_total = []

def TS_DualMA__create_metrics_out_of_prices(price_update):
    TS_DualMA__self.small_window.append(price_update)
    TS_DualMA__self.large_window.append(price_update)

    if len(TS_DualMA__self.small_window) > 50:
        TS_DualMA__self.small_window.popleft()

    if len(TS_DualMA__self.large_window) > 100:
        TS_DualMA__self.large_window.popleft()

    if len(TS_DualMA__self.small_window) == 50:
        if average(TS_DualMA__self.small_window) > average(TS_DualMA__self.large_window):
            TS_DualMA__self.long_signal = True
        else:
            TS_DualMA__self.long_signal = False
        return True

    return False

def TS_DualMA__buy_sell_or_hold_something(book_event):
    if TS_DualMA__self.long_signal and TS_DualMA__self.paper_position <= 0:
        TS_DualMA__self.create_order(book_event, book_event["bid_quantity"], "buy")
        TS_DualMA__self.paper_position += book_event["bid_quantity"]
        TS_DualMA__self.paper_cash -= (book_event["bid_quantity"] * book_event["bid_price"])

    elif TS_DualMA__self.paper_position > 0 and not TS_DualMA__self.long_signal:
        TS_DualMA__self.create_order(book_event, book_event["bid_quantity"], "sell")
        TS_DualMA__self.paper_position -= book_event["bid_quantity"]
        TS_DualMA__self.paper_cash -= (-book_event["bid_quantity"] * book_event["bid_price"])

    TS_DualMA__self.paper_holdings = (TS_DualMA__self.paper_position * book_event["bid_price"])
    TS_DualMA__self.paper_total = (TS_DualMA__self.paper_holdings + TS_DualMA__self.paper_cash)
    # print('total=%d, holding=%d, cash=%d' %
    #       (TS_DualMA__self.total, TS_DualMA__self.holdings, TS_DualMA__self.cash))

    TS_DualMA__self.list_paper_position.append(TS_DualMA__self.paper_position)
    TS_DualMA__self.list_paper_cash.append(TS_DualMA__self.paper_cash)
    TS_DualMA__self.list_paper_holdings.append(TS_DualMA__self.paper_holdings)
    TS_DualMA__self.list_paper_total.append(TS_DualMA__self.paper_holdings + TS_DualMA__self.paper_cash)

    TS_DualMA__self.list_position.append(TS_DualMA__self.position)
    TS_DualMA__self.holdings = TS_DualMA__self.position * book_event["bid_price"]
    TS_DualMA__self.list_holdings.append(TS_DualMA__self.holdings)
    TS_DualMA__self.list_cash.append(TS_DualMA__self.cash)
    TS_DualMA__self.list_total.append(TS_DualMA__self.holdings + TS_DualMA__self.cash)

def TS_DualMA__create_order(book_event,quantity,side):
        TS_DualMA__self.order_id+=1
        ord = {
            'id': TS_DualMA__self.order_id,
            'price': book_event['bid_price'],
            'quantity': quantity,
            'side': side,
            'action': 'to_be_sent'
        }
        TS_DualMA__self.orders.append(ord.copy())

def TS_DualMA__signal(book_event):
    if book_event['bid_quantity'] != -1 and book_event['offer_quantity'] != -1:
        TS_DualMA__create_metrics_out_of_prices(book_event['bid_price'])
        TS_DualMA__buy_sell_or_hold_something(book_event)

def TS_DualMA__execution():
    orders_to_be_removed=[]

    for index, order in enumerate(TS_DualMA__self.orders):

        if order['action'] == 'to_be_sent':
            # Send order
            order['status'] = 'new'
            order['action'] = 'no_action'
            if TS_DualMA__self.ts_2_om is None:
                print('Simulation mode')
            else:
                TS_DualMA__self.ts_2_om.append(order.copy())

        if order['status'] == 'rejected' or order['status']=='cancelled':
            orders_to_be_removed.append(index)

        if order['status'] == 'filled':
            orders_to_be_removed.append(index)
            pos = order['quantity'] if order['side'] == 'buy' else -order['quantity']
            TS_DualMA__self.position+=pos
            TS_DualMA__self.holdings = TS_DualMA__self.position * order['price']
            TS_DualMA__self.pnl-=pos * order['price']
            TS_DualMA__self.cash -= pos * order['price']

    for order_index in sorted(orders_to_be_removed,reverse=True):
        del (TS_DualMA__self.orders[order_index])

def TS_DualMA__handle_input_from_bb(book_event=None):
    if TS_DualMA__self.ob_2_ts is None:
        print('simulation mode')
        TS_DualMA__handle_book_event(book_event)
    else:
        if len(TS_DualMA__self.ob_2_ts)>0:
            be=TS_DualMA__handle_book_event(TS_DualMA__self.ob_2_ts.popleft())
            TS_DualMA__handle_book_event(be)

def TS_DualMA__handle_book_event(book_event):
    if book_event is not None:
        TS_DualMA__self.current_bid = book_event['bid_price']
        TS_DualMA__self.current_offer = book_event['offer_price']
        TS_DualMA__signal(book_event)
        TS_DualMA__execution()

def TS_DualMA__lookup_orders(id):
    count=0
    for o in TS_DualMA__self.orders:
        if o['id'] ==  id:
            return o, count
        count+=1
    return None, None

def handle_response_from_om():
    if TS_DualMA__self.om_2_ts is not None:
        TS_DualMA__handle_market_response(TS_DualMA__self.om_2_ts.popleft())
    else:
        print('simulation mode')

def TS_DualMA__handle_market_response(order_execution):
    print(order_execution)
    order,_=TS_DualMA__self.lookup_orders(order_execution['id'])
    if order is None:
        print('error not found')
        return
    order['status']=order_execution['status']
    TS_DualMA__execution()

def TS_DualMA__get_pnl():
    return TS_DualMA__self.pnl + TS_DualMA__self.position * (TS_DualMA__self.current_bid + TS_DualMA__self.current_offer)/2

