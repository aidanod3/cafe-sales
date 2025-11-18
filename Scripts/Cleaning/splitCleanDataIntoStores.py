import pandas as pd
from pathlib import Path

root = Path(__file__).resolve().parents[2]

cleanedDataPath = root / "Data" / "cleanedData" / "cleaned_coffee_shop_sales.csv"
df = pd.read_csv(cleanedDataPath)

outputPath = root / "Data" / "cleanedData" / "perStore"

for storeId, Stores in df.groupby("store_id"):
    fileName = f"Store_{storeId}.csv"
    filePath = outputPath / fileName

    Stores.to_csv(filePath, index=False)
