import pandas as pd

basic_mr = pd.read_csv('basic_trend_following.csv')
vol_mr = pd.read_csv('volatility_adjusted_trend_following.csv')

import matplotlib.pyplot as plt

basic_mr['BasicTrendFollowingPnl'].plot(x='Date', color='b', lw=1., legend=True)
vol_mr['VolatilityAdjustedTrendFollowingPnl'].plot(x='Date', color='g', lw=1., legend=True)
plt.show()
