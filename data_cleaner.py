import os
import pandas as pd
from datetime import datetime

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
df = (df.loc['2010-09-07 00:00:01' : '2010-12-16 23:59:59'])
#print(df)

# Creates second dataframe to drop duplicates and header each day
df2 = df.drop_duplicates(subset=['Date'])
#df2.reset_index(drop=True, inplace=True)
#df2.set_index(['Date'])
print(df2)


df2.between_time('17:15:00' , '23:59:59')


df3 = df.between_time('17:14:00' , '17:14:59')
df3.loc['Price*Vol'] = ((df3["Price"] * df3['Volume']))
df3 = df3.groupby(['Date']).sum()

df3['VWAP'] = (df3['Price*Vol'] / df3['Volume'])
print(df3)



#df3['Traded after 1715'] = 




