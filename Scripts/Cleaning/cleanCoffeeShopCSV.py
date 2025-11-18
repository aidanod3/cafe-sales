import pandas as pd
from pathlib import Path

root = Path(__file__).resolve().parents[2]

originalDataPath = root / "Data" / "rawData" / "coffee_shop_sales.csv"
originalData = pd.read_csv(originalDataPath)

originalData["dateAndTimeForTransaction"] = pd.to_datetime(
    originalData["transaction_date"] + " " + originalData["transaction_time"],
    format="%m/%d/%y %H:%M:%S"
)

originalData = originalData.drop(columns="transaction_date")
originalData = originalData.drop(columns="transaction_time")

originalData["transaction_id"] = originalData["transaction_id"].astype(int)
originalData["transaction_qty"] = originalData["transaction_qty"].astype(int)
originalData["store_id"] = originalData["store_id"].astype(int)
originalData["product_id"] = originalData["product_id"].astype(int)
originalData["unit_price"] = originalData["unit_price"].astype(float)

originalData = originalData.drop(columns="product_detail")

outputCSV = root / "Data" / "cleanedData" / "cleaned_coffee_shop_sales.csv"

originalData.to_csv(outputCSV, index=False)

