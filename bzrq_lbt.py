# !/bin/python3
import pandas as pd
import numpy as np

# from pandas_datareader import data
import yfinance as yf
import matplotlib.pyplot as plt
import h5py
from collections import deque
from box import Box


def load_financial_data(start_date, end_date, output_file):
    try:
        df = pd.read_pickle(output_file)
        print("File data found...reading GOOG data")
    except FileNotFoundError:
        print("File not found...downloading the GOOG data")
        # df = data.DataReader('GOOG', 'yahoo', start_date, end_date)
        df = yf.download("GOOG", start_date, end_date)
        df.to_pickle(output_file)

    return df


goog_data = load_financial_data(start_date="2001-01-01", end_date="2018-01-01", output_file="goog_data.pkl")
goog_data.to_hdf("goog_data.h5", "goog_data", mode="w", format="table", data_columns=True)
goog_data_from_h5_file = h5py.File("goog_data.h5")


print(goog_data_from_h5_file["goog_data"]["table"])
print(goog_data_from_h5_file["goog_data"]["table"][:])
for attributes in goog_data_from_h5_file["goog_data"]["table"].attrs.items():
    print(attributes)


# for each price update:
#     create_metric_out_of_prices()
#     buy_sell_or_hold_something()
#     next_price()


def average(lst):
    return sum(lst) / len(lst)


LBT__self = Box({})


def LBT____init__():
    LBT__self.small_window = deque()
    LBT__self.large_window = deque()
    LBT__self.list_position = []
    LBT__self.list_cash = []
    LBT__self.list_holdings = []
    LBT__self.list_total = []

    LBT__self.long_signal = False
    LBT__self.position = 0
    LBT__self.cash = 10000
    LBT__self.total = 0
    LBT__self.holdings = 0


def LBT__create_metrics_out_of_prices(price_update):
    LBT__self.small_window.append(price_update["price"])
    LBT__self.large_window.append(price_update["price"])

    if len(LBT__self.small_window) > 50:
        LBT__self.small_window.popleft()

    if len(LBT__self.large_window) > 100:
        LBT__self.large_window.popleft()

    if len(LBT__self.small_window) == 50:
        if average(LBT__self.small_window) > average(LBT__self.large_window):
            LBT__self.long_signal = True
        else:
            LBT__self.long_signal = False

        return True

    return False


def LBT_buy_sell_or_hold_something(price_update):
    if LBT__self.long_signal and LBT__self.position <= 0:
        print(
            str(price_update["date"])
            + " send buy order for 10 shares price="
            + str(price_update["price"])
        )
        LBT__self.position += 10
        LBT__self.cash -= 10 * price_update["price"]
    elif LBT__self.position > 0 and not LBT__self.long_signal:
        print(
            str(price_update["date"])
            + " send sell order for 10 shares price="
            + str(price_update["price"])
        )
        LBT__self.position -= 10
        LBT__self.cash -= -10 * price_update["price"]

    LBT__self.holdings = LBT__self.position * price_update["price"]
    LBT__self.total = LBT__self.holdings + LBT__self.cash
    print(
        "%s total=%d, holding=%d, cash=%d"
        % (
            str(price_update["date"]),
            LBT__self.total,
            LBT__self.holdings,
            LBT__self.cash,
        )
    )

    LBT__self.list_position.append(LBT__self.position)
    LBT__self.list_cash.append(LBT__self.cash)
    LBT__self.list_holdings.append(LBT__self.holdings)
    LBT__self.list_total.append(LBT__self.holdings + LBT__self.cash)


LBT____init__()

for line in zip(goog_data.index, goog_data["Adj Close"]):
    date = line[0]
    price = line[1]
    price_information = {"date": date, "price": float(price)}
    is_tradable = LBT__create_metrics_out_of_prices(price_information)
    if is_tradable:
        LBT_buy_sell_or_hold_something(price_information)


plt.plot(LBT__self.list_total, label="Holdings+Cash using Naive BackTester")
plt.legend()
plt.show()
