from dash import Dash, html, dash_table, dcc, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

# bootstrap theme
app = Dash(__name__, external_stylesheets=[dbc.themes.ZEPHYR])
server = app.server

# load and clean data
file_path = "Data/processedData/daily_revenue_per_store.tsv"

df = pd.read_csv(file_path, sep='\t', names=['date_store', 'daily_revenue'])

df[['date', 'store_id']] = df['date_store'].str.split('|', expand=True)
df['daily_revenue'] = df['daily_revenue'].astype(float)
df['date'] = pd.to_datetime(df['date'], format='%m/%d/%y')

df = df[['date', 'store_id', 'daily_revenue']].sort_values(['date','store_id'])

# convert store_id to string
df['store_id'] = df['store_id'].astype(str)

# monthly data
monthly = (
    df.groupby([df['date'].dt.to_period('M').astype(str), 'store_id'])['daily_revenue']
    .sum()
    .reset_index()
    .rename(columns={'date': 'month', 'daily_revenue': 'revenue'})
)

# weekly data
weekly = (
    df.groupby([df['date'].dt.isocalendar().week, 'store_id'])['daily_revenue']
    .sum()
    .reset_index()
    .rename(columns={'date': 'week', 'daily_revenue': 'revenue'})
)

# hourly data
hourly_file = "Data/processedData/hourly_revenue_per_store.tsv"
hourly_df = pd.read_csv(hourly_file, sep='\t', names=['store_datetime', 'revenue'])
# split into store_id + datetime
hourly_df[['store_id', 'datetime']] = hourly_df['store_datetime'].str.split('|', expand=True)
hourly_df['store_id'] = hourly_df['store_id'].astype(str)
# convert datetime correctly
hourly_df['datetime'] = pd.to_datetime(hourly_df['datetime'], format="%Y-%m-%d %H:%M:%S")
# extract date and hour
hourly_df['date'] = hourly_df['datetime'].dt.date
hourly_df['hour'] = hourly_df['datetime'].dt.hour
hourly_df = hourly_df[['date', 'store_id', 'hour', 'revenue']]
hourly_df = hourly_df.sort_values(['date', 'store_id', 'hour'])

def make_fig(timeframe, selected_stores):
    if timeframe == "Daily":
        filtered = df[df["store_id"].isin(selected_stores)]
        fig = px.line(filtered, x="date", y="daily_revenue", color="store_id",
                      markers=True, title="Daily Revenue per Store")

    elif timeframe == "Weekly":
        filtered = weekly[weekly["store_id"].isin(selected_stores)]
        fig = px.line(filtered, x="week", y="revenue", color="store_id",
                      markers=True, title="Weekly Revenue per Store")

    else:  # monthly
        filtered = monthly[monthly["store_id"].isin(selected_stores)]
        fig = px.line(filtered, x="month", y="revenue", color="store_id",
                      markers=True, title="Monthly Revenue per Store")

    fig.update_layout(template="plotly_white")
    return fig

# monthly item sales per store
item_file = "Data/processedData/monthlySalesPerItemPerStore.tsv"
# product lookup table (convert item_id to product_detail)
lookup_file = "Data/processedData/lookupTableDetailed.csv"

# load lookup table
lookup_table = pd.read_csv(lookup_file)
lookup_table["product_id"] = lookup_table["product_id"].astype(int)

# load item sales
item_df = pd.read_csv(
    item_file,
    sep="\t",
    names=["store_item_month", "revenue"]
)

# split
item_df[["store_id", "product_id", "month"]] = (
    item_df["store_item_month"].str.split("|", expand=True)
)

item_df["store_id"] = item_df["store_id"].astype(int)
item_df["product_id"] = item_df["product_id"].astype(int)
item_df["revenue"] = item_df["revenue"].astype(float)

#merge on product_id
item_df = item_df.merge(lookup_table, on="product_id", how="left")






