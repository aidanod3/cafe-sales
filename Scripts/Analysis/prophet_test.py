import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt

# tsv path
file_path = "../../Data/processedData/daily_revenue_per_store.tsv"

# read tsv into dataframe
df = pd.read_csv(file_path, sep='\t', names=['date_store', 'daily_revenue'])

# split composite key into 'date' and 'store_id'
df[['date', 'store_id']] = df['date_store'].str.split('|', expand=True)

# convert data types from string
df['daily_revenue'] = df['daily_revenue'].astype(float)
df['date'] = pd.to_datetime(df['date'], format='%m/%d/%y')
df = df.sort_values(['date', 'store_id']).reset_index(drop=True)

# remove date_store col
df = df[['date', 'store_id', 'daily_revenue']]

# rename cols
df = df.rename(columns={'date': 'ds', 'daily_revenue': 'y'})

# separate into training and testing data
last_index = df.index[-1]
training_data_max = round(last_index * 0.8) # 119292

training_data = df[df.index <= training_data_max] # (0 -> 434)
testing_data = df[df.index > training_data_max] # (435 -> 542)

# group training data by store_id
grouped = training_data.groupby('store_id')

# degroup into separate df's and remove store_id col
df_store3 = grouped.get_group('3')[['ds', 'y']]
df_store5 = grouped.get_group('5')[['ds', 'y']]
df_store8 = grouped.get_group('8')[['ds', 'y']]

# print(df_store3)
# print(df_store5)
# print(df_store8)

m = Prophet()
m.fit(df_store3)

future = m.make_future_dataframe(periods=36)
print(future)

forecast = m.predict(future)
print(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(36))

fig1 = m.plot(forecast)
plt.show()