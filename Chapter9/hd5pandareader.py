#!/bin/python3
import pandas as pd
import numpy as np
from pandas_datareader import data
import matplotlib.pyplot as plt
import h5py

def load_financial_data(start_date, end_date,output_file):
    try:
        df = pd.read_pickle(output_file)
        print('File data found...reading GOOG data')
    except FileNotFoundError:
        print('File not found...downloading the GOOG data')
        df = data.DataReader('GOOG', 'yahoo', start_date, end_date)
        df.to_pickle(output_file)
    return df

goog_data=load_financial_data(start_date='2001-01-01',
                    end_date = '2018-01-01',
                    output_file='goog_data.pkl')


goog_data.to_hdf('goog_data.h5','goog_data',mode='w',format='table',data_columns=True)

h = h5py.File('goog_data.h5')

print(h['goog_data']['table'])
print(h['goog_data']['table'][:])
for attributes in h['goog_data']['table'].attrs.items():
    print(attributes)
