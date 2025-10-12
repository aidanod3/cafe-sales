from dash import Dash, dash_table, dcc
import pandas as pd
import os
import plotly.express as px

pd.set_option('future.no_silent_downcasting', True)

if os.path.exists("coffee_shop_sales.pkl"):
    # load cached dataframe
    df = pd.read_pickle("coffee_shop_sales.pkl")
else:
    # read from csv
    df = pd.read_excel("coffee_shop_sales.xlsx")
    df.to_pickle("coffee_shop_sales.pkl")

# create timestamp column
df['timestamp'] = df['transaction_date'].astype(str) + ' ' + df['transaction_time'].astype(str)
# make timestamp column datetime type
df['timestamp'] = pd.to_datetime(df['timestamp'], format='%Y-%m-%d %H:%M:%S')

# create total column (transaction_qty * unit_price)
df['total'] = df['transaction_qty'] * df['unit_price']

# --- queries ---

# print number of sales for each day (all locations)
# print("total num sales: \n")
# print(df.groupby(['transaction_date'])['transaction_id'].count())

# print total revenue for each day (all locations)
# print("total revenue: \n")
# print(df.groupby(['transaction_date'])['total'].sum())

# print number of sales for each day (per location)
# print("total num sales per location: \n")
# print(df.groupby(['transaction_date', 'store_location'])['transaction_id'].count())

# print total revenue for each day (per location)
# print("total revenue per location: \n")
# print(df.groupby(['transaction_date', 'store_location'])['total'].sum())

# print monthly revenue (all locations)
# print("monthly revenue: \n")
# print(df.groupby([pd.to_datetime(df['transaction_date']).dt.month])['total'].sum())

# print monthly revenue (per location)
# print("monthly revenue per location: \n")
# print(df.groupby([pd.to_datetime(df['transaction_date']).dt.month, 'store_location'])['total'].sum())

monthly = (
    df.groupby([pd.to_datetime(df['transaction_date']).dt.month, 'store_location'])['total']
    .sum()
    .reset_index()
    .rename(columns={'transaction_date': 'month', 'total': 'revenue'})
)

fig = px.line(
    monthly,
    x='month',
    y='revenue',
    color='store_location',
    markers=True,
    title='Monthly Revenue per Location'
)

print(monthly)
app = Dash()


app.layout = [

    # display all data
    dash_table.DataTable(data=df.to_dict('records'), page_size=10),

    dcc.Graph(figure=fig)
]

if __name__ == '__main__':
    app.run(debug=True)

