import pandas as pd
from prophet import Prophet
from sklearn.metrics import mean_absolute_error, mean_squared_error
import matplotlib.pyplot as plt
import numpy as np

# load data
file_path = "../../Data/processedData/daily_revenue_per_store.tsv"
df = pd.read_csv(file_path, sep='\t', names=['date_store', 'daily_revenue'])
df[['ds', 'store_id']] = df['date_store'].str.split('|', expand=True)
df['y'] = df['daily_revenue'].astype(float)
df['ds'] = pd.to_datetime(df['ds'], format='%m/%d/%y')
df = df[['ds', 'store_id', 'y']].sort_values(['ds', 'store_id']).reset_index(drop=True)

# stores to forecast
stores = ["3", "5", "8"]

results = []  # store accuracy metrics here

for store_id in stores:
    print("=" * 60)
    print(f"Running Forecast for Store {store_id}")
    print("=" * 60)

    # subset
    store_df = df[df['store_id'] == store_id][['ds', 'y']]

    # split: last month = test
    cutoff_date = store_df['ds'].max() - pd.DateOffset(months=1)
    train_df = store_df[store_df['ds'] <= cutoff_date]
    test_df = store_df[store_df['ds'] > cutoff_date]

    # fit prophet
    m = Prophet()
    m.fit(train_df)

    # future dataframe (same length as test)
    future = m.make_future_dataframe(periods=len(test_df))
    forecast = m.predict(future)

    # join predicted with actual
    forecast_test = forecast.set_index('ds').join(test_df.set_index('ds'), how='inner')
    y_true = forecast_test['y'].values
    y_pred = forecast_test['yhat'].values

    # metrics
    mae = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    mape = np.mean(np.abs((y_true - y_pred) / y_true)) * 100

    results.append({
        "store_id": store_id,
        "MAE": mae,
        "RMSE": rmse,
        "MAPE": mape
    })

    # print results
    print(f"MAE:  {mae:.2f}")
    print(f"RMSE: {rmse:.2f}")
    print(f"MAPE: {mape:.2f}%")

    # plot
    fig = m.plot(forecast)
    plt.scatter(test_df['ds'], test_df['y'], color='red', label='Actual')
    plt.title(f'Store {store_id} Forecast vs Actual')
    plt.legend()
    plt.tight_layout()
    plt.show()

# summary table at end
print("\nforecast summary")
summary_df = pd.DataFrame(results)
print(summary_df)
