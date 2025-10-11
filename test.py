from dash import Dash, dash_table, dcc
import plotly.express as px
import pandas as pd
import os
import openpyxl

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
