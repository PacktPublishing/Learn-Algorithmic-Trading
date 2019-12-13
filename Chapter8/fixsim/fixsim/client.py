import quickfix
import copy
import uuid
import random
import datetime
#import yaml

from twisted.internet import task

from sim import (FixSimError, FixSimApplication, create_fix_version,
                 instance_safe_call, create_logger, IncrementID, load_yaml)


class Subscription(object):
    def __init__(self, symbol):
        super(Subscription, self).__init__()
        self.symbol = symbol
        self.currency = self.symbol.split("/")[0]

    def __repr__(self):
        return "<Subscription %s>" % self.symbol


class Subscriptions(object):
    def __init__(self):
        self.subscriptions = {}

    def add(self, subscription):
        if subscription.symbol in self.subscriptions:
            raise KeyError("Subscription for symbol has already exist")
        self.subscriptions[subscription.symbol] = subscription

    def get(self, symbol):
        subscription = self.subscriptions.get(symbol, None)
        return subscription

    def __iter__(self):
        return self.subscriptions.values().__iter__()


class OrderBook(object):
    def __init__(self):
        self.quotes = []

    def setSnapshot(self, snaphot):
        raise NotImplementedError()

    def __iter__(self):
        return self.quotes.__iter__()

    def get(self, quoteID):
        for quote in self.quotes:
            if quote.id == quoteID:
                return quote

        return None


class IDGenerator(object):
    def __init__(self):
        self._orderID = IncrementID()
        self._reqID = IncrementID()

    def orderID(self):
        return self._orderID.generate()

    def reqID(self):
        return self._reqID.generate()


def create_initiator(initiator_config, simulation_config):
    def create_subscriptions(instruments):
        result = Subscriptions()

        for instrument in instruments:
            subscription = Subscription(instrument['symbol'])
            result.add(subscription)

        return result

    settings = quickfix.SessionSettings(initiator_config)
    config = load_yaml(simulation_config)

    fix_version = create_fix_version(config)

    subscriptions = create_subscriptions(config['instruments'])

    logger = create_logger(config)
    subscribe_interval = config.get('subscribe_interval', 1)
    skip_snapshot_chance = config.get('skip_snapshot_chance', 0)
    application = Client(fix_version, logger, skip_snapshot_chance, subscribe_interval, subscriptions)
    storeFactory = quickfix.FileStoreFactory(settings)
    logFactory = quickfix.ScreenLogFactory(settings)
    initiator = quickfix.SocketInitiator(application, storeFactory, settings, logFactory)
    return initiator


class Snapshot(object):
    def __init__(self, symbol):
        self.symbol = symbol
        self.bid = []
        self.ask = []

    def getRandomQuote(self):
        is_bid = random.randrange(0, 2)
        if is_bid:
            quotes = self.bid
        else:
            quotes = self.ask

        quote = random.choice(quotes)
        return quote

    def addBid(self, quote):
        quote.side = Quote.SELL
        self.bid.append(quote)

    def addAsk(self, quote):
        quote.side = quote.BUY
        self.ask.append(quote)

    def __repr__(self):
        return "Snapshot %s\n    BID: %s\n    ASK: %s" % (self.symbol, self.bid, self.ask)


class Quote(object):
    SELL = '2'
    BUY = '1'

    def __init__(self):
        super(Quote, self).__init__()
        self.side = None
        self.symbol = None
        self.currency = None
        self.price = None
        self.size = None
        self.id = None

    def __repr__(self):
        return "(%s %s %s, %s)" % (str(self.id), self.side, str(self.price), str(self.size))


