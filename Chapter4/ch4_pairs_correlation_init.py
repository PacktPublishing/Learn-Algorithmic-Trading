import pandas as pd
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import coint
import seaborn


from pandas_datareader import data

symbolsIds = ['SPY','AAPL','ADBE','LUV','MSFT',\
              'SKYW','QCOM',
                 'HPQ','JNPR','AMD','IBM']

def load_financial_data(symbols, start_date, end_date,output_file):
    try:
        df = pd.read_pickle(output_file)
        print('File data found...reading symbols data')
    except FileNotFoundError:
        print('File not found...downloading the symbols data')
        df = data.DataReader(symbols, 'yahoo', start_date, end_date)
        df.to_pickle(output_file)
    return df

data=load_financial_data(symbolsIds,start_date='2001-01-01',
                    end_date = '2018-01-01',
                    output_file='multi_data_large.pkl')




def find_cointegrated_pairs(data):
    n = data.shape[1]
    pvalue_matrix = np.ones((n, n))
    keys = data.keys()
    pairs = []
    for i in range(n):
        for j in range(i+1, n):
            result = coint(data[keys[i]], data[keys[j]])
            pvalue_matrix[i, j] = result[1]
            if result[1] < 0.02:
                pairs.append((keys[i], keys[j]))
    return pvalue_matrix, pairs


pvalues, pairs = find_cointegrated_pairs(data['Adj Close'])
print(pairs)

seaborn.heatmap(pvalues, xticklabels=symbolsIds,
                yticklabels=symbolsIds, cmap='RdYlGn_r',
                mask = (pvalues >= 0.98))
plt.show()
print (pairs)


print(data.head(3))