# layout
app.layout = dbc.Container([

    html.H2("Coffee Shop Dashboard", className="my-4"),

    # revenue trends card (daily/weekly/monthly)
    dbc.Card([
        dbc.CardHeader("Revenue Trends"),

        dbc.CardBody([

            # store selector
            dbc.Row([
                dbc.Col([
                    html.Label("Select Store(s):"),
                    dcc.Dropdown(
                        id="store-dropdown",
                        options=[{"label": f"Store {s}", "value": str(s)} for s in [3, 5, 8]],
                        value=["3", "5", "8"],
                        multi=True,
                        placeholder="Select store(s)"
                    )
                ], width=4)
            ], className="mb-3"),

            dbc.Tabs(
                [
                    dbc.Tab(label="Daily", tab_id="Daily"),
                    dbc.Tab(label="Weekly", tab_id="Weekly"),
                    dbc.Tab(label="Monthly", tab_id="Monthly"),
                ],
                id="revenue-tabs",
                active_tab="Monthly",
                className="mb-4"
            ),

            dcc.Graph(id="revenue-graph")
        ])
    ], className="shadow mb-4"),

    # hourly revenue card
        dbc.Card([
            dbc.CardHeader("Hourly Revenue"),
            dbc.CardBody([
                dbc.Row([
                    dbc.Col([
                        dcc.Dropdown(
                            id="hourly-store",
                            options=[{"label": f"Store {s}", "value": str(s)} for s in [3, 5, 8]],
                            value="3",
                            clearable=False
                        )
                    ], md=3),

                    dbc.Col([
                        dcc.DatePickerSingle(
                            id="hourly-date",
                            date=df['date'].min(),  # default earliest date
                            display_format="YYYY-MM-DD"
                        )
                    ], md=3)
                ], className="mb-3"),

                dcc.Graph(id="hourly-graph")
            ])
        ], className="shadow mb-4"),

    # monthly item sales card
    dbc.Card([
        dbc.CardHeader("Monthly Item Sales per Store"),
        dbc.CardBody([

            dbc.Row([
                dbc.Col([
                    html.Label("Select Month:"),
                    dcc.Dropdown(
                        id="item-month",
                        options=[{"label": m, "value": m} for m in sorted(item_df["month"].unique())],
                        value=sorted(item_df["month"].unique())[0],
                        clearable=False
                    )
                ], md=3),

                dbc.Col([
                    html.Label("Select Store:"),
                    dcc.Dropdown(
                        id="item-store",
                        options=[{"label": f"Store {s}", "value": s} for s in sorted(item_df["store_id"].unique())],
                        value=sorted(item_df["store_id"].unique())[0],
                        clearable=False
                    )
                ], md=3),

                dbc.Col([
                    html.Label("Select Category:"),
                    dcc.Dropdown(
                        id="item-category",
                        options=([{"label": "All Categories", "value": "ALL"}] +
                                 [{"label": c, "value": c} for c in sorted(item_df["product_category"].unique())]),
                        value="ALL",
                        clearable=False
                    )
                ], md=3),
            ], className="mb-3"),

            dcc.Graph(id="item-sales-graph")
        ])
    ], className="shadow mb-4"),

], fluid=True)

# callback: update graph when tab or store changes
@app.callback(
    Output("revenue-graph", "figure"),
    Input("revenue-tabs", "active_tab"),
    Input("store-dropdown", "value")
)
def update_graph(active_tab, selected_stores):
    return make_fig(active_tab, selected_stores)

# hourly chart callback
@app.callback(
    Output("hourly-graph", "figure"),
    Input("hourly-store", "value"),
    Input("hourly-date", "date")
)
def update_hourly_graph(store_id, selected_date):

    selected_date = pd.to_datetime(selected_date).date()

    filtered = hourly_df[
        (hourly_df["store_id"] == store_id) &
        (hourly_df["date"] == selected_date)
    ]

    fig = px.bar(
        filtered,
        x="hour",
        y="revenue",
        title=f"Hourly Revenue – Store {store_id} on {selected_date}",
        labels={"hour": "Hour of Day", "revenue": "Revenue"}
    )

    fig.update_layout(template="plotly_white")
    return fig

@app.callback(
    Output("item-sales-graph", "figure"),
    Input("item-month", "value"),
    Input("item-store", "value"),
    Input("item-category", "value")
)
def update_item_sales(selected_month, store_id, selected_category):

    # base filters
    filtered = item_df[
        (item_df["month"] == selected_month) &
        (item_df["store_id"] == int(store_id))
    ]

    # apply category filtering unless ALL is selected
    if selected_category != "ALL":
        filtered = filtered[filtered["product_category"] == selected_category]

    if filtered.empty:
        fig = px.bar(title="No data available for this selection.")
        fig.update_layout(template="plotly_white")
        return fig

    filtered = filtered.sort_values("revenue", ascending=False)

    fig = px.bar(
        filtered,
        x="product_detail",
        y="revenue",
        color="product_category",
        text_auto=".2s",
        title=(
            f"All Categories – Store {store_id} – {selected_month}"
            if selected_category == "ALL"
            else f"{selected_category} – Store {store_id} – {selected_month}"
        ),
        labels={
            "product_detail": "Product",
            "revenue": "Revenue",
            "product_category": "Category"
        }
    )

    fig.update_layout(
        template="plotly_white",
        xaxis_tickangle=45,
        margin=dict(l=40, r=20, t=60, b=120)
    )
    return fig


if __name__ == '__main__':
    app.run(debug=True)