class Client(FixSimApplication):
    MKD_TOKEN = "MKD"

    def __init__(self, fixVersion, logger, skipSnapshotChance, subscribeInterval, subscriptions):
        super(Client, self).__init__(fixVersion, logger)

        self.skipSnapshotChance = skipSnapshotChance
        self.subscribeInterval = subscribeInterval
        self.subscriptions = subscriptions
        self.orderSession = None
        self.marketSession = None
        self.idGen = IDGenerator()
        self.loop = task.LoopingCall(self.subscribe)
        self.loop.start(self.subscribeInterval, True)

    def onCreate(self, sessionID):
        pass

    def onLogon(self, sessionID):
        sid = str(sessionID)
        # print "ON LOGON sid", sid
        if sid.find(self.MKD_TOKEN) != -1:
            self.marketSession = sessionID
            self.logger.info("FIXSIM-CLIENT MARKET SESSION %s", self.marketSession)
        else:
            self.orderSession = sessionID
            self.logger.info("FIXSIM-CLIENT ORDER SESSION %s", self.orderSession)

    def onLogout(self, sessionID):
        # print "ON LOGOUT"
        return

    def toAdmin(self, sessionID, message):
        # print "TO ADMIN", message
        return

    def fromAdmin(self, sessionID, message):
        # print "FROM ADMIN"
        return

    def toApp(self, sessionID, message):
        # print "TO APP"
        return

    def subscribe(self):
        if self.marketSession is None:
            self.logger.info("FIXSIM-CLIENT Market session is none, skip subscribing")
            return

        for subscription in self.subscriptions:
            message = self.fixVersion.MarketDataRequest()
            message.setField(quickfix.MDReqID(self.idGen.reqID()))
            message.setField(quickfix.SubscriptionRequestType(quickfix.SubscriptionRequestType_SNAPSHOT_PLUS_UPDATES))
            message.setField(quickfix.MDUpdateType(quickfix.MDUpdateType_FULL_REFRESH))
            message.setField(quickfix.MarketDepth(0))
            message.setField(quickfix.MDReqID(self.idGen.reqID()))

            relatedSym = self.fixVersion.MarketDataRequest.NoRelatedSym()
            relatedSym.setField(quickfix.Product(quickfix.Product_CURRENCY))
            relatedSym.setField(quickfix.SecurityType(quickfix.SecurityType_FOREIGN_EXCHANGE_CONTRACT))
            relatedSym.setField(quickfix.Symbol(subscription.symbol))
            message.addGroup(relatedSym)

            group = self.fixVersion.MarketDataRequest.NoMDEntryTypes()
            group.setField(quickfix.MDEntryType(quickfix.MDEntryType_BID))
            message.addGroup(group)
            group.setField(quickfix.MDEntryType(quickfix.MDEntryType_BID))
            message.addGroup(group)

            self.sendToTarget(message, self.marketSession)

    def onMarketDataSnapshotFullRefresh(self, message, sessionID):
        skip_chance = random.choice(range(1, 101))
        if self.skipSnapshotChance > skip_chance:
            self.logger.info("FIXSIM-CLIENT onMarketDataSnapshotFullRefresh skip making trade with random choice %d", skip_chance)
            return

        fix_symbol = quickfix.Symbol()
        message.getField(fix_symbol)
        symbol = fix_symbol.getValue()

        snapshot = Snapshot(symbol)

        group = self.fixVersion.MarketDataSnapshotFullRefresh.NoMDEntries()
        fix_no_entries = quickfix.NoMDEntries()
        message.getField(fix_no_entries)
        no_entries = fix_no_entries.getValue()

        for i in range(1, no_entries + 1):
            message.getGroup(i, group)
            price = quickfix.MDEntryPx()
            size = quickfix.MDEntrySize()
            currency = quickfix.Currency()
            quote_id = quickfix.QuoteEntryID()

            group.getField(quote_id)
            group.getField(currency)
            group.getField(price)
            group.getField(size)

            quote = Quote()
            quote.price = price.getValue()
            quote.size = size.getValue()
            quote.currency = currency.getValue()
            quote.id = quote_id.getValue()

            fix_entry_type = quickfix.MDEntryType()
            group.getField(fix_entry_type)
            entry_type = fix_entry_type.getValue()

            if entry_type == quickfix.MDEntryType_BID:
                snapshot.addBid(quote)
            elif entry_type == quickfix.MDEntryType_OFFER:
                snapshot.addAsk(quote)
            else:
                raise RuntimeError("Unknown entry type %s" % str(entry_type))

        self.makeOrder(snapshot)

    def makeOrder(self, snapshot):
        self.logger.info("FIXSIM-CLIENT Snapshot received %s", str(snapshot))
        quote = snapshot.getRandomQuote()

        self.logger.info("FIXSIM-CLIENT make order for quote %s", str(quote))
        order = self.fixVersion.NewOrderSingle()
        order.setField(quickfix.HandlInst(quickfix.HandlInst_AUTOMATED_EXECUTION_ORDER_PUBLIC_BROKER_INTERVENTION_OK))
        order.setField(quickfix.SecurityType(quickfix.SecurityType_FOREIGN_EXCHANGE_CONTRACT))

        order.setField(quickfix.OrdType(quickfix.OrdType_PREVIOUSLY_QUOTED))
        order.setField(quickfix.ClOrdID(self.idGen.orderID()))
        order.setField(quickfix.QuoteID(quote.id))

        order.setField(quickfix.SecurityDesc("SPOT"))
        order.setField(quickfix.Symbol(snapshot.symbol))
        order.setField(quickfix.Currency(quote.currency))
        order.setField(quickfix.Side(quote.side))

        order.setField(quickfix.OrderQty(quote.size))
        order.setField(quickfix.FutSettDate("SP"))
        order.setField(quickfix.Price(quote.price))
        order.setField(quickfix.TransactTime())
        order.setField(quickfix.TimeInForce(quickfix.TimeInForce_IMMEDIATE_OR_CANCEL))
        self.sendToTarget(order, self.orderSession)


    def onExecutionReport(self, message, sessionID):
        self.logger.info("FIXSIM-CLIENT EXECUTION REPORT  %s", str(message))

    def dispatchFromApp(self, msgType, message, beginString, sessionID):
        if msgType == '8':
            self.onExecutionReport(message, sessionID)
        elif msgType == 'W':
            self.onMarketDataSnapshotFullRefresh(message, sessionID)

