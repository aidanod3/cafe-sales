from dash import Dash, dash_table, dcc
import pandas as pd
import plotly.express as px

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

monthly = (
    df.groupby([pd.to_datetime(df['date']).dt.month, 'store_id'])['daily_revenue']
    .sum()
    .reset_index()
    .rename(columns={'date': 'month', 'daily_revenue': 'revenue'})
)

fig = px.line(
    monthly,
    x='month',
    y='revenue',
    color='store_id',
    markers=True,
    title='Monthly Revenue per Location'
)

app = Dash()

app.layout = [

    # display all data
    dash_table.DataTable(data=df.to_dict('records'), page_size=10),

    dcc.Graph(figure=fig)
]

if __name__ == '__main__':
    app.run(debug=True)
