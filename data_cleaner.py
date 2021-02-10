import os
import pandas as pd
import numpy as np

path = os.getcwd()
print(path)

# Open file and place headers
df = pd.read_csv('BNZ10_clean.csv', header = None)
df.columns = ["Timestamp", "Price", "Volume", "Ref Timestamp"]

# Convert timestamp to YYYY-MM-DD and slices requested dates
df['Timestamp'] = pd.to_datetime(df['Timestamp'], unit ='ms')
date_only = ((df['Timestamp']).dt.date)
df['Date'] = date_only
df = df.set_index(['Timestamp'])
df = (df.loc['2010-09-07 00:00:01' : '2010-12-06 23:59:59'])

# Creates date headers and first price traded each day
df2 = df.drop_duplicates(subset=['Date'])

# Calculates the VMAP between 1714 and 1715
df3 = df.between_time('17:14:00' , '17:14:59')
df3['PriceVol'] = (df3.Price * df3.Volume)
df3 = df3.groupby(['Date']).sum()
df3['VWAP'] = (df3.PriceVol / df3.Volume)

# Flags and seperates trades that occur after 1715 with identical price to first traded price
df4 = df.between_time('17:15:00' , '23:59:59')
df_combined = pd.merge(df2, df4, on=['Date'])
df_combined['Flag'] = np.where(df_combined.Price_x == df_combined.Price_y, 'True', 'False')
df_boolean = df_combined[df_combined['Flag'] == 'True']
df_boolean = df_boolean.drop_duplicates(subset=['Date'])

# Cleans up and merges dataframes so requested data remains
df3 = df3.drop(['Price', 'Volume', 'PriceVol'], axis=1)
df2 = df2.drop(['Ref Timestamp', 'Volume'], axis=1)
df_results = pd.merge(df3, df2, on=['Date'])
df_boolean = df_boolean[df_boolean.columns.difference(['Price_x', 'Volume_x', 'Ref Timestamp_x', 'Volume_y', 'Price_y'])]
df_results = df_results.merge(df_boolean, how = 'left', left_on=['Date'], right_on=['Date'])

# Cleans up final dataframe with all requested data
df_results = df_results.rename(columns={"Price": "First Trading Price", "Ref Timestamp_y": "Time"})
df_results = df_results[['Date', 'First Trading Price' , 'VWAP', 'Flag', 'Time']]
df_results = df_results.replace(np.nan, '', regex=True)
df_results['Time'] = (pd.to_datetime(df_results['Time'])).dt.time
df_results['Time'] = df_results['Time'].fillna('')

print(df_results)

df_results.to_csv('Results.csv', index=False)
